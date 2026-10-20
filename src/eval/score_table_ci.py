"""Paper score table (Instruct score + Instruct-minus-NoInstruct delta) with paired BCa 95% CIs. CPU-only.
    python -u src/eval/score_table_ci.py 2>&1 | tee logs/score_table_ci.log
"""

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

from src.utils.eval.isd_metrics import ISDMetricsCalculator  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
EVAL_DIR = project_root / CFG["paths"]["evaluation_dir"]
OUT_DIR = project_root / CFG["paths"]["score_table_ci_dir"]
SUITES = CFG["score_table"]["suite_dirs"]
TRAINERS = CFG["score_table"]["trainers"]
OURS = CFG["score_table"]["ours"]
TOL = CFG["score_table"]["reproduce_tol"]
BOOT = CFG["bootstrap"]
BATCH = CFG["score_table"]["bootstrap_batch"]
EFF_VARIANTS = CFG["score_table"]["efficiency_variants"]


def _paired(a: pd.DataFrame, b: pd.DataFrame, key: str, col: str):
    """Align two per-item CSVs on `key`; FATAL if their item sets differ."""
    if set(a[key]) != set(b[key]) or a[key].duplicated().any() or b[key].duplicated().any():
        raise RuntimeError(f"item sets differ or repeat on '{key}' ({len(a)} vs {len(b)} rows)")
    m = a[[key, col]].merge(b[[key, col]], on=key, suffixes=("_a", "_b")).sort_values(key)
    return m[key].to_numpy(), m[f"{col}_a"].to_numpy(dtype=float), m[f"{col}_b"].to_numpy(dtype=float)


def _check(name: str, recomputed: float, stored: float, tol: float):
    if not np.isfinite(recomputed) or abs(recomputed - stored) > tol:
        raise RuntimeError(f"{name}: recomputed {recomputed:.10f} != stored {stored:.10f} (tol {tol})")


def load_truthfulqa(model: str):
    d = EVAL_DIR / SUITES["truthfulqa"] / model
    ids, h, c = _paired(pd.read_csv(d / "honest_responses.csv"), pd.read_csv(d / "confident_responses.csv"),
                        "question_idx", "has_uncertainty")
    _check(f"TruthfulQA {model}", h.mean() - c.mean(), json.load(open(d / "metrics.json"))["adaptation_score"], TOL["exact"])
    return ids, (h - c,)


def load_cond_safety(model: str):
    d = EVAL_DIR / SUITES["conditional_safety"] / model
    ids, s, p = _paired(pd.read_csv(d / "strict_responses.csv"), pd.read_csv(d / "permissive_responses.csv"),
                        "prompt_idx", "is_refusal")
    # stored score is the ABSOLUTE refusal-rate gap |strict - permissive| (paper: M3 = |STRICT - PERMIS.|)
    _check(f"Cond. Safety {model}", abs(s.mean() - p.mean()), json.load(open(d / "metrics.json"))["adaptation_score"], TOL["exact"])
    return ids, (s - p,)


def load_length(model: str):
    d = EVAL_DIR / SUITES["length_control"] / model
    ids, det, con = _paired(pd.read_csv(d / "detailed_responses.csv"), pd.read_csv(d / "concise_responses.csv"),
                            "prompt_idx", "word_count")
    _check(f"Length Ctrl {model}", det.sum() / con.sum(), json.load(open(d / "metrics.json"))["adaptation_score"], TOL["exact"])
    return ids, (det, con)


