---
title: AI Drift: How to Catch the Defect With No Error Message
short: Catch AI drift
wiki: AI-Drift-How-to-Catch-the-Defect-With-No-Error-Message
description: AI drift is behaviour changing with no deploy and no error. Why accuracy alerts arrive late, what to watch instead, and the two thresholds that catch it.
dek: No code changed, nothing threw, no alert fired — and three months later a customer noticed the assistant offers credits where it used to offer refunds.
level: Intermediate
keywords: AI model drift, LLM drift detection, AI monitoring in production, model performance degradation, output distribution monitoring, concept drift, AI observability, silent model failure
updated: 2026-09-24
---

> [!TIP]
> **Drift in one sentence.** Drift is an AI system changing its behaviour with no deploy, no error and
> no alert — because the world, its inputs, its data or the model behind it moved — and you catch it by
> watching the **mix of its outputs** against **two thresholds**, the week-on-week change and the level
> against a frozen baseline, with a breach wired to re-open the release gate on its own.

{{model:g_drift}}

**In this lesson** you'll learn:

- what causes drift in an AI agent, and why ordinary monitoring never sees it;
- why the output mix beats accuracy as an early signal;
- the two thresholds, and why one is never enough.

## Sound familiar?

- The dashboards are green, the error rate is flat, and the complaints are rising.
- Quality dropped this week and nobody deployed anything.
- The drift alert is set at 5% a week, and it has never fired.

Your existing monitoring answers whether the system is up and fast. It was never looking for this.

## What is AI drift?

A probabilistic system changes behaviour when the world moves. The questions customers ask shift with
the season; a partner changes its rules; the documents the agent retrieves are edited; the provider
updates the model behind an alias; or a failover quietly routes calls to a smaller model. None of these
is a deploy, none raises an error, and all of them change what the agent does.

## Catch it, step by step

### Step 1 · Pin what you can, and log what answered

Pin the model version in each environment's manifest, so an update is a change you make rather than
one that happens to you, and **log which model and prompt version answered every call**, so a failover
shows up in the data rather than in a complaint.

### Step 2 · Choose the output mix to watch

Pick the mix of decisions that matters — refunds versus credits, escalations versus resolutions,
rebookings versus waitlists — and chart it weekly. Watch the **output mix, not the accuracy**: accuracy
needs labels and arrives weeks late, while the mix is visible the same day.

### Step 3 · Set two thresholds, not one

A weekly threshold catches a jump; a baseline threshold catches a slide. At SkyWays the
refund-to-credit mix went from **61/39** in week one to **48/52** in week eight — thirteen points — and a
5% week-on-week alert never fired, because the slide averaged **1.9 points a week**. A second threshold,
on the level against a frozen baseline, catches exactly that. A slide of two points a week never trips a
weekly rule and still moves you thirty points in a quarter.

### Step 4 · Wire a breach to the release gate

When either threshold is breached, the [release gate](lesson:ai-governance-gates) re-opens
automatically: the affected action can drop back to shadow while the cause is found. If re-opening
needs somebody to decide to do it, it will be decided in the next steering meeting.

### Step 5 · Keep a labelled sample, on a schedule

Labels arrive late, but they still arrive. Have people judge a small sample of live cases on a fixed
schedule, per slice, and compare with the golden-set bar. It confirms what the mix suggested and
catches the drift that does not change the mix.

## Where you'll use it

- **From the first day of live traffic**, for every action the agent takes.
- **After any upstream change** — a new model version, a changed data source, a partner's rule change.
- **In the sponsor's report**, as a KPI: the output mix is a business metric, not a technical one.

## Why it matters

Drift is the defect with no error message, so it is found by whoever is looking — and if nobody is,
by a customer, months later. Watching the mix against two thresholds turns a slow, silent slide into
an alert in the second week instead of a complaint in the third month.

## Try it

A support agent's escalation rate was 20% at launch. Weekly readings since: 20, 21, 22, 23.5, 25, 26%.
The alert fires on a weekly change above 3 points. **Has it fired, and what would have caught it?**

<details><summary>Show the answer</summary>

**It has not fired** — the largest weekly change is 1.5 points. But the level has moved from 20% to 26%
in five weeks, a 30% relative rise. A baseline threshold — for example, alert when the level is more than
3 points from the frozen launch baseline — would have fired in week four, at 23.5%. Then check the logs
for what changed: a model version, a data source, or the questions customers are asking.

</details>

## Key takeaways

1. **Drift is behaviour changing with no deploy** — pin the model, and log which model answered every call.
2. **Watch the output mix**, not the accuracy: it is visible the same day, and labels arrive late.
3. **Two thresholds** — weekly and against a frozen baseline — with a breach that re-opens the release gate itself.

## FAQ

### What is drift in an AI model?

A change in the model's or the system's behaviour over time without a change to its code, caused by
changes in the inputs it sees, the data it retrieves, the world it describes or the model version
serving it. It shows up as a shift in outputs, not as an error.

### How do you detect LLM drift in production?

Chart the distribution of the agent's decisions — its output mix — weekly, against both a week-on-week
threshold and a threshold on the level versus a frozen baseline; log which model and prompt version
produced every response; and review a labelled sample per slice on a schedule.

### Can a model change even if I do not deploy anything?

Yes. A provider can update the model behind an alias, a failover can route calls to a different model,
and the documents or data the agent retrieves can change. Pinning the model version and logging which
model answered each call are how you notice.

### Why is a single drift threshold not enough?

Because a slow slide never crosses a weekly threshold. A system that drifts two points a week never
trips a five-point weekly alert, and still moves thirty points in a quarter. A threshold on the level
against a fixed baseline catches what the weekly one cannot.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Leave the customer a drift chart with two thresholds and a named reader. Drift is what breaks an agent after the FDE has gone. | Ask a coding agent to add the weekly output-mix job to the customer's scheduler. |
| **A product manager or FDPM** | Choose the output mix to watch, and the two thresholds: week on week, and against a frozen baseline. | Have a model propose the mix from the agent's output categories and their history. |
| **A GenAI or agentic AI engineer** | Pin model versions, log what answered every call, and keep a labelled sample on a schedule. | Ask a coding agent for the answering-model field and the sampling job. |

**Across the enterprise.** Watch drift centrally across products, with one job and one dashboard, because
a provider's model update reaches every team on the same day.

**The ten-minute workflow.** Check a history for the slide a weekly alert misses:

```text
Here is the weekly count of the agent's decisions by type since launch: <table>. Using weeks 1–2 as a
frozen baseline, flag every week in which a type's share moved more than <x> points week on week, or
more than <y> points from the baseline. Show a table and the first week each threshold fired.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Watch the output mix against two thresholds; drift re-opens the release gate | **Original** — this playbook | [QA lead, step 8](site:qa/#watch) · [Mental Models](wiki:Mental-Models#drift-is-the-defect-with-no-error-message) |
| The 5% drift alert | **Original** — a working default to tune | [Sources and Confidence](wiki:Sources-and-Confidence#the-working-methods-and-how-to-tune-each) |
| Pin the model; log which model answered | **Original** — this playbook | [Error Index](wiki:Error-Index#quality-dropped-with-no-deploy) |
| Concept drift, as a field of study | **Borrowed** | Gama, J. et al. (2014). A survey on concept drift adaptation. *ACM Computing Surveys* 46(4) |
| The SkyWays drift | **Illustrative** — a fictional airline | [The simulator](sim:#/) |
