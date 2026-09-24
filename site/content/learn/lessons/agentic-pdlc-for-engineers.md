---
title: The Agentic PDLC for Software Engineers: Build With Agents
short: For engineers
wiki: Agentic-PDLC-for-Software-Engineers
description: How software engineers work in the agentic PDLC: a context file, story files, exact code first, gated tools, a harness that decides merges, and a bolt a day.
dek: The model does the typing and the sweep. You own the floor it stands on, the boundary it cannot cross, and the check that decides what merges.
level: Beginner
keywords: software engineer AI agents, how to work with AI coding agents, AI pair programming workflow, Claude Code workflow, building LLM applications, AI engineering best practices, engineering lead AI
updated: 2026-09-24
---

> [!TIP]
> **The role in one sentence.** In the agentic PDLC the engineering lead writes the context file every
> coding agent reads, builds each bolt from a story file, puts every number the product acts on in
> tested code, enforces every limit in a tool's signature, wires the harness that blocks a merge when a
> slice falls below its bar, and ships a slice a day — letting the model type, never letting it hold the
> boundary.

{{map:agentic-pdlc-for-engineers}}

**In this lesson** you'll learn:

- the engineering lead's eight steps, and why P0 is deliberately not on your clock;
- the three things you own that no model may: the floor, the boundary and the merge check;
- how to use coding agents so they make you faster rather than busier.

## Sound familiar?

- The agent re-implemented a calculation inline, confidently, and it was wrong by eighteen dollars.
- "Review your answer before returning it" was added to the prompt; scores did not move and the bill rose.
- The evaluation job posts a comment on every pull request, and on the Thursday before the pilot someone clicked past it.

Each is a boundary held by a request instead of by code. The engineer's job is to move each one into
code.

## What changes for an engineer?

**You stop treating a prompt rule as a control, and start shipping a slice a day.** Coding agents make
the typing cheap; they do not make it correct. What you own is everything around the typing: the
context the agent reads, the file it builds from, the deterministic floor under it, the limits it
cannot cross, and the check that decides whether what it built may merge.

## Your eight steps

### P0 · Frame — not on the clock

You read the brief and start nothing. An engineer who starts building in P0 is building the prototype
the requirements will later be written around.

### P1 · Design & Spec