def load_ecliptica(model: str, calc: ISDMetricsCalculator):
    """Per-prompt mean fidelity and mean pairwise shift, via the scorer's own methods (cached per model)."""
    d = EVAL_DIR / SUITES["ecliptica"] / model
    cache = OUT_DIR / f"ecliptica_per_prompt_{model}.npz"
    if cache.exists():
        z = np.load(cache)
        return z["ids"], (z["F"], z["S"])
    # keep_default_na=False: an empty generation must stay "" (what the scorer embedded), not NaN
    df = pd.read_csv(d / f"{model}_isd_responses.csv", keep_default_na=False)
    fid = []
    for _, row in df.iterrows():
        exp = row["expected_characteristics"]
        exp = json.loads(exp.replace("'", '"')) if isinstance(exp, str) else exp
        fid.append(calc.evaluate_fidelity_embedding(row["response"], row["instruction_type"], exp, row["prompt_id"]).fidelity_score)
    df["fidelity"] = fid
    by_prompt = {}
    for _, row in df.iterrows():
        by_prompt.setdefault(int(row["prompt_id"]), {})[row["instruction_type"]] = row["response"]
    shift = {r.prompt_id: r.mean_shift for r in calc.calculate_semantic_shift(by_prompt)}
    per_prompt = df.groupby("prompt_id")["fidelity"].mean()
    ids = per_prompt.index.to_numpy()
    F = per_prompt.to_numpy()
    S = np.array([shift[int(i)] for i in ids])
    stored = json.load(open(d / f"{model}_isd_metrics.json"))
    _check(f"ECLIPTICA fidelity {model}", float(df["fidelity"].mean()), stored["mean_fidelity"], TOL["embedding"])
    _check(f"ECLIPTICA shift {model}", float(S.mean()), stored["mean_semantic_shift"], TOL["embedding"])
    _check(f"ECLIPTICA score {model}", float(df["fidelity"].mean() * S.mean()), stored["instruction_awareness_score"], TOL["embedding"])
    np.savez(cache, ids=ids, F=F, S=S)  # written only after all three reproduction checks pass
    return ids, (F, S)


# Statistic per suite on the per-item arrays (vectorized along `axis` for scipy).
STAT = {
    "truthfulqa": lambda d, axis=-1: np.mean(d, axis=axis),
    "conditional_safety": lambda d, axis=-1: np.abs(np.mean(d, axis=axis)),
    "length_control": lambda det, con, axis=-1: np.sum(det, axis=axis) / np.sum(con, axis=axis),
    "ecliptica": lambda F, S, axis=-1: np.mean(F, axis=axis) * np.mean(S, axis=axis),
}


def ci(arrays, stat, paired=True, axis=0, bounded=False):
    """BCa interval; `bounded` statistics (efficiency, floor 10) may sit at the edge of their bootstrap
    distribution, where BCa's bias correction is infinite: that case alone reports the percentile interval."""
    res = bootstrap(arrays, stat, paired=paired, vectorized=True, n_resamples=BOOT["n_iterations"],
                    confidence_level=BOOT["confidence_level"], method=BOOT["method"], batch=BATCH,
                    axis=axis, random_state=np.random.default_rng(0))
    lo, hi = float(res.confidence_interval.low), float(res.confidence_interval.high)
    if np.isfinite(lo) and np.isfinite(hi):
        return lo, hi, BOOT["method"]
    dist, point = res.bootstrap_distribution, float(stat(*arrays, axis=axis))
    if bounded and (dist.min() >= point or dist.max() <= point):
        q = (1 - BOOT["confidence_level"]) / 2
        lo, hi = (float(x) for x in np.quantile(dist, [q, 1 - q]))
        print(f"BCa undefined: estimate {point:.4f} is at the edge of its bootstrap distribution; percentile interval reported")
        return lo, hi, "percentile"
    raise RuntimeError(f"bootstrap returned a non-finite interval (estimate {point:.4f})")


def summarize(suite, inst, noinst):
    ids_i, arr_i = inst
    ids_n, arr_n = noinst
    if not np.array_equal(ids_i, ids_n):
        raise RuntimeError(f"{suite}: Instruct and NoInstruct were scored on different items")
    f = STAT[suite]
    k = len(arr_i)
    score = float(f(*arr_i))
    delta = score - float(f(*arr_n))
    s_lo, s_hi, _ = ci(arr_i, f)
    d_lo, d_hi, _ = ci(tuple(arr_i) + tuple(arr_n), lambda *a, axis=-1: f(*a[:k], axis=axis) - f(*a[k:], axis=axis))
    return {"n": int(len(ids_i)), "score": score, "score_ci": [s_lo, s_hi],
            "delta": delta, "delta_ci": [d_lo, d_hi]}


