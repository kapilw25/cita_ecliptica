"""naming-prefix check (2026-10-19): files whose name holds a kind word anywhere but first.

    python3 .claude/skills/naming-prefix/check_prefix.py <folder> [<folder> ...]
"""
import os
import re
import sys

KINDS = ("log", "jobs", "plan", "audit", "sheet", "run", "tracker")


def main():
    hits = 0
    for root in sys.argv[1:] or ["."]:
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x != "legacy" and not x.startswith(".")]
            for n in files + dirs:
                stem = os.path.splitext(n)[0]
                if re.match(r"^(v\d+|p\d+|\d+)_", stem):
                    continue                              # a skill's number scheme comes first
                parts = re.split(r"[_\-]", stem.lower())
                for k in KINDS:
                    if k in parts[1:] and parts[0] != k:
                        rest = [p for p in parts if p != k]
                        print(f"{os.path.join(d, n)}: kind '{k}' not first -> {k}_{'_'.join(rest)}{os.path.splitext(n)[1]}")
                        hits += 1
                        break
    print("OK: every kind word comes first" if not hits else f"{hits} name(s) to fix")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
