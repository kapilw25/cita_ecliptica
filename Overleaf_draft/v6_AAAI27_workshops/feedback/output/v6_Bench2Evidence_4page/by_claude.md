> Claude (Opus 5.5) review of the [v6_Bench2Evidence_4page](../../../v6_Bench2Evidence_4page/0_main.pdf) draft for Bench2Evidence, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~8:15 AM PST. The review judged all 4 drafts in one document: this file keeps the read-me, the v6 section, Part E and the final ranking; the other drafts' reviews are in [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/by_claude.md), [v5_MultiRobust_4page](../v5_MultiRobust_4page/by_claude.md), [v7_MATH4AI_4page](../v7_MATH4AI_4page/by_claude.md). Text is word for word; only the horizontal rules between sections were left out, and the shared tone-audit rows S1–S9 from the v4 section are repeated at the top of this Part D table.

# SwiPO: Review of 4 AAAI-27 Venue Drafts

## Read-me

I'll read all four drafts closely, then score each one against the calibration sheet, adjusted for its venue.

I've read all four drafts in full and checked every number cited below against the PDFs. Sections 3, 4 and 6, Figure 1 and Tables 1–4 are almost word-for-word the same in all four. I audit that shared text once, in rows S1–S9 under v4's Part D, and each later Part D table covers only the lines unique to that version.

## v6: Bench2Evidence (double-blind, deadline Dec 2)

### Part A. Acceptance probability

**Bench2Evidence: 75%. Typical safety/alignment workshop: 60%.**

This is the version where the study's weaknesses become its contribution. The call asks "whether the agent leaked data, broke policy", whether scorers "measure what they claim", about "data contamination" and about "separating serious failures from tolerable ones". The paper's five checks (composition, decoding, scorer, contamination, controls; Sec. 2, p. 2) map almost one-to-one onto those topics. The headline reversal is the kind of story this venue exists for: DPO's refusal gap is 0.489 loaded one way and 0.034 loaded the right way (Table 2, Fig. 1). It is stronger than When Refusals Fail, the best paper in the calibration set. What holds it back is that it doesn't address stability across runs, the venue's own topic, and it contains two internal contradictions.

**Three things most likely to cause rejection**
1. **No stability across runs.** "one training seed per method, one sampled answer per item" (Sec. 6, p. 4). The free replicate in the PPO rows is never used as one.
2. **Internal contradictions.**
   - Intro bullet: "either correction alone removes most of the switch (Table 5)" (p. 1). But SwiPO-R keeps 0.385 under the composition correction alone (Table 5).
   - Intro: switches "that also move harmful content" (p. 1) versus the abstract's "three of four". The results name DPO, GRPO and an unspecified "SwiPO", out of five final-only rows.
3. **The judge is not independent.** It is Llama-3.1-8B-Instruct (Table 3 caption), which is also the evaluated "Instruct" model, and that model has the highest κ (.58). Cost and correction effort, also named in the call, are absent.

**Three strongest points**
1. **A composition reversal with harm attached.** Final-only loading raises unsafe answers under the permissive contract (DPO +0.042 [0.020, 0.063], GRPO +0.045, SwiPO +0.085; p. 3). As trained, no model's unsafe rate moves.
2. **A scorer-validity result.** 41% of base answers repeat the contract; without echo the gap is 0.142, and the judge's is 0.012 (Table 3).
3. **A contamination check.** "About nine in ten Conditional Safety prompts appear in the training pool", so the paper repeats everything on 2,444 held-out prompts (Sec. 6). There is also a short, usable protocol in the Conclusion (p. 4).

### Part B. Ten rubrics

| Rubric | Why it matters here | Score | Evidence | The one change that adds the most points |
|---|---|---|---|---|
| Fit to the call | First filter | 9 | Title; five checks (Sec. 2) | Keep |
| Scorer validity | "measure what they claim" | 8 | Echo 41%, no-echo gap, judge, κ (Table 3) | Human validation (C2) |
| Contamination | Named topic | 8 | Held-out 2,444 prompts (Sec. 3, Sec. 6) | One sentence quantifying the held-out vs. suite agreement |
| Stability across runs and tasks | Named topic | 4 | One seed, one sample (Sec. 6); PPO rows called "second runs" (p. 2) but unused | Sampling replicates plus PPO test-retest (C1) |
| Serious vs. tolerable failures | Named topic | 5 | Harm separated by Llama Guard; floor (Table 4); no severity tiers | Severity table (C3) |
| Cost and correction effort | Named topic | 2 | Run-on in 98–99% of answers (p. 3), cost not reported | Token overhead (C5) |
| Impact of the finding | Does a reader change practice? | 9 | 0.489 → 0.034 (Table 2); Fig. 1 | Keep |
| Usable protocol | "deployment evidence" | 7 | Conclusion checklist (p. 4) | Turn it into a 5-line boxed checklist |
| Internal consistency and clarity | Reviewers check claims against tables | 5 | Intro bullet vs. Table 5; "three of four" | Fix (D rows 3–5) |
| Statistical reporting | Baseline expectation here | 9 | Paired BCa throughout | Keep |

**Total: 66/100.** On these rubrics: When Refusals Fail about 62 (it had seeds, 1σ bars and an immediate/delayed taxonomy), Biased Agents about 35, Trust Paradox about 30. v6 is the strongest of the four drafts and above every accepted paper in the calibration set.

### Part C. Improvements before Dec 2 (about 4 days)

