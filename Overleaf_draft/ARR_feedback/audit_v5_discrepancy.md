# 🔎 Discrepancy audit: SwiPO arXiv paper (v5) vs code, results and the submitted abstract

> Source: read-only sub-agent audit of `Overleaf_draft/v5_arxiv_v2_SwiPO/` against `src/`, `outputs/`, `configs/`, the Optuna databases and `v4_AAAI27_student_abstract/0_main_AAAI.tex`, 2026-10-20 (after the em-dash pass). ✅ = re-checked by hand.

## ✅ Re-checked by hand

| # | Finding | Evidence |
|---|---|---|
| 1 | ECLIPTICA prompts are author-written, not HH-RLHF | `src/eval/isd_dataset.py` `PROMPT_CATEGORIES` (300 literals) |
| 3 | Scorer is all-MiniLM-L6-v2 with fidelity = (1+cos)/2 to a text prototype, not E5 centroids | `src/utils/eval/isd_metrics.py` L50, L161-177 |
| 6 | Training attaches ONE refusal-style instruction per prompt; Y+ is always the safe reply; no contrasting contract is trained | `src/utils/train/data_prep/loader_pku.py` L121-140, `formatters.py` |
| 7 | Conditional Safety evaluates the 1,222 PKU test clear-contrast prompts, which are inside the 12,035-pair training pool (90/10 resplit) | `loader_pku.py` L7-44, `src/train/{dpo,cita}.py`, `conditional_safety.py` L200-225 |
| 11 | AQI is min-max / sigmoid normalized within each model's run, so it does not rank models | `src/utils/eval/aqi/aqi_dealign_xb_chi.py` L858-932 |
| 12 | The plotted bootstrap CIs resample different statistics from the printed scores | `src/eval/combined_plots.py` L70-150 (fixed by `src/eval/score_table_ci.py`) |
| 29 | Loss = lambda_DPO x TRL dpo_loss (with reference log-ratios) + lambda_KL x mean log-ratio on the pairs | `src/utils/train/cita_trainer.py` L187-212, L262-268 |

## 📋 Full table (agent output)

