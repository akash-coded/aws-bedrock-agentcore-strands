# How to cut sprints into bolts

<!-- tutorial:lesson -->*New to this? Start with the lesson **[Bolts vs sprints](Bolts-vs-Sprints-Planning-When-AI-Writes-the-Code)** — the idea step by step, with a worked problem. This page is the reference.*<!-- /tutorial:lesson -->

When building is fast, the unit of planning shrinks to match. A **bolt** is a thin, shippable slice
reviewed and integrated the same day.

The product manager decides the **cadence**. The architect decides the **cut**. Getting the second one
wrong is what makes the first one fail.

This is the [delivery loop](The-Eight-Loops#delivery), shared between the two of them. It is the same
ground as Ship in [the engineering lead's journey](Journey-Engineering-Lead), told as a procedure
rather than as a role.

### At a glance

| | |
| --- | --- |
| **Reach for it when** | The plan is ordered by priority, and day three needs something from day seven. |
| **Owner** | Engineering lead |
| **Phase** | P2 · Build & Prove |
| **Closes** | [Delivery](The-Eight-Loops#delivery) — P2 → P2 |
| **Moves** | 6 |
| **You leave with** | An ordered bolt list with one unknown each, a story file per bolt, and an exposure curve that falls from day one |

---

## The six moves

<!-- picture:wikimap:cut-sprints -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-cut-sprints.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-cut-sprints.dark.webp"><img alt="Six moves for cutting sprints into bolts, with a re-cut when the cut was wrong" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-cut-sprints.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-cut-sprints.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| # | Move | Produces | Done when |
| --- | --- | --- | --- |
| 1 | [Set the cadence](#1--set-the-cadence) | A cadence agreement, with an integration deadline | Evidence arrives daily, and it is something merged |
| 2 | [Cut by dependency, not by priority](#2--cut-by-dependency-not-by-priority) | An ordered bolt list, one unknown each | Every bolt can be built on its day without waiting |
| 3 | [Change the ceremonies](#3--change-the-ceremonies) | The new standup, demo and review shape | Standup asks about integration and today's one unknown |
| 4 | [Write the story file](#4--write-the-story-file) | One six-part file per bolt, versioned | A bolt can be built with the chat window closed |
| 5 | [Measure exposure in unknown-days](#5--measure-exposure-in-unknown-days) | The exposure curve for the plan | The curve falls from day one |
| 6 | [Re-cut, out loud, before you start](#6--re-cut-out-loud-before-you-start) | A re-cut note, raised in the morning | Nobody discovers a bad cut at two in the afternoon |

---

## 1 · Set the cadence

**Before the first bolt, while the team is still planning in fortnights.**

The agent builds a story in hours, then sits idle while the team waits for the sprint review.
Meanwhile leadership wants to see something every day.

| | Five stories in a two-week sprint | Ten daily bolts |
| --- | --- | --- |
| Working days | 10 | 10 |
| Evidence for leadership | A demo on day 14 | Every day |
| Cost of a wrong turn | Two weeks | One day |
| Integration | Day 13, all at once | Same day, every day |
| Definition of done | "Meets the story" | Meets the story **and** passes the harness for its slice |

Same ten days. The difference is where the risk sits.

Cadence is a product decision because it is a promise about evidence: how often it arrives, and what
counts. The answer that makes the rest of this page work is **something merged**, not something
demonstrated. A demo can be assembled from branches; a merge cannot.

| The PM decides | The architect decides |
| --- | --- |
| How often evidence arrives | What each bolt contains |
| What counts as evidence | The order they are built in |
| The integration deadline | Which unknown each day carries |
| When the shadow run starts | Where the plug goes |

Put both in one pair of hands and you get a plan that is optimistic about order and pessimistic about
pace, which is the combination that produces a demo on day fourteen.

### What you actually do

1. **Decide how often evidence arrives, and write down what counts.** *Merged to main and green on
   its slice* is evidence. *Working on my branch* is a status update wearing the same clothes.
2. **Fix the integration deadline, not the start time.** A team that agrees "merged by four" has a
   cadence. A team that agrees "we start at nine" has a habit.
3. **Do not promise ten bolts because there are ten days.** The cut decides how many there are; the
   cadence decides the rhythm they arrive in. Confusing the two is how a cut gets padded to fit.
4. **Name a standing time for raising a bad cut.** Nine in the morning, in the standup, before the day
   is spent. Move 6 is the procedure; this is the slot it happens in.
5. **Publish the day's bolt and its one unknown where leadership can read it.** Daily evidence is
   exactly what the cadence is being bought with, and an unread log is not evidence.
6. **Agree what happens on a day that fails.** One bolt, one unknown, one reason — so a failed day
   produces a finding rather than a recovery plan. Say that out loud before the first one.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Turn the sprint backlog into a candidate bolt list, one line each, with a guess at the single unknown per item. It is a starting list for the architect, never the cut itself |
| **An editor agent** | Keep the daily log current from the merge history: what merged, when, which slice the harness ran. Otherwise the log is written on Friday from memory |
| **A cheap tier** | Draft the daily note to leadership from what actually merged, in three lines. Dull, daily, and the reason the cadence stays visible |
| **Do not delegate** | The promise of a daily cadence to leadership. It is a commitment about your team's week made by someone who will be asked about it on the day it slips |

### The artefact

<details><summary><b>Template · Cadence agreement</b></summary>

```markdown
# Cadence · <feature> · agreed <date>
PM <name> owns this document. The architect owns the cut it points at.

## The promise
| | |
|---|---|
| Evidence arrives | <daily> |
| What counts as evidence | <merged to main, green on its slice in the harness> |
| What does not count | <a branch, a demo assembled by hand, a screenshot> |
| Integration deadline | <16:00 local, every working day> |
| Where it is published | <the bolt log, link> |

## The day
| Time | What | Who |
|------|------|-----|
| <09:00> | <standup: did yesterday's bolt integrate? what is today's one unknown?> | <team> |
| <09:15> | <re-cut raised here, if the bolt cannot be built alone> | <engineer -> architect> |
| <by 16:00> | <merged, reviewed by band> | <engineer + reviewer> |
| <16:30> | <daily note to leadership, three lines, from what merged> | <PM> |

## When a day fails
<One bolt, one unknown, one reason. A failed day produces a named finding by 16:00 and
the next day's bolt is unchanged unless the architect re-cuts.>

## What the PM will NOT do
- <decide the order of the bolts>
- <approve a pull request they cannot evaluate>
- <add a bolt to fill a day>
```
</details>

**Done when** — evidence arrives daily, it is something merged, and the integration deadline is a time
of day rather than an intention.

---

## 2 · Cut by dependency, not by priority

**Once the cadence exists, and before anyone starts day one.**

A bolt must be **buildable and testable alone**. That constraint sets the order, and it is not the
order the backlog is in.

<!-- picture:figure:bolt_days -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/engineering/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/figure-bolt-days.dark.webp"><img alt="A bolt plan: one risk per bolt, the walking skeleton first" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/figure-bolt-days.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/engineering/">Open the live, interactive version</a></sub>
<!-- /picture -->

The ordering rules, in priority order:

1. **The walking skeleton first.** The thinnest end-to-end path, with no model in it. It proves the
   pieces connect, which is the assumption everything else rests on.
2. **Pure exact code early.** It is unit-testable in isolation, so it never blocks and never waits.
3. **Checkers after the steps they check.** Obvious, and still mis-ordered often.
4. **The plug before any gated write that needs it.** This is the classic failure: the rebook bolt is
   scheduled for day four and the MCP server it needs for day six.
5. **The proof last.** The harness needs something to run against.

> **One unknown per bolt.** Then a day can fail for exactly one reason, and you know which.

Tool: [Sprint-to-bolt planner](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bolts)

The five rules are not preferences; each one removes a specific failure that costs a day:

| Rule | The failure it removes | What that failure looks like |
| --- | --- | --- |
| Skeleton first | Building on an architecture nobody has connected | Day nine: the reservation adapter has never authenticated |
| Exact code early | Review capacity consumed when it is scarcest | Two probabilistic bolts queued behind each other on day four |
| Checkers after | A checker with nothing to check | A day spent on scaffolding and a stub |
| Plug before consumer | A bolt that cannot start | Day four, at two in the afternoon |
| Proof last | A harness measuring an empty system | A green run that proves nothing |

The cut comes from the [paper design](How-to-Design-an-Agent-on-Paper): the exact steps are already
tagged, the tools are already banded, and the gated writes are already named. If the cut is hard to
produce, the usual cause is that the map does not exist yet.

### What you actually do

1. **Start from the map, not from the backlog.** Every exact step is a candidate bolt that stands
   alone; every consequential tool is a bolt with a plug in front of it.
2. **Write a depends-on column before writing a day column.** The order falls out of the dependencies;
   choosing days first means bending dependencies to fit them.
3. **Give every bolt exactly one unknown, and name it in words.** *Can it beat the desk?* is an
   unknown. *Build the ranker* is a task.
4. **Split any bolt with two unknowns.** A two-unknown day cannot fail informatively: the standup
   produces a discussion, and the discussion takes the next morning too.
5. **Check the plugs explicitly, in one pass.** Walk every gated write and confirm the thing it calls
   is already merged. This single pass removes the most common ordering error there is.
6. **Assign a band per bolt from the most dangerous tool it touches.** The band comes from the path,
   never from the author, and it decides the review before the review is needed.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **A cheap tier** | Generate the dependency-ordered plan from the bolt list plus a depends-on column, and flag cycles, plugs after consumers and no-dependency items sitting at the end |
| **Claude Code** | Derive candidate bolts from the exact/best-guess map and the tool list in the repository, with the band already attached from the path rule |
| **Chat LLM, adversarially** | "Which of these bolts secretly has two unknowns?" It is good at this, and every hit it finds is a day you do not lose |
| **Do not delegate** | The cut itself. It is a claim about what your repository and your team can do in a day, and a model ordering a list it cannot build produces a confident plan with the day-four failure still in it |

### The artefact

<details><summary><b>Template · The bolt cut</b></summary>

```markdown
# Bolt cut · <feature> · <n> bolts · architect <name> · <date>

## The order, and the rule that produced it
| Day | Bolt | Depends on | The ONE unknown | Band | Rule |
|-----|------|-----------|-----------------|------|------|
| 1 | <walking skeleton — read a booking, show it. NO MODEL> | — | <do the pieces connect?> | R1 | skeleton first |
| 2 | <fare_difference(), exact, unit-tested> | 1 | <the rounding rule> | R1 | exact early |
| 3 | <visa and codeshare eligibility, exact> | 1 | <where the partner rules live> | R1 | exact early |
| 4 | <rank_alternatives(), best-guess, measured> | 2 | <can it beat the desk?> | R2 | |
| 5 | <independent checker after ranking> | 4 | <which model judges> | R2 | checker after |
| 6 | <MCP server, reads open> | 1 | <auth to the booking system> | R2 | plug before consumer |
| 7 | <rebook() gated write> | 6 | <idempotency> | R3 | |
| 8 | <issue_refund(max 400) + confirmation token> | 7 | <who mints the token> | R4 | |
| 9 | <shadow path behind a flag> | 5, 8 | <flag plumbing> | R2 | |
| 10 | <golden set and harness in CI> | 9 | <slice tagging> | R1 | proof last |

## Plug check — walked <date> by <name>
| Gated write | The plug it needs | Plug day | Consumer day | OK? |
|-------------|-------------------|----------|--------------|-----|
| <rebook()> | <MCP server> | <6> | <7> | yes |

## Bolts that were split, and why
| Original | Two unknowns | Became |
|----------|--------------|--------|
| <"rank and price the options"> | <the ranking quality AND the rounding rule> | <bolts 2 and 4> |

## Not in this cut
<what was deliberately left out, and which later cut it belongs to>
```
</details>

<details><summary><b>Prompt · Order the bolts by dependency, not by priority</b></summary>

```text
Here are the bolts for <feature>, each with a one-line description and a depends-on
column: <paste>.

Produce a day-by-day order in which every bolt's dependencies come strictly before it.

RULES, applied in this priority order:
1. The walking skeleton first — the thinnest end-to-end path with NO model in it.
2. Pure exact code early. It is testable alone, so it never blocks anyone.
3. Checkers after the steps they check.
4. Any plug (MCP server, connector, adapter) BEFORE the gated write that needs it.
5. The proof — golden set and harness — last.

Then report, separately and BEFORE the plan:
- any CYCLE, where two bolts wait on each other. A cycle is always a mis-cut and means
  one of them is really two bolts. Name which one.
- any plug scheduled after its consumer in the order I gave you
- any bolt with NO dependencies that I had scheduled late
- any bolt carrying more than ONE unknown, and how you would split it

If there is no walking skeleton in my list, add one and say what it would cover.
Do not add anything else. A plan with a bolt I did not ask for is worse than a short one.
```
</details>

**Done when** — every bolt can be built on its scheduled day without waiting for anything, and the
plug check has been walked row by row.

---

## 3 · Change the ceremonies

**On the first day of the new cadence, not gradually.**

| Ceremony | Before | With bolts |
| --- | --- | --- |
| Planning | Two weeks of stories | Tomorrow's bolt, from its story file |
| Standup | Status round | "Did yesterday's bolt integrate? What is today's one unknown?" |
| Definition of done | Meets the story | Meets the story, passes its slice in the harness, **and is integrated** |
| Demo | Day 14 | Every day, from what actually merged |
| Review | End of sprint | By risk band, same day |

The standup question is the load-bearing change. Two questions, both answerable in a sentence, both
producing a fact rather than a narrative. A status round produces "I'm continuing with the ranker",
which is true, unfalsifiable and worth nothing.

The review change is the one that fails quietly. Same-day integration only works if review capacity
is available the same day, and that means routing by band rather than reviewing everything twice —
see [How to Review by Risk Band](How-to-Review-by-Risk-Band).

### What you actually do

1. **Replace the status round with the two questions, and hold the line for a fortnight.** People
   revert to narrative under pressure, and the first failed bolt is the pressure.
2. **Demo from what merged, with nothing prepared.** If the demo needs preparation it is not evidence
   of the cadence, it is evidence of a good preparer.
3. **Move review to the same day and route it by band.** R1 goes to the harness and one look at the
   end; R4 gets two named approvers, every time.
4. **Make "integrated" part of done, out loud.** A bolt that meets its story and sits on a branch has
   not happened, and saying that once in week one saves saying it five times in week three.
5. **Keep planning to tomorrow only.** Planning further ahead re-creates the sprint, because a
   two-week plan makes today's finding expensive to act on.
6. **Put the one unknown on the board, not in someone's head.** It is the only thing that makes the
   next morning's standup answerable in a sentence.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **An editor agent** | Assemble the daily demo note from the merge log and the harness output: what merged, which slice ran, what it scored. Thirty seconds instead of ten minutes |
| **A cheap tier** | Route each change to its band by path, and open the review with the band already set. The band comes from the path rule, never from the author |
| **Chat LLM** | Rewrite a status-round standup transcript as the two questions, to show the team the difference. It works better as a demonstration than as an instruction |
| **Do not delegate** | Holding the definition of done. Deciding that an unintegrated bolt does not count is a social act, and it needs a person who will be unpopular for ten minutes |

### The artefact

<details><summary><b>Template · The day, and the two questions</b></summary>

```markdown
# Bolt day · <date> · <feature>

## Standup, <09:00>, <n> minutes
| Engineer | Did yesterday's bolt integrate? | Today's ONE unknown |
|----------|--------------------------------|---------------------|
| <name> | <yes, 15:40, harness green on <slice>> | <can the ranker beat the desk on same-day?> |
| <name> | <no — see the re-cut note> | <blocked, raised to the architect at 09:05> |

Nothing else is discussed here. Anything longer than a sentence moves to a named
conversation with two names and a time on it.

## Today's bolt
| | |
|---|---|
| Bolt | <n · title> |
| Story file | <path> |
| Band | <R2, from the path rule> |
| Reviewer | <name, assigned now, not at 16:00> |
| Integration deadline | <16:00> |

## Demo, from what merged
| Merged | Slice | Harness | Shown as |
|--------|-------|---------|----------|
| <bolt n> | <codeshare> | <82% against a bar of 80%> | <the actual run, not a slide> |

## Done, for today
- [ ] Meets the story
- [ ] Passes its slice in the harness
- [ ] **Integrated to main**
```
</details>

**Done when** — standup asks the two questions and nothing else, and the demo is whatever merged.

---

## 4 · Write the story file

**The evening before the bolt, or the morning of it — never during.**

A bolt that needs a chat thread was cut wrong, or its file is incomplete. Six parts, one file,
versioned next to the code:

```markdown
# Bolt 7 · rebook() gated write

## Context      (by reference, never pasted)
  /context/shared/standards.md · /context/domain/booking-model.md
  /context/product/architecture.md · ADR-004, ADR-007

## Spec         (EARS)
  WHEN the passenger accepts a proposed alternative
   AND the fare difference has been computed
  THE SYSTEM SHALL rebook the segment within 10 seconds.
  BOUNDARY  Never rebook without a computed fare difference.

## Tools        rebook(pnr, segment, fare_delta, confirmation) → R3

## Tests        golden slice: "rebook" (40 cases, bar 85%)
                unit: rebook_requires_fare_delta, rebook_is_idempotent

## Done when    harness green on the rebook slice, integrated to main, trace row written

## Cost         ~1,900 tokens/call, mid tier
```

It is BMAD's *shard* and spec-driven development's unit at once. Because it is a file, it is
reviewable as a diff and versioned alongside the code it produces.

The six parts each answer a question the builder would otherwise ask, and the order is deliberate:

| Part | The question it answers | The failure when it is missing |
| --- | --- | --- |
| Context, **by reference** | What must I already know? | Pasted context goes stale silently and costs tokens on every call |
| Spec, in **EARS** | What exactly must be true? | Prose is interpreted, and the interpretation is not reviewable |
| Tools | What may I call, and at what band? | A signature invented at 2pm, with the cap left out |
| Tests | How will we know? | Tests written after the code, to fit the code |
| Done when | When do I stop? | A bolt that expands to fill the day |
| Cost | What does one call cost? | The token bill discovered in month three |

Context **by reference** is the part teams get wrong most often. A path is read at build time and is
always current; a paste is a copy that was true once.

### What you actually do

1. **Write the file before the day starts, and never during it.** A file written mid-build is a
   transcript of what happened, not a brief, and it cannot be reviewed.
2. **Reference context by path, never paste it.** Paths stay current, cost nothing to keep current,
   and make the story file reviewable as a short diff.
3. **Copy the spec from the agent PRD rather than rewriting it.** Two versions of an EARS clause is
   two specifications, and the build follows the one in front of it.
4. **Name the tools with their bands and their required parameters.** `rebook(pnr, segment,
   fare_delta, confirmation)` says more about the design than a paragraph would.
5. **Write the tests before the implementation exists, and require them to be seen failing.** A test
   that has never failed has not been shown to test anything.
6. **Treat every question the builder has to ask as a defect in the file.** Log it, fix the template
   tonight, and the next bolt is cheaper. That loop is the actual product of this move.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Draft the six-part file from one line of the cut plus the agent PRD, leaving every unknown as an explicit gap rather than filling it in |
| **Claude Code** | Build the bolt from the file with the chat window closed. Every question it has to ask is a defect in the file, and that list is the finding |
| **A cheap tier** | Check each file mechanically: six parts present, context as paths not pastes, every tool banded, a number in the done-when |
| **Do not delegate** | The done-when. It is the line that stops a bolt expanding to fill the day, and it is a judgement about what is enough today rather than eventually |

### The artefact

<details><summary><b>Template · Story file, six parts</b></summary>

```markdown
# Bolt <n> · <title>
_Day <n> · Band <R<n>> · Architect's cut <date> · One unknown: <in words>_

## 1 · Context      (by reference — paths only, never pasted)
  <context/shared/standards.md> · <context/domain/<model>.md>
  <context/product/architecture.md> · <ADR-00n, ADR-00n>

## 2 · Spec         (EARS — copied from the agent PRD, not rewritten)
  WHEN <trigger>
   AND <precondition>
  THE SYSTEM SHALL <observable behaviour> within <n> <unit>.
  BOUNDARY  Never <forbidden action> without <the control>.

## 3 · Tools
  <tool_name(param, param, param)> -> <R<n>>
  <what it must NOT be able to do: e.g. no write while the shadow flag is on>

## 4 · Tests        (written first, and seen failing)
  golden slice: "<slice>" (<n> cases, bar <n>%)
  unit: <name_of_test>, <name_of_test>

## 5 · Done when
  <harness green on the <slice> slice, integrated to main by <16:00>, trace row written>

## 6 · Cost
  <~n tokens/call, <tier> tier> · <expected calls per case: n>

## File defects found while building this bolt
| What the builder had to ask | Fixed in the template? |
|-----------------------------|------------------------|
| <> | <> |
```
</details>

<details><summary><b>Prompt · Draft the story file from one line of the cut</b></summary>

```text
Write the six-part story file for this bolt.

BOLT: <one line from the cut, with its depends-on and its one unknown>
AGENT PRD: <paste, or give the path>
AVAILABLE CONTEXT PATHS: <list them>

OUTPUT SHAPE — exactly six numbered sections, in this order:
  1 Context (PATHS ONLY — never paste file contents)
  2 Spec (EARS, copied verbatim from the PRD where it exists)
  3 Tools (signature, required parameters, band)
  4 Tests (golden slice with a bar, plus named unit tests)
  5 Done when (one testable sentence, with a time in it)
  6 Cost (tokens per call and tier)

RULES:
- Anything you do not know goes in a final list headed GAPS. Do not invent a bar, a
  band, a token figure or a test name to make the file look complete.
- Do not rewrite the EARS clause. If the PRD's wording is ambiguous, quote it and add
  the ambiguity to GAPS.
- The file must be buildable with no further conversation. Read it back and ask what a
  builder would still have to ask; put each of those in GAPS too.
```
</details>

<details><summary><b>Prompt · Build today's bolt from its file alone</b></summary>

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

**Done when** — the bolt can be built with the chat window closed, and every question that still had
to be asked is written down as a defect in the file.

---

## 5 · Measure exposure in unknown-days

**When the cut exists and before it is agreed, as the check on the order.**

A useful measure of how risky a plan is: **the sum, over every day, of the unknowns still open.**

> **exposure = Σ, over every day, of the unknowns still open**

Two plans, same ten bolts:

| Plan | Day 1 unknowns | Day 10 unknowns | Exposure |
| --- | --- | --- | --- |
| Skeleton first, exact early, risk retired daily | 10 | 0 | **Low** — the curve falls from day one |
| Integration on day 9 | 10 | 10 until day 9 | **High** — every unknown is open until the end |

The point of the skeleton is not that it is impressive. It is that it retires the largest unknown —
"do these pieces connect at all" — on day one, for almost no cost.

Counted out, the difference is stark. Ten unknowns retired one a day gives 10+9+8+…+1 = **55
unknown-days**. The same ten held open until day nine and then cleared gives 10 × 9 + 1 = **91**.
Same work, same people, same ten days, and two-thirds more time spent not knowing.

The curve is more useful than the total. A plan whose curve is flat for the first four days has its
risk in the wrong place, whatever its total says, because a finding on day five costs five days of
built work and a finding on day one costs half a day.

### What you actually do

1. **List the unknowns before you list the bolts.** There are usually fewer than the bolt count, and
   two bolts sharing an unknown is a hint that one of them is not carrying its own.
2. **Assign exactly one unknown to each bolt, and mark the day it is retired.** Retired means
   answered by something merged, not by a conversation.
3. **Add the column up and plot it.** Ten numbers. It takes two minutes and it is the only view that
   shows the shape of the risk rather than its total.
4. **Look at the first three days, not the total.** A curve that is flat early is the failure mode,
   and reordering early bolts is nearly free before the plan starts.
5. **Rank the unknowns by what they would cost if answered late.** *Do the pieces connect* costs the
   whole plan; *the rounding rule* costs an hour. Retire the expensive ones first.
6. **Re-plot after any re-cut.** A re-cut that moves a plug also moves an unknown, and the curve is
   how you check the new order is not worse than the old one.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Compute the exposure curve from the bolt list and plot it, then do the same for two candidate orders. Ten minutes, and it makes the comparison visible rather than arguable |
| **Chat LLM** | Rank the unknowns by what each would cost if it were answered on day nine instead of day one. The ranking is the reordering argument |
| **Chat LLM, adversarially** | "Which unknown in this list is really three unknowns?" The compound one is what makes a curve look better than the plan is |
| **Do not delegate** | Deciding an unknown is retired. Only somebody who has seen the thing work can say it is answered, and a model reading a plan cannot |

### The artefact

<details><summary><b>Template · Unknown-days ledger</b></summary>

```markdown
# Exposure · <feature> · plan <version> · <date>

## The unknowns, ranked by what they cost if answered late
| # | The unknown, in words | Cost if it comes back badly on day 9 | Retired by bolt |
|---|----------------------|--------------------------------------|-----------------|
| 1 | <do the pieces connect at all?> | <the whole plan> | <1> |
| 2 | <auth to the booking system> | <bolts 6-9, four days> | <6> |
| 3 | <can the ranker beat the desk?> | <the feature's value line> | <4> |
| 4 | <the rounding rule> | <an hour> | <2> |

## The curve
| Day | Bolt | Unknown retired | Still open | Running total |
|-----|------|-----------------|-----------|---------------|
| 1 | <skeleton> | <#1> | <9> | <9> |
| 2 | <fare_difference> | <#4> | <8> | <17> |
| 3 | | | | |
| ... | | | | |
| 10 | | | **0** | **<n>** |

**Exposure = <n> unknown-days.** Comparison order <B> scored <n>. Chosen: <A>, because
<the curve falls from day one rather than on day nine>.

## Shape check
| Question | Answer |
|----------|--------|
| Is the curve flat for the first <3> days? | <no> |
| Is the most expensive unknown retired first? | <yes — bolt 1> |
| Does any bolt carry two unknowns? | <no — <x> was split> |
```
</details>

<details><summary><b>Prompt · Compute the exposure curve and find the flat start</b></summary>

```text
Here is a bolt plan: one row per day, with the bolt, its dependencies and its single
unknown. <paste>

OUTPUT SHAPE:
1. A table: day | bolt | unknown retired | unknowns still open | running total.
2. The total exposure in unknown-days, with the arithmetic shown for the first three
   rows so I can check it.
3. The same computation for ONE alternative order that you propose, and the difference.
4. A SHAPE CHECK: is the curve flat for the first three days? Which unknown is the most
   expensive if answered late, and on what day is it retired?

RULES:
- exposure = the sum, over every day, of the unknowns still open at the end of that day.
- An unknown is retired only by something that merges. A conversation does not retire it;
  if a row claims one, flag it.
- Flag any bolt carrying more than one unknown, and any unknown that is really several.
  Both make the curve look better than the plan is.
- Do not reorder to minimise the total at the cost of the dependency rules. State the
  rules you preserved.
```
</details>

**Done when** — the curve falls from day one, the most expensive unknown is retired first, and no bolt
carries two.

---

## 6 · Re-cut, out loud, before you start

**At nine in the morning, in the standup — never at two in the afternoon.**

Say so **before** starting it, not halfway through. A bolt that cannot be built alone was cut wrong,
and the fix belongs with the architect, not with the engineer who discovered it at 2pm.

The usual causes:

| Symptom | Cause | Fix |
| --- | --- | --- |
| "I need the MCP server that is scheduled for Thursday" | Plug ordered after its consumer | Move the plug earlier |
| "I need the other half of this feature" | The slice is not thin, it is **cut in half** | Re-cut vertically, not horizontally |
| "I cannot test it without the model being right" | Exact and best-guess bundled in one bolt | Split them; the exact half stands alone |

The information is nearly always available at nine. What is usually missing is somebody willing to
say the cut was wrong before spending the day proving it, which is a cultural property rather than a
technical one — and it is bought by the architect responding with a re-cut rather than a defence.

The three-question test, before opening the editor:

| Question | If no |
| --- | --- |
| Does everything this bolt calls already exist on main? | A plug is ordered after its consumer. Move the plug |
| Can it be tested without any other unmerged work? | It was cut horizontally. Re-cut it vertically |
| Is there exactly one thing here we do not know? | Split it; each half gets its own day |

### What you actually do

1. **Run the three questions before opening the editor.** Two minutes, every morning, and it is the
   whole of this move's cost.
2. **Raise it in the standup, not in a message an hour later.** The architect is in the room and the
   day has not been spent, which are the two conditions that make a re-cut cheap.
3. **Say what is missing, not that you are blocked.** *rebook needs the MCP server, which is day six*
   is actionable in an hour. *Blocked* is a status.
4. **Let the architect re-cut, and do not route around it.** An engineer who builds the missing half
   to unblock themselves has produced a two-unknown day and a review nobody can band.
5. **Write the re-cut down, with the cause.** Plug after consumer, cut horizontally, or two unknowns
   bundled — the cause is what stops the same mistake in the next cut.
6. **Take the replacement bolt from the same list, not from the backlog.** The plan has other bolts
   with no unmet dependencies; the backlog has priorities, which is what the cut was avoiding.

### Where a model helps

| Tool | Use it for |
| --- | --- |
| **A cheap tier** | Run the three questions against tomorrow's bolt overnight, using the story file and the merge log. A flag at nine is worth more than a finding at two |
| **Claude Code** | Check mechanically whether everything the bolt's story file names is already on main — tools, modules, fixtures. It answers question one with evidence |
| **Chat LLM** | Given the symptom, classify the cause as plug-after-consumer, cut-horizontally or two-unknowns, and propose the vertical re-cut. It is good at the third one |
| **Do not delegate** | The claim that a bolt cannot be built alone. It is a statement about your repository and your day, and it has to be said to the architect by someone who will own being wrong |

### The artefact

<details><summary><b>Template · Re-cut note</b></summary>

```markdown
# Re-cut · bolt <n> · raised <date> at <09:05> — BEFORE the build started
Raised by <name> · Decided by <architect name> · Time to decide: <1 hour>

## The three questions
| Question | Answer |
|----------|--------|
| Does everything this bolt calls already exist on main? | <no — <the MCP server> is day 6> |
| Can it be tested without other unmerged work? | <yes> |
| Is there exactly one unknown? | <yes> |

## What is missing, specifically
<rebook() calls the MCP server, which is scheduled for day 6. This is a plug ordered
after its consumer.>

## Cause
<plug after consumer | cut horizontally, not vertically | two unknowns bundled>

## The re-cut
| | Before | After |
|---|--------|-------|
| <MCP server, reads open> | day <6> | day <4> |
| <rebook() gated write> | day <4> | day <6> |

Exposure re-checked: <unchanged / n unknown-days, from n>.

## Today's bolt instead
<bolt <n>, which has no unmet dependencies>

## What goes back into the next cut
<check every gated write against its plug in one pass — this is rule 4 and it was
missed on <date>>
```
</details>

<details><summary><b>Prompt · Test a bolt for standalone buildability</b></summary>

```text
Here is tomorrow's bolt story file: <paste>. Here is what is currently on main:
<paste the module list, tool list, or let me point you at the repository>.

Answer these three questions, in this order, with evidence:
1. Does EVERYTHING this bolt calls already exist on main? List each dependency and where
   you found it, or say it is missing.
2. Can this bolt be tested without any other unmerged work? Name the tests and what each
   one needs.
3. Is there exactly ONE thing here we do not know? If there are two, name both and
   propose the split.

Then, if any answer is no, classify the cause as exactly one of:
  PLUG AFTER CONSUMER · CUT HORIZONTALLY · TWO UNKNOWNS BUNDLED
and propose the re-cut, including which bolt should be built tomorrow instead.

RULES:
- Evidence for question 1 means a path or a symbol you actually found, not an assumption
  that it probably exists.
- Do not propose building the missing piece as part of this bolt. That is the failure
  this check exists to prevent.
- If all three answers are yes, say so in one line and stop.
```
</details>

**Done when** — the three questions were asked before the editor was opened, and any re-cut was raised
in the morning with its cause written down.

---

## SkyWays · day 30, the first bolt ships by four in the afternoon

> The first bolt was a walking skeleton: read a booking, show it, no model anywhere in it. It shipped
> by four in the afternoon, and what it bought was not the feature but the answer to the question
> every other bolt was resting on — whether the pieces connect. The exact code went on days two and
> three, so review capacity was free when the ranking bolt arrived. The one re-cut came on day four
> and was raised at nine in the morning rather than at two: `rebook()` needed the MCP server
> scheduled for day six, a plug ordered after its consumer. Moving the plug cost an hour. Discovering
> it mid-build would have cost the day.

Three of the six moves are visible in that paragraph: the cut put the skeleton first and the exact
code early, the ceremony gave the re-cut a nine o'clock slot, and the re-cut itself was raised as a
cause rather than as a blockage. The hour it cost is the whole argument for the other five moves.

---

## Common mistakes

| Mistake | What it costs | Instead |
| --- | --- | --- |
| Ordering by priority | The most valuable bolt is scheduled first and cannot be built | Order by dependency; priority decides what is in the cut, not when |
| Scheduling the plug after its consumer | A whole day, mid-week, every time | Walk every gated write against its plug in one pass |
| Two unknowns in one bolt | The day fails and nobody can say which half failed | One unknown per bolt, named in words, or split it |
| No walking skeleton | The architecture is unproven until day nine, when everything rests on it | Half a day, no model in it, day one |
| Context pasted into the story file | It goes stale silently and costs tokens on every call | Reference by path; paths are read at build time |
| Discovering a bad cut at 2pm | The day, and the next morning's standup | The three questions before the editor opens |
| Done means "meets the story" | Ten branches and an integration day | Done means merged, green on its slice, same day |
| A demo that needed preparing | Evidence of a good preparer, not of a cadence | Demo whatever merged, with nothing prepared |

---

## Try it

**Exercise.** Take your current sprint. Write each story on a line with a "depends on" column, then
order them so that every item's dependencies come before it.

<details>
<summary>What the exercise reveals</summary>

Three things, reliably.

**A cycle.** Two items each waiting on the other. This is always a mis-cut, and it means one of them
is really two items.

**A plug scheduled after its consumer.** The most common single error, and the one that costs a whole
day mid-sprint.

**An item with no dependencies that was scheduled last.** Usually the exact code — the fare math, the
eligibility rules. It stands alone, it is cheap, it unblocks review capacity, and it is sitting at the
end of the plan because it looked boring.

If your ordered list has no walking skeleton at the top, add one. It is half a day and it is the only
bolt that tells you whether the architecture is real.
</details>

**Exercise 2.** Take the ordered list you just produced and compute its exposure: for each day, count
the unknowns still open, and add the ten numbers up. Then move one bolt and compute it again.

<details>
<summary>What the two numbers show</summary>

The total matters less than where it falls. Ten unknowns retired one a day comes to 55 unknown-days;
the same ten held until day nine comes to 91. Moving a single early bolt usually moves the total by
five or six, which is worth knowing but is not the point.

The point is the **first three days**. If the curve is flat there, your plan spends its cheapest days
not learning anything, and the finding that would have cost half a day on Monday will cost five days
on Friday. Reordering before the plan starts is free; reordering on day five is a re-cut, an apology
and a slipped demo.

If moving a bolt improves the total but breaks the dependency rules, the rules win. Exposure is a
check on the order, not a replacement for it.
</details>

**Exercise 3.** Take the story file for the next thing your team is about to build and hand it to a
coding agent with the chat window closed. Count the questions it has to ask.

<details>
<summary>What the count means</summary>

Zero questions means the file is complete, which on a first attempt is rare and usually means the
bolt is smaller than you thought.

One or two questions is the normal, healthy result, and both are template defects rather than agent
failures. The usual two are a missing band on a tool and a done-when with no number in it — the first
because bands live in the architect's head, the second because "works" feels like a finish line until
somebody has to decide whether it has been crossed.

More than four questions and the bolt was cut wrong rather than written up badly. Look for two
unknowns bundled together; that is almost always what produces a file the builder cannot follow.
Whatever the count, the fix goes into the template tonight, and the next bolt is cheaper than this
one. That loop, and not the file, is what this move is actually for.
</details>

---

**Next:** [How to Review by Risk Band](How-to-Review-by-Risk-Band) · [How to Prove the Bar](How-to-Prove-the-Bar)
· [Role: Engineering lead](Role-Engineering-Lead) · [The Eight Loops](The-Eight-Loops)
