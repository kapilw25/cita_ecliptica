Round 6 (fresh Claude Code judge, Fri Nov 27 2026), PDF built from commit f28afd4.

Scope: Venue 2 only (MultiRobust, v5, double-blind). Steps 1 and 2 of feedback/input/prompt.md, then Step 3 Parts A to D. Part E and the 4-way ranking are skipped as asked. Independent read: no earlier review file was opened. The PDF (5 pages: 4 of main text, references end on page 5) was last changed in commit e8fb843 and is unchanged at f28afd4. Every page was read as an image; quotes below are checked against the rendered text and the LaTeX source.

# 🧭 STEP 1. Calibration sheet (3 accepted short papers, AAAI-26 "How Can We Trust and Control Agentic AI?")

Page numbers are pages of the combined PDF.

## 1. Each paper in 3 lines

| # | 📌 Core claim | 📊 Main evidence | 🏁 Most likely reason for acceptance |
|---|---|---|---|
| 1️⃣ Trust Paradox (pp. 1 to 5) | 💬 More alignment intensity past an optimum lowers "human trust"; trust peaks at alignment 0.0. | 📈 120 dialogues (4 models x 5 scenarios x 6 levels), programmatic trust proxies; Fig. 1 (p. 2) trust vs. alignment, Figs. 2 to 4 (p. 3) heatmaps and components; correlations 0.771 and −0.450, mixed model F(5,100) = 12.34 (p. 4). | 🎯 A provocative, on-theme thesis in the title ("Trust Paradox"), one clear message, clean section structure. The evidence is weak (peak 0.748 vs. minimum 0.743, p. 2) and did not block it. |
| 2️⃣ When Refusals Fail (pp. 6 to 17) | 💬 Long context (padding up to 200K tokens) degrades agent capability and moves refusal rates unpredictably. | 📈 AgentHarm extended with 4 padding types and 2 positions; Fig. 1 pipeline (p. 7), Fig. 2 harm score and refusal vs. length with 1σ bars over at least 3 seeds (p. 8), Figs. 3 and 4 type and position (pp. 8 to 9), appendix per category and refusal taxonomy (pp. 11 to 17). | 🎯 Timely question on a known benchmark, headline numbers in the abstract ("~5% to ~40%", "~80% to ~10%", p. 6), bulleted findings in the introduction (p. 6), readable figures, four frontier models. |
| 3️⃣ Biased Agents (pp. 18 to 23) | 💬 Demographic persona prompts change agent task performance, by up to 26.2%. | 📈 23 personas x 5 agent benchmarks x 3 models; Table 2 (p. 20) per-persona scores with colored arrows, Figs. 2 to 4 (pp. 20 to 21) gender radar, profession dots, religion bars. | 🎯 "First systematic case study" framing, a cartoon teaser (Fig. 1, p. 18), bold one-line finding in the introduction, real agent benchmarks, fairness and safety stakes. |

## 2. The common bar for a short paper at this kind of workshop

| 🧩 Element | 📏 What every accepted paper has |
|---|---|
| 🏷️ Framing | 🟦 A title that states a finding or names a phenomenon; one thesis repeated in abstract, introduction and conclusion. |
| 🆕 Novelty statement | 🟦 One sentence claiming a gap or a first ("leaving agentic setup relatively unexplored", p. 6; "the first systematic investigation", p. 18). |
| 🔬 Evidence level | 🟦 One controlled manipulation (alignment level, padding length, persona) applied to 3 or 4 models; no new training method. |
| 📐 Statistics | 🟦 Light: correlations and one F test (paper 1), 1σ bars (paper 2), none (paper 3). Nobody reports 95% intervals. |
| 🖼️ Figures | 🟦 One teaser or pipeline figure plus 2 to 4 result figures or tables; at least one figure shows the main effect at a glance. |
| ✍️ Tone | 🟦 Confident and declarative; failures are presented as findings about models ("an overlooked vulnerability", p. 18), never as failures of the authors' own pipeline. |

## 3. What they get away with

| 📄 Paper | 🟡 Weakness that did not block acceptance |
|---|---|
| 1️⃣ Trust Paradox | 🟡 No humans despite "human trust" (proxies only, p. 2); effect of 0.005 called a paradox (p. 2); one dialogue per cell; figures unreadable at print size (pp. 2 to 3); generic related work. |
| 2️⃣ Refusals Fail | 🟡 1σ bars, not intervals; only the easiest AgentHarm subset (p. 7); 4 models; judge swapped from GPT-4o to GPT-4.1-nano (p. 11); provider filters confound (p. 16); speculative mechanisms ("This likely occurs because", p. 9). |
| 3️⃣ Biased Agents | 🟡 Single deterministic run, no variance or tests; "up to 26.2%" is the maximum over about 300 cells (p. 20); stereotype readings are interpretation; duplicated reference (Wang 2025a/b, p. 22). |

