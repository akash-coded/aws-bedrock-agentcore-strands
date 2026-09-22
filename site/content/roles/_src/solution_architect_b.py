"""Solution architect · steps 4-6."""

STEPS_B = [
{
 "n": 4, "id": "shape", "phase": "Shape",
 "title": "Decide how many agents, and how deep the process runs",
 "when": "P0, straight after the map and before any framework is named",
 "purpose": (
   "Leadership said agent-first and an engineer has built fifteen agents to show what is possible. "
   "Your answer is a number and a condition. **Start single, escalate only on a named limit** — "
   "because each added agent is another context to manage and another hand-off to get wrong, and n "
   "agents have **n(n-1)/2** possible hand-offs between them. The same judgement governs process: "
   "run only the lifecycle stages a given change actually needs, decided per change rather than per "
   "programme."),
 "activities": [
   {"do": "Start single, and put the burden of proof on the second agent",
    "detail": "One agent with its tools handles almost every feature. The default is not a "
              "preference; it is the only position that makes an addition explain itself."},
   {"do": "Count the hand-offs before agreeing to any topology",
    "detail": "Five agents have ten possible hand-offs, fifteen have a hundred and five, and none of "
              "them appears in the diagram. Coordination cost grows faster than the work it splits."},
   {"do": "Test every proposed agent against a fan-out tool",
    "detail": "Parallelism is a property of a **tool**, not of an agent count. Four partner searches "
              "run at once inside one call with zero hand-offs; as four agents they cost six."},
   {"do": "Separate out the roles that are not agents at all",
    "detail": "The pricer is exact work and becomes a function. The reviewer is the one separation "
              "that usually earns itself, because independence is the entire mechanism of a checker."},
   {"do": "Write the escalation condition as a limit with a number in it",
    "detail": "*We move to an orchestrator when a single context exceeds X on multi-leg "
              "international* is a decision. *We might need more agents later* is how a swarm comes "
              "back by default the first time somebody wants more speed."},
   {"do": "Set the process depth per change, not per programme",
    "detail": "A one-line fix skips discovery and most design; a new subsystem runs everything; a "
              "regulatory rule change runs design and validation and no discovery. The living spec is "
              "the backbone on every row."},
   {"do": "Put 'revisit at the trace review' on the record",
    "detail": "Shape is re-decided on evidence, and the evidence arrives in production. A shape "
              "decision with no review date hardens into an assumption nobody remembers making."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Describe the proposed topology and ask for the single-agent version of the same feature, "
           "with the hand-off count for each. The contrast is the argument you need in the room.",
    "caution": "It agrees with whichever design you described first. Ask it to perform the collapse, "
               "not to give an opinion on the design."},
   {"tool": "Claude Code",
    "use": "Point it at an existing multi-agent repository and have it count the agents, the tools, "
           "the distinct contexts and the messages passed between them. Most swarms are a different "
           "size from the one on the whiteboard.",
    "caution": "Make it list the hand-offs it found rather than only a total. The count you can argue "
               "about in a review is the one somebody can read."},
   {"tool": "Chat LLM, adversarially",
    "use": "Ask it to make the strongest possible case for the second agent. If the strongest case "
           "cannot name a limit with a number in it, you have your answer and it cost five minutes.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The escalation condition itself. It depends on your context sizes, your latency budget "
           "and the shape of your team, and it is the line that decides whether the design survives "
           "contact with an enthusiastic engineer.",
    "caution": None},
 ],
 "artifact": {
   "name": "Agent-fit and process-depth decision",
   "good": "A number of agents, the hand-off count that number implies, and a named limit with a "
           "figure in it that would justify the next one. Plus one depth row per kind of change, so "
           "method stops being argued per ticket.",
   "owner": "Solution architect"},
 "template": {
   "title": "Shape and depth decision", "lang": "markdown",
   "body": """# Shape decision · <feature>
_Decided: <date> · Owner: <name> · Revisit at: the P3 trace review_

## How many agents
| Question | Answer | Evidence |
|----------|--------|----------|
| Is this AI at all? | <yes — the PM's AI-fit record> | <link> |
| How many agents? | **<n>, with tools** | |
| Does one context genuinely overload? | <no — largest case measured at <n> tokens against a <n> limit> | <measurement, date> |
| Are there parallel sub-tasks a fan-out tool cannot express? | <no — <n> partner searches run inside one tool> | |
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
| <the pricer> | exact work | a function — map, step <n> |
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
"""},
 "prompts": [
   {"title": "Collapse a proposed topology",
    "when": "Someone has proposed several agents and you have to answer today",
    "body": """Here is a proposed multi-agent design: <paste, including each agent's job>.

Produce the SINGLE-AGENT version of the same feature, then compare the two.

OUTPUT SHAPE:
1. A table: | Proposed agent | What it really is | Where it goes in the single-agent design |
   Allowed values for the middle column: EXACT WORK (a function) · PARALLELISM (a
   fan-out tool) · INDEPENDENCE (a checker) · THE AGENT ITSELF · GENUINELY A SECOND AGENT.
2. The hand-off count for each design, computed as n(n-1)/2, with n stated.
3. For every GENUINELY A SECOND AGENT row, the named limit that justifies it — a number,
   not an adjective.

RULES:
- Parallelism is a property of a TOOL. Do not accept "these can run at the same time"
  as a reason for a second agent.
- A checker is the one separation that usually earns itself, because independence is
  the whole mechanism. Say so where it applies.
- Arithmetic is never an agent. It is a function.
- If you cannot name a limit with a number in it, write "no limit found" rather than
  inventing one. That answer is the useful one."""},
   {"title": "Write the escalation condition",
    "when": "Before the shape decision goes on the record",
    "body": """I am recording a single-agent design for <feature>. Write the escalation condition
that would justify moving to an orchestrator with workers.

OUTPUT SHAPE — exactly two bullets, each in this form:
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
latency budget, how many parallel calls the fan-out tool makes>"""},
   {"title": "Assign a depth row to this week's changes",
    "when": "The team wants one process for everything",
    "body": """Here are the changes my team has in flight: <paste, one per line>.

Assign each a process depth. Run only the lifecycle stages the change actually needs.

OUTPUT SHAPE, one table:
| Change | P0 | P1 | P2 | P3 | Method weight | The stage I am skipping, and why that is safe |

Allowed cell values: full · yes · light · —

RULES:
- The living spec is the backbone on EVERY row, including the one-line fixes. It is
  the constant; everything else flexes around it.
- The full persona trail is layered on ONLY where the work is audited and multi-team.
  On a small feature it is twelve personas between an engineer and a one-line change.
- A regulatory rule change usually needs design and validation and no discovery. Say
  where that applies and where it does not.
- The last column is the point of the exercise. If you cannot say why skipping a stage
  is safe, do not skip it."""},
 ],
 "example": {
   "title": "SkyWays · fifteen agents, a hundred and five hand-offs",
   "body": "An engineer had built fifteen agents to show what the framework could do. The collapse "
           "took an afternoon and one table. The pricer was exact work and became a function. The "
           "searcher was parallelism and became a fan-out tool running four partner queries inside a "
           "single call. The planner was the agent itself. Only the reviewer survived as something "
           "separate, because independence is the entire mechanism of a checker. One agent, one "
           "fan-out tool, one function and one checker — **zero hand-offs against a hundred and "
           "five**. The line that mattered most went on the record underneath: an orchestrator when a "
           "single context exceeds the measured limit on multi-leg international cases, or when more "
           "than three partner calls must run in parallel and one tool cannot express it. Without a "
           "number in that sentence the swarm returns by default, and it returns with a reasonable "
           "explanation attached."},
 "pitfalls": [
   "Adding an agent for a reason that cannot be written as a limit with a number. *For speed* and "
   "*for separation of concerns* both survive a design review and neither can be tested at the plan "
   "gate, which is where the addition actually has to be caught.",
   "Buying parallelism with agents. Four partner searches run at once inside one fan-out tool with no "
   "hand-offs at all; as four agents they cost six hand-offs, a coordinator and four contexts.",
   "One process weight for the whole programme. Heavy ceremony on a one-line fix is twelve personas "
   "between an engineer and a change, and light ceremony on the audited module is the audit finding.",
 ],
 "done_when": "The record states a number of agents, the hand-off count that number implies, and a "
              "limit with a figure in it that would justify the next one.",
},
{
 "n": 5, "id": "decide", "phase": "Decide",
 "title": "Merge the utility trees, then write only the ADRs that earn one",
 "when": "Day nine, the ratification workshop, and the dated records that follow it",
 "purpose": (
   "Nine candidates, six people, two hours. Without the trees the room argues about words and runs "
   "out of time exactly on the contested items; with them, the uncontested NFRs go through in twenty "
   "minutes and the remaining hundred go to the conflicts, which are the only reason six people were "
   "needed at once. A conflict is not a difference of taste. It is a **priority gap of five or more "
   "between two stakeholders**, and each one owes a decision record. Records are written at "
   "trade-off points and nowhere else — forty records in a week buries the three that mattered."),
 "activities": [
   {"do": "Score every candidate on value and complexity, per stakeholder",
    "detail": "One to three on each, from each person's own point of view. The scoring is quick; the "
              "value is that two people who would have argued now disagree in a column you can read."},
   {"do": "Compute priority = value × (4 − complexity) and merge the trees",
    "detail": "The formula rewards high value at low difficulty, which is the order a workshop should "
              "actually take things in. Merging is what turns six opinions into one agenda."},
   {"do": "Mark every gap of five or more as a conflict",
    "detail": "Below five it is a difference of emphasis and the room will settle it in a minute. At "
              "five and above there is a genuine trade-off underneath, and that is what a record is "
              "for."},
   {"do": "Ratify the uncontested candidates first, as one block",
    "detail": "Six go through in twenty minutes because the trees already agree. Working down the "
              "list in order at thirteen minutes each runs out of time precisely on the conflicts."},
   {"do": "Name the sensitivity points and give each a date for its record",
    "detail": "A sensitivity point is rated high on both importance and difficulty: one design "
              "decision changes the outcome. Stop at the ratified list and in week three somebody "
              "re-opens the model tier with no record of why it was settled."},
   {"do": "Write a record only where there was a trade-off",
    "detail": "An ADR is earned by a decision that could reasonably have gone the other way. A record "
              "for every decision is the same as none, because the three that matter are unfindable."},
   {"do": "Run build, buy or borrow as a matrix, a three-year cost, a door and a flip test",
    "detail": "Weights come from the ratified NFRs, so you are not inventing them. Count the people "
              "and not just the licence, and assess whether the decision is a one-way door before you "
              "let the score decide."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Merge the stakeholder trees, compute every priority and produce the conflict list with "
           "the gaps. Tedious arithmetic across six people and nine candidates, done in seconds.",
    "caution": "Check the formula. It inverts 4 − complexity about as often as it gets it right, and "
               "an inverted priority column reverses the entire workshop agenda."},
   {"tool": "Claude Code",
    "use": "Build the decision matrix as a sheet with the weights and ratings in named cells, so the "
           "flip test is one keystroke rather than a paragraph of reasoning.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Draft the record from your bullet points, with the rejected options as a required "
           "section and the review date as a named trigger.",
    "caution": "Its rejected-options section flatters the decision you already made. Require each "
               "rejection to cite the score, the three-year cost or the door, and send it back when a "
               "rejection reads as a reason rather than a number."},
   {"tool": "Do not delegate",
    "use": "Choosing which decisions earn a record. That judgement is what keeps the folder readable, "
           "and a readable folder is the only kind a coding agent or a new joiner benefits from.",
    "caution": None},
 ],
 "artifact": {
   "name": "Ratified NFR sheet + the ADRs at the sensitivity points",
   "good": "Every ratified line carries a number, every sensitivity point carries a dated record, and "
           "every record names what it rejected together with the score that rejected it.",
   "owner": "Solution architect"},
 "template": {
   "title": "Ratification and the decision record", "lang": "markdown",
   "body": """# Ratification · <product> · <date>
_Workshop: <n> people, <n> candidates, two hours · Chair: <name>_

## Merged utility tree
> priority = value x (4 - complexity), each stakeholder scoring 1 to 3

| NFR | <frontline> | <compliance> | <finance> | <ops> | Gap | Conflict? |
|-----|------------|--------------|-----------|-------|-----|-----------|
| <latency 30s P95> | <6> | <2> | <2> | <4> | <4> | no |
| <cost per case $0.60> | <1> | <2> | <9> | <3> | <8> | **yes — ADR-<n>** |
| <accuracy 80% codeshare> | <9> | <6> | <2> | <6> | <7> | **yes — ADR-<n>** |
| <refunds over $400 approved> | <2> | <9> | <4> | <3> | <7> | **yes — ADR-<n>** |

**Rule:** a gap of 5 or more between any two stakeholders is a conflict, and every
conflict is a decision-record trigger.

**Not a real conflict, though it looks like one:** <auditability against latency —
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

**Options, weighted from the ratified NFRs** — score = sum(weight x rating), rated 1-3
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
"""},
 "prompts": [
   {"title": "Merge the utility trees and find the conflicts",
    "when": "You have every stakeholder's scores and the workshop is tomorrow",
    "body": """Merge these stakeholder utility trees and find the conflicts.

Each stakeholder scored each candidate NFR on business VALUE (1-3) and COMPLEXITY (1-3).

  priority = value x (4 - complexity)

OUTPUT SHAPE:
1. One table: a row per NFR, a column per stakeholder holding their priority, then a
   GAP column holding the largest difference between any two stakeholders.
2. SHOW THE ARITHMETIC for at least three rows, so I can check you have not inverted
   the formula.
3. CONFLICTS: every NFR whose gap is 5 or more. Each one owes a decision record.
4. FALSE CONFLICTS: pairs that look opposed and are not, with the reason. The usual
   example is auditability against latency — logging costs milliseconds and the model
   choice costs seconds.
5. A proposed agenda: the uncontested NFRs first as one time-boxed block, then the
   conflicts one at a time.

RULES:
- Do not average the stakeholders. The gap is the signal and an average destroys it.
- Do not reword anyone's NFR.
- If a stakeholder did not score an NFR, leave the cell blank. Never impute a score.

SCORES:
<paste>"""},
   {"title": "Score build, buy or borrow, and run the flip test",
    "when": "A framework or platform decision is on the table",
    "body": """Score this decision as a weighted matrix, then test how firm the answer is.

CRITERIA AND WEIGHTS — these come from my ratified NFRs. Do not change them:
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
- Where you do not know a number, write UNKNOWN and name who would have it."""},
   {"title": "Draft the ADR, with the rejections argued from the numbers",
    "when": "The decision is made and the record is what makes it stay made",
    "body": """Draft an architecture decision record from my notes below.

OUTPUT SHAPE — exactly these sections, in this order:
  Status (accepted or superseded, with the date and what it supersedes)
  Context (the trade-off that forced a decision, in three sentences)
  Decision (what we are doing, and the named review point)
  Consequence (what it costs now, and what it keeps open)
  Rejected (one entry per option, each carrying the NUMBER that rejected it)
  Flip test (which single input would have to move, and by how much)

RULES:
- The Rejected section is the part that matters and the part that gets written badly.
  Every rejection cites the matrix score, the three-year cost or the door. A rejection
  that reads as a preference is a failure — rewrite it, or tell me the number is missing.
- Do not flatter the decision. If an option scored within a point of the winner, that
  belongs in Context, not in Rejected.
- Keep it to one screen. A coding agent reads this in its context pack, which is exactly
  why it must be short and exact.
- The review point is a date or a named trigger, never "later".

MY NOTES:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · nine ratified, three records owed",
   "body": "The nine candidates went into a two-hour workshop with the trees already merged. Six were "
           "uncontested and were ratified in twenty minutes; the remaining hundred minutes went to "
           "the three conflicts, which were the only reason six people had been put in one room. "
           "**Nine ratified NFRs with three sensitivity points**, each given a date for its record "
           "rather than a promise. The conflict that turned up is the one that usually turns up — "
           "latency against cost per case, because the faster answer needs the larger model. "
           "**ADR-004** was the framework decision and it repays a second read: the weighted totals "
           "came out four points apart across three options, and buy and borrow tied at $360,000 over "
           "three years once the people were counted, which made the licence the small number all "
           "along. The matrix did not break the tie. The **door** did: borrow, behind an interface "
           "layer, with a named review at month twelve — two weeks of work now to keep a swap at "
           "weeks rather than quarters."},
 "pitfalls": [
   "A vote with sticky dots on a wall. The loudest group wins, cost per case collects two dots, and "
   "it comes back three months later as a crisis with an invoice attached to it.",
   "A record for every decision. Forty in a week and the three that mattered cannot be found; an ADR "
   "is earned by a trade-off, not by a meeting having happened.",
   "A record with no rejected options. It reads as a preference, and the first incident re-litigates "
   "it from the beginning because there is nothing on paper to defend.",
 ],
 "done_when": "Every ratified NFR carries a number, every sensitivity point carries a dated record, "
              "and every record names what it rejected with the score that rejected it.",
},
{
 "n": 6, "id": "bound", "phase": "Bound",
 "title": "Set the authority budget before the token budget",
 "when": "P1, before a single tool is written",
 "purpose": (
   "The first question is not how much the agent may spend. It is **what it may change, touch or "
   "commit.** A cheap task with too much authority is far more dangerous than an expensive one with "
   "none. The product manager decides where the allowed-alone line sits; your job is to make it "
   "enforceable, which means the cap lives in a tool signature and not in prompt text. **A prompt is "
   "a request. A tool contract is a boundary.** A model can be talked past a request; a typed "
   "parameter that raises cannot be talked past, whatever the model has been convinced of."),
 "activities": [
   {"do": "List every tool the agent can call, before anyone sizes its tokens",
    "detail": "Authority comes first because it is the thing a budget cannot fix. An agent with a "
              "small token allowance and a refund tool is the dangerous configuration."},
   {"do": "Band each tool R1 to R5 by what the action could damage",
    "detail": "Reversible draft, reversible change to real work, hard to reverse with a small blast "
              "radius, money or identity or policy, irreversible. The band belongs to the tool and is "
              "assigned once, so it is never argued per pull request."},
   {"do": "Move every cap into the tool signature and delete it from the prompt",
    "detail": "An injected instruction can override a sentence. It cannot override a typed parameter "
              "that raises. This is a morning's work and it is the highest-value morning in P1."},
   {"do": "Keep the sentence that explains the rule",
    "detail": "The prompt carries the policy and makes the agent behave well by default; the "
              "signature carries the enforcement and makes bad behaviour impossible. You want both, "
              "and confusing them is how a design lists five controls and enforces none."},
   {"do": "Mint the confirmation token outside the model's reach",
    "detail": "A token the model can produce is not a gate. Bind it to the booking, the amount and "
              "the approver, give it an expiry, and write the test that a forged or reused one "
              "raises."},
   {"do": "Tag every ingested text source untrusted, including partner APIs",
    "detail": "The partner is not attacking you; whoever can write into their free-text field might "
              "be. Trust is a property of the channel you control, not of the organisation at the "
              "other end of it."},
   {"do": "Classify every open decision hard or soft, then give the soft ones a placeholder",
    "detail": "Four questions and one *no* makes it hard. A soft gate with no stub or interface layer "
              "behind it is a hard gate nobody has admitted to, and the build queues anyway."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Band a tool list R1 to R5 with a reason per row and the control location named. A good "
           "first pass, and it is consistent in a way a room full of people is not.",
    "caution": "It bands by the size of the change. A one-line change to a refund cap is R4 — re-read "
               "every R1 and R2 that touches money, identity or a policy commitment."},
   {"tool": "Claude Code",
    "use": "Grep every prompt and tool description for currency symbols, *never*, *always*, *ask "
           "before* and *do not*, then have it write the enforced version and both tests for each hit "
           "that would cost money or be irreversible.",
    "caution": "A hit list is not a fix. Require the over-cap test and the no-confirmation test in "
               "the same pass, or the work stops at the list and the list gets stale."},
   {"tool": "Chat LLM",
    "use": "Run the four hard-or-soft questions over your open decisions and propose a placeholder "
           "for each soft one — a stub, an interface layer, a default tier behind a gateway.",
    "caution": "It marks almost everything soft, because everything looks reversible on paper. "
               "Question one is the one it answers too generously."},
   {"tool": "Do not delegate",
    "use": "Whether a wrong action can be undone, and how fast. That is a fact about your ledger, "
           "your regulator and your customers, and *we would notice* is not an answer to it.",
    "caution": None},
 ],
 "artifact": {
   "name": "Authority budget + gate map",
   "good": "Every tool banded, every cap in a signature with a test beside it, every money action "
           "with a named approver, and every open decision classified with a real placeholder behind "
           "the soft ones.",
   "owner": "Solution architect"},
 "template": {
   "title": "Authority budget and gate map", "lang": "markdown",
   "body": """# Authority budget and gate map · <feature>
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
"""},
 "prompts": [
   {"title": "Band a tool list by risk of action",
    "when": "You have the tool surface and no bands yet",
    "body": """Band every tool below on the R1-R5 ladder.

R1  reversible draft or sandbox — review at the end
R2  reversible change to real work — review before merge
R3  hard to reverse, small blast radius — approve first
R4  money, identity or a policy commitment — a NAMED approver, every time
R5  irreversible or safety-critical — not delegated at all

OUTPUT SHAPE, one table:
| Tool | Band | What ONE wrong call could damage | Where the control must live | The test that proves it |

RULES:
- Band by what the ACTION could damage, never by the size of the change. A one-line
  change to a refund cap is R4.
- The control column may not say "the prompt". It says: a typed parameter, a required
  confirmation token, a permission scope, or "no tool exists".
- Every R4 row names the approver role.
- Every R5 row says that no tool exists — not that the tool is discouraged.
- Flag any tool carrying a generic action parameter. One broad manage_<thing>(action)
  tool is accidental authority and must be split, because any path through it could
  cancel something.

TOOLS:
<paste the signatures, or the list with one line of description each>"""},
   {"title": "Move the caps out of the prompts, with the tests",
    "when": "Monday morning, on any repository with an agent in it",
    "body": """Search every prompt, system message and tool description in this repository for rules
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
  missing-confirmation case. Both assert that the call RAISES — never that the reply
  contains an apology, because wording changes with the next prompt edit.
- Do not remove the explanatory sentence from the prompt. Say which sentences to keep.
- Show me the search commands before the results."""},
   {"title": "Classify the open decisions hard or soft",
    "when": "The build is queuing behind a list of open questions",
    "body": """Classify each open decision below. Ask the four questions IN ORDER and stop at the
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
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · the cap that existed everywhere except the code",
   "body": "The engineer had wired the assistant to do everything, to show how capable it was. The "
           "authority budget put search and drafting at R1 and R2, cancelling a hold at R3, rebooking "
           "and refunds at R4 with a named approver, and changing a passenger identity at R5 with no "
           "tool existing at all. The **$400** from the day-six constraint register became a typed "
           "parameter on the refund signature, with two tests beside it. That is what the artefact "
           "said. On **day 82** a passenger received a **$2,000 refund** that was not owed, and the "
           "postmortem reconstructed the state exactly: with either the cap or the approver enforced "
           "the refund is impossible, so both were absent from the code. Five layers had been listed "
           "in the design and none was enforced. Two of them were written down — in the prompt — "
           "which is precisely why *we had a cap* felt true and was not."},
 "pitfalls": [
   "Sizing the check to the diff. A one-line change to a refund cap is the highest band there is, and "
   "*small changes do not need a gate* is the sentence that precedes most money incidents.",
   "A cap that lives in prompt text. It lowers a probability and closes no path, and it reads exactly "
   "like a control in a design review, which is the whole reason it is dangerous.",
   "Treating every open decision as hard. The build queues behind eleven questions that could each "
   "have run behind a stub, and the delay gets blamed on governance rather than on the classification.",
 ],
 "done_when": "A grep of every prompt returns no cap, no currency amount and no 'ask before', and "
              "each rule you removed has an over-cap or no-confirmation test standing in its place.",
},
]
