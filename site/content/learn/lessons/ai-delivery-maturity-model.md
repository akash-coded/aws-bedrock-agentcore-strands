---
title: AI Maturity Model: Six Controls You Can Test in Ten Minutes
short: The maturity model
wiki: AI-Delivery-Maturity-Model
description: An AI maturity model that counts controls, not tools: six controls, each proven by a test you run in minutes, and how to pick the next one to build.
dek: Tool adoption is the metric that rewards the least mature behaviour available. Count what is enforced instead.
level: Intermediate
keywords: AI maturity model, AI maturity assessment, AI delivery maturity, how to measure AI maturity, AI governance maturity, AI readiness assessment, generative AI maturity model, AI capability maturity
updated: 2026-09-24
---

> [!TIP]
> **The model in one sentence.** Agentic delivery maturity is a count of six controls, not of tools:
> a context file the agent reads, a spec with a bar and an owner on every item, a harness that gates the
> merge per slice, caps in tool signatures, a trace that redacts, and production evidence with drift
> watched. Each is proven by running a test, your level is how many you can show, and the next control
> to build is the first one missing.

{{map:ai-delivery-maturity-model}}

**In this lesson** you'll learn:

- the six controls and the test that proves each one;
- why a decided control scores as absent, and why the level is deliberately unweighted;
- how to run the check in ten minutes, and what to build next.

## Sound familiar?

- The maturity slide counts AI tools adopted, and the number only ever goes up.
- Every control was marked present, and the refund the cap should have stopped still went out.
- The team says it is "not ready for level four yet", as if the levels were a staircase.

The first rewards buying tools, the second scores intent, and the third mistakes a checklist for a ladder.

## What is an AI maturity model?

**A way to say how safely and repeatably a team delivers with AI, and what to improve next.** Most
maturity models are staged ladders, in the tradition of the Capability Maturity Model's five levels. For
agentic delivery that shape misleads, because the controls that matter are independent and very unequal
in cost: capping a tool in its signature is an afternoon's work, while production evidence by segment
takes a quarter. A team with many AI tools and no gates is **less** mature, ships less safely and costs
more than a team with one tool and tight control.

## Run the check, step by step

### Step 1 · Score each control by running its test

| # | Control | The test |
| --- | --- | --- |
| 1 | A context file the agent reads | It exists in the repository and was updated this month |
| 2 | Every item has a spec, a bar and a named owner | Pick a story at random and look |
| 3 | The harness gates the merge, per slice | A slice below its bar blocks the merge, even if the average rises |
| 4 | Caps live in tool signatures, not prompts | Grep the prompts for the cap and find none; find it in the signature |
| 5 | The trace redacts | Search a week of rows for a passport number and find none |
| 6 | Production evidence by segment, with drift watched | The drift alert re-opens the release gate by itself |

