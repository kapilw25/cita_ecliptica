"""Two-contract SwiPO (G1a, G1b; src/train/g1_contracts_build.py data) against the one-contract SwiPO-R on the same chain and against
their shared start (the DPO adapter alone): strict-minus-permissive refusal gap, paired over the 1,222 prompts, LLM judge and first-turn
phrase heuristic; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/two_contract_g1.py 2>&1 | tee logs/two_contract_g1.log
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
OUT = project_root / "outputs/evaluation/contract_gap/two_contract_g1.json"
ONE = "CITA_Instruct_AsTrained"   # SwiPO-R: one contract, chain base + DPO adapter
START = "DPO_Instruct"            # the DPO adapter alone, the start of SwiPO-R and of both G1 runs
TWO = {"G1a": "G1a_SwiPO2C_Instruct_AsTrained", "G1b": "G1b_SwiPOTwoTier_Instruct_AsTrained"}
SCORERS = {"judge": "is_refusal_judge", "phrase_first_turn": "is_refusal_heuristic_first_turn"}
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def gaps(model: str, col: str) -> pd.Series:
    s = pd.read_csv(LABELS / model / "strict.csv").set_index("prompt_idx")[col].astype(float)
    p = pd.read_csv(LABELS / model / "permissive.csv").set_index("prompt_idx")[col].astype(float)
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {model} strict and permissive labels cover different prompts")
    return s - p


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x,), MEAN, paired=False)
    return {"value": float(x.mean()), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


res = {}
for tag, model in TWO.items():
    res[tag] = {"model": model}
    for name, col in SCORERS.items():
        g, one, start = gaps(model, col), gaps(ONE, col), gaps(START, col)
        if not (g.index.equals(one.index) and g.index.equals(start.index)):
            raise SystemExit(f"FATAL: {model}, {ONE} and {START} were judged on different prompts")
        res[tag][name] = {"gap": interval(g.to_numpy()), "minus_one_contract": interval((g - one).to_numpy()),
                          "minus_start": interval((g - start).to_numpy())}
        r = res[tag][name]
        print(f"{tag} {name:18s} gap {r['gap']['value']:+.3f} [{r['gap']['ci'][0]:+.3f}, {r['gap']['ci'][1]:+.3f}] | "
              f"minus SwiPO-R {r['minus_one_contract']['value']:+.3f} [{r['minus_one_contract']['ci'][0]:+.3f}, "
              f"{r['minus_one_contract']['ci'][1]:+.3f}] | minus start {r['minus_start']['value']:+.3f} "
              f"[{r['minus_start']['ci'][0]:+.3f}, {r['minus_start']['ci'][1]:+.3f}]")
OUT.write_text(json.dumps({"meta": {"gap": "strict minus permissive refusal rate per prompt, first turn",
                                    "one_contract": ONE, "start": START, "labels": str(LABELS.relative_to(project_root)),
                                    "training_data": "src/train/g1_contracts_build.py: PKU-SafeRLHF train pairs whose safety and "
                                                     "helpfulness labels disagree; strict contract prefers the safer response, "
                                                     "permissive the more helpful one (configs/pipeline.yaml g1_contracts)",
                                    "ci": "95% BCa, 10,000 resamples over prompts, paired"},
                           "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
