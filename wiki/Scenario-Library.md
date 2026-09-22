# Scenario library

Thirteen episodes from SkyWays, and twelve more from other industries.

The airline case is deliberately one case, followed all the way through. This page is the other half:
the same playbook applied to healthcare, banking, insurance, retail, logistics, the public sector and
an internal helpdesk — because the test of a method is whether it survives a change of domain.

Use these for workshops, interview practice, or as the first hour of a new engagement.

---

## Part one · SkyWays, ninety days

One airline, one rebooking assistant for disrupted passengers, four people: **Priya** owns the
product, **Arjun** the architecture, **Sam** the engineering, **Maya** the quality.

Each episode opens on a moment with a number in it and closes one loop.

| Day | Episode | Who | Closes | The number |
| --- | --- | --- | --- | --- |
| 1 | Two discovery meetings | Arjun | requirements | **31** requirements from six people, four of them duplicates |
| 4 | The requirements email that keeps the duplicates | Arjun | requirements | All **31** lines kept, each credited |
| 6 | Constraints, and the NFRs they reshape | Arjun | requirements | One constraint — **$400** — reshapes three of nine NFRs |
| 9 | The NFR workshop | Arjun | requirements | **9** ratified NFRs, **3** pulling against each other |
| 12 | The first ADRs, at the trade-off points | Arjun | decision | **2** written, **1** scheduled. Not one more |
| 15 | From a thirty-page brief to eight fields | Priya | spec | **30 pages → 8 fields**; five were never decided |
| 20 | Build, buy or borrow the framework | Arjun | decision | **6** weighted criteria; the fastest start loses on the door |
| 30 | The first bolt ships by four in the afternoon | Sam | delivery | A walking skeleton, **day 1** |
| 45 | Eighty-two point four against a bar of eighty | Maya | trust | **82.4%** vs **80%** — and the lower bound says not yet |
| 60 | Nine pull requests and a four-day queue | Sam | delivery | **18** slots needed, **4.5** a day available |
| 75 | A bill 4.4 times the estimate, with flat traffic | Arjun | cost | **1.6 × 1.5 × 1.3 × 1.41 = 4.40** |
| 82 | A refund of $2,000 that was not owed | Maya | incident | **5** layers claimed, **0** enforced |
| 90 | Both numbers, in front of the steering committee | Priya | governance | **−43%** person-days and **$310** a story |

Read them in order:
[the story](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/story).

---

## Part two · the same playbook, twelve other cases

Each one is a single decision with a trap attached. They are written to be argued with.

---

### 1 · Hospital discharge summaries

**The ask.** Draft the discharge summary from the notes, so clinicians stop writing them at 9pm.

**AI-fit.** Judgement: yes. Volume: high. **Recoverable: no** — a wrong medication line can reach a
patient. So: *assisted and gated*, never autonomous. The clinician signs every one.

**The decisive move.** Derive the bar **with the hold in place**. Unheld, the damage per wrong summary
is unbounded and the bar is effectively unreachable. With a clinician confirming before the summary
leaves the system, the damage is "a few minutes of correction", and a bar in the seventies is both
honest and shippable.

**The trap.** Treating "a clinician reviews it" as a process note rather than as a **control that
changes the arithmetic**. Written down, it is the reason the project is viable. Left implicit, someone
will eventually propose removing it to save time.

→ [How to Prove the Bar](How-to-Prove-the-Bar)

---

### 2 · Insurance claims triage

**The ask.** Read the claim, classify it, and compute the indicative payout.

**The decisive move.** Split the step. Classification is best-guess and measured. **The payout is
exact and belongs in code** — a function the model calls and reads, never a number the model produces.

**The trap.** The step looks like one step, so it gets built as one prompt, and the prompt contains
the word "exactly". Then it returns $80 where the policy says $62, fluently, with no error, and the
first person to notice is the claimant.

