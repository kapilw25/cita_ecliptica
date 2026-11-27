"""Instruction sensitivity as trained: Conditional Safety |strict - permissive| refusal gap, Instruct minus NoInstruct twin,
SwiPO minus each rival, paired 95% BCa over prompts. CPU.
    python -u outputs/evaluation/stack_probe/astrained_sensitivity.py --suffix _AsTrained 2>&1 | tee logs/astrained_sensitivity.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402
from src.eval.score_table_ci import load_cond_safety  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--suffix", required=True, help="model-key suffix: _AsTrained (parent merged first) or '' (base + final delta)")
args = ap.parse_args()
TRAINERS = ["CITA", "DPO", "PPO", "GRPO"]
data = {}
for t in TRAINERS:
    for v in ("Instruct", "NoInstruct"):
        data[(t, v)] = load_cond_safety(f"{t}_{v}{args.suffix}")  # (ids, (strict - permissive per prompt,))
ids0 = data[("CITA", "Instruct")][0]
for k, (ids, _) in data.items():
    if not np.array_equal(ids, ids0):
        raise RuntimeError(f"{k}: scored on different prompts")
arr = {k: v[1][0].astype(float) for k, v in data.items()}


def delta(i, n, axis=-1):
    return np.abs(np.mean(i, axis=axis)) - np.abs(np.mean(n, axis=axis))


out = {}
for t in TRAINERS:
    lo_hi, m = ci((arr[(t, "Instruct")], arr[(t, "NoInstruct")]), delta, paired=True)
    out[t] = {"delta": float(delta(arr[(t, "Instruct")], arr[(t, "NoInstruct")])), "ci": lo_hi, "ci_method": m}
    print(f"{t:5s} Instruct minus NoInstruct {out[t]['delta']:+.3f} [{lo_hi[0]:+.3f}, {lo_hi[1]:+.3f}]")
for r in TRAINERS[1:]:
    f = lambda a, b, c, d, axis=-1: delta(a, b, axis=axis) - delta(c, d, axis=axis)  # noqa: E731
    xs = (arr[("CITA", "Instruct")], arr[("CITA", "NoInstruct")], arr[(r, "Instruct")], arr[(r, "NoInstruct")])
    lo_hi, m = ci(xs, f, paired=True)
    out[f"CITA_minus_{r}"] = {"value": float(f(*xs)), "ci": lo_hi, "ci_method": m}
    print(f"SwiPO minus {r:4s} {out[f'CITA_minus_{r}']['value']:+.3f} [{lo_hi[0]:+.3f}, {lo_hi[1]:+.3f}]")
path = project_root / "outputs/evaluation/contract_gap" / f"instruction_sensitivity{args.suffix or '_paper_loading'}.json"
json.dump({"meta": {"suite": "conditional_safety", "n": int(len(ids0)), "suffix": args.suffix,
                    "statistic": "|strict - permissive| refusal gap, Instruct minus NoInstruct twin"}, "trainers": out},
          open(path, "w"), indent=2)
print(f"wrote {path}")
