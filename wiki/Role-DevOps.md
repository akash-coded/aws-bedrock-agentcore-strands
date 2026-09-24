# Role: DevOps and platform

<!-- tutorial:lesson -->*The short version is the lesson **[For DevOps and platform](Agentic-PDLC-for-DevOps-and-Platform-Teams)** — the whole role in one sitting. This page goes deeper.*<!-- /tutorial:lesson -->

You are on the hook for **the floor everything else stands on** — and for the three signals a normal
stack does not have. You hold no product gate. You build the gates, which is a larger job and a
quieter one.

> **Looking for what to do on Monday?** That is the
> [journey](Journey-DevOps) — eight steps in order, each with its artefact, a template and prompts,
> and [interactive on the site](https://akash-coded.github.io/aws-bedrock-agentcore-strands/devops/).
>
> This page is the standing definition of the job: what you own, what you may settle alone, what
> crosses your desk, how the role fails, and how anyone can tell from outside whether it is being
> done.

---

## What stays the same, and what changes

| You have always done this | What a model in the middle adds |
| --- | --- |
| Accounts, landing zones, tagging, budgets | A **per-call cost record**, because the bill is now behaviour rather than capacity. Spend can rise several times over on flat traffic |
| Pipelines and required checks | One of the required checks is now **probabilistic**. It reports a lower bound, and a lower bound can fall without anything being broken |
| Environments and parity | **Model version and prompt version are part of parity.** Two environments that differ by model version are not comparable, and nothing will tell you |
| Secrets, IAM, least privilege | The identity now belongs to something that can be **talked into** using it. Least privilege has to survive persuasion, not just misconfiguration |
| Logs, metrics, traces | Three signals a normal stack does not have: **cost per call**, **attempts per case**, and **drift** against the launch set |
| Rollback | The **prompt is a deployable artefact**, so rollback includes it. And a runaway needs a cap rather than a fix — it is not a bug, it is an absent breaker |
| Incident response | An incident can arrive **with no deploy at all**, because the data or the traffic changed underneath a system that did not |

---

## What you own, what you shape, and what you must not touch

| | |
| --- | --- |
| **You own** | The landing zone and the cost baseline · the model access matrix and the gateway · environment manifests, model version included · the pipeline definition and the required checks · flag configuration and the deploy path · the trace schema, the cost record and the alarm set · the execution role policy and the egress allowlist · the rehearsed recovery runbook and the containment cap |
| **You shape** | The bar, which is the product manager's · what the harness contains, which is QA's · where the checkers go, which is the architect's |
| **You must not touch** | **When to widen** — that is the product manager's gate on live evidence · the verdict on a slice · what the sponsor is shown |

Your job at cut-over is not to decide, it is to make the decision **cheap to take and cheap to
reverse.** Widening should be a configuration change, rehearsed, undoable in one action, at three in
the morning, by somebody who did not build it.

---

## The eight decisions only you can make

| Step | The decision | Why it cannot be delegated | Where it lands |
| --- | --- | --- | --- |
| Baseline | The account boundary, and what may live in production | Blast radius is a business fact — which failures you can survive, and which end something | Landing zone stack |
| Access | Which models are permitted for which data | A residency and contract question about your own organisation, not a capability question | Model access matrix |
| Environments | That a redacted export is safe to put in an evaluation environment | Somebody with accountability reads it and accepts the risk. A model cannot accept a risk | Environment manifest set |
| Pipeline | The decision to merge past a red check | There are legitimate reasons to do it, and every one of them has a name attached | Pipeline definition |
| Deploy | That widening is a configuration change and not a deployment | The decision to widen is the product manager's; making it reversible in one action is yours | Flag configuration |
| Observe | What is masked and what is kept | A legal and contractual question about your own data, and it cannot be answered from the outside | Trace schema |
| Protect | The blast radius of a new permission | What a wrong write costs, and who has to unwind it, are facts about your business | Execution role policy |
| Recover | Declaring the incident over | Somebody with accountability looks at the state of the world — what was written, what was sent, what cannot be unwound — and says so | Recovery runbook |

---

## What crosses your desk

<!-- picture:wikimap:role-devops -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-devops.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-devops.dark.webp"><img alt="What arrives on the platform's desk, from whom, and what leaves it, to whom" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-devops.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-devops.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| Phase | You receive | You hand over | To |
| --- | --- | --- | --- |
| **P0 · Frame** | The candidate list | The landing zone, tags and a cost baseline — *before the first call*, because a baseline taken afterwards is a guess | Everyone |
| **P1 · Design & Spec** | The authority budget · the gate map · the data classes in play | The model access matrix · one gateway · comparable environments with versions pinned | Engineering lead · QA lead |
| **P2 · Build & Prove** | The harness, and what it must block | A required status check that cannot be bypassed · a flag to ship behind | Engineering lead |
| **P3 · Run & Learn** | Traces, alarms, the bill | The three signals · the smallest identity that can do the job · a rehearsed rollback and a containment cap | Product manager · Solution architect |

**The P0 row is the one that is always late and should never be.** A cost baseline is an afternoon's
work before anything runs and an argument afterwards.

---

## How this role fails

**A budget alarm instead of a cost record.** You learn about the bill from finance, monthly, in
aggregate.
*The tell:* you cannot answer *"what does one case cost?"* without an export and an afternoon.

**Environments that differ by model version.** Staging and production disagree and nobody can say
why, because the thing that differs is not in any manifest.
*The tell:* the manifest has no model version and no prompt version in it.

**A required check that is not required.** The harness runs, reports, and does not block.
*The tell:* a merge in the last month with the suite red or skipped and no name against it.

**Least privilege that never met persuasion.** The role is minimal and the agent holding it has never
been tested against someone trying to talk it past the boundary.
*The tell:* there is no injection suite, or it is not a regression test.

**A rollback that has never been run.** It is written down, which is not the same thing.
*The tell:* the runbook has no date on its last rehearsal. If it has never been rehearsed, you do not
have a rollback, you have a hope with steps.

**No cap.** A runaway does not need a bug — two components politely handing work back and forth will
do, and nothing stops them.
*The tell:* there is an alarm on spend and none on attempts. Spend tells you next month; attempts tell
you within the hour.

---

## How you are measured

| | What it means |
| --- | --- |
| **Time to reverse** | How long from *"widen it back"* to it being back, measured by rehearsal rather than by belief |
| **Cost per case, on demand** | Anyone can get the number for any slice, this week, without an export |
| **Blast radius, written down** | Every permission the agent holds has a cost of being wrong and a person who would unwind it |

Uptime is necessary and not sufficient. An agentic system can be entirely available and quietly wrong,
and the three signals above are what separate those two states.

---

## Your first thirty days in the role

1. **Get cost per call into a record you own**, tagged by slice. Everything else on this list is
   easier once this exists, and the number gets harder to reconstruct every week.
2. **Put model version and prompt version into the environment manifest.** Then check whether staging
   and production actually match.
3. **Check whether the harness blocks.** Not whether it runs. If a merge can happen without it, fix
   that before anything else in the pipeline.
4. **Alarm on attempts per case**, not only on spend. This is the cheapest early warning there is.
5. **Rehearse the rollback once**, with a date, including the prompt. Then write the date in the
   runbook.
6. **Set a containment cap** on anything that can call itself, directly or through another component.
   A runaway needs no bug, only no breaker.

---

## Your Monday list

Five things, in order, that move a platform furthest for the least effort:

1. Add a **cost record per call**, tagged by slice. One afternoon, and it makes the product manager's
   second number checkable rather than asserted.
2. Put the **model version** in the environment manifest and diff your environments.
3. Make the eval harness a **required** status check, and see who objects — the objection is
   information.
4. Add an **alarm on attempts per case**. Threshold it at roughly twice the normal tail.
5. Rehearse the **rollback**, prompt included, and date it.

---

## Try it

**Exercise 1.** Take the most consequential tool your agent can call. Write down what a wrong call
costs, who would notice, and who would unwind it.

<details>
<summary>What you should notice</summary>

For most teams the first column is answerable, the second is vague and the third is empty. An
unwinder who does not exist is the definition of an unbounded blast radius, and it is a platform
finding rather than a product one — the permission is yours to grant.

If the cost of a wrong call exceeds what the team can unwind in a working day, that tool belongs
behind a gate regardless of how accurate the model is. Accuracy and blast radius are independent, and
teams routinely trade the first hoping it fixes the second.
</details>

**Exercise 2.** Find out what one case costs. Give yourself ten minutes.

<details>
<summary>What you should notice</summary>

If you cannot do it in ten minutes, you cannot do it during an incident either, and the bill
conversation will happen without you in it. The fix is not a dashboard; it is a per-call record with
the slice on it. A dashboard built over an aggregate can only ever tell you that something rose.
</details>

---

## Where the detail lives

| You want | Go to |
| --- | --- |
| The day-to-day walk, with templates and prompts | [Journey · DevOps](Journey-DevOps) |
| Cost per call, cache ordering, tiers, attempts | [How to Control the Token Bill](How-to-Control-the-Token-Bill) |
| Least privilege that survives persuasion | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) |
| Making the harness a check that cannot be bypassed | [How to Prove the Bar](How-to-Prove-the-Bar) |
| Turning an incident into a control | [How to Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem) |
| Practising the judgement calls | [Exercises](Exercises-and-Answers) · [Scenario Library](Scenario-Library) |

**Next:** [Journey · DevOps](Journey-DevOps) · [Role: Engineering Lead](Role-Engineering-Lead) ·
[Role: QA Lead](Role-QA-Lead)
