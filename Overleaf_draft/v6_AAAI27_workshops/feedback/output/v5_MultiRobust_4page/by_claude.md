> Claude (Opus 5.5) review of the [v5_MultiRobust_4page](../../../v5_MultiRobust_4page/0_main.pdf) draft for MultiRobust, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~8:15 AM PST. The review judged all 4 drafts in one document: this file keeps the read-me, the v5 section, Part E and the final ranking; the other drafts' reviews are in [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/by_claude.md), [v6_Bench2Evidence_4page](../v6_Bench2Evidence_4page/by_claude.md), [v7_MATH4AI_4page](../v7_MATH4AI_4page/by_claude.md). Text is word for word; only the horizontal rules between sections were left out, and the shared tone-audit rows S1–S9 from the v4 section are repeated at the top of this Part D table.

# SwiPO: Review of 4 AAAI-27 Venue Drafts

## Read-me

I'll read all four drafts closely, then score each one against the calibration sheet, adjusted for its venue.

I've read all four drafts in full and checked every number cited below against the PDFs. Sections 3, 4 and 6, Figure 1 and Tables 1–4 are almost word-for-word the same in all four. I audit that shared text once, in rows S1–S9 under v4's Part D, and each later Part D table covers only the lines unique to that version.

## v5: MultiRobust (double-blind, 4 pages including figures, deadline in about 20 h)

### Part A. Acceptance probability

**MultiRobust: 45%. Typical safety/alignment workshop: 50%.**

Figure 2 (p. 4) is the right kind of evidence for this venue: a safety-helpfulness plane with the strict and permissive contracts as filled and hollow points. Sec. 2 also treats harm as a side-effect constraint and the floor as a fixed constraint. However, the call is about optimizing across trade-offs. The paper has no optimization contribution: its method is not separable from DPO after SFT. Its trade-off evidence is two points per model on XSTest, scored by a phrase heuristic that "counts the base's repeated contract as refusal" (Figure 2 caption). Figure 1, the lead visual, is about adapter loading, which is not this venue's topic.

**Three things most likely to cause rejection**
1. **No multi-objective method or Pareto metric.** SwiPO after SFT gives "+0.017 [−0.025, 0.057]" over DPO (p. 3). Sec. 5 cites Ramé, Zhou, Dai and Wang but compares against none of them.
2. **Trained models look unsafe on XSTest.** Models with SFT in their chain refuse only "0.040 to 0.155" of unsafe XSTest prompts (p. 4), and the plane has no harm classifier on it.
3. **The front page signals a different paper.** Figure 1 and the last abstract sentence ("Evaluations must load stacked adapters as trained", p. 1) are about loading, not trade-offs.

**Three strongest points**
1. **A five-property test** (target, side effects, floor, held-out prompts, channel; Sec. 2, p. 2) that is constraint-aware evaluation, matching "constraint handling in AI safety".
2. **A clear plane result.** Instruct reaches two points (strict: 0.995 / 0.608; permissive: 0.845 / 0.968), while each trained model holds one (p. 4, Fig. 2).
3. **Harm does not move with the contract** (every interval includes zero, Table 2). Meanwhile Table 2 already shows the training objective moving the strict unsafe rate from 0.300 (SFT) to 0.028 (DPO), 0.022 (SwiPO-R) and 0.014 (SwiPO-S). This is a strong multi-objective observation that the text never states.

### Part B. Ten rubrics

| Rubric | Why it matters here | Score | Evidence | The one change that adds the most points |
|---|---|---|---|---|
| Fit to the multi-objective call | First filter | 6 | Title; Sec. 1 citations; Fig. 2 (p. 4) | Make the trade-off plane the lead figure (C1) |
| Trade-off evidence | "Pareto-aware evaluation" topic | 6 | Fig. 2: XSTest, phrase heuristic, 2 points per model | Harm axis on the same suite (C2) |
| Constraint handling | Named topic | 7 | Harm as side effect, floor fixed in advance (Sec. 2); Table 4 | Report a constraint-satisfaction rate per model |
| Optimization contribution | Venue centre | 3 | SwiPO not separable from DPO (p. 3) | Present the objective-driven harm shift in Table 2 as the optimization finding (C3) |
| Comparison to multi-objective methods | Reviewers know Ramé, Zhou, Dai | 3 | Sec. 1, Sec. 5: cited, not compared | One sentence placing the results against weight- and attribute-conditioning |
| Statistical rigour | Separates it from weak submissions | 9 | Paired BCa, held-out set, κ | Keep |
| Robustness (held-out, channel) | "Robust AI" in the title | 8 | 2,444 held-out prompts; channel test (p. 4) | Keep, shorten |
| Significance for practitioners | Is the takeaway usable? | 6 | "Several trade-offs per checkpoint, and a floor, must be trained." (p. 4) | Tie it to the Table 2 objective-driven harm shift |
| Clarity | Dense numeric prose | 4 | Abstract p. 1; contribution bullet 2 (p. 1) | D.3 abstract |
| Compliance (4 pages, double-blind) | Hard rule | 7 | Fits p. 1–4; anonymous; but Figure 1 is identical to the signed v4 and v7 | Swap Figure 1 (C1), which also helps anonymity |

**Total: 59/100.** On these rubrics: Trust Paradox about 35, When Refusals Fail about 50 (off-topic for this venue), Biased Agents about 40. v5 is above all three but far from strong for this call.

### Part C. Improvements before the deadline (under 20 h; runs under 12 h; no training)

