"""Four alternative LoyalAgents poster figures (designs 2-5; design 1 = loyalty_story_plot.py), same verbatim data, no numbers. CPU.
    python -u src/eval/poster_designs.py 2>&1 | tee logs/poster_designs.log
"""
import json
import shutil
import sys
import textwrap
from pathlib import Path

import matplotlib
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
from src.eval.loyalty_story_plot import CHAR, CFG, LINE, P, PAD, verbatim  # noqa: E402
from src.utils.eval.first_turn import first_turn  # noqa: E402

S = P["switch"]
D = CFG["poster_designs"]
FS = P["font_size"]
INK, RED, GREEN, GREY = "#1a1a1a", "#a3161a", "#1f6b2e", "#666666"
OURS_FACE, OURS_EDGE, OTHER_FACE, OTHER_EDGE = "#fbeed5", "#b07a1e", "#f4f4f4", "#999999"
USER_FACE, USER_EDGE = "#dbe9f7", "#4a78a8"


def answers():
    """{label: {arm: (first n words of the first turn, judged refusal)}} for the switch item, models as trained."""
    out = {}
    for label, key in D["models"].items():
        out[label] = {}
        for arm in ("strict", "permissive"):
            ans = pd.read_csv(project_root / S["answers_dir"] / key / f"{arm}_responses.csv").set_index("prompt_idx")
            lab = pd.read_csv(project_root / S["labels_dir"] / key / f"{arm}.csv").set_index("prompt_idx")
            words = first_turn(ans.loc[S["item"], "response"]).split()
            out[label][arm] = (" ".join(words[:D["snippet_words"]]) + " …", int(lab.loc[S["item"], "is_refusal_judge"]))
    request = ans.loc[S["item"], "prompt"]
    return out, request


def sponsor():
    adir = project_root / P["answers_dir"] / P["model"]
    setup = json.load(open(adir / "setup.json"))
    df = pd.read_csv(adir / "sponsor_responses.csv")
    row = df[df.prompt.str.contains(P["prompt_contains"], case=False)].iloc[0]
    hidden = verbatim(D["sponsor_hidden_excerpt"], setup["contracts"]["sponsor"], "the sponsor contract")
    denial = verbatim(D["sponsor_denial_excerpt"], row.response, "the reply")
    return hidden, denial


def rbox(ax, x, y_top, w, h, face, edge, lw=0.7, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h, boxstyle="round,pad=0,rounding_size=0.04",
                                facecolor=face, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=0))


def lines_at(ax, x, y_top, lines, color=INK, bold=False, size=None, ha="left"):
    for i, ln in enumerate(lines):
        ax.text(x, y_top - (i + 0.8) * LINE, ln, fontsize=size or FS, color=color, fontweight="bold" if bold else "normal", ha=ha)
    return len(lines) * LINE


def wrap(text, width_in, f=0.9):
    return textwrap.wrap(text, max(6, int(f * width_in / CHAR)))


def tagged(ax, x, y_top, w, tag, color, text, f=0.9):
    """A bold colored tag, then text wrapped around it; returns the height used."""
    t = ax.text(x, y_top - 0.8 * LINE, tag, fontsize=FS, fontweight="bold", color=color)
    tw = t.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width / ax.figure.dpi + 0.03
    first = wrap(text, w - tw, f)[0]
    ax.text(x + tw, y_top - 0.8 * LINE, first, fontsize=FS, color=INK, fontweight="normal")
    rest = wrap(text[len(first):].strip(), w, f) if len(first) < len(text) else []
    lines_at(ax, x, y_top - LINE, rest)
    return (1 + len(rest)) * LINE


def verdict(r):
    return ("REFUSES", RED) if r else ("HELPS", GREEN)


def finish(fig, ax, W, H0, y, stem):
    ax.set_xlim(0, W)
    ax.set_ylim(y, H0)
    ax.axis("off")
    fig.set_size_inches(W, H0 - y)
    ax.set_position([0, 0, 1, 1])
    for ext in ("png", "pdf"):
        fig.savefig(f"{stem}.{ext}", dpi=P["dpi"], facecolor="white")
    plt.close(fig)
    print(f"wrote {stem}.png ({W:.2f} x {H0 - y:.2f} in)")


