> ChatGPT review of the [v7_MATH4AI_4page](../../../v7_MATH4AI_4page/0_main.pdf) draft for MATH4AI, from the judge prompt [prompt.md](../../input/prompt.md), on the 4 open-venue PDFs built Fri Nov 27 2026 ~6:40 AM PST (commit 7e71010). Saved Fri Nov 27 2026 ~7:30 AM PST. The review judged all 4 drafts in one answer: this file keeps the shared parts and the v7 parts; the other drafts' reviews are in [v4_LoyalAgents_4page_astrained](../v4_LoyalAgents_4page_astrained/by_chatgpt.md), [v5_MultiRobust_4page](../v5_MultiRobust_4page/by_chatgpt.md), [v6_Bench2Evidence_4page](../v6_Bench2Evidence_4page/by_chatgpt.md). Chat-page widget leftovers were turned into tables; every judge sentence and number is kept.

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

# **4. V7 — MATH4AI (W2)**

**Deadline:** December 2, 2026, 4:00 AM PST · Approximately four days

What a One-Contract Preference Loss Can and Cannot Make Switchable

swipo_v7_MATH4AI.pdf

## **PART A — Acceptance probability**

| Setting                 | Estimate   |
| ----------------------- | ---------- |
| MATH4AI acceptance      | **52%**    |
| Typical safety workshop | **67%**    |
| Reviewer score          | **64/100** |

**Recommendation:** Borderline, leaning weak reject.

V7 is empirically competitive with previously accepted safety-workshop papers, but MATH4AI imposes a different standard. Its mathematical contribution is Proposition 1 and Corollary 1 on p. 2, which establish loss separability under independent contract-specific parameters. The result is correct under the stated assumptions, but follows directly from linearity of expectation. More importantly, actual Llama models share parameters across contracts, and the paper explicitly acknowledges that the corollary places no bound on shared-parameter drift. The conclusion that a switchable checkpoint necessarily requires several contracts per request therefore does not follow from the proposition. A mathematically sophisticated reviewer is likely to identify this gap immediately.

### **Three strongest acceptance reasons**

| Rank | Strength                                                          | Evidence                                                                                                                                               |
| ---- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | 🟢 Explicit mathematical result                                   | Proposition 1 and Corollary 1 establish contract-wise gradient separability under independent parameters. p. 2                                         |
| 2    | 🟢 Recognition of the SwiPO objective's mathematical limitations  | The empirical log-ratio penalty is not a divergence estimate, and unboundedness is discussed. p. 2, §§2–3                                              |
| 3    | 🟢 Empirical comparisons relative to initialization               | Both SwiPO chains are compared against their starting points, including paired uncertainty intervals and instrument-dependent effects. p. 2, §2        |

### **Three most likely rejection reasons**

| Rank | Reviewer objection                                                                                                                                                  | Severity     |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 1    | Proposition 1 is elementary, and its independent-parameter assumption does not describe standard transformer-based LLMs. p. 2                                        | 🔴 Very high |
| 2    | The claimed necessity of several contracts per request does not follow from separability; shared parameters can generalize or systematically change unseen-contract behavior. pp. 1–2, 4 | 🔴 Very high |
| 3    | The empirical experiments do not measure gradients, parameter coupling or any mathematical quantity that directly tests the proposed explanation. pp. 2–4             | 🔴 High      |

### **The fundamental mathematical issue**

The paper establishes, under independently parameterized contracts:

$$
L(\theta)=\sum_I p(I)L_I(\theta_I)
$$

Consequently,

$$
\nabla_{\theta_I}L=p(I)\nabla_{\theta_I}L_I.
$$

If only contract $I_0$ occurs in training, then:

$$
\nabla_{\theta_I}L=0,\qquad I\ne I_0.
$$

This is a valid observation under the independence assumptions and ordinary gradient updates.

However, this does not prove that a shared-parameter neural network requires several training contracts for switchability.

Consider a simple shared-parameter policy:

$$
P_\theta(\text{refusal}\mid I)=\sigma(\theta I).
$$

Suppose training occurs only at $I=1$, with an objective that increases $\theta$. The two unseen contracts $I=2$ and $I=-1$ can then develop increasingly different refusal probabilities.

#### **Mathematical counterexample: shared-parameter generalization**

Illustrative mathematical construction, not an additional SwiPO experiment.

