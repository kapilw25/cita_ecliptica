> Claude (Opus 5.5) review of the [v7_MATH4AI_4page](../../../v7_MATH4AI_4page/0_main.pdf) draft for MATH4AI, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~8:15 AM PST. The review judged all 4 drafts in one document: this file keeps the read-me, the v7 section, Part E and the final ranking; the other drafts' reviews are in [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/by_claude.md), [v5_MultiRobust_4page](../v5_MultiRobust_4page/by_claude.md), [v6_Bench2Evidence_4page](../v6_Bench2Evidence_4page/by_claude.md). Text is word for word; only the horizontal rules between sections were left out, and the shared tone-audit rows S1–S9 from the v4 section are repeated at the top of this Part D table.

# SwiPO: Review of 4 AAAI-27 Venue Drafts

## Read-me

I'll read all four drafts closely, then score each one against the calibration sheet, adjusted for its venue.

I've read all four drafts in full and checked every number cited below against the PDFs. Sections 3, 4 and 6, Figure 1 and Tables 1–4 are almost word-for-word the same in all four. I audit that shared text once, in rows S1–S9 under v4's Part D, and each later Part D table covers only the lines unique to that version.

## v7: MATH4AI (single-blind, deadline Dec 2)

### Part A. Acceptance probability

**MATH4AI: 35%. Typical safety/alignment workshop: 45%.**

A mathematics reviewer will read Sec. 2 first, and it is thin:
- **Proposition 1 is linearity of expectation.** Its proof is two lines (p. 2).
- **Its assumption never holds in the models tested.** It requires "parameters θ_I that no other contract uses", which no transformer has.
- **Under shared parameters the corollary predicts nothing.** The paper says so itself: "The corollary bounds no drift through shared parameters, so any change in the gap is drift, of either sign." (p. 2). No outcome of the experiment could contradict it.

The empirical half is rigorous, but about 60% of the page space is the shared audit (sponsor, authority, floor), which doesn't test the theorem. Poster tracks at math workshops are lenient, which is why this isn't lower.

**Three things most likely to cause rejection**
1. **The result is trivial** and its assumption is unrealistic (Prop. 1, p. 2).
2. **The claimed test is unfalsifiable**, and one claim goes beyond the data. "The direction depends on the instrument, as drift would" (p. 2) clearly holds only for SwiPO-R (−0.113 by phrase vs. +0.055 by judge). For the other steps the phrase change is near zero (Tables 2–3). The corollary also makes no prediction about whether the instruments agree.
3. **The proposed loss is "unbounded below"** (p. 2) for λ > 0. A math reviewer will ask why a loss without a minimizer is proposed, and the paper doesn't say.

**Three strongest points**
1. **A mechanism for the empirical null.** One-contract data cannot reward a contract difference. The paper links this to the Borda-count critique of pooled DPO (Siththaranjan et al.; Conitzer et al.; p. 1).
2. **A crisp, testable prescription:** "tuples that pair one request with several contracts and different preferred answers" (Conclusion, p. 4).
3. **Careful scope** ("for gradients, not minimizers", p. 2) and rigorous intervals on every empirical claim.

### Part B. Ten rubrics

