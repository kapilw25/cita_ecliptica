> ChatGPT review of the [v5_MultiRobust_4page](../../../v5_MultiRobust_4page/0_main.pdf) draft for MultiRobust, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~7:30 AM PST. The review judged all 4 drafts in one answer: this file keeps the shared parts and the v5 parts; the other drafts' reviews are in [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/by_chatgpt.md), [v6_Bench2Evidence_4page](../v6_Bench2Evidence_4page/by_chatgpt.md), [v7_MATH4AI_4page](../v7_MATH4AI_4page/by_chatgpt.md). Chat-page widget leftovers were turned into tables; every judge sentence and number is kept.

# **AAAI-27 Reviewer Evaluation: SwiPO Across Four Venues**

I have reviewed all four PDFs against the AAAI-26 accepted-paper calibration sheet and the specific research priorities of each AAAI-27 venue.

My central assessment is that SwiPO's strongest contribution in these drafts is no longer the superiority of a preference-optimization algorithm. It is the discovery that apparent switchable alignment depends on the training chain, the evaluation instrument, and the distinction between refusal behavior and actual harmful content.

That is a legitimate and potentially compelling workshop contribution. In particular, it follows the successful research pattern of When Refusals Fail, the strongest of the three previously calibrated papers: an apparently meaningful safety metric can conceal a substantially different underlying behavior.

There are nevertheless three issues that affect all four drafts:

- The experiments concern single-turn LLM behavior rather than fully operational agents.
- The statistical evidence is strong at the prompt level, but does not establish reproducibility across training seeds.
- Some conclusions are stronger than the evidence permits, especially claims that a safety floor exists, that several contracts per request are mathematically necessary, or that one training method cannot create switchability.

## **Calibration reference**

| Previously accepted AAAI-26 paper     | Calibration score | Main acceptance strength                          |
| ------------------------------------- | ----------------- | ------------------------------------------------- |
| The Trust Paradox                     | 64/100            | Memorable conceptual discovery                    |
| From Biased Chatbots to Biased Agents | 73/100            | Broad empirical vulnerability analysis            |
| When Refusals Fail                    | 88/100            | Controlled safety evaluation and failure analysis |

The scores and acceptance probabilities below are reviewer estimates, not official venue statistics. They assume compliance with formatting, anonymity and submission policies. The suggested score gains are conditional on successfully completing the proposed changes.

For computational estimates, I assume access to an existing working Llama-3.1-8B inference pipeline and a modern GPU with sufficient memory. Actual throughput should be verified with a small pilot because GPU specifications were not supplied.

# **2. V5 — MultiRobust (W38)**

**Deadline:** November 28, 2026, 3:59 AM PST · Under 20 hours

Can One Preference-Trained LLM Checkpoint Serve Several Safety-Helpfulness Trade-offs?

swipo_v5_MultiRobust.pdf

## **PART A — Acceptance probability**

| Setting                 | Estimate   |
| ----------------------- | ---------- |
| MultiRobust acceptance  | **78%**    |
| Typical safety workshop | **74%**    |
| Reviewer score          | **76/100** |

**Recommendation:** Accept.

This version has a direct connection to multi-objective alignment through its five-property robustness framework and XSTest safety-helpfulness visualization. Figure 2 on p. 4 is a particularly valuable venue-specific addition because it moves beyond reporting a single refusal gap and compares two competing behavioral objectives. However, the study does not perform multi-objective training, and the principal trade-off figure relies on the same phrase heuristic that the paper identifies as vulnerable to contract repetition. Reviewers may question whether it establishes a meaningful trade-off in helpfulness and safety rather than two refusal-related proxies.

### **Three strongest acceptance reasons**

| Rank | Strength                                               | Evidence                                                                                                                                |
| ---- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | 🟢 Venue-specific two-objective evaluation             | XSTest compares unsafe-prompt refusal and safe-prompt answer rates, including strict and permissive contracts. p. 4, Figure 2           |
| 2    | 🟢 Clear robustness framework                          | Target, side effects, floor, held-out prompts and channel. p. 2, §2                                                                     |
| 3    | 🟢 Controlled optimizer and training-chain comparison  | DPO, GRPO, SFT, SwiPO-R and SwiPO-S compared under corrected composition, with paired intervals. pp. 2–3, Tables 2–3                     |

### **Three most likely rejection reasons**

| Rank | Reviewer objection                                                                                                                                                       | Severity       |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| 1    | The study evaluates single-contract training, rather than actually optimizing multiple objectives or training a Pareto-conditioned policy. p. 2, §3                        | 🔴 High        |
| 2    | Figure 2 uses phrase-based refusal scoring despite substantial disagreement with the semantic judge. pp. 3–4, Table 3 and Figure 2                                        | 🔴 High        |
| 3    | Safe-prompt answer rate does not independently establish answer quality, and unsafe-prompt refusal does not establish the absence of harmful content. p. 4, Figure 2; p. 3, Table 2 | 🟠 Medium–high |

Importantly, the released PPO adapter is not a valid trained PPO competitor. The paper appropriately detects this in §3, but its comparative figure should label PPO as an additional SFT evaluation, not visually imply a fourth independent optimizer.

## **PART B — Ten venue-specific rubrics**

