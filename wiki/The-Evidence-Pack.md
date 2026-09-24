# The evidence pack

<!-- tutorial:lesson -->*New to this? Start with the lesson **[The evidence pack](The-Evidence-Pack-Before-Each-Hand-off)** — the idea step by step, with a worked problem. This page is the reference.*<!-- /tutorial:lesson -->

The **minimum artefact set**: the few documents owed at each hand-off between phases. Together they are
what you show an auditor, a new team member, or yourself in six months when nobody remembers why the
refund cap is $400.

An artefact is owed when the next phase cannot start without it. Everything else is optional.

Live version: [Evidence pack](https://akash-coded.github.io/aws-bedrock-agentcore-strands/#/evidence/ev-p0).

---

## What "owed" means

Owed is a stronger word than useful. An owed artefact is one whose absence stops the next phase from
being done properly rather than slowly — and the test is not whether somebody wants it, but whether
the next phase would have to invent it.

| State | What it means | What the next phase does |
| --- | --- | --- |
| **Owed and present** | It exists, it is current, and the receiving owner has read it | Starts |
| **Owed and stale** | It exists and the system has moved past it | Starts, then builds on a fiction |
| **Owed and absent** | It does not exist | Invents it, silently, usually correctly-looking |
| **Not owed** | Useful, and nobody downstream is blocked | Keep it if someone reads it; delete it otherwise |

The dangerous state is the middle one, because a stale artefact passes every check that asks whether
a document exists. The pack index below carries a date column for exactly this reason.

<details><summary><b>Template · The pack index</b></summary>

```markdown
# Evidence pack · <product> · index
One row per owed artefact. This page is the pack; everything else is a link from it.
Owner of the index: <name>   Last full review: <date>

| # | Artefact | Hand-off | Owner | Link | Version | Last changed | Current? | Read by |
|---|----------|----------|-------|------|---------|--------------|----------|---------|
| 1 | <pain register> | P0→P1 | <PM> | <link> | v3 | <date> | yes | <architect> |
| 2 | <ratified NFRs + sensitivity points> | P0→P1 | <architect> | <link> | v2 | <date> | yes | <PM, eng> |
| 3 | <eight-field spec> | P1→P2 **hard** | <PM> | <link> | v7 | <date> | yes | <eng lead> |
| 4 | <acceptance bar sheet, per slice> | P1→P2 **hard** | <PM> | <link> | v2 | <date> | **stale** | <QA> |
| 5 | <authority budget + gate map> | P1→P2 **hard** | <architect> | <link> | v4 | <date> | yes | <eng lead> |

## The three numbers this pack is built on
| Number | Value | First set in | By whom | Where it is enforced today |
|--------|-------|--------------|---------|-----------------------------|
| <cases per day> | <240> | <pain register, day 1> | <PM> | <the value line denominator> |
| <refund cap> | <$400> | <constraint register, day 6, regulatory> | <architect> | <tool signature: refund(amount_gbp: Money(max=400))> |
| <cost per case> | <$0.60> | <ratified NFRs, day 9> | <architect> | <weekly alert at 3x, owner <name>> |

<The third column of that last row is the one that matters. A number that is "in the record"
and nowhere else is a number nobody is holding.>

## Stale — artefacts the system has moved past
| Artefact | Last changed | What changed underneath it | Owner | Refresh by |
|----------|--------------|-----------------------------|-------|------------|
| <bar sheet> | <date> | <two slices were added in bolt 9> | <PM> | <date> |

## Owed and absent
| Artefact | Hand-off | Owner | Due | What is being invented in its place right now |
|----------|----------|-------|-----|------------------------------------------------|
| | | | | |

## Not owed, kept anyway
| Artefact | Who reads it | Delete if nobody does by <date> |
|----------|--------------|----------------------------------|
| | | |
```
</details>

---

## P0 → P1 · soft

| Artefact | Owner | One line of what good looks like |
| --- | --- | --- |
| The pain as a measurement | PM | Who has it, how often, what it costs today, and the evidence |
| AI-fit verdict | PM | Judgement? Volume? Recoverable? Three answers and a build shape |
| Value line | PM | Cases × minutes × rate, **minus** run cost and review load |
| Autonomy decision record | PM | Per action, with the door named: one-way or two-way |
| Credited FRs and consolidated FRs | Architect | All lines with names, then the consolidation |
| Constraints by type | Architect | Technical, regulatory, commercial — sorted before any target is set |
| Ratified NFRs with sensitivity points | Architect | Six-part scenarios, with three points named for records |

**The test for this hand-off:** can the architect start designing without asking the PM a question?

### How it actually goes wrong

The pack is complete and all of it is prose. The pain is a paragraph rather than a line with a count,
the value line has no subtraction in it, and the NFRs are adjectives. Nothing is missing and nothing
is usable, so the architect designs against an impression and the first real number is chosen in P2
by whoever needed one. SkyWays' whole ninety days hang off a single line written on day two — 240
cases a day, 38 minutes each, 11% codeshare, $9.40 per case from the Q2 ticket export — and it
survived to the steering committee because every later artefact pointed back at it.

### What good looks like

| Sign | The test |
| --- | --- |
| The pain is one line and a sceptic can open its evidence | A ticket export, a queue chart, a recording. Not an anecdote |
| The value line has a minus sign in it | Run cost and review load are subtracted, not mentioned |
| The AI-fit verdict names what was rejected | A verdict with one option considered is a preference |
| Every NFR is a six-part scenario with a number | Environment included — "at what load, at what time, in what state" |
| The autonomy record names the door per action | One-way for a cash refund, two-way for a draft itinerary |

**Whose daily work this is:** [Journey: Product manager](Journey-Product-Manager) for the first four
rows, [Journey: Solution architect](Journey-Solution-Architect) for the last three.

---

## P1 → P2 · the hard gate

This is the one hand-off that halts. Everything downstream is built and measured against these.

| Artefact | Owner | One line of what good looks like |
| --- | --- | --- |
| The eight-field spec, acceptance in EARS | PM | One screen; a coding agent builds from it unaided |
| Acceptance bar sheet, per slice | PM | Derived from damage and saving, not invented |
| ADRs at the sensitivity points | Architect | One per trade-off point, with what was rejected |
| The exact / best-guess map | Architect | Every step tagged, with the proof each kind needs |
| Authority budget and gate map | Architect | R1–R5 per tool, caps in signatures |
| Agent PRD and topology | Architect | One agent unless a named limit says otherwise |
| Context layers | Architect | Shared → domain → product → task, each versioned |
| Story files | Engineering | Self-contained: context, spec, tools, tests, done-when, cost |
| Golden set, first 50 cases | QA | Real historical cases, tagged by slice |

**The test:** hand the pack to an engineer who was not in the room. If they can build the first bolt
without a conversation, the gate is passable.

### How it actually goes wrong

Every row is ticked and one of them describes a control that was never implemented. The authority
budget says R4 on refunds with a $400 cap and a named approver; the refund tool's signature accepts
any amount and the execution role can invoke it. The document is accurate about the decision and
silent about the enforcement, and nothing in a tick-box review distinguishes the two. SkyWays crossed
this gate in exactly that state on day 12 and paid for it on day 82, when $2,000 went out that was
not owed — entirely within the agent's permissions and entirely outside its policy.

The second failure is the pack that exists in nine places. A spec in Confluence, bars in a
spreadsheet, the authority budget in an ADR, story files in the repo, and no index — so no one person
has ever seen the whole set, and the question "is this gate passable" cannot be answered in an
afternoon.

### What good looks like

| Sign | The test |
| --- | --- |
| Every artefact has an **enforced-or-written** verdict, not just a tick | Grep the signature for the cap. Grep the policy for the approver |
| An engineer who was not in the room built bolt 1 with no questions | Count the questions. Zero is the target and it is achievable |
| Each bar has a derivation line beneath it | "80% because a missed codeshare costs $<n>" beats a round number |
| The golden set's 50 cases are real and tagged by slice | Invented cases prove the prompt, not the product |
| One index links all nine | If there is no index, the pack is a folklore, not an artefact |

<details><summary><b>Template · P1 → P2 hard-gate sign-off sheet</b></summary>

```markdown
# Hard gate · P1 → P2 · <feature>
This gate HALTS. It is crossed by one named person with the nine rows below in front of them.
Signed by: <name, role>   Date: <date>   Decision: <PASS | REFUSE | PASS WITH WAIVER>

## The nine owed artefacts
| # | Artefact | Owner | Exists | Current | **Enforced or only written?** | Link |
|---|----------|-------|--------|---------|-------------------------------|------|
| 1 | Eight-field spec, acceptance in EARS | <PM> | yes | <date> | n/a — it is a document | <link> |
| 2 | Acceptance bar sheet, per slice | <PM> | yes | <date> | **enforced** — harness reads <eval/bars.json> | <link> |
| 3 | ADRs at the sensitivity points | <architect> | <3 of 3> | <date> | n/a | <link> |
| 4 | Exact / best-guess map | <architect> | yes | <date> | n/a | <link> |
| 5 | Authority budget and gate map | <architect> | yes | <date> | **WRITTEN ONLY** — see below | <link> |
| 6 | Agent PRD and topology | <architect> | yes | <date> | n/a | <link> |
| 7 | Context layers, versioned | <architect> | yes | <date> | enforced — read by path, not pasted | <link> |
| 8 | Story files for bolts 1–<n> | <eng> | yes | <date> | n/a | <link> |
| 9 | Golden set, first 50 cases, tagged by slice | <QA> | <50> | <date> | enforced — harness is a required check | <link> |

## The enforcement check — run, not remembered
| Control | Decided in | Should live in | Grep / command I ran | Result |
|---------|-----------|-----------------|----------------------|--------|
| <$400 refund cap> | <constraint register, day 6> | <refund tool signature> | <rg "max=400" src/tools/> | <0 hits — NOT ENFORCED> |
| <named approver above cap> | <autonomy record, day 12> | <tool + IAM policy> | <rg "approver" src/ infra/> | <prompt only> |
| <bar blocks the merge> | <bar sheet> | <required status check> | <gh api .../branch protection> | <required: true> |

<Any control found only in a prompt, a runbook or a document is NOT ENFORCED. Write it in
capitals. This single column is the difference between a gate and a formality.>

## The three questions the receiving owner answered
| Question | Answer |
|----------|--------|
| Can you build bolt 1 without asking anybody anything? | <yes / the <n> questions below> |
| Which number in the pack do you not believe? | <> |
| Which control would you be unable to test? | <> |

## Decision
<PASS — all nine present and every control in the enforcement check found in code.>
<REFUSE — row <n> is written only; the build does not open until it is enforced.>
<PASS WITH WAIVER — attach the hard-gate waiver, with the blast radius filled in.>

Signed: <name>, <date>. Receiving owner: <name>, who has read this sheet.
```
</details>

<details><summary><b>Prompt · Score the pack against the minimum set</b></summary>

```text
You are checking an evidence pack against the minimum artefact set for one hand-off.

The minimum set for <P0→P1 | P1→P2 | P2→P3 | P3→P0>:
<paste the rows from this page, including the "what good looks like" column>

Below is what the team actually has.

Produce:
1. | # | Artefact | Exists? | Current? (date it last changed vs the last code change) | Meets "what good looks like"? | Verdict |
   Verdicts: PRESENT / STALE / THIN / ABSENT. THIN means it exists and does not meet the
   description in the third column — say which part it misses.
2. Every artefact that describes a CONTROL. For each, state where the control is decided and
   where it would have to live to be enforced, and mark it ENFORCED, UNKNOWN or WRITTEN ONLY.
3. The gaps in dependency order: which missing artefact must be produced before the others are
   worth producing.
4. An estimate of hours for each gap, and say plainly which two are an afternoon each.

RULES:
- STALE is a real verdict and it is the one people miss. If an artefact has not changed since
  before the last two slices were added, it is stale. Say so.
- Never accept "it is in the prompt" as enforcement. Never accept "we agreed" as an artefact.
- Do not suggest artefacts that are not on the minimum set. The point of a minimum set is that
  it is minimal.
- If you cannot tell whether something is current, ask for the one date that would settle it.

WHAT THE TEAM HAS:
<paste links, contents, or an honest list>
```
</details>

---

## P2 → P3 · soft

| Artefact | Owner | One line of what good looks like |
| --- | --- | --- |
| Bolt plan in dependency order | Architect | Each slice buildable and testable alone |
| The score **with its lower bound** | QA | And the number of cases still owed to prove the bar |
| Review lanes by risk band | Engineering | A path rule, not a per-PR argument |
| The bar as a running test, harness in CI | Engineering | A slice below its bar blocks the merge |
| Checker placement and implementation | Engineering | Independent: different model or fresh adversarial context |
| Gated tool implementations | Engineering | Over-cap raises; no-confirm raises; both tested |
| Shadow-run comparison | QA | Decision by decision, over the window, against the threshold |
| Cut-over plan | PM | Five percent first, widen on evidence, rollback rehearsed |

### How it actually goes wrong

The score crosses without its denominator. Eighty-two percent reads as clearing an eighty percent
bar, and on forty cases it has proven nothing — the lower bound is nearer sixty-eight. Then the
cut-over plan says five percent, which is right, and the date beside it was chosen from a calendar
rather than from the division: at 240 cases a day, five percent is twelve cases a day, so a slice
needing 500 cases takes 42 days. Nobody who promised a fortnight had done the arithmetic, and the
pressure that follows is what turns five percent into fifty.

### What good looks like

| Sign | The test |
| --- | --- |
| Every score is three numbers: **n, score, lower bound** | Two numbers is not a result |
| The cut-over date was derived, not chosen | cases needed ÷ (traffic share × cases per day), shown |
| The rollback was **rehearsed** and timed | Four switches, four stopwatch numbers, in the runbook |
| Both gated-tool tests exist, separately | Over-cap and no-confirmation are different holes |
| The harness has blocked a merge | An evaluation that has never gone red is not a gate |

**Whose daily work this is:** [Journey: Engineering lead](Journey-Engineering-Lead) for the harness,
the lanes and the gated tools; [Journey: QA lead](Journey-QA-Lead) for the score, the checker and the
shadow run.

---

## P3 → the next P0 · soft

| Artefact | Owner | One line of what good looks like |
| --- | --- | --- |
| Two-number report | Sponsor | Saving and spend on one line, with the review and re-run rows |
| Drift readout | PM | One output mix, charted weekly, with an alert threshold |
| Redacted trace | Architect | Replayable, and not a breach target |
| Root-cause note for a bill that left its estimate | Architect | One of the four signatures, traced to the decision that allowed it |
| The incident, turned into a brief | PM | Pain, evidence, missing control, fix, value |
| Maturity self-check | Sponsor | A level, its test, and the next control to build |

### How it actually goes wrong

This hand-off has no receiving owner sitting in a meeting, because the next P0 has not started. So
the artefacts are produced and go nowhere: the two-number report is presented and filed, the drift
chart hangs on a wall, the postmortem closes six tickets. SkyWays' refund-versus-credit mix moved
from 61/39 to 48/52 over eight weeks with no deploy, no error and no alert — the threshold was 5%
week over week and the slide averaged 1.9 points a week, so it never fired while the behaviour moved
thirteen points. The chart had been visible the whole time. Nobody owned reading it.

### What good looks like

| Sign | The test |
| --- | --- |
| The drift alert threshold matches the drift the system actually shows | A 5% weekly threshold cannot see a 1.9-point weekly slide |
| A drift alert **re-opens the release gate** without a human deciding to | It is wired |
| The postmortem produced a brief, not a ticket list | Pain, evidence, missing control, value, owner, date |
| The bill root-cause note names an amended ADR | Not an approved budget |
| The trace is replayable and would embarrass nobody if leaked | Search a week of rows for a passport pattern. Zero hits |

**Whose daily work this is:** [Journey: DevOps](Journey-DevOps) for the trace, the bill note and the
rollback; [Journey: Product manager](Journey-Product-Manager) for the drift readout and the brief.

---

## The pack as one picture

<!-- picture:map:the-evidence-pack -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-evidence-pack/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-the-evidence-pack.dark.webp"><img alt="The evidence pack: what each of the four hand-offs owes, with the test for each" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/map-the-evidence-pack.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-evidence-pack/">Open the live, interactive version</a></sub>
<!-- /picture -->

---

## Using the pack

**As a review checklist.** Walk the four artefacts at a design review: the map, the spec, the ADRs and
the authority budget. A review that does not walk them is a look, not a review.

**As an onboarding path.** A new engineer reads the spec, the map and the context layers, in that
order, and can build a bolt on day two.

**As an audit trail.** The pack answers "who decided this, when, on what evidence, and what did they
reject" for every decision that bound the product.

**As a gap report.** Print the four tables. Tick what exists. The ticks you cannot make are your
backlog, in dependency order, for free.

### How it actually goes wrong

The pack is treated as a filing obligation, so it is written once, at the end, by one person, for a
reader who does not exist. Everything in it is true and nothing in it is used — which means nobody
notices when it stops being true. Six weeks later a new engineer reads it, builds against it, and is
wrong in a way that takes three days to find, because a document that is never used is never
corrected.

The four uses above are the correction mechanism. A pack walked at a design review, read by an
onboarding engineer and queried by an auditor gets fixed continuously, by the people who find the
errors, at the moment they find them.

### What good looks like

| Use | Present looks like | Absent looks like |
| --- | --- | --- |
| **Review checklist** | The four artefacts are open on screen and the review follows them | A walkthrough of the code, with the artefacts mentioned |
| **Onboarding path** | A named new joiner built a bolt on day two | Onboarding is pairing, and the pack is never opened |
| **Audit trail** | An audit question was answered from the pack alone, in an hour | The answer required interviewing three people |
| **Gap report** | The backlog's top two items came from unticked rows | The backlog came from a planning meeting |

<details><summary><b>Template · Design review walk sheet</b></summary>

```markdown
# Design review · <feature> · <date>
Four artefacts, walked in this order. Forty-five minutes. Not a code walkthrough.
Chaired by: <architect>   Present: <names>

## 1 · The exact / best-guess / consequential map (10 min)
| Step | Kind | Proof it owes | Present? |
|------|------|---------------|----------|
| <fare rule lookup> | exact | <unit test, equality> | yes |
| <choose alternative> | best-guess | <golden set, share at bar> | yes |
| <issue refund> | consequential | <over-cap test AND no-confirm test> | **one of two** |

Question asked at every row: **is this the kind of step we think it is?**
Anything reclassified here: <>

## 2 · The spec (10 min)
| Field | Present | The question the room asked |
|-------|---------|------------------------------|
| <the bar, per slice> | yes | <derived from what?> |
| <the fallback> | yes | <to which queue, within how long?> |

## 3 · The decision records (10 min)
| ADR | Sensitivity point | Status | What was rejected | Still true? |
|-----|-------------------|--------|-------------------|-------------|
| <ADR-001> | <cost per case> | accepted | <all-frontier routing> | <measured? no> |

Any ADR whose number has never been measured since it was ratified: <list it. This is the
day-75 failure mode.>

## 4 · The authority budget (15 min — the longest, deliberately)
| Tool | Band | Cap | Cap enforced where? | Approver enforced where? |
|------|------|-----|---------------------|---------------------------|
| <refund> | R4 | <$400> | <signature? policy? PROMPT?> | <> |

<The only acceptable answers in the last two columns are a file and a line. "The prompt" is
recorded as NOT ENFORCED and becomes an action before this review closes.>

## Actions out of this review
| # | Action | Owner | Due | Which of the four it came from |
|---|--------|-------|-----|--------------------------------|
| 1 | | | | |
```
</details>

<details><summary><b>Template · Gap report</b></summary>

```markdown
# Evidence pack gap report · <product> · <date>
Produced by printing the four hand-off tables and ticking what exists. Twenty minutes.

## Score
| Hand-off | Owed | Present | Stale | Absent |
|----------|------|---------|-------|--------|
| P0 → P1 | 7 | <n> | <n> | <n> |
| P1 → P2 **hard** | 9 | <n> | <n> | <n> |
| P2 → P3 | 8 | <n> | <n> | <n> |
| P3 → P0 | 6 | <n> | <n> | <n> |

## The backlog this produces, in dependency order
| # | Missing artefact | Depends on | Owner | Estimate | What it unblocks |
|---|------------------|------------|-------|----------|------------------|
| 1 | <exact / best-guess map> | – | <architect> | <20 min for one feature> | <the bar sheet and the authority budget> |
| 2 | <acceptance bar sheet> | <1> | <PM> | <an afternoon> | <the harness> |
| 3 | <authority budget> | <1> | <architect> | <an afternoon> | <gated tool tests, review lanes> |

<Dependency order is free: the map is the artefact the other two are derived from.>

## Present but WRITTEN ONLY — controls that are decided and not enforced
| Control | Decided in | Lives in today | Must live in | Owner | Due |
|---------|-----------|-----------------|--------------|-------|-----|
| <$400 cap> | <day 6> | <the system prompt> | <tool signature> | <name> | <date> |

<Treat this table as more urgent than the absent list. An absent artefact is a known gap; a
written-only control is a gap everybody believes is closed.>

## Stale — present, and the system has moved past them
| Artefact | Last changed | What moved underneath it | Refresh by |
|----------|--------------|---------------------------|------------|
| | | | |

## The two we are doing this fortnight
<name two. Not six.>
```
</details>

<details><summary><b>Prompt · Answer an audit question from the pack alone</b></summary>

```text
You are answering an audit question using ONLY the evidence pack pasted below. You may not use
general knowledge about how such systems usually work.

The question: "<e.g. why is the refund cap $400, who decided it, on what evidence, and what
was rejected?>"

Produce:
1. The answer, in under 120 words, with a citation to a specific artefact and date for every
   claim. Format each citation as [<artefact>, <version or date>].
2. | Part of the question | Answered by | Citation | Confidence: EVIDENCED / INFERRED / NOT IN PACK |
3. Everything the pack does NOT answer, stated as a gap rather than filled in.
4. For each gap, the artefact that should have contained it and who owns that artefact.
5. One sentence: if an auditor asked this question today, would the pack alone satisfy them?

RULES:
- Never fill a gap with a plausible reason. NOT IN PACK is the correct and useful answer.
- Distinguish the decision from its enforcement. "The cap was decided on <date>" and "the cap
  is enforced in <file>" are two different claims needing two different citations.
- If an artefact is undated or unversioned, say so — an uncited artefact is weak evidence.
- Do not recommend improvements to the pack. Answer the question and list the gaps.

THE PACK:
<paste>
```
</details>

<details><summary><b>Prompt · Build the onboarding path from the pack</b></summary>

```text
You are writing a two-day onboarding path for an engineer joining a team that builds an agentic
product. They have the evidence pack below and nothing else. No pairing, no meetings.

Produce:
1. A reading order — the artefacts, in sequence, with one line on what each answers and roughly
   how long it takes to read. Aim for under three hours of reading in total.
2. After each artefact, one question the reader should be able to answer. Give the answer from
   the pack so they can check themselves.
3. The first bolt they should build on day two, chosen from the story files: the smallest one
   that touches the real spine rather than a leaf.
4. A list of every question they will still have to ask a person. Each one is a gap in the pack
   — say which artefact should have closed it.

RULES:
- Order by dependency, not by importance. The map before the bar sheet, because the bar sheet
  is derived from it.
- Do not include anything not in the pack. If the pack lacks a context file, say the first day
  will be spent discovering conventions, and that this is the cost of not having one.
- Never suggest they "ask the team if unsure". The point of this exercise is to count how often
  they would have to.
- Keep it under one page.

THE PACK:
<paste the index and the artefacts>
```
</details>

---

## Where a model helps across this page

| Tool | Use it for |
| --- | --- |
| **Claude Code** | The enforcement check on the hard gate: grep the tool signatures for the cap, the policies for the approver, the branch protection for the required check. A control it cannot find in code is written only |
| **Claude Code** | Staleness. Compare each artefact's last-changed date against the last change to the code it describes, and list the ones the system has moved past |
| **Chat LLM** | Scoring the pack against the minimum set, with STALE and THIN as real verdicts rather than a tick or a cross |
| **Chat LLM** | Rehearsing the audit: ask it a question about a decision and let it answer from the pack alone. What it cannot answer is what an auditor will not be able to either |
| **Do not delegate** | Deciding to cross the hard gate with a row unticked. The model can score the pack; the person whose name is on the sheet is the control |

---

## Try it

Pick your current feature and fill in the P1 → P2 table honestly — the hard-gate one.

Then add one column to it: **enforced, or only written?** A cap in a prompt, an approver in a runbook
and a redaction rule in a convention all go in the second column. Grep for each one; the whole
exercise takes twenty minutes and it is the single highest-yield thing on this page.

<details>
<summary>What to do with the gaps</summary>

Two artefacts are missing on almost every team: the **acceptance bar per slice** and the **authority
budget**. They are also the two cheapest to produce, roughly an afternoon each, and they are the two
that show up in production incidents when absent. Build those two before adding anything else to the
pack.

If the **exact / best-guess map** is missing as well, build it first. It is the artefact the other two
are derived from, and it takes twenty minutes for one feature.
</details>

<details>
<summary>What the enforced-or-written column usually turns up</summary>

A team that scores nine out of nine on existence typically scores six or seven once the column is
added, and the rows that fail are almost always the same two: the cap and the approver. They fail
together, because both were decided in the same conversation and neither produced a code change.

That is the exact state SkyWays was in when it crossed the gate on day 12, and it stayed in it for
seventy days without anything going wrong — which is the part worth sitting with. A written-only
control is not a gap the team feels. It is a gap that feels closed, right up until the day it is
tested by a case nobody wrote.
</details>

<details>
<summary>Try it · the audit rehearsal</summary>

Take the number in your product that a regulator or a customer would most likely ask about. For
SkyWays it is the $400.

Answer four questions using the pack alone, with a citation for each: who decided it, when, on what
evidence, and what was rejected. Then answer a fifth, which is the one that matters: **where is it
enforced, and which test fails if it is removed?**

Most teams can answer the first four from the pack in about ten minutes. The fifth is either a file
and a line, or it is a conversation — and a conversation is the answer you do not want to be giving
in the week after an incident.
</details>

---

**Next:** [Gates and Governance](Gates-and-Governance) · [The Agentic PDLC](The-Agentic-PDLC) ·
[Formulas and Calculators](Formulas-and-Calculators) · [Exercises and Answers](Exercises-and-Answers) ·
[Journey: Solution architect](Journey-Solution-Architect) · [Journey: QA lead](Journey-QA-Lead)