| Rubric | Why it matters here | Score | Evidence | The one change that adds the most points |
|---|---|---|---|---|
| Fit to the call | "mathematical foundations of AI agents" | 5 | Sec. 2 is 1 of 7 sections | Cut the shared audit; lead with the theory |
| Mathematical depth and novelty | Core criterion | 3 | Prop. 1 via linearity (p. 2) | Proposition 2 on the population optimum (C2) |
| Correctness and realism of assumptions | Reviewers check hypotheses | 6 | Correct; "θ_I that no other contract uses" unrealistic | Restate as a gradient-coupling result with shared θ |
| Testability (theory → prediction → test) | Separates theory from commentary | 3 | "any change in the gap is drift, of either sign" (p. 2) | Multi-contract training test (C1) |
| Empirical support for the theory | Experiments should test the statement | 6 | Steps −0.034 to +0.055 by judge (p. 2); rigorous but indirect | C1 |
| Connection to the theory literature | Positioning | 4 | Siththaranjan; Conitzer; no DPO-optimum theory (e.g. IPO) | Cite and use the DPO closed-form optimum (C2) |
| "Stability and reliability of agentic AI" | Named topic | 5 | Drift framing (Sec. 2) | Phrase the corollary as a reliability guarantee about unseen contracts |
| Clarity of formal presentation | Math readers | 6 | Eq. 1 and Eq. 2 repeat the same loss (p. 2) | Delete Eq. 2 |
| Honesty about scope | Valued | 9 | "for gradients, not minimizers" (p. 2) | Keep |
| Prescriptive value | Future-shaping theme | 6 | Conclusion, p. 4, untested | C1 |

**Total: 54/100.** On a math rubric all three accepted papers would score low (about 25–35), since none has theory. That comparison is less informative here than the venue's own norms, where v7 sits below a typical accepted poster on depth.

### Part C. Improvements before Dec 2 (new training allowed)

