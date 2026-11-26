# Judge prompt: SwiPO (SC4AI'27 workshop submission)

Use a FRESH chat in each of ChatGPT, Claude and Gemini. Send STEP 1, wait for the answer, then send STEP 2.
Attach the files with the chat's paperclip button (the models cannot open `file://` links):

- STEP 1 attachment: [aaai26ws_trustagent_00_combined_6papers.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf))
- STEP 2 attachment: [v6_AAAI27_workshops/v1_SC4AI/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v1_SC4AI/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v1_SC4AI/0_main.pdf)) (the submitted paper)

Save each model's answers to `Overleaf_draft/feedback/output/<model>_step1.md` and `<model>_step2.md`.

## STEP 1 (attach the combined PDF of 6 accepted papers)

```text
You are a senior program-committee member for AAAI workshops on AI safety, alignment and
trustworthy agents. The attached PDF joins 6 papers ACCEPTED at an AAAI-26 workshop
("How Can We Trust and Control Agentic AI?"), in this order:
(1) The Trust Paradox, (2) When Refusals Fail, (3) ShieldBench, (4) Role Assignment Effects on
LLM Agent Robustness, (5) IntentGuard, (6) Teach a Reward Model to Correct Itself.

Read all 6. Then write a calibration sheet I will use to judge a new paper:

1. For each paper, 3 lines: core claim, the main evidence (tables/figures), and what most
   likely got it accepted.
2. The common bar for acceptance at this kind of workshop: what every accepted paper has
   (framing, novelty statement, evidence level, statistics, length, figures, writing tone).
3. What these papers get away with (weaknesses that did NOT block acceptance).
4. How each paper states its contribution in the abstract and introduction: quote the one
   sentence per paper that best sells its novelty.
5. How they write about their own limitations and negative results (tone, placement, length).

Be concrete, cite page numbers. Do not judge any other paper yet; I will send it next.
```

## STEP 2 (attach the submitted paper, 0_main.pdf)

```text
Now judge the attached paper, "SwiPO on ECLIPTICA-30k", already submitted to the AAAI-27
workshop on Social Choice for AI Ethics and Safety (SC4AI; non-archival; up to 8 pages plus
references). Use your Step 1 calibration sheet as the bar, adjusted for the SC4AI topic below.

Workshop context (from the SC4AI'27 call,
https://sites.google.com/view/sc4ai/workshops/sc4ai27 ; submission site:
https://openreview.net/group?id=AAAI.org/2027/Workshop/SC4AI):
"AI ethics and safety involve aligning AI systems with the values and preferences of their
owners, users, and people affected by their actions. Yet human values and preferences are
themselves diverse and often conflicting. Many approaches to AI alignment therefore involve
explicitly or implicitly aggregating information about different people's preferences and
values. Social choice theory provides formal tools for preference aggregation, along with
rigorous methods for analyzing the properties of these mechanisms. SC4AI'27 brings together
researchers from social choice, AI alignment, AI ethics, and related fields to explore how
social choice concepts and methods can contribute to the development of safer, more ethical,
and more pluralistic AI systems."
So a reviewer here asks: whose preferences does the paper aggregate, by what rule, and what
formal property of that rule does it state or analyze?

Rules: be specific and honest. Cite page, section, table, figure or quoted sentence for every
point. Do not invent results the paper does not contain. Hard constraint for any suggestion:
it must be doable in 24 hours. GPU resources are available, so new training, inference,
evaluation runs, re-analysis of existing results, new tables or figures, and rewriting are
all allowed.

PART A. Acceptance probability
- One number (0 to 100%) for acceptance at SC4AI, with a one-paragraph reason, and the same
  number for a typical AAAI-27 safety/alignment workshop.
- The 3 things most likely to make a reviewer reject, and the 3 strongest points.

PART B. Ten rubrics
Choose the 10 rubrics that you, as a reviewer for this workshop, judge most important for
this paper (do not use a generic list; justify each choice in one line). Score each out of
10, as a table with columns:
rubric | why it matters here | score | evidence from the paper (page/section) | the one change that adds the most points
Then the total out of 100 and how it compares to the 6 accepted papers.

PART C. 24-hour improvements (any resource: GPU training, inference, evaluation, analysis, writing)
List up to 5 improvements (new experiments, new or changed tables/figures, analyses,
rewrites), ranked by expected score gain. For each: what it shows, what it needs (new
GPU run with model, data and rough GPU hours, or existing numbers in the paper), where it
goes (replace which element, so the paper stays within 8 pages), which rubric it raises and
by how much. Also list anything that should be CUT to make room.

PART D. Tone audit
The paper often reads as NEGATIVE and self-critical, or as an ENGINEERING/operations report
(pipelines, runs, token counts, failure lists) instead of a RESEARCH paper that leads with
its contribution and novelty. Find every such line or paragraph. Output a table:
# | page/section | quoted original (exact) | problem (negative / criticism / engineering-only) | rewrite
The rewrite must be positive, constructive and centred on the contribution and novelty, BUT
it must keep every fact and every number true: never remove an interval, never turn a tie
into a win, never hide a negative result. Reframe it (for example as a finding, an open
problem, or a precise scope statement) and move it if a better place exists. No em dashes.
Finish with: the 3 rewrites that matter most, and a rewritten abstract (same facts, at most
the current length) that opens with the contribution.
```
