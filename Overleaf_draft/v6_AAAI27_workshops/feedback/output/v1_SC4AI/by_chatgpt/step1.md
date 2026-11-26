# 🤖 ChatGPT · Step 1 · Calibration sheet

> **Judge:** ChatGPT (fresh chat, worked 3 m 32 s) · **Input:** [combined PDF of 6 accepted papers](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 1
>
> **Workshop:** AAAI-26 "How Can We Trust and Control Agentic AI?" · Page numbers = PDF pages of the combined file.

> [!NOTE]
> The judge's text below is kept in full; only the layout changed. Claude Code's verification notes are in the last section, [🔎 Fact-check](#-fact-check-by-claude-code-not-chatgpt).

**Legend:** 📄 paper · 🎯 core claim · 📊 main evidence · ✅ likely acceptance reason · ⚠️ calibration detail · 🟢 essential · 🟡 helpful, not universal · ⚪ not required

## 📌 TL;DR

| What | ChatGPT's answer |
|---|---|
| 🏁 Central takeaway | The accepted set rewards a **clear, workshop-relevant contribution backed by concrete empirical evidence**. It does not require frontier-scale models, exhaustive benchmarks, extensive inferential statistics, or a solved safety problem. |
| ⚖️ Key distinction | A paper with a **limited but clearly demonstrated** contribution is tolerated; a paper whose **claims extend beyond what its experiments establish** is not. |
| 📈 Statistics | Formal significance tests are **not** a universal bar in this sample. |
| 🖼️ Figures | All six use visual evidence; strongly recurring. |
| 📏 Length | Main text about 4 to 7 pages before references. |

This calibration is based on the papers as they appear in the 82-page PDF, including appendices where relevant. It separates what the papers demonstrate from what may have made them attractive to reviewers. There are no reviewer scores or deliberations, so the acceptance explanations are informed inferences, not confirmed reasons.

## 1️⃣ The six accepted papers: three-line assessment each

### 📄 1. The Trust Paradox: When Over-Alignment Reduces Human Trust in Agentic AI · pp. 1–5

| | |
|---|---|
| 🎯 **Core claim** | Increasing alignment intensity does not necessarily increase trust; excessive safety, politeness, and deference can reduce perceived trustworthiness. |
| 📊 **Main evidence** | 120 generated dialogues across four Llama models, five scenarios, six alignment levels. Figure 1 (p. 2) shows the non-monotonic relationship; Figures 2–4 (p. 3) compare models, scenarios, trust components; p. 4 reports $F(5,100)=12.34,\ p<0.001$ plus component correlations. |
| ✅ **Likely accepted because** | A memorable, counterintuitive proposition (more alignment may reduce trust) that fits the workshop theme, supported by a compact multi-factor experiment and a clear practical implication. |
| ⚠️ **Calibration detail** | Does not measure human trust directly; the score is built from programmatic dialogue proxies. The peak-to-minimum trust difference is small: 0.748 vs 0.743. Remember this gap between framing strength and evidence limits when reviewing a similarly ambitious claim. |

### 📄 2. When Refusals Fail: Unstable Safety Mechanisms in Long-Context LLM Agents · pp. 6–17

| | |
|---|---|
| 🎯 **Core claim** | Long context can degrade both agent capability and refusal behavior; advertised context-window capacity does not guarantee safe or reliable agent execution. |
| 📊 **Main evidence** | AgentHarm across four models, varying context length, padding type, and position. Figure 2 (p. 8) plots harmful/benign performance and refusal rates; Figures 3–4 (pp. 8–9) compare padding types and placement. Error bars are $1\sigma$; the appendix documents at least three seeds. |
| ✅ **Likely accepted because** | A timely, concrete safety gap (long-context safety in tool-using agents, not just long-context text generation), with striking evidence of capability degradation and model-dependent refusal instability. |
| ⚠️ **Calibration detail** | Main experiments use the easiest AgentHarm subset (tasks with hints and detailed instructions); the authors call their results an upper bound. The appendix covers category-specific behavior and delayed refusals, where an agent acts before refusing. |

### 📄 3. ShieldBench: Evaluating the Persistence of LLM Safety Interventions · pp. 18–25

| | |
|---|---|
| 🎯 **Core claim** | A safety intervention should be judged not only by its immediate effect but by whether its gains persist after retraining or adversarial pressure. |
| 📊 **Main evidence** | Six weight-space interventions × five 7B–8B models × three datasets (HarmBench, HEX-Phi, WMDP). Figures 1–6 (pp. 20–21) persistence heatmaps; Figures 7–11 (p. 22) stress gradients; Tables 2–4 (p. 23) before/after comparisons. |
| ✅ **Likely accepted because** | A clearly articulated benchmark, a unified comparative evaluation, datasets of differing difficulty, and a useful negative finding: no single intervention works across models and risk domains. |
| ⚠️ **Calibration detail** | The central result is not "safety edits work" but that persistence depends on intervention × architecture × dataset. WMDP exposes failures that look less apparent on the easier HarmBench. |

### 📄 4. From Biased Chatbots to Biased Agents: Role Assignment Effects on LLM Agent Robustness · pp. 26–31

| | |
|---|---|
| 🎯 **Core claim** | Demographic persona assignments can change an LLM agent's task performance, even when the identity is irrelevant to the task. |
| 📊 **Main evidence** | Three models, 23 personas across four demographic categories, five agentic benchmarks. Table 2 (p. 28) is central; Figures 2–4 (pp. 28–29) break down gender, profession, religion. Some reductions reach 26.2%. |
| ✅ **Likely accepted because** | A straightforward extension of persona-bias concerns into action-taking agents, across multiple domains, with a striking, easily communicated result. |
| ⚠️ **Calibration detail** | Results are heterogeneous: some personas reduce performance, others improve it, and effects differ by model and task. The paper frames this volatility as a robustness and fairness concern, not a uniform harm. |

### 📄 5. IntentGuard: Safeguard LLM Agents via Intent Alignment · pp. 32–45

| | |
|---|---|
| 🎯 **Core claim** | Agent safety should be evaluated against the user's original intent throughout execution, not only against static rules or isolated tool calls. |
| 📊 **Main evidence** | Runtime framework with a Plan Gate and Tool Gate on Agent Security Bench. Table 1 (p. 37) vs several defenses; Tables 2–6 (pp. 37–38) domain performance, model selection, gate ablations, components, rewrite limits; Figures 1–3 motivating example, workflow, use case. |
| ✅ **Likely accepted because** | A practical defense with a distinctive design, end-to-end agent evaluation, security and utility metrics, several baselines, and ablations showing why components matter. |
| ⚠️ **Calibration detail** | Adds inference overhead: 10.50 requests and 16.43 s (GPT-4o IntentGuard) vs 3.40 requests and 11.23 s (no defense). A System Administration outlier shows weaker utility. |

### 📄 6. Teach a Reward Model to Correct Itself (REFORM) · pp. 46–82

| | |
|---|---|
| 🎯 **Core claim** | A reward model can help discover its own blind spots: REFORM generates class-consistent but reward-inconsistent examples, then uses targeted augmentation to improve robustness. |
| 📊 **Main evidence** | Anthropic HH and PKU Beavertails, Mistral-7B and Qwen 2.5 14B reward models. Figures 4–5 (p. 51) failure discovery and perturbation robustness; Figures 6–8 and Table 1 (p. 52) downstream alignment and reward utility; appendix adds Qwen results and trade-offs. |
| ✅ **Likely accepted because** | A distinctive self-improvement mechanism, a clear link to reward hacking and alignment, and evidence across datasets, perturbations, reward models, and downstream alignment strategies. |
| ⚠️ **Calibration detail** | Reports 35–45% average robustness improvement, but the reward-utility table shows small drops in unperturbed accuracy: a robustness/utility trade-off, not zero regression. |

## 2️⃣ The common acceptance bar in this sample

The six papers are not methodologically uniform (a compact empirical study, benchmarks, runtime defenses, a reward-model training procedure). The shared bar is a set of recurring qualities, not a single numerical standard.

| Dimension | What recurs across the accepted papers | Calibration implication |
|---|---|---|
| 🧭 Problem framing | Each names a specific safety, trust, bias, or robustness problem with consequences for deployed LLMs or agents. | Needs a recognizable problem, not just an interesting behavior. |
| 🕳️ Gap statement | Each explains what existing evaluations, methods, or assumptions miss. | Novelty should answer a stated gap. |
| 💡 Novelty | A named phenomenon, benchmark, guardrail, systematic case study, or procedure. | A new algorithm is not mandatory; a new evaluation perspective can suffice. |
| 📊 Evidence | Every paper has empirical comparisons across models, settings, tasks, or datasets. | The claim needs observable evidence and a meaningful comparison. |
| 📈 Statistics | Varies widely: some inferential statistics, others means, plots, tables. | Formal significance testing is not universal here. |
| 🖼️ Figures and tables | All six use figures and/or tables for the central claim. | Visual evidence is expected, not decoration. |
| 📏 Length | Main text about 4 to 7 pages before references. | A tightly scoped contribution fits. |
| ✍️ Writing tone | Direct, problem-first, assertive about the contribution, practical. | A clear, confident narrative matters. |
| ⚠️ Limitations | All acknowledge some; amount and placement vary. | Candid acknowledgment is compatible with acceptance; exhaustive analysis is not universal. |

### 🧭 Framing: a concrete gap plus a consequence

The introductions follow a recognizable sequence:

1. **Establish the risk:** trust miscalibrated, refusals fail, safety edits brittle, personas distort behavior, actions drift from intent, reward models exploited.
2. **Identify the missing piece:** the behavior was not tested in this setting, under this stressor, or with the needed persistence or utility measure.
3. **State the contribution:** name the study, benchmark, framework, or procedure.
4. **Connect to deployment:** why it matters for trustworthy or safe AI.

Visible in When Refusals Fail (p. 6), ShieldBench (pp. 18–19), Role Assignment (p. 26), IntentGuard (pp. 32–33).

### 💡 Novelty: explicit, not necessarily theoretical

They make novelty legible early ("first systematic case study", "first benchmark", "novel runtime guardrail", "we introduce"). Three kinds of contribution fit:

| Kind | Examples |
|---|---|
| 🔬 New empirical finding | The Trust Paradox; persona effects on agents |
| 🧪 New evaluation framework | ShieldBench; long-context agent evaluation |
| 🛠️ New intervention or mechanism | IntentGuard; REFORM |

### 📊 Evidence footprints vary widely

| Paper | Main evidence footprint |
|---|---|
| The Trust Paradox | 4 models × 5 scenarios × 6 alignment levels; 120 dialogues |
| When Refusals Fail | 4 models, 176 AgentHarm samples, several context lengths, padding types, positions; ≥ 3 seeds |
| ShieldBench | 5 small open models × 6 interventions × 3 datasets, adversarial fine-tuning stress tests |
| Role Assignment | 3 models × 23 personas × 5 benchmarks |
| IntentGuard | 90K ReAct traces, about 1.2M tool-invocation steps in the benchmark; multiple defenses and ablations |
| REFORM | 2 preference datasets, 2 reward-model sizes, 4 perturbation types, 3 downstream alignment strategies |

The commonality is a **measurable comparison tied to the main claim**, not a fixed number of experiments.

### 📈 Statistics: no strict p-value requirement

| Paper | Statistical reporting |
|---|---|
| The Trust Paradox | Mixed-effects analysis, F statistic, correlations, p-values (p. 4) |
| When Refusals Fail | Means and SD over ≥ 3 seeds, $1\sigma$ error bars (pp. 8–9; appendix p. 11) |
| ShieldBench | Heatmaps, persistence scores, stress gradients, tables (pp. 20–23); little conventional inference |
| Role Assignment | Baseline-relative changes; no p-values, CIs, or repeated-run uncertainty (pp. 27–29) |
| IntentGuard | Some five-run averages in model-selection ablation (p. 37); no consistent significance analysis |
| REFORM | Comparative metrics and plots; no systematic significance testing in main text (pp. 50–52) |

**Calibration:** formal statistics strengthen a paper, but this set does not make p-values, CIs, or significance tests universal prerequisites.

### 🖼️ Visual storytelling

| Paper | Main visual strategy |
|---|---|
| The Trust Paradox | Central trend plot plus model, scenario, component plots |
| When Refusals Fail | Workflow and error-bar plots across lengths, types, positions |
| ShieldBench | Persistence heatmaps, model-method comparisons, stress gradients |
| Role Assignment | Motivating illustration, large comparative table, persona-effect plots |
| IntentGuard | Architecture/workflow diagrams, baseline tables, ablations, execution examples |
| REFORM | Method diagrams, perturbation comparisons, downstream quality plots |

### ✍️ Length and writing tone

Main text about four to seven pages before references; appendices vary (When Refusals Fail several pages; IntentGuard prompt templates and use cases; REFORM very extensive). Style is mostly:

- problem-first, not a long theoretical preamble;
- assertive in the abstract and introduction;
- explicit about the contribution;
- organized around a few results or research questions;
- practical about deployment implications;
- more cautious about mechanisms than about the core observed result.

Strong terms ("first", "comprehensive", "model-agnostic") are not disqualifying, as long as the evaluation supports them.

## 3️⃣ What these accepted papers get away with

Weaknesses visible in accepted papers (not a claim that they are unimportant):

| Paper | Weaknesses that did not prevent acceptance |
|---|---|
| The Trust Paradox | Programmatic proxies instead of human trust; small trust difference; all four models Llama-family; interpretation stronger than direct human evidence. |
| When Refusals Fail | Easiest AgentHarm subset; few models; provider safety filters may confound; some token counts not tokenizer-normalized. |
| ShieldBench | Only 7B–8B open models; adversarial fine-tuning approximates adaptive attacks; incomplete dataset coverage; WMDP lacks paired benign/harmful prompts; little inferential statistics. |
| Role Assignment | Three models, limited benchmarks/personas; no significance or uncertainty; single deterministic configurations; stereotype explanations are interpretations, not tested mechanisms. |
| IntentGuard | Relies on LLM-based gates; meaningful runtime and request overhead; one outlier domain; model-agnostic claim qualified by model capability; limitations in appendix. |
| REFORM | Two preference datasets, few perturbation types; LLM-based evaluation for some metrics; one sampling round for some experiments; imperfect coverage of non-preferred responses and capitalization robustness; some results in appendix. |

### ⭐ The five most important tolerated weaknesses

1. **Limited generalization is common.** Few models, datasets, or environments; broader coverage left to future work.
2. **Mechanism claims can outrun the experiments.** ShieldBench's weight-space geometry; persona paper's stereotype explanations.
3. **Statistical reporting is uneven.** Persona paper: broad table, sizeable changes, little inference; others use SD without significance tests.
4. **Some metrics are proxies.** Trust Paradox dialogue proxies; REFORM LLM-based judgments; IntentGuard ASR, FNR, RER.
5. **Important caveats sit in appendices.** IntentGuard, REFORM, When Refusals Fail.

> **Overall lesson:** a paper need not solve the field's whole problem. It must define a credible slice, offer a distinct contribution, and provide evidence that makes that slice worth discussing.

## 4️⃣ The novelty-selling sentence from each paper

| Paper | Novelty sentence | Page |
|---|---|---|
| 1. The Trust Paradox | "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." | p. 1 |
| 2. When Refusals Fail | "Prior works have focused mainly on evaluation of LLMs on long-context prompts, leaving agentic setup relatively unexplored, both from capability and safety perspectives." | p. 6 |
| 3. ShieldBench | "We introduce ShieldBench, a benchmark designed to evaluate not only immediate safety compliance but also the persistence of safety interventions under realistic usage conditions." | p. 18 |
| 4. Role Assignment | "We present the first systematic case study showing that demographic-based persona assignments can alter LLM agents' behavior and degrade performance across diverse domains." | p. 26 |
| 5. IntentGuard | "IntentGuard maintains coherent agent intent through continuous intent alignment during task execution, incorporating two safety gates: the Plan Gate and the Tool Gate." | p. 32 |
| 6. REFORM | "Use the RM itself as a search signal to generate responses that contradict its own scoring while preserving the underlying preference class." | p. 46 |

**Pattern:** these sentences do not open with implementation details. They say what is new and what problem it addresses; configurations, metrics, and implementation come later.

## 5️⃣ How the papers discuss limitations and negative results

| Paper | Where limitations appear | Tone and treatment of negative results |
|---|---|---|
| The Trust Paradox | Short "Limitations and Future Work" on p. 4, then an ethical statement. | Brief, non-defensive. Main caveat (programmatic proxies, not human evaluation) turned into a future-work recommendation. |
| When Refusals Fail | Discussion on p. 9; fuller "Limitations and Ethics" in appendix, p. 16. | Detailed and candid: model-specific differences, limits of refusal rate as a metric, delayed refusals; names the easiest-subset choice and API confounds. |
| ShieldBench | Formal "Limitations" on p. 24. | Structured: model scale, attack sophistication, dataset coverage, fine-tuning setup, compute, open-source-only scope. HEX-Phi and WMDP failures are central to the argument. |
| Role Assignment | "Limitations and Future Work" paragraph, p. 29. | Concise, forward-looking; mixed effects discussed in results, not hidden. |
| IntentGuard | No substantial main-text section; short "A.3 Limitations" in appendix, p. 42. | Main text still discloses the outlier domain, model-choice dependence, and runtime/request cost. |
| REFORM | Embedded in Results, p. 50; expanded in appendix, pp. 56–57 and 59–62. | Results-driven and candid: incomplete discovery for some non-preferred responses, sampling cost, slight regressions, top-k and Best-of-N trade-offs. |

### ✅ What they do well with negative results

1. **They explain why the negative result matters.** ShieldBench uses WMDP failures to argue persistence evaluation is necessary; When Refusals Fail uses divergent refusal behavior to question refusal rate as a metric.
2. **They acknowledge trade-offs without abandoning the contribution.** IntentGuard's cost and weak domain; REFORM's slight drops. Presented as constraints, not reasons to discard the idea.
3. **Placement is flexible.** Main text or appendix, but caveats and major negative findings appear somewhere.

## 6️⃣ Practical calibration summary

| Question | What the accepted sample suggests |
|---|---|
| Relevant to trustworthy, safe, aligned, or robust agents? | 🟢 Essential. All six connect directly to the theme. |
| Is the gap clear and specific? | 🟢 Essential. |
| Is there a recognizable contribution? | 🟢 Essential (phenomenon, study, benchmark, framework, or algorithm). |
| Evidence directly supporting the central claim? | 🟢 Essential, despite different evidence footprints. |
| Multiple models and datasets? | 🟡 Helpful, not universal. |
| p-values and confidence intervals? | ⚪ Not a universal requirement here. |
| An ablation study? | ⚪ No; prominent in method papers only. |
| Figures? | 🟢 Strongly recurring; all six use them. |
| Limitations in the main text? | ⚪ No; some use appendices. |
| Must the contribution be a new algorithm? | ⚪ No; empirical studies and benchmarks were accepted. |

> **Central takeaway:** the accepted set rewards a clear, workshop-relevant research contribution backed by concrete empirical evidence. The key distinction is between a paper with a **limited but clearly demonstrated** contribution and one whose **claims extend substantially beyond its experiments**. The accepted examples tolerate the former, not the latter.

## 🔎 Fact-check (by Claude Code, not ChatGPT)

Checked 2026-11-26 against the text of the [combined PDF](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf).

| # | Judge claim | Found in the PDF? | Verdict |
|---|---|---|---|
| 1 | Page ranges 1–5, 6–17, 18–25, 26–31, 32–45, 46–82 | Each paper's title is on pp. 1, 6, 18, 26, 32, 46 | ✅ |
| 2 | Trust Paradox: 120 dialogues; $F(5,100)=12.34$; trust 0.748 vs 0.743 | All three numbers present | ✅ |
| 3 | Role Assignment: reductions up to 26.2% | Present | ✅ |
| 4 | IntentGuard: 10.50 requests, 16.43 s vs 3.40 requests, 11.23 s | All four present | ✅ |
| 5 | REFORM: 35–45% average robustness improvement | "average improvement of 35%–45%" present | ✅ |
| 6 | Novelty quotes for papers 1, 3, 4 ("Trust Paradox in AI alignment", "We introduce ShieldBench", "first systematic case study") | Present | ✅ |
| 7 | Other details (figure/table numbers per page, appendix page numbers, quotes for papers 2, 5, 6) | Not checked line by line | ⚪ unverified |
