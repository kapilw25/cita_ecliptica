"""Contract gap per suite with 95% BCa CIs for any models, plus paired differences vs the first model. CPU.
    python -u src/eval/contract_gap_table.py --name g4_prompted_baseline --models Llama31_Instruct_Prompted DPO_Instruct PPO_Instruct GRPO_Instruct CITA_Instruct 2>&1 | tee logs/contract_gap_g4.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from tqdm import tqdm

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.eval.score_table_ci import CFG, STAT, ci, load_cond_safety, load_ecliptica, load_length, load_truthfulqa  # noqa: E402
from src.utils.eval.isd_metrics import ISDMetricsCalculator  # noqa: E402

OUT_DIR = project_root / CFG["paths"]["evaluation_dir"] / "contract_gap"
SUITES = ["conditional_safety", "length_control", "truthfulqa", "ecliptica"]
STAT_NOTE = {"conditional_safety": "|strict - permissive| refusal rate", "length_control": "detailed / concise total words",
             "truthfulqa": "honest - confident uncertainty-marker rate", "ecliptica": "mean fidelity x mean semantic shift"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True, help="model keys; the first is the reference for paired differences")
    ap.add_argument("--suites", nargs="+", choices=SUITES, default=SUITES)
    ap.add_argument("--name", required=True, help="output stem: outputs/evaluation/contract_gap/<name>.json")
    args = ap.parse_args()
    calc = ISDMetricsCalculator(use_llm_judge=False) if "ecliptica" in args.suites else None
    loaders = {"truthfulqa": load_truthfulqa, "conditional_safety": load_cond_safety, "length_control": load_length,
               "ecliptica": lambda m: load_ecliptica(m, calc)}
    ref = args.models[0]
    out = {}
    pbar = tqdm(total=len(args.suites) * (2 * len(args.models) - 1), desc="contract_gap", unit="cell")
    for suite in args.suites:
        f = STAT[suite]
        data = {m: loaders[suite](m) for m in args.models}  # each loader re-checks its stored score (FATAL on mismatch)
        ids0 = data[ref][0]
        for m in args.models:
            if not np.array_equal(data[m][0], ids0):
                raise RuntimeError(f"{suite}: {m} was scored on different items than {ref}")
        rows = out[suite] = {}
        for m in args.models:
            arr = data[m][1]
            lo, hi, meth = ci(arr, f, bounded=True)
            r = rows[m] = {"n": int(len(ids0)), "score": float(f(*arr)), "ci": [lo, hi], "ci_method": meth}
            pbar.update(1)
            line = f"{suite:18s} {m:28s} {r['score']:8.3f} [{lo:.3f}, {hi:.3f}]"
            if m != ref:
                b = data[ref][1]
                k = len(arr)
                dlo, dhi, dm = ci(tuple(arr) + tuple(b), lambda *x, axis=-1: f(*x[:k], axis=axis) - f(*x[k:], axis=axis))
                r["minus_ref"] = {"value": r["score"] - float(f(*b)), "ci": [dlo, dhi], "ci_method": dm}
                pbar.update(1)
                line += f" | minus {ref}: {r['minus_ref']['value']:+.3f} [{dlo:+.3f}, {dhi:+.3f}]"
            print(line)
    pbar.close()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = {"models": args.models, "reference": ref, "statistic": {s: STAT_NOTE[s] for s in args.suites},
            "bootstrap": CFG["bootstrap"], "resampling_unit": "item, paired across models"}
    path = OUT_DIR / f"{args.name}.json"
    json.dump({"meta": meta, "suites": out}, open(path, "w"), indent=2)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
