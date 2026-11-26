# 🟠 Claude · Step 2 · Review of "SwiPO on ECLIPTICA-30k" (SC4AI'27)

> **Judge:** Claude (same chat as [Step 1](step1.md)) · **Paper judged:** [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf) (9 pages, submitted) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 2

> [!NOTE]
> The judge's text below is kept in full; only the layout changed. Claude Code's verification notes are in the last section, [🔎 Fact-check](#-fact-check-by-claude-code-not-the-judge).

**Legend:** 🟢 strong · 🟡 moderate · 🔴 weak · 🅰️🅱️🅲🅳 the four parts of the prompt · 📍 page reference · § = the judge's own section numbering (the paper's sections are unnumbered)

## 📌 TL;DR

| | Claude's verdict |
|---|---|
| 🎯 **Acceptance, SC4AI'27** | **55%** |
| 🛡️ **Acceptance, typical AAAI-27 safety/alignment workshop** | **65%** |
| 🧮 **Rubric total** | **51 / 100** now → **about 76 / 100** with the five Part C changes |
| 💪 **What carries it** | The social-choice framing and the statistics (best of the seven papers on both). |
| 🚩 **What puts it at risk** | The experiment, the headline metric, and the self-critical tone. |
| 📍 **Rank vs accepted papers** | Mid-pack (51), between Biased Agents (~42) and When Refusals Fail (~57). |

**Section map used by the judge:** §1 Introduction (p1), §2 Switching Versus Aggregating (p1–3), §3 ECLIPTICA (p3–4), §4 SwiPO (p4), §5 Experiments (p4–6), §6 Open Problems (p6), §7 Related Work (p7), §8 Limitations (p7–8), §9 Ethics (p8), §10 Conclusion (p8). The main text fills exactly 8 pages, so anything added must replace something.

## 🅰️ Part A · Acceptance probability

| Venue | Estimate |
|---|---|
| 🎯 SC4AI'27 | **55%** |
| 🛡️ Typical AAAI-27 safety/alignment workshop | **65%** |

### Reason: the SC4AI reviewer's three questions have clear answers

| Question | Answer in the paper |
|---|---|
| 👥 Whose preferences | Annotators grouped by role, weighted by $p(r)$ (§2, 📍 p1–2) |
| 🗳️ Which rule | Pooled DPO is an implicit Borda count over hidden roles (📍 p2, citing Siththaranjan et al.). Switching means no aggregation inside the model, but a choice over the contract menu that is "dictatorial" (📍 p3). |
| 📐 Which property | Proposition 1, "no influence across roles" (📍 p3), plus a Gibbard–Satterthwaite argument for user-selected contracts (📍 p3) |

The three-role Borda example is correct (refusal 0.80, guidance 1.25, detail 0.95, 📍 p2). §6 is written for exactly this audience. On statistics the paper is far above every accepted paper in the calibration set: paired BCa intervals on every number (📍 p4–6).

### What holds it back

1. Proposition 1 is close to trivial under its tabular assumption; the paper itself says it "describes the design, not our experiment" (📍 p3).
2. The method's defining experiment (training opposite contracts) "we have not run" (📍 p4).
3. The paper argues against itself: the abstract ends on "cannot be separated from DPO" (📍 p1); §8 opens by citing the reviewers of an earlier version (📍 p7); the conclusion answers its own title with "not yet" (📍 p8).

A social-choice reviewer may like §2 and §6 and still reject because the empirical half undercuts the method named in the title. A general safety workshop accepts weaker evidence than this (the Trust Paradox got in on 0.748 vs 0.743), hence the higher second number.

### 🚩 3 most likely reasons for rejection

| # | Reason | Evidence |
|---|---|---|
| 1️⃣ | **The experiment doesn't test the proposed design.** | SwiPO is "designed so that contracts with opposite targets on the same prompt can coexist in one checkpoint" (📍 p1), yet "the reported run trains a single refusal-oriented safety contract" (§8, 📍 p7). In the reported run SwiPO is DPO continued from the DPO checkpoint with one system message plus a KL term (§4, 📍 p4). |
| 2️⃣ | **The headline numbers don't measure what they claim.** | • 86.7% efficiency includes AQI, which "does not rank models against each other" (📍 p4, p7); without AQI the lead over DPO is +15.7 [−4.1, 39.7] (📍 p5); without TruthfulQA as well, DPO leads on the point estimate (86.8 vs 77.8, 📍 p5). • Δ compares two separately trained models (📍 p4); SwiPO's ECLIPTICA Instruct score is the lowest of the four (0.367, 📍 p5). • Fidelity ignores the query: 0.560 true prompt, 0.565 scrambled (📍 p7–8). • About 9 in 10 Conditional Safety prompts were seen in training (📍 p7). • 46–67% of answers loop (📍 p5). |
| 3️⃣ | **Thin formal social choice plus a self-undermining tone.** | Within a role the rule is still pooled Borda (📍 p3). No rule is proposed or analysed for the floor or the menu; they are open problems (§6, 📍 p6). Gibbard–Satterthwaite is cited, not applied (📍 p3). The text repeatedly frames results as failures (Part D). |

