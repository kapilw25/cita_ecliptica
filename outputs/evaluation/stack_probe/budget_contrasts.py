"""Bench2Evidence error decomposition (ChatGPT v6 priority 2): per model, the loading effect (final adapter alone minus as trained) under
each scorer, the scorer effect (phrase minus judge, first turn) under each loading, their interaction, and the total error of the
published audit (final-only phrase gap minus as-trained judge gap), paired over the 1,222 Conditional Safety prompts; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/budget_contrasts.py 2>&1 | tee logs/budget_contrasts.log
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
OUT = project_root / "outputs/evaluation/contract_gap/budget_contrasts.json"
PAIRS = {"DPO": ("DPO_Instruct", "DPO_Instruct_AsTrained"), "GRPO": ("GRPO_Instruct", "GRPO_Instruct_AsTrained"),
         "SwiPO-R": ("CITA_Instruct", "CITA_Instruct_AsTrained"), "SwiPO-S": ("CITA_Instruct_Chain_FinalOnly", "CITA_Instruct_Chain")}
SCORERS = {"phrase": "is_refusal_heuristic_first_turn", "judge": "is_refusal_judge"}
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x.astype(float),), MEAN, paired=False)
    return {"value": float(np.mean(x)), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


def gaps(model: str) -> dict:
    """Per-prompt strict-minus-permissive refusal (-1, 0, +1) under each scorer."""
    s = pd.read_csv(LABELS / model / "strict.csv").set_index("prompt_idx").sort_index()
    p = pd.read_csv(LABELS / model / "permissive.csv").set_index("prompt_idx").sort_index()
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {model}: strict and permissive labels cover different prompts")
    return {k: (s[c].astype(bool).astype(float) - p[c].astype(bool).astype(float)) for k, c in SCORERS.items()}


res, index = {}, None
for name, (final, trained) in PAIRS.items():
    f, t = gaps(final), gaps(trained)
    for g in (*f.values(), *t.values()):
        if index is None:
            index = g.index
        if not g.index.equals(index):
            raise SystemExit(f"FATAL: {name}: label files cover different prompts")
    fP, fJ, tP, tJ = (x.to_numpy() for x in (f["phrase"], f["judge"], t["phrase"], t["judge"]))
    res[name] = {"cells": {"final_phrase": interval(fP), "final_judge": interval(fJ), "trained_phrase": interval(tP), "trained_judge": interval(tJ)},
                 "loading_effect_phrase": interval(fP - tP), "loading_effect_judge": interval(fJ - tJ),
                 "scorer_effect_final": interval(fP - fJ), "scorer_effect_trained": interval(tP - tJ),
                 "interaction": interval((fP - fJ) - (tP - tJ)), "total_error": interval(fP - tJ)}
    r = res[name]
    fmt = lambda k: f"{r[k]['value']:+.3f} [{r[k]['ci'][0]:+.3f}, {r[k]['ci'][1]:+.3f}]"  # noqa: E731
    print(f"{name:8s} loading|phrase {fmt('loading_effect_phrase')} loading|judge {fmt('loading_effect_judge')} scorer|final "
          f"{fmt('scorer_effect_final')} scorer|trained {fmt('scorer_effect_trained')} interaction {fmt('interaction')} total {fmt('total_error')}")
OUT.write_text(json.dumps({"meta": {"labels": "outputs/evaluation/refusal_judge/<model>/{strict,permissive}.csv (src/eval/refusal_judge.py)",
                                    "scorers": SCORERS, "unit": "per-prompt strict-minus-permissive refusal, first turn",
                                    "total_error": "final-only phrase gap minus as-trained judge gap = loading effect (phrase) + scorer effect "
                                                   "(as trained)", "ci": "95% BCa over prompts, 10,000 resamples"}, "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
