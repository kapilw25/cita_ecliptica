---
name: paper-variants
description: One source, many workshop drafts. Shared sections of a paper live once in a common/ folder that every venue draft pulls in with \input; each venue folder keeps only its venue parts (title, abstract, first paragraph, framing, venue switches). One build script rebuilds every draft and runs the page and tone gates per draft, then one fresh checker agent per draft reads its PDF pages for format problems. Drafts at or past their deadline are frozen and never rebuilt by a shared edit. Use in any project with several venue drafts of one paper (Hospital-Bench, SwiPO, FactorJEPA), whenever a judge fix or a wording change should reach every draft, when creating a new venue draft, and when the owner says sync, all drafts, common parts, variants or venues.
---

> **Copy of the canonical skill** (owner pick Fri Nov 27 2026: full copy in cita_ecliptica). Canonical: [dataset-bench-lab .claude/skills/paper-variants/SKILL.md](https://github.com/kapilw25/dataset-bench-lab/blob/main/.claude/skills/paper-variants/SKILL.md), copied from commit 397749a. Edit the canonical file first, then re-copy it here, so the two never drift.

# 🧬 paper-variants: one source, many workshop drafts

**Owner order Fri Nov 27 2026 ~12:30 AM PST:** "create SKILL for optionA, which can be shared across all 3 projects". Option A: "Shared sections live in one common/ folder that every draft pulls in with \input. Each draft keeps only its venue parts ... One build makes all 6, then a checker agent reads each PDF."
**Why (measured, Nov 26-27 2026):** three judge rewrites had to be typed into MakingSense and EvalAIScientists one copy at a time, 4 hours before their deadline; 6 of 9 judge fixes made on Bench2Evidence had never reached those two drafts. One shared file would have carried them in one edit.
**Pattern sources:** one source with venue switches ([ISI multi-version LaTeX](https://ant.isi.edu/~calvin/latex-multidoc.htm), CTAN [optional](https://ctan.org/pkg/optional) and [tagging](https://ctan.org/pkg/tagging)); shared snippets plus a drift check ([Grafana shared content](https://grafana.com/docs/writers-toolkit/write/reuse-content/reuse-shared-content/)).
**Status (Fri Nov 27 2026 1:10 AM PST, owner: "AUTO-SYNC ... FIX it NOW, what are you waiting for?"):** 🟢 Hospital-Bench is migrated for its two urgent drafts. `v3_AAAI_workshop/common/` holds `sec/0_fig.tex`, `sec/2_benchmark.tex`, `sec/3_results.tex`, `arm_macros.tex`, `price_macros.tex`; MakingSense and EvalAIScientists `\input` them (pdftotext of both PDFs identical before and after, 0 diff lines, 5 pages each). `build_all.sh` rebuilds every draft with the drift gate (`variants/_gates/drift_gate.py`, selftest 3 of 3, caught a planted stale copy) and all per-draft gates, skips `FROZEN` drafts, prints one table. 🟡 Bench2Evidence still has its own copies (its sections differ; deadline Dec 1). 🟢 SwiPO is migrated for all four upcoming venues (Fri Nov 27 ~12:15 AM PST, note b), with generated venue numbers. ⚪ FactorJEPA not migrated.
**Owner order the same night overrides the 6-hour rule below for this migration:** it ran 3 hours before the deadline because the proof (identical PDF text) was cheap and the sync was the point. The rule still holds by default.
**Lesson (owner, same night):** "why are you stoppign at EXPLANAtion? dont you understand the mergency?" When an audit finds a problem in a draft with a deadline, fix it in the same turn and show the proof; an explanation without the fix is not an answer.

**Legend:** 🟢 shared once · 🟡 venue-only · 🔒 frozen · ✅ check passes · ❌ refused

## 📌 TL;DR

| # | Rule |
|---|---|
| 1 | 🟢 Text that is the same in every draft lives ONCE in `common/` (methods, setup, tables, figures, macros, refs, limits). |
| 2 | 🟡 A venue folder holds only `0_main.tex` with the venue parts plus `venue.tex` (switches). No copy of a common file, ever. |
| 3 | 🟡 A sentence that must differ for one venue goes behind a switch in `common/` (`\ifvenueX ... \fi`), not into a second copy. |
| 4 | 🔒 A draft whose deadline is under 6 h away, or already submitted, gets a `FROZEN` file; the build skips it and keeps its PDF. |
| 5 | ✅ One command rebuilds every unfrozen draft and runs the page, number and tone gates on each; one failing draft does not stop the others, and the run ends with a table. |
| 6 | ✅ Then one fresh checker agent per draft reads only that draft's page pictures and returns PASS/FAIL per format check. A FAIL is fixed in that draft's venue parts or by a switch, then rebuilt. |
| 7 | 🎯 Every draft choice (pages, cuts, titles) is judged by AAAI workshop acceptance odds: stay at 4 pages even where the call allows more, and pose the title as a question the abstract answers (section below). |

## 🎯 Every draft decision serves workshop acceptance (owner Fri Nov 27 2026 ~5:55 PM PST)

- **The owner:** "Stay at 4 pages to have a higher probability of acceptance at AAAI workshops >> keep all decisions with this goal in mind", and, on a judge's title idea: "try to convert TITLE into QUESTION ... to build the hook; update existing skills ... to not needed to repeat these instructions".
- **4 pages, even where the call allows more** (SwiPO LoyalAgents allows 8): short papers are judged on the idea and its first evidence, poster sessions take far more of them than oral slots take long papers, and a long paper invites "missing baselines or ablations". A new result earns its lines by a cut from the judges' cut lists.
- **The title is a question the abstract answers in its first sentence.** SwiPO, Nov 27: "Whose Contract Does an AI Agent Follow? ...", "Does a Contract Select a Pareto Point? ...", "Which Model Does an Alignment Benchmark Measure?", "Can One Contract Teach a Model to Switch? ...". Each venue title stays unique, and a title still changes only on the owner's OK. Question titles draw more downloads but fewer citations ([Jamali and Nikzad 2011](https://link.springer.com/doi/10.1007/s11192-011-0412-z), 2,172 PLoS articles); at a workshop the reviewer's first read decides.

## 1️⃣ Layout (same in all 3 projects)

```
<workshop dir>/                 e.g. v3_AAAI_workshop/ (Hospital-Bench), v6_AAAI27_workshops/ (SwiPO), v4_AAAI_workshop/ (FactorJEPA)
  venues.md                     deadlines, page limits, status per venue (already there in all 3)
  common/                       🟢 written once
    sec/2_method.tex ...        shared sections
    macros.tex  numbers.tex     shared macros; numbers come from generated files, never typed
    refs.bib  figs/             shared bibliography and figures
  v1_<Venue>_4page/             🟡 one folder per venue draft
    0_main.tex                  title, abstract, first paragraph, contribution framing, \input{../common/...}
    venue.tex                   \venueXtrue switches, venue page limit, track
    TODOs.md                    venue-only open items
    FROZEN                      🔒 optional: "submitted Fri Nov 27 3:59 AM PST" (build skips the folder)
  build_all.sh                  rebuild every unfrozen draft + gates + summary table
```

| 🧩 Part | 🟢 common/ | 🟡 venue folder |
|---|---|---|
| 📝 Title, abstract, first paragraph | ❌ | ✅ |
| 🎯 Contribution framing for the venue's call | ❌ | ✅ |
| 🔬 Method, benchmark, setup, tables, figures | ✅ | ❌ |
| 🔢 Numbers | ✅ generated macro files | ❌ never typed |
| 🧱 Limits, ethics, release, AI-use | ✅ | ❌ |
| 🔀 One sentence that differs for one venue | ✅ behind `\ifvenueX` | ❌ no copy |

## 2️⃣ The build (one command per project)

`build_all.sh` (or the project's existing builder, see section 5) first regenerates the numbers file from the results files and fails if a number the abstract or conclusion states is missing from the shared body (an audit that reads `.tex` source sees `\nName{}`, not its value, so this check replaces it). Then, for every `v*_*/` folder without `FROZEN`:

1. `latexmk -pdf 0_main.tex` inside the venue folder (TEXINPUTS includes `../common`).
2. The project's per-draft gates: page limit (body pages, word positions, no spill into a column of the reference page), numbers against the generated files, abstract and body tone, overclaim, AI signatures.
3. Drift gate: refuse (❌) if a venue folder holds a file whose name exists in `common/` (a stale copy), or a `.tex` paragraph of 40+ words identical to one in `common/` (pasted instead of `\input`).
4. One summary table: draft, pages, each gate PASS/FAIL. Exit non-zero if any unfrozen draft fails.

A FROZEN draft is listed as 🔒 with its last PDF's sha256, so a shared edit can never silently change a submitted paper.

## 3️⃣ The checker agent (one per draft, fresh, read-only)

After the build, spawn one agent per rebuilt draft, in parallel, each given ONLY that draft's page pictures (render at 96 dpi with the project's page shooter) and the venue's page rule from `venues.md`. Brief:

> Read every page picture of this draft. Report PASS/FAIL with page and position for: body within the page limit; nothing spills past the last body page; no overfull line or text off the margin; every figure and table readable at 100% zoom and referenced in the text; no orphan heading at a column bottom; anonymous (no names, no affiliations, no identifying links); references start after the body; title and abstract match the venue's theme. Do not suggest content changes. Do not edit files.

A FAIL is fixed in the venue folder (cut venue words) or with a switch in `common/` for that venue, then that draft alone is rebuilt and re-checked.

## 4️⃣ Editing rules

| ⚠️ | Rule |
|---|---|
| 🟢 Judge fix to a shared sentence | Edit `common/` once, run the build-all script, read every draft's page gate. A draft pushed over its limit is fixed in its venue parts, never by forking the shared file. |
| 🟡 Fix for one venue only | Venue folder, or a switch in `common/`. Say which in the commit message. |
| 🔒 Within 6 h of a deadline | Write `FROZEN` in that draft first; shared edits stop reaching it. Unfreeze only by owner order. |
| 🔢 Numbers | Only from generated macro files; a typed number in `common/` or a venue file is a gate FAIL (Hospital-Bench numbers_gate, R10/R21; SwiPO `make_numbers.py` writes `common/numbers.tex`, and `build_all.py` fails a venue file that types a decimal). |
| 🧩 LaTeX switches | A control word eats the space after it: write `\fi{}` and `\nName{}` mid-sentence. The array package does not expand a macro inside a column spec: switch the whole `\begin{tabular}{...}` through a macro. A macro may expand to `&`, so `\uses{a}{b}` can drop two columns for one venue. |
| 🧾 Gates are per draft | A gate that passes on one draft says nothing about another; every draft runs every gate. |

## 5️⃣ Per-project map

| 🗂️ Project | 📁 Workshop folder | 📋 Venues | 🔧 Builder today |
|---|---|---|---|
| 🏥 Hospital-Bench | [v3 workshop](https://github.com/kapilw25/dataset-bench-lab/tree/main/papers/p03-spatial-agent-bench/overleaf/v3_AAAI_workshop) | [venues](https://github.com/kapilw25/dataset-bench-lab/blob/main/papers/p03-spatial-agent-bench/overleaf/v3_AAAI_workshop/venues.md) | 🟡 one builder per draft, gates shared (note a) |
| 🤝 SwiPO (prev CiTA) | [v6 workshops](https://github.com/kapilw25/cita_ecliptica/tree/main/Overleaf_draft/v6_AAAI27_workshops) | [venues](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/venues.md) | 🟢 [build_all.py](https://github.com/kapilw25/cita_ecliptica/blob/main/Overleaf_draft/v6_AAAI27_workshops/build_all.py) + make_numbers.py (note b) |
| 🧠 FactorJEPA | [v4 workshop](https://github.com/kapilw25/factorjepa/tree/main/overleaf/v4_AAAI_workshop) | [venues](https://github.com/kapilw25/factorjepa/blob/main/overleaf/v4_AAAI_workshop/venues.md) | 🟡 each draft folder builds alone (note c) |

- Note a (Hospital-Bench): `variants/build_variant.sh <name>` plus `variants/_vdir.py`, which finds `vN_<Venue>_4page/0_main.tex`; the gates are in `variants/_gates/`.
- Note b (SwiPO): venue folders `v4_LoyalAgents_4page_astrained`, `v5_MultiRobust_4page`, `v6_Bench2Evidence_4page`, `v7_MATH4AI_4page`; `v1`-`v3` FROZEN. Switches `\ifanon`, `\ifvenueLoyal|Robust|Bench|Math` in `common/preamble.tex`. Each `venue.tex` records the review mode read from the venue's OpenReview submission invitation (`authors.readers` restricted to the venue means double-blind), never guessed.
- Note c (FactorJEPA): one folder per draft, `v1_Human_Centric` and `v2_Cog2Soc`.

## 6️⃣ Migrating a project (one time, after its nearest deadline)

1. Freeze every draft due within 6 h (`FROZEN` file) and copy its PDF aside.
2. Pick the most-judged draft as the base (Hospital-Bench: `v1_Bench2Evidence_4page`). Move its sections that are not venue parts into `common/`; replace them in the base with `\input{../common/...}`.
3. For each other draft: diff its sections against `common/`. Identical text becomes an `\input`; a sentence that differs on purpose becomes a switch; an accidental difference (an old wording) takes the `common/` text, and the commit says which judge fix it brings.
4. Rebuild all, run every gate, and compare each draft's pdftotext with its pre-migration PDF: every difference must be an intended one (a judge fix arriving) and every number must be identical (Hospital-Bench did this check for the folder move on Nov 26: 0 diff lines). Then prove the sync once: in a scratch copy, add a sentinel sentence to one `common/` file, rebuild every draft, and grep the sentinel in each PDF; plant a pasted paragraph, a stale copy and a typed number in one venue folder and confirm the gates refuse all three.
5. Checker agents on every draft; push only when all are PASS.

## 🧾 Log

| 📅 Date | 📝 What |
|---|---|
| 2026-11-27 | 🟢 SwiPO migrated (cita_ecliptica 87299df to 9f9cc82): LoyalAgents pdftotext 0 diff lines after the move; sentinel in 4 of 4 PDFs; gates caught the planted paste, stale copy and typed number; every number in the 4 PDFs identical before and after the switch to generated macros. Two corrections (KL description, contract echo) then reached all 4 drafts in one shared edit each. |
| 2026-11-27 | 🟢 Skill written by owner order. Trigger case: MakingSense and EvalAIScientists lacked 6 of 9 Bench2Evidence judge fixes; 3 were typed into both drafts by hand 4 h before the deadline (commit 3725a6b04, every number identical). |
