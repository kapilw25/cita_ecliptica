Round 7 (fresh Claude Code judge, Fri Nov 27 2026), PDF built from commit a6004fe.
Score: 64 / 100. Acceptance probability: 58% at MultiRobust, 65% at a typical AAAI-27 safety/alignment workshop.

> 📄 Judged: `Overleaf_draft/v6_AAAI27_workshops/v5_MultiRobust_4page/0_main.pdf` (built Fri Nov 27 20:47 PST, 5 pages: 4 main + 1 references). Every page was read as an image and as text. Venue: MultiRobust (W38), double-blind, 4 pages including figures and tables. Deadline Sat Nov 28 3:59 AM PST (about 7 hours from this review), so Part C is limited to rewrites, re-analysis of existing numbers, and cuts. No earlier review or score file was opened.

## 🧭 Step 1. Calibration sheet (3 accepted short papers, AAAI-26 "How Can We Trust and Control Agentic AI?")

### 1. Each paper in three lines

| 📚 Paper | 🎯 Core claim | 📊 Main evidence | 🏆 What most likely got it accepted |
|---|---|---|---|
| 🧊 (1) Trust Paradox, pp. 1-5 | 🎯 Raising prompt-level "alignment intensity" past minimal lowers a trust proxy | 📊 120 dialogues, 4 Llama models x 5 scenarios x 6 levels; Fig. 1 U-curve (p. 2), Fig. 2 heatmaps (p. 3), r = 0.771 and -0.450, mixed-effects F(5,100) = 12.34 (p. 4) | 🏆 A named, counter-intuitive phenomenon in the title and one hook figure; topical for "trust" |
| 🎲 (2) When Refusals Fail, pp. 6-17 | 🎯 Agent capability and refusal shift unpredictably with context length, type and position | 📊 AgentHarm with 1K to 200K tokens of padding, 4 frontier models; Fig. 1 design (p. 7), Figs. 2-4 with 1-sigma bars over at least 3 seeds (pp. 8-9, App. B p. 11) | 🏆 Clean design figure, four bulleted findings on p. 6, a clear safety consequence |
| 🤖 (3) Biased Agents, pp. 18-23 | 🎯 Demographic personas change agent task success by up to 26.2% | 📊 Table 2 (p. 20): 3 models x 5 benchmarks x personas; Figs. 2-4 (pp. 20-21) | 🏆 "First systematic case study" framing, a cartoon teaser (Fig. 1 p. 18), one big table |

### 2. Common bar for a short paper

- 🟩 A one-sentence question or phenomenon in the title, answered in the abstract.
- 🟩 One teaser or design figure on page 1 or 2, then 3 to 5 findings stated as bullets or bold paragraph leads (paper 2 p. 6; paper 3 bold leads p. 19).
- 🟨 Evidence from 3 to 5 models on public benchmarks; statistics are light (paper 1 p-values, paper 2 1-sigma bars, paper 3 none).
- 🟩 Plain, confident prose; one idea per paragraph; few numbers per sentence.

### 3. What they get away with

- 🟥 Paper 1: trust is a programmatic proxy, no humans (p. 4); a correlation of -0.143 is called a paradox (p. 3); 0.748 vs 0.743 presented as a finding (p. 2); no intervals.
- 🟨 Paper 2: 1-sigma bars only; API-provider safety filters confound results, admitted (p. 17); only the easiest AgentHarm subset (p. 9).
- 🟥 Paper 3: single deterministic runs, no variance or tests; stereotype readings of single-point differences (pp. 20-21).

### 4. One sentence per paper that sells its novelty

- 🧊 (1) "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." (p. 1)
- 🎲 (2) "Our work addresses this gap. We find that LLM agents could be sensitive to length, type, and placement of the context, exhibiting unexpected and inconsistent shifts in task performance and in refusals to execute harmful requests." (p. 6)
- 🤖 (3) "In this case study, we provide the first systematic investigation demonstrating that demographic-based persona assignments can measurably undermine LLM agents' task execution." (p. 18)

### 5. Limitations and negative results

- 🟩 All three put limitations at the end, in 3 to 6 sentences, framed as scope ("Due to budget constraints, we evaluated a limited set of models", paper 2 p. 9; "broader coverage ... would further clarify", paper 3 p. 21).
- 🟩 Negative results are framed as findings about the world ("Refusal rates shift unpredictably", paper 2 p. 6), never as failures of the authors' own method.

### 6. Evaluation evidence

- 🧊 (1) No repeated runs; correlations and a mixed-effects test; no failure taxonomy.
- 🎲 (2) At least 3 seeds, 1-sigma bars; an immediate vs. delayed refusal taxonomy (App. H, Fig. 11, p. 12) separates serious failures (partial harm executed) from minor ones.
- 🤖 (3) Single runs; arrows color-coded by size of degradation (Table 2), no severity split.

### 7. What a 4-page paper must show, and may leave out

- 🟩 Must: one question, one design, one decisive figure or table, 3 to 4 findings, a short limitations paragraph.
- 🟨 May leave out: extra baselines, ablations, human evaluation, significance tests. Paper 2 moved most detail to 8 pages of appendix; MultiRobust counts appendices toward the 4 pages, so that route is closed here.

