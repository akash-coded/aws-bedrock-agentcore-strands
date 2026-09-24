---
title: Agentic PDLC for Program Managers: Boards, Bolts, Reporting
short: For program managers
wiki: Agentic-PDLC-for-Program-Managers
description: How a program or delivery manager runs agentic AI delivery: the board, the cadence, the decision log, the review queue, gate conditions and two numbers.
dek: You do not own a phase. You own the system the phases run in — and the waits between them, which is where agentic programmes lose their weeks.
level: Beginner
keywords: AI program manager, technical program manager AI, delivery manager AI projects, how to manage AI agent projects, AI project reporting, agile delivery manager AI, AI project risk management
updated: 2026-09-23
---

> [!TIP]
> **The role in one sentence.** In agentic delivery the programme or delivery manager owns the system
> the phases run in rather than any one phase — the evidence board, the daily cadence, the log of open
> decisions with owners and dates, the review queue, the lead-time items started on day one, the
> conditions (not dates) for each gate, and the two-number report the sponsor reads.

{{map:agentic-pdlc-for-program-managers}}

**In this lesson** you'll learn:

- the eight things a programme manager runs across the four phases of agentic delivery;
- how to report progress when "code complete" is roughly the halfway point;
- which decisions are yours to chase and which are never yours to make.

## Sound familiar?

- The status report says green every week, and the launch still slips by a month.
- A decision has been "being discussed" for three weeks, and the build is quietly working around it.
- The plan has a launch date, and nobody has computed how long the canary needs.

In agentic delivery most of the lost time is waits between the phases, not work inside them — and the
waits belong to nobody unless they belong to you.

## What changes for a programme manager?

**You stop tracking tasks to done, and start tracking evidence to decisions.** When agents build a
story in hours, work is rarely the bottleneck. The waits are: a decision nobody owns, a review queue, an
access request made late, a canary that needs more traffic than the date allows. The role becomes
making those waits visible, owned and short.

## Your eight moves

### P0 · Frame

**1 · Set up the board, and take the baseline.** An evidence board with risk-band swimlanes, and — before
anything changes — person-days per story today. It takes an afternoon and cannot be recovered later.
[The board](lesson:agentic-kanban-board) **2 · Start the lead-time items.** Model access per model and
per region, data-export approvals, security review: requested in week one, whatever the plan says.

### P1 · Design & Spec

**3 · Run the decision log.** Every open decision, classified hard or soft, each with an owner and a
date; soft ones name their placeholder. A decision with no owner is the most useful thing you can find.
[The hard gate](lesson:the-hard-gate) **4 · Agree the cadence.** With the product manager and the
architect: how often evidence arrives — usually daily — and the integration deadline that goes with it.

### P2 · Build & Prove

**5 · Run the daily rhythm.** Standup asks two things: did yesterday's bolt integrate, and what is today's
one unknown? The demo is daily, from what merged. [Bolts vs sprints](lesson:bolts-vs-sprints)
**6 · Watch the review queue.** Count review in slots, not tickets; queue time is slots needed ÷ slots
cleared a day. When it passes two days, the policy is the problem. [Review by risk](lesson:review-ai-generated-code)

### P3 · Run & Learn

**7 · Schedule gates by condition, not by date.** The shadow window is fixed in advance; each widening
names its evidence; the rollback is rehearsed with a stopwatch before cut-over. Put the evidence days —
cases needed ÷ cases per day at the canary share — in the plan. [Cut delivery time](lesson:cut-delivery-time)
**8 · Assemble the two numbers, and run the maturity check.** The saving beside the spend, with review
hours and re-runs, every cycle; and each quarter, the six-control check with the first missing control
named. [Maturity](lesson:ai-delivery-maturity-model)

## What is yours, and what is not

| Yours to run | Not yours to make |
| --- | --- |
| The board, the cadence and the daily rhythm | The acceptance bar — the product manager derives it |
| The decision log: owners, dates, placeholders | The decisions themselves — you chase them, their owners make them |
| The review queue and the lead-time items | The risk band of a change — the path rule decides it |
| Gate conditions and the rollback rehearsal on the calendar | Whether a slice has earned wider use — QA's call |
| Assembling the two-number report | Signing it — the sponsor is accountable |

## How to use a model in this role