### 💪 3 strongest points

| # | Strength | Evidence |
|---|---|---|
| 1️⃣ | **The core idea:** aggregation moves from training into the instruction channel. | Mapped onto four social-choice concepts (oversight, agenda setting, a collective floor, misreporting shifting to deployers; §2, 📍 p2–3), summarised in Table 1 (📍 p3). The §6 problems (proportional committee selection for menus, priority among principals, choosing the floor, fairness across contracts; 📍 p6) fit SC4AI well. |
| 2️⃣ | **The floor test is useful for safety policy.** | Categories fixed before any rate was computed. Permissive-contract refusal on violence, trafficking and similar requests is only 0.11–0.30, and the drop is at least as large as elsewhere (Table 6, 📍 p6). |
| 3️⃣ | **Statistical and artifact quality above all six calibration papers.** | Paired 95% BCa intervals with 10,000 resamples (📍 p4). Captions say bold marks a point estimate, not a significant difference (Tables 4–6). Code and both datasets released (📍 p1). Tuning imbalance disclosed (📍 p4). |

## 🅱️ Part B · Ten rubrics

| # | Rubric | Why it matters here | Score | Evidence from the paper | The one change that adds the most points |
|---|---|---|---|---|---|
| 1 | Social-choice substance: whose preferences, which rule, which property | The SC4AI reviewer's core question | 🟡 **6** | Eqs. 1–2 and the Borda reading (p2); three-role example (p2); Prop. 1 (p3); G–S (p3). Prop. 1 holds only for "a tabular or unlimited-capacity policy" and "describes the design, not our experiment" (p3). Within-role rule unchanged (p3). | Measure cross-role influence empirically: perturb one role's labels and measure how much the other contract moves (C5) |
| 2 | Novelty over Conitzer et al. / Siththaranjan et al. / Sorensen et al. | SC4AI reviewers know these papers | 🟢 **7** | "Switching does not dissolve the social-choice problem. It moves it to the instruction channel" (p1). Two-tier floor/menu/channel design (p3). Positioned against MaxMin-RLHF and CoSA (p7). | State the relocation as the first, titled contribution (Part D) |
| 3 | The experiment tests the proposed design | The method is defined by opposite contracts coexisting | 🔴 **3** | "training on contrasting pairs is the experiment the objective was built for, and we have not run it" (p4); §8 first bullet (p7) | Train strict and permissive contracts with opposite targets, plus a trained floor (C1) |
| 4 | Validity of the switching measures (Δ, efficiency, AQI) | The headline 86.7% rests on them | 🔴 **4** | Δ measured "against the plain model, not one model with and without it" (p4). AQI "does not rank models" yet is in efficiency (p4, p7). Lead over PPO/GRPO "comes from a lower NoInstruct twin" (p5). | Make the within-model contract gap the primary metric and drop AQI from efficiency (C4) |
| 5 | Benchmark validity (ECLIPTICA) | It is a named contribution | 🟡 **5** | Full-factorial design (p3); author-written contracts, 90 of 100 unscored (p4); fidelity ignores the query (0.560 / 0.565 / 0.571, p7–8) | Add a query-sensitive fidelity score from the existing logs (C4) |
| 6 | Floor analysis and safety relevance | The paper's most SC4AI-native empirical claim | 🟢 **7** | Categories fixed in advance; Table 6 (p6). But "most of these prompts were seen in training" (p6–7). | Re-run on held-out prompts and train an explicit floor (C1) |
| 7 | Statistical rigor | Reviewers reward it, and it is rare | 🟢 **8** | BCa paired intervals throughout (p4–6); one seed and one sample per case (p7) | Add 3 seeds for DPO and SwiPO (C2) |
| 8 | Baselines and fairness | Any "SwiPO beats X" claim depends on them | 🔴 **4** | Only SwiPO tuned (p4, p7). No prompted instruction-tuned model, CoSA, SimPO or KTO (p8). | Add Llama-3.1-8B-Instruct prompted with the same contracts (C2) |
| 9 | Output quality (degeneration) | A switch that loops is not a clean switch (§1 criterion, p1) | 🔴 **3** | "46 to 67% of Instruct-model ECLIPTICA answers contain over 30% duplicated sentences" (p5); "disclosed, not fixed" (p8) | Re-decode with a repetition penalty and re-score (C2) |
| 10 | Framing, clarity and tone | Decides whether the reviewer reads a contribution or a lab report | 🔴 **4** | Title answered "not yet" (p8). §8 opener about earlier reviewers (p7). Abstract closes on a tie (p1). Engineering detail in the main text (p4). | Rewrite abstract, contributions, §8 opener, conclusion (C3, Part D) |
| | **Total** | | **51 / 100** | | |

### 📊 Comparison with the 6 accepted papers

Rough re-scores on the same rubrics (rubrics 1–2 read as "conceptual framing" for papers outside social choice):

