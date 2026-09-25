# Product manager · the journey, end to end

<!-- tutorial:lesson -->*The short version is the lesson **[For product managers](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/agentic-pdlc-for-product-managers/)**, the whole role in one sitting. This page goes deeper.*<!-- /tutorial:lesson -->

**From a vibe to a number you can defend**

8 steps · 50 sub-steps · 8 templates · 21 prompts

This is the reading copy. The [interactive version](https://akash-coded.github.io/aws-bedrock-agentcore-strands/product-manager/) has a copy button on every template and prompt, which is what you want when you are actually doing the work.

This page is the walk. For the standing definition of the job, what you own, what you may settle alone, what crosses your desk and how the role fails, see [Role Product Manager](Role-Product-Manager).

---

Your job has not changed. **What** and **why** are still yours, and nobody else in the room can decide them. What changes is that the thing you write is now read by a machine that cannot ask you what you meant, and that part of your product is right *a share of the time* rather than always.

Those two facts ripple through every step below. A vibe becomes a measurement because the machine downstream cannot interpret a vibe. A success criterion becomes a number per slice because 'it works' is no longer a yes or a no. And a launch becomes a shadow run because you cannot reason your way to knowing whether it agrees with the humans it is replacing.

Eight steps. Each one ends in an artefact somebody else needs, with the template to write it and the prompts to draft it faster.

## The arc

Eight steps, and the four phases they sit in. Where the hard gate falls on your own arc is the thing worth noticing: it is a different place for every role.

<!-- picture:wikimap:journey-product-manager -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-product-manager.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-product-manager.dark.webp"><img alt="The product manager's eight steps placed on the four phases, with the artefact each one produces" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-product-manager.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-journey-product-manager.light.webp">Open the picture full size</a></sub>
<!-- /picture -->


| # | Phase | Step | What it produces |
| --- | --- | --- | --- |
| 1 | P0 | [**Discover**, Turn the vibe into a measurement](#1--discover) | Pain register |
| 2 | P0 | [**Qualify**, Decide whether this is AI at all](#2--qualify) | AI-fit decision record |
| 3 | P0 | [**Frame**, Size the value and set the autonomy](#3--frame) | Value line + autonomy decision record |
| 4 | P1 | [**Specify**, Write the spec a machine can build from](#4--specify) | Eight-field spec + acceptance bar sheet |
| 5 | P1 | [**Plan**, Plan in bolts, not sprints](#5--plan) | Bolt plan |
| 6 | P2 | [**Gate**, Hold the three gates that are yours](#6--gate) | Gate decision record |
| 7 | P3 | [**Launch**, Shadow, then five percent, then widen](#7--launch) | Cut-over decision |
| 8 | P3 | [**Learn**, Report two numbers and turn incidents into the next frame](#8--learn) | Two-number report · drift readout · next-P0 brief |

## What is yours, and what is not

| Yours to own | Not yours, stop signing these |
| --- | --- |
| The **intent** gate (is this worth doing at all? | **Behaviour** and **expansion** gates. Those are the QA lead's, and your name on them helps nobody |
| The **release** gate) is it safe to show real users? | Pull request approvals you cannot evaluate |
| The **plan** gate, shared with the architect | Model choice, temperature, framework (behaviours are yours, knobs are engineering's |
| The autonomy level per action, and the door it sits behind | The golden set's contents) you set the bar, QA curates the cases |
| The acceptance bar per slice, derived rather than guessed |  |
| The two-number report to whoever funds this |  |

## How to use a model in this role

> Use a model for the **drafting and the arithmetic**, never for the judgement. It can turn six interview transcripts into a deduplicated pain register in a minute, and it will happily invent a value line if you let it. The pattern that works: you bring the numbers and the decision, the model brings the structure and the first draft, and every artefact leaves your hands having been read by you. Where a step below says *do not delegate*, that is a judgement the model has no standing to make.

---

> **P0 · Frame begins here**, *is this worth doing, is it AI at all, and how much may the machine do?*

## 1 · Discover

### Turn the vibe into a measurement

*Week one, before anyone designs anything*

Requests arrive as vibes. *Make rebooking smarter.* You cannot size a vibe, prioritise it, or hand it to a machine. This step converts it into four facts (who has the pain, how often, what it costs today, and the evidence) and everything downstream refers back to that line. It is the old product discipline, now mandatory, because the machine downstream cannot ask you what you meant.

**What you actually do**

1. **Find who actually holds the pain**: Not the person who raised the request. The frontline agent, the contact-centre lead, the passenger. Ask each of them to describe the last time it happened, not the general case.
2. **Count it**: Cases per day or per week. If nobody knows, that is the first finding, and ops can usually produce it in an afternoon from a ticket export.
3. **Cost it**: Minutes per case × loaded cost per minute, plus anything that leaks, a lost passenger, a goodwill credit, an SLA breach. Cost per case is the number you will be asked for and the one nobody has.
4. **Find the evidence**: A ticket export, a call recording, a queue chart. One artefact a sceptic can open. An anecdote is not evidence; an anecdote with a number behind it is.
5. **Write the one-line statement**: Who · how often · what it costs · the evidence. One line. If it takes a paragraph, you have two pains and should split them.
6. **Refuse to open a spec until the line exists**: This is the discipline the step really is. Everything after this refers back to it, so a missing line becomes a missing justification at the funding conversation.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Paste six interview transcripts and ask for the distinct pains with the speaker beside each. It is very good at deduplicating what six people said in five different ways.<br>⚠ Ask it to keep the speaker's name on every line. Merged-without-attribution is how a stakeholder later says they were never heard. |
| **Claude Code** | Point it at a ticket export and have it produce the counts: cases per week, median handling time, the tail. It writes and runs the script, so you get the number and the method.<br>⚠ Read the script. A count over the wrong date column is confidently wrong. |
| **Spreadsheet + LLM** | Have it build the cost-per-case arithmetic as a sheet with the assumptions in named cells, so a sceptic can change one and watch the answer move. |
| **Do not delegate** | Deciding which pain is worth solving. The model will rank by how vividly it was described, which correlates with who is most articulate, not with what it costs. |

**The artefact**

| | |
| --- | --- |
| Produces | **Pain register** |
| Good looks like | One line per pain, each with a name, a frequency, a cost and a link to the evidence. Sorted by cost, not by who asked. Readable in thirty seconds. |
| Owner | Product manager |

<details><summary><b>Template · Pain register</b></summary>

```markdown
# Pain register · <product>
_Last updated: <date> · Owner: <name>_

| # | The pain, in one line | Who holds it | Frequency | Cost today | Evidence |
|---|----------------------|--------------|-----------|-----------|----------|
| 1 | <Who> cannot <do what>, so <consequence> | <role, named person> | <n/day> | <$n per case · $n/yr> | [<source>](<link>) |
| 2 | | | | | |

## How cost per case was computed
- Handling time: <n> min, from <source>
- Loaded cost per minute: $<n>, from <source>
- Leakage per failed case: $<n>: <what leaks, and how it was estimated>
- **Cost per case = $<n>**

## What is NOT in here
- <pains raised that were out of scope, and why, so nobody re-raises them>

## Open numbers
| Missing | Who can produce it | By when |
|---------|--------------------|---------|
| <e.g. leakage rate> | <ops lead> | <date> |
```

</details>

<details><summary><b>Prompt · Deduplicate discovery notes, with credit</b>, After the interviews, before you write the register</summary>

```text
You are helping a product manager consolidate discovery notes.

Below are <n> interview transcripts about <problem area>.

Produce a table with one row per DISTINCT pain:
| Pain, in one sentence | Everyone who raised it (names) | Their exact words (shortest quote) | Frequency mentioned | Cost mentioned |

Rules:
- Keep EVERY name. If four people said the same thing, all four names go on that row.
- Do not merge two pains that have different causes, even if they have the same symptom.
- If a frequency or cost was not mentioned, write "not stated", never estimate.
- At the end, list separately: things stated as solutions rather than pains.

TRANSCRIPTS:
<paste>
```

</details>

<details><summary><b>Prompt · Turn a vibe into a measured statement</b>, You have one request and no numbers</summary>

```text
A stakeholder asked for: "<the vibe, verbatim>"

Act as a sceptical product manager. Do NOT propose a solution.

1. Rewrite it as: WHO has the pain · HOW OFTEN · WHAT IT COSTS today · EVIDENCE.
2. For each of the four, mark it KNOWN or UNKNOWN based only on what I gave you.
3. For every UNKNOWN, write the single question I should ask, and who is most likely to
   have the answer.
4. Tell me which ONE unknown, if it came back badly, would kill this request. Ask that first.

Context I have: <paste what you know>
```

</details>

<details><summary><b>Prompt · Cost-per-case arithmetic from a ticket export</b>, You have data and need the number defensible</summary>

```text
I have a ticket export at <path>. Columns: <list them>.

Write and run a script that reports:
- tickets per week for the last 12 weeks, and the trend
- median and p90 handling time, for <category> only
- the share that were reopened or escalated
- cost per case = median handling minutes x $<rate>/min

Then print the assumptions you made as a list, and flag any column you had to
interpret. Show me the script before the numbers. I need to check the date column
and the category filter.
```

</details>

**Worked example · SkyWays · day one**

> The request was *make rebooking smarter*. After two days it read: **Disrupted passengers wait an average of 38 minutes for a rebooking decision; 240 cases a day; 11% are codeshare, which no simple rule can handle; measured cost $9.40 per case from the Q2 ticket export.** That single line survived to the steering committee on day 90, because every later artefact pointed back at it. The 38 minutes became the latency NFR, the 240 became the denominator of the value line, and the 11% became the slice that carried the whole risk.

**Pitfalls**

- Writing the pain as a missing feature. *We need an AI assistant* is a solution, and it forecloses the cheaper answer before anyone has looked.
- Accepting 'everyone knows it is slow'. If nobody will name a number, the honest register entry is the number as UNKNOWN with a named owner and a date, not a guess dressed up as a finding.
- Counting the saving and not the leak. The passenger who left is usually worth more than the minutes.

**Done when**, Someone who was not in any of the interviews can read one line and tell you what the problem is, how big it is, and where the number came from.

---

## 2 · Qualify

### Decide whether this is AI at all

*Immediately after the register, before any design*

Leadership says agent-first. Half of what you are asked to build is a rule, and a rule done by a model is slower, dearer and less correct than a rule done by code. Three questions settle it, in order, and the recorded answer is what lets you say no with evidence instead of as an opinion. Expect two or three of your top five to come back as rules. That is the healthy result.

**What you actually do**

1. **Ask: is there a genuine judgement call?**: Something where two competent humans could reasonably differ. If the criteria are published and unambiguous, it is a rule, and code does rules perfectly and provably.
2. **Ask: is the volume high enough?**: A probabilistic system carries fixed costs, evaluation, gates, a harness. Below some volume a person is simply cheaper, and saying so is a service to everyone.
3. **Ask: is a wrong answer recoverable?**: If not, a person stays in the loop. This is not a maturity level you grow out of; it is a property of the action.
4. **Classify into one of four builds**: Rule (code) · assisted (model drafts, person decides) · agentic with gates · fully agentic. Most real features are the middle two.
5. **Write the verdict with its comparison line**: Record what you rejected and why. That line is your argument the next time the directive arrives, and it saves you re-running the analysis from memory.
6. **Take it to the architect before design starts**: The verdict fixes the shape of the product. Changing it later means starting again, which is exactly why it is a hard gate.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Run the three questions against a backlog in bulk. Give it the three questions and ten items, and ask for a verdict plus the one sentence justifying each.<br>⚠ It will be generous. It wants things to be AI. Re-read every YES on question one and ask yourself whether the criteria are actually published somewhere. |
| **Chat LLM, adversarially** | Ask it to argue the opposite: 'make the strongest case that this is a rule, not a model'. The strongest case against is the cheapest review you will get. |
| **Do not delegate** | The recoverability answer. Whether a wrong action can be undone is a fact about your business, your regulator and your customers, and the model does not know any of them. |

**The artefact**

| | |
| --- | --- |
| Produces | **AI-fit decision record** |
| Good looks like | One row per candidate, three answers, a verdict, and the rejected alternative. Signed and dated. Short enough that leadership reads it. |
| Owner | Product manager |

<details><summary><b>Template · AI-fit decision record</b></summary>

```markdown
# AI-fit · <feature>
_Decided: <date> · Decided by: <name> · Status: accepted / superseded_

## The three questions
| # | Question | Answer | Why |
|---|----------|--------|-----|
| 1 | Is there a genuine judgement call? | yes / no | <two competent people could differ about ...> |
| 2 | Is the volume high enough to carry a probabilistic system? | yes / no | <n cases/day> |
| 3 | Is a wrong answer recoverable? | yes / no / partly | <what happens, and how fast it can be undone> |

## Verdict
**<Rule in code | Assisted, person decides | Agentic with gates | Fully agentic>**

## What we rejected, and why
- **Rule in code**, <rejected because ... / chosen because ...>
- **A person**, <cost at this volume>
- **Fully agentic**, <rejected because step <x> is unrecoverable>

## Consequence
- The unrecoverable steps are: <list>: these are gated regardless of how good the model gets.
- Revisit when: <named trigger, e.g. "the regulator's rule changes", not a date>
```

</details>

<details><summary><b>Prompt · Triage a backlog for AI fit</b>, You have ten requests and an agent-first directive</summary>

```text
For each item below, answer these three questions IN ORDER and stop at the first "no":

1. Is there a genuine judgement call, could two competent people reasonably differ?
   (If the criteria are published and unambiguous, answer NO: it is a rule.)
2. Is the volume high enough to justify evaluation, gates and a harness?
3. Is a wrong answer recoverable?

Then classify: RULE (code) / ASSISTED (model drafts, person decides) / AGENTIC WITH GATES /
FULLY AGENTIC.

Output a table: Item | Q1 | Q2 | Q3 | Verdict | One-line justification.

Be strict on Q1. Most backlog items are rules. If you are unsure, answer NO and say what
would have to be true for it to be a judgement call.

ITEMS:
<paste>
```

</details>

<details><summary><b>Prompt · Argue the opposite</b>, Before you commit to an agentic verdict</summary>

```text
I have concluded that <feature> should be built as <verdict>.

Make the strongest possible case that I am wrong and it should instead be <the cheaper
alternative: a rule in code / a person>.

Be specific and concrete. Use my own numbers below. Where my reasoning depends on an
assumption I have not evidenced, name it.

End with: the single piece of evidence that would settle this either way.

MY REASONING:
<paste the record>
```

</details>

**Worked example · SkyWays · the verdict that shaped everything**

> Judgement: yes: which alternative suits this passenger depends on their connection, their fare rules, whether they will accept an overnight. Volume: 240 a day. Recoverable: **partly**: a proposed rebooking can be withdrawn, a cash refund cannot. So the verdict was *agentic with gates*, and the gate went on the refund. That single 'partly' is why the product has a named approver on refunds ninety days later, and why the $2,000 incident on day 82 was a failure to implement a decision already made rather than a failure to make it.

**Pitfalls**

- Treating the directive as the answer. *Everything must be agent-first* is a strategy, not a design input, and the AI-fit record is how you serve the strategy honestly rather than theatrically.
- Answering question three with 'we would notice'. Noticing is not recovering. The test is whether the action can be undone, and how fast.
- Recording the verdict without the rejected options. A verdict with no alternatives reads as a preference and gets re-litigated at the first incident.

**Done when**, You can hand the record to a sceptical executive and they can see what you decided, what you rejected, and what would change your mind, without you in the room.

---

## 3 · Frame

### Size the value and set the autonomy

*Before the budget conversation, and before anyone writes a prompt*

Two numbers come out of this step and both get argued about later, so derive them now. **Value** is arithmetic, not adjectives, and the honest version subtracts what it costs to run and what it costs to check. **Autonomy** is set per action and follows the cost of a mistake, never what the model is capable of. Get autonomy wrong and you are arguing about 'the assistant' for six weeks; get it right and the argument becomes a two-minute lookup.

**What you actually do**

1. **Write the value line with real numbers**: cases × minutes saved × cost per minute, minus cases × run cost, minus the review load. Every term from the pain register. Nothing as an adjective.
2. **Get the run cost from engineering**: Tokens per case, cached and routed. Early on this is an estimate; ask for the estimate and the assumption behind it, and re-ask once there is a real per-call log.
3. **Add the review row, honestly**: What share of cases a human checks, and for how long. It is high in the first cycle and falls as the artefacts sharpen. Omitting it is what makes cycle two look like a regression when it is actually the recovery.
4. **List the feature's actions, not the feature**: Show options · rebook same-day · rebook across partners · issue a refund. Autonomy is per action. A product-level autonomy level forces everything to the strictness of the riskiest action or the looseness of the safest.
5. **Score each action on cost of a mistake and reversibility**: Reversibility is the hinge and the column that ends most arguments. Three executives stop disagreeing once the question is per action and the answer is derived.
6. **Set the level, and the evidence that would raise it**: Levels rise on evidence, one step at a time, and an incident usually drops one. Write the raising condition down now, while nobody is under pressure.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Give it the value-line formula and your numbers and have it produce the table plus a sensitivity view: which single input, if wrong by 20%, changes the answer most.<br>⚠ Check every number it echoes back. Models are careless with arithmetic they were handed in prose; ask it to show the calculation, not just the total. |
| **Claude Code** | Have it build the value line as a small script or sheet with the assumptions as named variables, so finance can change one and watch the answer move. |
| **Chat LLM** | Paste the action list and ask it to sort them by reversibility and name what a single wrong action costs. Useful as a first pass that you then correct.<br>⚠ It does not know your refund policy or your regulator. Treat its cost estimates as prompts for your own thinking, never as inputs. |
| **Do not delegate** | The autonomy level itself. This is the decision that money and regulators hang off, and it is yours with your name on it. |

**The artefact**

| | |
| --- | --- |
| Produces | **Value line + autonomy decision record** |
| Good looks like | A net number per day with every term shown, and a table of actions each with a level, a reversibility mark and the evidence that would raise it. |
| Owner | Product manager |

<details><summary><b>Template · Value line and autonomy record</b></summary>

```markdown
# Value and autonomy · <feature>
_Decided: <date> · Owner: <name>_

## Value line
| Term | Value | Source |
|------|-------|--------|
| Cases per day | <n> | pain register |
| Minutes saved per case | <n> | <measured how> |
| Cost per minute (loaded) | $<n> | finance |
| **Gross saving / day** | **$<n>** | = cases x minutes x rate |
| Run cost per case (tokens, cached + routed) | $<n> | engineering, <date> |
| Share of cases reviewed | <n>% | cycle 1 estimate |
| Review minutes per reviewed case | <n> | |
| **Net / day** | **$<n>** | |

Cycle-2 expectation: review share falls to <n>%, net becomes $<n>/day. Say this now,
so the cost story has a trajectory rather than a surprise.

## Autonomy, per action
| Action | Cost of ONE mistake | Reversible? | Level | Raise it when |
|--------|--------------------|-------------|-------|---------------|
| <show options> | ~$0 | yes | acts alone | n/a |
| <same-day rebook> | $<n> | mostly | acts, monitored | <evidence> |
| <cross-partner rebook> | $<n> | with effort | acts, veto window | <evidence> |
| <issue refund> | $<n> | **no** | **named approver, every time** | does not rise without <x> |

## The door
Actions marked NOT reversible are one-way doors. They stay gated regardless of measured
accuracy, because the bar that would justify removing the gate is not reachable.

## Review cadence
Levels are reviewed <monthly> against evidence. An incident drops the level of the action
involved by one, automatically.
```

</details>

<details><summary><b>Prompt · Build the value line, with sensitivity</b>, You have the pain register numbers</summary>

```text
Compute a value line from these inputs and SHOW THE ARITHMETIC at each step.

net per day = (cases x minutes_saved x cost_per_minute)
            - (cases x run_cost_per_case)
            - (cases x review_share x review_minutes x cost_per_minute)

INPUTS:
- cases per day: <n>
- minutes saved per case: <n>
- loaded cost per minute: $<n>
- run cost per case: $<n>
- review share: <n>%
- review minutes per reviewed case: <n>

Then:
1. Give me the net per day, per month, per year.
2. Sensitivity: for each input, show the net if it were 20% worse. Rank them by impact.
3. Tell me which single input is both high-impact AND least evidenced. That is the one
   I should go and measure before I present this.
```

</details>

<details><summary><b>Prompt · Draft the autonomy table</b>, You have the action list and need a first pass</summary>

```text
Here are the actions <feature> can take: <list them>.

For each, produce a row:
| Action | What ONE wrong instance costs | Reversible? (yes / with effort / no) | Suggested level |

Levels, in order: acts alone · acts monitored · acts with a veto window · named approver
every time · not delegated at all.

Rules:
- Set the level from cost-of-mistake and reversibility ONLY. Ignore how capable the model is.
- Anything involving money, identity or a regulatory commitment defaults to "named approver".
- Anything irreversible defaults to "not delegated".
- Where you do not know our costs, write UNKNOWN, do not estimate.

Then list the questions I must answer before this table can be signed.
```

</details>

<details><summary><b>Prompt · Pressure-test an autonomy level</b>, Someone wants a level raised</summary>

```text
An executive wants <action> raised from <level A> to <level B>, because
"it has been right every time for <period>".

Act as a sceptical risk reviewer. Tell me:
1. What sample size would be needed to support that claim, given the bar for this action?
   (bar = damage / (damage + saving); show the arithmetic)
2. What the lower bound of the observed success rate actually is at the sample size we have.
3. What is the DOOR, if we raise it and it goes wrong, how fast can we go back?
4. The smallest safe step: what is the ONE level up, with what monitoring?

Our numbers: <cases in period>, <errors>, <damage per wrong>, <saving per right>.
```

</details>

**Worked example · SkyWays · the table that ended the argument**

> Three executives were arguing about how much the assistant should do. One wanted drafting only, one wanted automatic rebooking, one wanted refunds too. The argument ran for two weeks because it was about *the assistant*. Recast as four actions with a reversibility column, it took twenty minutes: options act alone, same-day rebooking acts monitored, cross-partner gets a veto window, refunds get a named approver every time. Nobody had to lose, because nobody had been arguing about the same thing.

**Pitfalls**

- A value line with an adjective in it. *Significantly faster* cannot be defended when the token bill lands, and the token bill always lands.
- Setting autonomy from model capability. The question is never what it can do; it is what a mistake costs and whether you can undo it.
- Omitting the review row to make cycle one look better. Cycle two then looks like a regression, and you spend the meeting explaining an artefact of your own reporting.

**Done when**, Finance can change one assumption in your value line and see the answer move, and every action has a level that somebody derived rather than preferred.

---

> **P1 · Design & Spec begins here**, *what exactly is being built, and under whose authority?*

## 4 · Specify

### Write the spec a machine can build from

*P1, before the first bolt is cut*

A thirty-page PRD is read by nobody and interpreted differently by everyone, and when handed to a coding agent it produces the wrong thing confidently. The spec is the one place the machine can look, so it must be exact and small: three classical fields plus five agentic ones, on one screen. The five agentic fields are almost always the decisions nobody had made, which is the real value of the exercise, not the document.

**What you actually do**

1. **Keep the three classical fields**: Title, value, acceptance. These do not change and the PRD already has them.
2. **Add the five agentic fields**: The model's role · autonomy · the bar per slice · the fallback · the records it must write. Each has an owner: autonomy is yours, the bar is yours with QA, the fallback is the architect's, the records are the architect's.
3. **Write acceptance in EARS, not prose**: WHEN a trigger AND a condition THE SYSTEM SHALL a behaviour, within a measure. Every 'should' in your criteria is a place the agent will invent something.
4. **Add a BOUNDARY line per thing that must never happen**: Negative requirements are invisible to a model unless stated. *Never issue a refund without a named approver* is a boundary, and it also becomes a test.
5. **Derive the bar per slice**: bar = damage / (damage + saving), per kind of case. A single bar for the whole feature is how the hard slice ships broken while the easy one waits.
6. **Shard the PRD rather than delete it**: The thirty pages stay as the source. Use a cheap model to cut them into per-feature specs. The PRD is for humans and history; the spec is for building.
7. **Run the reading test**: Hand the eight fields to someone who was not in the room and ask them to build it. Every question they ask is a field you have not finished.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM (cheap tier)** | Shard a long PRD into per-feature eight-field specs. This is the single highest-leverage delegation in the role: mechanical, verifiable, and it takes you an hour by hand.<br>⚠ It will fill the five agentic fields with plausible guesses. Blank them out and decide each one yourself, the guesses are the exact thing you are trying to surface. |
| **Chat LLM** | Convert prose acceptance criteria to EARS and report how many 'should's it removed. The count is a useful measure of how much ambiguity you were shipping.<br>⚠ Check that every SHALL ends in a measure. It will happily produce a clean EARS sentence with no number in it. |
| **Chat LLM, adversarially** | The reading test, cheaply: 'you are a coding agent, build this, and list every assumption you had to make'. Its assumption list is your gap list. |
| **Do not delegate** | The bar and the autonomy fields. Both are business risk decisions with your name on them, and both have a formula, use the formula, not the model. |

**The artefact**

| | |
| --- | --- |
| Produces | **Eight-field spec + acceptance bar sheet** |
| Good looks like | One screen. A coding agent builds from it unaided, and the QA lead can write tests from it without asking you a question. |
| Owner | Product manager |

<details><summary><b>Template · The eight-field agentic spec</b></summary>

```markdown
# Spec · <feature>
_Version <n> · <date> · Owner: <name> · Source PRD: <link>_

**1 · Title**
<one line>

**2 · Value**
<the value-line net, and the pain register line it serves>

**3 · Acceptance criteria (EARS)**
WHEN <trigger> AND <condition>
THE SYSTEM SHALL <observable behaviour>
WITHIN <measure: time, count or threshold>.

WHEN <...> THE SYSTEM SHALL <...> WITHIN <...>.

BOUNDARY  The system shall NEVER <thing that must not happen>.
BOUNDARY  The system shall NEVER <...>.

**4 · The model's role**
<Which steps the model decides, in one sentence. Which steps are exact code. Which
 step changes something real.>

**5 · Autonomy**
| Action | Level | Approver |
|--------|-------|----------|
| <action> | <level> | <role, if gated> |

**6 · The bar, per slice**
| Slice | Saving per right case | Damage per wrong case | Bar | With a hold? |
|-------|----------------------|----------------------|-----|--------------|
| <same-day> | $<n> | $<n> | <n>% | |
| <codeshare> | $<n> | $<n> | <n>% | |
| <refund> | $<n> | $<n> | <n>% | yes, <what the hold is> |

**7 · Fallback**
<What happens when the model cannot meet the bar on a case, or a tool fails. Who or what
 catches it, and what the passenger/user sees.>

**8 · Records**
<What must be written for every consequential action: which fields, redacted how, kept
 how long.>

---
## Reading test
Handed to <name> on <date>. Questions they asked:
1. <question> -> field <n> updated
2. <...>
```

</details>

<details><summary><b>Prompt · Shard a PRD into eight-field specs</b>, You have a long PRD and need per-feature specs</summary>

```text
Below is a product requirements document.

Split it into one spec per feature. For each, output EXACTLY these eight fields:
1 Title
2 Value
3 Acceptance criteria, in EARS: WHEN <trigger> AND <condition> THE SYSTEM SHALL
  <behaviour> WITHIN <measure>. Plus BOUNDARY lines for anything that must never happen.
4 The model's role
5 Autonomy
6 The bar, per slice
7 Fallback
8 Records

CRITICAL: for fields 4-8, write "NOT DECIDED, <the question that must be answered>"
wherever the PRD does not actually say. Do NOT infer, do NOT use a sensible default.
Those gaps are the output I am looking for.

PRD:
<paste>
```

</details>

<details><summary><b>Prompt · Prose to EARS, with a ambiguity count</b>, Your criteria are full of 'should'</summary>

```text
Rewrite these acceptance criteria in EARS.

Format: WHEN <trigger> AND <condition> THE SYSTEM SHALL <observable behaviour>
WITHIN <measure>.

Rules:
- Every SHALL must end in a measure: a time, a count or a threshold. If the original has
  no number, write WITHIN <MEASURE MISSING> and list it at the end.
- Turn every "should", "may", "as appropriate", "if needed" into either a hard condition
  or a separate criterion. List each one you removed and what you replaced it with.
- Add a BOUNDARY line for every implied prohibition.

Finish with: (a) count of ambiguous terms removed, (b) list of missing measures.

CRITERIA:
<paste>
```

</details>

<details><summary><b>Prompt · The reading test, as an agent would fail it</b>, Before you hand the spec to engineering</summary>

```text
You are a coding agent. You will build EXACTLY what this spec says and nothing
more. You cannot ask questions.

1. List every assumption you would have to make to start building.
2. For each, say what you would most likely assume, and what the cost would be if that
   assumption were wrong.
3. Point at the single sentence in the spec most likely to be interpreted two ways, and
   give me both readings.
4. Tell me which of the eight fields is weakest.

Do not build anything. Do not suggest improvements. Just show me where I was vague.

SPEC:
<paste>
```

</details>

**Worked example · SkyWays · thirty pages to eight fields**

> The PRD was thirty pages and the spec was one screen. Three fields transferred straight across. Of the five agentic fields, **five were undecided**: nobody had said what the model's role was versus the fare engine's, what autonomy refunds had, what accuracy counted as good, what happened when it could not decide, or what had to be logged. Each was settled with its owner in under an hour. The document took a morning; the decisions it forced were the point. The one that mattered most was the fallback: without it, the engineer would have chosen one by default, because the code has to do something.

**Pitfalls**

- Letting the model fill the five agentic fields. Its guesses are plausible and they are exactly the decisions you were trying to surface.
- A single bar for the whole feature. The easy slice waits while the hard slice ships below its bar, and the average hides both.
- Deleting the PRD. It is the source you shard from and the record of why; the spec is the thing you build from. They do different jobs.

**Done when**, A coding agent and the QA lead both read the spec the same way, and neither has to ask you a question to start.

---

## 5 · Plan

### Plan in bolts, not sprints

*P1 to P2, once the spec is signed*

When building is fast, the unit of planning shrinks to match. The agent builds a story in hours and then waits nine days for a sprint review, while leadership wants evidence daily. A **bolt** is a thin, shippable slice reviewed and integrated the same day. Same ten working days; evidence on all ten instead of a demo on the fourteenth, and a wrong turn costs one day rather than two weeks.

**What you actually do**

1. **Cut the sprint's stories into daily slices**: Each must be shippable alone. Five stories usually become eight to twelve bolts, and the ones that will not split are the ones hiding two risks.
2. **Put the walking skeleton on day one**: The thinnest end-to-end path with no model in it. It proves the pieces connect, which is the assumption every other bolt rests on, and it costs half a day.
3. **Give each bolt exactly one unknown**: Then a day can fail for one reason and you know which. Two unknowns in a bolt means a day spent bisecting rather than building.
4. **Hand the cut to the architect for dependency order**: You decide the cadence; they decide the order. This division matters: a plan ordered by business priority will schedule a gated write before the plug it needs.
5. **Put the shadow run in the plan as a milestone**: Not a launch date. A window with a threshold. Fixing it now stops it being negotiated away later, when a date is under pressure.
6. **Move the demo to every day**: Leadership asked for visibility, and a daily merged slice is better visibility than a rehearsed fortnightly demo.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Give it the stories and ask for a bolt cut with a 'depends on' column and one unknown per bolt. It is good at spotting the story that contains two risks.<br>⚠ It will not know your integration realities. The dependency column it produces is a draft for the architect, not a plan. |
| **Claude Code** | Have it topologically sort the bolts from the depends-on column and refuse cycles. A cycle always means a mis-cut, so the failure is the finding. |
| **Chat LLM** | Draft the story file for tomorrow's bolt from the spec: context by reference, EARS slice, tools, tests, done-when, cost. Mechanical work, done well.<br>⚠ It will paste context rather than reference it. Insist on links to the context layers, or the story file becomes forty thousand tokens. |
| **Do not delegate** | Which slice ships first. That is a business call about where the value and the risk are, and under a deadline it is the whole decision. |

**The artefact**

| | |
| --- | --- |
| Produces | **Bolt plan** |
| Good looks like | One line per bolt with its single unknown, its dependency, and its day. The walking skeleton is on day one, and nothing is scheduled before the thing it needs. |
| Owner | Product manager, with the architect on ordering |

<details><summary><b>Template · Bolt plan</b></summary>

```markdown
# Bolt plan · <feature> · <cycle>
_Cadence: one bolt per day, reviewed and integrated same day_

| Day | Bolt | The ONE unknown it retires | Depends on | Slice it serves | Done when |
|-----|------|---------------------------|-----------|-----------------|-----------|
| 1 | Walking skeleton, <read X, show it>, no model | do the pieces connect? | — | all | end to end, in staging |
| 2 | <exact function> | <...> | — | <slice> | unit tests green |
| 3 | | | | | |

## Rules for this plan
- A bolt that cannot be built alone was cut wrong, send it back before starting it.
- Exact code early: it stands alone and never blocks.
- The plug (MCP / integration) lands before any gated write that needs it.
- The proof (harness, golden set) is last, because it needs something to run against.

## Milestones that are not dates
| Milestone | Condition, not date |
|-----------|--------------------|
| Shadow run starts | harness green on all slices at their bar |
| Shadow run ends | <n> days AND <n>% agreement per slice |
| Cut-over to 5% | shadow threshold met; rollback rehearsed |
| Widen | live lower bound holds above bar, per slice |

## What leadership sees
Daily: what merged yesterday. Weekly: the two numbers.
```

</details>

<details><summary><b>Prompt · Cut stories into bolts</b>, You have a sprint backlog and need daily slices</summary>

```text
Cut these stories into bolts. A bolt is a thin slice that can be built, tested and
integrated in ONE day, ALONE.

For each bolt give me:
| Bolt | The ONE unknown it retires | Depends on | Can it be built alone? |

Rules:
- If a bolt would retire two unknowns, split it.
- If a bolt cannot be built alone, say so and explain what it needs.
- Put a walking skeleton first: the thinnest end-to-end path with NO model in it.
- Pure deterministic code (calculations, validations) should come early, it stands alone.
- Anything that writes or changes real data comes after the integration it depends on.

Finally: list any story that resisted splitting, and say what two risks it is hiding.

STORIES:
<paste>
```

</details>

<details><summary><b>Prompt · Draft tomorrow's story file</b>, The bolt is chosen and engineering needs a self-contained brief</summary>

```text
Write an agent-ready story file for this bolt. It must be buildable with NO chat
history and NO access to me.

Sections, exactly:
## Context: LINKS ONLY to the context layers and ADRs. Do not paste their contents.
## Spec (the EARS criteria for THIS slice only, copied from the spec verbatim.
## Tools) signatures the bolt may call, with their risk band.
## Tests (the golden slice it must pass and its bar, plus unit assertions.
## Done when) one testable line.
## Cost: expected tokens per call and the tier.

BOLT: <name and the one unknown>
SPEC EXTRACT: <paste the relevant EARS lines>
CONTEXT LAYERS: <paths>
```

</details>

**Worked example · SkyWays · ten days, ten proofs**

> The sprint held five stories and a demo on day fourteen. Recut, it became ten bolts. Day one was a walking skeleton that read a booking and displayed it, no model, half a day, and it found a credentials problem in the reservation adapter that would otherwise have surfaced on day nine. Day two was the fare-difference function, unit tested, standing alone. The first model call did not appear until day four, by which point everything it depended on was proven. The wrong turn that cycle cost one day.

**Pitfalls**

- Ordering by business priority. That is the right way to choose what is in the plan and the wrong way to sequence it; the architect's dependency order is what makes each day buildable.
- A bolt with two unknowns. When the day fails you spend the next one bisecting, which is the cost the whole practice exists to avoid.
- Letting the shadow run become a date. It is a window with a threshold; as a date it will lose the argument to the launch the first time they conflict.

**Done when**, Every bolt in the plan can be built on its scheduled day without waiting for anything, and the walking skeleton is on day one.

---

> **P2 · Build & Prove begins here**, *does it meet the bar, slice by slice?*

> ⛔ **The hard gate. P1 to P2.** Everything past this point depends on the spec, the acceptance bar per slice and the authority budget being signed. It is the one crossing nothing downstream survives without. [why](The-Agentic-PDLC).

## 6 · Gate

### Hold the three gates that are yours

*Throughout P2, at every bolt and every release*

Five gates exist across the lifecycle and you own three. A gate is a decision with evidence in front of a named person and their name on it, not a click, not a status column, not a meeting that ends in 'fine'. The common failure is a product manager approving a pull request they cannot evaluate while nobody asks them the one thing they can judge, which is whether it is worth doing at all.

**What you actually do**

1. **Claim intent, plan and release; decline the other two**: Behaviour and expansion belong to the QA lead. Ask to be removed from those sign-offs. Your name on a judgement you cannot make weakens every gate you do hold.
2. **Write the evidence line for each gate before you need it**: Intent: pain register, AI-fit verdict, value line. Plan: bolt cut, authority budget, gate map. Release: shadow comparison, rollback rehearsed. Empty evidence line, no gate.
3. **Audit last month's approvals**: List them and strike the ones you could not evaluate. The list is usually longer than expected and it is the fastest way to make this concrete with your team.
4. **Read the eval readout in the shape of your bar sheet**: Per slice, against its bar, with the lower bound. Not one percentage. You do not need to understand the harness; you need the readout in the shape of the artefact you wrote.
5. **Write down the rejection rule**: Any slice below its bar rejects the change, however good the headline. Written down once, it stops being re-argued per release.
6. **Make a drift alert re-open the release gate**: Automatically. This is what turns a chart into a control, and it is a one-line policy decision that you own.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Chat LLM** | Paste a release summary and your bar sheet and ask: which slices are below bar, and what does the overall number hide? It is reliable at the comparison and it never gets bored.<br>⚠ Give it the lower bounds, not just the scores, or it will tell you a 40-case slice has passed. |
| **Claude Code** | Have it produce the per-slice readout from the harness output automatically, in the shape of your bar sheet, so the readout arrives already comparable. |
| **Chat LLM** | Before a release gate, ask it to list every way this change could regress a slice that was not tested. A cheap pre-mortem. |
| **Do not delegate** | The gate decision itself. A gate is defined by a name on it. A model cannot hold accountability, so it cannot hold a gate. |

**The artefact**

| | |
| --- | --- |
| Produces | **Gate decision record** |
| Good looks like | Three named decisions per release with the evidence attached, rather than a stream of approvals nobody can defend. |
| Owner | Product manager |

<details><summary><b>Template · Gate decision record</b></summary>

```markdown
# Gate · <intent | plan | release> · <feature> · <date>

**Decision:** pass / hold / reject
**Decided by:** <name>  (a gate has exactly one name on it)

## Evidence in front of me
| What | Value | Link |
|------|-------|------|
| <for intent: pain register line> | | |
| <for intent: AI-fit verdict> | | |
| <for intent: value line, net/day> | $<n> | |
| <for plan: bolt cut reviewed by architect> | yes/no | |
| <for plan: authority budget, caps in tool signatures> | yes/no | |
| <for release: shadow agreement, per slice> | | |
| <for release: rollback rehearsed on> | <date> | |

## Per-slice check (release gate)
| Slice | Score | Lower bound | Bar | Pass? |
|-------|-------|-------------|-----|-------|
| | | | | |

**Rule:** any slice whose LOWER BOUND is below its bar rejects the change, whatever the
overall number says.

## Conditions attached to a pass
- <e.g. refunds stay gated; widen only on live evidence>

## What would re-open this gate
- A drift alert above <n>% week over week (automatic)
- An incident on any gated action
```

</details>

<details><summary><b>Prompt · Per-slice release readout</b>, QA hands you a score and you need to decide</summary>

```text
Compare this evaluation output against my acceptance bars.

Produce ONE table:
| Slice | Score | n | 95% lower bound | Bar | PASS / FAIL / UNPROVEN |

Rules:
- lower bound = p - 1.96 * sqrt(p*(1-p)/n). Show it even if they gave me only the score.
- PASS only if the LOWER BOUND is at or above the bar.
- If the score is above the bar but the lower bound is not, mark UNPROVEN and tell me how
  many more cases are needed: n = 1.96^2 * p * (1-p) / (p - bar)^2.
- Flag any slice that got WORSE than the previous run, even if it still passes.

Finish with one line: ship, or do not ship, and the single reason.

BARS: <paste bar sheet>
RESULTS: <paste>
```

</details>

<details><summary><b>Prompt · Audit my own approvals</b>, You suspect you are signing things you cannot judge</summary>

```text
Here are the approvals I gave last month: <paste list>.

For each, tell me:
- Which of the five gates it belongs to: intent / plan / behaviour / release / expansion.
- Whether a product manager can evaluate it, or whether it needs engineering or QA judgement.
- If I could not evaluate it: who should have signed, and what I should have been asked instead.

Then give me the short script I can use to hand the wrong ones back.
```

</details>

**Worked example · SkyWays · the readout that stopped a release**

> The overall golden-set score rose from 79% to 84% and the team wanted to ship. The readout in bar-sheet shape showed codeshare had fallen from 81% to 77%, against a bar of 80. The headline had improved because the easy high-volume slice improved, and averaging hid a real regression on the slice that carried all the risk. The change was rejected in four minutes, because the artefact arrived in the shape of the decision rather than in the shape of the harness.

**Pitfalls**

- Approving what you cannot evaluate. It feels cooperative and it devalues every gate you hold.
- Accepting a single accuracy number. The slice that carries the risk is always the one the average hides.
- Treating a gate as a meeting. A gate is a name and an evidence line; the meeting is optional.

**Done when**, Every release has three named decisions with evidence attached, and you have been removed from the two sign-offs that were never yours.

---

> **P3 · Run & Learn begins here**, *is it still doing what we launched, and what did it cost?*

## 7 · Launch

### Shadow, then five percent, then widen

*The end of P2 into P3*

Never switch on with nothing to compare against. A shadow run puts the agent beside the live process, deciding and logged but taking no action, for a window fixed in advance. Then five percent of real traffic, then wider, and the widening is earned by live evidence rather than by a date. If it does not match the humans, you learned that for free.

**What you actually do**

1. **Put a shadow window in the plan before any switch-on date exists**: Fourteen days is a common default. Fixing it early stops it being negotiated away when a launch date is under pressure.
2. **Set the threshold, and the money exception**: 95% agreement per slice is a reasonable default. Money actions are excluded from automatic agreement and stay gated regardless of what the shadow shows.
3. **Compare per slice, decision by decision**: Overall agreement of 96% can sit on top of 64% on refunds. The headline is the trap.
4. **Read every disagreement in the first week**: Personally. The disagreements are the cheapest product research you will ever get, and half of them are the humans being wrong, which is also a finding.
5. **Rehearse the rollback before the cut-over**: Not during. With a flag-driven shadow path the rollback is the flag, and you should have watched someone throw it.
6. **Widen on evidence, slice by slice**: Compute how long each share needs: days = cases needed / (share × cases per day). A small share is the safe place to start and a slow place to learn, which is why you widen.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it build the nightly comparison: agreement per slice, the disagreement list ranked by cost, and a chart. This is a reporting job, done once, run every night.<br>⚠ Insist the comparison is per slice from the start. Retrofitting slices onto an aggregate comparison means re-running the window. |
| **Chat LLM** | Cluster the disagreements and name the themes. Forty disagreements usually collapse into four causes, and the clustering is exactly what a model is good at.<br>⚠ Read the raw disagreements yourself first, at least in week one. The clusters are more useful once you know what the edges look like. |
| **Chat LLM** | Compute the widening schedule from cases-needed and traffic share, and tell you the date each slice could widen if evidence holds. |
| **Do not delegate** | The cut-over decision, and any decision to exclude a slice from gating. Those are yours. |

**The artefact**

| | |
| --- | --- |
| Produces | **Cut-over decision** |
| Good looks like | A comparison per slice over a fixed window, a threshold met or not met, a rehearsed rollback, and a widening schedule with conditions rather than dates. |
| Owner | Product manager |

<details><summary><b>Template · Shadow run and cut-over decision</b></summary>

```markdown
# Cut-over decision · <feature>
_Shadow window: <start> to <end> (<n> days) · Decided: <date> · By: <name>_

## Agreement, per slice
| Slice | Decisions compared | Agreed | Agreement | Threshold | Met? |
|-------|--------------------|--------|-----------|-----------|------|
| <same-day> | <n> | <n> | <n>% | 95% | |
| <codeshare> | <n> | <n> | <n>% | 95% | |
| <refund> | <n> | <n> | <n>% | n/a, stays gated | |

**Money actions are excluded from automatic agreement and remain gated regardless.**

## Disagreements, the themes
| Theme | Count | Agent right / desk right | Action |
|-------|-------|--------------------------|--------|
| | | | |

## Rollback
- Mechanism: <the flag>
- Rehearsed on <date> by <name>; time to revert: <n> minutes
- Who can throw it without asking: <names>

## Widening schedule: conditions, not dates
| Share | Cases needed | Days at this share | Widen when |
|-------|--------------|--------------------|-----------|
| 5% | <n> | <n> | live lower bound >= bar on <slice> |
| 25% | <n> | <n> | as above, plus zero <class> incidents |
| 100% | | | |

## Decision
<cut over to 5% on <date> | extend the shadow by <n> days | do not proceed, because ...>
```

</details>

<details><summary><b>Prompt · Nightly shadow comparison spec</b>, Setting up the shadow run</summary>

```text
Write the spec for a nightly job comparing an agent's shadow decisions against the
live human desk.

It must output, PER SLICE (not just overall):
- decisions compared, agreed, agreement %
- a ranked list of disagreements: the input, the agent's decision, the desk's decision,
  and the estimated cost of the difference
- a flag on any slice whose agreement dropped versus the previous night

Constraints:
- money actions are reported separately and never counted toward automatic agreement
- the agent must never write; add an assertion that fails the job if a write is detected
- output is one markdown file and one CSV

Our slices: <list>. Our data: <where the decisions are logged>.
```

</details>

<details><summary><b>Prompt · Cluster the disagreements</b>, You have a week of shadow output</summary>

```text
Here are <n> cases where the agent and the human desk disagreed.

1. Cluster them into at most 6 themes. Name each theme in plain words.
2. For each theme: how many cases, and is the AGENT or the DESK more often right? Say
   which and why, do not assume the human is the ground truth.
3. Rank the themes by estimated cost of being wrong, not by frequency.
4. For the top theme, tell me whether the fix is the spec, the prompt, the tools, or the
   bar, and what specifically I would change.

DISAGREEMENTS:
<paste>
```

</details>

<details><summary><b>Prompt · Widening schedule arithmetic</b>, Shadow passed and you need a credible plan</summary>

```text
Compute a widening schedule.

For each slice give me: cases needed to prove the bar, then days of live evidence at 5%,
25% and 100% of traffic.

cases needed = 1.96^2 * p * (1-p) / (p - bar)^2
days = cases needed / (share x cases per day)

Then write the schedule as CONDITIONS, never dates: "widen to 25% when the live lower
bound on <slice> holds at or above <bar> for <n> consecutive days".

Flag any slice where 5% would take more than 30 days, those need a bigger starting
share or a different approach, and I need to know now.

Slices, observed scores, bars, cases/day: <paste>
```

</details>

**Worked example · SkyWays · what seven days bought**

> The full plan needed ten weeks and the sponsor had six, so the shadow window was cut from fourteen days to seven, but only on the simple slice, and with every disagreement read. Seven days at 144 same-day cases a day is about a thousand decisions, which bounds a 97% slice tightly. Codeshare stayed at 76% against a bar of 80 and did not ship, and nobody pretended otherwise. The sponsor heard it as a trade rather than a delay: sixty percent of the load in six weeks, proven, with codeshare next.

**Pitfalls**

- Cutting over at fifty percent. Half your users meet the first-day failure, and first-day failures are the ones that get remembered.
- A three-day shadow as a formality. It contains no weekend and no disruption day, so it buys false confidence at full price.
- Reading only the aggregate agreement. The slice with the money in it is small, and small slices disappear into averages.

**Done when**, You can tell the sponsor what share of traffic the agent handles, what evidence earned it, and how fast you can take it back.

---

## 8 · Learn

### Report two numbers and turn incidents into the next frame

*P3, every cycle, forever*

This is the step that decides whether the programme survives. A first cycle can genuinely save time and cost more, and that is survivable, if it arrives from you rather than from finance. Then production becomes the source of the next P0: drift is a KPI you watch, and an incident is a brief you write, not a name you find.

**What you actually do**

1. **Take the baseline before the pilot**: An afternoon's work, and worthless afterwards. This is the single most commonly skipped step in the whole role, and it is unrecoverable once the pilot has started.
2. **Report time saved and money spent, together, always**: Plus two rows that keep them honest: review hours added, and re-runs. The programme is cancelled on the number you hid, never on the one you showed.
3. **State the trajectory, not just the point**: Cost turns positive from cycle two as the review load falls. Say so in cycle one, with the expected number, so cycle two is a confirmation rather than a surprise.
4. **Chart one output mix weekly**: The one that would embarrass you if it drifted. A probabilistic system changes behaviour when the world shifts under it, with no deploy and no error.
5. **Set the drift alert, and wire it to the release gate**: Five percent week over week as a starting default. The wiring is what makes it a control rather than a chart nobody opens.
6. **Rewrite every incident as a brief**: Pain, evidence, the missing enforced control, the fix, the value. A postmortem that produces a name has not finished; one that produces a control has.
7. **Run the maturity self-check, honestly**: Six controls, present or absent. Your level is how many you have; your next step is the first one you do not. It replaces the tool-count metric, which rewards the least mature behaviour available.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Build the two-number report from the engineering ledger automatically, every cycle, with the review and re-run rows included by construction so they cannot be quietly dropped. |
| **Chat LLM** | Draft the steering-committee narrative from the numbers. Ask it for the version a sceptical CFO would ask questions about, then answer those questions before the meeting.<br>⚠ Do not let it choose which numbers to feature. That selection is the integrity of the report and it is yours. |
| **Chat LLM** | Turn a postmortem transcript into the five-part brief, forcing the missing-control question. It is good at holding the format when the room wants to talk about blame.<br>⚠ Check that its 'missing control' is genuinely enforceable. It will happily propose a better prompt, which is a request, not a control. |
| **Do not delegate** | Deciding what to report. Everything else in this step can be drafted; the choice of what the sponsor sees is the job. |

**The artefact**

| | |
| --- | --- |
| Produces | **Two-number report · drift readout · next-P0 brief** |
| Good looks like | One page the sponsor reads in a minute, with both numbers, the trajectory, and the honest rows. Plus a brief that turns the last incident into the next thing you build. |
| Owner | Product manager |

<details><summary><b>Template · Two-number report and next-P0 brief</b></summary>

```markdown
# Cycle <n> · <feature> · <date>

## The two numbers
| | Baseline | Now | Change |
|---|---------|-----|--------|
| Person-days per story | <n> | <n> | <n>% |
| Token spend per story | — | $<n> | |
| Review hours added per story | <n> | <n> | +<n> |
| Re-runs per story | — | <n> | |

**Net this cycle:** saved <n> person-days, spent $<n> and <n> review hours.
**Trajectory:** review load falls to ~<n>h in cycle <n+1> as <what sharpens>; net becomes <n>.

_Baseline taken <date>, BEFORE the pilot, from <source>._

## Drift
| Output mix watched | Last week | This week | Change | Alert at |
|--------------------|-----------|-----------|--------|----------|
| <e.g. % refund vs credit> | <n>% | <n>% | <n>pp | 5pp w/w |

A drift alert re-opens the release gate automatically. Last triggered: <date / never>.

## Maturity
| # | Control | Have it? |
|---|---------|----------|
| 1 | A context file the agent reads | |
| 2 | Every item has a spec, a bar and an owner | |
| 3 | The harness gates the merge, per slice | |
| 4 | Caps live in tool signatures, not prompts | |
| 5 | The trace redacts | |
| 6 | Production evidence by segment, drift watched | |

**Level: <n> of 6. Next: <the first missing one>.**

---
# Next P0 · <title>
**Pain** (<what happened, as a measurement>
**Evidence**) <trace id, date, link>
**Finding**, the enforced control that was missing: <name it>
**Fix**, <the control, where it will live>
**Value**, <this class of incident becomes impossible, not less likely>
```

</details>

<details><summary><b>Prompt · Build the two-number report</b>, End of cycle, from the engineering ledger</summary>

```text
Build a two-number cycle report from this ledger.

MUST include, in this order:
1. Person-days per story: baseline vs now, and % change
2. Token spend per story
3. Review hours added per story (this keeps number 1 honest, never omit it)
4. Re-runs per story (the leak signal)
5. A net line: "saved X person-days, spent $Y plus Z review hours"

Then:
- State the trajectory: what happens to the review load next cycle and why.
- Flag any number where the baseline was taken AFTER the pilot started, because that
  number is not defensible and I need to say so rather than be caught.

Do NOT drop a row because it is unflattering. Do not editorialise.

LEDGER:
<paste>
```

</details>

<details><summary><b>Prompt · Postmortem to next-P0 brief</b>, After an incident, while the room is still arguing</summary>

```text
Turn this incident into a P0 brief. Use EXACTLY this structure:

**Pain** (what happened, as a measurement (amount, count, who was affected)
**Evidence**) the trace or log reference
**Finding** (the ENFORCED CONTROL that, if present, would have made this IMPOSSIBLE
**Fix**) where that control will live (a tool signature, a gate, a permission)
**Value**: what class of incident becomes impossible

Rules:
- Do not name a person. Do not name the input that triggered it.
- "A better prompt" is NOT a control, a prompt is a request that a model can be talked
  past. If your finding is a prompt change, you have not found the control yet.
- Distinguish detection (an alert) from prevention (a cap). Say which yours is.
- If several layers failed, list each as ENFORCED / A REQUEST / ABSENT.

INCIDENT:
<paste>
```

</details>

<details><summary><b>Prompt · The sceptical CFO rehearsal</b>, Before the steering meeting</summary>

```text
You are a sceptical CFO. Here is my cycle report: <paste>.

Ask me the five hardest questions you would ask, in the order you would ask them.
Prioritise:
- anything where the baseline is weak or was taken late
- the gap between the saving and the spend
- whether the saving is real or has moved cost somewhere I am not measuring
- what happens to the spend at 10x volume

For each question, tell me what a good answer looks like and what a bad one sounds like.
Do not be polite.
```

</details>

**Worked example · SkyWays · day ninety**

> The report said 40 to 45 percent fewer person-days and a token bill of $4,200, on one line, with the review hours and the re-run count beside them. The review row was up, and it was in the report, with the reason and the expected fall. The programme continued: not because the numbers were flattering, but because both of them came from the team. The counterfactual is well documented elsewhere: every cycle showing time saved, none showing spend, and a CFO arriving at a budget review with a number nobody in the programme had seen.

**Pitfalls**

- Taking the baseline after the pilot started. Unrecoverable, and everyone can tell.
- Withholding the cost number while it is still bad, meaning to show it once it improves. That is the exact sequence that gets programmes cancelled, and it is usually done by people trying to protect them.
- Counting AI tool adoption as maturity. It rewards the least mature behaviour available; nine tools with no gates is level one.

**Done when**, Your sponsor has never learned a number about this programme from someone other than you.

---

## Read next

- [The wiki page for this role](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Product-Manager)
- [The same case as thirteen episodes](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/story)
- [Every formula on one page](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators)

**Other roles:** [Solution Architect](Journey-Solution-Architect) · [Engineering Lead](Journey-Engineering-Lead) · [QA Lead](Journey-QA-Lead) · [DevOps](Journey-DevOps)

- [The manual, interactive](https://akash-coded.github.io/aws-bedrock-agentcore-strands/) · [every template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/) · [every prompt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/) · [frameworks and acronyms](https://akash-coded.github.io/aws-bedrock-agentcore-strands/frameworks/)