| Rubric                       | Why it matters here                                          | Score      | Evidence                                          | Highest-value change                                                |
| ---------------------------- | ------------------------------------------------------------ | ---------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| Multi-objective relevance    | Central to the workshop's scope                              | 🟢 9       | pp. 1–2, §§1–2                                    | Elevate the safety-helpfulness trade-off figure                     |
| Optimization novelty         | Must explain what optimization contributes                   | 🟢 8       | p. 2, SwiPO formulation                           | Distinguish conditional DPO from the log-ratio penalty              |
| Objective validity           | Safety and utility must be measured independently            | 🟡 7       | Tables 2–3; Figure 2                              | Add semantic scoring and actual unsafe-content rates                |
| Trade-off visualization      | Reviewers expect evidence of multiple operating points       | 🟢 8       | p. 4, Figure 2                                    | Redraw using judge-based operating points                           |
| Baseline fairness            | Optimizer comparisons require correct starting conditions    | 🟢 8       | Figure 1; Table 2                                 | Label PPO as SFT replication; clarify tuning asymmetry              |
| Constraint handling          | A trade-off should not violate a safety floor                | 🟡 7       | Table 4                                           | Separate absolute harmful-content risk from invariance              |
| Experimental robustness      | Effects should generalize beyond training prompts            | 🟢 8       | pp. 2–3, 2,444 held-out prompts and XSTest        | Show held-out objective-specific intervals                          |
| Statistical reliability      | Distinguishes real trade-off movement from noise             | 🟡 7       | Paired BCa intervals; p. 4, §6                    | Repeat inference at several seeds                                   |
| Optimization interpretation  | A negative result should explain the training limitation     | 🟡 7       | pp. 2–3, SwiPO-R/S comparison                     | Report each optimizer's change relative to its own starting point   |
| Research narrative           | Findings should be optimization-centered                     | 🟡 7       | Abstract; Figure 1                                | Lead with contract-dependent trade-off behavior rather than loading |
| **Total**                    |                                                              | **76/100** |                                                   |                                                                     |

**Comparison:** V5 is above the calibrated Biased Agents paper (73) and Trust Paradox (64), but below When Refusals Fail (88). Its statistical reporting is comparatively strong; its central weakness is the validity of the two objective proxies.

## **PART C — Improvements before the deadline**

| Priority | Improvement and what it demonstrates | Required work | Placement and cut | Estimated gain |
| -------- | ------------------------------------ | ------------- | ----------------- | -------------- |
| 1 | **Judge-based safety-helpfulness operating-point plot.** Determines whether apparent trade-offs survive semantic refusal scoring. | Existing XSTest responses for 250 safe and 200 unsafe prompts, both contracts. Re-analysis if judge labels are saved; otherwise judge existing outputs using Llama-3.1-8B-Instruct. Approximately 0–4 GPU hours. | Replace Figure 2, p. 4. No added space. | +2 objective validity, +2 visualization |
| 2 | **Separate refusal and harmful-content objectives.** Report safe-answer rate, unsafe-refusal rate and Llama Guard unsafe-answer rate as distinct endpoints. | Existing responses; Llama Guard 3 scoring if XSTest harm labels are unavailable. Approximately 1–3 GPU hours. | Add a compact table or companion panel within the redesigned Figure 2; remove the lengthy sponsor discussion on p. 4. | +2 constraint handling |
| 3 | **Matched starting-point comparison.** Show each training stage's change in judge and phrase gaps with paired intervals. | Existing outputs and bootstrap code; no new training. Approximately 1–2 hours, CPU. | Replace part of §4's training-chain discussion or Table 1's stance/confidence rows. | +2 optimization interpretation |
| 4 | **Inference stability check.** Repeat selected XSTest evaluations with two additional decoding seeds. | Instruct, DPO, SwiPO-R and SwiPO-S; approximately 150 prompts, two contracts and two additional samples, 2,400 generations. Approximately 4–10 GPU hours depending on throughput. | Add one short stability statement to the Figure 2 caption; compress related work. | +1 statistical reliability |
| 5 | **Pareto-aware interpretation.** Identify observed non-dominated operating points, without claiming a statistically established Pareto frontier. | Existing objective values and paired bootstrap draws. Approximately 1 hour. | Replace “One trade-off point per trained model” paragraph with precise operating-point analysis. | +1 narrative and interpretation |

**Potential revised score: approximately 84–86/100**

Prioritize improvements 1–3. They directly address the optimization workshop's expectations and can be completed without new training. Improvement 4 is optional if the 12-hour inference budget is becoming restrictive.

### **Recommended trade-off figure redesign**

*Illustrative reconstruction of the reported Instruct operating points, p. 4. No additional results are assumed. Existing phrase-based estimates, with reported 95% intervals. Recompute this plot using semantic labels before submission. Do not assume the resulting points remain unchanged.*

