"""Cost of run-on answers (Bench2Evidence, Claude v6 C5): on Conditional Safety with the paper's decoding, the share of answers that run
past the model's first turn and the share of generated words that fall after it, per model as trained; 95% BCa over answers. CPU.
    python -u outputs/evaluation/stack_probe/runon_cost.py 2>&1 | tee logs/runon_cost.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402
from src.utils.eval.first_turn import first_turn  # noqa: E402

DIR = project_root / "outputs/evaluation/Conditional_Safety_Evaluation"
OUT = project_root / "outputs/evaluation/contract_gap/runon_cost.json"
MODELS = ["SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained", "CITA_Instruct_AsTrained",
          "CITA_Instruct_Chain"]
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x.astype(float),), MEAN, paired=False)
    return {"value": float(np.mean(x)), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


res = {}
for m in MODELS:
    df = pd.concat([pd.read_csv(DIR / m / f"{arm}_responses.csv", keep_default_na=False) for arm in ("strict", "permissive")])
    full = df["response"].astype(str)
    turn = full.map(first_turn)
    w_full = full.str.split().str.len().to_numpy(float)
    w_turn = turn.str.split().str.len().to_numpy(float)
    if (w_turn > w_full).any():
        raise SystemExit(f"FATAL: {m}: a first turn is longer than its answer")
    runs_on = (w_full > w_turn)
    extra = np.where(w_full > 0, (w_full - w_turn) / np.maximum(w_full, 1), 0.0)
    res[m] = {"runs_on": interval(runs_on), "share_of_words_after_first_turn": interval(extra),
              "mean_words_full": float(w_full.mean()), "mean_words_first_turn": float(w_turn.mean())}
    r = res[m]
    print(f"{m:26s} runs on {r['runs_on']['value']:.3f} [{r['runs_on']['ci'][0]:.3f}, {r['runs_on']['ci'][1]:.3f}] | words after first turn "
          f"{r['share_of_words_after_first_turn']['value']:.3f} [{r['share_of_words_after_first_turn']['ci'][0]:.3f}, "
          f"{r['share_of_words_after_first_turn']['ci'][1]:.3f}] | mean words {r['mean_words_full']:.0f} vs {r['mean_words_first_turn']:.0f}")
OUT.write_text(json.dumps({"meta": {"suite": "Conditional Safety, paper decoding (no stop at end of turn), both arms pooled",
                                    "first_turn": "src/utils/eval/first_turn.py", "unit": "whitespace words",
                                    "ci": "95% BCa over answers, 10,000 resamples"}, "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
