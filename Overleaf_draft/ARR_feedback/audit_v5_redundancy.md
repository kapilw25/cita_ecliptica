# 🔁 Redundancy audit: SwiPO arXiv paper (v5, 79 pages)

> Source: read-only sub-agent audit of `Overleaf_draft/v5_arxiv_v2_SwiPO/`, 2026-10-20, before the em-dash pass (line numbers may have shifted by a few). ✅ = re-checked by hand against the sources.

**Bottom line:** about 24 of the 79 pages repeat material that appears elsewhere (row total 28.2 pages; overlaps and float repacking bring the realistic net to 22 to 26 pages, so roughly 79 → 55). Only about 1.5 pages of the repetition is in the main body.

## ✅ Findings re-checked by hand

| Finding | Evidence |
|---|---|
| Labels `sec:training_pipeline_exp` and `sec:training_dynamics` are each defined twice | `7_results.tex:55,70` and `F_extended_results.tex:18,143`; LaTeX log: "multiply defined" |
| Decoding described two ways | `B_pipeline_diagrams.tex:446` "sampling (temperature=0.7, top-p=0.9)" vs `9_limitation.tex:22` "greedy decoding" |
| KL ablation disagrees | `H_faq.tex:305` best λ = 0.0005 vs `E_ablations.tex:36` best λ = 0.00023 (and λ=0 margin 4.0 vs 3.8) |

## 📋 Full table (agent output)

Legend: abs = abstract, TLDR = key-ideas box, concl = Conclusion; intro, 5isd, 4swipo, 7res, 9lim = main-body files; A to I, O = appendix source files; Q# = FAQ number as printed; pN = PDF page.

