"""No-KL ablation (ARR reviewer shuX; owner pick Fri Nov 27 2026): SwiPO on the SFT chain with lambda = 0 (contract-conditioned DPO) against
SwiPO-S (same chain, data and settings, lambda > 0) and against their shared start (DPO as trained): refusal gap under the LLM judge and the
first-turn phrase heuristic, and the Llama Guard 3 unsafe-rate gap, paired over the 1,222 prompts; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/nokl_compare.py 2>&1 | tee logs/nokl_compare.log
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
HARM = project_root / "outputs/evaluation/floor_harm/conditional_safety/full"
OUT = project_root / "outputs/evaluation/contract_gap/nokl_compare.json"
NOKL, SWIPO_S, START = "CITA_Instruct_Chain_noKL", "CITA_Instruct_Chain", "DPO_Instruct_AsTrained"
SCORERS = {"judge": "is_refusal_judge", "phrase_first_turn": "is_refusal_heuristic_first_turn"}
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def arm(root: Path, model: str, a: str, col: str, harm: bool) -> pd.Series:
    f = root / f"{model}_{a}_labels.csv" if harm else root / model / f"{a}.csv"
    return pd.read_csv(f).set_index("prompt_idx").sort_index()[col].astype(float)


def gap(model: str, col: str, harm: bool = False) -> pd.Series:
    """Per-prompt strict-minus-permissive refusal, or permissive-minus-strict unsafe (harm)."""
    root = HARM if harm else LABELS
    s, p = arm(root, model, "strict", col, harm), arm(root, model, "permissive", col, harm)
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {model}: strict and permissive labels cover different prompts")
    return (p - s) if harm else (s - p)


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x,), MEAN, paired=False)
    return {"value": float(x.mean()), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


res = {}
specs = {**{k: (c, False) for k, c in SCORERS.items()}, "harm_llama_guard": ("unsafe", True)}
for name, (col, harm) in specs.items():
    g, s_, st = gap(NOKL, col, harm), gap(SWIPO_S, col, harm), gap(START, col, harm)
    if not (g.index.equals(s_.index) and g.index.equals(st.index)):
        raise SystemExit(f"FATAL: {name}: {NOKL}, {SWIPO_S} and {START} were scored on different prompts")
    res[name] = {"gap": interval(g.to_numpy()), "minus_swipo_s": interval((g - s_).to_numpy()), "minus_start": interval((g - st).to_numpy())}
    r = res[name]
    print(f"{name:18s} no-KL gap {r['gap']['value']:+.3f} [{r['gap']['ci'][0]:+.3f}, {r['gap']['ci'][1]:+.3f}] | minus SwiPO-S "
          f"{r['minus_swipo_s']['value']:+.3f} [{r['minus_swipo_s']['ci'][0]:+.3f}, {r['minus_swipo_s']['ci'][1]:+.3f}] | minus start "
          f"{r['minus_start']['value']:+.3f} [{r['minus_start']['ci'][0]:+.3f}, {r['minus_start']['ci'][1]:+.3f}]")
strict_unsafe = {m: interval(arm(HARM, m, "strict", "unsafe", True).to_numpy()) for m in (NOKL, SWIPO_S, START)}
for m, r in strict_unsafe.items():
    print(f"strict unsafe rate {m:26s} {r['value']:.3f} [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}]")
OUT.write_text(json.dumps({"meta": {"models": {"no_kl": NOKL, "swipo_s": SWIPO_S, "start": START},
                                    "gap": "refusal: strict minus permissive per prompt, first turn; harm: permissive minus strict Llama Guard 3 "
                                           "unsafe rate on the full answer", "ci": "95% BCa, 10,000 resamples over prompts, paired"},
                           "gaps": res, "strict_unsafe_rate": strict_unsafe}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