| Paper | Approx. score |
|---|---|
| Trust Paradox | ~28 |
| ShieldBench | ~40 |
| Biased Agents | ~42 |
| 🟠 **SwiPO (this paper)** | **51** |
| When Refusals Fail | ~57 |
| IntentGuard | ~58 |
| REFORM | ~62 |

SwiPO sits mid-pack: **best** of the seven on statistics (rubric 7) and conceptual framing (rubrics 1–2), **worst** on claim–experiment alignment (rubric 3) and tone (rubric 10). No accepted paper argued against its own headline the way this one does. With the Part C changes it would reach about 76 and top the set.

## 🅲 Part C · 24-hour improvements (ranked by expected gain)

GPU budget about 42 A100-hours total, about 11 hours of wall time on 4 GPUs, with writing in parallel. The paper is already submitted, so these apply if an OpenReview revision window is open, or for the camera-ready.

### C0. Summary

| Rank | Improvement | Gain | Rubrics (before → after) | Compute |
|---|---|---|---|---|
| 1️⃣ C1 | Run the designed experiment: opposite contracts, trained floor, pooled baseline | **+7** | 3: 3→7 · 6: 7→9 · 1: 6→7 | ~16 GPU-h |
| 2️⃣ C2 | Fix degeneration, add the missing baseline and seeds | **+6** | 9: 3→6 · 8: 4→6 · 7: 8→9 | ~15 GPU-h |
| 3️⃣ C3 | Rewrite the framing | **+5** | 10: 4→8 · 2: 7→8 | none |
| 4️⃣ C4 | Repair the measurements from existing logs | **+4** | 4: 4→7 · 5: 5→6 | ~1.5 GPU-h |
| 5️⃣ C5 | Measure Proposition 1 (influence across roles) | **+3** | 1: 7→9 · 2: 8→9 | ~10 GPU-h |

### C1. 1️⃣ Run the designed experiment: opposite contracts, a trained floor and a pooled baseline · +7

**What it shows:** the paper's own design and the SC4AI story in one experiment. PKU-SafeRLHF carries both a safety label (`safer_response_id`) and a helpfulness label (`better_response_id`). Two contracts:

| Contract | Preferred response $Y^+$ |
|---|---|
| 🛑 Strict | the safer response |
| 🟢 Permissive | the more helpful response |

Pairs where the two labels disagree give genuinely opposite targets on the same prompt. Three training runs, all from the existing DPO checkpoint:

| Run | Setup |
|---|---|
| (a) | Two-contract SwiPO |
| (b) | Two-tier SwiPO: as (a), but in the five Table 6 floor categories $Y^+$ = safer under both contracts |
| (c) | Pooled DPO on the same mixed data, no contract in the input (the implicit-Borda baseline of Eq. 1) |

**Report:** strict-minus-permissive refusal gap per model; the floor-minus-other gap (Table 6 quantity), which should fall for (b); where pooled DPO (c) lands between the two contracts (the §2 "compromise nobody chose", measured).

- **Needs:** Llama-3.1-8B, LoRA 16, the paper's settings. Data doubles, so about 4 h per SwiPO run (paper: 120 min for one contract, p4) and about 3.5 h for pooled DPO. Evaluate on 1,222 PKU-SafeRLHF prompts outside the 12,035-pair pool, stratified by harm category, so the "seen prompts" caveat (p7) disappears. About 16 GPU-h.
- **Where it goes:** new Table 7 plus one §5 paragraph ("Training contrasting contracts"), in the space freed by cutting Figure 2.

