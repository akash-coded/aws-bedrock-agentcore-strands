---
title: How to Run an Agentic AI Project: A Step-by-Step Playbook
short: How to run an agentic AI project
wiki: How-to-Run-an-Agentic-AI-Project
description: Twelve steps, from a vague request to an AI agent in production that someone can defend — who owns each step, what it produces, and the one thing never delegated.
dek: The whole lifecycle on one page, in the order you will do it. Each step links to the lesson that goes deeper.
level: Beginner
keywords: how to run an AI project, AI agent project plan, agentic AI project management, AI project steps, AI implementation roadmap, how to deliver an AI agent, AI project checklist
updated: 2026-09-23
---

> [!TIP]
> **The playbook in one sentence.** Run an agentic AI project in twelve steps across four phases:
> measure the pain, decide whether it needs a model, and set autonomy per action (**P0**); map every
> step, write an eight-field spec with a bar per slice, and put every limit in code (**P1**); build in
> bolts behind a harness and prove it in shadow (**P2**); then widen on evidence, watch for drift and
> report what it saved beside what it cost (**P3**).

{{board:delegation}}

**In this lesson** you'll learn:

- the twelve steps of an agentic AI project, in order, with the owner of each;
- what each step leaves behind, so you know when it is done;
- where the model helps at each step, and the one decision per phase it must never make.

## Sound familiar?

- The project plan is a Gantt chart with "build the agent" as one bar in the middle.
- Nobody can say who decides whether the agent is good enough to launch.
- The steps exist, but in the wrong order: the prototype came first and the requirements were written around it.

The order is the point. Every step below makes a later one cheaper, and doing them out of order is
how agentic projects end up rebuilt.

## The twelve steps

### P0 · Frame — is it worth doing, and is it AI at all?

**Step 1 · Measure the pain.** Turn the request into one line: who has the problem, how often, what
it costs today, and the evidence. *Owner: product manager.* [P0 Frame](lesson:p0-frame)

**Step 2 · Decide whether it is AI at all.** A genuine judgement call? Enough volume? Recoverable if
wrong? Two or three of your top five requests will come back as rules. *Owner: product manager.*

**Step 3 · Size the value and set autonomy per action.** Net value after running and checking it, and
an autonomy level for each action from what a mistake costs. *Owner: product manager, with the sponsor.*

### P1 · Design & Spec — what exactly, and under whose authority?

**Step 4 · Map every step.** Tag each step exact, best-guess or consequential; exact work goes in
code. *Owner: solution architect.* [P1 Design & Spec](lesson:p1-design-and-spec)

**Step 5 · Write the eight-field spec and derive the bars.** One screen, acceptance in EARS, a bar
per slice from damage and saving. *Owner: product manager, with QA.*
[How accurate an agent must be](lesson:how-accurate-must-an-ai-agent-be)

**Step 6 · Set the authority budget, and sign the hard gate.** Every tool banded, every cap in a
signature with a test. Nothing enters P2 until the spec, the bars and the budget are signed.
*Owner: solution architect.* [The hard gate](lesson:the-hard-gate)

### P2 · Build & Prove — does it meet the bar, slice by slice?

**Step 7 · Cut bolts, walking skeleton first.** One unknown per bolt, cut by dependency, integrated
the same day. *Owner: engineering lead.* [Bolts vs sprints](lesson:bolts-vs-sprints)

**Step 8 · Build the exact floor and the gated tools.** Functions and tests before prompts; caps that
raise; confirmation tokens the model cannot mint. *Owner: engineering lead.*
[Guardrails that hold](lesson:ai-guardrails-that-hold)

**Step 9 · Put the harness in CI.** Golden cases per slice, the lower bound reported, a merge blocked
when a touched slice falls below its bar. *Owner: QA lead.* [Prove the bar](lesson:prove-ai-accuracy)

**Step 10 · Run it in shadow.** The agent decides on live traffic and acts on nothing; agreement per
slice over a window fixed in advance. *Owner: QA lead.* [Shadow and cut-over](lesson:shadow-mode-and-cutover)

### P3 · Run & Learn — is it still true, and what did it cost?

