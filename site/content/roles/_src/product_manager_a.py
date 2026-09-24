"""Product manager · steps 1-4. Imported by build_content.py."""

HEAD = {
    "id": "product-manager",
    "name": "Product manager",
    "short": "PM",
    "accent": "#3E6B8A",
    "tagline": "From a vibe to a number you can defend",
    "arc": ["Discover", "Qualify", "Frame", "Specify", "Plan", "Gate", "Launch", "Learn"],
    "intro": [
        "Your job has not changed. **What** and **why** are still yours, and nobody else in the room "
        "can decide them. What changes is that the thing you write is now read by a machine that "
        "cannot ask you what you meant, and that part of your product is right *a share of the time* "
        "rather than always.",
        "Those two facts ripple through every step below. A vibe becomes a measurement because the "
        "machine downstream cannot interpret a vibe. A success criterion becomes a number per slice "
        "because 'it works' is no longer a yes or a no. And a launch becomes a shadow run because you "
        "cannot reason your way to knowing whether it agrees with the humans it is replacing.",
        "Eight steps. Each one ends in an artefact somebody else needs, with the template to write it "
        "and the prompts to draft it faster.",
    ],
    "owns": [
        "The **intent** gate — is this worth doing at all?",
        "The **release** gate — is it safe to show real users?",
        "The **plan** gate, shared with the architect",
        "The autonomy level per action, and the door it sits behind",
        "The acceptance bar per slice, derived rather than guessed",
        "The two-number report to whoever funds this",
    ],
    "not_yours": [
        "**Behaviour** and **expansion** gates — those are the QA lead's, and your name on them helps nobody",
        "Pull request approvals you cannot evaluate",
        "Model choice, temperature, framework — behaviours are yours, knobs are engineering's",
        "The golden set's contents — you set the bar, QA curates the cases",
    ],
    "ai_stance": (
        "Use a model for the **drafting and the arithmetic**, never for the judgement. It can turn six "
        "interview transcripts into a deduplicated pain register in a minute, and it will happily "
        "invent a value line if you let it. The pattern that works: you bring the numbers and the "
        "decision, the model brings the structure and the first draft, and every artefact leaves your "
        "hands having been read by you. Where a step below says *do not delegate*, that is a judgement "
        "the model has no standing to make."
    ),
    "reads": [
        ["The wiki page for this role", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Product-Manager"],
        ["The same case as thirteen episodes", "../simulator/#/story"],
        ["Every formula on one page", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators"],
    ],
}

STEPS_A = [
{
 "n": 1, "id": "discover", "phase": "Discover",
 "title": "Turn the vibe into a measurement",
 "when": "Week one, before anyone designs anything",
 "purpose": (
   "Requests arrive as vibes. *Make rebooking smarter.* You cannot size a vibe, prioritise it, or hand "
   "it to a machine. This step converts it into four facts — who has the pain, how often, what it "
   "costs today, and the evidence — and everything downstream refers back to that line. It is the old "
   "product discipline, now mandatory, because the machine downstream cannot ask you what you meant."),
 "activities": [
   {"do": "Find who actually holds the pain",
    "detail": "Not the person who raised the request. The frontline agent, the contact-centre lead, the "
              "passenger. Ask each of them to describe the last time it happened, not the general case."},
   {"do": "Count it",
    "detail": "Cases per day or per week. If nobody knows, that is the first finding, and ops can "
              "usually produce it in an afternoon from a ticket export."},
   {"do": "Cost it",
    "detail": "Minutes per case × loaded cost per minute, plus anything that leaks — a lost passenger, "
              "a goodwill credit, an SLA breach. Cost per case is the number you will be asked for and "
              "the one nobody has."},
   {"do": "Find the evidence",
    "detail": "A ticket export, a call recording, a queue chart. One artefact a sceptic can open. An "
              "anecdote is not evidence; an anecdote with a number behind it is."},
   {"do": "Write the one-line statement",
    "detail": "Who · how often · what it costs · the evidence. One line. If it takes a paragraph, you "
              "have two pains and should split them."},
   {"do": "Refuse to open a spec until the line exists",
    "detail": "This is the discipline the step really is. Everything after this refers back to it, so a "
              "missing line becomes a missing justification at the funding conversation."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Paste six interview transcripts and ask for the distinct pains with the speaker beside each. "
           "It is very good at deduplicating what six people said in five different ways.",
    "caution": "Ask it to keep the speaker's name on every line. Merged-without-attribution is how a "
               "stakeholder later says they were never heard."},
   {"tool": "Claude Code",
    "use": "Point it at a ticket export and have it produce the counts: cases per week, median handling "
           "time, the tail. It writes and runs the script, so you get the number and the method.",
    "caution": "Read the script. A count over the wrong date column is confidently wrong."},
   {"tool": "Spreadsheet + LLM",
    "use": "Have it build the cost-per-case arithmetic as a sheet with the assumptions in named cells, "
           "so a sceptic can change one and watch the answer move.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "Deciding which pain is worth solving. The model will rank by how vividly it was described, "
           "which correlates with who is most articulate, not with what it costs.",
    "caution": None},
 ],
 "artifact": {
   "name": "Pain register",
   "good": "One line per pain, each with a name, a frequency, a cost and a link to the evidence. Sorted "
           "by cost, not by who asked. Readable in thirty seconds.",
   "owner": "Product manager"},
 "template": {
   "title": "Pain register", "lang": "markdown",
   "body": """# Pain register · <product>
_Last updated: <date> · Owner: <name>_

| # | The pain, in one line | Who holds it | Frequency | Cost today | Evidence |
|---|----------------------|--------------|-----------|-----------|----------|
| 1 | <Who> cannot <do what>, so <consequence> | <role, named person> | <n/day> | <$n per case · $n/yr> | [<source>](<link>) |
| 2 | | | | | |

## How cost per case was computed
- Handling time: <n> min, from <source>
- Loaded cost per minute: $<n>, from <source>
- Leakage per failed case: $<n> — <what leaks, and how it was estimated>
- **Cost per case = $<n>**

## What is NOT in here
- <pains raised that were out of scope, and why — so nobody re-raises them>

## Open numbers
| Missing | Who can produce it | By when |
|---------|--------------------|---------|
| <e.g. leakage rate> | <ops lead> | <date> |
"""},
 "prompts": [
   {"title": "Deduplicate discovery notes, with credit",
    "when": "After the interviews, before you write the register",
    "body": """You are helping a product manager consolidate discovery notes.

Below are <n> interview transcripts about <problem area>.

Produce a table with one row per DISTINCT pain:
| Pain, in one sentence | Everyone who raised it (names) | Their exact words (shortest quote) | Frequency mentioned | Cost mentioned |

Rules:
- Keep EVERY name. If four people said the same thing, all four names go on that row.
- Do not merge two pains that have different causes, even if they have the same symptom.
- If a frequency or cost was not mentioned, write "not stated" — never estimate.
- At the end, list separately: things stated as solutions rather than pains.

TRANSCRIPTS:
<paste>"""},
   {"title": "Turn a vibe into a measured statement",
    "when": "You have one request and no numbers",
    "body": """A stakeholder asked for: "<the vibe, verbatim>"

Act as a sceptical product manager. Do NOT propose a solution.

1. Rewrite it as: WHO has the pain · HOW OFTEN · WHAT IT COSTS today · EVIDENCE.
2. For each of the four, mark it KNOWN or UNKNOWN based only on what I gave you.
3. For every UNKNOWN, write the single question I should ask, and who is most likely to
   have the answer.
4. Tell me which ONE unknown, if it came back badly, would kill this request. Ask that first.

Context I have: <paste what you know>"""},
   {"title": "Cost-per-case arithmetic from a ticket export",
    "when": "You have data and need the number defensible",
    "body": """I have a ticket export at <path>. Columns: <list them>.

Write and run a script that reports:
- tickets per week for the last 12 weeks, and the trend
- median and p90 handling time, for <category> only
- the share that were reopened or escalated
- cost per case = median handling minutes x $<rate>/min

Then print the assumptions you made as a list, and flag any column you had to
interpret. Show me the script before the numbers — I need to check the date column
and the category filter."""},
 ],
 "example": {
   "title": "SkyWays · day one",
   "body": "The request was *make rebooking smarter*. After two days it read: **Disrupted passengers wait "
           "an average of 38 minutes for a rebooking decision; 240 cases a day; 11% are codeshare, which "
           "no simple rule can handle; measured cost $9.40 per case from the Q2 ticket export.** "
           "That single line survived to the steering committee on day 90, because every later artefact "
           "pointed back at it. The 38 minutes became the latency NFR, the 240 became the denominator of "
           "the value line, and the 11% became the slice that carried the whole risk."},
 "pitfalls": [
   "Writing the pain as a missing feature. *We need an AI assistant* is a solution, and it forecloses the "
   "cheaper answer before anyone has looked.",
   "Accepting 'everyone knows it is slow'. If nobody will name a number, the honest register entry is the "
   "number as UNKNOWN with a named owner and a date, not a guess dressed up as a finding.",
   "Counting the saving and not the leak. The passenger who left is usually worth more than the minutes.",
 ],
 "done_when": "Someone who was not in any of the interviews can read one line and tell you what the problem "
              "is, how big it is, and where the number came from.",
},
{
 "n": 2, "id": "qualify", "phase": "Qualify",
 "title": "Decide whether this is AI at all",
 "when": "Immediately after the register, before any design",
 "purpose": (
   "Leadership says agent-first. Half of what you are asked to build is a rule, and a rule done by a "
   "model is slower, dearer and less correct than a rule done by code. Three questions settle it, in "
   "order, and the recorded answer is what lets you say no with evidence instead of as an opinion. "
   "Expect two or three of your top five to come back as rules. That is the healthy result."),
 "activities": [
   {"do": "Ask: is there a genuine judgement call?",
    "detail": "Something where two competent humans could reasonably differ. If the criteria are "
              "published and unambiguous, it is a rule, and code does rules perfectly and provably."},
   {"do": "Ask: is the volume high enough?",
    "detail": "A probabilistic system carries fixed costs — evaluation, gates, a harness. Below some "
              "volume a person is simply cheaper, and saying so is a service to everyone."},
   {"do": "Ask: is a wrong answer recoverable?",
    "detail": "If not, a person stays in the loop. This is not a maturity level you grow out of; it is a "
              "property of the action."},
   {"do": "Classify into one of four builds",
    "detail": "Rule (code) · assisted (model drafts, person decides) · agentic with gates · fully "
              "agentic. Most real features are the middle two."},
   {"do": "Write the verdict with its comparison line",
    "detail": "Record what you rejected and why. That line is your argument the next time the directive "
              "arrives, and it saves you re-running the analysis from memory."},
   {"do": "Take it to the architect before design starts",
    "detail": "The verdict fixes the shape of the product. Changing it later means starting again, which "
              "is exactly why it is a hard gate."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Run the three questions against a backlog in bulk. Give it the three questions and ten "
           "items, and ask for a verdict plus the one sentence justifying each.",
    "caution": "It will be generous. It wants things to be AI. Re-read every YES on question one and ask "
               "yourself whether the criteria are actually published somewhere."},
   {"tool": "Chat LLM, adversarially",
    "use": "Ask it to argue the opposite: 'make the strongest case that this is a rule, not a model'. "
           "The strongest case against is the cheapest review you will get.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The recoverability answer. Whether a wrong action can be undone is a fact about your "
           "business, your regulator and your customers, and the model does not know any of them.",
    "caution": None},
 ],
 "artifact": {
   "name": "AI-fit decision record",
   "good": "One row per candidate, three answers, a verdict, and the rejected alternative. Signed and "
           "dated. Short enough that leadership reads it.",
   "owner": "Product manager"},
 "template": {
   "title": "AI-fit decision record", "lang": "markdown",
   "body": """# AI-fit · <feature>
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
- **Rule in code** — <rejected because ... / chosen because ...>
- **A person** — <cost at this volume>
- **Fully agentic** — <rejected because step <x> is unrecoverable>

## Consequence
- The unrecoverable steps are: <list> — these are gated regardless of how good the model gets.
- Revisit when: <named trigger, e.g. "the regulator's rule changes" — not a date>
"""},
 "prompts": [
   {"title": "Triage a backlog for AI fit",
    "when": "You have ten requests and an agent-first directive",
    "body": """For each item below, answer these three questions IN ORDER and stop at the first "no":

1. Is there a genuine judgement call — could two competent people reasonably differ?
   (If the criteria are published and unambiguous, answer NO: it is a rule.)
2. Is the volume high enough to justify evaluation, gates and a harness?
3. Is a wrong answer recoverable?

Then classify: RULE (code) / ASSISTED (model drafts, person decides) / AGENTIC WITH GATES /
FULLY AGENTIC.

Output a table: Item | Q1 | Q2 | Q3 | Verdict | One-line justification.

Be strict on Q1. Most backlog items are rules. If you are unsure, answer NO and say what
would have to be true for it to be a judgement call.

ITEMS:
<paste>"""},
   {"title": "Argue the opposite",
    "when": "Before you commit to an agentic verdict",
    "body": """I have concluded that <feature> should be built as <verdict>.

Make the strongest possible case that I am wrong and it should instead be <the cheaper
alternative: a rule in code / a person>.

Be specific and concrete. Use my own numbers below. Where my reasoning depends on an
assumption I have not evidenced, name it.

End with: the single piece of evidence that would settle this either way.

MY REASONING:
<paste the record>"""},
 ],
 "example": {
   "title": "SkyWays · the verdict that shaped everything",
   "body": "Judgement: yes — which alternative suits this passenger depends on their connection, their "
           "fare rules, whether they will accept an overnight. Volume: 240 a day. Recoverable: "
           "**partly** — a proposed rebooking can be withdrawn, a cash refund cannot. So the verdict was "
           "*agentic with gates*, and the gate went on the refund. That single 'partly' is why the "
           "product has a named approver on refunds ninety days later, and why the $2,000 incident on "
           "day 82 was a failure to implement a decision already made rather than a failure to make it."},
 "pitfalls": [
   "Treating the directive as the answer. *Everything must be agent-first* is a strategy, not a design "
   "input, and the AI-fit record is how you serve the strategy honestly rather than theatrically.",
   "Answering question three with 'we would notice'. Noticing is not recovering. The test is whether the "
   "action can be undone, and how fast.",
   "Recording the verdict without the rejected options. A verdict with no alternatives reads as a "
   "preference and gets re-litigated at the first incident.",
 ],
 "done_when": "You can hand the record to a sceptical executive and they can see what you decided, what "
              "you rejected, and what would change your mind — without you in the room.",
},
]