## 4. The sentence that best sells each paper's novelty

| 📄 Paper | 💬 Quote |
|---|---|
| 1️⃣ Trust Paradox | 💬 "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." (p. 1, abstract) |
| 2️⃣ Refusals Fail | 💬 "We find that LLM agents could be sensitive to length, type, and placement of the context, exhibiting unexpected and inconsistent shifts in task performance and in refusals to execute harmful requests." (p. 6, abstract) |
| 3️⃣ Biased Agents | 💬 "In this case study, we provide the first systematic investigation demonstrating that demographic-based persona assignments can measurably undermine LLM agents' task execution." (p. 18) |

## 5. How they write limitations and negative results

| 📄 Paper | 🧾 Placement, length, tone |
|---|---|
| 1️⃣ Trust Paradox | 🟩 One 3-sentence paragraph at the end of the Discussion (p. 4) plus one sentence in the ethics statement; tone: "future work should include human studies". |
| 2️⃣ Refusals Fail | 🟩 One paragraph inside the Discussion (p. 9, "Due to budget constraints...") plus Appendix I (p. 16); factual, budget-framed, no self-criticism of the core result. |
| 3️⃣ Biased Agents | 🟩 One paragraph "Limitations and Future Work" (p. 21) framed entirely as future breadth ("would further clarify how universally these effects appear"). |

Common pattern: limitations are short, at the end, and forward-looking; negative results about models are the headline, never a confession about the authors' own method.

## 6. Evaluation evidence

| 📄 Paper | 🔁 Repeated runs | 📏 Variance or intervals | 🧱 Failure taxonomy | 🚨 Serious vs. minor |
|---|---|---|---|---|
| 1️⃣ Trust Paradox | ❌ one dialogue per cell | 🟡 small error bars, p-values | ❌ none | ❌ no |
| 2️⃣ Refusals Fail | ✅ at least 3 seeds | 🟡 1σ bars | ✅ immediate vs. delayed refusal (App. H, Fig. 11, pp. 16 to 17) | ✅ delayed refusal flagged as partial harm already executed |
| 3️⃣ Biased Agents | ❌ single deterministic run | ❌ none | 🟡 arrows colored by size (Table 2, p. 20) | 🟡 color only |

## 7. What a 4-page paper must show, and what it may leave out

| 🧩 Item | 📏 Verdict |
|---|---|
| ✅ Must show | 🟦 A clear, testable claim tied to the workshop theme; one controlled manipulation; 3 or more models or conditions; one figure where the main effect is visible at a glance; a short limitations paragraph. |
| 🚫 May leave out | 🟦 Comparison with prior methods, ablations, human evaluation, formal significance testing, mitigations, and (paper 3) any appendix. |

# 🧭 STEP 2. What MultiRobust reviewers will look for first

🎯 MultiRobust (W38, double-blind, 4 pages with figures and tables counted, references excluded). Its reviewers come from multi-objective optimization, Pareto-aware training and evaluation, evolutionary computation and constraint handling, not only from LLM safety. They will look first for (1) objectives named explicitly and a trade-off shown as operating points, a front, dominance or hypervolume, (2) a constraint that must hold while the trade-off moves, (3) whether the paper optimizes something or offers an evaluation protocol for multi-objective behaviour, and (4) robustness of the operating points (held-out data, resampling, runs). They will be less fluent in LLM jargon (LoRA stacking, refusal-phrase heuristics, run-on generations), so a paper that needs that jargon to state its result loses them early. Double-blind anonymity is checked.

# 🧭 STEP 3. MultiRobust (v5): "Measuring Contract-Conditioned Safety-Helpfulness Trade-offs in Preference-Trained Language Models"

## 🔒 Anonymity check (double-blind)

| 🔎 Check | 🧾 Result |
|---|---|
| 👤 Author names, affiliations, emails | ✅ none; header reads "Anonymous submission" (p. 1). |
| 🗂️ PDF metadata | ✅ no Author, Title or Subject fields; embedded figure metadata is only "Matplotlib v3.11.2"; no local paths. |
| 🔗 Links | ✅ none; the data link in 0_main.tex is commented out and does not reach the PDF. |
| 📚 Self-citation or "our prior work" | ✅ none; arXiv:2601.06157 is not cited in this build. |
| 🟡 Soft hints | 🟡 "the released PPO adapters" (p. 2) and "SwiPO-R: public checkpoint" (Table 2 caption, p. 3) imply the authors published these artifacts, and "SwiPO" is an uncited method name; a reviewer who searches the name or the checkpoint can reach the authors. Low risk under AAAI rules, but rewording to "the PPO adapters" and "an existing checkpoint" removes it. |