1. **Test the prescription.**
   - *Shows:* whether multi-contract tuples create a switch that one-contract training cannot. This turns the corollary into a falsifiable prediction.
   - *Needs:* duplicate the PKU-SafeRLHF pairs under two contracts. Under strict, prefer the safer response (the dataset's safety preference label). Under permissive, prefer the more helpful one (the helpfulness label) on non-floor categories and the safer one on floor categories. Train DPO (λ = 0) and SwiPO on the SFT chain with existing hyper-parameters: about 4–8 GPU-hours each. Evaluate gap, judge, harm and floor: about 2 GPU-hours.
   - *Prediction to state in advance:* the judge gap exceeds the one-contract drift band (−0.034 to +0.055), and the floor gap difference turns negative.
   - *Where:* one short table replacing Table 4.
   - *Raises:* testability +4, prescriptive value +2, empirical support +2.
   - *Caveat:* report it either way.
2. **Proposition 2 (population optimum).**
   - *Shows:* the statement a math reviewer expects. With full conditional capacity and λ = 0, the DPO minimizer satisfies β∆(I, X) = logit P(y_w ≻ y_l | I, X) for each contract. The switch at the optimum therefore equals the difference in preference logits across contracts, and data with one contract leaves it unidentified. This extends the known closed form of DPO to conditioning on I.
   - *Needs:* about half a day of writing.
   - *Where:* after Corollary 1. Add a remark that SwiPO's λ > 0 has no minimizer, so only the gradient statements cover it.
   - *Raises:* depth +2, literature +1, correctness +1.
3. **Make the existing test falsifiable.**
   - *Shows:* a drift band taken from switches training never targeted. Table 1 gives length (word ratio 1.015–1.089), confidence (−0.011 to +0.004) and sponsor (≤ 0.002).
   - *Needs:* re-analysis only.
   - *Where:* replaces the "as drift would" sentence (D row 5).
   - *Raises:* testability +2.
4. **Gradient-coupling measurement (stretch).**
   - *Shows:* whether the first-order drift sign is predicted by the training gradient.
   - *Needs:* the cosine between ∇ log π(refusal | I_strict, X) − ∇ log π(refusal | I_perm, X) and ∇L_I0 on 200 prompts per checkpoint. About 2 GPU-hours.
   - *Where:* one sentence and one number per step.
   - *Raises:* depth +1.
5. **Remove the overclaims** (D rows 5–6).
   - *Raises:* correctness +1.

**Cut to make room:** the sponsor and authority paragraphs (p. 4), Table 4, and the Stance, Promotion and Authority rows of Table 1 (about 30 lines); the duplicate Eq. 2 in Setup (p. 2).

### Part D. Tone audit (S1–S9 apply; S2 matters most here, because the loss is the object of the theory)

Rows S1–S9 are the shared rows from the v4 section; they apply to all four versions.

| # | Page / section | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| S1 | p. 2, Sec. 3 Models (all versions) | "The released PPO adapters are untrained: all 224 of their LoRA B matrices are zero, so PPO as trained is the SFT model and its final adapter alone is the base model, and its rows are second runs of those two." | Negative, engineering | "The released PPO adapters leave the weights unchanged (all 224 LoRA B matrices are zero), which gives the study a built-in replicate: PPO as trained re-runs the SFT model, and its final adapter alone re-runs the base model." |
| S2 | p. 2, Sec. 3 (all) | "on data answers it is no divergence estimate, and minimizing it lowers both likelihoods." | Criticism of own loss | "evaluated on the data answers, ρ̄θ acts as a likelihood penalty rather than a divergence estimate: minimizing it lowers both likelihoods." |
| S3 | Sec. 4, p. 2–3 (all) | "Scoring only each answer's first turn changes nothing (Table 3), a check needed because the models with SFT in their chain run past their turn in 98 to 99% of answers under the base model's stopping rule." | Engineering | "The gaps are robust to decoding: under the base model's stopping rule, models with SFT in their chain continue past their turn in 98 to 99% of answers, and scoring only the first turn leaves every gap unchanged (Table 3)." |
| S4 | Sec. 4, p. 3 (all) | "Trained with one contract, SwiPO's loss does not restore the lever once SFT is in the chain." | Negative | "The two chains identify the training chain, not the loss, as what sets SwiPO's lever: trained with one contract after SFT, SwiPO does not restore it." |
| S5 | Sec. 4 floor paragraph, p. 3–4 (all) | "read as a refusal floor, it holds for none, so a refusal floor has to be a training target." | Negative | "read as a refusal floor, it holds for no trained model, which identifies the refusal floor as a target that training must supply explicitly." |
| S6 | Sec. 6, p. 4 (all) | "SwiPO received the only tuning budget (13 Optuna trials); DPO and GRPO use fixed settings, so the comparison favors SwiPO." | Self-critical | "SwiPO alone was tuned (13 Optuna trials; DPO and GRPO use fixed settings), so the comparison favors SwiPO, which makes the null result for SwiPO after SFT conservative." |
| S7 | Sec. 6, p. 4 (all) | "Refusal is scored by a phrase heuristic that agrees poorly with an LLM judge (κ 0.03 to 0.58, Table 3), so we claim a lever only where the instruments agree, and harm by one classifier (Llama Guard 3); neither is yet checked against human labels." | Negative | "Because the phrase heuristic and the LLM judge agree only partly (κ 0.03 to 0.58, Table 3), we claim a lever only where both detect it, and score harm with one classifier (Llama Guard 3); neither instrument has yet been validated against human labels, the next step." |
| S8 | Table 1, Stance row, p. 3 (all) | "not readable: the score tracks how much answers differ, ranking the prompted model last" | Negative about own metric | "metric check: embedding similarity tracks how much answers differ (it ranks the prompted model last), so we report it without a conclusion" |
| S9 | Table 1, floor row, p. 3 (all) | "not learned: moves as much as elsewhere" | Negative label | "no trained floor yet: moves as much as elsewhere" |
| 1 | Abstract, p. 1 | "By the refusal-phrase heuristic neither SwiPO chain gains over its start" | Negative | "Consistent with the corollary, neither SwiPO chain gains over its start by the refusal-phrase heuristic" |
| 2 | Sec. 2, p. 2 | "We state both results for gradients, not minimizers: with λ > 0 the penalty lowers both likelihoods and L is unbounded below." | Self-criticism of the loss | "Both results are stated for gradients, the quantity training follows, so they hold without a minimizer; this matters because with λ > 0 the penalty lowers both likelihoods and L is unbounded below." |
| 3 | Sec. 2, p. 2 | "The corollary bounds no drift through shared parameters, so any change in the gap is drift, of either sign." | Undercuts the result | "The corollary leaves drift through shared parameters unbounded and predicts no systematic, contract-specific gain; any change in the gap is therefore drift, of either sign." |
| 4 | Sec. 2, p. 2 | "By phrase neither chain gains." | Negative | "By phrase, neither chain gains, as the corollary allows." |
| 5 | Sec. 2, p. 2 | "The direction depends on the instrument, as drift would." | Overclaim (clear only for SwiPO-R) | "For SwiPO-R the direction depends on the instrument (−0.113 by phrase, +0.055 by judge), consistent with drift rather than a learned switch." |
| 6 | Conclusion, p. 4 | "Trained with one contract, SwiPO, DPO, and GRPO change their starting model's switch only by small drift whose sign depends on the instrument;" | Same overgeneralization | "Trained with one contract, SwiPO, DPO, and GRPO change their starting model's switch only by small drift (−0.034 to +0.055 by judge), whose sign can depend on the instrument;" |

**D.2. The three rewrites that matter most:** #5 (it removes a claim a reviewer can falsify from Tables 2–3), #3 (it states the corollary's prediction) and #2.

**D.3. Rewritten abstract** (219 words; current 229)

> We show when a contract-conditioned preference loss can make one checkpoint switch behavior with a natural-language contract I. For a policy class with independent conditionals per contract, the loss separates into one term per contract, so each contract's behavior is updated only by its own data; with a single training contract, no term of the loss rewards a difference between other contracts, and training can move the switch only by drift through shared parameters. We test this on preference-trained Llama-3.1-8B models (DPO, GRPO, and SwiPO, an instruction-conditioned DPO with a log-ratio penalty to the reference model; the released PPO adapter is untrained), each trained with one safety contract and evaluated as trained. Consistent with the corollary, neither SwiPO chain gains over its start by the refusal-phrase heuristic (change in the strict-minus-permissive gap +0.017, 95% interval −0.025 to +0.057, and −0.113, −0.155 to −0.070), and an LLM judge sees the five one-contract training steps move the gap by −0.034 to +0.055. The pretrained model alone has a phrase gap of 0.299 (0.266 to 0.332), mostly wording the judge does not see (0.012), which supervised fine-tuning on one contract removes; only SwiPO started without it keeps a switch under both instruments (judge 0.128). The separability result therefore makes precise what a switchable checkpoint needs: training data with several contracts per request.

## Part E. Across the four versions

### Disagreements between the PDFs

1. **Concurrent-submission disclosure.**
   - v4 footnote 1 (p. 2): "4-page versions are under review at AAAI-27 MultiRobust, MATH4AI, and Bench2Evidence."
   - v7 footnote 1 (p. 2): "…under review at AAAI-27 LoyalAgents, MultiRobust, and Bench2Evidence."
   - v5 and v6 have no disclosure; their footnote 1 is "Stacked adapters can be loaded two ways; Table 2 reports both".
   - On Nov 28, the MATH4AI and Bench2Evidence versions are not yet under review, so v4's wording is inaccurate on its submission date.
2. **Harm under final-only loading.**
   - v6 intro (p. 1): switches "that also move harmful content".
   - v6 abstract: "three of four also move harmful content".
   - Results in all versions: "DPO +0.042 …, GRPO +0.045 …, SwiPO +0.085" (p. 2–3). There are five final-only rows, and which SwiPO is meant is unspecified.
3. **Whether either correction removes the switch.**
   - v6 intro: "either correction alone removes most of the switch (Table 5)".
   - Table 5 itself: SwiPO-R keeps 0.385 under the composition correction alone.
4. **Whether training moved the switch at all.**
   - v4 abstract: "Every model with SFT in its chain barely follows any contract we tested".
   - v7 Sec. 2 (p. 2): "SwiPO-R (+0.055 [+0.010, +0.099]) and DPO (+0.047 [+0.002, +0.091]) exclude zero".
   - These are not strictly contradictory, since DPO's resulting judge gap of 0.025 ± 0.030 includes zero. But a reader of both versions will see "DPO training changed the switch" in one and "barely follows" in the other.
5. **Table 1, Stance row.**
   - v4: "as trained 0.14 to 0.17, SwiPO-R 0.37 (0.07)".
   - v5–v7 add "(final adapter alone 0.37 to 0.39)".
6. **The same experiments are framed as three different sets of five.**
   - v4: "five controls" (authority, disclosure, conflicts, limits, audit).
   - v5: "five-property" test (target, side effects, floor, held-out prompts, channel).
   - v6: "Five checks" (composition, decoding, scorer, contamination, controls).
   - None of these contradict each other, but a chair who reads all four will notice the same number recast three ways over identical tables.
7. **v6's ethics sentence repeats v4's framework.** "the contract must come from an accountable principal, be disclosed and logged, and sit above a floor" (v6, p. 4) restates v4's Sec. 2 controls.

### One paper or four?

A program chair would read these as **one paper sent four times with different front matter.** By 8-word-sequence overlap of the main text, 57–68% of any two versions is shared, and 45–56% of each version is shared by all four. On top of that, Figure 1, Section 3, most of Section 4, Tables 1–4 and Section 6 are verbatim in all of them.

The most visible problem is the identical Figure 1, the first thing a reader sees. It is about adapter loading, which is v6's topic and incidental to the other three. It also undermines double-blind review for v5 and v6, because the same figure appears in the signed v4 and v7.

**What is distinct in each version**

| Version | Distinct content | Verdict |
|---|---|---|
| v6 | Table 5 (error budget), the check framing, and its own results paragraph | Most distinct |
| v7 | Proposition 1, Corollary 1, and the drift analysis (Sec. 2) | Distinct front, shared body |
| v4 | Sec. 2 controls and two extra columns in Table 1 | Mostly shared |
| v5 | Figure 2 and one XSTest paragraph | Least distinct |

**What most needs to change.** v5 needs it most, then v4. Give each version its own lead figure: the trade-off plane for v5, the loyalty levers for v4. Reorder Results so the venue's finding comes first, and cut the rows and paragraphs that serve other venues (Part C cut lists).

Also make the concurrent-submission disclosure consistent across all four. LoyalAgents explicitly accepts work under review elsewhere and Bench2Evidence accepts published work. MultiRobust and MATH4AI say nothing, so the disclosure is safest stated the same way everywhere, in third person for the double-blind venues.

## Ranking by acceptance probability, with the most valuable change for each

1. **v6 Bench2Evidence: 75% (deadline Dec 2).** Add stability across runs. Present the PPO rows as test-retest replicates (existing numbers) and add 3 more sampled answers per prompt for all 8 configurations (about 6–8 GPU-hours). Also fix the intro bullet that Table 5 contradicts.
2. **v4 LoyalAgents: 55% (about 20 h).** Replace Figure 1 with a loyalty-lever figure built from existing numbers: judge gap, sponsor rate and user-override gap per model. Rewrite the abstract to open with "the only model that follows contracts is also the one a hidden sponsor and the user can turn" (D.3).
3. **v5 MultiRobust: 45% (about 20 h).** Make the safety-helpfulness plane the lead figure and put harm on it: Llama Guard 3 on the existing XSTest answers, under 1 GPU-hour. Also state Table 2's objective-driven harm shift (SFT 0.300 → DPO 0.028, SwiPO-S 0.014).
4. **v7 MATH4AI: 35% (deadline Dec 2).** Train the multi-contract model the corollary prescribes (about 10–18 GPU-hours including evaluation), with the prediction stated in advance. That turns an unfalsifiable statement into a tested one, and it is the only change that moves v7 from a restatement to a result.

Given the clock, I'd spend today on v4 and v5 using rewrites, re-plots and the two short Llama Guard runs. The GPU budget for the GRPO-free multi-contract training and the resampling runs can go to v6 and v7 this weekend.
