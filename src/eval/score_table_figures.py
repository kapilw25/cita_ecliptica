"""Paper radar (instruction-alignment efficiency) and heatmap (raw scores with 95% BCa intervals) drawn from score_table_ci.json. CPU-only.
    python -u src/eval/score_table_figures.py 2>&1 | tee logs/score_table_figures.log
"""

import json
import sys
from pathlib import Path

import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import Normalize  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from tqdm import tqdm  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.eval.plotting import get_model_color, save_figure_dual_format  # noqa: E402
from src.utils.eval.display_names import get_display_names  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
CI_JSON = project_root / CFG["paths"]["score_table_ci_dir"] / "score_table_ci.json"
OUT_DIR = project_root / CFG["paths"]["score_table_figures_dir"]
FIG = CFG["score_table_figures"]
SUITES = FIG["suite_order"]
LABELS = FIG["suite_labels"]
WITHIN = set(FIG["within_model"])
TRAINERS = CFG["score_table"]["trainers"]
NAME = get_display_names()
show = lambda t: NAME.get(t, t)  # noqa: E731
FS = 12  # plot-standards rule 7: every text element at least 12 pt bold


def scaled_deltas(table):
    """Per-suite min-max of the Instruct-minus-NoInstruct delta onto [0.1, 1], as in the efficiency score."""
    raw = {s: np.array([table[t][s]["delta"] for t in TRAINERS]) for s in SUITES}
    out = {}
    for s, v in raw.items():
        lo, hi = v.min(), v.max()
        out[s] = 0.1 + 0.9 * (v - lo) / (hi - lo if hi > lo else 1.0)
    return raw, out


def radar(data):
    table, eff = data["table"], data["efficiency"]["all"]["trainers"]
    raw, scaled = scaled_deltas(table)
    for i, t in enumerate(TRAINERS):  # the drawn polygon must reproduce the reported efficiency exactly
        mean = 100 * np.mean([scaled[s][i] for s in SUITES])
        if abs(mean - eff[t]["efficiency"]) > 1e-6:
            raise RuntimeError(f"{t}: scaled mean {mean:.6f} != efficiency {eff[t]['efficiency']:.6f} in {CI_JSON.name}")
    angles = np.linspace(0, 2 * np.pi, len(SUITES), endpoint=False)
    fig = plt.figure(figsize=(7.4, 8.8))
    ax = fig.add_axes([0.16, 0.27, 0.68, 0.54], polar=True)  # room above for the title and the top axis label
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    for i, t in enumerate(TRAINERS):
        r = [scaled[s][i] for s in SUITES]
        color = get_model_color(f"{t}_Instruct")
        ax.plot(np.r_[angles, angles[:1]], r + r[:1], "o-", color=color, linewidth=2.5, markersize=8)
        ax.fill(np.r_[angles, angles[:1]], r + r[:1], color=color, alpha=0.12)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=FS, color="#404040")
    ax.set_rlabel_position(36)
    ax.set_xticks(angles)
    ax.set_xticklabels([])
    ax.grid(True, linestyle="--", linewidth=1.0, color="#606060", alpha=0.7)
    for k, s in enumerate(SUITES):
        if s in WITHIN:
            txt = f"{LABELS[s]}\nwithin-model, not ranked"
        else:
            best = int(np.argmax(raw[s]))
            txt = f"{LABELS[s]}\nbest $\\Delta$ {raw[s][best]:+.3f} ({show(TRAINERS[best])})"
        x = np.sin(angles[k])  # clockwise from the top: positive x is the right half
        ha = "center" if abs(x) < 0.2 else ("left" if x > 0 else "right")
        va = "bottom" if np.cos(angles[k]) > 0.2 else ("top" if np.cos(angles[k]) < -0.2 else "center")
        ax.text(angles[k], 1.12, txt, ha=ha, va=va, fontsize=FS, fontweight="bold")
    fig.suptitle("Instruction-alignment efficiency, Llama-3.1-8B\n(relative to these four trainers)",
                 fontsize=FS + 1, fontweight="bold", y=0.995)
    handles = [Line2D([0], [0], marker="o", color=get_model_color(f"{t}_Instruct"), linewidth=2.5, markersize=8) for t in TRAINERS]
    labels = [f"{show(t)} {eff[t]['efficiency']:.1f}% [{eff[t]['ci'][0]:.1f}, {eff[t]['ci'][1]:.1f}]" for t in TRAINERS]
    leg = fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.075), ncol=2, frameon=True,
                     prop={"size": FS, "weight": "bold"}, title="Efficiency: mean scaled $\\Delta$ [95% BCa]", title_fontsize=FS)
    leg.get_title().set_fontweight("bold")
    fig.text(0.5, 0.02, "Vertices: $\\Delta$ min-max scaled to [0.1, 1] per suite (no interval);\nraw $\\Delta$ with 95% intervals in the score table",
             ha="center", va="bottom", fontsize=FS, fontweight="bold", color="#404040")
    return fig


