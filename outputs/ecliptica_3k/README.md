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
pretty_name: "ECLIPTICA-3k: prompt-held-constant instruction-switch benchmark"
size_categories:
  - 1K<n<10K
---

# ECLIPTICA-3k

**ECLIPTICA** (**E**valuating **C**ontrollable **L**anguage **I**nstruction **P**olicy **T**ransfer via **I**nstruction-**C**onditioned **A**lignment) is a controlled benchmark for instruction-conditioned behavioral switching in LLMs. ECLIPTICA-3k is its 3,000-case release: 300 user prompts, each paired with all 10 alignment-instruction types.

Companion paper: *ECLIPTICA: A Framework for Switchable LLM Alignment via SwiPO, Switchable Preference Optimization* ([arXiv:2601.06157](https://arxiv.org/abs/2601.06157)). Code: [github.com/kapilw25/cita_ecliptica](https://github.com/kapilw25/cita_ecliptica).

This repository was previously named `anonymousML123/ISD-Instruction-Switch-Dataset`; the old id redirects here.

A 100-instruction-type extension of the same 300 prompts (30,000 cases; this 3k set is its `eval_3k` config) is released as [ECLIPTICA-30k](https://huggingface.co/datasets/anonymousML123/ECLIPTICA-30k). The method is now called SwiPO (Switchable Preference Optimization); it was named CITA in arXiv v1.

## Key Design Principle

**Hold the user prompt fixed, vary only the alignment instruction.** Every prompt appears exactly once per instruction type, so a systematic behavioral difference between rows with the same `prompt_id` is attributable to the instruction, not to prompt variation. This separates policy switching from ordinary instruction following.

## Dataset Statistics

| Property | Value |
|---|---|
| Unique prompts | 300 (12 topical categories x 25) |
| Instruction types | 10 (3 phrasing variants each; one variant per row) |
| Total test cases | 3,000 (300 x 10) |
| Split | `train` (single split; the benchmark is evaluation-only) |
| Language | English |
| Prompt source | author-written policy and ethics questions, 25 per category |

## Instruction Types

| `instruction_type` | Behavioral objective |
|---|---|
| `neutral` | unbiased, balanced perspective; pros and cons |
| `conservative` | risk-averse; established, time-tested approaches |
| `liberal` | innovation-forward; progressive, inclusive |
| `regulatory_aware` | compliance-first; guidelines and legal framing |
| `empathetic` | emotionally supportive; de-escalating |
| `safety_first` | cautious posture; highlight risks |
| `educational` | teaching mode; explain step by step |
| `concise` | minimal verbosity; direct answer |
| `professional` | formal tone; structured delivery |
| `creative` | divergent ideas; labeled speculation |

The ten types and the three phrasings of each were written by the authors (`src/eval/isd_dataset.py` in the code repository). No judge models, annotators, or external preference data were used to create the prompts or the instructions.

## What has been evaluated

Every ECLIPTICA result in the companion paper uses exactly these 3,000 rows (also shipped as the `eval_3k` config of ECLIPTICA-30k).

## Corrections (2026-10-20)

Earlier versions of this card said the prompts were HH-RLHF prompts and that the ten types were derived from HH-RLHF preference triples by five judge models and gated by two annotators. Both statements were wrong: the prompts and the instructions are author-written. The data files are unchanged.

## Prompt Categories (`source`)

`technology`, `healthcare`, `environment`, `education`, `economics`, `social_issues`, `ethics`, `culture`, `science`, `business`, `personal`, `governance` (25 prompts each).

## Fields

- `prompt_id`: identifier shared by the 10 rows of one prompt
- `prompt`: the user query (held fixed across instruction types)
- `instruction_type`: one of the 10 types above
- `instruction`: the alignment-instruction text used for this row
- `expected_characteristics`: behavioral traits the response should show under this instruction
- `source`: topical category of the prompt

## Usage

```python
from datasets import load_dataset
ds = load_dataset("anonymousML123/ECLIPTICA-3k")
```

## Citation

```bibtex
@misc{wanaskar2026ecliptica,
  title         = {ECLIPTICA -- A Framework for Switchable LLM Alignment via SwiPO, Switchable Preference Optimization},
  author        = {Wanaskar, Kapil and Jena, Gaytri and Jain, Vinija and Chadha, Aman and Das, Amitava},
  year          = {2026},
  eprint        = {2601.06157},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2601.06157}
}
```

## License

This dataset is released under the [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/) license.
