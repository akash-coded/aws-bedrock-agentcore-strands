---
title: Bolts vs Sprints: Planning Work When AI Writes the Code
short: Bolts vs sprints
wiki: Bolts-vs-Sprints-Planning-When-AI-Writes-the-Code
description: When AI builds a story in hours, a two-week sprint leaves it idle. How to plan in bolts: one unknown each, cut by dependency, integrated the same day.
dek: The unit of planning shrinks to match the speed of building. The hard part is not the cadence — it is the cut.
level: Intermediate
keywords: bolts vs sprints, agile with AI agents, sprint planning with AI, AI-DLC bolts, how to plan AI development, story slicing, walking skeleton, daily integration
updated: 2026-09-23
---

> [!TIP]
> **Bolts in one sentence.** A bolt is a thin, shippable slice of work carrying **one unknown**,
> built and integrated the same day — so when a coding agent can finish a story in hours, the team
> plans a day at a time instead of a fortnight, cuts the work by **dependency** rather than by
> priority, and starts with a walking skeleton that proves the pieces connect before anything clever
> is built.

{{figure:bolt_days}}

**In this lesson** you'll learn:

- what a bolt is, where the term comes from, and how it differs from a sprint story;
- how to cut a plan by dependency so every bolt can be built on its day;
- how the ceremonies change — standup, demo, review and done.

## Sound familiar?

- The agent finishes a story on Tuesday; the sprint review is a week on Friday.
- Day three's work needs something that is scheduled for day seven.
- The demo on day fourteen is the first time anyone learns whether the pieces fit.

A sprint was sized for how fast people build. When the building is fast, the sprint becomes a queue.

## What is a bolt?

A **bolt** is AWS AI-DLC's name for a work cycle of hours or days, replacing the sprint when AI does
much of the building. This playbook adds three rules that make bolts work: **each bolt carries exactly
one unknown**, the plan is **cut by dependency, not by priority**, and a bolt is **integrated the same
day** it is built.

The product manager decides the **cadence** — how often evidence arrives. The solution architect
decides the **cut** — what goes in which bolt. Getting the cut wrong is what makes the cadence fail.

## How to plan in bolts, step by step

### Step 1 · Set the cadence by how often you want evidence

Agree how often something merged, integrated and measured should arrive. For most agentic builds the
answer is daily. The integration deadline is part of the agreement: a bolt that is built but not
integrated has not happened.

### Step 2 · Cut by dependency, not by priority

Order the bolts so each can be built on its day without waiting for another. That usually means: a
**walking skeleton** first — the thinnest end-to-end path, with no model in it — then the exact code,
because it stands alone, then the model layer, then the gated writes, each after the control it needs.
At SkyWays a two-week sprint of five stories became ten one-day bolts, and day one's skeleton — read
a booking, display it — found a credentials problem that would otherwise have surfaced in week two.

### Step 3 · Give every bolt exactly one unknown

A bolt with two unknowns cannot tell you which one failed. A bolt with none should have been merged
yesterday. Write the unknown down: *does the reservation adapter authenticate?*, *can the ranker hit
its bar on same-day cases?* The plan's risk then falls as a measurable curve — the sum, over every
day, of the unknowns still open — and the walking skeleton is why it falls from day one.

### Step 4 · Write a story file per bolt