```text
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| #   | SEV  | LOCATION (file: quote)         | WHAT DISAGREES                                 | EVIDENCE                           | PROPOSED FIX                 |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 1   | HIGH | 5_isd_dataset: '300 prompts    | Prompts are 300 author-written policy          | src/eval/isd_dataset.py            | Say author-written over 12   |
|     |      | (taken from                    | questions (12 cats x 25, mean 6.6 words), not  | PROMPT_CATEGORIES (300 literals);  | categories; drop HH-RLHF     |
|     |      | \citep{bai2022training})'; v4  | HH-RLHF.                                       | configs/ecliptica_taxonomy_100.yam | cite (fix v4 too).           |
|     |      | abstract: '300 HH-RLHF         |                                                | l 'all prompts are open            |                              |
|     |      | prompts'                       |                                                | policy/ethics questions'           |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 2   | HIGH | 5_isd: 'is \textbf{not         | Code defines the 10 types by hand ('5 from     | src/eval/isd_dataset.py            | Rewrite as hand-designed     |
|     |      | hand-written}', 10K HH         | Proposal Table 2 + 5 Additional (to reach      | ISD_INSTRUCTIONS; no judge         | taxonomy, or produce and     |
|     |      | triples, 5 judges, BERTScore   | 10)'), 3 hand-written variants each; leftover  | outputs, BERTScore, seed triples   | release the judge/annotation |
|     |      | 3-of-5, 2 annotators >=4/5;    | off-topic variants ('supports artists          | or ratings anywhere in repo        | artifacts.                   |
|     |      | Fig ecliptica_pipeline; Tab    | concerned about AI', 'Favor traditional        | (grep): none found                 |                              |
|     |      | judge_models; v4 'derived ...  | human-created art forms') are applied to       |                                    |                              |
|     |      | by five judge models and gated | unrelated prompts (D Examples 5, 7-10). Same   |                                    |                              |
|     |      | by two annotators'             | origin as the 90 'hand-designed' 30k types.    |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 3   | HIGH | D_dataset_details L156:        | Code: all-MiniLM-L6-v2; Fidelity =             | src/utils/eval/isd_metrics.py L50, | Replace the sentence with    |
|     |      | 'embedded using E5-large-v2    | (cos(response, text prototype 'A response that | L161-177; src/eval/isd.py L548;    | the B/code definition.       |
|     |      | and compared against           | is ...')+1)/2; Shift = mean pairwise cosine    | configs/rebuttal/exp*.yaml         |                              |
|     |      | instruction-specific centroids | distance of the 10 responses. No E5, no        | embedding_model                    |                              |
|     |      | ... Fidelity (probability of   | centroids, no classifier. (B L467 is correct.) |                                    |                              |
|     |      | correct instruction            |                                                |                                    |                              |
|     |      | classification)'               |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 4   | HIGH | 9_limitation: 'With greedy     | All suites sample once (T=0.7, top-p=0.9) with | src/eval/isd.py L185-188;          | 'single sampled generation   |
|     |      | decoding at 512 new tokens'; C | no generation seed; caps are 512 (ECLIPTICA,   | truthfulqa.py L354-357;            | (T=0.7, top-p 0.9),          |
|     |      | L9: 'all reported metrics are  | Length), 256 (TruthfulQA, Cond Safety), 150    | conditional_safety.py L345-348;    | deterministic scoring';      |
|     |      | deterministic'; TL;DR 'five    | (AQI). Only the scorers are deterministic.     | length_control.py L226-229; aqi.py | per-suite caps.              |
|     |      | deterministic suites';         |                                                | L247-250                           |                              |
|     |      | intro/O_discussion 'five       |                                                |                                    |                              |
|     |      | deterministic benchmarks'; B   |                                                |                                    |                              |
|     |      | L446 'max 512 new tokens'      |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 5   | HIGH | 7_results L9: 'preference data | All training uses PKU-SafeRLHF (B, FAQ Q4, Fig | src/utils/train/data_prep/loader_p | 'PKU-SafeRLHF'; drop HH      |
|     |      | is drawn from Anthropic HH     | training_pipeline agree). PPO uses prompts +   | ku.py; src/train/ppo.py, grpo.py   | cite; fix v4 sentence.       |
|     |      | (hh-rlhf)'; F L20 '\cite{ji202 | RM, GRPO heuristic rewards, not preference     |                                    |                              |
|     |      | 4pku,bai2022training}'; v4     | pairs.                                         |                                    |                              |
|     |      | Setup 'preference pairs then   |                                                |                                    |                              |
|     |      | train PPO, GRPO'               |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 6   | HIGH | 4_cita: 'Y+>Y- is defined      | Training gives each prompt ONE deterministic   | loader_pku.py                      | Describe the real            |
|     |      | relative to I'; 'paired        | refusal instruction ('You must REFUSE any      | synthesize_system_instruction      | conditioning; drop Q17       |
|     |      | conditions (I_a,X),(I_b,X)     | requests involving {harms}. Always prioritize  | L121-140; data_prep/formatters.py  | premise; fix B template (or  |
|     |      | with incompatible targets';    | user safety over helpfulness.'); Y+ is always  | format_*_Instruct                  | retrain with contrasting     |
|     |      | FAQ Q17 'You train on 10       | the safe reply. No ECLIPTICA type, permissive  |                                    | pairs).                      |
|     |      | instruction types'; B L37      | or contrasting instruction is ever trained; B  |                                    |                              |
|     |      | template 'may involve [harm].  | quotes a different template.                   |                                    |                              |
|     |      | Respond safely and helpfully.' |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 7   | HIGH | 7_results Tab benchmarks: Cond | Eval set is PKU-SafeRLHF test split,           | conditional_safety.py L200-225; Co | Name PKU test (1,222),       |
|     |      | Safety                         | clear-contrast, n=1,222. Those 1,222 prompts   | nditional_Safety_Evaluation/*/metr | disclose overlap, or re-run  |
|     |      | \citep{mazeika2024harmbench},  | are also in training (SFT/DPO/SwiPO train on   | ics.json n_prompts=1222;           | on a held-out set.           |
|     |      | '1{,}000'; B L495-497 'Based   | train+test clear-contrast 12,035, 90/10        | loader_pku.py L7-44; sft.py L171,  |                              |
|     |      | on HarmBench ... 1,000         | split), so ~90% of eval prompts were seen in   | dpo.py L201                        |                              |
|     |      | prompts'                       | training.                                      |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 8   | HIGH | 7_results Tab benchmarks:      | Length Control n=805 (all of AlpacaEval).      | Length_Control_Evaluation/*/metric | 805 / 817 prompts, one       |
|     |      | Length Ctrl '1{,}000',         | TruthfulQA has 817 questions (1,634 = 817 x 2  | s.json n_prompts=805; TruthfulQA_E | counting convention (1,610 / |
|     |      | TruthfulQA '1{,}634'; B L513   | generations). Table mixes conventions (TQA x2, | valuation/*/metrics.json           | 1,634 / 2,444 cases).        |
|     |      | '1,000 prompts from            | others not).                                   | n_questions=817                    |                              |
|     |      | AlpacaEval'; B L481 '1,634     |                                                |                                    |                              |
|     |      | questions'                     |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 9   | HIGH | 1_introduction L355: '54x      | Unrounded Delta: SwiPO 0.05385, DPO 0.00122 -> | TruthfulQA_Evaluation/{CITA,DPO}_{ | Drop the ratio; report       |
|     |      | stronger adaptation than DPO   | 44x, not 54x. DPO Delta is 1 question of 817;  | Instruct,NoInstruct}/metrics.json  | +0.054 vs +0.001 with a CI.  |
|     |      | (+0.054 vs +0.001)'; FAQ Q1    | heatmap CI on SwiPO_I is +/-0.19.              | adaptation_score                   |                              |
|     |      | table + text, Q22              |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 10  | HIGH | H_faq Q1 Tab                   | Main body, Tab improvement_comparison, F and   | AQI_Evaluation/*/*_metrics_summary | -6.2 / +26.4; remove '86%    |
|     |      | faq_benchmark_deltas: 'AQI &   | v4: AQI Delta DPO -6.2, SwiPO +26.4. FAQ       | .csv; iter_plans/iter18_OverleafDr | better'.                     |
|     |      | +22.4 & +41.7 & 86% better'    | values are stale (older AQI run, 95.6%         | aft/key_numbers_17plots.md L217    |                              |
|     |      |                                | efficiency era).                               |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 11  | HIGH | 7_results/B/F: 'AQI = (CHI +   | Code: AQI = 0.5*CHI_norm + 0.5*XB_norm with    | src/utils/eval/aqi/aqi_dealign_xb_ | Define AQI as coded and      |
|     |      | XB)/2'; F: 'scale is 0-100,    | CHI min-max normalized within each model's own | chi.py L858-932; AQI_Evaluation/*/ | caveat, or renormalize       |
|     |      | with 100 representing perfect  | 7 axioms+overall and XB sigmoid-normalized,    | *_metrics_summary.csv              | across models before         |
|     |      | cluster separation'            | floored at 10. Overall AQI is bounded [5,55];  |                                    | ranking.                     |
|     |      |                                | SwiPO_I 55.0 is the ceiling (CHI_norm 100,     |                                    |                              |
|     |      |                                | XB_norm 10) and not comparable across models   |                                    |                              |
|     |      |                                | (SFT_NI raw CHI 430 > SwiPO_I 294, yet AQI     |                                    |                              |
|     |      |                                | 52.0 < 55.0).                                  |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 12  | HIGH | F Fig heatmap: '95% CI ...     | CIs are of different statistics: TQA on        | src/eval/combined_plots.py         | Bootstrap the reported       |
|     |      | from per-sample metrics'; F    | marker-count differences (mean 0.21 for        | L70-150; Length CITA_Instruct      | statistic, or drop the CIs.  |
|     |      | L517 'TruthfulQA and           | SwiPO_I), Cond Safety on refusal-confidence    | metrics.json avg_ratio=4.077; figu |                              |
|     |      | Conditional Safety show        | differences, Length on per-sample ratio (mean  | res/evaluation/combined_plots/heat |                              |
|     |      | relatively narrow intervals'   | 4.08 for SwiPO_I vs reported 1.14; heatmap     | map.pdf                            |                              |
|     |      | vs L542 '+/-0.11-0.28'; L548   | prints +/-4.00 on 0.987). Text also            |                                    |                              |
|     |      | 'SwiPO_I (0.013 +/-0.19)'      | self-contradicts on TQA width.                 |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 13  | HIGH | 7_results L71 + F L107:        | Actual LRs: NoInstruct 6.83e-6, Instruct       | outputs/training/CITA_{Instruct,No | '~21% lower than             |
|     |      | SwiPO_Instruct needs '~50%     | 5.41e-6 (21% lower); DPO 1e-5 (Instruct is 46% | Instruct}_config.json;             | SwiPO_NoInstruct (46% below  |
|     |      | lower LR than                  | lower). Search bounds: Instruct                | src/train/cita_optuna.py L98-119;  | DPO); Instruct space capped  |
|     |      | SwiPO_NoInstruct'; B L251,     | [2.5e-6,5.5e-6], NoInstruct [5e-6,8e-6]        | DPO_*_config.json                  | after an LR=6.83e-6          |
|     |      | L321, L328 'LR upper bound is  | (x0.69, disjoint), so 'Instruct prefers lower  |                                    | explosion'. Pick one         |
|     |      | halved'; E L243 '~50% lower LR | LR and smaller lambda_KL' (F Tab caption) is   |                                    | comparator.                  |
|     |      | than standard DPO'; E L260-263 | imposed by the bounds.                         |                                    |                              |
|     |      | 'lr_max = 0.5 x                |                                                |                                    |                              |
|     |      | lr_max_NoInstruct'; C L62-64   |                                                |                                    |                              |
|     |      | 'lower learning rate for SwiPO |                                                |                                    |                              |
|     |      | than DPO'                      |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 14  | HIGH | B L297-318: lambda_KL          | Code: Instruct lambda [1e-4,1e-3] linear, beta | src/train/cita_optuna.py L103-119; | Copy the coded spaces;       |
|     |      | [0.0001,0.01] log, LR          | [0.08,0.15], WD [0.005,0.015], warmup          | outputs/training/optuna_cita.db,   | '19+15 launched, 13+13       |
|     |      | [1e-6,2e-5], beta [0.05,0.3],  | [0.05,0.10]; NoInstruct lambda [5e-4,1.5e-3],  | optuna_cita_instruct.db            | completed'.                  |
|     |      | WD [0.001,0.1], warmup         | beta [0.08,0.12], WD [0.008,0.012], warmup     |                                    |                              |
|     |      | [0.03,0.15]; 'Total trials: 15 | [0.05,0.15]. DBs: NoInstruct 19 trials (13     |                                    |                              |
|     |      | (NoInstruct) + 15 (Instruct)'; | complete), Instruct 15 (13 complete).          |                                    |                              |
|     |      | 7_results/C/E '13 trials'      |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 15  | HIGH | B L332-350: Trial 5 'Weight    | DB/configs: Trial 5 WD 0.00907, warmup 0.0749; | optuna DBs trial_params;           | Use F's values in B.         |
|     |      | decay = 0.0047', 'Warmup ratio | Trial 7 WD 0.01094, warmup 0.0996. F Tab       | CITA_*_config.json                 |                              |
|     |      | = 0.086'; Trial 7 'Weight      | hyperparams_exp and C Tab full_hyperparams     |                                    |                              |
|     |      | decay = 0.0127', 'Warmup ratio | match the DB; B does not.                      |                                    |                              |
|     |      | = 0.054'                       |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 16  | HIGH | B Tab dpo_vs_cita_comparison:  | Main body, F, FAQ Q5: DPO ~6.0; logs: DPO      | DPO_*_config.json                  | DPO 6.0-6.1, SwiPO 7.2-7.5.  |
|     |      | 'Typical margin & 2.5--3.5 &   | final margins 6.11 (I), 6.01 (NI). 2.95 is DPO | eval_rewards/margins;              |                              |
|     |      | 6.5--7.5'                      | at step 200 in an early iter.                  | iter_plans/iter2/report.md L100    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 17  | HIGH | E Tab kl_ablation (lambda=0:   | Three mutually inconsistent versions (best     | src/utils/train/cita_trainer.py    | Remove both tables and the   |
|     |      | 3.8/0.22; 0.0005: 6.8/0.34;    | lambda, margins, 41% vs 20-30% drop). No such  | L91-92; optuna DBs; outputs/evalua | Q6/Q13/Q23 claims, or run    |
|     |      | best 0.00023: 7.5/0.37); FAQ   | runs exist: the trainer raises ValueError for  | tion/ISD_Evaluation_Embedding (10  | the sweep.                   |
|     |      | Q13 (lambda=0: 4.0/0.22;       | lambda_KL<=0, Optuna never sampled 0, 5e-5 or  | models only): none found           |                              |
|     |      | lambda=0.0005 is best:         | 1e-3 (Instruct), and ECLIPTICA was only run on |                                    |                              |
|     |      | 7.5/0.37); FAQ Q6 'removing KL | the 10 final models.                           |                                    |                              |
|     |      | causes 20-30% performance      |                                                |                                    |                              |
|     |      | drop'; FAQ Q23 'we ablate the  |                                                |                                    |                              |
|     |      | KL anchor and sweep lambda_KL' |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 18  | HIGH | E Tab beta_ablation (beta      | No runs: Optuna beta in [0.08,0.15].           | optuna DBs; figures/appendix/hp_ab | Remove table; keep DB-backed |
|     |      | 0.05/0.10/0.15/0.20; acc       | Contradicts E Fig hp_beta text ('margin        | lation_beta.pdf (beta axis         | plots.                       |
|     |      | 85/89/91/92%; margin           | inverted-U, peaks 0.10-0.12; at beta>0.14 ...  | 0.09-0.15): none found for table   |                              |
|     |      | 4.2/7.5/8.1/9.2; ECLIPTICA     | collapse') and table is monotonic in margin.   |                                    |                              |
|     |      | .29/.37/.35/.31)               | 'best 0.10' vs used 0.107.                     |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 19  | HIGH | E L236: 'sharp margin drop at  | DB: trials 1/3/4 have lambda 2.40e-4, 2.65e-4, | optuna_cita_instruct.db            | Attribute low margins to LR; |
|     |      | low lambda_KL (trials 1, 3, 4) | 6.51e-4 (not low) and the three lowest LRs     | trial_params / trial_values        | drop per-trial ECLIPTICA     |
|     |      | demonstrates that the KL       | (2.6e-6, 3.2e-6, 2.8e-6); trials with          |                                    | claims.                      |
|     |      | anchor is not optional'; L227  | lambda<1.5e-4 (2, 5) reach margins 6.98, 5.60. |                                    |                              |
|     |      | 'At lambda_KL < 1.5e-4 ... low | No per-trial ECLIPTICA eval exists.            |                                    |                              |
|     |      | margins'; L171/L251 Trial 7    |                                                |                                    |                              |
|     |      | 'best ECLIPTICA', trials 0/12  |                                                |                                    |                              |
|     |      | 'degraded switching'           |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 20  | HIGH | H_faq Q12 Tab                  | No results: exp4 was planned, not run. Values  | src/eval/exp4_system_prompt.py     | Delete Q12 table/claims or   |
|     |      | faq_cita_vs_prompting:         | are the placeholder template of the rebuttal   | exists; outputs/rebuttal has only  | run exp4.                    |
|     |      | zero-shot 0.12, few-shot 0.18, | plan (which also lists DPO_Instruct 0.25, CITA | exp1, exp1_5, exp2;                |                              |
|     |      | DPO+prompting 0.25, SwiPO 0.37 | 0.41). Measured DPO_Instruct = 0.389 > SwiPO   | iter_plans/iter19_rebuttal/plan.md |                              |
|     |      | (+robustness/consistency       | 0.367.                                         | L560-563                           |                              |
|     |      | labels); 'Jailbreak            |                                                |                                    |                              |
|     |      | resistance'                    |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 21  | HIGH | H_faq Q10 (paraphrases,        | No paraphrase, composition or unseen-type eval | outputs/rebuttal/exp2_query_scramb | Delete; report exp2 in       |
|     |      | 'concise AND professional',    | exists. The repo's own query-scrambled test    | led/verdict.txt, summary.json:     | Limitations.                 |
|     |      | 'Pattern matching would fail   | (exp2) reports 'SHORTCUT learning (full ~      | none found for                     |                              |
|     |      | ...'); unnumbered Q after Q22  | scrambled)': SwiPO_I fidelity full 0.560 vs    | paraphrase/composition             |                              |
|     |      | ('Paraphrase robustness',      | scrambled 0.565. I_discussion_floats L1 lists  |                                    |                              |
|     |      | 'Compositional generalization  | paraphrase checks as future work.              |                                    |                              |
|     |      | ... we measure joint           |                                                |                                    |                              |
|     |      | satisfaction'); Q17 success    |                                                |                                    |                              |
|     |      | rates ~90/75/60/30%            |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 22  | HIGH | H_faq Q11: 'No catastrophic    | No red-teaming or harm checker was run. Under  | Conditional_Safety_Evaluation/CITA | Delete the claim and the     |
|     |      | safety failures observed:      | PERMISSIVE, SwiPO_I does not refuse 83.3% of   | _Instruct/metrics.json             | untested failure modes.      |
|     |      | SwiPO never produced harmful   | 1,222 PKU prompts that carry a labeled unsafe  | permissive_refusal_rate=0.167:     |                              |
|     |      | content ... in our             | reply; O_discussion says Cond Safety does not  | none found for red-teaming         |                              |
|     |      | red-teaming'; failure-mode     | certify permissive non-harm.                   |                                    |                              |
|     |      | table (>2K tokens, 'Klingon')  |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 23  | HIGH | H_faq Q16: 'We verified SwiPO  | No capability or Base->SwiPO results exist.    | src/eval/exp3_capability.py        | Delete or run.               |
|     |      | doesn't degrade base           |                                                | exists, no outputs/rebuttal/exp3*; |                              |
|     |      | capabilities (perplexity,      |                                                | outputs/training has no base-init  |                              |
|     |      | coherence)'; Q7: 'Training     |                                                | SwiPO run: none found              |                              |
|     |      | SwiPO directly on base Llama   |                                                |                                    |                              |
|     |      | ... produces 40% lower         |                                                |                                    |                              |
|     |      | ECLIPTICA scores'              |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 24  | HIGH | H_faq Q21: '30.6 pp gap        | SwiPO differs from DPO by an extra training    | Tab improvement_comparison;        | Soften to a hypothesis.      |
|     |      | explained entirely by KL       | stage, Optuna tuning, LR and beta; nothing     | CITA_*_config.json vs              |                              |
|     |      | architecture'; Q20: mode       | isolates KL. DPO has the largest Delta on      | DPO_*_config.json                  |                              |
|     |      | collapse is 'exactly what we   | ECLIPTICA and Cond Safety, so it is not        |                                    |                              |
|     |      | observe with DPO (+0.001)'     | collapsed.                                     |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 25  | HIGH | H_faq Q18 Tab                  | SwiPO-named repos return HTTP 401 (do not      | curl                               | Use the CITA repo URLs (or   |
|     |      | faq_reproducibility: anonymous | exist); CITA-named repos return 200. PPO/GRPO  | huggingface.co/api/models/...;     | create SwiPO aliases); state |
|     |      | ML123/llama3-8b-pku-SwiPO-{NoI | checkpoints are missing from the table.        | src/utils/train/model_utils.py     | per-stage compute.           |
|     |      | nstruct,Instruct}-DPO-*; Q18   | Compute: C Tab compute says PPO 17 h + GRPO 12 | L463-480;                          |                              |
|     |      | text and Q7: '~4.5 hours       | h + DPO 103 min + SwiPO 120 min (plus Optuna   | src/train/{ppo,grpo,cita}.py       |                              |
|     |      | total'                         | ~20-24 h per variant); 4.5 h is only           | docstrings; cita_optuna.py L12-13  |                              |
|     |      |                                | SFT+DPO+SwiPO for one variant.                 |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 26  | HIGH | C Tab hardware: 'GPU & NVIDIA  | Same section says PPO/GRPO need 80GB;          | requirements_gpu.txt L29-32;       | A100-40GB/80GB rows; real    |
|     |      | A100-40GB', 'PyTorch 2.1 +     | README/requirements tested on A100-80GB. Pins: | requirements_grpo.txt L18, L40,    | versions.                    |
|     |      | Transformers 4.35', 'Optuna    | torch 2.5.1, transformers 4.51.0 (4.56.2 for   | L66; requirements.txt L45;         |                              |
|     |      | 3.4'                           | GRPO), TRL 0.11.4 / 0.22.2, Optuna 4.1.0.      | README.md L14                      |                              |
|     |      |                                | Transformers 4.35 cannot load Llama-3.1.       |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 27  | HIGH | 1_introduction L343: 'SwiPO    | Abstract/TL;DR/Fig                             | src/utils/train/cita_trainer.py    | Remove SFT from the          |
|     |      | couples supervised fine-tuning | cita_objective_box/derivation define 2 terms   | L262-268                           | objective wording (SFT is    |
|     |      | with contrastive preference    | (preference + lambda KL); B L286 'NO L_SFT';   |                                    | only the stage before DPO).  |
|     |      | optimization'; L352: 'an       | trainer loss = lambda_DPO*L_DPO +              |                                    |                              |
|     |      | objective that combines SFT    | lambda_KL*L_KL.                                |                                    |                              |
|     |      | and contrastive preference     |                                                |                                    |                              |
|     |      | learning'                      |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 28  | HIGH | G_qualitative: 'SwiPO_Instruct | None of these texts appear in any output;      | grep over outputs/evaluation: none | Label as illustrative        |
|     |      | Response' crypto table;        | crypto and criticism prompts are not in        | found; src/eval/isd_dataset.py     | (author-written) or replace  |
|     |      | 'Observed response (failure):  | ECLIPTICA or any eval set; composition was     |                                    | with logged outputs.         |
|     |      | Thank you for the feedback.    | never evaluated. The neighbor prompt is a PKU  |                                    |                              |
|     |      | [stops abruptly]'; 5_isd Tab   | test prompt, not an ECLIPTICA prompt.          |                                    |                              |
|     |      | ecliptica_one_prompt (10       |                                                |                                    |                              |
|     |      | 'Model response R(I,X)' for    |                                                |                                    |                              |
|     |      | the neighbor prompt)           |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 29  | MED  | 4_cita Fig cita_objective_box  | Code uses TRL dpo_loss (reference log-ratios   | src/utils/train/cita_trainer.py    | Put pi_ref in Delta; call    |
|     |      | + A derivation: Delta = log    | vs frozen DPO checkpoint) and 'KL' =           | L187-212                           | the anchor a sequence        |
|     |      | pi_theta(Y+|I,X) - log         | 1/2[mean(log pi_theta - log pi_ref)(Y+) +      |                                    | log-ratio estimate.          |
|     |      | pi_theta(Y-|I,X);              | same(Y-)] on offline pairs: a signed           |                                    |                              |
|     |      | KL(pi_theta||pi_0) as          | log-ratio, not a KL. B L251/L277 states the    |                                    |                              |
|     |      | expectation under pi_theta     | code form. No SFT term or Fisher-norm penalty  |                                    |                              |
|     |      |                                | anywhere (checked all appendices).             |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 30  | MED  | H_faq Q1: Delta 'normalized to | Code: 0.1 + 0.9 * min-max across the 4         | src/utils/eval/plotting.py         | One definition, incl. 0.1    |
|     |      | [0,1], then averaged'; B L551: | trainers per suite, then mean. Recomputed 86.7 | L778-800                           | floor and 'relative to the 4 |
|     |      | 'normalizing each Delta to its | / 56.1 / 36.0 / 20.4: matches, but it is a     |                                    | trainers'.                   |
|     |      | maximum possible value'; v4:   | relative score (best trainer on a suite =      |                                    |                              |
|     |      | 'after min-max normalization'  | 100%).                                         |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 31  | MED  | F L336-343: 'SwiPO_NoInstruct  | B L432 and code: NoInstruct models never       | truthfulqa.py L304-312;            | Drop the interpretation;     |
|     |      | performs worst (-0.040) ...    | receive the HON/CONF (or STRICT/PERMISSIVE,    | conditional_safety.py L298-305;    | state what Delta measures.   |
|     |      | inherits DPO's baseline        | ECLIPTICA) instruction, so their two runs are  | isd.py L143-149                    |                              |
|     |      | miscalibration'; 'negative ... | the same prompt sampled twice; NoInstruct      |                                    |                              |
|     |      | more uncertainty under the     | scores are sampling noise and Delta also mixes |                                    |                              |
|     |      | CONFIDENT instruction'         | in test-time instruction presence.             |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 32  | MED  | O_discussion L60: '(7.5 vs     | DPO 0.919/0.916 vs SwiPO 0.890 (I) / 0.891     | DPO_*/checkpoint-1354/trainer_stat | '92% vs 89%'; caveat margin  |
|     |      | 6.0) at similar training       | (NI): ~3 pp, not similar. Margins are against  | e.json; optuna_cita_instruct.db    | comparability.               |
|     |      | accuracy (~89%)'; F L561       | different references (SFT vs DPO checkpoint)   | trial 7;                           |                              |
|     |      | 'similar preference accuracy   | and betas (0.1 vs 0.107/0.119), so '25% higher | CITA_NoInstruct/checkpoint-1354    |                              |
|     |      | (~89%)'; FAQ Q5 'DPO 91% vs    | margin' is not like-for-like.                  |                                    |                              |
|     |      | SwiPO 89% (-2%)'; F L163 '~3   |                                                |                                    |                              |
|     |      | percentage points'             |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 33  | MED  | D Tab pku_stats: 'Total        | Loader: 10,813 train + 1,222 test              | loader_pku.py L7-44; none found    | Report 12,035 and 90/10      |
|     |      | Examples 44,137', 'Training    | clear-contrast = 12,035, split 90/10 (~10,831  | for 44,137                         | everywhere.                  |
|     |      | Split 83%', 'Validation Split  | / 1,204). No source for 44,137 or 83/17.       |                                    |                              |
|     |      | 17%'; FAQ Q4: '10,813          |                                                |                                    |                              |
|     |      | preference pairs'; B L35:      |                                                |                                    |                              |
|     |      | '12,035'                       |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 34  | MED  | B L417/L423 and F L47: '10     | Results report 8 models (v4: 'all eight        | outputs/evaluation/*/SFT_* ;       | Report SFT rows or say 8     |
|     |      | model variants'; Fig           | models'); SFT results exist but are omitted.   | AQI_Evaluation/SFT_NoInstruct      | evaluated.                   |
|     |      | evaluation_pipeline '10        | With SFT, SFT_NI AQI 52.0 is second-best       | metrics_summary.csv                |                              |
|     |      | Models'; F L487 '26%           | (SwiPO_I +5.8%).                               |                                    |                              |
|     |      | improvement over the           |                                                |                                    |                              |
|     |      | second-best model (PPO_I       |                                                |                                    |                              |
|     |      | 43.5)'                         |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 35  | MED  | H_faq Q2: 'ECLIPTICA measures  | Main body presents ECLIPTICA (Fidelity x       | 7_results Tab benchmarks;          | Align Q2 with main; 'adapted |
|     |      | behavioral shift magnitude,    | Shift) as the instruction-alignment benchmark. | custom.bib                         | from'; fix cite.             |
|     |      | not alignment quality'; Q3:    | Cond Safety and Length Control are             |                                    |                              |
|     |      | 'TruthfulQA, Conditional       | author-built conversions (PKU test,            |                                    |                              |
|     |      | Safety, Length Control, and AQ | AlpacaEval); AQI is cited to ETHICS            |                                    |                              |
|     |      | I~\cite{hendrycks2023aligning} | (hendrycks) instead of                         |                                    |                              |
|     |      | are independent, established   | borah-etal-2025-alignment.                     |                                    |                              |
|     |      | benchmarks'                    |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 36  | MED  | C L150-159: 'We verify that    | No such truncation or hard-negative logic (PKU | src/train/*.py, src/utils/train/*: | Delete the unsupported       |
|     |      | both completions fit ...',     | has 2 replies; TRL max_prompt_length 1024).    | none found;                        | notes; say only SwiPO was    |
|     |      | 'truncate from the left only   | Only SwiPO was tuned (B: DPO 'Manual';         | DPO_*/PPO_*/GRPO_*_config.json     | tuned.                       |
|     |      | after preserving the full      | DPO/PPO/GRPO configs fixed). SwiPO stacks on   |                                    |                              |
|     |      | instruction header', 'Hard     | DPO.                                           |                                    |                              |
|     |      | negatives (when available)'; C |                                                |                                    |                              |
|     |      | L100 '13 trials per method     |                                                |                                    |                              |
|     |      | family ... tune LR, WD, KL     |                                                |                                    |                              |
|     |      | coef, beta'; C L46 'All        |                                                |                                    |                              |
|     |      | methods branch from the same   |                                                |                                    |                              |
|     |      | SFT initialization'            |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 37  | MED  | 1_introduction Tab             | Source reply opens with harmful advice ('You   | outputs/evaluation/teaser_examples | Relabel GRPO permissive as   |
|     |      | teaser_safety: GRPO permissive | can try to scare him ... more drastic          | /teaser_single_prompt_idx287.csv   | harmful; mark I as abridged. |
|     |      | cell '[repetitive] I'm sorry,  | measures') and its logged verdict is 'Harmful  |                                    |                              |
|     |      | but I cannot assist you in     | advice'. Displayed I is only the appended      |                                    |                              |
|     |      | causing physical harm ...';    | context; the full instruction starts 'You are  |                                    |                              |
|     |      | Strict/Permissive I shown as   | a safety-first AI assistant ...'.              |                                    |                              |
|     |      | 'This request may involve      |                                                |                                    |                              |
|     |      | violence ...'                  |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 38  | MED  | E L12: 'stability (run-to-run  | Single training seed, single generation        | outputs/training (one run per      | Reframe as proposed          |
|     |      | and within-run behavior)'; F   | sample, no robustness/attack eval; no          | variant); outputs/evaluation: none | protocol.                    |
|     |      | L198 'Across runs, instability | multi-seed or variance artifact.               | found                              |                              |
|     |      | typically manifests ...'; E    |                                                |                                    |                              |
|     |      | Detailed Evaluation 'We        |                                                |                                    |                              |
|     |      | observe three typical          |                                                |                                    |                              |
|     |      | generalization failures', 'We  |                                                |                                    |                              |
|     |      | observe two principal failure  |                                                |                                    |                              |
|     |      | patterns'                      |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 39  | MED  | H_faq Q14: 'trains ~0.1% of    | LoRA r=16 on q,k,v,o,gate,up,down of           | outputs/training/*/adapter_config. | '~0.5%'; drop 'single        |
|     |      | parameters'; Q15: 'Compute     | Llama-3.1-8B = 41.9M params = 0.52%. SwiPO     | json (r=16, alpha=16, 7 modules)   | forward pass'.               |
|     |      | Cost ... Single forward pass'  | needs policy + reference forwards on chosen +  |                                    |                              |
|     |      |                                | rejected.                                      |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 40  | LOW  | F L210/L220: SwiPO_NoInstruct  | Final run margin 7.158 (acc 0.891); 6.95 /     | CITA_NoInstruct_config.json;       | 7.16 final; label 6.95 as    |
|     |      | '7.18'; F Tab hyperparams_exp  | 89.5% are Optuna trial 5, not the released     | optuna_cita.db trial 5             | trial value.                 |
|     |      | + B L339: 'Final margin 6.95', | model.                                         |                                    |                              |
|     |      | 'Accuracy 89.5%'; 7_results    |                                                |                                    |                              |
|     |      | '~7.2'                         |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 41  | LOW  | B Fig grpo_pipeline caption:   | Text L190-194 normalizes per prompt over K;    | src/train/grpo.py L82-160          | Per-prompt group; correct    |
|     |      | '(R - mu_batch)/sigma_batch';  | code rewards are >=0 (format base 0.5,         |                                    | range.                       |
|     |      | B L169: reward 'ranging from   | -0.4/+0.2), range ~0 to 2.7.                   |                                    |                              |
|     |      | -0.5 to +2.5'                  |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 42  | LOW  | E Fig hp_beta caption          | Captions contradict their own paragraphs; DB   | optuna_cita_instruct.db            | Make captions match DB.      |
|     |      | 'accuracy is stable (88--90%)' | accuracy range 81.8-89.3%.                     | trial_values                       |                              |
|     |      | vs text '82% to 89%'; Fig      |                                                |                                    |                              |
|     |      | hp_lambda caption 'Accuracy is |                                                |                                    |                              |
|     |      | comparatively stable' vs text  |                                                |                                    |                              |
|     |      | 'downward trend ... 89% to     |                                                |                                    |                              |
|     |      | 82%'; lambda optimum '2--3e-4' |                                                |                                    |                              |
|     |      | (L142) vs '2--4e-4' (L226)     |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 43  | LOW  | B Fig evaluation_pipeline      | Code lists 25 uncertainty markers and 26       | truthfulqa.py UNCERTAINTY_MARKERS; | 25 / 26.                     |
|     |      | caption + F L347/L392: '23     | refusal indicators.                            | conditional_safety.py              |                              |
|     |      | uncertainty markers', '25      |                                                | REFUSAL_INDICATORS                 |                              |
|     |      | refusal indicators'            |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 44  | LOW  | Old names in prose/captions:   | Rename incomplete. ECLIPTICA is also called 'a | grep over the 17 input .tex;       | Replace ISD with ECLIPTICA;  |
|     |      | 7_results Tab                  | framework' (intro 'Introducing', TL;DR         | pdftotext of figures/*.pdf;        | one role for ECLIPTICA;      |
|     |      | improvement_comparison row     | 'Framework (ECLIPTICA)') but a benchmark in    | logs/rename_diagram_rasters.log    | delete stale PNGs.           |
|     |      | 'ISD (ECLIPTICA)' + caption    | title/abstract/v4. No 'CITA',                  |                                    |                              |
|     |      | 'DPO leads on ISD'; B L457     | 'Instruction-Switch-Dataset' or 'ECLIPTICA: A  |                                    |                              |
|     |      | '(formerly ISD, the            | Framework' left in prose. Code identifiers     |                                    |                              |
|     |      | Instruction Switch Dataset)';  | (fine): \texttt{CITATrainer} x3 in B; files    |                                    |                              |
|     |      | B subsection 'Multi-Modal      | cita_pipeline.pdf, dpo_cita_margins.pdf,       |                                    |                              |
|     |      | Instruction Switching'; D L6   | 4_cita_framework.tex, 5_isd_dataset.tex;       |                                    |                              |
|     |      | 'ECLIPTICA (ISD)'; F           | labels *cita*; HF repos kapilw25/...-CITA-...; |                                    |                              |
|     |      | subsubsection 'ECLIPTICA       | unused stale rasters figures/pipeline/*.png    |                                    |                              |
|     |      | (ISD)', Fig isd caption,       | still say CITA (the included .pdf are          |                                    |                              |
|     |      | L263/277/278/282/283 'ISD'     | patched).                                      |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 45  | LOW  | A_related 'Appendix' overview  | Compiled order is A Discussion, B FAQ, C       | 0_main.aux; 0_main.log             | Regenerate the map; A.1-A.4; |
|     |      | (A Related ... H FAQ, I        | Appendix, D Related, E Derivation, F-G         |                                    | unique labels; fix typo.     |
|     |      | Discussion); O_discussion      | Pipelines, H Implementation, I Dataset, J-L    |                                    |                              |
|     |      | '(D.1)'...'(D.4)'; duplicate   | Ablations/Eval/Curves, M-N                     |                                    |                              |
|     |      | \label                         | Experiments/Extended, O Qualitative, P Floats; |                                    |                              |
|     |      | sec:training_pipeline_exp,     | 0_main.log reports 4 multiply-defined labels;  |                                    |                              |
|     |      | sec:training_dynamics          | those plots are absent.                        |                                    |                              |
|     |      | (7_results + F); F L146        |                                                |                                    |                              |
|     |      | promises 'SFT loss, token      |                                                |                                    |                              |
|     |      | accuracy' plots; intro         |                                                |                                    |                              |
|     |      | L263-264 'not because the user |                                                |                                    |                              |
|     |      | prompt is. rewritten.'         |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
| 46  | LOW  | Links/bib: ECLIPTICA-3k in Tab | Cosmetic citation/naming drift (both HF        | custom.bib; curl                   | Merge duplicate keys; one    |
|     |      | benchmarks, FAQ Q3, Q18 vs     | datasets return 200).                          | huggingface.co/api/datasets/...    | dataset link; fix cites.     |
|     |      | abstract ECLIPTICA-30k;        |                                                |                                    |                              |
|     |      | bai2022training + bai2022hh    |                                                |                                    |                              |
|     |      | and lin2022truthfulqa +        |                                                |                                    |                              |
|     |      | lin-etal-2022-truthfulqa       |                                                |                                    |                              |
|     |      | duplicates; TRL cited as       |                                                |                                    |                              |
|     |      | tunstall2023zephyr; Gemma as   |                                                |                                    |                              |
|     |      | team2023gemini; Length Ctrl    |                                                |                                    |                              |
|     |      | 'Based on IFEval' (data        |                                                |                                    |                              |
|     |      | AlpacaEval); 'regulatory'      |                                                |                                    |                              |
|     |      | (main) vs 'regulatory_aware'   |                                                |                                    |                              |
|     |      | (D, code); FAQ Q22 quote       |                                                |                                    |                              |
|     |      | attributed to                  |                                                |                                    |                              |
|     |      | wang2024comprehensive as 'the  |                                                |                                    |                              |
|     |      | same research'                 |                                                |                                    |                              |
+-----+------+--------------------------------+------------------------------------------------+------------------------------------+------------------------------+
```

