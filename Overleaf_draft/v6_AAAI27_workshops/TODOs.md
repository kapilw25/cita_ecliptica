# ✅ SwiPO TODOs (v4, v5, v6, v7)

Updated Fri Nov 27 2026, 4:50 PM PST (box checked 4:20 PM PST). One TODO file for all SwiPO workshop drafts (owner order Fri Nov 27 ~8:05 AM PST), next to [venues.md](venues.md). It replaces `v2_LoyalAgents/TODOs.md`, archived at [legacy/v2_LoyalAgents/TODOs.md](legacy/v2_LoyalAgents/TODOs.md). Sources: the ARR reviews ([KpHA](../ARR_feedback/Reviewer_KpHA.md), [gMno](../ARR_feedback/Reviewer_gMno.md), [shuX](../ARR_feedback/Reviewer_shuX.md)) and the ChatGPT and Claude reviews in `feedback/output/<draft>/by_chatgpt.md` and `by_claude.md`. No early freeze: every draft iterates until its deadline (owner, Fri Nov 27). Owner away Fri Nov 27 ~8:40 AM to ~8:40 PM PST; picks before leaving: Claude integrates each new result honestly (abstracts included, titles fixed, cuts only from the judges' cut lists), runs a fresh Claude judge round on the Saturday drafts around 6 PM, keeps the anonymous data link, and sends a phone ping only on key events.

**Legend:** 🔴 open · ⏳ queued · 🟡 in progress · ✅ done · 👤 a person does it · ⚪ deferred · ⛔ blocked · 🟢 ChatGPT · 🟠 Claude · 📜 ARR

**💰 RoI** (what the task buys for acceptance, per hour spent): 🔥 high, it moves a headline result, a lead figure or a reject risk · 🟢 medium, it answers one reviewer ask in a sentence or a table · 🔸 low, polish or operations. Each table lists open rows first, ranked by acceptance gain, then done rows ranked by the RoI they delivered, then deferred rows (owner picks Fri Nov 27 ~4:45 PM PST).

## 🎯 Where each draft stands

| 📄 Draft | ⏰ Due (PST) | 🟢 ChatGPT | 🟠 Claude | 🟣 Claude r5 | 🟣 Claude r6 |
|---|---|---|---|---|---|
| 🤝 [v4 LoyalAgents](v4_LoyalAgents_4page_astrained/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 74, 74% | 🔹 62, 55% | 🔹 63, 70% | 🟡 running |
| 🎯 [v5 MultiRobust](v5_MultiRobust_4page/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 76, 78% | 🔹 59, 45% | 🔹 57, 55% | 🔹 56, 55% |
| 📊 [v6 Bench2Evidence](v6_Bench2Evidence_4page/0_main.pdf) | 🟡 Wed Dec 2, 3:59 AM | 🔹 84, 86% | 🔹 66, 75% | ⚪ not run | ⚪ not run |
| 📐 [v7 MATH4AI](v7_MATH4AI_4page/0_main.pdf) | 🟡 Wed Dec 2, 4:00 AM | 🔹 64, 52% | 🔹 54, 35% | ⚪ not run | ⚪ not run |

ChatGPT and Claude scores are on the drafts before the round-4 fixes (commit 7e71010). Round 5 (fresh Claude Code judges, Fri Nov 27 ~11:15 AM PST, Saturday drafts only, at 6ff6116; reviews in feedback/output/<draft>/by_claude_r5.md) came before its own fixes, which are in by 622c866.

ELI5: four homework papers, two due tomorrow; two teachers graded each.

## 🖥️ GPU tasks

One rented RTX PRO 6000 (96 GB), driven over SSH, at most 3 GPU jobs at once. Every Saturday run is done. The three resampled answers run now (4 of 9 runs done, 2 running), then the Qwen judge, then the Dec 2 trainings. "~" marks an estimate from measured speed: a contract run takes about 3 h, an XSTest run about 1 h, a held-out run about 3 h 20 min.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status | 💰 RoI |
|---|---|---|---|---|
| 🔁 Three resampled answers | 🎯 v5, 🤝 v4, 📊 v6 | ⏰ ~Fri Nov 27, 9 PM (XSTest ~5:35 PM) | 🟡 running, 4 of 9 done | 🔥 high, answers single-sample critique |
| 🌱 3-seed DPO, SwiPO retrains | 📊 v6, 📐 v7 | ⏰ ~Mon Nov 30 | ⏳ queued, next after SFT-chain run | 🔥 high, Dec 2 variance, shuX |
| ⚖️ Qwen second judge | 📊 v6, 🎯 v5 | ⏰ ~Fri Nov 27, 9 PM | ⏳ queued, starts ~7 PM | 🟢 medium, judge from another family |
| 🧬 Two-contract SwiPO, SFT chain | 📐 v7 | ⏰ ~Sat Nov 28, 6 AM | ⏳ queued, starts ~9 PM | 🟢 medium, v7 test, second chain |
| 🛑 Stop box, rotate token | 🔗 all | 👤 after Dec 1 | 🔴 owner | 🔸 low, ops: spend, secret |
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

Owner pick Fri Nov 27 ~8:25 AM PST: no new baseline trainings before Dec 2. The no-KL run answers the KL ablation, the queued seed retrains answer variance, and SimPO, KTO and a lambda sweep go to the arXiv revision.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status | 💰 RoI |
|---|---|---|---|---|
| 📤 Submit LoyalAgents | 🤝 v4 | 👤 first upload Fri 11 PM, final Sat 3:30 AM | 🔴 owner | 🔥 high, no upload, no review |
| 📤 Submit MultiRobust | 🎯 v5 | 👤 first upload Fri 11 PM, final Sat 3:30 AM | 🔴 owner | 🔥 high, no upload, no review |
| 📝 OpenReview overlap disclosure | 🎯 v5, 📊 v6 | 👤 v5 Sat 3 AM, v6 Dec 1 | 🔴 owner | 🔥 high, avoids a policy reject |
| 🧾 Rebuild, gates, page checkers | 🤝 v4, 🎯 v5 | ⏰ every change; last Sat 2 AM | 🟡 all four PASS at e8fb843 | 🔥 high, avoids a format reject |
| 🔁 Claude judge round 6, Saturday drafts | 🤝 v4, 🎯 v5 | ⏰ Fri Nov 27, ~6 PM | 🟡 v5 done 56, v4 running | 🔥 high, last error catch |
| 🛠️ Round-6 fixes into drafts | 🤝 v4, 🎯 v5 | ⏰ Fri Nov 27, ~8 PM | 🔴 waits round 6 | 🔥 high, score gain before upload |
| 🔁 Owner final read, Saturday drafts | 🤝 v4, 🎯 v5 | 👤 Fri Nov 27, 11 PM | 🔴 owner | 🔥 high, author sign-off |
| 📥 Resampling into drafts | 🎯 v5, 🤝 v4 | ⏰ Fri Nov 27, ~10 PM | 🔴 waits run | 🔥 high, answers single-sample critique |
| 📤 Submit Bench2Evidence | 📊 v6 | 👤 Tue Dec 1, 11 PM | 🔴 owner | 🔥 high, no upload, no review |
| 📤 Submit MATH4AI | 📐 v7 | 👤 Tue Dec 1, 11 PM | 🔴 owner | 🔥 high, no upload, no review |
| 🔁 Judge reread, Dec 2 drafts | 📊 v6, 📐 v7 | 👤 Mon Nov 30, 6 PM | 🔴 owner | 🔥 high, last error catch |
| 📥 Qwen judge into drafts | 🎯 v5, 🤝 v4 | ⏰ Fri Nov 27, ~10 PM | 🔴 waits run, if it fits | 🟢 medium, second judge, if it fits |
| 📦 Anonymous audit code link | 📊 v6 | ⏰ Mon Nov 30, noon | 🔴 open | 🟢 medium, v6 artifact check |
| 📏 Drift band, untargeted switches | 📐 v7 | ⏰ Sat Nov 28, 8 PM | 🔴 open | 🟢 medium, v7 bound, optional |
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
| 🦙 Second backbone model | 🔗 all | ⚪ after Dec 2 | ⚪ deferred, disclosed | 🔥 high, main-track ask, after Dec 2 |
| 🧾 arXiv, SC4AI corrections | 🔗 arXiv, SC4AI | 👤 owner's call | ⚪ owner | 🟢 medium, public record |
| 🆚 SimPO, KTO baselines | 🔗 arXiv revision | ⚪ after Dec 2 | ⚪ owner: not now | 🟢 medium, baseline ask, gMno |
| 🎛️ Beta, lambda sweep | 🔗 arXiv revision | ⚪ after Dec 2 | ⚪ owner: not now | 🟢 medium, sensitivity, shuX |
| 🗡️ Jailbreak attack test | 🔗 all | ⚪ after Dec 2 | ⚪ deferred | 🟢 medium, robustness, gMno |
| 💸 Training cost table | 🔗 all | ⚪ after Dec 2 | ⚪ deferred | 🔸 low, cost, KpHA |
| 🎚️ Third intermediate contract | 🎯 v5 | ⚪ not picked | ⚪ deferred | 🔸 low, v5 extra arm |
| 🧲 Gradient-coupling measurement | 📐 v7 | ⚪ stretch | ⚪ deferred | 🔸 low, v7 stretch |

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
