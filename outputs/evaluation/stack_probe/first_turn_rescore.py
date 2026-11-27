"""Conditional Safety refusal gap re-scored on the FIRST assistant turn only: as-trained models do not stop at <|eot_id|> (base
generation_config stops on <|end_of_text|>), so answers run on into invented user/assistant turns that the phrase heuristic also reads.
Cuts each answer at the first decoded role header ("user\\n\\n" / "assistant\\n\\n") and re-applies the same heuristic. 95% BCa, CPU.
    python -u outputs/evaluation/stack_probe/first_turn_rescore.py 2>&1 | tee logs/first_turn_rescore.log
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.conditional_safety import detect_refusal_heuristic  # noqa: E402
from src.eval.floor_leakage import ci  # noqa: E402

CS = project_root / "outputs/evaluation/Conditional_Safety_Evaluation"
MODELS = ["Llama31_Base_Prompted", "SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained",
          "CITA_Instruct_AsTrained", "CITA_Instruct_Chain", "DPO_Instruct", "PPO_Instruct", "GRPO_Instruct", "CITA_Instruct",
          "CITA_Instruct_Chain_FinalOnly", "Llama31_Instruct_Prompted"]
BOUNDARY = re.compile(r"(?:user|assistant)\n\n")
TAIL = re.compile(r"(?:user|assistant)\s*$")  # a header cut off by the token cap


def first_turn(text) -> str:
    text = text if isinstance(text, str) else ""
    m = BOUNDARY.search(text)
    head = text[:m.start()] if m else text
    return TAIL.sub("", head)


def load(model: str):
    arms = {}
    for arm in ("strict", "permissive"):
        d = pd.read_csv(CS / model / f"{arm}_responses.csv").sort_values("prompt_idx")
        cut = d.response.map(first_turn)
        arms[arm] = {"ids": d.prompt_idx.to_numpy(), "full": d.is_refusal.astype(float).to_numpy(),
                     "first": cut.map(lambda t: detect_refusal_heuristic(t)["is_refusal"]).astype(float).to_numpy(),
                     "cut_rate": float(d.response.fillna("").str.contains(BOUNDARY).mean()),
                     "first_words": float(cut.str.split().str.len().mean())}
    if not np.array_equal(arms["strict"]["ids"], arms["permissive"]["ids"]):
        raise RuntimeError(f"{model}: arms scored different prompts")
    return arms


def mean(a, axis=-1):
    return np.mean(a, axis=axis)


def diff(a, b, axis=-1):
    return np.mean(a, axis=axis) - np.mean(b, axis=axis)


out = {}
for m in MODELS:
    a = load(m)
    d_full = a["strict"]["full"] - a["permissive"]["full"]
    d_first = a["strict"]["first"] - a["permissive"]["first"]
    f_lo_hi, _ = ci((d_full,), mean, paired=True)
    g_lo_hi, method = ci((d_first,), mean, paired=True)
    x_lo_hi, _ = ci((d_first, d_full), diff, paired=True)
    out[m] = {"n": int(len(d_full)), "gap_full_text": float(d_full.mean()), "gap_full_text_ci": f_lo_hi,
              "gap_first_turn": float(d_first.mean()), "gap_first_turn_ci": g_lo_hi,
              "first_minus_full": float(d_first.mean() - d_full.mean()), "first_minus_full_ci": x_lo_hi, "ci_method": method,
              "refusal_first_turn": {k: float(a[k]["first"].mean()) for k in ("strict", "permissive")},
              "refusal_full_text": {k: float(a[k]["full"].mean()) for k in ("strict", "permissive")},
              "runon_rate": {k: a[k]["cut_rate"] for k in ("strict", "permissive")},
              "first_turn_words": {k: a[k]["first_words"] for k in ("strict", "permissive")}}
    r = out[m]
    print(f"{m:30s} run-on {r['runon_rate']['strict']:.2f} | full {r['gap_full_text']:+.3f} | first turn {r['gap_first_turn']:+.3f} "
          f"[{g_lo_hi[0]:+.3f}, {g_lo_hi[1]:+.3f}] | refusal S/P first {r['refusal_first_turn']['strict']:.2f}/"
          f"{r['refusal_first_turn']['permissive']:.2f} full {r['refusal_full_text']['strict']:.2f}/{r['refusal_full_text']['permissive']:.2f}"
          f" | words {r['first_turn_words']['strict']:.0f}")
path = project_root / "outputs/evaluation/contract_gap/first_turn_rescore.json"
json.dump({"meta": {"statistic": "strict minus permissive refusal rate, phrase heuristic on the first assistant turn",
                    "boundary_regex": BOUNDARY.pattern, "suite": "conditional_safety"}, "models": out}, open(path, "w"), indent=2)
print(f"wrote {path}")
