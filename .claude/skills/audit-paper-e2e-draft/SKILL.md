---
name: audit-paper-e2e-draft
description: End-to-end audit of a LaTeX paper draft the way a senior reviewer reads it, in one command - tables (bold winners under a declared rule, a 95% CI in every metric cell, captions that say what bold means), build log (errors, undefined refs, duplicate labels, overfull boxes), PDF (page budget, '??', em-dash glyphs), cross-references (every table, figure and numbered equation cited), numbers (every abstract and conclusion number traced to the body), overclaiming words, undefined acronyms, required sections, bibliography, double-blind anonymity, plus the audit-ai-signatures and paper-consistency checks. Use before calling any draft final, before any submission, re-upload or arXiv upload, after editing a table, figure, abstract or conclusion, and when the user reports formatting or consistency mistakes.
---

# /audit-paper-e2e-draft - one command, every mistake a reviewer catches

Why (owner, 2026-10-20): the SC4AI draft passed the prose and version checkers while three tables
had no bold winner, one table had no per-cell intervals, two figures were never cited, three
equations were numbered but never referenced, the abstract's efficiency interval appeared nowhere
in the body, and four acronyms were never spelled out. Each was caught by the owner or by this
audit, never by the checks we had. Errors of this kind are common: an automated study of 2,500
ICLR, NeurIPS and TMLR papers found 4.7 objective mistakes per paper, rising over time
([To Err Is Human, 2025](https://arxiv.org/abs/2512.05925)).

## Step 1 - build, then run

```bash
latexmk -pdf <main.tex>          # the audit reads the .log, .blg and .pdf next to the .tex
python3 .claude/skills/audit-paper-e2e-draft/check_draft.py <main.tex> --max-pages 8 \
    --ref <submitted-version.tex> --forbid "<withdrawn claim>" [--double-blind] [--claims]
```

One ASCII table, exit 1 on any FAIL. `--claims` prints every overclaiming word with its line.
Re-run after every fix: a fix can create a new FAIL (adding text pushed SC4AI past page 8).

## What it checks, and why each one is here

| # | Mistake authors make | Check | Source |
|---|---|---|---|
| 1 | Winner not bold, wrong cell bold, bold read as significance | `% bold:` rule per tabular; FAIL on missing or wrong bold; caption must say what bold means | [Card et al. 2020](https://arxiv.org/abs/2010.06595) (63% bold the best, rarely say if it is significant); [offline MARL audit](https://arxiv.org/abs/2406.09068) |
| 2 | Metric reported with no interval, or no word on how it was computed | WARN on any decimal cell without `\pm` or `[..]` unless `% ci: <reason>`; caption must say 95% | [NeurIPS checklist](https://neurips.cc/Conferences/2022/PaperInformation/PaperChecklist) (error bars, how computed) |
| 3 | Abstract or conclusion number that the body never shows | FAIL if a number there is missing from the body and tables | [manusights](https://manusights.com/academy/lessons/MFIG3); table/text mismatches in [To Err Is Human](https://arxiv.org/abs/2512.05925) |
| 4 | Broken or missing cross-references; figures never cited | FAIL on undefined refs, duplicate labels, '??' in the PDF; WARN on uncited tables, figures, sections | [To Err Is Human](https://arxiv.org/abs/2512.05925) (5.3% of mistakes); [Klein](https://people.eecs.berkeley.edu/~klein/cs288/sp10/writing-comments.pdf) |
| 5 | Numbered equations that nothing cites | WARN on numbered equation blocks without a label | [JMLR formatting errors](https://jmlr.csail.mit.edu/format/formatting-errors.2015.02.09.html) |
| 6 | Over the page limit | FAIL if the main text (before References) passes `--max-pages` | [Fournier-Viger](https://data-mining.philippe-fournier-viger.com/common-mistakes-writing-research-paper/) |
| 7 | Captions that do not stand alone | WARN on captions under 12 words | [Klein](https://people.eecs.berkeley.edu/~klein/cs288/sp10/writing-comments.pdf) (reviewers scan figures and captions) |
| 8 | Overclaiming, speculation as fact | WARN listing significant, state of the art, outperform, prove, guarantee, always, never | [Lipton and Steinhardt 2018](https://arxiv.org/abs/1807.03341) |
| 9 | Acronyms and terms never defined | WARN on acronyms never written as `Long form (ACR)` and not a cited method name | [Studia UBB editorial](https://www.cs.ubbcluj.ro/~studia-i/contents/2010-4/01-Editorial.pdf) (undefined concepts) |
| 10 | No limitations section | FAIL without Limitations or Conclusion; WARN without Ethics | [NeurIPS checklist](https://neurips.cc/Conferences/2022/PaperInformation/PaperChecklist) |
| 11 | Missing or incomplete references | FAIL on a cited key missing from the .bib or without title or year; WARN on BibTeX warnings | [JMLR formatting errors](https://jmlr.csail.mit.edu/format/formatting-errors.2015.02.09.html) |
| 12 | LaTeX build problems | FAIL on errors; WARN on overfull boxes | [arXiv common mistakes](https://info.arxiv.org/help/faq/mistakes.html) |
| 13 | Identity leaks in a double-blind submission | with `--double-blind`: FAIL on visible names, GitHub user links, own arXiv links | venue rules |
| 14 | Machine-written prose tells, em dashes (house rule) | runs `audit-ai-signatures`; PDF em-dash glyphs FAIL (style files insert them) | owner rule 2026-09 |
| 15 | Versions of one paper that disagree | runs `paper-consistency` with `--ref` (title, authors, abstract numbers, withdrawn claims) | owner incidents 2026-10 |

## Step 2 - declare a bold rule above every numeric tabular

```latex
% bold: row max cols=2-6                                          % winner per row, label column = 1
% bold: col max cols=2; col min cols=5                            % per column, direction per column
% bold: row max cols=3,5,7,9; row max cols=4,6,8,10 rows=\ast     % second rule only on rows marked \ast
% bold: none (text table)
% ci: LITMUS (AQI) has no per-item score (stated in the caption)
```

Bold means the best point estimate (owner decision 2026-10-20) and every caption says so. Leave a
column out of the rule when it has no better direction, and say that in the caption. Generate the
rows from the results JSON with the rule applied; never bold by hand.

## Step 3 - what no script can judge (read the PDF as the reviewer will)

- Math: re-derive every equation and proof step; every symbol defined before use, one meaning per
  symbol. Math errors are 54% of the mistakes found in published AI papers ([To Err Is Human](https://arxiv.org/abs/2512.05925)).
- Each claim-word use from `--claims` against its interval: a bolded or "higher" result whose
  interval overlaps the runner-up is not a win.
- Bold direction: is higher really better for every bolded column, under every contract? Never bold a
  metric the paper itself says does not compare models (SC4AI Table 4 bolded the within-model AQI row).
- Symbols in an early equation that are only defined in a later section (SC4AI used sigma, beta and
  Delta in Section 2, defined in Section 4); estimators named for what they are (a mean log-ratio on
  dataset pairs is not an unbiased KL estimate).
- Figure labels: every axis code or abbreviation (M1 to M5) defined in the caption or text; no
  overlapping tick or value labels; titles that do not claim more than the caption (an "overall
  performance" title on a relative score).
- Text agrees with tables and figures: every range, winner and count in a sentence matches the cells.
- Figures readable at print size; same model names, order and colors in every table and figure.
- Source comment above every table and figure names the results file its numbers come from.

Related: [audit-ai-signatures](../audit-ai-signatures/SKILL.md), `~/.claude/skills/paper-consistency`
(both are called by this audit and still work alone).
