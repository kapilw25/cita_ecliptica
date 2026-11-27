"""ECLIPTICA-3k score (mean fidelity x mean pairwise semantic shift, the scorer of src/eval/score_table_ci.py) for each model
as trained and with the final adapter only, on the full answer and on its first turn; 95% BCa over prompts. CPU (MiniLM).
    python -u outputs/evaluation/stack_probe/ecliptica_astrained.py 2>&1 | tee logs/ecliptica_astrained.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.score_table_ci import EVAL_DIR, STAT, SUITES, ci, load_ecliptica  # noqa: E402
from src.utils.eval.first_turn import first_turn  # noqa: E402
from src.utils.eval.isd_metrics import ISDMetricsCalculator  # noqa: E402

PAIRS = [("DPO_Instruct", "DPO_Instruct_AsTrained"), ("PPO_Instruct", "PPO_Instruct_AsTrained"),
         ("GRPO_Instruct", "GRPO_Instruct_AsTrained"), ("CITA_Instruct", "CITA_Instruct_AsTrained")]
EXTRA = ["Llama31_Instruct_Prompted"]
OUT = project_root / "outputs/evaluation/contract_gap/ecliptica_astrained.json"


def first_turn_arrays(model: str, calc: ISDMetricsCalculator):
    """Per-prompt fidelity and shift with every answer cut to its first turn (run-on answers invent further turns)."""
    df = pd.read_csv(EVAL_DIR / SUITES["ecliptica"] / model / f"{model}_isd_responses.csv", keep_default_na=False)
    cut = df["response"].map(first_turn)
    run_on = float((cut != df["response"]).mean())
    df["response"] = cut
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
    return ids, (per_prompt.to_numpy(), np.array([shift[int(i)] for i in ids])), run_on


def row(ids_arr):
    ids, (F, S) = ids_arr
    lo, hi, method = ci((F, S), STAT["ecliptica"])
    return ids, (F, S), {"score": float(STAT["ecliptica"](F, S)), "ci": [lo, hi], "ci_method": method,
                         "fidelity": float(F.mean()), "shift": float(S.mean()), "n_prompts": int(len(ids))}


def diff(a, b):
    """Paired difference b minus a of the score, over the prompts both share."""
    ids_a, (Fa, Sa) = a
    ids_b, (Fb, Sb) = b
    if not np.array_equal(ids_a, ids_b):
        raise RuntimeError("models were scored on different prompts")
    stat = lambda fa, sa, fb, sb, axis=-1: STAT["ecliptica"](fb, sb, axis=axis) - STAT["ecliptica"](fa, sa, axis=axis)  # noqa: E731
    lo, hi, method = ci((Fa, Sa, Fb, Sb), stat)
    return {"value": float(stat(Fa, Sa, Fb, Sb)), "ci": [lo, hi], "ci_method": method}


calc = ISDMetricsCalculator(use_llm_judge=False)
res = {}
for model in [m for p in PAIRS for m in p] + EXTRA:
    full_ids, full_arr, full = row(load_ecliptica(model, calc))
    ft_ids, ft_arr, run_on = first_turn_arrays(model, calc)
    _, _, ft = row((ft_ids, ft_arr))
    ft["share_answers_cut"] = run_on
    res[model] = {"full": full, "first_turn": ft, "_arrays": {"full": (full_ids, full_arr), "first_turn": (ft_ids, ft_arr)}}
    print(f"{model:28s} full {full['score']:.3f} [{full['ci'][0]:.3f}, {full['ci'][1]:.3f}] (F {full['fidelity']:.3f}, S {full['shift']:.3f})"
          f" | first turn {ft['score']:.3f} [{ft['ci'][0]:.3f}, {ft['ci'][1]:.3f}] (F {ft['fidelity']:.3f}, S {ft['shift']:.3f})")
for final, trained in PAIRS:
    for view in ("full", "first_turn"):
        d = diff(res[final]["_arrays"][view], res[trained]["_arrays"][view])
        res[trained][view]["minus_final_only"] = d
        print(f"{trained:28s} {view:10s} as trained minus final only {d['value']:+.3f} [{d['ci'][0]:+.3f}, {d['ci'][1]:+.3f}]")
for m in res:
    res[m].pop("_arrays")
OUT.write_text(json.dumps({"meta": {"score": "mean fidelity x mean pairwise semantic shift (all-MiniLM-L6-v2), ECLIPTICA-3k",
                                    "ci": "95% BCa, 10,000 resamples over prompts (configs/pipeline.yaml bootstrap)"},
                           "models": res}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