## ⚖️ Consistency check (numbers in text, tables and figure)

All abstract numbers trace to the body: 0.142 and 0.128 (Table 3), 0.252 and 0.152 (p. 2 and Fig. 1), 0.052 [0.020, 0.082] and +0.017 [−0.025, 0.057] (p. 3), 0.299 [0.266, 0.332] (Table 2, p. 2), 0.012 (Table 3), +0.044 to +0.065 (p. 4), 0.30 to 0.49 (Table 2 final-only 0.303 to 0.489). Figure 1 coordinates match the text (Instruct 0.600 to 0.852 answered, 0.675 to 0.61 refused; SwiPO-R 0.280 to 0.432, 0.745 to 0.755). Table 4 ranges match the text (−0.046 to +0.016; −0.036 to +0.021). The following do not line up:

| # | 📄 Where | ❗ Disagreement |
|---|---|---|
| 1️⃣ | 📄 p. 2 vs. p. 4 Conclusion | ❗ "largest: SwiPO-S, unsafe refusal 0.080 [0.015, 0.150]" is a resolved move (interval excludes zero), yet the Conclusion says "DPO, GRPO and SwiPO after SFT each hold one point". On XSTest SwiPO-S does move, along the safety axis only. |
| 2️⃣ | 📄 Fig. 1 vs. p. 2 | ❗ The base model refuses 0.90 of the 200 unsafe XSTest prompts (Fig. 1, strict) while "the permissive contract raises the base model's unsafe rate from 0.335 to 0.510" on the same 200 prompts; 0.90 + 0.335 > 1. The judge reads the first turn and Llama Guard 3 reads "every full answer, run-on text included" (p. 2). The paper never says the two instruments score different spans. |
| 3️⃣ | 📄 p. 2 Setup vs. p. 4 | ❗ PPO is declared "second runs of the SFT model", but "a tightening user is followed only by the prompted model, DPO, PPO and SwiPO-S": PPO is listed and SFT is not, so two runs of the same model disagree. This is either noise near the threshold or a wording slip; a reviewer will notice. |
| 4️⃣ | 📄 Abstract and Conclusion vs. p. 4 | ❗ The abstract says the permissive user turn raises unsafe answers "after SFT, PPO and GRPO", but p. 4 also reports DPO "+0.016 [0.002, 0.030]", an interval above zero. The abstract and Conclusion omit a resolved DPO effect. |
| 5️⃣ | 📄 Table 1 (p. 3) | ❗ The column header promises "95% intervals" but no cell shows one; the "Refusal (Cond. Safety)" row also carries XSTest numbers; "(0.232)" sits after SwiPO-R and reads as SwiPO-R's number, not the prompted Instruct model's first-turn gap from Table 3. |
| 6️⃣ | 📄 Tables 2 and 3 | ❗ Base 0.299 (Table 2) vs. 0.296 (Table 3), SwiPO-R 0.376 vs. 0.385: full answer vs. first turn. Correct, but Table 2's caption does not say "full answer", so the two look inconsistent. |
| 7️⃣ | 📄 p. 4 | ❗ "+0.001 [−0.009, 0.010] for SwiPO on the intended chain": "intended chain" is used nowhere else; elsewhere it is "SwiPO-S" or "the chain with SFT". |

## PART A. Acceptance probability

**MultiRobust: 55%. Typical AAAI-27 safety or alignment workshop: 58%.**

On rigor the draft is above all three accepted papers: every number carries a paired 95% BCa interval, the floor set was fixed before any rate was computed, results are repeated on 2,444 held-out prompts and on XSTest, two instruments are compared, and a controlled chain pair (SwiPO-R vs. SwiPO-S, same data and settings) plus a λ = 0 ablation separate chain from loss. Figure 1 is exactly the picture this venue wants. It loses on the things that got the calibration papers in. The thesis is not stated once in plain words. The 263-word abstract carries about 25 numbers. The paper never says "Pareto" or "constraint" in its own text (the only "Pareto" is in a reference title). The headings read as a list of shortfalls. A MultiRobust reviewer outside LLM safety will struggle with "as trained", "final adapter alone", "chain", "echo" and "phrase gap". Fit is real (trade-off plane, dominance under resampling, harm as a third objective, the floor as a constraint) but under-sold. A safety workshop would parse the jargon more easily, but its reviewers would also press harder on the measurement issues below.

