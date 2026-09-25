# Solution architect · the journey, end to end

**From requirements to a system that holds**

8 steps · 55 sub-steps · 8 templates · 24 prompts

This is the reading copy. The [interactive version](https://akash-coded.github.io/aws-bedrock-agentcore-strands/solution-architect/) has a copy button on every template and prompt, which is what you want when you are actually doing the work.

This page is the walk. For the standing definition of the job, what you own, what you may settle alone, what crosses your desk and how the role fails, see [Role Solution Architect](Role-Solution-Architect).

---

The method has not changed. You still run discovery, sort constraints before you ratify anything, write quality requirements as scenarios, build utility trees, record the decisions that involved a trade-off, and review a design against artefacts rather than against a diagram. Twenty years of craft carries straight over, and the part that carries over is most of the job.

What changes is that some of the steps you are designing are **probabilistic**, and a probabilistic step needs a different kind of proof. An exact step is proven by a unit test that is green or red. A best-guess step is proven by a measured share on real cases. A step that changes something real is proven by a confirmation the model cannot mint. Deciding which is which, before anyone builds, is the artefact this role is really for.

Eight steps, from the first discovery meeting to the incident that redesigns the system. Each ends in something engineering, QA or the product manager needs, with the template to write it and the prompts to draft it faster.

## The arc

Eight steps, and the four phases they sit in. Where the hard gate falls on your own arc is the thing worth noticing: it is a different place for every role.

<!-- picture:wikimap:journey-solution-architect -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-solution-architect.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-solution-architect.dark.webp"><img alt="The solution architect's eight steps placed on the four phases, with the artefact each one produces" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-solution-architect.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-solution-architect.light.webp">Open the picture full size</a></sub>
<!-- /picture -->


| # | Phase | Step | What it produces |
| --- | --- | --- | --- |
| 1 | P0 | [**Elicit**, Run two discovery meetings and credit every line](#1--elicit) | Credited requirements email |
| 2 | P0 | [**Constrain**, Sort the constraints, then write every NFR as a scenario](#2--constrain) | Constraint register + candidate NFR scenarios |
| 3 | P1 | [**Map**, Tag every step exact, best-guess or consequential](#3--map) | Exact / best-guess / consequential map |
| 4 | P1 | [**Shape**, Decide how many agents, and how deep the process runs](#4--shape) | Agent-fit and process-depth decision |
| 5 | P1 | [**Decide**, Merge the utility trees, then write only the ADRs that earn one](#5--decide) | Ratified NFR sheet + the ADRs at the sensitivity points |
| 6 | P1 | [**Bound**, Set the authority budget before the token budget](#6--bound) | Authority budget + gate map |
| 7 | P1 | [**Detail**, Layer the context, wrap the system, place the checker](#7--detail) | Layered context spec + server schema + checker placement |
|  —  | P2 | *Answers against the map; does not re-open it* |  —  |
| 8 | P3 | [**Evolve**, Make the running system cheap, auditable and able to redesign itself](#8--evolve) | Caching and routing config · redacted trace spec · the incident ADR |

## What is yours, and what is not

| Yours to own | Not yours, stop signing these |
| --- | --- |
| The **ratified NFRs**, their sensitivity points, and the workshop that produces them | The **intent** and **release** gates. Those are the product manager's, and your name on them dilutes the two you do hold |
| The **exact / best-guess / consequential map**, and the proof each kind needs | Temperature, top-p, framework version, SDK call shape, you specify behaviours, engineering picks the knobs, and a knob in a design document is wrong at the next release |
| The shape: how many agents, and the named limit that would justify another one | The golden set's contents and the judge rubric. QA curates the cases, you place the checker |
| The **authority budget** and the gate map: every cap in a tool signature | Which pain is worth solving, and what a mistake costs the business |
| The architecture decision records, one per trade-off point and nowhere else |  |
| The **plan gate**, shared with the product manager, and the drift tests at every bolt |  |

## How to use a model in this role

> Use a model where the work is **mechanical and checkable**, and nowhere near the trade-offs. It will turn two transcripts into a credited requirement register, rewrite nine adjectives as six-part scenarios, grep a repository for arithmetic hiding in prompts, and draft an MCP schema from an API surface, all of it faster than you and none of it beyond your ability to verify. It will also band a money tool R2 because the diff is one line, put everything in the shared context layer, and write an ADR whose rejected-options section flatters the decision you already made. Where a step below says *do not delegate*, the reason is always the same: the answer is a fact about your business, your regulator or your risk appetite, and the model has no way to know any of them.

---

> **P0 · Frame begins here**, *is this worth doing, is it AI at all, and how much may the machine do?*

## 1 · Elicit

### Run two discovery meetings and credit every line

*Days one to four, before anybody writes a quality target*

Six people have a say, and putting all six in one room first is the mistake. You get the same thirty-one requirements, forty minutes of two of them talking past each other, and less goodwill than you started with. Two meetings split by proximity to the work get you the same lines with the goodwill intact, because the second meeting exists for whoever was not in the first. Then the discipline the rest of the role rests on: **credit before you consolidate.** A voice that was dropped comes back in week five as a constraint, and by then it arrives as a change request.

**What you actually do**

1. **Split discovery in two, by proximity to the work**: The three most senior give you cost and control and no frontline view; the three closest to the work give you speed and systems and no compliance view. Either order works. What does not work is one room of six.
2. **Read every requirement back, with the name attached**: Eleven minutes for thirty-one lines. The duplicates get read out four times and nobody objects, because each of the four belongs to somebody sitting there.
3. **Refuse to consolidate on the whiteboard**: Live consolidation produces twelve clean lines and two people who spend the project believing theirs was deleted. Consolidation is an editing job and it belongs in the email, where the reasoning can sit beside it.
4. **Send all the lines, credited, duplicates kept**: The consolidation goes underneath with its rationale. Sending only the twelve saves one page and costs an afternoon of replies, all asking the same question.
5. **Flag the requirements that describe a model's behaviour**: Usually three of them. They cannot be satisfied by a function, and their acceptance will be a measured share rather than a pass or a fail, so the shape is settled here instead of argued in the sprint that has to test them.
6. **Write down who was not in either room**: Name them, name the constraint they hold, and book the meeting. An unheard stakeholder is a late constraint, and a late constraint re-opens NFRs that were already ratified.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Paste both transcripts and ask for one row per distinct requirement with every speaker's name on it. It is very good at noticing that four people described one thing four ways.<br>⚠ It merges and drops attribution by default. Require a name on every line, then check the count: distinct rows plus duplicates should equal what you actually heard. |
| **Claude Code** | Have it hold the register as a file (id, verbatim line, person, meeting) and generate the consolidation map from it, so the email is produced rather than retyped.<br>⚠ Make it assert that every source requirement appears in exactly one consolidated line. A requirement that appears in none is the one that comes back in week five. |
| **Chat LLM (cheap tier)** | Separate the requirements from the things that are not requirements: motivations, solutions and preferences. Three piles, and only one of them belongs in the email.<br>⚠ It accepts a solution as a requirement when it is phrased as one. Re-read every line that names a technology; almost none of them are requirements. |
| **Do not delegate** | The read-back itself. The mechanism is a person hearing their own words said aloud with their name attached, and there is no version of that a model performs on your behalf. |

**The artefact**

| | |
| --- | --- |
| Produces | **Credited requirements email** |
| Good looks like | Every line as it was raised, credited, duplicates intact, with the consolidation and its reasoning underneath. A stakeholder finds their own words in under ten seconds. |
| Owner | Solution architect |

<details><summary><b>Template · Credited requirements email</b></summary>

```markdown
# Requirements identified by the team and key stakeholders
_<product> · discovery on <date 1> and <date 2> · circulated by <name>, <date>_

Below are **all <n> requirements**, each credited to the person who raised it.
Duplicates are kept deliberately: if two of you said the same thing, both lines are
here. The consolidation follows underneath, with the reasoning for each merge.

## Every line, as it was said
| ID | The requirement, in the words it was raised | Raised by | Meeting |
|----|--------------------------------------------|-----------|---------|
| FR-01 | <Show alternative flights within one screen> | <R. Mehta, frontline> | 1 |
| FR-02 | <Show the passenger their options quickly> | <R. Mehta, frontline> | 1 |
| FR-03 | <Options must appear fast enough to hold a call> | <S. Okafor, contact centre> | 1 |
| ... | | | |
| FR-<n> | <Every refund must be attributable to a person> | <A. Lindqvist, compliance> | 2 |

## Consolidated to <m> functional requirements
| ID | Consolidated requirement | From | Why these merged |
|----|-------------------------|------|------------------|
| FR-A | <Present ranked alternatives within 30 seconds at P95> | FR-01, FR-02, FR-03 | <one behaviour, three phrasings; the measure is FR-03's> |
| FR-B | | | |

**Coverage:** every one of the <n> lines above appears in exactly one consolidated
requirement. Nothing was dropped.

## Conflicts: for the workshop, not for an editor
| ID | Requirement A | Requirement B | Who holds each | Workshop item |
|----|--------------|---------------|----------------|---------------|
| X-1 | <FR-07, faster options> | <FR-22, lower cost per case> | <name> / <name> | <date> |

## The requirements that describe a model's behaviour
These cannot be satisfied by a function. Their acceptance will be a measured share
on real cases, not a pass or a fail, and they are flagged now so that nobody writes
their acceptance criteria in the wrong shape.
- FR-<n>: <why two competent people could differ>

## Raised, but not a requirement
| Raised as | What it actually is | Where it went |
|-----------|--------------------|---------------|
| <No headcount this year> | a motivation | the pain register |
| <We should use <framework>> | a solution | the build / buy / borrow matrix |

## Who was not in either room
| Who | The constraint they hold | Meeting booked |
|-----|-------------------------|----------------|
| <role, named> | <what only they know> | <date> |

## What happens next
Constraints sorted by type on <date>. Candidate NFRs as six-part scenarios on
<date>. The ratification workshop on <date>. Reply if a line is wrong, missing or
credited to the wrong person, that correction is free now and expensive in week five.
```

</details>

<details><summary><b>Prompt · Consolidate two discovery transcripts, credit intact</b>, After the second meeting, before you write the email</summary>

```text
You are helping a solution architect consolidate two discovery meetings about
<problem area>.

OUTPUT SHAPE: one markdown table, one row per DISTINCT requirement:
| FR id | The requirement, in the words it was raised | Everyone who raised it (names) | Meeting(s) |

RULES:
- Keep EVERY name. If four people raised the same requirement, all four names go on
  that row.
- Number rows FR-01 upward in the order first said, not in order of importance.
- Do not rewrite anyone's phrasing into better English. The verbatim line is the
  point; it is what each person will look for.
- Do not merge two requirements with different causes, even when they share a symptom.
- Below the table, list separately under three headings: MOTIVATIONS (why the project
  exists), SOLUTIONS (someone naming a technology or design), PREFERENCES. None of
  these are requirements.
- Finish with three counts: distinct requirements, total lines heard, names credited.

TRANSCRIPT 1, <who was in the room>:
<paste>

TRANSCRIPT 2, <who was in the room>:
<paste>
```

</details>

<details><summary><b>Prompt · Build the consolidation map, and prove it is complete</b>, You have the full credited list and need the short one</summary>

```text
Here is the full credited requirement list: <paste>.

Produce the consolidation, and prove nothing was lost.

OUTPUT SHAPE:
1. | Consolidated ID | Consolidated requirement | From (source ids) | Why these merged |
2. A coverage check: every source id, and the consolidated line it landed in.
3. The list of source ids that landed in NONE. This list must be empty.
4. The list of source ids that landed in MORE THAN ONE. This list must be empty.

RULES:
- A consolidated line must be testable. Three vague lines merged into one vague line
  has saved a page and decided nothing.
- Where sources disagree on a number, take the tightest and name its source in the
  "why" column.
- Never drop a requirement for being minor. Merge it or list it.
- If two sources genuinely conflict, do NOT merge them. Emit a CONFLICT row carrying
  both names. That is a workshop item, not an editing decision.
```

</details>

<details><summary><b>Prompt · Find the requirements that describe a model's behaviour</b>, Before the constraint review, so acceptance is shaped correctly</summary>

```text
Below is a consolidated functional requirement list: <paste>.

Tell me which of these describe a MODEL'S behaviour rather than a function's.

OUTPUT SHAPE, one table:
| FR | Model behaviour? | Why | What its acceptance will have to look like |

RULES:
- It is a model behaviour when two competent people could reasonably differ about
  whether a given output satisfies it.
- If the criteria are published and unambiguous, answer NO. It is a function and it
  gets a unit test.
- For every YES, the acceptance column says "a measured share on real cases" and
  names the slice the share would be measured on.
- For every NO, the acceptance column names the assertion.
- Be strict. Most requirements are functions. If unsure, answer NO and say what
  would have to be true to make it a judgement.

Finish with the count of YES rows. Three is typical. More than six usually means the
list has not been consolidated tightly enough.
```

</details>

**Worked example · SkyWays · thirty-one lines from six people**

> Day one, the three closest to the work: seventeen requirements, eleven of them about speed and the systems the assistant would have to touch, and no compliance view at all. Day two, the other three, opening with a credited read-back of day one: fourteen more, nine about cost and control. **Thirty-one lines from six people**, four of which were the same requirement said four ways. The read-back took eleven minutes and every duplicate was read out with its author's name on it. The email went on day four with all thirty-one lines and the consolidation to twelve underneath. Nobody replied asking where their requirement had gone. One line (*every refund must be attributable to a person*, from compliance) became the $400 cap two days later, and it was on the list only because somebody who was not in the first meeting was invited to the second.

**Pitfalls**

- Putting all six in one room to save a meeting. You get the same thirty-one requirements, forty minutes of the compliance officer and the frontline agent arguing, and nobody feeling heard.
- Consolidating live, in front of everyone. The whiteboard version looks efficient and it produces two stakeholders who believe their requirement was deleted, which surfaces as resistance later.
- Sending only the consolidated list. It saves one page and costs an afternoon of replies, and every reply is the same question about where a line went.

**Done when**, Any of the six can open the email, find their own words verbatim with their name beside them, and follow the line to the consolidated requirement it became.

---

## 2 · Constrain

### Sort the constraints, then write every NFR as a scenario

*Days six to nine, and never after ratification*

A constraint can make a quality target impossible, so constraints come first, and they are sorted **by type**, because the type decides what each one does to the design. A technical constraint reshapes the integration, a regulatory one becomes a number inside a tool signature, and a commercial one bounds the tier you may choose. Only then the quality requirements, written as six-part scenarios, because an adjective cannot be tested, ranked or traded off. Two of them are the ones teams forget to write and then need: the **autonomy level** and the **cost per case**.

**What you actually do**

1. **Sort every constraint into technical, regulatory or commercial**: The type is not a filing convenience. Regulatory becomes a typed parameter, technical forces an adapter or a server in front of something, commercial bounds the model tier and therefore the latency you can promise.
2. **Strike the motivations that are pretending to be constraints**: *No headcount this year* does not bound the design; it is the reason the assistant exists, and it belongs in the pain register. The test is whether the line names a design it rules out.
3. **Turn each regulatory constraint into a number and a place**: Refunds over $400 need a named approver is a number and a location, a typed parameter and a token the model cannot mint. Left as a sentence it stays a sentence, and a sentence is what a postmortem finds missing.
4. **Write every candidate NFR in six parts**: Source, stimulus, artefact, environment, response, measure. The part everyone omits is environment (under what load, at what hour, in what degraded state) and its absence is precisely what makes a latency target arguable for two hours.
5. **Add autonomy level and cost per case to the candidate list**: Both are quality attributes and both are measurable. A ratified cost per case is what makes an unexpected bill a monitored number with an alert rather than a surprise arriving four weeks late.
6. **Ground every measure in something real before the workshop**: Pull the current P95 from the request log. A measure invented in the room is ratified in the room and missed in production, and nobody can say when it became unachievable.
7. **Hold the constraint review before anything is ratified**: Ratify first and add constraints after, and the room signs a latency target the legacy adapter cannot meet. Then the workshop is held twice, with the same six people.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Have it rewrite adjective-shaped requirements as six-part scenarios, with a line under each naming which of the six parts the original did not contain.<br>⚠ The missing-parts line is the output that matters. Without it, it invents a plausible environment clause and you ratify a condition nobody agreed to. |
| **Claude Code** | Point it at the request log and have it report the current P95, the peak hour and the shape of the tail, so the measure in the scenario is grounded in today's behaviour.<br>⚠ Read the query. A P95 across all hours is not the P95 the scenario is about, and the gap between the two is usually the entire argument. |
| **Chat LLM (cheap tier)** | Sort a raw constraint dump into technical, regulatory and commercial, and flag every line that does not bound the design.<br>⚠ It files organisational motivations under commercial because they mention money. Re-read that pile asking of each line: what design does this rule out? |
| **Do not delegate** | Deciding whether a constraint is real. The only way to learn that a $400 threshold is a policy your compliance officer can change, rather than a regulation, is to ask her. |

**The artefact**

| | |
| --- | --- |
| Produces | **Constraint register + candidate NFR scenarios** |
| Good looks like | Every constraint typed and naming a design it rules out, and every candidate NFR in six parts with a number in the measure and a source for that number. |
| Owner | Solution architect |

<details><summary><b>Template · Constraint register and candidate NFRs</b></summary>

```markdown
# Constraints and candidate NFRs · <product>
_Compiled: <date> · Owner: <name> · Ratification workshop: <date>_

## Constraints, by type
| # | Constraint | Type | The design it rules out | Source |
|---|-----------|------|------------------------|--------|
| C-1 | <Every refund over $400 needs a named approver> | regulatory | <any autonomous refund path; becomes a typed cap plus an approver token> | <A. Lindqvist, compliance, <date>> |
| C-2 | <The reservation system exposes SOAP only> | technical | <direct integration; forces an adapter or one server in front> | <platform team> |
| C-3 | <Passenger data must stay in region> | regulatory | <any cross-region model endpoint> | <legal, <date>> |
| C-4 | <No new licence spend above $<n> a year> | commercial | <the managed tier of options B and C> | <finance> |

**Test applied to every line:** it names a design it rules out. If that column would
be empty, it is not a constraint.

## Struck from the list
| Raised as a constraint | What it is | Where it went |
|-----------------------|------------|---------------|
| <No headcount this year> | a motivation | the pain register |
| <We should use <framework>> | a solution | the build / buy / borrow matrix |

## Candidate NFRs, as six-part scenarios

### NFR-<n> · <latency>
| Part | Value |
|------|-------|
| Source | <a disrupted passenger> |
| Stimulus | <asks for rebooking options> |
| Artefact | <the rebooking assistant> |
| Environment | <during a peak hour, with one partner API degraded> |
| Response | <proposes ranked alternatives> |
| Measure | <within 30 seconds at P95> |

_Measure grounded in:_ <request log, <date>, today's P95 is <n>s>
_Constraint it must respect:_ <C-2, the adapter adds <n>s>

### NFR-<n> · autonomy level
| Part | Value |
|------|-------|
| Source | <the agent> |
| Stimulus | <reaches a step that changes something real> |
| Artefact | <the tool layer> |
| Environment | <normal running, and during an incident> |
| Response | <requires the approver named for that action> |
| Measure | <100% of <action> calls carry a confirmation token; over-cap raises> |

### NFR-<n> · cost per case
| Part | Value |
|------|-------|
| Source | <a passenger request> |
| Stimulus | <completes one rebooking conversation> |
| Artefact | <the assistant, across every model call it makes> |
| Environment | <at <n> cases a day, cached and routed> |
| Response | <completes within budget> |
| Measure | <$<n> per case, alerting at 3x on the daily per-call log> |

## Missing before the workshop
| What | Who can produce it | By when |
|------|--------------------|---------|
| <peak-hour P95 through the adapter> | <platform> | <date> |
| <whether C-1 is regulation or policy> | <compliance> | <date> |
```

</details>

<details><summary><b>Prompt · Adjective to six-part scenario</b>, You have a list of quality requirements and none of them can be tested</summary>

```text
Rewrite each quality requirement below as a six-part scenario.

The six parts: SOURCE (who or what triggers it) · STIMULUS (what they do) · ARTEFACT
(the part of the system that responds) · ENVIRONMENT (load, hour, degraded state) ·
RESPONSE (what the system does) · MEASURE (the number, with its statistic).

OUTPUT SHAPE, per requirement:
- the original line, verbatim
- a table of the six parts
- one line: PARTS MISSING FROM THE ORIGINAL: <list them>

RULES:
- Never invent a number. Where the original has no measure, write
  <MEASURE NOT STATED> and collect it in a list at the end.
- Never invent an environment. Write <ENVIRONMENT NOT STATED>. Do NOT write "under
  normal load". That is the invented clause that gets ratified and then argued about
  for the rest of the project.
- The MEASURE must carry a statistic: P95, per case, per week, percentage of a named
  slice. "Fast" and "under 30 seconds" are both unfinished, for different reasons.

Finish with two lists: measures not stated, and environments not stated. Those two
lists are what I take back to the people who raised the requirements.

REQUIREMENTS:
<paste>
```

</details>

<details><summary><b>Prompt · Sort a constraint list, and test every line</b>, You have a dump of constraints from four sources</summary>

```text
Sort the lines below into TECHNICAL, REGULATORY, COMMERCIAL or NOT A CONSTRAINT.

OUTPUT SHAPE, one table:
| Line | Type | The design it rules out | Where it must end up | Source named? |

RULES:
- The test for a constraint is that it names a design it rules out. Apply it to every
  line and fill the third column. If that column would be empty, the type is NOT A
  CONSTRAINT.
- NOT A CONSTRAINT splits three ways and you must say which: a MOTIVATION (the reason
  the project exists), a SOLUTION (someone naming a technology), a PREFERENCE.
- For every REGULATORY line, the fourth column names a place in the system: a typed
  parameter, a required token, a permission. Never "the prompt".
- For every TECHNICAL line, the fourth column names the integration shape it forces:
  an adapter, one server in front, a queue.
- Flag any line with no named source. An unsourced constraint usually turns out to be
  somebody's memory of a rule that has since changed.

LINES:
<paste>
```

</details>

<details><summary><b>Prompt · Write the two NFRs everyone forgets</b>, Your candidate list is complete and you suspect it is not</summary>

```text
I am writing candidate NFRs for <feature>. I have <n> so far, listed below.

Write exactly two more, as six-part scenarios, and only these two:
1. AUTONOMY LEVEL: what the system may do without a person, per action.
2. COST PER CASE: the run cost of one completed case, across every model call.

RULES:
- Both must be measurable and both must carry a number in the MEASURE part.
- For autonomy, the measure is about ENFORCEMENT, not intent. "100% of <action> calls
  carry a confirmation token" is a measure; "the agent asks before refunding" is not.
- For cost per case, put the alert multiple inside the measure, so the number is
  monitored rather than merely agreed.
- Then, for each NFR I already have, say in one line whether the new one is in tension
  with it. I expect latency against cost per case; tell me if there are others.
- Say explicitly which tensions are NOT real. Auditability against latency usually is
  not: logging costs milliseconds and the model choice costs seconds.

Do not propose any other NFRs. I have the rest.

MY CURRENT LIST:
<paste>
```

</details>

**Worked example · SkyWays · the sentence that should have been a signature**

> Day six, the constraints went up sorted by type. Regulatory: **every refund over $400 needs a named approver**, and *passenger data stays in region*. Technical: the reservation system exposes SOAP only, which decided the integration shape before anyone argued about it. Commercial: a licence ceiling that later became a weight in the build/buy/borrow matrix. One line, *no headcount this year*, was struck as a motivation and moved to the pain register. Nine candidates went into the workshop as six-part scenarios, and two of them, **autonomy level** and **cost per case at $0.60**, were on the list only because someone asked what was missing. The $400 was a number from day six. It was still only a number in a document on day 82, when a $2,000 refund went out with neither the cap nor the approver anywhere in the code, which is a failure of step six, not of this one, and the difference is worth being precise about.

**Pitfalls**

- Ratifying the NFRs and adding the constraints afterwards. The room signs a latency target the legacy adapter cannot meet, and the whole workshop is held a second time.
- An NFR that is an adjective. *Fast*, *reliable* and *secure* survive the workshop because nobody can disagree with them, and then they cannot be tested, ranked or traded against anything.
- Leaving cost per case off the candidate list. It is the quality attribute that arrives as an invoice, and a number nobody ratified is a number nobody monitors.

**Done when**, Every candidate NFR has all six parts with a statistic in the measure and a source for that number, and every line on the constraint register names a design it rules out.

---

> **P1 · Design & Spec begins here**, *what exactly is being built, and under whose authority?*

## 3 · Map

### Tag every step exact, best-guess or consequential

*P0, the first design artefact, and it takes an hour for one feature*

The product manager sorted the feature. This is a judgement, this is arithmetic. That is right and it is not enough. You sort at the level of **every step**, and you add the column that decides both what gets built and how it gets proven. Exact steps are functions proven by a unit test. Best-guess steps are model calls proven by a measured share on real cases. Consequential steps are a tool plus a gate, proven by a required confirmation. Choosing the kind of evidence each step will need, before anybody builds it, is what the artefact is for.

**What you actually do**

1. **List steps, not features**: Read the booking, find candidates, compute the fare difference, check eligibility, draft the message, rebook, refund. Seven rows for one feature is normal, and the rows are where the design actually lives.
2. **Tag each step exact, best-guess or consequential**: Exact means right every single time. Best-guess means right a share of the time. Consequential means it changes something real, and a step is often consequential as well as one of the other two rather than instead of it.
3. **Fill the proof column before anything else**: A unit test, a measured share on a named slice, or a required confirmation. Engineering builds from the kind column and QA builds their test plan from the proof column, which is what makes an hour's work worth an hour.
4. **Draw the data flow and mark where numbers cross**: Numbers flow from an exact step into a best-guess one and never the other way. Drawing the arrows is how you find the step that computes a value and then acts on it.
5. **Apply the rule that never breaks**: The best-guess machine never does the exact math. The model may call the function and read the result; it never computes the value it then acts on. A fluent wrong number is the failure no prompt-level test catches, $80 when the ledger says $62.
6. **Grep the prompts for calculate, compute and total**: Each hit is a function waiting to exist. It takes ten minutes and it is the most reliably productive ten minutes available to this role.
7. **Hand the map to QA as their test plan**: The proof column is already the shape of their work: which steps need assertions, which need a golden slice with a bar, and which need a confirmation test that fails closed.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Give it the step list and the three definitions and ask for a tagged table with the proof column filled. A good first pass on an unfamiliar feature, and it surfaces steps you had quietly folded together.<br>⚠ It under-uses **consequential**. Re-read every row: anything that writes, sends, books, cancels or moves money is consequential whatever else it also is. |
| **Claude Code** | Have it search the repository (prompt files, system messages, tool descriptions, long string literals) for arithmetic verbs and currency symbols, and list every hit with its file and line.<br>⚠ It matches vocabulary, not intent. *Tell the passenger what they owe* is arithmetic in a prompt and contains none of the words you searched for. |
| **Chat LLM, adversarially** | Ask it to find the step that is doing two things at once. A step you cannot classify is almost always a judgement and a calculation bundled into one call, and both halves classify immediately once they are separated. |
| **Do not delegate** | Deciding what counts as money. Whether a fee waiver, a goodwill credit or a seat upgrade is a consequential action is a fact about your business, and the model guesses from the wording of the step. |

**The artefact**

| | |
| --- | --- |
| Produces | **Exact / best-guess / consequential map** |
| Good looks like | One row per step with its kind, its owner and its proof. Engineering can see what to write in code, QA can see what to test and how, and every number the feature computes sits on the code side of the line. |
| Owner | Solution architect |

<details><summary><b>Template · Exact / best-guess / consequential map</b></summary>

```markdown
# Exact / best-guess / consequential map · <feature>
_Drawn: <date> · Owner: <name> · Read by: engineering and QA_

## The three kinds
| Kind | What it is | Built as | Proven by |
|------|-----------|----------|-----------|
| Exact | Must be right every single time | A function | A unit test, green or red |
| Best-guess | Right a share of the time | A model call | A measured share on real cases |
| Consequential | Changes something real | A tool **plus** a gate | A required confirmation |

## The map
| # | Step | Kind | Owner | Proof | The assertion or bar |
|---|------|------|-------|-------|---------------------|
| 1 | <read the booking> | exact | code | unit test | <returns the record or raises> |
| 2 | <find candidate flights> | best-guess | model | measured share | <80% on codeshare, n = 500> |
| 3 | <compute the fare difference> | **exact** | code | unit test | <100 - 20 = 80, always> |
| 4 | <check visa and codeshare eligibility> | exact | code | unit test | <rule table, every branch> |
| 5 | <draft the passenger message> | best-guess | model | independent judge | <tone, policy, no invented claims> |
| 6 | <rebook the seat> | consequential | tool + gate | required confirmation | <no token, raises> |
| 7 | <issue a refund> | consequential | tool + gate | required confirmation | <amount <= <cap>, named approver> |

## Data flow
<booking> -> 1 -> 2 -> 3 (numbers only) -> 4 -> 5 -> 6 -> 7

**The rule that never breaks:** the best-guess machine never does the exact math. The
model may call step 3 and read its result. It never computes the value it then acts on.

## Arithmetic found inside prompts
| File | Line | The phrase | What it computes | The function it becomes |
|------|------|-----------|------------------|------------------------|
| <prompts/rebook.md> | <42> | <"work out what they owe"> | <fare difference> | <fare_difference(pnr, new_leg)> |
| | | | | |

Acted-on values are the urgent list. Displayed-only values can wait a cycle.

## Steps that resisted classification
| Step | The two things it was doing | How it split |
|------|----------------------------|--------------|
| <"price and recommend"> | <a judgement and a calculation> | <rank_alternatives() + fare_difference()> |

## Handover
- Engineering builds from the **Kind** column.
- QA builds the test plan from the **Proof** column.
- Every consequential row also appears in the authority budget, banded R1 to R5.
```

</details>

<details><summary><b>Prompt · Tag a feature's steps, with the proof column</b>, You have the step list and need the map in front of engineering today</summary>

```text
Tag every step of this feature. Use exactly three kinds.

EXACT: must be right every single time. Built as a function. Proven by a unit test.
BEST-GUESS: right a share of the time. Built as a model call. Proven by a measured
  share on real cases.
CONSEQUENTIAL: changes something real. Built as a tool PLUS a gate. Proven by a
  required confirmation.

OUTPUT SHAPE, one table:
| # | Step | Kind | Owner (code / model / tool+gate) | Proof | The assertion or bar |

RULES:
- A step can be CONSEQUENTIAL as well as exact or best-guess. Tag it consequential and
  say in the owner column what the other half is.
- Anything that writes, sends, books, cancels, refunds or changes an identity is
  CONSEQUENTIAL whatever else it looks like.
- Every number the feature computes and then acts on is EXACT. No exceptions, and do
  not accept "the model is good at arithmetic" as one.
- The proof column may not say "review" or "testing". It says: a unit test, a measured
  share on a named slice, or a required confirmation.
- After the table, draw the data flow as one line of arrows and mark where a number
  crosses from an exact step into a best-guess one.

Finish with: any step you could not classify, and the two things it is doing.

STEPS:
<paste>
```

</details>

<details><summary><b>Prompt · Find the arithmetic hiding in the prompts</b>, Monday morning, on any repository that already has an agent in it</summary>

```text
Search this repository for arithmetic that lives in a prompt instead of in code.

Look in prompt files, system messages, tool descriptions, and any string literal long
enough to be an instruction.

Search for at least: calculate, compute, total, sum, difference, subtract, multiply,
percentage, work out, how much, amount owed, and every currency symbol.

OUTPUT SHAPE, one table:
| File | Line | The phrase | What it computes | ACTED ON or DISPLAYED | The function it becomes |

RULES:
- Match intent, not vocabulary. "Tell the passenger what they owe" is arithmetic and
  contains none of the words above. Include it.
- ACTED ON means the value feeds a tool call, a booking, a payment or a message to a
  customer. That is the urgent list; put it first.
- Do not change any code. Produce the list and a suggested function signature per row.
- Show me the search command you ran BEFORE the results, so I can see what you did not
  look in.
```

</details>

<details><summary><b>Prompt · Split the step that does two things</b>, One step will not classify and the map is stuck on it</summary>

```text
This step resisted classification as exact, best-guess or consequential:

<paste the step, and how it is currently described or prompted>

A step that cannot be classified is almost always doing two things at once: a
judgement and a calculation, or a judgement and a write.

1. Name the two things it is doing.
2. Split it into two steps and classify each.
3. For the exact half, write the function signature (name, typed parameters, return
   type) and the one unit test that would prove it.
4. For the best-guess half, write what it is deciding in one sentence, and the slice
   its measured share would be reported on.
5. State what may pass between them, and in which direction.

If it genuinely is one thing, say so, tell me which kind it is, and tell me why the
classification felt hard, that reason is usually itself a finding.
```

</details>

**Worked example · SkyWays · the row that was worth the hour**

> Seven steps, three kinds. Reading the booking, checking visa and codeshare eligibility and computing the fare difference came out **exact**: lookups and rules, proven by unit tests. Ranking the alternatives and drafting the passenger message came out **best-guess**, proven by a measured share with the codeshare bar at 80%. Rebooking the seat and issuing a refund came out **consequential**: a tool plus a gate, proven by a confirmation. The row that paid for the whole artefact was the fare difference. It had been sitting inside a prompt as *work out what they owe*, and a prompt that computes money produces $80 when the ledger says $62, fluently, with no error and no red test. Ten minutes of grepping found two more like it in the same feature.

**Pitfalls**

- Tagging at the level of the feature. *The rebooking assistant is best-guess* is true and useless; the fare difference inside it is exact, and that single row is why the map exists.
- A prompt that computes a number the agent then acts on. It fails fluently, with no exception and no red test, and the first person to notice is the passenger reading the wrong figure.
- Filling the kind column and leaving the proof column for later. Later is the sprint where QA asks what good looks like for step four, and the answer gets invented under deadline pressure.

**Done when**, Every step has a kind and a proof, and a grep of the prompts for arithmetic verbs and currency symbols returns nothing whose value the agent then acts on.

---

## 4 · Shape

### Decide how many agents, and how deep the process runs

*P0, straight after the map and before any framework is named*

Leadership said agent-first and an engineer has built fifteen agents to show what is possible. Your answer is a number and a condition. **Start single, escalate only on a named limit**, because each added agent is another context to manage and another hand-off to get wrong, and n agents have **n(n-1)/2** possible hand-offs between them. The same judgement governs process: run only the lifecycle stages a given change actually needs, decided per change rather than per programme.

**What you actually do**

1. **Start single, and put the burden of proof on the second agent**: One agent with its tools handles almost every feature. The default is not a preference; it is the only position that makes an addition explain itself.
2. **Count the hand-offs before agreeing to any topology**: Five agents have ten possible hand-offs, fifteen have a hundred and five, and none of them appears in the diagram. Coordination cost grows faster than the work it splits.
3. **Test every proposed agent against a fan-out tool**: Parallelism is a property of a **tool**, not of an agent count. Four partner searches run at once inside one call with zero hand-offs; as four agents they cost six.
4. **Separate out the roles that are not agents at all**: The pricer is exact work and becomes a function. The reviewer is the one separation that usually earns itself, because independence is the entire mechanism of a checker.
5. **Write the escalation condition as a limit with a number in it**: *We move to an orchestrator when a single context exceeds X on multi-leg international* is a decision. *We might need more agents later* is how a swarm comes back by default the first time somebody wants more speed.
6. **Set the process depth per change, not per programme**: A one-line fix skips discovery and most design; a new subsystem runs everything; a regulatory rule change runs design and validation and no discovery. The living spec is the backbone on every row.
7. **Put 'revisit at the trace review' on the record**: Shape is re-decided on evidence, and the evidence arrives in production. A shape decision with no review date hardens into an assumption nobody remembers making.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Describe the proposed topology and ask for the single-agent version of the same feature, with the hand-off count for each. The contrast is the argument you need in the room.<br>⚠ It agrees with whichever design you described first. Ask it to perform the collapse, not to give an opinion on the design. |
| **Claude Code** | Point it at an existing multi-agent repository and have it count the agents, the tools, the distinct contexts and the messages passed between them. Most swarms are a different size from the one on the whiteboard.<br>⚠ Make it list the hand-offs it found rather than only a total. The count you can argue about in a review is the one somebody can read. |
| **Chat LLM, adversarially** | Ask it to make the strongest possible case for the second agent. If the strongest case cannot name a limit with a number in it, you have your answer and it cost five minutes. |
| **Do not delegate** | The escalation condition itself. It depends on your context sizes, your latency budget and the shape of your team, and it is the line that decides whether the design survives contact with an enthusiastic engineer. |

**The artefact**

| | |
| --- | --- |
| Produces | **Agent-fit and process-depth decision** |
| Good looks like | A number of agents, the hand-off count that number implies, and a named limit with a figure in it that would justify the next one. Plus one depth row per kind of change, so method stops being argued per ticket. |
| Owner | Solution architect |

<details><summary><b>Template · Shape and depth decision</b></summary>

```markdown
# Shape decision · <feature>
_Decided: <date> · Owner: <name> · Revisit at: the P3 trace review_

## How many agents
| Question | Answer | Evidence |
|----------|--------|----------|
| Is this AI at all? | <yes: the PM's AI-fit record> | <link> |
| How many agents? | **<n>, with tools** | |
| Does one context genuinely overload? | <no: largest case measured at <n> tokens against a <n> limit> | <measurement, date> |
| Are there parallel sub-tasks a fan-out tool cannot express? | <no: <n> partner searches run inside one tool> | |
| Is the build audited and multi-team? | <no> | |

## The hand-off arithmetic
| Agents | Possible hand-offs, n(n-1)/2 | |
|--------|------------------------------|--|
| 1 | 0 | **chosen** |
| <5> | <10> | <the orchestrator option> |
| <15> | <105> | <the proposal that started this> |

Every hand-off is a place coordination can be wrong, and none of them appears in the
diagram that made the design look reasonable.

## What was proposed, and what it actually is
| Proposed agent | What it really is | Where it goes |
|----------------|-------------------|---------------|
| <the pricer> | exact work | a function, map, step <n> |
| <the searcher> | parallelism | a fan-out tool, <n> calls in one |
| <the reviewer> | independence | a checker: different model, or fresh adversarial context |
| <the planner> | the agent itself | the single agent |

## The escalation condition
We move to <orchestrator + workers> when, and only when:
- <a single context exceeds <n> tokens on <named case class>>, **or**
- <more than <n> sub-tasks must run in parallel AND a fan-out tool cannot express it>

Baseline measured <date>: <the number today>. Anything outside these two is a swarm
arriving by default.

## Process depth, per change
| Kind of change | P0 | P1 | P2 | P3 | Method weight |
|----------------|----|----|----|----|---------------|
| <one-line fix> | — | light | yes | — | living spec + a single agent |
| <this feature> | yes | yes | yes | yes | living spec + the five gates |
| <audited module> | yes | full | full | full | living spec + the full persona trail |
| <regulatory rule change> | — | yes | yes | light | spec diff + validation |

**Rule:** the living spec is the backbone everywhere. The heavy persona trail is
layered on only where the work is audited and multi-team. Depth flexes per change.
```

</details>

<details><summary><b>Prompt · Collapse a proposed topology</b>, Someone has proposed several agents and you have to answer today</summary>

```text
Here is a proposed multi-agent design: <paste, including each agent's job>.

Produce the SINGLE-AGENT version of the same feature, then compare the two.

OUTPUT SHAPE:
1. A table: | Proposed agent | What it really is | Where it goes in the single-agent design |
   Allowed values for the middle column: EXACT WORK (a function) · PARALLELISM (a
   fan-out tool) · INDEPENDENCE (a checker) · THE AGENT ITSELF · GENUINELY A SECOND AGENT.
2. The hand-off count for each design, computed as n(n-1)/2, with n stated.
3. For every GENUINELY A SECOND AGENT row, the named limit that justifies it, a number,
   not an adjective.

RULES:
- Parallelism is a property of a TOOL. Do not accept "these can run at the same time"
  as a reason for a second agent.
- A checker is the one separation that usually earns itself, because independence is
  the whole mechanism. Say so where it applies.
- Arithmetic is never an agent. It is a function.
- If you cannot name a limit with a number in it, write "no limit found" rather than
  inventing one. That answer is the useful one.
```

</details>

<details><summary><b>Prompt · Write the escalation condition</b>, Before the shape decision goes on the record</summary>

```text
I am recording a single-agent design for <feature>. Write the escalation condition
that would justify moving to an orchestrator with workers.

OUTPUT SHAPE: exactly two bullets, each in this form:
  "We move to <topology> when <measurable thing> exceeds <number> on <named case class>."

Then, below them:
- How each thing would be measured today, and with what.
- The measurement I should take NOW as a baseline, so the condition can later be
  evaluated rather than argued about.
- What I would have to change in the design if the condition were met tomorrow.

RULES:
- Every condition carries a number and a named case class. "If the context gets too
  big" is not a condition.
- Do not propose more than two. A list of conditions is a list of excuses.
- Do not include anything of the form "if the team feels it would be cleaner".

CONTEXT: <the feature, the largest case class, current context size if known, the
latency budget, how many parallel calls the fan-out tool makes>
```

</details>

<details><summary><b>Prompt · Assign a depth row to this week's changes</b>, The team wants one process for everything</summary>

```text
Here are the changes my team has in flight: <paste, one per line>.

Assign each a process depth. Run only the lifecycle stages the change actually needs.

OUTPUT SHAPE, one table:
| Change | P0 | P1 | P2 | P3 | Method weight | The stage I am skipping, and why that is safe |

Allowed cell values: full · yes · light ·, 

RULES:
- The living spec is the backbone on EVERY row, including the one-line fixes. It is
  the constant; everything else flexes around it.
- The full persona trail is layered on ONLY where the work is audited and multi-team.
  On a small feature it is twelve personas between an engineer and a one-line change.
- A regulatory rule change usually needs design and validation and no discovery. Say
  where that applies and where it does not.
- The last column is the point of the exercise. If you cannot say why skipping a stage
  is safe, do not skip it.
```

</details>

**Worked example · SkyWays · fifteen agents, a hundred and five hand-offs**

> An engineer had built fifteen agents to show what the framework could do. The collapse took an afternoon and one table. The pricer was exact work and became a function. The searcher was parallelism and became a fan-out tool running four partner queries inside a single call. The planner was the agent itself. Only the reviewer survived as something separate, because independence is the entire mechanism of a checker. One agent, one fan-out tool, one function and one checker, **zero hand-offs against a hundred and five**. The line that mattered most went on the record underneath: an orchestrator when a single context exceeds the measured limit on multi-leg international cases, or when more than three partner calls must run in parallel and one tool cannot express it. Without a number in that sentence the swarm returns by default, and it returns with a reasonable explanation attached.

**Pitfalls**

- Adding an agent for a reason that cannot be written as a limit with a number. *For speed* and *for separation of concerns* both survive a design review and neither can be tested at the plan gate, which is where the addition actually has to be caught.
- Buying parallelism with agents. Four partner searches run at once inside one fan-out tool with no hand-offs at all; as four agents they cost six hand-offs, a coordinator and four contexts.
- One process weight for the whole programme. Heavy ceremony on a one-line fix is twelve personas between an engineer and a change, and light ceremony on the audited module is the audit finding.

**Done when**, The record states a number of agents, the hand-off count that number implies, and a limit with a figure in it that would justify the next one.

---

## 5 · Decide

### Merge the utility trees, then write only the ADRs that earn one

*Day nine, the ratification workshop, and the dated records that follow it*

Nine candidates, six people, two hours. Without the trees the room argues about words and runs out of time exactly on the contested items; with them, the uncontested NFRs go through in twenty minutes and the remaining hundred go to the conflicts, which are the only reason six people were needed at once. A conflict is not a difference of taste. It is a **priority gap of five or more between two stakeholders**, and each one owes a decision record. Records are written at trade-off points and nowhere else, forty records in a week buries the three that mattered.

**What you actually do**

1. **Score every candidate on value and complexity, per stakeholder**: One to three on each, from each person's own point of view. The scoring is quick; the value is that two people who would have argued now disagree in a column you can read.
2. **Compute priority = value × (4 − complexity) and merge the trees**: The formula rewards high value at low difficulty, which is the order a workshop should actually take things in. Merging is what turns six opinions into one agenda.
3. **Mark every gap of five or more as a conflict**: Below five it is a difference of emphasis and the room will settle it in a minute. At five and above there is a genuine trade-off underneath, and that is what a record is for.
4. **Ratify the uncontested candidates first, as one block**: Six go through in twenty minutes because the trees already agree. Working down the list in order at thirteen minutes each runs out of time precisely on the conflicts.
5. **Name the sensitivity points and give each a date for its record**: A sensitivity point is rated high on both importance and difficulty: one design decision changes the outcome. Stop at the ratified list and in week three somebody re-opens the model tier with no record of why it was settled.
6. **Write a record only where there was a trade-off**: An ADR is earned by a decision that could reasonably have gone the other way. A record for every decision is the same as none, because the three that matter are unfindable.
7. **Run build, buy or borrow as a matrix, a three-year cost, a door and a flip test**: Weights come from the ratified NFRs, so you are not inventing them. Count the people and not just the licence, and assess whether the decision is a one-way door before you let the score decide.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Merge the stakeholder trees, compute every priority and produce the conflict list with the gaps. Tedious arithmetic across six people and nine candidates, done in seconds.<br>⚠ Check the formula. It inverts 4 − complexity about as often as it gets it right, and an inverted priority column reverses the entire workshop agenda. |
| **Claude Code** | Build the decision matrix as a sheet with the weights and ratings in named cells, so the flip test is one keystroke rather than a paragraph of reasoning. |
| **Chat LLM** | Draft the record from your bullet points, with the rejected options as a required section and the review date as a named trigger.<br>⚠ Its rejected-options section flatters the decision you already made. Require each rejection to cite the score, the three-year cost or the door, and send it back when a rejection reads as a reason rather than a number. |
| **Do not delegate** | Choosing which decisions earn a record. That judgement is what keeps the folder readable, and a readable folder is the only kind a coding agent or a new joiner benefits from. |

**The artefact**

| | |
| --- | --- |
| Produces | **Ratified NFR sheet + the ADRs at the sensitivity points** |
| Good looks like | Every ratified line carries a number, every sensitivity point carries a dated record, and every record names what it rejected together with the score that rejected it. |
| Owner | Solution architect |

<details><summary><b>Template · Ratification and the decision record</b></summary>

```markdown
# Ratification · <product> · <date>
_Workshop: <n> people, <n> candidates, two hours · Chair: <name>_

## Merged utility tree
> priority = value x (4 - complexity), each stakeholder scoring 1 to 3

| NFR | <frontline> | <compliance> | <finance> | <ops> | Gap | Conflict? |
|-----|------------|--------------|-----------|-------|-----|-----------|
| <latency 30s P95> | <6> | <2> | <2> | <4> | <4> | no |
| <cost per case $0.60> | <1> | <2> | <9> | <3> | <8> | **yes. ADR-<n>** |
| <accuracy 80% codeshare> | <9> | <6> | <2> | <6> | <7> | **yes. ADR-<n>** |
| <refunds over $400 approved> | <2> | <9> | <4> | <3> | <7> | **yes. ADR-<n>** |

**Rule:** a gap of 5 or more between any two stakeholders is a conflict, and every
conflict is a decision-record trigger.

**Not a real conflict, though it looks like one:** <auditability against latency, 
logging costs milliseconds, the model choice costs seconds>. The trees show this,
which is why you build them instead of debating them.

## The agenda the trees produce
- 0:00-0:20  ratify the <n> uncontested NFRs as one block
- 0:20-2:00  the <n> conflicts, one at a time

## Ratified
| # | NFR | Value | Sensitivity point? | Record owed |
|---|-----|-------|--------------------|-------------|
| NFR-1 | <latency> | <30s at P95, peak hour> | no | — |
| NFR-2 | <cost per case> | <$0.60, alert at 3x> | **yes** | ADR-<n>, <date> |
| NFR-3 | <accuracy> | <80% on codeshare> | **yes** | ADR-<n>, <date> |
| NFR-4 | <authority> | <refunds over $400 need a named approver> | **yes** | ADR-<n>, <date> |

## ADR-<n> · <the decision>
**Status** <accepted> · <date> · supersedes <none>
**Context** <the conflict in one sentence, with the two priorities that produced it>

**Options, weighted from the ratified NFRs**: score = sum(weight x rating), rated 1-3
| Criterion | Weight | <build> | <buy> | <borrow> |
|-----------|--------|---------|-------|----------|
| <portability> | 3 | <2> | <1> | <3> |
| <team skills> | 3 | <1> | <2> | <3> |
| <security> | 3 | <3> | <3> | <2> |
| <cost> | 2 | <1> | <2> | <3> |
| <velocity> | 2 | <1> | <3> | <3> |
| <vendor support> | 1 | <1> | <3> | <2> |
| **total** | | **<n>** | **<n>** | **<n>** |

**Three-year cost, people counted** <buy: $<n> licence + $<n> people = **$<n>**> ·
<borrow: $<n> + $<n> = **$<n>**> · the licence is the small number once people count
**The door** <borrow behind an interface layer: two-way, two weeks now> · <buy:
one-way-ish, and the exit cost grows every month>
**Decision** <what was chosen> · named review at <month 12>
**Consequence** <what it costs now, and what it keeps open>
**Rejected** <one line per option, each carrying the number that rejected it>
**Flip test** <which single weight would have to move, and by how much, to change the winner>
```

</details>

<details><summary><b>Prompt · Merge the utility trees and find the conflicts</b>, You have every stakeholder's scores and the workshop is tomorrow</summary>

```text
Merge these stakeholder utility trees and find the conflicts.

Each stakeholder scored each candidate NFR on business VALUE (1-3) and COMPLEXITY (1-3).

  priority = value x (4 - complexity)

OUTPUT SHAPE:
1. One table: a row per NFR, a column per stakeholder holding their priority, then a
   GAP column holding the largest difference between any two stakeholders.
2. SHOW THE ARITHMETIC for at least three rows, so I can check you have not inverted
   the formula.
3. CONFLICTS: every NFR whose gap is 5 or more. Each one owes a decision record.
4. FALSE CONFLICTS: pairs that look opposed and are not, with the reason. The usual
   example is auditability against latency, logging costs milliseconds and the model
   choice costs seconds.
5. A proposed agenda: the uncontested NFRs first as one time-boxed block, then the
   conflicts one at a time.

RULES:
- Do not average the stakeholders. The gap is the signal and an average destroys it.
- Do not reword anyone's NFR.
- If a stakeholder did not score an NFR, leave the cell blank. Never impute a score.

SCORES:
<paste>
```

</details>

<details><summary><b>Prompt · Score build, buy or borrow, and run the flip test</b>, A framework or platform decision is on the table</summary>

```text
Score this decision as a weighted matrix, then test how firm the answer is.

CRITERIA AND WEIGHTS: these come from my ratified NFRs. Do not change them:
<paste: criterion, weight 1-3>

OPTIONS: <build / buy / borrow, or the named options>

OUTPUT SHAPE:
1. The matrix: each option rated 1-3 per criterion with one line of reasoning per cell.
   score = sum(weight x rating). Show the totals.
2. A three-year cost table with three columns: licence, people, total. Count the people.
3. THE DOOR, per option: two-way (reversible cheaply) or one-way, and what the exit
   costs. Say whether an interface layer converts a one-way door into a two-way one,
   and what that layer costs to build.
4. THE FLIP TEST: which single weight or rating would have to move, and by how much,
   before the winner changes. One sentence.

RULES:
- If the spread between first and last is small, say so plainly. A close matrix means
  the criteria do not separate the options, and the tie is then broken by the door.
- Never let cost outrank the weights I gave you.
- Where you do not know a number, write UNKNOWN and name who would have it.
```

</details>

<details><summary><b>Prompt · Draft the ADR, with the rejections argued from the numbers</b>, The decision is made and the record is what makes it stay made</summary>

```text
Draft an architecture decision record from my notes below.

OUTPUT SHAPE: exactly these sections, in this order:
  Status (accepted or superseded, with the date and what it supersedes)
  Context (the trade-off that forced a decision, in three sentences)
  Decision (what we are doing, and the named review point)
  Consequence (what it costs now, and what it keeps open)
  Rejected (one entry per option, each carrying the NUMBER that rejected it)
  Flip test (which single input would have to move, and by how much)

RULES:
- The Rejected section is the part that matters and the part that gets written badly.
  Every rejection cites the matrix score, the three-year cost or the door. A rejection
  that reads as a preference is a failure, rewrite it, or tell me the number is missing.
- Do not flatter the decision. If an option scored within a point of the winner, that
  belongs in Context, not in Rejected.
- Keep it to one screen. A coding agent reads this in its context pack, which is exactly
  why it must be short and exact.
- The review point is a date or a named trigger, never "later".

MY NOTES:
<paste>
```

</details>

**Worked example · SkyWays · nine ratified, three records owed**

> The nine candidates went into a two-hour workshop with the trees already merged. Six were uncontested and were ratified in twenty minutes; the remaining hundred minutes went to the three conflicts, which were the only reason six people had been put in one room. **Nine ratified NFRs with three sensitivity points**, each given a date for its record rather than a promise. The conflict that turned up is the one that usually turns up, latency against cost per case, because the faster answer needs the larger model. **ADR-004** was the framework decision and it repays a second read: the weighted totals came out four points apart across three options, and buy and borrow tied at $360,000 over three years once the people were counted, which made the licence the small number all along. The matrix did not break the tie. The **door** did: borrow, behind an interface layer, with a named review at month twelve, two weeks of work now to keep a swap at weeks rather than quarters.

**Pitfalls**

- A vote with sticky dots on a wall. The loudest group wins, cost per case collects two dots, and it comes back three months later as a crisis with an invoice attached to it.
- A record for every decision. Forty in a week and the three that mattered cannot be found; an ADR is earned by a trade-off, not by a meeting having happened.
- A record with no rejected options. It reads as a preference, and the first incident re-litigates it from the beginning because there is nothing on paper to defend.

**Done when**, Every ratified NFR carries a number, every sensitivity point carries a dated record, and every record names what it rejected with the score that rejected it.

---

## 6 · Bound

### Set the authority budget before the token budget

*P1, before a single tool is written*

The first question is not how much the agent may spend. It is **what it may change, touch or commit.** A cheap task with too much authority is far more dangerous than an expensive one with none. The product manager decides where the allowed-alone line sits; your job is to make it enforceable, which means the cap lives in a tool signature and not in prompt text. **A prompt is a request. A tool contract is a boundary.** A model can be talked past a request; a typed parameter that raises cannot be talked past, whatever the model has been convinced of.

**What you actually do**

1. **List every tool the agent can call, before anyone sizes its tokens**: Authority comes first because it is the thing a budget cannot fix. An agent with a small token allowance and a refund tool is the dangerous configuration.
2. **Band each tool R1 to R5 by what the action could damage**: Reversible draft, reversible change to real work, hard to reverse with a small blast radius, money or identity or policy, irreversible. The band belongs to the tool and is assigned once, so it is never argued per pull request.
3. **Move every cap into the tool signature and delete it from the prompt**: An injected instruction can override a sentence. It cannot override a typed parameter that raises. This is a morning's work and it is the highest-value morning in P1.
4. **Keep the sentence that explains the rule**: The prompt carries the policy and makes the agent behave well by default; the signature carries the enforcement and makes bad behaviour impossible. You want both, and confusing them is how a design lists five controls and enforces none.
5. **Mint the confirmation token outside the model's reach**: A token the model can produce is not a gate. Bind it to the booking, the amount and the approver, give it an expiry, and write the test that a forged or reused one raises.
6. **Tag every ingested text source untrusted, including partner APIs**: The partner is not attacking you; whoever can write into their free-text field might be. Trust is a property of the channel you control, not of the organisation at the other end of it.
7. **Classify every open decision hard or soft, then give the soft ones a placeholder**: Four questions and one *no* makes it hard. A soft gate with no stub or interface layer behind it is a hard gate nobody has admitted to, and the build queues anyway.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Band a tool list R1 to R5 with a reason per row and the control location named. A good first pass, and it is consistent in a way a room full of people is not.<br>⚠ It bands by the size of the change. A one-line change to a refund cap is R4, re-read every R1 and R2 that touches money, identity or a policy commitment. |
| **Claude Code** | Grep every prompt and tool description for currency symbols, *never*, *always*, *ask before* and *do not*, then have it write the enforced version and both tests for each hit that would cost money or be irreversible.<br>⚠ A hit list is not a fix. Require the over-cap test and the no-confirmation test in the same pass, or the work stops at the list and the list gets stale. |
| **Chat LLM** | Run the four hard-or-soft questions over your open decisions and propose a placeholder for each soft one, a stub, an interface layer, a default tier behind a gateway.<br>⚠ It marks almost everything soft, because everything looks reversible on paper. Question one is the one it answers too generously. |
| **Do not delegate** | Whether a wrong action can be undone, and how fast. That is a fact about your ledger, your regulator and your customers, and *we would notice* is not an answer to it. |

**The artefact**

| | |
| --- | --- |
| Produces | **Authority budget + gate map** |
| Good looks like | Every tool banded, every cap in a signature with a test beside it, every money action with a named approver, and every open decision classified with a real placeholder behind the soft ones. |
| Owner | Solution architect |

<details><summary><b>Template · Authority budget and gate map</b></summary>

```markdown
# Authority budget and gate map · <feature>
_Owner: <name> · <date> · The allowed-alone line comes from the PM's autonomy record_

## Authority, before any token budget
| Tool | Band | What ONE wrong call damages | Where the control lives | The test |
|------|------|----------------------------|------------------------|----------|
| <search_flights> | R1 | nothing; read-only | permission scope: read only | <no write scope granted> |
| <draft_message> | R2 | a reply a person then sends | review before it merges | <a draft can never auto-send> |
| <cancel_hold> | R3 | a held seat | approve first | <no approval, raises> |
| <rebook> | **R4** | a real booking and a fare | confirmation token | <no token, raises> |
| <issue_refund> | **R4** | money | amount at or below <cap>, typed in the signature, + a named approver | <over-cap raises; no-confirm raises> |
| <change_passenger_identity> | **R5** | identity | not delegated; no tool exists | <no such tool in the schema> |

**The ladder is about the action, not the diff.** A one-line change to <cap> is R4.

## Caps moved out of prompts
| Was, in the prompt | Now, in the signature | Tests written |
|--------------------|----------------------|---------------|
| <"never refund more than $400"> | <issue_refund(amount: Money, ...)>, raising above <CAP> | <test_over_cap_raises> |
| <"ask before rebooking"> | <rebook(..., confirmation: ConfirmToken)> | <test_no_confirmation_raises> |

The explanatory sentence **stays** in the prompt. It is policy and it makes the agent
behave well by default. The signature is what makes bad behaviour impossible once the
prompt has been talked past.

## The confirmation token
- Minted by: <the approver's screen>. Never by the model, never by a tool the model calls.
- Bound to: <booking id + amount + approver identity>
- Expires: <n> minutes
- Test: <a forged, reused or expired token raises>

## Ingest: everything the agent reads is untrusted
| Source | Tagged untrusted? | In the weekly injection suite? |
|--------|-------------------|-------------------------------|
| <passenger message> | yes | yes |
| <partner API free-text fields> | <yes> | <yes> |
| <uploaded documents> | <yes> | <yes> |
| <retrieved knowledge chunks> | <yes> | <yes> |

## Open decisions: hard or soft
Four questions, in order. **One "no" makes it hard.**
1. Can it be reversed cheaply once the build has started?
2. Can the build proceed behind a placeholder?
3. Is there a named owner and a date?
4. Does everything downstream survive if the answer changes?

| Decision | Q1 | Q2 | Q3 | Q4 | Verdict | Placeholder | Owner | By |
|----------|----|----|----|----|---------|-------------|-------|----|
| <autonomy level on refunds> | no | — | — | — | **HARD** | — | <name> | <phase> |
| <model tier per slice> | yes | yes | yes | yes | soft | <mid tier behind the gateway> | <name> | <date> |
| <framework> | yes | yes | yes | yes | soft | <an interface layer in front of it> | <name> | <date> |
| <retrieval design> | yes | yes | yes | yes | soft | <a stub returning the fare-rules file> | <name> | <date> |
```

</details>

<details><summary><b>Prompt · Band a tool list by risk of action</b>, You have the tool surface and no bands yet</summary>

```text
Band every tool below on the R1-R5 ladder.

R1  reversible draft or sandbox, review at the end
R2  reversible change to real work, review before merge
R3  hard to reverse, small blast radius (approve first
R4  money, identity or a policy commitment) a NAMED approver, every time
R5  irreversible or safety-critical, not delegated at all

OUTPUT SHAPE, one table:
| Tool | Band | What ONE wrong call could damage | Where the control must live | The test that proves it |

RULES:
- Band by what the ACTION could damage, never by the size of the change. A one-line
  change to a refund cap is R4.
- The control column may not say "the prompt". It says: a typed parameter, a required
  confirmation token, a permission scope, or "no tool exists".
- Every R4 row names the approver role.
- Every R5 row says that no tool exists, not that the tool is discouraged.
- Flag any tool carrying a generic action parameter. One broad manage_<thing>(action)
  tool is accidental authority and must be split, because any path through it could
  cancel something.

TOOLS:
<paste the signatures, or the list with one line of description each>
```

</details>

<details><summary><b>Prompt · Move the caps out of the prompts, with the tests</b>, Monday morning, on any repository with an agent in it</summary>

```text
Search every prompt, system message and tool description in this repository for rules
that are currently only requests.

Search for at least: every currency symbol and amount, "never", "always", "do not",
"ask before", "make sure", "you must not", "only if", "limit", "maximum", "cap",
"approval", "confirm".

OUTPUT SHAPE, one table:
| File | Line | The sentence | Would ignoring it cost money, expose data or be irreversible? | The enforced version | The two tests |

RULES:
- The fourth column is the triage. Rules that fail it are fine as policy and should
  stay exactly where they are; say so rather than proposing work.
- The enforced version is a typed parameter that raises, a required confirmation token,
  or a narrowed permission. Never a better sentence.
- For every row that needs enforcing, WRITE the two tests: the over-limit case and the
  missing-confirmation case. Both assert that the call RAISES, never that the reply
  contains an apology, because wording changes with the next prompt edit.
- Do not remove the explanatory sentence from the prompt. Say which sentences to keep.
- Show me the search commands before the results.
```

</details>

<details><summary><b>Prompt · Classify the open decisions hard or soft</b>, The build is queuing behind a list of open questions</summary>

```text
Classify each open decision below. Ask the four questions IN ORDER and stop at the
first "no". One "no" makes it hard.

1. Can it be reversed cheaply once the build has started?
2. Can the build proceed behind a placeholder?
3. Is there a named owner and a date?
4. Does everything downstream survive if the answer changes?

OUTPUT SHAPE, one table:
| Decision | Q1 | Q2 | Q3 | Q4 | HARD or SOFT | The placeholder | What settles it, and when |

RULES:
- Be strict on Q1. "We would only have to change some code" is a NO once that decision
  has reached everywhere the code goes.
- Every SOFT row must carry a real placeholder: a stub, an interface layer, a default
  tier behind a gateway. A soft gate with no placeholder is a hard gate nobody has
  admitted to, and the build queues regardless of the label.
- Every HARD row names the phase it must close in.
- Do not mark a decision soft because it feels small. Size is not the test.

DECISIONS:
<paste>
```

</details>

**Worked example · SkyWays · the cap that existed everywhere except the code**

> The engineer had wired the assistant to do everything, to show how capable it was. The authority budget put search and drafting at R1 and R2, cancelling a hold at R3, rebooking and refunds at R4 with a named approver, and changing a passenger identity at R5 with no tool existing at all. The **$400** from the day-six constraint register became a typed parameter on the refund signature, with two tests beside it. That is what the artefact said. On **day 82** a passenger received a **$2,000 refund** that was not owed, and the postmortem reconstructed the state exactly: with either the cap or the approver enforced the refund is impossible, so both were absent from the code. Five layers had been listed in the design and none was enforced. Two of them were written down, in the prompt, which is precisely why *we had a cap* felt true and was not.

**Pitfalls**

- Sizing the check to the diff. A one-line change to a refund cap is the highest band there is, and *small changes do not need a gate* is the sentence that precedes most money incidents.
- A cap that lives in prompt text. It lowers a probability and closes no path, and it reads exactly like a control in a design review, which is the whole reason it is dangerous.
- Treating every open decision as hard. The build queues behind eleven questions that could each have run behind a stub, and the delay gets blamed on governance rather than on the classification.

**Done when**, A grep of every prompt returns no cap, no currency amount and no 'ask before', and each rule you removed has an over-cap or no-confirmation test standing in its place.

---

## 7 · Detail

### Layer the context, wrap the system, place the checker

*P1 into P2, as the design becomes something an engineer can build*

Three details decide whether the design works, and none of them is visible in a diagram. **Context** is the largest single driver of both quality and cost, and it wants to be layered and inherited rather than pasted. A legacy system wants **one well-defined door** instead of a custom wire per product, which is what turns M applications times N systems into M + N. And a chain of best-guess steps **multiplies** rather than averages: four steps at 90% each is 66%, and it fails fluently, so nobody notices until a passenger does.

**What you actually do**

1. **Draw the four context layers, each inherited by the one below**: Shared for org-wide standards, security and tone; domain for the business model; product for this application; task for this feature. A new product writes only the last two and onboards in a day instead of a week.
2. **Name what is genuinely domain-level**: This is the layer teams forget and it holds most of the real reuse, the booking model, the fare rules, the things every product in the area needs and each one currently re-invents in its own prompt.
3. **Make every override declare its reason and its scope**: A silent override is drift with a good explanation attached. Declared, it is a decision somebody can review; undeclared, it is the stale copy nobody can find.
4. **Send the slice a task needs, never the whole stack**: Forty thousand tokens of standards in every call is both the bill and the quality problem: a bigger context makes answers worse, not better, and it is the habit that hides behind *for context*.
5. **Wrap each system as one server with three primitives**: Tools are actions the model may invoke, resources are read-only data the application supplies, prompts are templates a person picks. Split reads from writes and require a confirmation on every write in the contract, not in the description.
6. **Multiply the chain, do not average it**: Four steps at 90% is 66%, end to end wrong one time in three. Length is the enemy, so the first defence is removing a step, every step you remove multiplies back.
7. **Place an independent checker after each costly, easy-to-miss generating step**: Independent means a different model, or the same model in a fresh context with an adversarial brief. A model reading its own output shares its own blind spots, which is exactly why *review your answer* does not work.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Paste a product's prompt dump and ask it to sort every line into shared, domain, product or task, with one line of reasoning each. It is fast and it makes the duplication obvious.<br>⚠ It puts almost everything in shared, because shared is where general-sounding sentences go. The domain layer is the one it will not find for you. |
| **Claude Code** | Have it generate the server schema from an existing API surface: resources for read-only data, tools split into open reads and gated writes, prompts for the templates a person picks.<br>⚠ It offers one broad manage_thing(action) tool because that is tidy. Any path through such a tool carries the authority of the worst action it can reach, reject it and make it enumerate. |
| **Chat LLM** | Write the checker's brief. It is an adversarial instruction (find what is wrong, list the violations, do not rewrite) and it is a different artefact from the brief that generated the answer.<br>⚠ Never run the checker in the context that produced the output, and prefer a different model. Self-review returns a confident yes and no finding. |
| **Do not delegate** | Deciding where the checkers go. Each one costs a call, and putting them everywhere is the same error as putting them nowhere; the judgement is which wrong answers are both expensive and easy to miss. |

**The artefact**

| | |
| --- | --- |
| Produces | **Layered context spec + server schema + checker placement** |
| Good looks like | One place to edit each rule, one server per system with reads open and writes gated in the contract, and a checker after each generating step whose errors are expensive and invisible. |
| Owner | Solution architect |

<details><summary><b>Template · Context layers, server schema and checker placement</b></summary>

```markdown
# Detail design · <feature>
_Owner: <name> · <date> · Read by: engineering and QA_

## 1 · Context layers, inherited downward
| Layer | Holds | Example files | Who edits |
|-------|-------|---------------|-----------|
| shared | org-wide standards, security, tone, glossary | <standards.md · security.md · tone.md> | <platform> |
| domain | the business model for this area | <booking-model.md · fare-rules.md> | <you> |
| product | this application's architecture and APIs | <architecture.md · apis.md> | <the product team> |
| task | this feature's spec, bar and file list | <spec.md · bar.md · files.md> | <the bolt's owner> |

**Rules**
- A new product writes ONLY product and task. It inherits the rest.
- A shared change is one commit, and every product picks it up.
- An override declares its reason and its scope. A silent override is a drift.
- Send the slice a task needs, never the whole stack: <40k> tokens becomes <2k>.
- The domain layer is the one teams forget, and it holds most of the reuse.

## 2 · The server for <system>
| Primitive | Controlled by | Entries |
|-----------|---------------|---------|
| resources, read-only data | the application | <booking_record · passenger_history · fare_rules> |
| tools, open reads | the model | <search_flights · check_availability> |
| tools, gated writes | the model, within the contract | <rebook (CONFIRM)> · <issue_refund (CONFIRM, amount at or below the cap)> |
| prompts, templates | the person | <draft_disruption_reply> |

- Transport: <Streamable HTTP in production, stdio for local development>
- Auth: <as the specification's authorization framework requires>
- Trace: every tool call logged (input, decision, output, model version
- **Rejected:** <one broad manage_booking(action) tool) any path through it could cancel>

M applications times N systems becomes M + N. Build the server once and any compliant
client plugs into it.

## 3 · The chain, and where the checkers go
> <0.9> x <0.9> x <0.9> x <0.9> = **<0.66>**: multiply, never average

| # | Step | Kind | Checker? | Why |
|---|------|------|----------|-----|
| <1> | <read the booking> | best-guess | no | <low stakes, caught downstream> |
| <2> | <choose the flights> | best-guess | **yes** | <costly to get wrong, easy to miss> |
| <3> | <compute the fare> | exact | no | <a unit test, not a checker> |
| <4> | <draft the message> | best-guess | **yes** | <false claims and tone, invisible to the drafter> |
| <5> | <rebook> | consequential | no | <a confirmation, not a checker> |

**Independence**: each checker runs on <a different model> OR <the same model in a
fresh context with an adversarial brief>. Never a self-review, and never inside the
context that produced the output.

**Checker brief, step <n>:** <Find what is wrong with this. Do these options satisfy
every stated constraint? List the violations. Do not rewrite.>

**Re-draft cap:** <2> rounds, then escalate to a person.
```

</details>

<details><summary><b>Prompt · Sort a prompt dump into context layers</b>, Every product pastes the same forty pages and one copy has gone stale</summary>

```text
Below is everything currently pasted into the prompts of <product>.

Sort every line into exactly one of four layers and say why.

  SHARED   org-wide standards, security, tone of voice, glossary
  DOMAIN   the business model for this area: entities, rules that hold across products
  PRODUCT  this application's architecture, APIs and conventions
  TASK     this feature's spec, its bar and its file list

OUTPUT SHAPE:
1. A table: | Line (truncated) | Layer | Why | Duplicated in how many products? |
2. A DOMAIN section listed separately and in full. This is the layer teams forget and
   I want to read it on its own.
3. A list of lines that contradict each other, with both versions and the products they
   came from. These are the stale copies.
4. For each layer, the token count, so I can see what a task actually needs to be sent.

RULES:
- Resist putting things in SHARED. A line belongs in shared only if a product in a
  DIFFERENT business area would also need it. Apply that test explicitly per line.
- A line that names this feature is TASK, however general it sounds.
- Do not rewrite any line. Sorting is the job.

PROMPT DUMP:
<paste>
```

</details>

<details><summary><b>Prompt · Draft the server schema, reads open and writes gated</b>, Before anyone writes a third custom integration to the same system</summary>

```text
Design a single server exposing <system> to any compliant AI client.

Expose exactly three kinds of thing:
  RESOURCES  read-only data the application supplies
  TOOLS      actions the model may invoke
  PROMPTS    templates a person picks

OUTPUT SHAPE:
1. resources: name, what it returns, who controls it.
2. tools, in TWO separate lists: OPEN READS and GATED WRITES. Every gated write carries
   a required confirmation parameter in its signature and its risk band.
3. prompts: name and when a person would pick it.
4. A REJECTED section: designs you considered and discarded, with the reason.
5. The trace row each tool call writes.

RULES:
- Never propose one broad tool with an action parameter. Any path through such a tool
  carries the authority of the most dangerous action it can reach. Enumerate instead.
- A read tool must have no side effects, and you must say how that is enforced rather
  than asserted.
- Every write tool's confirmation is a typed parameter, not an instruction in the
  description. A description is a request.
- Where the underlying system exposes something that should not be reachable at all,
  say so and leave it out. Not every capability becomes a tool.

SYSTEM: <the API surface, or a link to it>
```

</details>

<details><summary><b>Prompt · Compute the chain and place the checkers</b>, Engineering says ninety percent is solid</summary>

```text
Here are the steps of <feature>, with each best-guess step's measured or estimated
accuracy: <paste>.

1. Compute the end-to-end success rate by MULTIPLYING the best-guess steps. Show the
   multiplication. Do not average anything.
2. Tell me what that rate means in plain words: wrong roughly one time in how many.
3. Option one, SHORTEN: which steps could be removed or merged, and what the rate
   becomes. Look especially for exact work that has crept into a prompt, and for two
   calls doing what one could do.
4. Option two, CHECK: which steps get an independent checker. Place them only where a
   wrong answer is COSTLY and EASY TO MISS. Give the rate after checkers, and state
   the assumption you used about what a checker recovers.
5. For each checker: the model or context that makes it independent, and its brief,
   written as an adversarial instruction.
6. The re-draft cap, and what happens when it is hit.

RULES:
- Exact steps do not get a checker. They get a unit test. Say so rather than skipping
  them silently.
- Consequential steps do not get a checker. They get a required confirmation.
- Do not propose raising the model tier on every step. That is the expensive answer to
  a structural problem, and say so if someone has suggested it.
```

</details>

**Worked example · SkyWays · 66%, and the layer nobody had written**

> Two findings came out of the same afternoon. The chain had three best-guess steps in it, and multiplied rather than averaged it came out well below what the bar sheet implied, failing fluently, which is why nobody had noticed. Two checkers went in, after choosing the flights and after drafting the message, each on a different model with an adversarial brief and a re-draft cap of two rounds. The second finding was quieter. Every product was pasting forty pages of standards into every call; a security rule had changed the month before and two products still carried the old one with nobody able to say which. Four layers fixed it, and the layer that was missing entirely was **domain**: the booking model and the fare rules that every product in the area needed and each had re-invented. The same afternoon put the fifteen-year-old reservation system behind one server: resources for the read-only data, search open, rebook and refund gated in the contract, and a single broad manage_booking tool rejected because any path through it could cancel a booking.

**Pitfalls**

- Everything in the shared layer. It is where general-sounding sentences go, and the result is a shared file every product has to read around and a domain layer that never gets written at all.
- One broad tool with an action parameter. It looks tidy in the schema, and it means every path through it carries the authority of the most dangerous action it can reach.
- A checker reading its own output in its own context. It shares the blind spots that produced the error, so it returns a confident yes and the chain keeps its 66%.

**Done when**, Every rule has exactly one place it can be edited, every write tool requires a confirmation the model cannot mint, and the chain accuracy is a multiplication with a checker after each step whose errors are expensive and invisible.

---

> **P3 · Run & Learn begins here**, *is it still doing what we launched, and what did it cost?*

> ⛔ **The hard gate. P1 to P2.** Everything past this point depends on the spec, the acceptance bar per slice and the authority budget being signed. It is the one crossing nothing downstream survives without. [why](The-Agentic-PDLC).

## 8 · Evolve

### Make the running system cheap, auditable and able to redesign itself

*P2 into P3, and then for as long as the system runs*

Three things decide whether an architecture survives contact with production. The **bill**, which is a design question and not a finance one: caching pays only if the layout lets it hit, and routing pays only if a breaker stops the runaway. The **trace**, which has to be replayable by audit without becoming a breach target, which means redact rather than omit. And the **incident**, which is where your next design decision comes from, a postmortem that produces a name has not finished; one that produces an enforced control has.

**What you actually do**

1. **Lay the prompt out for the cache, with the marker on the last stable block**: The cache matches an exact prefix in the order tools, system, messages. Put the passenger's request first *for emphasis* and no two calls share a prefix, so caching is switched on and never hits.
2. **Count the reuse before turning caching on**: cost with cache = ( w + 0.1 × (N − 1) ) × T × p against N × T × p without. The documented multipliers, read September 2026: a five-minute write is 1.25× input, a one-hour write 2×, a read 0.1×, and Fable and Mythos 5.1 read at 0.025×. Break-even is the **second** use; at one use it costs more.
3. **Choose the window from the traffic pattern, not from the cheaper write**: Five minutes everywhere is the trap. On traffic arriving every twelve minutes the five-minute cache has always expired, so every call pays a write, and the cheaper write paid on every call costs more than the dearer write paid once.
4. **Route by complexity and put a breaker on every loop**: A delay lookup should not cost what a multi-leg international rebooking costs. MAX_LOOPS = 5, then a hard stop and a hand-off, because no legitimate case needs fifty and a runaway burns until somebody notices.
5. **Redact the trace, and mark the cache hits in it**: Masking keeps the decision replayable and the identifier out of the store; omitting the field breaks the audit. Then exclude cache hits from the latency alert, or a fast response gets reported as a suspected failure.
6. **Rewrite every incident as the missing-control question**: Which control, if present, would have made this impossible? Reconstruct the state from that question rather than from the timeline, and the answer is an ADR and a tool signature rather than a ticket and a name.
7. **Migrate legacy piece by piece, with a rule sheet where the docs are missing**: Score each module on risk, documentation, coupling, reversibility and how much it teaches; wrap it behind a clean interface, route a slice, grow the new, retire the old. Payments last, and never the whole codebase in one context.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Reorder one live prompt for the cache and add the assertion that proves it, cache tokens read above zero on the second call. Then have it pull the four ratios from the per-call log: tokens per call, tier mix, cache hit ratio, retries per conversation.<br>⚠ Make it check for anything volatile inside the cached block. One timestamp or request id misses the prefix on every call, and the config file will still say caching is on. |
| **Chat LLM** | Compute the break-even and the saving for your reuse count and window, and tell you which window the traffic pattern actually argues for.<br>⚠ Paste the vendor's current pricing page into the prompt rather than trusting its memory of the multipliers. A stale multiplier turns the arithmetic into a decision you cannot defend in front of finance. |
| **Claude Code** | Extract a rule sheet from a legacy module (rule id, condition, action, source line, confidence) so the agent reads a few hundred tokens of intent instead of four thousand lines that bury it.<br>⚠ Everything below 0.9 confidence goes to a person first. Those rows are where the code is doing something the comments deny, which is the part worth reading yourself. |
| **Do not delegate** | The missing-control finding. Naming the control that would have made an incident impossible is the one judgement in the postmortem, and a model will happily propose a better prompt, which is a request rather than a control. |

**The artefact**

| | |
| --- | --- |
| Produces | **Caching and routing config · redacted trace spec · the incident ADR** |
| Good looks like | One configuration file for caching and routing, reviewed like code; a trace row that is replayable and holds no raw identifier; and an incident record whose finding is an enforced control rather than a person. |
| Owner | Solution architect |

<details><summary><b>Template · Run-time architecture and the incident record</b></summary>

```markdown
# Run-time architecture · <feature>
_Owner: <name> · <date> · Config reviewed like code: <path>_

## Caching layout
[tools] [system] [shared context] [domain context <- cache marker] [task] [the request]
  stable ---------------------------------------------------------> | volatile

- The cache matches an EXACT prefix, in the order tools -> system -> messages, up to
  the marked block. The changing request goes last, always.
- Documented multipliers, read September 2026: five-minute write 1.25x input ·
  one-hour write 2x · read 0.1x · <Fable and Mythos 5.1 read at 0.025x>
- cost with cache = ( w + 0.1 x (N - 1) ) x T x p, against N x T x p without.
  **Break-even is the second use.** At N = 1 it costs more than not caching.
- Window: <five minutes> because <calls arrive seconds apart and each hit refreshes it
  free>. Choose one hour when <a call every twelve minutes means the short cache has
  always expired and every call pays a write>.
- Minimum cacheable block: <about 1,024 tokens, model dependent>

| What breaks the cache | Present here? |
|-----------------------|---------------|
| The request placed first, for emphasis | <no> |
| A timestamp, request id or session id inside the cached block | <no> |
| A model switch mid-task, the cache is model-scoped | <forbidden in the team rules> |
| Fewer than the minimum cacheable tokens | <no> |

## Routing and the breaker
| Complexity score | Tier | Example |
|------------------|------|---------|
| below <0.3> | <cheap> | <is my flight delayed?> |
| <0.3> to <0.7> | <mid> | <am I owed a hotel under the regulation?> |
| above <0.7> | <frontier> | <missed connection, lost bag, wedding tomorrow> |

- MAX_LOOPS = <5> on every loop, then a hard stop and a hand-off to a person.
- A per-transaction token cap, next to the breaker.
- Alert on cost per case at **3x** the ratified figure, from the daily per-call log.

## The trace row
ts · input (passport ****1234, card ****9902) · tools called · decision ·
model version · approver · cost · cache tokens read

- **Redact, do not omit.** Masking keeps the decision replayable and the identifier out
  of the store. Omitting the field breaks the audit instead.
- Retention: <90 days hot, then aggregate>. Traces are production data; guard them like
  production.
- Mark cache hits and EXCLUDE them from the latency alert, or a fast response is
  reported as a suspected failure and someone proposes switching the cache off.
- Test: <a passport number never reaches a row>.

## Incident to design change · <date>
**Reconstruct** <with the cap enforced: impossible. With the approver enforced:
impossible. Therefore both were absent. That is the state the system was in.>
**Finding** the enforced control that was missing: <name it>
**Not the finding** <the input, the person who typed it, or any control that would only
have detected it afterwards>
**Change** <the typed parameter, the gate or the permission, and the file it lives in>
**Record** <ADR-<n>> · autonomy on <action> drops one level, raised again only on evidence
**Verify** <QA re-runs the attack; it must now be stopped twice over>
```

</details>

<details><summary><b>Prompt · Diagnose a bill that left its estimate</b>, The invoice has moved and traffic has not</summary>

```text
My token bill is <n>x its estimate and traffic is flat. Diagnose it from the
per-call log at <path>, not from the price list, the prices did not change.

Compute four ratios, the baseline period against now:
- tokens per call
- share of calls on the frontier tier
- cache hit ratio
- retries per conversation

OUTPUT SHAPE:
1. A table: | Signature | Baseline | Now | Factor |
2. The PRODUCT of the four factors, with the arithmetic shown. If the product is close
   to the ratio between the two invoices, say so and stop looking.
3. If the product is well below the invoice ratio, name what structural change is not
   explained by habit: traffic, a new feature, or a price change I should go and check.
4. A fix order, computed as priority = (factor - 1) / days to fix. Show the arithmetic.

RULES:
- Do NOT rank by the largest change in a ratio. Retries often rise the most in relative
  terms and contribute the smallest factor on the bill.
- For each fix, name where the control lives afterwards: a config file reviewed like
  code, a breaker constant, a rule about prompt ordering.
- Each of these was a sensible decision made by a careful person. "Remind the team to
  be careful with tokens" is not a fix; say what makes the habit visible on the day.
```

</details>

<details><summary><b>Prompt · Turn the incident into an enforced control</b>, After any incident, while the room is still discussing the input</summary>

```text
Turn this incident into a design change. Use EXACTLY this structure.

**Timeline** (what happened, minute by minute, from the input to the consequence
**Reconstruct**) for each control that was supposed to exist, state whether the
  incident is POSSIBLE or IMPOSSIBLE with it enforced. The combination that is possible
  is the state the system was actually in.
**Finding** (the ENFORCED control that, if present, would have made this IMPOSSIBLE
**Not the finding**) the input, the person, and any control that would only have
  DETECTED it
**Change** (the typed parameter, the confirmation token or the permission, and the
  file it will live in
**Record**) the record number, and the autonomy level that drops as a result
**Verify**: the test QA re-runs, and what "stopped twice over" means here

RULES:
- Do not name a person. Do not name the input that triggered it.
- "A better prompt" is NOT a control. A prompt is a request a model can be talked past.
  If your finding is a prompt change, you have not found the control yet.
- Classify every layer that was supposed to help as ENFORCED, A REQUEST, or ABSENT, and
  be honest about the ones that were written down only in the prompt.
- Separate detection from prevention and say which yours is. An alert tells you
  afterwards; a cap makes it impossible.

INCIDENT:
<paste the trace and the postmortem notes>
```

</details>

<details><summary><b>Prompt · Extract a rule sheet from a legacy module</b>, A team lead wants to feed the whole codebase to the agent</summary>

```text
Extract a rule sheet from this legacy module, so an agent can read the intent
instead of the code.

OUTPUT SHAPE, one table:
| rule_id | Condition | Action | Source (file:line) | Confidence 0-1 |

RULES:
- One row per business rule. A rule is a condition and an action, not a code path.
- Every row cites a file and a line. A rule with no source cannot be verified and must
  not be written down.
- Confidence is your honest reading of whether the code does what the row claims.
  Anything below 0.9 goes to a person before it goes anywhere near the agent; mark
  those rows clearly.
- Where a comment and the code disagree, follow the CODE and say so in the row. Low
  confidence usually means the code does something the comments deny.
- Do not modify any code and do not propose a refactor.

Then, separately:
- A migration score for this module out of 25: risk, documentation, coupling,
  reversibility, and how much it teaches. Say where it falls in the order, and confirm
  that anything touching payments is last.
- The clean interface this module should sit behind before the agent touches it.

MODULE: <path>
```

</details>

**Worked example · SkyWays · day 75 and day 82**

> Two numbers from the same fortnight, and two different kinds of design change. On **day 75 the bill was 4.4 times its estimate** with traffic flat, which meant behaviour had changed and behaviour is only visible per call. The four ratios explained it exactly: tokens per call 1.6, frontier share 1.5, cache hit ratio 1.3, retries 1.41, and 1.6 × 1.5 × 1.3 × 1.41 = 4.40. Four habits, each a sensible decision made by a careful person. It had started with an engineer reordering a prompt for clarity and moving the passenger's request to the front, which changed the prefix on every call and left caching switched on and never hitting. The fix order came from (factor − 1) ÷ days, which put the context trim first and the retry breaker last, the breaker being the right fix in the wrong position. Then **day 82** and the $2,000 refund, which produced the other kind of change: not a ticket and not a name, but an ADR, a typed parameter and an autonomy level dropped by one. The cost-per-case NFR had been ratified on day nine at $0.60 and then never measured, which is how four weeks passed before anybody looked. The record was amended to make it a monitored number with a named owner and an alert at three times.

**Pitfalls**

- Turning caching on without counting the reuse. Below two uses of the same prefix it costs more than it saves, and the configuration file will still report that caching is enabled.
- A latency alert that flags cache hits as suspected failures. It reports hundreds of them, somebody proposes switching the cache off, and the bill rises by about a third within a day because the anomaly was the cache working.
- A postmortem that ends in a name, or in a better prompt. Neither is a control, and the next incident of the same class is already scheduled.

**Done when**, The second call on a live prompt reports cache tokens read, a runaway loop stops at five, a passport number never reaches a trace row, and your last incident produced a typed parameter rather than a name.

---

## Read next

- [The wiki page for this role](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Solution-Architect)
- [The same case, step by step, in the simulator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/sa/step-1)
- [Every decision tree on one page](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Decision-Trees)

**Other roles:** [Product Manager](Journey-Product-Manager) · [Engineering Lead](Journey-Engineering-Lead) · [QA Lead](Journey-QA-Lead) · [DevOps](Journey-DevOps)

- [The manual, interactive](https://akash-coded.github.io/aws-bedrock-agentcore-strands/) · [every template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/) · [every prompt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/) · [frameworks and acronyms](https://akash-coded.github.io/aws-bedrock-agentcore-strands/frameworks/)

