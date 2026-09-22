"""Product manager · steps 3-5."""

STEPS_B = [
{
 "n": 3, "id": "frame", "phase": "Frame",
 "title": "Size the value and set the autonomy",
 "when": "Before the budget conversation, and before anyone writes a prompt",
 "purpose": (
   "Two numbers come out of this step and both get argued about later, so derive them now. **Value** "
   "is arithmetic, not adjectives, and the honest version subtracts what it costs to run and what it "
   "costs to check. **Autonomy** is set per action and follows the cost of a mistake, never what the "
   "model is capable of. Get autonomy wrong and you are arguing about 'the assistant' for six weeks; "
   "get it right and the argument becomes a two-minute lookup."),
 "activities": [
   {"do": "Write the value line with real numbers",
    "detail": "cases × minutes saved × cost per minute, minus cases × run cost, minus the review load. "
              "Every term from the pain register. Nothing as an adjective."},
   {"do": "Get the run cost from engineering",
    "detail": "Tokens per case, cached and routed. Early on this is an estimate; ask for the estimate "
              "and the assumption behind it, and re-ask once there is a real per-call log."},
   {"do": "Add the review row, honestly",
    "detail": "What share of cases a human checks, and for how long. It is high in the first cycle and "
              "falls as the artefacts sharpen. Omitting it is what makes cycle two look like a "
              "regression when it is actually the recovery."},
   {"do": "List the feature's actions, not the feature",
    "detail": "Show options · rebook same-day · rebook across partners · issue a refund. Autonomy is "
              "per action. A product-level autonomy level forces everything to the strictness of the "
              "riskiest action or the looseness of the safest."},
   {"do": "Score each action on cost of a mistake and reversibility",
    "detail": "Reversibility is the hinge and the column that ends most arguments. Three executives "
              "stop disagreeing once the question is per action and the answer is derived."},
   {"do": "Set the level, and the evidence that would raise it",
    "detail": "Levels rise on evidence, one step at a time, and an incident usually drops one. Write "
              "the raising condition down now, while nobody is under pressure."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Give it the value-line formula and your numbers and have it produce the table plus a "
           "sensitivity view: which single input, if wrong by 20%, changes the answer most.",
    "caution": "Check every number it echoes back. Models are careless with arithmetic they were handed "
               "in prose; ask it to show the calculation, not just the total."},
   {"tool": "Claude Code",
    "use": "Have it build the value line as a small script or sheet with the assumptions as named "
           "variables, so finance can change one and watch the answer move.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Paste the action list and ask it to sort them by reversibility and name what a single wrong "
           "action costs. Useful as a first pass that you then correct.",
    "caution": "It does not know your refund policy or your regulator. Treat its cost estimates as "
               "prompts for your own thinking, never as inputs."},
   {"tool": "Do not delegate",
    "use": "The autonomy level itself. This is the decision that money and regulators hang off, and it "
           "is yours with your name on it.",
    "caution": None},
 ],
 "artifact": {
   "name": "Value line + autonomy decision record",
   "good": "A net number per day with every term shown, and a table of actions each with a level, a "
           "reversibility mark and the evidence that would raise it.",
   "owner": "Product manager"},
 "template": {
   "title": "Value line and autonomy record", "lang": "markdown",
   "body": """# Value and autonomy · <feature>
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
"""},
 "prompts": [
   {"title": "Build the value line, with sensitivity",
    "when": "You have the pain register numbers",
    "body": """Compute a value line from these inputs and SHOW THE ARITHMETIC at each step.

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
3. Tell me which single input is both high-impact AND least evidenced — that is the one
   I should go and measure before I present this."""},
   {"title": "Draft the autonomy table",
    "when": "You have the action list and need a first pass",
    "body": """Here are the actions <feature> can take: <list them>.

For each, produce a row:
| Action | What ONE wrong instance costs | Reversible? (yes / with effort / no) | Suggested level |

Levels, in order: acts alone · acts monitored · acts with a veto window · named approver
every time · not delegated at all.

Rules:
- Set the level from cost-of-mistake and reversibility ONLY. Ignore how capable the model is.
- Anything involving money, identity or a regulatory commitment defaults to "named approver".
- Anything irreversible defaults to "not delegated".
- Where you do not know our costs, write UNKNOWN — do not estimate.

Then list the questions I must answer before this table can be signed."""},
   {"title": "Pressure-test an autonomy level",
    "when": "Someone wants a level raised",
    "body": """An executive wants <action> raised from <level A> to <level B>, because
"it has been right every time for <period>".

Act as a sceptical risk reviewer. Tell me:
1. What sample size would be needed to support that claim, given the bar for this action?
   (bar = damage / (damage + saving); show the arithmetic)
2. What the lower bound of the observed success rate actually is at the sample size we have.
3. What is the DOOR — if we raise it and it goes wrong, how fast can we go back?
4. The smallest safe step: what is the ONE level up, with what monitoring?

Our numbers: <cases in period>, <errors>, <damage per wrong>, <saving per right>."""},
 ],
 "example": {
   "title": "SkyWays · the table that ended the argument",
   "body": "Three executives were arguing about how much the assistant should do. One wanted drafting "
           "only, one wanted automatic rebooking, one wanted refunds too. The argument ran for two weeks "
           "because it was about *the assistant*. Recast as four actions with a reversibility column, it "
           "took twenty minutes: options act alone, same-day rebooking acts monitored, cross-partner "
           "gets a veto window, refunds get a named approver every time. Nobody had to lose, because "
           "nobody had been arguing about the same thing."},
 "pitfalls": [
   "A value line with an adjective in it. *Significantly faster* cannot be defended when the token bill "
   "lands, and the token bill always lands.",
   "Setting autonomy from model capability. The question is never what it can do; it is what a mistake "
   "costs and whether you can undo it.",
   "Omitting the review row to make cycle one look better. Cycle two then looks like a regression, and "
   "you spend the meeting explaining an artefact of your own reporting.",
 ],
 "done_when": "Finance can change one assumption in your value line and see the answer move, and every "
              "action has a level that somebody derived rather than preferred.",
},
{
 "n": 4, "id": "specify", "phase": "Specify",
 "title": "Write the spec a machine can build from",
 "when": "P1, before the first bolt is cut",
 "purpose": (
   "A thirty-page PRD is read by nobody and interpreted differently by everyone, and when handed to a "
   "coding agent it produces the wrong thing confidently. The spec is the one place the machine can "
   "look, so it must be exact and small: three classical fields plus five agentic ones, on one screen. "
   "The five agentic fields are almost always the decisions nobody had made — which is the real value "
   "of the exercise, not the document."),
 "activities": [
   {"do": "Keep the three classical fields",
    "detail": "Title, value, acceptance. These do not change and the PRD already has them."},
   {"do": "Add the five agentic fields",
    "detail": "The model's role · autonomy · the bar per slice · the fallback · the records it must "
              "write. Each has an owner: autonomy is yours, the bar is yours with QA, the fallback is "
              "the architect's, the records are the architect's."},
   {"do": "Write acceptance in EARS, not prose",
    "detail": "WHEN a trigger AND a condition THE SYSTEM SHALL a behaviour, within a measure. Every "
              "'should' in your criteria is a place the agent will invent something."},
   {"do": "Add a BOUNDARY line per thing that must never happen",
    "detail": "Negative requirements are invisible to a model unless stated. *Never issue a refund "
              "without a named approver* is a boundary, and it also becomes a test."},
   {"do": "Derive the bar per slice",
    "detail": "bar = damage / (damage + saving), per kind of case. A single bar for the whole feature "
              "is how the hard slice ships broken while the easy one waits."},
   {"do": "Shard the PRD rather than delete it",
    "detail": "The thirty pages stay as the source. Use a cheap model to cut them into per-feature "
              "specs. The PRD is for humans and history; the spec is for building."},
   {"do": "Run the reading test",
    "detail": "Hand the eight fields to someone who was not in the room and ask them to build it. "
              "Every question they ask is a field you have not finished."},
 ],
 "ai": [
   {"tool": "Chat LLM (cheap tier)",
    "use": "Shard a long PRD into per-feature eight-field specs. This is the single highest-leverage "
           "delegation in the role: mechanical, verifiable, and it takes you an hour by hand.",
    "caution": "It will fill the five agentic fields with plausible guesses. Blank them out and decide "
               "each one yourself — the guesses are the exact thing you are trying to surface."},
   {"tool": "Chat LLM",
    "use": "Convert prose acceptance criteria to EARS and report how many 'should's it removed. The "
           "count is a useful measure of how much ambiguity you were shipping.",
    "caution": "Check that every SHALL ends in a measure. It will happily produce a clean EARS sentence "
               "with no number in it."},
   {"tool": "Chat LLM, adversarially",
    "use": "The reading test, cheaply: 'you are a coding agent, build this, and list every assumption "
           "you had to make'. Its assumption list is your gap list.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The bar and the autonomy fields. Both are business risk decisions with your name on them, "
           "and both have a formula — use the formula, not the model.",
    "caution": None},
 ],
 "artifact": {
   "name": "Eight-field spec + acceptance bar sheet",
   "good": "One screen. A coding agent builds from it unaided, and the QA lead can write tests from it "
           "without asking you a question.",
   "owner": "Product manager"},
 "template": {
   "title": "The eight-field agentic spec", "lang": "markdown",
   "body": """# Spec · <feature>
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
| <refund> | $<n> | $<n> | <n>% | yes — <what the hold is> |

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
"""},
 "prompts": [
   {"title": "Shard a PRD into eight-field specs",
    "when": "You have a long PRD and need per-feature specs",
    "body": """Below is a product requirements document.

Split it into one spec per feature. For each, output EXACTLY these eight fields:
1 Title
2 Value
3 Acceptance criteria — in EARS: WHEN <trigger> AND <condition> THE SYSTEM SHALL
  <behaviour> WITHIN <measure>. Plus BOUNDARY lines for anything that must never happen.
4 The model's role
5 Autonomy
6 The bar, per slice
7 Fallback
8 Records

CRITICAL: for fields 4-8, write "NOT DECIDED — <the question that must be answered>"
wherever the PRD does not actually say. Do NOT infer, do NOT use a sensible default.
Those gaps are the output I am looking for.

PRD:
<paste>"""},
   {"title": "Prose to EARS, with a ambiguity count",
    "when": "Your criteria are full of 'should'",
    "body": """Rewrite these acceptance criteria in EARS.

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
<paste>"""},
   {"title": "The reading test, as an agent would fail it",
    "when": "Before you hand the spec to engineering",
    "body": """You are a coding agent. You will build EXACTLY what this spec says and nothing
more. You cannot ask questions.

1. List every assumption you would have to make to start building.
2. For each, say what you would most likely assume, and what the cost would be if that
   assumption were wrong.
3. Point at the single sentence in the spec most likely to be interpreted two ways, and
   give me both readings.
4. Tell me which of the eight fields is weakest.

Do not build anything. Do not suggest improvements. Just show me where I was vague.

SPEC:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · thirty pages to eight fields",
   "body": "The PRD was thirty pages and the spec was one screen. Three fields transferred straight "
           "across. Of the five agentic fields, **five were undecided** — nobody had said what the "
           "model's role was versus the fare engine's, what autonomy refunds had, what accuracy counted "
           "as good, what happened when it could not decide, or what had to be logged. Each was settled "
           "with its owner in under an hour. The document took a morning; the decisions it forced were "
           "the point. The one that mattered most was the fallback: without it, the engineer would have "
           "chosen one by default, because the code has to do something."},
 "pitfalls": [
   "Letting the model fill the five agentic fields. Its guesses are plausible and they are exactly the "
   "decisions you were trying to surface.",
   "A single bar for the whole feature. The easy slice waits while the hard slice ships below its bar, "
   "and the average hides both.",
   "Deleting the PRD. It is the source you shard from and the record of why; the spec is the thing you "
   "build from. They do different jobs.",
 ],
 "done_when": "A coding agent and the QA lead both read the spec the same way, and neither has to ask you "
              "a question to start.",
},
{
 "n": 5, "id": "plan", "phase": "Plan",
 "title": "Plan in bolts, not sprints",
 "when": "P1 to P2, once the spec is signed",
 "purpose": (
   "When building is fast, the unit of planning shrinks to match. The agent builds a story in hours and "
   "then waits nine days for a sprint review, while leadership wants evidence daily. A **bolt** is a "
   "thin, shippable slice reviewed and integrated the same day. Same ten working days; evidence on all "
   "ten instead of a demo on the fourteenth, and a wrong turn costs one day rather than two weeks."),
 "activities": [
   {"do": "Cut the sprint's stories into daily slices",
    "detail": "Each must be shippable alone. Five stories usually become eight to twelve bolts, and the "
              "ones that will not split are the ones hiding two risks."},
   {"do": "Put the walking skeleton on day one",
    "detail": "The thinnest end-to-end path with no model in it. It proves the pieces connect, which is "
              "the assumption every other bolt rests on, and it costs half a day."},
   {"do": "Give each bolt exactly one unknown",
    "detail": "Then a day can fail for one reason and you know which. Two unknowns in a bolt means a "
              "day spent bisecting rather than building."},
   {"do": "Hand the cut to the architect for dependency order",
    "detail": "You decide the cadence; they decide the order. This division matters — a plan ordered by "
              "business priority will schedule a gated write before the plug it needs."},
   {"do": "Put the shadow run in the plan as a milestone",
    "detail": "Not a launch date. A window with a threshold. Fixing it now stops it being negotiated "
              "away later, when a date is under pressure."},
   {"do": "Move the demo to every day",
    "detail": "Leadership asked for visibility, and a daily merged slice is better visibility than a "
              "rehearsed fortnightly demo."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Give it the stories and ask for a bolt cut with a 'depends on' column and one unknown per "
           "bolt. It is good at spotting the story that contains two risks.",
    "caution": "It will not know your integration realities. The dependency column it produces is a "
               "draft for the architect, not a plan."},
   {"tool": "Claude Code",
    "use": "Have it topologically sort the bolts from the depends-on column and refuse cycles. A cycle "
           "always means a mis-cut, so the failure is the finding.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Draft the story file for tomorrow's bolt from the spec: context by reference, EARS slice, "
           "tools, tests, done-when, cost. Mechanical work, done well.",
    "caution": "It will paste context rather than reference it. Insist on links to the context layers, "
               "or the story file becomes forty thousand tokens."},
   {"tool": "Do not delegate",
    "use": "Which slice ships first. That is a business call about where the value and the risk are, and "
           "under a deadline it is the whole decision.",
    "caution": None},
 ],
 "artifact": {
   "name": "Bolt plan",
   "good": "One line per bolt with its single unknown, its dependency, and its day. The walking skeleton "
           "is on day one, and nothing is scheduled before the thing it needs.",
   "owner": "Product manager, with the architect on ordering"},
 "template": {
   "title": "Bolt plan", "lang": "markdown",
   "body": """# Bolt plan · <feature> · <cycle>
_Cadence: one bolt per day, reviewed and integrated same day_

| Day | Bolt | The ONE unknown it retires | Depends on | Slice it serves | Done when |
|-----|------|---------------------------|-----------|-----------------|-----------|
| 1 | Walking skeleton — <read X, show it>, no model | do the pieces connect? | — | all | end to end, in staging |
| 2 | <exact function> | <...> | — | <slice> | unit tests green |
| 3 | | | | | |

## Rules for this plan
- A bolt that cannot be built alone was cut wrong — send it back before starting it.
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
"""},
 "prompts": [
   {"title": "Cut stories into bolts",
    "when": "You have a sprint backlog and need daily slices",
    "body": """Cut these stories into bolts. A bolt is a thin slice that can be built, tested and
integrated in ONE day, ALONE.

For each bolt give me:
| Bolt | The ONE unknown it retires | Depends on | Can it be built alone? |

Rules:
- If a bolt would retire two unknowns, split it.
- If a bolt cannot be built alone, say so and explain what it needs.
- Put a walking skeleton first: the thinnest end-to-end path with NO model in it.
- Pure deterministic code (calculations, validations) should come early — it stands alone.
- Anything that writes or changes real data comes after the integration it depends on.

Finally: list any story that resisted splitting, and say what two risks it is hiding.

STORIES:
<paste>"""},
   {"title": "Draft tomorrow's story file",
    "when": "The bolt is chosen and engineering needs a self-contained brief",
    "body": """Write an agent-ready story file for this bolt. It must be buildable with NO chat
history and NO access to me.

Sections, exactly:
## Context — LINKS ONLY to the context layers and ADRs. Do not paste their contents.
## Spec — the EARS criteria for THIS slice only, copied from the spec verbatim.
## Tools — signatures the bolt may call, with their risk band.
## Tests — the golden slice it must pass and its bar, plus unit assertions.
## Done when — one testable line.
## Cost — expected tokens per call and the tier.

BOLT: <name and the one unknown>
SPEC EXTRACT: <paste the relevant EARS lines>
CONTEXT LAYERS: <paths>"""},
 ],
 "example": {
   "title": "SkyWays · ten days, ten proofs",
   "body": "The sprint held five stories and a demo on day fourteen. Recut, it became ten bolts. Day one "
           "was a walking skeleton that read a booking and displayed it — no model, half a day, and it "
           "found a credentials problem in the reservation adapter that would otherwise have surfaced on "
           "day nine. Day two was the fare-difference function, unit tested, standing alone. The first "
           "model call did not appear until day four, by which point everything it depended on was "
           "proven. The wrong turn that cycle cost one day."},
 "pitfalls": [
   "Ordering by business priority. That is the right way to choose what is in the plan and the wrong way "
   "to sequence it; the architect's dependency order is what makes each day buildable.",
   "A bolt with two unknowns. When the day fails you spend the next one bisecting, which is the cost the "
   "whole practice exists to avoid.",
   "Letting the shadow run become a date. It is a window with a threshold; as a date it will lose the "
   "argument to the launch the first time they conflict.",
 ],
 "done_when": "Every bolt in the plan can be built on its scheduled day without waiting for anything, and "
              "the walking skeleton is on day one.",
},
]
