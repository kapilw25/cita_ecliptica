"""G1/G2 contract-pair datasets: shared helpers for g1_contracts_build.py and the trainers (load with sha256 check)."""

import hashlib
import json
from pathlib import Path

from datasets import Dataset

COLUMNS = ["prompt", "chosen", "rejected"]   # TRL explicit-prompt preference format
SPLITS = ("train", "val")
STATS_FILE = "stats.json"


def norm_prompt(text: str) -> str:
    """Prompt key for exclusion and dedupe: whitespace collapsed, lower-cased."""
    return " ".join(text.split()).lower()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def user_prompt(messages: list) -> str:
    """The user turn of a prompt message list (exactly one is expected)."""
    users = [m["content"] for m in messages if m["role"] == "user"]
    if len(users) != 1:
        raise ValueError(f"expected one user turn, found {len(users)}")
    return users[0]


def load_contract_pairs(data_dir) -> tuple:
    """Load <variant>/train.jsonl and val.jsonl; FATAL if a file is missing or differs from ../stats.json."""
    data_dir = Path(data_dir).resolve()
    stats_path = data_dir.parent / STATS_FILE
    if not stats_path.exists():
        raise FileNotFoundError(f"{stats_path} missing: run src/train/g1_contracts_build.py first")
    stats = json.load(open(stats_path))
    variant = data_dir.name
    if variant not in stats["variants"]:
        raise ValueError(f"unknown variant {variant!r}; built variants: {sorted(stats['variants'])}")
    out = []
    for split in SPLITS:
        path = data_dir / f"{split}.jsonl"
        meta = stats["files"][f"{variant}/{split}.jsonl"]
        digest = file_sha256(path)
        if digest != meta["sha256"]:
            raise RuntimeError(f"{path} sha256 {digest[:12]} != stats {meta['sha256'][:12]}: re-copy or rebuild the data")
        ds = Dataset.from_list([json.loads(line) for line in open(path, encoding="utf-8")])
        if len(ds) != meta["rows"] or ds.column_names != COLUMNS:
            raise RuntimeError(f"{path}: {len(ds)} rows, columns {ds.column_names}; stats say {meta['rows']} rows, {COLUMNS}")
        out.append(ds)
    print(f"  Contract data {variant}: {stats['variants'][variant]}")
    print(f"  Train rows: {len(out[0]):,} | Val rows: {len(out[1]):,} (sha256 verified against {stats_path.name})")
    return out[0], out[1]
