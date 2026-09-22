# How to choose: build, buy or borrow

The agent framework decision, as a weighted matrix, a three-year cost and a decision record. Five
moves. The interesting number is never the licence.

Run it live:
[simulation](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/simulations/bvb) ·
[matrix tool](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/toolkit/bvb).

---

## 1 · Frame the decision

Get the scope and the horizon right before anything else, because both are usually set too small.

| Framing | Verdict |
| --- | --- |
| "Which option is cheapest this quarter?" | Cost is one criterion of six, and a quarter is the wrong horizon. This is how portability is lost without anyone deciding to lose it |
| **"The framework for every agent in this product, over three years, including the cost of leaving"** | One decision for the whole product, a three-year horizon, and an honest look at the exit |

---

## 2 · Criteria and weights

Six criteria. The weights come from the ratified NFRs and the utility trees, so they are already
agreed — you are not inventing them here.

| Criterion | Weight for a regulated airline with a small team |
| --- | --- |
| Portability | **3** |
| Team skills | **3** |
| Security | **3** |
| Cost | 2 |
| Velocity | 2 |
| Vendor support | 1 |

Equal weights claim the team has no priorities, which is never true. If you cannot justify a weight,
go back to the utility trees; that is what they are for.

Weighting **team skills** at 3 is not sentiment. It is Conway's law: a design the team cannot operate
is a design that will be worked around.

---

## 3 · Rate the options

> **score = Σ weight × rating**, each option rated 1 to 3 per criterion.

Rate the matrix **before** anyone states a preference. A preference with no matrix behind it is the
decision that gets argued again at every incident.

For SkyWays the weighted totals come out close: **borrow** highest, **build** next, **buy** last, with
only four points between first and last.

That closeness is the finding, not a disappointment. When the spread is small, the matrix has told you
the criteria do not separate the options — so the tie is broken by something else.

**The flip test:** how far would one weight have to move before the winner changes? If a single point
on one criterion flips the result, say so in the record. It tells the next reader how firm the
decision is.

---

## 4 · Three-year cost, and the door

Two numbers that do not appear on any vendor page.

**Count the people, not just the licence.**

| Option | Licence, 3 years | People, 3 years | Total |
| --- | --- | --- | --- |
| Buy | higher | lower | **$360,000** |
| Borrow | lower | higher | **$360,000** |
| Build | none | much higher | **~3×** |

Buy and borrow tie once the people are counted. The licence was the small number all along.

**Then look at the door.** A decision is a **two-way door** if it can be reversed cheaply and a
**one-way door** if it cannot.

| Option | The door |
| --- | --- |
| Borrow, behind an interface layer | **Two-way.** Two weeks now to build the interface; a swap is then weeks, not quarters |
| Buy | **One-way-ish.** The exit cost is the migration, and it grows every month |
| Build | One-way, and the maintenance never ends |

The door breaks the tie. Two weeks of interface layer now is the price of keeping the decision
reversible for three years — which matters more than usual here, because agent frameworks are
changing faster than the products built on them.

---

## 5 · Write the decision record

Not into the sprint log. A sprint log is where decisions go to be forgotten, and this one will be
asked again at the first bill.

```
ADR-004 · Agent framework

Status      accepted, 2026-02-20
Context     Six weighted criteria from the ratified NFRs; three options rated;
            three-year cost with people counted; door assessed.
Decision    Borrow the open framework, behind an interface layer.
            Named review at month twelve.
Consequence An interface layer costs two weeks now, and keeps the swap at weeks
            rather than quarters. Team skills score 3 and the team already knows it.
Rejected    Buy — ties on three-year cost, but the door is one-way and the exit
                  cost grows monthly.
            Build — roughly three times the cost, with maintenance forever, for
                  a capability that is not our differentiator.
Flip test   Portability would have to drop from 3 to 1 for "buy" to win.
```

Four things the record must carry: the decision, its consequence, **the options it rejected and why**,
and the review date. The rejected options are the part people omit and the part the next reader needs.

---

## When the matrix and the team disagree

It happens, and it is allowed. The matrix **recommends**; the record is where you say why you followed
it or did not.

What is not allowed is skipping the matrix because the team already prefers something. Rate the
options, then overrule the score on the record if you have a reason. The reason is what stops the
question coming back.

---

## Try it

**Exercise 1.** Your team is choosing between a managed agent service and an open framework. The
managed service scores higher on velocity and vendor support; the open framework scores higher on
portability and cost. Weights are unset. What do you do first?

<details>
<summary>Answer</summary>

**Go and get the weights from the ratified NFRs** — do not invent them in this meeting.

If the NFR workshop ratified cost per case and portability as high-value, high-difficulty items, then
those weights are already agreed and the matrix is nearly filled in. If it did not ratify them, that
is the real finding: you are about to make a three-year decision against criteria nobody has agreed,
and an hour spent on the utility trees now saves the argument later.

Then run the flip test either way, because on a close call the useful output is not the winner but
*how firm the winner is*.
</details>

**Exercise 2.** Finance asks why you are spending two weeks building an interface layer around a
framework that works fine. Answer in three sentences.

<details>
<summary>A defensible answer</summary>

"The framework is the fastest thing to start with and the thing most likely to change under us —
agent frameworks are moving faster than the products built on them. Two weeks now makes that swap a
matter of weeks rather than quarters, which is the difference between a planned migration and a
rewrite. It is also what lets us close the framework decision as a **soft** gate and keep building,
instead of halting the phase until we are certain."

The last sentence is the one finance cares about: the interface layer is not insurance, it is what
keeps the build moving while the decision is still open.
</details>

---

**Next:** [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) ·
[Gates and Governance](Gates-and-Governance) · [Role: Solution architect](Role-Solution-Architect) ·
[Decision Trees](Decision-Trees)
