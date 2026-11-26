"""Refusal gap (strict minus permissive) per PKU-SafeRLHF harm category for the four Instruct models, 95% BCa whiskers, floor categories starred. CPU-only.
    python -u src/eval/floor_per_category_plot.py 2>&1 | tee logs/floor_per_category_plot.log
"""

import json
import sys
from pathlib import Path

import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from tqdm import tqdm  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.eval.plotting import get_model_color, save_figure_dual_format  # noqa: E402
from src.utils.eval.display_names import get_display_names  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
FLOOR_JSON = project_root / CFG["paths"]["floor_leakage_dir"] / "floor_leakage.json"
FIG = CFG["floor_leakage"]["per_category_figure"]
OUT_DIR = project_root / FIG["dir"]
VARIANT = CFG["floor_leakage"]["variant"]
FLOOR = set(CFG["floor_leakage"]["floor_categories"])
TRAINERS = CFG["score_table"]["trainers"]
NAME = get_display_names()
FS = 12  # plot-standards rule 7: every text element at least 12 pt bold


def main():
    data = json.load(open(FLOOR_JSON))
    if data["meta"]["variant"] != VARIANT:
        raise RuntimeError(f"{FLOOR_JSON.name} holds variant {data['meta']['variant']}, config expects {VARIANT}")
    per = {t: data["models"][f"{t}_{VARIANT}"]["per_category"] for t in TRAINERS}
    cats = list(per[TRAINERS[0]])
    for t in TRAINERS:
        if set(per[t]) != set(cats):
            raise RuntimeError(f"{t}: category set differs from {TRAINERS[0]}")
    mean_gap = {c: np.mean([per[t][c]["gap"] for t in TRAINERS]) for c in cats}
    order = sorted(cats, key=lambda c: mean_gap[c])  # largest mean gap at the top
    lo = min(per[t][c]["gap_ci"][0] for t in TRAINERS for c in cats)
    hi = max(per[t][c]["gap_ci"][1] for t in TRAINERS for c in cats)
    print(f"{len(cats)} categories x {len(TRAINERS)} trainers; gap CIs span [{lo:.3f}, {hi:.3f}]; x_max = {FIG['x_max']}")
    if hi > FIG["x_max"] or lo < 0:
        raise RuntimeError(f"CI range [{lo:.3f}, {hi:.3f}] falls outside the axis [0, {FIG['x_max']}]")

    fig, ax = plt.subplots(figsize=(7.2, 9.6))
    y = np.arange(len(order))
    for i, c in enumerate(order):
        if c in FLOOR:
            ax.axhspan(i - 0.5, i + 0.5, color="#f2dede", zorder=0)
    offsets = (np.arange(len(TRAINERS)) - (len(TRAINERS) - 1) / 2) * FIG["dodge"]
    for k, t in enumerate(tqdm(TRAINERS, desc="floor_per_category_plot", unit="trainer")):
        g = np.array([per[t][c]["gap"] for c in order])
        ci = np.array([per[t][c]["gap_ci"] for c in order])
        color = get_model_color(f"{t}_{VARIANT}")
        err = ax.errorbar(g, y + offsets[k], xerr=[g - ci[:, 0], ci[:, 1] - g], fmt="o", color=color,
                          markersize=6, capsize=2, elinewidth=1.2, zorder=3)
        for line in err[2]:
            line.set_alpha(0.45)  # plot-standards rule 5: whiskers must not hide the dots
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} *" if c in FLOOR else c for c in order], fontsize=FS, fontweight="bold")
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlim(0, FIG["x_max"])
    ax.set_xlabel("Refusal gap: strict minus permissive contract", fontsize=FS, fontweight="bold")
    ax.tick_params(axis="x", labelsize=FS)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_title("Refusal gap by harm category, Llama-3.1-8B Instruct models\n(95% BCa intervals; * and shading = floor category)",
                 fontsize=FS, fontweight="bold")
    handles = [Line2D([0], [0], marker="o", linestyle="", color=get_model_color(f"{t}_{VARIANT}"), markersize=8) for t in TRAINERS]
    fig.legend(handles, [NAME.get(t, t) for t in TRAINERS], loc="lower center", ncol=len(TRAINERS), frameon=False,
               prop={"size": FS, "weight": "bold"}, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf, png = save_figure_dual_format(fig, OUT_DIR / FIG["stem"], dpi=300)
    plt.close(fig)
    print(f"wrote {png} and {pdf}")


if __name__ == "__main__":
    main()
