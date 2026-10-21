# 📮 SC4AI'27 OpenReview submission sheet (SwiPO)

> Venue: Social Choice for AI Ethics and Safety 2027, AAAI-27 workshop, Montréal, Feb 22-23, 2027 (non-archival). Submit at <https://openreview.net/group?id=AAAI.org/2027/Workshop/SC4AI>. **Deadline: Nov 20, 2026 (AoE)**; notification Dec 2, 2026.

## 🧾 Fields to paste

| Field | Value |
|---|---|
| **Title** | SwiPO on ECLIPTICA-30k: Can You Trust One LLM Checkpoint to Switch Its Alignment for Every Agent Role? |
| **Authors (order)** | Kapil Wanaskar, Gaytri Jena, Vinija Jain, Aman Chadha, Amitava Das (each needs an OpenReview profile) |
| **Paper type** | Full paper (6-8 pages excluding references and appendices) |
| **Anonymized?** | No (the call lets authors choose; the paper and its arXiv version are public) |
| **PDF** | `Overleaf_draft/v6_AAAI27_SC4AI/0_main.pdf` |
| **Keywords** | pluralistic alignment; steerable alignment; social choice; preference optimization; instruction-conditioned alignment; LLM agents; benchmark |
| **TL;DR** | Conditioning preference optimization on a natural-language contract removes aggregation across roles inside training, but moves the social-choice problem to who sets the contract, which contracts are offered, and what no contract may lift. |

**Abstract (plain text):**

Preference optimization such as DPO pools comparisons from annotators who hold different roles, and prior work shows that when the role is not recorded, the learned policy ranks answers by an implicit Borda count over these hidden roles, a rule nobody chose. We study the steerable pluralistic alternative, in which a natural-language alignment instruction writes the role's behavioral contract into the input, so one model can fit each role's preference without aggregating them. Switching does not dissolve the social-choice problem. It moves it to the instruction channel: who may set the instruction (oversight), which contracts are offered (agenda setting and elicitation), which constraints no contract may lift (a collective choice over everyone affected), and who gains from misreporting (deployers rather than annotators). We ground these questions empirically. ECLIPTICA-30k crosses 300 prompts with 100 alignment-instruction types; every result here is on ECLIPTICA-3k, its evaluated 10-type, 3,000-case subset. SwiPO (Switchable Preference Optimization) conditions preference optimization on the instruction under a mandatory KL anchor; the run reported here trains a single safety contract and tests contracts it never saw. On Llama-3.1-8B the switch is real: every trained model's refusal rate moves by 0.30 to 0.49 between a strict and a permissive contract. The switch also reaches the requests a collective floor would most plausibly cover: on violence, physical harm, trafficking, and threats to public health or national security, the permissive contract cuts refusals at least as much as elsewhere. SwiPO reaches 86.7% instruction-alignment efficiency (95% interval 76.8 to 96.2), relative to the four trainers compared, against 56.1% (DPO), 36.1% (GRPO), and 20.4% (PPO); it leads PPO and GRPO, but without the within-model AQI suite it cannot be separated from DPO, which switches more under safety contracts.

## ✅ Pre-submit checklist

| Check | Status |
|---|---|
| AAAI-27 two-column format, `\nocopyright` (non-archival) | ✅ |
| Main text 6-8 pages excluding references | ✅ references start on page 8, so the main text is under 8 pages |
| Every number traceable to `outputs/` (score CIs: `outputs/evaluation/score_table_ci/score_table_ci.json`) | ✅ Table 4, Findings, abstract and conclusion use the 2026-10-20 run |
| No em-dashes / AI tells (`.claude/skills/audit-ai-signatures`) | ✅ PASS 2026-10-20 (0 em dashes in PDF) |
| Version consistency (`~/.claude/skills/paper-consistency`) | ✅ PASS 2026-10-20 vs v5 (only hit: a vspace length, not a claim) |
| Linked arXiv paper (2601.06157) agrees with this PDF | ✅ Paper link removed 2026-10-20 (arXiv v2 not posted yet) |
| HF dataset cards agree with this PDF | ✅ both cards corrected 2026-10-20 (author-written prompts and types, evaluated subset named, Corrections note); citation title still arXiv v1 until v2 posts |
| Floor analysis (2026-10-20): Table 6, appendix Table 7, Proposition 1 | ✅ numbers from `outputs/evaluation/floor_leakage/floor_leakage.json` (`src/eval/floor_leakage.py`); floor set fixed in `configs/pipeline.yaml` before computing |
| OpenReview copy matches this PDF and abstract | ⬜ re-upload `~/Downloads/SwiPO_on_Ecliptica30k.pdf` and paste the abstract above (it gained one sentence) |
| Full draft audit (`.claude/skills/audit-paper-e2e-draft/check_draft.py --max-pages 8 --ref v4`) | ✅ PASS 2026-10-20: 0 FAIL, 24 PASS, 1 WARN (claim words, each read) |
