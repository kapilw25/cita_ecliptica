"""Build ECLIPTICA-30k (300 prompts x 100 instruction types) from the evaluated 3k subset + the 100-type taxonomy. CPU-only.
    python -u src/eval/ecliptica_30k_build.py 2>&1 | tee logs/ecliptica_30k_build.log
    HF_TOKEN=... python -u src/eval/ecliptica_30k_build.py --push 2>&1 | tee logs/ecliptica_30k_build.log
"""

from __future__ import annotations

import argparse
import os
import random
import shutil
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd
import yaml
from datasets import load_dataset
from huggingface_hub import HfApi
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.eval.isd_dataset import ISD_INSTRUCTIONS  # noqa: E402  (the 10 evaluated types, single source)
from src.utils.config import load_pipeline_config  # noqa: E402

COLUMNS_3K = ["prompt_id", "prompt", "instruction_type", "instruction", "expected_characteristics", "source"]
PARQUET_NAME = "train-00000-of-00001.parquet"


def load_taxonomy(path: Path) -> dict:
    """Load configs/ecliptica_taxonomy_100.yaml and check its shape against ISD_INSTRUCTIONS."""
    tax = yaml.safe_load(path.read_text())
    assigned = sorted(t for lst in tax["original_types"].values() for t in lst)
    if assigned != sorted(ISD_INSTRUCTIONS):
        raise RuntimeError(f"taxonomy original_types {assigned} != isd_dataset.ISD_INSTRUCTIONS {sorted(ISD_INSTRUCTIONS)}")
    n_new = sum(len(spec["new_types"]) for spec in tax["axes"].values())
    if len(tax["axes"]) != tax["n_axes"] or n_new + len(ISD_INSTRUCTIONS) != tax["n_types"]:
        raise RuntimeError(f"taxonomy declares {tax['n_axes']} axes / {tax['n_types']} types, found {len(tax['axes'])} / {n_new + len(ISD_INSTRUCTIONS)}")
    for axis, spec in tax["axes"].items():
        n_axis = len(tax["original_types"].get(axis, [])) + len(spec["new_types"])
        if n_axis != tax["settings_per_axis"]:
            raise RuntimeError(f"axis {axis} has {n_axis} settings, expected {tax['settings_per_axis']}")
        for name, t in spec["new_types"].items():
            if name in ISD_INSTRUCTIONS:
                raise RuntimeError(f"new type {name} clashes with an original type")
            if len(t["variants"]) != 3 or len(t["expected_characteristics"]) != 3:
                raise RuntimeError(f"type {name}: need 3 variants and 3 expected_characteristics")
    return tax


def type_axis_table(tax: dict) -> Dict[str, Dict[str, str]]:
    """Map every one of the 100 instruction types to its axis and axis kind."""
    table: Dict[str, Dict[str, str]] = {}
    for axis, spec in tax["axes"].items():
        for name in tax["original_types"].get(axis, []):
            table[name] = {"axis": axis, "axis_kind": spec["kind"], "origin": "ecliptica_3k_evaluated"}
        for name in spec["new_types"]:
            table[name] = {"axis": axis, "axis_kind": spec["kind"], "origin": "taxonomy_100_unevaluated"}
    if len(table) != tax["n_types"]:
        raise RuntimeError(f"{len(table)} types mapped, expected {tax['n_types']}")
    return table


def load_3k(repo_id: str) -> pd.DataFrame:
    """Download the evaluated 3k subset and verify it is the 300 x 10 factorial grid."""
    df = load_dataset(repo_id, split="train").to_pandas()
    if list(df.columns) != COLUMNS_3K:
        raise RuntimeError(f"{repo_id}: columns {list(df.columns)} != {COLUMNS_3K}")
    n_prompts = df["prompt_id"].nunique()
    types = sorted(df["instruction_type"].unique())
    if types != sorted(ISD_INSTRUCTIONS):
        raise RuntimeError(f"{repo_id}: instruction types {types} != ISD_INSTRUCTIONS")
    per_prompt = df.groupby("prompt_id")["instruction_type"].nunique()
    if len(df) != n_prompts * len(types) or (per_prompt != len(types)).any():
        raise RuntimeError(f"{repo_id}: not a full factorial grid ({len(df)} rows, {n_prompts} prompts)")
    return df


