"""XSTest safety-helpfulness plane from xstest_contract.py's summary: refusal on unsafe prompts vs answer rate on safe prompts per
model, strict (filled) to permissive (hollow) arrows, 95% BCa whiskers on both axes. CPU-only.
    python -u src/eval/xstest_tradeoff_plot.py --decode_variant stop_eot 2>&1 | tee logs/xstest_tradeoff_plot_stop_eot.log
    python -u src/eval/xstest_tradeoff_plot.py 2>&1 | tee logs/xstest_tradeoff_plot.log
    python -u src/eval/xstest_tradeoff_plot.py --decode_variant stop_eot --paper 2>&1 | tee logs/xstest_tradeoff_plot_paper.log
"""

import argparse
import json
import re
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
from src.utils.eval.display_names import get_display_names, substitute  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
X = CFG["xstest_contract"]
P = X["plot"]
ARMS = ("strict", "permissive")
FS = P["font_size"]
NAME = get_display_names()
REF = "#3a3f47"  # neutral ink for the contract-style legend entries and the no-discrimination line
plt.rcParams.update({"font.size": FS, "font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold"})  # rule 7


def versioned(out_dir, stem):
    """v<i>_<stem>: the stem's existing number (a regeneration keeps it), else the next free number in the folder (rule 11)."""
    nums = {}
    for p in out_dir.glob("v*_*"):
        m = re.match(r"v(\d+)_(.+)$", p.stem)
        if m:
            nums.setdefault(m.group(2), set()).add(int(m.group(1)))
    if stem in nums:
        if len(nums[stem]) != 1:
            raise SystemExit(f"FATAL: {out_dir} holds {stem} under several numbers {sorted(nums[stem])}")
        return f"v{nums[stem].pop()}_{stem}"
    return f"v{max((n for s in nums.values() for n in s), default=0) + 1}_{stem}"


def model_color(key):
    return P["colors"][key] if key in P["colors"] else get_model_color(key)


def check(models):
    """FATAL unless every model has a legend label, a distinct color and the same prompt counts."""
    missing = [k for k in models if k not in P["labels"]]
    if missing:
        raise SystemExit(f"FATAL: no xstest_contract.plot.labels entry for {missing} (configs/pipeline.yaml)")
    colors = {k: model_color(k) for k in models}
    clash = {c: [k for k in models if colors[k] == c] for c in set(colors.values())}
    clash = {c: ks for c, ks in clash.items() if len(ks) > 1}
    if clash:
        raise SystemExit(f"FATAL: models share a color {clash}; add a distinct hex under xstest_contract.plot.colors")
    ns = {json.dumps(models[k]["n"], sort_keys=True) for k in models}
    if len(ns) != 1:
        raise SystemExit(f"FATAL: models were scored on different prompt counts {ns}")
    return colors, models[next(iter(models))]["n"]


def limits(models):
    """Axis ranges: outermost CI ends plus axis_pad (not clipped to [0, 1], so a rate at 0 or 1 does not sit on the frame)."""
    out = []
    for metric in ("refusal_unsafe", "answer_safe"):
        ends = np.array([models[k]["contracts"][a][metric]["ci"] for k in models for a in ARMS])
        out.append((ends.min() - P["axis_pad"], ends.max() + P["axis_pad"]))
    return out


def draw(ax, models, colors):
    radius = np.sqrt(P["marker_size"]) / 2  # marker radius in points: arrows stop at the marker edge
    for key in tqdm(models, desc="xstest_tradeoff_plot", unit="model"):
        c, pts = colors[key], {}
        for arm in ARMS:
            r = models[key]["contracts"][arm]
            x, y = r["refusal_unsafe"]["rate"], r["answer_safe"]["rate"]
            (xlo, xhi), (ylo, yhi) = r["refusal_unsafe"]["ci"], r["answer_safe"]["ci"]
            err = ax.errorbar(x, y, xerr=[[x - xlo], [xhi - x]], yerr=[[y - ylo], [yhi - y]], fmt="none", ecolor=c,
                              elinewidth=1.6, capsize=3, zorder=2)
            for artist in (*err[1], *err[2]):
                artist.set_alpha(P["ci_alpha"])
            ax.scatter(x, y, s=P["marker_size"], facecolors=c if arm == "strict" else "white", edgecolors=c, linewidths=2.2, zorder=4)
            pts[arm] = (x, y)
            print(f"  {key:28s} {arm:10s} refusal on unsafe {x:.3f} [{xlo:.3f}, {xhi:.3f}] | answer on safe {y:.3f} [{ylo:.3f}, {yhi:.3f}]")
        ax.annotate("", xy=pts["permissive"], xytext=pts["strict"], zorder=3,
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2, shrinkA=radius, shrinkB=radius, mutation_scale=16))


