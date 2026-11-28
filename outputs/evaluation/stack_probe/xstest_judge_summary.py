"""XSTest safety-helpfulness summary under the LLM refusal judge (first turn), in the shape xstest_tradeoff_plot.py reads; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/xstest_judge_summary.py 2>&1 | tee logs/xstest_judge_summary.log
    python -u outputs/evaluation/stack_probe/xstest_judge_summary.py --judge qwen 2>&1 | tee logs/xstest_judge_summary_qwen.log
    python -u src/eval/xstest_tradeoff_plot.py --summary outputs/evaluation/contract_gap/xstest_contract_judge_stop_eot.json --paper 2>&1 | tee logs/xstest_tradeoff_judge_paper.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
X = CFG["xstest_contract"]
ROOT = project_root / "outputs/evaluation/stop_eot"
ap = argparse.ArgumentParser(description="XSTest per-axis summary under an LLM refusal judge (CPU)")
ap.add_argument("--judge", choices=sorted(CFG["refusal_judge"]["alt_judges"]), default=None,
                help="a judge from another family (refusal_judge.py --judge NAME); adds agreement with the default judge")
ARGS = ap.parse_args()
TAG = f"_{ARGS.judge}" if ARGS.judge else ""
DEFAULT_LABELS = ROOT / "refusal_judge_xstest"  # src/eval/refusal_judge.py --suite xstest --decode_variant stop_eot (box run)
LABELS = ROOT / f"refusal_judge_xstest{TAG}"
ANSWERS = ROOT / X["dir_name"]           # src/eval/xstest_contract.py --decode_variant stop_eot: holds the safe/unsafe label per prompt
OUT = project_root / X["summary_dir"] / f"{X['summary_name']}_judge{TAG}_stop_eot.json"
ARMS = ("strict", "permissive")
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731
DIFF = lambda a, b, axis=-1: np.mean(a, axis=axis) - np.mean(b, axis=axis)  # noqa: E731


def kappa(a, b, axis=-1):
    """Cohen's kappa of two binary label vectors (vectorized over resamples)."""
    po = np.mean(a == b, axis=axis)
    pa, pb = np.mean(a, axis=axis), np.mean(b, axis=axis)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return np.where(pe < 1, (po - pe) / np.where(pe < 1, 1 - pe, 1), 1.0)


def agreement(model):
    """This judge vs the default judge on the same answers, both contracts pooled: share agreeing and kappa, 95% BCa (paired)."""
    a, b = [], []
    for arm_ in ARMS:
        x = pd.read_csv(LABELS / model / f"{arm_}.csv").set_index("prompt_idx")["is_refusal_judge"].astype(bool)
        y = pd.read_csv(DEFAULT_LABELS / model / f"{arm_}.csv").set_index("prompt_idx")["is_refusal_judge"].astype(bool).reindex(x.index)
        if y.isna().any():
            raise SystemExit(f"FATAL: {model} {arm_}: the default judge has no label for some prompts")
        a.append(x.to_numpy(float)); b.append(y.to_numpy(float))
    a, b = np.concatenate(a), np.concatenate(b)
    agree = lambda u, v, axis=-1: np.mean(u == v, axis=axis)  # noqa: E731
    out = {}
    for name, fn in (("agreement", agree), ("kappa", kappa)):
        (lo, hi), m = ci((a, b), fn, paired=True)
        out[name] = {"value": float(fn(a, b)), "ci": [lo, hi], "ci_method": m, "n": int(len(a))}
    return out


def rate(x):
    (lo, hi), method = ci((x.astype(float),), MEAN, paired=False)
    return {"n": int(len(x)), "rate": float(x.mean()), "ci": [lo, hi], "ci_method": method}