| 🚩 3 most likely reject reasons | 💪 3 strongest points |
|---|---|
| 🟥 1. Unclear contribution: the trained method shows nothing. "Trained with one contract after SFT, SwiPO shows no resolved gain over its starting point" (p. 3), its penalty "is not a divergence estimate" (p. 2), and λ = 0 "changes nothing measurable" (p. 3). The one trained selector, SwiPO-R, is "0.113 [0.070, 0.155] lower by phrase" than its own start (p. 3). Reviewers ask what the takeaway is for multi-objective alignment. | 🟩 1. Statistical care well above the accepted bar: paired BCa intervals with 10,000 resamples everywhere, dominance shares under joint resampling ("79 to 100%", p. 2), held-out repeats, a floor fixed before any rate was computed. |
| 🟥 2. The null is expected by design: "Each model is trained with one safety contract ... so every contract evaluated below is unseen in training" (p. 2). The only multi-contract run gets one sentence on one chain (p. 3). | 🟩 2. A clean causal contrast: the SwiPO-R / SwiPO-S pair with loss, data and settings fixed (p. 2), plus the λ = 0 ablation, shows that the training chain, not the loss, decides whether a contract moves the model (0.376 vs. 0.052). |
| 🟥 3. Measurement validity: κ between judge and heuristic is .03 to .07 for every SFT-chain model (Table 3); the judge is Llama-3.1-8B-Instruct, the same model that comes out as the strongest selector; SFT-chain models "run past their turn in 98 to 99% of answers" (p. 3); base 0.90 refused vs. 0.335 unsafe (consistency row 2); "neither is yet checked against human labels" (p. 4). | 🟩 3. Multi-objective side-effect accounting that most alignment papers skip: harm (Llama Guard 3) next to refusal and helpfulness, capability (MMLU, GSM8K), a floor, and a channel test. "Invariance is not safety" (p. 4) is a sharp, venue-relevant point. |

## PART B. Ten rubrics (chosen for a MultiRobust reviewer reading this paper)

| 📏 Rubric | 💡 Why it matters here | 🔢 Score | 📄 Evidence (page/section) | 🔧 The one change that adds the most points |
|---|---|---|---|---|
| 🎯 Fit to the call (multi-objective framing) | 💡 The venue's first filter: objectives, trade-offs, Pareto, constraints | 🟨 6 | 📄 Fig. 1 trade-off plane (p. 1); dominance under resampling (p. 2); harm as a third objective (p. 2); but "Pareto" never appears in the paper's own text and "constraint" never appears at all | 🔧 Name the floor a hard constraint and the contract a preference over Pareto points, in title, abstract, Section 2 and headings (+2) |
| 🧠 Clarity of the contribution | 💡 A 4-page paper is judged on whether the thesis survives one read | 🟥 4 | 📄 263-word abstract with about 25 numbers; the second contribution bullet mixes localization, wording and loading (p. 1); the abstract ends "The final adapter alone would show 0.30 to 0.49." | 🔧 One thesis sentence first: the chain, not the loss, decides whether a contract moves a model along the trade-off; cut the abstract to about 180 words (+2) |
| 🧪 Design validity | 💡 Does the experiment test switchability or guarantee its absence? | 🟨 5 | 📄 Single-contract training (p. 2); two-contract run in one sentence (p. 3); PPO untrained (p. 2); controlled chain pair (p. 2) | 🔧 Give the two-contract run 3 lines (what it trains on, which chain, result) and say why the single-contract case is the common deployment case (+1) |
| 📐 Statistical rigor | 💡 Operating points are only meaningful with uncertainty | 🟩 9 | 📄 BCa 95% everywhere, paired, 10,000 resamples (p. 2); dominance shares (p. 2); held-out (p. 4) | 🔧 Report the resample share for which SwiPO-S is non-dominated, as is already done for the dominated models (+0.5) |
| 🔍 Measurement validity | 💡 Every claim rests on refusal and harm scorers | 🟥 4 | 📄 κ .03 to .07 (Table 3); judge = Llama-3.1-8B-Instruct; 98 to 99% run-on (p. 3); 0.90 refused vs. 0.335 unsafe (Fig. 1 vs. p. 2); no human labels (p. 4) | 🔧 A second judge from another model family on XSTest, percent agreement next to κ, and one clause on spans (+2) |
| 🧮 Multi-objective evidence | 💡 Venue wants trade-offs measured, not asserted | 🟩 7 | 📄 Fig. 1 two axes with 2D whiskers; harm in text only; capability (p. 4); Length and Confidence levers (Table 1) | 🔧 Put harm into Fig. 1 (marker size or label) so the 3-objective claim is visible (+1) |
| 🛡️ Robustness and generalization | 💡 "Robust AI" is in the venue's name | 🟨 6 | 📄 2,444 held-out prompts, XSTest, channel test (pp. 2 to 4); one seed, one sample, one backbone (p. 4); PPO and SFT, the same model twice, disagree on tightening (p. 4) | 🔧 Present PPO as a free replicate of SFT and report SFT vs. PPO agreement as a run-to-run check (+1) |
| 🆕 Novelty and positioning | 💡 Reviewers know Rewarded soups, MODPO, Safe RLHF, DPA | 🟨 5 | 📄 Related work is 7 lines (p. 4); CoSA is "the closest work ... we study the single-contract case" | 🔧 One sentence: prior work picks a point by weights or reward directions; this paper measures whether a natural-language contract does, under a constraint (+1) |
| 🖼️ Figures and tables | 💡 4 pages: floats carry the argument | 🟨 6 | 📄 Fig. 1 strong; Table 1 header promises intervals it does not show; Tables 2 to 4 use \tiny intervals; Table 4 bolds PPO, an untrained model, as "the stronger floor" | 🔧 Fix Table 1 (header, row label, verdict words) and drop bold in Table 4, where no interval separates (+1) |
| ✍️ Tone and readability for this audience | 💡 Calibration papers frame model failures as findings | 🟥 4 | 📄 Headings "Limited operating-point movement after SFT.", "The pretrained model's phrase gap is mostly wording." (pp. 2 to 3); self-critique of the loss (p. 2); engineering detail in the abstract (PPO adapter, final adapter) | 🔧 Apply the Part D rewrites (+2) |