def build_new_rows(df3k: pd.DataFrame, tax: dict, seed: int) -> pd.DataFrame:
    """One row per (prompt, new type); the phrasing variant is sampled with a fixed seed, as in the 3k build."""
    prompts = (df3k[["prompt_id", "prompt", "source"]].drop_duplicates("prompt_id")
               .sort_values("prompt_id").to_dict("records"))
    new_types: List[tuple] = [(axis, name, t) for axis, spec in tax["axes"].items()
                              for name, t in spec["new_types"].items()]
    rng = random.Random(seed)
    rows = []
    for p in tqdm(prompts, desc="ecliptica_30k_build", unit="prompt"):
        for _axis, name, t in new_types:
            rows.append({
                "prompt_id": int(p["prompt_id"]),
                "prompt": p["prompt"],
                "instruction_type": name,
                "instruction": rng.choice(t["variants"]),
                "expected_characteristics": list(t["expected_characteristics"]),
                "source": p["source"],
            })
    return pd.DataFrame(rows, columns=COLUMNS_3K)


def verify_full(full: pd.DataFrame, df3k: pd.DataFrame, tax: dict) -> None:
    """Fail loud unless full is exactly 300 x 100 and contains the 3k rows verbatim."""
    n_prompts, n_types = df3k["prompt_id"].nunique(), tax["n_types"]
    if len(full) != n_prompts * n_types:
        raise RuntimeError(f"full has {len(full)} rows, expected {n_prompts * n_types}")
    if full.duplicated(["prompt_id", "instruction_type"]).any():
        raise RuntimeError("duplicate (prompt_id, instruction_type) pairs")
    if (full.groupby("instruction_type").size() != n_prompts).any() or (full.groupby("prompt_id").size() != n_types).any():
        raise RuntimeError("grid is not balanced (each type x 300 prompts, each prompt x 100 types)")
    kept = full[full["instruction_type"].isin(ISD_INSTRUCTIONS)][COLUMNS_3K].reset_index(drop=True)
    orig = df3k[COLUMNS_3K].reset_index(drop=True)
    key = ["prompt_id", "instruction_type"]
    merged = orig.merge(kept, on=key, suffixes=("_3k", "_full"))
    if len(merged) != len(orig):
        raise RuntimeError("3k rows missing from full")
    for col in ("prompt", "instruction", "source"):
        if (merged[f"{col}_3k"] != merged[f"{col}_full"]).any():
            raise RuntimeError(f"3k rows altered in full (column {col})")
    if any(list(a) != list(b) for a, b in zip(merged["expected_characteristics_3k"], merged["expected_characteristics_full"])):
        raise RuntimeError("3k rows altered in full (expected_characteristics)")


