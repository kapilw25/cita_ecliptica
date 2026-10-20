---
name: naming-prefix
description: Name similar files and folders with a shared KIND prefix so they sort together (log_hourly.md, log_12hour.md, jobs_hourly.md), and check a folder for names that break it. Use whenever creating or renaming a file or folder that has siblings of the same kind (logs, job lists, plans, trackers, audits, sheets), and on /naming-prefix.
---

# /naming-prefix - the kind first, so siblings sort together

Why (owner order 2026-10-19): `hourly_log.md` and `12hour_log.md` sat apart in the folder listing because the kind ("log")
came last; the owner: "add common PREFIX to similar files", e.g. `log_hourly.md`, `log_12hour.md`. Before this skill only
version prefixes had rules (figures `v<i>_` in plot-standards rule 11, notes `vNN_` in audit-goal).

## The rule

- A file or folder that has siblings of the same kind starts with that kind: `<kind>_<what>[_<date>].<ext>`.
  Kinds in use: `log_` (time logs), `jobs_` (scheduled job lists), `plan_`/`pNN_` (plans), `audit_`, `sheet_`, `run_`.
- Existing number schemes stay and come first where a skill sets them: notes `vNN_`, plan folders `pNN_`, plan files
  `NN_`, figures `v<i>_`. The kind prefix is for the files that have no such scheme.
- A rename moves every reference in the same change: links in md files, scripts, scheduled job prompts, skills, memory.
  `grep -rn "<old name>"` over the repo and memory must print nothing afterwards.
- Archives keep their old names inside `legacy/` (they are records, not live siblings).

## Check

`python3 .claude/skills/naming-prefix/check_prefix.py <folder>` lists every file whose name holds a known kind word
anywhere but first (e.g. `log_hourly.md` -> `log_hourly.md`); `legacy/` is skipped. Exit 1 on any hit.

Related: [plot-standards](../plot-standards/SKILL.md) rule 11, [audit-goal](../audit-goal/SKILL.md) ("Where a written plan
lives"), [tables-md](../tables-md/SKILL.md) Rule 12 (the logs this was first applied to).
