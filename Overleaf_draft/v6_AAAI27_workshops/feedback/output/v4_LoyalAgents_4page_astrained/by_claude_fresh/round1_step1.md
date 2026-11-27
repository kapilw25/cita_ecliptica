# STEP 1: Calibration sheet from 6 papers accepted at the AAAI-26 workshop "How Can We Trust and Control Agentic AI?"

Source: `aaai26ws_trustagent_00_combined_6papers.pdf` (82 pages). Page numbers below are pages of the combined PDF ("p."), so they can be checked in one file.

| # | Paper | Combined-PDF pages | Main text | References | Appendix |
|---|---|---|---|---|---|
| 1 | The Trust Paradox | pp. 1-5 | pp. 1-4 (about 3.7 pages) | p. 5 | none |
| 2 | When Refusals Fail | pp. 6-17 | pp. 6-9 (4 pages) | p. 10 | pp. 11-17 |
| 3 | ShieldBench | pp. 18-25 | pp. 18-24 (about 6.5 pages) | pp. 24-25 | none |
| 4 | Role Assignment Effects ("From Biased Chatbots to Biased Agents") | pp. 26-31 | pp. 26-29 (about 3.7 pages) | pp. 29-31 | none |
| 5 | IntentGuard | pp. 32-45 | pp. 32-38 (about 6.5 pages) | p. 39 | pp. 40-45 |
| 6 | Teach a Reward Model to Correct Itself (REFORM) | pp. 46-82 | pp. 46-52 (about 7 pages) | pp. 53-55 | pp. 56-82 |

## 1. Each paper in three lines

**(1) The Trust Paradox** (pp. 1-5)
- Core claim: raising "alignment intensity" (a system-prompt dial from 0.0 to 1.0) beyond an optimum lowers trust; trust peaks at 0.0, and authenticity correlates with trust (0.771) while obedience correlates negatively (-0.450) (abstract, p. 1).
- Evidence: 120 dialogues = 4 Llama models x 5 scenarios x 6 intensity levels (p. 2); Figure 1 trust vs intensity (p. 2), Figures 2-4 heatmaps, scenario curves and component plots (p. 3); mixed-effects test F(5,100) = 12.34, p < 0.001 and correlations (p. 4).
- Why accepted: a named, counterintuitive phenomenon ("Trust Paradox") squarely on the workshop's "trust" theme, a clean single-variable design, and confident implications ("optimal alignment requires balancing safety with trust", p. 1). Not the strength of evidence (see Section 3).

**(2) When Refusals Fail** (pp. 6-17)
- Core claim: agents with 1M-2M token windows lose more than 50% of capability by 100K tokens of padding, and refusal rates shift unpredictably (GPT-4.1-nano about 5% to about 40%, Grok 4 Fast about 80% to about 10% at 200K) (abstract, p. 6).
- Evidence: AgentHarm extended with padding length, type and position; Figure 2 harm score and refusal vs padding (p. 8), Figure 3 padding type (p. 8), Figure 4 position (p. 9); error bars are 1 sigma over at least 3 seeds (Appendix B, p. 11); per-category figures in the appendix (p. 13).
- Why accepted: a known agent-safety benchmark pushed along one controllable, deployment-relevant axis; four bulleted findings in the abstract; real tool-using agents; an honest limitations paragraph; the most rigorous of the short papers.

**(3) ShieldBench** (pp. 18-25)
- Core claim: "the first benchmark explicitly designed to evaluate the persistence of LLM safety interventions" (p. 18); persistence depends on the interaction of method, model and dataset ("weight-space geometry", p. 23).
- Evidence: 6 weight-space edits x 5 open 7-8B models x 3 datasets (HarmBench, HEX-Phi, WMDP); absolute and row-normalized persistence heatmaps (Figures 1-6, pp. 20-21), stress gradients under adversarial fine-tuning (Figures 7-11, p. 22), persistence tables (Tables 2-4, p. 23).
- Why accepted: a "first benchmark" claim with breadth (90 model x method x dataset cells) and a crisp takeaway ("no single intervention universally dominates", p. 19).

