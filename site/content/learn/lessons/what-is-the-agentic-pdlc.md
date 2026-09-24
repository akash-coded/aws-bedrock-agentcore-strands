---
title: What Is the Agentic PDLC? The P0–P3 Framework Explained
short: What is the agentic PDLC?
wiki: What-Is-the-Agentic-PDLC
description: The agentic PDLC is a four-phase lifecycle — Frame, Design & Spec, Build & Prove, Run & Learn — for software in which an AI model does part of the work.
dek: Four phases, one hard gate and a line that comes back. The whole framework in one sitting, with the reason behind each piece.
level: Beginner
keywords: agentic PDLC, P0 to P3 framework, agentic product development lifecycle, AI product development lifecycle, agentic SDLC, AI-DLC, how to run agentic AI projects
updated: 2026-09-24
---

> [!TIP]
> **The agentic PDLC in one sentence.** It is a product lifecycle for software in which an AI model
> makes some of the decisions, run in four phases: **P0 Frame** decides whether it is worth building
> and how much the machine may do, **P1 Design & Spec** writes it down so a machine can build it,
> **P2 Build & Prove** builds it in slices against a measured bar, and **P3 Run & Learn** watches it
> in production until what you learn becomes the next P0.

{{board:pdlc}}

**In this lesson** you'll learn:

- what each of the four phases decides, and the condition that ends it;
- why only one of the four hand-offs is a hard gate;
- how the framework sits beside AWS AI-DLC, the BMAD Method, spec-driven development and Scrum.

## Sound familiar?

- The demo worked in week two. It is week eleven, and nobody can say whether it is good enough to launch.
- The spec was signed, and every engineer still asked the same three questions in their first week.
- The bill arrived at four times the estimate with traffic flat, and it went to finance instead of back to the design.

Each of those is a phase that ended on a date instead of on evidence. That is the specific failure
the agentic PDLC is built to prevent.

## What is the agentic PDLC?

A **product development lifecycle (PDLC)** is the path a product takes from an idea to something
people rely on. The **agentic PDLC** is that path redrawn for products in which a large language
model does part of the work — drafts the reply, chooses the tool, issues the refund.

The redraw is needed because a model breaks an assumption every older lifecycle made: that software
does the same thing every time. A model is right most of the time, fluent all of the time, and wrong
without raising an error. So the lifecycle has to answer three questions a waterfall plan or a
Scrum board never asked: **how right is right enough, who decided that, and how will we know when it
stops being true?**

It answers them with four phases. They are numbered P0 to P3 so they sort in order, and so nobody
mistakes them for one vendor's stage names.

## The four phases, step by step

| | Phase | The question it answers | Accountable | It ends when |
| --- | --- | --- | --- | --- |
| **P0** | Frame | Is it worth doing, is it AI at all, and how much may the machine do? | Product manager | The pain is a measurement and the AI-fit verdict is recorded |
| **P1** | Design & Spec | What exactly is being built, and under whose authority? | Solution architect | The spec, the bar and the guardrails are signed |
| **P2** | Build & Prove | Does it meet the bar, slice by slice? | Engineering lead | The golden set clears the bar and a shadow run agrees |
| **P3** | Run & Learn | Is it still doing what we launched, and what did it cost? | Sponsor | Two numbers are reported and the next P0 brief exists |

### Step 1 · P0 Frame — decide before anything is built

P0 turns a request into a measurement: "customers hate waiting" becomes a count, a cost and a link
to the evidence a sceptic can open. It then asks whether the job needs a model at all — many do not
— and sets how much the machine may do on its own, one action at a time. It ends when the pain has a
number and the AI-fit verdict, including what was rejected, is written down.
[P0 Frame in depth](lesson:p0-frame).

### Step 2 · P1 Design & Spec — write it so a machine can build it

P1 writes down what will be built precisely enough that a coding agent, or an engineer who was not
in the room, can build it without asking. That means acceptance criteria in a checkable syntax, an
**acceptance bar for each slice** derived from what a mistake costs, and the guardrails: what the
agent may do, what needs a person, and which limits live in code rather than in the prompt. It ends
when all three are signed. [P1 in depth](lesson:p1-design-and-spec).

