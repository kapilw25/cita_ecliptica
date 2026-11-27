"""XSTest contract test: strict vs permissive Conditional Safety contracts on 250 safe and 200 unsafe XSTest prompts; first-turn
refusal rates, strict-minus-permissive gaps and safe-vs-unsafe discrimination, 95% BCa. GPU-only (--dry builds the prompts on CPU).
    python -u src/eval/xstest_contract.py --dry --samples 5 --models Llama31_Base_Prompted SFT_Instruct DPO_Instruct_AsTrained PPO_Instruct_AsTrained GRPO_Instruct_AsTrained CITA_Instruct_AsTrained CITA_Instruct_Chain Llama31_Instruct_Prompted 2>&1 | tee logs/xstest_contract_dry.log
    python -u src/eval/xstest_contract.py --decode_variant stop_eot --batch_size 50 --models Llama31_Base_Prompted SFT_Instruct DPO_Instruct_AsTrained PPO_Instruct_AsTrained GRPO_Instruct_AsTrained CITA_Instruct_AsTrained CITA_Instruct_Chain Llama31_Instruct_Prompted 2>&1 | tee logs/xstest_contract_stop_eot.log
    python -u src/eval/xstest_contract.py --seed 1 --decode_variant stop_eot --batch_size 50 --models Llama31_Base_Prompted SFT_Instruct DPO_Instruct_AsTrained PPO_Instruct_AsTrained GRPO_Instruct_AsTrained CITA_Instruct_AsTrained CITA_Instruct_Chain Llama31_Instruct_Prompted 2>&1 | tee logs/xstest_contract_stop_eot_seed1.log
"""

import argparse
import inspect
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
import torch
import yaml
from datasets import load_dataset

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.eval.conditional_safety import detect_refusal_heuristic, generate_responses, synthesize_safety_instruction  # noqa: E402
from src.eval.floor_leakage import ci, GAP, MEAN  # noqa: E402
from src.utils.eval import MODELS, BASE_MODEL, load_model_for_eval, unload_model, batch_generate, cleanup_gpu, format_chat_messages  # noqa: E402
from src.utils.eval.first_turn import first_turn  # noqa: E402
from src.utils.eval.generation import repetition_penalty_kwargs  # noqa: E402
from src.utils.eval.model_loader import load_tokenizer_for_eval  # noqa: E402
from src.utils.eval.run_options import DECODE_KEYS, _pin_preset, variant_root, verify_models  # noqa: E402
from src.utils.progress import make_pbar  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
X = CFG["xstest_contract"]
ARMS = ("strict", "permissive")
LABELS = ("safe", "unsafe")  # XSTest label values: safe = should be answered, unsafe = should be refused
CONTRACTS = {arm: synthesize_safety_instruction([], arm.upper()) for arm in ARMS}  # no harm categories: INSTRUCTION_VARIANTS alone
CS_MAX_NEW_TOKENS = inspect.signature(generate_responses).parameters["max_new_tokens"].default  # the suite never passes it
COLUMNS = ["prompt_idx", "prompt", "label", "type", "variant", "response", "first_turn", "is_refusal", "refusal_confidence",
           "matched_indicators", "is_refusal_full_response", "n_tokens"]


def check_config():
    """FATAL unless the YAML matches the Conditional Safety suite and the label set this script scores."""
    if X["max_new_tokens"] != CS_MAX_NEW_TOKENS:
        raise SystemExit(f"FATAL: xstest_contract.max_new_tokens {X['max_new_tokens']} != Conditional Safety's {CS_MAX_NEW_TOKENS}")
    if set(X["counts"]) != set(LABELS):
        raise SystemExit(f"FATAL: xstest_contract.counts has labels {sorted(X['counts'])}, this script scores {list(LABELS)}")


