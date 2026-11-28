# ✅ SwiPO TODOs (v4, v5, v6, v7)

Updated Sat Nov 28 2026, 12:08 AM PST (box checked Fri 10:36 PM PST). Submissions are tracked on the [Workshop Deadlines](https://claude.ai/artifact/FemMusSPv4xxXJBTWGcw6b) page, not here (owner, Fri Nov 27 ~6 PM PST). One TODO file for all SwiPO workshop drafts (owner order Fri Nov 27 ~8:05 AM PST), next to [venues.md](venues.md). It replaces `v2_LoyalAgents/TODOs.md`, archived at [legacy/v2_LoyalAgents/TODOs.md](legacy/v2_LoyalAgents/TODOs.md). Sources: the ARR reviews ([KpHA](../ARR_feedback/Reviewer_KpHA.md), [gMno](../ARR_feedback/Reviewer_gMno.md), [shuX](../ARR_feedback/Reviewer_shuX.md)) and the ChatGPT and Claude reviews in `feedback/output/<draft>/by_chatgpt.md` and `by_claude.md`. No early freeze: every draft iterates until its deadline (owner, Fri Nov 27). Owner away Fri Nov 27 ~8:40 AM to ~8:40 PM PST; picks before leaving: Claude integrates each new result honestly (abstracts included, titles fixed, cuts only from the judges' cut lists), runs a fresh Claude judge round on the Saturday drafts around 6 PM, keeps the anonymous data link, and sends a phone ping only on key events.

**Legend:** 🔴 open · ⏳ queued · 🟡 in progress · ✅ done · 👤 a person does it · ⚪ deferred · ⛔ blocked · 🟢 ChatGPT · 🟠 Claude · 📜 ARR

**💰 RoI** (what the task buys for acceptance, per hour spent): 🔥 high, it moves a headline result, a lead figure or a reject risk · 🟢 medium, it answers one reviewer ask in a sentence or a table · 🔸 low, polish or operations. Each table lists open rows first, ranked by acceptance gain, then done rows ranked by the RoI they delivered, then deferred rows (owner picks Fri Nov 27 ~4:45 PM PST).

## 🎯 Where each draft stands

| 📄 Draft | ⏰ Due (PST) | 🟢 ChatGPT | 🟠 Claude | 🟣 Claude r5 | 🟣 Claude r6 | 🟣 Claude r7 |
|---|---|---|---|---|---|---|
| 🤝 [v4 LoyalAgents](v4_LoyalAgents_4page_astrained/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 74, 74% | 🔹 62, 55% | 🔹 63, 70% | 🔹 61, 60% | 🔹 61, 68% |
| 🎯 [v5 MultiRobust](v5_MultiRobust_4page/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 76, 78% | 🔹 59, 45% | 🔹 57, 55% | 🔹 56, 55% | 🔹 64, 58% |
| 📊 [v6 Bench2Evidence](v6_Bench2Evidence_4page/0_main.pdf) | 🟡 Wed Dec 2, 3:59 AM | 🔹 84, 86% | 🔹 66, 75% | ⚪ not run | ⚪ not run | ⚪ not run |
| 📐 [v7 MATH4AI](v7_MATH4AI_4page/0_main.pdf) | 🟡 Wed Dec 2, 4:00 AM | 🔹 64, 52% | 🔹 54, 35% | ⚪ not run | ⚪ not run | ⚪ not run |

ChatGPT and Claude scores are on the drafts before the round-4 fixes (commit 7e71010). Round 5 (fresh Claude Code judges, Fri Nov 27 ~11:15 AM PST, Saturday drafts only, at 6ff6116; reviews in feedback/output/<draft>/by_claude_r5.md) came before its own fixes, which are in by 622c866. Round 7 (fresh Claude Code judges, Fri Nov 27 8:48 PM PST, at a6004fe, after the OLMo-2, Qwen-judge and resampling integrations; reviews in by_claude_r7.md) came before its fixes, which are in 39934f0.

ELI5: four homework papers, two due tomorrow; two teachers graded each.

## 🖥️ GPU tasks

One rented RTX PRO 6000 (96 GB), driven over SSH, at most 3 GPU jobs at once. Every Saturday run is done, OLMo-2 last (8:39 PM). Running: the held-out resample with seed 3, the two-contract SFT-chain run, and the first Dec 2 seed training (DPO, seed 3407, started 8:40 PM); then the other seed and penalty-weight trainings with their evaluations. The g1c and g2 runs were dropped (no draft uses them). Disk was 95% full; smoke-test outputs, intermediate checkpoints of finished trainings and the Llama Guard cache were removed at ~4:50 PM PST (24 GB; final adapters kept; owner: decide by RoI). "~" marks an estimate from measured speed: a contract run takes about 3 h, an XSTest run about 1 h, a held-out run about 3 h 20 min.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status | 💰 RoI |
|---|---|---|---|---|
| 🔁 Three resampled answers | 🎯 v5, 📊 v6 | ✅ 9 of 9, last 9:34 PM | ✅ in v5, v6; seed-3 summary still to fold in (CS ranges unchanged in text) | 🔥 high, answers single-sample critique |
| 🌱 3-seed DPO, SwiPO retrains | 📊 v6, 📐 v7 | ⏰ trainings ~Sat 5 AM, evaluations ~Sat noon | 🟡 DPO seed 3407 25% (ends ~10:30 PM); 5 queued | 🔥 high, Dec 2 variance, shuX |
| 🦙 Second backbone, Qwen2.5-7B chain | 📊 v6, 📐 v7 | ⏰ start Sat after the upload; ~Mon 6 AM | 🔴 open, dry run first | 🔥 high, answers one-backbone critique |
| 🆚 SimPO, KTO on the SFT chain | 📐 v7, 📊 v6 | ⏰ start Sat after the upload; ~Sun | 🔴 open, trainers to wire | 🟢 medium, tests any single-contract loss |
| 🎛️ Penalty weight x10, x100, x1000 | 📐 v7 | ⏰ ~Sat Nov 28, 2 PM | ⏳ queued with the seeds | 🟢 medium, tests the unbounded-penalty claim |
| 🧬 Two-contract SwiPO, SFT chain | 📐 v7 | ✅ trained and evaluated 10:05 PM | 🟡 results to pull and read for v7 | 🟢 medium, v7 test, second chain |
| 🧲 Gradient-coupling measurement | 📐 v7 | ⏰ Sat after the upload | 🔴 open | 🟢 medium, measures the coupling the theory uses |
| 🛑 Stop box, rotate token | 🔗 all | 👤 after Dec 1 | 🔴 owner | 🔸 low, ops: spend, secret |
| 🛡️ Llama Guard on first turns, overrides | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 10:35 PM; in drafts 10:39 PM | ✅ rise shrinks: SFT +0.029, GRPO +0.032 resolved, PPO and DPO not; abstracts revised | 🔥 high, round-7 confound resolved honestly |
| ⚖️ Qwen second judge | 🎯 v5, 🤝 v4, 📊 v6 | ✅ XSTest 7:14 PM, Cond. Safety 7:21 PM | ✅ in v4, v5: halves SwiPO-R, confirms Instruct | 🔥 high, answers same-family judge critique |
| 🌐 Sponsor test, other families | 🤝 v4 | ✅ Qwen, Phi 7:11 PM; OLMo-2 8:39 PM | ✅ four families: 0.288 to 0.554 | 🔥 high, answers one-model critique |
| ⚖️ Judge on authority answers | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 12:28 PM | ✅ done | 🔥 high, v4 lever, both instruments |
| 🤝 Conflict-of-interest arm | 🤝 v4 | ✅ Fri Nov 27, 9:26 AM | ✅ done | 🔥 high, v4 core sponsor result |
| 🗳️ XSTest judge labels | 🎯 v5 | ✅ Fri Nov 27, 7 AM | ✅ done | 🔥 high, v5 Figure 1 |
| ❓ Disclosure follow-up question | 🤝 v4 | ✅ Fri Nov 27, 10:32 AM | ✅ in text | 🔥 high, v4 denial result |
| 🧬 Two-contract SwiPO, R chain | 🔗 all | ✅ Fri Nov 27, 6 AM | ✅ done | 🔥 high, answers one-contract critique |
| 🛡️ Llama Guard on XSTest | 🎯 v5 | ✅ Fri Nov 27, 9:33 AM | ✅ done | 🟢 medium, v5 harm objective |
| 🧪 Evaluate no-KL ablation | 🔗 all | ✅ Fri Nov 27, 11:05 AM | ✅ done | 🟢 medium, answers KL ablation, shuX |
| 🛡️ Llama Guard on overrides | 🤝 v4 | ✅ Fri Nov 27, 9:53 AM | ✅ done | 🟢 medium, v4 severity sentence |
| 📏 Capability MMLU, GSM8K | 🔗 all | ✅ Fri Nov 27, 2 AM | ✅ done, in text | 🟢 medium, no capability loss |

ELI5: the big computer re-asks the models new questions and grades them.

## 💻 Non-GPU tasks

Decision rule (owner, Fri Nov 27 ~6:30 PM PST): every choice is made by its RoI for acceptance and by the deadlines of the open submissions; nothing else blocks a task, and decisions are not asked. Earlier holds (no new baseline trainings before Dec 2) are lifted; rows that stay deferred say which RoI reason keeps them there.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status | 💰 RoI |
|---|---|---|---|---|
| 📝 OpenReview overlap disclosure | 🎯 v5, 📊 v6 | 👤 v5 Sat 3 AM, v6 Dec 1 | 🔴 owner | 🔥 high, avoids a policy reject |
| 🧾 Rebuild, gates, page checkers | 🤝 v4, 🎯 v5 | ⏰ every change; final build by Sat 2 AM | 🟡 all four PASS (10:39 PM build) | 🔥 high, avoids a format reject |
| 🔁 Owner final read, Saturday drafts | 🤝 v4, 🎯 v5 | 👤 Fri Nov 27, 11 PM | 🔴 owner | 🔥 high, author sign-off |
| 🔁 Judge reread, Dec 2 drafts | 📊 v6, 📐 v7 | 👤 Mon Nov 30, 6 PM | 🔴 owner | 🔥 high, last error catch |
| 📦 Anonymous audit code link | 📊 v6 | ⏰ Mon Nov 30, noon | 🔴 open | 🟢 medium, v6 artifact check |
| 📏 Drift band, untargeted switches | 📐 v7 | ⏰ Sat Nov 28, 8 PM | 🔴 open | 🟢 medium, v7 bound, optional |
| 🔁 Claude judge round 7, Saturday drafts | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 9:01 PM | ✅ v4 61 (68%), v5 64 (58%) | 🔥 high, last error catch after new results |
| 🖼️ LoyalAgents Figure 1 qualitative | 🤝 v4 | ✅ Sat Nov 28, 12:02 AM | ✅ owner picked design 4 of 5: who-controls map, then (1) SwiPO vs DPO, GRPO, PPO verbatim on one request, (2) hidden sponsor promotes and denies; no numbers (v8_loyalty_map) | 🔥 high, owner: system design plus qualitative sample |
| 🖼️ MultiRobust Figure 1 qualitative | 🎯 v5 | ✅ Sat Nov 28, 12:08 AM | ✅ owner pick: same map plus switch example replaces the trade-off plot; plot numbers stay in text (v9_contract_map) | 🔥 high, page-1 hook |
| 🛠️ Round-7 fixes into drafts | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 9:10 PM | ✅ second-judge wording, tightening result, Pareto front, overclaims, all four PASS | 🔥 high, score gain before upload |
| 🔁 Claude judge round 6, Saturday drafts | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 4:35 PM | ✅ v4 61, v5 56 | 🔥 high, last error catch |
| 🛠️ Round-6 fixes into drafts | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 4:42 PM | ✅ text fixes in, all four PASS | 🔥 high, score gain before upload |
| 📥 Other-family sponsor into v4 | 🤝 v4 | ✅ Qwen, Phi 7:05 PM; OLMo-2 8:46 PM | ✅ abstract (four families), Fig. 1(c), text | 🔥 high, answers one-model critique |
| 📥 Resampling into drafts | 🎯 v5, 📊 v6 | ✅ Fri Nov 27, 7:15 PM | ✅ v5, v6; v4 and v7 by RoI no | 🔥 high, answers single-sample critique |
| 📥 Qwen judge into drafts | 🎯 v5, 🤝 v4 | ✅ Fri Nov 27, 7:30 PM | ✅ Table 3 column, text, abstracts | 🔥 high, answers same-family judge critique |
| 🔗 Data link: anonymous or named | 🔗 all | ✅ Fri Nov 27, 11:29 AM | ✅ cut in v5, v6 | 🔥 high, stopped a blind leak |
| 🧭 Authority split, loosen vs tighten | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 12:33 PM | ✅ both instruments | 🔥 high, found SwiPO-R yields |
| 🧭 Loyalty-lever Figure 1 | 🤝 v4 | ✅ Fri Nov 27, 9:35 AM | ✅ done | 🔥 high, v4 lead figure |
| 📈 Trade-off plane as Figure 1 | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done | 🔥 high, v5 lead figure |
| 📥 Conflict result into paper | 🤝 v4 | ✅ Fri Nov 27, 9:35 AM | ✅ done | 🔥 high, v4 core result |
| 🏷️ Titles, merged abstracts | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done | 🔥 high, first thing read |
| 📐 Non-identifiability, counterexample | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done | 🔥 high, v7 core theory |
| 🧸 Toy shared-parameter experiment | 📐 v7 | ✅ Fri Nov 27, 10:09 AM | ✅ new Figure 1 | 🔥 high, v7 Figure 1 |
| 🚨 Severity tiers table | 📊 v6 | ✅ Fri Nov 27, 10:03 AM | ✅ Table 5 | 🟢 medium, v6 severity, Table 5 |
| 🧮 Paired loading-by-scorer contrasts | 📊 v6 | ✅ Fri Nov 27, 10:01 AM | ✅ in Table 5 | 🟢 medium, v6 interaction test |
| 📐 Proposition 2, population optimum | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, v7 second result |
| 📥 Harm on XSTest plane | 🎯 v5 | ✅ Fri Nov 27, 9:39 AM | ✅ sentence, not plotted | 🟢 medium, v5 harm objective |
| ⚖️ Dominance, non-dominated points | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, v5 Pareto claim |
| 📥 Override severity sentence | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 9:56 AM | ✅ done | 🟢 medium, v4 severity |
| 📥 No-KL row and sentence | 🔗 all | ✅ Fri Nov 27, 11:09 AM | ✅ sentence, all four | 🟢 medium, answers KL ablation |
| 📏 Capability line, all drafts | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, no capability loss |
| 🗳️ Judge-scored XSTest figure | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, v5 figure on judge |
| 🔤 TrueType fonts, no Type 3 | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, format compliance |
| ♾️ Penalty unboundedness stated | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, v7 math correctness |
| ✍️ Round-4 wording fixes | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done | 🟢 medium, tone, clarity |
| 🗂️ Held-out results by category | 📊 v6 | ✅ Fri Nov 27, 11:41 AM | ✅ one sentence | 🔸 low, v6, one sentence |
| ⏱️ Run-on token cost | 📊 v6 | ✅ Fri Nov 27, 9:50 AM | ✅ in text | 🔸 low, v6, one sentence |
| 🔁 PPO test-retest line | 📊 v6 | ✅ Fri Nov 27, 8 AM | ✅ done | 🔸 low, v6, one line |
| 📉 Objective-driven harm differences | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ in text | 🔸 low, v5, one clause |
| 🔤 Larger Figure 1 text | 📊 v6, 📐 v7 | ✅ Fri Nov 27, 9:58 AM | ✅ about 17% larger | 🔸 low, v6, v7 readability |
| 🧾 arXiv, SC4AI corrections | 🔗 arXiv, SC4AI | 👤 after Dec 2 | ⚪ public posting is the owner's | 🟢 medium, public record |
| 🗡️ Jailbreak attack test | 🔗 all | ⚪ after Dec 2 | ⚪ RoI: no open venue asks for attacks | 🟢 medium, robustness, gMno |
| 💸 Training cost table | 🔗 all | ⚪ after Dec 2 | ⚪ RoI: no room at 4 pages | 🔸 low, cost, KpHA |
| 🎚️ Third intermediate contract | 🎯 v5 | ⚪ closed | ⚪ RoI: MultiRobust closes Sat 3:59 AM | 🔸 low, v5 extra arm |

ELI5: fix words, tables and pictures on the laptop; no big computer needed.

## 🧑‍⚖️ Human-annotation tasks

Anything that cannot finish without a human rater lives here and in no other table. Picks the same minute (owner, Fri Nov 27 ~8:10 AM PST): blind human labels, with Claude only drawing the sample and building the page (an LLM judge is not checked by another LLM); the owner labels 150 sponsor answers tonight.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status | 💰 RoI |
|---|---|---|---|---|
| ✍️ Label 150 sponsor answers | 🤝 v4 | 👤 Fri Nov 27, 10 PM | 🔴 owner, 0 of 150 at 4:20 PM | 🔥 high, only human check, v4 |
| 📥 Sponsor labels into paper | 🤝 v4 | ⏰ 1 h after the labels, by Sat 1 AM | 🔴 waits labels | 🔥 high, v4 kappa sentence |
| 🧑‍⚖️ Blind labels, three raters | 📊 v6 | 👤 Mon Nov 30, noon | 🔴 owner, 2 raters | 🔥 high, v6 scorer validity |
| 📊 Kappa per scorer | 📊 v6 | ⏰ Mon Nov 30, 6 PM | 🔴 open | 🔥 high, v6 scorer validity |
| 🏷️ Build sponsor labeling page | 🤝 v4 | ✅ Fri Nov 27, 9:39 AM | ✅ live, 150 items | 🟢 medium, enables the labels |
| 🧪 Draw scorer-validation sample | 📊 v6 | ✅ Fri Nov 27, 10:13 AM | ✅ 200 stratified | 🟢 medium, enables the labels |
| 📋 Extend Safety Answer Check | 📊 v6 | ✅ Fri Nov 27, 10:13 AM | ✅ live, 300 items | 🟢 medium, enables the labels |

ELI5: jobs where a real person must read the answers and judge them.

## 🔎 Where each row comes from

| 🧩 Row | 🔗 Source |
|---|---|
| 🤝 Conflict-of-interest arm | 🟢 ChatGPT v4 C1 |
| ❓ Disclosure follow-up | 🟠 Claude v4 C3 |
| 🛡️ Override severity | 🟠 Claude v4 C4 |
| 🧭 Loyalty-lever figure | 🟠 Claude v4 C1 |
| 🏷️ Sponsor labels | 🟢 ChatGPT v4 C2 |
| 📈 Plane as Figure 1 | 🟠 Claude v5 C1 |
| 🛡️ Harm on XSTest plane | 🟢🟠 both, v5 C2 |
| ⚖️ Dominance statistic | 🟢🟠 both, v5 C5 |
| 📉 Objective-driven harm | 🟠 Claude v5 C3 |
| 🔁 Resampled answers | 🟢🟠 both · 📜 shuX |
| ⚖️ Qwen second judge | 🟠 Claude v6 C4 |
| 🧑‍⚖️ Scorer validation | 🟢🟠 both · 📜 shuX |
| 🚨 Severity tiers | 🟠 Claude v6 C3 |
| 🧮 Loading-by-scorer contrasts | 🟢 ChatGPT v6 C2 |
| ⏱️ Run-on cost | 🟠 Claude v6 C5 |
| 🗂️ Held-out by category | 🟢 ChatGPT v6 C5 |
| 📦 Audit code link | 🟢 ChatGPT v6 C4 |
| 🧬 Two-contract training | 🟢🟠 both, v7 |
| 📐 Non-identifiability, counterexample | 🟢 ChatGPT v7 C1 |
| 📐 Proposition 2 | 🟠 Claude v7 C2 |
| 🧸 Toy experiment | 🟢 ChatGPT v7 C3 |
| 📏 Drift band | 🟠 Claude v7 C3 |
| 🖼️ Own lead figures | 🟠 Claude Part E |
| 📏 Capability line | 📜 shuX |
| 🧪 No-KL ablation | 📜 shuX |
| 🌱 Seed retrains | 📜 shuX · 🟢 Part E |
| 🦙 Second backbone | 📜 all three |
| 🆚 SimPO, KTO | 📜 gMno |
| 🎛️ Beta, lambda sweep | 📜 shuX |
| 🗡️ Jailbreak test | 📜 gMno |
| 💸 Training cost | 📜 KpHA |
| 🔗 Data link decision | 🟠 page checkers |

ELI5: every job on this list was asked for by a reviewer.