def compare(suite, ours, rival):
    """Paired CI of ours minus rival on the Instruct score and on delta (both trainers scored on the same items)."""
    (ids_oi, a_oi), (_, a_on) = ours
    (ids_ri, a_ri), (_, a_rn) = rival
    if not np.array_equal(ids_oi, ids_ri):
        raise RuntimeError(f"{suite}: {OURS} and its rival were scored on different items")
    f = STAT[suite]
    k = len(a_oi)
    s_diff = float(f(*a_oi)) - float(f(*a_ri))
    d_diff = (float(f(*a_oi)) - float(f(*a_on))) - (float(f(*a_ri)) - float(f(*a_rn)))
    s_lo, s_hi, _ = ci(tuple(a_oi) + tuple(a_ri), lambda *a, axis=-1: f(*a[:k], axis=axis) - f(*a[k:], axis=axis))
    d_lo, d_hi, _ = ci(tuple(a_oi) + tuple(a_on) + tuple(a_ri) + tuple(a_rn),
                    lambda *a, axis=-1: (f(*a[:k], axis=axis) - f(*a[k:2 * k], axis=axis))
                    - (f(*a[2 * k:3 * k], axis=axis) - f(*a[3 * k:], axis=axis)))
    return {"score_diff": s_diff, "score_diff_ci": [s_lo, s_hi], "delta_diff": d_diff, "delta_diff_ci": [d_lo, d_hi]}


def suite_block(suite, loaded):
    """One bootstrap sample per suite: rows = trainer x (Instruct, NoInstruct) x 2 channels, columns = items."""
    ids0 = loaded[TRAINERS[0]][suite][0][0]
    rows = []
    for t in TRAINERS:
        for ids, arrs in loaded[t][suite]:
            if not np.array_equal(ids, ids0):
                raise RuntimeError(f"{suite}: {t} was scored on different items than {TRAINERS[0]}")
            rows.extend(arrs if len(arrs) == 2 else (arrs[0], arrs[0]))  # 1-channel suites: second row is an unused copy
    return np.stack(rows)


def block_deltas(suite, X, k, axis=-1):
    """Instruct-minus-NoInstruct delta of every trainer from a suite block; trainers on the last axis."""
    f = STAT[suite]
    d = [f(*X[4 * i:4 * i + k], axis=axis) - f(*X[4 * i + 2:4 * i + 2 + k], axis=axis) for i in range(len(TRAINERS))]
    return np.stack(d, axis=-1)


def efficiency(deltas):
    """Per-suite min-max across trainers onto [0.1, 1], mean over suites, in % (src/utils/eval/plotting.py)."""
    D = np.stack(np.broadcast_arrays(*deltas), axis=-2)
    lo, hi = D.min(-1, keepdims=True), D.max(-1, keepdims=True)
    span = np.where(hi > lo, hi - lo, 1.0)
    return 100 * np.mean(0.1 + 0.9 * (D - lo) / span, axis=-2)


def efficiency_table(loaded, aqi_delta, pbar):
    """Efficiency per trainer and ours-minus-rival, BCa over items (suites resampled independently, AQI held fixed)."""
    out = {}
    for name, suites in EFF_VARIANTS.items():
        boot = [s for s in suites if s != "aqi"]
        blocks = tuple(suite_block(s, loaded) for s in boot)
        k = [len(loaded[OURS][s][0][1]) for s in boot]

        def eff(*X, axis=-1):
            d = [block_deltas(s, x, ki, axis=axis) for s, x, ki in zip(boot, X, k)]
            if "aqi" in suites:
                d.append(aqi_delta)
            return efficiency(d)

        point = eff(*blocks)
        o = TRAINERS.index(OURS)
        out[name] = {"suites": suites, "trainers": {}, "vs_ours": {}}
        for i, t in enumerate(TRAINERS):
            lo, hi, how = ci(blocks, lambda *X, axis=-1, i=i: eff(*X, axis=axis)[..., i], paired=False, axis=-1, bounded=True)
            out[name]["trainers"][t] = {"efficiency": float(point[i]), "ci": [lo, hi], "ci_method": how}
            print(f"efficiency[{name}] {t:5s} {point[i]:5.1f} [{lo:5.1f}, {hi:5.1f}] ({how})")
            pbar.update(1)
            if t == OURS:
                continue
            lo, hi, how = ci(blocks, lambda *X, axis=-1, i=i: eff(*X, axis=axis)[..., o] - eff(*X, axis=axis)[..., i],
                             paired=False, axis=-1, bounded=True)
            out[name]["vs_ours"][t] = {"diff": float(point[o] - point[i]), "ci": [lo, hi], "ci_method": how}
            print(f"efficiency[{name}] {OURS}-{t:5s} {point[o] - point[i]:+5.1f} [{lo:+5.1f}, {hi:+5.1f}] ({how})")
            pbar.update(1)
    return out


