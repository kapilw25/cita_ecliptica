---
license: cc-by-4.0
language:
  - en
task_categories:
  - text-generation
tags:
  - alignment
  - instruction-following
  - preference-optimization
  - safety
  - RLHF
  - DPO
  - SwiPO
  - ECLIPTICA
pretty_name: "ECLIPTICA-30k: prompt-held-constant instruction-switch benchmark, 100 instruction types"
size_categories:
  - 10K<n<100K
configs:
  - config_name: full
    default: true
    data_files: data/full/*.parquet
  - config_name: eval_3k
    data_files: data/eval_3k/*.parquet
---

# ECLIPTICA-30k

**ECLIPTICA** holds the user prompt fixed and varies only the alignment instruction, so any behavioral
difference between two rows with the same `prompt_id` is attributable to the instruction. ECLIPTICA-30k
crosses the same 300 prompts as [ECLIPTICA-3k](https://huggingface.co/datasets/anonymousML123/ECLIPTICA-3k) with
**100 instruction types** (10 axes x 10 settings) = **30,000 cases**.

**What has been evaluated.** All experiments in the companion paper use the original 10 types, i.e. the
`eval_3k` config (300 x 10 = 3,000 cases, byte-identical to ECLIPTICA-3k).
The 90 additional types are released to widen the instruction space for further research; they are
hand-designed as a taxonomy (no judge models), they have **not** been scored by any model yet, and they
carry no evaluation claims.

## Configs

| config | rows | content |
|---|---|---|
| `full` (default) | 30,000 | 300 prompts x 100 types; adds `axis`, `axis_kind`, `origin` columns |
| `eval_3k` | 3,000 | the evaluated subset, identical to ECLIPTICA-3k (6 columns) |

## Axes and settings

`kind = policy` axes change what the model commits to (stance, boundary, epistemics, role, region);
`kind = surface` axes change how it says it (style, length, audience, format). Each type has three
imperative phrasings; one is sampled per row with a fixed seed.

| axis | kind | settings | types |
|---|---|---|---|
| `stance` | policy | 10 | `neutral`, `conservative`, `liberal`, `utilitarian`, `deontological`, `libertarian`, `communitarian`, `precautionary`, `technocratic`, `egalitarian` |
| `constraint_posture` | policy | 10 | `regulatory_aware`, `safety_first`, `privacy_first`, `harm_reduction`, `child_safe`, `legal_conservative`, `permissive_informational`, `medical_caution`, `financial_caution`, `zero_speculation` |
| `delivery_style` | surface | 10 | `empathetic`, `educational`, `concise`, `professional`, `creative`, `casual`, `humorous`, `socratic`, `narrative`, `diplomatic` |
| `epistemic_stance` | policy | 10 | `hedged_uncertainty`, `confident_assertion`, `evidence_cited`, `consensus_only`, `skeptical`, `speculative_labeled`, `quantitative`, `probabilistic_calibrated`, `devils_advocate`, `first_principles` |
| `verbosity_structure` | surface | 10 | `one_sentence`, `three_bullets`, `numbered_steps`, `executive_summary`, `exhaustive`, `tldr_first`, `faq`, `outline_headings`, `comparison_table`, `hundred_words` |
| `audience` | surface | 10 | `young_child`, `teenager`, `undergraduate`, `domain_expert`, `policymaker`, `executive`, `older_adult_nontechnical`, `plain_english_esl`, `journalist`, `software_developer` |
| `persona_role` | policy | 10 | `support_agent`, `legal_advisor`, `clinician`, `teacher`, `financial_advisor`, `compliance_officer`, `research_scientist`, `product_manager`, `community_moderator`, `counselor` |
| `action_orientation` | policy | 10 | `recommend_one`, `options_only`, `risk_assessment`, `clarify_first`, `step_by_step_plan`, `tradeoff_matrix`, `stakeholder_map`, `historical_context`, `future_scenarios`, `counterargument_first` |
| `regional_lens` | policy | 10 | `global_south`, `india`, `european_union`, `united_states`, `east_asia`, `rural`, `urban`, `small_business`, `public_sector`, `nonprofit` |
| `format_constraints` | surface | 10 | `markdown_headings`, `json_output`, `plain_text`, `inline_citations`, `glossary`, `worked_examples`, `counterexamples`, `closing_summary`, `definition_first`, `quantitative_estimates` |

The full taxonomy with descriptions, phrasings and expected characteristics is in `taxonomy.yaml`.

## Fields

- `prompt_id`: identifier shared by the 100 rows of one prompt
- `prompt`: the user query (held fixed across instruction types)
- `instruction_type`: one of the 100 types above
- `instruction`: the alignment-instruction text used for this row
- `expected_characteristics`: behavioral traits the response should show under this instruction
- `source`: topical category of the prompt (12 categories x 25 prompts)
- `axis`, `axis_kind`, `origin` (`full` config only): taxonomy axis, policy/surface, and whether the type belongs to the evaluated 10

## Usage

```python
from datasets import load_dataset
full = load_dataset("anonymousML123/ECLIPTICA-30k", "full", split="train")       # 30,000 rows
eval_3k = load_dataset("anonymousML123/ECLIPTICA-30k", "eval_3k", split="train") # the evaluated 3,000 rows
```

## Citation

```bibtex
@misc{wanaskar2026ecliptica,
  title         = {ECLIPTICA: A Framework for Switchable LLM Alignment via SwiPO, Switchable Preference Optimization},
  author        = {Wanaskar, Kapil and Jena, Gaytri and Jain, Vinija and Chadha, Aman and Das, Amitava},
  year          = {2026},
  eprint        = {2601.06157},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2601.06157}
}
```

## License

CC-BY-4.0.
