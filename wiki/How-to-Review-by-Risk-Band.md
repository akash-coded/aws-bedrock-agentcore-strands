# How to review by risk band

<!-- tutorial:lesson -->*New to this? Start with the lesson **[Review AI code by risk](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/review-ai-generated-code/)** — the idea step by step, with a worked problem. This page is the reference.*<!-- /tutorial:lesson -->

Nine pull requests, a four-day queue, and two reviewers who cannot read any faster. Adding a third
reviewer takes three months to hire and the agent will produce more changes long before then.

**The policy is the bottleneck, not the people.** It treats nine changes as equally dangerous.

Run it live:
[simulation](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/review) ·
[queue calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/queue).

### At a glance

| | |
| --- | --- |
| **Reach for it when** | The queue is days long and the policy is two senior reviewers on everything. |
| **Owner** | Engineering lead |
| **Phase** | P2 · Build & Prove |
| **Closes** | [Delivery](The-Eight-Loops#delivery) — P2 → P2 |
| **Moves** | 6 |
| **You leave with** | A band per tool, a generated path rule nobody can self-assess around, readers routed by band, and three comparable numbers every month |

---

## The six moves

<!-- picture:wikimap:review-band -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-review-band.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-review-band.dark.webp"><img alt="Six moves for reviewing by risk band, from reading the queue to measuring the policy" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-review-band.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-review-band.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| # | Move | Produces | Done when |
| --- | --- | --- | --- |
| 1 | [Read the queue](#1--read-the-queue-with-littles-law) | Slots needed, slots available, queue time | The queue is a number, not a feeling |
| 2 | [Band by what it touches](#2--band-by-what-the-change-touches) | A band per tool, R1 to R5 | No band anywhere was decided by the size of a diff |
| 3 | [Put the band in a path rule](#3--put-the-band-in-a-path-rule) | A generated rule file in the repository | Nobody classifies their own work |
| 4 | [Route the readers](#4--route-the-readers-by-band) | Reviewers per band, and what each reads for | Slots needed falls without a reviewer reading faster |
| 5 | [The harness-only lane](#5--open-the-harness-only-lane-and-count-the-escapes) | A lane charter and a weekly escape count | The escape count exists and somebody reads it |
| 6 | [Measure the policy](#6--measure-the-policy-or-it-will-be-repealed) | Three comparable numbers, monthly | All three are on one page next quarter |

Moves 1 to 4 are an afternoon. Move 5 is what makes the afternoon survivable, and move 6 is what
makes it survive the next reorganisation.

---

## 1 · Read the queue with Little's law

**Before any policy change. You cannot argue with a queue you have not measured.**

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

Two reviewers producing 4.5 slots a day is about 2.25 each — roughly two substantial reviews per
person per working day, which is what an experienced engineer with other duties actually manages.
That number is not a target to raise. Pushing it produces the review that scrolls to the bottom and
approves, which costs a slot and buys nothing.

Note what does not change between the columns: the number of changes, the number of people, and the
reading speed. Routing removes **eleven of the eighteen slots**, a 61% cut, by deciding that four
changes do not need a person and three need one rather than two.

### What you actually do

1. **Count slots, not pull requests.** A change requiring two reviewers consumes two slots. The
   queue is denominated in reading, and reading is the thing in short supply.
2. **Measure slots available from the last four weeks, not from a job description.** Count reviews
   actually completed and divide by working days. It is always lower than people expect, and the gap
   is the meetings.
3. **Hold capacity constant in every scenario you model.** A plan that needs a new hire is not a
   policy change; it is a recruitment request with a three-month lead time.
4. **Write the current policy down in one sentence.** "Two senior reviewers on everything" is usually
   nowhere in writing, which is why nobody has noticed it is the bottleneck.
5. **Compute the queue under three policies, not two.** Current, routed, and the pessimistic routing
   where the harness-only lane is closed. The third number is what you will need in move 5.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Pull the last quarter's merged pull requests from the API with their reviewers and timestamps, and compute slots consumed and slots available per day. An hour, and it replaces an argument with a table |
| **Chat LLM** | Model the queue under several policies at once: slots needed and queue time for each, with the arithmetic shown. It is reliable at this and it will not flatter the option you prefer |
| **Do not delegate** | The capacity figure. It is a statement about what your named colleagues can sustain, and an optimistic one turns a policy change into a broken promise |

### The artefact

<details><summary><b>Template · Queue reading</b></summary>

```markdown
# Review queue · <team> · <date>

## Capacity, measured — not assumed
| Reviewer | Reviews completed, last <n> weeks | Working days | Slots/day |
|----------|----------------------------------|--------------|-----------|
| <name> | <n> | <n> | <n> |
| <name> | <n> | <n> | <n> |
| **Total** | | | **<n>** |

Source: <where the counts came from>. This is capacity, not a target.

## The queue today
| | Value |
|---|------|
| Changes waiting | <n> |
| Policy, in one sentence | <e.g. two senior reviewers on everything> |
| Slots needed | <n> |
| Slots available per day | <n> |
| **Queue time = needed / available** | **<n> days** |

## Scenarios, same people, same reading speed
| Policy | Slots needed | Queue time | Change |
|--------|-------------|------------|--------|
| Today | <n> | <n> days | — |
| Routed by band (2 / 1 / 0) | <n> | <n> days | <n>% |
| Routed, harness-only lane CLOSED (2 / 1 / 1) | <n> | <n> days | <n>% |

The third row is the fallback if escapes appear. Know its cost before you need it.

## What we are not proposing
| Proposal | Why not |
|----------|---------|
| Hire a third reviewer | <3 months; the agent produces more changes before then> |
| Ask reviewers to read faster | <it produces the scroll-and-approve, which costs a slot and buys nothing> |
```
</details>

<details><summary><b>Prompt · Model the queue under several policies</b></summary>

```text
Here is a review queue: <n> changes waiting, <n> review slots available per day, and the
current policy is <describe>.

Here are the changes, each with the most dangerous thing it touches: <paste>.

1. Compute slots needed and queue time under the CURRENT policy.
   queue time = slots needed / slots available per day. Show the arithmetic.
2. Compute the same for each of these policies:
   - 2 reviewers on R4/R5, 1 on R2/R3, 0 on R1
   - 2 on R4/R5, 1 on R2/R3, 1 on R1 (the harness-only lane closed)
   - <any policy I add here>
3. Produce one table: policy, slots needed, queue time, percentage change.

Rules:
- Hold slots available per day CONSTANT across every scenario. Do not model hiring.
- Do not reduce the reviewer count on R4/R5 in any scenario. Two named readers on a
  money path is a constraint, not a variable.
- State the assumption you made about part-slots if a change needs a partial review.

Then one line: which policy, and the single reason.
```
</details>

**Done when** — the queue is a number with its arithmetic beside it, and you know the cost of the
fallback policy before you have needed it.

---

## 2 · Band by what the change touches

**Before anything is routed. Get this wrong and the routing routes the wrong things.**

Size measures typing. It does not measure danger.

| Change | Size | Touches | Band | Readers |
| --- | --- | --- | --- | --- |
| A · rewrite 400 lines of help text | Large | Nothing that acts | R1 | Harness, plus one at the end |
| B · alter 3 lines in the refund tool's cap check | **Tiny** | `issue_refund` | **R4/R5** | **Two, every time** |
| C · add a read-only search filter | Small | A read tool | R2 | Harness alone |

> **A change inherits the band of whatever it touches.** Three lines in a refund cap is the highest
> band there is; four hundred lines of help text cannot move money.

The ladder itself, which is the same one the governance page uses:

| Band | The action | The check |
| --- | --- | --- |
| **R1** | Reversible draft, sandbox | Review at the end |
| **R2** | Reversible change to real work | Review before merge |
| **R3** | Hard to reverse, small blast radius | Approve first |
| **R4** | Money, identity, policy | A **named** approver, every time |
| **R5** | Irreversible or safety-critical | Not delegated at all |

The bands describe **consequences**, not complexity. A trivial change to an R4 path is R4. A
fiendishly difficult change to a documentation generator is R1. The instinct to read "R5" as "hard"
is the single most common misreading, and it is the one that puts a senior reviewer on a
well-engineered R1 and a junior one on a three-line cap change.

### What you actually do

1. **Start from the authority budget, not from the repository.** The budget already says what each
   tool may do and to what limit. The band is that statement, restated as a review requirement.
2. **Band the tool, then the files behind it.** One band per tool, assigned once. Files inherit it
   from the tool they implement, so a band is never a per-change judgement.
3. **Ask what a wrong version of this change would do, at its worst.** Not what it is intended to do.
   The worst case is the band, which is why a cap check and the money it caps share one.
4. **Give shared code the band of its most dangerous caller.** A helper used by both the search tool
   and the refund tool is R4. This is the rule teams most often omit, and it is where the escape
   comes from.
5. **Band the configuration too.** Caps, routing tables, prompt files and feature flags change
   behaviour without changing code, and an unbanded config file is a hole straight through the
   policy.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Trace which files each tool's implementation reaches, including shared helpers, and produce the file-to-tool map. Doing this by hand is where the misses happen |
| **Chat LLM** | For each tool, ask what the worst consequence of a wrong change to it would be, in one sentence, then band from that. It is good at the worst case and you correct the boundaries |
| **Do not delegate** | The R4 and R5 assignments. They are a statement about money, identity and irreversibility in your business, and they are the rows an auditor will read |

### The artefact

<details><summary><b>Template · Band assignment, from the authority budget</b></summary>

```markdown
# Review bands · <product> · v<n> · <date>
Generated from: authority budget v<n>. Bands describe CONSEQUENCE, never difficulty.

## Per tool
| Tool | What a wrong change could do, at worst | Band | Reviewers | Files behind it |
|------|---------------------------------------|------|-----------|-----------------|
| <search_flights> | <return a wrong option; caller can ignore it> | R2 | 1 | <src/tools/search/**> |
| <rebook_passenger> | <move a passenger onto a wrong itinerary> | R3 | 1 | <src/tools/rebook/**> |
| <issue_refund> | <move money to the wrong account, irreversibly> | **R4** | **2 named** | <src/tools/refund/**> |
| <change_identity> | <unbounded> | **R5** | **not delegated** | <src/tools/identity/**> |

## Shared code — banded by its most dangerous caller
| Path | Called by | Highest caller band | Band |
|------|-----------|--------------------|------|
| <src/lib/money.ts> | <refund, payment> | R4 | **R4** |
| <src/lib/format.ts> | <all> | R4 | **R4** |

## Configuration — behaviour without code
| File | What it changes | Band |
|------|----------------|------|
| <config/caps.yaml> | <the refund cap in the tool signature> | **R4** |
| <config/routing.yaml> | <which model serves which request class> | R3 |
| <prompts/**> | <what the agent is asked to do> | R3 |

## Everything else
| Path | Band | Why |
|------|------|-----|
| <docs/**>, <content/**> | R1 | Cannot act |

## Disputes
| Path | Proposed | Assigned | Decided by | Date |
|------|----------|----------|-----------|------|
```
</details>

<details><summary><b>Prompt · Band a change by what it touches</b></summary>

```text
Here is a diff and the file-to-band map for our repository: <paste both>.

1. List every path the diff touches, with its band from the map.
2. State the band of the CHANGE: the highest band of any path it touches. Say which path
   set it.
3. If any touched path is NOT in the map, list it separately as UNBANDED and say which
   tool it appears to serve. An unbanded path is a gap in the map, not an R1.

Rules:
- Do not consider the size of the diff. Lines changed is not an input to this.
- Do not consider how well written the change is. The band is about consequence.
- If the diff touches shared code, say which tools call it and apply the band of the
  most dangerous caller.
- Never lower a band because the change "looks safe". The band belongs to the path.

Then, in one sentence, say what a wrong version of this change would do at its worst.
```
</details>

**Done when** — every tool, every shared helper and every behaviour-bearing config file has a band,
and no band anywhere was decided by the size of a diff.

---

## 3 · Put the band in a path rule

**The same afternoon. This is the move that stops the argument recurring.**

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

Three properties make the rule work, and all three are easy to omit:

| Property | Without it |
| --- | --- |
| **Highest band wins** when a change matches several patterns | A change touching both `docs/**` and `config/caps.yaml` merges as R1 |
| **A default** for anything unmatched | New paths arrive unbanded and are therefore unreviewed |
| **The file itself is banded** at the level it governs | Anyone can lower their own band by editing the rule in the same pull request |

That third one is the important one. `.github/review-bands.yml` must be R4, because a change to it
can turn an R4 path into an R1 path. A policy that can be edited by the person it constrains is not
a policy.

### What you actually do

1. **Generate the rule from the authority budget, do not write it by hand.** A hand-written rule
   drifts from the budget within a month and then nobody knows which is authoritative.
2. **Set the default band high, not low.** Unmatched paths get R3 until somebody bands them. A
   permissive default turns every new directory into a hole.
3. **Make highest-band-wins explicit and test it.** A change touching help text and a cap file is
   R4. Write the test with that exact case in it.
4. **Band the rule file at R4 and say so in the file.** A comment at the top naming what it governs
   and why it is banded, so the next reader does not helpfully lower it.
5. **Fail the build, do not warn.** A review requirement that can be merged past is a suggestion,
   and suggestions do not survive a release week.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Generate the rule file from the authority budget, plus the check that fails when a tool in the budget has no path pattern. The drift check matters more than the generator |
| **Chat LLM** | Given the rule and a set of recent diffs, find every change that would have matched no pattern. It reliably surfaces the new directory nobody banded |
| **Do not delegate** | Merging a change to the rule file itself. It is the one file that can quietly disable everything else on this page |

### The artefact

<details><summary><b>Template · The path rule, with its guards</b></summary>

```yaml
# .github/review-bands.yml
# GENERATED from authority budget v<n> on <date>. Do not hand-edit.
# This file is itself R4: a change here can turn an R4 path into an R1 path.
# Regenerate with: <command>

default: R3          # unmatched paths are NOT R1. New directories are not free.
resolution: highest  # a change matching several patterns takes the HIGHEST band

bands:
  R5: ["src/tools/identity/**"]
  R4: ["src/tools/refund/**", "src/tools/payment/**", "config/caps.yaml",
       "src/lib/money.ts", ".github/review-bands.yml"]
  R3: ["src/tools/rebook/**", "config/routing.yaml", "prompts/**"]
  R2: ["src/tools/search/**", "src/api/**"]
  R1: ["docs/**", "content/**"]

readers:
  R5: {people: 0, note: "not delegated - no pull request opens this path"}
  R4: {people: 2, named: true, from: "<approver group>"}
  R3: {people: 1}
  R2: {people: 0, harness: required}
  R1: {people: 0, harness: required}

enforcement:
  on_unmatched: use_default
  on_missing_tool: fail        # a tool in the budget with no pattern fails the build
  merge_without_required_readers: fail   # fail, never warn
```
</details>

<details><summary><b>Prompt · Generate the path rule and find the drift</b></summary>

```text
Here is our authority budget (tools, what each may do, and its limits): <paste>.
Here is the repository's file tree: <paste>.

1. Produce a path-rule file mapping paths to bands R1-R5, derived from the budget.
2. It must include: an explicit DEFAULT band for unmatched paths (choose R3, not R1, and
   say why in a comment), a HIGHEST-BAND-WINS resolution rule, and the rule file itself
   banded at the level of the most dangerous path it governs.
3. List every tool in the budget that has NO path pattern. That list is the drift, and it
   is the most important output — put it first.
4. List every directory in the tree that matches NO pattern, with the band you would
   give it and why.

Rules:
- Do not infer a band from a directory name alone. Say which tool each pattern serves.
- Shared libraries take the band of their most dangerous caller. Name the caller.
- Do not propose patterns that would let an author lower their own band.

Then write the three tests I should have: one for highest-band-wins, one for an unmatched
path, and one for an attempt to edit the rule file alongside a code change.
```
</details>

**Done when** — the band comes from a generated file in the repository, that file is itself R4, and
an unmatched path gets R3 rather than nothing.

---

## 4 · Route the readers by band

**Once the rule exists. This is where the four days become 1.6.**

| Band | Readers | What the reader is for |
| --- | --- | --- |
| **R4 / R5** | Two, named | The authority: does this change what the tool may do, or the limit it may do it to? |
| **R2 / R3** | One | Correctness and blast radius, with the harness having already run |
| **R1** | None | The harness alone |

Applied to the nine: two changes at R4/R5 take two readers each, three at R2/R3 take one each, four
at R1 take none.

> **(2 × 2) + (3 × 1) + (4 × 0) = 7 slots**, against 18. At 4.5 slots a day the queue goes from
> **4.0 days to 1.6 days**, with the same two people reading at the same speed.

The saving is not evenly spread, and that is the point. The two R4 changes still get everything they
had: two named readers, every time, no exceptions for size or urgency. What changed is that they no
longer queue behind four documentation updates.

Tell the reader what to read for, per band, or you get the same review at three different lengths.
An R4 review is not a longer R2 review; it asks a different question. R2 asks whether the code is
right. R4 asks whether the **authority** has changed — whether the tool can now do something it
could not do yesterday, or do it to a larger number.

### What you actually do

1. **Write what each band's reader checks, as a short list.** Three or four items per band. Without
   it, the R4 reviewer reads for style and misses the cap.
2. **Name the R4 approvers explicitly, as a group.** "A senior engineer" is not a named approver;
   a list of four people, two of whom must sign, is.
3. **Require the two R4 readers to be independent of the author.** Including when the author is an
   agent, in which case its operator counts as the author.
4. **Put the band and the reason in the pull request automatically.** "R4 — touches
   `config/caps.yaml`" as a comment from the rule, so nobody has to look it up or argue about it.
5. **Refuse urgency as a band modifier.** The urgent three-line cap change is precisely the one the
   policy exists for, and a single exception becomes the precedent within a month.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Post the band, the path that set it, and the per-band checklist into the pull request automatically, and request the right reviewers. The routing is worthless if a human has to trigger it |
| **Chat LLM** | Draft the per-band checklists from the authority budget, so the R4 list asks about limits and approvers rather than about naming and tests |
| **Chat LLM** | Before an R4 review, summarise what the diff changes about the tool's *authority* specifically: the cap, the approver, the set of accounts it can reach |
| **Do not delegate** | The R4 approval. Two named people, every time. A model cannot hold accountability, so it cannot be one of the two |

### The artefact

<details><summary><b>Template · Review policy, one page</b></summary>

```markdown
# Review policy · <team> · v<n> · <date>
Bands come from .github/review-bands.yml, generated from authority budget v<n>.
Nobody bands their own change. Urgency is not a band modifier.

## Readers per band
| Band | Human readers | Named? | Harness | Merge blocked until |
|------|--------------|--------|---------|---------------------|
| R5 | — | — | — | **No pull request opens this path.** Change the budget first |
| R4 | 2 | yes, from <group> | required | both named approvals + harness green |
| R3 | 1 | no | required | one approval + harness green |
| R2 | 1 | no | required | one approval + harness green |
| R1 | 0 | — | required | harness green |

## What each reader checks
**R4 — the authority.** Not the style.
- Does this change what the tool MAY do, or the LIMIT it may do it to?
- Is the cap still in the tool signature rather than in a prompt?
- Does the approver requirement still fire, and is there a test that proves it?
- Could this change be reverted in <n> minutes if it were wrong?

**R3 / R2 — correctness and blast radius.**
- What is the worst thing a wrong version does, and who notices first?
- Does the harness cover the case this change is about?

**R1 — nothing. The harness alone.**

## Named R4 approvers
| Name | Role | Since |
|------|------|-------|
Two of the above must approve. Neither may be the author, or the author's operator if the
change was produced by an agent.

## Exceptions
There are none. An urgent R4 change is the reason this policy exists.
Escalation when an approver is unavailable: <the standing deputy, named>.

## Slots
| Band | Changes/week | Slots each | Slots/week |
|------|-------------|-----------|------------|
| R4/R5 | <n> | 2 | <n> |
| R2/R3 | <n> | 1 | <n> |
| R1 | <n> | 0 | 0 |
| **Total** | | | **<n>** vs **<n>** under the old policy |
```
</details>

**Done when** — slots needed has fallen without anybody reading faster, and every R4 change still
has two named readers who are not its author.

---

## 5 · Open the harness-only lane, and count the escapes

**The same week you open it. Not later, and not when somebody asks.**

Four of the nine changes would merge with no person reading them. That is either the best thing in
your process or the worst, and which one depends entirely on a number you have to keep.

> **A lane with no reader is exactly as safe as its harness.**

So **count the escapes**: defects that reached production through the harness-only lane, reviewed
every week. Without that count, an unreviewed lane is just unreviewed merging with a better name —
and the industry numbers on that are not encouraging: Faros AI reported 31% more pull requests
merging with no review at all in 2026, alongside a large rise in the time a reviewed PR sits waiting.

The right posture: open the lane, keep the count, and close the lane the moment escapes appear.

### What zero escapes actually means

A count of zero is evidence, and it is weaker evidence than it feels. Four harness-only merges a week
for twelve weeks is 48 merges. Zero escapes in 48 bounds the true escape rate at roughly **6%** —
that is the rule of three, `3 ÷ n` — not at zero. It is enough to keep the lane open and nowhere near
enough to widen it.

| Merges through the lane | Zero escapes bounds the rate at about |
| --- | --- |
| 12 | 25% |
| 48 | 6% |
| 100 | 3% |
| 200 | 1.5% |

Which is the same statistical shape as the [acceptance bars](How-to-Prove-the-Bar): a small
denominator proves very little, and the honest number is the bound rather than the count.

### What you actually do

1. **Write the lane's charter before you open it.** What may use it, what the harness must prove,
   who reads the count, and the exact condition that closes it. A lane with no closing condition
   never closes.
2. **Define an escape narrowly and in advance.** A defect that reached production through a
   harness-only merge. Not "a bug somebody found" — the definition will be argued over on the day it
   matters, so settle it while nobody has a stake.
3. **Count weekly, on a standing agenda item, even when it is zero.** A count that is only produced
   when somebody is worried is a count that will not exist when it is needed.
4. **Report the bound, not the count.** "Zero in 48, which bounds the rate at about 6%" is honest and
   it pre-empts the argument that zero means safe.
5. **Close the lane on the first escape and say so in advance.** Reopening is a decision with
   evidence behind it; leaving it open after an escape is a decision nobody will admit to making.
6. **Re-run the harness against every escape, afterwards.** An escape that the harness still misses
   means the lane cannot reopen; an escape the harness now catches is the strongest argument you
   will ever have for the lane.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Tag every merge with the lane it took, so the escape count is a query rather than an archaeology exercise. Without the tag the count cannot be produced honestly |
| **Chat LLM** | For each production defect, classify which lane its change took and whether the harness could have caught it. It is fast and you check the ones it marks as escapes |
| **Do not delegate** | The decision to keep the lane open. It is the only control standing between an agent's output and production on those paths |

### The artefact

<details><summary><b>Template · Harness-only lane charter and escape log</b></summary>

```markdown
# Harness-only lane · <team> · opened <date> · owner <name>

## What may use this lane
| Band | Eligible | Also required |
|------|----------|---------------|
| R1 | yes | harness green |
| R2 | <yes / no> | <harness green + no new dependency> |
| R3, R4, R5 | **no** | — |

## What the harness must prove before a merge is allowed with no reader
| Check | Present? | Covers |
|-------|----------|--------|
| <schema / contract tests> | | |
| <the golden set, per slice, against its bar> | | |
| <no change to any banded path> | | |
| <no new external dependency> | | |

## Definition of an escape, agreed <date>
A defect that reached PRODUCTION through a merge that took this lane.
Not an escape: <a defect caught in staging; a defect on a reviewed path>.
Agreed by: <names>. This definition is not revised during an incident.

## The count — reviewed weekly, on the agenda, even at zero
| Week | Merges through the lane | Escapes | Cumulative merges | Cumulative escapes | Bound on the rate (3/n) |
|------|------------------------|---------|-------------------|--------------------|------------------------|
| <w1> | <n> | 0 | <n> | 0 | <n>% |

Reported as the BOUND, not the count. Zero in <n> merges bounds the rate at about <n>%.

## Closing condition, agreed in advance
**The lane closes on the first escape.** Fallback policy: one reader on R1/R2, which
costs <n> slots a week and <n> days of queue — computed in the queue reading.
Reopening requires: <the harness change that catches the escape, plus <n> weeks at zero>.

## Escapes
| Date | Change | What reached production | Would the harness catch it now? | Lane state |
|------|--------|------------------------|--------------------------------|------------|
```
</details>

<details><summary><b>Prompt · Classify escapes and test the harness against them</b></summary>

```text
Here are our production defects for the last <n> weeks: <paste>.
Here is the merge log, with the review lane each change took: <paste>.
Here is what our harness checks: <paste>.

1. For each defect, identify the change that caused it and the lane that change took.
   Mark each: ESCAPE (reached production through the harness-only lane), CAUGHT, or
   REVIEWED-AND-MISSED (a person read it and it went through anyway).
2. For every ESCAPE, say whether the harness as it stands today would catch it, and if
   not, what check would. Be specific about the check, not about "more testing".
3. Report the escape count AND the bound: zero escapes in n merges bounds the true rate
   at about 3/n, so give me that percentage.
4. Count the REVIEWED-AND-MISSED separately and tell me the ratio. If human review is
   missing as much as the harness, that is an argument about the review, not the lane.

Rules:
- Use the definition of an escape I gave you. Do not broaden it.
- Do not conclude the lane is safe from a zero count. Report the bound.
- Do not recommend closing or widening the lane. Give me the numbers.
```
</details>

**Done when** — the escape count exists as a weekly query, it is reported as a bound rather than a
count, and the condition that closes the lane was written before the lane opened.

---

## 6 · Measure the policy, or it will be repealed

**From the first week, and every month after.**

Three numbers, together. Any one alone can be argued with.

| Number | Before | After |
| --- | --- | --- |
| Review slots needed | 18 | **7** |
| Days in the queue | 4.0 | **1.6** |
| Escapes from the harness-only lane | – | **0** |

"The reviewers feel less pressure" is true and cannot be compared with anything. Next quarter nobody
will remember why the policy exists. These three can be compared, and they are what keeps the policy
alive.

The three are load-bearing as a set. Slots needed alone invites the response that you have simply
stopped reviewing. Queue time alone is a throughput claim with no safety claim beside it. The escape
count alone says nothing about whether the change was worth making. Reported together they answer the
only question anybody actually has, which is whether you went faster without going blind.

> **Report the escape count even when it is zero, and especially when it is zero.** A number that
> appears for the first time in the month it is non-zero looks like a cover-up, whatever the
> intention.

### What you actually do

1. **Publish all three on one page, monthly, in the same place each time.** A number that moves
   between documents cannot be compared, and comparison is the whole purpose.
2. **Keep the before column forever.** In six months nobody will remember that the queue was four
   days, and the before column is the entire argument.
3. **Add the band distribution as a fourth line once you have it.** It is what shows the policy is
   routing rather than relabelling — if R1 grows every month, something is being mislabelled.
4. **Name an owner for the page, not a team.** Reports owned by teams stop being produced in the
   month somebody leaves.
5. **Re-derive the bands whenever the authority budget changes.** The rule is generated; a budget
   change that does not regenerate it is a silent divergence between what a tool may do and how
   carefully it is read.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Generate the three numbers from the repository and the incident log each month, so the report exists whether or not anybody remembers to write it |
| **Chat LLM** | Draft the paragraph a sceptical engineering director would want beside the numbers, then answer their three hardest questions before the meeting |
| **Do not delegate** | Deciding what goes in the report. Omitting the escape count in a good month is what makes it unpublishable in a bad one |

### The artefact

<details><summary><b>Template · Review policy scoreboard</b></summary>

```markdown
# Review policy · month <n> · <date> · owner <name>
Policy in force: v<n>, from <date>. Bands generated from authority budget v<n>.

## The three numbers
| | Before the policy | Last month | This month |
|---|------------------|------------|------------|
| Review slots needed per <n> changes | 18 | <n> | <n> |
| Days in the queue | 4.0 | <n> | <n> |
| **Escapes from the harness-only lane** | – | <n> | **<n>** |

Merges through the harness-only lane, cumulative: <n>. Escapes: <n>.
Bound on the escape rate: about <n>% (3/n). Reported at zero as well as above it.

## Band distribution — is the policy routing, or relabelling?
| Band | Changes this month | Share | Share last month |
|------|-------------------|-------|------------------|
| R4/R5 | <n> | <n>% | <n>% |
| R2/R3 | <n> | <n>% | <n>% |
| R1 | <n> | <n>% | <n>% |

If the R1 share climbs every month, paths are being mislabelled or added unbanded.
Unmatched paths that took the default this month: <n>. <They need banding.>

## Changes to the policy this month
| Date | What changed | Why | Approved by |
|------|-------------|-----|-------------|
| | <regenerated from authority budget v<n>> | <new tool <name>> | |

## Still true
- No R4 change merged with fewer than two named approvers: yes / **no, see <ref>**
- No author approved their own change: yes / no
- The rule file was not edited alongside a code change: yes / no
```
</details>

**Done when** — all three numbers are on one page with their before column, and the escape count is
published in the months it is zero.

---

## Why this matters more with agents in the loop

The review queue is where agentic delivery gets stuck, and the published numbers are consistent about
it:

| Finding | Source |
| --- | --- |
| Median time a pull request sits in review rose sharply in 2026 | Faros AI, 22,000 developers |
| 31% more pull requests merging with no review at all | Faros AI, 2026 |
| 98% more pull requests merged per developer, while org-level delivery stayed flat | Faros AI, 2025, 10,000 developers |
| 90% of developers use AI tools; 80% report a productivity gain | DORA 2025, ~5,000 respondents |
| 30% still place little or no trust in AI-generated code | DORA 2025, ~5,000 respondents |

The middle lines are the same story from both ends. **More changes are produced; the same number of
people read them.** Routing by risk is how you spend the reading you have on the changes that can hurt
you.

The last two lines are worth holding together. Almost everyone uses these tools and most report a
gain, while a third do not trust the output — and both groups are right. The output is worth having
and it needs reading. A policy that reads everything equally is how a team with both of those beliefs
ends up acting on neither.

---

## Common mistakes

| Mistake | What it costs | Instead |
| --- | --- | --- |
| Treating nine changes as equally dangerous | Eighteen slots and a four-day queue | Route by band: two, one, none |
| Banding by diff size | A three-line refund cap change reviewed as a small change | A change inherits the band of whatever it touches |
| Letting the author set the band | Nine changes in ten are labelled R1 within a month | A path rule in the repository, generated from the authority budget |
| Reading "R5" as "hard" | A senior reviewer on a difficult R1 and a junior one on a cap check | The bands describe consequence, never complexity |
| Leaving shared helpers unbanded | The escape comes through `lib/` | Shared code takes the band of its most dangerous caller |
| Leaving config unbanded | A cap changes with no review, and no code changed | Caps, routing, prompts and flags are banded too |
| A rule file anyone can edit | An author lowers their own band in the same pull request | The rule file is R4 and says so at the top |
| A permissive default | Every new directory is a hole in the policy | Unmatched paths get R3 until somebody bands them |
| Warning instead of failing | A review requirement that can be merged past is a suggestion | Fail the build |
| An urgent exception on an R4 | The precedent, within a month | An urgent R4 change is the reason the policy exists |
| A harness-only lane with no count | Unreviewed merging with a better name | Count escapes weekly, and close the lane on the first |
| Reading zero escapes as proof | Zero in 48 bounds the rate at about 6%, not at zero | Report the bound |
| Reporting queue time alone | It reads as "we stopped reviewing" | All three numbers, together, with the before column |

---

## Try it

**Exercise 1.** Take last week's merged pull requests. For each, write the band of the **most
dangerous tool the change touches** — not the size of the diff.

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

**Exercise 2.** Your queue has nine changes, two reviewers, and 4.5 review slots a day. What does the
queue look like under the current policy and under routing?

<details>
<summary>Answer</summary>

Under "two senior reviewers on everything": 9 × 2 = **18 slots**, and 18 ÷ 4.5 = **4.0 days**.

Under routing, with two changes at R4/R5, three at R2/R3 and four at R1:
(2 × 2) + (3 × 1) + (4 × 0) = **7 slots**, and 7 ÷ 4.5 = **1.6 days**.

Eleven slots removed — 61% — with the same two people reading at the same speed. Nothing about
capacity changed. The only thing that changed was a policy sentence.

Now compute the fallback, in case escapes appear and the harness-only lane closes: (2 × 2) + (3 × 1)
+ (4 × 1) = 11 slots, and 11 ÷ 4.5 = **2.4 days**. Still well under four, which is the number that
makes closing the lane an easy decision rather than a fight.
</details>

**Exercise 3.** Your harness-only lane has merged 48 changes in twelve weeks with zero escapes. A
director asks whether it is safe to extend the lane to R3.

<details>
<summary>Answer</summary>

Zero in 48 bounds the true escape rate at about **6%**, by the rule of three. That is evidence the
lane is working at R1 and R2. It is not evidence about R3, because no R3 change has ever taken the
lane — you have measured a different population.

There is also a consequence argument that the count cannot answer. R3 means hard to reverse. The
whole reason the lane is tolerable at R1 and R2 is that a wrong merge is cheap to undo, and at R3
that stops being true. The bound would have to be far tighter, on R3 changes specifically, before the
question is even about statistics.

The answer that keeps both the lane and the relationship: "Zero in 48 bounds it at six percent, which
is why the lane stays open at R1 and R2. Extending to R3 changes what a wrong merge costs, so I would
want the escape count on R3-shaped changes first — which means running them through the harness in
shadow while a person still reads them."
</details>

---

**Next:** [Gates and Governance](Gates-and-Governance) · [How to Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts)
· [How to Prove the Bar](How-to-Prove-the-Bar) · [How to Control the Token Bill](How-to-Control-the-Token-Bill)
· [Role: Engineering lead](Role-Engineering-Lead) · [Formulas and Calculators](Formulas-and-Calculators)
