"""Figure 1 of the as-trained paper: adapter-stack diagram (as trained vs as loaded) + refusal gap per model under both loadings, 95% BCa whiskers. CPU-only.
    python -u src/eval/loading_teaser_plot.py 2>&1 | tee logs/loading_teaser_plot.log
    python -u src/eval/loading_teaser_plot.py --layout column 2>&1 | tee logs/loading_teaser_plot_column.log
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Patch  # noqa: E402
from tqdm import tqdm  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.eval.plotting import get_model_color, save_figure_dual_format  # noqa: E402
from src.utils.eval.display_names import get_display_names  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
GAP_JSON = project_root / CFG["paths"]["evaluation_dir"] / "contract_gap" / "astrained_conditional_safety.json"
CHAIN_JSON = project_root / CFG["paths"]["evaluation_dir"] / "contract_gap" / "chain_final_only_pair.json"  # SwiPO-S pair
OUT_DIR = project_root / CFG["paths"]["evaluation_dir"] / "contract_gap" / "figures"
STEMS = {"wide": "v1_loading_teaser", "column": "v2_loading_teaser_column"}  # plot-standards rule 11: version prefix per figure
TRAINERS = CFG["score_table"]["trainers"]
NAME = get_display_names()
FS = 14  # plot-standards rule 7: at least 12 pt bold (printed at about half size across the page)
GREEN, RED, GREY = "#157f4b", "#cf2a2a", "#8a8f98"


def box(ax, x, y, w, h, text, edge, fill, dashed=False, color="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.03", linewidth=2,
                                edgecolor=edge, facecolor=fill, linestyle="--" if dashed else "-"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=FS - 2, fontweight="bold", color=color, linespacing=1.1)


def diagram(ax):
    """Two rows: as trained (parent merged, then own adapter) vs as loaded in earlier versions (parent missing)."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    rows = [(0.56, "As trained", GREEN, False), (0.08, "Final adapter only (parent missing)", RED, True)]
    for y, label, color, missing in rows:
        ax.add_patch(FancyBboxPatch((0.0, y - 0.03), 1.0, 0.40, boxstyle="round,pad=0.0,rounding_size=0.04",
                                    linewidth=2.5, edgecolor=color, facecolor="none"))
        ax.text(0.02, y + 0.33, label, ha="left", va="top", fontsize=FS, fontweight="bold", color=color)
        box(ax, 0.03, y, 0.27, 0.20, "Llama 3.1\n8B base", "black", "#eceef2")
        if missing:
            box(ax, 0.365, y, 0.27, 0.20, "parent\nmissing", GREY, "white", dashed=True, color=GREY)
        else:
            box(ax, 0.365, y, 0.27, 0.20, "+ parent\nadapter", "black", "#d9f3e5")
        box(ax, 0.70, y, 0.27, 0.20, "+ own\nadapter", "black", "#fff2cc")
        for x0 in (0.30, 0.635):
            ax.annotate("", xy=(x0 + 0.065, y + 0.10), xytext=(x0, y + 0.10),
                        arrowprops=dict(arrowstyle="->", lw=2, color="black"))
    ax.text(0.5, -0.06, "parent: SFT; SwiPO-R: DPO; SwiPO-S: SFT + DPO", ha="center", va="top",
            fontsize=FS - 2, fontweight="bold", color="#3a3f47")


def pairs():
    """(label, final-adapter-only key, as-trained key) per model; SwiPO-R = as released, SwiPO-S = intended chain."""
    out = [(NAME.get(t, t) + ("-R" if t == "CITA" else ""), f"{t}_Instruct", f"{t}_Instruct_AsTrained") for t in TRAINERS]
    return out + [("SwiPO-S", "CITA_Instruct_Chain_FinalOnly", "CITA_Instruct_Chain")]


