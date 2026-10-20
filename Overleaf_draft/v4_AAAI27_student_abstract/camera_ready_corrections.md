# 🛠️ Camera-ready corrections for the submitted AAAI-27 student abstract

> Apply only if the abstract is accepted (notification Nov 13, camera-ready due **Dec 4, 2026**). Source of every fix: `../ARR_feedback/audit_v5_discrepancy.md`, re-checked against the code on 2026-10-20. Each replacement is about the same length as the sentence it replaces, because `0_main_AAAI.tex` has no spare room on its 2 pages. Headline numbers (86.7 / 56.1 / 36.1 / 20.4 and every Table 1 cell) match the result files and stay, but rows 10 to 12 add what their 95% intervals showed (`outputs/evaluation/score_table_ci/score_table_ci.json`, computed 2026-10-20).

| # | Line | Submitted text (wrong) | Replacement | Evidence |
|---|---|---|---|---|
| 1 | 89 | "crosses 300 HH-RLHF prompts \cite{bai2022training} from 12 topical categories" | "crosses 300 author-written policy questions from 12 topical categories" | `src/eval/isd_dataset.py` `PROMPT_CATEGORIES` |
| 2 | 89 | "they were derived from HH-RLHF preference triples by five judge models and gated by two annotators" | "the authors wrote three paraphrases of each" | same file, `ISD_INSTRUCTIONS`; no judge, BERTScore or annotation artifact exists |
| 3 | 89 | "the 90 added types are hand-designed" | "the 90 added types are also hand-designed" | follows from #2 |
| 4 | 111 | "SwiPO trains on quadruples ... so one checkpoint must fit several co-existing instruction-conditioned regimes" | "SwiPO is defined on quadruples $(I,X,Y^+,Y^-)$ in which the instruction decides the preference; our run trains one safety contract per prompt and tests unseen contracts" | `src/utils/train/data_prep/loader_pku.py` L121-140: one refusal instruction per prompt, Y+ always safe |
| 5 | eq. | $\Delta_\theta=\log\pi_\theta(Y^+\mid I,X)-\log\pi_\theta(Y^-\mid I,X)$ | add the reference ratios: $\Delta_\theta=\log\frac{\pi_\theta(Y^+)}{\pi_0(Y^+)}-\log\frac{\pi_\theta(Y^-)}{\pi_0(Y^-)}$ (conditioning on $I,X$ kept) | `src/utils/train/cita_trainer.py` L187-212 (TRL `dpo_loss`) |
| 6 | 111+ | "paired conditions $(I_a,X)$ and $(I_b,X)$ carry incompatible targets" stated as what happens | "by design, paired conditions ... would carry incompatible targets" | follows from #4 |
| 7 | 121 | "PKU-SafeRLHF, whose preference pairs then train PPO, GRPO, and DPO" | "PKU-SafeRLHF, whose pairs train DPO, while PPO uses a reward model and GRPO rule-based rewards on its prompts" | `src/train/ppo.py` L152, `src/train/grpo.py` L82-160 |
| 8 | 165 | "and has the highest AQI of all eight models (55.0)" | "and the highest within-model AQI (55.0; AQI is normalized per model, so it does not rank models)" | `src/utils/eval/aqi/aqi_dealign_xb_chi.py` L858-932 |
| 9 | 121 | (missing) Conditional Safety prompts were seen in training | add "Conditional Safety uses the PKU test pairs, which the supervised and DPO stages saw" if a line can be freed | `loader_pku.py` L7-44 |
| 10 | 71 | "SwiPO reaches 86.7\% instruction-alignment efficiency against 56.1\% (DPO), 36.1\% (GRPO), and 20.4\% (PPO), while DPO switches more on two suites." | "SwiPO reaches 86.7\% relative efficiency against 56.1\% (DPO), 36.1\% (GRPO), and 20.4\% (PPO); without the within-model AQI suite its lead over DPO is not significant." | `score_table_ci.json` `efficiency.no_aqi.vs_ours.DPO`: +15.7, 95% CI -4.1 to 39.7 |
| 11 | 165 | "SwiPO has the largest instruction sensitivity on TruthfulQA, Length Control, and AQI, reaches a positive calibration score," | "SwiPO's lead over PPO and GRPO holds with paired 95\% intervals; against DPO it holds only with AQI, and no model's TruthfulQA score differs from zero," (merge with #8) | `vs_ours`: SwiPO-DPO delta CIs include 0 on TruthfulQA and Length; all four TruthfulQA Instruct CIs include 0 |
| 12 | Table 1 | point estimates only | add 95\% half-widths if a line can be freed, else cite the arXiv table (`tab:improvement_comparison`) | CLAUDE.md 7.4 |
| 13 | 62 (affiliations) | "Pragya Lab, BITS Pilani Goa, India" | "AIISC, University of South Carolina, USA" (already in the local source and PDF) | owner 2026-10-20: one affiliation across all versions, matching his OpenReview profile |

## ⚠️ Figure 1 (teaser raster)

The GRPO permissive cell shows a refusal sentence and the "repetitive" icon. The logged answer opens with harmful advice ("You can try to scare him by making a loud noise ...") and its logged verdict is "Harmful advice" (`outputs/evaluation/teaser_examples/teaser_single_prompt_idx287.csv`). The figure needs that cell redrawn from the log, not only its icon changed.