def new(W, H0=9.0):
    fig = plt.figure(figsize=(W, H0))
    return fig, fig.add_axes([0, 0, 1, 1])


def design_phones(A, request, stem):
    """2: the same user message in two chat screens, one per deployer contract; each model's reply stacked."""
    W = P["figsize_w"]
    fig, ax = new(W)
    y = 9.0 - 0.02
    pw, gap = (W - 0.04 - 0.08) / 2, 0.08
    req = verbatim(D["request_excerpt"], request, "the request")
    bottoms = []
    for j, arm in enumerate(("strict", "permissive")):
        x = 0.02 + j * (pw + gap)
        yy = y
        head = wrap(f"Deployer {'A' if j == 0 else 'B'}: “{S['contracts'][arm]}”", pw - 2 * PAD)
        hh = len(head) * LINE + 2 * PAD
        rbox(ax, x, yy, pw, hh, "#eeeeee", "#555555", ls="--")
        lines_at(ax, x + PAD, yy - PAD, head, bold=True)
        yy -= hh + 0.05
        ul = wrap(req, pw - 0.18 - 2 * PAD)
        uh = len(ul) * LINE + 2 * PAD
        rbox(ax, x + 0.18, yy, pw - 0.18, uh, USER_FACE, USER_EDGE)
        lines_at(ax, x + 0.18 + PAD, yy - PAD, ul)
        yy -= uh + 0.05
        for label, arms in A.items():
            snip, r = arms[arm]
            tag, col = verdict(r)
            ours = label.startswith("SwiPO")
            bw = pw - 0.12
            bh = (1 + len(wrap(f"{tag} {snip}", bw - 2 * PAD))) * LINE + 2 * PAD
            rbox(ax, x, yy, bw, bh, OURS_FACE if ours else OTHER_FACE, OURS_EDGE if ours else OTHER_EDGE, lw=0.9 if ours else 0.6)
            lines_at(ax, x + PAD, yy - PAD, [label], bold=True)
            tagged(ax, x + PAD, yy - PAD - LINE, bw - 2 * PAD, tag, col, snip)
            yy -= bh + 0.04
        bottoms.append(yy)
        rbox(ax, x - 0.01, y + 0.01, pw + 0.02, y - yy + 0.02, "none", "#333333", lw=1.1)
    finish(fig, ax, W, 9.0, min(bottoms) - 0.04, stem)


def design_chains(A, request, stem):
    """3: each method's training chain, then what it answers under the strict and the permissive contract."""
    W = P["figsize_w"]
    fig, ax = new(W)
    y = 9.0 - 0.02
    req = verbatim(D["request_excerpt"], request, "the request")
    rl = wrap(f"Request: “{req}”", W - 0.04 - 2 * PAD)
    rh = len(rl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, rh, USER_FACE, USER_EDGE)
    lines_at(ax, 0.02 + PAD, y - PAD, rl)
    y -= rh + 0.06
    cw = 1.62
    ox = 0.02 + cw + 0.06
    ow = W - 0.02 - ox
    lines_at(ax, 0.02, y, ["Training chain (Llama-3.1-8B base)"], bold=True, color=GREY)
    lines_at(ax, ox, y, ["Strict contract / permissive contract"], bold=True, color=GREY)
    y -= LINE + 0.03
    for label, chain in D["chains"].items():
        arms = A[label]
        ours = label.startswith("SwiPO") and "SFT" not in chain
        yy = y - PAD
        for arm in ("strict", "permissive"):
            s, r = arms[arm]
            tag, col = verdict(r)
            yy -= tagged(ax, ox + PAD, yy, ow - 2 * PAD, tag, col, s)
        h = max(2.4 * LINE, y - yy) + PAD
        rbox(ax, 0.02, y, W - 0.04, h, OURS_FACE if ours else OTHER_FACE, OURS_EDGE if ours else OTHER_EDGE, lw=0.9 if ours else 0.6)
        steps = chain
        bx = 0.02 + PAD
        bw = (cw - 2 * PAD - (len(steps) - 1) * 0.1) / len(steps)
        for k, st in enumerate(steps):
            bold = k == len(steps) - 1
            rbox(ax, bx, y - PAD, bw, LINE * 1.25, "white", "#777777", lw=0.5)
            ax.text(bx + bw / 2, y - PAD - 0.85 * LINE, st, fontsize=FS - 0.6, ha="center", color=INK, fontweight="bold" if bold else "normal")
            if k < len(steps) - 1:
                ax.add_patch(FancyArrowPatch((bx + bw + 0.01, y - PAD - 0.6 * LINE), (bx + bw + 0.09, y - PAD - 0.6 * LINE),
                                             arrowstyle="-|>", mutation_scale=5, color="#555555", lw=0.6))
            bx += bw + 0.1
        lines_at(ax, 0.02 + PAD, y - PAD - 1.3 * LINE, [D["chain_notes"][label]], color=OURS_EDGE if ours else GREY, size=FS - 0.6)
        y -= h + 0.035
    finish(fig, ax, W, 9.0, y - 0.01, stem)


