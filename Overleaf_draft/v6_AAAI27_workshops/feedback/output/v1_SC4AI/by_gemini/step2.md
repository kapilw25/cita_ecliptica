# 🔷 Gemini · Step 2 · Review of "SwiPO on ECLIPTICA-30k" (SC4AI'27)

> **Judge:** Gemini (same chat as [Step 1](step1.md)) · **Paper judged:** [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf) (9 pages, submitted) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 2

> [!WARNING]
> **Two of Gemini's presentation findings are false.** It says σ, β, λ, Δ render as blanks in Eqs. 1–3 and that the titles of Figures 2–3 are clipped. The rendered PDF shows all symbols and both full titles; these are artifacts of Gemini's text extraction. Skip those fixes. Details in [🔎 Fact-check](#-fact-check-by-claude-code-not-the-judge).

> [!NOTE]
> The judge's text below is kept in full; only the layout changed.

**Legend:** 🟢 strong · 🟡 moderate · 🔴 weak · 🅰️🅱️🅲🅳 the four parts of the prompt · 📍 page reference · § = section number in the paper

## 📌 TL;DR

| | Gemini's verdict |
|---|---|
| 🎯 **Acceptance, SC4AI'27** | **55%** |
| 🛡️ **Acceptance, typical AAAI-27 safety/alignment workshop** | **35%** (lower than SC4AI, unlike the other two judges) |
| 🧮 **Rubric total** | **62.5 / 100** |
| 📍 **vs accepted papers** | ~6–10 points below the bar (Gemini scores the accepted empirical papers 68–76) |
| 💪 **What carries it** | SC4AI-tailored social-choice framing, the floor-leakage audit, paired bootstrap statistics and released artifacts. |
| 🚩 **What sinks it** | "Self-inflicted execution gaps": the unrun contrasting-contract training, 46–67% looping, prompt-insensitive fidelity, defeatist framing. |

## 🅰️ Part A · Acceptance probability

| Venue | Estimate | Reason |
|---|---|---|
| 🎯 SC4AI'27 | **55%** | Directly answers SC4AI's prompt (whose preferences, which rule, which properties) by mapping steerable alignment to Borda-count avoidance (Proposition 1), Gibbard–Satterthwaite dictatorship over the contract menu, and a two-tier floor/menu governance design (§2, 📍 pp. 2–3), with an open benchmark and an empirical floor-leakage audit (§5, Table 6, 📍 p. 6). Borderline risk from severe self-sabotage: the paper states it has not run the training experiment SwiPO was built for (§4, 📍 p. 4; §8, 📍 p. 7), relies on an uncalibrated composite (AQI) for its headline win over DPO (§5, 📍 p. 5; §8, 📍 p. 7), and reads like a debugging log rather than a research contribution. |
| 🛡️ Typical AAAI-27 safety/alignment workshop | **35%** | Against the 6 accepted papers (where even single-setting audits like the Trust Paradox or Role Assignment present a clean, completed primary experiment), a general safety reviewer will penalize an incomplete training run ("the experiment SwiPO was designed for... has not been run", §10, 📍 p. 8), 46–67% looping across all models (§5, 📍 p. 5), and a tie with plain DPO once AQI is removed (Table 3, 📍 p. 5). |

### 🚩 Top 3 reasons a reviewer will reject

| # | Reason | Evidence |
|---|---|---|
| 1️⃣ | **Unrun core experiment and a tie with plain DPO** | SwiPO is formulated to train opposite contracts on the same prompt (Eq. 3, §4, 📍 p. 4), yet the reported run trains one refusal contract and cannot be separated from DPO once AQI (which does not rank models) is dropped (+15.7 [−4.1, 39.7], §5, 📍 p. 5; §8, 📍 p. 7). |
| 2️⃣ | **Degenerate generation and metric flaws** | 46–67% of Instruct ECLIPTICA outputs contain over 30% duplicated sentences/5-grams at 512 tokens (§5, 📍 p. 5); ECLIPTICA's fidelity is insensitive to the user prompt (0.560 true vs 0.565 scrambled vs 0.571 instruction-only, §8, 📍 p. 7); TruthfulQA carries zero switching signal (§5, 📍 p. 5). |
| 3️⃣ | **Tuning confound and data leakage** | Only SwiPO got 13 Optuna trials while DPO, PPO, GRPO used fixed defaults (§4, 📍 p. 4; §8, 📍 p. 7); about 90% of the 1,222 Conditional Safety test prompts were seen during SFT/DPO/SwiPO training (§8, 📍 p. 7). |

### 💪 Top 3 strongest points

| # | Strength | Evidence |
|---|---|---|
| 1️⃣ | **Sharp, workshop-tailored social-choice framing** | Proposition 1 (zero cross-role manipulation under $\mathcal{L}_{\text{cond}}$), Gibbard–Satterthwaite dictatorship over the menu, and a testable two-tier (collective floor vs deployer menu) design fit SC4AI'27 better than almost any standard RLHF paper (§2, 📍 pp. 2–3). |
| 2️⃣ | **Empirical floor-leakage audit** | Pre-registered 347 third-party harm prompts (violence, trafficking, public health, national security); permissive contracts drop refusals just as steeply there (+0.017 to +0.100 gap difference): a concrete governance finding independent of which trainer wins (§5, Table 6, 📍 p. 6). |
| 3️⃣ | **Rigorous paired bootstrap statistics and artifact release** | Unlike 4 of the 6 calibration papers, every prompt-level metric has paired 95% BCa intervals (10,000 resamples), plus public code and ECLIPTICA-30k/3k datasets (Tables 4–6, 📍 pp. 5–6; Abstract, 📍 p. 1). |

## 🅱️ Part B · Ten rubrics

| # | Rubric | Why it matters here | Score | Evidence (📍) | The one change that adds the most points |
|---|---|---|---|---|---|
| 1 | Social-choice and governance framing | Core SC4AI mandate: whose preferences, by what rule, which formal properties | 🟢 **8.5** | §2 (pp. 2–3): hidden roles → Borda count, Proposition 1 (no cross-role influence), Gibbard–Satterthwaite on menu selection, two-tier floor/menu model | State the formal axioms satisfied or violated by the two-tier rule (anonymity / strategy-proofness across roles vs dictatorship over the menu) in a compact summary table |
| 2 | Alignment between method and experiment | Reviewers expect the tested algorithm to run the objective in the equations | 🔴 **4.0** | §4 (p. 4) and §8 (p. 7) admit the run trains one contract, not the contrasting $(I_a, X), (I_b, X)$ pairs Eq. 3 was designed for | Train SwiPO (and DPO) on contrasting multi-role pairs (e.g. strict vs permissive, concise vs detailed) on Llama-3.1-8B; add the row to Table 4 |
| 3 | Benchmark and metric validity | ECLIPTICA-30k is a headline contribution; its score must measure query-conditioned switching | 🟡 **5.0** | §3 (p. 4) defines fidelity × shift on responses alone; §8 (p. 7): scrambled prompts give the same fidelity (0.565 vs 0.560); TruthfulQA has zero signal (§5, p. 5) | Replace or augment MiniLM response-only fidelity with a prompt-aware metric (NLI/judge or query-relevance-weighted) and drop or replace TruthfulQA |
| 4 | Empirical rigor and fair baselines | "SwiPO beats DPO/PPO/GRPO" fails if tuning or metrics are asymmetric | 🟡 **5.5** | §4 (p. 4), §8 (p. 7): 13 Optuna trials for SwiPO vs fixed baselines; AQI non-comparable yet in Efficiency % (§5, p. 5) | Remove AQI from the cross-model composite (make the 4-suite or 3-signal-suite paired bootstrap primary) and match DPO's tuning budget |
| 5 | Safety floor and harm analysis | Central ethics/safety finding: does pluralistic switching erode hard boundaries | 🟢 **8.0** | §5, Table 6 (p. 6): 347 pre-specified third-party harm prompts; permissive contracts lower refusals at least as much as on general prompts | Separate "safe de-escalation" from "harmful compliance" on a stratified sample of the 347 floor prompts |
| 6 | Generation quality and sanity checks | Heavy looping invalidates lexical/embedding metrics and deployment claims | 🔴 **4.0** | §5 (p. 5), §8 (p. 7): 46–67% of Instruct ECLIPTICA outputs over 30% duplicated at 512 tokens | Re-run inference on existing checkpoints with `repetition_penalty=1.15` and report clean scores |
| 7 | Statistical reporting and uncertainty | Paired intervals separate real switching from decoding noise | 🟢 **8.5** | §5, Tables 4–6 (pp. 5–6): 10,000-resample paired 95% BCa intervals on every item-level suite, plus NoInstruct noise baselines | Add multi-seed inference (3 seeds) on ECLIPTICA-3k and Conditional Safety |
| 8 | Presentation, figures, readability | Workshop papers are judged quickly | 🟡 **6.5** | Figure 1 (p. 2) and Tables 1–6 clear; Figures 2 (p. 7) and 3 (p. 8) "oversized, text-clipped at the top", with non-comparable AQI axes | Fix "clipped titles", shrink both figures to single column, fix "formatting glitches (\lambda and \sigma missing in Eqs. 1–3)" ⚠️ *see fact-check: the clipping and glyph claims are false* |
| 9 | Positioning and scholarly tone | Accepted papers frame limitations constructively, not as a bug report | 🔴 **4.5** | Abstract (p. 1), Intro (p. 1), §8 (p. 7), Conclusion (p. 8) lead with what was not done and conclude "not yet" | Reframe around the positive discoveries (zero-shot cross-contract transfer, the empirical absence of an emergent floor); move caveats to one concise Limitations paragraph |
| 10 | Open science and reproducibility | Released data and code raise workshop value and trust | 🟢 **8.0** | Abstract (p. 1): GitHub and Hugging Face links for ECLIPTICA-30k and 3k; exact hyperparameters in §4 (p. 4) | Release evaluation logs and scoring scripts with a clean held-out Conditional Safety split |
| | **Total** | | **62.5 / 100** | | |

### 📊 Comparison to the 6 accepted papers

In Gemini's calibration, pure empirical/conceptual workshop papers (Trust Paradox, Role Assignment, When Refusals Fail) scored **68–76** because they executed their stated experiment cleanly and framed modest or negative findings as discoveries. SwiPO has stronger theory (§2) and better intervals (Tables 4–6) than 4 of the 6, but sits **~6–10 points below the bar** because of self-inflicted execution gaps: unrun contrasting-contract training, 46–67% looping, prompt-insensitive fidelity, and defeatist framing.

## 🅲 Part C · 24-hour improvements (ranked by expected gain)

### C0. Summary

| Rank | Improvement | Rubric gain | Compute (judge's estimate) |
|---|---|---|---|
| 1️⃣ | Train and evaluate SwiPO vs DPO on contrasting contracts | #2: 4.0 → 8.5 (+4.5) · #4: 5.5 → 7.0 (+1.5) | ~4–5 h on 1× A100-40GB |
| 2️⃣ | Repetition-penalty re-run plus a query-aware ECLIPTICA metric | #6: 4.0 → 8.0 (+4.0) · #3: 5.0 → 7.5 (+2.5) | ~2–3 GPU-h |
| 3️⃣ | Purge AQI and TruthfulQA from the primary efficiency metric | #4: 5.5 → 8.0 (+2.5) | 0 GPU-h + one ~2 h DPO run |
| 4️⃣ | Held-out floor audit plus harmful-compliance annotation | #5: 8.0 → 9.5 (+1.5) | ~0.5 GPU-h |
| 5️⃣ | Full tone rewrite plus "broken LaTeX/figure" fixes | #9: 4.5 → 8.5 (+4.0) · #8: 6.5 → 8.5 (+2.0) | 0 GPU-h |

### C1. 1️⃣ Train and evaluate SwiPO vs DPO on contrasting contracts (closes the #1 rejection vector)

- **What it shows:** that Eq. 3 actually separates opposing contracts trained on the same prompt, and whether the mandatory KL anchor ($\lambda > 0$) prevents mode collapse or cross-contract interference better than conditional DPO ($\lambda = 0$).
- **What it needs:** contrasting pairs from PKU-SafeRLHF (or UltraFeedback/HelpSteer): a strict contract ($Y^+$ = safe refusal) paired with a helpful/permissive contract ($Y^+$ = helpful response on benign/borderline prompts). Train 2 models on Llama-3.1-8B (conditional DPO vs SwiPO) plus a $\lambda = 0$ ablation. ~4–5 h on 1× A100-40GB (2 h per LoRA run + 30 min inference).
- **Where it goes:** a "Multi-Contract Trained" block (conditional DPO vs SwiPO vs $\lambda = 0$) in Table 4 (p. 5) and §5, replacing the repeated disclaimers that contrasting training was not run.
- **Rubric impact:** method–experiment alignment 4.0 → 8.5 (+4.5); empirical rigor 5.5 → 7.0 (+1.5).

### C2. 2️⃣ Re-run inference with a repetition penalty and add a query-aware ECLIPTICA metric

- **What it shows:** removes the 46–67% looping artifact across all 8 checkpoints and shows ECLIPTICA measures query-grounded instruction following rather than query-blind style.
- **What it needs:** inference-only re-run on ECLIPTICA-3k, Length Control, Conditional Safety with `repetition_penalty=1.15` and `no_repeat_ngram_size=4`; score ECLIPTICA with a query-conditioned metric (e.g. cosine similarity between [prompt + prototype] and response, or an open 8B NLI/judge check on 500 pairs). ~2–3 GPU-h.
- **Where it goes:** update Tables 4 and 5 (pp. 5–6); define the query-aware fidelity in §3 Scoring (p. 4).
- **Rubric impact:** generation quality 4.0 → 8.0 (+4.0); benchmark validity 5.0 → 7.5 (+2.5).

### C3. 3️⃣ Purge non-comparable AQI and zero-signal TruthfulQA from the primary efficiency metric

- **What it shows:** a valid comparison over the three active switching suites (ECLIPTICA, Conditional Safety, Length Control), plus a matched-hyperparameter DPO baseline.
- **What it needs:** recomputation from existing logs (0 GPU-h) plus one quick DPO run with matched learning rate/β (~2 GPU-h).
- **Where it goes:** Table 3 (p. 5) and Figure 2 (p. 7) report 3-suite Efficiency % with per-suite Δs; LITMUS/AQI moves to a standalone representation-geometry paragraph in §5.
- **Rubric impact:** empirical rigor 5.5 → 8.0 (+2.5).

### C4. 4️⃣ Held-out floor-leakage audit plus harmful-compliance annotation

- **What it shows:** fixes the 90% train/test overlap critique by evaluating only on the held-out 10% PKU-SafeRLHF split ("n ≈ 1,200 if re-evaluated on the official test set without mixing into the 90% train split, or filtering Table 6 to the 10% unseen split"), and classifies permissive non-refusals into safe de-escalation (like SwiPO in Fig. 1) vs actionable harm.
- **What it needs:** existing logs filtered to unseen prompts plus a lightweight classifier/heuristic pass on the 347 floor prompts (~0.5 GPU-h).
- **Where it goes:** Table 6 (p. 6) and §5 "Is there a floor?" (p. 6).
- **Rubric impact:** safety floor 8.0 → 9.5 (+1.5).

### C5. 5️⃣ Full positioning and tone rewrite plus "broken LaTeX/figure formatting" fixes

- **What it shows:** turns an apologetic engineering status report into a confident, research-led SC4AI contribution, while "fixing missing math symbols (σ, λ, β in Eqs. 1–3, pp. 2, 4) and clipped figure titles (Figs. 2–3, pp. 7–8)".
- **What it needs:** 0 GPU-h (editing and matplotlib regeneration).
- **Where it goes:** Abstract, Introduction, §8 Limitations, §10 Conclusion, Eqs. 1–3, Figs. 2–3.
- **Rubric impact:** tone 4.5 → 8.5 (+4.0); presentation 6.5 → 8.5 (+2.0).

> [!CAUTION]
> The symbol and clipping parts of C5 are based on false readings (see fact-check). Only the tone rewrite applies.

### ✂️ What to cut to stay within 8 pages

| Element | Cut | Saves |
|---|---|---|
| TruthfulQA in Tables 3–4 and Figures 2–3 | §5 admits it has zero switching signal; keep one sentence in §5 as a negative control | ~12 lines + one radar/heatmap column |
| Figures 2 (p. 7) and 3 (p. 8) | Shrink to single-column width side by side | ~0.6 page |
| §8 Limitations (p. 7) | Compress "9 bulleted confessions (~42 lines)" to one tight paragraph (~10 lines), as in the Trust Paradox and Role Assignment papers; drop self-criticisms resolved by improvements 1–4 | ~0.4 page |
| "Broken LaTeX glyphs" (\sigma, \beta, \lambda, \Delta as blanks/boxes in Eqs. 1–3, Tables 3–4, Fig. 2 caption) | Fix | ⚠️ *false: glyphs render correctly* |

## 🅳 Part D · Tone audit

**Problem tags:** 🔻 negative / defeatist · 🛡️ defensive · ⚙️ engineering-only · 🔁 repetitive · 💥 invites rejection

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 1 | p. 1, Abstract | "the run reported here trains a single safety contract and tests contracts it never saw." | 🛡️ leads with a limitation instead of framing zero-shot cross-contract transfer as a setup | "We evaluate SwiPO in a strict zero-shot transfer regime, training on a single safety contract and testing generalization across ten unseen behavioral contracts." |
| 2 | p. 1, Abstract | "it leads PPO and GRPO, but without the within-model AQI suite it cannot be separated from DPO, which switches more under safety contracts." | 🔻 ends the abstract on a defeatist tie | "Across paired bootstrap evaluations, SwiPO achieves 86.7% relative efficiency (95% CI: 76.8 to 96.2) versus 56.1% (DPO), 36.1% (GRPO), and 20.4% (PPO), leading on multi-suite balance (83.4% vs. 67.6% without within-model AQI, CI: -4.1 to 39.7) while plain DPO produces larger refusal shifts on safety contracts." ⚠️ *see fact-check: "leading" on a non-significant difference* |
| 3 | p. 1, §1 Contributions | "every experiment uses ECLIPTICA-3k, its 10-type, 3,000-case subset." | ⚙️ apologetic about dataset scale | "ECLIPTICA-30k, a full-factorial benchmark holding the prompt fixed while varying only the alignment instruction (300 prompts across 100 instruction types), paired with a 3,000-case evaluation suite (ECLIPTICA-3k) spanning 10 core behavioral axes." |
| 4 | p. 1, §1 Contributions | "the run reported here trains one safety contract and measures transfer to unseen ones." | 🔁 frames the experiment as incomplete | "SwiPO, an instruction-conditioned preference optimization objective with a mandatory KL anchor (λ > 0), evaluated here on zero-shot transfer from a single safety contract to unseen behavioral contracts." |
| 5 | p. 1, §1 Contributions | "A five-suite evaluation with paired 95% intervals, in which SwiPO beats PPO and GRPO but cannot be separated from DPO once a within-model metric is set aside, reported with every failure mode and data caveat we found." | 🔻 reads like a QA bug report | "A five-suite paired bootstrap evaluation quantifying cross-contract transfer, floor leakage across 347 severe-harm prompts, and the behavioral trade-offs between SwiPO, DPO, PPO, and GRPO." |
| 6 | p. 2, §2 | "(This is the design; the experiment in Section 5 does not yet train opposite contracts.)" | 🛡️ self-critical parenthetical | "In Section 5, we isolate the cross-contract generalization regime of this objective by training on a single safety contract and evaluating transfer to opposing unseen contracts." |
| 7 | p. 3, §2 (Prop. 1) | "With shared weights, as with LoRA on one backbone, training one contract does move the others, which is the interference question in the Limitations; and the reported run trains a single contract, so the proposition describes the design, not our experiment." | 🔻 undermines the theorem right after proving it | "Proposition 1 characterizes the unregularized capacity limit; under shared LoRA weights, cross-contract parameter coupling introduces finite-capacity interference, motivating the mandatory KL anchor in Section 4." |
| 8 | p. 4, §3 | "the 90 added types are also hand-designed and not yet scored by any model." | ⚙️ status update inside the benchmark definition | "The remaining 90 instruction types extend coverage across 10 orthogonal behavioral axes and are released as an open testbed for large-scale multi-role evaluation." |
| 9 | p. 4, §4 | "The run reported here does not yet use opposite contracts. ... training on contrasting pairs is the experiment the objective was built for, and we have not run it." | 💥 tells reviewers the main experiment is missing | "To establish a strict zero-shot transfer baseline before multi-contract supervision, we train SwiPO on a single safety contract derived from PKU-SafeRLHF and evaluate how far instruction conditioning transfers to unseen behavioral contracts; multi-contract training on opposing pairs is a direct next step." |
| 10 | p. 4, §4 Cost | "SwiPO's hyper-parameters were chosen by 13 completed Optuna trials per variant, while DPO, PPO, and GRPO use fixed settings, which favors SwiPO in the comparison below." | ⚙️ self-undermining disclosure mid-methods | "SwiPO uses hyperparameters selected via 13 Optuna trials (β = 0.107, lr = 5.4 × 10⁻⁶), whereas DPO, PPO, and GRPO use standard fixed configurations (noted in Section 8)." |
| 11 | p. 5, §5 Findings | "No Instruct model exceeds 0.39 of ECLIPTICA's maximum, and none reaches the Length Control target (best ratio 1.14). Every trainer also loops: 46 to 67% of Instruct-model ECLIPTICA answers contain over 30% duplicated sentences or 5-grams at 512 tokens, and all scores include them." | 🔻 raw failure dump | "Across all trainers, zero-shot transfer to unseen contracts exhibits substantial headroom: Instruct models reach at most 0.389 on ECLIPTICA and a 1.141 word ratio on Length Control, while 46% to 67% of 512-token ECLIPTICA completions show over 30% 5-gram or sentence repetition under standard sampling." |
| 12 | p. 6, §5 One case | "This is one prompt chosen to illustrate failure modes, not a measured rate." | 🛡️ apologetic about a qualitative case | "Figure 1 provides a qualitative trace of these contract-switching mechanics on a single borderline request; aggregate rates across 1,222 prompts follow in Table 6." |
| 13 | p. 6, §5 What the results say | "The efficiency score, being relative to these four trainers, says nothing about how close any of them is to a reliable switch; the absolute numbers say they are not." | 🔻 dismisses its own benchmark in the closing results sentence | "While relative efficiency ranks the trainers against one another, the absolute scores demonstrate that zero-shot transfer from a single safety contract leaves substantial room before single-checkpoint switching is reliable across arbitrary roles." |
| 14 | p. 7, §8 Limitations | "The reviewers of an earlier version asked for several experiments that need compute or annotation we do not have for this submission, and a code audit for this version found further caveats. We list them rather than claim them." | 💥 mentions prior reviewers and an internal code audit | "We summarize the primary scope boundaries of our experimental evaluation and benchmark metrics to guide future work." |
| 15 | p. 8, §10 Conclusion | "Every trainer still loops, and the experiment SwiPO was designed for, training opposite contracts on the same prompts, has not been run. The answer to the title question is therefore not yet." | 🔻 ends by declaring the work unfinished | "While zero-shot transfer from a single safety contract yields substantial refusal switching (0.30 to 0.49), current checkpoints exhibit high repetition and lack an emergent safety floor, indicating that reliable single-checkpoint switching requires explicit multi-contract training and a dedicated non-switchable safety tier." |

### 🥇 Top 3 rewrites that matter most

| Priority | Row | Why |
|---|---|---|
| 1️⃣ | **#9** (§4, p. 4, "...we have not run it") | Telling reviewers the main experiment was never run is the fastest path to a reject; reframing it as a deliberate zero-shot transfer evaluation turns an omission into a clean baseline. |
| 2️⃣ | **#14** (§8, p. 7, earlier reviewers and code audit) | Signals an unpolished resubmission; a crisp scope statement restores credibility. |
| 3️⃣ | **#15** (§10, p. 8, "not yet") | Ending on "not yet" reads like an incomplete lab note; closing with the architectural takeaway (zero-shot switching shows the need for multi-contract training plus a two-tier floor) serves SC4AI's audience. |

### ✍️ Rewritten abstract (contribution first; Gemini: "232 words vs. 274 original")

> Steerable pluralistic alignment conditions a language model on a natural-language behavioral contract so one checkpoint can serve distinct agent roles without pooling conflicting annotator preferences into an implicit Borda count. We show that switching does not dissolve the social-choice problem, but moves it to the governance of the instruction channel: who sets the contract (oversight), which contracts are offered (agenda setting), which constraints no contract may lift (a collective floor over affected third parties), and how strategic misreporting shifts from annotators to deployers (proved in Proposition 1). To study these mechanics empirically, we introduce ECLIPTICA-30k (300 prompts crossed with 100 alignment-instruction types, evaluated on its 10-type, 3,000-case ECLIPTICA-3k subset) and SwiPO (Switchable Preference Optimization), which conditions DPO on the instruction under a mandatory KL anchor. Evaluating zero-shot transfer on Llama-3.1-8B trained on a single safety contract, every preference-trained model shifts its refusal rate by 0.30 to 0.49 between strict and permissive contracts. However, no emergent safety floor appears: on 347 prompts involving violence, physical harm, trafficking, and threats to public health or national security, permissive contracts reduce refusals at least as much as elsewhere. Across five suites, SwiPO achieves 86.7% relative instruction-alignment efficiency (95% CI: 76.8 to 96.2) versus 56.1% (DPO), 36.1% (GRPO), and 20.4% (PPO), leading PPO and GRPO while remaining statistically tied with DPO once within-model AQI is excluded (83.4% vs. 67.6%, CI: -4.1 to 39.7).

## 🔎 Fact-check (by Claude Code, not the judge)

Checked 2026-11-26 against the submitted [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf): its text layer and rendered images of pp. 2, 7 and 8.

### ✅ Confirmed

| # | Judge claim | Where it is |
|---|---|---|
| 1 | Section numbers §2–§10, e.g. "8 Limitations", "10 Conclusion" | Paper headings (sections are numbered) |
| 2 | Unrun contrasting training (§4 p. 4, §8 p. 7, §10 p. 8); 13 Optuna trials; β = 0.107, lr = 5.4 × 10⁻⁶ | pp. 4, 7, 8 |
| 3 | +15.7 [−4.1, 39.7] without AQI; 86.7 [76.8, 96.2] vs 56.1 / 36.1 / 20.4 | Table 4 and text, p. 5 |
| 4 | 46–67% looping; fidelity 0.560 / 0.565 / 0.571; about 90% of 1,222 prompts seen in training | pp. 5, 7 |
| 5 | 347 floor prompts; gap differences +0.017 to +0.100 | Table 6, p. 6 |
| 6 | 0.389 (best ECLIPTICA) and 1.141 (best Length Control ratio) in rewrite #11 | Table 4 / Figure 3 (SwiPO_I Length Ctrl 1.141) |
| 7 | Rubric arithmetic 8.5+4+5+5.5+8+4+8.5+6.5+4.5+8 = 62.5 | arithmetic |

### ❌ Wrong

| # | Claim | What the PDF shows |
|---|---|---|
| 1 | **"\lambda and \sigma missing in Eqs. 1–3", "broken LaTeX glyphs rendering as blanks/boxes"** (rubric 8, C5, cut list) | Rendered p. 2 shows Eq. 1 with σ, β, Δ intact (and the text layer contains "σ β ∆θ"). The judge's own text extraction lost the symbols. **No fix needed.** |
| 2 | **"Figure 2 (p. 7) and Figure 3 (p. 8) ... text-clipped at the top"** | Rendered pp. 7–8 show both full titles ("Instruction Alignment Efficiency (Llama-3.1-8B)", "Model Performance (Llama-3.1-8B)"). **No fix needed.** (The "oversized" point is a fair layout opinion.) |
| 3 | **Rewrite #2: "leading on multi-suite balance (83.4% vs. 67.6% ... CI: -4.1 to 39.7)"** | The interval spans zero, so this turns a non-significant difference into a win, which the prompt forbids. Use "not separable from DPO". |
| 4 | **Abstract: "how strategic misreporting shifts from annotators to deployers (proved in Proposition 1)"** | Proposition 1 is "no influence across roles"; the misreporting point is an argument in §2 citing Siththaranjan et al., not a proof. Drop "(proved in Proposition 1)". |
| 5 | **Tie with DPO cited as "Table 3, p. 5"** | Table 3 describes the suites; the numbers are in Table 4 and the Findings text. |

### ⚠️ Issues to weigh

| # | Issue | Impact |
|---|---|---|
| 1 | **"Statistically tied with DPO"** in the abstract (same as the Claude judge): a non-significant difference is not evidence of equality. Prefer "not separable from DPO". | Medium |
| 2 | **Rewrite #7 adds a claim**: that cross-contract interference "motivat[es] the mandatory KL anchor". The paper does not tie the anchor to interference. | Medium: keep the fact, drop the new causal link |
| 3 | **C4 held-out count**: the 1,222 Conditional Safety prompts are themselves the test pairs, about 90% seen, so the unseen share is roughly 120 prompts, not "n ≈ 1,200". A larger held-out set needs new PKU-SafeRLHF prompts outside the training pool. | Plan the data before C4 |
| 4 | **C1 includes a λ = 0 ablation**; the paper's trainer requires λ > 0 (§8), so this needs a code change. The 4–5 h estimate also looks low if the contrasting data doubles the pairs (the paper's one-contract run took 120 min). | Feasibility |
| 5 | **C3 "match DPO's tuning budget" with one ~2 h run**: SwiPO had 13 Optuna trials, so one run does not match it. | Feasibility |
| 6 | **Word counts**: Gemini says its abstract is 232 words vs 274; measured 228 vs about 285. The §8 list has 10 bullets, not 9. | Low |
| 7 | **Its 35% (safety workshop) is below its 55% (SC4AI)**, the opposite of ChatGPT and Claude, and it scores the accepted papers 68–76 while Claude scores them 28–62. Both are subjective calibrations. | Informational |
