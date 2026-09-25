---
title: P3 Run & Learn: How to Run an AI Agent in Production Safely
short: P3 · Run & Learn
wiki: P3-Run-and-Learn-Run-an-AI-Agent-in-Production
description: P3 Run & Learn covers cut-over, rollback, drift and cost for AI agents in production, and the two-number report that decides whether the programme survives.
dek: Widen on evidence, rehearse the way back, watch the output mix, and report the saving beside the spend, every cycle, before anyone asks.
level: Intermediate
keywords: AI agent in production, LLM monitoring, AI drift detection, canary release AI, AI rollback, AI cost monitoring, AI ROI reporting, LLMOps, P3 run and learn
updated: 2026-09-24
---

> [!TIP]
> **P3 in one sentence.** P3 Run & Learn widens the agent's share of live traffic only as evidence
> arrives, rehearses the rollback before it is needed, watches the output mix for drift, reports what
> the feature saved **beside** what it cost on one line, and turns every incident, drift alert and
> surprising bill into the brief for the next P0.

{{figure:shadow_widen}}

**In this lesson** you'll learn:

- how to cut over from shadow to full traffic without betting on a date;
- how to catch drift, the defect with no error message, before a customer does;
- how to report value and cost so the programme survives its first bill.

## Sound familiar?

- Launch day was set in a meeting, and nobody divided the cases you need by the cases you get a day.
- Three months after launch a customer noticed the assistant now offers credits where it used to offer refunds.
- Finance found the token bill before the product manager reported the saving.

P3 is where each of those is either caught by a mechanism or discovered by someone else.

## What is P3 Run & Learn?

P3 is the fourth phase of the [agentic PDLC](lesson:what-is-the-agentic-pdlc), and the one that
never finishes. The **sponsor** is accountable for it. DevOps runs the flags, traces and recovery;
QA watches drift and runs the injection suite; the product manager reports the two numbers; the
architect turns incidents and bills into design changes.

A P3 cycle ends when **both numbers are reported and the brief for the next P0 exists**.

## P3, step by step

### Step 1 · Widen on evidence, not on a date

Four states, taken one at a time: **shadow**, where the agent decides on real traffic and acts on
nothing; a **5% canary**; **wider**, on evidence; then **all of it**. Each step is a condition, never
a date: and the arithmetic decides how long it takes. At 240 cases a day, 5% is twelve a day, so
five hundred cases takes 42 days. The safe share is the slow one, which is exactly why a cut-over
widens rather than holding.

Money actions stay gated at every stage, whatever the shadow shows. When the SkyWays sponsor had six
weeks instead of ten, the shadow window was cut from fourteen days to seven, on the simple slice
only, with every disagreement read.

### Step 2 · Rehearse the way back, and cap the runaway

Rollback is a capability, and a capability nobody has used is a belief. Before cut-over, throw every
switch with a stopwatch running and write the times down. SkyWays measured four: the kill switch in
**40 seconds**, flag to shadow in **2 minutes**, a prompt rollback in **3**, and a model rollback in
**11**, because it redeploys the runtime. Then cap the runaway: a loop limit on every agent, and a
cost limit per case that ends in a person's queue rather than in another retry.

### Step 3 · Watch for drift

**Drift** is behaviour changing with no deploy, no error and no alert. Your existing monitoring
answers whether the system is up and fast; it was never looking for this. Watch the **output mix**, the share of each kind of decision, because accuracy needs labels and arrives late, while the mix is
visible the same day.

Watch it against **two thresholds**, not one. The SkyWays refund-to-credit mix slid from 61/39 in
week one to 48/52 in week eight, thirteen points, and never tripped its 5% weekly alert, because it
moved 1.9 points a week. A second threshold, on the level against a frozen baseline, fires within
weeks where the weekly one never fires at all. Wire a breach to **re-open the release gate**
automatically.

### Step 4 · Report two numbers on one line

Report what the feature **saved** and what it **cost**, together, every cycle, before anyone asks,
with the two rows that stop either number being gamed: the review hours added, and the re-runs.

{{figure:two_numbers}}

A first cycle that saves time and costs more is survivable, if the sponsor hears it from you. On day
ninety SkyWays reported 40 to 45 percent fewer person-days and a token bill of $4,200 on one line,
with the rising review hours beside them and the reason they would fall. The programme continued:
not because the numbers were flattering, but because both of them came from the team.

### Step 5 · Turn what you learned into the next P0

A bill that leaves its estimate is a **design** question, not a finance one. SkyWays' day-75 bill was
4.4 times its estimate on flat traffic, and a per-call log showed four ordinary habits multiplying:

{{figure:bill_factors}}

