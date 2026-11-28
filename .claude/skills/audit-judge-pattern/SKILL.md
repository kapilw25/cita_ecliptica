---
name: audit-judge-pattern
description: Read every AI judge's feedback on a paper (feedback/output/*/by_claude|by_chatgpt|by_gemini/step2.md), extract the patterns the judges repeat (contribution first, 2-3 findings, implication close, no number list, no definitions or confessions in the abstract, judge "Before" sentences still in the paper), check the current PDF against them with judge_pattern_check.py, and FIX every finding in the same turn with wording that also passes the project's gates. Use after any judge round, before any submission, whenever a draft is rebuilt near a deadline, on /audit-judge-pattern, and when the owner says feedback, judges, pattern, engineering report, boring, robotic, tone, contribution or novelty.
---

> **Copy of the canonical skill** (owner Sat Nov 28 2026 ~5 AM PST: "build this skill cita repo too"). Canonical: [dataset-bench-lab .claude/skills/audit-judge-pattern/SKILL.md](https://github.com/kapilw25/dataset-bench-lab/blob/main/.claude/skills/audit-judge-pattern/SKILL.md), copied from commit d3e3915; the check script, which lives in `audit-cvpr-reviewer/` there, is copied into this folder. **cita usage** (from `Overleaf_draft/v6_AAAI27_workshops/`): `python3 ../../.claude/skills/audit-judge-pattern/judge_pattern_check.py <venue>/0_main.tex feedback/output/<venue>/by_*.md feedback/output/<venue>/by_*/*.md`. Pass the `.tex`, not the PDF: this copy reads the abstract from the source with its numbers filled in, because Figure 1's labels come before the abstract in pdftotext; J6 still reads the PDF next to it. Selftest 3 of 3. Edit the canonical file first, then re-copy, so the two never drift.

# 🧭 /audit-judge-pattern: the judges' pattern, checked and fixed, in every project

**Owner Fri Nov 27 2026 ~1:05 AM PST:** "build 3rd /audit-<skill> for the same: ... the two audit skills can't catch this because neither one reads the judges' feedback ... Neither extracts the pattern the judges repeat: contribution first, 2 or 3 findings, an implication at the end." Same night: "why are you stoppign at EXPLANAtion? dont you understand the mergency? just 3 hours left".
**Why (measured):** the MakingSense and EvalAIScientists abstracts kept a 25-28 number list and a term definition for 2 days, while all 3 judges' top rewrite was the abstract; SwiPO's judges named the same pattern ("Decides whether the reviewer reads a contribution or a lab report", 4/10). `/audit-cvpr-reviewer` scores pages against a fixed checklist and `/audit-like-a-human` checks layout; neither read the judges' files.

**Legend:** ✅ pass · ❌ fail, fixed in the same turn · 📝 decision row with reason · 🔁 rebuild

## 📌 TL;DR

| # | Step |
|---|---|
| 1 | 📥 Collect every `step2.md` of the draft's judges (all rounds) and the "rewrites that matter most" / "Before / After" parts. |
| 2 | 🧪 Run the check script on the PDF and the judge files (note c). |
| 3 | ❌ Each J1-J5 FAIL is rewritten NOW, in the venue's own theme, every number from the macro files, then 🔁 rebuild and rerun every gate. |
| 4 | 📝 Each J6 line (a judge's "Before" sentence still in the paper) is rewritten, or gets a decision row in the draft's TODOs.md with its reason. |
| 5 | 📸 Screenshot every changed spot (green) and send it; push. Explaining without fixing is not done. |

- Note c: `python3 .claude/skills/audit-cvpr-reviewer/judge_pattern_check.py <paper.pdf> <step2.md ...>`; `--selftest` gives 3 of 3.

## 🧹 Part D sweep: every row, not only the top items (owner Fri Nov 27 2026 ~1:25 AM PST)

- **The owner:** "we have hardly 2 hours left and it seems you are NOT following the feedback ... which SKILL will cover this?", then "go".
- **What went wrong:** each judge's step2.md has a Part D tone table (# | page | quoted original | problem | rewrite). Only the top items and phrase-matched rows were applied; the other rows were never walked, so 21 judge-quoted sentences stayed word for word in MakingSense and EvalAIScientists.
- **The rule:** after every judge round, walk EVERY Part D row of EVERY judge. For each row whose quoted original is still in the PDF, apply the rewrite (in `common/` when shared, so all drafts get it), keeping every number and fact, or write a decision row in the draft's TODOs.md with its reason. Done when J6 lists only rows with a decision.
- **Pinned reviewer sentences (review_coverage ledger):** a judge rewrite of a pinned sentence needs the owner's yes; then the new wording goes into `<draft>/ledger_overrides.json` (read by `variants/fit_ledger.py`), so the earlier reviewer's answer stays present and checked.
- **First run (Nov 27, 1:31 AM PST, commit 79e8f531f):** 12 rewrites, 7 pinned rows overridden (L01, L09, L13, L15, L16, L24, L52), every number identical, judge quotes still in the paper 21 to 4 (3 Figure 1 labels kept by owner pick, the AI-use statement). J6 prefix matching ignores punctuation, so a rewrite that keeps the judge's opening words can still be listed (the price sentence was).

## 1️⃣ The patterns (from both projects' judges)

| Code | Pattern the judges repeat | Check |
|---|---|---|
| 🚪 J1 | the work is presented in the first 3 sentences | "We present", "we introduce" or the name with a verb |
| 🔢 J2 | findings, not a number list | no 3 number-sentences in a row; at most 10 numbers per 100 words |
| 📖 J3 | no definitions in the abstract | no "is one model", "means that", "is defined as" |
| 🏁 J4 | close on what a reader should do | last sentence: should, points to, suggests, guides, so that |
| 🙅 J5 | never close on a confession or a tie | last sentence: no "not tested", "unverifiable", "tie" |
| 🧾 J6 | the judges' own "Before" sentences | still word for word in the PDF = rewrite or decision row |

## 2️⃣ Rewriting so the gates pass too

- 🧭 Sentence 1 says why the problem matters (Hospital-Bench abstract rule A1: no digit, no name), sentence 2 is "We present ...". This satisfies the judges and A1 together.
- 🎯 Pick the 2-3 findings that fit the venue's call, not the judges' venue: their rewrites were written for Bench2Evidence (repeats, deployment); MakingSense argues sensors, EvalAIScientists argues measurement checks.
- 🛡️ Keep the project's hard limits: "consistent with", never "confirming" (overclaim gate); pinned reviewer sentences stay word for word (review_coverage); failure words at most 3 per 100 words (abstract_tone D).
- 🔢 Numbers only from macros; a 1-number rewording is fine, a new number needs its own source.

## 3️⃣ The agent brief (fresh, read-only, when a second opinion is wanted)

> Read these judge files: <paths>. List the patterns at least 2 judges repeat about framing, tone and structure (quote each). Then read this paper's abstract, introduction's first paragraph and conclusion from the page pictures <paths>. For each pattern: PASS or FAIL with the quoted sentence, and one rewrite that keeps every number. Do not edit files.

## 4️⃣ Where it runs

| Project | How |
|---|---|
| 🏥 Hospital-Bench | 🟢 every draft build runs J1-J5 and fails on it (note a) |
| 🤝 SwiPO | 🟡 run the script by hand on each draft PDF (note b) |
| 🧠 FactorJEPA | 🟡 same as SwiPO (note b) |

- Note a: `variants/build_variant.sh` calls the script; `build_all.sh` in the workshop folder shows the result per draft.
- Note b: `python3 judge_pattern_check.py 0_main.pdf feedback/output/*/by_*/step2.md` from the workshop folder.

## 🧾 Log

| 📅 Date | 📝 What |
|---|---|
| 2026-11-27 | 🟢 Created by owner order. First run: MakingSense FAIL then PASS after the rewrite; EvalAIScientists FAIL then PASS after the rewrite (same night, both pushed); Bench2Evidence FAIL (J2 number list, J4 no implication), due Dec 1. Judges' own rewrites FAIL J2 (22-25 numbers), so J2 is stricter than the judges on number count; their shared ask is the structure. |