def main():
    ap = argparse.ArgumentParser(description="XSTest safety-helpfulness plane from xstest_contract.py's summary JSON (CPU)")
    ap.add_argument("--decode_variant", choices=sorted(CFG["decode_variants"]), default=None,
                    help="read <summary_dir>/<summary_name>_<variant>.json (the run made with the same --decode_variant)")
    ap.add_argument("--summary", type=Path, default=None,
                    help="explicit summary JSON (a _samples<N> smoke run, a test file); its name must start with summary_name")
    ap.add_argument("--out_dir", type=Path, default=project_root / P["dir"], help="figure folder (default xstest_contract.plot.dir)")
    ap.add_argument("--paper", action="store_true", help="one-column paper version: plot.paper figsize and legend columns, no in-image title")
    args = ap.parse_args()
    size = P["paper"] if args.paper else P
    variant = f"_{args.decode_variant}" if args.decode_variant else ""
    path = args.summary or project_root / X["summary_dir"] / f"{X['summary_name']}{variant}.json"
    if not path.stem.startswith(X["summary_name"]):
        raise SystemExit(f"FATAL: {path.name} does not start with {X['summary_name']}")
    data = json.load(open(path))
    models = data["models"]
    colors, n = check(models)
    (x0, x1), (y0, y1) = limits(models)
    print(f"{path}: {len(models)} models, {n} prompts, decode_variant {data['meta']['decode_variant']}")

    fig, ax = plt.subplots(figsize=size["figsize"])
    draw(ax, models, colors)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    handles = [Line2D([], [], marker="o", linestyle="none", markersize=11, markerfacecolor=colors[k], markeredgecolor=colors[k],
                      label=substitute(P["labels"][k], NAME)) for k in models]
    handles += [Line2D([], [], marker="o", linestyle="none", markersize=11, markerfacecolor=REF, markeredgecolor=REF, label="strict contract"),
                Line2D([], [], marker="o", linestyle="none", markersize=11, markerfacecolor="white", markeredgecolor=REF,
                       markeredgewidth=2.2, label="permissive contract"),
                Line2D([], [], marker=r"$\rightarrow$", linestyle="none", markersize=18, color=REF, label="strict to permissive")]
    if args.paper:  # the paper caption explains the arrow and the dotted line, so the legend keeps models and contracts only
        handles = handles[:-1]
    if max(x0, 1 - y1) <= min(x1, 1 - y0):  # y = 1 - x crosses the visible window: refusal on unsafe = refusal on safe
        ax.plot([0, 1], [1, 0], linestyle=":", color=REF, linewidth=1.8, alpha=0.7, zorder=1)
        if not args.paper:
            handles.append(Line2D([], [], linestyle=":", color=REF, linewidth=1.8, label="no discrimination (y = 1 - x)"))
    ax.set_xlabel("Refusal rate on unsafe prompts (safety) →", fontsize=FS, fontweight="bold")
    ax.set_ylabel("Answer rate on safe prompts (helpfulness) →", fontsize=FS, fontweight="bold")
    decode = data["meta"]["decode_variant"]
    if not args.paper:
        ax.set_title(f"XSTest: {n['safe']} safe, {n['unsafe']} unsafe prompts; 95% BCa CIs" + (f"\ndecoding: {decode}" if decode else ""),
                     fontsize=FS, fontweight="bold")
    ax.tick_params(labelsize=FS)
    ax.grid(linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    fig.canvas.draw()  # place the legend just below the x label (rule 3: legend below the axes, never over the data)
    label_box = ax.xaxis.label.get_window_extent().transformed(ax.transAxes.inverted())
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, label_box.y0), ncol=size["legend_ncol"], frameon=False,
              prop={"size": FS, "weight": "bold"}, handletextpad=0.3, columnspacing=1.0)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = versioned(args.out_dir, P["stem"] + path.stem[len(X["summary_name"]):] + (P["paper"]["stem_suffix"] if args.paper else ""))
    pdf, png = save_figure_dual_format(fig, args.out_dir / stem, dpi=P["dpi"])
    plt.close(fig)
    print(f"wrote {png} and {pdf}")


if __name__ == "__main__":
    main()
