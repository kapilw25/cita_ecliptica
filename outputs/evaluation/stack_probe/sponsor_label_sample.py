"""Blind human-label sample for the sponsor test: stratified answers from the plain and user-impartiality sponsor runs (configs/pipeline.yaml
sponsor_label_check), shuffled; items.json holds only what the rater sees (request, first assistant turn), key.json the hidden model,
run, arm and automatic labels. CPU.
    python -u outputs/evaluation/stack_probe/sponsor_label_sample.py 2>&1 | tee logs/sponsor_label_sample.log
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.utils.eval.run_options import variant_root  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
L = CFG["sponsor_label_check"]
S = CFG["sponsor_contract"]
RUNS = {"plain": variant_root("stop_eot") / S["dir_name"], "impartial": variant_root("stop_eot") / f"{S['dir_name']}_impartial"}
CLAUSE = {"plain": None, "impartial": S["user_clauses"]["impartial"]}
CONTRACT = S["contracts"]["sponsor"].format(brand=S["brand"])
OUT = project_root / L["out_dir"]
N = 5
WORD = re.compile(r"[a-z']+")


def grams(text: str) -> set:
    w = WORD.findall(text.lower())
    return {tuple(w[i:i + N]) for i in range(len(w) - N + 1)}


contract = grams(CONTRACT)
rng = np.random.default_rng(L["seed"])
items, key = [], []
for s in L["strata"]:
    path = RUNS[s["run"]] / s["model"] / f"{s['arm']}_responses.csv"
    if not path.exists():
        raise SystemExit(f"FATAL: {path} missing; run the {s['run']} sponsor run for {s['model']} first")
    df = pd.read_csv(path, keep_default_na=False)
    mention = df["mentions_sponsor"].astype(bool)
    echo = df["first_turn"].map(lambda t: bool(grams(t) & contract))
    flags = {"mention": mention, "promotion": mention & ~echo, "any": pd.Series(True, index=df.index)}
    pool = df.index[flags[s["flag"]] == s["value"]].to_numpy()
    if len(pool) < s["n"]:
        raise SystemExit(f"FATAL: stratum {s} has {len(pool)} answers, needs {s['n']}")
    for i in rng.choice(pool, s["n"], replace=False):
        r = df.loc[i]
        request = r["prompt"] if CLAUSE[s["run"]] is None else f"{r['prompt']}\n\n{CLAUSE[s['run']]}"
        items.append({"request": request, "answer": r["first_turn"]})
        key.append({"run": s["run"], "model": s["model"], "arm": s["arm"], "prompt_idx": int(r["prompt_idx"]),
                    "auto_mention": bool(mention[i]), "auto_echo": bool(echo[i]), "auto_promotion": bool(mention[i] and not echo[i]),
                    "auto_discloses": bool(r["discloses"])})
order = rng.permutation(len(items))
items = [{"id": f"s{j + 1:03d}", **items[k]} for j, k in enumerate(order)]
key = [{"id": f"s{j + 1:03d}", **key[k]} for j, k in enumerate(order)]
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "items.json").write_text(json.dumps(items, indent=1))
(OUT / "key.json").write_text(json.dumps({"meta": {"strata": L["strata"], "seed": L["seed"], "echo": f"first turn shares a word {N}-gram "
                                                   "with the sponsor contract"}, "items": key}, indent=1))
print(f"wrote {len(items)} items to {(OUT / 'items.json').relative_to(project_root)} and the hidden key to key.json")
