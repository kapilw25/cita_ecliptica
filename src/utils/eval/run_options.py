"""--non_interactive / --decode_variant flags shared by src/eval/{isd,conditional_safety,length_control,truthfulqa}.py (G3)."""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from ..config import REPO_ROOT, load_pipeline_config
from .checkpoint import set_checkpoint_root
from .cli_menus import set_non_interactive
from .generation import repetition_penalty_kwargs
from .model_loader import verify_hf_repos

CFG = load_pipeline_config()
DECODE_KEYS = ("repetition_penalty", "repetition_penalty_scope", "stop_tokens")  # batch_generate kwargs per preset


def add_run_args(parser: argparse.ArgumentParser) -> None:
    """Add --non_interactive and --decode_variant (the suite adds --mode itself)."""
    parser.add_argument("--non_interactive", action="store_true",
                        help="no menus, no stdin: needs --mode; evaluates only --models, resumes their checkpoints, "
                             "reuses completed ones, never deletes results; FATAL if any model fails")
    parser.add_argument("--decode_variant", choices=sorted(CFG["decode_variants"]), default=None,
                        help="decoding preset (configs/pipeline.yaml decode_variants); outputs and checkpoints go to "
                             "<paths.evaluation_dir>/<name>/ (needs --non_interactive)")


def variant_root(name: str) -> Path:
    """<paths.evaluation_dir>/<name>: a decode variant's tree, mirroring the paper's outputs/evaluation layout."""
    return REPO_ROOT / CFG["paths"]["evaluation_dir"] / name


def resolve_run(args: argparse.Namespace, parser: argparse.ArgumentParser, default_output_dir: Path) -> Tuple[Path, Dict]:
    """Apply the flags: returns (suite output dir, batch_generate decoding kwargs); without flags (default dir, {})."""
    if args.decode_variant and not args.non_interactive:
        parser.error("--decode_variant needs --non_interactive")
    if not args.non_interactive:
        return default_output_dir, {}
    if args.mode is None:
        parser.error("--non_interactive needs --mode")
    set_non_interactive(True)
    if args.decode_variant is None:
        print(f"--non_interactive: mode={args.mode}, paper decoding, outputs in {default_output_dir}")
        return default_output_dir, {}
    preset = CFG["decode_variants"][args.decode_variant]
    decode = {k: preset[k] for k in DECODE_KEYS}
    repetition_penalty_kwargs(decode["repetition_penalty"], decode["repetition_penalty_scope"], 0)  # FATAL before model load
    root = variant_root(args.decode_variant)
    root.mkdir(parents=True, exist_ok=True)
    _pin_preset(root / "decode_variant.json", args.decode_variant, decode)
    set_checkpoint_root(root / "checkpoints")
    output_dir = root / default_output_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"--non_interactive: mode={args.mode}, decode_variant={args.decode_variant} {decode}")
    print(f"   outputs: {output_dir}\n   checkpoints: {root / 'checkpoints'}")
    return output_dir, decode


def _pin_preset(path: Path, name: str, decode: Dict) -> None:
    """First run records the preset beside its outputs; a later run FATALs if the YAML preset has changed since."""
    record = {"decode_variant": name, **decode}
    if path.exists():
        with open(path) as f:
            pinned = json.load(f)
        if pinned != record:
            raise RuntimeError(f"{path} records {pinned}, configs/pipeline.yaml now gives {record}: "
                               f"outputs would mix two decodings (use a new preset name)")
        return
    tmp = path.with_suffix(f".tmp{os.getpid()}")
    with open(tmp, "w") as f:
        json.dump(record, f, indent=2)
    os.replace(tmp, path)  # atomic: suites started together never read a half-written file


def verify_models(model_keys: List[str], non_interactive: bool) -> List[str]:
    """verify_hf_repos as before; in --non_interactive mode FATAL if any requested model is missing on the Hub."""
    valid = verify_hf_repos(model_keys, interactive=not non_interactive)
    missing = [m for m in model_keys if m not in valid]
    if non_interactive and missing:
        raise SystemExit(f"FATAL: models not found on the Hub: {missing}")
    return valid


def fail_on_missing(model_keys: Iterable[str], done: Iterable[str], suite: str) -> None:
    """--non_interactive end-of-run check: every requested model produced results, else exit non-zero."""
    keys, done = list(model_keys), set(done)
    missing = [m for m in keys if m not in done]
    if missing:
        raise SystemExit(f"FATAL: {suite}: no results for {missing}")
    print(f"{suite}: all {len(keys)} requested models have results")
