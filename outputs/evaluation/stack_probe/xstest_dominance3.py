"""XSTest operating points with harm as a third objective (MultiRobust round-5 judge C2): refusal of unsafe prompts (LLM judge, higher),
answers to safe prompts (higher), Llama Guard 3 unsafe rate on unsafe prompts (lower); non-dominated set by point estimate and, for each
dominated point, the share of 10,000 joint prompt resamples in which its dominator keeps dominating it. CPU.
    python -u outputs/evaluation/stack_probe/xstest_dominance3.py 2>&1 | tee logs/xstest_dominance3.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.utils.progress import make_pbar  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
X = CFG["xstest_contract"]
B = CFG["bootstrap"]
LABELS = project_root / "outputs/evaluation/stop_eot/refusal_judge_xstest"
HARM = project_root / "outputs/evaluation/floor_harm/xstest/full"
OUT = project_root / "outputs/evaluation/contract_gap/xstest_dominance_judge_harm.json"
ARMS = ("strict", "permissive")


def load(model: str, arm: str):
    j = pd.read_csv(LABELS / model / f"{arm}.csv").set_index("prompt_idx").sort_index()["is_refusal_judge"].astype(bool)
    h = pd.read_csv(HARM / f"{model}_{arm}_labels.csv").set_index("prompt_idx").sort_index()
    if not j.index.equals(h.index):
        raise SystemExit(f"FATAL: {model} {arm}: judge and Llama Guard labels cover different prompts")
    return j.to_numpy(float), h["unsafe"].astype(float).to_numpy(), h["label"]


points, ref_label = {}, None
for d in sorted(p for p in LABELS.iterdir() if p.is_dir()):
    for arm in ARMS:
        j, u, lab = load(d.name, arm)
        if ref_label is None:
            ref_label = lab
        if not lab.equals(ref_label):
            raise SystemExit(f"FATAL: {d.name} {arm}: prompt labels differ from the first model")
        points[f"{d.name}|{arm}"] = (j, u)
unsafe_idx, safe_idx = np.flatnonzero((ref_label == "unsafe").to_numpy()), np.flatnonzero((ref_label == "safe").to_numpy())


def coords(p, ui, si):
    """(refusal of unsafe prompts, answers to safe prompts, unsafe rate on unsafe prompts)."""
    j, u = p
    return j[ui].mean(), 1 - j[si].mean(), u[ui].mean()


def dominates(a, b) -> bool:
    ge = a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2]
    return ge and (a[0] > b[0] or a[1] > b[1] or a[2] < b[2])


est = {k: coords(v, unsafe_idx, safe_idx) for k, v in points.items()}
front = [k for k in est if not any(dominates(est[o], est[k]) for o in est if o != k)]
dominated = {}
for k in est:
    if k in front:
        continue
    doms = [o for o in est if o != k and dominates(est[o], est[k])]
    best = max(doms, key=lambda o: (est[o][0] - est[k][0]) + (est[o][1] - est[k][1]) + (est[k][2] - est[o][2]))
    dominated[k] = {"by": best, "all_dominators": doms}
rng = np.random.default_rng(X["seed"])
n = B["n_iterations"]
hits = {k: 0 for k in dominated}
free = {k: 0 for k in est}  # resamples in which the point is non-dominated by every other point (round-6 judge C2)
pbar = make_pbar(total=n, desc="xstest_dominance3", unit="resample")
for _ in range(n):
    ui, si = rng.choice(unsafe_idx, len(unsafe_idx)), rng.choice(safe_idx, len(safe_idx))
    c = {k: coords(v, ui, si) for k, v in points.items()}
    for k, v in dominated.items():
        if dominates(c[v["by"]], c[k]):
            hits[k] += 1
    for k in est:
        if not any(dominates(c[o], c[k]) for o in est if o != k):
            free[k] += 1
    pbar.update(1)
pbar.close()
for k, v in dominated.items():
    v["share_of_resamples_dominated"] = hits[k] / n
print("share of resamples non-dominated:", ", ".join(f"{k} {free[k] / n:.3f}" for k in sorted(est, key=lambda k: -free[k])))
print("non-dominated (3 objectives):", ", ".join(f"{k} {tuple(round(x, 3) for x in est[k])}" for k in front))
for k, v in sorted(dominated.items(), key=lambda kv: -kv[1]["share_of_resamples_dominated"]):
    print(f"  {k:36s} {tuple(round(x, 3) for x in est[k])} dominated by {v['by']:36s} in {v['share_of_resamples_dominated']:.3f} of resamples")
OUT.write_text(json.dumps({"meta": {"objectives": ["refusal of unsafe prompts (LLM judge, higher)", "answers to safe prompts (judge, higher)",
                                                   "Llama Guard 3 unsafe rate on unsafe prompts (lower)"], "resamples": n,
                                    "resampling": "unsafe and safe prompts resampled with replacement, the same draw for every model"},
                           "points": {k: dict(zip(("refusal_unsafe", "answer_safe", "unsafe_rate"), map(float, v))) for k, v in est.items()},
                           "non_dominated": front, "dominated": dominated,
                           "share_non_dominated": {k: free[k] / n for k in est}}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