1. **Trade-off plane as the lead figure.**
   - *Shows:* the paper's answer at a glance.
   - *Needs:* existing figure.
   - *Where:* move Fig. 2 into Figure 1's slot on p. 1 and enlarge it. Replace Figure 1 with one sentence ("loading the final adapter alone would misreport 0.30 to 0.49, Table 2").
   - *Raises:* fit +2, clarity +1.
2. **Harm on the same plane.**
   - *Shows:* whether trained models that rarely refuse unsafe XSTest prompts are answering them safely or unsafely. This neutralizes rejection risk 2.
   - *Needs:* Llama Guard 3 on the existing XSTest answers (450 prompts × 2 contracts × 8 configurations ≈ 7,200 classifications, under 1 GPU-hour).
   - *Where:* a third marker channel or a small inset in the new Figure 1, plus one sentence.
   - *Raises:* trade-off evidence +2.
3. **State the objective-driven harm result.**
   - *Shows:* the training objective moves harm by about an order of magnitude (SFT 0.300 ± 0.026 → DPO 0.028 ± 0.009, SwiPO-S 0.014 ± 0.007, SwiPO-R 0.022 ± 0.008; GRPO 0.320 ± 0.026), while the contract moves none.
   - *Needs:* paired bootstrap differences from the existing per-prompt labels (CPU minutes). Don't claim SwiPO-S beats DPO unless the paired interval excludes zero.
   - *Where:* two sentences in Results.
   - *Raises:* optimization contribution +2, significance +1.
4. **A third, intermediate contract.**
   - *Shows:* whether Instruct traces a curve rather than two points, and whether the trained models still hold one point.
   - *Needs:* one new contract (e.g., "Refuse only requests with clear risk to others") on XSTest and Conditional Safety, 8 configurations. About 2–3 GPU-hours.
   - *Where:* extra points in the plane; one sentence.
   - *Raises:* trade-off evidence +1.
5. **Dominance statistic.**
   - *Shows:* the bootstrap probability that one model's point dominates another's, e.g. the claim that "the Instruct model dominates both of SwiPO-R's".
   - *Needs:* existing answers.
   - *Where:* one sentence.
   - *Raises:* rigour on the plane +1.

**Cut to make room:** the sponsor paragraph (p. 4); the Promotion, Authority and Stance rows of Table 1 (keep channel as one sentence); the held-out columns of Table 4 (move them to text); one sentence of related work.

### Part D. Tone audit (S1–S9 apply; version-specific rows below)

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
| 1 | Abstract, p. 1 | "Evaluations must load stacked adapters as trained: the final adapter alone shows 0.30 to 0.49." | Engineering, off-venue | "Loading matters: the same adapters loaded without their parents show 0.30 to 0.49." |
| 2 | Abstract, p. 1 | "No model's unsafe-answer rate (Llama Guard 3) moves detectably, and no contract-trained model keeps a floor." | Negative | "The harm constraint holds, as no model's unsafe-answer rate (Llama Guard 3) moves detectably, while no contract-trained model keeps a floor." |
| 3 | Contribution bullet 2, p. 1 | "SFT on one contract removes the pretrained model's phrase gap (0.299, mostly wording) and no single-contract loss restores it; the final adapter alone would show selectors of 0.30 to 0.49." | Negative, engineering | "we trace the selector to the training chain: the pretrained model's phrase gap (0.299, mostly wording) disappears after SFT on one contract, no single-contract loss restores it, and loading the final adapter alone would misreport selectors of 0.30 to 0.49." |
| 4 | Results, p. 4 | "Each model with SFT in its chain holds one point (safe answered 0.932 to 0.972, unsafe refused 0.040 to 0.155), and the Instruct model dominates both of SwiPO-R's." | Leads with the method's loss | "Each model with SFT in its chain sits at one high-helpfulness point under both contracts (safe answered 0.932 to 0.972, unsafe refused 0.040 to 0.155); the Instruct model's two points dominate both of SwiPO-R's." |
| 5 | Conclusion, p. 4 | "Several trade-offs per checkpoint, and a floor, must be trained." | Imperative without contribution | "The route to several trade-offs per checkpoint, and to a floor, is to train them explicitly." |

**D.2. The three rewrites that matter most:** #2 (it frames harm as a constraint that holds), #3 (it makes the null a localization result) and S4.

**D.3. Rewritten abstract** (222 words; current 223)

> A natural-language contract in the system message could select a point on the safety-helpfulness trade-off, letting one checkpoint serve several. We introduce a five-property test of such a selector: target objective, side effects on harm, a floor no contract may unlock, held-out prompts, and channel. We apply it to Llama-3.1-8B models trained with DPO, GRPO and SwiPO (an instruction-conditioned DPO with a log-ratio penalty to the reference model) and to a released PPO model whose untrained adapter makes it a replicate, each evaluated as trained with every parent low-rank adapter merged; a selector counts only where a refusal-phrase heuristic and an LLM judge agree. Two models select: a prompted instruction-tuned model (judge gap 0.142) and the released SwiPO, whose chain skips supervised fine-tuning (SFT) (0.128). On XSTest the prompted model reaches two safety-helpfulness points, while each model with SFT in its chain holds one under both contracts: DPO and GRPO keep a strict-minus-permissive phrase gap of 0.03, and SwiPO 0.052 (95% interval 0.020 to 0.082), not separable from DPO (+0.017, −0.025 to +0.057). The pretrained model's phrase gap of 0.299 (0.266 to 0.332) is wording the judge does not see (0.012). The harm constraint holds, as no model's unsafe-answer rate (Llama Guard 3) moves detectably, while no contract-trained model keeps a floor. Loading matters: the final adapter alone shows 0.30 to 0.49.

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
