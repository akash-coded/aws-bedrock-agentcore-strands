---
title: Agentic PDLC Exercises: 12 Problems with Worked Answers
short: Twelve exercises
wiki: Agentic-PDLC-Exercises-with-Answers
description: Twelve agentic AI delivery exercises with worked answers, three per phase: AI-fit, value, gates, bars, chains, bounds, cases, queues, bills, drift, controls.
dek: Reading a formula and using it with a room waiting are different skills. These are the calculations the work actually asks for, in the order it asks.
level: Intermediate
keywords: agentic AI exercises, AI project management exercises, AI product manager interview questions, LLM evaluation practice problems, AI delivery quiz, acceptance bar exercise, confidence interval exercise, AI training problems
updated: 2026-09-24
---

> [!TIP]
> **The set in one sentence.** Twelve problems, three per phase, each a decision the agentic PDLC asks
> for with the arithmetic that settles it: whether work is AI work, what it is worth, which decisions
> halt the build, what the bar is, what chaining costs, whether a score proves a bar, how many cases and
> days proof takes, how long review waits, what the bill will be, when drift fires, and what counts as a
> control. Every answer is worked, and links to the lesson that teaches it.

{{map:agentic-pdlc-exercises}}

**In this lesson** you'll practise:

- the four decisions of P0 and P1 that fix a project's shape and its bar;
- the proof arithmetic of P2 (lower bounds, cases needed, days of evidence, review queues;
- the production arithmetic of P3) the bill, drift and what counts as a control.

## Sound familiar?

- You have read that a score needs a lower bound, and could not say whether 45 out of 50 proves 85%.
- The formula looked obvious in the lesson and slipped away in the meeting.
- Most AI courses test what you remember; the work asks you to calculate.

These twelve are the calculations the work asks for, each small enough to do on a phone.

## How should you use these exercises?

**Commit to an answer before you open the worked one.** Each takes two to five minutes with a
calculator, and each links to the lesson that teaches it. The numbers are hypothetical, chosen to make one
point each; the lower bounds use 1.96, with the Wilson bound under about 100 cases, as the rest of this
tutorial does.

## P0 · Frame

### Exercise 1 · AI work, or a rule?

Three candidate features: **(a)** route each insurance claim to one of four teams by the product code on
the form; **(b)** draft replies to 800 complaints a day, reviewed before sending; **(c)** approve wire
transfers above $10,000. **Which is AI work?**

<details><summary>Show the answer</summary>

**Only (b).** (a) has no judgement call, two competent people would route the same code the same way,
so it is a rule. (b) has judgement, volume and a recoverable mistake, because a draft is reviewed before
it goes. (c) may involve judgement, but a wrong transfer is not recoverable, so at most it is assisted:
the model can prepare the case, and a named person approves every transfer.

</details>

