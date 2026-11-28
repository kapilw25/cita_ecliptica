#!/usr/bin/env python3
"""judge_pattern_check.py: fail a paper PDF on the tone pattern that every AI judge (Claude, ChatGPT, Gemini) flagged in BOTH projects,
before a judge or the owner has to point it out again.

Owner Fri Nov 27 2026 ~1:00 AM PST: "if you are not correcting any mistake unless I point it out, then whats the use of sharing these
feedbacks? ... why /audit-cvpr-reviewer and /audit-like-a-human SKILLs are useless? can you FIX them? to identify PATTERN from the
feedback, sound more human (cheerful positive focussing on contribution and novelty) and less AI robotic, engineering".
The pattern, quoted from the judges:
  Hospital-Bench (Claude, ChatGPT, Gemini v1): every judge's top rewrite was the abstract, opening with the contribution, 2-3 findings,
    and an implication close; "The abstract strings together about 25 numbers".
  SwiPO (Claude v1): "Framing, clarity and tone ... Decides whether the reviewer reads a contribution or a lab report" (scored 4/10),
    "Abstract closes on a tie"; (Gemini v1): "turns an apologetic engineering status report into a confident, research-led contribution".

Checks on the ABSTRACT (J1-J5) and the judges' own top asks (J6):
  J1 contribution early: a sentence among the first 3 presents the work (we present / introduce / propose / release, or "<Name> is/tests/...").
  J2 not a number list: no 3 sentences in a row with 3+ numbers each, and at most 10 numbers per 100 words.
  J3 no definitions: the abstract defines no term ("X is one model", "means that", "is defined as", "we call").
  J4 implication close: the last sentence says what follows (should / point(s) to / suggest / guide / motivate / call for / enable).
  J5 no negative close: the last sentence holds no confession or tie (not tested, unverifiable, cannot, no clear, not logged, tie).
  J6 judges' "Before" quotes: every sentence a judge quoted as "Before" in its top rewrites, still found word for word in the PDF,
     is listed as NOT ADDRESSED (a WARN each; the owner decides, a decision goes in the draft's TODOs.md).
Usage: python3 judge_pattern_check.py PAPER.pdf|VENUE/0_main.tex [JUDGE_step2.md ...]    exit 1 on any J1-J5 FAIL.
cita_ecliptica copy (Sat Nov 28 2026, owner: "build this skill cita repo too"): a .tex argument reads the abstract from the source with
every \newcommand number filled in (a figure at the top of page 1 puts its labels before the abstract in pdftotext, which made the PDF
reading take "Final adapter only (earlier evaluations)" as the abstract); J6 still reads the PDF next to the .tex.
       python3 judge_pattern_check.py --selftest
"""
import re, subprocess, sys

NUM = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
PRESENT = re.compile(r"\b(we (present|introduce|propose|release|contribute|build)|this paper (presents|introduces|proposes))\b", re.I)
DEFINE = re.compile(r"\b(is one model|means that|is defined as|we call|refers to)\b", re.I)
IMPLY = re.compile(r"\b(should|points? to|suggests?|guides?|motivates?|calls? for|enables?|opens? the way|so that)\b", re.I)
NEGCLOSE = re.compile(r"\b(not tested|unverifiable|unverified|cannot|no clear|not logged|tie|ties|inconclusive|remains? open)\b", re.I)

def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", t) if len(s.strip()) > 3]

def abstract_of(text):
    t = re.sub(r"This is an anonymized submission.*?if accepted\.", " ", text, flags=re.S)
    m = re.search(r"\bAbstract\b(.*?)(\n\s*(1\s+)?Introduction\b|\n\s*\d?\s*[A-Z][a-z]+ [a-z]+[^\n]{0,40}\n\s*\n)", t, re.S)
    a = m.group(1) if m else t[:2500]
    return re.sub(r"\s+", " ", a.replace("-\n", "")).strip()

def check_abstract(a):
    out, S = [], sentences(a)
    if not S: return ["J0 FAIL: no abstract found"]
    if not any(PRESENT.search(s) or re.search(r"^[A-Z][A-Za-z\-]+(Bench|Gym|PO|Net)\b.{0,40}\b(is|tests|grades|measures|turns)\b", s) for s in S[:3]):
        out.append("J1 FAIL: no sentence among the first 3 presents the work (we present / introduce / propose)")
    counts = [len(NUM.findall(s)) for s in S]; run = best = 0
    for c in counts: run = run + 1 if c >= 3 else 0; best = max(best, run)
    words = len(a.split()); nums = sum(counts); dens = 100 * nums / max(words, 1)
    if best >= 3: out.append(f"J2 FAIL: {best} sentences in a row carry 3+ numbers each (a number list, not findings)")
    if dens > 10: out.append(f"J2 FAIL: {nums} numbers in {words} words ({dens:.1f} per 100, limit 10)")
    for s in S:
        if DEFINE.search(s): out.append(f"J3 FAIL: the abstract defines a term: \"{s[:90]}\""); break
    if not IMPLY.search(S[-1]): out.append(f"J4 FAIL: the last sentence states no implication: \"{S[-1][:110]}\"")
    if NEGCLOSE.search(S[-1]): out.append(f"J5 FAIL: the abstract closes on a confession or tie: \"{S[-1][:110]}\"")
    return out

def judge_befores(md):
    t = open(md, encoding="utf-8").read(); outs = []
    for m in re.finditer(r"(?im)^\s*\**\s*before\s*\**\s*:?\s*\n?\s*[\"“](.{25,400}?)[\"”]", t): outs.append(m.group(1))
    # Part D tables: | # | where | "quote" |. Row ids may carry a letter or a dot (C1, B11, 4.1, 6.3: the Claude open-venue review, Fri Nov 27 2026), not only digits.
    for m in re.finditer(r"\|\s*[A-Z]?\d+(?:\.\d+)?\s*\|[^|\n]*\|\s*[\"“](.{25,300}?)[\"”]\s*\|", t): outs.append(m.group(1))
    return outs