Every test is something you **run**, not something you recall. Tick only what could be shown to you in
ten minutes. [Run the self-check](sim:#/toolkit/maturity)

### Step 2 · Mark a decided control as absent

Decided is not enforced. At SkyWays, this playbook's fictional airline, the refund cap was decided,
written into the autonomy record and repeated in the system prompt, so control 4 was marked present. On
day 82 a $2,000 refund went out that was not owed, because the refund tool's signature accepted any
amount. The test exists to catch exactly this.

### Step 3 · Read the list, not the number

The level is the count, **deliberately unweighted**, so that it cannot be argued about. The price is
that a team can score four with the two hardest controls missing, so report which controls are missing,
not only how many.

### Step 4 · Build the next control, and only that one

The next control to build is the **first one missing** from the list. Name an owner, a date and the test
you will run on that date. Six improvement actions at once produce none.

### Step 5 · Re-run it every quarter, and expect the score to fall once

Controls decay: a context file goes stale, a new tool is added without a cap, a harness check is
switched from required to optional during a crunch. A score that only ever rises is not being measured.

## Where you'll use it

- **Every quarter**, per team, in ten minutes.
- **When a board asks how mature the organisation is**: answer with a number out of six and the next
  control, not with a tool count.
- **Before widening an agent's use**, where controls 4 to 6 are the ones that matter.

## Why it matters

Adoption metrics reward buying tools; this rewards controlling them. Each of the six maps to a failure
this tutorial covers: an uninformed agent, an unmeasured bar, a regression hidden in an average, a cap
talked past, a leak in a log, drift nobody saw, so the score is a count of failures a team has closed.

## Try it

A team scores itself. The context file was last updated four months ago. Two of three stories picked at
random have a bar. Lowering a bar and pushing blocked the merge. The refund cap is in the prompt and the
autonomy record. A week of trace rows shows no passport numbers. The drift alert exists but does not
re-open the gate. **What is its level, and what does it build next?**

<details><summary>Show the answer</summary>

**Two out of six**: the harness (3) and the redacting trace (5). The context file is not current (1),
one story in three has no bar (2), the cap is decided but not enforced (4), and an alert that does not
re-open the gate is not control 6. The next control is the first missing one: bring the context file up
to date, an afternoon, then re-run its test.

</details>

## Key takeaways

1. **Count controls, not tools**: six of them, each present or absent.
2. **Score by running the test**: decided is not enforced.
3. **Build the first missing control**, one at a time, and re-run the check every quarter.

## FAQ

### What is an AI maturity model?

A structured way to assess how safely and repeatably an organisation delivers with AI, and what to
improve next. This one counts six enforced controls rather than tools adopted or stages reached, because
the controls are independent and each can be verified in minutes.

### How do you measure AI maturity?

Run a test for each control rather than asking whether it exists: grep the prompts for caps, push a
change that should fail the harness, search the trace for personal data, check that a drift alert
re-opens the release gate. The number of controls that pass is the level.

### What are the levels of AI maturity?

Here the level is simply the count, from zero to six, deliberately unweighted. Staged models such as
CMMI assume an order to climb; these controls do not have one, and a cheap control should never wait
behind an expensive one.

### How often should you reassess AI maturity?

Every quarter, and whenever tools, models or teams change. Controls decay silently, so a score that has
never gone down is a sign that it is being remembered rather than measured.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Score the customer on the six controls in week one by running each test. The first missing control is your first deliverable. | Ask a coding agent to run the six tests against the customer's repository and report each with its evidence. |
| **A product manager or FDPM** | Report the count and the next control each quarter, and expect the score to fall at least once. | Have a model compare this quarter's self-check with the last one and explain every change. |
| **A GenAI or agentic AI engineer** | Make each control testable in CI where you can: caps in signatures, redaction, the harness as a required check. | Ask a coding agent for a CI job that fails when a prompt states a cap the code does not enforce. |

**Across the enterprise.** Run the six-control check across every team each quarter. Publish the list, not
only the number, and fund the first missing control per team rather than a programme-wide initiative.

**The ten-minute workflow.** The self-check, scored by tests rather than by memory:

```text
Run a maturity self-check on this repository by testing, not asking: (1) a context file exists and
changed this month; (2) three random stories each have a spec, a bar and an owner; (3) the harness is a
required check that blocks a slice below its bar; (4) no cap exists only in a prompt; (5) the trace
redacts personal data; (6) a drift alert re-opens the release gate. Report each with its evidence.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Six controls, each with a test; the level is the count | **Original**: this playbook | [Maturity: control, not tool count](wiki:Gates-and-Governance#maturity-control-not-tool-count) |
| Read the list, not the number; build the first missing control | **Original**: this playbook | [For leadership](site:protocol/) |
| Staged maturity levels, which this model departs from | **Compare** | Paulk, M. C. et al. (1993). *Capability Maturity Model for Software, Version 1.1*. SEI, CMU/SEI-93-TR-024 |
| A yes-or-no check of a team that takes minutes | **Compare**: the same form | Spolsky, J. (2000). *The Joel Test: 12 Steps to Better Code*. Joel on Software |
| The day-82 refund | **Illustrative**: a fictional airline | [The simulator](sim:#/) |