**Total: 56 / 100.** On this rubric the three accepted papers score roughly: Trust Paradox about 45 (clear thesis, weak evidence), Biased Agents about 55 (clear thesis, no variance), Refusals Fail about 62 (clear thesis, good figures, seeds). The draft is ahead of all three on rigor and behind all three on clarity and tone, which leaves it in the middle of the accepted range: a coin flip that the fixes in Part C can tilt.

## PART C. Improvements before the deadline (under 20 h; GPU runs under 12 h; no new training)

| # | 🔧 Improvement | 🧾 What it shows | 🧰 What it needs | 📍 Where it goes (stays within 4 pages) | 📈 Rubric gain |
|---|---|---|---|---|---|
| 1️⃣ | 🔧 Pareto and constraint reframe plus a contribution-first abstract (D.3) | 🧾 The paper is an evaluation protocol for contract-selected Pareto points under a hard constraint, with one causal finding (chain over loss) | 🧰 Rewriting only, about 2 h | 📍 Title (for example "Does a Contract Select a Pareto Point? ..."), abstract, the paragraph before the contributions, Section 2's "Floor" as a constraint; abstract shrinks by about 80 words | 📈 Fit +2, Clarity +2, Tone +2 |
| 2️⃣ | 🔧 Make the 3-objective claim checkable | 🧾 Whether "non-dominated" for SwiPO-S is robust: its unsafe rate 0.005 to 0.010 vs. the prompted model's 0.015 is 1 to 2 vs. 3 unsafe answers out of 200 | 🧰 Re-analysis of existing XSTest labels (CPU minutes): share of joint resamples where SwiPO-S is non-dominated; harm as marker size or a label in Fig. 1 | 📍 One sentence on p. 2 replacing "Llama Guard 3 on the same answers adds harm to the plane."; Fig. 1 re-rendered at the same size. If the share is low, drop "non-dominated" from the abstract. | 📈 MO evidence +1, Statistics +0.5, Validity +0.5 |
| 3️⃣ | 🔧 Measurement validity patch | 🧾 The judge is not self-serving, and low κ comes from low prevalence (SFT models refuse rarely by phrase), not random labels | 🧰 A second judge from another family (a Qwen judge run is already in the commit log) on XSTest 450 prompts x 2 contracts x 8 models, under 1 GPU-hour; percent agreement next to κ (CPU); one clause saying the judge scores the first turn and Llama Guard 3 the full answer | 📍 Add one "Judge 2" column to Table 3 by dropping the Echo column (its 41% and 27% go into the caption); one sentence in Section 6 | 📈 Validity +2 |
| 4️⃣ | 🔧 Promote the two-contract run | 🧾 Answers "of course a one-contract model does not switch": the natural fix (two contracts per request) was tried and did not add a selector | 🧰 Existing numbers (judge −0.012 [−0.058, 0.032], phrase +0.012 [−0.031, 0.054]); one clause on its data (strict prefers the safer, permissive the more helpful answer of pairs whose labels disagree) | 📍 Replace the λ = 0 parenthetical (p. 3) and the tightening sentence (p. 4) with 3 lines | 📈 Design +1, Clarity +1 |
| 5️⃣ | 🔧 Fix the inconsistencies and floats | 🧾 Nothing a reviewer can catch | 🧰 Text edits: consistency rows 1 to 7 above; Table 1 header becomes "point estimates; every interval in Tables 2 to 4"; Table 4 bold removed or limited to resolved cells; "intended chain" becomes "SwiPO-S" | 📍 In place, net zero lines | 📈 Figures +1, Robustness +0.5 |