| Quantity (shared parameter θ = 1.00; the chat page let θ range from 0 to 3) | Refusal probability    |
| --------------------------------------------------------------------------- | ---------------------- |
| Training contract I = 1                                                     | 73.1%                  |
| Unseen contract I = 2                                                       | 88.1%                  |
| Unseen contract I = −1                                                      | 26.9%                  |
| Refusal-probability gap between the two unseen contracts                    | 61.2 percentage points |

Changing a shared parameter through one training contract can systematically change the behavior of other contracts.

The existing proposition does not rule this out.

The stronger and defensible contribution would be:

> Single-contract training does not directly identify or supervise the desired behavioral contrast between unseen contracts. Whether that contrast emerges depends on the model's inductive bias, initialization and shared-parameter dynamics.

That is a meaningful theoretical limitation, and it is consistent with the observed SwiPO results.

## **PART B — Ten venue-specific rubrics**

| Rubric                               | Why it matters here                                                   | Score      | Evidence                                          | Highest-value change                                                          |
| ------------------------------------ | --------------------------------------------------------------------- | ---------- | ------------------------------------------------- | ----------------------------------------------------------------------------- |
| Mathematical workshop relevance      | Must explain AI through mathematical structure                        | 🟡 7       | pp. 1–2, proposition                              | Make the theoretical result the dominant contribution                         |
| Mathematical novelty                 | Elementary separability alone has limited originality                 | 🔴 5       | Proposition 1, p. 2                               | Develop an identifiability result for unseen contracts                        |
| Formal theorem soundness             | Conclusions must follow from assumptions                              | 🟡 6       | Proposition 1 and Corollary 1                     | Separate independent-policy and shared-policy results                         |
| Applicability of assumptions         | Llama uses shared parameters                                          | 🔴 5       | p. 2, shared-parameter caveat                     | Derive a shared-parameter sensitivity expression                              |
| Optimization-objective analysis      | SwiPO's log-ratio penalty needs rigorous characterization             | 🟡 7       | Eqs. 1–2, p. 2                                    | Prove unboundedness under explicitly sufficient conditions                    |
| Theory-driven predictions            | Experiments should follow from testable mathematical hypotheses       | 🟡 7       | p. 2, five training-step comparison               | Distinguish illustrative observations from predictions                        |
| Empirical controls                   | Theory needs evidence relative to initialization                      | 🟢 8       | §§2–4; Tables 2–3                                 | Add a matched multi-contract training pilot                                   |
| Statistical reliability              | A single run cannot establish general optimization dynamics           | 🟡 6       | p. 4, §6                                          | Repeat targeted runs or a small theoretical experiment                        |
| Claim calibration                    | Necessity and sufficiency require rigorous proof                      | 🟡 6       | Abstract and conclusion                           | Replace unsupported necessity claims with identifiability statements          |
| Mathematical research presentation   | Formal results should receive adequate page allocation                | 🟡 7       | pp. 1–2 versus shared empirical sections          | Remove peripheral sponsor and governance material                             |
| **Total**                            |                                                                       | **64/100** |                                                   |                                                                               |

### **Comparison with accepted papers**

On this mathematical rubric, V7 is approximately at the score of Trust Paradox.

That does not mean its empirical evidence is as weak as Trust Paradox. V7 has stronger statistical reporting and evaluation controls. Its lower overall score arises because its mathematical contribution currently does not meet the same level of persuasiveness as its empirical contribution.

## **PART C — Improvements before the deadline**

### **Improvement 1: Strengthen the theoretical contribution**

I recommend presenting the paper around three logically distinct results.

| Result                                          | Statement                                                                                                                                                                           | Status                          |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Result 1: Contract-wise separability            | Retain the existing proposition, explicitly restricted to independently parameterized conditionals.                                                                                 | Existing result, p. 2           |
| Result 2: Unseen-contract non-identifiability   | Show that two policies agreeing on all observed training tuples can have identical empirical losses while exhibiting different behavior on unseen contracts, provided the policy class admits those extensions. | Proposed theoretical extension  |
| Result 3: Shared-parameter sensitivity          | Characterize how single-contract training can alter a behavioral contrast through parameter coupling, without claiming that such changes must be small or random.                   | Proposed theoretical extension  |

For the third result, define a differentiable contract-sensitivity functional $g(\theta)$, such as a contrast in refusal probabilities. Under a gradient step:

$$
\theta'=\theta-\eta\nabla L(\theta),
$$

a first-order Taylor expansion gives:

