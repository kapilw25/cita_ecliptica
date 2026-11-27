"""Each one-contract training step, start to end: strict-minus-permissive refusal gap of the trained model minus that of the model it
started from, paired over the 1,222 prompts, under the LLM judge and the first-turn phrase heuristic; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/judge_vs_start.py 2>&1 | tee logs/judge_vs_start.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

LABELS = project_root / "outputs/evaluation/refusal_judge"
OUT = project_root / "outputs/evaluation/contract_gap/judge_vs_start.json"
# (step, trained model as evaluated, the model its training started from), as in BASE_MODEL_MAP and src/utils/eval/model_loader.py
STEPS = [("SFT", "SFT_Instruct", "Llama31_Base_Prompted"),
         ("DPO", "DPO_Instruct_AsTrained", "SFT_Instruct"),
         ("GRPO", "GRPO_Instruct_AsTrained", "SFT_Instruct"),
         ("SwiPO-S", "CITA_Instruct_Chain", "DPO_Instruct_AsTrained"),
         ("SwiPO-R", "CITA_Instruct_AsTrained", "DPO_Instruct")]
SCORERS = {"judge": "is_refusal_judge", "phrase_first_turn": "is_refusal_heuristic_first_turn"}
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def gaps(model: str, col: str) -> pd.Series:
    s = pd.read_csv(LABELS / model / "strict.csv").set_index("prompt_idx")[col].astype(float)
    p = pd.read_csv(LABELS / model / "permissive.csv").set_index("prompt_idx")[col].astype(float)
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {model} strict and permissive labels cover different prompts")
    return s - p


res = {}
for step, end, start in STEPS:
    res[step] = {"end": end, "start": start}
    for name, col in SCORERS.items():
        ge, gs = gaps(end, col), gaps(start, col)
        if not ge.index.equals(gs.index):
            raise SystemExit(f"FATAL: {end} and {start} were judged on different prompts")
        d = (ge - gs).to_numpy()
        (lo, hi), method = ci((d,), MEAN, paired=False)
        (slo, shi), _ = ci((gs.to_numpy(),), MEAN, paired=False)
        (elo, ehi), _ = ci((ge.to_numpy(),), MEAN, paired=False)
        res[step][name] = {"start_gap": float(gs.mean()), "start_ci": [slo, shi], "end_gap": float(ge.mean()), "end_ci": [elo, ehi],
                           "end_minus_start": float(d.mean()), "ci": [lo, hi], "ci_method": method, "n": int(len(d))}
        r = res[step][name]
        print(f"{step:8s} {name:18s} start {r['start_gap']:+.3f} -> end {r['end_gap']:+.3f} | end minus start {r['end_minus_start']:+.3f} "
              f"[{lo:+.3f}, {hi:+.3f}]")
OUT.write_text(json.dumps({"meta": {"gap": "strict minus permissive refusal rate, per prompt", "pairing": "same prompts, end minus start",
                                    "labels": str(LABELS.relative_to(project_root)), "ci": "95% BCa, 10,000 resamples over prompts"},
                           "steps": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
