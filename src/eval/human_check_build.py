"""Blinded human-check items: 50 Conditional Safety prompts (25 floor, 25 other) x both contracts, spread over the 4 as-trained Instruct models. CPU-only.
    python -u src/eval/human_check_build.py 2>&1 | tee logs/human_check_build.log
"""

import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
H = CFG["human_check"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
CS_DIR = project_root / CFG["paths"]["evaluation_dir"] / "Conditional_Safety_Evaluation"
LAB_DIR = project_root / CFG["paths"]["evaluation_dir"] / "floor_harm" / "conditional_safety" / "full"
OUT_DIR = project_root / CFG["paths"]["evaluation_dir"] / "human_check"
ARMS = {"strict": "strict_responses.csv", "permissive": "permissive_responses.csv"}


def main():
    rng = np.random.default_rng(H["seed"])
    models = H["models"]
    first = pd.read_csv(CS_DIR / models[0] / ARMS["strict"])
    is_floor = first.harm_categories.map(lambda s: bool(FLOOR & set(ast.literal_eval(s))))
    floor_ids = first.prompt_idx[is_floor].to_numpy()
    other_ids = first.prompt_idx[~is_floor].to_numpy()
    half = H["n_prompts"] // 2
    picked = np.concatenate([rng.choice(floor_ids, half, replace=False), rng.choice(other_ids, H["n_prompts"] - half, replace=False)])
    owner = np.resize(np.arange(len(models)), len(picked))
    rng.shuffle(owner)  # each prompt goes to one model, counts balanced to within one
    tables = {}
    for m in models:
        for arm, fname in ARMS.items():
            r = pd.read_csv(CS_DIR / m / fname).set_index("prompt_idx")
            lab = pd.read_csv(LAB_DIR / f"{m}_{arm}_labels.csv").set_index("prompt_idx")
            if not r.index.equals(lab.index):
                raise RuntimeError(f"{m}/{arm}: responses and Llama Guard labels cover different prompts")
            tables[(m, arm)] = r.join(lab[["unsafe"]])
    rows = []
    for pid, mi in tqdm(zip(picked, owner), total=len(picked), desc="human_check_build", unit="prompt"):
        for arm in ARMS:
            r = tables[(models[mi], arm)].loc[pid]
            rows.append({"prompt_idx": int(pid), "model": models[mi], "contract": arm, "floor": bool(FLOOR & set(ast.literal_eval(r.harm_categories))),
                         "prompt": r.prompt, "response": r.response, "heuristic_refusal": bool(r.is_refusal),
                         "llama_guard_unsafe": bool(r.unsafe)})
    order = rng.permutation(len(rows))
    key = pd.DataFrame([rows[i] for i in order])
    key.insert(0, "item_id", [f"h{i + 1:03d}" for i in range(len(key))])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    key.to_csv(OUT_DIR / "key.csv", index=False)
    items = [{"id": r.item_id, "prompt": r.prompt, "response": r.response} for r in key.itertuples()]  # blinded: no model, no contract
    json.dump(items, open(OUT_DIR / "items.json", "w"), ensure_ascii=False, indent=0)
    print(f"{len(items)} items ({key.floor.sum()} floor answers); per model {key.model.value_counts().to_dict()}; "
          f"heuristic refusals {key.heuristic_refusal.sum()}, Llama Guard unsafe {key.llama_guard_unsafe.sum()}")
    print(f"wrote {OUT_DIR / 'items.json'} and {OUT_DIR / 'key.csv'}")


if __name__ == "__main__":
    main()
