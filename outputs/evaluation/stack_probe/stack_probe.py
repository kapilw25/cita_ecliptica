"""Diagnostic: does eval-time adapter stacking change behavior? Paper path loads base + one LoRA delta; training merged the parent first.
    cd /root/cita_ecliptica && source venv_CITA/bin/activate && python -u /root/stack_probe.py 100 2>&1 | tee /root/stack_probe/probe.log
"""
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from peft import PeftModel

sys.path.insert(0, "/root/cita_ecliptica")
from src.eval import conditional_safety as cs  # noqa: E402
from src.utils.eval import MODELS, batch_generate, cleanup_gpu, format_chat_messages, load_model_for_eval  # noqa: E402
from src.utils.eval.model_loader import HF_TOKEN  # noqa: E402

N = int(sys.argv[1])
MAX_NEW = 256
OUT = Path("/root/stack_probe")
OUT.mkdir(exist_ok=True)
VARIANTS = [  # (name, loader key = what load_model_for_eval merges, extra adapter merged on top)
    ("DPO_paper", "DPO_Instruct", None),
    ("DPO_stacked_SFT+DPO", "SFT_Instruct", "DPO_Instruct"),
    ("SwiPO_paper", "CITA_Instruct", None),
    ("SwiPO_astrained_DPO+SwiPO", "DPO_Instruct", "CITA_Instruct"),
]


def rep_frac(t):
    s = [x.strip() for x in re.split(r"(?<=[.!?])\s+", str(t)) if x.strip()]
    return 0.0 if len(s) < 2 else 1 - len(set(s)) / len(s)


prompts, cats = cs.load_safety_test_set(max_samples=N)
summary = {}
for name, key, extra in VARIANTS:
    t0 = time.time()
    model, tok = load_model_for_eval(key, attn_implementation="sdpa", max_gpu_memory="40GiB")
    if extra:
        print(f"merging {MODELS[extra]['hf_repo']} on top of {key}")
        model = PeftModel.from_pretrained(model, MODELS[extra]["hf_repo"], token=HF_TOKEN).merge_and_unload().eval()
    summary[name] = {}
    for variant in ("STRICT", "PERMISSIVE"):
        msgs = [[{"role": "system", "content": cs.synthesize_safety_instruction(c, variant)}, {"role": "user", "content": p}]
                for p, c in zip(prompts, cats)]
        outs = batch_generate(model=model, tokenizer=tok, prompts=format_chat_messages(tok, msgs), batch_size=50,
                              max_new_tokens=MAX_NEW, temperature=0.7, top_p=0.9, do_sample=True, show_progress=True,
                              desc=f"{name}/{variant}")
        ntok = np.array([len(tok(o, add_special_tokens=False)["input_ids"]) for o in outs])
        ref = np.array([cs.detect_refusal_heuristic(o)["is_refusal"] for o in outs], dtype=float)
        rep = np.array([rep_frac(o) for o in outs])
        summary[name][variant] = {"refusal": float(ref.mean()), "stopped_before_cap": float((ntok < MAX_NEW - 4).mean()),
                                  "mean_tokens": float(ntok.mean()), "repetitive_gt_0.3": float((rep > 0.3).mean()),
                                  "examples": [o[:400] for o in outs[:3]]}
        with open(OUT / f"{name}_{variant}.json", "w") as f:
            json.dump([{"prompt": p, "response": o} for p, o in zip(prompts, outs)], f, indent=1)
    s, p = summary[name]["STRICT"], summary[name]["PERMISSIVE"]
    summary[name]["refusal_gap"] = s["refusal"] - p["refusal"]
    print(f"== {name}: gap {summary[name]['refusal_gap']:+.3f} | strict ref {s['refusal']:.2f} perm ref {p['refusal']:.2f} | "
          f"stopped {s['stopped_before_cap']:.2f}/{p['stopped_before_cap']:.2f} | repetitive {s['repetitive_gt_0.3']:.2f}/"
          f"{p['repetitive_gt_0.3']:.2f} | {time.time() - t0:.0f}s", flush=True)
    del model
    cleanup_gpu()
    with open(OUT / "summary.json", "w") as f:
        json.dump(summary, f, indent=1)
print("STACK_PROBE_DONE")