Legend: 📚 paper . 🎯 claim . 📊 evidence . 🏆 acceptance driver . 🟩 strong or required . 🟨 partial . 🟥 weak

## 🏛️ Step 2. What each venue's reviewers look for first (brief)

- 🟦 **MultiRobust (this draft).** An explicit multi-objective reading: which objectives, how the front is measured, whether a method moves along the front, expands it, or leaves it; constraint handling (a hard constraint that must not be traded); some optimization content (a loss or training procedure that targets several trade-off points); and robust evaluation. Reviewers come from multi-objective optimization and will read the title, Figure 1, the abstract and the contribution list, then skim. They will not parse refusal-instrument subtleties unless the paper makes the payoff obvious.
- 🟩 LoyalAgents: whose interest the agent serves, conflicts of interest, disclosure.
- 🟧 Bench2Evidence: whether scores measure what they claim, stability across runs, severity of failures.
- 🟪 MATH4AI: a formal object (a definition, bound or model) that explains the empirical result.

## ⚖️ Step 3, Venue 2 (MultiRobust)

### 🅰️ Part A. Acceptance probability

**58% at MultiRobust; 65% at a typical AAAI-27 safety/alignment workshop.** The draft clears the evidence bar of the three accepted short papers by a wide margin: every number carries a paired 95% BCa interval (Setup, p. 2), the refusal result is replicated on 2,444 held-out prompts, on XSTest, under a second judge from another family, and over three resamples (pp. 2-3), and the floor set was fixed before any rate was computed (p. 2). None of the calibration papers had more than 1-sigma bars. Figure 1 (p. 1) is a native Pareto-plane evaluation, which fits MultiRobust's "Pareto-aware evaluation" and "constraint handling in AI safety" topics. What holds the number below 60%: a MultiRobust reviewer looks for optimization content, and the paper's own optimization results are null after SFT (SwiPO not separable from DPO, the penalty ablation changes nothing, the two-contract run stays at its start, p. 3); the thesis "the training chain, more than the loss, decides" rests on one pair of SwiPO runs with one seed and an uncrossed design; the closest multi-objective conditioning work (Panacea, Rewards-in-Context, Controllable Preference Optimization) and even DPO's own citation are missing; and the prose is so dense that a reviewer with 20 minutes will not extract the answer to the title question. A safety/alignment workshop rates the refusal-versus-harm and user-override findings (p. 4) closer to its core and forgives the missing optimization content, hence 65%.

**3 things most likely to make a reviewer reject**

| # | 🟥 Reject risk | 📄 Where |
|---|---|---|
| 1️⃣ | 🟥 Density hides the answer. The abstract runs about 285 words with about 25 numbers; the XSTest paragraph (p. 2, 24 lines) carries 14 intervals; the reader must track three refusal instruments, two loadings and eight model names (SwiPO-R, SwiPO-S, PPO as an SFT replicate, Base, Instruct). The accepted papers state 3 to 4 findings in bullets (paper 2 p. 6). | 📄 Abstract; Sec. 4 pp. 2-4 |
| 2️⃣ | 🟥 The causal thesis is under-identified and the method result is null. "With loss, data and settings fixed, the training chain, more than the loss, decides" (abstract, p. 1) rests on one SwiPO pair and "one training seed per method" (Sec. 6); DPO and GRPO were trained only on the SFT chain, so loss and chain are never crossed; the lambda = 0 ablation is run only on the SFT chain where SwiPO already has no lever (p. 3); and the one trained selector, SwiPO-R, is "not [separated] from DPO, PPO or GRPO" by the second judge on Conditional Safety (p. 3). | 📄 Abstract; Setup p. 2; Sec. 4 p. 3; Sec. 6 p. 4 |
| 3️⃣ | 🟥 Positioning. Related Work (p. 4) is three sentences and names CoSA as "the closest work"; it omits preference-conditioned Pareto alignment (Panacea, NeurIPS 2024, fits the helpfulness-harmlessness front on BeaverTails; Rewards-in-Context, ICML 2024; Controllable Preference Optimization, EMNLP 2024, which conditions a DPO-style loss on preference tokens). A MultiRobust reviewer will ask how SwiPO differs from CPO. DPO itself is never expanded or cited. | 📄 Sec. 5 p. 4; References p. 5 |

**3 strongest points**

