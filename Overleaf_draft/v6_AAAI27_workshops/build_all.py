"""Rebuild every unfrozen venue draft (paper-variants skill): numbers from JSON, latexmk, e2e audit at the venue page limit, drift and number gates.
    python3 Overleaf_draft/v6_AAAI27_workshops/build_all.py 2>&1 | tee logs/build_all_drafts.log
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_numbers  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = HERE / "common"
AUDIT = ROOT / ".claude/skills/audit-paper-e2e-draft/check_draft.py"
TEMPLATE_FILES = {"aaai2027.sty", "aaai2027.bst", "0_main.tex", "venue.tex", "FROZEN"}
MIN_WORDS = 40  # a venue paragraph this long, identical to one in common/, was pasted instead of \input
TYPED = re.compile(r"\d\.\d{2,}")  # a decimal number typed in a venue file instead of a common/numbers.tex macro


def paragraphs(text: str) -> set:
    body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("%"))
    return {" ".join(p.split()) for p in re.split(r"\n\s*\n", body) if len(p.split()) >= MIN_WORDS}


def drift(venue: Path) -> list:
    common_names = {p.name for p in COMMON.rglob("*") if p.is_file()}
    hits = [f"stale copy {p.name}" for p in venue.rglob("*") if p.is_file() and p.name in common_names
            and p.name not in TEMPLATE_FILES]
    shared = set().union(*(paragraphs(p.read_text()) for p in COMMON.glob("*.tex")))
    pasted = paragraphs((venue / "0_main.tex").read_text()) & shared
    typed = [m.group() for line in (venue / "0_main.tex").read_text().splitlines() if not line.lstrip().startswith("%")
             for m in TYPED.finditer(line.partition(" % ")[0])]
    return hits + [f"pasted paragraph: {p[:60]}..." for p in pasted] + [f"typed number {t} (use a common/numbers.tex macro)" for t in typed]


def venue_info(venue: Path) -> dict:
    v = (venue / "venue.tex").read_text()  # FileNotFoundError is the intended crash: an unfrozen draft needs its switches
    m = re.search(r"^% pages: (\d+)", v, re.M)
    if not m:
        raise RuntimeError(f"{venue.name}/venue.tex has no '% pages: N' line")
    return {"pages": int(m.group(1)), "anon": "\\anontrue" in v}


def main():
    make_numbers.main()  # regenerate common/numbers.tex; exits if an abstract or conclusion number is missing from the body
    drafts = sorted(d for d in HERE.glob("v*_*") if (d / "0_main.tex").exists())
    rows, failed = [], 0
    for d in drafts:
        if (d / "FROZEN").exists():
            pdf = d / "0_main.pdf"
            sha = hashlib.sha256(pdf.read_bytes()).hexdigest()[:12] if pdf.exists() else "no pdf"
            rows.append((d.name, "🔒 frozen", "-", "-", "-", sha))
            continue
        info = venue_info(d)
        print(f"== {d.name}: building (limit {info['pages']} pages, {'double' if info['anon'] else 'single'}-blind)", flush=True)
        b = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-silent", "0_main.tex"], cwd=d,
                           capture_output=True, text=True)
        build = "✅" if b.returncode == 0 else f"❌ latexmk {b.returncode}"
        cmd = [sys.executable, str(AUDIT), str(d / "0_main.tex"), "--max-pages", str(info["pages"])]
        a = subprocess.run(cmd + (["--double-blind"] if info["anon"] else []), capture_output=True, text=True)
        res = re.search(r"RESULT: (\w+)\s+\((\d+) FAIL, (\d+) WARN", a.stdout)
        audit = f"{'✅' if res and res.group(1) == 'PASS' else '❌'} {res.group(2)} FAIL {res.group(3)} WARN" if res else "❌ no result"
        if res and res.group(1) != "PASS":
            print("\n".join(line for line in a.stdout.splitlines() if "FAIL" in line), flush=True)
        dr = drift(d)
        for h in dr:
            print(f"   drift: {h}", flush=True)
        pages = subprocess.run(["pdfinfo", str(d / "0_main.pdf")], capture_output=True, text=True).stdout
        npages = re.search(r"Pages:\s+(\d+)", pages).group(1) if "Pages" in pages else "?"
        ok = b.returncode == 0 and res is not None and res.group(1) == "PASS" and not dr
        failed += not ok
        rows.append((d.name, build, audit, "✅" if not dr else f"❌ {len(dr)}", npages, "PASS" if ok else "FAIL"))
    w = [max(len(str(r[i])) for r in rows + [("draft", "build", "audit", "drift", "pdf pages", "result")]) for i in range(6)]
    for r in [("draft", "build", "audit", "drift", "pdf pages", "result")] + rows:
        print(" | ".join(str(x).ljust(w[i]) for i, x in enumerate(r)))
    if failed:
        sys.exit(f"{failed} unfrozen draft(s) failed")


if __name__ == "__main__":
    main()