def norm(s): return re.sub(r"[^a-z0-9% ]", "", re.sub(r"\s+", " ", s.lower())).strip()

def tex_macros(tex):
    """Every \\newcommand reachable through \\input from the main file; paths resolve from its folder, as LaTeX does."""
    from pathlib import Path
    root, defs, seen, todo = Path(tex).resolve().parent, {}, set(), [Path(tex).resolve()]
    while todo:
        f = todo.pop()
        if f in seen or not f.exists(): continue
        seen.add(f); t = f.read_text()
        for name, val in re.findall(r"\\newcommand\{?\\(\w+)\}?\{((?:[^{}]|\{[^{}]*\})*)\}", t): defs[name] = val
        for m in re.findall(r"\\input\{([^}]+)\}", t): todo.append((root / (m if m.endswith(".tex") else m + ".tex")).resolve())
    return defs

def abstract_of_tex(tex):
    src = open(tex, encoding="utf-8").read()
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S)
    if not m: sys.exit(f"FATAL: no abstract in {tex}")
    s, d = re.sub(r"(?<!\\)%.*", "", m.group(1)), tex_macros(tex)
    for _ in range(3):
        s = re.sub(r"\\(\w+)\{\}", lambda x: d.get(x.group(1), x.group(0)), s)
    s = re.sub(r"\\(mbox|textbf|emph|textit|text)\{([^}]*)\}", r"\2", s)
    s = s.replace("$-$", "-").replace("\\%", "%").replace("~", " ")
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    return re.sub(r"\s+", " ", re.sub(r"\\[a-zA-Z]+", "", s).replace("{", "").replace("}", "")).strip()

def main(pdf, mds):
    tex = pdf if pdf.endswith(".tex") else None
    if tex: pdf = tex[:-4] + ".pdf"
    text = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    a = abstract_of_tex(tex) if tex else abstract_of(text)
    fails = check_abstract(a); flat = norm(text.replace("-\n", ""))
    print(f"judge_pattern_check: {pdf}\n  abstract: {len(a.split())} words, {len(sentences(a))} sentences")
    for f in fails: print("  " + f)
    warn = 0
    for md in mds:
        for q in judge_befores(md):
            k = norm(q)[:70]
            if len(k) > 30 and k in flat: warn += 1; print(f"  J6 WARN NOT ADDRESSED ({md.split('/')[-2]}): \"{q[:110]}\"")
    print(f"  {'FAIL' if fails else 'PASS'} J1-J5 ({len(fails)} finding(s)), J6 {warn} judge quote(s) still in the paper")
    return 1 if fails else 0

def selftest():
    old = ("Embodied agents that help in hospitals must turn what they see into actions that hold up across a whole chore. Yet most benchmarks "
           "score a single step or the final outcome, which hides where a long task first goes wrong. We present HospitalBench, 10 hospital chores "
           "of five steps designed to link. A chain is one model running the five steps of a chore, and its first break is the first step it fails. "
           "A scripted robot passes 20 of 20 starts, and a random agent passes no step of 57 chains. Across seven frontier vision-language models, "
           "6 of 137 chains finish, and 78% of the counted failures (99 of 127) end at step 1 (guided) or step 2, the first unguided step. Two controls "
           "show what moves the score: blanking the pictures lowers Opus 5.5 from 1.25 to 0.45 mean steps over 20 chains, while true object positions "
           "lift Terra 6.1 from 1.16 to 2.47 on 19 paired chains. A 108-fold price spread across default settings leaves mean steps between 0.7 and 1.7. "
           "Our findings point to locating objects as a key lever for Terra 6.1 on long embodied chores.")
    new = ("Embodied agents that help in hospitals must turn what they see into actions that hold up across a whole chore. We present HospitalBench, "
           "10 hospital chores of five linked steps in which every step of a camera-driven agent is graded from scene state, so a score shows whether "
           "a chore succeeds and where it first goes off course. Between a scripted robot that solves 20 of 20 starts and a random agent that scores "
           "zero, seven frontier vision-language models finish 6 of 137 chains, and 78% of their failures come at the first or second step. The "
           "pictures carry real weight: blanking them lowers Opus 5.5 from 1.25 to 0.45 mean steps, and true object positions lift Terra 6.1 from "
           "1.16 to 2.47, while a 108-fold price spread barely moves the score. Controlled replays give evidence consistent with the intended "
           "dependence on 12 of 33 tested links. These findings point to locating objects, rather than a pricier model, as the lever for long "
           "embodied chores, and to step-level grading as the way to find it.")
    swipo_tie = "We present SwiPO, a method. It reaches 0.56 on A. On B the methods tie and the gap is not tested."
    cases = [("old MakingSense abstract (owner: 'boring engineering report')", old, True),
             ("new MakingSense abstract (Nov 27 1:15 AM)", new, False),
             ("SwiPO-style close on a tie (Claude v1: 'Abstract closes on a tie')", swipo_tie, True)]
    ok = 0
    for name, a, want_fail in cases:
        f = check_abstract(a); got = bool(f); ok += got == want_fail
        print(f"{'ok ' if got == want_fail else 'BAD'} {name}: {'FAIL' if got else 'PASS'} {f[:3]}")
    print(f"selftest {ok} of {len(cases)}"); return 0 if ok == len(cases) else 1

if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]: sys.exit(selftest())
    if len(sys.argv) < 2: sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