Let a model assemble the daily note from the merge log and the harness output — what merged, which
slice ran, what it scored — in thirty seconds instead of ten minutes, and draft the weekly report from
the board. Do not let it summarise a decision as made when it is only discussed, or turn a lower bound
into a pass: read every number it reports against its source.

## Where you'll use it

- **In the first week of any agentic programme**: board, baseline, lead-time requests.
- **Every morning**: the two standup questions and the daily demo.
- **Every week and every cycle**: the review queue, the decision log, and the two numbers.

## Why it matters

A status report built on tasks says green while an agentic programme slips, because tasks finish fast
and evidence does not. A report built on evidence — what merged, what is proven, what is waiting on
whom — shows the slip the week it starts, when it is still cheap to fix.

## Try it

Your programme has: a spec signed last week; a framework choice "still being evaluated" with no owner;
model access requested in one region but the data must stay in another; a canary planned at 5% of
300 cases a day with 600 cases needed. **List what you do this week.**

<details><summary>Show the answer</summary>

**Four things.** Give the framework decision an owner and a date, and a placeholder — an interface
layer — so the build can proceed. Request model access in the region the data must stay in, today.
Put the canary's length in the plan: 600 ÷ (5% × 300) = **40 days**, and ask whether a wider share is
acceptable for low-risk actions. And confirm the board's Specified column shows the signed spec, bar
and authority budget, so the hard gate is visible as passed.

</details>

## Key takeaways

1. You own **the system and the waits**, not a phase: board, cadence, decisions, queue, lead times.
2. **Track evidence to decisions**, and put gate conditions — never bare dates — in the plan.
3. **Assemble the two numbers** every cycle and the **maturity check** every quarter.

## FAQ

### What does a program manager do in an AI project?

Runs the delivery system around the phases: an evidence-based board, a daily cadence, a log of open
decisions with owners and dates, the review queue, the early requests for access and approvals, gate
conditions on the calendar, and the report of value beside cost that the sponsor reads.

### How do you report progress on an AI agent project?

By evidence, not tasks: what merged and integrated each day, which slices are proven against their bars,
what is in shadow or live and what earned it, what is waiting on which decision, and the saving beside
the spend. Code complete is roughly the halfway point.

### How do you manage risk in an agentic AI project?

Keep a decision log that classifies each open decision as hard — settled before its phase closes — or
soft — running behind a placeholder with an owner and a date — and chase the owners. Most schedule risk
is a decision nobody owns; most product risk is a limit that lives only in a prompt.

### Do agentic projects still need a delivery manager?

Yes. Agents shorten the building; they do not shorten decisions, review queues, access requests or the
time live traffic takes to produce evidence. Someone has to own those waits.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Across several customer deployments you are running a programme: one board, one decision log and one review-queue number per customer. | Ask a model to merge every customer's status into one programme view, blocked decisions first. |
| **A product manager or FDPM** | Give the programme manager your gate conditions in writing. They become dates only when the evidence arrives. | Have a model turn the gate conditions into a milestone plan triggered by evidence, not by dates. |
| **A GenAI or agentic AI engineer** | Keep the integration deadline honest by publishing same-day integration and the review queue every day. | Ask a coding agent for a daily job that posts both numbers to the team channel. |

**Across the enterprise.** A programme office for AI delivery tracks decisions, lead times and evidence
across teams. The review queue and the blocked decisions are its critical path — not the build.

**The ten-minute workflow.** A decision log, pulled from the week's noise:

```text
Here are this week's meeting notes and chat excerpts: <paste>. Extract every decision made or deferred.
For each: the decision, hard or soft (can it be reversed cheaply once building starts?), the owner, the
date it is due, and what is blocked until it is made. List decisions with no owner first.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The programme manager's eight moves, as a role | **Original** — this tutorial, assembled from the playbook's roles and gates | [Gates and Governance](wiki:Gates-and-Governance) |
| The daily note from the merge log | **Original** — this playbook | [How to cut sprints into bolts](wiki:How-to-Cut-Sprints-into-Bolts) |
| Queue time = slots needed ÷ slots per day | **Borrowed** | Little, J. D. C. (1961). *Operations Research* 9(3) |
| Visualise work and limit work in progress | **Borrowed** | Anderson, D. J. (2010). *Kanban*. Blue Hole Press |
| The SkyWays figures | **Illustrative** — a fictional airline | [The simulator](sim:#/) |
