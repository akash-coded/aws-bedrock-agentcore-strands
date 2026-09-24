---
title: The Agentic PDLC for Product Managers: What Changes Monday
short: For product managers
wiki: Agentic-PDLC-for-Product-Managers
description: What an AI product manager does in the agentic PDLC: measure the pain, decide if it is AI at all, set autonomy per action, derive the bar, report two numbers.
dek: Your leverage moves upstream. The slow part of building is no longer the building — it is deciding precisely what right means, and who may act.
level: Beginner
keywords: AI product manager, product management for AI agents, how AI changes product management, AI PM skills, AI product requirements, agentic AI product management, PM role in AI projects
updated: 2026-09-24
---

> [!TIP]
> **The role in one sentence.** In the agentic PDLC the product manager turns requests into measured
> pains, decides which work is genuinely AI work, sets autonomy one action at a time, derives the
> acceptance bar for each slice from what a mistake costs, owns the intent and release gates, and
> reports what the feature saved beside what it cost — and stops approving anything they cannot evaluate.

{{map:agentic-pdlc-for-product-managers}}

**In this lesson** you'll learn:

- the eight steps a product manager takes across the four phases, and what each leaves behind;
- what is yours to own now, and what you should stop signing;
- how to use a model in the role — and the judgements it must never make for you.

## Sound familiar?

- You are asked to approve pull requests you cannot read, and to sign off a demo you cannot fault.
- The business case says "significantly faster", and finance will ask for a number next quarter.
- Three stakeholders want three different things from "the assistant", and the meeting has run for two weeks.

The role has not disappeared; its centre of gravity has moved. The work that decides whether an
agentic product succeeds now happens before anything is built.

## What changes for a product manager?

**You stop approving pull requests, and start deriving the bar from what a mistake costs.** When
agents write the code, the slowest part of building is deciding exactly what to build and what counts
as right — and a coding agent cannot ask you what you meant. So the discipline you always had becomes
mandatory: the pain is a measurement, the spec is exact, and "good enough" is a number per slice.

## Your eight steps

### P0 · Frame — the phase you lead

**1 · Discover.** Turn the request into one line: who, how often, what it costs, the evidence. At
SkyWays, "make rebooking smarter" became *240 disrupted passengers a day, 38 minutes each, $9.40 a
case*. **2 · Qualify.** Three questions — judgement, volume, recoverability — and expect two or three of
your top five to be rules. **3 · Frame.** A value line net of running and checking it, and autonomy set
per action from what a mistake costs. [P0 Frame](lesson:p0-frame)

### P1 · Design & Spec