Grep for *calculate*, *compute*, *total*, *sum*. Every hit is a function waiting to exist.

→ [Role: Solution architect](Role-Solution-Architect)

---

### 3 · Bank KYC document reader

**The ask.** Extract identity details from uploaded documents and flag mismatches.

**The decisive move.** Every uploaded document is **untrusted text**, tagged at the ingest layer. The
identity-change tool is **R5 and not delegated at all**; the agent may flag, never amend.

**The trap.** Injection through a document rather than a chat box. Instructions in white text inside
a PDF, or in a field a previous system wrote. The defence is not a better prompt — it is that the
identity tool cannot be called by the agent, whatever the agent has been convinced of.

→ [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary)

---

### 4 · Retail returns agent

**The ask.** Approve returns, arrange collection, and waive the restocking fee where the policy allows.

**The decisive move.** Three actions, three autonomy levels. Approving a return within policy is
reversible: the agent acts. Arranging collection costs money but is small and bounded: monitored.
**Waiving the fee is money** — R4, with a cap in the tool signature.

**The trap.** Setting autonomy "for the returns agent" as one level, which forces the whole product to
the strictness of its riskiest action, or — worse — to the looseness of its safest.

→ [Decision Trees](Decision-Trees) · [Role: Product manager](Role-Product-Manager)

---

### 5 · Internal IT helpdesk

**The ask.** Answer password, VPN and printer questions.

**AI-fit.** Judgement: mild. Volume: very high. Recoverable: yes, trivially.

**The decisive move.** This is the case where the honest bar is genuinely around **50%**, no hold is
needed, and most of the ceremony in this playbook is **wrong**. Damage per wrong answer is one minute
and a human hand-off; saving per right answer is about the same. `bar = N ÷ (N+1)` with N = 1.

**The trap.** Applying the airline's apparatus to it. Eleven gates and a shadow run for a printer
question is how a method gets a reputation for slowing teams down — and that reputation is then used
to skip the gates on the refund tool, where they mattered.

**Depth is decided per change.** This one is shallow.

→ [The Agentic PDLC](The-Agentic-PDLC)

---

### 6 · Legal contract redlining

**The ask.** Mark risky clauses and propose alternative wording.

**The decisive move.** The checker must be **independent**. A model reviewing its own redline shares
its own blind spots: it proposed the clause, and it will tell you the clause is fine.

Different model, or a fresh context with an adversarial brief — "find what is wrong with this
redline" — given the constraints and the output only, never the drafter's reasoning.

**The trap.** "We added a review step and quality did not improve." The step was the drafter grading
itself.

→ [Role: QA lead](Role-QA-Lead)

---

### 7 · Logistics re-routing

**The ask.** When a shipment is disrupted, find an alternative route, re-book the legs, notify the
customer and update the ledger.

**The decisive move.** Count the chain before promising anything. Six best-guess steps, each measured
at 92%, is **0.92⁶ = 0.61** end to end. Right about three times in five, and failing fluently.

Shorten the chain first — two of the six are usually exact work that crept into a prompt — then place
checkers after the steps that are costly and easy to miss.

**The trap.** Averaging. "Each step is 92%, so the flow is about 92%." Multiply, never average.

→ [Formulas and Calculators](Formulas-and-Calculators)

---

### 8 · Public-sector benefits eligibility

**The ask.** Decide whether an applicant qualifies.

**AI-fit.** Judgement: **no** — eligibility is a published rule set. Volume: high. Recoverable: no,
and legally appealable.

**The decisive move.** Say the unpopular thing: **this is a rule, and code does it.** The model's
legitimate job is the surrounding work — reading unstructured evidence, drafting the explanation,
flagging missing documents — never the determination itself.

**The trap.** An agent-first directive from above. The AI-fit record is the artefact that lets you
say no with evidence rather than as an opinion, and it is why the record exists at all.

→ [Role: Sponsor](Role-Sponsor)

---

### 9 · Supplier pricing agent, six months in

