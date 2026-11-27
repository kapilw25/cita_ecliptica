"""Capability as trained (lm-eval, src/eval/exp3_capability.py --mode astrained, box run): MMLU 5-shot and GSM8K accuracy per model with
95% BCa over items, and each model minus the base model paired over the same items. CPU.
    python -u outputs/evaluation/stack_probe/capability_ci.py 2>&1 | tee logs/capability_ci.log
"""
import json
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

SRC = project_root / "outputs/rebuttal/exp3_capability/astrained"
OUT = project_root / "outputs/evaluation/contract_gap/capability_astrained.json"
MODELS = ["base", "SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained", "CITA_Instruct_AsTrained"]
TASKS = {"mmlu": ("acc", "acc,none"), "gsm8k": ("exact_match", "exact_match,strict-match")}
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def items(model: str, task: str) -> dict:
    """Per-item score keyed by (subtask, doc_id); the first record of an item is the one lm-eval scored first (strict-match for GSM8K)."""
    key, _ = TASKS[task]
    out = {}
    for line in open(SRC / f"{model}_{task}_samples.jsonl"):
        r = json.loads(line)
        out.setdefault((r["task"], r["doc_id"]), float(r[key]))
    return out


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x,), MEAN, paired=False)
    return {"value": float(x.mean()), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


res = {}
for task, (_, agg) in TASKS.items():
    base = items("base", task)
    order = sorted(base)
    res[task] = {}
    for m in MODELS:
        s = items(m, task)
        if sorted(s) != order:
            raise SystemExit(f"FATAL: {m} {task} was scored on other items than the base model")
        x = np.array([s[k] for k in order])
        reported = json.load(open(SRC / f"{m}_{task}.json"))["results"][task][agg]
        if abs(x.mean() - reported) > 1e-9:
            raise SystemExit(f"FATAL: {m} {task}: item mean {x.mean():.4f} differs from lm-eval's {reported:.4f}")
        b = np.array([base[k] for k in order])
        res[task][m] = {"acc": interval(x), "minus_base": interval(x - b)}
        r = res[task][m]
        print(f"{task:6s} {m:26s} {r['acc']['value']:.3f} [{r['acc']['ci'][0]:.3f}, {r['acc']['ci'][1]:.3f}] | minus base "
              f"{r['minus_base']['value']:+.3f} [{r['minus_base']['ci'][0]:+.3f}, {r['minus_base']['ci'][1]:+.3f}] (n={r['acc']['n']})")
OUT.write_text(json.dumps({"meta": {"source": str(SRC.relative_to(project_root)), "mmlu": "5-shot, 100 items per subject (57 subjects)",
                                    "gsm8k": "5-shot, first 100 problems, strict-match", "pairing": "same items, model minus base",
                                    "ci": "95% BCa, 10,000 resamples over items"}, "tasks": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
