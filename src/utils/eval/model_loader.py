"""Llama-3.1-8B + LoRA adapter loader (10-method MODELS dict, FA2 + BF16)."""

import gc
import time
import torch
from typing import Tuple, List

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from huggingface_hub import HfApi

from pathlib import Path

from ..train.model_utils import load_hf_token

# Repo root: src/utils/eval/model_loader.py → up 4 = repo root
project_root = Path(__file__).resolve().parent.parent.parent.parent

# ===================================================================
# Shared Configuration
# ===================================================================

BASE_MODEL = "meta-llama/Llama-3.1-8B"
MODEL_NAME = "Llama-3.1-8B"  # Short name for figure titles
HF_TOKEN = load_hf_token(project_root)

# Standardized model configurations (used by ALL evaluation scripts)
MODELS = {
    # "Baseline": {
    #     "hf_repo": None,  # No adapter - just base model
    #     "display_name": "Baseline (Unaligned)",
    #     "use_instruction": False,
    # },
    "SFT_NoInstruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-SFT-NoInstruct-Baseline-NoInstruct",
        "display_name": "SFT NoInstruct",
        "use_instruction": False,
    },
    "SFT_Instruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-SFT-Instruct-Baseline-NoInstruct",
        "display_name": "SFT Instruct",
        "use_instruction": True,
    },
    "DPO_NoInstruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-DPO-NoInstruct-SFT-NoInstruct",
        "display_name": "DPO NoInstruct",
        "use_instruction": False,
    },
    "DPO_Instruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-DPO-Instruct-SFT-Instruct",
        "display_name": "DPO Instruct",
        "use_instruction": True,
    },
    "CITA_NoInstruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-CITA-NoInstruct-DPO-NoInstruct",
        "display_name": "CITA NoInstruct",
        "use_instruction": False,
    },
    "CITA_Instruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-CITA-Instruct-DPO-Instruct",
        "display_name": "CITA Instruct",
        "use_instruction": True,
    },
    "PPO_NoInstruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-PPO-NoInstruct-SFT-NoInstruct",
        "display_name": "PPO NoInstruct",
        "use_instruction": False,
    },
    "PPO_Instruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-PPO-Instruct-SFT-Instruct",
        "display_name": "PPO Instruct",
        "use_instruction": True,
    },
    "GRPO_NoInstruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-GRPO-NoInstruct-SFT-NoInstruct",
        "display_name": "GRPO NoInstruct",
        "use_instruction": False,
    },
    "GRPO_Instruct": {
        "hf_repo": "kapilw25/llama3-8b-pku-GRPO-Instruct-SFT-Instruct",
        "display_name": "GRPO Instruct",
        "use_instruction": True,
    },
    "Llama31_Instruct_Prompted": {  # G4: off-the-shelf Instruct model, contract given only in the prompt
        "hf_repo": None,
        "base_model": "meta-llama/Llama-3.1-8B-Instruct",
        "display_name": "Llama-3.1-8B-Instruct (prompted)",
        "use_instruction": True,
    },
    # G1/G2: local LoRA folders from src/train/{cita,dpo}.py --output-dir (never on the Hub: the permissive-trained
    # adapters are not released). An absolute hf_repo is a local folder (Hub ids are never absolute). All take the
    # eval contracts (use_instruction True): pooled DPO saw no contract in training, but it must get the same strict
    # and permissive system prompts as SwiPO at eval, otherwise its strict-minus-permissive gap is 0 by construction.
    "G1a_SwiPO2C_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g1/a_swipo2c/lora_model_CITA_Instruct"),
        "display_name": "G1a SwiPO 2-contract",
        "use_instruction": True,
    },
    "G1b_SwiPOTwoTier_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g1/b_twotier/lora_model_CITA_Instruct"),
        "display_name": "G1b SwiPO two-tier",
        "use_instruction": True,
    },
    "G1c_PooledDPO_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g1/c_pooled/lora_model_DPO_Instruct"),
        "display_name": "G1c pooled DPO (no contract)",
        "use_instruction": True,
    },
    "G2a_SwiPO2C_Flip30_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g2/a_swipo2c_flip30/lora_model_CITA_Instruct"),
        "display_name": "G2a SwiPO 2-contract, 30% permissive flipped",
        "use_instruction": True,
    },
    "G2c_PooledDPO_Flip30_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g2/c_pooled_flip30/lora_model_DPO_Instruct"),
        "display_name": "G2c pooled DPO, 30% permissive flipped",
        "use_instruction": True,
    },
    # G1 c1: pooled no-contract data trained with cita.py and the SwiPO settings (G1c above = c2, dpo.py settings);
    # contracts at eval for the same reason as c2.
    "G1c1_PooledSwiPO_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g1/c_pooled_cita/lora_model_CITA_Instruct"),
        "display_name": "G1c1 pooled, SwiPO settings (no contract)",
        "use_instruction": True,
    },
    # G5: seed reruns on one box (Blackwell, SDPA), seed 3407 included so all three seeds share the stack.
    "G5_DPO_seed3407_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/DPO_Instruct_seed3407/lora_model_DPO_Instruct"),
        "display_name": "DPO Instruct (G5 seed 3407)",
        "use_instruction": True,
    },
    "G5_DPO_seed1_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/DPO_Instruct_seed1/lora_model_DPO_Instruct"),
        "display_name": "DPO Instruct (G5 seed 1)",
        "use_instruction": True,
    },
    "G5_DPO_seed2_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/DPO_Instruct_seed2/lora_model_DPO_Instruct"),
        "display_name": "DPO Instruct (G5 seed 2)",
        "use_instruction": True,
    },
    "G5_CITA_seed3407_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/CITA_Instruct_seed3407/lora_model_CITA_Instruct"),
        "display_name": "CITA Instruct (G5 seed 3407)",
        "use_instruction": True,
    },
    "G5_CITA_seed1_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/CITA_Instruct_seed1/lora_model_CITA_Instruct"),
        "display_name": "CITA Instruct (G5 seed 1)",
        "use_instruction": True,
    },
    "G5_CITA_seed2_Instruct": {
        "hf_repo": str(project_root / "outputs/training/g5/CITA_Instruct_seed2/lora_model_CITA_Instruct"),
        "display_name": "CITA Instruct (G5 seed 2)",
        "use_instruction": True,
    },
}


