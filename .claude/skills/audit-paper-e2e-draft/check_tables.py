"""Audit every LaTeX tabular for missing or wrong bold winners, missing 95% CIs, and captions that never say what bold means.
    python3 .claude/skills/audit-paper-e2e-draft/check_tables.py Overleaf_draft/v6_AAAI27_SC4AI/0_main.tex   (also run by check_draft.py)
"""

import re
import sys
from pathlib import Path

RULE_CMDS = re.compile(r"\\(toprule|bottomrule|hline)\b|(?<!c)\\midrule\b|\\cmidrule(\([^)]*\))?\{[^}]*\}|\\addlinespace(\[[^\]]*\])?")
NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)")


def expand_inputs(path: Path, seen=None) -> str:
    """Inline every \\input{...} (relative to the main file's folder), like the other paper checkers."""
    seen = seen or set()
    if path in seen:
        raise RuntimeError(f"\\input cycle at {path}")
    seen.add(path)
    text = path.read_text()

    def sub(m):
        p = path.parent / m.group(1)
        p = p if p.suffix else p.with_suffix(".tex")
        return expand_inputs(p, seen) if p.exists() else m.group(0)
    return re.sub(r"^[^%\n]*?\\input\{([^}]+)\}", lambda m: m.group(0).replace(m.group(0), sub(m)), text, flags=re.M)


def strip_comment(line: str) -> str:
    return re.split(r"(?<!\\)%", line, maxsplit=1)[0]


def cell_value(cell: str):
    """(value, decimals) of the number a cell starts with, ignoring bold, CI suffixes and math signs; None if not numeric."""
    s = re.sub(r"\{\\tiny[^{}]*\}", "", cell)
    s = s.replace("\\textbf{", "").replace("$-$", "-").replace("$+$", "+").replace("{", "").replace("}", "")
    s = s.replace("$", "").strip()
    m = NUM.match(s)
    if not m:
        return None
    txt = m.group(0)
    return float(txt), (len(txt.split(".")[1]) if "." in txt else 0)


def parse_rules(text: str):
    """'row max cols=2-6; col min cols=5 rows=\\ast' -> list of dicts."""
    rules = []
    for part in [p.strip() for p in text.split(";") if p.strip()]:
        m = re.match(r"(row|col)\s+(max|min)\s+cols=([\d,\-]+)(?:\s+rows=(\S+))?$", part)
        if not m:
            raise RuntimeError(f"unparsable bold rule: '{part}'")
        cols = []
        for tok in m.group(3).split(","):
            a, _, b = tok.partition("-")
            cols += list(range(int(a), int(b or a) + 1))
        rules.append({"axis": m.group(1), "mode": m.group(2), "cols": cols, "rows": m.group(4)})
    return rules


def row_selected(rule, i, row):
    sel = rule["rows"]
    if sel is None:
        return True
    if re.fullmatch(r"\d+(-\d+)?(,\d+(-\d+)?)*", sel):  # body-row numbers, e.g. rows=1-8,11-12
        for tok in sel.split(","):
            a, _, b = tok.partition("-")
            if int(a) <= i + 1 <= int(b or a):
                return True
        return False
    return sel in row[0]


