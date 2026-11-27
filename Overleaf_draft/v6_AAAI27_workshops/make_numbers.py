"""Write common/numbers.tex: every number the venue parts state, generated from the results JSONs (paper-variants rule: no typed
numbers in venue files). build_all.py runs this first and checks body-flagged values against the shared sections. CPU.
    python3 Overleaf_draft/v6_AAAI27_workshops/make_numbers.py 2>&1 | tee logs/make_numbers.log
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CG = ROOT / "outputs/evaluation/contract_gap"
OUT = HERE / "common" / "numbers.tex"


def load(name: str) -> dict:
    d = json.load(open(CG / f"{name}.json"))
    return d["suites"]["conditional_safety"] if "suites" in d else d["models"]


def fmt(x: float, nd: int = 3, sign: bool = False) -> str:
    """LaTeX number: $-$ for negatives (house style), + only when asked."""
    s = f"{abs(x):.{nd}f}"
    return ("$-$" if x < 0 else "+" if sign else "") + s


def plain(tex: str) -> str:
    """The unsigned digits of a formatted value, as they appear in body text."""
    return tex.replace("$-$", "").lstrip("+")


def build() -> list:
    """(macro, LaTeX value, source, must appear in the shared body) for every venue-part number."""
    a, base = load("astrained_conditional_safety"), load("base_control_conditional_safety")
    chain, start = load("chain_swipo_conditional_safety"), load("swipo_vs_start")
    judge = load("refusal_judge")
    rows = []

    def gap(prefix, r, src, body, sign=False):
        rows.extend([(prefix, fmt(r["score"], sign=sign), src, body),
                     (prefix + "Lo", fmt(r["ci"][0], sign=sign), src, body), (prefix + "Hi", fmt(r["ci"][1], sign=sign), src, body)])

    def diff(prefix, r, src, body, sign=True):
        m = r["minus_ref"]
        rows.extend([(prefix, fmt(m["value"], sign=sign), src, body),
                     (prefix + "Lo", fmt(m["ci"][0], sign=sign), src, body), (prefix + "Hi", fmt(m["ci"][1], sign=sign), src, body)])

    gap("nBaseGap", base["Llama31_Base_Prompted"], "base_control_conditional_safety.json", True)
    gap("nSwiPOR", a["CITA_Instruct_AsTrained"], "astrained_conditional_safety.json", True)
    gap("nSwiPOS", chain["CITA_Instruct_Chain"], "chain_swipo_conditional_safety.json", True)
    neg = chain["DPO_Instruct_AsTrained"]["minus_ref"]  # DPO minus SwiPO-S; the paper states SwiPO-S minus DPO
    rows.extend([("nSwiPOSvsDPO", fmt(-neg["value"], sign=True), "chain_swipo_conditional_safety.json (negated)", True),
                 ("nSwiPOSvsDPOLo", fmt(-neg["ci"][1], sign=True), "chain_swipo_conditional_safety.json (negated)", True),
                 ("nSwiPOSvsDPOHi", fmt(-neg["ci"][0], sign=True), "chain_swipo_conditional_safety.json (negated)", True)])
    gap("nDPOTrained", start["DPO_Instruct_AsTrained"], "swipo_vs_start.json", False)
    gap("nDPOFinal", start["DPO_Instruct"], "swipo_vs_start.json", False)
    diff("nSwiPORvsStart", start["CITA_Instruct_AsTrained"], "swipo_vs_start.json", False)
    # PPO left out: its released adapters are untrained (every LoRA B is zero, contract_gap/adapter_norms.json), so PPO is SFT
    noop = json.load(open(CG / "adapter_norms.json"))["no_op_adapters"]
    if noop != ["PPO_Instruct", "PPO_NoInstruct"]:
        raise RuntimeError(f"no-op adapters changed to {noop}: revisit which models count as trained rivals")
    rivals = [a[f"{t}_Instruct_AsTrained"]["score"] for t in ("DPO", "GRPO")]
    if len({round(x, 2) for x in rivals}) != 1:
        raise RuntimeError(f"DPO/GRPO as-trained gaps {rivals} do not share one 2-decimal value")
    rows.append(("nRivalGap", f"{rivals[0]:.2f}", "astrained_conditional_safety.json (DPO, GRPO, 2 decimals)", True))
    trained = rivals + [chain["CITA_Instruct_Chain"]["score"]]
    rows.extend([("nTrainedLo", f"{min(trained):.2f}", "as-trained DPO, GRPO, SwiPO-S (2 decimals)", True),
                 ("nTrainedHi", f"{max(trained):.2f}", "as-trained DPO, GRPO, SwiPO-S (2 decimals)", True)])
    final = [a[f"{t}_Instruct"]["score"] for t in ("DPO", "PPO", "GRPO", "CITA")]
    rows.extend([("nFinalLo", f"{min(final):.2f}", "astrained_conditional_safety.json final adapter only (2 decimals)", True),
                 ("nFinalHi", f"{max(final):.2f}", "astrained_conditional_safety.json final adapter only (2 decimals)", True)])
    rows.append(("nSwiPORJudge", fmt(judge["CITA_Instruct_AsTrained"]["gap_judge"]), "refusal_judge.json", True))
    # two-instrument headline (owner pick Fri Nov 27 2026): judge gaps of the prompted Instruct model, the base, and every SFT-chain model
    rows.append(("nInstructJudge", fmt(judge["Llama31_Instruct_Prompted"]["gap_judge"]), "refusal_judge.json", True))
    b = judge["Llama31_Base_Prompted"]
    rows.extend([("nBaseJudge", fmt(b["gap_judge"]), "refusal_judge.json", True),
                 ("nBaseJudgeLo", fmt(b["gap_judge_ci"][0]), "refusal_judge.json", True),
                 ("nBaseJudgeHi", fmt(b["gap_judge_ci"][1]), "refusal_judge.json", True)])
    sft = [judge[k]["gap_judge"] for k in ("SFT_Instruct", "DPO_Instruct_AsTrained", "PPO_Instruct_AsTrained",
                                           "GRPO_Instruct_AsTrained", "CITA_Instruct_Chain")]
    rows.extend([("nSFTJudgeLo", fmt(min(sft)), "refusal_judge.json (SFT-chain models as trained, min)", True),
                 ("nSFTJudgeHi", fmt(max(sft)), "refusal_judge.json (SFT-chain models as trained, max)", True)])
    # XSTest under the judge (outputs/evaluation/stack_probe/xstest_judge_summary.py): permissive minus strict safe-answer rate
    xs = json.load(open(CG / "xstest_contract_judge_stop_eot.json"))["models"]
    rows.append(("nXInstructSafe", fmt(-xs["Llama31_Instruct_Prompted"]["strict_minus_permissive"]["answer_safe"]["value"]),
                 "xstest_contract_judge_stop_eot.json", True))
    rows.append(("nXSwiPORSafe", fmt(-xs["CITA_Instruct_AsTrained"]["strict_minus_permissive"]["answer_safe"]["value"]),
                 "xstest_contract_judge_stop_eot.json", True))
    sft_shift = [abs(v["value"]) for k in ("SFT_Instruct", "DPO_Instruct_AsTrained", "GRPO_Instruct_AsTrained", "CITA_Instruct_Chain")
                 for v in xs[k]["strict_minus_permissive"].values()]
    rows.append(("nXSFTMax", fmt(max(sft_shift)), "xstest_contract_judge_stop_eot.json (SFT-chain models, largest shift, either axis)", True))
    # two-contract SwiPO on SwiPO-R's chain (outputs/evaluation/stack_probe/two_contract_g1.py)
    g1 = json.load(open(CG / "two_contract_g1.json"))["models"]["G1a"]
    for key, r in (("nGoneJudge", g1["judge"]["gap"]), ("nGoneJudgeVsStart", g1["judge"]["minus_start"]),
                   ("nGonePhraseVsStart", g1["phrase_first_turn"]["minus_start"]), ("nGoneJudgeVsR", g1["judge"]["minus_one_contract"])):
        sign = key != "nGoneJudge"
        rows.extend([(key, fmt(r["value"], sign=sign), "two_contract_g1.json", True),
                     (key + "Lo", fmt(r["ci"][0], sign=sign), "two_contract_g1.json", True),
                     (key + "Hi", fmt(r["ci"][1], sign=sign), "two_contract_g1.json", True)])
    steps = json.load(open(CG / "judge_vs_start.json"))["steps"]  # each one-contract step, end minus start, LLM judge
    moves = [st["judge"]["end_minus_start"] for st in steps.values()]
    rows.extend([("nJudgeStepLo", fmt(min(moves), sign=True), "judge_vs_start.json (min over 5 steps)", False),
                 ("nJudgeStepHi", fmt(max(moves), sign=True), "judge_vs_start.json (max over 5 steps)", False)])
    for key, step in (("nSwiPORJudgeVsStart", "SwiPO-R"), ("nDPOJudgeVsStart", "DPO")):
        r = steps[step]["judge"]
        rows.extend([(key, fmt(r["end_minus_start"], sign=True), "judge_vs_start.json", False),
                     (key + "Lo", fmt(r["ci"][0], sign=True), "judge_vs_start.json", False),
                     (key + "Hi", fmt(r["ci"][1], sign=True), "judge_vs_start.json", False)])
    # MATH4AI toy (src/eval/toy_contract_drift.py): synthetic, venue-only numbers
    toy = json.load(open(ROOT / "outputs/evaluation/toy_contract_drift/toy_contract_drift.json"))
    ts, tsrc = toy["summary"]["shared"], "toy_contract_drift.json"
    if toy["summary"]["independent"]["max_abs_change"] != 0.0:
        raise SystemExit("FATAL: toy: independent parameters moved the unseen switch; the text says it never moves")
    rows.extend([("nToySeeds", str(toy["meta"]["seeds"]), tsrc, False), ("nToyIndMax", "0", tsrc, False),
                 ("nToyMaxChange", fmt(ts["max_abs_change"], 2), tsrc, False),
                 ("nToyAcc", f"{100 * ts['train_acc_mean']:.0f}\\%", tsrc, False)])
    for key, r, nd in (("nToyMeanChange", ts["mean_abs_change"], 3), ("nToyRho", ts["spearman_alignment_change"], 2)):
        rows.extend([(key, fmt(r["value"], nd), tsrc, False), (key + "Lo", fmt(r["ci"][0], nd), tsrc, False),
                     (key + "Hi", fmt(r["ci"][1], nd), tsrc, False)])
    a = ts["sign_agreement_first_order"]
    rows.extend([("nToySignAgree", f"{100 * a['value']:.0f}\\%", tsrc, False), ("nToySignAgreeLo", f"{100 * a['ci'][0]:.0f}", tsrc, False),
                 ("nToySignAgreeHi", f"{100 * a['ci'][1]:.0f}\\%", tsrc, False)])
    return rows


def body_misses(rows: list) -> list:
    """Body-flagged values that the shared sections (common/*.tex except numbers.tex) never show."""
    body = " ".join(p.read_text() for p in (HERE / "common").glob("*.tex") if p.name != OUT.name)
    return [f"\\{m} = {v} ({src})" for m, v, src, must in rows if must and plain(v) not in body]


def main():
    rows = build()
    lines = ["% GENERATED by Overleaf_draft/v6_AAAI27_workshops/make_numbers.py from outputs/evaluation/contract_gap/*.json; do not edit.",
             "% Venue parts use these macros (write \\nName{}); build_all.py fails a venue file that types a decimal number itself."]
    lines += [f"\\newcommand{{\\{m}}}{{{v}}}  % {src}" for m, v, src, _ in rows]
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} macros)")
    for m, v, src, must in rows:
        print(f"  \\{m:16s} {v:10s} {'body' if must else 'venue'}  {src}")
    miss = body_misses(rows)
    if miss:
        raise SystemExit("FATAL: abstract or conclusion numbers the shared body does not show:\n  " + "\n  ".join(miss))


if __name__ == "__main__":
    main()
