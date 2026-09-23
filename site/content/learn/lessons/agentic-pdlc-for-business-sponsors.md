---
title: The Agentic PDLC for Business Sponsors: Ask for Two Numbers
short: For business sponsors
wiki: Agentic-PDLC-for-Business-Sponsors
description: What a business sponsor owns in an agentic AI programme: funding past cycle one, the autonomy ceiling, what counts as evidence, and three reports to insist on.
dek: You are the only person on the programme with no delivery deadline — which is exactly why the governance loop, and the stop decision, are yours.
level: Beginner
keywords: AI project sponsor, executive sponsor AI, AI business case, how to fund AI projects, AI ROI reporting, AI steering committee, AI programme governance, business owner AI agent
updated: 2026-09-23
---

> [!TIP]
> **The role in one sentence.** The business sponsor of an agentic programme owns whether it is funded
> past its first cycle, the autonomy ceiling for the organisation, what will be accepted as evidence,
> and the governance loop — and exercises all four by insisting on three reports: **two numbers** every
> cycle, a **drift readout** every week, and an **incident brief** after every incident.

{{figure:two_numbers}}

**In this lesson** you'll learn:

- what a sponsor owns, what a sponsor shapes, and what a sponsor must not touch;
- the three reports to receive, and what their absence tells you;
- what to do on the two days that actually test the role: the bill, and the incident.

## Sound familiar?

- The last three reviews had a screen share and no interval.
- The first you heard of the cost was from finance, at its worst.
- Every postmortem ends with a list of actions, and the same thing happens again.

The sponsor's power is not in the reviews; it is in what the reviews are required to contain.

## What changes for a sponsor?

Most of the job is familiar — backing a programme, setting risk appetite, reading a business case,
stopping a programme that is not working. What a model in the middle changes is **what counts as
evidence** for each of those:

| You have always done this | What changes |
| --- | --- |
| Backing a programme, and stopping one | The stop decision rests on evidence you specified in advance — a demo is not evidence |
| Setting risk appetite | It becomes an autonomy level **per action**, not one setting for "the AI" |
| Reading a business case | The running cost moves with behaviour, not volume — a bill can multiply on flat traffic |
| Steering and status | Two numbers against a dated baseline, with the review hours visible |
| Asking whether it works | A lower bound per slice, because a score without an interval has said nothing |

## Your part, step by step

### Step 1 · Know what is yours, what you shape, and what you must not touch

| You own | You shape | You must not touch |
| --- | --- | --- |
| Funding past cycle one | The roadmap — the product manager's | The verdict on a slice |
| The organisation's autonomy ceiling | The architecture — the architect's | Which slice ships first |
| What you will accept as evidence | The bar — which is derived, not chosen | The gate decisions |
| The governance loop, and the name on it | | The design |

The temptation is to reach into delivery when a number disappoints. It never works, and it costs the
role its point: an independent reading of whether the programme is working.

### Step 2 · Insist on three reports

| Report | Cadence | If it is missing |
| --- | --- | --- |
| **Two numbers** — the saving beside the spend, with review hours and re-runs | Every cycle | You will hear the cost from finance instead |
| **Drift readout** — the output mix against its thresholds | Weekly | Behaviour will change with no deploy and no alert |
| **Incident brief** — the missing control, the fix, the next P0 | On every incident | Postmortems will end in a name rather than a control |

### Step 3 · Fund on trajectory, not on promise

A first cycle that saves time and costs more is normal. Fund past it on the trajectory: the review load
falling, and the re-run count falling with it. At SkyWays — this playbook's fictional airline — day
ninety's report showed **43% fewer person-days per story** and **$310 of tokens per story**, with review
hours up and the reason they would fall. The programme continued because both numbers came from the team.

### Step 4 · When the bill arrives, ask which signature

A bill several times its estimate on flat traffic is normal in early cycles, and it is a **design**
question. Ask which of four signatures the per-call log shows — tokens per call up, tier mix moved to the
expensive model, cache hit ratio down, retries up — and which decision record allowed it. A spending
freeze stops the work and teaches nothing. [Why the bill is 4×](lesson:ai-agent-costs)