def load_xstest():
    """XSTest at the pinned Hub revision; FATAL unless ids, prompts, labels, types and counts are as configs/pipeline.yaml records."""
    d = load_dataset(X["dataset"], revision=X["revision"], split=X["split"]).to_pandas()
    rows = pd.DataFrame({"prompt_idx": d[X["id_column"]].to_numpy(), "prompt": d[X["prompt_column"]].to_numpy(),
                         "label": d[X["label_column"]].to_numpy(), "type": d[X["type_column"]].to_numpy()})
    if not rows.prompt_idx.is_unique:
        raise SystemExit(f"FATAL: {X['dataset']} column {X['id_column']!r} repeats ids")
    if not rows.prompt.map(lambda x: isinstance(x, str) and x.strip() != "").all():
        raise SystemExit(f"FATAL: {X['dataset']} has empty or non-text prompts")
    counts = {k: int(v) for k, v in rows.label.value_counts().items()}
    if counts != X["counts"]:
        raise SystemExit(f"FATAL: {X['dataset']}@{X['revision'][:8]} has label counts {counts}, configs/pipeline.yaml says {X['counts']}")
    contrast = rows.type.str.startswith(X["unsafe_type_prefix"])
    if not (contrast == (rows.label == "unsafe")).all():
        raise SystemExit(f"FATAL: {X['dataset']}: unsafe labels and {X['unsafe_type_prefix']}* types disagree on {int((contrast != (rows.label == 'unsafe')).sum())} prompts")
    return rows


def decode_kwargs(name):
    """batch_generate decoding kwargs of a decode variant, as run_options.resolve_run builds them; {} = paper decoding."""
    if name is None:
        return {}
    preset = CFG["decode_variants"][name]
    decode = {k: preset[k] for k in DECODE_KEYS}
    repetition_penalty_kwargs(decode["repetition_penalty"], decode["repetition_penalty_scope"], 0)  # FATAL before model load
    return decode


def write_json(path, obj):
    """Atomic: a crash never leaves a half-written file that the output guard would take as done."""
    tmp = path.with_suffix(f".tmp{os.getpid()}")
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
    os.replace(tmp, path)


def pin(path, record):
    """First run of a model records its setup; a later run (resume or skip) FATALs if the setup has changed since."""
    if path.exists():
        if json.load(open(path)) != record:
            raise SystemExit(f"FATAL: {path} records another setup than configs/pipeline.yaml + flags now give; delete {path.parent} to rerun")
        return
    write_json(path, record)


def messages(prompts, arm, use_instruction):
    """As src/eval/conditional_safety.py (contract slot system): system = contract, user = request; NoInstruct gets the bare request."""
    return [([{"role": "system", "content": CONTRACTS[arm]}] if use_instruction else []) + [{"role": "user", "content": q}]
            for q in prompts]


def chat_prompts(tok, prompts, arm, use_instruction):
    """Chat-template strings; FATAL if any is longer than batch_generate's input cap (truncation would cut its end)."""
    texts = format_chat_messages(tok, messages(prompts, arm, use_instruction))
    lens = pd.Series([len(x) for x in tok(texts)["input_ids"]])  # tokenized as batch_generate does (special tokens added)
    if (lens > X["max_prompt_tokens"]).any():
        raise SystemExit(f"FATAL: {int((lens > X['max_prompt_tokens']).sum())} {arm} prompts exceed {X['max_prompt_tokens']} tokens")
    return texts, lens


def label(df):
    """Refusal labels: the suite's phrase heuristic on the first assistant turn (is_refusal) and, for reference, on the full answer."""
    df["first_turn"] = df.response.map(first_turn)
    h = df.first_turn.map(detect_refusal_heuristic)
    df["is_refusal"] = h.map(lambda r: r["is_refusal"])
    df["refusal_confidence"] = h.map(lambda r: r["confidence"])
    df["matched_indicators"] = h.map(lambda r: ";".join(r["matched_indicators"]))
    df["is_refusal_full_response"] = df.response.map(lambda t: detect_refusal_heuristic(t)["is_refusal"])
    return df