**1 · Prepare** the context file every coding tool reads — stack, context layers by path, conventions,
commands that have actually been run, a never-touch list. An hour's work, and the biggest quality lever
you have. [AIDD's five habits](lesson:what-is-aidd)

### P2 · Build & Prove — the phase you lead

**2 · Slice**: build each bolt from a six-part story file, never a chat thread. **3 · Floor**: every
number that gets acted on is a function with a unit test — SkyWays' prompt returned $80 where the ledger
said $62. **4 · Layer**: the model calls on top, with an independent checker after the expensive ones.
**5 · Gate**: caps and confirmation tokens in tool signatures, each with two tests seen failing first.
**6 · Harness**: the golden set in CI as a required check, in cost order, per slice.
**7 · Ship**: one bolt a day in dependency order, the shadow path behind a flag, the rollback rehearsed.
[P2 Build & Prove](lesson:p2-build-and-prove)

### P3 · Run & Learn

**8 · Operate**: caching that hits, routing by complexity with a loop cap, a trace that redacts, an
injection suite run weekly, and the effort-and-token ledger the product manager's cost number is built
from. [Why the bill is 4×](lesson:ai-agent-costs)

## What is yours, and what is not

| Yours to own | Not yours |
| --- | --- |
| The context file, and the story file every bolt is built from | The bolt cut — the architect's; you say whether each bolt can be built alone |
| The deterministic floor: every acted-on number is a tested function | The acceptance bar — the product manager derives it; you make it run |
| The boundary: caps and confirmation tokens in signatures | The golden set's contents and the judge rubric — QA's |
| The harness in CI, and the per-slice rule that blocks a merge | The cut-over and widening — you build the flag; the PM throws it |
| Build order within the cut, integrated the same day, and the ledger | |

## How to use a model in this role

Use a model for **the typing and the sweep, never for the boundary**. It will write a correct function
faster than you can — and just as happily write a cap into a prompt and report the cap as done. Let it
draft *inside* something you wrote: a context file, a story file, a signature you already fixed. Every
line that moves money, changes a booking or writes a trace row is read by a person before it merges.

## Where you'll use it

- **On day one of a repository**: the context file, before the first agent session.
- **The evening before each bolt**: its story file, so the chat window can stay shut.
- **On every change to a gated tool**: two named readers, and the over-cap and no-confirmation tests.

## Why it matters

Coding agents amplify whatever habits surround them. With a floor, a boundary and a harness, they
produce more working software; without them, they produce more plausible software, faster — and the
difference only shows in production.

## Try it

An agent wrote `issue_credit(customer_id, amount)` and the prompt says credits over $50 need approval.
**What do you change before this merges?**

<details><summary>Show the answer</summary>

**The signature, and two tests.** Give `amount` a bound so a value over $50 raises unless a valid
confirmation token — created only by a person's approval — is passed; write `test_over_cap_raises` and
`test_no_confirmation_raises`, and see both fail before the fix makes them pass. Keep the sentence in the
prompt so the agent behaves well by default. Band the tool as money, so the change needs two named
readers.

</details>

## Key takeaways

1. **The model types; you hold the floor, the boundary and the merge check.**
2. **Context file first, story file per bolt**, and every acted-on number in tested code.
3. **Ship a bolt a day** behind a flag, with the harness deciding what merges.

## FAQ

### How do software engineers work with AI coding agents?

By giving the agent what it needs to be right and taking away what lets it be dangerous: a context file
it reads every session, a story file per unit of work, tested functions for anything exact, limits in
tool signatures, and a harness that blocks merges when quality drops — then reviewing by risk.

### What does an engineering lead own in an AI project?

The context and story files, the deterministic floor, the enforced boundary in tool signatures, the
evaluation harness in CI, the build order within the architect's cut, and the ledger of effort and tokens
that the cost report is built from.

### Should AI agents write production code?

Yes, inside structure: from a story file, against a context file, on top of tested exact code, with
limits enforced in signatures and a harness that gates the merge. Code that moves money or changes
records is read by people before it merges.

### What is a deterministic floor?

The set of functions, each with a unit test, that do every exact thing the feature relies on —
arithmetic, lookups, published rules — so that no number the product acts on ever comes from a model.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | In the customer's codebase, start with the context file and one walking skeleton. A merged change on day one is your credibility. | Have a coding agent read the repository and draft the context file before your first meeting. |
| **A product manager or FDPM** | Give engineers story files with the spec lines and the done-when. A coding agent cannot ask you what you meant. | Ask a model to rewrite a ticket as a story file and list every question an engineer would still have. |
| **A GenAI or agentic AI engineer** | Your loop: exact code first, then the model step with its checker. The harness decides the merge, and caps live in signatures. | Run the coding agent from the story file with a failing test first, and let the test define done. |

**Across the enterprise.** Standard scaffolding — context file, story template, harness, per-call log —
across repositories makes any engineer productive on any team's agent in a day.

**The ten-minute workflow.** Test-first with a coding agent:

```text
Here is the story file for today's bolt: <paste>. Before any implementation, write the failing tests:
unit tests for every exact step, one golden-slice test for the best-guess step against its bar, and one
refusal test for every cap. Then implement until they pass. Stop and ask if the story file does not say
what "right" means for a step.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The engineering lead's eight steps, owns and not-yours | **Original** — this playbook | [Engineering lead, end to end](site:engineering/) · [Role: Engineering lead](wiki:Role-Engineering-Lead) |
| The shift: stop treating a prompt rule as a control | **Original** — this playbook | [For leadership](site:protocol/) |
| The walking skeleton | **Borrowed** | Cockburn, A. (2004). *Crystal Clear*. Addison-Wesley |
| The SkyWays examples | **Illustrative** — a fictional airline | [Journey: Engineering lead](wiki:Journey-Engineering-Lead) |
