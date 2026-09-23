---
title: How to Roll Out Agentic AI Delivery: A 90-Day Plan
short: Rolling it out in 90 days
wiki: How-to-Roll-Out-Agentic-AI-Delivery
description: A 90-day plan for rolling out agentic AI delivery: pick for provability, write the artefacts, build in slices, shadow beside the humans, report two numbers.
dek: The sequence that works is deliberately unglamorous in the middle — and each phase has one trap that reliably catches capable teams.
level: Intermediate
keywords: AI rollout plan, how to roll out AI in an organisation, AI adoption roadmap, 90 day AI plan, AI transformation plan, AI pilot to production, AI change management, scaling AI agents
updated: 2026-09-23
---

> [!TIP]
> **The plan in one sentence.** Roll out agentic delivery one feature at a time over ninety days: pick
> a feature for provability rather than value and take a baseline (days 1–15); write the spec, the bars,
> the authority budget and a context file (15–30); build in daily slices proven in CI (30–60); run it in
> shadow beside the people doing the work, then cut over at 5% (60–90); and report two numbers from the
> first cycle.

```mermaid
flowchart TB
  D1["<b>Days 1–15 · Choose</b><br/><i>for provability, not value</i><br/><i>trap: the flagship</i>"]
  D2["<b>Days 15–30 · Specify</b><br/><i>spec, bars, authority</i><br/><i>trap: the persuasive demo</i>"]
  D3["<b>Days 30–60 · Build</b><br/><i>a slice a day, in CI</i><br/><i>signal: merges most days</i>"]
  D4["<b>Days 60–90 · Shadow</b><br/><i>beside the people, then 5%</i><br/><i>rule: widen on evidence</i>"]
  D5(["<b>Day 90 on · Report</b><br/><i>two numbers, every cycle</i><br/><i>signal: feature two</i><br/><i>needs less of you</i>"])
  D1 --> D2 --> D3 --> D4 --> D5

  classDef p0 fill:#5169811A,stroke:#516981,stroke-width:1.5px
  classDef p1 fill:#4B5CC81A,stroke:#4B5CC8,stroke-width:1.5px
  classDef p2 fill:#0E7F7C1A,stroke:#0E7F7C,stroke-width:1.5px
  classDef p3 fill:#9C68031A,stroke:#9C6803,stroke-width:1.5px
  class D1 p0
  class D2 p1
  class D3,D4 p2
  class D5 p3
```

**In this lesson** you'll learn:

- the five phases of a first rollout, and the trap or signal in each;
- why the first feature is chosen for provability, with the arithmetic that proves it;
- the six objections you will hear, and what answers each.

## Sound familiar?

- The first agentic project was the flagship, and a year later it is still a pilot.
- A demo convinced everyone in week three, and nothing has reached production since.
- The people doing the work today are described as resistant, and nobody has asked them anything.

Each is a sequencing mistake, and none needs a reorganisation to fix.

## What does a first rollout have to achieve?

**One feature proven end to end, whose artefacts the second feature can copy.** Not a portfolio of
pilots, and not tool adoption. The first feature buys the organisation a spec template, a bar derivation,
an authority budget, a harness in CI and a rehearsed rollback — and the evidence that the method works
here. The second feature should then need less attention than the first.

## Roll it out, step by step

### Step 1 · Days 1–15 — pick the wrong-looking thing

Choose one feature for **provability rather than value**: high volume, low damage per mistake, and an
existing human process to compare against. Run the three AI-fit questions across the top ten candidates
and publish the ones that came back as rules. **Take the baseline now** — person-days per story, before
anything changes. **The trap:** starting with the flagship, which has the highest bar, the least
tolerance for a first attempt and the most spectators. [Is it AI work?](lesson:p0-frame)

### Step 2 · Days 15–30 — write the artefacts nobody wants to write

The eight-field spec, the acceptance bar per slice, the authority budget and a context file in the
repository. Five of the eight spec fields will be undecided, and those five are the value of the
exercise. **The trap:** a demo exists by now and it is persuasive. A demo is the easy 20%; it cannot tell
you how often the system is wrong on the cases you did not choose. [P1 · Design and Spec](lesson:p1-design-and-spec)

### Step 3 · Days 30–60 — build in slices, prove in CI

A shippable slice a day, each proven before the next: a walking skeleton with no model in it first, caps
moved out of prompts into tool signatures, the golden set at fifty real cases running in CI, review
routed by risk band. **The signal:** something merged most days. If the demo is still the only evidence
at day 45, the slices are not slices. [P2 · Build and Prove](lesson:p2-build-and-prove)

### Step 4 · Days 60–90 — prove it beside the humans

Run it in shadow next to the people doing the work, deciding but never acting, for a window agreed in
advance and read daily per slice. Keep money actions gated whatever the shadow shows. Rehearse the
rollback before the cut-over, then cut over at 5% and widen on live evidence rather than on a date. If it
does not match, you learned that for free. [Shadow and cut-over](lesson:shadow-mode-and-cutover)

### Step 5 · Day 90 onward — report honestly, and let production set the agenda

Two numbers from the first cycle: the saving and the spend. A surprise bill goes back into the design,
an incident produces a control rather than a name, drift is watched weekly, and the maturity check is
re-run each quarter. **The signal that it took:** the second feature needs less of your attention than
the first, because the artefacts now exist to copy. [The maturity model](lesson:ai-delivery-maturity-model)

