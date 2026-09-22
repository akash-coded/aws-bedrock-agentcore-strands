# How to review by risk band

Nine pull requests, a four-day queue, and two reviewers who cannot read any faster. Adding a third
reviewer takes three months to hire and the agent will produce more changes long before then.

**The policy is the bottleneck, not the people.** It treats nine changes as equally dangerous.

Run it live:
[simulation](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/simulations/review) ·
[queue calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/queue).

---

## Read the queue with Little's law

> **queue time = review slots needed ÷ review slots available per day**

| | Before | After routing |
| --- | --- | --- |
| Changes waiting | 9 | 9 |
| Policy | Two senior reviewers on everything | Two / one / none, by band |
| Slots needed | **18** | **7** |
| Slots available per day | 4.5 | 4.5 |
| **Queue time** | **4.0 days** | **1.6 days** |

Capacity is fixed by people. The only lever you actually control is **slots needed**, and that is a
policy variable.

---

## The band follows what the change touches

Size measures typing. It does not measure danger.

| Change | Size | Touches | Band | Readers |
| --- | --- | --- | --- | --- |
| A · rewrite 400 lines of help text | Large | Nothing that acts | R1 | Harness, plus one at the end |
| B · alter 3 lines in the refund tool's cap check | **Tiny** | `issue_refund` | **R4/R5** | **Two, every time** |
| C · add a read-only search filter | Small | A read tool | R2 | Harness alone |

> **A change inherits the band of whatever it touches.** Three lines in a refund cap is the highest
> band there is; four hundred lines of help text cannot move money.

---

## Who assigns the band

Not the author. Every author believes their own change is low risk, and within a month nine changes in
ten are labelled R1.

**A path rule in the repository, mapped from the authority budget.** The files behind each tool carry
that tool's band, and the repository applies it automatically.

```yaml
# .github/review-bands.yml — generated from the authority budget, reviewed like code
R5: ["src/tools/identity/**"]
R4: ["src/tools/refund/**", "src/tools/payment/**", "config/caps.yaml"]
R3: ["src/tools/rebook/**"]
R2: ["src/tools/search/**", "src/api/**"]
R1: ["docs/**", "content/**"]
```

Nobody classifies their own work, and the argument moves from the pull request — where it is
re-litigated every time — to the authority budget, where it is settled once.

---

## The harness-only lane

Four of the nine changes would merge with no person reading them. That is either the best thing in
your process or the worst, and which one depends entirely on a number you have to keep.

> **A lane with no reader is exactly as safe as its harness.**

So **count the escapes**: defects that reached production through the harness-only lane, reviewed
every week. Without that count, an unreviewed lane is just unreviewed merging with a better name —
and the industry numbers on that are not encouraging: Faros AI reported 31% more pull requests
merging with no review at all in 2026, alongside a large rise in the time a reviewed PR sits waiting.

The right posture: open the lane, keep the count, and close the lane the moment escapes appear.

---

## Measure the policy, or it will be repealed

Three numbers, together. Any one alone can be argued with.

| Number | Before | After |
| --- | --- | --- |
| Review slots needed | 18 | **7** |
| Days in the queue | 4.0 | **1.6** |
| Escapes from the harness-only lane | – | **0** |

"The reviewers feel less pressure" is true and cannot be compared with anything. Next quarter nobody
will remember why the policy exists. These three can be compared, and they are what keeps the policy
alive.

---

## Why this matters more with agents in the loop

The review queue is where agentic delivery gets stuck, and the published numbers are consistent about
it:

| Finding | Source |
| --- | --- |
| Median time a pull request sits in review rose sharply in 2026 | Faros AI, 22,000 developers |
| 31% more pull requests merging with no review at all | Faros AI, 2026 |
| 98% more pull requests merged per developer, while org-level delivery stayed flat | Faros AI, 2025, 10,000 developers |
| 30% still place little or no trust in AI-generated code | DORA 2025, ~5,000 respondents |

The last two lines are the same story from both ends. **More changes are produced; the same number of
people read them.** Routing by risk is how you spend the reading you have on the changes that can hurt
you.

---

## Try it

**Exercise.** Take last week's merged pull requests. For each, write the band of the **most dangerous
tool the change touches** — not the size of the diff.

<details>
<summary>What you will find, and what to do</summary>

Most teams find the distribution is roughly 10% R4/R5, 30% R2/R3 and 60% R1 — while the *review
policy* treats all of them as R3 or above. That gap is your queue time, and it is free to reclaim.

You will probably also find one R4 change that went through on a single quick approval because it was
three lines. That is the finding worth taking to the team, because it is the exact shape of the
incident that follows: a small change to a money path, reviewed as a small change.

Then write the path rule. It is an afternoon, it is generated from an artefact you should already
have, and it ends the per-pull-request argument permanently.
</details>

---

**Next:** [Gates and Governance](Gates-and-Governance) · [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts)
· [Role: Engineering lead](Role-Engineering-Lead) · [Formulas and Calculators](Formulas-and-Calculators)