$$
g(\theta')-g(\theta)
=
-\eta\left\langle\nabla g(\theta),\nabla L(\theta)\right\rangle
+O(\eta^2).
$$

This provides a mathematical description of shared-parameter coupling.

It explains why a single-contract objective may increase or decrease an unseen-contract contrast, depending on gradient alignment. It does not, by itself, establish that any observed empirical change is caused by a particular gradient interaction.

### **Improvement 2: Analyze the SwiPO penalty properly**

V7's discussion of the objective being unbounded below is potentially interesting but needs explicit conditions.

For one preference pair, let a sufficiently expressive policy rescale both observed answer probabilities by a factor $c$, while redistributing the remaining probability mass elsewhere:

$$
\pi_c(y_w)=c\pi(y_w),
\qquad
\pi_c(y_l)=c\pi(y_l).
$$

Then the DPO log-ratio margin is unchanged:

$$
\Delta_c=\Delta.
$$

But the mean log-ratio penalty becomes:

$$
\bar\rho_c=\bar\rho+\log c.
$$

Therefore, for $\lambda>0$,

$$
L_c=L+\lambda\log c.
$$

As $c$ approaches zero, this expression approaches negative infinity, provided the policy class permits the required probability redistribution consistently across the training support.

That is a useful mathematical observation about the objective. It should be framed as a characterization of the empirical penalty, not merely as an admission of an implementation weakness.

### **Ranked deadline-feasible improvements**

| Priority | Improvement and what it demonstrates | Required work | Placement and what to cut | Estimated gain |
| -------- | ------------------------------------ | ------------- | ------------------------- | -------------- |
| 1 | **Repair and extend the theorem.** Add unseen-contract non-identifiability, a shared-parameter counterexample and the first-order sensitivity expression. | Mathematical derivation and checking, approximately 4–8 hours. No GPU. | Expand §2 into the main theoretical contribution. Cut sponsor and authority experiments from p. 4 and shorten Table 1. | +2 mathematical novelty, +2 applicability, +2 claim calibration |
| 2 | **Formalize the log-ratio penalty's behavior.** Provide sufficient conditions for unboundedness and distinguish it from KL regularization. | Mathematical derivation, approximately 2–3 hours. No GPU. | Replace the informal penalty discussion and duplicate Eqs. 1–2 exposition. | +2 objective analysis |
| 3 | **Theory-oriented toy experiment.** Compare independent contract parameters against shared parameters under single-contract optimization. | Simple logistic or categorical model with controlled synthetic contract-conditioned preference pairs. Multiple random seeds; CPU or less than 1 GPU hour. | Replace Figure 1's adapter schematic or the least relevant empirical table. | +2 theory-driven evidence |
| 4 | **Matched single-contract versus multi-contract training pilot.** Tests whether explicitly supervised contrast improves switchability. | Existing Llama-3.1-8B DPO parent, approximately 500–1,000 quality-controlled training prompts with contrasting contracts and policy-appropriate safe responses. Match loss, initialization, update count and data budget. Approximately 12–36 GPU hours for a small LoRA pilot and evaluation, conditional on the working pipeline. | Replace Table 4 and the sponsor discussion with a compact training-condition comparison. | +2 empirical controls, potentially +1 stability if repeated |
| 5 | **Theory-aligned introduction and conclusion.** Make non-identifiability and shared-parameter coupling the central contribution. | Rewriting, approximately 1–2 hours. | Replace existing abstract, contribution bullets and conclusion. | +1 mathematical presentation |

**Potential revised score: approximately 78–82/100**

The first three improvements are much safer deadline investments than rushing into new LLM training.

If the matched training pilot cannot be completed with a fair comparison and sufficient evaluation, omit it. A coherent theoretical paper with a controlled toy experiment is preferable to an incomplete training comparison.

### **What to cut**

| Cut or compress                                 | Reason                                                              |
| ----------------------------------------------- | ------------------------------------------------------------------- |
| Sponsor experiment, p. 4                        | Strong LoyalAgents relevance but limited mathematical relevance     |
| User/system authority discussion, pp. 3–4       | Does not directly test the proposition                              |
| Length, confidence and stance rows of Table 1   | Add breadth without supporting the mathematical result              |
| Detailed floor discussion                       | Secondary unless formalized as a constrained optimization problem   |
| Duplicated objective exposition across §§2–3    | Frees space for actual mathematical derivations                     |

The goal should be to devote approximately 1.5 of the four main pages to the theoretical contribution, instead of presenting a predominantly empirical paper with a short proposition added near the beginning.

## **PART D — Tone audit**

### **D.1 — Shared and MATH4AI-specific passages**

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

Apply C1–C22 and the common Table 1 label corrections. In V7, C1–C3 appear on p. 2, C4–C5 span pp. 2–3, C6–C14 appear on p. 3, C15–C19 span pp. 3–4 and C20–C22 appear on p. 4.

For this venue, the most serious problems are not negative wording. They are mathematical claims that go beyond the proved result.

| # | Page/section | Quoted original | Problem | Recommended rewrite |
| - | ------------ | --------------- | ------- | ------------------- |
| T1 | p. 1, title | “What a One-Contract Preference Loss Can and Cannot Make Switchable” | Negative construction; vague mathematical contribution | Contract-Wise Separability and the Limits of Single-Contract Preference Optimization |
| T2 | p. 1, abstract | “We state when a contract-conditioned preference loss can produce such a switch.” | Overstates the scope of the theorem | We characterize the contract-specific gradient supervision provided by a conditioned preference loss. |
| T3 | p. 1, abstract | “so training can move the switch only by drift through shared parameters.” | Treats shared-parameter generalization as unstructured drift | Consequently, behavioral differences between unseen contracts can change through shared-parameter coupling rather than direct contrast supervision. |
| T4 | p. 1, abstract | “By the refusal-phrase heuristic neither SwiPO chain gains over its start” | Positive point estimate incorrectly grouped with measured decline | Phrase-based scoring reveals an unresolved improvement for SwiPO-S and a statistically resolved decrease for SwiPO-R relative to their respective starting configurations. |
| T5 | p. 1, abstract | “only SwiPO started without it keeps a switch under both instruments” | Negative framing; requires scope restriction | Among the contract-trained configurations, SwiPO initialized without SFT retains switching under both measurement instruments. |
| T6 | p. 1, abstract | “A switchable checkpoint therefore needs training data with several contracts per request, which the separability result makes precise.” | Unsupported mathematical necessity | The separability result identifies the absence of direct supervision for unseen-contract contrasts, motivating training data that explicitly represents multiple contracts and their preferred responses. |
| T7 | p. 1, contribution | “the loss is blind to every other contract” | Informal criticism | Under independent contract-specific parameterization, a single-contract loss provides gradients only to the observed contract's conditional parameters. |
| T8 | p. 2, §2 | “DPO is the case λ = 0 with I dropped” | Imprecise formulation | Setting λ = 0 recovers the DPO objective conditioned on the supplied prompt, which may include I; SwiPO additionally introduces the log-ratio penalty with λ > 0. |
| T9 | p. 2, §2 | “We state both results for gradients, not minimizers: with λ > 0 the penalty lowers both likelihoods and L is unbounded below.” | Reads defensively; missing sufficient conditions | The results concern gradient supervision rather than existence of minimizers. For λ > 0, jointly reducing the observed response-pair likelihoods can drive the objective arbitrarily low in policy classes permitting the required probability redistribution. |
| T10 | p. 2, §2 | “The argument uses only that L is an expectation over tuples, so it covers SFT and GRPO as well.” | Overgeneralization | The separability argument extends to objectives with contract-local loss terms and independent contract-specific parameters, including corresponding SFT and GRPO formulations when their additional terms satisfy these conditions. |
| T11 | p. 2, §2 | “The corollary bounds no drift through shared parameters, so any change in the gap is drift, of either sign.” | Labels a mechanism without establishing it | The independent-parameter corollary does not bound changes under shared parameterization. Such changes may have either sign and can arise through parameter coupling and generalization. |
| T12 | p. 2, §2 | “By phrase neither chain gains.” | Incorrect interpretation of uncertainty | Phrase-based scoring yields an unresolved change of +0.017 [−0.025, +0.057] for SwiPO-S and a decrease of −0.113 [−0.155, −0.070] for SwiPO-R. |
| T13 | p. 2, §2 | “The direction depends on the instrument, as drift would.” | Treats measurement disagreement as evidence for a particular mechanism | The estimated direction depends on the measurement instrument, demonstrating that conclusions about contract sensitivity require explicit behavioral definitions. |
| T14 | p. 4, Related Work | “which Proposition 1 shows is what makes a conditioned optimum switchable.” | Proposition concerns gradients, not optimal policies; does not prove sufficiency | These approaches provide direct supervision across multiple conditions, addressing the contract-support limitation characterized by Proposition 1. |
| T15 | p. 4, Conclusion | “A contract-conditioned preference loss separates by contract, so it fits only the switch its data contains.” | Omits independence assumption; overstates result | Under independently parameterized conditionals, a contract-conditioned preference loss separates into contract-specific objectives, identifying the scope of direct gradient supervision. |
| T16 | p. 4, Conclusion | “Trained with one contract, SwiPO, DPO, and GRPO change their starting model’s switch only by small drift whose sign depends on the instrument” | No theoretical bound on magnitude; judge changes can be resolved | Under the evaluated single-contract training configurations, phrase-based and judge-based measurements exhibit different changes relative to initialization, motivating explicit analysis of shared-parameter coupling. |
| T17 | p. 4, Conclusion | “A switchable checkpoint needs tuples that pair one request with several contracts and different preferred answers.” | Unsupported necessity claim | Paired requests with contrasting contracts and preferred answers offer a direct mechanism for supervising the behavioral differences that single-contract data do not explicitly identify. |

### **D.2 — Three most important rewrites**

1. **T6 and T17: Remove the unsupported necessity claim.** A reviewer can reject this paper on logical grounds even if all empirical results are accepted.
2. **T11 and T13: Distinguish shared-parameter coupling from an empirically established mechanism.** The experiments measure behavior, not gradients or parameter coupling.
3. **T12: Preserve the correct interpretation of paired intervals.** SwiPO-S has a positive point estimate whose interval includes zero. SwiPO-R has a resolved negative phrase-based change and a resolved positive judge-based change.

### **D.3 — Rewritten abstract**

This version preserves the current mathematical result without claiming that the proposed new theorems or experiments have been completed.

We characterize gradient supervision in contract-conditioned preference optimization through a separability result: for independently parameterized contract conditionals, the objective decomposes into contract-specific losses, so each conditional receives gradients from its own training data. With one training contract, contrasts between unseen contracts receive no direct supervision; their behavior can nevertheless change through shared-parameter coupling. We examine this distinction in preference-trained Llama-3.1-8B models using DPO, GRPO, and SwiPO, an instruction-conditioned DPO with a reference-model log-ratio penalty, alongside a released PPO model with an untrained adapter. All configurations use single-contract training and complete checkpoint reconstruction. Relative to initialization, phrase-based refusal gaps change by +0.017 (95% interval −0.025 to +0.057) for retrained SwiPO and −0.113 (−0.155 to −0.070) for released SwiPO. The LLM judge measures changes from −0.034 to +0.055 across five single-contract training steps. The pretrained model's phrase gap of 0.299 (0.266 to 0.332) contrasts with a judge gap of 0.012 and is substantially attenuated by supervised fine-tuning. Among contract-trained configurations, SwiPO initialized without supervised fine-tuning retains switching under both instruments (judge gap 0.128). These findings distinguish direct contract-contrast supervision from initialization-dependent and shared-parameter behavior, motivating preference data that explicitly represent multiple contracts and their desired responses.

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
| V7 — MATH4AI | Replace the unsupported multi-contract necessity claim with a rigorous non-identifiability result, a shared-parameter counterexample and a sensitivity derivation. | Expand §2 using space from peripheral empirical results. Estimated gain: 6 points. No GPU required. |

# **Deadline-prioritized action plan for this venue**

Since LoyalAgents and MultiRobust have less than 20 hours remaining, I would allocate effort according to deadline rather than acceptance ranking.

Submission sprint (the chat page showed 9 tasks, 0/9 completed; this file keeps the shared tasks and this venue's tasks):

| When | Task | Estimate | Status |
| ---- | ---- | -------- | ------ |
| Nov 27 • While inference runs | Apply abstract rewrites, correct null-result language and relabel PPO. | 1–2 working hours | ⬜ |
| Nov 27–28 • Before submission | Verify four-page layouts, anonymity and related-submission disclosure. | 1 working hour | ⬜ |
| Nov 28–30 | Strengthen MATH4AI theory, derive penalty behavior and run a toy experiment. | 6–12 working hours | ⬜ |
| Nov 30–Dec 1 | Optional matched multi-contract training pilot if time and compute permit. | 12–36 GPU hours | ⬜ |
| Dec 1 | Final consistency and four-page formatting checks for the Dec 2 submissions. | 2–3 working hours | ⬜ |

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