**4 · Specify.** Eight fields on one screen; the five agentic ones are the decisions nobody made.
[The eight-field spec](lesson:p1-design-and-spec#step-2--write-the-eight-field-spec) **5 · Plan.**
You set the cadence — how often evidence arrives; the architect sets the cut.
[Bolts vs sprints](lesson:bolts-vs-sprints)

### P2 · Build & Prove

**6 · Gate.** Five gates exist and three are yours: **intent**, **release**, and **plan** shared with
the architect. Behaviour and expansion are QA's. Strike every approval you cannot evaluate.
[The five gates](lesson:ai-governance-gates)

### P3 · Run & Learn

**7 · Launch.** Shadow, then 5%, then wider — earned by evidence, never by a date.
[Shadow and cut-over](lesson:shadow-mode-and-cutover) **8 · Learn.** Two numbers on one line, every
cycle, before anyone asks — and every incident turned into the brief for the next P0.

## What is yours, and what is not

| Yours to own | Not yours — stop signing these |
| --- | --- |
| The intent and release gates, and the plan gate with the architect | The behaviour and expansion gates — QA's |
| Autonomy per action, and the door it sits behind | Pull requests you cannot evaluate |
| The acceptance bar per slice, derived rather than guessed | Model choice, temperature, framework — behaviours are yours, knobs are engineering's |
| The two-number report to whoever funds the work | The golden set's contents — you set the bar, QA curates the cases |

## How to use a model in this role

Use a model for **the drafting and the arithmetic, never for the judgement**. It can turn six interview
transcripts into a deduplicated pain register in a minute — and it will happily invent a value line if
you let it. You bring the numbers and the decision; the model brings the structure and the first draft;
every artefact leaves your hands having been read by you. What it must not decide: what a mistake costs
your business, and which actions may happen without a person.

## Where you'll use it

- **On Monday**: write the pain line for the feature in front of you, with a number and a source.
- **At the next steering meeting**: recast "how much should the assistant do?" as a table of actions.
- **At every release**: the two numbers, on one line, from you rather than from finance.

## Why it matters

When agents write the code, the product manager who can write an executable specification — exact,
small, with a bar per slice — is the most valuable person in the room. The one who approves pull
requests and signs demos is the least, and is also where most agentic projects lose control of what
they are building.

## Try it

A stakeholder asks you to approve a change that raises the agent's refund cap from $400 to $600 "to
reduce escalations". **Which of your steps does this touch, and what do you ask for before deciding?**

<details><summary>Show the answer</summary>

**Step 3 (autonomy) and step 6 (the plan gate).** Raising a money cap changes the autonomy of a
consequential action, which is yours. Ask for the evidence: how many escalations sit between $400 and
$600, what a wrong refund in that band costs, whether the bar for refunds is re-derived at the new
damage, and whether the new cap will be enforced in the tool's signature with its tests — not only in
the prompt. Then decide, and record it with a named approver.

</details>

## Key takeaways

1. **Your leverage is upstream**: measured pain, AI-fit, autonomy per action, and a derived bar.
2. **Three gates are yours** — intent, release and plan — and approvals you cannot evaluate are not.
3. **Report two numbers** every cycle, and let the model draft while you decide.

## FAQ

### What does a product manager do in an AI project?

Frames the problem as a measured pain, decides whether it genuinely needs AI, sets how much the agent
may do on its own per action, derives the accuracy bar for each kind of case from what a mistake costs,
writes the spec, owns the intent and release decisions, and reports value beside cost after launch.

### How is AI changing product management?

It moves the product manager's leverage upstream. Implementation is faster, so the bottleneck is
deciding precisely what to build and what counts as right. Writing requirements a machine can build
from, and bars derived from money, become core skills.

### Should product managers approve AI-generated code?

No. Approving pull requests you cannot evaluate adds a name without adding a check. Code review belongs
to engineering by risk band; the product manager's decisions are intent, autonomy, the bar and release.

### What skills does an AI product manager need?

Turning a vague request into a measurement; knowing when a problem is not AI; setting autonomy per
action from reversibility; deriving acceptance bars from damage and saving; writing precise, small
specs; and reporting cost beside value. Most are old product skills made mandatory.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | At a small customer you are often the PM as well: measure the pain, run the AI-fit, and get autonomy per action signed by someone who owns the risk. | Ask a model to interview you as the customer's PM, and write the pain register from your answers. |
| **A product manager or FDPM** | Your Monday: one pain measured, one bar derived, one approval you cannot evaluate removed. As an FDPM, add a fourth: sort each customer request into configuration, service or product. | Have a model classify last quarter's customer requests that way, with the evidence of a pattern behind every "product". |
| **A GenAI or agentic AI engineer** | Ask the PM for the bar per slice and autonomy per action before you build. If they are missing, draft them and ask for a signature. | Ask a model to draft the bar sheet from the spec, for the PM to correct rather than write. |

**Across the enterprise.** Define the AI PM's artefacts centrally — pain register, AI-fit record, bar sheet,
autonomy record — so product managers in every team are judged on the same evidence.

**The ten-minute workflow.** A pain line that survives to the steering committee:

```text
Interview me about the problem our AI feature is meant to solve. Ask one question at a time, and keep
going until you can write one line: "<who> waits <minutes> for <what>; <n> cases a day; <share> are
<the hard slice>; measured cost <$> a case, from <source>." Do not supply any number I have not given
you; mark it UNKNOWN instead.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The product manager's eight steps, owns and not-yours | **Original** — this playbook | [Product manager, end to end](site:product-manager/) · [Role: Product manager](wiki:Role-Product-Manager) |
| The shift: stop approving pull requests, start deriving the bar | **Original** — this playbook | [For leadership](site:protocol/) |
| The SkyWays examples | **Illustrative** — a fictional airline | [Journey: Product manager](wiki:Journey-Product-Manager) |
