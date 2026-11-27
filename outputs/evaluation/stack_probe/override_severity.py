"""Override severity (LoyalAgents): Llama Guard 3 unsafe rate when the user turn carries the opposite contract, minus the same system
contract alone, paired over the 1,222 Conditional Safety prompts (all and floor), per model as trained; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/override_severity.py 2>&1 | tee logs/override_severity.log
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

HARM = project_root / "outputs/evaluation/floor_harm"
CONFLICT, ALONE = HARM / "conflict/full", HARM / "conditional_safety/full"
OUT = project_root / "outputs/evaluation/contract_gap/override_severity.json"
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def interval(x: np.ndarray) -> dict:
    (lo, hi), method = ci((x.astype(float),), MEAN, paired=False)
    return {"value": float(np.mean(x)), "ci": [lo, hi], "ci_method": method, "n": int(len(x))}


def labels(root: Path, model: str, arm: str) -> pd.DataFrame:
    return pd.read_csv(root / f"{model}_{arm}_labels.csv").set_index("prompt_idx").sort_index()


meta = json.load(open(CONFLICT / "floor_harm_astrained.json"))["meta"]
floor_cats = set(meta["floor_categories"])
res = {}
for model in json.load(open(CONFLICT / "floor_harm_astrained.json"))["models"]:
    res[model] = {}
    for arm in ("strict", "permissive"):  # the system contract; in the conflict run the user turn carries the other one
        c, a = labels(CONFLICT, model, arm), labels(ALONE, model, arm)
        if not c.index.equals(a.index):
            raise SystemExit(f"FATAL: {model} {arm}: the conflict and system-only runs cover different prompts")
        floor = a["harm_categories"].map(lambda s: bool(set(ast.literal_eval(s)) & floor_cats)).to_numpy()  # list literal written by floor_harm_classify
        d = c["unsafe"].to_numpy(float) - a["unsafe"].to_numpy(float)
        res[model][arm] = {"system_only": interval(a["unsafe"].to_numpy(float)), "with_opposite_user_turn": interval(c["unsafe"].to_numpy(float)),
                           "override_minus_alone": interval(d), "override_minus_alone_floor": interval(d[floor])}
    r = res[model]["strict"]
    print(f"{model:28s} strict system: alone {r['system_only']['value']:.3f} -> user permissive {r['with_opposite_user_turn']['value']:.3f} | "
          f"change {r['override_minus_alone']['value']:+.3f} [{r['override_minus_alone']['ci'][0]:+.3f}, {r['override_minus_alone']['ci'][1]:+.3f}]"
          f" | floor {r['override_minus_alone_floor']['value']:+.3f} [{r['override_minus_alone_floor']['ci'][0]:+.3f}, "
          f"{r['override_minus_alone_floor']['ci'][1]:+.3f}]")
OUT.write_text(json.dumps({"meta": {"classifier": meta["classifier"], "pairing": "same prompt_idx, same system contract; the conflict run adds "
                                    "the opposite contract in the user turn", "floor_categories": meta["floor_categories"],
                                    "ci": "95% BCa over prompts, 10,000 resamples"}, "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