```text
┌────┬───────────┬──────────────────────────────────────────────────────┬────────────────────────┬────────────────────────────────────┬───────┐
│ #  │ type      │ locations (file + short quote)                       │ keep                   │ cut or merge                       │ pages │
├────┼───────────┼──────────────────────────────────────────────────────┼────────────────────────┼────────────────────────────────────┼───────┤
│ 1  │ rep. fig  │ D: 10 full-width [p] boxes "Example 1: Corporate Tax │ tab:instruction_full + │ cut 9 boxes (opt. 10x3 phrasings   │ 4.5   │
│    │           │ Avoidance".."Example 10" (p44-48), each re-lists the │ 1 box                  │ table)                             │       │
│    │           │ same 30 expected markers as tab:instruction_full and │                        │                                    │       │
│    │           │ tab:characteristics_taxonomy                         │                        │                                    │       │
│ 2  │ rep. tab  │ I: limitations_glance L1-L6, roadmap_glance,         │ 9lim text              │ cut 3 tables; move L1 paraphrase,  │ 2.0   │
│    │           │ tab:limitations = 9lim + Future Work; unreferenced   │                        │ L3 judge drift, L5 out-of-grid     │       │
│ 3  │ rep. tab  │ I: discussion_glance, discussion_claims, tradeoffs   │ O D.3 trade-off para   │ cut 3 tables                       │ 1.5   │
│    │           │ (unreferenced) = O D.1-D.3 + F "Interpretation"      │                        │                                    │       │
│ 4  │ rep. fig  │ F: 5 bar-chart figures = the 40 heatmap cells; F     │ CI heatmap (#19)       │ drop or one 5-panel fig            │ 1.5   │
│    │           │ prose repeats each value 3-4x                        │                        │                                    │       │
│ 5  │ rep. tab  │ Metric definitions 4x: 7res tab:benchmarks, B eval   │ tab:benchmarks + B     │ cut B G.1-G.5, F metric paras;     │ 1.3   │
│    │           │ caption, B G.1-G.5, F x5; B says sampling, 9lim      │ caption                │ move B G.6 (86.7% definition) to   │       │
│    │           │ says greedy                                          │                        │ 7res                               │       │
│ 6  │ other     │ E sec K "Detailed Evaluation" (p55-57): no numbers;  │ G                      │ cut or 3-line pointer              │ 1.3   │
│    │           │ restates FAQ Q10/Q11/Q23, I L1/L5, G                 │                        │                                    │       │
│ 7  │ FAQ dup   │ Q13+Q20+Q21+Q22 (why KL); Q13 table disagrees with E │ E table + 1 merged Q   │ merge to 1; drop "explained        │ 1.1   │
│    │           │ tab:kl_ablation (λ=0 margin 4.0 vs 3.8; best 0.0005  │                        │ entirely by KL"                    │       │
│    │           │ vs 0.00023)                                          │                        │                                    │       │
│ 8  │ rep. claim│ O D.1-D.3 sentences verbatim from 5isd, intro:363,   │ 4swipo, 5isd, 7res;    │ cut D.1, most of D.2, D.3 paras    │ 1.1   │
│    │           │ Fig 2 caption, 4swipo:177; D.3 deltas = 7res table   │ O keeps D.4            │ 1-3                                │       │
│ 9  │ FAQ dup   │ Q6 = 4swipo "key departure"; Q7 = B + 7res + F; Q15  │ main + B               │ cut 3; Q6 "20-30% drop" vs E -41%; │ 1.05  │
│    │           │ = feature table + C compute                          │                        │ Q7 "~4.5 h" vs C 17 h / 12 h       │       │
│ 10 │ FAQ dup   │ Q1 delta table (AQI +22.4/+41.7 vs main -6.2/+26.4); │ 7res, F M.4            │ cut 3; move "average normalized    │ 1.0   │
│    │           │ Q2 = O D.3 + 7res + F; Q5 = F M.4 + O D.3            │                        │ radius" into radar caption         │       │
│ 11 │ rep. fig  │ F fig:training_margins = same dpo_cita_margins.pdf   │ 7res fig               │ cut copy                           │ 1.0   │
│    │           │ as 7res fig:main_training_margins                    │                        │                                    │       │
│ 12 │ FAQ dup   │ Q8 = 9lim Inference Overhead; Q9 = 9lim Dual-Use;    │ 9lim, intro            │ cut 3; add Q9 "audit trails" to    │ 0.8   │
│    │           │ Q19 = intro role table + TLDR                        │                        │ 9lim                               │       │
│ 13 │ FAQ dup   │ Q10, Q17, Q23 all claim paraphrase + composition     │ 1 merged Q             │ merge; cite source or drop         │ 0.75  │
│    │           │ robustness; contradicted by I L1 and a G failure     │                        │                                    │       │
│ 14 │ rep. tab  │ F M.1 = 7res + B (duplicate label); M.2              │ 7res, B                │ cut M.1, M.2; fix labels           │ 0.75  │
│    │           │ tab:model_variants (unreferenced) = B list           │                        │                                    │       │
│ 15 │ rep. fig  │ I Toolbox (p79) Steps 1-4 = Fig 2 = A derivation =   │ Fig 2, A               │ cut Steps 1-5; Steps 6-7 into O    │ 0.75  │
│    │           │ TLDR equation; Step 5 = tab:benchmarks               │                        │ D.4                                │       │
│ 16 │ rep. tab  │ D tab:ecliptica_stats + "Source Categories" = 5isd + │ 5isd tables; D         │ cut stats panel, category para,    │ 0.7   │
│    │           │ tab:prompt_categories; "300 x 10 = 3,000" ~11x       │ instruction_full       │ taxonomy                           │       │
│ 17 │ rep. tab  │ SwiPO hyper-parameters 3x and disagreeing: B (WD     │ C table + NoInstruct   │ cut B lists, F table               │ 0.65  │
│    │           │ 0.0047/0.0127, warmup 0.086/0.054), F (0.0091/       │ column                 │                                    │       │
│    │           │ 0.0109, 7.5%/10%), C (0.011, 10%)                    │                        │                                    │       │
│ 18 │ FAQ dup   │ Q4, Q14 = 9lim Model Generalization; Q4 "10,813      │ 9lim                   │ cut both                           │ 0.6   │
│    │           │ pairs" vs B 12,035 vs D 44,137                       │                        │                                    │       │
│ 19 │ rep. fig  │ Heatmap twice: 7res heatmap_no_ci and F heatmap      │ CI version in main     │ cut F copy                         │ 0.6   │
│ 20 │ rep. claim│ E: "Goldilocks" 4x, Trial 7 justified 4x             │ 1 Trial-7 para         │ trim                               │ 0.5   │
│ 21 │ rep. tab  │ teaser and 5isd table both use the neighbor prompt;  │ teaser                 │ move 10-answer table to D          │ 0.45  │
│    │           │ the 5isd one is never referenced                     │                        │                                    │       │
│ 22 │ rep. fig  │ B Fig 7 "reproduced from Figure 3"                   │ 7res Fig 3             │ cut copy                           │ 0.45  │
│ 23 │ FAQ dup   │ Q3 (cites hendrycks2023aligning for AQI vs borah in  │ Q3 short, Q11          │ trim Q3/Q11, drop Q24 (ARR-only    │ 0.4   │
│    │           │ main), Q11 failure table, Q24 aclpubcheck            │                        │ aclpubcheck)                       │       │
│ 24 │ other     │ Optuna/TPE explained 5x; trials 13 vs "15 + 15" (B)  │ B search space         │ cut 4 blurbs                       │ 0.35  │
│ 25 │ rep. claim│ "~50% lower LR, sequences 30-40% longer" 7x          │ 7res + B               │ cut C, E x2, F                     │ 0.3   │
│ 26 │ rep. claim│ "regimes nearby and traversable" ~20x                │ 4swipo KL para + A     │ cut the rest                       │ 0.3   │
│ 27 │ rep. claim│ "one policy per checkpoint" ~13x, "no retraining /   │ abs + intro "Static    │ cut TLDR x3, A, D, E, F copies     │ 0.3   │
│    │           │ N checkpoints" ~12x                                  │ alignment"             │                                    │       │
│ 28 │ rep. claim│ TLDR box restates abstract, intro, Fig 2 equation;   │ abs, concl             │ TLDR to 3 bullets                  │ 0.3   │
│    │           │ concl para 1 repeats abstract sentences 1-2          │                        │                                    │       │
│ 29 │ rep. tab  │ method-comparison tables 5x (4swipo, A, Q15, Q21, B) │ main table + B         │ cut A table                        │ 0.3   │
│ 30 │ rep. fig  │ 5isd: instruction derivation told 3x                 │ fig + 2 sentences      │ compress                           │ 0.25  │
│ 31 │ rep. claim│ agentic motivation ~7x                               │ intro                  │ A to 1 sentence; cut F para        │ 0.2   │
│ 32 │ rep. fig  │ objective written 6x; B form (L_DPO + mean           │ Fig 2 + A              │ reconcile B                        │ 0.2   │
│    │           │ log-ratio) differs from Fig 2                        │                        │                                    │       │
│ 33 │ other     │ App. C roadmap letters A-I do not match the PDF      │ none                   │ delete                             │ 0.2   │
│ 34 │ rep. claim│ "DPO still switches more on ECLIPTICA/Cond. Safety"  │ abs, 7res caption, O   │ cut rest                           │ 0.15  │
│    │           │ ~14x                                                 │                        │                                    │       │
│ 35 │ rep. claim│ following vs alignment ~15x; the only definition is  │ RQ3 + restored 5isd    │ cut F, O, D, G copies              │ 0.15  │
│    │           │ inside a 5isd comment block                          │ definition             │                                    │       │
│ 36 │ rep. claim│ "offline 40GB vs online 80GB" 5x                     │ C tab:compute          │ cut others                         │ 0.15  │
│ 37 │ rep. claim│ 86.7% sentence 10x, "54x" 4x                         │ abs, intro, caption,   │ cut 7res:132, O C3                 │ 0.1   │
│    │           │                                                      │ concl                  │                                    │       │
│ 38 │ other     │ related work split between intro and A; intro        │ 1 intro sentence       │ move paragraph into A; cite CoSA   │ 0.1   │
│    │           │ promises a design-differences table that does not    │                        │                                    │       │
│    │           │ exist; CoSA in bib but never cited                   │                        │                                    │       │
│ 39 │ bib dup   │ printed twice: TruthfulQA, HH-RLHF, Llama 3; six     │ one key each           │ re-key 3 pairs; delete 6 unused    │ 0.1   │
│    │           │ unused second keys (OPT-IML, SteerLM, CoSA arXiv...) │                        │ entries                            │       │
│ 40 │ FAQ keep  │ Q12, Q16, Q18 add new content (Q12 "DPO + prompting  │ keep (fix Q12)         │ none                               │ 0     │
│    │           │ 0.25" vs F DPO_Instruct 0.389)                       │                        │                                    │       │
└────┴───────────┴──────────────────────────────────────────────────────┴────────────────────────┴────────────────────────────────────┴───────┘
```

## 🧭 Summary

| # | Source of repetition | Pages |
|---|---|---|
| 1 | Experiments and results told again in appendices B, C, E, F (rows 4, 5, 11, 14, 17, 19, 22, 24, 25) | ~6.9 |
| 2 | FAQ: 18 of 24 answers restate the main text, Limitations or another answer (rows 7, 9, 10, 12, 13, 18, 23) | ~5.7 |
| 3 | Discussion told 3 to 4 times across O, I and 9_limitation (rows 2, 3, 8, 15) | ~5.4 |
| 4 | Ten example boxes in Appendix D (row 1) | 4.5 |

⚠️ Several duplicate copies **disagree** with each other (AQI deltas in Q1, KL ablation in Q13, hyper-parameters across B/C/F, training-data size 10,813 vs 12,035 vs 44,137, Optuna trials 13 vs 15+15, sampling vs greedy, compute ~4.5 h vs 17 h), so keeping one copy also removes the contradiction. The discrepancy audit (`audit_v5_discrepancy.md`) checks which copy is correct against the code.
