# ✅ TODOs: v2_LoyalAgents from ~51 to 80/100

**Target venue:** 🤝 [LoyalAgents (W27)](https://loyalagents.github.io/aaai27/) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/LoyalAgents) · ⏰ **Sat Nov 28, 3:59 AM PST** · 📬 Wed Dec 2 · 📄 full ≤ 8 p · 🟢 whose contract the agent follows

**Built from** the three judges' Step 2 reviews of the SC4AI version (same paper, other framing):
[ChatGPT](../feedback/output/v1_SC4AI/by_chatgpt/step2.md) (49) ·
[Claude](../feedback/output/v1_SC4AI/by_claude/step2.md) (51) ·
[Gemini](../feedback/output/v1_SC4AI/by_gemini/step2.md) (62.5). Written 2026-11-26.

**Decisions (owner, 2026-11-26):** one merged 10-rubric scale · ETAs for RTX Pro 6000 96GB · split into batches (LoyalAgents itself gets the 4-page paper, see below) · rubrics re-mapped to LoyalAgents.

**Legend:** 🖥️ GPU task · 📝 non-GPU task · 🅿️ 4-page task · 🔴 batch 1 of the 8-page plan · 🟡 batch 2 (later venues) · ⚠️ needs your OK first · R1–R10 merged rubrics below

## 🆕 Plan change (owner, 2026-11-26): LoyalAgents gets a 4-page finding paper

**What goes to LoyalAgents by Sat Nov 28, 3:59 AM PST:** one 4-page finding paper in [`../v3_LoyalAgents_4page/`](../v3_LoyalAgents_4page/). Its claim is "whose contract does the agent follow? There's no safety floor by default", and SwiPO appears as one of the four trained models rather than as the headline. Every claim in it rests on results we already have.

**Why 4 pages:** the call says shorter papers are "reviewed relative to their length", and it accepts one paper per idea (no per-author limit, single-blind). A short paper avoids the judges' top reason to reject: it no longer claims what SwiPO's unrun multi-contract experiment would show. **The 8-page `v2_LoyalAgents/` and every G/N task below move to the next venue** (Bench2Evidence Dec 2, then later calls).

### 🅿️ 4-page tasks (before Sat Nov 28, 3:59 AM PST)

**Owner decision (2026-11-26):** run all of them: GPU tasks P4 and P5, and the new CPU task P7. The GPU work runs on a rented RTX PRO 6000 that this Mac session drives over SSH (see the [gpu-ssh-desktop guide](../../../docs/guide_gpu_ssh_claude_desktop.md)).

**Status:** ✅ done · 🌓 partly done · ⏳ running · 🕒 queued · ⛔ waiting on another task · 👤 owner action · 🔁 changed by owner order
**Times:** PST, updated Thu Nov 26, 07:48 AM from live progress (62 to 77 s per batch per process while 4 jobs share the GPU). Times marked "est." are projections from the measured speed and are re-checked as runs finish.

#### 🖥️ GPU tasks (4-page)

One RTX PRO 6000 (96 GB). Only the 4 Instruct models are needed, because the floor analysis uses Instruct models. Since 06:31 AM the 4 models run as parallel processes, and a chain script starts each next step by itself.

| ID | Status | Task | Files | ETA (PST) | Effect on the judges' concerns |
|---|---|---|---|---|---|
| **P4a** | ✅ | Build held-out prompts: PKU-SafeRLHF prompts outside the 12,035 pair training pool, deduplicated, with harm categories. 2,444 prompts, 918 of them floor prompts, none in the pool | [floor_heldout_build.py](../../../src/eval/floor_heldout_build.py) · [heldout_prompts.jsonl](../../../outputs/evaluation/floor_heldout/heldout_prompts.jsonl) · pool rule in [loader_pku.py](../../../src/utils/train/data_prep/loader_pku.py) | done Thu Nov 26 | sets up the held-out test |
| **P4b** | ✅ | Smoke test: 10 prompts × 2 contracts × 4 models | [floor_heldout.py](../../../src/eval/floor_heldout.py) | done Thu Nov 26, 06:24 AM | loading, SDPA and refusal scoring work |
| **P4c** | ✅ | Held-out generation: strict and permissive contracts on all 2,444 prompts, 4 Instruct models in parallel. Same contracts and refusal detector as the suite. Refusal gap (strict minus permissive): DPO 0.501, SwiPO 0.405, PPO 0.309, GRPO 0.309, close to the suite's 0.489 / 0.400 / 0.303 / 0.325 | [floor_heldout.py](../../../src/eval/floor_heldout.py) · contracts from [conditional_safety.py](../../../src/eval/conditional_safety.py) · [answers](../../../outputs/evaluation/floor_heldout/full/) | done Thu Nov 26, 08:00 AM | removes the "9 in 10 floor prompts seen in training" caveat (R9 7.7 → 8.5) |
| **P4d** | ✅ | Held-out floor table with 95% BCa (918 floor of 2,444 prompts). Floor minus other prompts, permissive-contract refusal gap: every interval spans zero (DPO +0.015, PPO +0.041, GRPO +0.023, SwiPO +0.046), so no floor by default on unseen prompts either. Per-category gaps: 74 of 76 above zero (PPO Environmental Damage and GRPO Copyright Issues span zero) | [floor_leakage.py](../../../src/eval/floor_leakage.py) · [floor_leakage_heldout.json](../../../outputs/evaluation/floor_leakage/floor_leakage_heldout.json) | done Thu Nov 26, 08:00 AM | same |
| **P5a** | ✅ | Smoke test: Llama Guard 3 verdicts on 10 answers | [floor_harm_classify.py](../../../src/eval/floor_harm_classify.py) | done Thu Nov 26, 06:25 AM | classifier loads and parses |
| **P5b** | ✅ | Harmful vs safe answers on the paper's 1,222 prompts (347 floor), strict and permissive, 4 models. Floor unsafe rate, permissive minus strict: DPO +0.104, GRPO +0.075, SwiPO +0.124 (95% intervals above zero), PPO −0.017 (spans zero; about half unsafe under both). ⚠️ Adds a model-based classifier to one analysis; the "no LLM judge" sentence must say so | [floor_harm_classify.py](../../../src/eval/floor_harm_classify.py) · input answers in [Conditional Safety outputs](../../../outputs/evaluation/Conditional_Safety_Evaluation/) | done Thu Nov 26, 06:51 AM | turns "bounds harm from above" into a measured harm rate (R9 8.5 → 9.0) |
| **P5c** | ✅ | Same classifier on the held-out answers. Floor unsafe rate, strict → permissive: DPO 0.069 → 0.157, SwiPO 0.385 → 0.534, PPO 0.588 → 0.633, GRPO 0.580 → 0.631; every permissive-minus-strict interval above zero (SwiPO +0.149 [+0.107, +0.191] is the largest) | [floor_harm_classify.py](../../../src/eval/floor_harm_classify.py) · [floor_harm.json](../../../outputs/evaluation/floor_harm/heldout/full/floor_harm.json) | done Thu Nov 26, 08:15 AM | harm rate on unseen prompts |
| **P5d** | ✅ | Copy all results from the box to this Mac (scp), commit and push | [floor_heldout](../../../outputs/evaluation/floor_heldout/) · [floor_harm](../../../outputs/evaluation/floor_harm/) | done Thu Nov 26, 08:25 AM | results reach the paper |
| **P5e** | 🔁 | Box kept: owner order 08:30 AM, "complete all GPU tasks mentioned in TODOs, do NOT STOP" (List 1 below). Destroy after the last G task | vast.ai console | after List 1 | stops cost |

#### 📝 Non-GPU tasks (4-page)

| ID | Status | Task | Files | ETA (PST) | Effect on the judges' concerns |
|---|---|---|---|---|---|
| **P1** | ✅ | Outline from v2 and v1: abstract, intro, "Whose contract?" section, lever table, floor table, Figure 1 example, setup, results, open problems, scope statement | [v2 paper](../v2_LoyalAgents/0_main.tex) · [v1 paper](../v1_SC4AI/0_main.tex) | done Thu Nov 26 | sets what the paper claims |
| **P7** | ✅ | Per-category figure: refusal gap (strict minus permissive) for 19 harm categories × 4 trainers, 95% BCa whiskers, floor rows marked. Result: all 76 gaps above zero | [floor_per_category_plot.py](../../../src/eval/floor_per_category_plot.py) · [figure PNG](../../../outputs/evaluation/floor_leakage/figures/v1_floor_per_category.png) | done Thu Nov 26 | new evidence from existing data (R9 +, R5 +) |
| **P2a** | ✅ | Write the 4-page paper, finding first; efficiency gets one sentence; "not separable from DPO", never "tied" | [4-page paper](../v3_LoyalAgents_4page/0_main.tex) | done Thu Nov 26 | the "designed experiment unrun" and "AQI in the headline" problems become non-issues; fixes tone (R10) |
| **P2b** | ✅ | Add the P4 and P5 numbers, keep 4 pages: held-out columns in the floor table, a "Harmful answers" paragraph (Llama Guard 3), "no LLM judge" qualified, limitations updated, abstract and contribution 3 mention the replication | [4-page paper](../v3_LoyalAgents_4page/0_main.tex) | done Thu Nov 26, 09:10 AM | R9 |
| **P3a** | ✅ | Build + e2e audit (4 pages) + version check against v4: 0 FAIL | [audit skill](../../../.claude/skills/audit-paper-e2e-draft/SKILL.md) | done Thu Nov 26 | ready to submit as is |
| **P3b** | ✅ | Re-run build, audit and version check after P2b: 0 FAIL, 2 WARN, main text ends on page 4 | [audit skill](../../../.claude/skills/audit-paper-e2e-draft/SKILL.md) | done Thu Nov 26, 09:15 AM | 0 FAIL before submitting |
| **P6** | 👤 | Submit on OpenReview: single-blind; disclose arXiv 2601.06157 and the SC4AI submission; paste the new abstract | [LoyalAgents OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/LoyalAgents) | any time now (G4 or G1 rows may still be added); deadline **Sat Nov 28, 3:59 AM** | submission |

**Risks that remain in the 4-page paper:** one backbone and one seed; about 9 in 10 floor prompts were seen in training (P4 fixes this); a non-refusal isn't necessarily harmful (P5 fixes this). The judges scored the 8-page SC4AI version, so the 4-page paper has no rubric score yet.

## 📌 Score path (8-page v2, next venue)

| Stage | Merged score | What gets done |
|---|---|---|
| 📍 Now (judges' average) | **~51** | submitted SC4AI text |
| 🔴 After batch 1 | **~72** | 📝 N1–N8 + 🖥️ G1, G3, G4, G6, G7, G8 |
| 🟡 After batch 2 | **~78–80** | 🖥️ G2, G5, G9, G10 + 📝 N9 |

> [!IMPORTANT]
> **80 is reachable only if every item lands and the results cooperate.** The +1.5 that closes the gap depends on G3 actually removing the looping (R7 6.5 → 8). Every score below is a projection from the judges' rubrics, not a measured outcome, and each result is reported whichever way it comes out.

## 🧮 Merged rubric scale (current X)

Each merged rubric averages the matching rubrics from the three judges (e.g. "the experiment tests the design" = ChatGPT #6, Claude #3, Gemini #2). SC4AI rubrics are re-read for LoyalAgents.

| # | Merged rubric (LoyalAgents reading) | ChatGPT | Claude | Gemini | **Now** |
|---|---|---|---|---|---|
| R1 | Venue framing and formal content: whose contract, which rule, which property | #1 8, #3 3, #4 5 | #1 6 | #1 8.5 | **6.6** |
| R2 | Loyalty evaluation: conflicts between principals (deployer vs user vs third party) | #2 2 | n/a | n/a | **2.0** |
| R3 | Method novelty (SwiPO beyond conditional DPO) | #5 6 | #2 7 | n/a | **6.5** |
| R4 | The experiment tests the design (opposite contracts in one model) | #6 3 | #3 3 | #2 4 | **3.3** |
| R5 | Measurement validity (Δ, AQI in efficiency, query-blind fidelity) | #7 4 | #4 4, #5 5 | #3 5 | **4.5** |
| R6 | Baselines and fairness (tuning budget, missing baselines) | #8 4 | #8 4 | #4 5.5 | **4.5** |
| R7 | Output quality (46–67% looping) | n/a | #9 3 | #6 4 | **3.5** |
| R8 | Statistics and reproducibility (BCa, seeds, artifacts) | #9 6 | #7 8 | #7 8.5, #10 8 | **7.4** |
| R9 | Safety floor and governance analysis | #10 8 | #6 7 | #5 8 | **7.7** |
| R10 | Writing, tone, presentation | n/a | #10 4 | #9 4.5, #8 6.5 | **4.8** |
| | **Total** | | | | **~51** |

## 🖥️ List 1 · GPU tasks

**ETA basis:** the paper's measured A100-40GB times (SwiPO 120 min, DPO 103 min per run) used as an upper bound for one RTX Pro 6000 96GB; not yet measured on that card. "Wall" assumes 3 GPUs in parallel where runs are independent. Every new GPU script follows CLAUDE.md (tqdm, resume, tee log, wandb, output guard, 95% BCa CI).

**Run order on the one RTX PRO 6000** (owner order Thu Nov 26, 08:30 AM: run every task below without stopping; status at 1:20 PM PST). **🔴 5:50 PM PST, owner back, three picks:** (1) the 3 judges grade the 4-page paper only after the revision (its judge files are still empty: never graded); (2) draft an as-trained copy, done: [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/0_main.tex) (95c8df6; v3 unchanged; red pending marks for the intended-chain SwiPO, held-out columns, Length Control, TruthfulQA; audit 3 FAIL: main text ends on page 5, a pending time in the abstract, and the reference abstract's 56.1/36.1/20.4 and ECLIPTICA sizes left out because they are base + final adapter numbers); (3) the queued G3 and G7 evaluations now run on the as-trained models, plus G7 for SwiPO. Also queued: as-trained Length Control and TruthfulQA after `base_cs`, and Llama Guard on the as-trained held-out answers (`/root/astrained_heldout_harm.sh`). Intended-chain SwiPO Instruct at step ~250 of 1,354 (12 s/step), NoInstruct started 5:39 PM; results ~11 PM to midnight (est.). Open for the owner after that: which SwiPO chain the G5 seeds and G2 use. **🔴 3:55 PM PST, as-trained results at full scale (main draft unchanged):** Conditional Safety, 1,222 prompts ([table](../../../outputs/evaluation/contract_gap/astrained_conditional_safety.json), 94ad737). Refusal gap with 95% BCa: as trained, SwiPO Instruct 0.376 [0.346, 0.407]; DPO 0.034 [0.007, 0.063], PPO 0.033, GRPO 0.034; NoInstruct twins 0.002 to 0.021; SFT 0.022. Loaded as in the paper: SwiPO 0.400, DPO 0.489, PPO 0.303, GRPO 0.325. Confound: SwiPO's chain has no SFT, and every chain with SFT sits near 0.03; SwiPO's real starting point (base + DPO delta) had 0.489, and SwiPO training lowered it by 0.113 [0.070, 0.155]. Llama Guard floor unsafe as trained: DPO 0.049 strict / 0.037 permissive, SwiPO 0.035 / 0.058 (paper loading: DPO 0.089 / 0.193, SwiPO 0.314 / 0.438). Over all 1,222 prompts ([table](../../../outputs/evaluation/floor_harm/conditional_safety/full/harm_gap_all_prompts.json), f20fd77), no as-trained model's Llama Guard unsafe rate moves with the contract (permissive minus strict: SwiPO +0.011 [-0.002, +0.024], DPO -0.002, PPO +0.016, GRPO +0.016, all intervals include 0); SwiPO and DPO as trained are 2 to 3% unsafe under both contracts, PPO and GRPO about 33%. So as-trained SwiPO's 0.376 refusal gap is mostly wording (strict: "I'm sorry"; permissive: instruction-like text), not more compliance; paper loading moved harm (SwiPO +0.085 [+0.053, +0.118]). Asked the owner at 3:50 PM; no answer, so option 1 ran on the 5-minute default at 3:58 PM (queue lines `train_chain_cita_i`/`_ni` ahead of `train_smoke_g1c`, eval waiter `/root/chain_eval.sh`; G1c2, G2 and G5 start about 2 h later): retrain SwiPO on the intended chain (SFT, then DPO, then SwiPO; `cita.py --base_model <SFT>,<DPO>`, 0e0ef83), Instruct and NoInstruct, first in line when G1a/G1b free memory (~6 PM), evaluated by ~3 AM Fri (est.). Also queued: base-model control `Llama31_Base_Prompted` after G1c2. **🔴 1:45 PM PST, adapter stacking (owner decision pending; option 1 ran on the 5-minute default: evaluate both ways, main draft unchanged until the owner approves):** every trainer merges its parent adapter into Llama-3.1-8B and trains a new LoRA (`BASE_MODEL_MAP`: DPO/PPO/GRPO on SFT, SwiPO on the DPO adapter alone, so SwiPO's chain never had SFT), and each Hub adapter holds only its own delta, but `model_loader.py` has loaded base + one delta since May. Every paper number except SFT is therefore a partly assembled model. 100-prompt probe ([summary](../../../outputs/evaluation/stack_probe/summary.json)): DPO base+delta refusal gap +0.41 (stops before the cap 38%, repetitive 14%) vs DPO as trained (SFT+DPO) +0.04 (stops 94%, repetitive 0%; it declines by explaining, which the refusal heuristic does not count); SwiPO base+delta +0.37 vs as trained (DPO+SwiPO) +0.45. Matches the G6 control (SFT, correctly composed, gap about 0). Added `<key>_AsTrained` loader keys (06b5ab7). Running: Conditional Safety for the 8 as-trained models (done ~4 PM, est.); queued: G1a/b both ways (~6:30 PM), held-out floor for the 4 as-trained Instruct models, G1c1/c2 both ways (~midnight), then leakage and Llama Guard for all with `--tag g1` (~3 AM Fri, est.). **1:20 PM PST:** G6 ✅ (prompted-Instruct floor added to the 4-page paper, audit 0 FAIL, 4 pages). G1a at step 616 of 1,354 and G1b running (about 20 s/step with three runs sharing the GPU, finish ~5:30 to 6 PM PST, est.); G1c1 (pooled data, SwiPO settings) started 12:05 PM, finish ~8 PM (est.); G1c2 (pooled DPO) starts after its smoke test once G1a frees memory, finish ~11 PM (est.); G1 evaluation then ~2 h, results ~Fri 1 AM PST (est.). Earlier status (10:15 AM): G8 ✅ is P5b + P5c above. G4 ✅ (done 10:35 AM, [table](../../../outputs/evaluation/contract_gap/g4_prompted_baseline.json)): the prompted Llama-3.1-8B-Instruct moves refusal by 0.232 [0.209, 0.257], less than every trained model (paired +0.070 to +0.257, all above zero), but length (ratio 7.68 [7.17, 8.15] vs 1.07 to 1.14) and confidence (0.399 [0.360, 0.437] vs about 0) far more; it stops at end of turn while the trained models loop. Added to the 4-page paper (audit 0 FAIL, 4 pages). G1 ⏳: owner choices 09:30 AM: both-safe pairs dropped (floor share 31%), baseline (c) in two versions (c1 SwiPO settings, c2 DPO settings), G5 adds a seed-3407 rerun; smoke test passed 09:55 AM (TRL 0.24, SDPA); G1a started 09:56 AM (12.4 s/step), G1b 10:10 AM. Queue after them: G6 held-out controls → G1c1 → G1c2 → G7 → G3 (rep. penalty 1.15) → G2 → G5 (6 runs) → G9 → G10. Checked and ruled out (10:00 AM): the trained models' looping is not a stop-token artifact (SwiPO concise answers stay at 281 words when generation stops at end of turn). G1 results ~Thu night (est.), in time for the 4-page paper (deadline Sat Nov 28, 3:59 AM); the list ends around Sun Nov 29 (est.).

| ID | When | Task (what it shows) | Needs | ETA | Rubric X → Y |
|---|---|---|---|---|---|
| **G1** | 🔴 ⏳ | **Train opposite contracts in one model** (all 3 judges' #1 fix). Strict contract: $Y^+$ = safer response; permissive contract: $Y^+$ = more helpful response, on PKU-SafeRLHF pairs where the two labels disagree. Runs from the existing DPO checkpoint: (a) 2-contract SwiPO, (b) two-tier SwiPO (floor categories: $Y^+$ = safer under both contracts), (c) pooled DPO, no contract (the implicit-Borda baseline of Eq. 1). Report strict-minus-permissive refusal gap, floor-minus-other gap (should fall for b), where (c) lands. ⚠️ permissive adapter is never released; one sentence added to Ethics. | data builder (new, uses `safer_response_id` / `better_response_id`; verify fields) · 3 LoRA runs · eval on Cond. Safety + ECLIPTICA-3k + Table 6 | dev 3 h (CPU) · train ≤ 4 h/run × 3 = ≤ 12 GPU-h · eval 3 GPU-h · **wall ≈ 8 h** | R4 3.3 → 7.5 · R2 3.0 → 5.0 · R1 7.3 → 8.0 · R3 7.0 → 7.5 · R9 7.7 → 8.5 |
| **G3** | 🔴 🕒 | **Re-decode with a repetition penalty** (1.15, same temperature/top-p) for all 8 checkpoints; re-score with the existing deterministic scorers. Shows whether switching survives without looping. | existing checkpoints, vLLM | ~4 GPU-h · wall 1.5 h | R7 3.5 → 6.5 · R5 +0.25 |
| **G4** | 🔴 ✅ | **Prompted Llama-3.1-8B-Instruct baseline** given the same contracts as a system prompt (the baseline every judge expects). | base Instruct model, existing eval scripts | ~1 GPU-h | R6 5.0 → 6.0 |
| **G6** | 🔴 ✅ | **Held-out floor test**: re-run Cond. Safety and Table 6 on PKU-SafeRLHF prompts outside the 12,035-pair pool (the pool is the clear-contrast pairs of both splits, `loader_pku.py`, so held-out prompts must come from other pairs, deduplicated by prompt). Removes the "9 in 10 seen" caveat. **Done Thu 1:15 PM PST:** 2,444 held-out prompts (918 floor); trained models' floor-minus-other gap difference +0.015 to +0.046 (every interval includes 0); NoInstruct and SFT controls gap ≈ 0; the prompted Llama-3.1-8B-Instruct has a floor (−0.115 [−0.161, −0.065] suite, −0.066 [−0.087, −0.045] held-out) by refusing 0.72 (suite) to 0.88 (held-out) of other requests under the permissive contract; Llama Guard unsafe on its permissive floor answers 0.012 [0.003, 0.029]. In the 4-page paper ([floor_leakage_controls.json](../../../outputs/evaluation/floor_leakage/floor_leakage_controls.json), [floor_harm_controls.json](../../../outputs/evaluation/floor_harm/conditional_safety/full/floor_harm_controls.json)). | prompt-dedup script (CPU 1 h) · inference 8 checkpoints × 2 contracts | ~2 GPU-h | R9 +0.25 · R5 +0.25 |
| **G7** | 🔴 🕒 | **Query-sensitivity for all 4 trainers**: extend `src/eval/exp2_query_scrambled.py` (SwiPO only today: 0.560 / 0.565 / 0.571) to DPO, PPO, GRPO; report fidelity(true) − fidelity(scrambled) as a query-aware score. | existing script, n = 1,000 × 3 conditions × 3 trainers | ~2 GPU-h | R5 5.5 → 6.5 |
| **G8** | 🔴 ✅ | **Harmful vs safe non-refusals on the 347 floor prompts** (Gemini): classify permissive non-refusals as safe de-escalation vs actionable harm with a safety classifier (e.g. Llama Guard 3). ⚠️ adds a model-based classifier to one analysis; the paper's "no LLM judge" statement must say so. | existing permissive outputs | ~0.5 GPU-h | R9 8.5 → 9.0 |
| **G2** | 🟡 🕒 | **Measure Proposition 1** (cross-role influence): retrain G1(a) and G1(c) with 30% of permissive-contract labels flipped; measure how far strict-contract behavior moves (Prop. 1 predicts 0 for tabular policies; pooled DPO should move). | G1 data | 2 runs × ≤ 4 h + 1 h eval ≈ 9 GPU-h | R1 8.0 → 8.5 · R3 7.5 → 8.0 |
| **G5** | 🟡 🕒 | **Two extra seeds** for DPO and SwiPO; ±seed std on the efficiency row. | existing configs | 4 runs × ≤ 2 h + 2 h eval ≈ 10 GPU-h | R8 7.4 → 8.5 · R6 6.0 → 6.5 |
| **G9** | 🟡 🕒 | **Second backbone** (e.g. Qwen2.5-7B): SFT → DPO → SwiPO, Instruct and NoInstruct; the "one backbone" limitation every judge lists. | full pipeline on a new base | ≈ 16 GPU-h | R8 8.5 → 9.0 · R6 6.5 → 7.5 |
| **G10** | 🟡 🕒 | **Score the 90 unscored ECLIPTICA-30k types** (27,000 cases) for the 8 checkpoints; tests interference at 100 contracts. | existing scorer | ≈ 12 GPU-h | R5 7.0 → 7.5 |

**GPU totals:** 🔴 batch 1 ≈ 25 GPU-h (wall ≈ 10 h on 3 GPUs; G1 is the critical path) · 🟡 later ≈ 47 GPU-h.

## 📝 List 2 · Non-GPU tasks

| ID | When | Task | Needs | ETA | Rubric X → Y |
|---|---|---|---|---|---|
| **N1** | 🔴 | **Tone rewrite** using the judges' agreed rewrites: Limitations opener (drop "reviewers of an earlier version ... code audit"), Conclusion ("not yet" → the governance takeaway), abstract ending, contribution bullet 4, "(This is the design ...)", "Against DPO the picture changes", Prop. 1 "Two limits apply" → scope sentence. Rules: keep every number and interval; write **"not separable from DPO"**, never "statistically tied" or "leading" (the judges' rewrites that overclaim are listed in each fact-check). | v2 `0_main.tex` | 3 h | R10 4.8 → 7.0 |
| **N2** | 🔴 | **Fix the headline metric**: efficiency without AQI (83.4 vs 67.6, +15.7 [−4.1, 39.7]) becomes the primary number; add the within-model contract gap row (Cond. Safety 0.489 / 0.303 / 0.325 / 0.400); AQI shrinks to one sentence. | `score_table_ci.json` (variants already computed) | 2 h | R5 4.5 → 5.5 · R6 4.5 → 5.0 |
| **N3** | 🔴 ⚠️ | **Make room**: replace the Figure 2 radar with a paired-comparison table; drop the Figure 3 heatmap (repeats Table 4); Table 5 → one sentence ("fidelity overlaps on eight of ten types"). Frees ≈ 1.1 pages for G1's table. **Needs your OK: changes figures.** | existing numbers | 2 h | R10 7.0 → 7.5 |
| **N4** | 🔴 | **Formal-property table for the principal hierarchy**: rows deployer / user / affected third party; columns: who sets the contract, Prop. 1 (no influence across roles) and its tabular-policy scope, menu choice (dictatorial), floor (non-switchable). | §2 text | 2 h | R1 6.6 → 7.3 · R3 6.5 → 7.0 |
| **N5** | 🔴 | **Loyalty-evaluation framing**: recast Table 6 and G1 as LoyalAgents topics 3 (evaluation) and 6 (conflicts of interest): a deployer's permissive contract vs a third party's safety. | v2 §2 lever table, Table 6 | 1.5 h | R2 2.0 → 3.0 |
| **N6** | 🔴 | **Integrate GPU results** (G1, G3, G4, G6, G7, G8) into tables and §5 within 8 pages; every new number with a 95% BCa interval. | GPU outputs | 3 h | enables the GPU gains above |
| **N7** | 🔴 | **Rebuild and audit**: `latexmk`, `/audit-paper-e2e-draft` (0 FAIL, ≤ 8 pages), `paper-consistency` against v4. | build tools | 1 h | R10 7.5 → 8.0 |
| **N8** | 🔴 | **Submit the 8-page v2 to the next venue** (you): disclose the SC4AI and LoyalAgents submissions; paste the new abstract. | OpenReview login | 0.5 h | (submission) |
| **N9** | 🟡 | **Small human check**: 50 prompts × 2 contracts, 2–3 annotators rate contract adherence and harm; validates the deterministic scores. | annotators | 3–4 person-h | R2 5.0 → 6.5 · R5 7.5 → 8.0 |
| **N10** | ⚠️ | **Retitle** (Claude's suggestion). Conflicts with the rule that all versions share one title (v4 is the reference), so not counted in the score. | your decision | 0.5 h | n/a |

**Non-GPU total:** 🔴 ≈ 15 h writing · 🟡 ≈ 4 person-h.

## 🗓️ Suggested order for batch 1 (8-page v2, next venue)

| Slot | GPU lane | Writing lane |
|---|---|---|
| 1 | G1 data builder (CPU) → start G1 (a), (b), (c) in parallel | N1 tone rewrite · N2 headline metric |
| 2 | G3, G4, G7 on the spare GPUs while G1 trains | N4 property table · N5 loyalty framing · N3 (if OK'd) |
| 3 | G1 eval → G6 → G8 | N6 integrate results |
| 4 | | N7 rebuild + audit → N8 submit to the next venue (Bench2Evidence, Wed Dec 2, 3:59 AM PST) |

## 📊 Projected score by rubric

| # | Rubric | Now | 🔴 Batch 1 | 🟡 Batch 2 |
|---|---|---|---|---|
| R1 | Venue framing and formal content | 6.6 | 8.0 | 8.5 |
| R2 | Loyalty evaluation | 2.0 | 5.0 | 6.5 |
| R3 | Method novelty | 6.5 | 7.5 | 8.0 |
| R4 | Experiment tests the design | 3.3 | 7.5 | 7.5 |
| R5 | Measurement validity | 4.5 | 7.0 | 8.0 |
| R6 | Baselines and fairness | 4.5 | 6.0 | 7.5 |
| R7 | Output quality | 3.5 | 6.5 | 6.5–8.0 (if looping is gone) |
| R8 | Statistics and reproducibility | 7.4 | 7.4 | 9.0 |
| R9 | Safety floor and governance | 7.7 | 9.0 | 9.0 |
| R10 | Writing, tone, presentation | 4.8 | 8.0 | 8.0 |
| | **Total** | **~51** | **~72** | **~78–80** |
