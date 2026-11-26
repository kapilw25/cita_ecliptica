"""Shared GPU batch generation + chat-template formatting + memory cleanup."""

import gc
import inspect
import torch
from typing import List, Dict, Callable, Optional
from tqdm import tqdm
from transformers import LogitsProcessorList, RepetitionPenaltyLogitsProcessor

PENALTY_SCOPES = ("all", "generated")  # all = HF/vLLM default (prompt + generated tokens); generated = prompt exempt


def cleanup_gpu():
    """
    Proper GPU memory cleanup

    Call after unloading models to ensure memory is freed.
    Uses gc.collect() + torch.cuda.empty_cache() like toxicity.py
    """
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def repetition_penalty_kwargs(penalty: Optional[float], scope: str, prompt_len: int) -> Dict:
    """model.generate kwargs for a repetition penalty; {} when penalty is None (paper decoding, nothing passed)."""
    if penalty is None:
        return {}
    if scope not in PENALTY_SCOPES:
        raise ValueError(f"repetition_penalty_scope must be one of {PENALTY_SCOPES}, got {scope!r}")
    kwargs = {"repetition_penalty": penalty}  # builds HF's processor at its default slot (before temperature/top-p)
    if scope == "generated":
        if "prompt_ignore_length" not in inspect.signature(RepetitionPenaltyLogitsProcessor.__init__).parameters:
            raise RuntimeError("repetition_penalty_scope='generated' needs transformers>=4.52 (prompt_ignore_length)")
        # same type as the default processor, so generate() swaps it in at the same slot (HF logs a warning once)
        kwargs["logits_processor"] = LogitsProcessorList(
            [RepetitionPenaltyLogitsProcessor(penalty=penalty, prompt_ignore_length=prompt_len)])
    return kwargs


def stop_token_kwargs(tokenizer, stop_tokens: Optional[List[str]]) -> Dict:
    """model.generate eos_token_id override from token strings; {} when None (model's generation_config decides)."""
    if stop_tokens is None:
        return {}
    ids = [tokenizer.convert_tokens_to_ids(t) for t in stop_tokens]
    bad = [t for t, i in zip(stop_tokens, ids) if i is None or i == tokenizer.unk_token_id]
    if bad:
        raise ValueError(f"stop tokens not in the tokenizer vocabulary: {bad}")
    return {"eos_token_id": ids}


def batch_generate(
    model,
    tokenizer,
    prompts: List[str],
    batch_size: int = 8,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    do_sample: bool = True,
    show_progress: bool = True,
    desc: str = "Generating",
    checkpoint_callback: Callable = None,
    checkpoint_interval: int = 100,
    repetition_penalty: Optional[float] = None,
    repetition_penalty_scope: str = "all",
    stop_tokens: Optional[List[str]] = None
) -> List[str]:
    """
    Batch generation with configurable batch_size

    Args:
        model: Loaded model
        tokenizer: Loaded tokenizer
        prompts: List of formatted prompts (already with chat template applied)
        batch_size: Number of prompts to process at once (default 8)
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        do_sample: Whether to use sampling
        show_progress: Show tqdm progress bar
        desc: Description for progress bar
        checkpoint_callback: Function to call for checkpointing (receives list of responses so far)
        checkpoint_interval: Save checkpoint every N responses
        repetition_penalty: None = not passed to generate (paper decoding); else HF repetition_penalty
        repetition_penalty_scope: "all" (prompt + generated tokens) or "generated" (prompt exempt)
        stop_tokens: None = model's generation_config eos; else token strings that end generation

    Returns:
        List of generated response strings
    """
    responses = []
    device = next(model.parameters()).device
    stop_kwargs = stop_token_kwargs(tokenizer, stop_tokens)

    iterator = range(0, len(prompts), batch_size)
    if show_progress:
        iterator = tqdm(iterator, desc=desc, total=(len(prompts) + batch_size - 1) // batch_size)

    for i in iterator:
        batch_prompts = prompts[i:i+batch_size]

        # Tokenize batch
        inputs = tokenizer(
            batch_prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=2048
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate batch
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                pad_token_id=tokenizer.eos_token_id,
                **repetition_penalty_kwargs(repetition_penalty, repetition_penalty_scope, inputs["input_ids"].shape[1]),
                **stop_kwargs
            )

        # Decode responses (skip prompt tokens)
        for j, output in enumerate(outputs):
            prompt_length = inputs['input_ids'][j].shape[0]
            response = tokenizer.decode(
                output[prompt_length:],
                skip_special_tokens=True
            ).strip()
            responses.append(response)

        # Checkpoint callback
        if checkpoint_callback and len(responses) % checkpoint_interval == 0:
            checkpoint_callback(responses)

    return responses


def format_chat_messages(
    tokenizer,
    messages_list: List[List[Dict[str, str]]],
    add_generation_prompt: bool = True
) -> List[str]:
    """
    Format multiple message lists using chat template

    Args:
        tokenizer: Tokenizer with chat_template
        messages_list: List of message lists, each like [{"role": "system", ...}, {"role": "user", ...}]
        add_generation_prompt: Whether to add generation prompt

    Returns:
        List of formatted prompt strings
    """
    formatted = []
    for messages in messages_list:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt
        )
        formatted.append(text)
    return formatted