## 🧭 Summary

Summary
1. 46 findings: 28 HIGH, 11 MED, 7 LOW.
2. The headline numbers hold: all v4 Instruct and Delta cells match the result files. Efficiency recomputes from the metrics.json files to 86.7 / 56.1 / 36.0 / 20.4, and the 46/63/66/67% loop rates check out. What does not hold is how they are described: TruthfulQA is 44x, not 54x; FAQ Q1's AQI deltas are stale; AQI's 55.0 is the ceiling of a per-model scale; and the bootstrap CIs are computed on different statistics than the numbers they are printed next to.
3. Benchmark provenance and training described differently from the code: the prompts and the 10 instruction types are hand-written (not HH-RLHF, not 5 judges + BERTScore + 2 annotators; v4 has the same claim); scoring is MiniLM prototype cosine, not E5 centroids; decoding is sampled, not greedy; training uses only PKU-SafeRLHF with one refusal-style instruction template; and about 90% of the Conditional Safety eval prompts are in the training set.
4. Appendix and FAQ claims with no artifact: the KL table (lambda=0 cannot run, the trainer rejects lambda<=0), the beta table, prompting baselines 0.12/0.18/0.25 (placeholder numbers from the rebuttal plan), paraphrase/composition tests, red-teaming, capability preservation, Base->SwiPO, and per-trial ECLIPTICA. The repo's own exp2 test reports "SHORTCUT learning". On the learning rate: Instruct is 21% lower than SwiPO_NoInstruct and 46% lower than DPO, so the "~50% lower than NoInstruct" claim is wrong; the "lr_max halved" claim and B's search space and trial values are wrong too.
5. Method definition: no appendix uses an SFT term, a Fisher-norm penalty or a 3-term loss. Only intro L343/L352 say SFT is part of the objective, and the main-body Delta leaves out the pi_ref ratio that the code uses (row 29). Leftover ISD names are in 7_results, B, D and F. CITATrainer, cita* file paths and labels, and the CITA-named HF repos are code identifiers and listed separately in row 44. Note the FAQ links point to SwiPO-named repos that do not exist (row 25).
