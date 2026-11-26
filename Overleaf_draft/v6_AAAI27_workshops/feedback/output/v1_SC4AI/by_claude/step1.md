# 🟠 Claude · Step 1 · Calibration sheet

> **Judge:** Claude (fresh chat) · **Input:** [combined PDF of 6 accepted papers](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf) · **Prompt:** [prompt.md](../../../input/prompt.md), STEP 1
>
> **Workshop:** AAAI-26 "How Can We Trust and Control Agentic AI?" · Page numbers = pages of the combined 82-page PDF (papers run 1–5, 6–17, 18–25, 26–31, 32–45, 46–82). Every paper carries the copyright line "Trustworthy Agentic AI Workshop@AAAI".

> [!NOTE]
> The judge's text below is kept in full; only the layout changed. Claude Code's verification notes are in the last section, [🔎 Fact-check](#-fact-check-by-claude-code-not-the-judge).

**Legend:** 🎯 claim · 📊 evidence · ✅ likely acceptance reason · 🐛 internal error the reviewers missed · ⚠️ tolerated weakness

## 📌 TL;DR

| What | Claude's answer |
|---|---|
| 🏁 Acceptance floor | About **paper 1** (Trust Paradox): one on-theme claim, one quantitative experiment, 3+ figures, a limitations paragraph. |
| 📍 Typical accepted paper | Closer to **papers 2 and 4**: a clean controlled study on a known benchmark with a headline number. |
| 📈 Statistics | **Effectively not required.** Only paper 2 has error bars. |
| ✍️ Tone | Confident and implication-heavy; hedging is rare in the main text. |
| ⚠️ Limitations | Short (median about one paragraph), at the end or in the appendix, written as scope or budget, not as threats to validity. |
| 🐛 Errors tolerated | Several accepted papers contain internal contradictions reviewers missed (see section 3). |

## 1️⃣ Per-paper summary

### 📄 (1) The Trust Paradox · pp. 1–5 · one independent author

| | |
|---|---|
| 🎯 **Claim** | Making a model "more aligned" through stronger safety and deference prompting lowers trust; trust peaks at minimal alignment (α = 0.0). |
| 📊 **Evidence** | 120 dialogues (4 Llama models × 5 scenarios × 6 α levels), i.e. one dialogue per cell. Trust is a hand-weighted composite proxy, Eq. 1 (p. 2). Fig. 1 trust curve (p. 2); Figs. 2–4 heatmaps and components (p. 3); stats $F(5,100)=12.34$, $r = 0.771 / -0.450$ (p. 4). No tables. Headline effect: trust **0.748 vs 0.743** (p. 2). |
| ✅ **Why it got in** | A provocative, on-theme, counterintuitive claim with a catchy name; the workshop appears to accept position-style evidence. |

### 📄 (2) When Refusals Fail · pp. 6–17

| | |
|---|---|
| 🎯 **Claim** | Long context makes agent capability and refusal unstable: models advertised with 1–2M-token windows lose more than 50% performance by about 100K tokens, and refusal rates move in opposite directions across models. |
| 📊 **Evidence** | AgentHarm with 1K–200K padding: 4 padding types × 2 positions × 4 models. Fig. 2 length and refusal (p. 8), Fig. 3 padding type (p. 8), Fig. 4 position (p. 9); 1σ error bars over ≥ 3 seeds (p. 11); per-category and delayed-refusal appendix (Figs. 8–11, pp. 12–17). |
| ✅ **Why it got in** | Timely, clean controlled design on an established benchmark; an easy headline ("degrades at 100K despite a 2M window"); the only paper with error bars; extensive appendix. |

### 📄 (3) ShieldBench · pp. 18–25

| | |
|---|---|
| 🎯 **Claim** | Whether a safety edit survives adversarial fine-tuning depends on method × model × dataset; no single intervention dominates. |
| 📊 **Evidence** | 6 weight-editing methods × 5 open 7–8B models × 3 datasets (HarmBench, HEx-PHI, WMDP). Persistence heatmaps absolute and row-normalised (Figs. 1–6, pp. 20–21); stress gradients (Figs. 7–11, p. 22); before/after harm tables (Tables 2–4, p. 23). |
| ✅ **Why it got in** | Broad systematic coverage, a "persistence" angle new to this audience, many figures. |

### 📄 (4) From Biased Chatbots to Biased Agents · pp. 26–31

| | |
|---|---|
| 🎯 **Claim** | Task-irrelevant personas (gender, race/origin, religion, profession) change agent performance by up to 26.2 points. |
| 📊 **Evidence** | 23 personas × 3 models × 5 benchmarks (ALFWorld, WebShop, three AgentBench tasks). Big Table 2 (p. 28) race/origin; Fig. 2 gender (p. 28); Figs. 3–4 profession and religion (p. 29). |
| ✅ **Why it got in** | A socially salient, easy-to-grasp result moving a known chatbot phenomenon into agents; simple, reproducible setup with a headline number. |

### 📄 (5) IntentGuard · pp. 32–45

| | |
|---|---|
| 🎯 **Claim** | A training-free guardrail checking each plan and tool call against the user's original intent (Plan Gate + Tool Gate) blocks prompt injection better than rule-based defences. |
| 📊 **Evidence** | ASB benchmark, 5 attack types, 5 prompt-level baselines plus Llama Guard 3. Table 1 (p. 37): ASR **71.45 → 6.15**, RER **9.95 → 55.98**. Per-domain Table 2 (p. 37); ablations on LLM choice, gates, filters, rewrite limit (Tables 3–6, pp. 37–38); case studies Fig. 3 (p. 38) and Figs. 4–7 (appendix); full per-attack Table 7 (p. 44). |
| ✅ **Why it got in** | A complete method paper (baselines, ablations, cost columns, case studies, anonymous code link) with a very large headline improvement. |

### 📄 (6) REFORM · pp. 46–82

| | |
|---|---|
| 🎯 **Claim** | A reward model can generate its own failure cases by reward-guided controlled decoding; retraining on those failures for the top 5% of pairs improves robustness without hurting downstream alignment. |
| 📊 **Evidence** | Anthropic HH and PKU BeaverTails; Mistral-7B and Qwen-2.5-14B RMs. Fig. 4 failure discovery vs baselines (p. 51); Fig. 5 win-rate drop under 4 perturbations (p. 51); Table 1 clean accuracy (p. 52); Figs. 6–8 BoN, PPO, DPO (pp. 50–52); 27-page appendix with examples and code. |
| ✅ **Why it got in** | Most technically mature of the six, near main-conference grade: formal method, two datasets, two models, three downstream alignment regimes. |

## 2️⃣ The common bar

| Dimension | What all six have | Range observed (= the floor) |
|---|---|---|
| 🧭 Framing | Title and abstract framed in trust, safety or agentic terms, plus a "why this matters for deployment" paragraph | Topical fit is loose: papers 1, 3 and 6 contain no agents at all. |
| 💡 Novelty statement | An explicit gap sentence in the abstract, repeated in the intro ("first", "novel", "overlooked", "counterintuitive") | Incremental is fine: moving a known effect into agents (2, 4) or combining existing methods and datasets into a benchmark (3) counts. |
| 📊 Evidence level | At least one quantitative experiment on public models or benchmarks | From 120 synthetic dialogues scored by a proxy (1) to 2 datasets × 2 RMs × 3 alignment regimes (6). Only method papers (5, 6) have baselines; finding papers have none. |
| 📈 Statistics | Effectively not required | Error bars only in paper 2 (1σ, ≥ 3 seeds). Paper 5 repeats one ablation 5 times (p. 36). Paper 1's p-values don't fit its effect sizes. Papers 3, 4, 6 report no variance. |
| 📏 Length | AAAI two-column template | Main text about 3.5 pages (1, 4) to about 7 pages (5, 6). Appendices unrestricted: 7 pp. (2), 6 pp. (5), 27 pp. (6). |
| 🖼️ Figures | Every paper has at least 3 | Four of six put a schematic or teaser on p. 1–2 (2: Fig. 1; 4: Fig. 1; 5: Figs. 1–2; 6: Figs. 1–3). The rest are heatmaps, log-x line plots, bar charts. |
| ✍️ Writing tone | Confident and implication-heavy ("reveals", "critical vulnerability", "concerning"); results interpreted mechanistically without mechanistic evidence | Hedging is rare in the main text. |
| 📦 Reproducibility signal | Usually a promise rather than an artifact | Anonymous link (5); "will release" (2, p. 16); toolkit or seed claims with no link (3, p. 24; 6, p. 47). |

## 3️⃣ What they got away with (weaknesses that did not block acceptance)

### ⚠️ Tiny or untested effects with strong claims

- **Paper 1:** the whole "paradox" is trust 0.748 vs 0.743 (p. 2). $r = -0.143$ is called "statistically significant" without a p-value (p. 3). n = 1 per cell. "Human trust" is never measured with humans.
- **Paper 4:** a single deterministic run. On ALFWorld scores move in 2-point steps (one task = 2 pts), yet ±2–6 pt shifts are read as stereotypes (pp. 28–29).

### ⚠️ Missing controls

- **Paper 4:** the baseline drops the persona prefix entirely (p. 27) and there is no neutral-persona control, so "persona effect" and "prefix effect" are confounded.
- **Paper 5:** no adaptive attacker targeting the gates themselves.

### ⚠️ Undefined core metrics

- **Paper 3** never defines "persistence", the harmfulness judge, or the three adversarial-fine-tuning intensities (pp. 20, 24), despite its intro criticising benchmarks that depend on AI judges (p. 18).

### ⚠️ Mechanistic stories with no mechanistic measurement

- **Paper 3:** "weight-space geometry" (modular vs entangled, p. 23) inferred only from scores.
- **Paper 4:** noise-level shifts attributed to "latent human-like stereotype biases" (p. 28).

### 🐛 Internal contradictions the reviewers missed

| Paper | Contradiction |
|---|---|
| 2 | Abstract: Grok refusal goes from about 80% to about 10% (p. 6). Body: it falls to about 40%, "half as high" (pp. 8–9). GPT-5 accessed via OpenRouter (p. 9, Table 2 p. 14) but via the OpenAI API in Appendix I (p. 16). |
| 5 | Table 3 labelled "Naive Attack" (p. 36) but its 4o/4o numbers match the Combined Attack row of Table 7 (p. 44). Text calls 4o + 4o-mini "the best pair" (p. 37), but Table 3 shows 4o/4o is better. GuardAgent results promised for the appendix (pp. 33, 35) never appear. "Ten domains" listed as nine (pp. 35–36), and Table 2 uses different domains. "DPD" expanded as Direct Paraphrase in the caption but Dynamic Prompt Rewriting in the text. |
| 1 | Text says authenticity rises with alignment (p. 3), contradicting its own trust story. Lists "Llama-3.3-8B", but Meta released Llama 3.3 only at 70B. Conclusion comes before the Discussion (p. 4). |
| 3 | Mistral called "entangled" (p. 23) yet gets 0.94 with TaLoS on WMDP. Conclusion credits Task Vectors (p. 24) though they were among the weakest methods. |
| 6 | Broken cross-references ("Appendix .", "Section .", "Table/Figure 1"). Cites "Figure 10" meaning Fig. 6 (p. 50). Leftover names "REFROM" and "FMRM". The abstract's "35%–45% average improvement" (p. 46) can't be traced to any number in the main text. |

### ⚠️ A strong baseline left undiscussed

- **Paper 5:** Llama Guard 3 reaches ASR 8.57 vs IntentGuard's 6.15 (Table 1, p. 37), yet the text says baselines give only "modest improvements". The 3× LLM-call overhead (3.4 → 10.5 requests) is reported but never argued for.

### ⚠️ Narrow scope

- Easiest AgentHarm subset only (paper 2).
- One benchmark despite "key benchmarks" in the abstract (paper 5).
- 7–8B models only (paper 3).
- One sampling round "due to cost" (paper 6, p. 50).
- "First" claims accepted without a literature check (papers 3, 4). Paper 1's related work cites MMLU as an alignment benchmark (p. 1).

## 4️⃣ How each paper sells its contribution

| Paper | Quote | Where | Style |
|---|---|---|---|
| Trust Paradox | "We present evidence for a Trust Paradox in AI alignment: increasing alignment intensity beyond optimal levels actually reduces human trust in AI systems." | abstract, p. 1 | Named phenomenon; no contribution list |
| When Refusals Fail | "Prior works have focused mainly on evaluation of LLMs on long-context prompts, leaving agentic setup relatively unexplored, both from capability and safety perspectives." | abstract, p. 6 | Gap sentence, then four bulleted "key findings" in the intro (p. 6) |
| ShieldBench | "we introduce ShieldBench, the first benchmark explicitly designed to evaluate the persistence of LLM safety interventions." | intro, p. 18 | Three research questions plus "Our contributions are threefold" (pp. 18–19) |
| Biased Agents | "In this case study, we provide the first systematic investigation demonstrating that demographic-based persona assignments can measurably undermine LLM agents' task execution." | intro, p. 26 | "First" claim plus a headline number (26.2%); no list |
| IntentGuard | "The core intuition behind our method is: a hazardous agent action, either caused by adversarial attacks from the external world or hallucination in LLMs' own reasoning steps, often serves an alternative purpose that deviates from the original task objectives." | intro, p. 33 | Intuition statement plus a worked example (Fig. 1); no list |
| REFORM | "Use the RM itself as a search signal to generate responses that contradict its own scoring while preserving the underlying preference class." | intro, p. 46 | Problem / Gap / Key idea / Method headings, then Claims C1–C3 plus Contributions C1–C6 (pp. 46–47), overlapping |

**Pattern:** the novelty sentence is always in the abstract, and four of six repeat or sharpen it on the first intro page. Finding papers lead with "first" or a named effect plus a number; method papers lead with the core idea in one sentence.

## 5️⃣ How they write about limitations and negative results

| Paper | Placement | Length | Tone and handling |
|---|---|---|---|
| 1 | "Limitations and Future Work" (p. 4), repeated in the Ethical Statement | 4 lines | Names one limitation (proxies, not humans) and turns it into future work; silent on effect size and n. |
| 2 | Inside the Discussion (p. 9) plus Appendix I (p. 16) | About 6 lines main, about 20 appendix | The most candid: blames budget, names the easiest-subset bias, provider filters, tokenizer drift; says to treat cross-model comparisons "with caution". States its negative result plainly: GPT-5's high refusal "prevent[s] us from drawing strong conclusions" (p. 8). |
| 3 | Dedicated "Limitations" section (p. 24) | 6 bolded items, about 25 lines | Presented as scope (scale, attacks, datasets, compute, open-source only); compute explains variance; failures recast as insight ("These failures are important because…", p. 22). |
| 4 | "Limitations and Future Work" (p. 29) | 1 short paragraph | Coverage only, then a 3-item future-work list; gains (↑) read as more evidence of "volatility" rather than noise. |
| 5 | Nothing in the main text; Appendix A.3 (p. 42) | About 10 lines | Framed as "open questions" (LLM dependence, fast-moving field). The System Admin outlier gets one "likely due to…" clause (p. 36); the PNA drop is argued away as an upper bound on false positives (p. 36). |
| 6 | No section; scattered caveats plus an appendix FAQ (p. 56) | One clause per caveat | Weaknesses as "slight" caveats in captions (capitalisation drop, Fig. 5, p. 51; semantic diversity, Fig. 7, p. 52) and as Q&A ("Why doesn't our method have a complete coverage…", p. 56); scope hedged in Related Work ("Rather than claiming it to be a universal solution", p. 48). |

**Pattern:**

- Limitations are short (median about one paragraph), at the end or in the appendix, written as scope or budget constraints rather than threats to validity.
- No paper discusses statistical power or the risk that its headline effect is noise.
- Negative results stay in the main text only when they can be framed as an insight; otherwise they go into a caption hedge or the appendix.

> **For judging the next paper:** the acceptance floor is about paper 1 (one on-theme claim, one quantitative experiment, 3+ figures, a limitations paragraph). The typical accepted paper is closer to papers 2 and 4: a clean controlled study on a known benchmark with a headline number.

## 🔎 Fact-check (by Claude Code, not the judge)

Checked 2026-11-26 against the text of the [combined PDF](../../../input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf).

| # | Judge claim | Found in the PDF? | Verdict |
|---|---|---|---|
| 1 | Copyright line on every paper | "Copyright © 2026, Trustworthy Agentic AI Workshop@ Association for the Advancement of Artificial Intelligence" | ✅ (wording shortened by the judge) |
| 2 | Paper 1: 0.748 vs 0.743; $r = 0.771$, $-0.450$, $-0.143$; "Llama-3.3-8B" | All present | ✅ |
| 3 | Paper 2 contradiction: abstract "∼80% to ∼10%" vs body "half as high at 200K"; OpenRouter | Abstract: "Grok 4 Fast decreases from ∼80% to ∼10% at 200K tokens"; body: "80% gradually decreases ... becoming half as high at 200K tokens" | ✅ the contradiction is real |
| 4 | Paper 5: ASR 71.45 → 6.15, RER 9.95 → 55.98, Llama Guard 3 ASR 8.57, "modest improvement" | All present | ✅ |
| 5 | Paper 6: "REFROM", "FMRM", "Figure 10" leftovers | All present | ✅ |
| 6 | Novelty quotes for papers 3, 4, 5 and REFORM's "Rather than claiming it to be a universal solution" | All present verbatim | ✅ |
| 7 | Other details (ALFWorld 2-point steps, Table 3 vs Table 7 match in paper 5, Mistral 0.94 TaLoS, appendix page counts) | Not checked line by line | ⚪ unverified |
