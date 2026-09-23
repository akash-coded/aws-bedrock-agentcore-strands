---
title: How Accurate Does an AI Agent Need to Be? The 3-Step Answer
short: How accurate must an agent be?
wiki: How-Accurate-Does-an-AI-Agent-Need-to-Be
description: An AI agent's accuracy bar comes from money, not a round number: divide the damage of a wrong answer by the saving of a right one, per slice.
dek: Every bar in the document is 80%, and nobody knows why. Here is where the real number comes from — and why a human hold can lower it.
level: Intermediate
keywords: how accurate should an AI agent be, AI accuracy threshold, acceptance criteria for AI, AI agent evaluation threshold, LLM accuracy requirements, human in the loop accuracy, break-even accuracy
updated: 2026-09-23
---

> [!TIP]
> **The answer in one sentence.** An AI agent must be accurate enough that its right answers pay for
> its wrong ones — so for each slice of work, divide the **damage** of a wrong answer by the
> **saving** of a right one to get *N*, and the break-even bar is **N ÷ (N + 1)**: 50% where a mistake
> costs what a success saves, 80% where it costs four times as much, 98% where it costs fifty times —
> unless a person holds the action and cuts the damage.

{{figure:bar_sheet}}

**In this lesson** you'll learn:

- where the accuracy an agent needs actually comes from, and the one-line formula;
- why every slice needs its own bar, and how to cut a feature into slices;
- how a human hold lowers the bar, and when a bar is telling you to redesign.

## Sound familiar?

- Every acceptance bar in the spec is 80%, because 80% sounds rigorous.
- One accuracy number for the whole feature — and the refunds hide inside it.
- The model is at 91%, the target is 98%, and the team has spent a month trying to close the gap with prompts.

Each is a bar that was chosen instead of derived. Derived bars are different for every slice, and one
of them usually says the design needs changing, not the model.

## Where does the bar come from?

From what a right answer saves and what a wrong one costs. If a right answer saves *s* and a wrong one
costs *d*, then at accuracy *a* the agent earns *a × s* and loses *(1 − a) × d* per case. It breaks
even when those are equal, which gives:

> **N = damage ÷ saving**, and **bar = N ÷ (N + 1)**

One wrong case undoes the saving from *N* right ones, so the agent breaks even at *N* right for every
wrong. Anything above the bar is value; anything below it costs more than it saves.

## Set the bar, step by step

### Step 1 · Cut the feature into slices that fail differently

A slice is a group of cases whose mistakes cost about the same. SkyWays — the fictional airline this
playbook follows — cut its rebooking assistant into same-day moves, codeshare rebookings and refunds,
because a wrong same-day suggestion costs a few dollars of an agent's time and a wrong refund costs
the refund.

### Step 2 · Put a saving and a damage on each slice

| Slice | Saving | Damage | N | Bar |
| --- | --- | --- | --- | --- |
| Same-day lookup | $4 | $4 | 1 | **50%** |
| Codeshare rebooking | $9 | $36 | 4 | **80%** |
| Refund, no hold | $12 | $600 | 50 | **98%** |
| Refund, **with a human hold** | $12 | $30 | 2.5 | **71%** |

Damage is not always money — a wrongly refused benefit, a misleading medical summary. Put a number on
it anyway; if you genuinely cannot, that is the finding: the step needs a person regardless of any bar.

### Step 3 · Read the bars for design, not just for testing

The last two rows are the lever. **A hold lowers the damage, so it lowers the bar**: a person checking
refunds before they go out cuts the damage of a wrong one from $600 to $30, and the bar from 98% to
71%. Nothing about the model changed. That is why a human in the loop is a commercial instrument, not
friction — and why a bar above about 95% is usually a design smell: it says the step is too dangerous
to run unheld, and the answer is a hold, not a better prompt.

## Where you'll use it

- **In P1**, before any prompt is written: the bars go into the eight-field spec and are signed at
  the hard gate.
- **When the team is arguing about "accuracy"**: ask which slice, and what a mistake costs in it.
- **When an agent is stuck below a very high bar**: redesign with a hold, and re-derive the bar.

## Why it matters

A bar that is not derived cannot be defended when a regulator, a customer or a finance director asks
why the agent was allowed to launch. A derived bar is a sentence: *it breaks even at 80% on codeshare,
because a wrong one costs four times what a right one saves.* And one bar per feature ships the hard
slice below its bar while the easy one is held back for no reason.

## Try it

A support agent drafts replies that a person always reads before sending (saving $2 a case, damage $1
when a person must rewrite it). It also issues goodwill credits alone (saving $3, damage $45 when one
is issued wrongly). **What bar does each need, and what would you change?**

<details><summary>Show the answer</summary>

**Drafts: 33%. Credits: about 94%.** For drafts N = 1 ÷ 2 = 0.5 and the bar is 0.5 ÷ 1.5 ≈ 33% — the
person reading each draft keeps the damage small. For credits N = 45 ÷ 3 = 15 and the bar is
15 ÷ 16 ≈ 94%, which is close to the design-smell line. The change: put a hold on credits — a person
approves any credit above a threshold — and re-derive; if the hold cuts the damage to $6, N = 2 and
the bar falls to about 67%.

</details>

## Key takeaways

1. The bar comes from money: **N = damage ÷ saving**, **bar = N ÷ (N + 1)**, per slice.
2. **Every slice gets its own bar** — one bar per feature hides the slice that matters.
3. **A hold lowers the damage, so it lowers the bar**; a bar above about 95% means redesign, not re-prompt.

## FAQ

### What accuracy is good enough for an AI agent?

It depends on the slice. Divide what a wrong answer costs by what a right answer saves; the agent
breaks even at N ÷ (N + 1) of that ratio. Low-stakes, easily-corrected work can break even near 50%;
money actions without a human check can need 98% or more.

### Why not just use 80% or 90% as the target?

Because a round number is not connected to anything a mistake costs, so it is either too strict for
the easy slices, which then wait for no reason, or too loose for the dangerous ones, which ship below
the level that pays. It also cannot be defended to anyone who asks where it came from.

### How does human-in-the-loop change the accuracy needed?

A person who checks an action before it takes effect lowers the damage of a wrong answer, and so
lowers the bar. At SkyWays a hold on refunds cut the damage from $600 to $30 and the bar from 98% to
71% — which is often the difference between shipping and never shipping.

### Is a derived bar enough to launch?

No — it is the target. Proving the agent meets it takes a golden set per slice and the lower bound of
the score, not the score itself, followed by a shadow run on live traffic.
[Prove it with a sample](lesson:prove-ai-accuracy).

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The break-even bar N ÷ (N + 1), per slice, and the hold as a lever | **Original** — this playbook | [Formulas](wiki:Formulas-and-Calculators#the-acceptance-bar--working-method) · [Mental Models](wiki:Mental-Models#a-hold-is-a-lever-not-a-brake) |
| Expected-value break-even for a decision under uncertainty | **Borrowed** | Standard decision theory; see Raiffa, H. (1968). *Decision Analysis*. Addison-Wesley |
| The SkyWays slices and figures | **Illustrative** — a fictional airline | [Try the bar calculator](sim:#/toolkit/bar) |