def is_local_adapter(hf_repo) -> bool:
    """True when an entry's hf_repo is a local adapter folder (absolute path) rather than a Hub id."""
    return hf_repo is not None and Path(hf_repo).is_absolute()


def local_adapter_dir(hf_repo: str) -> str:
    """FATAL if the local adapter folder is missing (train it with --output-dir or copy it to this box first)."""
    if not (Path(hf_repo) / "adapter_config.json").exists():
        raise FileNotFoundError(f"local adapter missing: {hf_repo} (no adapter_config.json)")
    return hf_repo


# ===================================================================
# Model Loading
# ===================================================================

def load_model_for_eval(model_key: str, attn_implementation: str = "flash_attention_2",
                        max_gpu_memory: str = "22GiB") -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    """
    Load model from HuggingFace in BF16

    Args:
        model_key: Key from MODELS dict (e.g., "CITA_Instruct", "DPO_NoInstruct")
        attn_implementation: "flash_attention_2" (default, falls back to SDPA when flash-attn is missing) or "sdpa"
            (Blackwell boxes without a flash-attn build; loaded directly, no fallback)
        max_gpu_memory: GPU memory cap for device_map="auto" (default 22GiB as before; 96GB cards can raise it)

    Returns:
        Tuple of (model, tokenizer)
    """
    print(f"\n{'='*80}")
    print(f"Loading {MODELS[model_key]['display_name']} for evaluation")
    print(f"{'='*80}")

    model_info = MODELS[model_key]
    hf_repo = model_info["hf_repo"]
    base_model = model_info.get("base_model", BASE_MODEL)  # per-entry base (prompted Instruct baseline); default = SFT base

    if is_local_adapter(hf_repo):
        print(f"Loading local adapter: {local_adapter_dir(hf_repo)}")
    elif hf_repo:
        print(f"Loading from HuggingFace: {hf_repo}")
    else:
        print("Loading base model (no adapter)")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model, token=HF_TOKEN)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"  # Required for decoder-only models in batch generation

    # Set Llama-3.1 chat template
    if tokenizer.chat_template is None:
        tokenizer.chat_template = (
            "{% for message in messages %}"
            "{% if loop.first and message['role'] != 'system' %}"
            "{{ '<|begin_of_text|>' }}"
            "{% endif %}"
            "{{ '<|start_header_id|>' + message['role'] + '<|end_header_id|>\\n\\n' + message['content'] + '<|eot_id|>' }}"
            "{% endfor %}"
            "{% if add_generation_prompt %}"
            "{{ '<|start_header_id|>assistant<|end_header_id|>\\n\\n' }}"
            "{% endif %}"
        )
        print("Set Llama-3.1 chat template")

    # Load base model in BF16
    print(f"Loading base model in BF16: {base_model}")

    # Force GPU-only (no CPU offloading) to prevent Flash Attention failures
    max_memory = {0: max_gpu_memory, "cpu": "0GiB"}  # Explicitly disallow CPU offloading

    if attn_implementation == "sdpa":
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            max_memory=max_memory,
            attn_implementation="sdpa",
            token=HF_TOKEN
        )
        print("Using PyTorch SDPA attention")
    elif attn_implementation != "flash_attention_2":
        raise ValueError(f"attn_implementation must be 'flash_attention_2' or 'sdpa', got {attn_implementation!r}")
    else:
        try:
            model = AutoModelForCausalLM.from_pretrained(
                base_model,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                max_memory=max_memory,
                attn_implementation="flash_attention_2",
                token=HF_TOKEN
            )
            print("Using Flash Attention 2")
        except Exception:
            print("Flash Attention 2 unavailable, using PyTorch SDPA")
            model = AutoModelForCausalLM.from_pretrained(
                base_model,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                max_memory=max_memory,
                attn_implementation="sdpa",
                token=HF_TOKEN
            )

    # Load LoRA adapter if specified
    if hf_repo is not None:
        source = "local folder" if is_local_adapter(hf_repo) else "HuggingFace"
        print(f"{'Loading' if is_local_adapter(hf_repo) else 'Downloading'} adapter from {source}: {hf_repo}")
        try:
            model = PeftModel.from_pretrained(model, hf_repo, token=HF_TOKEN)
            print("Merging adapter weights...")
            model = model.merge_and_unload()
            print("Adapter merged")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load adapter from {source}: {hf_repo}\n"
                f"Error: {e}\n\n"
                f"Possible causes:\n"
                f"  1. Model not yet trained and pushed to HuggingFace\n"
                f"  2. Training performance did not improve (push_automation skipped push)\n"
                f"  3. HuggingFace authentication issue (check HF_TOKEN in .env)\n"
            )

    model.eval()
    print(f"{MODELS[model_key]['display_name']} loaded successfully")

    return model, tokenizer