(Saver's note: the chat page drew this as a plot; its point values were not part of the copied text.)

### **What to cut**

The sponsor and authority experiments are interesting, but neither is the strongest evidence for a multi-objective optimization workshop. Compress them to a short robustness observation in Table 1.

Keep the floor analysis, the two-objective plot, held-out tests and both refusal instruments. These provide the core of V5's distinct contribution.

## **PART D — Tone audit**

### **D.1 — Shared and MultiRobust-specific corrections**

#### **Shared passages C1–C22 (defined in the review's V4 section; they apply to every draft)**

Quotations below normalize PDF line breaks and line-break hyphenation. When only a heading or table-cell label is quoted, the accompanying numerical evidence should remain unchanged.

| # | Page/section | Quoted original | Problem | Recommended rewrite |
| - | ------------ | --------------- | ------- | ------------------- |
| C1 | p. 2, Setup | “The released PPO adapters are untrained: all 224 of their LoRA B matrices are zero, so PPO as trained is the SFT model and its final adapter alone is the base model, and its rows are second runs of those two.” | Engineering diagnosis | Adapter verification identifies a useful control: all 224 LoRA B matrices in the released PPO adapters are zero. Consequently, its as-trained and final-adapter-only evaluations provide additional runs of SFT and the base model, respectively, rather than an independent trained PPO comparison. |
| C2 | p. 2, Setup | “The pair separates the effect of the chain from the effect of the loss.” | Overstates causal identification | Holding the SwiPO loss, data, and hyperparameters fixed enables a controlled comparison of the two training-chain configurations. |
| C3 | p. 2, Setup | “on data answers it is no divergence estimate, and minimizing it lowers both likelihoods.” | Negative mathematical description; important fact | The penalty acts directly on the mean log-ratio of the observed response pair, rather than estimating a distributional divergence, and favors reducing their joint log-likelihood. |
| C4 | p. 2, Results | “The pretrained model’s phrase gap is mostly wording.” | Dismissive finding | Contract repetition inflates phrase-based estimates of refusal switching. |
| C5 | p. 2, Results | “Much of it is wording: 41% of its answers repeat the contract, whose strict version is full of refusal words, and without the repeated sentences the gap is 0.142 [0.113, 0.173]; an LLM judge of whether the reply refuses or deflects finds no gap (0.012 [−0.018, 0.042]; Table 3).” | Defensive tone and non-significance described as absence | Contract repetition accounts for a substantial portion of the measured phrase gap: 41% of answers repeat the contract, and removing repeated sentences reduces the gap to 0.142 [0.113, 0.173]. Semantic refusal scoring yields 0.012 [−0.018, 0.042], an interval that includes zero (Table 3). |
| C6 | p. 2, Results | “As trained, SFT on one contract removes it (0.022; 0.033 in PPO’s second run), and DPO and GRPO keep 0.034.” | Failure-focused wording | Single-contract SFT substantially attenuates the phrase-based gap to 0.022, with 0.033 in the additional PPO-labelled run; DPO and GRPO each yield 0.034. |
| C7 | p. 2, Results | “The final adapter alone shows 0.30 to 0.49 for every model, at or above the base’s 0.299: loaded that way, each model inherits the base model’s prompt-following, wording included (judge 0.006 to 0.074).” | Operations framing; causal mechanism overstated | Model composition is an important determinant of measured switchability: final-adapter-only configurations produce phrase gaps of 0.30 to 0.49, compared with 0.299 for the base model, while judge-based gaps range from 0.006 to 0.074. |
| C8 | p. 2, Results | “On held-out prompts DPO and GRPO fall from 0.501 and 0.309 to 0.068 [0.046, 0.091] and 0.027 [0.009, 0.044].” | Decline-focused wording | Held-out evaluation independently reproduces the composition-dependent reduction: DPO changes from 0.501 to 0.068 [0.046, 0.091], and GRPO from 0.309 to 0.027 [0.009, 0.044]. |
| C9 | p. 3, Results | “Loading also decides harm” | Engineering-focused heading | Model composition changes conclusions about unsafe-content sensitivity. |
| C10 | p. 3, Results | “Scoring only each answer’s first turn changes nothing (Table 3), a check needed because the models with SFT in their chain run past their turn in 98 to 99% of answers under the base model’s stopping rule.” | Operations language; overstates invariance | First-turn scoring preserves the main qualitative findings (Table 3), despite additional generated turns in 98 to 99% of answers from models with SFT in their chain under the base stopping rule. |
| C11 | p. 3, Results | “The training chain decides SwiPO’s lever.” | Overly deterministic causal wording | SwiPO's contract sensitivity differs across training-chain configurations. |
| C12 | p. 3, Results | “Against its starting point (the DPO adapter alone) the instruments disagree: 0.113 [0.070, 0.155] lower by phrase, 0.055 [0.010, 0.099] higher by judge.” | Reads as a disappointing result rather than a measurement discovery | Relative to its DPO-adapter-only starting point, SwiPO-R reveals an instrument-dependent effect: the phrase gap decreases by 0.113 [0.070, 0.155], whereas the judge-based gap increases by 0.055 [0.010, 0.099]. |
| C13 | p. 3, Results | “Trained with one contract, SwiPO’s loss does not restore the lever once SFT is in the chain.” | Negative; generalizes from one run | In the evaluated single-contract configuration, SwiPO-S retains limited contract sensitivity, with no resolved improvement over its DPO starting point. |
| C14 | p. 3, Results | “The contract changes wording, not harm.” | Overstates a null result; actual refusal behavior can also change | Refusal switching and unsafe-content switching are empirically distinct. |
| C15 | p. 3, Results | “The test detects a floor where one exists (the prompted Instruct model, below) and finds none in the trained models” | Overinterprets the operational floor test | The floor test distinguishes the prompted Instruct model from the contract-trained models, providing evidence of selective refusal protection in the former but not resolving such an effect in the latter. |
| C16 | p. 3, Results | “Read as a harm constraint, the floor holds for every trained model, because no contract moves harm; read as a refusal floor, it holds for none, so a refusal floor has to be a training target.” | Equates statistical non-detection with safety; unsupported necessity | The unsafe-rate comparisons reveal no statistically resolved contract effect, whereas the refusal-gap comparisons provide no evidence of preferential protection for floor requests in the trained models. These distinct criteria motivate explicit floor-related training objectives. |
| C17 | pp. 3–4, Results | “The user’s contract wins a conflict.” | Universal claim from one strong result | Opposing contracts reveal model-dependent instruction authority. |
| C18 | p. 4, Results | “SwiPO-R’s lever cancels (0.037 [−0.002, 0.074]), and the models with SFT in their chain, whose levers are 0.03 to 0.05, lean slightly to the user (−0.011 to −0.032), as does the base (−0.092 [−0.131, −0.054]).” | Interprets an interval crossing zero as cancellation | SwiPO-R exhibits an unresolved conflict gap of 0.037 [−0.002, 0.074]. Models with SFT in their chain have original gaps of 0.03 to 0.05 and conflict-gap estimates of −0.011 to −0.032; the base model shows −0.092 [−0.131, −0.054]. |
| C19 | p. 4, Results | “Only the prompted model serves a hidden sponsor.” | Absolute claim despite nonzero promotion by other models | Prompted Instruct exhibits the strongest undisclosed-sponsorship response. |
| C20 | p. 4, Limitations | “SwiPO received the only tuning budget (13 Optuna trials); DPO and GRPO use fixed settings, so the comparison favors SwiPO.” | Self-critical phrasing; actual effect of unequal tuning unknown | SwiPO receives 13 Optuna tuning trials, whereas DPO and GRPO use fixed settings. This asymmetric tuning budget potentially favors SwiPO and limits conclusions about comparative optimizer performance. |
| C21 | p. 4, Limitations | “About nine in ten Conditional Safety prompts appear in the training pool, so we repeat the refusal-gap, floor and harm results on 2,444 held-out prompts.” | Defensive tone | To assess generalization beyond Conditional Safety, where approximately nine in ten prompts appear in the training pool, we additionally evaluate refusal gaps, floor protection, and unsafe-content rates on 2,444 held-out prompts. |
| C22 | p. 4, Limitations | “Refusal is scored by a phrase heuristic that agrees poorly with an LLM judge (κ 0.03 to 0.58, Table 3), so we claim a lever only where the instruments agree, and harm by one classifier (Llama Guard 3); neither is yet checked against human labels.” | Self-critical, but scientifically necessary | We triangulate refusal behavior using a phrase heuristic and an LLM judge, whose agreement ranges from κ = 0.03 to 0.58 (Table 3), and require convergent evidence for a switching claim. Unsafe content is measured independently using Llama Guard 3; both evaluations remain to be validated against human annotations. |

#### **Shared Table 1 wording audit**

These terse cell descriptions appear in all four versions. They make the table resemble an internal debugging summary rather than a research-results table.

| Original label, p. 3                     | Problem                                                | Replacement label                                |
| ---------------------------------------- | ------------------------------------------------------ | ------------------------------------------------ |
| “removed by SFT”                         | Absolute causal language                               | Attenuated after SFT                             |
| “harm held fixed”                        | Null result described as invariance                    | No detected unsafe-rate shift                    |
| “not learned: moves as much as elsewhere” | Failure framing and implied equivalence               | No resolved floor-specific reduction             |
| “small”                                  | Subjective judgment                                    | Limited length sensitivity                       |
| “held fixed”                             | Implied equivalence                                    | No resolved confidence-marker shift              |
| “not readable”                           | Dismissive, operational language                       | Divergence score does not establish adherence    |
| “ignored”                                | Absolute language despite nonzero rates                | Limited promotion response                       |
| “the user wins”                          | Informal, oversimplified                               | User-favoring conflict-gap estimates             |

Keep every numerical value and interval following these labels.

Two further shared wording changes are worthwhile. Table 2 and Table 3's caption, “No bold: no better direction,” can become “No preferred direction is prespecified.” Table 4's overlapping intervals should be described as descriptive uncertainty, not as a formal test of between-model differences.

Apply C1–C22 and the Table 1 wording corrections from V4. In V5, C1–C12 principally appear on p. 2; C13–C16 on pp. 3–4; and C17–C22 on p. 4. The exact shared wording and associated intervals remain as quoted above.

The following additional passages are specific to MultiRobust.

| # | Page/section | Quoted original | Problem | Recommended rewrite |
| - | ------------ | --------------- | ------- | ------------------- |
| M1 | p. 1, title | “Can One Preference-Trained LLM Checkpoint Serve Several Safety-Helpfulness Trade-offs?” | Relevant but question-only framing | Measuring Contract-Conditioned Safety-Helpfulness Trade-offs in Preference-Trained Language Models |
| M2 | p. 1, abstract | “Two models select” | Ambiguous; selection of a trade-off is stronger than a refusal shift | Two models exhibit contract-dependent refusal behavior under both measurement instruments. |
| M3 | p. 1, abstract | “each such model holds one safety-helpfulness point under both contracts, where the prompted model reaches two.” | Implies exact equality without an equivalence test | XSTest reveals limited operating-point movement for models with SFT, whereas prompted Instruct exhibits two distinct observed operating points. |
| M4 | p. 1, abstract | “No model’s unsafe-answer rate (Llama Guard 3) moves detectably, and no contract-trained model keeps a floor.” | Negative framing; floor absence overstated | Unsafe-content scoring with Llama Guard 3 reveals no detectable contract effect, while floor-specific refusal comparisons provide no resolved evidence of preferential protection among contract-trained models. |
| M5 | p. 1, introduction | “a model that refuses more protects third parties and serves fewer legitimate users.” | Assumes refusal is synonymous with safety | Safety and helpfulness can conflict when refusal behavior affects both harmful and legitimate requests. |
| M6 | p. 1, contributions | “SFT on one contract removes the pretrained model’s phrase gap (0.299, mostly wording) and no single-contract loss restores it” | Failure-focused and overly general | Single-contract SFT substantially attenuates the pretrained model's phrase gap of 0.299, which is largely driven by wording; the evaluated subsequent training losses retain limited switching in the SFT-based chain. |
| M7 | p. 2, §2 | “A contract pair (strict, permissive) picks one of two points on a trade-off” | Assumes success before testing it | A strict/permissive contract pair provides a controlled test of whether natural-language conditioning can select distinct trade-off operating points. |
| M8 | p. 2, §2 | “the rate of unsafe answers judged by Llama Guard 3, a constraint every contract must respect.” | No explicit allowable risk threshold defined | Unsafe-answer rates judged by Llama Guard 3 provide a separate measure of potential safety side effects. |
| M9 | p. 4, Results heading | “One trade-off point per trained model.” | Overstates equivalence | Limited operating-point movement in SFT-based models. |
| M10 | p. 4, Results | “Each model with SFT in its chain holds one point (safe answered 0.932 to 0.972, unsafe refused 0.040 to 0.155), and the Instruct model dominates both of SwiPO-R’s.” | Conflates observed point estimates with established dominance | Models with SFT in their chain cluster within safe-answer rates of 0.932 to 0.972 and unsafe-refusal rates of 0.040 to 0.155. The observed Instruct operating points dominate both SwiPO-R operating points by point estimates. |
| M11 | p. 4, Figure 2 caption | “Phrase heuristic, first turn (it counts the base’s repeated contract as refusal)” | Exposes a central measurement limitation without resolving it | First-turn phrase-based estimates with 95% BCa intervals; contract repetition can inflate the base model's estimated refusal rate. |
| M12 | p. 4, Conclusion | “Several trade-offs per checkpoint, and a floor, must be trained.” | Unsupported necessity claim | The findings motivate training objectives that explicitly represent multiple operating points and floor-specific safety requirements. |

For M11, rewriting alone is not sufficient. The judge-based figure in Part C is the actual scientific improvement.

### **D.2 — Three most important rewrites**

1. **M7:** Frame the contract as a hypothesized trade-off selector, not a successful selector by definition.
2. **M10:** Present the comparison as observed operating points and point-estimate dominance.
3. **M12:** Replace unsupported claims about necessary training conditions with evidence-based optimization implications.

### **D.3 — Rewritten abstract**

We introduce a five-property robustness framework for evaluating natural-language contracts as selectors of safety-helpfulness operating points: target sensitivity, side effects, safety floors, held-out generalization, and instruction channel. We apply it to Llama-3.1-8B models trained with DPO, GRPO, and SwiPO, an instruction-conditioned DPO with a reference-model log-ratio penalty, alongside a released PPO model with an untrained adapter. Evaluating complete training chains, we identify refusal switching under both phrase-based and LLM-judge scoring in prompted Instruct (judge gap 0.142) and released SwiPO without supervised fine-tuning (SFT) (0.128). With SFT, DPO and GRPO yield phrase gaps of 0.03, and retrained SwiPO yields 0.052 (95% interval 0.020 to 0.082), with an unresolved improvement over DPO of +0.017 (−0.025 to +0.057). XSTest reveals limited operating-point movement in SFT-based models and distinct operating points in prompted Instruct. The pretrained model's phrase gap of 0.299 (0.266 to 0.332) contrasts with a judge gap of 0.012. Unsafe-answer rates measured by Llama Guard 3 exhibit no detectable contract shift, and trained-model floor comparisons reveal no resolved preferential refusal protection. Final-adapter-only evaluations yield phrase gaps of 0.30 to 0.49. These findings identify measurement and training-chain considerations for robust multi-objective alignment.

# **PART E — Cross-version analysis**

## **E.1 — Numerical and textual consistency**

### **Numerical consistency of the main results**

I found no conflicting numerical values among the corresponding cells of Tables 2–4 across the four drafts.

That is a substantial positive point. The common experimental results have been maintained consistently while the venue-specific narratives have changed.

| Shared result              | V4     | V5     | V6     | V7     |
| -------------------------- | ------ | ------ | ------ | ------ |
| DPO final-only phrase gap  | 0.489  | 0.489  | 0.489  | 0.489  |
| DPO as-trained gap         | 0.034  | 0.034  | 0.034  | 0.034  |
| PPO-labelled as-trained gap | 0.033 | 0.033  | 0.033  | 0.033  |
| GRPO as-trained gap        | 0.034  | 0.034  | 0.034  | 0.034  |
| SwiPO-R as-trained gap     | 0.376  | 0.376  | 0.376  | 0.376  |
| SwiPO-S as-trained gap     | 0.052  | 0.052  | 0.052  | 0.052  |
| Base-model gap             | 0.299  | 0.299  | 0.299  | 0.299  |
| SwiPO-R judge gap          | 0.128  | 0.128  | 0.128  | 0.128  |
| Instruct judge gap         | 0.142  | 0.142  | 0.142  | 0.142  |
| Conditional Safety prompts | 1,222  | 1,222  | 1,222  | 1,222  |
| Held-out PKU prompts       | 2,444  | 2,444  | 2,444  | 2,444  |
| Bootstrap resamples        | 10,000 | 10,000 | 10,000 | 10,000 |
| Training-pool overlap      | ~90%   | ~90%   | ~90%   | ~90%   |

Sources: Table 2, Table 3, Setup and Limitations in each PDF.

However, there are meaningful inconsistencies in how identical numbers are interpreted.

## **E.2 — Claims requiring reconciliation**

| # | First version / exact wording | Second version / exact wording | Assessment |
| - | ----------------------------- | ------------------------------ | ---------- |
| 1 | V4 p. 1: “No model’s unsafe-answer rate (Llama Guard 3) moves with the contract” | V5 p. 1: “No model’s unsafe-answer rate (Llama Guard 3) moves detectably” | 🟠 V5 is more statistically defensible. An interval including zero does not establish invariance. |
| 2 | V7 p. 2: “By phrase neither chain gains.” | V4/V5 p. 1 report the difference “+0.017, −0.025 to +0.057” | 🔴 The positive point estimate is not a demonstrated gain, but neither does it establish the absence of a gain. |
| 3 | V6 p. 4: “Either check alone removes most of the switch.” | V4 p. 3: SwiPO-R “keeps 0.376 [0.346, 0.407]” | 🔴 Composition correction does not remove most of SwiPO-R's phrase gap. V6's Table 5 also shows 0.399 versus 0.385 under the two compositions. |
| 4 | V7 p. 1: “A switchable checkpoint therefore needs training data with several contracts per request” | V4/V5 p. 1 identify “a prompted instruction-tuned model (judge gap 0.142)” | 🟠 Not a demonstrated numerical contradiction, but the mathematical necessity is not established. The prompted model's full training history is not controlled. |
| 5 | V6 p. 1: “as-trained models run past the end of their turn” | V4 p. 3: “the models with SFT in their chain run past their turn in 98 to 99% of answers” | 🟠 V6 generalizes the run-on behavior beyond the group explicitly identified in the results. |
| 6 | V4 p. 1: “no trained model protects floor requests more than others, so a floor must be trained.” | V6 pp. 3–4: “Read as a harm constraint, the floor holds for every trained model” | 🔴 A lack of detectable harm-rate movement does not establish a protected safety floor. Distinguish absolute safety, refusal selectivity and invariance. |
| 7 | V5 p. 4: “Each model with SFT in its chain holds one point” | V4/V5/V6/V7 Tables 2–3 report small nonzero gap estimates for these models | 🟠 The study supports limited sensitivity, not necessarily statistical equivalence between operating points. |
| 8 | V4 p. 4: “Only the prompted model serves a hidden sponsor.” | V5/V6/V7 p. 4 report “SwiPO-R 0.017 [0.010, 0.029]” | 🟠 The same issue exists within V4. Prompted Instruct has the strongest promotion response; it is not the only configuration with nonzero promotion. |
| 9 | V7 p. 4: “which Proposition 1 shows is what makes a conditioned optimum switchable.” | V7 p. 2: “We state both results for gradients, not minimizers” | 🔴 Internal mathematical inconsistency. The proposition does not establish the properties of an optimum. |
| 10 | V4/V5/V6/V7, Setup: “All four trainers start from Llama-3.1-8B ... with LoRA adapters ... and supervised fine-tuning (SFT)” | The same Setup describes “SwiPO-R, the released model” as continuing from the base with the DPO adapter merged | 🟠 Clarify the intended training pipeline versus the actually reconstructed training chains. |
| 11 | V4/V5/V6/V7, Results: “Scoring only each answer’s first turn changes nothing” | Tables 2–3: DPO changes from 0.034 to 0.021; SwiPO-S from 0.052 to 0.033 | 🟠 The principal qualitative conclusions persist, but numerical estimates do change. |
| 12 | V6 p. 1: “three of four also move harmful content” | All versions' results report DPO +0.042, GRPO +0.045 and “SwiPO +0.085” under final-only loading | 🟡 Not a numerical contradiction, but explicitly identify which SwiPO configuration produces the +0.085 result. |

### **Apparent discrepancies that are not actual contradictions**

| Values | Explanation |
| ------ | ----------- |
| DPO 0.489 in Table 2 versus 0.495 in V6 Table 5 | Full-answer versus first-turn phrase scoring |
| SwiPO-R 0.376 in Table 2 versus 0.385 in Table 3 | Different answer-scoring boundaries |
| Base 0.299 in Table 2 versus 0.296 in Table 3 | Full-answer versus first-turn scoring |
| SwiPO-S minus DPO reported as +0.017 although displayed values differ by 0.018 | Consistent with differences calculated before rounding |
| SwiPO-R 0.376 versus 0.128 | Phrase heuristic versus semantic refusal judge; not interchangeable metrics |
| Instruct 0.142 versus 0.169 | Conditional Safety versus XSTest judge-based gaps |

I would explicitly standardize metric names throughout all four drafts to prevent reviewers from incorrectly treating these values as contradictory.

## **E.3 — Three shared scientific issues more important than tone**

### **Issue 1: Invariant harm is not equivalent to safety**

The paper's own Table 2 establishes why this distinction matters.

Absolute unsafe-answer rates under the strict contract, models as trained. Table 2 in all four versions.

| Model                 | Unsafe-answer rate, strict contract |
| --------------------- | ----------------------------------- |
| SwiPO-S               | 1.4%                                |
| SwiPO-R               | 2.2%                                |
| DPO                   | 2.8%                                |
| SFT                   | 30.0%                               |
| GRPO                  | 32.0%                               |
| PPO-labelled SFT run  | 32.3%                               |
| Base                  | 40.4%                               |

Rates are Llama Guard 3 classifications rather than human-validated harm labels. Displayed values are point estimates; retain the original Table 2 intervals when reporting them in the paper.

A model with an unsafe-answer rate of approximately 32% under both contracts is not necessarily safer than a model with a lower but contract-sensitive rate.

The correct distinction is between:

- **Safety level:** How often does the model produce unsafe answers?
- **Safety invariance:** How much does that rate change when the contract changes?
- **Floor protection:** Are particularly serious categories preferentially protected?

The current manuscript sometimes conflates these concepts. Correcting that distinction would improve all four versions.

### **Issue 2: SwiPO-R has a scientifically interesting positive result**

The draft correctly reports that the two instruments disagree about SwiPO-R's change relative to its starting point.

V7 p. 2; shared Results section in V4–V6. Change relative to starting checkpoint. Reported paired 95% intervals. Zero indicates no change from the starting point.

| Comparison          | Correct interpretation                                            |
| ------------------- | ----------------------------------------------------------------- |
| SwiPO-R, phrase     | 🔴 Measured decrease of −0.113 [−0.155, −0.070]                   |
| SwiPO-R, judge      | 🟢 Measured increase of +0.055 [0.010, 0.099]                     |
| SwiPO-S, phrase     | 🟡 Positive estimate of +0.017 [−0.025, +0.057], unresolved       |
| SwiPO-S versus DPO  | 🟡 Neither superiority nor equivalence is established             |

Do not sell SwiPO-R as universally superior. But equally, do not bury its positive judge-based change beneath the statement that neither chain gains.

The research contribution is that different behavioral instruments lead to different conclusions about the same preference-training intervention.

### **Issue 3: Independent training runs versus prompt-level uncertainty**

All four papers acknowledge in §6 that they use:

- One training seed per method.
- One sampled answer per item.
- One SwiPO-S run.
- 10,000 prompt-level bootstrap resamples.

The 10,000 bootstrap resamples quantify uncertainty over sampled prompts. They do not constitute 10,000 independent model runs.

When Refusals Fail reported at least three seeds in its supplementary evaluation, which remains an important difference between that paper's evidence and the current SwiPO study.

This limitation is tolerable for short workshop papers, but it is particularly important for MultiRobust and MATH4AI, where claims about optimization robustness are central.

## **E.4 — Are these distinct papers or one paper submitted four times?**

### **Assessment from a program-chair perspective**

Currently, I would interpret them as four venue-specific presentations of one underlying empirical study, not four independently developed research papers.

That is not automatically inappropriate for non-archival workshops, but it depends on the individual venue policies. Non-archival status by itself does not guarantee that overlapping simultaneous submissions are permitted.

The shared main-text structure is highly visible.

| Component                         | V4                                  | V5                         | V6                                  | V7                                      |
| --------------------------------- | ----------------------------------- | -------------------------- | ----------------------------------- | --------------------------------------- |
| Title                             | Distinct                            | Distinct                   | Distinct                            | Distinct                                |
| Abstract                          | Distinct                            | Distinct                   | Distinct                            | Distinct                                |
| Introduction                      | Tailored                            | Tailored                   | Tailored                            | Tailored                                |
| Venue-specific framework          | Principal-agent                     | Five-property robustness   | Five evidence checks                | Mathematical proposition                |
| Figure 1                          | Identical                           | Identical                  | Identical                           | Identical                               |
| Experimental Setup                | Nearly identical                    | Nearly identical           | Nearly identical                    | Nearly identical                        |
| Tables 2–4                        | Identical data                      | Identical data             | Identical data                      | Identical data                          |
| Core Results prose                | Nearly identical                    | Nearly identical           | Nearly identical                    | Nearly identical                        |
| Venue-specific empirical addition | Loyalty interpretation in Table 1   | XSTest Figure 2            | Scorer/composition Table 5          | Starting-point interpretation in §2     |
| Limitations                       | Nearly identical                    | Nearly identical           | Nearly identical                    | Nearly identical                        |
| Conclusion                        | Tailored                            | Tailored                   | Tailored                            | Tailored                                |

### **Distinctiveness scores**

These are subjective reviewer estimates of how independently the scientific contribution is articulated, rather than text-similarity percentages.

| Version               | Distinctiveness | Distinct contribution                     |
| --------------------- | --------------- | ----------------------------------------- |
| V6 — Bench2Evidence   | 8.5/10          | Reusable benchmark-validity audit         |
| V5 — MultiRobust      | 7.5/10          | Trade-off operating-point analysis        |
| V7 — MATH4AI          | 7/10            | Mathematical proposition and corollary    |
| V4 — LoyalAgents      | 6.5/10          | Principal-agent reinterpretation          |

### **What makes each version distinct, and what should change?**

| Version | Present distinct contribution | Current duplication concern | Most important differentiation |
| ------- | ----------------------------- | --------------------------- | ------------------------------ |
| V4 LoyalAgents | Principal-agent framework and governance controls | Sponsor and authority experiments appear in all four drafts | Add an explicit user-versus-operator conflict experiment and lead with it |
| V5 MultiRobust | Two-dimensional XSTest operating-point visualization | Most experiments remain general refusal analysis | Make objective-specific semantic evaluation and trade-off analysis the primary results |
| V6 Bench2Evidence | Five-check protocol and factorial evaluation Table 5 | Much of the shared results section is unrelated to benchmark validity | Center the paper on measurement errors, validated scoring and evaluation stability |
| V7 MATH4AI | Proposition 1 and Corollary 1 | Most empirical content does not test the mathematical result | Develop genuinely stronger theoretical results and theory-driven experiments |

The answer is not to rewrite more sentences with synonyms. It is to ensure that each venue receives an evaluation or analysis addressing a genuinely different scientific question.

**Shared SwiPO study:** checkpoints, contract interventions, refusal scoring, harm classification, bootstrap evaluation.

| Venue          | Question                              | Analysis                                  |
| -------------- | ------------------------------------- | ----------------------------------------- |
| LoyalAgents    | Whose interests are served?           | Principal versus operator conflict        |
| MultiRobust    | Which objectives can be switched?     | Safety and utility operating points       |
| Bench2Evidence | Which measurements are trustworthy?   | Evaluation-validity decomposition         |
| MATH4AI        | What does the loss identify?          | Mathematical identifiability and coupling |

## **E.5 — Submission disclosure and anonymity**

There is one particularly important administrative difference.

V4 and V7 include a footnote stating:

> “Related versions: arXiv:2601.06157 and an AAAI-27 SC4AI paper load the final adapter alone (the as-trained sizes here replace theirs, e.g. SwiPO’s 86.7% relative efficiency)”

They additionally identify the other workshop versions under review. See p. 2, footnote 1 of each respective draft.

V5 and V6 instead state:

> “Stacked adapters can be loaded two ways; Table 2 reports both, and every claim uses the model as trained.”

The double-blind versions do not contain equivalent related-submission disclosure.

This difference is understandable given their anonymity requirements, but I would recommend checking the chairs' instructions on how to disclose overlapping submissions anonymously or privately.

| Administrative concern        | V4                                          | V5                                  | V6                                  | V7                                          |
| ----------------------------- | ------------------------------------------- | ----------------------------------- | ----------------------------------- | ------------------------------------------- |
| Required review format        | Single-blind                                | Double-blind                        | Double-blind                        | Single-blind                                |
| Current author information    | Named                                       | Anonymous                           | Anonymous                           | Named                                       |
| Related submission disclosure | Present                                     | Not equivalent                      | Not equivalent                      | Present                                     |
| Code link on first page       | Present                                     | Omitted                             | Omitted                             | Present                                     |
| Main-text limit               | 4-page draft within permitted limit         | 4 pages                             | 4 pages                             | 4 pages                                     |
| Additional check              | Accurate simultaneous-submission status     | Anonymous data/code provenance      | Anonymous related-work disclosure   | Accurate simultaneous-submission status     |

I have not independently verified each venue's current overlapping-submission policy. The acceptance estimates assume the submissions are eligible under those rules.

Because earlier versions used final-adapter-only loading, there is also a scientific reason to clearly identify which conclusions have been superseded. In particular, the 86.7% relative-efficiency claim mentioned in the V4/V7 footnote should not continue to be presented as a validated result of the intended training chains without supporting corrected analysis.

# **Final ranking of all four submissions**

## **Current acceptance probability**

| Rank | Venue               | Reviewer score | Acceptance probability |
| ---- | ------------------- | -------------- | ---------------------- |
| 1    | V6 — Bench2Evidence | 84/100         | **86%**                |
| 2    | V5 — MultiRobust    | 76/100         | **78%**                |
| 3    | V4 — LoyalAgents    | 74/100         | **74%**                |
| 4    | V7 — MATH4AI        | 64/100         | **52%**                |

Subjective PC-style estimates for the current manuscripts. These are not measured venue acceptance rates.

## **Complete comparison**

| Rank | Venue          | Current score | Venue acceptance | Typical safety workshop | Potential improved score | Main weakness                                  |
| ---- | -------------- | ------------- | ---------------- | ----------------------- | ------------------------ | ---------------------------------------------- |
| 🥇 1 | Bench2Evidence | 84            | 86%              | 77%                     | 91–94                    | No human-validated scorer                      |
| 🥈 2 | MultiRobust    | 76            | 78%              | 74%                     | 84–86                    | Trade-off figure relies on fragile heuristic   |
| 🥉 3 | LoyalAgents    | 74            | 74%              | 73%                     | 82–84                    | Obedience does not establish loyalty           |
| 4    | MATH4AI        | 64            | 52%              | 67%                     | 78–82                    | Mathematical conclusion exceeds proved result  |

The improved scores assume the proposed work is completed successfully and produces interpretable evidence. A new experiment could also weaken a claim, so these are targets rather than guaranteed improvements.

# **Single most valuable change for this venue**

| Venue | Change | Placement, gain and cost |
| ----- | ------ | ------------------------ |
| V5 — MultiRobust | Rebuild Figure 2 using semantic refusal scores, distinguishing safe-prompt answer rates from unsafe-content rates. | Replace the existing figure. Estimated gain: 4 points. Approximately 0–4 GPU hours for refusal rescoring. |

# **Deadline-prioritized action plan for this venue**

Since LoyalAgents and MultiRobust have less than 20 hours remaining, I would allocate effort according to deadline rather than acceptance ranking.

Submission sprint (the chat page showed 9 tasks, 0/9 completed; this file keeps the shared tasks and this venue's tasks):

| When | Task | Estimate | Status |
| ---- | ---- | -------- | ------ |
| Nov 27 • Immediate | Re-score existing XSTest outputs for MultiRobust and rebuild Figure 2. | 0–4 GPU hours | ⬜ |
| Nov 27 • While inference runs | Apply abstract rewrites, correct null-result language and relabel PPO. | 1–2 working hours | ⬜ |
| Nov 27–28 • Before submission | Verify four-page layouts, anonymity and related-submission disclosure. | 1 working hour | ⬜ |

The GPU-hour estimates are planning ranges, not measured runtimes. If only one GPU is available, the first two inference tasks should be scheduled sequentially within the approximately 12-hour budget, prioritizing rescoring saved responses and reducing the LoyalAgents subset if necessary.

## **Final verdict**

Compared with the three accepted AAAI-26 short papers, the corrected SwiPO study has substantial strengths:

| Dimension                              | Assessment                     |
| -------------------------------------- | ------------------------------ |
| Research relevance                     | 🟢 Strong                      |
| Empirical breadth                      | 🟢 Strong                      |
| Statistical reporting                  | 🟢 Strong at prompt level      |
| Evaluation controls                    | 🟢 Strong                      |
| Reproducibility across training runs   | 🟡 Limited                     |
| Human validation                       | 🟠 Missing                     |
| Actual agent execution                 | 🟠 Missing                     |
| Mathematical depth                     | 🟠 Needs improvement           |
| Venue-specific differentiation         | 🟡 Moderate to strong          |

The corrected results do not make SwiPO an unpublishable study. They change the most defensible research contribution.

**The strongest narrative is not that SwiPO wins, nor that SwiPO fails. It is that contract-conditioned alignment exposes a distinction between apparent switching, semantically measured switching, unsafe-content behavior and the training chain that produces them.**

That is particularly valuable for Bench2Evidence, competitive for MultiRobust and LoyalAgents, and potentially valuable for MATH4AI if the mathematical claims are made substantially more rigorous.

My recommendation is to submit all eligible versions with appropriate overlap disclosures, prioritize the two imminent deadlines, and spend the remaining four-day improvement window primarily on human-validated evidence for V6 and stronger mathematics for V7.