def audit(text: str):
    findings = []
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines) if re.search(r"\\begin\{tabular\*?\}", strip_comment(ln))]
    for s in starts:
        # annotations: '% bold:' / '% ci:' comment lines between the enclosing \begin{table} (or 8 lines up) and \begin{tabular}
        lo = s
        while lo > 0 and s - lo < 12 and not re.search(r"\\begin\{table\*?\}", lines[lo]):
            lo -= 1
        ann = {k: None for k in ("bold", "ci")}
        for ln in lines[lo:s]:
            m = re.match(r"\s*%\s*(bold|ci):\s*(.*)$", ln)
            if m:
                ann[m.group(1)] = m.group(2).strip()
        e = next(i for i in range(s, len(lines)) if re.search(r"\\end\{tabular\*?\}", strip_comment(lines[i])))
        tail = "\n".join(lines[e:e + 30])
        label = re.search(r"\\label\{([^}]+)\}", tail)
        caption = re.search(r"\\caption\{(.*)", tail)
        name = label.group(1) if label else f"line {s + 1}"
        body_txt = "\n".join(strip_comment(ln) for ln in lines[s + 1:e])
        body_txt = body_txt.split("\\bottomrule")[0]  # note rows after \bottomrule are not data
        chunks = re.split(r"\\\\(?:\[[^\]]*\])?", body_txt)
        header, rows, in_body = [], [], False
        has_midrule = bool(re.search(r"(?<!c)\\midrule", body_txt))
        for ch in chunks:
            if re.search(r"(?<!c)\\midrule", ch):
                in_body = True
            clean = RULE_CMDS.sub("", ch).strip()
            if not clean:
                continue
            cells = [c.strip() for c in re.split(r"(?<!\\)&", clean)]
            (rows if (in_body or not has_midrule and header) else header).append(cells)
        numeric_rows = [r for r in rows if sum(cell_value(c) is not None and "." in c for c in r[1:]) >= 2]
        is_comparison = len(numeric_rows) >= 2
        bold_cells = {(i, j) for i, r in enumerate(rows) for j, c in enumerate(r) if "\\textbf" in c}
        if ann["bold"] is None:
            if is_comparison:
                findings.append((name, "bold", "FAIL", "numeric comparison table with no '% bold:' rule above \\begin{tabular}"))
            continue
        if ann["bold"].startswith("none"):
            if bold_cells:
                findings.append((name, "bold", "FAIL", f"rule says none but {len(bold_cells)} bold cell(s) present"))
            else:
                findings.append((name, "bold", "PASS", ann["bold"]))
        else:
            expected, covered = set(), set()
            for rule in parse_rules(ann["bold"]):
                pick = max if rule["mode"] == "max" else min
                groups = []
                if rule["axis"] == "row":
                    for i, r in enumerate(rows):
                        if row_selected(rule, i, r):
                            groups.append([(i, j) for j in rule["cols"] if j - 1 < len(r)])
                else:
                    for j in rule["cols"]:
                        groups.append([(i, j) for i, r in enumerate(rows) if row_selected(rule, i, r) and j - 1 < len(r)])
                for g in groups:
                    vals = {(i, j): cell_value(rows[i][j - 1]) for i, j in g}
                    vals = {k: v for k, v in vals.items() if v is not None}
                    covered |= set(vals)
                    if len(vals) < 2:
                        continue
                    best = pick(round(v, d) for v, d in vals.values())
                    expected |= {k for k, (v, d) in vals.items() if round(v, d) == best}
            actual = {(i, j + 1) for i, j in bold_cells}
            missing, wrong, outside = expected - actual, (actual & covered) - expected, actual - covered
            show = lambda ks: ", ".join(f"r{i + 1}c{j}={cell_value(rows[i][j - 1])[0]:g}" for i, j in sorted(ks)[:6])
            if missing:
                findings.append((name, "bold", "FAIL", f"{len(missing)} winner(s) not bold: {show(missing)}"))
            if wrong:
                findings.append((name, "bold", "FAIL", f"{len(wrong)} bold cell(s) are not the winner: {show(wrong)}"))
            if outside:
                findings.append((name, "bold", "FAIL", f"{len(outside)} bold cell(s) outside the declared rule: {show(outside)}"))
            if not (missing or wrong or outside):
                findings.append((name, "bold", "PASS", f"{len(expected)} winner(s) bold; rule: {ann['bold']}"))
            if bold_cells and not (caption and re.search(r"[Bb]old", caption.group(1))):
                findings.append((name, "caption", "WARN", "table has bold cells but the caption never says what bold means"))
        no_ci = [(i, j) for i, r in enumerate(rows) for j, c in enumerate(r[1:], start=2)
                 if cell_value(c) is not None and "." in c and "\\pm" not in c and "\\tiny[" not in c]
        if no_ci and ann["ci"] is None:
            findings.append((name, "ci", "WARN", f"{len(no_ci)} metric cell(s) without a 95% CI ({{\\tiny$\\pm$..}} or {{\\tiny[..]}}); "
                             "add one or declare '% ci: <reason>'"))
        elif no_ci:
            findings.append((name, "ci", "PASS", f"{len(no_ci)} cell(s) exempt: {ann['ci']}"))
    return findings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    rows = []
    for arg in sys.argv[1:]:
        p = Path(arg).resolve()
        rows += [(p.name,) + f for f in audit(expand_inputs(p))]
    w = [max(len(str(r[k])) for r in rows + [("file", "table", "check", "status", "detail")]) for k in range(5)]
    w[4] = min(w[4], 90)
    bar = lambda l, m, r: l + m.join("─" * (x + 2) for x in w) + r
    print(bar("┌", "┬", "┐"))
    print("│" + "│".join(f" {h:<{w[k]}} " for k, h in enumerate(("file", "table", "check", "status", "detail"))) + "│")
    print(bar("├", "┼", "┤"))
    for r in rows:
        print("│" + "│".join(f" {str(v)[:w[k]]:<{w[k]}} " for k, v in enumerate(r)) + "│")
    print(bar("└", "┴", "┘"))
    fail = any(r[3] == "FAIL" for r in rows)
    print("RESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