An incident is the same: its postmortem asks which **enforced control** was missing, never who was
careless, and it ends as a typed parameter, a test and new golden cases, plus a brief for the next
P0. [The eight loops](lesson:the-eight-loops) are how that learning finds its way back.

## Where you'll use it

- **From the first day of live traffic, forever.** P3 does not end; each cycle ends.
- **After every prompt, model or configuration change**, which re-runs the harness and, if the mix
  moves, re-opens the release gate.
- **In every sponsor update**, which carries the two numbers on one line.

## Why it matters

Gartner's forecast that over 40% of agentic AI projects will be cancelled by 2027 names escalating
costs as a cause. Costs escalate quietly and are found by finance; drift degrades quietly and is found
by customers. P3 exists so that both are found by you, first, with a design change already drafted.

## Try it

An agent handles 400 cases a day. The team wants 600 cases of live evidence before widening beyond a
10% canary. **How many days will the canary take, and what would halve it?**

<details><summary>Show the answer</summary>

**Fifteen days.** 10% of 400 is 40 cases a day, and 600 ÷ 40 = 15. Doubling the share to 20% halves
it to seven and a half days, at the cost of doubling the exposure while the evidence is still
thin. Lowering the requirement would also shorten it, but only honestly if the bar and its lower
bound allow fewer cases. Effort cannot shorten it: evidence arrives at the speed of traffic.

</details>

## Key takeaways

1. **Widen on evidence**: shadow, 5%, wider, all, each step a condition, and its length set by arithmetic.
2. **Watch the output mix against two thresholds**, and let a breach re-open the release gate on its own.
3. **Report two numbers on one line**, the saving beside the spend, and turn every bill and incident into the next P0.

## FAQ

### How do you monitor an AI agent in production?

Add three signals to your usual uptime and latency monitoring: the cost of each case, a trace of what
the agent did and why, and the mix of its outputs over time. Alert on the mix against both a weekly
change and a fixed baseline, and review a sample of cases against human judgement on a schedule.

### What is AI model drift?

Drift is a change in an AI system's behaviour without any change to its code, because the world, the
inputs, the upstream model or the data it retrieves has moved. It raises no error, which is why it is
watched through the distribution of outputs rather than through failures.

### How do you roll back an AI agent?

Keep four switches and time each one in a rehearsal before launch: a kill switch, moving the action's
flag back to shadow, rolling back the prompt, and rolling back the model version. A model rollback is
usually the slowest, because it redeploys the runtime.

### How do you measure the ROI of an AI agent after launch?

Report two numbers together: the saving, measured against the baseline from P0, and the full cost,
including tokens, review time and re-runs. Reporting only the saving is how a programme gets
cancelled when finance finds the other number.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Stay through the first widening: rehearse the rollback with the customer's on-call, time every switch, and leave a drift chart they can read without you. | Ask a model to write the customer's runbook from your deployment configuration and the rollback rehearsal log. |
| **A product manager or FDPM** | Report two numbers on one line every cycle, and widen by arithmetic, days of evidence per share, never by date. | Have a model draft the cycle report from the tracker export and the token log, with review hours and re-runs beside the saving. |
| **A GenAI or agentic AI engineer** | Log the answering model, prompt version and flag state on every response, and chart the output mix weekly against two thresholds. | Ask a coding agent to add the weekly drift job and wire a breach to flip the release flag. |

**Across the enterprise.** Aggregate every product's two numbers and drift chart into one portfolio view.
The incidents and bills P3 produces are the pipeline of next quarter's P0 briefs.

**The ten-minute workflow.** The cycle report, drafted from raw data:

```text
Here is this cycle's data: <tracker export, token log, review log>. Write the two-number report:
person-days per story against the baseline of <n>, token spend per story, review hours added and
re-runs per story, each with its change. Add one paragraph on the trend and the single biggest risk
to the saving. Do not smooth away a rising re-run count.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Shadow, 5%, widen on evidence; the two drift thresholds; the two-number report | **Original**: this playbook | [QA lead](site:qa/#watch) · [Gates and Governance](wiki:Gates-and-Governance#paired-indicators-and-the-two-number-report) |
| Report every measure beside its side effect | **Borrowed** | Grove, A. (1983). *High Output Management*. Random House |
| Why a single number gets pushed | **Borrowed** | Goodhart, C. (1975). Goodhart's law |
| Blameless postmortems | **Borrowed** | Beyer, B. et al. (2016). *Site Reliability Engineering*. O'Reilly |
| Canary release and shadow deployment | **Borrowed** | General practice |
| Escalating costs as a cause of cancellation | **Borrowed** | Gartner (2025). [Press release, 25 June](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) |
| The SkyWays figures | **Illustrative**: a fictional airline | [Try the cut-over calculator](sim:#/toolkit/cutover) |