### Step 3 · P2 Build & Prove — build in slices, prove each one

P2 builds in **bolts**: cycles of hours or days, one risk each, starting with a walking skeleton that
runs end to end. Every slice is measured against its bar on a golden set, and a merge that drops a
slice below its bar is blocked. P2 closes with a **shadow run**, in which the agent handles live
traffic without acting and its answers are compared with what people actually did.
[P2 in depth](lesson:p2-build-and-prove).

### Step 4 · P3 Run & Learn — keep it true, and learn from it

P3 widens the live share gradually, watches the output mix for drift, and reports **two numbers on
one line**: what the feature saved and what it cost. An incident, a drift alert or a bill that leaves
its estimate does not end in a ticket — it ends in a brief for the next P0.
[P3 in depth](lesson:p3-run-and-learn).

## The one hard gate

Four hand-offs connect the phases, and only one of them is hard.

{{map:what-is-the-agentic-pdlc}}

A **soft** hand-off may cross with a placeholder, a named owner and a date, which keeps work moving
while a decision is still being measured. The **hard** one may not: nothing enters P2 until the
spec, the bar and the guardrails are signed. It is hard because it is the last point at which
changing your mind costs a document instead of a rewrite — a one-way door, where the others are
two-way. [Why the gate sits exactly there](lesson:the-hard-gate).

## How it fits beside AI-DLC, BMAD, spec-driven development and Scrum

The agentic PDLC is a spine, not a rival method. The methods you have heard of each occupy part of it.

{{frameworks:methods}}

| Method | What it is | Where it sits |
| --- | --- | --- |
| **AWS AI-DLC** | AI proposes and people decide, across Inception, Construction and Operations, in bolts of hours or days | Inception ≈ P0–P1 · Construction ≈ P2 · Operations ≈ P3 |
| **BMAD Method** | Agent personas that mirror an agile team, each handing a document on | Mostly P0–P2 |
| **Spec-driven development** | The spec is the maintained artefact; code is generated from it, as in Kiro or GitHub Spec Kit | P1 and P2 |
| **Scrum** | Time-boxed sprints over a backlog | Inside P2, where the sprint's unit becomes a bolt |

