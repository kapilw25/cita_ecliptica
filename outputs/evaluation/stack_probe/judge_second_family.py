"""Second refusal judge from another family (Qwen2.5-7B-Instruct) on Conditional Safety, first turn: per-model strict-minus-permissive
judged gap, SwiPO-R minus each model with SFT in its chain (paired over prompts), and agreement with the default Llama judge; 95% BCa. CPU.
    python -u outputs/evaluation/stack_probe/judge_second_family.py 2>&1 | tee logs/judge_second_family.log
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

EVAL = project_root / "outputs/evaluation"
DEFAULT, SECOND = EVAL / "refusal_judge", EVAL / "refusal_judge_qwen"   # src/eval/refusal_judge.py [--judge qwen]
OUT = EVAL / "contract_gap/judge_second_family.json"
MODELS = ["Llama31_Base_Prompted", "SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained",
          "CITA_Instruct_AsTrained", "CITA_Instruct_Chain", "Llama31_Instruct_Prompted"]
SFT_CHAIN = ["SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained", "CITA_Instruct_Chain"]
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def labels(root: Path, model: str, arm: str) -> pd.Series:
    return pd.read_csv(root / model / f"{arm}.csv").set_index("prompt_idx").sort_index()["is_refusal_judge"].astype(bool).astype(float)


def gap(root: Path, model: str) -> pd.Series:
    s, p = labels(root, model, "strict"), labels(root, model, "permissive")
    if not s.index.equals(p.index):
        raise SystemExit(f"FATAL: {root.name}/{model}: strict and permissive labels cover different prompts")
    return s - p


def interval(x: np.ndarray) -> dict:
    (lo, hi), m = ci((x,), MEAN, paired=False)
    return {"value": float(x.mean()), "ci": [lo, hi], "ci_method": m, "n": int(len(x))}


def kappa(a, b, axis=-1):
    po = np.mean(a == b, axis=axis)
    pa, pb = np.mean(a, axis=axis), np.mean(b, axis=axis)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return np.where(pe < 1, (po - pe) / np.where(pe < 1, 1 - pe, 1), 1.0)


res, gaps = {}, {}
for m in MODELS:
    g2, g1 = gap(SECOND, m), gap(DEFAULT, m)
    if not g2.index.equals(g1.index):
        raise SystemExit(f"FATAL: {m}: the two judges labelled different prompts")
    gaps[m] = g2
    a = np.concatenate([labels(SECOND, m, x).to_numpy() for x in ("strict", "permissive")])
    b = np.concatenate([labels(DEFAULT, m, x).reindex(labels(SECOND, m, x).index).to_numpy() for x in ("strict", "permissive")])
    agree = lambda u, v, axis=-1: np.mean(u == v, axis=axis)  # noqa: E731
    (alo, ahi), am = ci((a, b), agree, paired=True)
    (klo, khi), km = ci((a, b), kappa, paired=True)
    res[m] = {"gap_second_judge": interval(g2.to_numpy()), "gap_default_judge": interval(g1.to_numpy()),
              "agreement": {"value": float(agree(a, b)), "ci": [alo, ahi], "ci_method": am},
              "kappa": {"value": float(kappa(a, b)), "ci": [klo, khi], "ci_method": km}}
    r = res[m]
    print(f"{m:28s} Qwen gap {r['gap_second_judge']['value']:+.3f} [{r['gap_second_judge']['ci'][0]:+.3f}, {r['gap_second_judge']['ci'][1]:+.3f}] | "
          f"Llama {r['gap_default_judge']['value']:+.3f} | agreement {r['agreement']['value']:.3f} kappa {r['kappa']['value']:.2f}")
contrasts = {}
for m in SFT_CHAIN + ["Llama31_Base_Prompted"]:
    d = (gaps["CITA_Instruct_AsTrained"] - gaps[m].reindex(gaps["CITA_Instruct_AsTrained"].index)).to_numpy()
    contrasts[f"SwiPO-R minus {m}"] = interval(d)
    c = contrasts[f"SwiPO-R minus {m}"]
    print(f"SwiPO-R minus {m:24s} {c['value']:+.3f} [{c['ci'][0]:+.3f}, {c['ci'][1]:+.3f}]")
OUT.write_text(json.dumps({"meta": {"second_judge": "Qwen/Qwen2.5-7B-Instruct, same prompt as the default judge (meta-llama/Llama-3.1-8B-Instruct), first turn",
                                    "gap": "strict minus permissive judged refusal, 1,222 Conditional Safety prompts, models as trained",
                                    "ci": "95% BCa over prompts, 10,000 resamples; contrasts paired over prompts"},
                           "models": res, "contrasts": contrasts}, indent=2))
print(f"wrote {OUT.relative_to(project_root)}")
