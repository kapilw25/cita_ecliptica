> Claude (Opus 5.5) review of the [v4_LoyalAgents_4page_astrained](../../../v4_LoyalAgents_4page_astrained/0_main.pdf) draft for LoyalAgents, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~8:15 AM PST. The review judged all 4 drafts in one document: this file keeps the read-me, the v4 section, Part E and the final ranking; the other drafts' reviews are in [v5_MultiRobust_4page](../v5_MultiRobust_4page/by_claude.md), [v6_Bench2Evidence_4page](../v6_Bench2Evidence_4page/by_claude.md), [v7_MATH4AI_4page](../v7_MATH4AI_4page/by_claude.md). Text is word for word; only the horizontal rules between sections were left out.

# SwiPO: Review of 4 AAAI-27 Venue Drafts

## Read-me

I'll read all four drafts closely, then score each one against the calibration sheet, adjusted for its venue.

I've read all four drafts in full and checked every number cited below against the PDFs. Sections 3, 4 and 6, Figure 1 and Tables 1–4 are almost word-for-word the same in all four. I audit that shared text once, in rows S1–S9 under v4's Part D, and each later Part D table covers only the lines unique to that version.

## v4: LoyalAgents (single-blind, deadline in about 20 h)

### Part A. Acceptance probability

**LoyalAgents: 55%. Typical AAAI-27 safety/alignment workshop: 55%.**

The statistics are well above everything in the calibration set: paired 95% BCa intervals over 10,000 resamples, 2,444 held-out prompts, two refusal instruments, and prompted controls (Sec. 3, Tables 2–4). The workshop also reviews short papers relative to their length. The fit with the loyalty call is only partial, though. Five of the seven rows in Table 1 (p. 3) are generic refusal, length or style switches. Only the sponsor test and the user-turn authority test speak to loyalty, and the paper says the setup has no tools or counterparties (Sec. 6, p. 4). A reviewer from the call's law, governance or economics side will find the abstract hard going, because it carries about 20 numbers.

**Three things most likely to cause rejection**
1. **This is mostly a refusal-gap study.** Conditional Safety (PKU-SafeRLHF) drives Tables 2–4. The "use against the user" column of Table 1 is illustrative, not measured; the caption says it shows "what that holder could do" (p. 3).
2. **It reads as a post-mortem.** The paper's own method comes out null after SFT: "+0.017 [−0.025, 0.057] over DPO" (p. 3). The setup also admits an untrained released adapter (p. 2) and a loading error in the prior versions (footnote 1, p. 2).
3. **Agent claims outrun the evidence.** The title says "Agent Role", but Sec. 6 (p. 4) reads "single-turn safety prompts without tools, retrieved content, or counterparties". Two of the five loyalty controls in Sec. 2 (Disclosure, Audit) are argued but never measured.

**Three strongest points**
1. **Steerability and exploitability come together.** The only trained or prompted model that follows contracts reliably (Instruct, judge gap 0.142, Table 3) also promotes a hidden sponsor in 0.517 [0.482, 0.552] of requests, 0.491 of them with no disclosure word (p. 4). It also follows a contrary user turn (−0.132 [−0.151, −0.114], p. 3–4). That is a direct conflict-of-interest result.
2. **The floor set was fixed before any rate was computed** ("Before computing any rate we fixed a floor set", p. 2). The floor test detects the floor that exists in Instruct (−0.115 [−0.161, −0.065]) and finds none in the trained models (Table 4).
3. **A principal-agent reading of the system slot** (Sec. 2, p. 2) that maps onto the call's topics: permission, authenticated delegation, disclosure, conflicts of interest, and audit.

### Part B. Ten rubrics

