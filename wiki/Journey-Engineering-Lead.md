# Engineering lead · the journey, end to end

<!-- tutorial:lesson -->*The short version is the lesson **[For engineers](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/agentic-pdlc-for-engineers/)** — the whole role in one sitting. This page goes deeper.*<!-- /tutorial:lesson -->

**From a story file to a shipped bolt**

8 steps · 50 sub-steps · 8 templates · 24 prompts

This is the reading copy. The [interactive version](https://akash-coded.github.io/aws-bedrock-agentcore-strands/engineering/) has a copy button on every template and prompt, which is what you want when you are actually doing the work.

This page is the walk. For the standing definition of the job — what you own, what you may settle alone, what crosses your desk and how the role fails — see [Role Engineering Lead](Role-Engineering-Lead).

---

Your tests, your reviews and your releases all still exist. What changes is that part of the system is right *a share of the time*, so 'it works' stops being a yes or a no and becomes a number per slice — and the boundary that stops the thing doing harm has to live in your code, because **a prompt is a request and a tool contract is a boundary**.

Two habits carry most of the difference. Everything the agent needs arrives in a **file it can read** — a context file at session start, a story file per bolt — rather than in a chat thread nobody can diff or re-run. And the work is split before it is written: exact work is a function with a unit test, best-guess work is a model call with a measured share, and the best-guess machine never does the exact math.

Eight steps, in the order you would actually do them. Each one ends in something that lives in the repository: a file, a function, a signature, a workflow, a log. If a step's artefact is not in git, the step did not happen.

## The arc

Eight steps, and the four phases they sit in. Where the hard gate falls on your own arc is the thing worth noticing: it is a different place for every role.

<!-- picture:wikimap:journey-engineering -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-engineering.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-engineering.dark.webp"><img alt="The engineering lead's eight steps placed on the four phases, with the artefact each one produces" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-engineering.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-engineering.light.webp">Open the picture full size</a></sub>
<!-- /picture -->


| # | Phase | Step | What it produces |
| --- | --- | --- | --- |
| — | P0 | *Not on the clock — reads the brief, starts nothing* | — |
| 1 | P1 | [**Prepare** — Write the context file every coding tool reads](#1--prepare) | Context file set |
| 2 | P2 | [**Slice** — Build from a story file, never a chat thread](#2--slice) | Agent-ready story file |
| 3 | P2 | [**Floor** — Write the deterministic floor before any prompt](#3--floor) | Exact-code inventory, implemented |
| 4 | P2 | [**Layer** — Add the model calls, and an independent checker after the risky ones](#4--layer) | Checker implementation |
| 5 | P2 | [**Gate** — Put the boundary in the tool signature](#5--gate) | Gated tool implementation |
| 6 | P2 | [**Harness** — Wire the eval harness into CI, in cost order](#6--harness) | Eval harness in CI |
| 7 | P2 | [**Ship** — Build bolt by bolt, and put the shadow path behind a flag](#7--ship) | Bolt build log |
| 8 | P3 | [**Operate** — Cache, route, trace, test the injection, and keep the ledger](#8--operate) | Operations set — caching, routing, trace, injection suite, ledger |

## What is yours, and what is not

| Yours to own | Not yours — stop signing these |
| --- | --- |
| The **context file** every coding tool reads, and the story file every bolt is built from | The **bolt cut** itself — the architect decides the cut; you decide whether each one can be built alone, and say so before you start it |
| The **deterministic floor** — every number that gets acted on is a function with a test | The **acceptance bar** per slice — the PM derives it from damage and saving. You make it run |
| The **boundary**: caps and confirmation tokens in tool signatures, never in prompt text | The golden set's contents and the judge's rubric — those belong to the QA lead |
| The eval harness in CI, and the per-slice rule that blocks a merge | The cut-over and the widening — you build the flag and rehearse the rollback; the PM throws it |
| The build order within the architect's dependency sequence, integrated the same day |  |
| The effort-and-token ledger the product manager's cost number is built from |  |

## How to use a model in this role

> Use a model for **the typing and the sweep**, never for the boundary. It will write a correct `fare_difference()` faster than you can, and it will just as happily write a cap into a prompt and report the cap as done. The pattern that works: the model drafts *inside* something you wrote — a context file, a story file, a signature you already fixed — and every line that moves money, changes a booking or writes a trace row is read by a person before it merges. Where a step below says *do not delegate*, the model has no standing, and it is almost always because the decision is about what the code must **refuse** rather than what it should do.

---

> **P1 · Design & Spec begins here** — *what exactly is being built, and under whose authority?*

## 1 · Prepare

### Write the context file every coding tool reads

*Day one on the repository, before the first agent session*

Every AI coding tool reads a file from the repository before it does anything, and most teams have not written one. It is an hour of work and the single biggest quality lever you have, because it is the only instruction that reaches every session, every engineer and every tool without anyone remembering to type it. Write it once, point it at the context layers rather than copying them, and grow it by adding the rule that bit you last week.

**What you actually do**

1. **Find out which file each of your tools actually reads** — Claude Code reads `CLAUDE.md` as project memory, committed to git, with enterprise policy above it and a user-level file for personal preferences. Copilot reads `.github/copilot-instructions.md` plus scoped `.github/instructions/*.instructions.md`. Codex CLI reads `AGENTS.md`. Cursor reads `.cursor/rules/*.mdc`.
2. **Weight the two kinds differently** — Copilot's file steers inline suggestions; Claude Code's drives autonomous actions. The same sentence about never editing an applied migration is advice in the first case and a standing instruction in the second, so write the never-touch list for the second.
3. **Write four sections and nothing else** — Stack, conventions, commands, never-touch. Anything longer stops being read — by the model, because the rules are diluted, and by the engineer who is supposed to maintain it. Under a hundred lines is a working target.
4. **Point at the context layers, never copy them** — `/context/shared/standards.md` by path, not pasted. A copy is a fork: the security rule changes in the shared layer and the agent carries on quoting last quarter's version back at the team that wrote it.
5. **Make every command one you have actually run** — A command that does not exist is worse than no command. The agent improvises a plausible one, reads the error as an environment problem, works around it, and you review a diff resting on a green that never happened.
6. **Grow it with the rule that bit you last week** — Every time, one line, dated at the bottom. That is the whole maintenance policy and it is the only one that survives a busy quarter. Review the diff like code, because it is.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Point it at the repository and ask for a first draft from what is actually there — the build files, the test runner, the directory layout. It reads the tree faster than you do and it gets the stack section right.<br>⚠ Make it run every command it proposes and paste the output into the session. Left alone it will write `npm test` into a Python repository because the shape of the file suggests a line like that belongs there. |
| **An editor agent (Copilot, Cursor)** | Have it derive the scoped instruction files per path from the one project file, so the narrow rules about `src/tools/**` sit next to the narrow code they govern.<br>⚠ Scoped files multiply. Keep one owner and one review, or within a month you have six of them quietly contradicting each other and no way to tell which one won. |
| **A cheap tier** | Feed it last month's pull request review comments and ask which corrections repeat. The repeats are your missing conventions, already evidenced and already argued. |
| **Do not delegate** | The never-touch list. It is a statement about what your organisation cannot afford to lose, and every line on it is there because of an incident the model has never seen. |

**The artefact**

| | |
| --- | --- |
| Produces | **Context file set** |
| Good looks like | One project file per tool, all pointing at the same context layers, all committed. Four sections, under a hundred lines, and a dated line at the bottom recording the last rule that was added and why. |
| Owner | Engineering lead |

<details><summary><b>Template · CLAUDE.md · the project context file</b></summary>

```markdown
# CLAUDE.md · <repo name>
Project memory. Committed. Read at the start of every session. The same content is
mirrored to .github/copilot-instructions.md (inline suggestions) and AGENTS.md.

## Stack
- <language + version> · <framework> · <package manager>
- Tests <pytest> · Lint <ruff> · Types <mypy --strict on src/tools/**>
- Infra <CDK in infra/> · Deploy <how, and who is allowed to>

## Context layers — READ THESE BY PATH. Do not paste them into a prompt.
- /context/shared/standards.md        org standards, security, tone
- /context/domain/<booking-model>.md  the domain vocabulary
- /context/product/architecture.md    this product, plus ADR-001..ADR-<n>
If a rule here disagrees with a layer, the layer wins and this file is out of date.

## Conventions
- Exact work is a function with a unit test. Never compute money in a prompt.
- Every tool that writes takes a confirmation token. Reads do not.
- One model per task — the cache is model-scoped and a switch discards it.
- A new dependency is an issue first, never an addition made in passing.

## Commands — every one of these has been run. Use them; do not improvise.
| To do this | Run |
|------------|-----|
| Unit tests | `<make test>` |
| The golden slice for one bolt | `<make golden SLICE=codeshare>` |
| Lint and types | `<make check>` |
| Local stack up | `<make up>` |

## Never touch
- `<config/caps.yaml>` — the authority budget. Changing a cap is an R4 change.
- `<src/tools/refund/**>` — two named reviewers, every time.
- `<migrations/>` — never edit an applied migration. Add a new one.
- `<src/trace/redact.py>` — security reviews every change here.

## Ask before
- Adding a tool to the agent's tool list
- Editing anything under `<src/prompts/>` — it re-runs the injection suite
- Touching a golden-set file. Those belong to QA, not to this repo's authors.

---
_Last rule added <date> — <the rule that bit us last week, in one line>_
```

</details>

<details><summary><b>Prompt · Draft the context file from the repository itself</b> — Hour one on a repository that has none</summary>

```text
You are writing the project context file that every coding agent on this
repository will read at the start of every session. The repository is at <path>
and the shared context layers live under </context/shared/>.

Read the repository first. Do not ask me questions you can answer by reading.

Produce EXACTLY four sections and nothing else:
1. Stack — language, framework, package manager, test runner, linter, type checker
2. Context layers — paths only, no pasted content
3. Commands — a table of task and command
4. Never touch — files where a mistake is expensive, one reason each

RULES:
- Run every command you put in section 3 and paste its output below the draft. If a
  command fails, remove it and say so; a command that does not work is worse than none.
- Do not invent conventions. Only write a convention you can point at a file for.
- Keep it under 100 lines. If you are over, cut section 3, never section 4.
- Mark anything you inferred rather than read with INFERRED, so I can check it.

OUTPUT: the file, then the command output, then a list of your INFERRED lines.
```

</details>

<details><summary><b>Prompt · Mine the review history for the rules you are missing</b> — You have a context file and want the next four lines of it</summary>

```text
Below are the review comments left on merged pull requests over <n> weeks.

Find the corrections that REPEAT. A correction made three times is a missing convention.

OUTPUT a table:
| The rule, as one imperative sentence | Times it was said | Example comment | Section |

Where Section is one of: conventions / commands / never-touch / not a rule.

RULES:
- Rank by how many times it recurs, not by how strongly it was worded.
- Merge comments that say the same thing differently; keep the clearest wording.
- Mark as "not a rule" anything that was a one-off judgement about that change. Those
  do not belong in a context file and adding them is how the file becomes unreadable.
- For each rule, say whether it could be ENFORCED instead — a lint rule, a CI check, a
  type. A rule that can be enforced should not be a line in a markdown file.

COMMENTS:
<paste>
```

</details>

<details><summary><b>Prompt · Audit the context file you already have</b> — The file exists, and sessions still go wrong in the same ways</summary>

```text
Here is our context file: <paste>. Here is the repository layout: <paste>.

Audit it and report, in this order:

1. DEAD COMMANDS — any command in the file that does not exist or does not run. Run each.
2. STALE PATHS — any path referenced that is not in the repository.
3. COPIED CONTEXT — any text that looks like a pasted copy of a shared standard rather
   than a reference to it. Copies go stale silently; say where the original should be.
4. VAGUE RULES — any line containing "appropriate", "correct", "as needed", "try to",
   "where possible". Rewrite each as something checkable, or recommend deleting it.
5. MISSING — of stack / context layers / conventions / commands / never-touch, which
   section is absent or thin?

Finish with the THREE lines you would add first, and the evidence for each.
Do not rewrite the whole file. I want the diff, not a replacement.
```

</details>

**Worked example · SkyWays · the two rules that were added in the first month**

> The first `CLAUDE.md` was twenty-two lines written in an hour: stack, four commands that had been run, and a never-touch list with `migrations/` on it. It grew twice. Once after an agent re-implemented the fare arithmetic inline rather than calling `fare_difference()` and returned $80 where the ledger said $62 — the line added was *never compute money in a prompt; call the function*. Once after a session switched model mid-task and the cache hit ratio collapsed, which added *one model per task*. Two sentences, and neither failure has recurred. That is the whole evidence the file needs.

**Pitfalls**

- Writing it once and never again. A context file that has not changed in three months describes a repository that no longer exists, and the agent is following it confidently.
- Pasting the shared standards into it instead of linking them. The copy goes stale the first time the standard changes, and the agent then argues with your security team using your own old words.
- Listing commands nobody has run. The agent improvises a plausible substitute, treats the failure as an environment problem, and you end up reviewing a diff built on a green that never happened.

**Done when** — A new engineer, or a fresh agent session, can clone the repository, run every command in the file, and have all of them work without asking anybody a question.

---

> **P2 · Build & Prove begins here** — *does it meet the bar, slice by slice?*

> ⛔ **The hard gate — P1 to P2.** Everything past this point depends on the spec, the acceptance bar per slice and the authority budget being signed. It is the one crossing nothing downstream survives without — [why](The-Agentic-PDLC).

## 2 · Slice

### Build from a story file, never a chat thread

*The evening before each bolt, once the architect has cut it*

A bolt that needs a chat thread was cut wrong, or its file is incomplete, and either way that is a finding rather than an inconvenience. The story file is one self-contained file with six parts, versioned beside the code it produces: context **by reference**, the spec in EARS, the tools with their risk bands, the tests, the done-when, and the cost. Because it is a file it is reviewable as a diff and re-runnable next month. It is BMAD's *shard* and spec-driven development's unit at once.

**What you actually do**

1. **Write the context section as paths, never as pastes** — `/context/domain/booking-model.md`, ADR-004, ADR-007. A pasted document is forty thousand tokens per call and, reliably, a worse answer than the slice would have given, because the relevant lines are now buried in material the model has to rank.
2. **Put the spec in EARS, with the boundary on its own line** — WHEN <trigger> AND <precondition> THE SYSTEM SHALL <response> WITHIN <limit>. Then BOUNDARY as a separate line, because that is the sentence that becomes a raise in the signature two steps from now rather than a hope in a paragraph.
3. **List the tools with the band from the authority budget** — `rebook(pnr, segment, fare_delta, confirmation) → R3`. The band comes from the budget, never from the author, and it decides how many people have to read the pull request.
4. **Name both kinds of test, by name** — The golden slice with its case count and its bar, and the unit tests spelled out: `rebook_requires_fare_delta`, `rebook_is_idempotent`. Named now, they get written. Described now, they get skipped and nobody can point at the moment it happened.
5. **Write the done-when so a machine can turn it red** — Harness green on the named slice, integrated to main, one trace row written. Three checkable things. 'Works as described' is not a done-when, it is a hope with a tick box next to it.
6. **Estimate the tokens per call and the tier** — Roughly 1,900 tokens, mid tier. It is an estimate and it is still worth writing, because the first bolt whose real number is triple its estimate is exactly where you find the document somebody pasted.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Give it the bolt's one-line description, the ADR numbers and the authority budget, and have it assemble the six sections. The mechanical part — resolving paths, copying the signature, pulling the band — is exactly what it is good at.<br>⚠ It will produce a spec sentence containing 'appropriately' or 'correctly'. Every one of those words is a decision nobody has made; strike it and write the number. |
| **A chat surface** | Paste a prose paragraph from the product manager and ask for it back as EARS, with the trigger, the precondition, the response and the limit as separate clauses.<br>⚠ Check the precondition. Models drop the AND clause more often than any other part, and the dropped clause is usually the one that stops an action happening before a number exists. |
| **A cheap tier** | Have it diff yesterday's story file against what actually merged and list the sections the file got wrong. That diff is how the template stops being aspirational. |
| **Do not delegate** | The BOUNDARY line. It is the one sentence in the file that says what the system must refuse, and it is written by the person who will be accountable when it does not. |

**The artefact**

| | |
| --- | --- |
| Produces | **Agent-ready story file** |
| Good looks like | One file, six sections, no repository pastes. An engineer can build the bolt from it with the chat window closed, and a reviewer can see every decision in it as a diff. |
| Owner | Engineering lead |

<details><summary><b>Template · Story file · one bolt</b></summary>

```markdown
# Bolt <7> · <rebook() gated write>
_Author <name> · Date <date> · Architect's cut: bolt <7> of <10>_

## 1 · Context — BY REFERENCE. These are not pasted into any prompt.
- /context/shared/standards.md
- /context/domain/<booking-model>.md
- /context/product/architecture.md
- ADR-<004> <one-line title> · ADR-<007> <one-line title>

## 2 · Spec (EARS)
WHEN   <the passenger accepts a proposed alternative>
AND    <the fare difference has been computed by fare_difference()>
THE SYSTEM SHALL <rebook the segment> WITHIN <10> seconds.

BOUNDARY  <Never rebook without a computed fare difference.>
BOUNDARY  <Never rebook a segment that has already departed.>

## 3 · Tools, with the band taken from the authority budget
| Signature | Band | Reads or writes |
|-----------|------|-----------------|
| `rebook(pnr, segment, fare_delta, confirmation) -> Booking` | R3 | writes |
| `get_booking(pnr) -> Booking` | R1 | reads |

## 4 · Tests
- Golden slice `<rebook>` — <40> cases, bar <85>%
- Unit `<rebook_requires_fare_delta>` · `<rebook_is_idempotent>` ·
       `<rebook_rejects_a_departed_segment>`
- Injection: <every attack string, aimed at rebook, from the passenger message
  and from the partner API notes field>

## 5 · Done when
- [ ] `<make golden SLICE=rebook>` at or above the bar, lower bound reported
- [ ] `<make test>` green, including the three unit tests named above
- [ ] merged to main and integrated <the same day>
- [ ] one redacted trace row per rebook, carrying the model version

## 6 · Cost
- ~<1,900> tokens per call, <mid> tier, prefix <cached, 5m>
- Expected cost per case $<0.04>. Alert at 3x.

## Can this bolt be built alone?
yes  /  **no — and if no, this is raised NOW, not at 2pm**: <what it needs that
does not exist yet, and who owns the re-cut>
```

</details>

<details><summary><b>Prompt · Assemble the story file for tomorrow's bolt</b> — The evening before, once the architect has the cut</summary>

```text
Assemble a story file for one bolt. Six sections, in this order:
context (by reference) · spec in EARS · tools with bands · tests · done-when · cost.

RULES:
- Section 1 contains PATHS ONLY. If you are tempted to paste a document, write the path
  and the specific heading inside it instead.
- Section 2 is EARS: WHEN <trigger> AND <precondition> THE SYSTEM SHALL <response>
  WITHIN <limit>. Every BOUNDARY goes on its own line, phrased as what the system must
  REFUSE, never as what it should try to do.
- No sentence may contain "appropriate", "correct", "reasonable", "as needed" or
  "where possible". If you cannot remove the word, write UNDECIDED and the question.
- Section 3 takes the band from the authority budget I give you. Do not assign one.
- Section 4 names the unit tests. Names, not descriptions.
- Section 5 must be checkable by a machine, in three lines or fewer.

OUTPUT the file, then a separate list headed UNDECIDED with every open question.

BOLT: <one line>
AUTHORITY BUDGET: <paste>
ADRs AND CONTEXT PATHS: <paste>
```

</details>

<details><summary><b>Prompt · Turn prose into EARS without losing a clause</b> — The spec arrived as a paragraph</summary>

```text
Rewrite the requirement below in EARS.

FORMAT:
WHEN   <trigger>
AND    <precondition>          (repeat for each; do NOT merge them)
THE SYSTEM SHALL <response>
WITHIN <limit, with a unit>

Then, separately, one BOUNDARY line per thing the system must refuse.

RULES:
- Preserve every precondition as its own AND line. Do not summarise two into one.
- If a limit is missing, write WITHIN <UNSPECIFIED> — never invent a number.
- List any word in the original that hides a decision ("appropriate", "quickly",
  "if possible") and say what decision it is hiding and who should make it.
- At the end, list anything in the prose that is a SOLUTION rather than a requirement.

PROSE:
<paste>
```

</details>

<details><summary><b>Prompt · Find what the file is missing, before building anything</b> — First thing on the build day</summary>

```text
Here is the story file for today's bolt: <paste>.

DO NOT WRITE ANY CODE. Do not start.

List every question you would have to ask me in order to build this bolt without
further conversation. For each question:
- which section of the file should have answered it
- what you would assume if nobody answered
- whether that assumption could move money, change a booking, or write a trace row

Then answer one thing: can this bolt be built and tested ALONE, with nothing that is
scheduled for a later day? If not, name exactly what is missing and stop.

Every question on your list is a defect in the file, not in me. I am going to fix the
file, and then you are going to build from it with this conversation closed.
```

</details>

**Worked example · SkyWays · the file that let the chat window stay shut**

> Bolt seven was `rebook()`. Its first story file pasted the booking model — nine hundred lines — into the context section. That session cost three times its estimate and produced a function that re-derived the fare delta rather than taking it as a parameter. The second version replaced the paste with two paths and added one BOUNDARY line: *never rebook without a computed fare difference*. That line became a raise in the signature the same afternoon, `rebook_requires_fare_delta` went red and then green, and the bolt integrated before five. The test of a story file is not whether it reads well. It is whether the chat window can stay shut.

**Pitfalls**

- Pasting the repository into the context section. It costs forty thousand tokens a call and returns a worse answer, because the slice that mattered is now buried in material the model has to rank.
- A spec sentence containing 'appropriately', 'correctly' or 'as needed'. Each one is a decision nobody has made, and it will be made by the model, silently, at about two in the afternoon.
- Keeping the chat thread as the real source and the file as documentation. The thread cannot be diffed, reviewed or re-run, so the second engineer builds a different bolt from the same file.

**Done when** — An engineer who was not in the planning conversation can build the bolt from the file alone, with the chat history closed, and the reviewer can see every decision as a diff.

---

## 3 · Floor

### Write the deterministic floor before any prompt

*The first coding day of each bolt*

Every number the feature computes and then acts on is a function, unit-tested, and never a prompt. This is the rule in the role with no exceptions, because a model doing arithmetic fails **fluently**: it returns $80 where the ledger says $62, with no error, no stack trace and nothing unusual in the wording, and the first person to notice is the customer. Walk the architect's exact/best-guess map and write a signature and one assertion for every step marked exact. It is the cheapest code in the build and it is the code that holds.

**What you actually do**

1. **Walk the architect's map line by line** — Every step marked **exact** becomes a function name before any of them becomes a body. The map already did the sorting; your job is to refuse to let a single exact step stay inside a prompt because it looked like one sentence.
2. **Write the signature and one assertion before the body** — One assertion per exact step, taken from the spec rather than from what the code happens to do, and watched going red. A test written after the implementation is a test of the implementation.
3. **Use exact types for money** — `Decimal`, never `float`. Round once, at a named boundary, with the rounding mode stated in the code. A good share of fare disputes in any airline system are two systems rounding differently and both being certain.
4. **Grep the prompts for calculate, compute, total, sum** — Every hit is a function waiting to exist. Run it over the prompt directory rather than the code, run it again after every prompt change, and make it a two-line CI check so the sweep does not depend on anyone remembering.
5. **Give the model the function, never the arithmetic** — It calls `fare_difference()` and reads the result. Expose it as a tool with a narrow signature so there is nothing else it could plausibly do with the numbers it has.
6. **Keep the floor out of the harness** — Exact code is proven by unit tests that are green or red, not by a measured share. If a fare function is being scored at 97% somebody has put it on the wrong side of the line, and 3% of the money is quietly in scope.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Hand it the spec clause and the signature and let it write the body and the table-driven cases. Exact code from a written rule is the work models do best, and the unit test tells you within seconds whether it worked.<br>⚠ Write the first assertion yourself. A model that writes both the code and its tests will make them agree with each other and disagree with the spec, and the suite goes green on the wrong behaviour. |
| **An editor agent** | Ask for the edge cases you did not list: zero, negative, identical fares, currency mismatch, a segment already flown. It is reliably better than a tired person at enumerating boundaries.<br>⚠ It enumerates, you decide. Half its cases are behaviours you deliberately put out of scope, and writing tests for those freezes decisions nobody ever made. |
| **A cheap tier** | Run the calculate/compute/total sweep across the prompt directory and return the candidate functions with the offending prompt line beside each. A sweep, not a judgement. |
| **Do not delegate** | Deciding that something is exact. That call comes from the architect's map and from whether the number gets acted on; a model asked the question answers from how the sentence is phrased. |

**The artefact**

| | |
| --- | --- |
| Produces | **Exact-code inventory, implemented** |
| Good looks like | One row per exact step with a function name, a test name and a green tick, and nothing left in the prompts that produces a number anybody acts on. |
| Owner | Engineering lead |

<details><summary><b>Template · The deterministic floor, and the test that comes first</b></summary>

```python
# src/exact/fare.py — the deterministic floor for <bolt 2>.
# Every number here is acted on, so none of it may live in a prompt.
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CURRENCY = "<GBP>"
PENNY = Decimal("0.01")


class CurrencyMismatch(ValueError):
    pass


@dataclass(frozen=True)
class Fare:
    amount: Decimal
    currency: str
    refundable: bool


def fare_difference(original: Fare, replacement: Fare) -> Decimal:
    # What the passenger owes. Never negative. Rounded once, here, half up.
    if original.currency != replacement.currency:
        raise CurrencyMismatch(f"{original.currency} vs {replacement.currency}")
    owed = max(replacement.amount - original.amount, Decimal("0"))
    return owed.quantize(PENNY, rounding=ROUND_HALF_UP)


# tests/exact/test_fare.py — the assertion comes from the spec and is written
# BEFORE the body above. A test written afterwards tests the implementation.
import pytest


def fare(amount: str) -> Fare:
    return Fare(Decimal(amount), CURRENCY, refundable=False)


def test_difference_is_the_ledger_number():
    # The case the prompt got wrong: it answered 80. The ledger says 62.
    assert fare_difference(fare("138.00"), fare("200.00")) == Decimal("62.00")


def test_a_cheaper_replacement_never_owes_a_negative():
    assert fare_difference(fare("200.00"), fare("138.00")) == Decimal("0.00")


def test_currency_mismatch_raises():
    with pytest.raises(CurrencyMismatch):
        fare_difference(fare("100.00"), Fare(Decimal("100.00"), "<USD>", False))


@pytest.mark.parametrize("before,after,owed", [
    ("100.005", "100.020", "0.02"),   # half up, applied once, at the boundary
    ("0.00", "0.00", "0.00"),
])
def test_rounds_half_up_exactly_once(before, after, owed):
    assert fare_difference(fare(before), fare(after)) == Decimal(owed)
```

</details>

<details><summary><b>Prompt · Turn the exact map into signatures and failing tests</b> — You have the architect's map and no code yet</summary>

```text
Below is the exact / best-guess map for <feature>, and the spec clauses.

For EVERY step marked EXACT, produce:
1. A function signature with precise types. Money is Decimal, never float.
2. ONE assertion taken from the spec clause — not from any implementation.
3. The exception it raises when its precondition is violated, named.

RULES:
- Write the tests FIRST, in a block I can run immediately. They must fail.
- Do not write any function bodies in this response.
- If a spec clause does not pin down a value precisely enough to assert on, write
  UNDECIDED and the exact question. Do not choose a plausible number.
- State the rounding rule for every monetary function: where it happens and which mode.
- Flag any step on the map marked BEST-GUESS that you think is actually exact, with the
  reason. Do not act on it; I will take it to the architect.

MAP: <paste>
SPEC CLAUSES: <paste>
```

</details>

<details><summary><b>Prompt · Sweep the prompts for arithmetic</b> — Weekly, and after every prompt change</summary>

```text
Search every file under <src/prompts/> for arithmetic that a model is being asked
to perform: the words calculate, compute, total, sum, difference, percentage, fee,
charge, and any currency symbol.

OUTPUT a table:
| File and line | The sentence | Is the number ACTED ON? | Function it should become |

RULES:
- "Acted on" means the value reaches a tool call, a customer, a ledger or a document.
  A number that only appears in an explanation to a human is not the same category —
  mark it EXPLANATORY and leave it alone.
- Propose a signature for every acted-on hit, with Decimal for money.
- Do not change any file. Return the table and the signatures only.
- At the end, give me the one-line shell command for this grep so I can put it in CI.
```

</details>

<details><summary><b>Prompt · Edge cases for an exact function</b> — The body is written and the tests feel thin</summary>

```text
Here is an exact function and its current tests: <paste>.
Here is the spec clause it implements: <paste>.

List the inputs that would break it or expose an undecided behaviour. Cover at least:
zero, negative, equal values, the rounding boundary, unit or currency mismatch, missing
optional fields, and the largest value the domain allows.

For each, output a row:
| Input | What the code does today | What the SPEC says | Decided or UNDECIDED |

RULES:
- Where the spec is silent, mark UNDECIDED and do NOT write a test for it. A test over
  an undecided behaviour freezes a decision nobody made.
- Only give me test code for the rows marked Decided.
- If the code and the spec disagree anywhere, say so first and loudly, before the table.
```

</details>

**Worked example · SkyWays · $80 where the ledger said $62**

> The fare difference began life inside the prompt, in a sentence containing the word *exactly*. It returned $80 where the ledger said $62 — fluently, with no error, and the passenger was the first to know. The fix was about forty lines: `fare_difference()` taking two `Decimal` fares, raising on a currency mismatch, rounding half up once, with one assertion asserting 62.00 and the number removed from the prompt entirely. What made the fix cheap is that the architect's map had marked the step exact on day one. What made it necessary is that nobody had walked the map before writing the prompt.

**Pitfalls**

- Leaving the arithmetic in the prompt because it is only one number. One number that gets acted on is the whole category, and it fails without producing an error anybody can catch.
- Letting the model write the code and its own assertions in one pass. They agree with each other, both disagree with the spec, and the suite goes green on the wrong behaviour.
- Using `float` for money. Two systems round differently, both are certain, and the difference surfaces weeks later as a reconciliation ticket nobody can reproduce.

**Done when** — Grepping the prompt directory for calculate, compute, total and sum returns nothing that gets acted on, and every exact step on the architect's map has a named function and a named test that has been seen red before it was seen green.

---

## 4 · Layer

### Add the model calls, and an independent checker after the risky ones

*Once the floor is green, mid-bolt*

The best-guess layer goes on top of the floor: ranking, drafting, classifying — the work that is right a share of the time and has to be measured rather than asserted. Chains multiply, so keep them short, then put a checker after the steps where a wrong answer is **costly and easy to miss**. The checker only earns its call if it is independent. A model reviewing its own output shares its own blind spots, which is why *review your answer before returning it* changes nothing measurable and still appears on the invoice.

**What you actually do**

1. **Count the chain before you build it** — Four steps at 90% each is 0.66 end to end, and it fails fluently. The first fix is always to shorten the chain: two of any six steps are usually exact work that crept into a prompt and belongs in the previous step.
2. **Place checkers where a mistake is costly AND easy to miss** — After choosing the flights and after drafting the passenger message. Not after computing the fare, which needs a unit test, and not after writing the trace row, which is exact. Every checker is a call you pay for on every case.
3. **Make the checker independent, and record which kind** — A different model, or the same model in a fresh context with an adversarial brief — *find what is wrong*. Write which one you chose in a comment beside it, because the next person to touch this will assume the cheap version was intended.
4. **Pass the constraints and the output, never the drafter's reasoning** — The reasoning is the contamination. Send the rules the output must satisfy and the artefact to be judged, and nothing that explains why the drafter believed it was fine, because that explanation was written to be convincing.
5. **Treat a fail as a re-draft, and cap the rounds at two** — A warning gets logged and ignored. Two rounds, then escalate to a person. An uncapped re-draft loop looks like diligence on a good day and is the same runaway as a missing loop cap on a bad one.
6. **Log the checker's verdict as its own trace field** — Pass or fail, plus the round number. Without it you cannot tell a chain that never fails from a checker that never fires, and on a dashboard those two look identical.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it implement the draft, check and re-draft loop against your interfaces, with the round cap and the verdict logging in the first version rather than as a follow-up ticket that never gets picked up.<br>⚠ Read what it passes to the checker. The obvious implementation forwards the whole conversation, which is precisely the contamination the checker exists to avoid. |
| **A second model as the checker** | Genuinely different weights, an adversarial brief and a rubric. This is the version that finds things, and it is the version you can defend to QA when they ask what independent means here.<br>⚠ It is a second bill on every case. Place it only where the architect's map says costly and easy to miss, and be able to name the cases that justified it. |
| **A chat surface** | Draft the adversarial rubric: the failure modes the checker must look for, in the order a good reviewer would look for them.<br>⚠ A rubric written from imagination finds imagined problems. Build the first version from the last twenty real disagreements, then extend it from first principles. |
| **Do not delegate** | Deciding which steps get a checker at all. It is a cost and risk trade-off across the whole chain, and a model asked step by step will recommend one everywhere, because each one is sensible in isolation. |

**The artefact**

| | |
| --- | --- |
| Produces | **Checker implementation** |
| Good looks like | A named checker after each risky generating step, independent by construction, capped at two re-drafts, with the verdict and round number in the trace. Placement written down with the reason beside it, so it can be argued with. |
| Owner | Engineering lead |

<details><summary><b>Template · The best-guess layer with an independent checker</b></summary>

```python
# src/agent/checked_step.py — the best-guess layer, checked independently.
# Independence here means <a different model family>. If that changes, QA is told.
from dataclasses import dataclass

from src.models import call          # call(model, system, user) -> str
from src.trace import trace

DRAFTER = "<drafting-model-id>"
CHECKER = "<a-different-model-id>"
MAX_REDRAFTS = 2

ADVERSARIAL = (
    "You are reviewing work you did not produce. Find what is wrong. You are\n"
    "given the CONSTRAINTS and the OUTPUT only, never the author's reasoning,\n"
    "and you must not ask for it. Reply PASS, or FAIL and one line per breach."
)


class NeedsAPerson(Exception):
    pass


@dataclass(frozen=True)
class Checked:
    output: str
    rounds: int


def checked_step(system: str, user: str, constraints: str, step: str) -> Checked:
    # Draft, check independently, re-draft at most twice, then escalate.
    feedback = ""
    for attempt in range(MAX_REDRAFTS + 1):
        draft = call(DRAFTER, system, user + feedback)
        # Constraints and output ONLY. The drafter's reasoning is the contamination.
        brief = f"CONSTRAINTS:\n{constraints}\n\nOUTPUT TO JUDGE:\n{draft}"
        verdict = call(CHECKER, ADVERSARIAL, brief)
        passed = verdict.strip().startswith("PASS")
        trace.write(step=step, round=attempt, checker=CHECKER,
                    checker_verdict="pass" if passed else "fail")
        if passed:
            return Checked(draft, attempt)
        feedback = f"\n\nA reviewer rejected the previous attempt:\n{verdict}"
    raise NeedsAPerson(f"{step}: {MAX_REDRAFTS} re-drafts rejected")


# tests/agent/test_checked_step.py
import pytest


def test_the_checker_never_sees_the_drafters_reasoning(spy):
    checked_step(system="<...>", user="<...>", constraints="<...>", step="<rank>")
    sent = spy.calls_to(CHECKER)[0].user
    assert sent.startswith("CONSTRAINTS:") and "OUTPUT TO JUDGE:" in sent
    assert "<thinking>" not in sent and "because I" not in sent


def test_escalates_to_a_person_after_two_redrafts(always_fails):
    with pytest.raises(NeedsAPerson):
        checked_step("<...>", "<...>", "<...>", step="<rank>")
```

</details>

<details><summary><b>Prompt · Decide where the checkers go</b> — You have the chain and the architect's map</summary>

```text
Here is the chain of steps for <feature>, with the architect's exact / best-guess
map beside it: <paste>.

For EACH step, output a row:
| Step | Exact or best-guess | Cost of a wrong answer | Easy to miss? | Checker? | Why |

RULES:
- An EXACT step never gets a checker. It gets a unit test. Say so on those rows.
- Recommend a checker ONLY where a wrong answer is both costly AND easy to miss. A
  wrong answer that the next step would reject anyway does not need one.
- Every checker is a model call on every case. Give me the estimated added cost per
  case for your recommendations, as a total.
- Then compute the end-to-end product of the per-step accuracies I gave you, and tell
  me whether SHORTENING the chain would buy more than any checker you proposed.

Finish with the single step you would check first if I could only afford one.
```

</details>

<details><summary><b>Prompt · Write the adversarial checker brief</b> — Implementing the checker</summary>

```text
Write the system prompt for an INDEPENDENT checker on this step: <describe>.

The checker will receive the CONSTRAINTS and the OUTPUT. It will never receive the
drafter's reasoning, and it must not ask for it.

The brief must:
- tell it plainly that it is reviewing work it did not produce, and to find what is wrong
- list the failure modes to look for, in the order a good reviewer would check them
- fix the reply shape: PASS, or FAIL followed by one line per violated constraint
- forbid rewriting the output; its job is a verdict, not a draft

RULES FOR YOU:
- Build the failure-mode list from the real disagreements I paste below, not from first
  principles. Anything you add from imagination, mark INVENTED.
- Do not include praise, encouragement or any instruction to be balanced. A checker that
  is being fair is a checker that is passing things.

REAL DISAGREEMENTS: <paste>
CONSTRAINTS THE OUTPUT MUST SATISFY: <paste>
```

</details>

<details><summary><b>Prompt · Audit a checker that is not finding anything</b> — You added a review step and quality did not move</summary>

```text
Here is our checker implementation and a sample of its inputs: <paste>.

Answer these five, in order, and stop at the first NO:

1. Is the checker a DIFFERENT model, or the same model in a genuinely fresh context?
2. Is the drafter's reasoning excluded from what the checker receives? Quote the exact
   lines of code that exclude it, or say it is not excluded.
3. Does the brief tell it to find what is WRONG, or to review and confirm?
4. Is there a cap on re-draft rounds, and does exceeding it escalate to a person rather
   than returning the last draft?
5. Is the verdict written to the trace on every case, pass and fail alike?

Then tell me the pass rate over the sample. A checker that has passed everything is
either unnecessary or broken, and those two are distinguished by the sample, not by
opinion. Say which one this is and what evidence would settle it.
```

</details>

**Worked example · SkyWays · the review step that changed nothing**

> A *review your answer before returning it* step was added after the ranking call. Scores did not move and the bill rose by about a fifth. The model was reading its own output with its own reasoning still in context, so it agreed with the same wrong flight choice it had just made, confidently, every time. Replacing it with a different model, given the constraints and the ranked list and nothing else, moved the codeshare slice by four points and — more usefully — started producing fails, which was the first evidence the checker was doing anything at all. The cap of two re-draft rounds was added the same day, after one case went round eleven times before anyone read the log.

**Pitfalls**

- 'Review your answer before returning it.' Same model, same context, same blind spots. It costs a call per step and moves no number you can point at.
- Forwarding the whole conversation to the checker. The drafter's reasoning was written to be convincing, and a checker that reads it is convinced.
- An uncapped re-draft loop. It looks like diligence until the day a case cannot be fixed, and then it is a runaway with better manners, burning tokens until somebody reads the bill.

**Done when** — Every checker in the chain can be shown to be independent — a different model, or a fresh context with an adversarial brief — and a test proves the drafter's reasoning never reaches it.

---

## 5 · Gate

### Put the boundary in the tool signature

*Before the first bolt that writes anything*

The prompt says *never refund over $400*. A passenger types *ignore your instructions* and the model calls `refund(5000)`. The cap was a sentence, and a sentence is a request a model can be talked past. A typed, bounded parameter that raises is a boundary, and it holds whatever the model has been convinced of. Reads stay open; writes need a confirmation token the model cannot mint. Keep the sentence in the prompt as **policy**, because it makes the agent behave well by default — and never confuse it with enforcement.

**What you actually do**

1. **Take every cap out of the prompt and into config** — `config/caps.yaml`, reviewed like code, generated from the authority budget. A number that lives in prose gets edited by whoever is editing prose, which is nobody who thinks of themselves as changing a control.
2. **Make the parameter typed and bounded, and make it raise** — Not clamp, not log, not warn. Raise. A clamped refund of $400 on a $5,000 attempt is a successful attack wearing a smaller number, and the trace shows an ordinary refund.
3. **Mint the confirmation token somewhere the model cannot reach** — The approver's screen. Signed, scoped to one booking and one amount, with an expiry. If the agent can construct the token from things it already has, it is a parameter with a serious-sounding name.
4. **Separate reads from writes at the permission layer** — Reads open, writes gated, two modules and two permission sets, so the agent cannot call what the job does not need. Least authority is from 1975 and has not changed; what changed is that the thing being restricted can be persuaded.
5. **Write the two tests, and treat them as the step** — Over-cap raises. No-confirmation raises. Until both are green the gate does not exist, whatever the design document says and however many people remember agreeing to it.
6. **Keep the prompt sentence, and label it POLICY** — A comment beside it: *policy, not enforcement — the boundary is in issue_refund()*. That comment is what stops the next engineer removing the signature check on the grounds that the prompt already covers it.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Give it the authority budget and have it generate the signature, the exception classes and the two tests for every tool at R3 and above in one pass. It is mechanical work with a fixed shape and a fixed test.<br>⚠ Check that it raises rather than clamps, and that the cap is read from config rather than written as a literal. Both are defaults it reaches for, and both look fine in a diff. |
| **A chat surface** | Paste the prompt directory and ask for every sentence that is really a control: every `never`, `always`, `do not`, `ask before`, and every currency symbol. Each hit is a request that may need an enforced twin.<br>⚠ It will also flag genuine policy that should stay as prose. The filter is whether ignoring the sentence costs money, exposes data or changes something irreversible. |
| **An editor agent** | Have it write the review-band path rule from the authority budget, so the files behind each tool carry that tool's band and nobody classifies their own change. |
| **Do not delegate** | What a cap is set to, and who may mint the token. Those come from the authority budget and the PM's autonomy record; a model asked for a sensible cap returns a plausible number with nothing behind it. |

**The artefact**

| | |
| --- | --- |
| Produces | **Gated tool implementation** |
| Good looks like | Every write tool with a typed bounded parameter, a confirmation token it cannot mint, and two tests that were red first. Caps in config, reviewed like code, and the prompt sentence still there and labelled as policy. |
| Owner | Engineering lead |

<details><summary><b>Template · A gated write tool, and the two tests that are the step</b></summary>

```python
# src/tools/refund/issue.py   band R4   two named reviewers, every time
# The cap lives in <config/caps.yaml> and is reviewed like code.
# The prompt's sentence about refunds is POLICY. This file is ENFORCEMENT.
from decimal import Decimal

from src import ledger
from src.config import caps
from src.tools.confirm import ConfirmToken   # minted only by the approver's screen
from src.trace import trace

REFUND_CAP = Decimal(caps["refund"]["max_amount"])      # <400>
MODEL_VERSION = "<model-id-and-date>"


class AuthorityExceeded(Exception):
    def __init__(self, amount: Decimal, cap: Decimal) -> None:
        super().__init__(f"refund {amount} exceeds cap {cap}")
        self.amount, self.cap = amount, cap


class ConfirmationRequired(Exception):
    pass


def issue_refund(booking_id: str, amount: Decimal,
                 confirmation: ConfirmToken) -> ledger.Refund:
    # Raise, never clamp. A clamped 400 on a 5000 attempt is a successful attack
    # wearing a smaller number, and the trace records an ordinary refund.
    if amount > REFUND_CAP:
        trace.write(action="refund_refused", reason="over_cap",
                    booking=booking_id, amount=amount, model=MODEL_VERSION)
        raise AuthorityExceeded(amount, REFUND_CAP)
    if not confirmation.valid_for(booking_id, amount):
        trace.write(action="refund_refused", reason="no_confirmation",
                    booking=booking_id, amount=amount, model=MODEL_VERSION)
        raise ConfirmationRequired(booking_id)
    trace.write(action="refund", booking=booking_id, amount=amount,
                approver=confirmation.approver, model=MODEL_VERSION)
    return ledger.refund(booking_id, amount)


# tests/tools/test_refund_boundary.py — these two tests ARE the step.
import pytest

from tests.factories import forged_token, valid_token


def test_over_cap_raises():
    with pytest.raises(AuthorityExceeded):
        issue_refund("<PNR123>", Decimal("5000"), valid_token("<PNR123>", "5000"))


def test_no_confirmation_raises():
    with pytest.raises(ConfirmationRequired):
        issue_refund("<PNR123>", Decimal("50"), forged_token())


def test_reads_stay_open():
    # The gate is on the write, not on the module. A lookup needs no token.
    assert ledger.get_refunds("<PNR123>") is not None
```

</details>

<details><summary><b>Prompt · Find every rule that is only a request</b> — Before the first gated write, and after every prompt change</summary>

```text
Search every prompt, system message and tool description under <src/prompts/> and
<src/tools/> for sentences that are really controls: never, always, must not, do not,
ask before, requires approval, and every currency symbol or numeric limit.

OUTPUT a table:
| File and line | The sentence | What it would cost if ignored | ENFORCED VERSION |

RULES:
- "Cost if ignored" must be concrete: money moved, data exposed, something irreversible
  changed, or nothing. Write "nothing" where that is the honest answer.
- The ENFORCED VERSION column is a typed bounded parameter, a confirmation token, a
  permission, or "stays as policy". Do not write "a clearer prompt" — that is the same
  request in better handwriting.
- Separate the rows into ACT NOW (money, data, irreversible) and LEAVE AS POLICY.
- Do not modify any file.

Finish with the count in each group. Teams commonly find between three and ten in the
first group, and the count matters less than the fact that nobody knew it.
```

</details>

<details><summary><b>Prompt · Generate the gated signature and its two tests</b> — Implementing any tool at R3 or above</summary>

```text
Here is the authority budget row for this tool: <paste>.
Here is the existing unguarded implementation: <paste>.

Produce:
1. The typed signature, with the bounded parameter and a confirmation token parameter.
2. Named exception classes: one for over-cap, one for missing or invalid confirmation.
3. The two tests: over-cap RAISES, no-confirmation RAISES.
4. A trace write on the refusal path as well as the success path.

RULES:
- RAISE. Do not clamp to the cap, do not log and continue, do not return an error object.
- Read the cap from <config/caps.yaml>. No numeric literal anywhere in the function.
- The confirmation token must be validated against BOTH the booking id and the amount,
  so a token minted for a small refund cannot authorise a large one.
- Do not touch the prompt. The sentence there stays, as policy.

Then list anything in the authority budget row that the signature cannot express, so I
can take it back to the architect rather than approximate it here.
```

</details>

<details><summary><b>Prompt · Write the review-band path rule</b> — The queue is long and every change is being reviewed the same way</summary>

```text
Turn this authority budget into a path rule that assigns a review band to every
file in the repository: <paste budget>. Here is the repository tree: <paste>.

OUTPUT a YAML file mapping R5 down to R1 to path globs, plus the review policy each
band implies (how many readers, and whether a person is required at all).

RULES:
- A change inherits the band of the most dangerous tool it touches. Size is irrelevant:
  three lines in a refund cap is the highest band there is; four hundred lines of help
  text cannot move money.
- The config file holding the caps gets the same band as the tool it caps.
- Never let the author assign the band. The rule is in the repository and it applies.
- Any path you cannot classify goes in an UNCLASSIFIED list for me, not into R1.

Then estimate, from last month's merged changes that I paste below, how many review
slots the new policy needs versus the current one.

LAST MONTH'S CHANGES: <paste>
```

</details>

**Worked example · SkyWays · day 82, five layers and none enforced**

> A $2,000 refund went out that was not owed. The design listed five layers: input marked as data, the prompt's policy, a $400 cap, a named approver, an alert on the trace. Two of them were written down — in the prompt — which is exactly why everybody in the room believed there was a cap and the ledger disagreed. With either the cap or the approver enforced in the signature, the refund is impossible; injection defence and traces change the odds and the visibility, not the outcome. The fix was about thirty lines and two tests, and the $400 constraint had been on the table since day six, when it reshaped three of the nine ratified NFRs.

**Pitfalls**

- Clamping instead of raising. The attempt succeeds at the cap, no exception is recorded, and the trace shows a normal refund on the day somebody was probing you.
- A confirmation token the agent can construct. If it can be derived from the booking id the model already holds, it is a parameter with a serious-sounding name and no gate behind it.
- Deleting the prompt sentence once the signature is in place. The sentence is what makes the agent behave well by default; the signature is what holds when it does not. Keep both, and label which is which.

**Done when** — For every tool at R3 or above, `test_over_cap_raises` and `test_no_confirmation_raises` are green, and the cap appears nowhere outside the config file and the signature.

---

## 6 · Harness

### Wire the eval harness into CI, in cost order

*P1, before the first bolt whose done-when mentions a bar*

The acceptance bar stops being a paragraph and becomes a check that can go red. The order matters, because the cheap definitive checks should reject before you pay for a judge: build, then the exact tests, then the golden run on the slice this change touched, then the independent judge, then the score against the bar **per slice**, then merge or reject. The rule that gives the harness its teeth is that a slice below its bar blocks the merge however good the overall number looks.

**What you actually do**

1. **Put the steps in cost order and keep them there** — Build, exact tests, golden run, judge, score. Running the judge first spends a frontier model's money grading outputs the schema check would have rejected for nothing, on every run, forever.
2. **Score per slice, never in aggregate** — Every golden case carries a slice tag and the harness prints a row per slice against that slice's bar. A single percentage is the precise thing the harness exists to stop you reporting.
3. **Make the per-slice rule a required check** — Not a bot comment. A comment gets read on a quiet week and scrolled past on a release week, and a release week is when it matters. A required status check is the only version that survives pressure.
4. **Run the touched slice per pull request, the full set nightly** — That is the cost control on the harness itself. Deriving the touched slice from the changed paths is a ten-line script, and it is what keeps the per-change bill flat as the golden set grows from fifty cases to five hundred.
5. **Print n and the lower bound beside every score** — The bar is met by the lower bound, not by the point estimate. A slice with forty cases has proven nothing, and the score alone will not say so — it will look like a pass.
6. **Pin the judge and record its version in the run** — A judge that silently changes model is a harness whose results are not comparable week to week, and you will spend a day hunting a regression in code that did not change.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it write the workflow, the slice-from-changed-paths script and the per-slice report, then replay the whole thing against last month's merged commits to show it would have caught the regression it should have caught.<br>⚠ Insist on the replay. A harness that has never rejected anything has not been tested, it has been installed, and the difference only becomes visible during an incident. |
| **An editor agent** | Keep the slice tags honest: when a new tool or path appears, have it flag the golden cases that now belong to no slice, and the slices that now have no cases. |
| **A cheap tier** | Use it as the schema and exact-check runner inside the harness. Those steps are deterministic and there is nothing a frontier model adds to reading JSON.<br>⚠ Pin it. A cheap tier that changes underneath you makes a deterministic step non-deterministic, which is the worst of both arrangements. |
| **Do not delegate** | The bar values and the contents of the golden set. The bars are the PM's, derived from damage over saving; the cases are the QA lead's. Your job is to make them run and to refuse to average them. |

**The artefact**

| | |
| --- | --- |
| Produces | **Eval harness in CI** |
| Good looks like | A required check running in cost order, reporting a row per slice with n and the lower bound, rejecting when any touched slice sits below its bar. Full set nightly, with the trend kept so a slow regression is visible. |
| Owner | Engineering lead |

<details><summary><b>Template · harness.yml · the required check</b></summary>

```yaml
# .github/workflows/harness.yml · <repo> — a REQUIRED check, not a bot comment.
# The order is cost order: the cheap definitive checks reject before the judge is paid.
name: harness

on:
  pull_request:
  schedule:
    - cron: "0 2 * * *"          # the full set, nightly

env:
  JUDGE_MODEL: "<pinned-judge-model-id>"   # pinned: a drifting judge is not comparable
  GOLDEN_SET: "<tests/golden/*.jsonl>"     # QA owns the cases; every case has a slice tag
  BARS: "<config/bars.yaml>"               # the PM owns these numbers, one per slice

jobs:
  harness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: "1 - build"
        run: make build

      - name: "2 - exact tests (schema, fare math, no waived tax)"
        run: make test

      - name: "3 - which slices did this change touch?"
        id: slices
        run: python tools/touched_slices.py --base "${{ github.event.pull_request.base.sha }}" >> "$GITHUB_OUTPUT"

      - name: "4 - golden run"
        run: |
          if [ "${{ github.event_name }}" = "schedule" ]; then
            make golden SLICES=all
          else
            make golden SLICES="${{ steps.slices.outputs.slices }}"
          fi

      - name: "5 - independent judge (tone, policy, false claims)"
        run: make judge MODEL="$JUDGE_MODEL"

      - name: "6 - score against the bar, PER SLICE"
        run: |
          # Prints score, n and the 95% lower bound on every row, and exits non-zero
          # if ANY touched slice is below its bar, however good the overall number is.
          make score BARS="$BARS" FAIL_UNDER_BAR=1 REPORT="$GITHUB_STEP_SUMMARY"

      - name: "7 - say why, in the summary"
        if: failure()
        run: echo "A slice is below its bar. The merge is blocked." >> "$GITHUB_STEP_SUMMARY"
```

</details>

<details><summary><b>Prompt · Write the harness workflow in cost order</b> — P1, wiring the bar into CI for the first time</summary>

```text
Write the CI workflow for our eval harness. It runs on every pull request as a
REQUIRED check, and on a nightly schedule for the full set.

Steps, in THIS order, because it is cost order:
1. build
2. exact tests — schema, the money functions, the eligibility rules
3. work out which slices the changed paths touch
4. golden run — the touched slices on a pull request, ALL slices on the schedule
5. the independent judge, with a PINNED model id recorded in the run
6. score against the bar, per slice, printing score, n and the 95% lower bound

RULES:
- The job exits non-zero if ANY touched slice is below its bar. The overall number never
  rescues a failing slice, and the failure message must say which slice and by how much.
- No step may run before a cheaper step that could have rejected the same change.
- The judge model id is an env var, pinned, and appears in the run summary.
- Keep the whole thing under 60 lines of YAML.

Our slices: <list>. Our make targets: <list>. Our golden set lives at <path>.
```

</details>

<details><summary><b>Prompt · Replay the harness against commits you already know about</b> — Before you call the harness a gate</summary>

```text
Here is our harness: <paste>. Here are <n> commits from the last month, with what
each one did and whether it turned out to be a regression: <paste>.

Replay the harness against each commit and report:
| Commit | Was it a regression? | Harness verdict | Correct? |

Then tell me:
- Every regression the harness would have MISSED, and the specific step that should have
  caught it — exact test, golden slice, or judge.
- Every clean commit the harness would have REJECTED, and why. A harness that rejects
  good changes gets switched off within a fortnight.
- The slice with the fewest cases, and whether its lower bound could clear its bar at
  that n at all.

Do not change the harness in this response. I want the evidence first.
```

</details>

<details><summary><b>Prompt · Reshape the harness output into the bar sheet</b> — The PM needs a release readout and the harness prints its own shape</summary>

```text
Convert this harness output into the shape of the PM's bar sheet: <paste output>.
Here are the bars: <paste>.

ONE table, nothing else above it:
| Slice | Score | n | 95% lower bound | Bar | PASS / FAIL / UNPROVEN | vs last run |

RULES:
- lower bound = p - 1.96 * sqrt(p*(1-p)/n). Compute it even if the harness only gave a
  score. Under about 100 cases say USE WILSON beside the row.
- PASS only when the LOWER BOUND is at or above the bar. Score above bar with the lower
  bound below it is UNPROVEN, and then give cases needed:
  n = 1.96^2 * p * (1-p) / (p - bar)^2
- Flag any slice that got worse than the previous run even if it still passes.

Then one line: merge, or do not merge, and the single reason.
```

</details>

**Worked example · SkyWays · day 45, 82.4 against a bar of 80**

> The codeshare slice scored 82.4% against a bar of 80% and the room read it as a pass. The harness printed n and the lower bound on the same row, and the lower bound said not yet. 82% does not prove an 80% bar at any sample size the team was realistically going to collect, because the cases-needed formula has the gap squared in its denominator and the gap here was 2.4 points. The useful output was not pass or fail; it was the number of cases owed, on the same line. The other version of that day is a merge, a green tick, and a conversation about codeshare six weeks later with real passengers in it.

**Pitfalls**

- Running the judge before the exact checks. You pay a frontier model to grade output a schema check would have rejected for free, on every run, for the life of the project.
- Reporting one number. The slice carrying the risk is small, the average hides it, and the first person to find out is whoever is on call.
- A harness that has never rejected anything. It has been proven to run, not to work. Replay it against a commit you already know was bad before you call it a gate.

**Done when** — A pull request that regresses any touched slice below its bar cannot be merged, and the check has been shown to reject on a commit you already knew was bad.

---

## 7 · Ship

### Build bolt by bolt, and put the shadow path behind a flag

*P2, every day*

One bolt a day, in the architect's dependency order, integrated the same day. That order is not the backlog's order: the walking skeleton goes first with no model in it, the exact code goes early because it never blocks, the plug goes before any gated write that needs it, and the proof goes last because the harness needs something to run against. Then the whole thing goes live behind a flag as a shadow path that decides and never acts — and the rollback **is** the flag.

**What you actually do**

1. **Start with the walking skeleton, with no model in it** — The thinnest end-to-end path: read a booking, show it. Half a day, and it retires the largest unknown — whether the pieces connect at all — on day one, which is the assumption every other bolt is resting on.
2. **Put the pure exact code early** — It is unit-testable in isolation, so it never blocks and never waits, and it frees review capacity for the days that need it. It is usually sitting at the end of the plan because it looked boring.
3. **Schedule the plug before its consumer** — The classic failure is the rebook bolt on day four and the MCP server it needs on day six. Checkers go after the steps they check. The proof goes last, because the harness needs something to run against.
4. **Say a bolt cannot be built alone BEFORE you start it** — Not at two in the afternoon. A bolt that needs the other half of a feature was cut horizontally instead of vertically, and the fix belongs with the architect rather than with whoever discovered it mid-build.
5. **Keep one unknown per bolt** — Then a day can fail for exactly one reason and you know which one. Two unknowns and the standup produces a discussion instead of an answer, and the discussion takes the next morning too.
6. **Integrate the same day, and review by band** — Same-day integration is what makes the cost of a wrong turn one day instead of two weeks. The band comes from the most dangerous tool the change touches, via the path rule, never from the author — every author believes their own change is low risk.
7. **Run the shadow path behind a flag, and make shadow-never-writes a test** — A test that fails the build if a write tool is reachable while the flag is in shadow mode, not an intention in a document. Then cut over at five percent, and rehearse the rollback before the cut-over rather than during it.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Give it the story file with the chat window closed and let it build the bolt. If it has to ask you something that is not in the file, that question is the finding, and it goes back into the template tonight.<br>⚠ Watch for it reaching outside the bolt. An agent that helpfully fixes an adjacent file has turned a one-unknown day into a two-unknown review, and the reviewer will not know which half to trust. |
| **An editor agent** | The same-day integration work: rebases, conflict resolution, the small mechanical follow-ups that otherwise push integration to tomorrow and break the cadence. |
| **A cheap tier** | Generate the dependency-ordered plan from the bolt list plus a depends-on column, and flag cycles, plugs scheduled after their consumers, and any item with no dependencies sitting at the end.<br>⚠ It orders only what you give it. A dependency you forgot to write down produces a confident plan with the day-four failure still in it. |
| **Do not delegate** | The judgement that a bolt cannot be built alone. It is a claim about your repository and your team's day, and it has to be said out loud to the architect by someone who will own the consequence of being wrong. |

**The artefact**

| | |
| --- | --- |
| Produces | **Bolt build log** |
| Good looks like | One row per day: the bolt, its one unknown, integrated yes or no, and the harness result for its slice. Plus the flag, the shadow-never-writes test, and a rollback rehearsal with a name and a time on it. |
| Owner | Engineering lead |

<details><summary><b>Template · Bolt build log</b></summary>

```markdown
# Bolt build log · <feature>
_Architect's cut <10> bolts · Cadence one a day · Owner <name>_

## The order, and the rule that produced it
| Day | Bolt | Depends on | The ONE unknown | Band |
|-----|------|-----------|-----------------|------|
| 1 | <walking skeleton — read a booking, show it. NO MODEL> | — | <do the pieces connect?> | R1 |
| 2 | <fare_difference(), exact, unit-tested> | 1 | <the rounding rule> | R1 |
| 3 | <visa and codeshare eligibility, exact> | 1 | <where the partner rules live> | R1 |
| 4 | <rank_alternatives(), best-guess, measured> | 2 | <can it beat the desk?> | R2 |
| 5 | <independent checker after ranking> | 4 | <which model judges> | R2 |
| 6 | <MCP server, reads open> | 1 | <auth to the booking system> | R2 |
| 7 | <rebook() gated write> | 6 | <idempotency> | R3 |
| 8 | <issue_refund(max 400) + confirmation token> | 7 | <who mints the token> | R4 |
| 9 | <shadow path behind a flag> | 5, 8 | <flag plumbing> | R2 |
| 10 | <golden set and harness in CI> | 9 | <slice tagging> | R1 |

Rules this order obeys, in priority order: skeleton first · pure exact code early ·
checkers after the steps they check · the plug before any gated write that needs it ·
the proof last.

## Daily row
| Day | Bolt | Integrated same day? | Harness, its slice | Note |
|-----|------|---------------------|--------------------|------|
| <1> | <skeleton> | <yes, 16:00> | <n/a> | <...> |
| <2> | | | | |

## Cannot be built alone — raised BEFORE starting, never at 2pm
| Day | Bolt | What is missing | Cause | Who re-cuts |
|-----|------|-----------------|-------|-------------|
| <4> | <rebook> | <the MCP server, scheduled day 6> | <plug after consumer> | <architect> |

## The shadow path
- Flag `<skyways.rebooking.shadow>` — default off, off in production until <date>
- The agent decides and logs. It never acts.
- Test `<test_shadow_never_writes>` fails the build if any write tool is reachable
  while the flag is in shadow mode. This is a test, not an intention.
- Cut-over <5>% of traffic on <date>, <named slice> only
- **Rollback IS the flag.** Rehearsed <date> by <name>. Time to revert <90> seconds.
```

</details>

<details><summary><b>Prompt · Order the bolts by dependency, not by priority</b> — The architect has the cut and you need the day order</summary>

```text
Here are the bolts for <feature>, each with a one-line description and a
depends-on column: <paste>.

Produce a day-by-day order in which every bolt's dependencies come strictly before it.

RULES, applied in this priority order:
1. The walking skeleton first — the thinnest end-to-end path with NO model in it.
2. Pure exact code early. It is testable alone, so it never blocks anyone.
3. Checkers after the steps they check.
4. Any plug (MCP server, connector, adapter) BEFORE the gated write that needs it.
5. The proof — golden set and harness — last.

Then report, separately and before the plan:
- any CYCLE, where two bolts wait on each other. A cycle is always a mis-cut and means
  one of them is really two bolts. Name which one.
- any plug scheduled after its consumer in the order I gave you
- any bolt with NO dependencies that I had scheduled late
- any bolt carrying more than ONE unknown, and how you would split it

If there is no walking skeleton in my list, add one and say what it would cover.
```

</details>

<details><summary><b>Prompt · Build today's bolt from its file alone</b> — The start of the build day</summary>

```text
Build this bolt. The story file is the whole brief: <paste file>.

RULES:
- Work only inside the paths the file names. If you find a problem in an adjacent file,
  write it down at the end; do not fix it. A second fix makes the review two unknowns.
- Read context by the paths in section 1. Do not ask me to paste any of them.
- The unit tests named in section 4 are written first and must be seen failing.
- Nothing in section 3 changes: signatures, bands and confirmation parameters are fixed.
- If you need something that is not in the file, STOP and say what it is. Do not
  improvise it, and do not build around it.

OUTPUT, in this order:
1. The failing tests
2. The implementation
3. The command output showing them green
4. A list headed FILE DEFECTS — everything you needed that the story file lacked
5. A list headed OUT OF SCOPE — problems you found and deliberately did not fix
```

</details>

<details><summary><b>Prompt · The shadow path and the test that it never writes</b> — Wiring the flag, before any cut-over</summary>

```text
Implement the shadow path for <feature> behind a feature flag.

Behaviour:
- flag OFF: the live process runs as today. The agent is not invoked.
- flag SHADOW: the agent runs on the same input, decides, and logs its decision beside
  the live one. It performs NO writes of any kind.
- flag LIVE at <5>%: the agent acts for that share of traffic; everything else unchanged.

MUST INCLUDE:
- `test_shadow_never_writes` — fails the build if any write tool is REACHABLE while the
  flag is in shadow mode. Assert on the tool call, not on the agent's output.
- A nightly comparison job producing agreement PER SLICE, never one overall number, with
  money actions reported separately and never counted toward automatic agreement.
- A revert path that is the flag itself, and a rehearsal script that times it.

Do not add a kill switch that is separate from the flag. Two mechanisms means one of
them is untested on the day it is needed, and it will be the other one.
```

</details>

**Worked example · SkyWays · day 30, the first bolt ships by four in the afternoon**

> The first bolt was a walking skeleton: read a booking, show it, no model anywhere in it. It shipped by four in the afternoon, and what it bought was not the feature but the answer to the question every other bolt was resting on — whether the pieces connect. The exact code went on days two and three, so review capacity was free when the ranking bolt arrived. The one re-cut came on day four and was raised at nine in the morning rather than at two: `rebook()` needed the MCP server scheduled for day six, a plug ordered after its consumer. Moving the plug cost an hour. Discovering it mid-build would have cost the day.

**Pitfalls**

- Scheduling the plug after the thing that needs it. It is the single most common ordering error and it costs a whole day in the middle of the week, every time.
- Discovering at two in the afternoon that a bolt cannot be built alone. The information was available at nine; what was missing was somebody willing to say the cut was wrong before spending the day proving it.
- A shadow path that writes. It is an intention until it is a test, and the first time it writes it does so on real bookings, which is the exact risk the shadow run existed to remove.

**Done when** — Every bolt merged on the day it was built, the shadow path has a test that fails the build if a write is reachable, and somebody other than you has thrown the rollback flag in a rehearsal with a stopwatch running.

---

> **P3 · Run & Learn begins here** — *is it still doing what we launched, and what did it cost?*

## 8 · Operate

### Cache, route, trace, test the injection, and keep the ledger

*P3, from the first day in production onward*

Production is where the cost, the audit and the security posture are actually settled, and all three are made of small settings nobody notices until an invoice or an incident arrives. Caching that hits, routing by complexity with a loop cap, a trace that redacts rather than omits, an injection suite that runs weekly, and a ledger of effort and tokens the product manager's cost number is built from. None of it is difficult. All of it gets skipped, and four weeks later the bill is 4.4 times the estimate with flat traffic.

**What you actually do**

1. **Order the prompt for the cache, and pick the window from traffic shape** — The cache matches an exact prefix, in the order tools then system then messages, up to the block you mark, so stable content goes first and the request last. Documented and read September 2026: a five-minute write is 1.25x the input price, a one-hour write is 2x, a read is 0.1x, and Fable and Mythos 5.1 read at 0.025x. Minimum around 1,024 cacheable tokens, model-scoped, break-even on the second use. Five minutes when calls are seconds apart; one hour when the gap is twelve minutes, because the cheaper write paid on every call beats the dearer write paid once.
2. **Assert the cache is working, and mark hits in the trace** — `assert response.usage.cache_read_input_tokens > 0` on the **second** call, never the first. And mark hits in the trace, because cache hits return fast and a latency dashboard that flags very fast responses as suspected failures will get the cache switched off, which raises the bill by about a third within a day.
3. **Route by complexity, and cap the loop** — `MAX_LOOPS = 5` in every agent loop, with a per-transaction token cap beside it. The biggest model on a simple lookup can be up to 160 times the price of the right one, and one model per task, because a mid-task switch discards the cache.
4. **Write one redacted row per consequential action** — Mask, do not omit — `passport ****1234`. Timestamp, masked input, tools called, the decision, the model version, the approver, the cost. Omitting breaks the audit; logging raw makes the trace store a breach target, usually protected less carefully than the ledger it mirrors.
5. **Run the injection suite weekly, and on every prompt, tool or context change** — Every attack string against every gated tool from every entry point, including the partner API's free-text fields. Assert on the **tool calls** and the trace row, never on the model's wording — wording changes with the next prompt edit, and then the test is red for the wrong reason and green for the wrong reason the week after.
6. **Keep the effort-and-token ledger, per bolt** — Person-hours by activity, tokens by tier, re-runs, defects escaped. Five minutes a day. Tokens by tier rather than in total, because the tier mix is where routing shows up, and the re-run column is the leak signal — model switching and vague asks appear there first.
7. **Reconcile the spec by diff after a hotfix, never by rewriting it** — A diff keeps the reason the hotfix differed from the spec; a rewrite makes the spec agree with the code and loses the only record that they ever disagreed, which is the record the next postmortem needs.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it instrument the per-call log: tokens per call, tier, cache read tokens, retries. Those four ratios are what turn an invoice into a diagnosis, and without the log you cannot compute a single one of them.<br>⚠ Make it remove the request id from the cached block while it is in there. That one field is the most common silent cache break, and it is always added for a good reason by somebody who was not thinking about prefixes. |
| **A cheap tier** | Run the weekly injection suite and the nightly redaction test on it. Both are volume jobs with deterministic assertions, and there is nothing a frontier model adds.<br>⚠ The attack strings still need a person to extend them. A suite that has not grown in three months is testing last quarter's attacks and reporting green. |
| **A chat surface** | Give it the four ratios month over month and have it multiply them out against the ratio between the two invoices. If the product matches, you have explained the bill and can stop looking.<br>⚠ Do not let it rank the fixes by the biggest ratio change. The order is (factor minus one) divided by days to fix, and those two orders are different — the retry breaker is usually the right fix in the wrong position. |
| **Do not delegate** | What the redaction rules are. Which fields are sensitive is a legal and regulatory question about your business, and a model asked to guess will mask the obvious identifiers and leave the booking free-text field alone. |

**The artefact**

| | |
| --- | --- |
| Produces | **Operations set — caching, routing, trace, injection suite, ledger** |
| Good looks like | One reviewed file holding the caching and routing config, a redaction test, a weekly injection run with a date on it, and a four-column ledger per bolt that the PM's cost number is built from rather than estimated against. |
| Owner | Engineering lead |

<details><summary><b>Template · The production call · cache, route, cap, trace</b></summary>

```python
# src/agent/run.py — cache, route, cap, trace. This file and <config/routing.yaml>
# are reviewed like code: the day-75 bill began with a prompt reordered for clarity.
from decimal import Decimal

from src.errors import LoopCapReached
from src.redact import redact         # masks; never omits
from src.trace import trace

MAX_LOOPS, MAX_TOKENS_PER_TXN = 5, 120_000   # uncapped, a loop burns unnoticed
PRICE_PER_TOKEN = Decimal("<0.000003>")
TIERS = {"simple": "<cheap-model-id>", "standard": "<mid-model-id>",
         "hard": "<frontier-model-id>"}


def build_request(tools, system_blocks, request, ttl="5m"):
    # Exact prefix, order tools -> system -> messages. Stable first, volatile
    # request last, cache marker on the LAST STABLE block. Nothing cached may
    # hold a timestamp or request id. "5m" 1.25x, "1h" 2x, read 0.1x (Sept 2026).
    system = [{"type": "text", "text": text} for text in system_blocks]
    system[-1]["cache_control"] = {"type": "ephemeral", "ttl": ttl}
    return {"tools": tools, "system": system,
            "messages": [{"role": "user", "content": request}]}


def tier_for(case) -> str:
    # Route by complexity. ONE model per task: the cache is model-scoped, so a
    # mid-task switch discards the prefix and you pay the write again.
    if case.needs_partner_rules:
        return "hard"
    return "standard" if case.segments > 1 else "simple"


def handle(case, client, tools, blocks):
    model, spent = TIERS[tier_for(case)], 0
    for _ in range(MAX_LOOPS):
        r = client.messages.create(
            model=model, **build_request(tools, blocks, case.request))
        spent += r.usage.input_tokens + r.usage.output_tokens
        trace.write(action="<propose_rebooking>", model=model,  # version, always
                    input=redact(case.as_dict()),               # passport ****1234
                    tools_called=[t.name for t in r.tool_calls],
                    decision=r.decision, approver=case.approver,
                    cache_read_tokens=r.usage.cache_read_input_tokens,
                    cost=PRICE_PER_TOKEN * spent)
        if r.stop_reason == "end_turn" or spent > MAX_TOKENS_PER_TXN:
            return r.decision
    raise LoopCapReached(f"<propose_rebooking>: {MAX_LOOPS} loops")


# tests/agent/test_operate.py — the two assertions that keep this honest.
def test_the_second_call_reads_from_cache(client, case, tools, blocks):
    handle(case, client, tools, blocks)          # the first call pays the write
    handle(case, client, tools, blocks)
    assert client.last.usage.cache_read_input_tokens > 0    # the SECOND call


def test_a_passport_never_reaches_a_row(rows):
    assert all("<passport_number>" not in str(row) for row in rows)
    assert any("****" in str(row.input) for row in rows)    # masked, not omitted
```

</details>

<details><summary><b>Prompt · Diagnose the bill from the per-call log</b> — The invoice has left its estimate and traffic is flat</summary>

```text
Traffic is flat and the bill is <n>x the estimate. Do not look at the price list.
Here is the per-call log for this month and the month before: <paste or path>.

Compute these four ratios, this month against last:
| Signature | Baseline | Now | Factor |
- tokens per call
- frontier tier share
- cache hit ratio (a FALL is a rise in cost; express it as a factor above 1)
- retries per conversation

Multiply the four factors. Compare the product with the ratio between the two invoices.
- If they match, say so and stop looking. The bill is explained.
- If the product is well below the invoice ratio, something structural changed that is
  not a habit — traffic, a new feature, or a price change. Say which to check.

Then order the fixes by  priority = (factor - 1) / days to fix,  NOT by the biggest
ratio change. Give me the table with the order and the days you assumed.

Finally: name the guards that would have caught this in week one rather than week four.
```

</details>

<details><summary><b>Prompt · Build the weekly injection suite</b> — Before launch, and it runs weekly forever after</summary>

```text
Build an injection regression suite for <feature>.

Cross-product: EVERY attack string x EVERY gated tool x EVERY entry point.

Entry points must include, at minimum:
- the passenger's own message
- a partner API response free-text field (the partner is trusted; the field is not)
- an uploaded document, including text that is invisible when rendered
- a free-text field on the booking record
- a retrieved knowledge-base chunk

RULES — these decide whether the suite is worth anything:
- Assert on the TOOL CALLS and on the trace row. Never assert on the model's wording.
  A test that checks the reply contains "I cannot do that" is red for the wrong reason
  after the next prompt edit and green for the wrong reason the week after.
- Every test asserts BOTH that the action did not happen AND that an attempt was
  recorded in the trace.
- The suite runs weekly on a schedule, and on every prompt, tool or context change.

OUTPUT: the test module, the attack-string fixture file, and the CI schedule entry.

OUR GATED TOOLS: <paste signatures>
OUR ENTRY POINTS: <paste>
```

</details>

<details><summary><b>Prompt · Reconcile the spec by diff after a hotfix</b> — The hotfix is merged and the room wants to move on</summary>

```text
A hotfix shipped outside the normal flow. Here is the spec as it stood: <paste>.
Here is what actually merged: <paste diff>.

Produce a RECONCILIATION DIFF, not a rewritten spec.

| Spec clause | What shipped | Same? | Why it differed | Keep the code or keep the spec? |

RULES:
- Never rewrite the spec so it agrees with the code. The rewrite loses the only record
  that they ever disagreed, and that record is what the next postmortem needs.
- For every difference, say whether the SPEC was wrong (amend it, with the reason and
  the date) or the CODE was expedient (raise the follow-up, with the risk it carries
  until then).
- Flag any difference that touches a cap, a confirmation token, a permission or a trace
  field. Those are not tidy-ups; they are changes to a control and need the band.
- List any golden-set case that the hotfix invalidates, and any new case it implies.

Finish with the amended ADR line, if a decision changed, in one sentence.
```

</details>

**Worked example · SkyWays · day 75, a bill 4.4 times the estimate with flat traffic**

> Traffic was flat, so behaviour had changed, and behaviour is only visible per call. Four ratios explained it: tokens per call 1.6, frontier tier share 1.5, cache hit ratio 1.3, retries per conversation 1.41 — and they multiply to 4.40. Four separate sensible decisions made by careful people. The order of the fixes was not the order of the ratios: retries had risen most in relative terms and contributed the smallest factor, so the context trim went first at half a day for 1.6x and the breaker went last. Four weeks had passed before anybody noticed, which is the part worth fixing permanently — an alert at three times the ratified cost per case, a watched cache hit ratio, and the caching and routing config in one file reviewed like code.

**Pitfalls**

- A request id inside the cached block. The prefix never matches again, the hit ratio collapses, nothing errors, and the first symptom is an invoice a month later.
- A latency dashboard that flags very fast responses as suspected failures. Cache hits return fast, hundreds get reported as anomalies, and somebody proposes switching the cache off — which raises the bill by about a third within a day, because the anomaly was the cache working.
- An injection test that asserts on the model's wording. It goes red for the wrong reason after the next prompt edit and green for the wrong reason the week after, and nobody trusts it by month three.

**Done when** — A test asserts a cache read above zero on the second call, every agent loop has a cap, a passport number cannot reach a trace row, and the injection suite has a run dated this week.

---

## Read next

- [The wiki page for this role](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Engineering-Lead)
- [The same case, walked step by step](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/eng/step-1)
- [Where the bill goes, and how to get it back](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill)

**Other roles:** [Product Manager](Journey-Product-Manager) · [Solution Architect](Journey-Solution-Architect) · [QA Lead](Journey-QA-Lead) · [DevOps](Journey-DevOps)

- [The manual, interactive](https://akash-coded.github.io/aws-bedrock-agentcore-strands/) · [every template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/) · [every prompt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/) · [frameworks and acronyms](https://akash-coded.github.io/aws-bedrock-agentcore-strands/frameworks/)