### Step 6 · Meet the resistance with evidence, not persuasion

| What you will hear | What is underneath | What answers it |
| --- | --- | --- |
| "This slows us down" | True for the first feature, untrue by the third | Show the artefacts being reused — the second spec takes an hour |
| "The model is good enough already" | Judged on curated examples | Ask for the score on the slice nobody picked, with its sample size |
| "We already have gates" | Approvals, not gates — clicks without evidence | Ask what would have made the last approver say no |
| "Engineering says the cap is handled" | Handled in a prompt | Ask to be shown it: prose or code decides the answer |
| "We cannot take a baseline, we have started" | True, and recoverable on the next feature | Say so in the report, and take one next time |
| "Our people will resist automation" | Often they resist being measured by it | Put the frontline in discovery first, and credit their requirements by name |

The move that does most of the change management is unglamorous: **credit every requirement to the
person who raised it, in writing, before consolidating any of them.** A voice that felt dropped in week
one comes back in week five as a constraint.

## When to use it

- **For an organisation's first agentic feature**, or its first since a failed pilot.
- **When a portfolio of pilots has stalled**: pick one, and run it through all five phases.
- **When a new business unit adopts the method**, with the first unit's artefacts as templates.

## Why it matters

A first rollout is decided in the two places teams most want to rush: the fortnight of artefacts, which
turns a demo into something that can be proven, and the shadow run, which is the only way to learn
whether the system agrees with the people doing the work. The plan spends its effort there, and the
first feature's artefacts are what make the second one cheaper.

## Try it

Leadership wants to start with the flagship: an agent that approves refunds. A wrong refund costs
nineteen times what a right one saves, and about twelve refund cases arrive a day. The alternative is an
agent that drafts replies, where a bad draft costs twice what a good one saves. **Using the bar, why
start with the drafts?** (Hypothetical numbers; assume the agent is right 96% of the time on refunds and
80% on drafts.)

<details><summary>Show the answer</summary>

**Because the refund slice cannot be proven inside a quarter.** Its bar is 19 ÷ 20 = 95%. Proving 95%
when the agent is right 96% of the time needs about 1.96² × 0.96 × 0.04 ÷ 0.01² ≈ 1,475 cases — at twelve
a day, about four months of evidence before the shadow run can end. The drafts' bar is 2 ÷ 3 ≈ 67%, and at
80% the Wilson lower bound clears it on about fifty cases. Start with the drafts, keep refunds with a
person, and let the first feature's artefacts carry the second.

</details>

## Key takeaways

1. **Pick the first feature for provability**, and take the baseline before anything changes.
2. **Spend the effort where the outcome is decided**: the artefacts fortnight, and the shadow run.
3. **Meet resistance with evidence**, and credit every requirement to the person who raised it.

## FAQ

### How do you roll out AI agents in an organisation?

One feature at a time: choose one that can be proven quickly, write its spec, bars and authority budget,
build it in daily slices proven in CI, run it in shadow beside the people doing the work, cut over
gradually, and report the saving and the cost together. Then copy its artefacts to the next feature.

### How long does it take to get an AI agent into production?

About ninety days for a first feature run this way, of which roughly a month is shadow and cut-over. Later
features are faster, because the spec template, harness and rollback already exist.

### Which AI use case should we start with?

A high-volume, low-damage task with an existing human process to compare against. The most valuable use
case usually has the highest bar and needs the most evidence, so it makes a poor first project.

### Why do AI pilots fail to reach production?

Two causes recur: the first feature was chosen for value and cannot clear its bar inside a quarter, or a
persuasive demo was treated as evidence and the specification, bars and tests were never written.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Choose the first feature with the customer for provability, not prestige, and write the AI-fit list that says why. | Ask a model to score the customer's candidates on volume, damage per mistake and an existing process to compare against. |
| **A product manager or FDPM** | Credit every requirement to the person who raised it, in writing, before consolidating any of them. | Have a model build the credited requirements register from the meeting transcripts. |
| **A GenAI or agentic AI engineer** | From day 30, merge something most days. If the demo is still the only evidence at day 45, the slices are not slices. | Ask a coding agent to report merges per day and harness results since day 30. |

**Across the enterprise.** Roll out one feature and one business unit at a time. The second unit starts
from the first unit's artefacts, and that reuse is where the enterprise-wide saving actually comes from.

**The ten-minute workflow.** A credited requirements register, straight from transcripts:

```text
Here are transcripts of our discovery meetings: <paste>. List every requirement stated, credited to the
person who said it, with the quote. Then group duplicates while keeping every credit, and list conflicts
between people as open questions. Do not merge or drop anything silently.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The ninety days, their traps and signals, and the resistance table | **Original** — this playbook | [For leadership](site:protocol/) |
| Choose the first feature for provability; the bar as damage ÷ (damage + saving) | **Original** — this playbook | [How accurate must an AI agent be?](lesson:how-accurate-must-an-ai-agent-be) |
| The walking skeleton | **Borrowed** | Cockburn, A. (2004). *Crystal Clear*. Addison-Wesley |
| Shadow deployment and canary release | **Borrowed** — general practice | See [Sources and Confidence](wiki:Sources-and-Confidence) |
| Early, visible wins sustain a change programme | **Compare** | Kotter, J. P. (1995). Leading change: why transformation efforts fail. *Harvard Business Review* 73(2) |
| The Wilson score interval | **Borrowed** | Wilson, E. B. (1927). *JASA* 22(158) |