**(4) Role Assignment Effects on LLM Agent Robustness** (pp. 26-31)
- Core claim: "the first systematic case study" showing that task-irrelevant demographic personas change agent performance, by up to 26.2% (p. 26).
- Evidence: 3 models (GPT-4o-mini, DeepSeek-V3, Qwen3-235B) x 23 personas x 5 agent benchmarks (ALFWorld, WebShop, Card Game, OS, Database); Table 2 of relative changes with arrows (p. 28); Figures 2-4 for gender, profession and religion (pp. 28-29).
- Why accepted: a quotable headline number, a fairness-meets-agents angle that is new for the venue, and a compact, readable Table 2.

**(5) IntentGuard** (pp. 32-45)
- Core claim: a training-free, model-agnostic runtime guardrail (Plan Gate plus Tool Gate) that checks each plan and tool call against the user's original intent; average attack success rate falls from 71.45 (no defense) to 6.15 (Table 1, p. 37).
- Evidence: Agent Security Bench with 5 prompt-injection families; Table 1 vs 6 baselines (p. 37), Table 2 per domain (p. 37), ablations on gate LLM, gate on/off, filter and rewrite limit (Tables 3-6, pp. 37-38), a worked case (Figure 3, p. 38), code link (p. 32).
- Why accepted: a working method with large margins on an established agent benchmark, ablations, and a framing (act only on the user's intent) that is close to "control" of agents.

**(6) Teach a Reward Model to Correct Itself (REFORM)** (pp. 46-82)
- Core claim: a reward model can be its own adversary; reward-guided decoding finds class-consistent but reward-inconsistent responses, and retraining on the top 5% most influential pairs improves robustness by 35%-45% without hurting in-distribution accuracy or Best-of-N, PPO and DPO quality (p. 46).
- Evidence: Anthropic HH and PKU BeaverTails with Mistral-7B and Qwen-2.5-14B; failure discovery radar (Figure 4, p. 51), win-rate drop under 4 perturbations (Figure 5, p. 51), win rate on clean data (Table 1, p. 52), downstream BoN, PPO and DPO quality (Figures 6-8, pp. 50-52).
- Why accepted: a full method paper with numbered claims C1-C3 and contributions C1-C6 (pp. 46-47), three downstream alignment regimes, and a long appendix; it reads like a main-conference paper placed at a workshop.

## 2. The common bar (what every accepted paper has)

| Dimension | What all six share | Range across the six |
|---|---|---|
| Framing | Opens on deployment risk of agents or aligned models and ends on implications for safe deployment | From "trust" (1) to agent tool use (2, 4, 5) to model internals (3, 6) |
| Novelty statement | One sentence in the abstract that names the new thing: a phenomenon (1), a gap (2), a "first" benchmark or study (3, 4), a "novel" framework (5), a new capability of reward models (6) | Two papers say "first" (pp. 18, 26); none states novelty relative to a named closest work |
| Evidence level | At least 3 models or configurations and at least one manipulated variable; one main table or figure carries the claim | 120 dialogues (1) to 6 x 5 x 3 grid (3); 2 to 5 models |
| Statistics | Very light. Only paper 2 shows uncertainty (1 sigma over at least 3 seeds, p. 11); paper 1 reports p-values and an F-test (p. 4); paper 5 averages 5 repeats without spread (p. 36); papers 3, 4 and 6 report point estimates only | No paper reports confidence intervals |
| Length | 4 to 7 pages of main text; appendices optional | 3.7 pages (1, 4) to 7 pages (6) |
| Figures | Every paper has a figure or table on its page 1 or 2 (ShieldBench's first is Table 1, p. 19) and at least 4 figures or tables in total | 4 (paper 1) to 15 (paper 3) |
| Writing tone | Confident and positive: findings are stated as facts about models, never as corrections of the authors' own process | "counterintuitive finding" (p. 1), "overlooked vulnerability" (p. 26), "significantly and consistently outperforming" (p. 32) |
| Completeness | Every result promised in the abstract is in the body; no placeholders | Papers 5 and 6 move some baselines and details to the appendix |

## 3. What these papers get away with (weaknesses that did not block acceptance)

- **No uncertainty at all** in papers 3, 4 and 6, and none of the six reports confidence intervals. Paper 4 interprets single deterministic runs ("we use deterministic decoding", p. 27) as stereotypes ("reflects societal stereotypes about domestic competencies", p. 28) even for shifts of 2-4 points.
- **Tiny effects called significant.** Paper 1's peak trust is 0.748 vs a minimum of 0.743 (p. 2), and it says "The Trust Paradox is statistically significant, with a correlation of -0.143" (p. 3). Its design has one dialogue per cell (4 x 5 x 6 = 120, p. 2).
- **Proxy metrics with built-in circularity.** Paper 1's trust score is T = 0.3 x (1 - O) + 0.3 x A + 0.2 x C + 0.2 x R (Eq. 1, p. 2), so the negative obedience-trust correlation is partly true by construction; trust is never measured with humans (admitted, p. 4).
- **Factual slips.** Paper 1 lists "Llama-3.3-8B-Instruct" (p. 2), and its figures are too small to read (pp. 2-3). Paper 5's text says the best pair is Plan GPT-4o with Tool GPT-4o-mini (p. 37), but in Table 3 that row has ASR 6.25 while the 4o/4o row has 4.75, the number Table 4 attributes to the "best pair" (p. 37).
- **Broken cross-references and typos.** Paper 6 has "Appendix ." and "Section ." throughout (pp. 49-50), "Table/Figure 1" (p. 50) and "REFORMconsistently" (p. 46).
- **Mechanisms asserted, not measured.** Paper 3 explains results by "weight-space geometry" ("Modular Encoding (MPT, Llama3)", p. 23) without measuring geometry; paper 2 explains position effects by attention behavior (p. 9) without a test.
- **Off-theme experiments at an agentic workshop.** Papers 1, 3 and 6 contain no agent (no tools, no multi-step actions) and were accepted anyway.
- **Narrowed evaluation.** Paper 2 uses only the easiest AgentHarm subset (p. 7) and four API models through different providers (p. 9); paper 6 uses "one round of sampling" (p. 50) and 512 test examples (p. 49).
- **Baselines moved out of sight.** Paper 5 reports GuardAgent only in the appendix "due to space constraints" (pp. 33, 35); its PNA falls from 79.00 to 75.75 and is argued to be an upper bound on false positives rather than measured (p. 36).
- **No limitations section in the main text** (paper 6), or only in the appendix (paper 5, A.3, p. 42).

What none of the six does: report a correction of the authors' own earlier numbers, leave placeholders for results not yet in, or rest its headline on a result its own pipeline confounds.

## 4. The one sentence per paper that best sells its novelty

| Paper | Quote | Where |
|---|---|---|
| (1) Trust Paradox | "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." | Abstract, p. 1 |
| (2) When Refusals Fail | "Prior works have focused mainly on evaluation of LLMs on long-context prompts, leaving agentic setup relatively unexplored, both from capability and safety perspectives. Our work addresses this gap." | Abstract, p. 6 |
| (3) ShieldBench | "we introduce ShieldBench, the first benchmark explicitly designed to evaluate the persistence of LLM safety interventions." | Introduction, "Our Contribution", p. 18 |
| (4) Role Assignment | "In this work, we present the first systematic case study showing that demographic-based persona assignments can alter LLM agents' behavior and degrade performance across diverse domains." | Abstract, p. 26 |
| (5) IntentGuard | "In this study, we present IntentGuard, a novel runtime guardrail framework that is training-free and model-agnostic." | Abstract, p. 32 (sold in the introduction by "We argue that the next action of an agent should be evaluated based on its current goals.", p. 33) |
| (6) REFORM | "Our results show that RMs can serve as their own adversary to expose and fix blind spots, yielding robust alignment without manual attribute priors or large scale relabeling." | Abstract, p. 46 |

Pattern: each sentence names one new object (a paradox, a gap, a benchmark, a case study, a framework, a capability) in the first or second sentence of the abstract, with no hedging and no reference to prior versions of the authors' work.

## 5. How they write about limitations and negative results

| Paper | Placement | Length | Tone (quoted) |
|---|---|---|---|
| (1) Trust Paradox | Last section before Ethics, repeated in Ethics (p. 4) | 3 sentences | "Our study has several limitations. We used programmatic proxies for human trust rather than direct human evaluation. Future work should include human studies to validate our findings" |
| (2) When Refusals Fail | One paragraph inside Discussion (p. 9), longer list in Appendix I (p. 16) | 5 sentences in main text | "Due to budget constraints, we evaluated a limited set of models." Negative results stated as findings about models: for GPT-5, "the initially low harm score prevent us from drawing strong conclusions" (p. 8) |
| (3) ShieldBench | Dedicated section after the conclusion, six bold-headed items (p. 24) | About 20 lines, the longest of the six | Scope language: "Model Scale", "Limited attack sophistication", "Computational constraints". Failures recast as insight: "These failures are important because they demonstrate that not all unsafe behaviors can be neutralized with blunt global edits" (p. 22) |
| (4) Role Assignment | "Limitations and Future Work" paragraph at the end (p. 29) | 3 sentences | Purely forward-looking: "broader coverage ... would further clarify how universally these effects appear" |
| (5) IntentGuard | Appendix A.3 only (p. 42) | 2 short paragraphs | "Although our experiments indicate the potential of IntentGuard ..., there are also several open questions for future study." The one bad domain is explained in one clause: "The only outlier is System Administration ... likely due to command-style tasks" (p. 36) |
| (6) REFORM | No limitations section; caveats inline | 1 clause each | "Due to cost constraints, we only considered one round of sampling" (p. 50); "There was a slight drop when it comes to the capitalization based perturbation." (Figure 5 caption, p. 51) |

Common pattern: limitations sit at the end or in the appendix, take one paragraph or less, are phrased as scope or future work, and never open a section. Negative results appear after the positive ones, in one sentence, followed by a reason or an implication. No paper lets a limitation change the headline claim.

## 6. Short papers (about 4 pages of main text) vs long ones

- **Short:** (1) Trust Paradox (pp. 1-4), (2) When Refusals Fail (pp. 6-9, plus a 7-page appendix), (4) Role Assignment (pp. 26-29).
- **Long:** (3) ShieldBench (about 6.5 pages, no appendix), (5) IntentGuard (about 6.5 pages plus appendix), (6) REFORM (about 7 pages plus a 27-page appendix).

| Aspect | Short papers (1, 2, 4) | Long papers (3, 5, 6) |
|---|---|---|
| Type | Finding papers: one phenomenon, no new method | Method (5, 6) or benchmark (3) papers |
| Design | One manipulated variable (alignment intensity; context length, type and position; persona) across 3-4 models | Grids of methods x models x datasets, baselines, ablations (paper 5 has four ablation tables, pp. 37-38) |
| Headline | A single number or a bullet list of findings in the abstract (26.2%; ">50% performance drops"; trust peak at 0.0) | A comparison with baselines (ASR 71.45 to 6.15; "35%-45%") |
| Evidence volume | 1 main figure or table plus 2-3 supporting ones | 6-15 figures and tables |
| Related work | Short (1, 2) or folded into the introduction (4 has no related-work section) | Full section with positioning |
| Statistics | Thin, but paper 2 shows 1 sigma bars over at least 3 seeds | Equally thin; no confidence intervals anywhere |
| Limitations | 1 paragraph | From none (6) to a full section (3) |

How the bar differs: a short paper is accepted for one clean, surprising, on-theme finding measured on a controlled axis across several models, written with confidence; reviewers do not ask for baselines, ablations or a method. A long paper is held to "does the method beat baselines, and do ablations explain why". Rigor is not what separates accepted from rejected at this venue: the weakest accepted short paper (1) has essentially no valid statistics. What all short ones have is completeness (no missing results), an unhedged headline, and a topic the call names. A 4-page paper that is statistically stronger than these but incomplete, hedged, or off-theme can still fall below this bar.
