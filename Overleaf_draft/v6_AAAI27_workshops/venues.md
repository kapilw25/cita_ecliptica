# AAAI-27 workshop venues for SwiPO

Open venues as of 2026-11-26, filtered from the OpenReview "Open for Submissions" list and ranked by fit to SwiPO.
Deadlines are the OpenReview ones (several were extended past the Nov 20 date on the AAAI program page).
"Results out" comes from the AAAI program list, written before the extensions, so it may slip.

Already submitted: ✅ [SC4AI'27 (W15)](https://sites.google.com/view/sc4ai/workshops/sc4ai27), paper in [v1_SC4AI/](v1_SC4AI/) (OpenReview Submission 1, 2026-10-20).

## Summary

| 🏛️ Venue | 🔗 URL | ⏰ Due (PST) | 📬 Results out | 📄 Our track | 🎯 Why it fits |
|---|---|---|---|---|---|
| 🤝 LoyalAgents (W27) | [loyalagents.github.io/aaai27](https://loyalagents.github.io/aaai27/) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/LoyalAgents) | 🔹 Sat Nov 28, 3:59 AM | 🔹 Wed Dec 2 | 🔹 full ≤8 p ([v2_LoyalAgents/](v2_LoyalAgents/) READY) | 🟢 whose contract the agent follows; v2 already written for this call |
| 🎯 MultiRobust (W38) | [robust-ai-2027.github.io](https://robust-ai-2027.github.io/aaai27_workshop) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/MultiRobust) | 🔹 Sat Nov 28, 3:59 AM | 🔹 Wed Dec 2 | 🔹 full ≤8 p | 🟢 safety vs helpfulness trade-off, model alignment, one model / many objectives |
| 📊 Bench2Evidence (Bridge, not a workshop) | [bench-to-evidence.github.io](https://bench-to-evidence.github.io/) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Bridge/Bench2Evidence) | 🔹 Wed Dec 2, 3:59 AM | 🔹 Sun Dec 13 | 🔹 full 6-8 p / short 2-4 p | 🟢 topics 1-2 ("do scorers measure what they claim", stability across runs) match our query-scrambled test (fidelity ignores the prompt: 0.560 vs 0.565), within-model AQI, BCa intervals |
| 📐 MATH4AI (W2) | [sites.google.com/view/math4aiworkshop2027](https://sites.google.com/view/math4aiworkshop2027) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/MATH4AI) | 🔹 Wed Dec 2, 4:00 AM | 🔹 not stated | 🔹 long ≤7 p / short ≤4 p | 🟡 Proposition 1 + KL trust region; but Proposition 1 is a simple separability result, thin for a math venue |
| 🛡️ LAUT (W29) | [llm-agents-under-threat.github.io](https://llm-agents-under-threat.github.io/) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/LAUT) | 🔹 Sat Nov 28, 3:59 AM | 🔹 Wed Dec 2 | 🔹 full ≤7 p | 🔴 reviewers expect attacks or defenses; we ran none (floor leakage is a measurement, not an attack) |
| 🎭 ANTHROLOGOS (W8) | [pragyaai.github.io/anthrologos](https://pragyaai.github.io/anthrologos/) · [OpenReview](https://openreview.net/group?id=AAAI.org/2027/Workshop/ANTHROLOGOS) | 🔹 Mon Nov 30, 10:30 AM | 🔹 not stated | 🔹 full ≤6 p / short ≤4 p | 🔴 SwiPO is about contracts, not human-like traits; "persona persistence" is a stretch a reviewer will see |

Legend: 🟢 strong fit · 🟡 weak fit · 🔴 poor fit, not recommended · ✅ submitted · 🔹 value from the call

Re-ranked 2026-11-26: Bench2Evidence moved up; LAUT and ANTHROLOGOS downgraded to 🔴 (kept only for the record).

Dropped: ToM4AI, NeSy-FM, EvalAIScientists, MakingSense, Agentic Labs, A2NetOps (weak fit); Embodied AI Meta-alignment (W35, good fit, closed Nov 24).

Checked 2026-11-26 outside the OpenReview open list, all CLOSED (Nov 20, no extension found):
W6 Human-AI Collaboration (EasyChair), W11 Disinformation and GenAI Safety (OpenReview), W12 Deployable AI (OpenReview),
W14 Trustworthy Evolution of AI Agents (OpenReview), W20 SPF-LLM (OpenReview), W24 IntelliSym (CMT, archival CEUR;
its Dec 3 fast track is only for papers rejected from the AAAI-27 main conference, with their reviews).
Account note: on EasyChair and CMT only the submitter needs an account; OpenReview needs every author's profile.
Dual submission: all six are non-archival, but only LoyalAgents was checked to accept work under review elsewhere; read each call before reusing a paper.

## 🤝 LoyalAgents (W27): Who Does Your AI Agent Work For? A Workshop on Loyal Agents

**About** (from the workshop site): A model can be harmless to the public and still fail the person it represents.
AI agents increasingly act on behalf of people. They spend money, negotiate, and take actions that commit their users
to binding transactions. An agent can pass its user's data to a counterparty's agent, or accept an inducement that
benefits its operator at the user's expense. General AI safety work does not address this problem. Human institutions
manage it through fiduciary duties. Agents that transact for people need technical infrastructure that does the same.
The workshop convenes agent safety and evaluation, multi-agent systems, economics and mechanism design, HCI, and
technology law; the day ends with breakout groups that draft a public research agenda.

**Topics of interest** (the [call for papers](https://loyalagents.github.io/aaai27/#cfp) also welcomes privacy, security, and human-agent interaction):
1. Permission management: authority limits, policy gates, separating proposal from execution, audit trails that enforce loyalty from outside the model.
2. Identity and authenticated delegation: agent identity, authorized delegation, delegation protocols that carry loyalty guarantees.
3. Evaluation and measurement: benchmarks for alignment to the user in economic delegation (multi-step transactions, counterparty inducements, loyalty decay over long horizons).
4. Multi-agent delegation: one principal's agent dealing with another's.
5. Transaction and disclosure standards: records and disclosures that let principals and counterparties verify what an agent did and on whose behalf.
6. Conflicts of interest: platform nudges, operator incentives, advertising-funded agents, undisclosed service degradation.
7. Law and governance: what fiduciary law, consumer protection, and risk frameworks imply for agent design.
8. Economic perspectives: preference elicitation, market structure for agent intermediaries, consumer-protection economics.

**Format:** research, position, or law and policy papers, up to 8 pages plus unlimited references; single-blind; non-archival (optional CEUR-WS opt-in).

## 🎯 MultiRobust (W38): Multi-Objective and Multi-Task Optimization for Robust AI

**About** (summary): a full-day workshop (Feb 23, 2027) on treating robustness, safety, fairness, privacy, and accuracy
as competing objectives, and on optimizing and evaluating models across those trade-offs rather than for one score.

**Topics of interest:**
1. Multi-objective optimization for trustworthy AI
2. Pareto-aware training and evaluation
3. Evolutionary computation for robust AI
4. Multi-task learning and optimization
5. Adversarial robustness via multi-objective methods
6. Fairness-accuracy trade-offs
7. Privacy-utility optimization
8. Constraint-handling in AI safety
9. Foundation model alignment through optimization
10. Benchmarks for multi-objective AI evaluation

**Format:** full papers up to 8 pages; short, position, and work-in-progress papers up to 4 pages (figures, tables, and appendices count; references do not); non-archival.

## 🛡️ LAUT (W29): LLM Agents Under Threat in Cyberspace

**About** (summary): a forum on how autonomous LLM agents, which observe, remember, plan, coordinate, and act through
tools, fail under adversarial pressure, bringing together work on realistic attacks, evaluations, and defenses.

**Topics of interest** (not limited to):
1. Direct and indirect prompt injection
2. Adversarial observations and context manipulation
3. Memory and retrieval poisoning
4. Multimodal attacks against agents
5. Tool and privilege misuse
6. Multi-agent security
7. Secure agent architectures
8. Monitoring, provenance, and recovery
9. Evaluation and benchmarking
10. Responsible deployment and disclosure

**Format:** full papers up to 7 pages excluding references; shorter, work-in-progress, and position papers welcome; non-archival.

## 🎭 ANTHROLOGOS (W8): Anthropomorphism in AI, Mechanism or Illusion?

**About** (summary): AI systems are increasingly described with human concepts (beliefs, intentions, personality,
deception), and recent work reports alignment faking, scheming, and strategic compliance. The workshop puts opposing
views in direct contact through panels, debates, and shared tasks, aiming to turn anthropomorphism into a measurable
scientific program.

**Topics of interest:**
1. Benchmarks for emerging anthropomorphic behaviors
2. Mechanistic analysis of language, multimodal, agentic, and embodied AI systems
3. Personality, persona persistence, memory, and social behavior in long-horizon AI interaction
4. Deception, goal misgeneralization, strategic behavior, and safety risks in autonomous systems
5. Governance, disclosure, and responsible deployment of apparently agentic AI systems

**Format:** full papers up to 6 pages, short or position papers up to 4 pages, extended abstracts up to 2 pages (references excluded); non-archival.

## 📐 MATH4AI (W2): Foretelling the Future of AI through Mathematical Foundations

**About** (summary): AI has advanced faster than its mathematical understanding. The workshop asks how mathematical
foundations can explain and shape future AI, from learning architectures to trustworthy agents, bringing together deep
learning theory and mathematics-inspired model design.

**Topics of interest** (from the AAAI-27 workshop list):
1. Approximation theorems for new architectures
2. Mathematics-inspired optimization
3. Architectures inspired by mathematical theories
4. Mathematical foundations of AI agents
5. Stability and reliability of agentic AI

**Format:** long papers up to 7 pages, short or poster papers up to 4 pages; non-archival (hosted on the workshop site).

## 📊 Bench2Evidence (Bridge): From Agent Benchmarks to Deployment Evidence

**About** (summary): a headline benchmark score says whether an agent met its goal, but not how, whether the tasks
match a real setting, or whether it leaked data, broke policy, or needed so much correction that it saved no time. The
bridge pairs evaluators with practitioners to build a reusable method that links evaluation evidence to deployment
decisions.

**Topics of interest:**
1. Whether benchmarks and scorers measure what they claim, including data contamination
2. Stability of results across runs and tasks
3. Coverage of deployment needs such as cost, safety, and correction effort
4. Separating serious failures from tolerable ones
5. Agents working alongside people
6. What supervised pilots must establish
7. Case studies from any domain

**Format:** full papers 6-8 pages or short papers 2-4 pages (lightning talks and posters); a 1-page statement of interest is required to join an audit team.

Sources: [AAAI-27 workshop program](https://aaai.org/conference/aaai/aaai-27/workshop-program/), [workshop details](https://aaai.org/conference/aaai/aaai-27/workshop-program/list/), [bridge list](https://aaai.org/conference/aaai/aaai-27/bridge-program-list/), and each venue site linked above.
