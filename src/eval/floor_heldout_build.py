"""Held-out floor prompts: PKU-SafeRLHF prompts outside the 12,035-pair training pool, with harm categories. CPU-only.
    python -u src/eval/floor_heldout_build.py 2>&1 | tee logs/floor_heldout_build.log
"""

import json
import sys
from pathlib import Path

import numpy as np
import yaml
from datasets import load_dataset, concatenate_datasets
from tqdm import tqdm

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
H = CFG["floor_leakage"]["heldout"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
OUT = project_root / H["dir"] / H["prompts_file"]


def categories(row, k):
    return {c for c, v in row[f"response_{k}_harm_category"].items() if v}


def main():
    if H["source"] != "both_unsafe":
        raise ValueError(f"unknown heldout source {H['source']!r}")
    if OUT.exists():
        n = sum(1 for _ in open(OUT))
        if n != H["n_prompts"]:
            raise RuntimeError(f"{OUT} has {n} prompts, config asks for {H['n_prompts']}; delete it to rebuild")
        print(f"{OUT} already holds {n} prompts; nothing to do")
        return
    ds = concatenate_datasets([load_dataset("PKU-Alignment/PKU-SafeRLHF", split=s) for s in ("train", "test")])
    clear = ds.filter(lambda x: x["is_response_0_safe"] != x["is_response_1_safe"])
    pool = set(clear["prompt"])  # every prompt the SFT, DPO, PPO, GRPO and SwiPO stages could have seen
    print(f"PKU-SafeRLHF rows {len(ds):,}; training pool {len(clear):,} pairs, {len(pool):,} unique prompts")
    both_unsafe = ds.filter(lambda x: (not x["is_response_0_safe"]) and (not x["is_response_1_safe"]))
    seen, rows = set(), []
    for r in tqdm(both_unsafe, desc="floor_heldout_build", unit="pair"):
        p = r["prompt"]
        if p in pool or p in seen:
            continue
        seen.add(p)
        cats = sorted(categories(r, 0) | categories(r, 1))
        if cats:
            rows.append({"prompt": p, "harm_categories": cats})
    if len(rows) < H["n_prompts"]:
        raise RuntimeError(f"only {len(rows)} unseen prompts with categories; config asks for {H['n_prompts']}")
    pick = np.sort(np.random.default_rng(H["seed"]).choice(len(rows), size=H["n_prompts"], replace=False))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n_floor = 0
    with open(OUT, "w") as f:
        for i, j in enumerate(pick):
            row = {"prompt_idx": i, **rows[j]}
            n_floor += bool(FLOOR & set(row["harm_categories"]))
            f.write(json.dumps(row) + "\n")
    leaked = sum(json.loads(line)["prompt"] in pool for line in open(OUT))
    if leaked:
        raise RuntimeError(f"{leaked} written prompts are in the training pool")
    print(f"{len(rows):,} unseen prompts available; wrote {H['n_prompts']} (seed {H['seed']}), {n_floor} floor, to {OUT}")


if __name__ == "__main__":
    main()