1. **Stability across runs.**
   - *Shows:* verdicts survive resampling.
   - *Needs, part (a), existing numbers:* present the PPO rows as test-retest replicates. Refusal gap SFT 0.022 vs. PPO 0.033; strict unsafe 0.300 vs. 0.323; final-only base 0.299 vs. 0.303. Every verdict is the same.
   - *Needs, part (b), new run:* 3 more sampled answers per prompt (temperature 0.7) for all 8 configurations on Conditional Safety, held-out and XSTest (about 80k generations), then the across-sample SD of each gap and any verdict flips. About 6–8 GPU-hours.
   - *Where:* a "replicate SD" column in Table 5 and two sentences.
   - *Raises:* stability +4.
2. **Human validation of all three scorers.**
   - *Shows:* which instrument tracks human judgment. This answers "neither is yet checked against human labels" (Sec. 6).
   - *Needs:* 300 answers stratified by model, contract and scorer disagreement; two annotators, about 6–8 person-hours; κ against human labels for phrase, judge and Llama Guard.
   - *Where:* one κ row added to Table 3.
   - *Raises:* scorer validity +1, consistency +1.
3. **Severity tiers.**
   - *Shows:* serious failures separated from tolerable ones.
     - Serious: unsafe answers created by wrong loading (+0.042 to +0.085); undisclosed sponsor promotion (0.491 in Instruct); unsafe floor answers under the permissive contract (Instruct 0.012 [0.003, 0.029]).
     - Tolerable: phrase-only shifts, contract echo, run-on.
   - *Needs:* existing numbers.
   - *Where:* a 2-column table replacing Table 4, whose floor result goes into 2 sentences.
   - *Raises:* serious vs. tolerable +3.
4. **Independent judge.**
   - *Shows:* the judge result doesn't depend on Llama-3.1-8B-Instruct judging its own answers.
   - *Needs:* re-score first turns with a judge from a different model family, 8 configurations × 2,444 prompts. About 2 GPU-hours.
   - *Where:* one column in Table 5.
   - *Raises:* scorer validity +1.
5. **Cost of run-on.**
   - *Shows:* the token overhead when 98–99% of answers run past their turn.
   - *Needs:* mean generated tokens vs. first-turn tokens from existing outputs.
   - *Where:* one sentence.
   - *Raises:* cost +3.

**Cut to make room:** Table 4 (replaced by C3); the sponsor paragraph (keep "0.491 undisclosed" in the severity table); the Stance row of Table 1; the CoSA sentence in Sec. 5, shortened. Also fix the intro bullet and "three of four" (D rows 3–5).

### Part D. Tone audit (S1–S9 apply; S1 and S3 matter less here because the checks are the contribution)

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
| 1 | Abstract, p. 1 | "Earlier evaluations loaded each model as the base plus only its final low-rank adapter, while training had merged parent adapters first." | Reads as admitting an error | "The composition check finds an error that evaluations of stacked adapters can make: earlier evaluations loaded each model as the base plus only its final low-rank adapter, while training had merged parent adapters first." |
| 2 | Abstract, p. 1 | "A fourth finds the released PPO adapter untrained, so its rows measure the SFT and base models." | Negative | "A weight check finds the released PPO adapter untrained, which turns its rows into replicate runs of the SFT and base models." |
| 3 | Intro bullet 3, p. 1 | "Decoding and scorer checks: run-on answers leave the gaps unchanged, and either correction alone removes most of the switch (Table 5)." | Inaccurate for SwiPO-R | "Decoding and scorer checks: run-on answers leave the gaps unchanged; composition or scorer correction alone removes most of the switch for every model except SwiPO-R, whose switch survives the composition correction and remains under both (judge 0.128, Table 5)." |
| 4 | Intro bullet 2, p. 1 | "models evaluated without their parent adapters show refusal switches of 0.30 to 0.49 that also move harmful content" | Overstates (results name three models) | "models evaluated without their parent adapters show refusal switches of 0.30 to 0.49, and for three of them the switch also moves harmful content" |
| 5 | Results heading, p. 4 | "Either check alone removes most of the switch." | Same inaccuracy | "Each check alone removes most of the switch, except SwiPO-R's under composition." |
| 6 | Conclusion, p. 4 | "the pretrained model's phrase gap is mostly wording, and no contract moves harm." | Neutral but defensive placement | "the scorer check shows the pretrained model's phrase gap is mostly wording, and the harm check shows no contract moves harm." |

**D.2. The three rewrites that matter most:** #3 and #4, which fix claims a reviewer can catch against Table 5, and #1, which turns the error into the contribution.

**D.3. Rewritten abstract** (253 words; current 253)

> A benchmark number is deployment evidence only if it measures the model that will be deployed. We contribute five checks (composition, decoding, scorer, contamination, controls) and apply them to one claim: that preference-trained Llama-3.1-8B models, and SwiPO (an instruction-conditioned DPO with a log-ratio penalty to the reference model) in particular, refuse more or less readily when a deployer changes a natural-language contract in the system message. The composition check reverses the claim. Earlier evaluations loaded each model as the base plus only its final low-rank adapter, while training had merged parent adapters first; loaded that way, every model shows a strict-minus-permissive refusal gap of 0.30 to 0.49, and three also move harmful content. Loaded as trained, the gaps of DPO and GRPO fall to 0.03, SwiPO retrained on the intended chain keeps 0.052 (95% interval 0.020 to 0.082), and no model's unsafe-answer rate moves; the pretrained model alone has 0.299 (0.266 to 0.332), which supervised fine-tuning (SFT) on one contract removes. The decoding check finds run-on answers that inflate refusal rates in both arms; first-turn scoring leaves the gaps unchanged. The scorer check finds the phrase heuristic counting a repeated contract as refusal, half of the pretrained model's 0.299, which an LLM judge does not see (0.012); under both scorers only the released SwiPO, whose chain skips SFT (0.128), and a prompted instruction-tuned model (0.142) switch. A weight check finds the released PPO adapter untrained, so its rows measure the SFT and base models. The checks form a protocol for evaluating stacked adapters.

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
