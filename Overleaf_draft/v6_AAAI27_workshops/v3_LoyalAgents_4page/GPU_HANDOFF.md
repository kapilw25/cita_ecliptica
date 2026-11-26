# 🖥️ GPU handoff: P4 + P5 for the 4-page LoyalAgents paper

**For:** a Claude Code session running on the rented RTX PRO 6000 (vast.ai instance 62701019, 96 GB, 16 CPU, 129 GB RAM, 100 GB disk).
**From:** the Mac session writing `v3_LoyalAgents_4page/0_main.tex`. **Deadline:** LoyalAgents, Sat Nov 28 2026, 3:59 AM PST.
**Plan and reasons:** [`../v2_LoyalAgents/TODOs.md`](../v2_LoyalAgents/TODOs.md), section "4-page tasks" (P4, P5).

## Rules

| Rule | Detail |
|---|---|
| ✅ Only these scripts | `src/eval/floor_heldout.py`, `src/eval/floor_harm_classify.py`, `src/eval/floor_leakage.py --source heldout`. Do not edit the paper or other files. |
| ✅ Fail loud | Any error stops the run; never add fallbacks or `\|\| true`. |
| ✅ Report every result | Whatever the numbers show, including "a floor exists on held-out prompts". |
| ❌ No training | Inference and classification only. |
| ❌ Secrets | `HF_TOKEN` comes from `.env` (the owner adds it); never print it. |

## Steps (run in order, each inside `tmux` from the repo root)

| # | Command | What it does | ETA |
|---|---|---|---|
| 0 | `mkdir -p logs && ./setup_env_uv.sh --gpu --from-wheels 2>&1 \| tee logs/setup_env_gpu.log` then `source venv_CITA/bin/activate` | Blackwell PyTorch (cu128) + prebuilt flash-attn wheel; the scripts use SDPA, so a flash-attn failure at the end does not block them | ~10–15 min |
| 1 | check `.env` has `HF_TOKEN` (without printing it): `grep -c '^HF_TOKEN=' .env` must print 1 | Llama-3.1-8B, the 4 adapters and Llama Guard 3 are gated | 1 min |
| 2 | `python -u src/eval/floor_heldout.py --SANITY --no-wandb 2>&1 \| tee logs/floor_heldout_sanity.log` | 10 prompts × 2 contracts × 4 models: checks loading, SDPA, batching, refusal detection | ~5 min |
| 3 | `python -u src/eval/floor_harm_classify.py --source conditional_safety --SANITY --no-wandb 2>&1 \| tee logs/floor_harm_sanity.log` | Llama Guard 3 loads and returns safe/unsafe verdicts | ~3 min |
| 4 | `python -u src/eval/floor_harm_classify.py --source conditional_safety --FULL --no-wandb 2>&1 \| tee logs/floor_harm_cs.log` | **P5** on the paper's existing 1,222-prompt answers (2 arms × 4 models) | ~15 min |
| 5 | `python -u src/eval/floor_heldout.py --FULL --no-wandb 2>&1 \| tee logs/floor_heldout_full.log` | **P4** generation: 2,444 unseen prompts (918 floor) × 2 contracts × 4 Instruct models; resumes after a crash | ~1–1.5 h |
| 6 | `python -u src/eval/floor_leakage.py --source heldout 2>&1 \| tee logs/floor_leakage_heldout.log` | floor table on the held-out answers, 95% BCa (CPU) | ~5 min |
| 7 | `python -u src/eval/floor_harm_classify.py --source heldout --FULL --no-wandb 2>&1 \| tee logs/floor_harm_heldout.log` | P5 on the held-out answers | ~25 min |
| 8 | `git add outputs/evaluation/floor_heldout/full outputs/evaluation/floor_leakage/floor_leakage_heldout.json outputs/evaluation/floor_harm logs/floor_*.log && git commit -m "P4/P5 results from RTX PRO 6000" && git push` | results back to GitHub for the Mac session (needs a GitHub login on the box; if none, stop and say so) | 2 min |

## Expected outputs

| File | Content |
|---|---|
| `outputs/evaluation/floor_heldout/full/<MODEL>_Instruct/{strict,permissive}_responses.csv`, `metrics.json` | answers + refusal flags, same columns as the Conditional Safety suite |
| `outputs/evaluation/floor_leakage/floor_leakage_heldout.json` | held-out floor table (floor vs other gap, per category) |
| `outputs/evaluation/floor_harm/{conditional_safety,heldout}/full/floor_harm.json` | unsafe-answer rate per model × contract × floor/other, permissive-minus-strict difference on floor prompts, 95% BCa |

## When done

Print one table: model, strict and permissive refusal rates on the held-out set, floor-minus-other gap with its interval, and the floor unsafe rate under each contract. Stopping or destroying the instance is the owner's call, not yours.