def arm(model, a):
    j = pd.read_csv(LABELS / model / f"{a}.csv").set_index("prompt_idx")["is_refusal_judge"].astype(bool)
    lab = pd.read_csv(ANSWERS / model / f"{a}_responses.csv", usecols=["prompt_idx", "label"]).set_index("prompt_idx")["label"]
    if not j.index.sort_values().equals(lab.index.sort_values()):
        raise SystemExit(f"FATAL: {model} {a}: judge labels and XSTest answers cover different prompts")
    lab = lab.reindex(j.index)
    if set(lab.unique()) != {"safe", "unsafe"} or (lab == "safe").sum() != X["counts"]["safe"]:
        raise SystemExit(f"FATAL: {model} {a}: label counts {lab.value_counts().to_dict()} differ from {X['counts']}")
    safe, unsafe = j[lab == "safe"].to_numpy(), j[lab == "unsafe"].to_numpy()
    (dlo, dhi), dm = ci((unsafe.astype(float), safe.astype(float)), DIFF, paired=False)
    return {"refusal_safe": rate(safe), "refusal_unsafe": rate(unsafe), "answer_safe": rate(~safe),
            "discrimination": {"value": float(unsafe.mean() - safe.mean()), "ci": [dlo, dhi], "ci_method": dm, "paired": False},
            "_labels": (j, lab)}


def shift(c):
    """Strict minus permissive per axis, paired over the same prompts (each prompt answered under both contracts)."""
    (js, lab), (jp, _) = c["strict"].pop("_labels"), c["permissive"].pop("_labels")
    jp = jp.reindex(js.index)
    out = {}
    for name, mask, sign in (("refusal_unsafe", lab == "unsafe", 1), ("answer_safe", lab == "safe", -1)):
        a, b = js[mask].to_numpy(float), jp[mask].to_numpy(float)
        d = sign * (a - b)
        (lo, hi), m = ci((d,), MEAN, paired=False)
        out[name] = {"value": float(d.mean()), "ci": [lo, hi], "ci_method": m, "paired": True}
    return out


models = {}
for d in sorted(p for p in LABELS.iterdir() if p.is_dir()):
    c = {a: arm(d.name, a) for a in ARMS}
    sh = shift(c)
    models[d.name] = {"model": d.name, "n": {"safe": c["strict"]["refusal_safe"]["n"], "unsafe": c["strict"]["refusal_unsafe"]["n"]},
                      "contracts": c, "strict_minus_permissive": sh}
    if ARGS.judge:
        models[d.name]["agreement_with_default_judge"] = agreement(d.name)
        g = models[d.name]["agreement_with_default_judge"]
        print(f"{d.name:28s} vs default judge: agreement {g['agreement']['value']:.3f} kappa {g['kappa']['value']:.2f} "
              f"[{g['kappa']['ci'][0]:.2f}, {g['kappa']['ci'][1]:.2f}]")
    s, p = c["strict"], c["permissive"]
    print(f"{d.name:28s} strict: unsafe refused {s['refusal_unsafe']['rate']:.3f} safe answered {s['answer_safe']['rate']:.3f} | "
          f"permissive: unsafe refused {p['refusal_unsafe']['rate']:.3f} safe answered {p['answer_safe']['rate']:.3f} | shift "
          + " ".join(f"{k} {v['value']:+.3f} [{v['ci'][0]:+.3f}, {v['ci'][1]:+.3f}]" for k, v in sh.items()))
OUT.write_text(json.dumps({"meta": {"decode_variant": "stop_eot", "scorer": f"LLM refusal judge (src/eval/refusal_judge.py{' --judge ' + ARGS.judge if ARGS.judge else ''}), first turn",
                                    "labels": str(LABELS.relative_to(project_root)), "answers": str(ANSWERS.relative_to(project_root)),
                                    "ci": "95% BCa, 10,000 resamples over prompts", "answer_safe": "1 - judge refusal on safe prompts"},
                           "models": models}, indent=2))
print(f"wrote {OUT.relative_to(project_root)} ({len(models)} models)")