Learn it: [Is it AI work at all?](lesson:p0-frame#step-2--decide-whether-it-is-ai-at-all)

### Exercise 2 · The value line

300 cases a day. The agent saves 12 minutes a case, at a loaded $0.80 a minute. Running it costs $0.40 a
case, and 30% of cases are reviewed, for 4 minutes each. **What is the net saving a day, and what is it
if the review share falls to 10%?**

<details><summary>Show the answer</summary>

**$2,472 a day, rising to $2,664.** Gross: 300 × 12 × $0.80 = $2,880. Run cost: 300 × $0.40 = $120.
Review: 300 × 30% × 4 × $0.80 = $288. Net: $2,880 − $120 − $288 = $2,472. At 10% reviewed the review
line is $96, so the net is $2,664, which is why the review share belongs in the value line from day one.

</details>

Learn it: [Size the value, net of running and checking it](lesson:p0-frame#step-3--size-the-value-net-of-running-and-checking-it)

### Exercise 3 · Hard or soft?

Two decisions are open at the end of P1. **(a)** Which agent framework to use: the code talks to it
through an interface layer, and an owner will decide by the 20th. **(b)** Whether the refund tool may pay
without an approver: nobody has decided, and the refund bolt starts next week. **Which halts the build?**

<details><summary>Show the answer</summary>

**(b) is hard; (a) is soft.** Ask the four questions (reversible cheaply, a placeholder, an owner and a
date, downstream survives a change) and one "no" makes it hard. (a) passes all four. (b) fails the
first three: the decision cannot be cheaply reversed once refunds are being paid, "the model behaves
sensibly" is not a placeholder, and nobody owns it with a date. Settle it before the gate.

</details>

Learn it: [The hard gate](lesson:the-hard-gate)

## P1 · Design and Spec

### Exercise 4 · Derive the bar

A wrong answer costs $45 to put right; a right one saves $5. **What is the bar, and what is it if a
person checks each answer before it lands, so that a mistake costs only the $15 of their time?**

<details><summary>Show the answer</summary>

**90%, falling to 75%.** The bar is damage ÷ (damage + saving): 45 ÷ 50 = 90%. With the check, 15 ÷ 20 =
75%. A human hold on the risky step lowers the damage, and therefore the bar, which is how a feature
ships safely at a score it could never have reached unaided.

</details>

Learn it: [How accurate must an AI agent be?](lesson:how-accurate-must-an-ai-agent-be)

### Exercise 5 · Chained steps

A plan chains six steps, each right 95% of the time. **How often is the whole chain right, and which
helps more: raising one step to 99%, or replacing one step with exact code?**

<details><summary>Show the answer</summary>

**73.5%, and replacing a step wins.** 0.95⁶ = 0.735. Raising one step to 99% gives 0.95⁵ × 0.99 = 0.766;
replacing it with code that is right every time gives 0.95⁵ = 0.774. Every step that can be exact should
be, before anyone tunes a prompt.

</details>

Learn it: [Chained steps multiply](lesson:p2-build-and-prove#step-4--put-an-independent-checker-after-the-risky-steps)

### Exercise 6 · How many agents?

A design gives each of seven departments its own agent. **How many possible hand-offs are there, and what
should each extra agent have to earn?**

<details><summary>Show the answer</summary>

**Twenty-one.** Seven agents have 7 × 6 ÷ 2 = 21 possible pairings, and each is a place where context is
lost and a limit must hold. Start with one agent and tools; add an agent only for a named limit (a
context overflow, or parallel work a tool cannot express) and give its hand-off a named limit of its own.

</details>

Learn it: [Decide how many agents](lesson:p1-design-and-spec#step-5--decide-how-many-agents-and-record-only-the-decisions-that-earn-it)

## P2 · Build and Prove

### Exercise 7 · Which slice is proven?

Both slices have a bar of 85%. Slice A scores 184 of 200 (92%); slice B scores 45 of 50 (90%). **Which
has proven its bar?**

<details><summary>Show the answer</summary>

**Only A.** A: 0.92 − 1.96 × √(0.92 × 0.08 ÷ 200) = 0.882, above 85%. B has under 100 cases, so use the
Wilson bound: 78.6%, below 85%: its score is five points above the bar and proves nothing yet. A score
without its sample size has said nothing.

</details>

Learn it: [Prove the bar](lesson:prove-ai-accuracy)

### Exercise 8 · Cases, then days

A slice scores 86% against a bar of 83%. It is 15% of 200 cases a day. **How many cases does proof need,
and how many days of traffic is that?**

<details><summary>Show the answer</summary>

**About 514 cases, or 18 days.** Cases needed = 1.96² × 0.86 × 0.14 ÷ 0.03² ≈ 514. The slice sees
15% × 200 = 30 cases a day, and 514 ÷ 30 ≈ 17.1, so 18 days. A score closer to its bar needs many more
cases, because the gap is squared.

</details>

Learn it: [Cut over and widen on evidence](lesson:shadow-mode-and-cutover#step-4--cut-over-at-5-per-action-and-widen-on-evidence)

### Exercise 9 · The review queue

Twelve changes are waiting: three touch money (R4), five are other writes (R2 to R3) and four are read-only
(R1). Reviewers complete five review slots a day. **How long is the queue with two readers on everything,
and with readers routed by band?**

<details><summary>Show the answer</summary>

**4.8 days, falling to 2.2.** Two readers each: 24 slots ÷ 5 = 4.8 days. By band (two readers for R4,
one for R2 to R3, the harness alone for R1) 3 × 2 + 5 × 1 + 4 × 0 = 11 slots ÷ 5 = 2.2 days, with the money
changes read first and by more people than before.

</details>

Learn it: [Review AI-generated code by risk](lesson:review-ai-generated-code)

## P3 · Run and Learn

### Exercise 10 · The bill

The estimate was $2,000 a month. The per-call log shows context resent on every turn (×1.5, a day to
fix), easy calls on the expensive model (×1.4, half a day), a cache that stopped hitting (×1.2, a day)
and retries with no cap (×1.3, two days). **What is the bill, and in what order do you fix it?**

<details><summary>Show the answer</summary>

**About $6,550; fix the routing, then the context, then the cache, then the breaker.** 1.5 × 1.4 × 1.2 ×
1.3 = 3.28, and $2,000 × 3.28 ≈ $6,550. Priority = (factor − 1) ÷ days: routing 0.8, context 0.5, cache
0.2, breaker 0.15. The breaker comes last and still matters: it is the fix that makes a runaway impossible.

</details>

Learn it: [Why the bill is 4×](lesson:ai-agent-costs)

### Exercise 11 · Drift

The share of cases the agent escalates to a person starts at 18% and rises 1.5 points a week. The weekly
alert fires on a change above 3 points; the baseline alert fires 5 points from the frozen baseline.
**Which fires, in which week, and what should it do?**

<details><summary>Show the answer</summary>

**The baseline alert, in week 4.** The weekly change is 1.5 points, so the weekly alert never fires. The
level reaches 22.5% in week 3 (4.5 points) and 24% in week 4 (6 points), crossing 5. The breach should
re-open the release gate by itself, not open a ticket someone may read.

</details>

Learn it: [Two thresholds, not one](lesson:ai-drift-monitoring#step-3--set-two-thresholds-not-one)

### Exercise 12 · A control, or not?

An agent emailed a customer's details to the wrong address. The postmortem proposes three actions:
**(a)** retrain the support lead who approved the prompt; **(b)** add "only send to verified addresses" to
the system prompt; **(c)** make the send tool require a verified-address token in its signature. **Which
is a control?**

<details><summary>Show the answer</summary>

**Only (c).** (a) names a person, which changes nothing the system does. (b) is a request, and a model can
be talked past a request. (c) is enforced: the tool cannot send without the token, whatever the model is
told. Ask which enforced control would have made the incident impossible, and accept only code.

</details>

Learn it: [AI incident postmortems](lesson:ai-incident-postmortem)

## Key takeaways

1. **Twelve problems, one per decision** the agentic PDLC asks for, three per phase.
2. **A few formulas carry most of it**: the bar, the lower bound, cases needed, the queue, the multiplier.
3. **Commit to an answer first**, then open the worked one, and the lesson behind it.

## FAQ

### What maths do these exercises need?

Arithmetic, percentages and one square root. The only formulas are the bar, a lower bound, the cases
needed, days of evidence, a queue and a product of factors, each stated in the answer.

### Can I use these exercises for training?

Yes. They work as a team exercise: give each person one phase, ask for an answer in two minutes, then
compare working. Credit the tutorial when you reuse them.

### Where can I practise with my own numbers?

The simulator's toolkit has a calculator for most of them (the bar, golden-set confidence, the review
queue, cut-over evidence and bill leaks) each prefilled and editable.

### Where can I find more exercises?

The playbook's wiki has thirty-one more in [Exercises and answers](wiki:Exercises-and-Answers), in
sets from framing to operations, each worked in full. The formulas they use are collected in
[Formulas and calculators](wiki:Formulas-and-Calculators).

### Why use 1.96 rather than 1.645?

1.96 is the stricter convention, and the one this tutorial, the wiki and the simulator's calculator all
use by default. A one-sided 1.645 asks the same question with a lower demand for evidence. Either is
defensible if it is fixed before anyone sees a score and written on the bar sheet.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Work all twelve before a customer engagement. They are the calculations the first month will ask of you. | Ask a model to rewrite each exercise with the customer's own numbers. |
| **A product manager or FDPM** | Use exercises 2, 4, 7 and 10 in interview loops for AI PMs, and ask for the working aloud. | Have a model generate variants with different numbers, with separate answer keys. |
| **A GenAI or agentic AI engineer** | Turn exercises 5, 8 and 9 into code: a chain calculator, a cases-needed function, a queue estimator. | Ask a coding agent to write them as tested functions in the team's utilities. |

**Across the enterprise.** Use the set as a shared baseline in training. A team that can do this arithmetic
argues about assumptions instead of definitions, which is the argument worth having.

**The ten-minute workflow.** Endless practice from one set:

```text
Here are twelve exercises with their answers: <paste the lesson>. Write a variant of each with different
numbers and one twist — a human hold, a smaller sample, a slice that falls while the average rises. Keep
the answers separate, with the working shown.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The twelve exercises | **Original**: this tutorial | Numbers hypothetical |
| The bar, the value line, the four gate questions, fix order | **Original**: this playbook | [Frameworks](site:frameworks/) |
| The Wilson score interval | **Borrowed** | Wilson, E. B. (1927). *JASA* 22(158) |
| Queue time from slots and throughput | **Borrowed** | Little, J. D. C. (1961). *Operations Research* 9(3) |
| One-way and two-way doors | **Borrowed** | Bezos, J. (2015). Letter to shareholders |
