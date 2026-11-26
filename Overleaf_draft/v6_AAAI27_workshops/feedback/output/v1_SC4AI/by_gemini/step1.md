# 🔷 Gemini · Step 1 · Calibration sheet

> **Judge:** Gemini (fresh chat) · **Input:** [combined PDF of 6 accepted papers](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 1
>
> **Workshop:** AAAI-26 "How Can We Trust and Control Agentic AI?"

> [!WARNING]
> **Gemini's page numbers for papers 2–6 run one page high.** The real ranges are 1–5, 6–17, 18–25, 26–31, 32–45, 46–82; Gemini uses 6–18, 19–26, 27–32, 33–46, 47–82. Subtract 1 from its page cites for papers 3–6. See [🔎 Fact-check](#-fact-check-by-claude-code-not-the-judge).

> [!NOTE]
> The judge's text below is kept in full; only the layout changed (page numbers left as Gemini wrote them).

**Legend:** 🎯 claim · 📊 evidence · ✅ likely acceptance reason · ⚠️ tolerated weakness

## 📌 TL;DR

| What | Gemini's answer |
|---|---|
| 🧭 Framing bar | Every paper ties a safety/alignment phenomenon to **operational deployment or agentic execution**, not pure theory or single-turn chat. |
| 💡 Novelty bar | A "first systematic study/benchmark" of an underexplored failure axis, or a "training-free / prior-free plug-in" fixing a concrete bottleneck. |
| 📊 Evidence bar | Minimum 3–5 models × 3–5 tasks; higher bar adds full suites and ablations. |
| 📈 Statistics | **Surprisingly light:** only paper 1 tests hypotheses, only paper 2 has error bars. |
| 📏 Length | Main text 4 to 7 pages; 4 to 11 figures; pipeline diagram on p. 1–2. |
| ⚠️ Limitations | Usually one short paragraph at the end; matter-of-fact, reframed as insight. |

## 1️⃣ Paper-by-paper breakdown

### 📄 (1) The Trust Paradox: When Over-Alignment Reduces Human Trust in Agentic AI · pp. 1–5

| | |
|---|---|
| 🎯 **Core claim** | Increasing alignment intensity ($\lambda > 0.6$) non-monotonically reduces human trust, because excessive obedience/hedging ($r = -0.450$) undermines perceived authenticity ($r = 0.771$). |
| 📊 **Main evidence** | 120 five-turn dialogues across 4 Llama models, 5 scenarios, 6 alignment levels ($\lambda \in [0.0, 1.0]$). Fig. 1 (p. 2): non-monotonic trust curve peaking at $\lambda = 0.0$ with 0.748 and dipping at $\lambda = 0.6$ to 0.743. Fig. 2 (p. 3) heatmaps/bars across models; Fig. 3 (p. 3) scenario sensitivity; Fig. 4 (p. 3) component trade-offs; mixed-effects model $F(5,100)=12.34,\ p<0.001$ (p. 4). |
| ✅ **Why accepted** | A punchy, counterintuitive framing ("Trust Paradox") aimed at the workshop's core tension (safety vs trustworthy agency), with clean visuals and formal statistical testing despite a lightweight setup. |

### 📄 (2) When Refusals Fail: Unstable Safety Mechanisms in Long-Context LLM Agents · pp. 6–18

| | |
|---|---|
| 🎯 **Core claim** | Long-context agents (even with advertised 1M–2M windows) lose over 50% capability around 100K tokens and show erratic, model-dependent refusal shifts, including dangerous "delayed refusals" after executing initial tool calls. |
| 📊 **Main evidence** | AgentHarm extensions across 4 frontier models (GPT-4.1-nano, GPT-5, DeepSeek-V3.1, Grok 4 Fast), 4 padding types, 2 positions up to 200K–800K tokens (Table 1, p. 8). Fig. 1 (p. 7) pipeline; Fig. 2 (p. 8) score and refusal curves (Grok 4 Fast refusals ~80% → ~10%, GPT-4.1-nano ~5% → ~40%); Figs. 3–4 (pp. 8–9) padding type and position; Figs. 5–11 (pp. 12–13, 17) subset, per-category, immediate vs delayed refusals. |
| ✅ **Why accepted** | High relevance to real agentic deployments (frontier models on multi-step tool use, not static QA) plus the discovery of delayed refusals (partial harm before refusing, p. 10 and Fig. 11, p. 17). |

### 📄 (3) ShieldBench · pp. 19–26 (Gemini's numbering)

| | |
|---|---|
| 🎯 **Core claim** | Safety interventions (weight-space edits) are not universally durable; survival under benign or adversarial fine-tuning depends on the geometric alignment between intervention type, architecture, and risk domain. |
| 📊 **Main evidence** | 6 weight-space editing methods (Table 1, p. 20) × 5 open 7B–8B models × 3 datasets (HarmBench, HEX-Phi, WMDP): absolute and row-normalized persistence heatmaps (Figs. 1–6, pp. 21–22), adversarial stress gradients (Figs. 7–11, p. 23), before/after harmfulness tables (Tables 2–4, p. 24). |
| ✅ **Why accepted** | Systematic unification of six contemporary editing/unlearning methods under one reproducible stress-testing pipeline, with a clear takeaway: high HarmBench scores mask fragility on multi-step procedural knowledge in WMDP. |

### 📄 (4) From Biased Chatbots to Biased Agents · pp. 27–32 (Gemini's numbering)

| | |
|---|---|
| 🎯 **Core claim** | Task-irrelevant demographic personas (gender, race/origin, religion, profession) introduce implicit stereotype biases that destabilize multi-step agent execution, causing up to 26.2% degradation. |
| 📊 **Main evidence** | 3 models (GPT-4o-mini, DeepSeek-V3, Qwen3-235B) × 23 personas (Table 1, p. 28) × 5 agentic benchmarks (ALFWorld, WebShop, Card Game, OS Interaction, Database). Table 2 (p. 29) full race/origin shifts (e.g. DeepSeek-V3 Card Game −26.2% under "from Africa"); Fig. 1 (p. 27) overview; Figs. 2–4 (pp. 29–30) gender, profession, religion. |
| ✅ **Why accepted** | Bridges a known NLP fairness issue (persona bias) into an underexplored agentic risk (operational reliability in tool use and planning) on 5 established benchmarks. |

### 📄 (5) IntentGuard · pp. 33–46 (Gemini's numbering)

| | |
|---|---|
| 🎯 **Core claim** | A training-free, model-agnostic runtime guardrail tracking continuous intent alignment at two dual-filter checkpoints (Plan Gate, Tool Gate) with automated plan rewriting beats static rule-based guardrails in both safety and utility. |
| 📊 **Main evidence** | Agent Security Bench, 5 prompt-injection attack types, 9–10 domains. Table 1 (p. 38): ASR 71.45% → 6.15%, Robust Execution Rate 9.95% → 55.98%; Table 2 (p. 38) cross-domain; Tables 3–6 (pp. 38–39) ablations on backbone LLMs, Plan vs Tool gates, filters, rewrite limit $R$; Table 7 (p. 45) per-attack; Figs. 1–7 architecture and traces. |
| ✅ **Why accepted** | A concrete defense (not just an audit) with thorough ablations, an anonymous code repository (p. 33), and simultaneous gains on safety (ASR/FNR) and utility (TSR/RER). |

### 📄 (6) Teach a Reward Model to Correct Itself (REFORM) · pp. 47–82 (Gemini's numbering)

| | |
|---|---|
| 🎯 **Core claim** | A reward model can be its own adversary via reward-guided constrained decoding, finding class-consistent, reward-inconsistent failures without attribute priors; retraining on the top 5% most influential augmented pairs improves OOD robustness by 35%–45% without hurting downstream alignment. |
| 📊 **Main evidence** | Anthropic HH and PKU BeaverTails, Mistral-7B and Qwen-2.5-14B: Fig. 4 (p. 52) failure-discovery radar vs baselines; Fig. 5 (p. 52) win-rate drop reductions across 4 perturbations; Table 1 (p. 53) unperturbed accuracy; Figs. 6–8 (pp. 51, 53) downstream BoN, PPO, DPO; Appendix Table 2 (p. 58) retraining vs fine-tuning; Figs. 9–15 (pp. 60–63). |
| ✅ **Why accepted** | Technical depth (constrained-decoding objective, influence-function data selection, end-to-end checks across BoN/PPO/DPO) plus comprehensive appendices (pp. 57–82). |

## 2️⃣ The common bar for acceptance

| Dimension | Gemini's finding |
|---|---|
| 🧭 Framing | Every paper connects a safety/alignment phenomenon to operational deployment or agentic execution (multi-step planning, tool use, downstream policy steering), not pure theory or static single-turn chat (paper 1 p. 1; paper 2 p. 6; paper 4 p. 27; paper 5 p. 33). |
| 💡 Novelty statement | Either a "first systematic study/benchmark" of an underexplored failure axis (papers 1–4) or a "training-free / prior-free plug-in framework" solving a concrete bottleneck (papers 5, 6). |
| 📊 Evidence (minimum) | 3–5 models across 3–5 tasks/benchmarks (paper 1: 4 models, 5 scenarios, 120 dialogues, p. 2; paper 2: 4 models, 176 tasks × padding grid, p. 7; paper 4: 3 models, 23 personas, 5 benchmarks, p. 28). |
| 📊 Evidence (higher) | Full suite plus ablations across components, hyperparameters, downstream algorithms (paper 3: 6 methods × 5 models × 3 datasets, p. 20; paper 5: 6 baselines + 4 ablation tables, pp. 38–39; paper 6: 2 models × 2 datasets × 3 RLHF pipelines, pp. 50–53). |
| 📈 Statistics | **Surprisingly light.** Only paper 1 runs formal tests (mixed-effects ANOVA F-test, Pearson r with p-values, p. 4); only paper 2 plots 1σ error bars over ≥ 3 seeds (pp. 8–9, 11). Papers 3–6 report point estimates, percentages, or row-normalized z-scores without CIs or tests. |
| 📏 Length | Main text 4 to 7 pages excluding references (paper 1: 4 pp.; paper 2: 4 pp. + 7 pp. appendix; paper 3: 6 pp.; paper 4: 4 pp.; paper 5: 7 pp. + 6 pp. appendix; paper 6: 7 pp. + 26 pp. appendix). |
| 🖼️ Figures | 4 to 11 figures in the main body: conceptual pipeline diagrams on p. 1–2 (paper 2 Fig. 1; paper 4 Fig. 1; paper 5 Figs. 1–2; paper 6 Figs. 1–3) plus multi-panel heatmaps, radar charts, or line plots. |
| ✍️ Writing tone | Direct, empirical, problem-solution ("Problem / Gap / Key idea / Claims" in paper 6; numbered takeaway bullets in papers 2 and 3). Claims framed around practical deployment risk rather than heavy formal proofs. |

## 3️⃣ What these papers get away with

| Weakness | Examples |
|---|---|
| ⚠️ **Synthetic / proxy measurements instead of human or real-world evaluation** | Paper 1 measures "human trust" with a hand-weighted formula of programmatic heuristics, $T = 0.3(1-O) + 0.3A + 0.2C + 0.2R$ (p. 2), with zero human subjects. Paper 2 uses random fiction/Wikipedia/token padding rather than realistic tool logs, and only the easiest AgentHarm subset ("hint and detailed prompt", pp. 7, 17). |
| ⚠️ **Tiny effects presented as major paradoxes** | Paper 1's "Trust Paradox" spans 0.005 on a [0, 1] scale (0.748 at $\lambda = 0.0$ to 0.743 at $\lambda = 0.6$, p. 2), with model means differing by 0.004 (0.748 vs 0.744, p. 3), accepted because the directional correlation is significant. |
| ⚠️ **No proposed mitigation (purely diagnostic)** | Papers 1, 2, 4 test no defense; documenting a clear, novel agent failure mode is enough (pp. 4, 10, 30). |
| ⚠️ **Provider / judge confounds and single-run variance** | Paper 2 mixes API providers (OpenAI vs OpenRouter, Table 2, p. 15), so platform moderation can't be separated from weights, and swaps GPT-4o for GPT-4.1-nano as judge for 3 of 4 models (Table 3, p. 15). Papers 3, 4, 6 omit error bars and seeds (pp. 21–24, 29, 52–53). |
| ⚠️ **Baseline omissions and inference overhead** | Paper 5 relegates GuardAgent to the appendix (absent from Table 1, pp. 34, 36, 38) and needs 3.1× more LLM requests (10.50 vs 3.40, Table 1, p. 38). Paper 6 must retrain the RM from scratch because fine-tuning fails (PKU utility 68.75% → 51.51%–52.32%, Appendix Table 2, p. 58). |
| ⚠️ **Rough polish and typos** | Missing Greek symbol rendering as "(=0.0)" in paper 1 (pp. 1–4); "Random perturbationtion" and "REFROM" in paper 6 figures (pp. 51–53, 60); "alnoe" in paper 5 (p. 39); duplicated references in paper 4 (Wang et al. 2025a/b, p. 31). |

## 4️⃣ Best novelty-selling sentence per paper

| Paper | Quote | Where |
|---|---|---|
| The Trust Paradox | "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." | Abstract, p. 1 |
| When Refusals Fail | "Prior works have focused mainly on evaluation of LLMs on long-context prompts, leaving agentic setup relatively unexplored, both from capability and safety perspectives. Our work addresses this gap." (or, as a single finding: "Agentic capabilities of models with 1M-2M token context windows degrade severely already at 100K tokens, with >50% performance drops both for benign and harmful tasks.") | Abstract / Intro, p. 6 |
| ShieldBench | "To address these limitations, we introduce ShieldBench, the first benchmark explicitly designed to evaluate the persistence of LLM safety interventions." | Intro, p. 19 |
| Role Assignment Effects | "In this work, we present the first systematic case study showing that demographic-based persona assignments can alter LLM agents' behavior and degrade performance across diverse domains." | Abstract, p. 27 |
| IntentGuard | "In this study, we present IntentGuard, a novel runtime guardrail framework that is training-free and model-agnostic." | Abstract, p. 33 |
| REFORM | "We introduce a preference distribution agnostic procedure that uses the reward model itself to guide controlled decoding toward mis specified responses while preserving the underlying preference class." | Abstract, p. 47 |

## 5️⃣ How accepted papers handle limitations and negative results

### Placement and length

| Pattern | Papers |
|---|---|
| **Standard (4 of 6):** a dedicated "Limitations and Future Work" subsection at the end of the main text, one short paragraph (~4–10 sentences) | Paper 1 (p. 4, 4 sentences); paper 2 (p. 10, 5 sentences, 2 paragraphs in Appendix I, p. 17); paper 3 (p. 25, 6 bullets, ~18 sentences); paper 4 (p. 30, 1 paragraph, 3 sentences) |
| **Appendix-only / inline (2 of 6)** | Paper 5: Limitations entirely in Appendix A.3 (pp. 43–44, 2 paragraphs), System Admin outlier noted inline (p. 37). Paper 6: no section; caveats inline (sampling cost, p. 51; capitalization in Fig. 5 caption, p. 52; diversity in Fig. 7 caption, p. 53) and in appendix QA (pp. 57–58). |

### Tone and framing of negative results

- **Matter-of-fact, non-defensive, constructive:** constraints stated plainly ("Due to budget/computational constraints…", paper 2 p. 10, paper 3 p. 25, paper 6 p. 51), then an immediate pivot to future work or scope.
- **Negative or mixed results reframed as insights:**

| Paper | How |
|---|---|
| 2 | Turns GPT-5's flat low harm score into a methodological note (benign tasks not run past 10K tokens, p. 8); highlights delayed refusals as a safety insight (p. 10). |
| 3 | Foregrounds intervention collapses (Llama-3.1-8B + Diverse Inversion falling to 0.18 on WMDP, p. 22) as proof that weight-space geometry governs durability. |
| 5 | Flags System Administration as "the only outlier" where TSR/RER trail the baseline, with a concrete hypothesis ("command-style tasks that complicate intent extraction", p. 37). |
| 6 | Reports where REFORM slightly underperforms (capitalization, Fig. 5, p. 52; naive/regularized fine-tuning failing vs full retraining, Appendix Table 2, p. 58). |

## 🔎 Fact-check (by Claude Code, not the judge)

Checked 2026-11-26 against the text of the [combined PDF](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf).

| # | Judge claim | Found in the PDF? | Verdict |
|---|---|---|---|
| 1 | Page ranges 6–18, 19–26, 27–32, 33–46, 47–82 | Titles are on pp. 6, **18**, **26**, **32**, **46** (pp. 19, 27, 33, 47 are mid-paper) | ❌ off by one for papers 3–6 (and paper 2's end) |
| 2 | 800K tokens, 176 tasks, GPT-4o-mini, Qwen3-235B, "from Africa" | All present | ✅ |
| 3 | Paper 1 Greek symbol missing, shows as "(=0.0)"; 0.744 model mean | Both present in the text layer | ✅ |
| 4 | GuardAgent in appendix only; typo "alnoe"; "perturbationtion"; 68.75% → 51.51%–52.32%; Wang et al. 2025a/2025b | All present | ✅ |
| 5 | Novelty quotes for papers 2 ("Our work addresses this gap"), 5 ("training-free and model-agnostic"), 6 ("preference distribution agnostic procedure") | Present verbatim | ✅ |
| 6 | Paper 1 trust formula $T = 0.3(1-O) + 0.3A + 0.2C + 0.2R$ | Not found as that string in the text layer (may be typeset math) | ⚪ unverified |
| 7 | Figure and table counts per paper, appendix page counts | Not checked line by line | ⚪ unverified |