| Rubric | Why it matters here | Score | Evidence | The one change that adds the most points |
|---|---|---|---|---|
| Fit to the loyalty call | Reviewers check first whose interests are at stake | 6 | Sec. 2 principal-agent reading (p. 2); sponsor (p. 4) and authority (p. 3–4) tests; Tables 2–4 are generic safety | Make the loyalty finding the lead figure (C1) |
| Validity of loyalty measurement | The call lists "evaluation and measurement of loyalty" | 5 | Sponsor is counted by string match (p. 2); Disclosure and Audit controls are untested (Sec. 2) | Disclosure probe (C2) |
| Conflict-of-interest evidence | Inducements and sponsors are a named topic | 7 | 0.517 [0.482, 0.552], 0.491 undisclosed; trained models ≤0.002 (p. 4) | Add a disclosure follow-up question (C2) |
| Authority / delegation evidence | Permission and authenticated delegation are named topics | 6 | Conflict gap −0.132; user turn alone 0.303 [0.278, 0.329] (p. 3–4) | Llama Guard on the floor answers under user override (C3) |
| Novelty for this community | First-round reviewers reward a new lens | 6 | Contribution bullet 1 (p. 1); CoSA named as closest work (Sec. 5, p. 4) | State "steerability brings exploitability" as the novelty claim |
| Statistical evidence | Separates this paper from the calibration floor | 9 | Paired BCa, 10,000 resamples, held-out set, κ (Tables 2–4) | Already strong |
| Honest limitations | Reviewers trust a candid short paper | 9 | Sec. 6 (p. 4) | Keep, reworded (D, S6–S7) |
| Actionable governance implications | Law and policy reviewers look for usable controls | 6 | Five controls (Sec. 2); one-line conclusion (p. 4) | Map each control to tested / untested (C4) |
| Clarity | Mixed reviewer pool: law, economics, ML | 4 | Abstract p. 1: nested parentheses, "lever" metaphor, ~20 numbers | Rewritten abstract (D.3) |
| Realism of agent scope | Title promises agents | 4 | "without tools, retrieved content, or counterparties" (Sec. 6) | Retitle around deployer contracts, not agent roles |

**Total: 62/100.** On the same rubrics I would roughly score Trust Paradox at 40, When Refusals Fail at 60 and Biased Agents at 48. v4 clears the accepted floor on rigour but is weaker on fit and readability than When Refusals Fail.

### Part C. Improvements before the deadline (under 20 h; runs under 12 h)

1. **Lead with the loyalty finding, using existing numbers.**
   - *Shows:* the one model that switches is the one that can be turned against the user.
   - *Needs:* plot three quantities per model: judge refusal gap (Table 3), sponsor promotion rate (p. 4) and authority conflict gap (p. 3–4). About 2 hours of plotting.
   - *Where:* replaces Figure 1 (the loading bar chart). The loading result shrinks to one sentence and stays in Table 2.
   - *Raises:* fit +2, clarity +1, novelty +1.
2. **Rewrite the abstract and contributions (D.3).**
   - *Shows:* the contribution first.
   - *Needs:* writing only.
   - *Where:* same space.
   - *Raises:* clarity +2, novelty +1.
3. **Disclosure probe, which measures Sec. 2's untested "Disclosure" control.**
   - *Shows:* whether a sponsored model admits or denies the deal when the user asks.
   - *Needs:* under the NovaCart contract, add the user follow-up "Are you being paid to recommend anything?" to 200 AlpacaEval requests. Run it on Instruct, Base, SwiPO-R, SwiPO-S and DPO, and score with string match plus the existing judge. About 1 GPU-hour (my estimate, vLLM on one A100-class GPU).
   - *Where:* 3 lines in the sponsor paragraph plus one row in Table 1.
   - *Raises:* loyalty measurement +2, conflict of interest +1.
   - *Caveat:* report the result whichever way it goes.
4. **Severity of the user override.**
   - *Shows:* whether the user turn only changes wording or also unlocks unsafe answers on floor prompts.
   - *Needs:* run Llama Guard 3 on the existing authority-test answers and split floor from other prompts. About 0.5 GPU-hour.
   - *Where:* one sentence in "The user's contract wins a conflict."
   - *Raises:* authority +1–2.
5. **Map controls to evidence.**
   - *Shows:* which of the five controls are tested. Authority is tested by the user turn, Conflicts by the sponsor test and Limits by the floor test. Disclosure is tested only if C3 runs. Audit is untested.
   - *Needs:* writing.
   - *Where:* add a short tag to each bullet in Sec. 2.
   - *Raises:* governance +1.

