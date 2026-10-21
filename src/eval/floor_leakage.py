"""Floor leakage: Conditional Safety refusal rates per harm category, strict vs permissive, BCa 95% CIs. CPU-only.
    python -u src/eval/floor_leakage.py 2>&1 | tee logs/floor_leakage.log
"""

import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import bootstrap
from tqdm import tqdm

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
SAFETY_DIR = project_root / CFG["paths"]["evaluation_dir"] / CFG["score_table"]["suite_dirs"]["conditional_safety"]
OUT_DIR = project_root / CFG["paths"]["floor_leakage_dir"]
TRAINERS = CFG["score_table"]["trainers"]
TOL = CFG["score_table"]["reproduce_tol"]["exact"]
BOOT = CFG["bootstrap"]
BATCH = CFG["score_table"]["bootstrap_batch"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
VARIANT = CFG["floor_leakage"]["variant"]

MEAN = lambda a, axis=-1: np.mean(a, axis=axis)  # noqa: E731
GAP = lambda s, p, axis=-1: np.mean(s, axis=axis) - np.mean(p, axis=axis)  # noqa: E731


def ci(arrays, stat, paired):
    """BCa interval; a rate at 0 or 1 (degenerate bootstrap distribution) falls back to the percentile interval."""
    res = bootstrap(arrays, stat, paired=paired, vectorized=True, n_resamples=BOOT["n_iterations"],
                    confidence_level=BOOT["confidence_level"], method=BOOT["method"], batch=BATCH,
                    random_state=np.random.default_rng(0))
    lo, hi = float(res.confidence_interval.low), float(res.confidence_interval.high)
    if np.isfinite(lo) and np.isfinite(hi):
        return [lo, hi], BOOT["method"]
    dist, point = res.bootstrap_distribution, float(stat(*arrays))
    if dist.min() >= point or dist.max() <= point:
        q = (1 - BOOT["confidence_level"]) / 2
        print(f"BCa undefined: estimate {point:.4f} is at the edge of its bootstrap distribution; percentile interval reported")
        return [float(x) for x in np.quantile(dist, [q, 1 - q])], "percentile"
    raise RuntimeError(f"bootstrap returned a non-finite interval (estimate {point:.4f})")


def load(model: str):
    """Strict and permissive answers to the same prompts, aligned on prompt_idx; FATAL on any mismatch."""
    d = SAFETY_DIR / model
    s, p = pd.read_csv(d / "strict_responses.csv"), pd.read_csv(d / "permissive_responses.csv")
    if set(s.prompt_idx) != set(p.prompt_idx) or s.prompt_idx.duplicated().any() or p.prompt_idx.duplicated().any():
        raise RuntimeError(f"{model}: strict and permissive prompt sets differ or repeat")
    m = s.merge(p[["prompt_idx", "prompt", "is_refusal"]], on="prompt_idx", suffixes=("_s", "_p")).sort_values("prompt_idx")
    if (m.prompt_s != m.prompt_p).any():
        raise RuntimeError(f"{model}: prompt text differs between arms")
    stored = json.load(open(d / "metrics.json"))["adaptation_score"]
    gap = m.is_refusal_s.mean() - m.is_refusal_p.mean()
    if abs(abs(gap) - stored) > TOL:
        raise RuntimeError(f"{model}: recomputed |gap| {abs(gap):.10f} != stored {stored:.10f}")
    cats = m.harm_categories.map(ast.literal_eval)
    return m.prompt_idx.to_numpy(), cats, m.is_refusal_s.to_numpy(dtype=float), m.is_refusal_p.to_numpy(dtype=float)


def rates(s, p):
    s_ci, s_m = ci((s,), MEAN, paired=True)
    p_ci, p_m = ci((p,), MEAN, paired=True)
    g_ci, g_m = ci((s, p), GAP, paired=True)
    return {"n": int(len(s)), "strict": float(s.mean()), "strict_ci": s_ci, "permissive": float(p.mean()), "permissive_ci": p_ci,
            "gap": float(s.mean() - p.mean()), "gap_ci": g_ci, "ci_method": sorted({s_m, p_m, g_m})}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    models = [f"{t}_{VARIANT}" for t in TRAINERS]
    loaded = {m: load(m) for m in models}
    ids0 = loaded[models[0]][0]
    if any(not np.array_equal(ids0, loaded[m][0]) for m in models):
        raise RuntimeError("trainers were scored on different prompt sets")
    cats = loaded[models[0]][1]
    all_cats = sorted({c for cs in cats for c in cs})
    missing = FLOOR - set(all_cats)
    if missing:
        raise RuntimeError(f"floor categories not in the data: {sorted(missing)}")
    is_floor = cats.map(lambda cs: bool(FLOOR & set(cs))).to_numpy()
    pbar = tqdm(total=len(models) * (3 + len(all_cats)), desc="floor_leakage", unit="cell")
    out = {}
    for m in models:
        _, _, s, p = loaded[m]
        r = out[m] = {"floor": rates(s[is_floor], p[is_floor]), "non_floor": rates(s[~is_floor], p[~is_floor])}
        pbar.update(2)
        d_f, d_n = s[is_floor] - p[is_floor], s[~is_floor] - p[~is_floor]
        dd_ci, dd_m = ci((d_f, d_n), lambda a, b, axis=-1: np.mean(a, axis=axis) - np.mean(b, axis=axis), paired=False)
        r["gap_floor_minus_non_floor"] = {"value": float(d_f.mean() - d_n.mean()), "ci": dd_ci, "ci_method": dd_m}
        pbar.update(1)
        r["per_category"] = {}
        for c in all_cats:
            k = cats.map(lambda cs, c=c: c in cs).to_numpy()
            r["per_category"][c] = rates(s[k], p[k])
            pbar.update(1)
        f, n, dd = r["floor"], r["non_floor"], r["gap_floor_minus_non_floor"]
        print(f"{m:15s} floor n={f['n']:4d} strict {f['strict']:.3f} permissive {f['permissive']:.3f} [{f['permissive_ci'][0]:.3f}, {f['permissive_ci'][1]:.3f}]"
              f" gap {f['gap']:+.3f} | non-floor n={n['n']:4d} gap {n['gap']:+.3f} | gap diff {dd['value']:+.3f} [{dd['ci'][0]:+.3f}, {dd['ci'][1]:+.3f}]")
    pbar.close()
    meta = {"bootstrap": BOOT, "floor_categories": sorted(FLOOR), "variant": VARIANT, "n_prompts": int(len(ids0)),
            "n_floor_prompts": int(is_floor.sum()), "resampling_unit": "prompt",
            "note": "floor = any listed PKU-SafeRLHF harm category; set fixed in configs/pipeline.yaml before computing; "
                    "gap = strict minus permissive refusal rate (paired); gap diff resamples floor and non-floor prompts independently"}
    path = OUT_DIR / "floor_leakage.json"
    json.dump({"meta": meta, "models": out}, open(path, "w"), indent=2)
    print(f"wrote {path} ({len(models)} models, {int(is_floor.sum())} floor of {len(ids0)} prompts, {len(all_cats)} categories)")


if __name__ == "__main__":
    main()
