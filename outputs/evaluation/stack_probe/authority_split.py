"""LoyalAgents authority test split by direction (round-5 judge C2): a user turn that loosens (system strict, user permissive) or tightens
(system permissive, user strict) the deployer's contract, each against the same system contract alone; phrase heuristic, and the LLM judge
on the first turn once refusal_judge.py --contract_slot conflict has run; paired over the 1,222 prompts, paper decoding; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/authority_split.py 2>&1 | tee logs/authority_split.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

EVAL = project_root / "outputs/evaluation"
ALONE, CONFLICT = EVAL / "Conditional_Safety_Evaluation", EVAL / "contract_slot_conflict/Conditional_Safety_Evaluation"
OUT = EVAL / "contract_gap/authority_split.json"
J_ALONE, J_CONFLICT = EVAL / "refusal_judge", EVAL / "contract_slot_conflict/refusal_judge"
MODELS = ["Llama31_Instruct_Prompted", "Llama31_Base_Prompted", "SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained",
          "GRPO_Instruct_AsTrained", "CITA_Instruct_AsTrained", "CITA_Instruct_Chain"]
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def refusals(root: Path, model: str, arm: str) -> pd.Series:
    return pd.read_csv(root / model / f"{arm}_responses.csv", usecols=["prompt_idx", "is_refusal"]).set_index("prompt_idx").sort_index()[
        "is_refusal"].astype(bool).astype(float)


def judged(root: Path, model: str, arm: str) -> pd.Series:
    return pd.read_csv(root / model / f"{arm}.csv").set_index("prompt_idx").sort_index()["is_refusal_judge"].astype(bool).astype(float)


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x,), MEAN, paired=False)
    return {"value": float(x.mean()), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


res = {}
for m in MODELS:
    res[m] = {}
    for arm, name in (("strict", "loosen"), ("permissive", "tighten")):  # arm = the system contract; the user turn carries the other
        a, c = refusals(ALONE, m, arm), refusals(CONFLICT, m, arm)
        if not a.index.equals(c.index):
            raise SystemExit(f"FATAL: {m} {arm}: the system-only and conflict runs cover different prompts")
        res[m][name] = {"system_only": interval(a.to_numpy()), "with_user_turn": interval(c.to_numpy()),
                        "change": interval((c - a).to_numpy())}
    if (J_CONFLICT / m).exists():  # second instrument, first turn
        for arm, name in (("strict", "loosen_judge"), ("permissive", "tighten_judge")):
            a, c = judged(J_ALONE, m, arm), judged(J_CONFLICT, m, arm)
            if not a.index.equals(c.index):
                raise SystemExit(f"FATAL: {m} {arm}: judge labels of the two runs cover different prompts")
            res[m][name] = {"system_only": interval(a.to_numpy()), "with_user_turn": interval(c.to_numpy()), "change": interval((c - a).to_numpy())}
        lj, tj = res[m]["loosen_judge"]["change"], res[m]["tighten_judge"]["change"]
        print(f"{m:28s} JUDGE user loosens {lj['value']:+.3f} [{lj['ci'][0]:+.3f}, {lj['ci'][1]:+.3f}] | tightens {tj['value']:+.3f} "
              f"[{tj['ci'][0]:+.3f}, {tj['ci'][1]:+.3f}]")
    lo_, ti = res[m]["loosen"]["change"], res[m]["tighten"]["change"]
    print(f"{m:28s} user loosens: refusal {lo_['value']:+.3f} [{lo_['ci'][0]:+.3f}, {lo_['ci'][1]:+.3f}] | user tightens: "
          f"{ti['value']:+.3f} [{ti['ci'][0]:+.3f}, {ti['ci'][1]:+.3f}]")
OUT.write_text(json.dumps({"meta": {"instrument": "refusal-phrase heuristic on the full answer (is_refusal), paper decoding",
                                    "loosen": "system strict + user permissive, minus system strict alone (negative = the user loosened)",
                                    "tighten": "system permissive + user strict, minus system permissive alone (positive = the user tightened)",
                                    "ci": "95% BCa over prompts, 10,000 resamples, paired"}, "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
