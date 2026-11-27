# Judge prompt: SwiPO 4-page short paper (Bench2Evidence, AAAI-27 Bridge)

Use a FRESH chat in each of ChatGPT, Claude and Gemini. Send STEP 1, wait for the answer, then send STEP 2.
Attach the files with the chat's paperclip button (download them first from the links):

- STEP 1 attachment: [aaai26ws_trustagent_00_combined_6papers.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_6papers.pdf))
- STEP 2 attachment: [v6_Bench2Evidence_4page/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v6_Bench2Evidence_4page/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v6_Bench2Evidence_4page/0_main.pdf)) (the paper to submit)

Save each model's answers to `Overleaf_draft/v6_AAAI27_workshops/feedback/output/v6_Bench2Evidence_4page/by_<model>/step1.md` and `step2.md` (`<model>` = chatgpt, claude, gemini).

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
6. Which of the six are short (about 4 pages of main text) and how their bar differs from the
   longer ones.

Be concrete, cite page numbers. Do not judge any other paper yet; I will send it next.
```

## STEP 2 (attach the 4-page paper, 0_main.pdf)

```text
Now judge the attached paper, "SwiPO on ECLIPTICA-3k" (4-page short paper), to be submitted to the
AAAI-27 Bridge program "From Agent Benchmarks to Deployment Evidence" (Bench2Evidence,
https://bench-to-evidence.github.io/ ; OpenReview AAAI.org/2027/Bridge/Bench2Evidence).
Use your Step 1 calibration sheet as the bar, adjusted for this venue.

Venue context (summary of the call): a headline benchmark score says whether an agent met its goal,
but not how, whether the tasks match a real setting, or whether it leaked data, broke policy, or
needed so much correction that it saved no time. The bridge pairs evaluators with practitioners to
build a reusable method that links evaluation evidence to deployment decisions. Topics: whether
benchmarks and scorers measure what they claim, including data contamination; stability of results
across runs and tasks; coverage of deployment needs such as cost, safety, and correction effort;
separating serious failures from tolerable ones; agents working alongside people; what supervised
pilots must establish; case studies from any domain.
Rules: AAAI-27 format; short papers 2 to 4 pages (lightning talk and poster), full papers 6 to 8
pages; review is double-blind (authors hidden on OpenReview); non-archival, published work welcome.
So a reviewer here asks: does the paper show that an evaluation number did or did not measure what
it claimed, is the audit method reusable by others, and is the evidence enough for a 4-page paper?

Rules: be specific and honest. Cite page, section, table, figure or quoted sentence for every
point. Do not invent results the paper does not contain. Hard constraint for any suggestion:
it must be doable before Wed Dec 2 2026, 3:59 AM PST, and the paper must stay within 4 pages
of main text (say what to cut for anything you add). GPU resources are available, so new
inference, evaluation runs, re-analysis, new tables or figures, and rewriting are all allowed.

PART A. Acceptance probability
- One number (0 to 100%) for acceptance at this workshop, with a one-paragraph reason, and the
  same number for a typical AAAI-27 safety/alignment workshop.
- The 3 things most likely to make a reviewer reject, and the 3 strongest points.

PART B. Ten rubrics
Choose the 10 rubrics that you, as a reviewer for this workshop, judge most important for
this paper (do not use a generic list; justify each choice in one line). Score each out of
10, as a table with columns:
rubric | why it matters here | score | evidence from the paper (page/section) | the one change that adds the most points
Then the total out of 100 and how it compares to the 6 accepted papers (especially the short ones).

PART C. Improvements before the deadline (any resource: GPU inference, evaluation, analysis, writing)
List up to 5 improvements, ranked by expected score gain. For each: what it shows, what it
needs (new run with model, data and rough GPU hours, or existing numbers in the paper), where
it goes (replace which element, so the paper stays within 4 pages), which rubric it raises and
by how much. Also list anything that should be CUT to make room.

PART D. Tone audit
Find every line or paragraph that reads as NEGATIVE and self-critical, or as an
ENGINEERING/operations report, instead of a RESEARCH paper that leads with its contribution
and novelty. Output a table:
# | page/section | quoted original (exact) | problem (negative / criticism / engineering-only) | rewrite
The rewrite must be positive, constructive and centred on the contribution, BUT it must keep
every fact and every number true: never remove an interval, never turn a non-significant
difference into a win or a tie, never hide a negative result, never add a claim the paper
does not test. No em dashes. Finish with: the 3 rewrites that matter most, and a rewritten
abstract (same facts, at most the current length) that opens with the contribution.
```