def heatmap(data):
    table = data["table"]
    rows, vals, half = [], [], []
    for t in TRAINERS:
        for arm in ("NoInstruct", "Instruct"):
            rows.append(f"{show(t)} {'NI' if arm == 'NoInstruct' else 'I'}")
            v, h = [], []
            for s in SUITES:
                c = table[t][s]
                if s in WITHIN:
                    v.append(c["score"] if arm == "Instruct" else c["score"] - c["delta"])
                    h.append(np.nan)
                else:
                    key, ck = ("score", "score_ci") if arm == "Instruct" else ("noinst_score", "noinst_score_ci")
                    v.append(c[key])
                    h.append((c[ck][1] - c[ck][0]) / 2)
            vals.append(v)
            half.append(h)
    V, H = np.array(vals), np.array(half)
    fig, ax = plt.subplots(figsize=(9.6, 6.4))
    cmap = plt.get_cmap("RdYlGn")
    for j, s in enumerate(SUITES):
        col = V[:, j]
        norm = Normalize(col.min(), col.max() if col.max() > col.min() else col.min() + 1)
        for i in range(len(rows)):
            face = (0.89, 0.89, 0.89, 1.0) if s in WITHIN else cmap(norm(col[i]))
            ink = "white" if 0.299 * face[0] + 0.587 * face[1] + 0.114 * face[2] < 0.45 else "black"  # contrast on dark cells
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=face, edgecolor="white", linewidth=1.5))
            num = f"{col[i]:.1f}" if abs(col[i]) >= 10 else f"{col[i]:.3f}"
            ci = "no interval" if np.isnan(H[i, j]) else f"$\\pm${H[i, j]:.3f}"
            ax.text(j + 0.5, i + 0.38, num, ha="center", va="center", fontsize=FS + 1, fontweight="bold", color=ink)
            ax.text(j + 0.5, i + 0.72, ci, ha="center", va="center", fontsize=FS, fontweight="bold", color=ink)
    for g in range(2, len(rows), 2):
        ax.axhline(g, color="black", linewidth=2.5)
    ax.set_xlim(0, len(SUITES))
    ax.set_ylim(len(rows), 0)
    ax.set_xticks(np.arange(len(SUITES)) + 0.5)
    ax.set_xticklabels([LABELS[s] + ("\n(within-model)" if s in WITHIN else "") for s in SUITES], fontsize=FS, fontweight="bold")
    ax.set_yticks(np.arange(len(rows)) + 0.5)
    ax.set_yticklabels(rows, fontsize=FS, fontweight="bold")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(0, 1))
    cb = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("Per-suite min-max of the raw score", fontsize=FS, fontweight="bold")
    cb.ax.tick_params(labelsize=FS)
    ax.set_title("Raw scores of all eight models, Llama-3.1-8B (NI: NoInstruct, I: Instruct)\n"
                 "95% BCa half-widths; LITMUS is normalized within each model, so it is grey and unranked",
                 fontsize=FS, fontweight="bold", pad=12)
    return fig


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.load(open(CI_JSON))
    jobs = [(FIG["radar_stem"], radar), (FIG["heatmap_stem"], heatmap)]
    for stem, draw in tqdm(jobs, desc="score_table_figures", unit="figure"):
        fig = draw(data)
        pdf, png = save_figure_dual_format(fig, OUT_DIR / stem, dpi=300)
        plt.close(fig)
        print(f"wrote {png} and {pdf}")


if __name__ == "__main__":
    main()