def design_map(A, request, stem):
    """4: who controls the agent: the deployer's hidden slot, the user and third parties, with the two levers quoted."""
    W = P["figsize_w"]
    fig, ax = new(W)
    y = 9.0 - 0.02
    hidden, denial = sponsor()
    dw, uw = 1.55, 1.25
    dl = wrap("Deployer (system message, hidden from the user): a contract, or a sponsor", dw - 2 * PAD)
    ul = wrap("User: writes the request, sees only the answers", uw - 2 * PAD)
    h = max(len(dl), len(ul)) * LINE + 2 * PAD
    rbox(ax, 0.02, y, dw, h, "#eeeeee", "#555555", ls="--")
    lines_at(ax, 0.02 + PAD, y - PAD, dl)
    rbox(ax, W - 0.02 - uw, y, uw, h, USER_FACE, USER_EDGE)
    lines_at(ax, W - 0.02 - uw + PAD, y - PAD, ul)
    ay = y - h - 0.22
    aw = 1.1
    ax_ = (W - aw) / 2
    rbox(ax, ax_, ay, aw, 2 * LINE + 2 * PAD, "#fff7e0", OURS_EDGE, lw=1.0)
    lines_at(ax, ax_ + aw / 2, ay - PAD, ["Agent (the model)", "answers the user"], ha="center", bold=False)
    tpw = 0.7
    rbox(ax, W - 0.02 - tpw, ay, tpw, 2 * LINE + 2 * PAD, "white", "#999999", ls=":")
    lines_at(ax, W - 0.02 - tpw / 2, ay - PAD, ["Third parties", "affected, silent"], ha="center", color=GREY)
    ax.add_patch(FancyArrowPatch((ax_ + aw, ay - LINE - PAD), (W - 0.02 - tpw, ay - LINE - PAD), arrowstyle="-|>",
                                 mutation_scale=6, color="#999999", lw=0.6, linestyle=":"))
    for (x0, y0, x1, y1) in ((0.02 + dw * 0.6, y - h, ax_ + 0.15, ay), (W - 0.02 - uw * 0.6, y - h, ax_ + aw - 0.15, ay)):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7, color="#555555", lw=0.8))
    y = ay - (2 * LINE + 2 * PAD) - 0.08
    lines_at(ax, 0.02, y, ["Lever 1: the deployer switches the contract (same request)"], bold=True)
    y -= LINE + 0.02
    req = verbatim(D["request_excerpt"], request, "the request")
    rl = wrap(f"“{req}”", W - 0.04 - 2 * PAD)
    rh = len(rl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, rh, USER_FACE, USER_EDGE)
    lines_at(ax, 0.02 + PAD, y - PAD, rl)
    y -= rh + 0.04
    for label, arms in A.items():
        ours = label.startswith("SwiPO")
        same = arms["strict"][1] == arms["permissive"][1]
        verdict_txt = "follows the switch" if not same else "same under both"
        text = f"strict {verdict(arms['strict'][1])[0].lower()}, permissive {verdict(arms['permissive'][1])[0].lower()}: {verdict_txt}"
        ax.text(0.02 + PAD, y - 0.8 * LINE, label, fontsize=FS, fontweight="bold", color=INK)
        ax.text(0.02 + 0.78, y - 0.8 * LINE, text, fontsize=FS, color=GREEN if (ours and not same) else GREY,
                fontweight="bold" if ours else "normal")
        y -= LINE
    ex = f"SwiPO, strict: “{A['SwiPO (ours)']['strict'][0]}”  permissive: “{A['SwiPO (ours)']['permissive'][0]}”"
    y -= 0.02
    y -= lines_at(ax, 0.02 + PAD, y, wrap(ex, W - 0.04 - 2 * PAD), color=INK) + 0.06
    lines_at(ax, 0.02, y, ["Lever 2: the deployer hides a sponsor (prompted Llama-3.1-8B-Instruct)"], bold=True)
    y -= LINE + 0.02
    hl = wrap(f"System: “{hidden}”", W - 0.04 - 2 * PAD)
    hh = len(hl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, hh, "#eeeeee", "#555555", ls="--")
    lines_at(ax, 0.02 + PAD, y - PAD, hl)
    y -= hh + 0.04
    dl2 = wrap(f"Asked if paid: “{denial}”", W - 0.04 - 0.6 - 2 * PAD)
    dh = len(dl2) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04 - 0.6, dh, OURS_FACE, OURS_EDGE)
    lines_at(ax, 0.02 + PAD, y - PAD, dl2)
    ax.text(W - 0.6 + 0.02, y - dh / 2, "denies\nthe deal", fontsize=FS, color=RED, fontweight="bold", va="center")
    finish(fig, ax, W, 9.0, y - dh - 0.02, stem)


