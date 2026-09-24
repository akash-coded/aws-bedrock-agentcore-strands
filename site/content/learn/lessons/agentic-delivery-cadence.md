---
title: Agentic Delivery Cadence: What Runs Daily, Weekly, Quarterly
short: The operating rhythm
wiki: Agentic-Delivery-Cadence-Daily-Weekly-Quarterly
description: The operating rhythm of an agentic AI project: what runs every day, on every change, every week, every cycle and every quarter — and who owns each check.
dek: Most failures in an agentic system are silent. The checks that catch them have to run on a clock, because nobody will complain in time.
level: Intermediate
keywords: AI project cadence, operating rhythm AI team, how often to evaluate LLM, AI agent monitoring schedule, agile ceremonies AI, LLM regression testing, AI governance cadence, AI ops review
updated: 2026-09-24
---

> [!TIP]
> **The rhythm in one sentence.** Agentic delivery runs on six clocks: every day a bolt is built,
> integrated and reviewed by risk band; on every prompt, model, tool or context change the harness and
> the injection suite run again; every week someone reads drift, the attack run and the board's three
> numbers; every cycle the sponsor gets two numbers; every quarter the maturity check is re-run; and every
> incident or surprise bill starts its own loop, with a named owner.

{{map:agentic-delivery-cadence}}

**In this lesson** you'll learn:

- what runs at each of the six cadences, and who owns it;
- why proof runs on two triggers — every change and every week;
- how to set the whole rhythm up in week one, so nothing depends on memory.

## Sound familiar?

- The injection tests passed at launch and have not been run since.
- Drift gets checked when someone complains, which is weeks after it started.
- The maturity score on the slide is the one from the kickoff deck.

Each is a check that exists and has no clock.

## What is an operating rhythm?

**A fixed schedule of checks, each with an owner and a dated artefact, so that loops close without
anybody having to remember them.** Ordinary software fails loudly: an error, an alert, a user who cannot
log in. An agentic system mostly fails quietly — behaviour drifts with no deploy, a bill multiplies on
flat traffic, an attack suite goes stale while it keeps reporting green. A check that runs only when
someone notices a problem will run too late for every one of those.

## Set up the six clocks, step by step

### Step 1 · Every day — build, integrate, review

One bolt with one unknown, integrated the same day. The standup asks two questions: did yesterday's bolt
integrate, and what is today's one unknown? Review depth comes from the most dangerous tool the change
touches, via the path rule, never from the author. During a shadow run, QA reads agreement per slice every
day. **Owners:** engineering lead, architect for the cut. [Bolts vs sprints](lesson:bolts-vs-sprints)

### Step 2 · On every change — prove it again

Every prompt, model, tool or context change runs the harness per slice as a required check, and the
injection suite — every attack string against every gated tool from every entry point. Pin the model
version in each environment, so that a provider's update arrives as a change rather than as a mystery.
**Owners:** QA lead for the harness and suite, DevOps for the pipeline.

### Step 3 · Every week — watch what fails silently

Chart the output mix against a week-on-week threshold and a frozen baseline. Run the injection suite on a
schedule, with a date on it, even when nothing changed. Read the board's three numbers — review queue in
days, same-day integration rate, cards in shadow and live — and count the defects that escaped the
lane with no human reader. **Owners:** QA lead, DevOps, programme manager. [Drift](lesson:ai-drift-monitoring)

### Step 4 · Every cycle — report both numbers

The saving and the spend on one line, with review hours and re-runs beside them, sent to the sponsor
before it is asked for. The sponsor asks the four questions — which of these are rules, what may it do
without a person, what are the two numbers, what level are we — in about ten minutes. **Owners:** product
manager, sponsor. [Measuring AI productivity](lesson:measure-ai-productivity)

### Step 5 · Every quarter — re-audit the controls

Re-run the six-control maturity check by running each test, and expect the score to fall at least once.
Extend the attack strings: a suite that has not grown in three months is testing last quarter's attacks
and reporting green. **Owners:** sponsor for the check, QA lead for the suite.
[The maturity model](lesson:ai-delivery-maturity-model)

### Step 6 · On an event — close the loops nobody waits for

An incident gets a missing-control postmortem that ends in an enforced control and the next P0 brief. A
surprise bill gets one question — which of the four signatures does the per-call log show? A drift
breach re-opens the release gate by itself. These are the backwards loops; each needs a named owner
before the event, not after it. [The eight loops](lesson:the-eight-loops)

## Who owns which clock