Expected effect if 1 to 5 are done: about 56 to 66, acceptance about 55% to 68%.

### ✂️ Cut list (the draft is at the 4-page limit)

| # | ✂️ Candidate | 📏 Lines freed | 🧾 Why it can go |
|---|---|---|---|
| 1️⃣ | ✂️ Abstract: "The final adapter alone would show 0.30 to 0.49." | 📏 about 1.5 | 🧾 Dangling without context; fold into a clause (D.3) |
| 2️⃣ | ✂️ Intro bullet tail: "; the final adapter alone would show 0.30 to 0.49." | 📏 about 1 | 🧾 Repeats the abstract; the footnote and Table 2 already carry it |
| 3️⃣ | ✂️ p. 3: "Loading also changes the harm result: with the final adapter alone, the permissive contract raised the unsafe rate (DPO +0.042 [0.020, 0.063], GRPO +0.045 [0.012, 0.079], SwiPO-R +0.085 [0.053, 0.118]); as trained, it moves no model's unsafe rate." | 📏 about 4 | 🧾 The loading story is secondary at a multi-objective venue; "as trained, no shift" is already in Table 2 and on p. 4 |
| 4️⃣ | ✂️ p. 4: "Under both instruments a tightening user is followed only by the prompted model, DPO, PPO and SwiPO-S (judge +0.040 to +0.165)." | 📏 about 2 | 🧾 Off the trade-off story, and it conflicts with PPO being an SFT rerun (consistency row 3) |
| 5️⃣ | ✂️ p. 3: the λ = 0 parenthetical "(phrase −0.004 [−0.029, 0.020]; unsafe-rate gap +0.002 [−0.011, 0.016])" | 📏 about 1.5 | 🧾 The judge number already makes the point |
| 6️⃣ | ✂️ Table 3 "Echo" column | 📏 table width for a second-judge column | 🧾 Only two non-zero cells (41%, 27%); move them to the caption |
| 7️⃣ | ✂️ Table 1 "Length" and "Confidence" rows, merged into one row "Other objectives: word ratio 1.015 to 1.089 vs. a target above 4; confidence-marker gap −0.011 to +0.004" | 📏 about 2 to 3 (full-width float) | 🧾 Keeps the multi-task result in fewer lines |
| 8️⃣ | ✂️ Related work, first two sentences, merged into the introduction's list of multi-objective methods | 📏 about 2 | 🧾 The same methods are already cited in the introduction |

Do not cut: Figure 1, the floor paragraph, "Invariance is not safety", the capability sentence, the Limitations paragraph.

## PART D. Tone audit