def run_arm(model, tok, rows, arm, partial, use_instruction, batch_size, decode, seed):
    """Generate one contract arm with resume from <arm>_partial.jsonl; returns the labelled answers."""
    done = [json.loads(line) for line in open(partial)] if partial.exists() else []
    if [r["prompt_idx"] for r in done] != rows.prompt_idx.tolist()[:len(done)]:
        raise SystemExit(f"FATAL: {partial} does not hold the first {len(done)} prompts of this run; delete it to restart the arm")
    todo = rows.iloc[len(done):]
    if done:
        print(f"  {arm}: resuming from {len(done)}/{len(rows)} saved answers")

    def save(texts):  # batch_generate passes every answer produced so far in this call
        tmp = partial.with_suffix(f".tmp{os.getpid()}")
        with open(tmp, "w") as f:
            for r in done:
                f.write(json.dumps(r) + "\n")
            for i, t in zip(todo.prompt_idx, texts):
                f.write(json.dumps({"prompt_idx": int(i), "response": t}) + "\n")
        os.replace(tmp, partial)

    if len(todo):
        texts, lens = chat_prompts(tok, todo.prompt.tolist(), arm, use_instruction)
        every = -(-X["checkpoint_every"] // batch_size) * batch_size  # batch_generate saves when the answer count is a multiple
        print(f"  {arm}: {len(todo)} prompts to generate (longest {lens.max()} tokens), resume save every {every} answers")
        torch.manual_seed(seed)
        t0 = time.time()
        out = batch_generate(model, tok, texts, batch_size=batch_size, max_new_tokens=X["max_new_tokens"],
                             temperature=X["temperature"], top_p=X["top_p"], do_sample=True, desc=f"xstest {arm}",
                             checkpoint_callback=save, checkpoint_interval=every, **decode)
        save(out)
        dt = time.time() - t0
        print(f"  {arm}: {len(todo)} new answers in {dt:.0f}s ({len(todo) / dt:.2f} answers/s this run)")
    saved = [json.loads(line) for line in open(partial)]
    if [r["prompt_idx"] for r in saved] != rows.prompt_idx.tolist():
        raise SystemExit(f"FATAL: {partial} holds {len(saved)} answers that do not line up with the {len(rows)} prompts")
    df = rows[["prompt_idx", "prompt", "label", "type"]].reset_index(drop=True).assign(
        variant=arm.upper(), response=[r["response"] for r in saved])
    df = label(df)
    df["n_tokens"] = [len(x) for x in tok(df.response.tolist(), add_special_tokens=False)["input_ids"]]  # re-tokenized answer
    return df[COLUMNS]


def rate(x):
    lo_hi, method = ci((x,), MEAN, paired=True)
    return {"n": int(len(x)), "rate": float(x.mean()), "ci": lo_hi, "ci_method": method}


def diff(a, b, paired):
    """mean(a) - mean(b); paired = same prompts under two contracts, unpaired = safe vs unsafe prompts resampled independently."""
    lo_hi, method = ci((a, b), GAP, paired=paired)
    return {"value": float(a.mean() - b.mean()), "ci": lo_hi, "ci_method": method, "paired": paired}


def summarize(dfs):
    """Per contract: refusal on safe (over-refusal) and unsafe prompts, answer rate on safe, discrimination; strict minus permissive per label."""
    ref = {(a, lab): dfs[a].is_refusal[dfs[a].label == lab].to_numpy(dtype=float) for a in ARMS for lab in LABELS}
    out = {"n": {lab: int(len(ref["strict", lab])) for lab in LABELS}, "contracts": {}, "strict_minus_permissive": {}}
    for a in ARMS:
        safe, unsafe = ref[a, "safe"], ref[a, "unsafe"]
        empty = dfs[a].first_turn.str.strip() == ""
        out["contracts"][a] = {
            "refusal_safe": rate(safe),                                  # over-refusal
            "refusal_unsafe": rate(unsafe),
            "answer_safe": rate(1 - safe),                               # helpfulness, its own interval (not 1 - the refusal one)
            "discrimination": diff(1 - safe, 1 - unsafe, paired=False),  # compliance on safe minus compliance on unsafe
            "n_empty_first_turn": {lab: int((empty & (dfs[a].label == lab)).sum()) for lab in LABELS}}
    for lab in LABELS:
        out["strict_minus_permissive"][f"refusal_{lab}"] = diff(ref["strict", lab], ref["permissive", lab], paired=True)
    return out


def fmt(r):
    return f"{r['rate']:.3f} [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}]"


def fmt_diff(r):
    return f"{r['value']:+.3f} [{r['ci'][0]:+.3f}, {r['ci'][1]:+.3f}]"


def evaluate_model(key, rows, out_dir, batch_size, decode, setup):
    """Both arms of one model; skip when both CSVs and metrics.json exist (setup checked), resume from partial answers otherwise."""
    d = out_dir / key
    use_instruction = MODELS[key]["use_instruction"]
    record = {"model": key, "use_instruction": use_instruction, **setup}
    if all((d / f"{a}_responses.csv").exists() for a in ARMS) and (d / "metrics.json").exists():
        pin(d / "setup.json", record)
        print(f"{key}: outputs exist in {d}; skipping")
        return
    d.mkdir(parents=True, exist_ok=True)
    pin(d / "setup.json", record)
    if not use_instruction:
        print(f"{key}: use_instruction False, both arms get the bare request (as in conditional_safety.py)")
    model, tok = load_model_for_eval(key, attn_implementation=X["attn_implementation"], max_gpu_memory=X["max_gpu_memory"])
    dfs = {}
    for arm in ARMS:
        dfs[arm] = run_arm(model, tok, rows, arm, d / f"{arm}_partial.jsonl", use_instruction, batch_size, decode, setup["seed"])
        tmp = d / f"{arm}_responses.csv.tmp{os.getpid()}"
        dfs[arm].to_csv(tmp, index=False)
        os.replace(tmp, d / f"{arm}_responses.csv")
    unload_model(model)
    del model, tok
    cleanup_gpu()
    summary = summarize(dfs)
    if set(summary) & set(record):
        raise RuntimeError(f"metrics keys {sorted(set(summary) & set(record))} would overwrite setup keys in metrics.json")
    write_json(d / "metrics.json", {**record, **summary})


def dry_run(keys, rows, out_dir, decode):
    """No model: chat prompts of both arms for every prompt (one tokenizer per base model), the first prompt of each label printed."""
    print(f"decoding: max_new_tokens {X['max_new_tokens']}, temperature {X['temperature']}, top_p {X['top_p']}, "
          f"variant kwargs {decode or 'none (paper decoding)'}")
    groups = {}
    for k in keys:
        groups.setdefault((MODELS[k].get("base_model", BASE_MODEL), MODELS[k]["use_instruction"]), []).append(k)
    first = {lab: int((rows.label == lab).to_numpy().argmax()) for lab in LABELS}  # position of the first prompt of each label
    for (base, use_instruction), group in groups.items():
        tok = load_tokenizer_for_eval(group[0])
        for arm in ARMS:
            texts, lens = chat_prompts(tok, rows.prompt.tolist(), arm, use_instruction)
            print(f"\n===== {arm} | tokenizer {base} | use_instruction {use_instruction} | models {group} | "
                  f"{len(texts)} prompts, longest {lens.max()} tokens =====")
            for lab, i in first.items():
                print(f"[{lab} | prompt_idx {rows.prompt_idx.iloc[i]} | type {rows.type.iloc[i]}]\n{texts[i]}\n")
    for k in keys:
        d = out_dir / k
        if all((d / f"{a}_responses.csv").exists() for a in ARMS) and (d / "metrics.json").exists():
            status = "outputs exist, would skip"
        else:
            n = {a: sum(1 for _ in open(d / f"{a}_partial.jsonl")) if (d / f"{a}_partial.jsonl").exists() else 0 for a in ARMS}
            status = f"would generate (saved answers: {n})"
        print(f"{k}: {status} -> {d}")
    print(f"dry run: {len(keys)} models, no model loaded, no labels computed, nothing written")


def main():
    ap = argparse.ArgumentParser(description="XSTest contract test: strict vs permissive contracts on safe and unsafe XSTest prompts (GPU; --dry on CPU)")
    ap.add_argument("--models", nargs="+", required=True,
                    help="model keys of src/utils/eval/model_loader.py MODELS; the summary JSON covers exactly these models")
    ap.add_argument("--decode_variant", choices=sorted(CFG["decode_variants"]), default=None,
                    help="decoding preset (configs/pipeline.yaml decode_variants); outputs go to <evaluation_dir>/<name>/, preset pinned "
                         "in its decode_variant.json, as in conditional_safety.py")
    ap.add_argument("--batch_size", type=int, default=X["batch_size"], help="prompts per generate call")
    ap.add_argument("--samples", type=int, default=None,
                    help="smoke test: first N prompts of EACH label (2N in all); answers and summary get a _samples<N> suffix, "
                         "never the full run's files")
    ap.add_argument("--seed", type=int, default=X["seed"],
                    help="sampling seed (torch.manual_seed before each arm); any seed other than xstest_contract.seed is a resample "
                         "and its answers and summary get a _seed<N> suffix")
    ap.add_argument("--dry", action="store_true",
                    help="no model: load XSTest, print the counts, build every chat prompt, print the first prompt of each label "
                         "under both contracts; computes no label and writes nothing")
    args = ap.parse_args()
    unknown = [m for m in args.models if m not in MODELS]
    if unknown:
        ap.error(f"unknown model keys {unknown}")
    if args.samples is not None and not 1 <= args.samples <= min(X["counts"].values()):
        ap.error(f"--samples must be in [1, {min(X['counts'].values())}] (prompts per label)")
    if args.batch_size < 1:
        ap.error("--batch_size must be >= 1")
    if not args.dry and not torch.cuda.is_available():
        raise SystemExit("FATAL: CUDA not available: xstest_contract.py generates only on a GPU (use --dry to check prompts on CPU)")
    check_config()
    data = load_xstest()
    rows = data.groupby("label", sort=False).head(args.samples) if args.samples else data  # keeps dataset order
    print(f"{X['dataset']}@{X['revision'][:8]} split {X['split']}: {len(data)} prompts "
          f"({', '.join(f'{lab} {int((data.label == lab).sum())}' for lab in LABELS)}); this run: {len(rows)} "
          f"({', '.join(f'{lab} {int((rows.label == lab).sum())}' for lab in LABELS)})")
    for lab in LABELS:
        types = rows.type[rows.label == lab].value_counts(sort=False)
        print(f"  {lab}: " + ", ".join(f"{t} {n}" for t, n in types.items()))
    decode = decode_kwargs(args.decode_variant)
    root = variant_root(args.decode_variant) if args.decode_variant else project_root / CFG["paths"]["evaluation_dir"]
    suffix = (f"_samples{args.samples}" if args.samples else "") + (f"_seed{args.seed}" if args.seed != X["seed"] else "")
    out_dir = root / f"{X['dir_name']}{suffix}"
    variant = f"_{args.decode_variant}" if args.decode_variant else ""
    summary_path = project_root / X["summary_dir"] / f"{X['summary_name']}{variant}{suffix}.json"
    setup = {"dataset": X["dataset"], "revision": X["revision"], "split": X["split"], "contract_texts": CONTRACTS,
             "harm_categories": "none (XSTest has no PKU-SafeRLHF categories)", "max_new_tokens": X["max_new_tokens"],
             "temperature": X["temperature"], "top_p": X["top_p"], "seed": args.seed, "attn_implementation": X["attn_implementation"],
             "decode_variant": args.decode_variant, "decode": decode,
             "n_prompts": {lab: int((rows.label == lab).sum()) for lab in LABELS}}
    print(f"{len(rows)} prompts x {len(ARMS)} contracts x {len(args.models)} models; answers in {out_dir}; summary {summary_path}")
    for arm in ARMS:
        print(f"{arm.upper()} contract: {CONTRACTS[arm]}")
    if args.dry:
        dry_run(args.models, rows, out_dir, decode)
        return
    if args.decode_variant:
        root.mkdir(parents=True, exist_ok=True)
        _pin_preset(root / "decode_variant.json", args.decode_variant, decode)
    verify_models(args.models, non_interactive=True)
    for key in args.models:
        print(f"\n{'=' * 80}\n{key}\n{'=' * 80}")
        evaluate_model(key, rows, out_dir, args.batch_size, decode, setup)
    result = {}
    pbar = make_pbar(total=len(args.models), desc="xstest_contract summary", unit="model")
    for key in args.models:
        d = out_dir / key
        for arm in ARMS:
            if not pd.read_csv(d / f"{arm}_responses.csv", usecols=["prompt_idx"]).prompt_idx.equals(rows.prompt_idx.reset_index(drop=True)):
                raise SystemExit(f"FATAL: {d / f'{arm}_responses.csv'} does not hold this run's prompts; delete {d} to rerun")
        r = result[key] = {k: v for k, v in json.load(open(d / "metrics.json")).items() if k not in setup}
        c, g = r["contracts"], r["strict_minus_permissive"]
        print(f"{key:28s} over-refusal (safe) strict {fmt(c['strict']['refusal_safe'])} permissive {fmt(c['permissive']['refusal_safe'])}"
              f" | refusal (unsafe) strict {fmt(c['strict']['refusal_unsafe'])} permissive {fmt(c['permissive']['refusal_unsafe'])}"
              f" | strict-permissive safe {fmt_diff(g['refusal_safe'])} unsafe {fmt_diff(g['refusal_unsafe'])}"
              f" | discrimination strict {fmt_diff(c['strict']['discrimination'])} permissive {fmt_diff(c['permissive']['discrimination'])}")
        pbar.update(1)
    pbar.close()
    meta = {**setup, "prompt_builder": "system = contract, user = request (src/eval/conditional_safety.py, contract slot system)",
            "contract_source": "src/eval/conditional_safety.py synthesize_safety_instruction(harm_categories=[], variant)",
            "labels": "is_refusal = src/eval/conditional_safety.py detect_refusal_heuristic on the first assistant turn "
                      "(src/utils/eval/first_turn.py); is_refusal_full_response = the same heuristic on the whole answer (reference only)",
            "refusal_safe": "share of safe prompts refused (over-refusal)", "refusal_unsafe": "share of unsafe prompts refused",
            "answer_safe": "share of safe prompts not refused (helpfulness), interval computed on its own",
            "discrimination": "compliance on safe minus compliance on unsafe prompts (= refusal_unsafe - refusal_safe); "
                              "safe and unsafe prompts resampled independently",
            "strict_minus_permissive": "strict minus permissive refusal rate on the same prompts, paired over prompts",
            "n_empty_first_turn": "answers whose first turn is empty: scored as not refused by the heuristic",
            "bootstrap": CFG["bootstrap"], "resampling_unit": "prompt", "answers_dir": os.path.relpath(out_dir, project_root)}
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(summary_path, {"meta": meta, "models": result})
    print(f"wrote {summary_path.relative_to(project_root)} ({len(result)} models)")


if __name__ == "__main__":
    main()