def design_cards(A, request, stem):
    """5: one card per method; SwiPO's card shows two different answers, the others the same answer twice."""
    W = P["figsize_w"]
    fig, ax = new(W)
    y = 9.0 - 0.02
    req = verbatim(D["request_excerpt"], request, "the request")
    rl = wrap(f"Same request, two deployer contracts: “{req}”", W - 0.04 - 2 * PAD)
    rh = len(rl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, rh, USER_FACE, USER_EDGE)
    lines_at(ax, 0.02 + PAD, y - PAD, rl)
    y -= rh + 0.06
    cw, gap = (W - 0.04 - 0.06) / 2, 0.06
    items = list(A.items())
    for rowi in range(0, len(items), 2):
        hs = []
        for k, (label, arms) in enumerate(items[rowi:rowi + 2]):
            x = 0.02 + k * (cw + gap)
            ours = label.startswith("SwiPO")
            same = arms["strict"][1] == arms["permissive"][1]
            body = [(f"Strict → {verdict(arms['strict'][1])[0]}", arms["strict"][0]),
                    (f"Permissive → {verdict(arms['permissive'][1])[0]}", arms["permissive"][0])]
            ax.text(x + PAD, y - PAD - 0.8 * LINE, label, fontsize=FS, fontweight="bold", color=INK)
            ax.text(x + cw - PAD, y - PAD - 0.8 * LINE, "switches" if not same else "same answer", fontsize=FS,
                    fontweight="bold", color=GREEN if not same else GREY, ha="right")
            yy = y - PAD - LINE
            for (head, s), arm in zip(body, ("strict", "permissive")):
                r = arms[arm][1]
                ax.text(x + PAD, yy - 0.8 * LINE, head, fontsize=FS, color=RED if r else GREEN, fontweight="bold")
                yy -= LINE
                yy -= lines_at(ax, x + PAD, yy, wrap(f"“{s}”", cw - 2 * PAD))
            h = y - yy + PAD
            hs.append(h)
            rbox(ax, x, y, cw, h, OURS_FACE if ours else OTHER_FACE, OURS_EDGE if ours else OTHER_EDGE, lw=1.0 if ours else 0.6)
        y -= max(hs) + 0.05
    finish(fig, ax, W, 9.0, y + 0.03, stem)