Each bolt gets a self-contained file an agent can build from with the chat window closed: context by
reference, the spec in EARS, the tools with their risk bands, the tests, the done-when and the cost.
A bolt that needs a chat thread was cut wrong. [The story file](lesson:what-is-aidd#step-2--build-from-a-story-file-not-a-chat-thread)

### Step 5 · Change the ceremonies

| Ceremony | With sprints | With bolts |
| --- | --- | --- |
| Planning | Two weeks of stories | Tomorrow's bolt, from its story file |
| Standup | A status round | "Did yesterday's bolt integrate? What is today's one unknown?" |
| Definition of done | Meets the story | Meets the story, passes its slice in the harness, **and is integrated** |
| Demo | Day fourteen | Every day, from what actually merged |
| Review | End of sprint | By risk band, the same day |

### Step 6 · Re-cut out loud, in the morning

When a bolt turns out to need another bolt's output, say so at standup and re-cut before the day is
spent — not at two in the afternoon. A re-cut is a finding about the plan, not a failure of the team.

## Where you'll use it

- **In P2**, from the first day of the build to the last.
- **When the team runs Scrum**: keep the sprint as a planning horizon if you like, and run bolts inside it.
- **When a programme manager reports progress**: the daily merge log is the progress report.

## Why it matters

The value of fast building is fast evidence. A two-week sprint turns an afternoon's work into a
fortnight's wait for feedback; a bolt turns it into a same-day answer. And cutting by dependency,
with the skeleton first, retires the biggest unknown — whether the pieces connect at all — on day one
instead of day fourteen.

## Try it

Here is a plan in priority order: (1) the refund action, (2) ranking alternatives, (3) the fare
calculation, (4) reading the booking. **Re-order it into bolts.**

<details><summary>Show the answer</summary>

**4, 3, 2, 1** — as a walking skeleton, then exact code, then the model, then the gated write.
Reading the booking end to end with no model is the skeleton that proves the pieces connect. The fare
calculation is exact code that blocks nothing. Ranking is the model layer, measured against its bar.
The refund goes last, because it is a gated write that needs its cap, its confirmation token and its
tests to exist first. Priority said the refund mattered most; dependency says it can only be built last.

</details>

## Key takeaways

1. A **bolt** is one unknown, built and **integrated the same day**.
2. **Cut by dependency, not by priority** — walking skeleton first, gated writes after their controls.
3. **The ceremonies follow**: tomorrow's bolt at planning, integration at standup, a daily demo, review by band.

## FAQ

### What is the difference between a bolt and a sprint?

A sprint is a time box, usually two weeks, holding several stories. A bolt is one thin slice of work
carrying a single unknown, built and integrated within hours or a day. Sprints plan a fortnight of
work; bolts plan tomorrow's.

### Where does the term "bolt" come from?

From AWS's AI-Driven Development Life Cycle, published in 2025, which uses bolts — cycles of hours or
days — in place of sprints. The rule of one unknown per bolt is this playbook's addition.

### Do bolts replace Scrum?

Not necessarily. Many teams keep a sprint as a planning horizon and run bolts inside it. What changes
is the unit of work, the standup question, the definition of done and the daily demo.

### What is a walking skeleton?

The thinnest possible version of the system that runs end to end — for an agent, typically reading an
input and producing an output with no model in the path. It proves the pieces connect before anything
difficult is built. The term comes from Alistair Cockburn.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Plan the engagement in bolts. Something merged most days is the trust currency of a customer engagement, and a stalled integration shows up on day two instead of week three. | Ask a model to cut the customer's epic into bolts with one unknown each, ordered by dependency. |
| **A product manager or FDPM** | Replace sprint planning with tomorrow's bolt: its one unknown, its story file and its done-when. | Have a model check every bolt for a second unknown and propose the split. |
| **A GenAI or agentic AI engineer** | Start with a walking skeleton with no model in it, schedule a tool's server before any write that uses it, and leave the proof for last. | Ask a coding agent to order the bolts by those rules and flag any cycle. |

**Across the enterprise.** Bolts change capacity planning: forecast in bolts integrated per day per team,
and let the review queue — not the build — set the pace of the portfolio.

**The ten-minute workflow.** Cut an epic into bolts:

```text
Here is an epic: <paste>. Cut it into bolts of at most one day, each with exactly one unknown. Order
them: a walking skeleton first with no model, exact code early, a tool's server before any gated write
that uses it, checkers after the steps they check, the proof last. Output: day, bolt, depends on, the
one unknown, risk band.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Bolts of hours or days in place of sprints | **Borrowed** | Raja SP (2025). [AI-Driven Development Life Cycle](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle). AWS |
| One unknown per bolt; cut by dependency; exposure in unknown-days | **Original** — this playbook | [How to cut sprints into bolts](wiki:How-to-Cut-Sprints-into-Bolts) |
| The walking skeleton | **Borrowed** | Cockburn, A. (2004). *Crystal Clear*. Addison-Wesley |
| Risk-first ordering | **Borrowed** | Boehm, B. (1988). A spiral model of software development and enhancement. *Computer* 21(5) |
| Sprints and their events | **Borrowed** | Schwaber, K. & Sutherland, J. (2020). [The Scrum Guide](https://scrumguides.org/) |
| The SkyWays plan | **Illustrative** — a fictional airline | [Try the bolt planner](sim:#/toolkit/bolts) |
