"""Engineering lead · head and steps 1-3. Imported by build_content.py."""

HEAD = {
    "id": "engineering",
    "name": "Engineering lead",
    "short": "ENG",
    "accent": "#2F6B57",
    "tagline": "From a story file to a shipped bolt",
    "arc": ["Prepare", "Slice", "Floor", "Layer", "Gate", "Harness", "Ship", "Operate"],
    "intro": [
        "Your tests, your reviews and your releases all still exist. What changes is that part of "
        "the system is right *a share of the time*, so 'it works' stops being a yes or a no and "
        "becomes a number per slice — and the boundary that stops the thing doing harm has to live "
        "in your code, because **a prompt is a request and a tool contract is a boundary**.",
        "Two habits carry most of the difference. Everything the agent needs arrives in a **file it "
        "can read** — a context file at session start, a story file per bolt — rather than in a chat "
        "thread nobody can diff or re-run. And the work is split before it is written: exact work is "
        "a function with a unit test, best-guess work is a model call with a measured share, and the "
        "best-guess machine never does the exact math.",
        "Eight steps, in the order you would actually do them. Each one ends in something that lives "
        "in the repository: a file, a function, a signature, a workflow, a log. If a step's artefact "
        "is not in git, the step did not happen.",
    ],
    "owns": [
        "The **context file** every coding tool reads, and the story file every bolt is built from",
        "The **deterministic floor** — every number that gets acted on is a function with a test",
        "The **boundary**: caps and confirmation tokens in tool signatures, never in prompt text",
        "The eval harness in CI, and the per-slice rule that blocks a merge",
        "The build order within the architect's dependency sequence, integrated the same day",
        "The effort-and-token ledger the product manager's cost number is built from",
    ],
    "not_yours": [
        "The **bolt cut** itself — the architect decides the cut; you decide whether each one can be "
        "built alone, and say so before you start it",
        "The **acceptance bar** per slice — the PM derives it from damage and saving. You make it run",
        "The golden set's contents and the judge's rubric — those belong to the QA lead",
        "The cut-over and the widening — you build the flag and rehearse the rollback; the PM throws it",
    ],
    "ai_stance": (
        "Use a model for **the typing and the sweep**, never for the boundary. It will write a correct "
        "`fare_difference()` faster than you can, and it will just as happily write a cap into a prompt "
        "and report the cap as done. The pattern that works: the model drafts *inside* something you "
        "wrote — a context file, a story file, a signature you already fixed — and every line that "
        "moves money, changes a booking or writes a trace row is read by a person before it merges. "
        "Where a step below says *do not delegate*, the model has no standing, and it is almost always "
        "because the decision is about what the code must **refuse** rather than what it should do."
    ),
    "reads": [
        ["The wiki page for this role", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Engineering-Lead"],
        ["The same case, walked step by step", "../simulator/#/eng/step-1"],
        ["Where the bill goes, and how to get it back", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill"],
    ],
}

STEPS_A = [
{
 "n": 1, "id": "prepare", "phase": "Prepare",
 "title": "Write the context file every coding tool reads",
 "when": "Day one on the repository, before the first agent session",
 "purpose": (
   "Every AI coding tool reads a file from the repository before it does anything, and most teams "
   "have not written one. It is an hour of work and the single biggest quality lever you have, "
   "because it is the only instruction that reaches every session, every engineer and every tool "
   "without anyone remembering to type it. Write it once, point it at the context layers rather than "
   "copying them, and grow it by adding the rule that bit you last week."),
 "activities": [
   {"do": "Find out which file each of your tools actually reads",
    "detail": "Claude Code reads `CLAUDE.md` as project memory, committed to git, with enterprise "
              "policy above it and a user-level file for personal preferences. Copilot reads "
              "`.github/copilot-instructions.md` plus scoped `.github/instructions/*.instructions.md`. "
              "Codex CLI reads `AGENTS.md`. Cursor reads `.cursor/rules/*.mdc`."},
   {"do": "Weight the two kinds differently",
    "detail": "Copilot's file steers inline suggestions; Claude Code's drives autonomous actions. The "
              "same sentence about never editing an applied migration is advice in the first case and "
              "a standing instruction in the second, so write the never-touch list for the second."},
   {"do": "Write four sections and nothing else",
    "detail": "Stack, conventions, commands, never-touch. Anything longer stops being read — by the "
              "model, because the rules are diluted, and by the engineer who is supposed to maintain "
              "it. Under a hundred lines is a working target."},
   {"do": "Point at the context layers, never copy them",
    "detail": "`/context/shared/standards.md` by path, not pasted. A copy is a fork: the security rule "
              "changes in the shared layer and the agent carries on quoting last quarter's version "
              "back at the team that wrote it."},
   {"do": "Make every command one you have actually run",
    "detail": "A command that does not exist is worse than no command. The agent improvises a "
              "plausible one, reads the error as an environment problem, works around it, and you "
              "review a diff resting on a green that never happened."},
   {"do": "Grow it with the rule that bit you last week",
    "detail": "Every time, one line, dated at the bottom. That is the whole maintenance policy and it "
              "is the only one that survives a busy quarter. Review the diff like code, because it is."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Point it at the repository and ask for a first draft from what is actually there — the "
           "build files, the test runner, the directory layout. It reads the tree faster than you do "
           "and it gets the stack section right.",
    "caution": "Make it run every command it proposes and paste the output into the session. Left "
               "alone it will write `npm test` into a Python repository because the shape of the file "
               "suggests a line like that belongs there."},
   {"tool": "An editor agent (Copilot, Cursor)",
    "use": "Have it derive the scoped instruction files per path from the one project file, so the "
           "narrow rules about `src/tools/**` sit next to the narrow code they govern.",
    "caution": "Scoped files multiply. Keep one owner and one review, or within a month you have six "
               "of them quietly contradicting each other and no way to tell which one won."},
   {"tool": "A cheap tier",
    "use": "Feed it last month's pull request review comments and ask which corrections repeat. The "
           "repeats are your missing conventions, already evidenced and already argued.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The never-touch list. It is a statement about what your organisation cannot afford to "
           "lose, and every line on it is there because of an incident the model has never seen.",
    "caution": None},
 ],
 "artifact": {
   "name": "Context file set",
   "good": "One project file per tool, all pointing at the same context layers, all committed. Four "
           "sections, under a hundred lines, and a dated line at the bottom recording the last rule "
           "that was added and why.",
   "owner": "Engineering lead"},
 "template": {
   "title": "CLAUDE.md · the project context file", "lang": "markdown",
   "body": r"""# CLAUDE.md · <repo name>
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
"""},
 "prompts": [
   {"title": "Draft the context file from the repository itself",
    "when": "Hour one on a repository that has none",
    "body": r"""You are writing the project context file that every coding agent on this
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

OUTPUT: the file, then the command output, then a list of your INFERRED lines."""},
   {"title": "Mine the review history for the rules you are missing",
    "when": "You have a context file and want the next four lines of it",
    "body": r"""Below are the review comments left on merged pull requests over <n> weeks.

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
<paste>"""},
   {"title": "Audit the context file you already have",
    "when": "The file exists, and sessions still go wrong in the same ways",
    "body": r"""Here is our context file: <paste>. Here is the repository layout: <paste>.

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
Do not rewrite the whole file. I want the diff, not a replacement."""},
 ],
 "example": {
   "title": "SkyWays · the two rules that were added in the first month",
   "body": "The first `CLAUDE.md` was twenty-two lines written in an hour: stack, four commands that "
           "had been run, and a never-touch list with `migrations/` on it. It grew twice. Once after "
           "an agent re-implemented the fare arithmetic inline rather than calling "
           "`fare_difference()` and returned $80 where the ledger said $62 — the line added was "
           "*never compute money in a prompt; call the function*. Once after a session switched model "
           "mid-task and the cache hit ratio collapsed, which added *one model per task*. Two "
           "sentences, and neither failure has recurred. That is the whole evidence the file needs."},
 "pitfalls": [
   "Writing it once and never again. A context file that has not changed in three months describes a "
   "repository that no longer exists, and the agent is following it confidently.",
   "Pasting the shared standards into it instead of linking them. The copy goes stale the first time "
   "the standard changes, and the agent then argues with your security team using your own old words.",
   "Listing commands nobody has run. The agent improvises a plausible substitute, treats the failure "
   "as an environment problem, and you end up reviewing a diff built on a green that never happened.",
 ],
 "done_when": "A new engineer, or a fresh agent session, can clone the repository, run every command "
              "in the file, and have all of them work without asking anybody a question.",
},
{
 "n": 2, "id": "slice", "phase": "Slice",
 "title": "Build from a story file, never a chat thread",
 "when": "The evening before each bolt, once the architect has cut it",
 "purpose": (
   "A bolt that needs a chat thread was cut wrong, or its file is incomplete, and either way that is "
   "a finding rather than an inconvenience. The story file is one self-contained file with six parts, "
   "versioned beside the code it produces: context **by reference**, the spec in EARS, the tools with "
   "their risk bands, the tests, the done-when, and the cost. Because it is a file it is reviewable "
   "as a diff and re-runnable next month. It is BMAD's *shard* and spec-driven development's unit at "
   "once."),
 "activities": [
   {"do": "Write the context section as paths, never as pastes",
    "detail": "`/context/domain/booking-model.md`, ADR-004, ADR-007. A pasted document is forty "
              "thousand tokens per call and, reliably, a worse answer than the slice would have "
              "given, because the relevant lines are now buried in material the model has to rank."},
   {"do": "Put the spec in EARS, with the boundary on its own line",
    "detail": "WHEN <trigger> AND <precondition> THE SYSTEM SHALL <response> WITHIN <limit>. Then "
              "BOUNDARY as a separate line, because that is the sentence that becomes a raise in the "
              "signature two steps from now rather than a hope in a paragraph."},
   {"do": "List the tools with the band from the authority budget",
    "detail": "`rebook(pnr, segment, fare_delta, confirmation) → R3`. The band comes from the budget, "
              "never from the author, and it decides how many people have to read the pull request."},
   {"do": "Name both kinds of test, by name",
    "detail": "The golden slice with its case count and its bar, and the unit tests spelled out: "
              "`rebook_requires_fare_delta`, `rebook_is_idempotent`. Named now, they get written. "
              "Described now, they get skipped and nobody can point at the moment it happened."},
   {"do": "Write the done-when so a machine can turn it red",
    "detail": "Harness green on the named slice, integrated to main, one trace row written. Three "
              "checkable things. 'Works as described' is not a done-when, it is a hope with a tick "
              "box next to it."},
   {"do": "Estimate the tokens per call and the tier",
    "detail": "Roughly 1,900 tokens, mid tier. It is an estimate and it is still worth writing, "
              "because the first bolt whose real number is triple its estimate is exactly where you "
              "find the document somebody pasted."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Give it the bolt's one-line description, the ADR numbers and the authority budget, and "
           "have it assemble the six sections. The mechanical part — resolving paths, copying the "
           "signature, pulling the band — is exactly what it is good at.",
    "caution": "It will produce a spec sentence containing 'appropriately' or 'correctly'. Every one "
               "of those words is a decision nobody has made; strike it and write the number."},
   {"tool": "A chat surface",
    "use": "Paste a prose paragraph from the product manager and ask for it back as EARS, with the "
           "trigger, the precondition, the response and the limit as separate clauses.",
    "caution": "Check the precondition. Models drop the AND clause more often than any other part, "
               "and the dropped clause is usually the one that stops an action happening before a "
               "number exists."},
   {"tool": "A cheap tier",
    "use": "Have it diff yesterday's story file against what actually merged and list the sections "
           "the file got wrong. That diff is how the template stops being aspirational.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The BOUNDARY line. It is the one sentence in the file that says what the system must "
           "refuse, and it is written by the person who will be accountable when it does not.",
    "caution": None},
 ],
 "artifact": {
   "name": "Agent-ready story file",
   "good": "One file, six sections, no repository pastes. An engineer can build the bolt from it with "
           "the chat window closed, and a reviewer can see every decision in it as a diff.",
   "owner": "Engineering lead"},
 "template": {
   "title": "Story file · one bolt", "lang": "markdown",
   "body": r"""# Bolt <7> · <rebook() gated write>
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
"""},
 "prompts": [
   {"title": "Assemble the story file for tomorrow's bolt",
    "when": "The evening before, once the architect has the cut",
    "body": r"""Assemble a story file for one bolt. Six sections, in this order:
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
ADRs AND CONTEXT PATHS: <paste>"""},
   {"title": "Turn prose into EARS without losing a clause",
    "when": "The spec arrived as a paragraph",
    "body": r"""Rewrite the requirement below in EARS.

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
<paste>"""},
   {"title": "Find what the file is missing, before building anything",
    "when": "First thing on the build day",
    "body": r"""Here is the story file for today's bolt: <paste>.

DO NOT WRITE ANY CODE. Do not start.

List every question you would have to ask me in order to build this bolt without
further conversation. For each question:
- which section of the file should have answered it
- what you would assume if nobody answered
- whether that assumption could move money, change a booking, or write a trace row

Then answer one thing: can this bolt be built and tested ALONE, with nothing that is
scheduled for a later day? If not, name exactly what is missing and stop.

Every question on your list is a defect in the file, not in me. I am going to fix the
file, and then you are going to build from it with this conversation closed."""},
 ],
 "example": {
   "title": "SkyWays · the file that let the chat window stay shut",
   "body": "Bolt seven was `rebook()`. Its first story file pasted the booking model — nine hundred "
           "lines — into the context section. That session cost three times its estimate and produced "
           "a function that re-derived the fare delta rather than taking it as a parameter. The second "
           "version replaced the paste with two paths and added one BOUNDARY line: *never rebook "
           "without a computed fare difference*. That line became a raise in the signature the same "
           "afternoon, `rebook_requires_fare_delta` went red and then green, and the bolt integrated "
           "before five. The test of a story file is not whether it reads well. It is whether the chat "
           "window can stay shut."},
 "pitfalls": [
   "Pasting the repository into the context section. It costs forty thousand tokens a call and returns "
   "a worse answer, because the slice that mattered is now buried in material the model has to rank.",
   "A spec sentence containing 'appropriately', 'correctly' or 'as needed'. Each one is a decision "
   "nobody has made, and it will be made by the model, silently, at about two in the afternoon.",
   "Keeping the chat thread as the real source and the file as documentation. The thread cannot be "
   "diffed, reviewed or re-run, so the second engineer builds a different bolt from the same file.",
 ],
 "done_when": "An engineer who was not in the planning conversation can build the bolt from the file "
              "alone, with the chat history closed, and the reviewer can see every decision as a diff.",
},
{
 "n": 3, "id": "floor", "phase": "Floor",
 "title": "Write the deterministic floor before any prompt",
 "when": "The first coding day of each bolt",
 "purpose": (
   "Every number the feature computes and then acts on is a function, unit-tested, and never a "
   "prompt. This is the rule in the role with no exceptions, because a model doing arithmetic fails "
   "**fluently**: it returns $80 where the ledger says $62, with no error, no stack trace and nothing "
   "unusual in the wording, and the first person to notice is the customer. Walk the architect's "
   "exact/best-guess map and write a signature and one assertion for every step marked exact. It is "
   "the cheapest code in the build and it is the code that holds."),
 "activities": [
   {"do": "Walk the architect's map line by line",
    "detail": "Every step marked **exact** becomes a function name before any of them becomes a body. "
              "The map already did the sorting; your job is to refuse to let a single exact step stay "
              "inside a prompt because it looked like one sentence."},
   {"do": "Write the signature and one assertion before the body",
    "detail": "One assertion per exact step, taken from the spec rather than from what the code "
              "happens to do, and watched going red. A test written after the implementation is a "
              "test of the implementation."},
   {"do": "Use exact types for money",
    "detail": "`Decimal`, never `float`. Round once, at a named boundary, with the rounding mode "
              "stated in the code. A good share of fare disputes in any airline system are two "
              "systems rounding differently and both being certain."},
   {"do": "Grep the prompts for calculate, compute, total, sum",
    "detail": "Every hit is a function waiting to exist. Run it over the prompt directory rather than "
              "the code, run it again after every prompt change, and make it a two-line CI check so "
              "the sweep does not depend on anyone remembering."},
   {"do": "Give the model the function, never the arithmetic",
    "detail": "It calls `fare_difference()` and reads the result. Expose it as a tool with a narrow "
              "signature so there is nothing else it could plausibly do with the numbers it has."},
   {"do": "Keep the floor out of the harness",
    "detail": "Exact code is proven by unit tests that are green or red, not by a measured share. If "
              "a fare function is being scored at 97% somebody has put it on the wrong side of the "
              "line, and 3% of the money is quietly in scope."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Hand it the spec clause and the signature and let it write the body and the table-driven "
           "cases. Exact code from a written rule is the work models do best, and the unit test tells "
           "you within seconds whether it worked.",
    "caution": "Write the first assertion yourself. A model that writes both the code and its tests "
               "will make them agree with each other and disagree with the spec, and the suite goes "
               "green on the wrong behaviour."},
   {"tool": "An editor agent",
    "use": "Ask for the edge cases you did not list: zero, negative, identical fares, currency "
           "mismatch, a segment already flown. It is reliably better than a tired person at "
           "enumerating boundaries.",
    "caution": "It enumerates, you decide. Half its cases are behaviours you deliberately put out of "
               "scope, and writing tests for those freezes decisions nobody ever made."},
   {"tool": "A cheap tier",
    "use": "Run the calculate/compute/total sweep across the prompt directory and return the "
           "candidate functions with the offending prompt line beside each. A sweep, not a judgement.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "Deciding that something is exact. That call comes from the architect's map and from "
           "whether the number gets acted on; a model asked the question answers from how the "
           "sentence is phrased.",
    "caution": None},
 ],
 "artifact": {
   "name": "Exact-code inventory, implemented",
   "good": "One row per exact step with a function name, a test name and a green tick, and nothing "
           "left in the prompts that produces a number anybody acts on.",
   "owner": "Engineering lead"},
 "template": {
   "title": "The deterministic floor, and the test that comes first", "lang": "python",
   "body": r"""# src/exact/fare.py — the deterministic floor for <bolt 2>.
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
"""},
 "prompts": [
   {"title": "Turn the exact map into signatures and failing tests",
    "when": "You have the architect's map and no code yet",
    "body": r"""Below is the exact / best-guess map for <feature>, and the spec clauses.

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
SPEC CLAUSES: <paste>"""},
   {"title": "Sweep the prompts for arithmetic",
    "when": "Weekly, and after every prompt change",
    "body": r"""Search every file under <src/prompts/> for arithmetic that a model is being asked
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
- At the end, give me the one-line shell command for this grep so I can put it in CI."""},
   {"title": "Edge cases for an exact function",
    "when": "The body is written and the tests feel thin",
    "body": r"""Here is an exact function and its current tests: <paste>.
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
- If the code and the spec disagree anywhere, say so first and loudly, before the table."""},
 ],
 "example": {
   "title": "SkyWays · $80 where the ledger said $62",
   "body": "The fare difference began life inside the prompt, in a sentence containing the word "
           "*exactly*. It returned $80 where the ledger said $62 — fluently, with no error, and the "
           "passenger was the first to know. The fix was about forty lines: `fare_difference()` "
           "taking two `Decimal` fares, raising on a currency mismatch, rounding half up once, with "
           "one assertion asserting 62.00 and the number removed from the prompt entirely. What made "
           "the fix cheap is that the architect's map had marked the step exact on day one. What made "
           "it necessary is that nobody had walked the map before writing the prompt."},
 "pitfalls": [
   "Leaving the arithmetic in the prompt because it is only one number. One number that gets acted on "
   "is the whole category, and it fails without producing an error anybody can catch.",
   "Letting the model write the code and its own assertions in one pass. They agree with each other, "
   "both disagree with the spec, and the suite goes green on the wrong behaviour.",
   "Using `float` for money. Two systems round differently, both are certain, and the difference "
   "surfaces weeks later as a reconciliation ticket nobody can reproduce.",
 ],
 "done_when": "Grepping the prompt directory for calculate, compute, total and sum returns nothing "
              "that gets acted on, and every exact step on the architect's map has a named function "
              "and a named test that has been seen red before it was seen green.",
},
]
