"""Strict-minus-permissive refusal gap with the contract in the system message (paper), in the user turn, and in conflict
(system arm + opposite contract in the user turn); paired 95% BCa over prompts, slot minus system. CPU.
    python -u outputs/evaluation/stack_probe/contract_slot_gap.py --slots user conflict 2>&1 | tee logs/contract_slot_gap.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
import src.eval.score_table_ci as sct  # noqa: E402
from src.eval.floor_leakage import ci  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--slots", nargs="+", choices=["user", "conflict"], required=True)
args = ap.parse_args()
SYSTEM_DIR = sct.EVAL_DIR
SUITE_DIR = sct.SUITES["conditional_safety"]


def gap(d, axis=-1):
    return np.mean(d, axis=axis)


def diff(a, b, axis=-1):
    return np.mean(a, axis=axis) - np.mean(b, axis=axis)


out = {}
for slot in args.slots:
    slot_dir = SYSTEM_DIR / f"contract_slot_{slot}"
    models = sorted(p.name for p in (slot_dir / SUITE_DIR).iterdir() if (p / "metrics.json").exists())
    if not models:
        raise RuntimeError(f"{slot_dir / SUITE_DIR}: no finished model")
    out[slot] = {}
    for m in models:
        sct.EVAL_DIR = SYSTEM_DIR
        ids_s, (d_sys,) = sct.load_cond_safety(m)
        sct.EVAL_DIR = slot_dir
        ids_x, (d_slot,) = sct.load_cond_safety(m)
        if not np.array_equal(ids_s, ids_x):
            raise RuntimeError(f"{m}: system and {slot} runs scored different prompts")
        g_lo_hi, g_m = ci((d_slot.astype(float),), gap, paired=True)
        s_lo_hi, _ = ci((d_sys.astype(float),), gap, paired=True)
        d_lo_hi, d_m = ci((d_slot.astype(float), d_sys.astype(float)), diff, paired=True)
        out[slot][m] = {"n": int(len(ids_s)), "system_gap": float(gap(d_sys)), "system_gap_ci": s_lo_hi,
                        "slot_gap": float(gap(d_slot)), "slot_gap_ci": g_lo_hi,
                        "slot_minus_system": float(diff(d_slot, d_sys)), "slot_minus_system_ci": d_lo_hi, "ci_method": d_m}
        r = out[slot][m]
        print(f"{slot:8s} {m:28s} system {r['system_gap']:+.3f} [{s_lo_hi[0]:+.3f}, {s_lo_hi[1]:+.3f}]  "
              f"{slot} {r['slot_gap']:+.3f} [{g_lo_hi[0]:+.3f}, {g_lo_hi[1]:+.3f}]  "
              f"diff {r['slot_minus_system']:+.3f} [{d_lo_hi[0]:+.3f}, {d_lo_hi[1]:+.3f}]")
path = project_root / "outputs/evaluation/contract_gap" / f"contract_slot_{'_'.join(args.slots)}.json"
json.dump({"meta": {"suite": "conditional_safety", "statistic": "strict arm minus permissive arm refusal rate (signed); "
                    "conflict: the arm is the system contract, the user turn carries the opposite one"}, "slots": out},
          open(path, "w"), indent=2)
print(f"wrote {path}")
