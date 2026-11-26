"""G1/G2 contract pairs: PKU-SafeRLHF pairs with safer != better, eval prompts excluded, 5 variants + stats. CPU-only.
    python -u src/train/g1_contracts_build.py 2>&1 | tee logs/g1_contracts_build.log
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import load_dataset

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_pipeline_config  # noqa: E402
from src.utils.progress import make_pbar  # noqa: E402
from src.utils.train.data_prep.loader_pku import load_pku_combined_clear_contrast  # noqa: E402
from src.utils.train.data_prep.contract_pairs import (  # noqa: E402
    COLUMNS, SPLITS, STATS_FILE, file_sha256, norm_prompt, user_prompt,
)

CFG = load_pipeline_config()
G = CFG["g1_contracts"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
OUT = project_root / G["dir"]
VARIANTS = {
    "a_swipo2c": "2-contract SwiPO: strict row chosen = safer, permissive row chosen = better",
    "b_twotier": "two-tier SwiPO: as a_swipo2c, but the permissive row picks the safer response when the pair has a floor category",
    "c_pooled": "pooled DPO: no contract text, both label directions of every pair",
}
FLIP_TAG = f"_flip{round(100 * G['flip_fraction'])}"


def categories(row, k):
    return {c for c, v in row[f"response_{k}_harm_category"].items() if v}


def safety_class(row):
    n_safe = int(row["is_response_0_safe"]) + int(row["is_response_1_safe"])
    return ("both_unsafe", "one_safe", "both_safe")[n_safe]


def eval_contract_sentences():
    """Sentences of the eval contracts, read from the eval source with ast (no import, no execution)."""
    tree = ast.parse((project_root / G["eval_contract_source"]).read_text())
    texts, n_fragments = [], 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "INSTRUCTION_VARIANTS" for t in node.targets):
            texts += list(ast.literal_eval(node.value).values())
        if isinstance(node, ast.FunctionDef) and node.name == "synthesize_safety_instruction":
            for j in ast.walk(node):
                if isinstance(j, ast.JoinedStr):
                    parts = [v.value for v in j.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
                    texts += parts
                    n_fragments += len(parts)
    if len(texts) <= n_fragments or not n_fragments:
        raise RuntimeError(f"eval contract wording not found in {G['eval_contract_source']}")
    sents = {s.strip().lower() for t in texts for s in re.split(r"(?<=[.!?])\s+", t)}
    return sorted(s for s in sents if len(s) >= G["min_sentence_chars"])


def check_training_contracts():
    eval_sents = eval_contract_sentences()
    templates = [t for group in G["contracts"].values() for t in group]
    hits = [(s, t) for s in eval_sents for t in templates if s in t.lower()]
    if hits:
        raise RuntimeError(f"training contracts reuse eval wording: {hits[:3]}")
    print(f"Training contracts: {len(templates)} templates share none of {len(eval_sents)} eval contract sentences")
    return len(eval_sents)


def excluded_prompt_sets():
    """{source: set of normalized prompts}; Cond. Safety eval set (test split, clear contrast) reported on its own."""
    sets = {}
    for split in G["exclude_splits"]:
        ds = load_dataset(G["dataset"], split=split)
        sets[f"split:{split}"] = {norm_prompt(p) for p in ds["prompt"]}
        clear = ds.filter(lambda x: x["is_response_0_safe"] != x["is_response_1_safe"])
        sets[f"split:{split}:clear_contrast"] = {norm_prompt(p) for p in clear["prompt"]}
    for rel in G["exclude_files"]:
        path = project_root / rel
        if path.suffix == ".jsonl":
            prompts = [json.loads(line)["prompt"] for line in open(path, encoding="utf-8")]
        elif path.suffix == ".parquet":
            prompts = pd.read_parquet(path, columns=["prompt"])["prompt"].tolist()
        else:
            raise ValueError(f"unsupported exclude file type: {rel}")
        sets[f"file:{rel}"] = {norm_prompt(p) for p in prompts}
    return sets


def contract(kind, base_idx, cat_idx, cats):
    text = G["contracts"][kind][base_idx]
    if cats:
        harm_list = ", ".join(sorted(cats)).lower()
        text += "\n\n" + G["contracts"][f"{kind}_category"][cat_idx].format(harm_list=harm_list)
    return text


def row(system, prompt, chosen, rejected):
    msgs = ([{"role": "system", "content": system}] if system is not None else []) + [{"role": "user", "content": prompt}]
    return {"prompt": msgs, "chosen": [{"role": "assistant", "content": chosen}],
            "rejected": [{"role": "assistant", "content": rejected}]}


def build_rows(p, flipped):
    """Rows of every variant for one pair p (dict from the pair manifest)."""
    strict, permissive = p["contract_strict"], p["contract_permissive"]
    y_s, y_b, x = p["safer"], p["better"], p["prompt"]
    perm_floor = (y_s, y_b) if p["floor"] else (y_b, y_s)
    rows = {
        "a_swipo2c": [row(strict, x, y_s, y_b), row(permissive, x, y_b, y_s)],
        "b_twotier": [row(strict, x, y_s, y_b), row(permissive, x, *perm_floor)],
        "c_pooled": [row(None, x, y_s, y_b), row(None, x, y_b, y_s)],
    }
    if flipped is not None:  # train split: the G2 variants flip the permissive-direction row
        rows["a_swipo2c" + FLIP_TAG] = [rows["a_swipo2c"][0], row(permissive, x, y_s, y_b) if flipped else rows["a_swipo2c"][1]]
        rows["c_pooled" + FLIP_TAG] = [rows["c_pooled"][0], row(None, x, y_s, y_b) if flipped else rows["c_pooled"][1]]
    return rows


def manifest(df, rng):
    """Pair-level records (labels resolved, contracts drawn once per pair so every variant sees the same text)."""
    c = G["contracts"]
    picks = {k: rng.integers(0, len(c[k]), size=len(df)) for k in ("strict", "permissive", "strict_category", "permissive_category")}
    recs = []
    for i, (idx, r) in enumerate(df.iterrows()):
        cats = categories(r, 0) | categories(r, 1)
        s, b = int(r["safer_response_id"]), int(r["better_response_id"])
        recs.append({
            "pair_id": int(idx), "prompt": r["prompt"], "safer": r[f"response_{s}"], "better": r[f"response_{b}"],
            "safer_response_id": s, "better_response_id": b, "safety_class": safety_class(r),
            "harm_categories": sorted(cats), "floor": bool(cats & FLOOR),
            "contract_strict": contract("strict", picks["strict"][i], picks["strict_category"][i], cats),
            "contract_permissive": contract("permissive", picks["permissive"][i], picks["permissive_category"][i], cats),
        })
    return recs


def counts(series):
    return {str(k): int(v) for k, v in series.value_counts().items()}


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def outputs_valid():
    stats_path = OUT / STATS_FILE
    if not stats_path.exists():
        return False
    files = json.load(open(stats_path))["files"]
    bad = [rel for rel, m in files.items() if not (OUT / rel).exists() or file_sha256(OUT / rel) != m["sha256"]]
    if bad:
        raise RuntimeError(f"{len(bad)} files in {OUT} differ from {STATS_FILE} (e.g. {bad[0]}); delete {OUT} to rebuild")
    print(f"{OUT} already holds {len(files)} verified files; nothing to do (delete the folder to rebuild)")
    return True


def main():
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    if outputs_valid():
        return
    n_eval_sents = check_training_contracts()
    rng = np.random.default_rng(G["seed"])

    src = load_dataset(G["dataset"], split=G["source_split"]).to_pandas()
    dis = src[src["safer_response_id"] != src["better_response_id"]].copy()
    if G["drop_both_safe"]:
        dis = dis[~(dis["is_response_0_safe"] & dis["is_response_1_safe"])].copy()
        print(f"drop_both_safe: kept {len(dis):,} disagreement pairs with at least one unsafe response")
    dis["key"] = dis["prompt"].map(norm_prompt)
    print(f"{G['dataset']} {G['source_split']}: {len(src):,} pairs; safer != better: {len(dis):,} pairs, {dis['key'].nunique():,} unique prompts")

    ex_sets = excluded_prompt_sets()
    excluded = {}
    drop = np.zeros(len(dis), dtype=bool)
    for name, keys in ex_sets.items():
        hit = dis["key"].isin(keys).to_numpy()
        excluded[name] = {"unique_prompts": len(keys), "pairs_removed": int(hit.sum())}
        drop |= hit
        print(f"  exclude {name}: {len(keys):,} prompts -> {int(hit.sum()):,} pairs removed")
    excluded["pairs_removed_total"] = int(drop.sum())
    pool = dis[~drop]
    shuffled = pool.iloc[rng.permutation(len(pool))]
    dedup = shuffled.drop_duplicates("key", keep="first")
    print(f"  after exclusion: {len(pool):,} pairs; after prompt dedupe: {len(dedup):,} pairs ({len(pool) - len(dedup):,} duplicates dropped)")

    n_train, n_val = G["target_rows"] // 2, G["val_rows"] // 2
    if n_train + n_val > len(dedup):
        raise RuntimeError(f"need {n_train + n_val} pairs, only {len(dedup)} eligible")
    released = load_pku_combined_clear_contrast()
    released_rows = {"train": len(released["train"]), "val": len(released["test"])}
    print(f"Released CITA run rows: {released_rows}; target rows {G['target_rows']} / {G['val_rows']} -> pairs {n_train} / {n_val}")

    parts = {"train": dedup.iloc[:n_train].sort_index(), "val": dedup.iloc[n_train:n_train + n_val].sort_index()}
    pairs = {split: manifest(df, rng) for split, df in parts.items()}
    n_flip = round(G["flip_fraction"] * n_train)
    flip = np.zeros(n_train, dtype=bool)
    flip[rng.choice(n_train, size=n_flip, replace=False)] = True
    for i, p in enumerate(pairs["train"]):
        p["flipped"] = bool(flip[i])

    flip_variants = [v + FLIP_TAG for v in G["flip_variants"]]
    if any(v not in VARIANTS for v in G["flip_variants"]):
        raise ValueError(f"flip_variants {G['flip_variants']} must be among {list(VARIANTS)}")
    all_variants = list(VARIANTS) + flip_variants
    rows = {v: {s: [] for s in SPLITS} for v in all_variants}
    pbar = make_pbar(total=n_train + n_val, desc="g1_contracts_build", unit="pair")
    for split in SPLITS:
        for p in pairs[split]:
            built = build_rows(p, p["flipped"] if split == "train" else None)
            for v, rs in built.items():
                rows[v][split] += rs
            pbar.update(1)
    pbar.close()
    for v in flip_variants:  # validation stays clean: the base variant's val rows
        rows[v]["val"] = rows[v.removesuffix(FLIP_TAG)]["val"]

    files = {}
    for v in all_variants:
        for split in SPLITS:
            rel = f"{v}/{split}.jsonl"
            write_jsonl(OUT / rel, rows[v][split])
    for split in SPLITS:
        write_jsonl(OUT / f"pairs_{split}.jsonl", pairs[split])

    # Leak check on the written files: no eval prompt, no train/val prompt overlap, columns as TRL expects
    all_ex = set().union(*ex_sets.values())
    leaks, overlap = 0, 0
    for v in all_variants:
        keys = {}
        for split in SPLITS:
            path = OUT / f"{v}/{split}.jsonl"
            recs = [json.loads(line) for line in open(path, encoding="utf-8")]
            if any(list(r) != COLUMNS for r in recs):
                raise RuntimeError(f"{path}: columns differ from {COLUMNS}")
            keys[split] = {norm_prompt(user_prompt(r["prompt"])) for r in recs}
            leaks += len(keys[split] & all_ex)
            files[f"{v}/{split}.jsonl"] = {"rows": len(recs), "sha256": file_sha256(path)}
        overlap += len(keys["train"] & keys["val"])
    if leaks or overlap:
        raise RuntimeError(f"FATAL: {leaks} eval prompts leaked, {overlap} train/val prompt overlaps")
    for split in SPLITS:
        path = OUT / f"pairs_{split}.jsonl"
        files[f"pairs_{split}.jsonl"] = {"rows": len(pairs[split]), "sha256": file_sha256(path)}

    def share(split, field):
        n = sum(p[field] for p in pairs[split])
        return {"pairs": n, "share": round(n / len(pairs[split]), 4)}

    stats = {
        "dataset": G["dataset"], "source_split": G["source_split"], "seed": G["seed"], "drop_both_safe": G["drop_both_safe"],
        "source_pairs": len(src),
        "label_disagreement": {"pairs": len(dis), "unique_prompts": int(dis["key"].nunique()),
                               "by_safety_class": counts(dis.apply(safety_class, axis=1))},
        "excluded": excluded,
        "eligible_pairs_after_exclusion": len(pool), "duplicate_prompt_pairs_dropped": len(pool) - len(dedup),
        "eligible_pairs_after_dedupe": len(dedup),
        "released_cita_rows": released_rows, "target_rows": G["target_rows"], "val_rows": G["val_rows"],
        "pairs": {s: len(pairs[s]) for s in SPLITS},
        "floor_categories": sorted(FLOOR),
        "floor": {s: share(s, "floor") for s in SPLITS},
        "safety_class": {s: counts(pd.Series([p["safety_class"] for p in pairs[s]])) for s in SPLITS},
        "two_tier_permissive_rows_set_to_safer": {s: share(s, "floor")["pairs"] for s in SPLITS},
        "flip": {"fraction": G["flip_fraction"], "train_pairs_flipped": n_flip, "variants": flip_variants,
                 "val": "unflipped (copy of the base variant's val rows)"},
        "contract_templates": {k: len(t) for k, t in G["contracts"].items()},
        "leak_check": {"eval_prompts_in_datasets": leaks, "train_val_prompt_overlap": overlap,
                       "eval_contract_sentences_checked": n_eval_sents, "eval_sentences_in_training_contracts": 0},
        "variants": {**VARIANTS, **{v: f"G2: {VARIANTS[v.removesuffix(FLIP_TAG)]}; {n_flip} train pairs have the permissive-direction label flipped to safer"
                                    for v in flip_variants}},
        "files": files,
    }
    with open(OUT / STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps({k: stats[k] for k in ("label_disagreement", "excluded", "eligible_pairs_after_dedupe", "pairs", "floor",
                                            "safety_class", "flip", "leak_check")}, indent=2))
    print(f"Wrote {len(files)} files + {STATS_FILE} to {OUT}")


if __name__ == "__main__":
    main()
