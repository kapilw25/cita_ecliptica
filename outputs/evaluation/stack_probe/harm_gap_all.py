"""Llama Guard unsafe rate, permissive minus strict, over all 1,222 Conditional Safety prompts, paired 95% BCa. CPU (reads cached labels).
    python -u outputs/evaluation/stack_probe/harm_gap_all.py 2>&1 | tee logs/harm_gap_all.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

LAB = project_root / "outputs/evaluation/floor_harm/conditional_safety/full"
MODELS = ["CITA_Instruct_AsTrained", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained",
          "CITA_NoInstruct_AsTrained", "DPO_NoInstruct_AsTrained", "PPO_NoInstruct_AsTrained", "GRPO_NoInstruct_AsTrained",
          "CITA_Instruct", "DPO_Instruct", "PPO_Instruct", "GRPO_Instruct", "SFT_Instruct", "Llama31_Instruct_Prompted",
          "Llama31_Base_Prompted", "CITA_Instruct_Chain", "CITA_NoInstruct_Chain"]
DIFF = lambda a, b, axis=-1: np.mean(a, axis=axis) - np.mean(b, axis=axis)  # noqa: E731
MEAN = lambda a, axis=-1: np.mean(a, axis=axis)  # noqa: E731
out = {}
for k in MODELS:
    s, p = pd.read_csv(LAB / f"{k}_strict_labels.csv"), pd.read_csv(LAB / f"{k}_permissive_labels.csv")
    if not s.prompt_idx.equals(p.prompt_idx):
        raise RuntimeError(f"{k}: strict and permissive prompt sets differ")
    a, b = p.unsafe.to_numpy(float), s.unsafe.to_numpy(float)
    d_ci, d_m = ci((a, b), DIFF, paired=True)
    out[k] = {"n": int(len(a)), "strict_unsafe": {"rate": float(b.mean()), "ci": ci((b,), MEAN, paired=True)[0]},
              "permissive_unsafe": {"rate": float(a.mean()), "ci": ci((a,), MEAN, paired=True)[0]},
              "permissive_minus_strict": {"value": float(a.mean() - b.mean()), "ci": d_ci, "ci_method": d_m}}
    print(f"{k:28s} strict {b.mean():.3f} permissive {a.mean():.3f} diff {a.mean() - b.mean():+.3f} [{d_ci[0]:+.3f}, {d_ci[1]:+.3f}]")
meta = {"classifier": "Llama Guard 3 (labels cached by src/eval/floor_harm_classify.py)", "prompts": "all Conditional Safety prompts",
        "note": "_AsTrained = parent adapter merged first, as trained; plain keys = base + final LoRA delta, as loaded for the paper"}
path = LAB / "harm_gap_all_prompts.json"
json.dump({"meta": meta, "models": out}, open(path, "w"), indent=2)
print(f"wrote {path}")
