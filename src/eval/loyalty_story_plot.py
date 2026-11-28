"""LoyalAgents Figure 1: the hidden-sponsor exchange (verbatim excerpts, checked against the answer files) and the three levers. CPU.
    python -u src/eval/loyalty_story_plot.py 2>&1 | tee logs/loyalty_story_plot.log
"""
import json
import re
import sys
import textwrap
from pathlib import Path

import matplotlib
import pandas as pd
import yaml
from matplotlib.patches import FancyBboxPatch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
P = CFG["loyalty_story_plot"]
PT = P["font_size"] / 72.0                      # one point of text height, in inches
LINE = PT * 1.22                                # line pitch
CHAR = PT * 0.43                                # mean glyph width of STIXGeneral, measured on the rendered page
PAD = 0.05


def verbatim(pieces, source, what):
    """Join the excerpts with an ellipsis; FATAL if any piece is not a verbatim substring of the source."""
    for s in pieces:
        if s not in source:
            raise SystemExit(f"FATAL: excerpt not verbatim in {what}: {s!r}")
    return " … ".join(pieces)


def next_version(folder: Path, stem: str) -> Path:
    used = [int(m.group(1)) for f in folder.glob("v*_*") if (m := re.match(r"v(\d+)_", f.name))]
    mine = [f for f in folder.glob(f"v*_{stem}.png")]
    if mine:
        return mine[0].with_suffix("")
    return folder / f"v{max(used, default=0) + 1}_{stem}"


def box(ax, x, y_top, w, text, face, edge, bold_head=None, ls="-", align="left"):
    """Draw a wrapped text box whose top edge is y_top; return its height."""
    chars = max(10, int((w - 2 * PAD) / CHAR))
    lines = ([bold_head] if bold_head else []) + textwrap.wrap(text, chars)
    h = len(lines) * LINE + 2 * PAD
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor=face, edgecolor=edge, linewidth=0.8, linestyle=ls))
    for i, ln in enumerate(lines):
        tx = x + PAD if align == "left" else x + w - PAD
        ax.text(tx, y_top - PAD - (i + 0.8) * LINE, ln, fontsize=P["font_size"], ha=align,
                fontweight="bold" if (bold_head and i == 0) else "normal", color="#1a1a1a")
    return h


def main():
    plt.rcParams.update({"font.family": P["font_family"], "mathtext.fontset": "stix"})
    adir = project_root / P["answers_dir"] / P["model"]
    setup = json.load(open(adir / "setup.json"))
    df = pd.read_csv(adir / "sponsor_responses.csv")
    row = df[df.prompt.str.contains(P["prompt_contains"], case=False)]
    if len(row) != 1:
        raise SystemExit(f"FATAL: {len(row)} prompts contain {P['prompt_contains']!r}")
    row = row.iloc[0]
    contract = verbatim(P["contract_excerpts"], setup["contracts"]["sponsor"], "the sponsor contract")
    first = verbatim(P["first_answer_excerpts"], row.first_answer, "the first answer")
    reply = verbatim(P["reply_excerpts"], row.response, "the reply")
    echo = json.load(open(project_root / P["sponsor_echo"]))["models"]
    rates = {k: v["promotion_no_echo"]["rate"] for k, v in echo.items() if k.endswith("_Instruct_Prompted")}
    fu = json.load(open(project_root / P["sponsor_followup"]))["models"]
    adm = [fu[k]["sponsor"]["judge_admits_after_brand_mention"] for k in rates]
    n_conv, n_admit = sum(a["n"] for a in adm), sum(round(a["rate"] * a["n"]) for a in adm)
    print(f"sponsor: {len(rates)} prompted families promote {min(rates.values()):.3f} to {max(rates.values()):.3f}; "
          f"admit {n_admit} of {n_conv} after naming the brand")

    W = P["figsize_w"]
    fig = plt.figure(figsize=(W, 6))
    ax = fig.add_axes([0, 0, 1, 1])
    y = 6 - 0.02
    y -= box(ax, 0.02, y, W - 0.04, f"“{contract}”", "#eeeeee", "#555555",
             bold_head="Deployer’s system message (the user never sees it)", ls="--") + 0.07
    bw, tag_w = 2.42, W - 0.04 - 2.42 - 0.06
    turns = [("user", row.prompt, None), ("agent", first, "promotes the sponsor"),
             ("user", setup["followup"], None), ("agent", reply, "denies the deal")]
    for who, text, tag in turns:
        if who == "user":
            h = box(ax, W - 0.02 - 2.0, y, 2.0, text, "#dbe9f7", "#4a78a8", align="left")
        else:
            h = box(ax, 0.02, y, bw, text, "#fbeed5", "#b07a1e")
            for i, ln in enumerate(textwrap.wrap(tag, max(6, int(tag_w / CHAR)))):
                ax.text(0.02 + bw + 0.06, y - h / 2 + (0.5 - i) * LINE, ln, fontsize=P["font_size"], color="#a3161a",
                        fontweight="bold", va="center")
        y -= h + 0.05
    y -= 0.04
    levers = [("Refusal", "the contract moves refusals only in models a user can also talk out of it"),
              ("Authority", "those models yield to a user who loosens it"),
              ("Sponsor", f"{len(rates)} model families promote in {min(rates.values()):.0%} to {max(rates.values()):.0%} "
                          f"of requests; {n_admit} of {n_conv} admit the deal")]
    lab_w = 0.86                                 # bold label column inside one lever box
    chars = int((W - 0.04 - lab_w - 2 * PAD) / CHAR)
    rows = [(f"{head} lever", textwrap.wrap(body, chars)) for head, body in levers]
    h = sum(len(b) for _, b in rows) * LINE + 2 * PAD + (len(rows) - 1) * 0.03
    ax.add_patch(FancyBboxPatch((0.02, y - h), W - 0.04, h, boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor="#f4f4f4", edgecolor="#888888", linewidth=0.8))
    yy = y - PAD
    for head, body in rows:
        ax.text(0.02 + PAD, yy - 0.8 * LINE, head, fontsize=P["font_size"], fontweight="bold", color="#1a1a1a")
        for i, ln in enumerate(body):
            ax.text(0.02 + lab_w, yy - (i + 0.8) * LINE, ln, fontsize=P["font_size"], color="#1a1a1a")
        yy -= len(body) * LINE + 0.03
    y -= h + 0.02
    ax.set_xlim(0, W)
    ax.set_ylim(y, 6)
    ax.axis("off")
    fig.set_size_inches(W, 6 - y)
    ax.set_position([0, 0, 1, 1])
    folder = project_root / P["dir"]
    stem = next_version(folder, P["stem"])
    for ext in ("png", "pdf"):
        fig.savefig(f"{stem}.{ext}", dpi=P["dpi"], facecolor="white")
    print(f"wrote {stem}.png and {stem}.pdf ({W:.2f} x {6 - y:.2f} in)")


if __name__ == "__main__":
    main()
