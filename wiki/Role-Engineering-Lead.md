# Role: engineering lead

<!-- tutorial:lesson -->*The short version is the lesson **[For engineers](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/agentic-pdlc-for-engineers/)**, the whole role in one sitting. This page goes deeper.*<!-- /tutorial:lesson -->

You are on the hook for **whether it meets the bar, slice by slice, and whether anyone can tell.** P2
is yours. It ends when the golden set clears the bar and a shadow run agrees — not when the code is
written.

> **Looking for what to do on Monday?** That is the
> [journey](Journey-Engineering-Lead) — eight steps in order, each with its artefact, a template and
> prompts, and [interactive on the site](https://akash-coded.github.io/aws-bedrock-agentcore-strands/engineering/).
>
> This page is the standing definition of the job: what you own, what you may settle alone, what
> crosses your desk, how the role fails, and how anyone can tell from outside whether it is being
> done.

---

## What stays the same, and what changes

| You have always done this | What a model in the middle adds |
| --- | --- |
| Sprint planning, estimation, the definition of done | **Bolts** of one risk each, a **story file** the agent reads, a **context file** it inherits |
| Unit, integration, contract and end-to-end tests | Exact work checked exactly; the acceptance bar becomes a **test that runs**; the harness gates CI |
| Pull requests and the review policy | Review depth follows the **risk of the action**. Money gets two readers, every time |
| CI/CD, environments, releases | A **shadow path behind a flag**, cut-over at five percent, rollback *is* the flag |
| Logs, metrics, traces, alerts | A **redacted** trace per step with token counts, and cache hits marked so nobody scores them as wrong answers |
| Threat modelling and security tests | An **injection suite that runs weekly**, tool signatures that raise on the cap, a confirmation token the model cannot mint |
| Incident response, postmortems, hotfixes | The postmortem asks which control was missing; the spec is reconciled **by diff** after a hotfix |

---

---

## What you own, what you shape, and what you must not touch

| | |
| --- | --- |
| **You own** | The context file set · the never-touch list · the agent-ready story file and its BOUNDARY line · the exact-code floor · the checker implementations · the gated tool signatures · the eval harness in CI · the bolt build log · caching, routing, tracing and the injection test |
| **You shape** | The bar, which is the product manager's · the golden set, which is QA's · where the checkers go, which is the architect's · the alarm thresholds, which are the platform's |
| **You must not touch** | The verdict on a slice · the autonomy level · what a cap *should* be — you implement the number the authority budget gives you · the decision to widen |

**Merging past a red check is yours, and it is a named decision.** There are legitimate reasons to do
it. Every one of them has a person attached and a note saying what was accepted.

---

## The eight decisions only you can make

| Step | The decision | Why it cannot be delegated | Where it lands |
| --- | --- | --- | --- |
| Prepare | The never-touch list | A statement about what your organisation cannot afford to lose. Every line needs somebody who would notice if it went | Context file set |
| Slice | The BOUNDARY line | The one sentence in the file that says what the system must *refuse*. A model asked to write it will write what the system should do | Agent-ready story file |
| Floor | Deciding that something is exact | The call comes from the architect's map and from whether the number is audited. Exactness is a consequence, not a preference | Exact-code inventory |
| Layer | Which steps get a checker at all | A cost and risk trade-off across the whole chain, which a model cannot price because it cannot see the bill | Checker implementation |
| Gate | What a cap is set to, and who may mint the token | Both come from the authority budget and the product manager's autonomy record. You implement them; you do not invent them | Gated tool implementation |
| Harness | That CI actually enforces the bar | The bar values are the product manager's and the set is QA's. Yours is that the check is required and cannot be bypassed | Eval harness in CI |
| Ship | That a bolt cannot be built alone | A claim about your repository and your team's day. Say it before the bolt starts, not on day nine | Bolt build log |
| Operate | What the redaction rules are | Which fields are sensitive is a legal and regulatory question about your business | Operations set |

---

## What crosses your desk

<!-- picture:wikimap:role-engineering-lead -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-engineering-lead.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-engineering-lead.dark.webp"><img alt="What arrives on the engineering lead's desk, from whom, and what leaves it, to whom" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-engineering-lead.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-role-engineering-lead.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| Phase | You receive | You hand over | To |
| --- | --- | --- | --- |
| **P0 · Frame** | Nothing yet, and that is deliberate | A sentence on what is not knowable until P1 | Product manager |
| **P1 · Design & Spec** | The map · the ADRs · the authority budget · the gate map | The context file set · the never-touch list · the boundary line | QA lead |
| **P2 · Build & Prove** | The eight-field spec · a bar per slice · the golden set | Bolts, in dependency order · the harness as a required check · a shadow path behind a flag | QA lead · Product manager |
| **P3 · Run & Learn** | The bill by factor · drift readouts | Caching and routing changes · the ledger behind the report | Solution architect · Product manager |

**The P0 row is not a gap.** Opening a branch in P0 is the most expensive habit in agentic delivery,
because it commits the team to a shape before anyone has decided whether the thing is AI at all.

---

## How this role fails

**The prompt that was asked to hold a boundary.** *"Never refund more than $400"* in the system
message, and a tool that accepts any number.
*The tell:* ask which line of code refuses. If the answer is a sentence in a prompt, there is no
control — only a request.

**A harness that can be bypassed.** The eval suite exists, runs, and is not a required check.
*The tell:* look for a merge in the last month with the suite red or skipped, and see whether anyone
had to put their name on it.

**Bolts cut by priority.** The plan orders work by business value, so day three needs something from
day seven.
*The tell:* a bolt that ends with *"blocked on…"* more than once in a quarter.

**The context file nobody reads because it is a novel.** Everything about the codebase, so a coding
agent gets no signal about what matters.
*The tell:* it has no never-touch list, or the never-touch list has no owner per line.

**Caching that reports itself on and hits nothing.** Anything variable sitting above the cache marker.
*The tell:* a hit ratio near zero while the line item says caching is enabled. See
[How to Control the Token Bill](How-to-Control-the-Token-Bill).

---

## How you are measured

| | What it means |
| --- | --- |
| **Evidence, not opinion** | Every slice that shipped has a lower bound and a shadow comparison behind it |
| **The queue** | Time from ready-for-review to merged, against the slots the review policy actually creates |
| **The ledger** | The per-call cost record that makes the product manager's second number checkable rather than asserted |

Velocity is not on this list on purpose. With a model in the middle, output rises first and review
load rises second, and a team measured on the first will hide the second until the bill or the
incident arrives.

---

## Your first thirty days in the role

1. **Ask which line of code refuses.** Pick the most consequential action in whatever is running and
   follow it down to the enforcement point. If it stops at a prompt, you have found the first job.
2. **Check whether the harness can be skipped.** Not whether it exists — whether a merge can happen
   without it, and whether anybody had to sign for that.
3. **Write the never-touch list** with a person against each line. If nobody can be named for a line,
   it is not actually never-touch.
4. **Re-cut one upcoming sprint as bolts** by dependency, not priority, and see how many of them could
   genuinely ship alone.
5. **Read the cache ordering.** Stable first, marker, then whatever changes. This is usually a
   half-day and the largest single line on the bill.
6. **Look at attempts per case, not retries.** The bill factor works on attempts, and a tail nobody is
   watching is how flat traffic produces a rising bill.

---

## Your Monday list

1. **Write `CLAUDE.md` today.** Single biggest quality lever, one hour.
2. Add `MAX_LOOPS` to every agent loop. Five to start. A loop with no cap burns until someone notices.
3. Move every cap from prompt text into a typed, bounded parameter, and write the two tests.
4. Wire `make golden` into CI as a required check, with the slice tag on every case.
5. Build tomorrow's bolt from its story file **with no repository pastes**. If you need the chat, the
   file is incomplete — and that is the finding.

---

---

## Try it

**Exercise 1.** A pull request improves the overall golden-set score from 79% to 84%. The codeshare
slice drops from 81% to 77%, against a bar of 80%. Ship it?

<details>
<summary>Answer</summary>

**No.** A slice below its bar rejects the change, however good the headline number is. The overall
score went up because the easy, high-volume slice improved, and averaging hid a real regression on
the slice that actually carries risk.

This is exactly why the gate is per slice and not overall, and why the readout the PM reads is shaped
like the bar sheet rather than as a single percentage.
</details>

**Exercise 2.** You add a "review your answer before returning it" step. Quality does not improve.
Why, and what is the fix?

<details>
<summary>Answer</summary>

The model is reviewing its own output **with its own reasoning still in context**, so it shares its
own blind spots. It says "looks good" about the same wrong flight choice it just made.

The fix is **independence**: a different model, or the same model in a fresh context with an
adversarial brief — "find what is wrong". Pass it the constraints and the output only, never the
drafter's reasoning. Treat a fail as a re-draft rather than a warning, and cap re-draft rounds at two
before escalating to a person.
</details>

**Exercise 3.** Audit wants every decision replayable. Privacy wants no passport numbers in logs. Your
current log satisfies neither. What do you build?

<details>
<summary>Answer</summary>

**Redact, do not omit.** One row per consequential action: timestamp, the input with sensitive fields
masked (`passport ****1234`), tools called, the decision, the model version, the approver, the cost.

Masking keeps the decision replayable while the identifier is not exposed. Omitting the field breaks
the audit; logging it raw makes the trace store a breach target — and it is usually protected less
well than the ledger it mirrors.

Then treat the trace store like production data: protected the same way, with a retention window and
an aggregation job after it. Add `redact()` before the trace writer, and make "a passport never
reaches a row" a test.
</details>

---

**Next:** [Role: QA lead](Role-QA-Lead) · [How to Control the Token Bill](How-to-Control-the-Token-Bill)
· [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) · [Formulas and Calculators](Formulas-and-Calculators)

---

## Where the detail lives

| You want | Go to |
| --- | --- |
| The day-to-day walk, with templates and prompts | [Journey · Engineering Lead](Journey-Engineering-Lead) |
| Cutting work into bolts | [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) |
| Reviewing by risk band | [How to Review by Risk Band](How-to-Review-by-Risk-Band) |
| Where a boundary is enforced | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) |
| Cache ordering, tiers, attempts | [How to Control the Token Bill](How-to-Control-the-Token-Bill) |
| Practising the judgement calls | [Exercises](Exercises-and-Answers) · [Scenario Library](Scenario-Library) |

**Next:** [Journey · Engineering Lead](Journey-Engineering-Lead) · [Role: QA Lead](Role-QA-Lead) ·
[Role: Solution Architect](Role-Solution-Architect)
