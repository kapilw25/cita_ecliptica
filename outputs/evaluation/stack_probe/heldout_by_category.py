"""Bench2Evidence held-out check by harm category (ChatGPT v6 priority 5): strict-minus-permissive refusal gap (phrase heuristic) on the 2,444
held-out PKU-SafeRLHF prompts, per harm category, models as trained; paired over prompts, 95% BCa; categories with at least min_n prompts. CPU.
    python -u outputs/evaluation/stack_probe/heldout_by_category.py 2>&1 | tee logs/heldout_by_category.log
"""
import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

HO = project_root / "outputs/evaluation/floor_heldout/full"
OUT = project_root / "outputs/evaluation/contract_gap/heldout_by_category.json"
MODELS = {"DPO": "DPO_Instruct_AsTrained", "PPO": "PPO_Instruct_AsTrained", "GRPO": "GRPO_Instruct_AsTrained",
          "SwiPO-R": "CITA_Instruct_AsTrained", "SwiPO-S": "CITA_Instruct_Chain", "Instruct (prompted)": "Llama31_Instruct_Prompted"}
MIN_N = 50  # smallest category reported: below this a gap interval spans most of [-1, 1]
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def arm(model: str, a: str) -> pd.DataFrame:
    return pd.read_csv(HO / model / f"{a}_responses.csv", usecols=["prompt_idx", "harm_categories", "is_refusal"]).set_index("prompt_idx").sort_index()


res = {}
for name, model in MODELS.items():
    s, p = arm(model, "strict"), arm(model, "permissive")
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {model}: strict and permissive held-out answers cover different prompts")
    gap = s["is_refusal"].astype(float) - p["is_refusal"].astype(float)
    cats = s["harm_categories"].map(ast.literal_eval)
    names = sorted({c for cs in cats for c in cs})
    res[name] = {"n_prompts": int(len(gap)), "categories": {}}
    for c in names:
        sel = cats.map(lambda cs, c=c: c in cs).to_numpy()
        if sel.sum() < MIN_N:
            continue
        (lo, hi), method = ci((gap.to_numpy()[sel],), MEAN, paired=False)
        res[name]["categories"][c] = {"gap": float(gap.to_numpy()[sel].mean()), "ci": [lo, hi], "ci_method": method, "n": int(sel.sum())}
    vals = [v["gap"] for v in res[name]["categories"].values()]
    excl = sum(1 for v in res[name]["categories"].values() if v["ci"][0] > 0 or v["ci"][1] < 0)
    res[name]["summary"] = {"min": min(vals), "max": max(vals), "n_categories": len(vals), "n_excluding_zero": excl}
    print(f"{name:20s} n={len(gap)} | {len(vals)} categories: gap {min(vals):+.3f} to {max(vals):+.3f}; {excl} exclude zero")
OUT.write_text(json.dumps({"meta": {"suite": "2,444 held-out PKU-SafeRLHF prompts (floor_heldout.py), phrase heuristic, paper decoding",
                                    "min_n": MIN_N, "ci": "95% BCa over prompts, 10,000 resamples; a prompt counts in every category it carries"},
                           "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