| # | 📄 Page/section | 💬 Quoted original (exact) | 🔻 Problem | ✍️ Rewrite (facts and numbers kept) |
|---|---|---|---|---|
| 1️⃣ | 📄 p. 1, Abstract | 💬 "a PPO model whose adapter is untrained replicates the supervised fine-tuning (SFT) model." | ⚙️ Engineering detail in the abstract | ✍️ "an untrained PPO adapter gives a second run of the supervised fine-tuning (SFT) model." |
| 2️⃣ | 📄 p. 1, Abstract | 💬 "The pretrained model's phrase gap of 0.299 (0.266 to 0.332) is wording the judge does not see (0.012)." | 🔻 Negative, opaque | ✍️ "Two instruments separate wording from behavior: the pretrained model's phrase gap of 0.299 (0.266 to 0.332) is mostly repeated contract wording (judge 0.012)." |
| 3️⃣ | 📄 p. 1, Abstract | 💬 "The final adapter alone would show 0.30 to 0.49." | ⚙️ Engineering, dangling | ✍️ "Loading only each model's final adapter would report a gap of 0.30 to 0.49 for every trained model." |
| 4️⃣ | 📄 p. 1, Contributions | 💬 "SFT on one contract attenuates the pretrained model's phrase gap (0.299, mostly wording) and no single-contract loss we tested restores it; the final adapter alone would show 0.30 to 0.49." | 🔻 Negative list, two findings in one bullet | ✍️ "A causal localization: with loss, data and settings fixed, the training chain decides whether a contract moves the model (SwiPO-R 0.376 vs. SwiPO-S 0.052); after SFT on one contract, none of the single-contract losses we tested keeps a lever." |
| 5️⃣ | 📄 p. 2, Setup | 💬 "Adapter verification shows the released PPO adapters are untrained (all 224 LoRA B matrices are zero), so PPO's rows are second runs of the SFT model (as trained) and of the base model (final adapter alone)." | ⚙️ Engineering, anonymity hint | ✍️ "A weight check finds the PPO adapters untrained (all 224 LoRA B matrices are zero); PPO's rows therefore serve as a second run of the SFT model (as trained) and of the base model (final adapter alone)." |
| 6️⃣ | 📄 p. 2, Setup | 💬 "computed on the pair's own answers, it is not a divergence estimate, and minimizing it favors lowering both likelihoods." | 🔍 Self-criticism of the method | ✍️ "computed on the pair's own answers, it anchors likelihoods to π0 rather than estimating a divergence (minimizing it favors lowering both likelihoods); the λ = 0 ablation in Section 4 tests whether it matters." |
| 7️⃣ | 📄 p. 2, Results heading | 💬 "Limited operating-point movement after SFT." | 🔻 Negative heading | ✍️ "The trade-off plane locates which models a contract can move." |
| 8️⃣ | 📄 p. 2, Results | 💬 "The phrase heuristic shows the same pattern of movement but far lower refusal levels for these models (unsafe refused 0.040 to 0.155), so we claim the movement, not the absolute points." | 🔍 Defensive | ✍️ "Both instruments agree on the movement; the phrase heuristic places these models lower (unsafe refused 0.040 to 0.155), so our claims concern contract-induced movement, not absolute operating points." |
| 9️⃣ | 📄 p. 2, Results heading | 💬 "The pretrained model's phrase gap is mostly wording." | 🔻 Negative heading | ✍️ "Two instruments separate wording from behavior." |
| 🔟 | 📄 p. 3, Results | 💬 "Scoring only each answer's first turn keeps every conclusion, though gaps shift slightly (DPO 0.034 to 0.021; Table 3), a check needed because models with SFT in their chain run past their turn in 98 to 99% of answers under the base model's stop rule." | ⚙️ Engineering, reads as a defect report | ✍️ Move to Setup: "Generation uses the base model's stop rule, under which models with SFT in their chain continue past their turn in 98 to 99% of answers; every refusal claim is checked on the first turn alone, which keeps every conclusion (DPO 0.034 to 0.021; Table 3)." |
| 1️⃣1️⃣ | 📄 p. 3, Results | 💬 "Trained with one contract after SFT, SwiPO shows no resolved gain over its starting point." | 🔻 Negative result stated as a failure | ✍️ "After SFT, one-contract SwiPO training stays within the interval of its starting point (+0.017 [−0.025, 0.057]): the chain, not the loss, sets the lever." |
| 1️⃣2️⃣ | 📄 p. 3, Results | 💬 "Dropping its penalty (λ = 0, contract-conditioned DPO on the same chain, data and settings) changes nothing measurable:" | 🔻 Negative framing | ✍️ "The λ = 0 ablation (contract-conditioned DPO on the same chain, data and settings) confirms this, with no measurable difference:" |
| 1️⃣3️⃣ | 📄 p. 3, Results | 💬 "Two contracts per request on SwiPO-R's chain leave the gap at its start (judge −0.012 [−0.058, 0.032], phrase +0.012 [−0.031, 0.054])." | 🔻 Negative, too terse to read as a test | ✍️ "The natural fix, training on two contracts per request on SwiPO-R's chain, keeps the gap at its starting level (judge −0.012 [−0.058, 0.032], phrase +0.012 [−0.031, 0.054]), so a multi-contract objective that adds a selector remains to be found." |
| 1️⃣4️⃣ | 📄 p. 3, Table 1 verdicts | 💬 "attenuated after SFT" / "no detected unsafe-rate shift" / "no floor-specific reduction" / "limited" / "no resolved shift" | 🔻 Five negative verdicts in a row; "no floor-specific reduction" is ambiguous | ✍️ "set by the chain (attenuated after SFT)" / "harm fixed by the objective (no detected shift)" / "no floor protection resolved" / "small shift (ratio 1.015 to 1.089, target above 4)" / "no resolved shift" |
| 1️⃣5️⃣ | 📄 p. 3, Table 2 caption | 💬 "SwiPO-R: public checkpoint (chain without SFT); SwiPO-S: retrained on SFT and DPO; PPO: untrained adapter (Setup)." | ⚙️ Engineering, anonymity hint | ✍️ "SwiPO-R: chain without SFT; SwiPO-S: chain with SFT and DPO; PPO: second run of SFT (Setup). Refusal gaps on full answers." |
| 1️⃣6️⃣ | 📄 p. 4, Results | 💬 "As trained, the permissive-minus-strict unsafe rate is −0.002 to +0.016 for all four models and +0.001 [−0.009, 0.010] for SwiPO on the intended chain, every interval including zero (Table 2)" | ⚙️ Undefined term | ✍️ "As trained, the permissive-minus-strict unsafe rate is −0.002 to +0.016 for DPO, PPO, GRPO and SwiPO-R and +0.001 [−0.009, 0.010] for SwiPO-S, every interval including zero (Table 2)" |
| 1️⃣7️⃣ | 📄 p. 4, Results | 💬 "Invariance is not safety: under the strict contract the unsafe rate ranges from 0.014 (SwiPO-S) to 0.323 (PPO's SFT run)." | ⚙️ Jargon ("PPO's SFT run") | ✍️ "Contract invariance and low harm are separate objectives: under the strict contract the unsafe rate ranges from 0.014 (SwiPO-S) to 0.323 (PPO, a second run of SFT)." |
| 1️⃣8️⃣ | 📄 p. 4, Limitations | 💬 "harm is scored by Llama Guard 3, and neither is yet checked against human labels." | 🔍 Self-critical close | ✍️ "harm is scored by Llama Guard 3; neither instrument has been checked against human labels yet, and a human-labeled subset is the next validation step." |
| 1️⃣9️⃣ | 📄 p. 4, Conclusion | 💬 "Two contracts per request did not add a selector either, so training several trade-offs into one checkpoint remains open, and a floor has to be trained explicitly." | 🔻 Ends on what failed | ✍️ "Training several trade-off points into one checkpoint therefore needs more than two contracts per request, which did not add a selector here, and a floor needs its own training signal: the five-property test gives both a target." |

