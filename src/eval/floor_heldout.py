"""Held-out floor test: strict and permissive contracts on unseen PKU-SafeRLHF prompts for the four Instruct models. GPU-only.
    python -u src/eval/floor_heldout.py --SANITY --no-wandb 2>&1 | tee logs/floor_heldout_sanity.log
    python -u src/eval/floor_heldout.py --FULL 2>&1 | tee logs/floor_heldout_full.log
    python -u src/eval/floor_heldout.py --FULL --no-wandb --seed 1 --models DPO_Instruct_AsTrained Llama31_Instruct_Prompted 2>&1 | tee logs/floor_heldout_seed1.log
"""

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
import torch
import yaml

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.eval import MODELS, load_model_for_eval, unload_model, batch_generate, cleanup_gpu, format_chat_messages  # noqa: E402
from src.utils.wandb_utils import add_wandb_args, init_wandb, log_metrics, finish_wandb  # noqa: E402
from src.eval.conditional_safety import synthesize_safety_instruction, detect_refusal_heuristic  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
H = CFG["floor_leakage"]["heldout"]
TRAINERS = CFG["score_table"]["trainers"]
VARIANT = CFG["floor_leakage"]["variant"]
SANITY_N = CFG["eval"]["sanity"]["conditional_safety"]
ARMS = {"STRICT": "strict_responses.csv", "PERMISSIVE": "permissive_responses.csv"}


def load_prompts(n):
    rows = [json.loads(line) for line in open(project_root / H["dir"] / H["prompts_file"])]
    if len(rows) != H["n_prompts"]:
        raise RuntimeError(f"{H['prompts_file']} has {len(rows)} prompts, config says {H['n_prompts']}; run floor_heldout_build.py")
    return rows[:n]


def run_arm(model, tokenizer, rows, arm, partial_path, use_instruction=True):
    """Generate one contract arm with resume; a NoInstruct model gets the bare request in both arms, as in the suite."""
    done = [json.loads(line) for line in open(partial_path)] if partial_path.exists() else []
    if done:
        print(f"  {arm}: resuming from {len(done)}/{len(rows)} saved answers")
    todo = rows[len(done):]
    messages = [([{"role": "system", "content": synthesize_safety_instruction(r["harm_categories"], arm)}] if use_instruction else [])
                + [{"role": "user", "content": r["prompt"]}] for r in todo]

    def save(texts):  # batch_generate passes every answer produced so far in this call
        with open(partial_path, "w") as f:
            for r in done:
                f.write(json.dumps(r) + "\n")
            for r, t in zip(todo, texts):
                f.write(json.dumps({"prompt_idx": r["prompt_idx"], "response": t}) + "\n")

    t0 = time.time()
    texts = batch_generate(model, tokenizer, format_chat_messages(tokenizer, messages), batch_size=H["batch_size"],
                           max_new_tokens=H["max_new_tokens"], temperature=H["temperature"], top_p=H["top_p"],
                           do_sample=True, desc=arm, checkpoint_callback=save, checkpoint_interval=H["batch_size"] * 4) if todo else []
    if todo:
        save(texts)
        print(f"  {arm}: {len(todo)} new answers in {time.time() - t0:.0f}s ({len(todo) / (time.time() - t0):.2f} prompts/s this run)")
    answers = {r["prompt_idx"]: r["response"] for r in (json.loads(line) for line in open(partial_path))}
    if len(answers) != len(rows):
        raise RuntimeError(f"{arm}: {len(answers)} answers for {len(rows)} prompts")
    out = []
    for r in rows:
        ref = detect_refusal_heuristic(answers[r["prompt_idx"]])
        out.append({"prompt_idx": r["prompt_idx"], "prompt": r["prompt"], "harm_categories": r["harm_categories"],
                    "variant": arm, "response": answers[r["prompt_idx"]], "is_refusal": ref["is_refusal"],
                    "refusal_confidence": ref["confidence"]})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--SANITY", action="store_true", help=f"first {SANITY_N} prompts, separate output dir")
    mode.add_argument("--FULL", action="store_true", help=f"all {H['n_prompts']} held-out prompts")
    ap.add_argument("--trainers", nargs="+", choices=TRAINERS, default=TRAINERS,
                    help="subset of trainers for this process; run one process per trainer in parallel to keep the GPU busy")
    ap.add_argument("--seed", type=int, default=H["seed"],
                    help="sampling seed; any seed other than floor_leakage.heldout.seed is a resample written to <dir>/full_seed<N>/")
    ap.add_argument("--models", nargs="+", choices=sorted(MODELS), default=None,
                    help="explicit model keys instead of --trainers (controls: NoInstruct models, the prompted Instruct baseline)")
    add_wandb_args(ap)
    args = ap.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available: floor_heldout.py is GPU-only")
    rows = load_prompts(SANITY_N if args.SANITY else H["n_prompts"])
    out_root = project_root / H["dir"] / (("sanity" if args.SANITY else "full") + (f"_seed{args.seed}" if args.seed != H["seed"] else ""))
    run = init_wandb("floor_heldout", "sanity" if args.SANITY else "full", {**H, "n": len(rows), "trainers": args.trainers},
                     enabled=not args.no_wandb)
    torch.manual_seed(args.seed)
    for key in args.models or [f"{t}_{VARIANT}" for t in args.trainers]:
        d = out_root / key
        if all((d / f).exists() for f in ARMS.values()) and (d / "metrics.json").exists():
            print(f"{key}: outputs exist in {d}; skipping")
            continue
        d.mkdir(parents=True, exist_ok=True)
        model, tokenizer = load_model_for_eval(key, attn_implementation=H["attn_implementation"], max_gpu_memory=H["max_gpu_memory"])
        rates = {}
        for arm, fname in ARMS.items():
            df = run_arm(model, tokenizer, rows, arm, d / f"{arm.lower()}_partial.jsonl", MODELS[key]["use_instruction"])
            df.to_csv(d / fname, index=False)
            rates[arm] = float(df.is_refusal.mean())
        unload_model(model)
        cleanup_gpu()
        metrics = {"adaptation_score": abs(rates["STRICT"] - rates["PERMISSIVE"]), "strict_refusal_rate": rates["STRICT"],
                   "permissive_refusal_rate": rates["PERMISSIVE"], "n_prompts": len(rows), "source": "heldout"}
        json.dump(metrics, open(d / "metrics.json", "w"), indent=2)
        log_metrics(run, {f"{key}/{k}": v for k, v in metrics.items() if isinstance(v, float)})
        print(f"{key}: strict {rates['STRICT']:.3f} permissive {rates['PERMISSIVE']:.3f} gap {rates['STRICT'] - rates['PERMISSIVE']:+.3f} (n={len(rows)})")
    finish_wandb(run)
    print(f"done; outputs in {out_root}. Next: python -u src/eval/floor_leakage.py --source heldout")


if __name__ == "__main__":
    main()