def unload_model(model):
    """Free GPU memory with proper cleanup"""
    if model is not None:
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            # Force inter-process memory collection
            torch.cuda.ipc_collect()
        print("Model unloaded, GPU memory freed")
        time.sleep(5)  # Give GPU time to fully release memory


def verify_hf_repos(model_keys: List[str], interactive: bool = True) -> List[str]:
    """
    Pre-flight verification of HuggingFace repositories

    Args:
        model_keys: List of model keys to verify
        interactive: If True, prompt user on missing repos

    Returns:
        List of valid model keys (missing ones removed)
    """
    print("\n" + "=" * 80)
    print("Verifying HuggingFace repositories...")
    print("=" * 80)

    hf_api = HfApi()
    missing_repos = []
    valid_keys = []

    for model_key in model_keys:
        if model_key not in MODELS:
            print(f"  ❌ {model_key}: Unknown model key")
            continue

        hf_repo = MODELS[model_key]['hf_repo']
        if is_local_adapter(hf_repo):  # no Hub check; FATAL (not skippable) when the folder is missing
            print(f"  ✅ {model_key}: {local_adapter_dir(hf_repo)} (local)")
            valid_keys.append(model_key)
        elif hf_repo:
            try:
                hf_api.repo_info(repo_id=hf_repo, repo_type="model", token=HF_TOKEN)
                print(f"  ✅ {model_key}: {hf_repo}")
                valid_keys.append(model_key)
            except Exception:
                print(f"  ❌ {model_key}: {hf_repo} (NOT FOUND)")
                missing_repos.append(model_key)
        else:
            print(f"  ✅ {model_key}: (base model only, no adapter)")
            valid_keys.append(model_key)

    if missing_repos and interactive:
        print("\n" + "=" * 80)
        print("⚠️  WARNING: Some models are missing from HuggingFace")
        print("=" * 80)
        print(f"Missing models: {', '.join(missing_repos)}")
        print("\nOptions:")
        print("  1) Continue evaluation (skip missing models)")
        print("  2) Abort evaluation")
        print("=" * 80)

        while True:
            choice = input("\nEnter choice (1 or 2): ").strip()
            if choice == "1":
                print("\n✅ Continuing evaluation (will skip missing models)")
                break
            elif choice == "2":
                print("\n❌ Aborting evaluation")
                return []
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")

    return valid_keys
