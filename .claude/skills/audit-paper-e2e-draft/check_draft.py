"""End-to-end draft audit: tables, build log, PDF, cross-refs, numbers, claims, acronyms, sections, bib, plus the prose and version checkers.
    python3 .claude/skills/audit-paper-e2e-draft/check_draft.py Overleaf_draft/v6_AAAI27_SC4AI/0_main.tex --max-pages 8 --ref Overleaf_draft/v4_AAAI27_student_abstract/0_main_AAAI.tex
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_tables import audit as audit_tables, expand_inputs, strip_comment  # noqa: E402

AI_SIGNATURES = HERE.parent / "audit-ai-signatures" / "check_ai_signatures.py"
CONSISTENCY = Path.home() / ".claude" / "skills" / "paper-consistency" / "check_paper_consistency.py"
CLAIM_WORDS = r"\b(significant(ly)?|state[- ]of[- ]the[- ]art|SOTA|outperform(s|ed)?|prove[sn]?|guarantee[sd]?|always|never|clearly|dramatic(ally)?|substantial(ly)?)\b"
ACRONYM_OK = {"AI", "ML", "LLM", "LLMs", "GPU", "CPU", "URL", "PDF", "USA", "AAAI", "API", "PhD", "MS", "AoE", "HF", "II", "III", "IV",
              "MMLU", "GSM8K", "HumanEval"}  # benchmark names, not acronyms to spell out


def prose(text: str) -> str:
    """Document body without comments, math, citation/ref keys and command names (for word-level checks)."""
    body = text.split("\\begin{document}", 1)[-1]
    body = "\n".join(strip_comment(ln) for ln in body.split("\n"))
    body = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|\\\[.*?\\\]", " ", body, flags=re.S)
    body = re.sub(r"\\begin\{(equation|align)\*?\}.*?\\end\{\1\*?\}", " ", body, flags=re.S)
    body = re.sub(r"\\(cite[tp]?|ref|label|eqref|url|includegraphics|input|bibliography\w*)(\[[^\]]*\])?\{[^}]*\}", " ", body)
    return body


def section_text(text: str, start_pat: str, end_pat: str) -> str:
    m = re.search(start_pat, text)
    if not m:
        return ""
    rest = text[m.end():]
    e = re.search(end_pat, rest)
    return rest[:e.start()] if e else rest


def numbers(s: str):
    """Numbers a reader would check (decimals, percentages, integers >= 11), normalized ('3,000' -> '3000')."""
    s = re.sub(r"\\(v|h)space\{[^}]*\}|\[[\d.]+(pt|em|ex|in|cm|mm)\]", " ", s)
    out = set()
    for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+\.\d+|\d+)(?![\w])", s):
        v = m.group(1).replace(",", "")
        if "." in v or int(v) >= 11:
            out.add(v)
    return out


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def audit(tex: Path, a) -> list:
    R = []
    add = lambda area, check, status, detail: R.append((area, check, status, detail))
    text = expand_inputs(tex)
    body = prose(text)
    log, pdf, blg = tex.with_suffix(".log"), tex.with_suffix(".pdf"), tex.with_suffix(".blg")

    # 1. tables: bold winners under a declared rule, CI in every metric cell, caption says what bold means
    for name, check, status, detail in audit_tables(text):
        add("table " + name, check, status, detail)

    # 2. build log: errors, unresolved references, duplicate labels, overfull boxes
    if not log.exists() or not pdf.exists() or log.stat().st_mtime < tex.stat().st_mtime:
        add("build", "log", "FAIL", f"{log.name} or {pdf.name} missing or older than {tex.name}: rebuild first")
    else:
        L = log.read_text(errors="ignore")
        errs = len(re.findall(r"^! ", L, flags=re.M))
        undef = sorted(set(re.findall(r"(?:Citation|Reference) `([^']+)' on page \d+ undefined", L)))
        multi = sorted(set(re.findall(r"Label `([^']+)' multiply defined", L)))
        over = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*lines? (\d+)", L)
        add("build", "errors", "FAIL" if errs else "PASS", f"{errs} LaTeX error(s)")
        add("build", "undefined", "FAIL" if undef else "PASS", ", ".join(undef[:8]) or "every citation and reference resolves")
        add("build", "labels", "FAIL" if multi else "PASS", ", ".join(multi[:8]) or "no label defined twice")
        add("build", "overfull", "WARN" if over else "PASS", "; ".join(f"{w}pt at line {n}" for w, n in over[:5]) or "no overfull box")

    # 3. PDF: page budget, '??' from broken refs, em-dash glyphs (style files can insert them)
    if pdf.exists():
        rc, info = run(["pdfinfo", str(pdf)])
        pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)) if rc == 0 else 0
        ref_page = None
        for p in range(1, pages + 1):
            _, pg = run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"])
            lines = [ln.strip() for ln in pg.split("\n") if ln.strip()]
            if "References" in lines:
                ref_page = p - 1 if lines and lines[0] == "References" else p
                break
        _, full = run(["pdftotext", str(pdf), "-"])
        if a.max_pages:
            if ref_page is None:
                add("pdf", "pages", "WARN", f"no 'References' heading found; {pages} pages in total")
            else:
                add("pdf", "pages", "FAIL" if ref_page > a.max_pages else "PASS",
                    f"main text ends on page {ref_page} (limit {a.max_pages}); {pages} pages with references and appendix")
        qq = full.count("??")
        add("pdf", "?? marks", "FAIL" if qq else "PASS", f"{qq} '??' in the PDF text (broken \\ref or \\cite)" if qq else "none")
        em = full.count("\u2014")
        add("pdf", "em dash", "FAIL" if em else "PASS", f"{em} em-dash glyph(s) in the PDF (house rule; check style-file macros)" if em else "none")

    # 4. cross-references: every table, figure and appendix is referenced in the text; numbered equations are referenced
    labels = re.findall(r"\\label\{([^}]+)\}", "\n".join(strip_comment(ln) for ln in text.split("\n")))
    refs = set(re.findall(r"\\(?:ref|cref|Cref|autoref|eqref)\{([^}]+)\}", text))
    unref = [lb for lb in labels if lb not in refs and re.match(r"(tab|fig|app|sec|eq):", lb)]
    add("refs", "unreferenced", "WARN" if unref else "PASS", ", ".join(unref) or "every labeled table, figure, section and equation is referenced")
    eq_envs = re.findall(r"\\begin\{(equation|align)\}(.*?)\\end\{\1\}", text, flags=re.S)
    eq_unlab = sum(1 for _, b in eq_envs if "\\label" not in b)
    add("refs", "equation numbers", "WARN" if eq_unlab else "PASS",
        f"{eq_unlab} numbered equation block(s) without a label; number only equations the text refers to" if eq_unlab else "ok")

    # 5. numbers: every number in the abstract and conclusion appears in the rest of the paper
    abstract = section_text(text, r"\\begin\{abstract\}", r"\\end\{abstract\}")
    concl = section_text(text, r"\\section\*?\{Conclusions?\}", r"\\section|\\bibliography|\\appendix|\\end\{document\}")
    rest = text.replace(abstract, " ").replace(concl, " ")
    rest_nums = numbers(rest)
    for where, s in (("abstract", abstract), ("conclusion", concl)):
        miss = sorted(numbers(s) - rest_nums)
        add("numbers", where, "FAIL" if miss else "PASS", ("not found in the body or tables: " + ", ".join(miss)) if miss else "every number traced to the body")

    # 6. claims: overclaiming vocabulary (Lipton & Steinhardt 2018) for a human look at each use
    hits = {}
    for m in re.finditer(CLAIM_WORDS, re.sub(r"``.*?''", " ", body, flags=re.S), flags=re.I):
        hits.setdefault(m.group(1).lower(), 0)
        hits[m.group(1).lower()] += 1
    add("claims", "wording", "WARN" if hits else "PASS",
        ("read each use against its interval (--claims lists them): " + ", ".join(f"{k} x{v}" for k, v in sorted(hits.items(), key=lambda t: -t[1]))) if hits else "no overclaiming words")
    if a.claims:
        for ln_no, ln in enumerate(text.split("\n"), start=1):
            for m in re.finditer(CLAIM_WORDS, strip_comment(ln), flags=re.I):
                print(f"claim  line {ln_no:4d}  {m.group(1):12s}  ...{strip_comment(ln)[max(0, m.start() - 60):m.end() + 50].strip()}...")

    # 7. acronyms: every acronym is spelled out once, '(ACRONYM)' or 'ACRONYM (...)', before or at first use
    unquoted = re.sub(r"``.*?''", " ", body, flags=re.S)  # quoted contract or model text is not the authors' wording
    words = re.findall(r"(?<![\\\w-])([A-Z][A-Z0-9]{1,}[a-z]?s?)(?![\w-])", unquoted)
    seen, undefined = set(), []
    for w in words:
        base = w.rstrip("s") if w.endswith("s") and w[:-1].isupper() else w
        if base in seen or base in ACRONYM_OK:
            continue
        seen.add(base)
        named_and_cited = re.search(r"%s\)?[~\s]*\\cite" % re.escape(base), text)  # a method or benchmark name with its citation
        if not (named_and_cited or re.search(r"\(%s\)|%s \(|%s:\s" % ((re.escape(base),) * 3), body)):
            undefined.append(base)
    add("text", "acronyms", "WARN" if undefined else "PASS", ("never spelled out: " + ", ".join(undefined[:15])) if undefined else "all spelled out")

    # 8. required sections
    heads = [h.lower() for h in re.findall(r"\\section\*?\{([^}]+)\}", text)]
    for need, sev in (("limitation", "FAIL"), ("conclusion", "FAIL"), ("ethic", "WARN")):
        ok = any(need in h for h in heads)
        add("sections", need, "PASS" if ok else sev, "present" if ok else f"no section heading containing '{need}'")

    # 9. captions: self-contained (states what is shown) and says '95%' when the table carries intervals
    for env in re.findall(r"\\begin\{(?:table|figure)\*?\}.*?\\end\{(?:table|figure)\*?\}", text, flags=re.S):
        cap = re.search(r"\\caption\{(.*)\}\s*\\label\{([^}]+)\}", env, flags=re.S)
        if not cap:
            continue
        words_n = len(re.sub(r"\\\w+|[{}$]", " ", cap.group(1)).split())
        has_ci = "\\pm" in env or "\\tiny[" in env
        if words_n < 12:
            add("caption " + cap.group(2), "length", "WARN", f"{words_n} words; a caption should stand alone (what, metric, n)")
        if has_ci and "95" not in cap.group(1):
            add("caption " + cap.group(2), "interval", "WARN", "cells carry intervals but the caption does not say 95% or how they were computed")

    # 10. bibliography: cited keys exist with title and year; BibTeX warnings
    bibs = re.findall(r"\\bibliography\{([^}]+)\}", text)
    entries = {}
    for b in (bibs[0].split(",") if bibs else []):
        bp = (tex.parent / b.strip()).with_suffix(".bib")
        if bp.exists():
            for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", bp.read_text(), flags=re.S):
                entries[m.group(1)] = m.group(2)
    cited = set(k.strip() for grp in re.findall(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]+)\}", text) for k in grp.split(","))
    missing = sorted(k for k in cited if k not in entries)
    thin = sorted(k for k in cited if k in entries and not (re.search(r"\btitle\s*=", entries[k], re.I) and re.search(r"\byear\s*=", entries[k], re.I)))
    add("bib", "entries", "FAIL" if missing or thin else "PASS",
        "; ".join(filter(None, [("missing: " + ", ".join(missing)) if missing else "", ("no title or year: " + ", ".join(thin)) if thin else ""])) or f"{len(cited)} cited keys complete")
    if blg.exists():
        warns = re.findall(r"^Warning--(.*)$", blg.read_text(errors="ignore"), flags=re.M)
        add("bib", "bibtex", "WARN" if warns else "PASS", "; ".join(warns[:4]) or "no BibTeX warnings")

    # 11. anonymity (double-blind venues only)
    if a.double_blind:
        auth = section_text(text, r"\\author\{", r"\\affiliations|\\maketitle|\\begin\{document\}")
        links = re.findall(r"\\link\{[^}]*\}\{([^}]*)\}|\\url\{([^}]*)\}", text)
        leaks = [u for pair in links for u in pair if u and re.search(r"github\.com/[\w-]+|arxiv\.org/abs", u)]
        anon = "anonymous" in auth.lower()
        add("anonymity", "authors", "PASS" if anon else "FAIL", "anonymous" if anon else "author names are visible")
        add("anonymity", "links", "FAIL" if leaks else "PASS", ", ".join(leaks[:4]) or "no identifying links")

    # 12. prose (audit-ai-signatures) and versions (paper-consistency)
    if AI_SIGNATURES.exists():
        rc, out = run([sys.executable, str(AI_SIGNATURES), str(tex)])
        add("prose", "ai-signatures", "PASS" if rc == 0 else "FAIL", out.strip().split("\n")[-1])
    if a.ref:
        if not CONSISTENCY.exists():
            add("versions", "paper-consistency", "FAIL", f"{CONSISTENCY} not found")
        else:
            cmd = [sys.executable, str(CONSISTENCY), "--ref", str(Path(a.ref).resolve()), str(tex)]
            for f in a.forbid:
                cmd += ["--forbid", f]
            rc, out = run(cmd)
            mine = [r for r in out.split("\n") if r.startswith("\u2502") and tex.name in r]
            bad = [re.sub(r"\s+", " ", r).strip("\u2502 ") for r in mine if " FAIL " in r]
            add("versions", "paper-consistency", "FAIL" if bad else "PASS",
                "; ".join(bad)[:200] or f"title, authors and abstract numbers agree with {Path(a.ref).name}")
    return R


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("tex", help="main .tex of the draft (built PDF and log must sit next to it)")
    ap.add_argument("--max-pages", type=int, default=0, help="venue limit on main-text pages (references and appendix excluded)")
    ap.add_argument("--ref", help="reference version for paper-consistency (title, authors, abstract numbers)")
    ap.add_argument("--forbid", action="append", default=[], help="phrase withdrawn after review; passed to paper-consistency")
    ap.add_argument("--double-blind", action="store_true", help="venue reviews double-blind: check names and identifying links")
    ap.add_argument("--claims", action="store_true", help="print every overclaiming-word use with its line, for review")
    a = ap.parse_args()
    tex = Path(a.tex).resolve()
    rows = audit(tex, a)
    hdr = ("area", "check", "status", "detail")
    w = [max(len(str(r[k])) for r in rows + [hdr]) for k in range(4)]
    w[3] = min(w[3], 96)
    bar = lambda l, m, r: l + m.join("\u2500" * (x + 2) for x in w) + r
    print(f"draft: {tex.name}")
    print(bar("\u250c", "\u252c", "\u2510"))
    print("\u2502" + "\u2502".join(f" {h:<{w[k]}} " for k, h in enumerate(hdr)) + "\u2502")
    print(bar("\u251c", "\u253c", "\u2524"))
    for r in rows:
        print("\u2502" + "\u2502".join(f" {str(v)[:w[k]]:<{w[k]}} " for k, v in enumerate(r)) + "\u2502")
    print(bar("\u2514", "\u2534", "\u2518"))
    n = {s: sum(r[2] == s for r in rows) for s in ("FAIL", "WARN", "PASS")}
    print(f"RESULT: {'FAIL' if n['FAIL'] else 'PASS'}  ({n['FAIL']} FAIL, {n['WARN']} WARN, {n['PASS']} PASS)")
    sys.exit(1 if n["FAIL"] else 0)


if __name__ == "__main__":
    main()
