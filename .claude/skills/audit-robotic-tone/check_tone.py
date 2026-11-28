"""Flag robotic, engineering-report sentences in a paper (abstract from the .tex, body from the built PDF), one row per sentence. CPU.
    python3 .claude/skills/audit-robotic-tone/check_tone.py <venue>/0_main.tex [--all] [--max-abstract-numbers 3]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HEDGES = ["not separable", "no resolved", "resolved", "at most", "slightly", "barely", "each interval", "including zero",
          "detectably", "limited", "not yet", "rarely", "weak", "unresolved", "no detectable", "does not move"]
ENGINEERING = ["adapter", "as trained", "first turn", "phrase gap", "phrase heuristic", "judge gap", "chain", "merged",
               "loading", "loads", "lora", "run-on", "checkpoint", "parent", "strict-minus-permissive", "pipeline",
               "heuristic", "instrument", "macro", "replicate"]
FINDING_VERBS = r"\b(we (show|find|found|reveal|discover|demonstrate|observe)|turns out|surpris|strikingly|only two|only one)\b"
IMPLICATION = r"\b(so |argues|suggests|means|matters|implies|implication|calls for|should|must|we need|which argues)\b"
MODEL_NAMES = r"[A-Za-z]+[-]?\d+(?:\.\d+)?(?:-[\w.]+)+|[A-Z][A-Za-z]*\d+(?:\.\d+)?-\d+B[\w-]*"
REFS = r"\((?:[^()]*et al\.[^()]*|[^()]*\b(19|20)\d\d[a-z]?)\)|(?:Section|Table|Figure|Fig\.|Eq\.)~?\s*\d+[a-z]?"


def numbers(s):
    s = re.sub(REFS, " ", re.sub(MODEL_NAMES, " ", s))
    return re.findall(r"(?<![\w.])[+\-−]?\d+(?:[.,]\d+)*%?", s)


def signals(s, in_abstract):
    out = []
    n = len(numbers(s))
    if n >= (2 if in_abstract else 3):
        out.append(f"number dump ({n} numbers)")
    if re.search(r"\[[^\]]*\d[^\]]*,\s*[^\]]*\d[^\]]*\]|\d\s*%\s*interval|95\\?%|\(\s*[+\-−]?\d[\d.]*\s*(to|,)\s*[+\-−]?\d", s):
        out.append("interval in prose")
    if s.count("(") >= 2:
        out.append(f"parenthesis stack ({s.count('(')})")
    w = len(s.split())
    if w > 35:
        out.append(f"too long ({w} words)")
    if s.count(";") >= 2:
        out.append(f"semicolon chain ({s.count(';')})")
    low = s.lower()
    h = [x for x in HEDGES if x in low]
    if len(h) >= 2:
        out.append("hedge stack (" + ", ".join(h[:3]) + ")")
    e = [x for x in ENGINEERING if x in low]
    if len(e) >= 2:
        out.append("engineering words (" + ", ".join(e[:3]) + ")")
    ac = set(re.findall(r"\b[A-Z]{2,}[A-Za-z0-9-]*\b", s))
    if len(ac) >= 4:
        out.append(f"acronym soup ({len(ac)})")
    if s.count(":") >= 2:
        out.append("telegraph style (colons)")
    return out


def sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(])", text) if len(x.split()) >= 5]


def macros(tex_path):
    """Every \\newcommand reachable through \\input from the main file (paths resolve from the main file's folder, as LaTeX does)."""
    defs, seen, todo = {}, set(), [tex_path]
    while todo:
        f = todo.pop()
        if f in seen or not f.exists():
            continue
        seen.add(f)
        text = f.read_text()
        for name, val in re.findall(r"\\newcommand\{?\\(\w+)\}?\{((?:[^{}]|\{[^{}]*\})*)\}", text):
            defs[name] = val
        for m in re.findall(r"\\input\{([^}]+)\}", text):
            todo.append((tex_path.parent / (m if m.endswith(".tex") else m + ".tex")).resolve())
    return defs


def detex(s, defs):
    s = re.sub(r"(?<!\\)%.*", "", s)
    for _ in range(3):
        s = re.sub(r"\\(\w+)\{\}", lambda m: defs.get(m.group(1), m.group(0)), s)
        s = re.sub(r"\\(\w+)(?![\w{])", lambda m: defs.get(m.group(1), m.group(0)), s)
    s = re.sub(r"\\(mbox|textbf|emph|textit|text)\{([^}]*)\}", r"\2", s)
    s = re.sub(r"\\cite\w*\{[^}]*\}", "(cite)", s)
    s = re.sub(r"~?\\ref\{[^}]*\}", " N", s)
    s = s.replace("$-$", "-").replace("\\%", "%").replace("``", '"').replace("''", '"').replace("~", " ")
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    return re.sub(r"\\[a-zA-Z]+", "", s).replace("{", "").replace("}", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex", type=Path)
    ap.add_argument("--all", action="store_true", help="also scan the body from the built PDF next to the .tex")
    ap.add_argument("--max-abstract-numbers", type=int, default=3)
    a = ap.parse_args()
    src = a.tex.read_text()
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S)
    if not m:
        sys.exit(f"FATAL: no abstract in {a.tex}")
    abstract = sentences(detex(m.group(1), macros(a.tex)))
    rows, verdicts = [], []
    total_nums = sum(len(numbers(s)) for s in abstract)
    if total_nums > a.max_abstract_numbers:
        verdicts.append(f"abstract carries {total_nums} numbers (max {a.max_abstract_numbers}): keep the 2-3 that carry the claim, move the rest to the body")
    if numbers(abstract[0]) or len(set(re.findall(r"\b[A-Z]{2,}\w*\b", abstract[0]))) >= 2:
        verdicts.append("sentence 1 is a spec, not a problem: open with why a reader should care")
    if not re.search(FINDING_VERBS, " ".join(abstract[:3]), re.I):
        verdicts.append("no finding stated as a finding in sentences 1-3 (we show / we find / surprisingly / only ...)")
    if numbers(abstract[-1]) and not re.search(IMPLICATION, abstract[-1], re.I):
        verdicts.append("last sentence ends on a number, not on why it matters")
    hedges = sum(len([x for x in HEDGES if x in s.lower()]) for s in abstract)
    if hedges >= 4:
        verdicts.append(f"abstract hedges {hedges} times: state the claim once, put the caveats in the body")
    for i, s in enumerate(abstract, 1):
        sig = signals(s, True)
        if sig:
            rows.append((f"abstract s{i}", sig, s))
    body_n = 0
    if a.all:
        pdf = a.tex.with_suffix(".pdf")
        if not pdf.exists():
            sys.exit(f"FATAL: --all needs the built PDF {pdf}")
        txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
        txt = txt.split("\nReferences\n")[0]
        if "Introduction\n" in txt:
            txt = txt[txt.index("Introduction\n"):]
        txt = re.sub(r"-\n(?=[a-z])", "", txt)
        paras = [p for p in re.split(r"\n\s*\n", txt) if len(p.split()) >= 25]
        start = next((i for i, p in enumerate(paras) if "Introduction" in p[:40]), 0)
        for p in paras[start:]:
            for s in sentences(p):
                toks = s.split()
                if sum(bool(re.search(r"\\d", t)) for t in toks) > 0.4 * len(toks):
                    continue  # a table row, not prose
                body_n += 1
                sig = signals(s, False)
                if len(sig) >= 2:
                    rows.append(("body", sig, s))
    print(f"\nROBOTIC-TONE AUDIT: {a.tex}")
    print(f"abstract: {len(abstract)} sentences, {total_nums} numbers; flagged {sum(r[0].startswith('abstract') for r in rows)}"
          + (f"; body: {body_n} sentences, flagged {sum(r[0] == 'body' for r in rows)}" if a.all else ""))
    for v in verdicts:
        print(f"  ABSTRACT: {v}")
    print(f"\n{'where':12s} | {'why it reads as a report':58s} | sentence")
    print("-" * 140)
    for where, sig, s in rows:
        print(f"{where:12s} | {'; '.join(sig)[:58]:58s} | {s[:150]}{'...' if len(s) > 150 else ''}")
    flagged = sum(r[0].startswith("abstract") for r in rows)
    robotic = bool(verdicts) or flagged * 2 > len(abstract)
    print(f"\nVERDICT: {'ROBOTIC: rewrite the flagged lines, then run the fresh-judge veto' if robotic else 'passes the counted checks: still run the fresh-judge veto'}")
    sys.exit(1 if robotic else 0)


if __name__ == "__main__":
    main()
