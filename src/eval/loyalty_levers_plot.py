"""LoyalAgents Figure 1: per model as trained, the deployer's refusal switch (LLM judge), a user turn that loosens the contract, and hidden-sponsor
promotion (with the user's impartiality request where that run exists); 95% BCa whiskers. CPU-only.
    python -u src/eval/loyalty_levers_plot.py 2>&1 | tee logs/loyalty_levers_plot.log
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
from matplotlib.patches import Patch  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.eval.plotting import get_model_color, save_figure_dual_format  # noqa: E402
from src.utils.eval.display_names import get_display_names, substitute  # noqa: E402
from src.utils.progress import make_pbar  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
P = CFG["loyalty_levers_plot"]
XP = CFG["xstest_contract"]["plot"]
CG = project_root / "outputs/evaluation/contract_gap"
FS = P["font_size"]
NAME = get_display_names()
plt.rcParams.update({"font.size": FS, "font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold"})  # rule 7


def versioned(out_dir: Path, stem: str) -> str:
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


def color(key: str) -> str:
    return XP["colors"][key] if key in XP["colors"] else get_model_color(key)


def label(key: str) -> str:
    """Short tick label: the caption says which models are prompted."""
    return substitute(XP["labels"][key], NAME).replace(" (prompted)", "")


def panels() -> list:
    """(title, y label, {model: (value, lo, hi)}, lower_is_better, second series or None) per panel, from the result JSONs."""
    judge = json.load(open(CG / "refusal_judge.json"))["models"]
    loosen = json.load(open(CG / "authority_split.json"))["models"]  # outputs/evaluation/stack_probe/authority_split.py
    sponsor = json.load(open(CG / "sponsor_echo_stop_eot.json"))["models"]
    a = {k: (judge[k]["gap_judge"], *judge[k]["gap_judge_ci"]) for k in P["models"]}
    b = {k: (loosen[k]["loosen_judge"]["change"]["value"], *loosen[k]["loosen_judge"]["change"]["ci"]) for k in P["models"]}  # LLM judge, as panel (a)
    c = {k: (sponsor[k]["promotion_no_echo"]["rate"], *sponsor[k]["promotion_no_echo"]["ci"]) for k in P["models"]}
    impartial, path = None, CG / "sponsor_impartial_stop_eot.json"
    if path.exists():  # outputs/evaluation/stack_probe/sponsor_impartial.py
        imp = json.load(open(path))["models"]
        impartial = {k: (v["promotion"]["impartial"]["value"], *v["promotion"]["impartial"]["ci"]) for k, v in imp.items()}
    return [("(a) Deployer's contract switches refusal", "judge gap", a, False, None),
            ("(b) User turn loosens a strict contract", "judged refusal\nchange", b, False, None),
            ("(c) Hidden sponsor promoted", "share of\nanswers", c, True, impartial)]


def draw(ax, title, ylab, data, lower_better, second):
    keys = sorted(data, key=lambda k: data[k][0], reverse=lower_better)  # rule 1: the best value sits rightmost
    x = np.arange(len(keys))
    w = P["bar_width"] if second else 2 * P["bar_width"]
    off = -w / 2 if second else 0.0
    for i, k in enumerate(keys):
        v, lo, hi = data[k]
        ax.bar(x[i] + off, v, width=w, color=color(k), edgecolor="black", linewidth=0.8, zorder=2)
        err = ax.errorbar(x[i] + off, v, yerr=[[v - lo], [hi - v]], fmt="none", ecolor="black", elinewidth=1.4, capsize=3, zorder=3)
        for artist in (*err[1], *err[2]):
            artist.set_alpha(P["ci_alpha"] * 2)
        if second and k in second:
            v2, lo2, hi2 = second[k]
            ax.bar(x[i] + w / 2, v2, width=w, color="white", edgecolor=color(k), hatch="///", linewidth=1.6, zorder=2)
            err = ax.errorbar(x[i] + w / 2, v2, yerr=[[v2 - lo2], [hi2 - v2]], fmt="none", ecolor="black", elinewidth=1.4, capsize=3, zorder=3)
            for artist in (*err[1], *err[2]):
                artist.set_alpha(P["ci_alpha"] * 2)
        print(f"  {title[:40]:40s} {k:28s} {v:+.3f} [{lo:+.3f}, {hi:+.3f}]"
              + (f" | with the user's request {second[k][0]:+.3f} [{second[k][1]:+.3f}, {second[k][2]:+.3f}]" if second and k in second else ""))
    ax.axhline(0, color="black", linewidth=0.9, zorder=1)
    ax.set_xticks(x)
    ax.set_xticklabels([("\n" if i % 2 else "") + label(k) for i, k in enumerate(keys)], fontsize=FS - 1)  # staggered: no overlap
    ax.set_ylabel(ylab, fontsize=FS - 1)
    ax.set_title(title, fontsize=FS, loc="left")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)


def main():
    ap = argparse.ArgumentParser(description="LoyalAgents Figure 1: three levers per model as trained (CPU)")
    ap.add_argument("--out_dir", type=Path, default=project_root / P["dir"], help="figure folder (default loyalty_levers_plot.dir)")
    args = ap.parse_args()
    specs = panels()
    fig, axes = plt.subplots(len(specs), 1, figsize=P["figsize"])
    pbar = make_pbar(total=len(specs), desc="loyalty_levers_plot", unit="panel")
    for ax, spec in zip(axes, specs):
        draw(ax, *spec)
        pbar.update(1)
    pbar.close()
    if specs[-1][4]:  # rule 2: the second arm is hatched and named in a legend below the axes (rule 3)
        fig.legend(handles=[Patch(facecolor="grey", edgecolor="black", label="hidden-sponsor contract"),
                            Patch(facecolor="white", edgecolor="grey", hatch="///", label="+ user asks for impartiality")],
                   loc="lower center", ncol=2, frameon=False, prop={"size": FS - 2, "weight": "bold"})
        fig.tight_layout(rect=(0, 0.04, 1, 1))
    else:
        fig.tight_layout()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    pdf, png = save_figure_dual_format(fig, args.out_dir / versioned(args.out_dir, P["stem"]), dpi=P["dpi"])
    plt.close(fig)
    print(f"wrote {png} and {pdf}")


if __name__ == "__main__":
    main()
