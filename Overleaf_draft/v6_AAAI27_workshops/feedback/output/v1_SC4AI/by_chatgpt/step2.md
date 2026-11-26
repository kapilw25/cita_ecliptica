# 🤖 ChatGPT · Step 2 · Review of "SwiPO on ECLIPTICA-30k" (SC4AI'27)

> **Judge:** ChatGPT (same chat as [Step 1](step1.md)) · **Paper judged:** [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf) (9 pages, submitted) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 2

> [!NOTE]
> The judge's text below is kept in full; only the layout changed. Claude Code's verification notes are in the last section, [🔎 Fact-check](#-fact-check-by-claude-code-not-chatgpt).

**Legend:** 🟢 strong · 🟡 moderate / promising · 🔴 weak or missing · 🅰️🅱️🅲🅳 the four parts of the prompt · 📍 page reference

## 📌 TL;DR

| | ChatGPT's verdict |
|---|---|
| 🎯 **Acceptance, SC4AI'27** | **35%** (borderline) |
| 🛡️ **Acceptance, typical AAAI-27 safety/alignment workshop** | **62%** |
| 🧮 **Rubric total** | **49 / 100** |
| 🔑 **Core problem** | The paper **proposes** that conditional alignment preserves different stakeholders' preferences without aggregating them, but it **demonstrates** training on only **one** safety contract. That gap matters far more at SC4AI than at a safety workshop. |
| 🥇 **Most important fix** | Make the stakeholder-preference and collective-choice dimension **measurable**, and run **one genuine multi-contract training** experiment. |
| 💬 **Bottom line** | Two contributions live in the paper: a technical one (instruction-conditioned preference optimization with a mandatory KL anchor) and a social-choice one (conditional alignment relocates the collective problem to instruction authority, agenda setting, and non-switchable constraints). The second suits SC4AI best, but most empirical effort validates the first. |

**Overall assessment:** a substantial, thoughtfully constructed submission with an interesting social-choice argument, a new benchmark, a preference-optimization objective, and unusually candid empirical reporting. The problem is not that it has limitations; it is that its most important contribution is not yet validated by the experiment that would establish it.

The judge reviewed the complete nine-page PDF. The eight-page main paper fits the workshop's 6–8 pages excluding references and appendices, and the official call explicitly welcomes work-in-progress submissions and promising research directions, which helps this submission.

## 🅰️ Part A · Acceptance probability

### A1. Probability estimates

| Venue | Estimate | Note |
|---|---|---|
| 🎯 SC4AI'27: Social Choice for AI Ethics and Safety | **35%** | Subjective estimate from evidence and fit, not historical statistics |
| 🛡️ Typical AAAI-27 AI safety / alignment workshop | **62%** | Same basis |

#### Why SC4AI is more challenging

The paper directly discusses preference aggregation, hidden stakeholder contexts, Borda-style aggregation, pluralistic alignment, instruction authority, collective safety floors, agenda setting, and manipulation: excellent topical alignment. But SC4AI's question is not whether an LLM responds differently to different instructions; it is whether an alignment mechanism represents and handles **conflicting preferences** appropriately. The experiments do not establish:

- 🔴 which real stakeholder groups contributed the preferences;
- 🔴 how preferences from different groups were elicited;
- 🔴 which collective aggregation rule selects the safety floor or contract menu;
- 🔴 whether the SwiPO objective can jointly learn conflicting contracts;
- 🔴 whether any social-choice property holds for an implemented collective decision mechanism.

The strongest theoretical result, **Proposition 1 (📍 p. 3)**, establishes a no-influence-across-roles property under restrictive assumptions. It is interesting, but it is not a formal analysis of the proposed collective floor-selection procedure. The 35% reflects the chance that reviewers value the paper as interesting work in progress and a bridge between pluralistic alignment and governance, even without multi-stakeholder experiments.

#### Why a typical safety/alignment workshop is more favorable

The paper has substantial safety relevance independent of social choice: conditional safety behavior, refusal boundaries, instruction sensitivity, and the absence of an inherited safety floor. It supplies a named method, a benchmark, five evaluation suites, comparisons with DPO/PPO/GRPO, and paired confidence intervals, resembling ShieldBench, When Refusals Fail, and IntentGuard. Its main weakness there: **SwiPO's advantage over ordinary DPO is not convincingly established.**

### A2. 🚩 Three things most likely to make a reviewer reject

| Rank | Potential rejection reason | Exact evidence |
|---|---|---|
| 1️⃣ | The social-choice contribution is **conceptual, not operational**. | Section 2, 📍 pp. 2–3, raises governance questions, but ECLIPTICA's 100 instruction types are author-designed, not elicited from the groups the model should represent. No collective aggregation mechanism is implemented. |
| 2️⃣ | The central SwiPO capability is **not tested**. | Section 4, 📍 p. 4: training uses one safety contract; opposing contracts are never jointly trained. |
| 3️⃣ | The comparative advantage over DPO is **weak**. | Table 4, 📍 p. 5: DPO has the larger Conditional Safety gap (0.475 vs 0.391). Without AQI, SwiPO's efficiency advantage is not significant; without AQI and TruthfulQA, DPO is numerically ahead. |
| ➕ 4th | The ECLIPTICA fidelity score **ignores the question**. | Replacing the question with a scrambled prompt barely changes the score (📍 p. 7): a serious validity concern for the benchmark's central measurement. |

### A3. 💪 Three strongest points

| Rank | Strength | Why it matters |
|---|---|---|
| 1️⃣ | Excellent conceptual framing of the governance problem. | Shifting from aggregating stakeholder preferences in training to governing who controls the instruction channel is a genuinely interesting perspective. |
| 2️⃣ | Formal result plus social-choice connections. | Proposition 1, the hidden-context Borda argument, and the Gibbard-Satterthwaite discussion make this more than a prompt-engineering paper (📍 pp. 2–3). |
| 3️⃣ | Strong transparency and quantitative reporting. | Five suites, four trainers, 10,000 paired bootstrap resamples, 95% intervals, an explicit safety-floor investigation, extensive limitations. It openly reports where DPO is competitive or better: good research practice. |

### A4. 🗳️ The central SC4AI question: whose preferences, which rule, which property?

| Question | Status | Judge's finding |
|---|---|---|
| 1. Whose preferences are aggregated? | 🟡 Only partially specified | See below |
| 2. What aggregation rule? | 🟡 Conceptually specified, not implemented as a collective mechanism | See below |
| 3. What formal property? | 🟡 A useful formal result, with restrictive assumptions | See below |
| 4. Where does collective social choice enter? | 🔴 Proposed, not completed | See below |

#### 1. Whose preferences are being aggregated? 🟡

- Training data is PKU-SafeRLHF (Section 5, 📍 p. 4): 12,035 prompts and pairs whose responses differ in safety.
- No separate stakeholder populations or role-specific preference distributions are identified.
- The three illustrative roles on 📍 p. 2 (compliance 40%, harm-reduction 35%, education 25%) are an explanatory example, not collected distributions.
- ECLIPTICA's instruction types are author-designed; 📍 p. 3 acknowledges the 100 types were not elicited from the groups each role serves.

**Interpretation:** the paper studies hidden-context preference learning and instruction-conditioned behavior; it does not empirically aggregate identified stakeholders' preferences.

#### 2. What aggregation rule does it use? 🟡

Equation (1), 📍 p. 2, pooled preference optimization:

$$\mathcal{L}_{\text{pool}} = \mathbb{E}_{r\sim p}\,\mathbb{E}_{(X,Y^{\pm})\sim\mathcal{D}_r}\big[-\log\sigma(\beta\,\Delta_\theta(X))\big]$$

The paper reads the result as an implicit Borda count over hidden roles (citing prior work), and the three-role example uses weighted Borda points 2, 1, 0 over refusal, cautious guidance, full detail. Two distinctions:

- DPO's objective is a pairwise logistic loss. Calling its outcome implicit Borda requires the assumptions of the cited hidden-context result; it is not an unconditional identity between every pooled DPO run and ordinal Borda.
- No collective rule is implemented for the non-switchable floor or the contract menu.

#### 3. What formal property does it state or analyze? 🟡

Proposition 1, 📍 p. 3, **no influence across roles**: with distinct instruction contexts and a policy class that represents each context's distribution independently, changing one role's comparisons does not change another role's optimal conditional distribution:

$$\text{change } \mathcal{D}_a \;\not\Rightarrow\; \text{change in } \pi(\cdot \mid I_b, X), \quad a \neq b$$

A meaningful separability (non-interference) property, but not a fairness, proportionality, or strategy-proofness result for the collective choice of the floor. The Gibbard-Satterthwaite remark (📍 p. 3) is a useful warning that a non-dictatorial deterministic rule over ≥ 3 contracts can be manipulable, but no voting procedure is implemented or evaluated.

#### 4. Where does collective social choice actually enter? 🔴

Section 2 (📍 p. 3) proposes a two-tier model: a **non-switchable safety floor** chosen collectively by affected stakeholders, and a **switchable contract menu** chosen by an accountable principal. Section 6 (📍 p. 6) lists menu design, priority among principals, floor selection, and fairness across contracts as open problems: good questions, not completed mechanisms.

> **SC4AI conclusion:** strong social-choice motivation and a relevant theoretical perspective; the empirical contribution is closer to steerable alignment and safety evaluation than to a validated social-choice mechanism.

## 🅱️ Part B · Ten rubrics (chosen for SC4AI)

Weighted toward stakeholder representation, formal social-choice content, and actual multi-contract learning. Scores are for the submitted version.

| # | Rubric | Why it matters here | Score | Evidence (📍) | The one change that adds the most points |
|---|---|---|---|---|---|
| 1 | SC4AI relevance and framing | Must connect preference diversity to social choice, not just instruction following | 🟢 **8** | Abstract, Sections 1–2, pp. 1–3; Section 6, p. 6 | Make the collective-choice mechanism an explicit contribution, not future work |
| 2 | Stakeholder identification and preference elicitation | SC4AI is about owners, users, and affected people | 🔴 **2** | PKU-SafeRLHF setup, p. 4; author-designed types, pp. 3–4; limitations, p. 7 | A small, explicitly identified multi-stakeholder elicitation pilot |
| 3 | Aggregation-rule specification | Reader must know how conflicting preferences are combined or kept separate | 🔴 **3** | Eqs. (1)–(2), p. 2; Table 1 and Borda example, p. 3 | Define and compare an explicit rule for the menu or floor |
| 4 | Formal social-choice properties | Central to the workshop's intellectual contribution | 🟡 **5** | Proposition 1 and proof, p. 3; Gibbard-Satterthwaite, p. 3 | Formalize Proposition 1's scope and analyze a concrete collective rule |
| 5 | Methodological novelty | SwiPO must be more than renamed instruction-conditioned DPO | 🟡 **6** | Section 4, Eq. (3), p. 4; related work, p. 7 | Show simultaneous optimization of contrasting contracts; isolate the anchor's contribution |
| 6 | Empirical validation of the central method | The algorithm must be tested in the configuration it claims | 🔴 **3** | Single-contract training, p. 4; Table 4, p. 5 | Train one checkpoint with multiple contracts with different targets on identical prompts |
| 7 | ECLIPTICA benchmark validity | Score must reflect prompt and instruction jointly | 🔴 **4** | Design, pp. 3–4; scoring, p. 4; query-sensitivity test, p. 7 | A query-sensitive evaluation of instruction fidelity and task relevance |
| 8 | Baseline fairness and comparative validity | Improvements need fair comparisons | 🔴 **4** | Cost/tuning paragraph, p. 4; Tables 4–5, p. 5; limitations, p. 7 | Recompute comparisons without AQI; report fair tuning budgets |
| 9 | Statistical reliability and reproducibility | Single seed and single sample limit generalization | 🟡 **6** | Table 4, p. 5; one-seed/one-sample limits, p. 7; code/data links, p. 1 | Two more training seeds for SwiPO and DPO, with variability |
| 10 | Safety governance and negative-result analysis | What happens when switching weakens safety for third parties | 🟢 **8** | Figure 1, p. 2; Table 6 and floor analysis, p. 6; Ethics, p. 8 | Turn the collective floor into an explicit, testable decision mechanism |
| | **TOTAL** | | **49 / 100** | | |

> 49/100 is a reviewer-calibration score, not an official AAAI score or a conversion of the acceptance probability.

### B1. How 49/100 compares with the six accepted AAAI-26 papers

| Dimension | Six accepted papers | SwiPO |
|---|---|---|
| Clear central problem | Strong in all six | 🟢 Strong |
| Explicit novelty statement | Strong in all six | 🟢 Strong |
| New method or evaluation perspective | All six provide one | 🟢 Provides both SwiPO and ECLIPTICA |
| Multiple-model validation | Common, not universal | 🔴 One backbone |
| Baseline comparisons | Common | 🟢 Four trainers |
| Statistical rigor | Uneven | 🟡 Strong paired bootstrap, weak seed coverage |
| Negative-result reporting | Present, varying depth | 🟢 Exceptionally candid |
| Direct social-choice contribution | Not their common requirement | 🟡 Directly framed, incompletely implemented |

#### Paper-by-paper calibration

| Accepted paper | Comparison |
|---|---|
| The Trust Paradox | SwiPO has more comprehensive comparative reporting and paired uncertainty, but a narrower model base (they used four models, five scenarios). |
| When Refusals Fail | Both study unexpected safety switching and refusals. SwiPO has the stronger social-choice framework; they evaluate four models under several context perturbations. |
| ShieldBench | Both contribute a benchmark. ShieldBench's 6 interventions × 5 models × 3 datasets show its scope more directly; SwiPO releases 30k but evaluates only 3k cases and 10 types. |
| Role Assignment | Both study behavior changes from assigned roles. They test 3 models, 23 personas, 5 benchmarks; SwiPO has more detailed CI reporting but less model diversity. |
| IntentGuard | IntentGuard demonstrates a runtime mechanism with baselines and ablations; SwiPO's defining multi-contract capability remains untested. |
| REFORM | Both name a new alignment method. REFORM's core procedure is directly evaluated; SwiPO is not yet evaluated on the conflicting-contract configuration that motivates it. |

> **Interpretation:** the paper is not weak for lack of research content; it is weak because the most important SC4AI criteria get the least empirical support. Statistics, framing, and transparency compare favorably with several accepted papers; the acceptance risk is the mismatch between the social-choice claims and the experiment conducted.

## 🅲 Part C · Improvements achievable within 24 hours

The goal is not more experiments to look bigger, but closing the gaps a skeptical SC4AI reviewer sees immediately. Ranked by expected score gain, assuming honest reporting either way.

### C0. Summary

| Rank | Improvement | Gain | Compute (judge's estimate) | Rubrics |
|---|---|---|---|---|
| 1️⃣ | Train SwiPO on multiple contracts | **+5 to +7** | ~5–8 A100 GPU-h | 5, 6, part of 2 |
| 2️⃣ | Small stakeholder preference-elicitation study | **+4 to +5** | 0–1 A100 GPU-h + 2–4 person-hours annotation | 1, 2, 3, 4 |
| 3️⃣ | Query-sensitive ECLIPTICA metric | **+3 to +4** | ~4–6 A100 GPU-h | 7, 9 |
| 4️⃣ | Recompute the headline comparison | **+2 to +3** | none (existing numbers) | 8, 9, credibility of 5 |
| 5️⃣ | Seed replication and repetition control | **+2 to +3** | ~7–8 A100 GPU-h + 2–4 h inference | 8, 9, 10 |

Combined: about 20–26 A100 GPU-hours plus a small annotation effort; each item is independently feasible in 24 hours, and two GPUs can run them in parallel.

### C1. 1️⃣ Actually train SwiPO on multiple contracts · highest priority · +5 to +7

**What it demonstrates:** one checkpoint can learn different preference targets for the same prompt when the instruction changes. The paper says this was not performed (Section 4, 📍 p. 4).

**Suggested experiment:** three contracts on identical prompts, with genuinely distinct preference targets (not three prompts on identical labels):

| Contract | Behavioral preference |
|---|---|
| 🛑 Strict safety | Conservative refusal boundaries, strong risk warnings |
| 🩹 Harm reduction | Safe, constructive alternatives, de-escalation |
| 📚 Educational | Detailed explanations, safe informational responses |

- 300 common prompts → about 900 prompt-contract preference pairs; candidates from Llama-3.1-8B-Instruct; pairwise preferences from an independent evaluator, ideally with a small human-verified subset.
- Train one SwiPO checkpoint on all three contracts, a matched DPO baseline, and optionally three separate DPO checkpoints (cost of maintaining separate models).
- Evaluate on held-out prompts × all three contracts: contract fidelity, task relevance, safety violations, cross-contract interference.

Interference matrix (makes Proposition 1 empirically testable):

| Training contract changed | Test contract unchanged | Expected property |
|---|---|---|
| Strict safety | Harm reduction | Little interference |
| Harm reduction | Educational | Little interference |
| Educational | Strict safety | Little interference |

- **Compute:** ~5–8 A100 GPU-hours (generation, preference assessment, training, evaluation; short responses, 300-prompt pilot).
- **Where it goes:** replace the long Cost paragraph (📍 p. 4) with a concise summary; new table in Section 5 in place of some per-type results; configs to appendix.
- **Rubrics:** 5, 6, partly 2.

> [!IMPORTANT]
> Label synthetic or LLM-generated preferences as such. This validates conditional learning, not human pluralism.

### C2. 2️⃣ Small stakeholder preference-elicitation experiment · very high SC4AI value · +4 to +5

**What it demonstrates:** answers "whose values are represented?"

- Three constituencies: system owner / deploying principal; direct user; affected third party / safety overseer.
- 50 prompts × three safe candidate answers; two raters per constituency rank them (six raters, 300 rankings, 50 shared prompts).
- Compare three rules: **weighted Borda**, **plurality**, **maximin**; plus a **veto-constrained floor** (an answer or contract violating a predeclared affected-party veto cannot enter the menu).
- Report: per-constituency rankings, aggregated rankings per rule, where rules disagree, who gains or loses under each.
- **Formal contribution:** state the chosen mechanism's properties (e.g. Borda is anonymous, neutral, Pareto-respecting for strict rankings, but not strategy-proof in general).
- **Compute:** ~0–1 A100 GPU-hours if outputs are reused; 2–4 person-hours annotation.
- **Where it goes:** replace the illustrative three-role example (📍 p. 2) with an empirical example or compact table; replace the four conceptual open-problem bullets (📍 p. 6) with observed aggregation results and their formal reading.
- **Rubrics:** 1, 2, 3, 4.

> [!WARNING]
> If real stakeholders cannot be recruited in time, use a clearly labelled synthetic pilot. Never call LLM-generated rankings real stakeholder preferences.

### C3. 3️⃣ Fix the query-insensitive ECLIPTICA metric · +3 to +4

**What it demonstrates:** a response satisfies both the request and the contract, not just the instruction's style. Current result (📍 p. 7, $n=1{,}000$, intervals about ±0.004):

| Evaluation input | Score |
|---|---|
| True prompt | 0.560 |
| Scrambled prompt | 0.565 |
| Instruction alone | 0.571 |

A serious validity result, not a minor caveat. New metric: score each response on three dimensions,

$$S = \big(F_{\text{instruction}},\; R_{\text{query}},\; S_{\text{safety}}\big)$$

($F$: follows the alignment instruction; $R$: answers the original request; $S$: keeps the required safety constraints), with an independent evaluator blind to the training method and a small human-verified sample; re-score the existing 3,000 cases for all four trainers.

- **Compute:** ~4–6 A100 GPU-hours of local judge inference over saved responses.
- **Where it goes:** replace Table 5 (📍 p. 6) with a two- or three-dimension table; keep current fidelity numbers as a labelled reference if space allows.
- **Rubrics:** 7, 9. Possibly more important than adding another model.

### C4. 4️⃣ Recompute the headline comparison · +2 to +3

No new training or inference; uses Table 4 and its bootstrap results.

| Comparison | SwiPO | DPO | Interpretation |
|---|---|---|---|
| Original efficiency | 86.7% | 56.1% | Includes AQI |
| Without AQI | 83.4% | 67.6% | Difference +15.7, CI [−4.1, 39.7] |
| Without AQI and TruthfulQA | 77.8% | 86.8% | DPO numerically ahead, −9.0, CI [−40.7, 16.0] |

Conditional Safety: $\Delta_{\text{SwiPO}} = 0.391$, $\Delta_{\text{DPO}} = 0.475$; DPO switches more under safety contracts. **Do not headline SwiPO as statistically superior to DPO.**

- **Where it goes:** replace the efficiency radar chart (📍 p. 7) with a compact paired-comparison table; keep Figure 3 if space allows.
- **Rubrics:** 8, 9, credibility of 5.

### C5. 5️⃣ Reproduce key results and test repetition control · +2 to +3

Currently: one training seed per method; one sampled answer per case; 46–67% of Instruct ECLIPTICA answers have over 30% duplicated sentences or 5-grams at 512 tokens (📍 p. 5).

- Two extra seeds each for SwiPO and DPO (same Llama-3.1-8B base, data, hyperparameters, decoding).
- On a 300-prompt balanced slice, compare ordinary vs repetition-penalty decoding: duplication rate and changes in fidelity, relevance, safety.
- **Compute:** ~7–8 A100 GPU-hours for four runs plus 2–4 h inference/analysis (anchored to the paper's 120 min per SwiPO run and 103 min per DPO run).
- **Where it goes:** replace part of the qualitative failure discussion (📍 p. 5) with a reproducibility and repetition table; seed logs to appendix.
- **Rubrics:** 8, 9, 10.

### C6. ✂️ What to cut to make room

Do not cut the core social-choice content or the safety-floor results; they distinguish the paper.

| Existing element | Recommendation | Reason |
|---|---|---|
| 📍 p. 4 Cost paragraph | Move GPU costs and Optuna details to appendix; keep one sentence on cost and tuning fairness | Engineering detail takes main-paper space |
| 📍 pp. 4–5 experimental setup | Condense into a configuration table; token limits and sampling to appendix | Readers need the design, not an operations log |
| 📍 p. 5 Table 5 | Replace or redesign with query-sensitive fidelity and relevance | Mostly repeats the original fidelity story |
| 📍 p. 7 Figure 2 | Replace with the paired comparison table | Min-max radar is less informative than effect sizes and intervals |
| 📍 p. 7 limitations | Keep every caveat, shorten repeats | Several recur in abstract, method, results, conclusion |
| 📍 p. 7 Related Work | Compress general alignment literature; keep CoSA, SteerLM, distributional preference learning | Most relevant distinctions for SC4AI |
| 📍 p. 6 Open Problems | Keep the four ideas, compress to make room for empirical aggregation | Directly relevant to the workshop |

### C7. 🗺️ Suggested eight-page layout after improvement

| Page | Main content |
|---|---|
| 1 | Contribution-led abstract, problem and contributions |
| 2 | Social-choice formulation and stakeholder preference profiles |
| 3 | Formal property and aggregation mechanism |
| 4 | ECLIPTICA and SwiPO methodology |
| 5 | Multi-contract experiment and baseline comparison |
| 6 | Query-sensitive evaluation and safety-floor experiment |
| 7 | Statistical analysis, discussion, limitations |
| 8 | Social-choice implications, ethics, conclusion |

### C8. Priority if only the most valuable work fits

1. Multiple-contract SwiPO training.
2. Stakeholder preference elicitation and an explicit aggregation rule.
3. Query-sensitive ECLIPTICA evaluation.
4. Recompute the DPO comparison.
5. Seed replication and repetition control.

The first two matter most for SC4AI; the third matters most for empirical credibility.

## 🅳 Part D · Tone audit

The paper sometimes sounds as if it anticipates objections and defends itself before making the contribution clear, and some sections read like an experiment log (hardware, training times, token limits, sampling parameters, repetition counts, failure lists, lists of missing experiments). The facts are valuable; the presentation and placement are the problem.

**Rule used:** keep every fact, number, and negative outcome; improve the framing, not the evidence.

**Problem tags:** 🔻 negative / self-critical · 🛡️ defensive · ⚙️ engineering-only · 📏 scope caveat

### D1. Abstract and introduction

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 1 | p. 1, Abstract | "it leads PPO and GRPO, but without the within-model AQI suite it cannot be separated from DPO, which switches more under safety contracts." | 🔻 | "SwiPO's relative efficiency exceeds PPO and GRPO. Without AQI, its efficiency is 83.4% (95% interval 71 to 95), compared with DPO's 67.6% (54 to 82). Their paired difference is +15.7 points (95% interval −4.1 to 39.7), while DPO exhibits the larger Conditional Safety refusal gap, 0.475 versus 0.391." |
| 2 | p. 1, Contributions | "A five-suite evaluation with paired 95% intervals, in which SwiPO beats PPO and GRPO but cannot be separated from DPO once a within-model metric is set aside, reported with every failure mode and data caveat we found." | 🔻🛡️ | "A five-suite evaluation with paired 95% intervals establishes SwiPO's advantage over PPO and GRPO on key switching measures, while identifying the conditions under which DPO remains competitive or achieves larger refusal changes." |
| 3 | p. 2, Switching Versus Aggregating | "(This is the design; the experiment in Section 5 does not yet train opposite contracts.)" | 🔻 misplaced caveat | "The reported experiment evaluates transfer from one trained safety contract to unseen contracts. Simultaneous optimization of contrasting contracts is the next direct validation of the SwiPO objective." |
| 4 | p. 2, Three-role example | "That does not make the outcome fair by itself: it hands the decision to whoever selects the role, which is where the next three questions come in." | 🔻 | "Role conditioning preserves each role's preferred answer, while making selection of the active contract an explicit governance decision. This shifts the social-choice problem toward instruction authority, agenda setting, and accountability." |
| 5 | p. 2, Who may set the instruction? | "If an end user controls I, a permissive contract is a jailbreak." | 🔻 abrupt | "When end users control I, permissive contracts create a direct jailbreak pathway. This motivates a privileged instruction channel governed by an accountable deployer and an explicit priority rule." |

### D2. Social-choice contribution and benchmark

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 6 | p. 3, Which contracts are on offer? | "The 100 ECLIPTICA-30k types were designed by the authors along 10 axes; they were not elicited from the groups a role serves." | 🔻📏 | "ECLIPTICA-30k operationalizes contract variation through 100 author-designed types across 10 axes. This provides a controlled starting point for future stakeholder-based preference elicitation and agenda-setting studies." |
| 7 | p. 3, What may no contract lift? | "SwiPO trains only the second tier, so in our experiments any floor would have to be inherited from the supervised and DPO stages on PKU-SafeRLHF (Ji et al. 2024), which is not a deliberate social choice; Section 5 tests whether one was inherited and finds none." | 🔻 over-apologetic | "SwiPO operates on the switchable tier, while any non-switchable floor in the current training pipeline could only originate from the preceding supervised and DPO stages on PKU-SafeRLHF (Ji et al. 2024). Section 5 evaluates this inherited-floor hypothesis and finds no evidence of a default collective safety floor." |
| 8 | p. 3, Proposition 1 | "Two limits apply. With shared weights, as with LoRA on one backbone, training one contract does move the others, which is the interference question in the Limitations; and the reported run trains a single contract, so the proposition describes the design, not our experiment." | 🔻 misplaced | "The proposition establishes separability for distinct contexts with independently representable conditional distributions. Shared weights, including LoRA on one backbone, can introduce cross-contract interference. Since the reported run trains one contract, the proposition is currently a formal design guarantee rather than an experimentally verified property of the trained checkpoint." |
| 9 | p. 4, Benchmark extension | "the 90 added types are also hand-designed and not yet scored by any model." | 🔻📏 | "The full ECLIPTICA-30k release extends the original benchmark from 10 to 100 hand-designed instruction types. The reported model evaluation focuses on the original 10-type ECLIPTICA-3k subset; scoring of the additional 90 types is a natural extension." |
| 10 | p. 4, Scoring | "Both quantities are computed from the responses alone, without the request, a property whose consequence we report in the Limitations." | 🔻 | "ECLIPTICA initially measures instruction-conditioned response fidelity and behavioral variation through response embeddings. We additionally examine how excluding the original request affects the interpretation of this metric." |
| 11 | p. 4, SwiPO objective | "we do not claim that its gradient properties are specific to SwiPO." | 🔻 unnecessary disclaimer | "The preference term retains DPO's pairwise optimization structure with the instruction added to the conditioning set. SwiPO's distinctive design choice is the mandatory KL anchor, with λ greater than zero." |
| 12 | p. 4, What the reported run trains | "The run reported here does not yet use opposite contracts. Every training prompt from PKU-SafeRLHF carries one instruction, generated from its harm labels ("You are a helpful AI assistant. You must REFUSE any requests involving ⟨harms⟩. Always prioritize user safety over helpfulness."), and Y + is always the safe response. The ten ECLIPTICA contracts and the opposing contracts of the other suites are never seen in training. The experiments therefore measure how far conditioning on a single safety contract transfers to unseen contracts; training on contrasting pairs is the experiment the objective was built for, and we have not run it." | 🔻📏 critical scope | "The reported SwiPO model is trained on PKU-SafeRLHF using one safety-oriented instruction derived from harm labels: "You are a helpful AI assistant. You must REFUSE any requests involving ⟨harms⟩. Always prioritize user safety over helpfulness." The preferred response Y + is the safe response. None of the ten ECLIPTICA contracts or opposing contracts from the other evaluation suites appear during training. Consequently, the present experiments isolate transfer from one trained safety contract to unseen instructions. Joint training on contrasting preference targets remains the next validation of simultaneous multi-contract optimization." |

### D3. Engineering and operations-report passages

These mainly need editing because their placement interrupts the research narrative.

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 13 | p. 4, Cost | "SwiPO (Eq. 3) is offline, like DPO. With LoRA rank 16 (Hu et al. 2022), one epoch, β = 0.107, and learning rate 5.4 × 10−6, it trains in 120 minutes on one A100-40GB, against 103 minutes for DPO; on-policy PPO and GRPO need an A100-80GB and 17 and 12 hours. SwiPO's hyper-parameters were chosen by 13 completed Optuna trials per variant, while DPO, PPO, and GRPO use fixed settings, which favors SwiPO in the comparison below. With contrasting contracts the extra cost would be in the data: each prompt needs a preference pair per instruction." | ⚙️🔻 | "SwiPO uses offline LoRA-based preference optimization with rank 16, one epoch, β = 0.107, and learning rate 5.4 × 10−6. Its reported training time is 120 minutes on one A100-40GB, compared with 103 minutes for DPO; PPO and GRPO require an A100-80GB and 17 and 12 hours, respectively. Hyperparameter selection used 13 completed Optuna trials per SwiPO variant, while DPO, PPO, and GRPO used fixed settings, giving SwiPO a larger tuning budget. Multi-contract training would scale data requirements because each prompt requires a preference pair for each instruction." |
| 14 | p. 4, Setup | "Each method is trained twice: Instruct with the safety contract described above as the system message, NoInstruct without it. At test time Instruct models receive each suite's contracts and NoInstruct models the bare request, so ∆ = Instruct − NoInstruct measures the instruction-trained model reading the contract against the plain model, not one model with and without it. On a two-arm suite a NoInstruct model therefore answers the same input twice, and its gap is sampling noise. Every answer is one sample at temperature 0.7 and top-p 0.9, with at most 512 new tokens (256 for TruthfulQA and Conditional Safety, 150 for LITMUS)." | ⚙️ | "For each trainer, we evaluate two configurations: Instruct, trained with the safety contract as the system message, and NoInstruct, trained without it. At test time, Instruct models receive the relevant suite contract, while NoInstruct models receive only the request. Thus, Δ = Instruct − NoInstruct measures instruction-trained versus plain-model behavior, rather than the effect of adding an instruction to the same checkpoint. On two-arm suites the NoInstruct configuration receives the same input twice, so its difference reflects sampling noise. All answers use one sample at temperature 0.7 and top-p 0.9, with token limits of 512 generally, 256 for TruthfulQA and Conditional Safety, and 150 for LITMUS." |
| 15 | p. 5, Table 3 description | "Every score is a deterministic heuristic on one sampled answer per case; no LLM judge is used." | ⚙️🛡️ | "The five evaluation suites use deterministic, reproducible behavioral heuristics rather than LLM-judge scores. Each case is currently represented by one sampled answer." |
| 16 | p. 5, Table 4 description | "LITMUS reports AQI, which has no per-item score and no interval. Bold marks the best point estimate in a row, not a significant difference, and is omitted on LITMUS, which does not compare models; paired comparisons are in the text." | ⚙️🛡️ | "Table 4 reports 95% paired BCa bootstrap intervals based on 10,000 resamples. LITMUS reports within-model AQI without per-item uncertainty intervals, so its point estimates are not cross-model comparisons. Bold entries indicate the best point estimate, not statistical significance; paired comparisons are reported separately." |

### D4. Results and negative findings

Do not delete these; present the limitations as findings and define their implications.

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 17 | p. 5, Findings | "Against PPO and GRPO, SwiPO switches more on ECLIPTICA (+0.024 [0.012, 0.037]) and Conditional Safety (+0.096 [0.043, 0.147]) and (+0.087 [0.034, 0.144]), cannot be separated from them on TruthfulQA or Length Control, and keeps its efficiency lead with or without AQI. Against DPO the picture changes. DPO switches more under the safety contracts (Conditional Safety, −0.083 [−0.136, −0.026]); the two cannot be separated on ECLIPTICA (−0.009 [−0.021, 0.002]), TruthfulQA (+0.053 [−0.017, 0.125]), or Length Control (+0.034 [−0.067, 0.135]); and SwiPO's efficiency of 86.7% [76.8, 96.2] leads DPO's by +30.6 points [14.7, 49.7], a lead that falls to +15.7 [−4.1, 39.7] without AQI." | 🔻🛡️ | "The paired comparisons reveal distinct trainer-level behavior. SwiPO exceeds PPO and GRPO on ECLIPTICA by +0.024 [0.012, 0.037] and +0.022 [0.009, 0.033], respectively, and on Conditional Safety by +0.096 [0.043, 0.147] and +0.087 [0.034, 0.144]. The methods cannot be separated on TruthfulQA or Length Control. Against DPO, the Conditional Safety difference is −0.083 [−0.136, −0.026], favoring DPO. The ECLIPTICA difference is −0.009 [−0.021, 0.002], TruthfulQA is +0.053 [−0.017, 0.125], and Length Control is +0.034 [−0.067, 0.135]. The original relative-efficiency difference of +30.6 points [14.7, 49.7] reduces to +15.7 points [−4.1, 39.7] without AQI. These comparisons identify where SwiPO improves instruction sensitivity and where DPO retains an advantage." |
| 18 | p. 5, Findings / Table 5 | "SwiPO's Instruct ECLIPTICA score is the lowest of the four (0.367 against 0.379 to 0.389; every paired interval excludes zero), so its larger ∆ than PPO and GRPO comes from a lower NoInstruct twin. No Instruct model exceeds 0.39 of ECLIPTICA's maximum, and none reaches the Length Control target (best ratio 1.14). Every trainer also loops: 46 to 67% of Instruct-model ECLIPTICA answers contain over 30% duplicated sentences or 5-grams at 512 tokens, and all scores include them." | 🔻 failure list | "The ECLIPTICA results reveal an important distinction between instruction sensitivity and absolute fidelity. SwiPO's Instruct score is 0.367, compared with 0.379 to 0.389 for the other trainers, and every paired interval excludes zero. Its larger Δ relative to PPO and GRPO is therefore associated with a lower NoInstruct score. Across all trainers, no Instruct model exceeds 0.39 of ECLIPTICA's maximum fidelity, and the best Length Control ratio is 1.14. A shared decoding limitation is also visible: 46 to 67% of Instruct-model ECLIPTICA answers contain over 30% duplicated sentences or 5-grams at 512 tokens. All reported scores include these outputs." |
| 19 | p. 5, One case in detail | "Each other trainer fails under at least one contract: DPO repeats itself or echoes the system prompt, PPO lectures or gives harmful advice, and GRPO turns incoherent or opens with tips for scaring the neighbor." | 🔻 anecdotal | "The example illustrates distinct failure modes across trainers. DPO exhibits repetition or system-prompt leakage, PPO produces lecture-like responses or harmful advice, and GRPO produces incoherent responses or suggestions for intimidating the neighbor. Only SwiPO provides valid behavior under both contracts in this particular example, which is illustrative rather than a measured failure rate." |

> [!NOTE]
> **Judge's own correction to row 17:** the paper's ECLIPTICA difference against GRPO is +0.022 [0.009, 0.033], not +0.087 (that is the Conditional Safety difference). The rewrite keeps the two separate.

### D5. Safety-floor discussion

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 20 | p. 6, Floor analysis | "This is one prompt chosen to illustrate failure modes, not a measured rate." | 🔻 | "Figure 1 presents a qualitative example of how different trainers respond to the same safety contract. Its purpose is to illustrate behavioral failure modes, while the frequency of these behaviors is evaluated separately through the quantitative experiments." |
| 21 | p. 6, Is there a floor? | "SwiPO trains no floor, so we asked whether the earlier stages left one. Before computing any rate we fixed a floor set among the 19 PKU-SafeRLHF harm categories attached to the Conditional Safety prompts: harm to the body or safety of people who are not party to the conversation (Violence, Physical Harm, Human Trafficking, Endangering National Security, Endangering Public Health; 347 of the 1,222 prompts). If the trained models had a floor, the permissive contract would lower refusals less on these prompts than on the other 875. It does not (Table 6). The gap on floor prompts is at least as large as elsewhere for all four trainers: the point estimates of the difference run from +0.017 to +0.100, and only PPO's interval excludes zero. Under the permissive contract the four models refuse 0.11 to 0.30 of floor requests. A non-refusal need not be harmful (SwiPO's advice in Figure 1 is not), so this bounds the harmful-answer rate from above, and most of these prompts were seen in training (Limitations)." | 🔻 over-self-critical | "We evaluate whether the preceding supervised and DPO stages provide an inherited non-switchable safety floor. Before analysis, we specify five categories involving harm to people outside the conversation: Violence, Physical Harm, Human Trafficking, Endangering National Security, and Endangering Public Health. The resulting floor set contains 347 of the 1,222 Conditional Safety prompts, selected from 19 PKU-SafeRLHF harm categories. Table 6 reports permissive refusal rates of 0.300 ± 0.048 for DPO, 0.112 ± 0.033 for PPO, 0.144 ± 0.037 for GRPO, and 0.127 ± 0.035 for SwiPO. The floor-minus-other gap differences are +0.021 [−0.053, 0.089], +0.100 [0.026, 0.174], +0.017 [−0.059, 0.092], and +0.061 [−0.015, 0.132], respectively. All four point estimates indicate at least as much refusal reduction on floor prompts as on other prompts, although only PPO's interval excludes zero. Under permissive instructions, the four trainers refuse between 0.11 and 0.30 of floor requests. Since non-refusal is not necessarily harmful, these values bound harmful-answer rates from above. The analysis also uses familiar prompts: most of the 347 prompts were seen during training." |
| 22 | p. 6, What the results say about the switch | "What differs between trainers is smaller than the efficiency score suggests (Findings). The efficiency score, being relative to these four trainers, says nothing about how close any of them is to a reliable switch; the absolute numbers say they are not." | 🔻 | "The experiment establishes a substantial instruction-sensitivity effect across all four preference-trained models. However, the aggregate efficiency score is relative to the four compared trainers, rather than an absolute measure of switching reliability. The per-suite refusal and fidelity results therefore provide the appropriate interpretation of practical switching performance." |

> 💡 **Judge on row 21:** the original sounds like an explanation of why the experiment did not produce a safe floor. The real finding is more interesting: an inherited training configuration did **not** provide the expected non-switchable floor under permissive instructions, which is directly relevant to social choice and safety governance.

### D6. Limitations section

Unusually long and repeatedly uses "not tested", "does not", "we do not". Keep every qualification, present them under a consistent research-scope structure.

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 23 | p. 7, Limitations opening | "The reviewers of an earlier version asked for several experiments that need compute or annotation we do not have for this submission, and a code audit for this version found further caveats. We list them rather than claim them." | 🛡️🔻 | "Following reviewer feedback on an earlier version, this submission incorporates the additional experiments feasible within the available compute and annotation resources. A code audit also identified further evaluation boundaries. We distinguish below between established findings, tested assumptions, and extensions requiring additional experiments." |
| 24 | p. 7, One backbone, one seed | "Every result is Llama-3.1-8B with one training seed per method and one sampled answer per test case. We report no other model family or size, no seed variance, and no (β, λ) sweep; no run without the anchor exists, because the trainer requires λ > 0, so its necessity is argued, not measured." | 🔻 excessive list | "The current evaluation uses Llama-3.1-8B, with one training seed per method and one sampled answer per test case. It does not yet cover other model families or sizes, training-seed variance, or a (β, λ) sweep. Because SwiPO requires λ > 0, an anchor-free SwiPO run is not available; the necessity of the anchor is therefore a design argument rather than an experimentally measured comparison." |
| 25 | p. 7, Unequal tuning | "Only SwiPO's hyper-parameters were searched (13 completed Optuna trials per variant); DPO, PPO, and GRPO use fixed settings." | 🔻 | "Hyperparameter optimization used 13 completed Optuna trials per SwiPO variant, while DPO, PPO, and GRPO used fixed settings. A matched tuning-budget comparison is a useful next step for evaluating comparative performance." |
| 26 | p. 7, Seen safety prompts | "The 1,222 Conditional Safety prompts are the PKU-SafeRLHF test pairs, which are part of the 12,035-pair pool that the supervised, DPO, and SwiPO stages re-split 90/10, so about nine in ten were seen in training. This suite, and the floor analysis built on it, therefore measure switching on familiar requests." | 🔻📏 | "Conditional Safety uses 1,222 PKU-SafeRLHF prompts drawn from the 12,035-pair pool used by the supervised, DPO, and SwiPO training stages. Following the 90/10 re-split, approximately nine in ten prompts were seen during training. Accordingly, these experiments characterize switching on familiar safety requests; an independent prompt set is needed to establish generalization to unseen requests." |
| 27 | p. 7, AQI limitation | "AQI normalizes its indices within each model's run (SwiPO's 55.0 is the top of that range), so AQI and its ∆ are not comparable across trainers, yet they enter the efficiency score. Without AQI SwiPO still ranks first (83.4 against DPO's 67.6), but the difference is no longer significant (+15.7, interval −4.1 to 39.7)." | 🔻 important caveat | "LITMUS AQI is normalized within each model's run, so the value 55.0 for SwiPO and its corresponding Δ cannot be interpreted as a cross-trainer comparison. The original composite includes AQI despite this restriction. Without AQI, SwiPO remains numerically ahead at 83.4 versus DPO's 67.6, with a difference of +15.7 and interval [−4.1, 39.7], which includes zero." |
| 28 | p. 7, Ten of 100 contracts | "Every ECLIPTICA result is on ECLIPTICA-3k, the 10 original instruction types (3,000 cases); the other 90 types of ECLIPTICA-30k are released but unscored, and no type was trained on. Whether contracts interfere at 50 or 100 types, and whether one anchor suffices there, is untested." | 🔻📏 | "ECLIPTICA-30k releases 100 instruction types, while all reported results use the original 10-type ECLIPTICA-3k evaluation (3,000 cases). The remaining 90 types are released but not yet model-scored, and no ECLIPTICA contract was used during training. Scaling the evaluation to 50 or 100 types will allow analysis of contract interference and anchor sufficiency at greater coverage." |
| 29 | p. 7, Fidelity score | "ECLIPTICA's fidelity score ignores the query. Keeping I but replacing X with another prompt leaves SwiPO's score unchanged (0.560 with the true prompt, 0.565 with a scrambled one, 0.571 with the instruction alone; n = 1,000, intervals about ±0.004). The score therefore measures instruction-conditioned style, not joint use of instruction and request; a query-sensitive metric is needed before ECLIPTICA can claim causal isolation of policy control." | 🔻 critical | "We conduct a query-sensitivity test of ECLIPTICA's fidelity measure. Holding I fixed while replacing X with a scrambled prompt yields 0.565, compared with 0.560 for the true prompt and 0.571 for the instruction alone (n = 1,000; intervals approximately ±0.004). This establishes the current metric's scope as instruction-conditioned response style rather than joint instruction-query alignment, motivating the query-sensitive evaluation proposed for the next version." |
| 30 | p. 7, Degenerate answers | "The repetition rates above are disclosed, not fixed; decoding with a repetition penalty and re-scoring is the next experiment." | 🔻⚙️ | "The current results expose repetition as a shared decoding artifact. A follow-up repetition-penalty evaluation will measure how much this behavior changes instruction fidelity and other reported metrics." |
| 31 | p. 7, Missing baselines and checks | "We do not compare with SimPO (Meng, Xia, and Chen 2024), KTO (Ethayarajh et al. 2024), multi-objective decoding, or an instruction-tuned model given the same contracts as a system prompt; we do not test general capabilities (MMLU, GSM8K, HumanEval) or adversarial jailbreak suites." | 🔻⚙️ checklist | "The current baseline suite includes DPO, PPO, and GRPO. Further comparisons with SimPO, KTO, multi-objective decoding, and an instruction-tuned model receiving the same contracts as a system prompt would broaden the method comparison. General-capability evaluation on MMLU, GSM8K, and HumanEval, together with adversarial jailbreak testing, would establish additional deployment boundaries." |
| 32 | p. 7, Coverage | "ECLIPTICA's prompts and contracts are author-written and the training data is PKU-SafeRLHF; all are in English, and creative, coding, and tutoring roles are under-represented." | 🔻📏 | "ECLIPTICA currently uses author-written English prompts and contracts, with PKU-SafeRLHF as the preference-training source. Broader coverage of creative, coding, and tutoring roles, alongside stakeholder-generated contracts, will expand the benchmark's representativeness." |

### D7. Ethics statement and conclusion

| # | 📍 | Quoted original (exact) | Problem | Rewrite |
|---|---|---|---|---|
| 33 | p. 8, Ethics Statement | "A switchable model is also a model whose safety behavior can be switched off: a permissive contract lowers refusals by design. We release the benchmark and code, not a deployed product, and Section 2 argues that the instruction must come from an accountable principal through a privileged channel, above a floor of constraints that no contract may lift; our floor analysis shows that no such floor arises by default. Who sets that floor is a collective decision that this paper does not make." | 🔻 | "Switchable alignment provides behavioral flexibility while making instruction authority a central safety-governance responsibility. A permissive contract lowers refusals by design, so we release the benchmark and code rather than a deployed product. Section 2 motivates an accountable principal, a privileged instruction channel, and a non-switchable floor of constraints. The floor analysis shows that such a floor does not arise by default, making its selection an explicit collective decision that remains an open governance question." |
| 34 | p. 8, Conclusion | "Trained on a single safety contract, SwiPO transfers to unseen contracts better than PPO and GRPO, but it cannot be separated from plain DPO once AQI, which does not compare models, is set aside (86.7% relative efficiency against DPO's 56.1% with it; 83.4% against 67.6%, an interval spanning zero, without it), and DPO switches more on refusals. Every trainer still loops, and the experiment SwiPO was designed for, training opposite contracts on the same prompts, has not been run. The answer to the title question is therefore not yet." | 🔻 highly negative | "Trained on one safety contract, SwiPO demonstrates transfer to unseen contracts and exceeds PPO and GRPO on important instruction-sensitivity measures. Its original relative efficiency is 86.7% versus DPO's 56.1% with AQI, and 83.4% versus 67.6% without AQI, although the latter difference has a 95% interval spanning zero. DPO produces the larger refusal change under Conditional Safety. Across all trainers, 46 to 67% of Instruct-model ECLIPTICA answers exhibit substantial repetition, and all reported scores include these outputs. The present results establish transfer from one trained safety contract rather than simultaneous learning of opposing contracts. The broader result is that conditional alignment shifts the social-choice problem toward governance of instruction authority, contract menus, and collective safety constraints." |

### D8. 🥇 The three rewrites that matter most

Prioritize these even if no new experiment is completed.

| Priority | Rewrite | How |
|---|---|---|
| 1️⃣ | Stop repeating that opposing contracts were not trained | It recurs in the abstract, contributions, method, limitations, and conclusion. State the scope once in the abstract, explain the single-contract setup in the method, and describe multi-contract training as the next validation. Do not imply simultaneous pluralistic learning was shown. |
| 2️⃣ | Replace the DPO comparison narrative | Do not market 86.7% vs 56.1% as an established win. Say the aggregate depends partly on within-model AQI, that the AQI-free difference spans zero, and that DPO switches more under Conditional Safety. This reads as more credible, not less. |
| 3️⃣ | Turn the ECLIPTICA metric limitation into a benchmark finding | The 0.560 vs 0.565 vs 0.571 result shows that instruction-conditioned style and joint task alignment are different constructs; introduce query-sensitive fidelity and task relevance as the next dimensions. Potentially publishable on its own. |

### D9. ✍️ Rewritten abstract (contribution first)

The current abstract is about 283 words; this version is no longer and keeps the key claims, numbers, and qualifications.

> We introduce SwiPO (Switchable Preference Optimization) and ECLIPTICA-30k to study steerable pluralistic alignment as an alternative to aggregating preferences across hidden stakeholder roles. ECLIPTICA-30k crosses 300 author-written policy and ethics prompts with 100 hand-designed instruction types; all reported experiments use ECLIPTICA-3k, its 10-type, 3,000-case subset. SwiPO extends DPO by conditioning preference optimization on an alignment instruction and adding a mandatory KL anchor. The reported run trains one refusal-oriented safety contract and measures transfer to unseen contracts; simultaneous training on conflicting contracts remains untested.
>
> On Llama-3.1-8B, every preference-trained Instruct model changes its refusal rate by 0.30 to 0.49 between strict and permissive contracts. Across violence, physical harm, trafficking, and threats to public health or national security, permissive instructions reduce refusals at least as much as elsewhere by point estimate, although only PPO's floor-versus-other gap has a 95% interval excluding zero.
>
> SwiPO achieves 86.7% relative instruction-alignment efficiency (95% interval 76.8 to 96.2), compared with 56.1% for DPO, 36.1% for GRPO, and 20.4% for PPO. Without AQI, SwiPO scores 83.4% against DPO's 67.6%, with a difference of +15.7 points (95% interval −4.1 to 39.7). Without AQI and TruthfulQA, DPO is numerically ahead, 86.8% versus 77.8% (difference −9.0, 95% interval −40.7 to 16.0). DPO also produces a larger Conditional Safety refusal gap.
>
> These findings demonstrate transfer to unseen alignment instructions and identify a governance challenge: who controls the instruction, which contracts are available, and what collective safety constraints no contract may lift.

What this version changes:

- ✅ opens with the contribution rather than a criticism of DPO;
- ✅ states the experimental scope immediately, without sounding like an apology;
- ✅ ends with the social-choice contribution (instruction authority, agenda setting, collective safety constraints);
- ✅ does not claim SwiPO beats DPO where the evidence does not support it.

## 🏁 Final reviewer verdict

| Category | Judgment |
|---|---|
| Social-choice relevance | 🟢 Strong |
| Originality of framing | 🟢 Strong |
| Formal social-choice contribution | 🟡 Moderate |
| SwiPO novelty | 🟡 Promising |
| Validation of multiple conflicting contracts | 🔴 Missing |
| Benchmark validity | 🔴 Needs improvement |
| Statistical presentation | 🟢 Good, with seed limitations |
| Safety and governance analysis | 🟢 Strong |
| Writing and positioning | 🟡 Needs reframing |

> **Bottom line:** two valuable contributions are inside this paper: a technical one (instruction-conditioned preference optimization under a mandatory KL anchor) and a social-choice one (conditional alignment relocates collective preference problems to instruction authority, agenda setting, and non-switchable constraints). The second suits SC4AI'27 best, but the paper spends most empirical effort on the first while making its strongest case through the second.
>
> **Single most important recommendation:** make the stakeholder-preference and collective-choice dimension measurable, and run at least one genuine multi-contract training experiment. The goal is not to make the paper look more successful than its results, but to make its strongest real contribution impossible for a reviewer to overlook.

## 🔎 Fact-check (by Claude Code, not ChatGPT)

Checked 2026-11-26 against the text of the submitted [v1_SC4AI/0_main.pdf](../../../../v1_SC4AI/0_main.pdf), the [SC4AI'27 call](https://sites.google.com/view/sc4ai/workshops/sc4ai27), and the paper source.

### ✅ Confirmed

| # | Judge claim | Where it is |
|---|---|---|
| 1 | 9-page PDF; call allows 6–8 pages excl. refs and appendices, and welcomes work in progress and promising directions | PDF; SC4AI call ("completed work, work in progress, position papers") |
| 2 | Three roles 40% / 35% / 25% on p. 2 | p. 2 ("compliance role (40% of the annotation pool) ...") |
| 3 | Proposition 1 and Gibbard-Satterthwaite on p. 3 | p. 3 |
| 4 | PKU-SafeRLHF 12,035 pairs; Cost paragraph and single-contract training on p. 4 | p. 4 |
| 5 | Cond. Safety gap DPO 0.475 vs SwiPO 0.391; efficiency 86.7 [76.8, 96.2] vs 56.1 / 36.1 / 20.4 | Table 4, p. 5 |
| 6 | Without AQI 83.4 [71, 95] vs 67.6 [54, 82]; diff +15.7 [−4.1, 39.7] | Table 4 and Limitations |
| 7 | Without AQI and TruthfulQA, DPO ahead 86.8 vs 77.8, diff −9.0 [−40.7, 16.0] | In the paper ("puts DPO ahead (86.8 against 77.8; difference −9.0 [−40.7, 16.0])") |
| 8 | Paired diffs: vs DPO −0.083 [−0.136, −0.026], −0.009 [−0.021, 0.002], +0.053, +0.034; +30.6 [14.7, 49.7] | Findings, p. 5 |
| 9 | Instruct ECLIPTICA 0.367 vs 0.379–0.389; 46 to 67% looping; best Length ratio 1.14; "One case in detail" on p. 5 | p. 5 |
| 10 | Table 6 rates 0.300 / 0.112 / 0.144 / 0.127 and diffs +0.021, +0.100, +0.017, +0.061; 347 of 1,222 prompts | Table 6, p. 6 |
| 11 | Query test 0.560 / 0.565 / 0.571; "The reviewers of an earlier version ..." on p. 7 | p. 7 |
| 12 | All 34 tone-audit quotes spot-checked (rows 3, 19, 22, 23 and others) exist in the PDF | PDF text |
| 13 | Rewritten abstract (D9) is shorter than the original and its numbers are all in the paper | D9: 238 words vs about 285 in the original |

### ⚠️ Issues found

| # | Issue | Impact |
|---|---|---|
| 1 | **Row 17's "quoted original (exact)" is not exact.** The paper reads "on ECLIPTICA (+0.024 [0.012, 0.037] and +0.022 [0.009, 0.033])"; the judge's quote drops the GRPO number, then its own note "corrects" the paper. The paper was right all along. | Low: the rewrite text itself is correct. |
| 2 | **Table 5 page is inconsistent.** C3 says Table 5 is on p. 6 (correct); C6 says "p. 5 Table 5". | Low. |
| 3 | **GPU-hour estimates are the judge's guesses** (A100 basis), not measured. The paper's own run times (120 min SwiPO, 103 min DPO) are real. | Plan with your own hardware numbers. |
| 4 | **C2 needs six human raters** (stakeholder elicitation). That needs people outside the author team, or a clearly labelled synthetic pilot; "2–4 person-hours" is optimistic for recruiting. | Feasibility, not a factual error. |
| 5 | **C1 and C3 introduce an LLM evaluator**, while the paper's point is "no LLM judge" (Table 3, p. 5). Adding one changes a stated design property; the paper would need to say so. | Design trade-off to decide, not an error. |