So the question worth arguing about is not *which method*, but *how deep this particular change
needs to go*. A one-line fix to a refund cap is tiny and deep; a large refactor of a read-only report
is big and shallow. [The named methods on one spine](wiki:The-Agentic-PDLC#how-the-named-methods-sit-on-the-spine).

## Where you'll use it

- **On every change that involves a model**, at the depth the change needs. A one-line fix to a
  refund cap runs all four phases in an afternoon; a new agent runs them over weeks.
- **Alongside the method you already use.** Stand-ups, backlogs and retrospectives carry on. What
  changes is what each phase must leave behind before the next one starts.
- **By every role.** Each phase has one accountable owner, but every role works in every phase —
  including the cells where a role should deliberately do nothing, which the
  [by-role board](site:#by-role) draws.

## Why it matters

- **It makes "good enough" a number.** Each phase ends on evidence someone can open, so a launch is a
  decision rather than a mood.
- **It moves the expensive decisions to where they are cheap.** Authority, the bar and the
  guardrails are settled on paper, before the code exists to argue for itself.
- **It closes the loop.** P3 produces the next P0, so an incident or a bill changes the design
  instead of the budget.

## Try it

A team at an insurer has a prototype agent that approves small claims. It demos well, and the
engineering lead wants to start building "for real" on Monday. The product manager has a measured
pain; the architect has a draft spec. **What must be true before the work can enter P2?**

1. The model and its temperature are chosen and written into the spec.
2. The spec, the acceptance bar for each slice and the guardrails are signed.
3. A sprint plan exists for the next six weeks.
4. The prototype is deployed to production behind a feature flag.

<details><summary>Show the answer</summary>

**2.** P1 → P2 is the one hard gate, and it opens on a signed spec, a bar per slice and the
guardrails. Option 1 is a known anti-pattern — fixing the model's knobs in a spec ties a requirement
to one vendor's settings, which belong to the build. Option 3 is a calendar, not evidence. Option 4
skips P2 altogether.

</details>

## Key takeaways

1. The agentic PDLC has four phases — **P0 Frame, P1 Design & Spec, P2 Build & Prove, P3 Run & Learn** — and each ends on evidence, never on a date.
2. **Only P1 → P2 is a hard gate**; the other hand-offs may cross with a placeholder, an owner and a date.
3. It is **a spine, not a rival method**: AI-DLC, BMAD, spec-driven development and Scrum each fit onto part of it.

## FAQ

### Is the agentic PDLC the same as AWS AI-DLC?

No. AI-DLC is AWS's methodology, published in 2025, in which AI proposes and people decide across
three phases — Inception, Construction and Operations — run as short bolts. The agentic PDLC is a
method-agnostic lifecycle that AI-DLC fits onto: Inception covers P0 and P1, Construction is P2, and
Operations is P3. You can run AI-DLC inside it.

### What do P0, P1, P2 and P3 stand for?

The four phases in order: P0 Frame, P1 Design & Spec, P2 Build & Prove and P3 Run & Learn. Numbering
starts at zero because framing happens before anything is designed — it is the phase teams most often
skip, and calling it P0 makes skipping it visible.

### Do I need all four phases for a small change?

Yes, at a small depth. A one-line change to a refund cap is still framed, specified, proven and
watched, in an afternoon. What scales with the change is how much each phase produces, not whether
it happens.

### Does the agentic PDLC replace Scrum or Agile?

No. It is a lifecycle, not a team process. Sprints, stand-ups and retrospectives carry on; in P2 the
unit of work becomes a bolt — one risk, hours or days — and the milestone becomes a passing shadow
run rather than a demo.

### Who owns the agentic PDLC?

Each phase has one accountable owner: the product manager for P0, the solution architect for P1, the
engineering lead for P2 and the sponsor for P3. The lifecycle as a whole — and especially the loops
that run backwards from P3 — belongs to the sponsor.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Place the customer's request on the four phases in the first meeting. Most arrive as "build an agent" and are an unanswered P0 question. | Paste the brief into a model and have it sort every sentence into P0–P3, then list what each phase is missing. |
| **A product manager or FDPM** | Make the phases the roadmap's spine: nothing enters P2 without a bar and an authority budget signed in P1. | Ask a model to redraw the roadmap as a P0–P3 table and flag every item in build without a signed spec. |
| **A GenAI or agentic AI engineer** | Before writing a prompt, ask which phase you are in. Coding before the bar and the limits exist means making P1's decisions by accident. | Put the phase and the spec's path in the context file, so the coding agent stops at work the spec does not cover. |

**Across the enterprise.** Teams keep their own method — Scrum, AI-DLC, Spec Kit — and the organisation
standardises only the four hand-offs and what each owes. That is what makes a portfolio of AI products
comparable at all.

**The ten-minute workflow.** Turn any brief into the questions nobody has answered yet:

```text
Here is a project brief: <paste>. Sort every sentence into the phase it belongs to: P0 Frame,
P1 Design & Spec, P2 Build & Prove, P3 Run & Learn. Then list, per phase, the decisions the brief
has not made, as questions I can put to the sponsor. Do not answer them yourself.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The four phases, their names and their end conditions | **Original** — this playbook | [Sources and Confidence](wiki:Sources-and-Confidence) |
| One hard gate and three soft hand-offs | **Original** — this playbook | [Gates and Governance](wiki:Gates-and-Governance) |
| Phases separated by gates that require evidence | **Borrowed** | Cooper, R. G. (1990). Stage-gate systems: a new tool for managing new products. *Business Horizons* 33(3) |
| Make hard-to-reverse decisions the gated ones | **Adapted** | Bezos, J. 2015 letter to Amazon shareholders — Type 1 and Type 2 decisions |
| Bolts: work cycles of hours or days | **Adapted** | Raja SP (2025). [AI-Driven Development Life Cycle: Reimagining Software Engineering](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle). AWS |
| Specs as the maintained artefact | **Borrowed** | Böckeler, B. (2025). [Understanding spec-driven development: Kiro, spec-kit and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |

**Go deeper:** [The Agentic PDLC](wiki:The-Agentic-PDLC) — the full reference, with a template for
every phase exit · [The four boards](site:) · [The simulator](sim:#/), the same framework as ninety
playable days.
