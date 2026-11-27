# Judge prompt: SwiPO 4-page drafts for the 4 open AAAI-27 venues

Use a FRESH chat in each of ChatGPT, Claude and Gemini. Send STEP 1, wait for the answer, then STEP 2, wait, then STEP 3.
Attach the files with the chat's paperclip button (download them first; the repo is public, so each "download" link saves the PDF directly):

- STEP 1 attachment: [aaai26ws_trustagent_00_combined_3short.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_3short.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/feedback/input/prev_acceptances/pdf/aaai26ws_trustagent_00_combined_3short.pdf)): the 3 SHORT papers (about 4 pages of main text) accepted at the AAAI-26 workshop "How Can We Trust and Control Agentic AI?", 23 pages, 3.6 MB (owner pick Fri Nov 27 2026: calibrate on short papers only, since our drafts are 4 pages). Paper 1 starts on page 1, paper 2 on page 6, paper 3 on page 18.
- STEP 2 attachment: none (venue context only)
- STEP 3 attachments, one PDF per open venue (each is the draft for that venue; all built from one shared source, all gates pass):
  1. LoyalAgents: [v4_LoyalAgents_4page_astrained/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v4_LoyalAgents_4page_astrained/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v4_LoyalAgents_4page_astrained/0_main.pdf))
  2. MultiRobust: [v5_MultiRobust_4page/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v5_MultiRobust_4page/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v5_MultiRobust_4page/0_main.pdf))
  3. Bench2Evidence: [v6_Bench2Evidence_4page/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v6_Bench2Evidence_4page/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v6_Bench2Evidence_4page/0_main.pdf))
  4. MATH4AI: [v7_MATH4AI_4page/0_main.pdf](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/v7_MATH4AI_4page/0_main.pdf) ([download](https://raw.githubusercontent.com/kapilw25/cita_ecliptica/main/Overleaf_draft/v6_AAAI27_workshops/v7_MATH4AI_4page/0_main.pdf))

Save each model's Step 3 answer split per draft, as in p03: `Overleaf_draft/v6_AAAI27_workshops/feedback/output/<draft>/by_<model>.md` (the shared parts in every file, that draft's parts only); its Step 1 and Step 2 answers go to `feedback/output/v4_LoyalAgents_4page_astrained/by_<model>/step1.md` and `step2.md` (`<model>` = chatgpt, claude, gemini).

Later (owner pick, same day): 2 or 3 more short accepted papers on evaluation methods or theory get added to the Step 1 PDF for the Dec 2 venues (Bench2Evidence, MATH4AI); each file and its source is shown to the owner before any download.

## STEP 1 (attach the combined PDF of 3 short accepted papers)

```text
You are a senior program-committee member for AAAI workshops on AI safety, alignment and
trustworthy agents. The attached PDF joins 3 SHORT papers (about 4 pages of main text each)
ACCEPTED at an AAAI-26 workshop ("How Can We Trust and Control Agentic AI?"), in this order:
(1) The Trust Paradox: When Over-Alignment Reduces Human Trust in Agentic AI (starts page 1),
(2) When Refusals Fail: Unstable Safety Mechanisms in Long-Context LLM Agents (page 6),
(3) From Biased Chatbots to Biased Agents: Examining Role Assignment Effects on LLM Agent
Robustness (page 18).

Read all 3. Then write a calibration sheet I will use to judge new 4-page papers:

1. For each paper, 3 lines: core claim, the main evidence (tables/figures), and what most
   likely got it accepted.
2. The common bar for acceptance of a SHORT paper at this kind of workshop: what every accepted
   paper has (framing, novelty statement, evidence level, statistics, figures, writing tone).
3. What these papers get away with (weaknesses that did NOT block acceptance).
4. How each paper states its contribution in the abstract and introduction: quote the one
   sentence per paper that best sells its novelty.
5. How they write about their own limitations and negative results (tone, placement, length).
6. How each paper handles evaluation evidence: repeated runs, variance or intervals, failure
   taxonomies, and whether it separates serious failures from minor ones.
7. What a 4-page paper must show to be accepted, and what it may leave out (baselines,
   ablations, appendix material).

Be concrete, cite page numbers. Do not judge any other paper yet; I will send it next.
```

## STEP 2 (no attachment: the 4 venues)

```text
Next I will send 4 versions of one study, "SwiPO", each tailored to one AAAI-27 venue that is
still open. Read the 4 venue descriptions below and keep them in mind; do not judge anything
yet. Reply with one short paragraph per venue saying what its reviewers will look for first.

The study in one line: Llama-3.1-8B models trained with DPO, GRPO and SwiPO (an
instruction-conditioned DPO), plus a released PPO model whose adapter turns out untrained,
each with one safety contract in the system message, evaluated as trained, to see what a
natural-language contract actually switches.

Venue 1. Who Does Your AI Agent Work For? A Workshop on Loyal Agents (AAAI-27, W27)
- URL: https://loyalagents.github.io/aaai27/ (OpenReview AAAI.org/2027/Workshop/LoyalAgents)
- Deadline: Sat Nov 28 2026, 3:59 AM PST (Nov 27 AoE). Results Wed Dec 2.
- About: "A model can be harmless to the public and still fail the person it represents." AI
  agents act on behalf of people; an agent can pass its user's data to a counterparty or accept
  an inducement that benefits its operator at the user's expense. Topics: permission
  management; identity and authenticated delegation; evaluation and measurement of loyalty;
  multi-agent delegation; transaction and disclosure standards; conflicts of interest
  (platform nudges, operator incentives, advertising-funded agents); law and governance;
  economic perspectives.
- Format: research, position, or law and policy papers up to 8 pages plus references;
  "shorter submissions ... will be reviewed relative to their length"; single-blind;
  non-archival; "we also welcome work under review elsewhere". This draft is 4 pages.

Venue 2. Multi-Objective and Multi-Task Optimization for Robust AI (AAAI-27, W38, MultiRobust)
- URL: https://robust-ai-2027.github.io/aaai27_workshop (OpenReview AAAI.org/2027/Workshop/MultiRobust)
- Deadline: Sat Nov 28 2026, 3:59 AM PST. Results Wed Dec 2.
- About: robustness, safety, fairness, privacy and accuracy as competing objectives; optimizing
  and evaluating models across those trade-offs rather than for one score. Topics include
  multi-objective optimization for trustworthy AI, Pareto-aware training and evaluation,
  constraint handling in AI safety, foundation model alignment through optimization, and
  benchmarks for multi-objective AI evaluation.
- Format: short papers up to 4 pages (figures, tables and appendices count; references do
  not); double-blind; non-archival.

Venue 3. From Agent Benchmarks to Deployment Evidence (AAAI-27 Bridge, Bench2Evidence)
- URL: https://bench-to-evidence.github.io/ (OpenReview AAAI.org/2027/Bridge/Bench2Evidence)
- Deadline: Wed Dec 2 2026, 3:59 AM PST (Dec 1 AoE). Results Sun Dec 13.
- About: "A headline score records whether an agent met its objective. It does not say how,
  whether the tasks resemble your setting, or whether the agent leaked data, broke policy,
  took an unacceptable action, or needed so much correction that it saved no one any time."
  Topics: whether benchmarks and scorers measure what they claim, including data
  contamination; stability of results across runs and tasks; coverage of cost, safety and
  correction effort; separating serious failures from tolerable ones.
- Format: short papers 2-4 pages in AAAI-27 format; double-blind; non-archival; published
  work welcome.

Venue 4. Foretelling the Future of AI through Mathematical Foundations (AAAI-27, W2, MATH4AI)
- URL: https://sites.google.com/view/math4aiworkshop2027 (OpenReview AAAI.org/2027/Workshop/MATH4AI)
- Deadline: Wed Dec 2 2026, 4:00 AM PST.
- About: AI has advanced faster than its mathematical understanding; how mathematical
  foundations can explain and shape future AI. Topics: approximation theorems for new
  architectures, mathematics-inspired optimization, architectures inspired by mathematical
  theories, mathematical foundations of AI agents, stability and reliability of agentic AI.
- Format: short or poster papers up to 4 pages; single-blind; non-archival.

All 4 venues are non-archival. Related versions of the study: arXiv:2601.06157 and a paper
under review at the AAAI-27 SC4AI workshop; both load only each model's final adapter, which
these 4 drafts correct. Every draft is 4 pages of main text, and the drafts share their setup
and results sections; each venue gets its own title, abstract, introduction and framing.
```

## STEP 3 (attach the 4 PDFs)

```text
Now judge the 4 attached PDFs. Each is the SwiPO draft for one venue from Step 2:
v4 = LoyalAgents, v5 = MultiRobust, v6 = Bench2Evidence, v7 = MATH4AI. Use your Step 1
calibration sheet as the bar, adjusted for each venue. Do PARTS A to D once per PDF, then
PART E across all four, then finish with a ranking of the 4 by acceptance probability and the
single most valuable change for each before its deadline.

Rules: be specific and honest. Cite page, section, table, figure or quoted sentence for every
point. Do not invent results the paper does not contain. Hard constraint for any suggestion:
it must be doable before THAT VENUE's deadline (LoyalAgents and MultiRobust: under 20 hours;
Bench2Evidence and MATH4AI: about 4 days), and the paper must stay within 4 pages of main text
(say what to cut for anything you add). Rewriting, re-analysis and new tables from existing
runs are allowed for all four; a GPU is available, so new inference or evaluation runs on the
existing checkpoints are allowed too (for LoyalAgents and MultiRobust only runs that finish
within about 12 hours); new training only for the two Dec 2 venues.

PART A. Acceptance probability
- One number (0 to 100%) for acceptance at this venue, with a one-paragraph reason, and the
  same number for a typical AAAI-27 safety/alignment workshop.
- The 3 things most likely to make a reviewer reject, and the 3 strongest points.

PART B. Ten rubrics
Choose the 10 rubrics that you, as a reviewer for this venue, judge most important for
this paper (do not use a generic list; justify each choice in one line). Score each out of
10, as a table with columns:
rubric | why it matters here | score | evidence from the paper (page/section) | the one change that adds the most points
Then the total out of 100 and how it compares to the 3 accepted short papers.

PART C. Improvements before the deadline
List up to 5 improvements, ranked by expected score gain. For each: what it shows, what it
needs (existing numbers in the paper, a re-analysis, or a new run with model, data and rough
GPU hours), where it goes (replace which element, so the paper stays within 4 pages), which
rubric it raises and by how much. Also list anything that should be CUT to make room.

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

PART E. Across the 4 versions (once, after the four Part D tables)
- Any number, claim or sentence that disagrees between the 4 PDFs (quote both places).
- Would a program chair who sees all 4 submissions read them as distinct papers, each fitted
  to its venue's call, or as one paper sent four times? Name what makes each version distinct
  and what most needs to change for a version that reads as a duplicate.
```
