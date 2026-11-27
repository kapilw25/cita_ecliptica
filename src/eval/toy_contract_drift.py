"""MATH4AI toy: contract-conditioned DPO on one contract, independent vs shared contract parameters; unseen-switch change and its first-order prediction. CPU-only.
    python -u src/eval/toy_contract_drift.py 2>&1 | tee logs/toy_contract_drift.log
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import yaml
from scipy.stats import rankdata
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.eval.floor_leakage import ci  # noqa: E402
from src.utils.eval.plotting import save_figure_dual_format  # noqa: E402
from src.utils.progress import make_pbar  # noqa: E402

CFG = yaml.safe_load(open(project_root / "configs" / "pipeline.yaml"))
T = CFG["toy_contract_drift"]
P = T["plot"]
plt.rcParams.update({"font.size": P["font_size"], "font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold"})


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def logits(params: dict, shared: bool, X: np.ndarray, k: int, E: np.ndarray) -> np.ndarray:
    """Refusal logit s(I_k, x) for every row of X."""
    if shared:
        return X @ (params["w"] + params["B"] @ E[k]) + params["c"] + params["v"] @ E[k]
    return X @ params["W"][k] + params["C"][k]


def grads_from_ds(ds: np.ndarray, shared: bool, X: np.ndarray, k: int, E: np.ndarray, params: dict) -> dict:
    """Parameter gradient of sum_i ds_i * s(I_k, x_i)."""
    g = {name: np.zeros_like(val) for name, val in params.items()}
    xs = X.T @ ds
    if shared:
        g["w"] += xs
        g["B"] += np.outer(xs, E[k])
        g["c"] += ds.sum()
        g["v"] += ds.sum() * E[k]
    else:
        g["W"][k] += xs
        g["C"][k] += ds.sum()
    return g


def dot(a: dict, b: dict) -> float:
    return float(sum(np.sum(a[n] * b[n]) for n in a))


def run_seed(s: int, shared: bool) -> dict:
    rng = np.random.default_rng(T["seed_base"] + s)  # same draw for both classes: data, embeddings, harm direction
    d, m, K = T["d"], T["m"], T["n_contracts"]
    u = rng.standard_normal(d)
    u /= np.linalg.norm(u)
    Xtr = rng.standard_normal((T["n_train"], d))
    Xte = rng.standard_normal((T["n_test"] * 4, d))
    Xte = Xte[Xte @ u > 0][: T["n_test"]]  # harmful test requests
    if len(Xte) < T["n_test"]:
        raise RuntimeError(f"seed {s}: only {len(Xte)} harmful test requests drawn")
    E = rng.standard_normal((K, m))
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    init = rng.standard_normal(d + d * m + 1 + m + K * (d + 1)) * T["init_scale"]
    if shared:
        params = {"w": init[:d], "B": init[d:d + d * m].reshape(d, m), "c": init[d + d * m:d + d * m + 1], "v": init[d + d * m + 1:d + d * m + 1 + m]}
    else:
        rest = init[d + d * m + 1 + m:]
        params = {"W": rest[:K * d].reshape(K, d), "C": rest[K * d:]}
    params = {n: v.copy() for n, v in params.items()}
    sign = np.where(Xtr @ u > 0, 1.0, -1.0)  # strict contract I0: refuse harmful (+1), comply otherwise (-1)
    s_ref = logits(params, shared, Xtr, 0, E)
    beta, n = T["beta"], len(Xtr)

    def loss_grad(p):
        delta = sign * (logits(p, shared, Xtr, 0, E) - s_ref)
        ds = -beta * sign * sig(-beta * delta) / n  # d/ds of mean -log sigma(beta * delta)
        return float(np.mean(np.logaddexp(0.0, -beta * delta))), grads_from_ds(ds, shared, Xtr, 0, E, p)

    def switch(p):
        return float(np.mean(sig(logits(p, shared, Xte, 1, E)) - sig(logits(p, shared, Xte, 2, E))))

    def switch_grad(p):
        z1, z2 = logits(p, shared, Xte, 1, E), logits(p, shared, Xte, 2, E)
        a1, a2 = sig(z1) * (1 - sig(z1)) / len(Xte), sig(z2) * (1 - sig(z2)) / len(Xte)
        g1, g2 = grads_from_ds(a1, shared, Xte, 1, E, p), grads_from_ds(-a2, shared, Xte, 2, E, p)
        return {k: g1[k] + g2[k] for k in g1}

    g0 = switch(params)
    _, gl = loss_grad(params)
    gg = switch_grad(params)
    first_order = -T["lr"] * dot(gg, gl)  # predicted change of the switch after one step
    for _ in range(T["steps"]):
        _, gl_t = loss_grad(params)
        for k in params:
            params[k] -= T["lr"] * gl_t[k]
    acc = float(np.mean(np.sign(logits(params, shared, Xtr, 0, E) - s_ref) == sign))
    return {"change": switch(params) - g0, "first_order": first_order, "alignment": float(E[0] @ (E[1] - E[2])), "train_acc": acc,
            "switch_start": g0}


def spearman(a, b, axis=-1):
    ra, rb = rankdata(a, axis=axis), rankdata(b, axis=axis)
    ra = ra - ra.mean(axis=axis, keepdims=True)
    rb = rb - rb.mean(axis=axis, keepdims=True)
    return np.sum(ra * rb, axis=axis) / np.sqrt(np.sum(ra ** 2, axis=axis) * np.sum(rb ** 2, axis=axis))


def versioned(out_dir: Path, stem: str) -> str:
    """v<i>_<stem>: the stem's existing number, else the next free number in the folder."""
    nums = {}
    for p in out_dir.glob("v*_*"):
        mm = re.match(r"v(\d+)_(.+)$", p.stem)
        if mm:
            nums.setdefault(mm.group(2), set()).add(int(mm.group(1)))
    if stem in nums:
        return f"v{min(nums[stem])}_{stem}"
    return f"v{max((x for v in nums.values() for x in v), default=0) + 1}_{stem}"


