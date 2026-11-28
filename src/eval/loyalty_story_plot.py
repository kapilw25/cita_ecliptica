"""LoyalAgents Figure 1: (a) one request under two deployer contracts, SwiPO vs DPO, GRPO, PPO; (b) the hidden-sponsor exchange. CPU.
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
from src.utils.eval.first_turn import first_turn  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
P = CFG["loyalty_story_plot"]
PT = P["font_size"] / 72.0                      # one point of text height, in inches
LINE = PT * 1.22                                # line pitch
CHAR = PT * 0.43                                # mean glyph width of STIXGeneral, measured on the rendered page
PAD = 0.045
INK, RED, GREEN = "#1a1a1a", "#a3161a", "#1f6b2e"


def verbatim(pieces, source, what):
    """Join the excerpts with an ellipsis; FATAL if any piece is not a verbatim substring of the source."""
    for s in pieces:
        if s not in source:
            raise SystemExit(f"FATAL: excerpt not verbatim in {what}: {s!r}")
    return " … ".join(pieces)


def next_version(folder: Path, stem: str) -> Path:
    mine = list(folder.glob(f"v*_{stem}.png"))
    if mine:
        return mine[0].with_suffix("")
    used = [int(m.group(1)) for f in folder.glob("v*_*") if (m := re.match(r"v(\d+)_", f.name))]
    return folder / f"v{max(used, default=0) + 1}_{stem}"


def text_lines(ax, x, y_top, lines, bold_first=False, color=INK, size=None):
    for i, ln in enumerate(lines):
        ax.text(x, y_top - (i + 0.8) * LINE, ln, fontsize=size or P["font_size"], color=color,
                fontweight="bold" if (bold_first and i == 0) else "normal")


def box(ax, x, y_top, w, text, face, edge, bold_head=None, ls="-"):
    """Draw a wrapped text box whose top edge is y_top; return its height."""
    lines = ([bold_head] if bold_head else []) + textwrap.wrap(text, max(10, int((w - 2 * PAD) / CHAR)))
    h = len(lines) * LINE + 2 * PAD
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h, boxstyle="round,pad=0,rounding_size=0.04",
                                facecolor=face, edgecolor=edge, linewidth=0.7, linestyle=ls))
    text_lines(ax, x + PAD, y_top - PAD, lines, bold_first=bool(bold_head))
    return h


def panel_switch(ax, W, y):
    """(a) One Conditional Safety request under the strict and the permissive contract, first turn of each model."""
    S = P["switch"]
    rows = []
    for label, key in S["models"].items():
        cells = []
        for arm in ("strict", "permissive"):
            ans = pd.read_csv(project_root / S["answers_dir"] / key / f"{arm}_responses.csv").set_index("prompt_idx")
            lab = pd.read_csv(project_root / S["labels_dir"] / key / f"{arm}.csv").set_index("prompt_idx")
            words = first_turn(ans.loc[S["item"], "response"]).split()
            if len(words) == 0:
                raise SystemExit(f"FATAL: empty first turn for {key} {arm} item {S['item']}")
            cells.append((" ".join(words[:S["snippet_words"]]) + "\u00a0\u2026", int(lab.loc[S["item"], "is_refusal_judge"])))
        rows.append((label, cells))
    request = ans.loc[S["item"], "prompt"]
    h = box(ax, 0.02, y, W - 0.04, request, "#dbe9f7", "#4a78a8", bold_head="(a) One request, two deployer contracts")
    y -= h + 0.05
    lab_w, gap = 0.44, 0.04
    cw = (W - 0.04 - lab_w - gap) / 2
    full = int((cw - 2 * PAD) / CHAR)
    heads = [textwrap.wrap(f"{arm.capitalize()}: “{S['contracts'][arm]}”", full) for arm in ("strict", "permissive")]
    for j, head in enumerate(heads):
        text_lines(ax, 0.02 + lab_w + j * (cw + gap) + PAD, y, head, color="#444444")
    y -= max(len(h) for h in heads) * LINE + 0.02
    renderer = ax.figure.canvas.get_renderer()
    for label, cells in rows:
        laid = []
        for t, r in cells:                       # tag in color, then the snippet; the first line is shortened by the tag's width
            tag = "REFUSES" if r else "HELPS"
            probe = ax.text(0, 0, tag, fontsize=P["font_size"], fontweight="bold")
            tag_w = probe.get_window_extent(renderer=renderer).width / ax.figure.dpi + 0.03
            probe.remove()
            first = textwrap.wrap(t, max(6, int((cw - 2 * PAD - tag_w) / CHAR)))[0]
            rest = textwrap.wrap(t[len(first):].strip(), full) if len(first) < len(t) else []
            laid.append((tag, r, tag_w, first, rest))
        h = max(1 + len(c[4]) for c in laid) * LINE + 2 * PAD
        ours = label.startswith("SwiPO")
        text_lines(ax, 0.02, y - PAD, label.split(" "), bold_first=True)
        for j, (tag, r, tag_w, first, rest) in enumerate(laid):
            x = 0.02 + lab_w + j * (cw + gap)
            ax.add_patch(FancyBboxPatch((x, y - h), cw, h, boxstyle="round,pad=0,rounding_size=0.04",
                                        facecolor="#fbeed5" if ours else "#f4f4f4", edgecolor="#b07a1e" if ours else "#999999",
                                        linewidth=0.9 if ours else 0.6))
            ax.text(x + PAD, y - PAD - 0.8 * LINE, tag, fontsize=P["font_size"], fontweight="bold", color=RED if r else GREEN)
            ax.text(x + PAD + tag_w, y - PAD - 0.8 * LINE, first, fontsize=P["font_size"], fontweight="normal", color=INK)
            text_lines(ax, x + PAD, y - PAD - LINE, rest)
        y -= h + 0.03
    return y


def panel_sponsor(ax, W, y):
    """(b) The prompted Llama-3.1-8B-Instruct under the hidden-sponsor contract, then the paid-or-not follow-up."""
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
    y -= box(ax, 0.02, y, W - 0.04, f"“{contract}”", "#eeeeee", "#555555",
             bold_head="(b) A hidden sponsor: deployer’s system message, unseen by the user", ls="--") + 0.045
    bw, uw = 2.5, 2.3
    tag_x = 0.02 + bw + 0.05
    for who, text, tag in [("user", row.prompt, None), ("agent", first, "promotes the sponsor"),
                           ("user", setup["followup"], None), ("agent", reply, "denies the deal")]:
        if who == "user":
            h = box(ax, W - 0.02 - uw, y, uw, text, "#dbe9f7", "#4a78a8")
        else:
            h = box(ax, 0.02, y, bw, text, "#fbeed5", "#b07a1e")
            for i, ln in enumerate(textwrap.wrap(tag, max(6, int((W - tag_x - 0.02) / CHAR)))):
                ax.text(tag_x, y - h / 2 + (0.5 - i) * LINE, ln, fontsize=P["font_size"], color=RED, fontweight="bold",
                        va="center")
        y -= h + 0.03
    return y


def main():
    plt.rcParams.update({"font.family": P["font_family"], "mathtext.fontset": "stix"})
    W, H0 = P["figsize_w"], 9.0
    fig = plt.figure(figsize=(W, H0))
    ax = fig.add_axes([0, 0, 1, 1])
    y = panel_switch(ax, W, H0 - 0.02) - 0.06
    y = panel_sponsor(ax, W, y) + 0.02
    ax.set_xlim(0, W)
    ax.set_ylim(y, H0)
    ax.axis("off")
    fig.set_size_inches(W, H0 - y)
    ax.set_position([0, 0, 1, 1])
    stem = next_version(project_root / P["dir"], P["stem"])
    for ext in ("png", "pdf"):
        fig.savefig(f"{stem}.{ext}", dpi=P["dpi"], facecolor="white")
    print(f"wrote {stem}.png and {stem}.pdf ({W:.2f} x {H0 - y:.2f} in)")


if __name__ == "__main__":
    main()
