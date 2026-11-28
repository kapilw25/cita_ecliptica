"""Run-to-run stability of the strict-minus-permissive refusal gaps: the original answers plus resamples per suite and model, and the
PPO rows as test-retest replicates (PPO as trained = SFT, PPO final only = base); 95% BCa over prompts. CPU.
    python -u outputs/evaluation/stack_probe/resample_stability.py --replicates_only 2>&1 | tee logs/resample_replicates.log
    python -u outputs/evaluation/stack_probe/resample_stability.py 2>&1 | tee logs/resample_stability.log
    python -u outputs/evaluation/stack_probe/resample_stability.py --heldout_seeds 1 2 2>&1 | tee logs/resample_stability_ho12.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
R = CFG["resample_stability"]
EVAL = project_root / CFG["paths"]["evaluation_dir"]
CS_DIR, XS_DIR = CFG["score_table"]["suite_dirs"]["conditional_safety"], CFG["xstest_contract"]["dir_name"]
HELD = project_root / CFG["floor_leakage"]["heldout"]["dir"]
FILES = ("strict_responses.csv", "permissive_responses.csv")
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def samples(suite):
    """(sample name, answers dir) for one suite: the original first, then each resample."""
    if suite == "conditional_safety":
        return [("original", EVAL / CS_DIR)] + [(v, EVAL / v / CS_DIR) for v in R["cs_variants"]]
    if suite == "xstest":
        root = EVAL / R["xstest_variant"]
        return [("original", root / XS_DIR)] + [(f"seed{s}", root / f"{XS_DIR}_seed{s}") for s in R["seeds"]]
    return [("original", HELD / "full")] + [(f"seed{s}", HELD / f"full_seed{s}") for s in HELDOUT_SEEDS]


def per_prompt_gap(d, model):
    """Strict minus permissive is_refusal per prompt, aligned on prompt_idx; FATAL on a missing file or a prompt mismatch."""
    s, p = (pd.read_csv(d / model / f, usecols=["prompt_idx", "is_refusal"]).set_index("prompt_idx").is_refusal.astype(float) for f in FILES)
    if not s.index.sort_values().equals(p.index.sort_values()):
        raise SystemExit(f"FATAL: {d / model}: strict and permissive arms cover different prompts")
    return (s - p.reindex(s.index)).sort_index()


def interval(x):
    (lo, hi), m = ci((x.to_numpy(),), MEAN, paired=False)
    return {"gap": float(x.mean()), "ci": [lo, hi], "ci_method": m, "n": int(len(x)), "excludes_zero": bool(lo > 0 or hi < 0)}


def stability(suite, models):
    out = {}
    for m in tqdm(models, desc=f"resample_stability {suite}", unit="model"):
        rows, ref = {}, None
        for name, d in samples(suite):
            g = per_prompt_gap(d, m)
            if ref is not None and not g.index.equals(ref):
                raise SystemExit(f"FATAL: {suite}/{m}/{name}: prompts differ from the original run")
            ref = g.index
            rows[name] = interval(g)
        gaps = np.array([r["gap"] for r in rows.values()])
        out[m] = {"samples": rows, "mean": float(gaps.mean()), "sd": float(gaps.std(ddof=1)), "min": float(gaps.min()), "max": float(gaps.max()),
                  "n_samples": int(len(gaps)), "verdict_flips": len({r["excludes_zero"] for r in rows.values()}) > 1}
        print(f"{suite:18s} {m:28s} gaps " + " ".join(f"{g:+.3f}" for g in gaps) + f" | sd {out[m]['sd']:.3f} | flips {out[m]['verdict_flips']}")
    return out


def replicates():
    """Test-retest: the same weights evaluated twice (PPO's all-zero adapter), per suite where both rows exist; difference paired over prompts."""
    out = {}
    for a, b in R["replicate_pairs"]:
        for suite, d in (("conditional_safety", EVAL / CS_DIR), ("heldout", HELD / "full"), ("xstest", EVAL / R["xstest_variant"] / XS_DIR)):
            if not all((d / k / f).exists() for k in (a, b) for f in FILES):
                continue
            ga, gb = per_prompt_gap(d, a), per_prompt_gap(d, b)
            if not ga.index.equals(gb.index):
                raise SystemExit(f"FATAL: {suite}: {a} and {b} cover different prompts")
            diff = ga - gb
            same = bool((diff == 0).all())  # a seeded suite on identical weights reproduces the same answers: not an independent replicate
            r = out[f"{suite}:{a}-vs-{b}"] = {"a": interval(ga), "b": interval(gb), "a_minus_b": interval(diff),
                                             "identical_labels": same, "independent_replicate": not same}
            print(f"replicate {suite:18s} {a} {r['a']['gap']:+.3f} vs {b} {r['b']['gap']:+.3f} | difference {r['a_minus_b']['gap']:+.3f} "
                  f"[{r['a_minus_b']['ci'][0]:+.3f}, {r['a_minus_b']['ci'][1]:+.3f}]" + (" (identical labels: same seed, not independent)" if same else ""))
    if not out:
        raise SystemExit("FATAL: no replicate pair has answers in any suite")
    return out


ap = argparse.ArgumentParser(description="Run-to-run stability of the refusal gaps and PPO test-retest replicates (CPU)")
ap.add_argument("--replicates_only", action="store_true", help="only the PPO test-retest pairs (no resample needed); writes <summary>_replicates.json")
ap.add_argument("--heldout_seeds", type=int, nargs="+", default=None,
                help="held-out resamples to use (default: resample_stability.seeds); a subset is recorded in the summary's meta")
args = ap.parse_args()
HELDOUT_SEEDS = args.heldout_seeds if args.heldout_seeds is not None else R["seeds"]
if not set(HELDOUT_SEEDS) <= set(R["seeds"]):
    raise SystemExit(f"FATAL: --heldout_seeds {HELDOUT_SEEDS} not all in resample_stability.seeds {R['seeds']}")
result = {"replicates": replicates()}
if not args.replicates_only:
    result["stability"] = {"conditional_safety": stability("conditional_safety", R["models"]), "xstest": stability("xstest", R["models"]),
                           "heldout": stability("heldout", R["heldout_models"])}
out = project_root / R["summary"]
if args.replicates_only:
    out = out.with_name(out.stem + "_replicates.json")
meta = {"gap": "strict minus permissive is_refusal (the suite's phrase heuristic: full answer for Conditional Safety and held-out, "
                "first turn for XSTest), paired over prompts", "samples": "original run plus resamples (configs/pipeline.yaml resample_stability)",
        "replicates": "PPO's released adapter is all zero, so its rows re-run SFT (as trained) and the base model (final only)",
        "ci": "95% BCa over prompts, 10,000 resamples", "sd": "across samples, ddof 1", "heldout_seeds": HELDOUT_SEEDS}
out.write_text(json.dumps({"meta": meta, **result}, indent=2))
print(f"wrote {out.relative_to(project_root)}")