> [!WARNING]
> **Safety note (judge's):** the permissive arm trains a model to comply more. Keep the floor categories in (b), do not release the permissive adapter on its own, and add one sentence to §9. Report the result whichever way it comes out.

### C2. 2️⃣ Fix degeneration and add the missing baseline and seeds · +6

**What it shows:**

- whether switching survives once looping is removed (the paper calls re-decoding "the next experiment", p8);
- whether training beats simply prompting an instruction-tuned model, the baseline reviewers will ask for first (listed as missing, p8);
- seed variance for the DPO vs SwiPO tie.

| Item | Compute |
|---|---|
| Re-decode all 8 checkpoints with repetition penalty 1.15, same temperature and top-p (about 11.5k generations per model with vLLM) | ~4 GPU-h |
| Llama-3.1-8B-Instruct given the same contracts | ~1 GPU-h |
| 2 extra seeds for DPO and SwiPO | ~8 GPU-h |
| Their evaluation, re-running the existing deterministic scorers | ~2 GPU-h |

**Where it goes:** a "rep. penalty" block and a "Prompted Instruct" column in Table 4, plus a ±seed std on the efficiency row. Replaces Figure 3.

### C3. 3️⃣ Rewrite the framing (no GPU) · +5

**What it shows:** the paper leads with the social-choice contribution; every negative result is kept, reframed as a finding, a scope statement or an open problem (all of Part D). Also retitle for SC4AI, for example **"Switching Instead of Aggregating: Where Social Choice Goes When One LLM Serves Many Roles"**; the current title asks a question the paper answers "not yet".

**Where it goes:** abstract, §1 contributions, the §8 opener and bullets, §10.

### C4. 4️⃣ Repair the measurements using existing logs (~1.5 GPU-h) · +4

- Make the **within-model contract gap** the primary metric. For two-arm suites this is already the Instruct row of Table 4 (Cond. Safety 0.489 / 0.303 / 0.325 / 0.400).
- Report efficiency **without AQI** as the main number (83.4 vs 67.6, p5), and without TruthfulQA too, since TruthfulQA has no signal (p5).
- Add a **query-sensitive fidelity**: fidelity with the true prompt minus fidelity with a scrambled prompt, from the existing scrambled-prompt analysis (p7–8).
- Re-run Conditional Safety and Table 6 on **held-out prompts** for the 8 existing checkpoints (inference only).

> [!CAUTION]
> **Honest caveat (judge's):** under the within-model metric SwiPO is lowest on ECLIPTICA and second on Conditional Safety. That is exactly why C3's reframing matters: the contribution is the framing and the floor result, not SwiPO's ranking.

**Where it goes:** Table 4 restructured (gap rows primary, Δ rows to the repository); Table 6 replaced by its held-out version.

### C5. 5️⃣ Measure Proposition 1: influence across roles · +3

**What it shows:** the formal property as a number. Retrain C1(a) and C1(c) with role a's labels perturbed (flip 30% of permissive-role pairs, simulating misreporting), then measure how much strict-contract behaviour moves: change in strict-contract refusal on held-out prompts, and per-prompt answer agreement before vs after.

**Expected:** Prop. 1 predicts zero spillover for tabular policies; pooled DPO should move; shared LoRA weights should give a small nonzero "interference rate" (§2's "Two limits apply", p3). This answers "which formal property, and how closely does the trained model satisfy it?"

- **Needs:** 2 training runs of about 4 h each plus about 2 GPU-h evaluation.
- **Where it goes:** a 3-row table and 4 lines right after Prop. 1 on p3, replacing the "Two limits apply" paragraph.

### ✂️ CUT to make room (about 1.8 pages freed vs about 1.2 needed)

| Element | Cut | Frees |
|---|---|---|
| Figure 2 (radar, p7) | Duplicates Table 4; legend is the AQI-inclusive efficiency | ~0.45 page |
| Figure 3 (heatmap, p8) | Duplicates Table 4's raw scores | ~0.4 page |
| Table 5 (p6) | Reduce to one sentence ("fidelity overlaps on eight of ten types") | ~0.3 page |
| LITMUS/AQI as a suite (Table 3 row, p4–5 text) | One sentence plus a pointer to the repository; it does not compare models | |
| Cost paragraph and decoding settings (p4) | One sentence plus the Table 3 caption | |
| §8 Limitations (about one column, p7–8) | About a third of a column, moving each caveat in place as a scope statement (Part D) | |

## 🅳 Part D · Tone audit

**Problem tags:** 🔻 negative / self-critical · ⚙️ engineering-only · 🛡️ defensive · 💥 very damaging

### D1. Title, abstract, introduction (p1–2)

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 1 | p1, title | "Can You Trust One LLM Checkpoint to Switch Its Alignment for Every Agent Role?" | 🔻 a question the paper answers "not yet" (p8); no social-choice signal | "Switching Instead of Aggregating: Where Social Choice Goes When One LLM Serves Many Roles (SwiPO and ECLIPTICA-30k)" |
| 2 | p1, abstract | "every result here is on ECLIPTICA-3k, its evaluated 10-type, 3,000-case subset." | ⚙️ scope interrupts the contribution | "(results use ECLIPTICA-3k, its evaluated 10-type, 3,000-case subset)", placed inside the ECLIPTICA sentence |
| 3 | p1, abstract | "the run reported here trains a single safety contract and tests contracts it never saw." | 🔻 framed as a shortfall | "Training one safety contract on Llama-3.1-8B and testing contracts it never saw, we find the switch is real:" |
| 4 | p1, abstract | "it leads PPO and GRPO, but without the within-model AQI suite it cannot be separated from DPO, which switches more under safety contracts." | 🔻 abstract ends on the weakest result | "it leads PPO and GRPO, and without the within-model AQI suite it is statistically tied with DPO, which switches more under safety contracts." |
| 5 | p1, §1 | "The outcome is one policy per checkpoint: a deployer who needs a second behavior must either prompt around the trained policy or align and maintain a second model." | ⚙️ engineering motivation for a social-choice venue | "The outcome is one aggregate behavior per checkpoint, chosen by a rule nobody selected; a deployer who needs a second behavior must prompt around it or align and maintain a second model." |
| 6 | p1, §1 | "every experiment uses ECLIPTICA-3k, its 10type, 3,000-case subset." | ⚙️ repeated scope | "with ECLIPTICA-3k (10 types, 3,000 cases) as the scored release." |
| 7 | p1, §1 | "the run reported here trains one safety contract and measures transfer to unseen ones." | 🔻 | "evaluated here in the zero-shot transfer setting: one trained safety contract, tested on unseen contracts." |
| 8 | p1, §1 | "A five-suite evaluation with paired 95% intervals, in which SwiPO beats PPO and GRPO but cannot be separated from DPO once a within-model metric is set aside, reported with every failure mode and data caveat we found." | 🔻 self-critical | "A five-suite evaluation in which every comparison is a paired 95% BCa interval: SwiPO switches more than PPO and GRPO, is statistically tied with DPO once the within-model AQI suite is set aside, and a pre-specified floor test shows that no trainer inherits a non-switchable floor." |
| 9 | p2, §2 | "(This is the design; the experiment in Section 5 does not yet train opposite contracts.)" | 🔻 negative aside | "(Section 5 evaluates the zero-shot case, one trained contract with transfer to unseen ones; training opposite contracts is the direct test of this design.)" |

### D2. Social-choice section, benchmark, method (p3–4)

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 10 | p3, §2 | "The 100 ECLIPTICA-30k types were designed by the authors along 10 axes; they were not elicited from the groups a role serves." | 🔻 self-criticism of an agenda-setting point that is really a contribution | "ECLIPTICA-30k makes the agenda explicit: its 100 types, designed by the authors along 10 axes, form a published menu that elicitation from the groups a role serves can test, extend, or replace." |
| 11 | p3, §2 | "SwiPO trains only the second tier, so in our experiments any floor would have to be inherited from the supervised and DPO stages on PKU-SafeRLHF (Ji et al. 2024), which is not a deliberate social choice; Section 5 tests whether one was inherited and finds none." | 🔻 negative framing of a positive finding | "Because SwiPO trains the second tier, we can ask whether a floor emerges by default from the supervised and DPO stages on PKU-SafeRLHF (Ji et al. 2024), without any deliberate social choice. Section 5 shows it does not, so the floor must be chosen and trained." |
| 12 | p3, §2 | "Two limits apply. With shared weights, as with LoRA on one backbone, training one contract does move the others, which is the interference question in the Limitations; and the reported run trains a single contract, so the proposition describes the design, not our experiment." | 🔻 | "Scope. The proposition is exact for unlimited-capacity policies; with shared weights, as with LoRA on one backbone, training one contract can move the others, and that interference is measurable (Section 8). Our reported run trains a single contract, so the proposition characterizes the design that a contrasting-contract run tests." |
| 13 | p4, §3 | "the 90 added types are also hand-designed and not yet scored by any model." | 🔻 | "the 90 added types are hand-designed and released for scoring, extending the evaluated grid tenfold." |
| 14 | p4, §3 | "Both quantities are computed from the responses alone, without the request, a property whose consequence we report in the Limitations." | 🔻 defers a weakness | "Both quantities are computed from the responses alone, so the score measures instruction-conditioned style; Section 8 quantifies this (fidelity 0.560 with the true prompt, 0.565 with a scrambled one)." |
| 15 | p4, §4 | "we do not claim that its gradient properties are specific to SwiPO." | 🔻 self-deprecating | "SwiPO's contribution is the contract-indexed data design and the mandatory anchor, not a new gradient." |
| 16 | p4, §4 | "The run reported here does not yet use opposite contracts." … "training on contrasting pairs is the experiment the objective was built for, and we have not run it." | 🔻 | "Training regime: zero-shot transfer. [keep the middle sentences] The experiments therefore isolate how far a single trained safety contract transfers to unseen contracts, the situation a deployer faces when adding a role; training on contrasting pairs is the next experiment the objective enables." |
| 17 | p4, §4 | "it trains in 120 minutes on one A100-40GB, against 103 minutes for DPO; on-policy PPO and GRPO need an A100-80GB and 17 and 12 hours." | ⚙️ | "SwiPO keeps DPO's offline cost (120 against 103 minutes on one A100-40GB), six to eight times below on-policy GRPO and PPO (12 and 17 hours on an A100-80GB)." |
| 18 | p4, §4 | "SwiPO's hyper-parameters were chosen by 13 completed Optuna trials per variant, while DPO, PPO, and GRPO use fixed settings, which favors SwiPO in the comparison below." | ⚙️🔻 (keep the disclosure) | "Tuning disclosure: SwiPO uses 13 Optuna trials per variant and the other trainers fixed settings, which favors SwiPO; its leads over PPO and GRPO should be read with this in mind, and its tie with DPO holds despite it." |

### D3. Experiments and results (p4–6)

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 19 | p4, §5 | "On a two-arm suite a NoInstruct model therefore answers the same input twice, and its gap is sampling noise." | ⚙️🔻 | "On a two-arm suite the NoInstruct gap therefore serves as an empirical noise floor for that suite." |
| 20 | p4, §5 | "Every answer is one sample at temperature 0.7 and top-p 0.9, with at most 512 new tokens (256 for TruthfulQA and Conditional Safety, 150 for LITMUS)." | ⚙️ | Move to the Table 3 caption unchanged. |
| 21 | p5, §5 | "Against DPO the picture changes." | 🔻 | "DPO is the strongest rival." |
| 22 | p5, §5 | "TruthfulQA carries no switching signal for any trainer: … which are sampling noise. Dropping TruthfulQA as well puts DPO ahead (86.8 against 77.8; difference −9.0 [−40.7, 16.0])." | 🔻 | "TruthfulQA yields a finding about the channel itself: no Instruct model's honest-minus-confident gap differs from zero, so an uncertainty contract switches none of the four trainers (the ∆ values come mostly from NoInstruct gaps of −0.006 to −0.040, which are sampling noise). Without TruthfulQA and AQI, DPO leads on the point estimate (86.8 against 77.8) and the difference interval spans zero (−9.0 [−40.7, 16.0])." |
| 23 | p5, §5 | "SwiPO's Instruct ECLIPTICA score is the lowest of the four (0.367 against 0.379 to 0.389; every paired interval excludes zero), so its larger ∆ than PPO and GRPO comes from a lower NoInstruct twin." | 🔻 | "Decomposing ∆ shows the source of SwiPO's ECLIPTICA lead over PPO and GRPO: a lower NoInstruct twin, while its Instruct score is the lowest of the four (0.367 against 0.379 to 0.389; every paired interval excludes zero). This motivates within-model contract gaps as the primary switching measure." |
| 24 | p5, §5 | "No Instruct model exceeds 0.39 of ECLIPTICA's maximum, and none reaches the Length Control target (best ratio 1.14)." | 🔻 | "The benchmark leaves wide headroom: the best Instruct model reaches 0.39 of ECLIPTICA's maximum, and the best Length Control ratio is 1.14 against a target above 4." |
| 25 | p5, §5 | "Every trainer also loops: 46 to 67% of Instruct-model ECLIPTICA answers contain over 30% duplicated sentences or 5-grams at 512 tokens, and all scores include them." | 🔻 | "ECLIPTICA exposes a failure mode shared by all four objectives: 46 to 67% of Instruct-model answers contain over 30% duplicated sentences or 5-grams at 512 tokens, and every reported score includes them." |
| 26 | p5, §5 | "Each other trainer fails under at least one contract: DPO repeats itself or echoes the system prompt, PPO lectures or gives harmful advice, and GRPO turns incoherent or opens with tips for scaring the neighbor." | 🔻 failure list | "The other three answers map the ways a switch can fail: repetition and system-prompt leakage (DPO), lecturing and harmful advice (PPO), incoherence and tips for scaring the neighbor (GRPO)." |
| 27 | p6, §5 | "This is one prompt chosen to illustrate failure modes, not a measured rate." | 🔻 | "Figure 1 illustrates the failure taxonomy; the measured rates are in Tables 4 and 6." |
| 28 | p6, §5 | "and most of these prompts were seen in training (Limitations)." | 🔻 negative aside | "and since about nine in ten of these prompts appeared in the training pool, the test probes familiar requests, where an inherited floor would be most likely to show." |
| 29 | p6, §5 | "What differs between trainers is smaller than the efficiency score suggests (Findings). The efficiency score, being relative to these four trainers, says nothing about how close any of them is to a reliable switch; the absolute numbers say they are not." | 🔻 | "The governance conclusion therefore holds for every trainer, while the trainer ranking is relative to these four. The absolute scores (best ECLIPTICA 0.39 of maximum, best length ratio 1.14 against a target above 4) mark the distance to a reliable switch, which ECLIPTICA is built to track." |
| 30 | p6, Table 5 caption | "No SwiPO interval lies above another trainer's." | 🔻 phrasing (the fact must stay) | "Per-type fidelity is statistically indistinguishable across trainers on eight of ten types, and no trainer, SwiPO included, is above all others on any type." (After the C2 cut, one sentence in §5.) |

### D4. Limitations, ethics, conclusion (p7–8)

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 31 | p7, §8 opener | "The reviewers of an earlier version asked for several experiments that need compute or annotation we do not have for this submission, and a code audit for this version found further caveats. We list them rather than claim them." | 💥 signals a rejected resubmission and a missing budget | "Scope and next experiments. Each item states what a claim covers and the experiment that extends it." |
| 32 | p7, §8 | "whether the objective separates trained, conflicting contracts is untested." | 🔻 | "Separating trained, conflicting contracts is the next experiment; its data (one preference pair per contract per prompt) is specified in Section 4." (Or report the C1 result.) |
| 33 | p7, §8 | "no run without the anchor exists, because the trainer requires λ > 0, so its necessity is argued, not measured." | 🔻 | "The anchor is mandatory by design (λ > 0); its contribution is motivated in Section 4, and an anchor-free ablation is an open experiment. Intervals capture item sampling, not seed variance." |
| 34 | p7, §8 | "so about nine in ten were seen in training. This suite, and the floor analysis built on it, therefore measure switching on familiar requests." | 🔻 | "About nine in ten Conditional Safety prompts appear in the training pool, so this suite and the floor analysis measure switching on familiar requests, where a trained boundary should be strongest." |
| 35 | p7, §8 | "AQI normalizes its indices within each model's run …, so AQI and its ∆ are not comparable across trainers, yet they enter the efficiency score." | 🔻 | "Efficiency with and without AQI. Because AQI normalizes within each model (SwiPO's 55.0 is the top of its own range), we report efficiency both ways: SwiPO ranks first in each (86.7 and 83.4), and without AQI its lead over DPO (67.6) is not significant (+15.7, interval −4.1 to 39.7)." |
| 36 | p7, §8 | "the other 90 types of ECLIPTICA-30k are released but unscored, and no type was trained on. Whether contracts interfere at 50 or 100 types, and whether one anchor suffices there, is untested." | 🔻 | "Results cover the 10 scored types, none trained on; the 90 released types make interference at 50 or 100 contracts, and the sufficiency of one anchor there, directly testable." |
| 37 | p7–8, §8 | "ECLIPTICA's fidelity score ignores the query." … "a query-sensitive metric is needed before ECLIPTICA can claim causal isolation of policy control." | 🔻 negative heading | "What fidelity measures. Replacing X leaves SwiPO's score essentially unchanged (0.560 true prompt, 0.565 scrambled, 0.571 instruction alone; n = 1,000, intervals about ±0.004), so fidelity measures instruction-conditioned style; a query-sensitive variant is the extension that lets ECLIPTICA isolate policy control causally." |
| 38 | p8, §8 | "The repetition rates above are disclosed, not fixed; decoding with a repetition penalty and re-scoring is the next experiment." | 🔻 | "Scores include the looping answers of Section 5; re-scoring under a repetition penalty separates switching from decoding." (Or report the C2 result.) |
| 39 | p8, §8 | "We do not compare with SimPO …, KTO …, multi-objective decoding, or an instruction-tuned model given the same contracts as a system prompt; we do not test general capabilities (MMLU, GSM8K, HumanEval) or adversarial jailbreak suites." | 🔻 negative list | "Comparison scope: the four trainers share one SFT base; SimPO, KTO, multi-objective decoding, a prompted instruction-tuned model, general-capability suites (MMLU, GSM8K, HumanEval), and jailbreak suites lie outside it." |
| 40 | p8, §9 | "Who sets that floor is a collective decision that this paper does not make." | 🔻 negative close | "Who sets that floor is a collective decision; this paper frames it and supplies the test (Table 6) that any chosen floor must pass." |
| 41 | p8, §10 | "Can one LLM checkpoint be trusted to switch its alignment for every agent role? … The answer to the title question is therefore not yet." | 💥 the paper's last word is a verdict against itself | See rewrite 2 below. |

### D5. 🥇 The 3 rewrites that matter most

| Priority | Row | Why |
|---|---|---|
| 1️⃣ | **#31, the §8 opener** | Telling SC4AI reviewers that an earlier version was reviewed and a "code audit" found caveats invites rejection. Replace with: "Scope and next experiments. Each item states what a claim covers and the experiment that extends it." |
| 2️⃣ | **#41, the Conclusion** | Replace the whole paragraph with the text below. |
| 3️⃣ | **#8, the 4th contribution bullet** | The contribution list is where a reviewer decides what the paper is, and it currently ends on "cannot be separated from DPO". The rewrite keeps the tie and adds the floor finding. |

**Rewritten Conclusion (#41):**

> Switchable alignment moves the aggregation question out of training and into governance: who controls the switch, which settings are offered, and what lies below it. Our evidence makes the last question pressing: in all four trained models, refusals on violence or trafficking requests fall under a permissive contract at least as far as any others, so a non-switchable floor does not arise by default and has to be chosen collectively and trained. Trained on a single safety contract, SwiPO transfers to unseen contracts better than PPO and GRPO and is statistically tied with DPO once AQI, which does not compare models, is set aside (86.7% relative efficiency against DPO's 56.1% with it; 83.4% against 67.6%, an interval spanning zero, without it); DPO switches more on refusals. A reliable switch for every agent role is still ahead: every trainer still loops, and training opposite contracts on the same prompts, the experiment SwiPO was designed for, is the next step ECLIPTICA-30k is built to measure.

### D6. ✍️ Rewritten abstract (283 words, same facts, opens with the contribution)

> When one model serves many agent roles, whose preferences does it follow, by what rule? Pooled preference optimization such as DPO answers implicitly: prior work shows that when the annotator's role is not recorded, the learned policy ranks answers by a Borda count over hidden roles, a rule nobody chose. We study the steerable pluralistic alternative, in which a natural-language alignment instruction writes the role's behavioral contract into the input, so one model fits each role's preference without aggregating them. Our first contribution locates where aggregation goes: the instruction channel, raising four social-choice questions: who may set the instruction (oversight), which contracts are offered (agenda setting and elicitation), which constraints no contract may lift (a collective choice over everyone affected), and who gains from misreporting (deployers rather than annotators). We ground them with ECLIPTICA-30k (300 prompts by 100 alignment-instruction types; results use ECLIPTICA-3k, its evaluated 10-type, 3,000-case subset) and SwiPO (Switchable Preference Optimization), which conditions preference optimization on the instruction under a mandatory KL anchor. Training one safety contract on Llama-3.1-8B and testing contracts it never saw, we find the switch is real: every trained model's refusal rate moves by 0.30 to 0.49 between a strict and a permissive contract. It also reaches the requests a collective floor would most plausibly cover: on violence, physical harm, trafficking, and threats to public health or national security, the permissive contract cuts refusals at least as much as elsewhere. SwiPO reaches 86.7% instruction-alignment efficiency (95% interval 76.8 to 96.2), relative to the four trainers compared, against 56.1% (DPO), 36.1% (GRPO), and 20.4% (PPO); it leads PPO and GRPO, and without the within-model AQI suite it is statistically tied with DPO, which switches more under safety contracts.

## 🔎 Fact-check (by Claude Code, not the judge)

Checked 2026-11-26 against the text of the submitted [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf).

### ✅ Confirmed

| # | Judge claim | Where it is |
|---|---|---|
| 1 | Three-role Borda: refusal 0.80, guidance 1.25, detail 0.95 | p. 2; arithmetic also checks (0.40·2 = 0.80; 0.40 + 0.35 + 0.25·2 = 1.25; 0.35·2 + 0.25 = 0.95) |
| 2 | Menu choice called "dictatorial"; Proposition 1, "Two limits apply", Gibbard–Satterthwaite on p. 3 | p. 3 |
| 3 | SwiPO continues from the DPO checkpoint | p. 4 ("SwiPO continues from the DPO checkpoint") |
| 4 | Cond. Safety Instruct row 0.489 / 0.303 / 0.325 / 0.400 (DPO, PPO, GRPO, SwiPO); SwiPO second | Table 4, p. 5 |
| 5 | Efficiency 86.7 [76.8, 96.2]; without AQI 83.4 vs 67.6, +15.7 [−4.1, 39.7]; without TruthfulQA too 86.8 vs 77.8, −9.0 [−40.7, 16.0] | Table 4 and text, p. 5 |
| 6 | NoInstruct TruthfulQA gaps −0.006 to −0.040 | p. 5 |
| 7 | Length Control "target above 4" (rewrites #24, #29) | p. 4, Table 3 ("target above 4") |
| 8 | Table 5 caption "No SwiPO interval lies above another trainer's"; "eight of ten types" | p. 6 |
| 9 | Query test 0.560 / 0.565 / 0.571; §8 opener about earlier reviewers | p. 7 |
| 10 | Rubric total 6+7+3+4+5+7+8+4+3+4 = 51; Part C GPU total 16 + 15 + 1.5 + 10 ≈ 42 | arithmetic |
| 11 | Rewritten abstract length | 283 words vs about 285 in the original |

### ⚠️ Issues found

| # | Issue | Impact |
|---|---|---|
| 1 | **"Statistically tied with DPO"** (rewrites #4, #8, #18, Conclusion, abstract). An interval spanning zero means the difference is **not significant**, not that the two are equal. A reviewer may read "tied" as a claimed equivalence. Safer: "not separable from DPO" or "the difference is not significant". | Medium: wording in the headline sentences. |
| 2 | **Rewrites #28 and #34 add claims the paper does not make**: "where an inherited floor would be most likely to show" and "where a trained boundary should be strongest". Both are plausible but untested; the prompt said keep every fact true. | Medium: drop or soften those clauses. |
| 3 | **Rewrite #17 "six to eight times below"**: 12 h / 120 min = 6×, 17 h / 120 min = 8.5×. Should read "six to eight and a half times". | Low. |
| 4 | **Rewrite #18 "its tie with DPO holds despite it"**: tuning favors SwiPO, so a non-significant result despite extra tuning is evidence against SwiPO, not for it; the clause reads as spin. | Low: drop the clause or say it plainly. |
| 5 | **C1 trains a permissive adapter on PKU-SafeRLHF's more-helpful (possibly harmful) responses.** The judge's safety note is right: keep the floor categories, never release that adapter. | Process: decide before running. |
| 6 | **C1 assumes 1,222 held-out PKU-SafeRLHF prompts outside our 12,035-pair pool.** The dataset does carry separate safety and helpfulness labels, but whether enough unseen pairs exist was not checked here. | Check the data before planning C1/C4. |
| 7 | **GPU-hour estimates are the judge's guesses** (A100 basis), not measured. | Plan with your own hardware numbers. |
| 8 | **§1–§10 numbering and the re-scores of the six accepted papers (~28 to ~62) are the judge's own**; the paper's sections are unnumbered and the re-scores are subjective. | Informational. |