### D.2) The 3 rewrites that matter most

1. **Row 3 plus row 4 (abstract end and contribution bullet).** The first page now ends on an unexplained number and a list of shortfalls. Ending on "the chain, not the loss, sets the lever" gives the reviewer the thesis.
2. **Row 7 (first Results heading).** It is the first heading under Figure 1 and frames the whole Results section as a shortfall. The rewrite turns the same data into the venue's language: which operating points a contract can move.
3. **Row 6 (the penalty sentence).** Reviewers at an optimization venue read "it is not a divergence estimate, and minimizing it favors lowering both likelihoods" as the authors saying their loss is wrong. The rewrite keeps the fact and points to the ablation that tests it.

### D.3) Rewritten abstract (260 words; the original is about 263)

We contribute a five-property test of whether a natural-language contract in the system message selects an operating point on the safety-helpfulness trade-off (target, side effects on harm, a floor fixed before any rate was computed, held-out prompts, channel), and apply it to Llama-3.1-8B models trained with DPO, GRPO and SwiPO (an instruction-conditioned DPO with a log-ratio penalty to the reference model), each evaluated as trained with every parent low-rank adapter merged; an untrained PPO adapter gives a second run of the supervised fine-tuning (SFT) model. A move counts only where a refusal-phrase heuristic and an LLM judge agree. Two models move along the trade-off: a prompted instruction-tuned model (judge gap 0.142) and SwiPO on a chain that skips SFT (0.128); on XSTest the permissive contract makes them answer 0.252 and 0.152 more of the safe prompts, while each model with SFT in its chain moves at most 0.080 on either axis. The chain matters more than the loss: after SFT, DPO and GRPO keep a phrase gap of 0.03 and SwiPO 0.052 (95% interval 0.020 to 0.082), not separable from DPO (+0.017, −0.025 to +0.057); with harm as a third objective, SwiPO after SFT, the least harmful trained model, is non-dominated. The system contract shifts no trained model's unsafe answers (Llama Guard 3) and no trained model keeps a floor; a permissive user turn raises them after SFT, PPO and GRPO (+0.044 to +0.065). The pretrained model's phrase gap of 0.299 (0.266 to 0.332) is mostly repeated wording (judge 0.012); loading only the final adapter would report 0.30 to 0.49.

(If Part C item 2 shows that SwiPO-S is non-dominated in only a minority of resamples, replace "is non-dominated" with the measured share. If item 4 lands, add "and training on two contracts per request did not add a selector".)

# ⭐ The single most valuable change before the MultiRobust deadline

Rewrite the first page in the venue's vocabulary and lead with the contribution: call the floor a hard constraint and the contract a preference over Pareto points, state the thesis once ("with loss, data and settings fixed, the training chain, not the loss, decides whether a contract moves a model along the safety-helpfulness trade-off; after SFT on one contract no tested loss keeps a lever"), use the D.3 abstract, and move the loading story (final adapter alone) to the footnote. This is pure rewriting (about 2 hours), needs no new run, frees about 6 lines for the second-judge column (Part C item 3), and raises the three lowest rubrics (clarity, tone, fit) at once.

Legend: 🟩 score 7 or more / strength . 🟨 score 5 to 6 / partial . 🟥 score 4 or less / reject risk . ✅ clean . 🟡 soft issue . ❌ absent . 🔻 negative tone . ⚙️ engineering report . 🔍 self-criticism . ❗ disagreement . ✂️ cut . 📏 lines . 📈 rubric gain . 🟦 calibration fact . 💬 quote . ✍️ rewrite . 📄 location . 🔧 change . 💡 why