def main():
    ap = argparse.ArgumentParser(description="MATH4AI toy: one-contract DPO, independent vs shared contract parameters (CPU)")
    ap.add_argument("--seeds", type=int, default=T["seeds"], help="number of seeds (default toy_contract_drift.seeds)")
    args = ap.parse_args()
    out = project_root / T["out_dir"]
    res = {"independent": [], "shared": []}
    pbar = make_pbar(total=2 * args.seeds, desc="toy_contract_drift", unit="run")
    for s in range(args.seeds):
        for cls in res:
            res[cls].append(run_seed(s, cls == "shared"))
            pbar.update(1)
    pbar.close()
    arr = {cls: {k: np.array([r[k] for r in rs]) for k in rs[0]} for cls, rs in res.items()}
    sh, ind = arr["shared"], arr["independent"]
    agree = (np.sign(sh["first_order"]) == np.sign(sh["change"])).astype(float)
    (alo, ahi), am = ci((agree,), lambda x, axis=-1: np.mean(x, axis=axis), paired=False)
    (rlo, rhi), rm = ci((sh["alignment"], sh["change"]), spearman, paired=True)
    (plo, phi), pm = ci((sh["first_order"], sh["change"]), spearman, paired=True)
    (mlo, mhi), mm_ = ci((np.abs(sh["change"]),), lambda x, axis=-1: np.mean(x, axis=axis), paired=False)
    summary = {
        "independent": {"max_abs_change": float(np.max(np.abs(ind["change"]))), "train_acc_mean": float(ind["train_acc"].mean())},
        "shared": {"mean_abs_change": {"value": float(np.mean(np.abs(sh["change"]))), "ci": [mlo, mhi], "ci_method": mm_},
                   "max_abs_change": float(np.max(np.abs(sh["change"]))),
                   "change_range": [float(sh["change"].min()), float(sh["change"].max())],
                   "sign_agreement_first_order": {"value": float(agree.mean()), "ci": [alo, ahi], "ci_method": am},
                   "spearman_alignment_change": {"value": float(spearman(sh["alignment"], sh["change"])), "ci": [rlo, rhi], "ci_method": rm},
                   "spearman_first_order_change": {"value": float(spearman(sh["first_order"], sh["change"])), "ci": [plo, phi], "ci_method": pm},
                   "train_acc_mean": float(sh["train_acc"].mean())}}
    out.mkdir(parents=True, exist_ok=True)
    (out / "toy_contract_drift.json").write_text(json.dumps({"meta": {k: v for k, v in T.items() if k != "plot"}, "summary": summary,
                                                             "runs": res}, indent=1))
    print(f"independent: largest |change| of the unseen switch {summary['independent']['max_abs_change']:.2e}, "
          f"train accuracy {summary['independent']['train_acc_mean']:.3f}")
    S = summary["shared"]
    print(f"shared: mean |change| {S['mean_abs_change']['value']:.3f} [{mlo:.3f}, {mhi:.3f}], range {S['change_range'][0]:+.3f} to "
          f"{S['change_range'][1]:+.3f}; sign matches first order in {S['sign_agreement_first_order']['value']:.3f} [{alo:.3f}, {ahi:.3f}]; "
          f"Spearman(alignment, change) {S['spearman_alignment_change']['value']:.3f} [{rlo:.3f}, {rhi:.3f}]; Spearman(first order, change) "
          f"{S['spearman_first_order_change']['value']:.3f} [{plo:.3f}, {phi:.3f}]; train accuracy {S['train_acc_mean']:.3f}")
    # figure: (a) change vs alignment, binned means with 95% CI whiskers; (b) change vs first-order prediction (shared)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=P["figsize"])
    edges = np.quantile(sh["alignment"], np.linspace(0, 1, T["bins"] + 1))
    centers, means, halves = [], [], []
    for lo_e, hi_e in zip(edges[:-1], edges[1:]):
        sel = (sh["alignment"] >= lo_e) & (sh["alignment"] <= hi_e)
        v = sh["change"][sel]
        centers.append(sh["alignment"][sel].mean())
        means.append(v.mean())
        halves.append(1.96 * v.std(ddof=1) / np.sqrt(len(v)))
    ax1.scatter(sh["alignment"], sh["change"], s=6, color=P["colors"]["shared"], alpha=0.25, linewidths=0)
    ax1.errorbar(centers, means, yerr=halves, fmt="o-", color=P["colors"]["shared"], ecolor="black", elinewidth=1.2, capsize=3, ms=5)
    ax1.scatter(ind["alignment"], ind["change"], s=8, color=P["colors"]["independent"], marker="s", alpha=0.5, linewidths=0)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_xlabel(r"alignment $e_{I_0}\cdot(e_{I_1}-e_{I_2})$")
    ax1.set_ylabel("change of\nunseen switch")
    ax1.set_title("(a) Unseen switch moves only with shared parameters", loc="left", fontsize=P["font_size"])
    ax2.scatter(sh["first_order"], sh["change"], s=6, color=P["colors"]["shared"], alpha=0.35, linewidths=0)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.set_xlabel(r"first-order prediction $-\eta\langle\nabla g,\nabla L\rangle$ at start")
    ax2.set_ylabel("change of\nunseen switch")
    ax2.set_title("(b) Its sign follows the first-order term", loc="left", fontsize=P["font_size"])
    for ax in (ax1, ax2):
        ax.grid(linestyle="--", alpha=0.4)
    fig.legend(handles=[Line2D([], [], marker="o", ls="", color=P["colors"]["shared"], label="shared parameters"),
                        Line2D([], [], marker="s", ls="", color=P["colors"]["independent"], label="independent per contract")],
               loc="lower center", ncol=2, frameon=False, prop={"size": P["font_size"] - 1, "weight": "bold"})
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    pdf, png = save_figure_dual_format(fig, fig_dir / versioned(fig_dir, P["stem"]), dpi=P["dpi"])
    plt.close(fig)
    print(f"wrote {out / 'toy_contract_drift.json'}, {png} and {pdf}")


if __name__ == "__main__":
    main()
