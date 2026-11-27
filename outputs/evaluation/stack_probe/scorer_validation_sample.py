"""Bench2Evidence scorer check: extend the Safety Answer Check items (100 random as-trained answers) with 200 answers stratified by
phrase / judge / Llama Guard agreement (configs/pipeline.yaml scorer_validation); every item shows the first assistant turn and the
run-on text apart. items.json is what raters see; key.csv holds model, contract and the three automatic labels. CPU.
    python -u outputs/evaluation/stack_probe/scorer_validation_sample.py 2>&1 | tee logs/scorer_validation_sample.log
"""
import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.utils.eval.first_turn import BOUNDARY, first_turn  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
V = CFG["scorer_validation"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
EVAL = project_root / CFG["paths"]["evaluation_dir"]
CS, JUDGE, GUARD = EVAL / "Conditional_Safety_Evaluation", EVAL / "refusal_judge", EVAL / "floor_harm/conditional_safety/full"
OUT = EVAL / "human_check"
ARMS = ("strict", "permissive")


def split(text: str) -> tuple:
    """(first assistant turn, run-on text after it) as the scorers saw them."""
    m = BOUNDARY.search(text)
    return first_turn(text), (text[m.start():] if m else "")


def pool(model: str) -> pd.DataFrame:
    rows = []
    for arm in ARMS:
        a = pd.read_csv(CS / model / f"{arm}_responses.csv", keep_default_na=False).set_index("prompt_idx")
        j = pd.read_csv(JUDGE / model / f"{arm}.csv").set_index("prompt_idx")
        g = pd.read_csv(GUARD / f"{model}_{arm}_labels.csv").set_index("prompt_idx")
        if not (a.index.sort_values().equals(j.index.sort_values()) and a.index.sort_values().equals(g.index.sort_values())):
            raise SystemExit(f"FATAL: {model} {arm}: answers, judge and Llama Guard labels cover different prompts")
        d = pd.DataFrame({"prompt": a["prompt"], "response": a["response"].astype(str), "harm_categories": a["harm_categories"],
                          "phrase": j["is_refusal_heuristic_first_turn"].astype(bool), "phrase_full": j["is_refusal_heuristic_full"].astype(bool),
                          "judge": j["is_refusal_judge"].astype(bool), "guard": g["unsafe"].astype(float) > 0.5})
        d["model"], d["contract"] = model, arm
        rows.append(d.reset_index())
    return pd.concat(rows, ignore_index=True)


rng = np.random.default_rng(V["seed"])
old_items = json.load(open(OUT / "items.json"))
old_key = pd.read_csv(OUT / "key.csv", keep_default_na=False)
if len(old_items) != len(old_key) or [x["id"] for x in old_items] != old_key["item_id"].tolist():
    raise SystemExit("FATAL: items.json and key.csv disagree; rebuild them with src/eval/human_check_build.py first")
if any("reply" in x for x in old_items):
    raise SystemExit("FATAL: items.json is already extended; this script runs once on the 100-item set")
taken = set(zip(old_key["model"], old_key["contract"], old_key["prompt_idx"].astype(int)))
P = pd.concat([pool(m) for m in V["models"]], ignore_index=True)
P = P[[(m, c, int(i)) not in taken for m, c, i in zip(P["model"], P["contract"], P["prompt_idx"])]]
new = []
for s in V["strata"]:
    sel = (P["phrase"] == s["phrase"]) & (P["judge"] == s["judge"])
    if "guard" in s:
        sel &= P["guard"] == s["guard"]
    cand = P[sel]
    if len(cand) < s["n"]:
        raise SystemExit(f"FATAL: stratum {s['name']} has {len(cand)} answers, needs {s['n']}")
    w = 1.0 / cand["model"].map(cand["model"].value_counts()).to_numpy()  # equal weight per model
    pick = cand.iloc[rng.choice(len(cand), s["n"], replace=False, p=w / w.sum())].copy()
    pick["stratum"] = s["name"]
    new.append(pick)
    P = P.drop(pick.index)
    print(f"{s['name']:15s} {s['n']:3d} of {len(cand):5d} | " + ", ".join(f"{k} {v}" for k, v in pick["model"].value_counts().items()))
new = pd.concat(new).sample(frac=1.0, random_state=V["seed"]).reset_index(drop=True)
# the first 100: add their automatic labels and the reply / run-on split
lab = {(m, c): pool(m).set_index(["contract", "prompt_idx"]) for m in old_key["model"].unique() for c in ARMS}
items, key = [], []
for x, (_, k) in zip(old_items, old_key.iterrows()):
    r = lab[(k["model"], k["contract"])].loc[(k["contract"], int(k["prompt_idx"]))]
    if r["response"] != x["response"]:
        raise SystemExit(f"FATAL: {x['id']}: the stored answer differs from the evaluation CSV")
    reply, runon = split(x["response"])
    items.append({"id": x["id"], "prompt": x["prompt"], "reply": reply, "runon": runon})
    key.append({"item_id": x["id"], "prompt_idx": int(k["prompt_idx"]), "model": k["model"], "contract": k["contract"],
                "floor": bool(set(ast.literal_eval(r["harm_categories"])) & FLOOR), "stratum": "random_astrained",
                "phrase_first_turn": bool(r["phrase"]), "phrase_full": bool(r["phrase_full"]), "judge": bool(r["judge"]), "guard": bool(r["guard"])})
for i, r in new.iterrows():
    iid = f"h{len(old_items) + i + 1:03d}"
    reply, runon = split(r["response"])
    items.append({"id": iid, "prompt": r["prompt"], "reply": reply, "runon": runon})
    key.append({"item_id": iid, "prompt_idx": int(r["prompt_idx"]), "model": r["model"], "contract": r["contract"],
                "floor": bool(set(ast.literal_eval(r["harm_categories"])) & FLOOR), "stratum": r["stratum"],
                "phrase_first_turn": bool(r["phrase"]), "phrase_full": bool(r["phrase_full"]), "judge": bool(r["judge"]), "guard": bool(r["guard"])})
(OUT / "items_100.json").write_text(json.dumps(old_items, indent=1))  # the original set, kept for the record
(OUT / "items.json").write_text(json.dumps(items, indent=1))
pd.DataFrame(key).to_csv(OUT / "key_scorer.csv", index=False)
print(f"wrote {len(items)} items to {(OUT / 'items.json').relative_to(project_root)} (first 100 unchanged in content, now split into reply and "
      f"run-on) and the hidden key to key_scorer.csv; the 100-item original is items_100.json")
