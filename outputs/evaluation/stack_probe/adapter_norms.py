"""Adapter audit: Frobenius norm of every LoRA A and B matrix in each released adapter; an adapter whose B matrices are all zero
adds nothing to the weights it is merged into (PEFT: delta W = B A * alpha / r). CPU, reads the Hub cache on the GPU box.
    python -u outputs/evaluation/stack_probe/adapter_norms.py 2>&1 | tee logs/adapter_norms.log
"""
import json
import sys
from pathlib import Path

from huggingface_hub import snapshot_download
from safetensors.torch import load_file

project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))
from src.utils.eval.model_loader import MODELS  # noqa: E402

KEYS = [f"{m}_{v}" for m in ("SFT", "DPO", "PPO", "GRPO", "CITA") for v in ("Instruct", "NoInstruct")]
OUT = project_root / "outputs/evaluation/contract_gap/adapter_norms.json"

rows = {}
for key in KEYS:
    repo = MODELS[key]["hf_repo"]
    snap = Path(snapshot_download(repo, local_files_only=True))  # FATAL if the box never downloaded it
    cfg = json.load(open(snap / "adapter_config.json"))
    w = load_file(str(snap / "adapter_model.safetensors"))
    a = {k: float(t.float().norm()) for k, t in w.items() if "lora_A" in k}
    b = {k: float(t.float().norm()) for k, t in w.items() if "lora_B" in k}
    if not a or len(a) != len(b):
        raise SystemExit(f"FATAL: {repo} has {len(a)} lora_A and {len(b)} lora_B tensors")
    rows[key] = {"hf_repo": repo, "revision": snap.name, "r": cfg["r"], "lora_alpha": cfg["lora_alpha"],
                 "n_lora_A": len(a), "n_lora_B": len(b), "n_lora_B_nonzero": sum(v > 0 for v in b.values()),
                 "sum_norm_B": sum(b.values()), "max_norm_B": max(b.values()), "sum_norm_A": sum(a.values())}
    r = rows[key]
    print(f"{key:18s} {repo:55s} B nonzero {r['n_lora_B_nonzero']:3d}/{r['n_lora_B']}  sum|B| {r['sum_norm_B']:8.3f}  "
          f"max|B| {r['max_norm_B']:.4f}  sum|A| {r['sum_norm_A']:.1f}")

noop = [k for k, r in rows.items() if r["n_lora_B_nonzero"] == 0]
OUT.write_text(json.dumps({"meta": {"what": "Frobenius norms of LoRA A and B per released adapter; all-zero B = no-op adapter",
                                    "ci": "none: exact weights, not a sample"},
                           "no_op_adapters": noop, "models": rows}, indent=2))
print(f"no-op adapters (every lora_B is zero): {noop}\nwrote {OUT.relative_to(project_root)}")