def aqi(model: str) -> float:
    rows = pd.read_csv(EVAL_DIR / SUITES["aqi"] / model / f"{model}_metrics_summary.csv")
    overall = rows[rows["Category"].str.lower() == "overall"]
    if len(overall) != 1:
        raise RuntimeError(f"AQI {model}: expected one 'overall' row, found {len(overall)}")
    return float(overall.iloc[0]["AQI [0-100] (↑)"])


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    calc = ISDMetricsCalculator(use_llm_judge=False)
    loaders = {"truthfulqa": load_truthfulqa, "conditional_safety": load_cond_safety,
               "length_control": load_length,
               "ecliptica": lambda m: load_ecliptica(m, calc)}
    if OURS not in TRAINERS:
        raise RuntimeError(f"score_table.ours={OURS} is not in score_table.trainers={TRAINERS}")
    rivals = [t for t in TRAINERS if t != OURS]
    table, loaded = {}, {}
    pbar = tqdm(total=len(TRAINERS) * (len(loaders) + 1) + len(rivals) * len(loaders)
                + len(EFF_VARIANTS) * (len(TRAINERS) + len(rivals)), desc="score_table_ci", unit="cell")
    for t in TRAINERS:
        table[t], loaded[t] = {}, {}
        for suite, load in loaders.items():
            loaded[t][suite] = (load(f"{t}_Instruct"), load(f"{t}_NoInstruct"))
            table[t][suite] = summarize(suite, *loaded[t][suite])
            r = table[t][suite]
            print(f"{t:5s} {suite:18s} n={r['n']:5d} score {r['score']:.4f} [{r['score_ci'][0]:.4f}, {r['score_ci'][1]:.4f}]"
                  f"  delta {r['delta']:+.4f} [{r['delta_ci'][0]:+.4f}, {r['delta_ci'][1]:+.4f}]")
            pbar.update(1)
        a_i, a_n = aqi(f"{t}_Instruct"), aqi(f"{t}_NoInstruct")
        table[t]["aqi"] = {"score": a_i, "delta": a_i - a_n, "score_ci": None, "delta_ci": None,
                           "note": "cluster-separation metric over the whole response set; no per-item score to resample"}
        print(f"{t:5s} {'aqi':18s} score {a_i:.2f}  delta {a_i - a_n:+.2f}  (no CI: cluster metric)")
        pbar.update(1)
    vs_ours = {}
    for r in rivals:
        vs_ours[r] = {}
        for suite in loaders:
            c = vs_ours[r][suite] = compare(suite, loaded[OURS][suite], loaded[r][suite])
            print(f"{OURS}-{r:5s} {suite:18s} score diff {c['score_diff']:+.4f} [{c['score_diff_ci'][0]:+.4f}, {c['score_diff_ci'][1]:+.4f}]"
                  f"  delta diff {c['delta_diff']:+.4f} [{c['delta_diff_ci'][0]:+.4f}, {c['delta_diff_ci'][1]:+.4f}]")
            pbar.update(1)
    eff = efficiency_table(loaded, np.array([table[t]["aqi"]["delta"] for t in TRAINERS]), pbar)
    pbar.close()
    out = OUT_DIR / "score_table_ci.json"
    meta = {"bootstrap": BOOT, "paired": True, "ours": OURS, "resampling_unit": {
        "truthfulqa": "question", "conditional_safety": "prompt", "length_control": "prompt", "ecliptica": "prompt"},
        "efficiency_note": "suites resampled independently, items paired across all 8 models; AQI delta held fixed"}
    json.dump({"meta": meta, "table": table, "vs_ours": vs_ours, "efficiency": eff}, open(out, "w"), indent=2)
    print(f"wrote {out} ({len(TRAINERS)} trainers x {len(loaders) + 1} suites, {len(rivals)} paired comparisons)")


if __name__ == "__main__":
    main()