**Step 11 · Cut over at 5%, widen on evidence, rehearse the rollback.** Each widening names the
evidence that earned it. *Owner: product manager and DevOps.* [P3 Run & Learn](lesson:p3-run-and-learn)

**Step 12 · Watch, report, and feed the next P0.** Drift against two thresholds; the saving beside
the spend; every incident turned into a control and a brief. *Owner: sponsor.*
[Drift](lesson:ai-drift-monitoring) · [Postmortems](lesson:ai-incident-postmortem)

## Where the model helps, and where it must not

The board above draws it phase by phase: **the model drafts, you check, and one thing per step is
never delegated**. The model can draft the pain register from interview notes, the spec from the
PRD, the tests from the spec and the postmortem from the trace. It must not decide what a mistake
costs your business, which actions it may take alone, whether a slice is good enough, or who is
accountable — those are facts about your business, regulator and ledger that no context makes
knowable from outside.

## Where you'll use it

- **As the project plan's skeleton**: twelve steps, each with an owner and an artefact, instead of one
  "build the agent" bar.
- **In a kick-off**, to show every role where it is accountable — and where it deliberately is not.
- **As an audit checklist** for a project already under way: find the first step that was skipped.

## Why it matters

Most agentic projects have the right activities in the wrong order. The prototype arrives before the
pain is measured, so the value is unknown; the build starts before the bar is set, so "good enough"
is argued at launch; the cap is decided in a document and enforced nowhere. The order in this list is
what prevents each of those.

## Try it

A team has a working prototype of a refund agent, a slide deck, and a launch date six weeks away.
**Which of the twelve steps is most likely to have been skipped, and what does it cost to do now?**

<details><summary>Show the answer</summary>

**Most likely steps 1, 5 and 6** — the measured pain, the bar per slice and the authority budget —
because a prototype-first project jumps from an idea to step 8. Doing them now is still cheap: a pain
line and a value line are an afternoon; the bars are arithmetic once the damage and saving per slice
are known; and the authority budget is a table plus a typed cap and two tests in the refund tool. What
is expensive is skipping them and discovering the gaps after launch.

</details>

## Key takeaways

1. **Twelve steps, four phases, one owner each** — and the order is what makes later steps cheap.
2. **Every step leaves an artefact**, so "done" is something a sceptic can open.
3. **The model drafts, you check**, and one decision per step is never delegated.

## FAQ

### What are the steps of an AI project?

Measure the pain; decide whether it needs AI; size the value and set autonomy; map every step; write
the spec and derive the bars; set the authority budget; cut bolts; build the exact floor and gated
tools; put the harness in CI; run in shadow; cut over and widen; then watch, report and feed the next
cycle.

### How long does an agentic AI project take?

It depends less on building than on evidence. A small change can run all twelve steps in an
afternoon; a new agent typically takes weeks, and the longest single wait is usually the live
evidence needed to widen a cut-over, which is set by traffic, not effort. SkyWays, the playbook's
worked example, ran ninety days.

### Who should lead an agentic AI project?

Each phase has one accountable owner — product manager, solution architect, engineering lead, and
the sponsor for the running system — and the sponsor owns the lifecycle as a whole. A programme or
delivery manager runs the cadence and the board across them.

### What is the most common mistake?

Building a prototype first and writing the requirements around it. The prototype then decides the
autonomy, the architecture and the bar by default, and the team spends the rest of the project
defending decisions nobody made on purpose.

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The twelve steps, their order and owners | **Original** — this playbook | [The Agentic PDLC](wiki:The-Agentic-PDLC) · [Gates and Governance](wiki:Gates-and-Governance#who-signs-what) |
| The model drafts, you check, one thing never delegated | **Original** — this playbook | [The Agentic PDLC](wiki:The-Agentic-PDLC#where-the-model-helps-and-where-it-must-not) |
| Gates opened by evidence | **Borrowed** | Cooper, R. G. (1990). Stage-gate systems. *Business Horizons* 33(3) |
| Bolts | **Adapted** | Raja SP (2025). [AI-Driven Development Life Cycle](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle). AWS |
| The SkyWays timeline | **Illustrative** — a fictional airline | [The simulator](sim:#/) |