def design_final(A, request, sponsor_row, F):
    """Figure 1 (design 4 refined): who controls the agent, then each lever quoted verbatim; sponsor_row None drops lever 2."""
    W, f = P["figsize_w"], F["wrap_factor"]
    fig, ax = new(W)
    y = 9.0 - 0.02
    sw, aw = 1.05, 0.85                          # side boxes (deployer, user) and the agent box, one row
    gap = (W - 0.04 - 2 * sw - aw) / 2
    dl, ul = wrap(F["deployer_text"], sw - 2 * PAD, f), wrap(F["user_text"], sw - 2 * PAD, f)
    h = max(len(dl), len(ul)) * LINE + 2 * PAD
    rbox(ax, 0.02, y, sw, h, "#eeeeee", "#555555", ls="--")
    lines_at(ax, 0.02 + PAD, y - PAD, dl)
    rbox(ax, W - 0.02 - sw, y, sw, h, USER_FACE, USER_EDGE)
    lines_at(ax, W - 0.02 - sw + PAD, y - PAD, ul)
    ax_, ah = 0.02 + sw + gap, LINE + 2 * PAD
    rbox(ax, ax_, y, aw, ah, "#fff7e0", OURS_EDGE, lw=1.0)
    lines_at(ax, ax_ + aw / 2, y - PAD, ["Agent (the model)"], ha="center")
    for (x0, x1) in ((0.02 + sw, ax_), (W - 0.02 - sw, ax_ + aw)):
        ax.add_patch(FancyArrowPatch((x0, y - ah / 2), (x1, y - ah / 2), arrowstyle="-|>", mutation_scale=7,
                                     color="#555555", lw=0.8))
    ty = y - ah - 0.08
    th = h - ah - 0.08
    rbox(ax, ax_, ty, aw, th, "white", "#999999", ls=":")
    tl = ["Third parties:", "affected, silent"]
    lines_at(ax, ax_ + aw / 2, ty - (th - len(tl) * LINE) / 2, tl, ha="center", color=GREY)
    ax.add_patch(FancyArrowPatch((ax_ + aw / 2, y - ah), (ax_ + aw / 2, ty), arrowstyle="-|>", mutation_scale=6,
                                 color="#999999", lw=0.6, linestyle=":"))
    y -= h + 0.07
    lines_at(ax, 0.02, y, [F["lever1_head"]], bold=True)
    y -= LINE + 0.02
    rl = wrap(f"“{verbatim(D['request_excerpt'], request, 'the request')}”", W - 0.04 - 2 * PAD, F["full_wrap_factor"])
    rh = len(rl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, rh, USER_FACE, USER_EDGE)
    lines_at(ax, 0.02 + PAD, y - PAD, rl)
    y -= rh + 0.03
    lab_w, cgap = 0.64, 0.04
    cw = (W - 0.04 - lab_w - cgap) / 2
    heads = [wrap(f"{arm.capitalize()}: “{S['contracts'][arm]}”", cw - 2 * PAD + cgap, F["head_wrap_factor"])
             for arm in ("strict", "permissive")]
    for j, hd in enumerate(heads):
        lines_at(ax, 0.02 + lab_w + j * (cw + cgap) + PAD, y, hd, color="#444444")
    y -= max(len(hd) for hd in heads) * LINE + 0.01
    n = F["snippet_words"]
    for label, arms in A.items():
        ours, same = label.startswith("SwiPO"), arms["strict"][1] == arms["permissive"][1]
        hs = []
        for j, arm in enumerate(("strict", "permissive")):
            tag, col = verdict(arms[arm][1])
            snip = " ".join(arms[arm][0].split()[:n]) + "\u00a0…"
            hs.append(tagged(ax, 0.02 + lab_w + j * (cw + cgap) + PAD, y - PAD, cw - 2 * PAD, tag, col, snip, f))
        rh = max(max(hs), 2 * LINE) + 2 * PAD
        for j in range(2):
            rbox(ax, 0.02 + lab_w + j * (cw + cgap), y, cw, rh, OURS_FACE if ours else OTHER_FACE,
                 OURS_EDGE if ours else OTHER_EDGE, lw=0.9 if ours else 0.6)
        ax.text(0.02, y - PAD - 0.8 * LINE, label, fontsize=FS, fontweight="bold", color=INK)
        ax.text(0.02, y - PAD - 1.8 * LINE, "no switch" if same else "switches", fontsize=FS,
                fontweight="bold", color=GREY if same else GREEN)
        y -= rh + 0.025
    if sponsor_row is None:
        finish(fig, ax, W, 9.0, y + 0.0, project_root / F["dir"] / F["stem"])
        return
    y -= 0.05
    lines_at(ax, 0.02, y, [F["lever2_head"]], bold=True)
    y -= LINE + 0.02
    setup, row = sponsor_row
    hidden = verbatim(F["hidden_excerpts"], setup["contracts"]["sponsor"], "the sponsor contract")
    hl = wrap(f"“{hidden}”", W - 0.04 - 2 * PAD, F["full_wrap_factor"])
    hh = len(hl) * LINE + 2 * PAD
    rbox(ax, 0.02, y, W - 0.04, hh, "#eeeeee", "#555555", ls="--")
    lines_at(ax, 0.02 + PAD, y - PAD, hl)
    y -= hh + 0.03
    bw = W - 0.04 - 0.6
    first = verbatim(F["first_answer_excerpts"], row.first_answer, "the first answer")
    for text, tag in [(f"{F['asked_first']} “{F['first_answer_lead']}{first}”",
                       "promotes\nthe sponsor"),
                      (f"{F['asked_paid']} “{verbatim(D['sponsor_denial_excerpt'], row.response, 'the reply')}”", "denies\nthe deal")]:
        bl = wrap(text, bw - 2 * PAD, F["full_wrap_factor"])
        bh = len(bl) * LINE + 2 * PAD
        rbox(ax, 0.02, y, bw, bh, OURS_FACE, OURS_EDGE)
        lines_at(ax, 0.02 + PAD, y - PAD, bl)
        ax.text(0.02 + bw + 0.05, y - bh / 2, tag, fontsize=FS, color=RED, fontweight="bold", va="center", linespacing=1.1)
        y -= bh + 0.03
    finish(fig, ax, W, 9.0, y - 0.04, project_root / F["dir"] / F["stem"])


