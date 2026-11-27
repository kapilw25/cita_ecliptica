# ✅ SwiPO TODOs (v4, v5, v6, v7)

Updated Fri Nov 27 2026, 10:13 AM PST. One TODO file for all SwiPO workshop drafts (owner order Fri Nov 27 ~8:05 AM PST), next to [venues.md](venues.md). It replaces `v2_LoyalAgents/TODOs.md`, archived at [legacy/v2_LoyalAgents/TODOs.md](legacy/v2_LoyalAgents/TODOs.md). Sources: the ARR reviews ([KpHA](../ARR_feedback/Reviewer_KpHA.md), [gMno](../ARR_feedback/Reviewer_gMno.md), [shuX](../ARR_feedback/Reviewer_shuX.md)) and the ChatGPT and Claude reviews in `feedback/output/<draft>/by_chatgpt.md` and `by_claude.md`. No early freeze: every draft iterates until its deadline (owner, Fri Nov 27). Owner away Fri Nov 27 ~8:40 AM to ~8:40 PM PST; picks before leaving: Claude integrates each new result honestly (abstracts included, titles fixed, cuts only from the judges' cut lists), runs a fresh Claude judge round on the Saturday drafts around 6 PM, keeps the anonymous data link, and sends a phone ping only on key events.

**Legend:** 🔴 open · ⏳ queued · 🟡 in progress · ✅ done · 👤 a person does it · ⚪ deferred · ⛔ blocked · 🟢 ChatGPT · 🟠 Claude · 📜 ARR

## 🎯 Where each draft stands

| 📄 Draft | ⏰ Due (PST) | 🟢 ChatGPT | 🟠 Claude |
|---|---|---|---|
| 🤝 [v4 LoyalAgents](v4_LoyalAgents_4page_astrained/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 74, 74% | 🔹 62, 55% |
| 🎯 [v5 MultiRobust](v5_MultiRobust_4page/0_main.pdf) | 🔴 Sat Nov 28, 3:59 AM | 🔹 76, 78% | 🔹 59, 45% |
| 📊 [v6 Bench2Evidence](v6_Bench2Evidence_4page/0_main.pdf) | 🟡 Wed Dec 2, 3:59 AM | 🔹 84, 86% | 🔹 66, 75% |
| 📐 [v7 MATH4AI](v7_MATH4AI_4page/0_main.pdf) | 🟡 Wed Dec 2, 4:00 AM | 🔹 64, 52% | 🔹 54, 35% |

Scores are on the drafts before the round-4 fixes (commit 7e71010); those fixes are in, so the next judge round re-scores.

ELI5: four homework papers, two due tomorrow; two teachers graded each.

## 🖥️ GPU tasks

One rented RTX PRO 6000 (96 GB), driven over SSH. The four Saturday runs go one after another in a side session, beside three running g3 jobs; Dec 2 runs wait in the queue behind them. "~" marks an estimate from measured speed.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status |
|---|---|---|---|
| 🤝 Conflict-of-interest arm | 🤝 v4 | ✅ Fri Nov 27, 9:26 AM | ✅ done |
| 🛡️ Llama Guard on XSTest | 🎯 v5 | ✅ Fri Nov 27, 9:33 AM | ✅ done |
| 🛡️ Llama Guard on overrides | 🤝 v4 | ✅ Fri Nov 27, 9:53 AM | ✅ done |
| ❓ Disclosure follow-up question | 🤝 v4 | ⏰ ~Fri Nov 27, 11:30 AM | 🟡 running |
| 🧪 Evaluate no-KL ablation | 🔗 all | ⏰ ~Fri Nov 27, 1 PM | ⏳ queued |
| 🔁 Three resampled answers | 📊 v6, 🎯 v5 | ⏰ ~Sat Nov 28 | ⏳ queued |
| ⚖️ Qwen second judge | 📊 v6 | ⏰ ~Sat Nov 28 | ⏳ queued |
| 🧬 Two-contract SwiPO, SFT chain | 📐 v7 | ⏰ ~Sun Nov 29 | ⏳ queued |
| 🌱 3-seed DPO, SwiPO retrains | 📊 v6, 📐 v7 | ⏰ ~Mon Nov 30 | ⏳ queued |
| 🧬 Two-contract SwiPO, R chain | 🔗 all | ✅ Fri Nov 27, 6 AM | ✅ done |
| 🗳️ XSTest judge labels | 🎯 v5 | ✅ Fri Nov 27, 7 AM | ✅ done |
| 📏 Capability MMLU, GSM8K | 🔗 all | ✅ Fri Nov 27, 2 AM | ✅ done, unused |
| 🛑 Stop box, rotate token | 🔗 all | 👤 after Dec 1 | 🔴 owner |

ELI5: the big computer re-asks the models new questions and grades them.

## 💻 Non-GPU tasks

Owner pick Fri Nov 27 ~8:25 AM PST: no new baseline trainings before Dec 2. The no-KL run answers the KL ablation, the queued seed retrains answer variance, and SimPO, KTO and a lambda sweep go to the arXiv revision.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status |
|---|---|---|---|
| 📈 Trade-off plane as Figure 1 | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🧭 Loyalty-lever Figure 1 | 🤝 v4 | ✅ Fri Nov 27, 9:35 AM | ✅ done |
| 📥 Conflict result into paper | 🤝 v4 | ✅ Fri Nov 27, 9:35 AM | ✅ done |
| 📏 Capability line, all drafts | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done |
| 📥 Harm on XSTest plane | 🎯 v5 | ✅ Fri Nov 27, 9:39 AM | ✅ sentence, not plotted |
| 📥 Override severity sentence | 🤝 v4, 🎯 v5 | ✅ Fri Nov 27, 9:56 AM | ✅ done |
| 📥 No-KL row and sentence | 🔗 all | ⏰ Fri Nov 27, 3 PM | 🔴 waits run |
| ⚖️ Dominance, non-dominated points | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 📉 Objective-driven harm differences | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ in text |
| 🔤 Larger Figure 1 text | 📊 v6, 📐 v7 | ✅ Fri Nov 27, 9:58 AM | ✅ about 17% larger |
| 🧾 Rebuild, gates, page checkers | 🤝 v4, 🎯 v5 | ⏰ Fri Nov 27, 9 PM | 🔴 open |
| 🔁 Judge reread, Saturday drafts | 🤝 v4, 🎯 v5 | 👤 Fri Nov 27, 11 PM | 🔴 owner |
| 🔗 Data link: anonymous or named | 🤝 v4, 📐 v7 | ✅ Fri Nov 27, 8:35 AM | ✅ owner: keep anonymous |
| 📝 OpenReview overlap disclosure | 🎯 v5, 📊 v6 | 👤 at submission | 🔴 owner |
| 📤 Submit LoyalAgents | 🤝 v4 | 👤 Sat Nov 28, 3 AM | 🔴 owner |
| 📤 Submit MultiRobust | 🎯 v5 | 👤 Sat Nov 28, 3 AM | 🔴 owner |
| 🧮 Paired loading-by-scorer contrasts | 📊 v6 | ✅ Fri Nov 27, 10:01 AM | ✅ in Table 5 |
| 🚨 Severity tiers table | 📊 v6 | ✅ Fri Nov 27, 10:03 AM | ✅ Table 5 |
| ⏱️ Run-on token cost | 📊 v6 | ✅ Fri Nov 27, 9:50 AM | ✅ in text |
| 📏 Drift band, untargeted switches | 📐 v7 | ⏰ Sat Nov 28, 8 PM | 🔴 open |
| 📐 Non-identifiability, counterexample | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 📐 Proposition 2, population optimum | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🧸 Toy shared-parameter experiment | 📐 v7 | ✅ Fri Nov 27, 10:09 AM | ✅ new Figure 1 |
| 🗂️ Held-out results by category | 📊 v6 | ⏰ Sun Nov 29, 7 PM | 🔴 open |
| 📦 Anonymous audit code link | 📊 v6 | ⏰ Mon Nov 30, noon | 🔴 open |
| 🔁 Judge reread, Dec 2 drafts | 📊 v6, 📐 v7 | 👤 Mon Nov 30, 6 PM | 🔴 owner |
| 📤 Submit Bench2Evidence | 📊 v6 | 👤 Tue Dec 1, 11 PM | 🔴 owner |
| 📤 Submit MATH4AI | 📐 v7 | 👤 Tue Dec 1, 11 PM | 🔴 owner |
| 🧾 arXiv, SC4AI corrections | 🔗 arXiv, SC4AI | 👤 owner's call | ⚪ owner |
| ✍️ Round-4 wording fixes | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🏷️ Titles, merged abstracts | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🗳️ Judge-scored XSTest figure | 🎯 v5 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🔁 PPO test-retest line | 📊 v6 | ✅ Fri Nov 27, 8 AM | ✅ done |
| ♾️ Penalty unboundedness stated | 📐 v7 | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🔤 TrueType fonts, no Type 3 | 🔗 all | ✅ Fri Nov 27, 8 AM | ✅ done |
| 🦙 Second backbone model | 🔗 all | ⚪ after Dec 2 | ⚪ deferred, disclosed |
| 🆚 SimPO, KTO baselines | 🔗 arXiv revision | ⚪ after Dec 2 | ⚪ owner: not now |
| 🎛️ Beta, lambda sweep | 🔗 arXiv revision | ⚪ after Dec 2 | ⚪ owner: not now |
| 🗡️ Jailbreak attack test | 🔗 all | ⚪ after Dec 2 | ⚪ deferred |
| 💸 Training cost table | 🔗 all | ⚪ after Dec 2 | ⚪ deferred |
| 🎚️ Third intermediate contract | 🎯 v5 | ⚪ not picked | ⚪ deferred |
| 🧲 Gradient-coupling measurement | 📐 v7 | ⚪ stretch | ⚪ deferred |

ELI5: fix words, tables and pictures on the laptop; no big computer needed.

## 🧑‍⚖️ Human-annotation tasks

Anything that cannot finish without a human rater lives here and in no other table. Picks the same minute (owner, Fri Nov 27 ~8:10 AM PST): blind human labels, with Claude only drawing the sample and building the page (an LLM judge is not checked by another LLM); the owner labels 150 sponsor answers tonight.

| 🧩 Task | 📄 Draft | ⏰ ETA (PST) | 🚦 Status |
|---|---|---|---|
| 🏷️ Build sponsor labeling page | 🤝 v4 | ✅ Fri Nov 27, 9:39 AM | ✅ live, 150 items |
| ✍️ Label 150 sponsor answers | 🤝 v4 | 👤 Fri Nov 27, 10 PM | 🔴 owner |
| 📥 Sponsor labels into paper | 🤝 v4 | ⏰ Sat Nov 28, 1 AM | 🔴 open |
| 🧪 Draw scorer-validation sample | 📊 v6 | ✅ Fri Nov 27, 10:13 AM | ✅ 200 stratified |
| 📋 Extend Safety Answer Check | 📊 v6 | ✅ Fri Nov 27, 10:13 AM | ✅ live, 300 items |
| 🧑‍⚖️ Blind labels, three raters | 📊 v6 | 👤 Mon Nov 30, noon | 🔴 owner, 2 raters |
| 📊 Kappa per scorer | 📊 v6 | ⏰ Mon Nov 30, 6 PM | 🔴 open |

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