def bars(ax, data):
    """Grouped bars per model: hatched = final adapter only (reference arm), solid = as trained; sorted by as-trained gap, largest right."""
    order = sorted(pairs(), key=lambda p: data[p[2]]["score"])
    x = np.arange(len(order))
    w = 0.38
    for i, (label, before_key, after_key) in enumerate(tqdm(order, desc="loading_teaser_plot", unit="model")):
        color = get_model_color(after_key)
        for key, hatch, dx in [(before_key, "///", -w / 2), (after_key, None, w / 2)]:
            r = data[key]
            lo, hi = r["ci"]
            ax.bar(i + dx, r["score"], w, color=color if hatch is None else "white", edgecolor=color, hatch=hatch, linewidth=2)
            err = ax.errorbar(i + dx, r["score"], yerr=[[r["score"] - lo], [hi - r["score"]]], fmt="none", ecolor="black",
                              capsize=3, elinewidth=1.4)
            for line in err[2]:
                line.set_alpha(0.6)
            ax.text(i + dx, hi + 0.015, f"{r['score']:.2f}", ha="center", va="bottom", fontsize=FS - 3, fontweight="bold")
        before, after = data[before_key]["score"], data[after_key]["score"]
        pct = (after - before) / before * 100  # plot-standards rule 1: per-pair delta, red when the gap falls; label uses a true minus sign
        top = max(data[k]["ci"][1] for k in (before_key, after_key))
        ax.text(i, top + 0.075, f"{pct:+.0f}% {'↓' if pct < 0 else '↑'}".replace("-", "\u2212"), ha="center", va="bottom", fontsize=FS - 2,
                fontweight="bold", color=RED if pct < 0 else GREEN)
    ax.set_xticks(x)
    ax.set_xticklabels([p[0] for p in order], fontsize=FS - 2, fontweight="bold")  # FS - 1 left SwiPO-S and SwiPO-R touching
    ax.set_ylim(0, 0.68)
    ax.set_ylabel("Refusal gap\n(strict minus permissive)", fontsize=FS, fontweight="bold")
    ax.tick_params(axis="y", labelsize=FS - 1)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    return [Patch(facecolor="white", edgecolor="black", hatch="///", label="final adapter only"),
            Patch(facecolor="#5b6573", edgecolor="black", label="as trained (parents merged)")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=sorted(STEMS), default="wide", help="wide: two panels side by side (figure*); column: stacked for one column")
    args = ap.parse_args()
    data = {**json.load(open(GAP_JSON))["suites"]["conditional_safety"],
            **json.load(open(CHAIN_JSON))["suites"]["conditional_safety"]}
    n = {data[k]["n"] for k in data}
    if len(n) != 1:
        raise RuntimeError(f"{GAP_JSON.name}: models scored on different prompt counts {n}")
    for _, before_key, after_key in pairs():
        for k in (before_key, after_key):
            if k not in data:
                raise RuntimeError(f"{GAP_JSON.name} + {CHAIN_JSON.name} have no {k}")
    if args.layout == "wide":
        fig = plt.figure(figsize=(14, 4.6))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.18)
        diagram(fig.add_subplot(gs[0]))
        handles = bars(fig.add_subplot(gs[1]), data)
        fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, prop={"size": FS, "weight": "bold"},
                   bbox_to_anchor=(0.69, 0.0))
        fig.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.22)  # explicit band below the axes for the legend (rule 3)
    else:  # one column: diagram above, bars below (rule 6: stacked panels)
        fig = plt.figure(figsize=(6.0, 6.2))  # same printed size as 7.0 x 7.2, text about 17% larger (both judges: Figure 1 text too small)
        gs = fig.add_gridspec(2, 1, height_ratios=[0.78, 1.22], hspace=0.12)
        diagram(fig.add_subplot(gs[0]))
        handles = bars(fig.add_subplot(gs[1]), data)
        fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, prop={"size": FS - 1, "weight": "bold"},
                   bbox_to_anchor=(0.5, 0.0))
        fig.subplots_adjust(left=0.15, right=0.985, top=0.99, bottom=0.11)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf, png = save_figure_dual_format(fig, OUT_DIR / STEMS[args.layout], dpi=300)
    plt.close(fig)
    print(f"n = {n.pop()} prompts per model; wrote {png} and {pdf}")


if __name__ == "__main__":
    main()