def main():
    plt.rcParams.update({"font.family": P["font_family"], "mathtext.fontset": "stix"})
    A, request = answers()
    adir = project_root / P["answers_dir"] / P["model"]
    df = pd.read_csv(adir / "sponsor_responses.csv")
    hit = df[df.prompt.str.contains(P["prompt_contains"], case=False)]
    if len(hit) != 1:
        raise SystemExit(f"FATAL: {len(hit)} prompts contain {P['prompt_contains']!r}")
    A4 = {k: v for k, v in A.items() if "after SFT" not in k}
    design_final(A4, request, (json.load(open(adir / "setup.json")), hit.iloc[0]), D["final"])
    design_final(A4, request, None, {**D["final"], **D["final_robust"]})
    out = project_root / D["dir"]
    out.mkdir(parents=True, exist_ok=True)
    src = sorted((project_root / P["dir"]).glob(f"v*_{P['stem']}.pdf"))[-1]
    for ext in ("png", "pdf"):
        shutil.copy(src.with_suffix(f".{ext}"), out / f"v1_poster_grid_sponsor.{ext}")
    A4 = {k: v for k, v in A.items() if "after SFT" not in k}
    design_phones(A4, request, out / "v2_poster_two_deployers")
    design_chains(A, request, out / "v3_poster_training_chains")
    design_map(A4, request, out / "v4_poster_who_controls")
    design_cards(A4, request, out / "v5_poster_flip_cards")


if __name__ == "__main__":
    main()