**The ask.** Nothing. It has been running fine since March.

**What happened.** A supplier changed their catalogue format. The agent quietly shifted from quoting
contract prices to quoting list prices on about a fifth of lines. No deploy, no error, no alert.
Finance found it in a quarterly reconciliation.

**The decisive move.** A **drift KPI**: the output mix charted weekly, with an alert at 5% week over
week, and a rule that a drift alert **re-opens the release gate**.

**The trap.** Believing that "no code changed" means "nothing changed". A probabilistic system changes
behaviour when the world shifts under it. This is the failure mode with no error message, and the only
defence is watching the mix.

→ [The Eight Loops](The-Eight-Loops#trust) · [Role: Product manager](Role-Product-Manager)

---

### 10 · Marketing copy at scale

**The ask.** Generate 40,000 product descriptions, refreshed monthly.

**The decisive move.** Two cost levers, both documented. **Batch** the run — nobody is waiting for it,
and batch is about half the on-demand rate. **Cache** the brand guidelines, tone rules and schema as
a stable prefix: 40,000 reads at 0.1× against one write at 1.25×.

**The trap.** Putting the product's details first in the prompt "because that is the important part".
The cache matches an exact prefix, so no two calls share one, and the hit ratio is zero. The bill
arrives anyway, and the caching line item shows it was enabled.

→ [How to Control the Token Bill](How-to-Control-the-Token-Bill)

---

### 11 · Manufacturing maintenance scheduler

**The ask.** Predict which machines need service, order parts, and book engineers.

**The decisive move.** Someone will propose one agent per plant. Ask the question: **what named limit
justifies each hand-off?** Four plants is six possible hand-offs; ten plants is forty-five. The
per-plant work is *parallelism*, which is a property of a fan-out tool, not of an agent count.

One agent, a fan-out tool across plants, exact code for the reorder thresholds, and a gate on ordering
parts because that is money.

**The trap.** Mistaking "these things happen in parallel" for "these need separate agents".

→ [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper)

---

### 12 · Telecoms churn-save offers

**The ask.** When a customer calls to cancel, offer a retention discount.

**The decisive move.** The discount is money leaving the business, so the cap lives **in the tool
signature**, not in the prompt, and anything above it needs a named approver. The agent may reason
about the policy; it cannot exceed the parameter.

**The trap.** This one is subtle and common: the cap is expressed as a *percentage* in the prompt and
as an *absolute* in the tool, and they disagree on high-value accounts. Two rules that both look
enforced, disagreeing exactly where the money is.

One source of truth, in config, reviewed like code, and a test for the boundary case.

→ [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary)

---

## Using these in a workshop

| Time you have | Run this |
| --- | --- |
| 20 minutes | One scenario. Ask the room for the AI-fit verdict and the autonomy level, then reveal |
| 60 minutes | Three scenarios from three domains, same three questions each. The pattern is the lesson |
| Half a day | The SkyWays episodes in order, with the [simulations](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/simulations/master) at days 9, 20, 75 and 82 |
| A full day | The above, plus each participant writing the paper agent for their **own** product |

The single most useful question in all of them, asked before anything else: **"which of these is
actually a rule?"**

---

## Write your own

A scenario earns its place if it has all four:

1. **A number in the opening line.** "31 requirements", "4.4 times the estimate". Without one, the
   discussion stays abstract.
2. **A decision with a defensible wrong answer.** If one option is obviously right, there is nothing
   to learn.
3. **A trap that a competent person would fall into.** Not carelessness — a sensible decision that
   turns out badly.
4. **A named artefact at the end.** What does the room leave with?

Post new ones in
[Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101) and good
ones will be added here with credit.

---

**Next:** [Exercises and Answers](Exercises-and-Answers) · [Decision Trees](Decision-Trees) ·
[Anti-Patterns](Anti-Patterns) · [The Agentic PDLC](The-Agentic-PDLC)
