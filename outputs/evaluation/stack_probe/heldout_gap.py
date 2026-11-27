"""Held-out refusal gap (strict - permissive, 2,444 prompts) per model, both loadings, 95% BCa over prompts. CPU.
    python -u outputs/evaluation/stack_probe/heldout_gap.py 2>&1 | tee logs/heldout_gap.log
"""
import json
import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import GAP, ci  # noqa: E402

D = project_root / "outputs/evaluation/floor_heldout/full"
out = {}
KEYS = [k for t in ["DPO", "PPO", "GRPO", "CITA"] for k in (f"{t}_Instruct", f"{t}_Instruct_AsTrained")] + ["CITA_Instruct_Chain"]
for k in KEYS:
    s = pd.read_csv(D / k / "strict_responses.csv").sort_values("prompt_idx")
    p = pd.read_csv(D / k / "permissive_responses.csv").sort_values("prompt_idx")
    if not s.prompt_idx.to_numpy().tolist() == p.prompt_idx.to_numpy().tolist():
        raise RuntimeError(f"{k}: strict and permissive prompt sets differ")
    a, b = s.is_refusal.to_numpy(float), p.is_refusal.to_numpy(float)
    lo_hi, m = ci((a, b), GAP, paired=True)
    out[k] = {"n": int(len(a)), "gap": float(a.mean() - b.mean()), "ci": lo_hi, "ci_method": m}
    print(f"{k:24s} gap {a.mean() - b.mean():+.3f} [{lo_hi[0]:+.3f}, {lo_hi[1]:+.3f}]")
path = project_root / "outputs/evaluation/contract_gap/heldout_gap_both_loadings.json"
json.dump({"meta": {"prompts": "2,444 held-out PKU-SafeRLHF prompts", "statistic": "strict - permissive refusal rate",
                    "note": "_AsTrained = parent adapter merged first; plain = base + final adapter"}, "models": out},
          open(path, "w"), indent=2)
print(f"wrote {path}")