| # | 🟩 Strength | 📄 Where |
|---|---|---|
| 1️⃣ | 🟩 Figure 1 is exactly the venue's object: each model's strict and permissive points on a refusal-of-unsafe by answer-to-safe plane with 95% BCa whiskers. It shows at a glance that the prompted Instruct model moves 0.252 up the helpfulness axis while the models with SFT cluster. | 📄 Fig. 1 p. 1; Sec. 4 p. 2 |
| 2️⃣ | 🟩 Rigor far above the calibration bar: paired BCa intervals with 10,000 resamples, held-out replication (2,444 prompts, 918 floor), a second judge family, first-turn rescoring, three resamples, dominance shares over 10,000 joint resamples, and an untrained PPO adapter turned into a run-to-run noise check. | 📄 Setup p. 2; Sec. 4 pp. 2-3; Tables 2-4 |
| 3️⃣ | 🟩 Two findings that matter beyond SwiPO: refusal and harm are distinct objectives (the system contract moves no trained model's unsafe rate, yet a permissive user turn raises it by +0.044 to +0.065 in SFT, PPO and GRPO with no resolved refusal drop, p. 4), and stacked adapters must be evaluated as trained (final adapter alone 0.30 to 0.49 against 0.02 to 0.05 as trained, Table 2). | 📄 Sec. 4 p. 4; Table 2 p. 3 |

### 🅱️ Part B. Ten rubrics (chosen for a MultiRobust reviewer)

| 🧩 Rubric | 💡 Why it matters here | 🔢 Score | 📄 Evidence from the paper | 🛠️ The one change that adds the most points |
|---|---|---|---|---|
| 🎯 Venue fit: Pareto framing | 💡 The call is Pareto-aware evaluation and constraint handling | 🟨 7 | 📄 Title question; Fig. 1 plane (p. 1); dominance shares (p. 2); floor as hard constraint (Sec. 2). But the main suite reduces each model to one scalar gap (Table 2), and the paper never names which points form the front | 🛠️ State the empirical front and which contract pairs trace a trade-off, from existing JSON (C1) |
| 🧭 Novelty and positioning | 💡 Reviewers know preference-conditioned multi-objective alignment | 🟥 5 | 📄 Sec. 5 (p. 4): CoSA only; no Panacea, RiC or CPO; DPO uncited | 🛠️ One related-work sentence with three citations (C5) |
| 📣 Contribution clarity | 💡 A 4-page paper is decided on page 1 | 🟨 6 | 📄 Two bullets (pp. 1-2); the second ends negatively: "no single-contract loss we tested restores it"; the thesis sentence appears twice (abstract, intro) | 🛠️ Rewrite the bullets as findings (D #5) |
| 🔬 Soundness of the central claim | 💡 "Chain more than loss" is the thesis | 🟥 5 | 📄 One SwiPO pair, one seed (Sec. 6); loss and chain not crossed; lambda = 0 only on the SFT chain (p. 3); SwiPO-R not separable from DPO, PPO, GRPO under the Qwen judge (p. 3) | 🛠️ Scope the thesis to these runs and name the uncrossed design in one clause; no GPU |
| 📊 Statistical rigor | 💡 Robust evaluation is the venue's theme | 🟩 9 | 📄 Paired BCa, 10,000 resamples (p. 2); held-out; resamples; joint-resample dominance (p. 2) | 🛠️ Give or point to intervals for Table 1's Length and Confidence rows (C3) |
| 🧪 Measurement validity | 💡 Refusal instruments define every result | 🟨 6 | 📄 Judge-heuristic kappa 0.03 to 0.58, six of eight models at 0.03 to 0.07 (Table 3); judges agree on 0.57 to 0.78 of answers (p. 2); no human labels (Sec. 6); 98 to 99% run past their turn (p. 3) | 🛠️ Say that agreement is required at the gap level, not per item, where kappa is introduced |
| 🧱 Constraint handling (floor) | 💡 "Constraint handling in AI safety" is a listed topic | 🟨 7 | 📄 Floor fixed before any rate (p. 2); gap-difference test, Table 4; prompted Instruct -0.115 [-0.161, -0.065] (p. 4) | 🛠️ Replace "no trained model keeps the floor" with "no resolved floor" (C3) |
| 🛡️ Robustness and generalization | 💡 Robust AI venue | 🟩 8 | 📄 XSTest outside every training pool, 2,444 held-out prompts, second judge family, first-turn rescoring (pp. 2-3); one backbone, one seed (Sec. 6) | 🛠️ Put "one seed, one backbone" next to the thesis, not only in Sec. 6 |
| ✍️ Writing density | 💡 Reviewers skim | 🟥 4 | 📄 Abstract about 285 words; undefined "no echo", "its start", "run past their turn", "two contracts per request" (p. 3) | 🛠️ Abstract rewrite (D.3) and cut numbers already in tables |
| 🖼️ Figures and tables | 💡 They carry a 4-page paper | 🟨 7 | 📄 Fig. 1 clear; Table 1 values 0.169 and 0.002 to 0.040 appear nowhere in the text; Table 4 headers collide; tiny intervals further shrunk by resizing | 🛠️ Fix Table 1 cells and caption; widen or drop bold in Table 4 (C3) |

**Total: 64 / 100.** Under the same ten rubrics I would place the accepted papers at about 50 (Trust Paradox: clarity high, rigor and validity low), about 70 (When Refusals Fail: clear figures and design, 1-sigma rigor) and about 64 (Biased Agents: clear table and teaser, no variance). This draft sits inside the accepted range but has the opposite profile: it beats all three on rigor and robustness and loses to all three on clarity, the dimension that carried each of them.

Legend: 🔢 🟩 8 to 10 . 🟨 6 to 7 . 🟥 5 or less

### 🅲 Part C. Improvements before the deadline (ranked by expected gain)

| Rank | 🛠️ What it shows | 🧰 What it needs | 📍 Where it goes (and what is cut) | 📈 Rubric gain |
|---|---|---|---|---|
| 1️⃣ | 🛠️ **Answer the title question with the front.** On XSTest (judge, refusal of unsafe by answers to safe) the non-dominated set is the four prompted-model points plus SwiPO-R's permissive point. SwiPO-R's strict point refuses safe and unsafe prompts alike (unsafe minus safe refusal 0.025 [-0.057, 0.106], against 0.187 [0.100, 0.271] under the permissive contract), sits on Figure 1's dotted line, and is dominated in 85% of 10,000 joint resamples. Only the prompted Instruct model trades one objective for the other (answers +0.252 for an unresolved 0.065 of unsafe refusal); SwiPO-S's permissive contract costs unsafe refusal (0.080 [0.015, 0.150]) for an unresolved answer change (+0.008 [-0.032, 0.048]). | 🧰 Re-analysis only, about 1 hour, no GPU. Every number already exists in `outputs/evaluation/contract_gap/xstest_contract_judge_stop_eot.json` ("discrimination", "strict_minus_permissive") and `xstest_dominance_judge.json` ("non_dominated"; SwiPO-R strict "share_of_resamples_dominated" 0.8473). Say these are point-estimate dominance statements | 📍 Replace the sentence "On refusal and helpfulness alone, every operating point ... (in 79 to 100% of 10,000 joint prompt resamples)" on p. 2 (keep its numbers inside the new sentence); shorten the base-model harm sentence ("On the 200 unsafe prompts ... run-on text included)") to one clause; change Fig. 1 caption "dotted: equal refusal of both" to "dotted: equal refusal of safe and unsafe prompts (no discrimination)" | 📈 Venue fit +2, contribution clarity +1, soundness +0.5 |
| 2️⃣ | 🛠️ **Abstract that a skimmer can use** (D.3): same facts, opens with the contribution, names refusal and harm as distinct objectives | 🧰 Rewrite only, 30 minutes | 📍 Replaces the abstract; then cut the duplicate thesis sentence in the intro ("Our thesis: with loss, data and settings fixed, ...") since the abstract and bullet carry it | 📈 Writing +2, contribution clarity +1 |
| 3️⃣ | 🛠️ **Fix overclaims and untraceable table values.** Abstract "shifts no trained model's unsafe answers" to "produces no resolved shift in"; "no trained model keeps the floor" to "no trained model shows a resolved floor" (Table 4 intervals reach -0.103 and -0.091); Conclusion "does not move their harm, which the training objective sets" to "produces no resolved change in their harm, whose level differs by objective"; Table 1 "XSTest judge 0.002 to 0.040 (0.169)" to numbers that appear in Sec. 4 (for example "XSTest judge: at most 0.080 on either axis (answers +0.252)"); Table 1 caption "95% intervals in Section 4" to add "(Length and Confidence: point estimates)"; expand and cite DPO (Rafailov et al. 2023) at first use; Intro "constraining helpfulness with a cost model (Dai et al. 2024)" to "maximizing helpfulness under a harm-cost constraint" | 🧰 Rewrite only, 30 to 45 minutes | 📍 In place; net length about zero | 📈 Soundness +1, figures and tables +1, constraint handling +0.5 |
| 4️⃣ | 🛠️ **Make the two-contract run the multi-task test** (the most on-call experiment in the paper, now one cryptic sentence). Proposed text, all numbers from `common/numbers.tex` and the sentence the other drafts already carry: "Training both points into one checkpoint, with two contracts per request (the strict contract prefers the safer and the permissive the more helpful answer of PKU-SafeRLHF pairs whose labels disagree), on SwiPO-R's chain stays at its starting point under both instruments (judge -0.012 [-0.058, 0.032], phrase +0.012 [-0.031, 0.054], against the DPO adapter alone): judge gap 0.061 [0.029, 0.093], 0.067 [0.021, 0.114] below SwiPO-R." | 🧰 Rewrite only, 20 minutes | 📍 Replaces "Two contracts per request on SwiPO-R's chain leave the gap at its start (judge -0.012 [-0.058, 0.032])." (p. 3). Cut to make room: turn "Three resamples of every answer keep this order (Conditional Safety: ...)" into "(three resamples keep this order)", saving about 3 lines | 📈 Venue fit +1, writing +0.5 |
| 5️⃣ | 🛠️ **Position against preference-conditioned Pareto alignment.** One sentence: "Panacea (Zhong et al. 2024), Rewards-in-Context (Yang et al. 2024) and Controllable Preference Optimization (Guo et al. 2024) condition one model on a preference vector or per-objective scores, Panacea on the helpfulness-harmlessness trade-off; we condition on a natural-language contract and test whether the selection survives the training chain." | 🧰 Rewrite plus three bib entries (verify each: arXiv 2402.02030, 2402.10207, 2402.19085), 20 minutes. References do not count toward the 4 pages | 📍 Sec. 5 after the decoding-time sentence. Cut to make room: footnote 1 (it repeats its own sentence, 2 lines) and the clause "so we claim the movement, not the absolute points" folded into the previous sentence | 📈 Novelty and positioning +2 |

**Cut list (to make room for C1, C4, C5):** 🔪 footnote 1 on p. 2 (duplicates "We evaluate each model as trained, parent adapters merged, and contrast it with the final adapter alone"); 🔪 the intro's second statement of the thesis; 🔪 "Three resamples ..." sentence to a parenthesis; 🔪 the base-model XSTest harm sentence to one clause; 🔪 "(the judge reads the first reply, Llama Guard 3 the full answer, run-on text included)" (already said in Setup).

**Not doable before this deadline (flagged):** ⛔ crossing loss and chain (DPO and GRPO trained on the chain without SFT) and a second seed for SwiPO-R and SwiPO-S need new GPU training, which MultiRobust's window does not allow; ⛔ a 100-answer human audit of both refusal instruments needs no GPU but about 2 hours of an author's labeling time, risky at 7 hours to deadline.

Legend: 🛠️ change . 🧰 cost . 📍 placement . 📈 gain . 🔪 cut . ⛔ out of time

### 🅳 Part D. Tone audit

| # | 📄 Page / section | 📝 Quoted original (exact) | 🚩 Problem | ✍️ Rewrite (facts and numbers unchanged, no em dashes) |
|---|---|---|---|---|
| 🔹 1 | 📄 p. 1 Abstract | 📝 "an untrained PPO adapter gives a second run of the supervised fine-tuning (SFT) model." | 🚩 Negative, engineering | ✍️ "a PPO adapter that holds no update serves as a second run of the supervised fine-tuning (SFT) model." |
| 🔹 2 | 📄 p. 1 Abstract | 📝 "SwiPO on a chain that skips SFT (0.128, halved by a second judge)" | 🚩 Criticism-led | ✍️ "SwiPO on a chain without SFT (0.128; 0.066 under a second judge)" |
| 🔹 3 | 📄 p. 1 Abstract | 📝 "After SFT, DPO and GRPO keep a phrase gap of 0.03 and SwiPO 0.052 (95% interval 0.020 to 0.082), not separable from DPO (+0.017, −0.025 to +0.057)." | 🚩 Negative about own method, no framing | ✍️ "Holding loss, data and settings fixed isolates the chain: after SFT, SwiPO's phrase gap (0.052, 95% interval 0.020 to 0.082) is not separable from DPO's (+0.017, −0.025 to +0.057), and DPO and GRPO keep 0.03." |
| 🔹 4 | 📄 p. 1 Abstract | 📝 "Loading only each model's final adapter would report a gap of 0.30 to 0.49." | 🚩 Engineering, last sentence of the abstract | ✍️ "Evaluating stacked adapters as trained matters: the final adapter alone would report gaps of 0.30 to 0.49, against 0.02 to 0.05 as trained." |
| 🔹 5 | 📄 p. 2 Contributions, bullet 2 | 📝 "only a prompted instruction-tuned model and SwiPO without SFT in its chain select; SFT on one contract attenuates the pretrained model's phrase gap (0.299, mostly wording) and no single-contract loss we tested restores it." | 🚩 Negative, the contribution ends on what failed | ✍️ "only a prompted instruction-tuned model and SwiPO without SFT in its chain select, which points to SFT on one contract, rather than the preference loss, as the step that fixes the operating point: after SFT, DPO, GRPO and SwiPO keep gaps of 0.03 to 0.05 (the pretrained model's 0.299 is mostly wording)." |
| 🔹 6 | 📄 p. 2 Setup, Models | 📝 "Our PPO adapters carry no update (all 224 LoRA B matrices are zero), so PPO's rows are free second runs of the SFT model (as trained) and of the base model (final adapter alone), a check on run-to-run noise." | 🚩 Negative, engineering | ✍️ "The PPO adapters hold no update (all 224 LoRA B matrices are zero); we use their rows as built-in replicates of the SFT model (as trained) and of the base model (final adapter alone), which measure run-to-run noise." |
| 🔹 7 | 📄 p. 2 Setup, footnote 1 | 📝 "Stacked adapters can be loaded two ways; Table 2 reports both, and every claim uses the model as trained." | 🚩 Engineering, repeats its own sentence | ✍️ Cut; the sentence it annotates already says this. |
| 🔹 8 | 📄 p. 2 Sec. 4 heading | 📝 "Limited operating-point movement after SFT." | 🚩 Negative lead for the first result | ✍️ "A contract moves the operating point of prompted models and SwiPO-R, not of models trained after SFT." |
| 🔹 9 | 📄 p. 2 Sec. 4 | 📝 "The phrase heuristic shows the same pattern of movement but far lower refusal levels for these models (unsafe refused 0.040 to 0.155), so we claim the movement, not the absolute points." | 🚩 Self-critical | ✍️ "The phrase heuristic reproduces this movement at lower absolute refusal levels (unsafe refused 0.040 to 0.155), so the movement, which both instruments support, is what we claim." |
| 🔹 10 | 📄 p. 3 Sec. 4 | 📝 "Scoring only each answer's first turn keeps every conclusion, though gaps shift slightly (DPO 0.034 to 0.021; Table 3), a check needed because models with SFT in their chain run past their turn in 98 to 99% of answers." | 🚩 Engineering, undefined defect | ✍️ "Every conclusion holds when only each answer's first turn is scored (DPO 0.034 to 0.021; Table 3), which matters because models with SFT in their chain continue generating past the end of their turn in 98 to 99% of answers." |
| 🔹 11 | 📄 p. 3 Sec. 4 | 📝 "Trained with one contract after SFT, SwiPO shows no resolved gain over its starting point." | 🚩 Negative about own method | ✍️ "With loss, data and settings shared, this contrast isolates the chain: SwiPO-R keeps its lever, while after SFT SwiPO adds no resolved gain over its DPO starting point." |
| 🔹 12 | 📄 p. 3 Sec. 4 | 📝 "Dropping its penalty (λ = 0, contract-conditioned DPO on the same chain, data and settings) changes nothing measurable: judge gap 0.026 [−0.004, 0.057], −0.002 [−0.044, 0.040] from SwiPO-S." | 🚩 Negative framing of an informative ablation | ✍️ "The penalty is not what holds the SFT chain back: with λ = 0 (contract-conditioned DPO on the same chain, data and settings) the judge gap is 0.026 [−0.004, 0.057], −0.002 [−0.044, 0.040] from SwiPO-S." |
| 🔹 13 | 📄 p. 3 Sec. 4 | 📝 "Two contracts per request on SwiPO-R's chain leave the gap at its start (judge −0.012 [−0.058, 0.032])." | 🚩 Negative and undefined ("its start", the run itself) | ✍️ Use the C4 sentence: the multi-task run, its preference rule, and its four intervals. |
| 🔹 14 | 📄 p. 4 Sec. 4, floor | 📝 "Unsafe rates show no resolved contract effect on floor prompts, but no trained model protects floor requests preferentially, which motivates a floor-specific training objective." | 🚩 Negative; "protects ... preferentially" is stronger than the intervals | ✍️ "Unsafe rates show no resolved contract effect on floor prompts, and no trained model shows resolved preferential protection of floor requests, which makes the floor a concrete target for a floor-specific training objective." |
| 🔹 15 | 📄 p. 4 Sec. 4, channel | 📝 "Llama Guard 3 prices the override against the strict system contract alone" | 🚩 Jargon ("prices") | ✍️ "Scored by Llama Guard 3 against the strict system contract alone, the override changes unsafe answers as follows:" |
| 🔹 16 | 📄 p. 4 Sec. 6 | 📝 "SwiPO received 13 Optuna tuning trials and DPO and GRPO fixed settings, an asymmetry that can favor SwiPO." | 🚩 Self-critical without saying what it does not affect | ✍️ "SwiPO received 13 Optuna tuning trials and DPO and GRPO fixed settings; this asymmetry can favor SwiPO over DPO and GRPO, but not SwiPO-R over SwiPO-S, which share data and hyper-parameters, so the chain contrast is unaffected." |
| 🔹 17 | 📄 p. 4 Sec. 6 | 📝 "harm is scored by Llama Guard 3, and neither is yet checked against human labels." | 🚩 Negative ending of limitations | ✍️ "harm is scored by Llama Guard 3; a human-label audit of both instruments is the next validation step." |
| 🔹 18 | 📄 p. 4 Conclusion | 📝 "DPO, GRPO and SwiPO after SFT barely move (gap 0.03 to 0.05; on XSTest at most 0.080), and the system contract does not move their harm, which the training objective sets" | 🚩 Overclaim ("does not move", "sets") | ✍️ "DPO, GRPO and SwiPO after SFT barely move (gap 0.03 to 0.05; on XSTest at most 0.080), and the system contract produces no resolved change in their harm, whose level differs by training objective" |
| 🔹 19 | 📄 p. 4 Conclusion | 📝 "Two contracts per request did not add a selector either, so training several trade-offs into one checkpoint remains open, and the floor, a hard constraint, has to be trained explicitly." | 🚩 Negative last sentence; "has to be trained explicitly" is not tested | ✍️ "The five-property test turns two open problems into measurable targets: training several trade-off points into one checkpoint (a two-contract run stayed at its starting point) and training the floor as an explicit hard constraint (no trained model shows a resolved floor)." |

Legend: 🔹 row . 📄 location . 📝 original . 🚩 problem . ✍️ rewrite

#### D.2) The 3 rewrites that matter most

1. 🥇 **#5, contribution bullet 2.** It is the reviewer's first statement of what the paper found, and it currently ends on "no single-contract loss we tested restores it". The rewrite keeps every fact and leads with the localization.
2. 🥈 **#18 and #19, the Conclusion.** The last paragraph is the reviewer's last impression; the rewrite removes two overclaims ("does not move", "has to be trained explicitly") and ends on measurable targets.
3. 🥉 **#16, the Optuna limitation.** As written it hands the reviewer a confound; the rewrite states, truthfully, that the chain contrast (the thesis) is immune to it because SwiPO-R and SwiPO-S share hyper-parameters (Setup, p. 2).

#### D.3) Rewritten abstract (same facts, 288 words against the current 289)

> We contribute a five-property test of whether a natural-language contract in the system message selects a Pareto point on the safety-helpfulness trade-off (target, side effects on harm, a floor as a hard constraint fixed before any rate was computed, held-out prompts, channel). We apply it to Llama-3.1-8B models trained with DPO, GRPO and SwiPO (an instruction-conditioned DPO with a log-ratio penalty to the reference model), each evaluated as trained with every parent low-rank adapter merged; a PPO adapter that holds no update serves as a second run of the supervised fine-tuning (SFT) model. With loss, data and settings fixed, and a move counted only where a refusal-phrase heuristic and an LLM judge agree, the training chain, more than the loss, decides whether a contract moves a model. Two models move their operating point: a prompted instruction-tuned model (judge gap 0.142) and SwiPO on a chain without SFT (0.128; 0.066 under a second judge). On XSTest the permissive contract makes them answer 0.252 and 0.152 more safe prompts, while each model with SFT in its chain moves at most 0.080 on either axis, as a judge from another family reproduces. After SFT, DPO and GRPO keep a phrase gap of 0.03 and SwiPO 0.052 (95% interval 0.020 to 0.082), not separable from DPO (+0.017, −0.025 to +0.057); the pretrained model's 0.299 is mostly repeated contract wording (judge 0.012). Refusal and harm behave as distinct objectives: the system contract produces no resolved shift in any trained model's unsafe answers (Llama Guard 3) and no trained model shows a resolved floor, yet a permissive user turn raises unsafe answers after SFT, PPO and GRPO (+0.044 to +0.065) and DPO (+0.016). The final adapter alone would report gaps of 0.30 to 0.49.

Note: "Two models move their operating point" replaces "Two models move along the trade-off" because SwiPO-R's XSTest move is along the helpfulness axis only, at unchanged unsafe refusal (0.745, 0.755; p. 2), which is not a move along a trade-off.

## 🕶️ Double-blind anonymity check

| 🔍 Check | 🚦 Result | 📄 Evidence |
|---|---|---|
| 🪪 Author block | ✅ clean | 📄 "Anonymous submission" header, no affiliations, no acknowledgments (p. 1, p. 4) |
| 🔗 Links, data, code | ✅ clean | 📄 No URL to own data or code in the PDF text; the data link is commented out in `0_main.tex` |
| 📚 Self-citation | ✅ clean | 📄 No own arXiv number or "our prior work" in text or references (p. 5) |
| 🏷️ PDF metadata | ✅ clean | 📄 No Title or Author fields; embedded figure metadata is only "Matplotlib v3.11.2"; no `/Users/` path or name in decompressed streams |
| 🧬 Method name | 🟡 low risk | 📄 If the public arXiv version (2601.06157) uses the name "SwiPO", a search for the name reveals the authors; AAAI normally permits preprints, but reviewers who search will find them |
| 🌐 Public repo | 🟡 low risk | 📄 Per `feedback/input/prompt.md` the repository is public; it holds this exact draft next to `common/authors.tex` with all names and an e-mail. A reviewer searching the title or a distinctive sentence could land on it. Consider making the repo private until decisions (Dec 2) |

Legend: 🚦 ✅ clean . 🟡 low risk . ❌ breach

## 🐞 Errors a reviewer would catch

### 🔢 Numbers in the text that disagree with, or cannot be traced to, a table or figure

1. 🔢 Table 1 (p. 3), Refusal row: "XSTest judge 0.002 to 0.040 (0.169)". Neither the range nor 0.169 appears anywhere in Section 4 of this draft, which reports XSTest only per axis (0.252, 0.065, 0.152, at most 0.080). They appear to be strict-minus-permissive refusal gaps pooled over all 450 XSTest prompts (0.169 = (250 x 0.252 + 200 x 0.065) / 450), but the draft never says so. The range also omits SwiPO-R (its pooled gap, by the same arithmetic, is about 0.080), although the column header says "range over contract-trained models".
2. 🔢 Table 1 caption: "Point estimates; 95% intervals in Section 4." Section 4 never discusses Length Ctrl or TruthfulQA, so the Length (1.015 to 1.089, 7.68) and Confidence (−0.011 to +0.004, 0.399) rows have no intervals anywhere, and "every interval includes zero" (Confidence row) cannot be checked.
3. 🔢 p. 3: "keeps a lever under every instrument (no echo 0.360, judge 0.128 [0.095, 0.162], Qwen judge 0.066 [0.029, 0.105]; Table 3)". Table 3 has no no-echo column, so 0.360 is cited to a table that does not contain it, and it has no interval.
4. 🔢 p. 3: "separates SwiPO-R's only from SwiPO-S (+0.049 [0.005, 0.093]) and SFT, not from DPO, PPO or GRPO (0.023 to 0.031)". The first number is a difference, the second set is those models' own Qwen gaps (Table 3: 0.029, 0.023, 0.031), and the SFT difference and the three non-separations have no intervals. A reader takes 0.023 to 0.031 as differences.
5. 🔢 Abstract and p. 2: "each model with SFT in its chain moves at most 0.080 on either axis". PPO has no point in Figure 1, so the statement covers four of the five models with SFT in their chain; the figure caption does not say PPO is omitted.
6. 🔢 p. 2: "The objective sets the level: 0.400 to 0.420 for SFT, PPO and GRPO". PPO's adapter "carry[ies] no update" (Setup), so its level cannot be set by its objective; it is the SFT level, as GRPO's nearly is.
7. 🔢 p. 4: "Capability does not move detectably against the base (5-shot MMLU −0.001 to +0.004, GSM8K −0.040 to +0.040, every interval including zero)". No sample sizes and no list of models, so a ±0.040 range on GSM8K cannot be judged.

### 📖 Undefined or unexpanded terms and acronyms

8. 📖 DPO is never expanded and never cited (no Rafailov et al. 2023 in the references, p. 5), although it is the main baseline and the base of SwiPO.
9. 📖 "SwiPO" is never expanded.
10. 📖 "no echo" (p. 3) is never defined (the earlier text says "without the repeated sentences").
11. 📖 "its start" and "Two contracts per request" (p. 3): the run's data and preference rule are never described in this draft.
12. 📖 "run past their turn" (p. 3) is never defined.
13. 📖 kappa means judge-heuristic agreement in Table 3 and Sec. 6 but judge-judge agreement on p. 2 ("κ 0.22 to 0.57"); same symbol, two pairs.
14. 📖 "first reply" (p. 2) and "first turn" (Table 3, p. 3) are used for the same thing without a definition.

### ⚠️ Claims stronger than their intervals

15. ⚠️ Abstract: "The system contract shifts no trained model's unsafe answers (Llama Guard 3) on either suite". Intervals include zero but reach +0.058 (SFT, Table 2) and +0.050 (GRPO); Table 1 itself says "no detected unsafe-rate shift". Also "either suite" when three suites carry the result (Conditional Safety, 2,444 held-out, XSTest).
16. ⚠️ Abstract: "no trained model keeps the floor"; Conclusion: "the floor, a hard constraint, has to be trained explicitly". Table 4 shows no resolved floor, but its intervals reach −0.103 (PPO) and −0.091 (SwiPO-S); absence of evidence is stated as absence.
17. ⚠️ Conclusion: "the system contract does not move their harm, which the training objective sets". "Does not move" is stronger than "every interval including zero", and "which the training objective sets" is causal from one seed per method.
18. ⚠️ Conclusion: "Under both refusal instruments, a contract selects ... in SwiPO without SFT in its chain". Under the third instrument the paper reports (Qwen, p. 3) SwiPO-R's Conditional Safety lever is not separable from DPO, PPO or GRPO.
19. ⚠️ Abstract: "Two models move along the trade-off". SwiPO-R moves "at unchanged unsafe refusal (0.745, 0.755)" (p. 2), so its permissive point is at least as good on both axes in point estimates; that is not a move along a trade-off, and its strict point lies on the dotted equal-refusal line of Figure 1.
20. ⚠️ Abstract and p. 1 thesis: "the training chain, more than the loss, decides". Loss and chain are not crossed (DPO and GRPO only on the SFT chain), there is one SwiPO pair and one seed (Sec. 6).
21. ⚠️ Intro (p. 1): "by constraining helpfulness with a cost model (Dai et al. 2024)". Safe RLHF maximizes helpfulness under a harm-cost constraint; a constraint-handling reviewer will flag this mischaracterization.

### ✏️ Broken or awkward sentences, references

22. ✏️ p. 4 Related Work: "Beside the training-time methods above" should be "Besides".
23. ✏️ p. 4: "Llama Guard 3 prices the override" (unclear verb).
24. ✏️ Setup (p. 2) calls Conditional Safety "the 1,222 PKU-SafeRLHF test prompts", while Sec. 6 (p. 4) says "about nine in ten Conditional Safety prompts appear in the training pool". Read together these look contradictory; state the overlap at first mention.
25. ✏️ References (p. 5): "Durme, B. V." should be "Van Durme, B."; "NeurIPS accepted version, arXiv:2406.18853" (Shi et al.) is not a venue string; MMLU, GSM8K, Qwen2.5 and Optuna are used without citations.
26. ✏️ Footnote 1 (p. 2) repeats the sentence it is attached to.

### 📐 Page layout (from the page images)

27. 📐 p. 2, right column, first line: "Suites. Conditional Safety poses the 1,222 PKU-" is visibly stretched (build log: Underfull hbox, badness 4713).
28. 📐 Figure 1 (p. 1): the cluster at refusal 0.40 to 0.60, answers 0.67 to 0.78 holds eight points with overlapping whiskers; DPO's strict and permissive markers nearly coincide and SFT and GRPO overlap. The legend's dark "strict contract" marker is close in color to "Base (prompted)" gray and the SwiPO-R navy. Labels are readable.
29. 📐 Table 4 (p. 4): the header cells "Gap diff." (suite) and "Permissive" (held-out) almost touch; the bracketed intervals are set in tiny type and then shrunk again by the column-width resize, so they are hard to read in print. Bold marks PPO, an untrained adapter, as the best suite gap difference, and the table has no SFT row to compare it with.
30. 📐 Tables 2 to 4 set every half-width and interval in tiny type; legible on screen at 200 dpi, marginal on paper.

Legend: 🔢 number . 📖 term . ⚠️ overclaim . ✏️ prose or reference . 📐 layout

## 🔗 Sources (related-work check for C5 and risk 3)

- [Panacea: Pareto Alignment via Preference Adaptation for LLMs (NeurIPS 2024)](https://papers.nips.cc/paper_files/paper/2024/hash/89f39d0b3d49a47606a165eefba2778c-Abstract-Conference.html), [arXiv 2402.02030](https://arxiv.org/abs/2402.02030)
- [Rewards-in-Context: Multi-objective Alignment of Foundation Models with Dynamic Preference Adjustment (ICML 2024)](https://proceedings.mlr.press/v235/yang24q.html), [arXiv 2402.10207](https://arxiv.org/pdf/2402.10207)
- [Controllable Preference Optimization: Toward Controllable Multi-Objective Alignment (EMNLP 2024)](https://aclanthology.org/2024.emnlp-main.85), [arXiv 2402.19085](https://arxiv.org/abs/2402.19085v1)