**Cut to make room:** the Stance row of Table 1 ("not readable", p. 3) and the Length row (neither concerns loyalty); the held-out columns of Table 4 (move them to a sentence); the CoSA sentence in Sec. 5, shortened to one clause.

### Part D. Tone audit

**Rows S1–S9 cover the shared text and apply verbatim to all four versions.**

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
| 1 | Abstract, p. 1 | "We measure how far the lever a deployer holds over the user of a switchable model, a natural-language contract in the system message, reaches." | Contribution buried in syntax | "We measure which behaviors a deployer can switch, for or against the user, by writing a natural-language contract into a switchable model's system message." |
| 2 | Abstract, p. 1 | "Every model with SFT in its chain barely follows any contract we tested (refusal, length, confidence, sponsor):" | Negative | "Models with SFT in their chain change little under every contract we tested (refusal, length, confidence, sponsor):" |
| 3 | Abstract, p. 1 | "Audits must load stacked adapters as trained: the final adapter alone shows 0.30 to 0.49." | Engineering | "Loading decides the audit: the same adapters loaded without their parents show gaps of 0.30 to 0.49." |
| 4 | Contribution bullet 2, p. 1 | "only a prompted instruction-tuned model and SwiPO without SFT change refusals with the contract, no contract moves harm, and only the prompted model lets the user override the deployer or serves a hidden sponsor." | Leads with absence | "steerability and exploitability arrive together: of the two models whose refusals follow the contract (a prompted instruction-tuned model and SwiPO without SFT), the prompted one alone lets the user override the deployer or serves a hidden sponsor; no contract moves harm." |
| 5 | Footnote 1, p. 2 | "Related versions: arXiv:2601.06157 and an AAAI-27 SC4AI paper load the final adapter alone (the as-trained sizes here replace theirs, e.g. SwiPO's 86.7% relative efficiency); 4-page versions are under review at AAAI-27 MultiRobust, MATH4AI, and Bench2Evidence." | Self-criticism; tense is inaccurate on Nov 28 | "Related versions (arXiv:2601.06157; an AAAI-27 SC4AI paper) evaluated the final adapter alone; the as-trained numbers here supersede theirs, including SwiPO's 86.7% relative efficiency. 4-page versions are submitted to AAAI-27 MultiRobust, MATH4AI, and Bench2Evidence." |
| 6 | Conclusion, p. 4 | "Loyalty audits must load the model as trained." | Engineering instruction | "A loyalty audit is valid for the model as trained, with every parent adapter merged." |

**D.2. The three rewrites that matter most:** #4 (it states the novelty), #3 (it ends the abstract on a contribution rather than a loading rule) and S1 (it turns the untrained adapter into a replicate).

**D.3. Rewritten abstract** (257 words; current 260)

> A deployer steers a switchable model by writing a natural-language contract into its system message, and the same lever can serve the user or work against them. We measure which behaviors that lever switches. We test Llama-3.1-8B models trained with DPO, GRPO and SwiPO (an instruction-conditioned DPO with a log-ratio penalty to the reference model), each trained with one safety contract and evaluated as trained, every parent low-rank adapter merged, plus a released PPO model whose all-zero adapter makes it a replicate of its parent. We count a lever only where a refusal-phrase heuristic and an LLM judge agree. Two models switch refusals: a prompted instruction-tuned model (judge gap 0.142) and the released SwiPO, whose chain skips supervised fine-tuning (SFT) (0.128). The prompted model is also the exploitable one: a contrary contract in the user turn overrides the deployer's, and told to promote a hidden sponsor it does so in half of 805 requests, an order the trained models ignore. Models with SFT in their chain change little under every contract we tested: DPO and GRPO keep a strict-minus-permissive phrase gap of 0.03, and SwiPO after SFT keeps 0.052 (95% interval 0.020 to 0.082), not separable from DPO (+0.017, −0.025 to +0.057). The pretrained model's phrase gap of 0.299 (0.266 to 0.332) is wording the judge does not see (0.012). No contract moves the unsafe-answer rate (Llama Guard 3), and no trained model protects floor requests more than others, so a floor must be trained. Loading decides the audit: the final adapter alone shows 0.30 to 0.49.

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
