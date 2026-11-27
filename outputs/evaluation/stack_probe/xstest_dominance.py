"""XSTest operating points under the LLM judge (models as trained x strict/permissive contract): the non-dominated set by point
estimate, and for each dominated point the share of 10,000 prompt resamples (safe and unsafe prompts resampled jointly across models,
so pairs stay paired) in which its dominator keeps dominating it. CPU.
    python -u outputs/evaluation/stack_probe/xstest_dominance.py 2>&1 | tee logs/xstest_dominance.log
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
ROOT = project_root / "outputs/evaluation/stop_eot"
LABELS, ANSWERS = ROOT / "refusal_judge_xstest", ROOT / X["dir_name"]
OUT = project_root / "outputs/evaluation/contract_gap/xstest_dominance_judge.json"
ARMS = ("strict", "permissive")


def load(model: str, arm: str):
    j = pd.read_csv(LABELS / model / f"{arm}.csv").set_index("prompt_idx")["is_refusal_judge"].astype(bool).sort_index()
    lab = pd.read_csv(ANSWERS / model / f"{arm}_responses.csv", usecols=["prompt_idx", "label"]).set_index("prompt_idx")["label"]
    return j, lab.reindex(j.index)


points, index, ref_label = {}, None, None
for d in sorted(p for p in LABELS.iterdir() if p.is_dir()):
    for arm in ARMS:
        j, lab = load(d.name, arm)
        if index is None:
            index, ref_label = j.index, lab
        if not (j.index.equals(index) and lab.equals(ref_label)):
            raise SystemExit(f"FATAL: {d.name} {arm} covers other prompts or labels than the first model")
        points[f"{d.name}|{arm}"] = j.to_numpy()
unsafe, safe = (ref_label == "unsafe").to_numpy(), (ref_label == "safe").to_numpy()


def coords(refusals: np.ndarray, u_idx: np.ndarray, s_idx: np.ndarray):
    """(refusal rate on unsafe prompts, answer rate on safe prompts) on the given prompt indices."""
    return refusals[u_idx].mean(), 1 - refusals[s_idx].mean()


u_all, s_all = np.flatnonzero(unsafe), np.flatnonzero(safe)
est = {k: coords(v, u_all, s_all) for k, v in points.items()}


def dominates(a, b) -> bool:
    return a[0] >= b[0] and a[1] >= b[1] and (a[0] > b[0] or a[1] > b[1])


front = [k for k in est if not any(dominates(est[o], est[k]) for o in est if o != k)]
dominated = {}
for k in est:
    if k in front:
        continue
    doms = [o for o in est if o != k and dominates(est[o], est[k])]
    best = max(doms, key=lambda o: (est[o][0] - est[k][0]) + (est[o][1] - est[k][1]))  # the dominator with the largest margin
    dominated[k] = {"by": best, "all_dominators": doms}
rng = np.random.default_rng(X["seed"])  # the XSTest suite seed (configs/pipeline.yaml xstest_contract.seed)
n = B["n_iterations"]
hits = {k: 0 for k in dominated}
pbar = make_pbar(total=n, desc="xstest_dominance", unit="resample")
for _ in range(n):
    u_idx, s_idx = rng.choice(u_all, len(u_all)), rng.choice(s_all, len(s_all))
    for k, v in dominated.items():
        if dominates(coords(points[v["by"]], u_idx, s_idx), coords(points[k], u_idx, s_idx)):
            hits[k] += 1
    pbar.update(1)
pbar.close()
for k, v in dominated.items():
    v["share_of_resamples_dominated"] = hits[k] / n
res = {"points": {k: {"refusal_unsafe": float(a), "answer_safe": float(b)} for k, (a, b) in est.items()},
       "non_dominated": front, "dominated": dominated}
print("non-dominated:", ", ".join(front))
for k, v in sorted(dominated.items(), key=lambda kv: -kv[1]["share_of_resamples_dominated"]):
    print(f"  {k:36s} dominated by {v['by']:36s} in {v['share_of_resamples_dominated']:.3f} of resamples")
OUT.write_text(json.dumps({"meta": {"scorer": "LLM refusal judge, first turn", "resamples": n,
                                    "resampling": "unsafe and safe prompts resampled with replacement, the same draw for every model",
                                    "dominance": "at least as high on both axes and higher on one"}, **res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