### Step 5 · When the incident arrives, ask which control

Ask one question — *which enforced control would have made this impossible?* — and do not accept a name,
a reminder or a prompt edit as the answer. [AI incident postmortems](lesson:ai-incident-postmortem)

## Where you'll use it

- **At the start**: name who owns governance — if the answer is "we all do", nobody does.
- **Every cycle**: the two numbers, on one line, from the team.
- **On the two hard days**: the bill and the incident, each with its one question.

## Why it matters

Programmes are cancelled on the number that was hidden — the one the sponsor saw for the first time when
it was worst. The sponsor's three reports make every number arrive early, from the team, with its pair,
which is what lets a programme survive a first cycle that costs more than it saves.

## Try it

Your programme's quarterly update shows a single accuracy figure of 91%, a demo, and "costs within
budget". **What do you ask for before the next funding decision?**

<details><summary>Show the answer</summary>

**The two numbers, per-slice evidence, and the drift readout.** Ask for the saving and the spend on one
line against the baseline, with review hours and re-runs beside them; the accuracy per slice, each with
its sample size and lower bound, against a derived bar; and the weekly output mix since launch. "Within
budget" is not a cost per case, 91% is not proof, and a demo is not evidence — decide on the three reports,
not on the update.

</details>

## Key takeaways

1. The sponsor owns **funding past cycle one, the autonomy ceiling, what counts as evidence, and governance**.
2. **Three reports**: two numbers every cycle, drift weekly, an incident brief on every incident.
3. On the two hard days, ask **which signature** and **which control** — never for a freeze or a name.

## FAQ

### What does a sponsor do in an AI project?

Decides whether the programme is funded past its first cycle, sets the organisation's ceiling on what
the agent may do without a person, specifies what will count as evidence, and owns governance — the one
loop no delivery role is accountable for — by insisting on three regular reports.

### How should a sponsor measure an AI programme's ROI?

With two numbers reported together every cycle: the saving against a dated baseline, and the full cost
including tokens, review time and re-runs. Fund past the first cycle on the trajectory of the review load
and re-run count, not on a promise.

### What should an AI steering committee ask?

Which of these are rules? What may the agent do without a person, and who decided? What are the two
numbers? What maturity level are we, and what is the next control? Those four questions, asked every
cycle, take about ten minutes.

### Should a sponsor approve AI releases?

No. Release, behaviour and expansion decisions belong to the product manager and QA, on evidence. The
sponsor specifies what evidence is acceptable and owns the governance loop — not the individual gates.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Give the customer's sponsor the two numbers every cycle, from you, before anyone asks. It is what renews an engagement. | Ask a model to draft the sponsor update from the cycle data in five lines. |
| **A product manager or FDPM** | Bring the sponsor decisions, not status: the autonomy ceiling, what counts as evidence, funding past cycle one. | Have a model turn your status report into the decisions only the sponsor can make, with options. |
| **A GenAI or agentic AI engineer** | Make the sponsor's three reports automatic: the two-number line, the drift readout and the incident brief. | Ask a coding agent for the scheduled job that assembles all three. |

**Across the enterprise.** Every sponsor in the portfolio receives the same three reports in the same
format, so funding decisions compare like with like.

**The ten-minute workflow.** A sponsor update in the only shape that works:

```text
Here is our programme update: <paste>. Rewrite it for the business sponsor as: the two numbers on one
line (the saving beside the spend, with review hours and re-runs), the decisions only the sponsor can
make this cycle with options and our recommendation, and one risk. Keep it under 200 words.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The sponsor's owns, shapes and must-not-touch; the three reports | **Original** — this playbook | [Role: Sponsor](wiki:Role-Sponsor) |
| The four questions and the two-number report | **Original** — this playbook | [For leadership](site:protocol/) |
| Measures reported beside their side effects | **Borrowed** | Grove, A. (1983). *High Output Management*. Random House |
| The SkyWays figures | **Illustrative** — a fictional airline | [The simulator](sim:#/) |
