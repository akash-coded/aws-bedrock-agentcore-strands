---
title: Shadow Mode and Canary Releases for AI Agents, Step by Step
short: Shadow mode and cut-over
wiki: Shadow-Mode-and-Canary-Releases-for-AI-Agents
description: How to launch an AI agent safely: run it in shadow beside the people doing the job, cut over at 5% per action, widen only on evidence, and rehearse the way back.
dek: The golden set proves the agent is right about the cases you chose. A shadow run proves it agrees with today's traffic — including the rule nobody wrote down.
level: Intermediate
keywords: shadow mode AI, canary release AI agent, how to launch an AI agent, AI rollout strategy, feature flags for AI, AI deployment best practices, gradual rollout LLM, dark launch
updated: 2026-09-23
---

> [!TIP]
> **The launch in one sentence.** Launch an AI agent in four states, one action at a time — **shadow**,
> where it decides on live traffic and acts on nothing; a **5% canary**; **wider** only as live evidence
> arrives; then **all of it** — with money actions gated at every stage, agreement reported per slice
> over a window fixed in advance, and every rollback switch timed in a rehearsal before cut-over.

{{model:g_funnel}}

**In this lesson** you'll learn:

- what a shadow run proves that a golden set cannot, and how to run one honestly;
- how to cut over per action behind flags, and widen on evidence rather than dates;
- why the rollback must be rehearsed, and what to measure when you do.

## Sound familiar?

- The launch plan says "go live on the 14th", with nothing to compare against on the 15th.
- The shadow run "passed" at 96%, and the refunds inside it agreed barely two times in three.
- Nobody has ever actually switched the agent off, so nobody knows how long it takes.

Each is a launch that bets instead of measuring. The four states replace the bet with evidence.

## What does a shadow run prove?

The golden set proves the agent is right about cases **you curated**. A **shadow run** proves
something different and harder: that it agrees with the people doing the job on **today's traffic** —
the storm day, the partner outage, the fare class that only appears in winter — by deciding every case
and acting on none.

It finds what nobody thought to write down. At SkyWays the harness had same-day rebooking at 88%, and
the shadow run agreed with the desk on 96% of same-day cases. On fourteen it did not, and all fourteen
were the same: the agent proposed a partner airline the evening shift never uses after 18:00, because
that partner's transfer desk closes. The rule was in nobody's spec and nobody's golden set; it lived in
six people's heads. It cost nothing to discover, because the write side was off.

## Launch, step by step

### Step 1 · Put every action behind its own flag

One flag per action — rebook, refund, message — each with four states: shadow, 5%, wider, all. The
prompt and the model version are deployable artefacts like code, and every trace records which flag
state and prompt version produced it.

### Step 2 · Run the shadow over a window fixed in advance

Fix the window before you start, not when the numbers look good. Report **agreement per slice**, read
every disagreement, and add a test that fails the build if a write is reachable from the shadow path.

### Step 3 · Keep money out of the headline

Report money actions separately and keep them gated whatever the shadow shows. SkyWays cleared its
threshold — 96% agreement over fourteen days against a 95% default — and inside it the agent disagreed
with the desk on **four of eleven** refunds. Eleven cases prove nothing either way, so the honest word
was *unproven*; and refunds should never have been inside the automatic figure at all.

### Step 4 · Cut over at 5%, per action, and widen on evidence

Start the lowest-risk action at 5% and leave the rest in shadow. Each widening names the evidence that
earned it — never a date. The length of each step is arithmetic: **days = cases needed ÷ (share ×
cases per day)**, so 500 cases at 5% of 240 a day is 42 days. The safe share is the slow one, which is
why a cut-over widens rather than holding.

### Step 5 · Widen across conditions, not just volume

At 5% for six weeks you will see a normal Tuesday many times and a storm day perhaps once. Widen
deliberately into the conditions you have not seen — nights, peaks, partner outages — rather than only
into more of the same traffic.

### Step 6 · Rehearse the way back, with a stopwatch

Before cut-over, have someone other than the author throw every switch and write the times down.
SkyWays measured four: the **kill switch** in 40 seconds, **flag to shadow** in 2 minutes, a **prompt
rollback** in 3, and a **model rollback** in 11, because it redeploys the runtime. A rollback nobody has
rehearsed is a belief, not a capability.

## Where you'll use it

- **At the end of P2**, after the behaviour gate and before any live traffic.
- **On every new action** added to a live agent: it starts in shadow, whatever the others are doing.
- **After an incident**: the affected action drops back to shadow until the evidence re-earns it.

## Why it matters

The first time an agent meets real traffic should not also be the first time it acts. Shadow turns the
rules that live in people's heads into findings that cost nothing; per-action flags keep a problem in
one action from becoming a problem in all of them; and a timed rollback turns "we can switch it off" into
a number the sponsor can rely on.

## Try it

An agent handles three actions: answering questions (read-only), rebooking (hard to reverse) and
issuing refunds (money). Shadow agreement over fourteen days: questions 97% on 2,000 cases, rebooking
94% on 400, refunds 90% on 30. The default threshold is 95%. **What goes live at 5%?**

<details><summary>Show the answer</summary>

**Only questions.** They clear the threshold on a large sample and cannot do harm. Rebooking is below
threshold: read its 24 disagreements, fix what they show and extend its shadow. Refunds stay gated
regardless — 30 cases prove nothing either way, and money actions are never widened on an automatic
agreement figure. The launch goes ahead; it just goes ahead one action at a time.

</details>

## Key takeaways

1. **Shadow proves agreement with today's traffic** — and surfaces the rules nobody wrote down.
2. **Four states per action**, money gated throughout, each widening earned by named evidence.
3. **Rehearse the rollback with a stopwatch** — kill switch, flag, prompt, model — before cut-over.

## FAQ

### What is shadow mode for AI?

A period in which an AI agent receives live traffic and makes every decision but takes no action,
while its decisions are logged and compared with what the people doing the job actually did. It is a
test on real conditions with no risk, because the write side is off.

### How long should an AI shadow run last?

Long enough for the slices that matter to accumulate the cases their verdict needs, and fixed before
it starts. Fourteen days is this playbook's default; the real answer is the cases needed divided by the
cases each slice sees per day.

### What is a canary release for an AI agent?

Sending a small share of live traffic — typically 5% — to the agent for one action, while the rest
continues as before, and widening only as evidence accumulates. For AI it should be done per action, so
a low-risk action can go live while a money action stays gated.

### How do you roll back an AI agent?

With switches rehearsed before launch: a kill switch, moving an action's flag back to shadow, rolling
back the prompt, and rolling back the model version. Time each in a rehearsal; the model rollback is
usually the slowest.

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Shadow deployment and canary release | **Borrowed** | General practice; see Beyer, B. et al. (2016). *Site Reliability Engineering*. O'Reilly |
| Four states per action, money gated, widening on named evidence | **Original** — this playbook | [QA lead](site:qa/#shadow) · [DevOps](site:devops/) |
| Days of live evidence | **Original** — this playbook | [Formulas](wiki:Formulas-and-Calculators#days-of-live-evidence--working-method) |
| 95% agreement over 14 days, and the 5% first cut-over | **Original** — working defaults to tune | [Sources and Confidence](wiki:Sources-and-Confidence#the-working-methods-and-how-to-tune-each) |
| The SkyWays figures | **Illustrative** — a fictional airline | [Try the cut-over calculator](sim:#/toolkit/cutover) |
