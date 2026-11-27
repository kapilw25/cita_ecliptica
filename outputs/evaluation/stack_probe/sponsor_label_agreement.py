"""Owner's blind sponsor labels vs the automatic flags (LoyalAgents, ChatGPT v4 C2): Cohen's kappa and agreement for promotion (recommends vs
no-echo mention), mention, disclosure and contract repetition (5-gram echo), plus the human promotion rate of the prompted Instruct model;
95% BCa over items. Labels come from the labeling page's store (ArtifactData list, saved as JSON files). CPU.
    python -u outputs/evaluation/stack_probe/sponsor_label_agreement.py --labels_dir <dir of labels/<id>.json> 2>&1 | tee logs/sponsor_label_agreement.log
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.eval.floor_leakage import ci  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
L = CFG["sponsor_label_check"]
KEY = project_root / L["out_dir"] / "key.json"
OUT = project_root / "outputs/evaluation/contract_gap/sponsor_label_agreement.json"
MEAN = lambda x, axis=-1: np.mean(x, axis=axis)  # noqa: E731


def kappa(a, b, axis=-1):
    """Cohen's kappa of two binary label vectors (vectorized over resamples)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    po = np.mean(a == b, axis=axis)
    pa, pb = np.mean(a, axis=axis), np.mean(b, axis=axis)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return np.where(pe < 1, (po - pe) / np.where(pe < 1, 1 - pe, 1), 1.0)


def stat(name, fn, *arrays):
    (lo, hi), method = ci(arrays, fn, paired=len(arrays) > 1)
    return {"value": float(fn(*arrays)), "ci": [lo, hi], "ci_method": method, "n": int(len(arrays[0])), "name": name}


def main():
    ap = argparse.ArgumentParser(description="Owner's sponsor labels vs automatic flags (CPU)")
    ap.add_argument("--labels_dir", type=Path, required=True, help="folder holding one <item id>.json per label document")
    args = ap.parse_args()
    key = {k["id"]: k for k in json.load(open(KEY))["items"]}
    labels = {}
    for f in sorted(args.labels_dir.rglob("*.json")):
        d = json.load(open(f))
        doc = d.get("data", d)  # runtime JSON from the store (a document with or without a data wrapper)
        iid = f.stem
        if iid in key and all(isinstance(doc.get(k), str) for k in ("promotes", "discloses", "repeats")):
            labels[iid] = doc
    if not labels:
        raise SystemExit(f"FATAL: no complete labels under {args.labels_dir}")
    ids = sorted(labels)
    h_rec = np.array([labels[i]["promotes"] == "recommends" for i in ids], float)
    h_men = np.array([labels[i]["promotes"] != "absent" for i in ids], float)
    h_dis = np.array([labels[i]["discloses"] == "discloses" for i in ids], float)
    h_rep = np.array([labels[i]["repeats"] == "yes" for i in ids], float)
    a_pro = np.array([key[i]["auto_promotion"] for i in ids], float)
    a_men = np.array([key[i]["auto_mention"] for i in ids], float)
    a_dis = np.array([key[i]["auto_discloses"] for i in ids], float)
    a_rep = np.array([key[i]["auto_echo"] for i in ids], float)
    res = {"n_labelled": len(ids), "n_items": len(key),
           "promotion": {"kappa": stat("kappa", kappa, h_rec, a_pro), "agreement": stat("agree", lambda a, b, axis=-1: np.mean(a == b, axis=axis), h_rec, a_pro)},
           "mention": {"kappa": stat("kappa", kappa, h_men, a_men)},
           "disclosure": {"kappa": stat("kappa", kappa, h_dis, a_dis)},
           "repetition": {"kappa": stat("kappa", kappa, h_rep, a_rep)}}
    inst = [i for i in ids if key[i]["model"] == "Llama31_Instruct_Prompted" and key[i]["arm"] == "sponsor"]
    for run in ("plain", "impartial"):
        sel = [i for i in inst if key[i]["run"] == run]
        if sel:
            res[f"instruct_{run}_human_recommends_given_auto_promotion"] = stat(
                "rate", MEAN, np.array([labels[i]["promotes"] == "recommends" for i in sel if key[i]["auto_promotion"]], float))
    for k, v in res.items():
        print(k, json.dumps(v)[:300])
    OUT.write_text(json.dumps({"meta": {"key": str(KEY.relative_to(project_root)), "labels_dir": str(args.labels_dir),
                                        "human": "owner, blind to model and run (labeling page)", "ci": "95% BCa over items, 10,000 resamples"},
                               "results": res}, indent=2))
    print(f"wrote {OUT.relative_to(project_root)}")


if __name__ == "__main__":
    main()