def write_card(out_dir: Path, tax: dict, repo_3k: str, repo_30k: str, n_prompts: int, n_rows_full: int) -> None:
    """Dataset card with two configs: full (30k) and eval_3k (the evaluated subset, verbatim)."""
    axis_rows = []
    for axis, spec in tax["axes"].items():
        settings = tax["original_types"].get(axis, []) + list(spec["new_types"])
        axis_rows.append(f"| `{axis}` | {spec['kind']} | {len(settings)} | " + ", ".join(f"`{s}`" for s in settings) + " |")
    card = f"""---
license: cc-by-4.0
language:
  - en
task_categories:
  - text-generation
tags:
  - alignment
  - instruction-following
  - preference-optimization
  - safety
  - RLHF
  - DPO
  - SwiPO
  - ECLIPTICA
pretty_name: "ECLIPTICA-30k: prompt-held-constant instruction-switch benchmark, 100 instruction types"
size_categories:
  - 10K<n<100K
configs:
  - config_name: full
    default: true
    data_files: data/full/*.parquet
  - config_name: eval_3k
    data_files: data/eval_3k/*.parquet
---

# ECLIPTICA-30k

**ECLIPTICA** holds the user prompt fixed and varies only the alignment instruction, so any behavioral
difference between two rows with the same `prompt_id` is attributable to the instruction. ECLIPTICA-30k
crosses the same {n_prompts} prompts as [ECLIPTICA-3k](https://huggingface.co/datasets/{repo_3k}) with
**{tax['n_types']} instruction types** ({tax['n_axes']} axes x {tax['settings_per_axis']} settings) = **{n_rows_full:,} cases**.

**What has been evaluated.** All experiments in the companion paper use the original 10 types, i.e. the
`eval_3k` config ({n_prompts} x 10 = {n_prompts * len(ISD_INSTRUCTIONS):,} cases, byte-identical to ECLIPTICA-3k).
The 90 additional types are released to widen the instruction space for further research; they are
hand-designed as a taxonomy (no judge models), they have **not** been scored by any model yet, and they
carry no evaluation claims.

## Configs

| config | rows | content |
|---|---|---|
| `full` (default) | {n_rows_full:,} | {n_prompts} prompts x {tax['n_types']} types; adds `axis`, `axis_kind`, `origin` columns |
| `eval_3k` | {n_prompts * len(ISD_INSTRUCTIONS):,} | the evaluated subset, identical to ECLIPTICA-3k (6 columns) |

## Axes and settings

`kind = policy` axes change what the model commits to (stance, boundary, epistemics, role, region);
`kind = surface` axes change how it says it (style, length, audience, format). Each type has three
imperative phrasings; one is sampled per row with a fixed seed.

| axis | kind | settings | types |
|---|---|---|---|
{chr(10).join(axis_rows)}

The full taxonomy with descriptions, phrasings and expected characteristics is in `taxonomy.yaml`.

## Fields

- `prompt_id`: identifier shared by the {tax['n_types']} rows of one prompt
- `prompt`: the user query (held fixed across instruction types)
- `instruction_type`: one of the {tax['n_types']} types above
- `instruction`: the alignment-instruction text used for this row
- `expected_characteristics`: behavioral traits the response should show under this instruction
- `source`: topical category of the prompt (12 categories x 25 prompts)
- `axis`, `axis_kind`, `origin` (`full` config only): taxonomy axis, policy/surface, and whether the type belongs to the evaluated 10

## Usage

```python
from datasets import load_dataset
full = load_dataset("{repo_30k}", "full", split="train")       # {n_rows_full:,} rows
eval_3k = load_dataset("{repo_30k}", "eval_3k", split="train") # the evaluated {n_prompts * len(ISD_INSTRUCTIONS):,} rows
```

## Citation

```bibtex
@misc{{wanaskar2026ecliptica,
  title         = {{ECLIPTICA: A Framework for Switchable LLM Alignment via SwiPO, Switchable Preference Optimization}},
  author        = {{Wanaskar, Kapil and Jena, Gaytri and Jain, Vinija and Chadha, Aman and Das, Amitava}},
  year          = {{2026}},
  eprint        = {{2601.06157}},
  archivePrefix = {{arXiv}},
  primaryClass  = {{cs.LG}},
  url           = {{https://arxiv.org/abs/2601.06157}}
}}
```

## License

CC-BY-4.0.
"""
    (out_dir / "README.md").write_text(card)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--push", action="store_true", help="upload the build dir to the HF repo in configs/pipeline.yaml")
    args = parser.parse_args()

    cfg = load_pipeline_config()["datasets"]
    tax_path = PROJECT_ROOT / cfg["ecliptica_taxonomy"]
    out_dir = PROJECT_ROOT / cfg["ecliptica_30k_dir"]

    tax = load_taxonomy(tax_path)
    axis_table = type_axis_table(tax)
    df3k = load_3k(cfg["ecliptica_3k"])
    n_prompts = df3k["prompt_id"].nunique()
    print(f"3k subset: {len(df3k)} rows, {n_prompts} prompts, {df3k['instruction_type'].nunique()} types")

    new_rows = build_new_rows(df3k, tax, cfg["ecliptica_30k_seed"])
    full = pd.concat([df3k[COLUMNS_3K], new_rows], ignore_index=True)
    full = full.sort_values(["prompt_id", "instruction_type"], kind="stable").reset_index(drop=True)
    for col in ("axis", "axis_kind", "origin"):
        full[col] = full["instruction_type"].map(lambda t, c=col: axis_table[t][c])
    verify_full(full, df3k, tax)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "data" / "full").mkdir(parents=True)
    (out_dir / "data" / "eval_3k").mkdir(parents=True)
    full.to_parquet(out_dir / "data" / "full" / PARQUET_NAME, index=False)
    df3k[COLUMNS_3K].to_parquet(out_dir / "data" / "eval_3k" / PARQUET_NAME, index=False)
    shutil.copy(tax_path, out_dir / "taxonomy.yaml")
    write_card(out_dir, tax, cfg["ecliptica_3k"], cfg["ecliptica_30k"], n_prompts, len(full))

    back = pd.read_parquet(out_dir / "data" / "full" / PARQUET_NAME)
    verify_full(back, df3k, tax)
    print(f"full: {len(back):,} rows = {n_prompts} prompts x {tax['n_types']} types "
          f"({back['origin'].value_counts().to_dict()}); eval_3k: {len(df3k):,} rows; written to {out_dir}")

    if args.push:
        token = os.environ["HF_TOKEN"]
        api = HfApi(token=token)
        api.create_repo(cfg["ecliptica_30k"], repo_type="dataset", exist_ok=True)
        info = api.upload_folder(folder_path=str(out_dir), repo_id=cfg["ecliptica_30k"], repo_type="dataset",
                                 commit_message=f"ECLIPTICA-30k: {n_prompts} prompts x {tax['n_types']} types "
                                                f"({len(full):,} rows) + eval_3k config")
        print(f"pushed to https://huggingface.co/datasets/{cfg['ecliptica_30k']} ({info})")


if __name__ == "__main__":
    main()
