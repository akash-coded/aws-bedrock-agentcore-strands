"""Solution architect · steps 1-3. Imported by build_content.py."""

HEAD = {
    "id": "solution-architect",
    "name": "Solution architect",
    "short": "SA",
    "accent": "#7A6A46",
    "tagline": "From requirements to a system that holds",
    "arc": ["Elicit", "Constrain", "Map", "Shape", "Decide", "Bound", "Detail", "Evolve"],
    "intro": [
        "The method has not changed. You still run discovery, sort constraints before you ratify "
        "anything, write quality requirements as scenarios, build utility trees, record the "
        "decisions that involved a trade-off, and review a design against artefacts rather than "
        "against a diagram. Twenty years of craft carries straight over, and the part that carries "
        "over is most of the job.",
        "What changes is that some of the steps you are designing are **probabilistic**, and a "
        "probabilistic step needs a different kind of proof. An exact step is proven by a unit test "
        "that is green or red. A best-guess step is proven by a measured share on real cases. A step "
        "that changes something real is proven by a confirmation the model cannot mint. Deciding "
        "which is which, before anyone builds, is the artefact this role is really for.",
        "Eight steps, from the first discovery meeting to the incident that redesigns the system. "
        "Each ends in something engineering, QA or the product manager needs, with the template to "
        "write it and the prompts to draft it faster.",
    ],
    "owns": [
        "The **ratified NFRs**, their sensitivity points, and the workshop that produces them",
        "The **exact / best-guess / consequential map**, and the proof each kind needs",
        "The shape — how many agents, and the named limit that would justify another one",
        "The **authority budget** and the gate map: every cap in a tool signature",
        "The architecture decision records, one per trade-off point and nowhere else",
        "The **plan gate**, shared with the product manager, and the drift tests at every bolt",
    ],
    "not_yours": [
        "The **intent** and **release** gates — those are the product manager's, and your name on "
        "them dilutes the two you do hold",
        "Temperature, top-p, framework version, SDK call shape — you specify behaviours, engineering "
        "picks the knobs, and a knob in a design document is wrong at the next release",
        "The golden set's contents and the judge rubric — QA curates the cases, you place the checker",
        "Which pain is worth solving, and what a mistake costs the business",
    ],
    "ai_stance": (
        "Use a model where the work is **mechanical and checkable**, and nowhere near the trade-offs. "
        "It will turn two transcripts into a credited requirement register, rewrite nine adjectives as "
        "six-part scenarios, grep a repository for arithmetic hiding in prompts, and draft an MCP "
        "schema from an API surface — all of it faster than you and none of it beyond your ability to "
        "verify. It will also band a money tool R2 because the diff is one line, put everything in the "
        "shared context layer, and write an ADR whose rejected-options section flatters the decision "
        "you already made. Where a step below says *do not delegate*, the reason is always the same: "
        "the answer is a fact about your business, your regulator or your risk appetite, and the model "
        "has no way to know any of them."
    ),
    "reads": [
        ["The wiki page for this role", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Solution-Architect"],
        ["The same case, step by step, in the simulator", "../simulator/#/sa/step-1"],
        ["Every decision tree on one page", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Decision-Trees"],
    ],
}

STEPS_A = [
{
 "n": 1, "id": "elicit", "phase": "Elicit",
 "title": "Run two discovery meetings and credit every line",
 "when": "Days one to four, before anybody writes a quality target",
 "purpose": (
   "Six people have a say, and putting all six in one room first is the mistake. You get the same "
   "thirty-one requirements, forty minutes of two of them talking past each other, and less goodwill "
   "than you started with. Two meetings split by proximity to the work get you the same lines with "
   "the goodwill intact, because the second meeting exists for whoever was not in the first. Then the "
   "discipline the rest of the role rests on: **credit before you consolidate.** A voice that was "
   "dropped comes back in week five as a constraint, and by then it arrives as a change request."),
 "activities": [
   {"do": "Split discovery in two, by proximity to the work",
    "detail": "The three most senior give you cost and control and no frontline view; the three "
              "closest to the work give you speed and systems and no compliance view. Either order "
              "works. What does not work is one room of six."},
   {"do": "Read every requirement back, with the name attached",
    "detail": "Eleven minutes for thirty-one lines. The duplicates get read out four times and nobody "
              "objects, because each of the four belongs to somebody sitting there."},
   {"do": "Refuse to consolidate on the whiteboard",
    "detail": "Live consolidation produces twelve clean lines and two people who spend the project "
              "believing theirs was deleted. Consolidation is an editing job and it belongs in the "
              "email, where the reasoning can sit beside it."},
   {"do": "Send all the lines, credited, duplicates kept",
    "detail": "The consolidation goes underneath with its rationale. Sending only the twelve saves one "
              "page and costs an afternoon of replies, all asking the same question."},
   {"do": "Flag the requirements that describe a model's behaviour",
    "detail": "Usually three of them. They cannot be satisfied by a function, and their acceptance "
              "will be a measured share rather than a pass or a fail — so the shape is settled here "
              "instead of argued in the sprint that has to test them."},
   {"do": "Write down who was not in either room",
    "detail": "Name them, name the constraint they hold, and book the meeting. An unheard stakeholder "
              "is a late constraint, and a late constraint re-opens NFRs that were already ratified."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Paste both transcripts and ask for one row per distinct requirement with every speaker's "
           "name on it. It is very good at noticing that four people described one thing four ways.",
    "caution": "It merges and drops attribution by default. Require a name on every line, then check "
               "the count: distinct rows plus duplicates should equal what you actually heard."},
   {"tool": "Claude Code",
    "use": "Have it hold the register as a file — id, verbatim line, person, meeting — and generate "
           "the consolidation map from it, so the email is produced rather than retyped.",
    "caution": "Make it assert that every source requirement appears in exactly one consolidated "
               "line. A requirement that appears in none is the one that comes back in week five."},
   {"tool": "Chat LLM (cheap tier)",
    "use": "Separate the requirements from the things that are not requirements: motivations, "
           "solutions and preferences. Three piles, and only one of them belongs in the email.",
    "caution": "It accepts a solution as a requirement when it is phrased as one. Re-read every line "
               "that names a technology; almost none of them are requirements."},
   {"tool": "Do not delegate",
    "use": "The read-back itself. The mechanism is a person hearing their own words said aloud with "
           "their name attached, and there is no version of that a model performs on your behalf.",
    "caution": None},
 ],
 "artifact": {
   "name": "Credited requirements email",
   "good": "Every line as it was raised, credited, duplicates intact, with the consolidation and its "
           "reasoning underneath. A stakeholder finds their own words in under ten seconds.",
   "owner": "Solution architect"},
 "template": {
   "title": "Credited requirements email", "lang": "markdown",
   "body": """# Requirements identified by the team and key stakeholders
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

## Conflicts — for the workshop, not for an editor
| ID | Requirement A | Requirement B | Who holds each | Workshop item |
|----|--------------|---------------|----------------|---------------|
| X-1 | <FR-07, faster options> | <FR-22, lower cost per case> | <name> / <name> | <date> |

## The requirements that describe a model's behaviour
These cannot be satisfied by a function. Their acceptance will be a measured share
on real cases, not a pass or a fail, and they are flagged now so that nobody writes
their acceptance criteria in the wrong shape.
- FR-<n> — <why two competent people could differ>

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
credited to the wrong person — that correction is free now and expensive in week five.
"""},
 "prompts": [
   {"title": "Consolidate two discovery transcripts, credit intact",
    "when": "After the second meeting, before you write the email",
    "body": """You are helping a solution architect consolidate two discovery meetings about
<problem area>.

OUTPUT SHAPE — one markdown table, one row per DISTINCT requirement:
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

TRANSCRIPT 1 — <who was in the room>:
<paste>

TRANSCRIPT 2 — <who was in the room>:
<paste>"""},
   {"title": "Build the consolidation map, and prove it is complete",
    "when": "You have the full credited list and need the short one",
    "body": """Here is the full credited requirement list: <paste>.

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
  both names. That is a workshop item, not an editing decision."""},
   {"title": "Find the requirements that describe a model's behaviour",
    "when": "Before the constraint review, so acceptance is shaped correctly",
    "body": """Below is a consolidated functional requirement list: <paste>.

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
list has not been consolidated tightly enough."""},
 ],
 "example": {
   "title": "SkyWays · thirty-one lines from six people",
   "body": "Day one, the three closest to the work: seventeen requirements, eleven of them about "
           "speed and the systems the assistant would have to touch, and no compliance view at all. "
           "Day two, the other three, opening with a credited read-back of day one: fourteen more, "
           "nine about cost and control. **Thirty-one lines from six people**, four of which were the "
           "same requirement said four ways. The read-back took eleven minutes and every duplicate "
           "was read out with its author's name on it. The email went on day four with all thirty-one "
           "lines and the consolidation to twelve underneath. Nobody replied asking where their "
           "requirement had gone. One line — *every refund must be attributable to a person*, from "
           "compliance — became the $400 cap two days later, and it was on the list only because "
           "somebody who was not in the first meeting was invited to the second."},
 "pitfalls": [
   "Putting all six in one room to save a meeting. You get the same thirty-one requirements, forty "
   "minutes of the compliance officer and the frontline agent arguing, and nobody feeling heard.",
   "Consolidating live, in front of everyone. The whiteboard version looks efficient and it produces "
   "two stakeholders who believe their requirement was deleted, which surfaces as resistance later.",
   "Sending only the consolidated list. It saves one page and costs an afternoon of replies, and "
   "every reply is the same question about where a line went.",
 ],
 "done_when": "Any of the six can open the email, find their own words verbatim with their name "
              "beside them, and follow the line to the consolidated requirement it became.",
},
{
 "n": 2, "id": "constrain", "phase": "Constrain",
 "title": "Sort the constraints, then write every NFR as a scenario",
 "when": "Days six to nine, and never after ratification",
 "purpose": (
   "A constraint can make a quality target impossible, so constraints come first — and they are "
   "sorted **by type**, because the type decides what each one does to the design. A technical "
   "constraint reshapes the integration, a regulatory one becomes a number inside a tool signature, "
   "and a commercial one bounds the tier you may choose. Only then the quality requirements, written "
   "as six-part scenarios, because an adjective cannot be tested, ranked or traded off. Two of them "
   "are the ones teams forget to write and then need: the **autonomy level** and the **cost per "
   "case**."),
 "activities": [
   {"do": "Sort every constraint into technical, regulatory or commercial",
    "detail": "The type is not a filing convenience. Regulatory becomes a typed parameter, technical "
              "forces an adapter or a server in front of something, commercial bounds the model tier "
              "and therefore the latency you can promise."},
   {"do": "Strike the motivations that are pretending to be constraints",
    "detail": "*No headcount this year* does not bound the design; it is the reason the assistant "
              "exists, and it belongs in the pain register. The test is whether the line names a "
              "design it rules out."},
   {"do": "Turn each regulatory constraint into a number and a place",
    "detail": "Refunds over $400 need a named approver is a number and a location — a typed "
              "parameter and a token the model cannot mint. Left as a sentence it stays a sentence, "
              "and a sentence is what a postmortem finds missing."},
   {"do": "Write every candidate NFR in six parts",
    "detail": "Source, stimulus, artefact, environment, response, measure. The part everyone omits is "
              "environment — under what load, at what hour, in what degraded state — and its absence "
              "is precisely what makes a latency target arguable for two hours."},
   {"do": "Add autonomy level and cost per case to the candidate list",
    "detail": "Both are quality attributes and both are measurable. A ratified cost per case is what "
              "makes an unexpected bill a monitored number with an alert rather than a surprise "
              "arriving four weeks late."},
   {"do": "Ground every measure in something real before the workshop",
    "detail": "Pull the current P95 from the request log. A measure invented in the room is ratified "
              "in the room and missed in production, and nobody can say when it became unachievable."},
   {"do": "Hold the constraint review before anything is ratified",
    "detail": "Ratify first and add constraints after, and the room signs a latency target the legacy "
              "adapter cannot meet. Then the workshop is held twice, with the same six people."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Have it rewrite adjective-shaped requirements as six-part scenarios, with a line under "
           "each naming which of the six parts the original did not contain.",
    "caution": "The missing-parts line is the output that matters. Without it, it invents a plausible "
               "environment clause and you ratify a condition nobody agreed to."},
   {"tool": "Claude Code",
    "use": "Point it at the request log and have it report the current P95, the peak hour and the "
           "shape of the tail, so the measure in the scenario is grounded in today's behaviour.",
    "caution": "Read the query. A P95 across all hours is not the P95 the scenario is about, and the "
               "gap between the two is usually the entire argument."},
   {"tool": "Chat LLM (cheap tier)",
    "use": "Sort a raw constraint dump into technical, regulatory and commercial, and flag every line "
           "that does not bound the design.",
    "caution": "It files organisational motivations under commercial because they mention money. "
               "Re-read that pile asking of each line: what design does this rule out?"},
   {"tool": "Do not delegate",
    "use": "Deciding whether a constraint is real. The only way to learn that a $400 threshold is a "
           "policy your compliance officer can change, rather than a regulation, is to ask her.",
    "caution": None},
 ],
 "artifact": {
   "name": "Constraint register + candidate NFR scenarios",
   "good": "Every constraint typed and naming a design it rules out, and every candidate NFR in six "
           "parts with a number in the measure and a source for that number.",
   "owner": "Solution architect"},
 "template": {
   "title": "Constraint register and candidate NFRs", "lang": "markdown",
   "body": """# Constraints and candidate NFRs · <product>
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

_Measure grounded in:_ <request log, <date> — today's P95 is <n>s>
_Constraint it must respect:_ <C-2 — the adapter adds <n>s>

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
"""},
 "prompts": [
   {"title": "Adjective to six-part scenario",
    "when": "You have a list of quality requirements and none of them can be tested",
    "body": """Rewrite each quality requirement below as a six-part scenario.

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
  normal load" — that is the invented clause that gets ratified and then argued about
  for the rest of the project.
- The MEASURE must carry a statistic: P95, per case, per week, percentage of a named
  slice. "Fast" and "under 30 seconds" are both unfinished, for different reasons.

Finish with two lists: measures not stated, and environments not stated. Those two
lists are what I take back to the people who raised the requirements.

REQUIREMENTS:
<paste>"""},
   {"title": "Sort a constraint list, and test every line",
    "when": "You have a dump of constraints from four sources",
    "body": """Sort the lines below into TECHNICAL, REGULATORY, COMMERCIAL or NOT A CONSTRAINT.

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
<paste>"""},
   {"title": "Write the two NFRs everyone forgets",
    "when": "Your candidate list is complete and you suspect it is not",
    "body": """I am writing candidate NFRs for <feature>. I have <n> so far, listed below.

Write exactly two more, as six-part scenarios, and only these two:
1. AUTONOMY LEVEL — what the system may do without a person, per action.
2. COST PER CASE — the run cost of one completed case, across every model call.

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
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · the sentence that should have been a signature",
   "body": "Day six, the constraints went up sorted by type. Regulatory: **every refund over $400 "
           "needs a named approver**, and *passenger data stays in region*. Technical: the "
           "reservation system exposes SOAP only, which decided the integration shape before anyone "
           "argued about it. Commercial: a licence ceiling that later became a weight in the "
           "build/buy/borrow matrix. One line — *no headcount this year* — was struck as a motivation "
           "and moved to the pain register. Nine candidates went into the workshop as six-part "
           "scenarios, and two of them, **autonomy level** and **cost per case at $0.60**, were on "
           "the list only because someone asked what was missing. The $400 was a number from day six. "
           "It was still only a number in a document on day 82, when a $2,000 refund went out with "
           "neither the cap nor the approver anywhere in the code — which is a failure of step six, "
           "not of this one, and the difference is worth being precise about."},
 "pitfalls": [
   "Ratifying the NFRs and adding the constraints afterwards. The room signs a latency target the "
   "legacy adapter cannot meet, and the whole workshop is held a second time.",
   "An NFR that is an adjective. *Fast*, *reliable* and *secure* survive the workshop because nobody "
   "can disagree with them, and then they cannot be tested, ranked or traded against anything.",
   "Leaving cost per case off the candidate list. It is the quality attribute that arrives as an "
   "invoice, and a number nobody ratified is a number nobody monitors.",
 ],
 "done_when": "Every candidate NFR has all six parts with a statistic in the measure and a source for "
              "that number, and every line on the constraint register names a design it rules out.",
},
{
 "n": 3, "id": "map", "phase": "Map",
 "title": "Tag every step exact, best-guess or consequential",
 "when": "P0, the first design artefact, and it takes an hour for one feature",
 "purpose": (
   "The product manager sorted the feature — this is a judgement, this is arithmetic. That is right "
   "and it is not enough. You sort at the level of **every step**, and you add the column that "
   "decides both what gets built and how it gets proven. Exact steps are functions proven by a unit "
   "test. Best-guess steps are model calls proven by a measured share on real cases. Consequential "
   "steps are a tool plus a gate, proven by a required confirmation. Choosing the kind of evidence "
   "each step will need, before anybody builds it, is what the artefact is for."),
 "activities": [
   {"do": "List steps, not features",
    "detail": "Read the booking, find candidates, compute the fare difference, check eligibility, "
              "draft the message, rebook, refund. Seven rows for one feature is normal, and the rows "
              "are where the design actually lives."},
   {"do": "Tag each step exact, best-guess or consequential",
    "detail": "Exact means right every single time. Best-guess means right a share of the time. "
              "Consequential means it changes something real, and a step is often consequential as "
              "well as one of the other two rather than instead of it."},
   {"do": "Fill the proof column before anything else",
    "detail": "A unit test, a measured share on a named slice, or a required confirmation. Engineering "
              "builds from the kind column and QA builds their test plan from the proof column, which "
              "is what makes an hour's work worth an hour."},
   {"do": "Draw the data flow and mark where numbers cross",
    "detail": "Numbers flow from an exact step into a best-guess one and never the other way. Drawing "
              "the arrows is how you find the step that computes a value and then acts on it."},
   {"do": "Apply the rule that never breaks",
    "detail": "The best-guess machine never does the exact math. The model may call the function and "
              "read the result; it never computes the value it then acts on. A fluent wrong number is "
              "the failure no prompt-level test catches — $80 when the ledger says $62."},
   {"do": "Grep the prompts for calculate, compute and total",
    "detail": "Each hit is a function waiting to exist. It takes ten minutes and it is the most "
              "reliably productive ten minutes available to this role."},
   {"do": "Hand the map to QA as their test plan",
    "detail": "The proof column is already the shape of their work: which steps need assertions, "
              "which need a golden slice with a bar, and which need a confirmation test that fails "
              "closed."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Give it the step list and the three definitions and ask for a tagged table with the proof "
           "column filled. A good first pass on an unfamiliar feature, and it surfaces steps you had "
           "quietly folded together.",
    "caution": "It under-uses **consequential**. Re-read every row: anything that writes, sends, "
               "books, cancels or moves money is consequential whatever else it also is."},
   {"tool": "Claude Code",
    "use": "Have it search the repository — prompt files, system messages, tool descriptions, long "
           "string literals — for arithmetic verbs and currency symbols, and list every hit with its "
           "file and line.",
    "caution": "It matches vocabulary, not intent. *Tell the passenger what they owe* is arithmetic in "
               "a prompt and contains none of the words you searched for."},
   {"tool": "Chat LLM, adversarially",
    "use": "Ask it to find the step that is doing two things at once. A step you cannot classify is "
           "almost always a judgement and a calculation bundled into one call, and both halves "
           "classify immediately once they are separated.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "Deciding what counts as money. Whether a fee waiver, a goodwill credit or a seat upgrade "
           "is a consequential action is a fact about your business, and the model guesses from the "
           "wording of the step.",
    "caution": None},
 ],
 "artifact": {
   "name": "Exact / best-guess / consequential map",
   "good": "One row per step with its kind, its owner and its proof. Engineering can see what to write "
           "in code, QA can see what to test and how, and every number the feature computes sits on "
           "the code side of the line.",
   "owner": "Solution architect"},
 "template": {
   "title": "Exact / best-guess / consequential map", "lang": "markdown",
   "body": """# Exact / best-guess / consequential map · <feature>
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
"""},
 "prompts": [
   {"title": "Tag a feature's steps, with the proof column",
    "when": "You have the step list and need the map in front of engineering today",
    "body": """Tag every step of this feature. Use exactly three kinds.

EXACT — must be right every single time. Built as a function. Proven by a unit test.
BEST-GUESS — right a share of the time. Built as a model call. Proven by a measured
  share on real cases.
CONSEQUENTIAL — changes something real. Built as a tool PLUS a gate. Proven by a
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
<paste>"""},
   {"title": "Find the arithmetic hiding in the prompts",
    "when": "Monday morning, on any repository that already has an agent in it",
    "body": """Search this repository for arithmetic that lives in a prompt instead of in code.

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
  look in."""},
   {"title": "Split the step that does two things",
    "when": "One step will not classify and the map is stuck on it",
    "body": """This step resisted classification as exact, best-guess or consequential:

<paste the step, and how it is currently described or prompted>

A step that cannot be classified is almost always doing two things at once: a
judgement and a calculation, or a judgement and a write.

1. Name the two things it is doing.
2. Split it into two steps and classify each.
3. For the exact half, write the function signature — name, typed parameters, return
   type — and the one unit test that would prove it.
4. For the best-guess half, write what it is deciding in one sentence, and the slice
   its measured share would be reported on.
5. State what may pass between them, and in which direction.

If it genuinely is one thing, say so, tell me which kind it is, and tell me why the
classification felt hard — that reason is usually itself a finding."""},
 ],
 "example": {
   "title": "SkyWays · the row that was worth the hour",
   "body": "Seven steps, three kinds. Reading the booking, checking visa and codeshare eligibility "
           "and computing the fare difference came out **exact** — lookups and rules, proven by unit "
           "tests. Ranking the alternatives and drafting the passenger message came out "
           "**best-guess**, proven by a measured share with the codeshare bar at 80%. Rebooking the "
           "seat and issuing a refund came out **consequential**: a tool plus a gate, proven by a "
           "confirmation. The row that paid for the whole artefact was the fare difference. It had "
           "been sitting inside a prompt as *work out what they owe*, and a prompt that computes "
           "money produces $80 when the ledger says $62 — fluently, with no error and no red test. "
           "Ten minutes of grepping found two more like it in the same feature."},
 "pitfalls": [
   "Tagging at the level of the feature. *The rebooking assistant is best-guess* is true and useless; "
   "the fare difference inside it is exact, and that single row is why the map exists.",
   "A prompt that computes a number the agent then acts on. It fails fluently, with no exception and "
   "no red test, and the first person to notice is the passenger reading the wrong figure.",
   "Filling the kind column and leaving the proof column for later. Later is the sprint where QA asks "
   "what good looks like for step four, and the answer gets invented under deadline pressure.",
 ],
 "done_when": "Every step has a kind and a proof, and a grep of the prompts for arithmetic verbs and "
              "currency symbols returns nothing whose value the agent then acts on.",
},
]