| Clock | What runs | Owner | The dated artefact |
| --- | --- | --- | --- |
| Every day | One bolt, same-day integration, review by band | Engineering lead | Bolt build log row |
| Every change | Harness per slice; injection suite | QA lead, DevOps | A red or green run, per slice |
| Every week | Drift readout; scheduled attack run; board numbers | QA lead, DevOps, programme manager | Drift chart, dated suite run |
| Every cycle | Two-number report; the four questions | Product manager, sponsor | The report, sent unasked |
| Every quarter | Maturity check; attack strings extended | Sponsor, QA lead | Self-check with the tests' output |
| On an event | Postmortem; bill diagnosis; gate re-opened | Named in advance | Control, ADR and next-P0 brief |

## Where you'll use it

- **In week one**, as the programme manager's setup checklist: every clock scheduled, every owner named.
- **As the agenda** of a weekly operations review — the drift chart, the attack run, the three numbers.
- **After an incident**, to find which clock should have caught it.

## Why it matters

The three loops with nobody waiting — cost, incident, governance — are exactly the ones that fail
silently. A clock turns each into a routine with an owner; without one, each is handled once, by whoever
happens to notice, and never fed back into the design.

## Try it

A team runs the harness on every merge and ran the injection suite once, before launch. Two months later
a partner API adds a free-text field to its booking payload. **Which clocks should catch the risk, and
which did the team skip?**

<details><summary>Show the answer</summary>

**Every change and every week.** A new free-text field is a new entry point — a context change — so the
injection suite should run against it at once, and it should already have been running weekly. The team
treated the suite as a launch gate rather than a regression, so the new field reaches the agent with
nothing testing whether text inside it can steer a gated tool.

</details>

## Key takeaways

1. **Silent failures need clocks**, not complaints: six cadences, each with an owner.
2. **Proof runs on two triggers** — every change, and every week even when nothing changed.
3. **Every clock leaves a dated artefact**, and the backwards loops are owned before the event.

## FAQ

### How often should you evaluate an LLM application?

On every change to a prompt, model, tool or retrieved context, through the evaluation harness per slice;
and continuously in production, with the output mix charted weekly against both a weekly threshold and a
fixed baseline.

### How often should AI agents be tested for prompt injection?

Weekly on a schedule, and on every prompt, tool or context change — every attack string against every
gated tool from every entry point. Extend the attack strings at least quarterly, or the suite reports
green against last quarter's attacks.

### What meetings does an agentic AI team need?

A short daily standup with two questions, a daily demo of the integrated bolt, a weekly operations review
of drift and the board's numbers, a sponsor review each cycle with two numbers and four questions, and a
quarterly maturity check.

### How do you monitor an AI agent after launch?

Chart its output mix weekly against two thresholds, keep a per-call log through one gateway for cost and
routing, keep a redacted trace per consequential action, and wire a drift breach to re-open the release gate.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Hand the customer a calendar, not a document: every clock scheduled and every owner named before you leave. | Ask a model to turn the six clocks into calendar entries and short runbooks for the customer's team. |
| **A product manager or FDPM** | Run the weekly operations review on three things — the drift chart, the attack run and the board's numbers — in thirty minutes, with no slides. | Have a model assemble the weekly review from those three sources. |
| **A GenAI or agentic AI engineer** | Put the clocks in code: scheduled jobs for drift and the injection suite, required checks on every change. | Ask a coding agent to add the scheduled workflows, with an alert when one misses a run. |

**Across the enterprise.** Across a portfolio the clocks run on shared infrastructure, and a missed clock is
an alert in its own right: the silent failure of the process, not only of the product.

**The ten-minute workflow.** Audit what actually runs on a clock:

```text
Here is what we run and when: <list of jobs, meetings and reports>. Map it to the six clocks — every day,
every change, every week, every cycle, every quarter, on an event. List each check with no clock, each
clock with no owner, and each check whose last run is older than its clock.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The six clocks as one schedule | **Original** — this tutorial, from the playbook's cadences | [Journey: Engineering lead](wiki:Journey-Engineering-Lead) |
| The weekly and every-change injection suite; a suite that stops growing | **Original** — this playbook | [Journey: Engineering lead](wiki:Journey-Engineering-Lead) |
| Two drift thresholds, with a breach that re-opens the gate | **Original** — this playbook | [Drift](lesson:ai-drift-monitoring) |
| The daily standup | **Adapted** — new questions for bolts | Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide* |
| Blameless postmortems | **Borrowed** | Beyer, B. et al. (2016). *Site Reliability Engineering*. O'Reilly |
