"""Product manager · steps 6-8."""

STEPS_C = [
{
 "n": 6, "id": "gate", "phase": "Gate",
 "title": "Hold the three gates that are yours",
 "when": "Throughout P2, at every bolt and every release",
 "purpose": (
   "Five gates exist across the lifecycle and you own three. A gate is a decision with evidence in "
   "front of a named person and their name on it — not a click, not a status column, not a meeting "
   "that ends in 'fine'. The common failure is a product manager approving a pull request they cannot "
   "evaluate while nobody asks them the one thing they can judge, which is whether it is worth doing "
   "at all."),
 "activities": [
   {"do": "Claim intent, plan and release; decline the other two",
    "detail": "Behaviour and expansion belong to the QA lead. Ask to be removed from those sign-offs. "
              "Your name on a judgement you cannot make weakens every gate you do hold."},
   {"do": "Write the evidence line for each gate before you need it",
    "detail": "Intent: pain register, AI-fit verdict, value line. Plan: bolt cut, authority budget, "
              "gate map. Release: shadow comparison, rollback rehearsed. Empty evidence line, no gate."},
   {"do": "Audit last month's approvals",
    "detail": "List them and strike the ones you could not evaluate. The list is usually longer than "
              "expected and it is the fastest way to make this concrete with your team."},
   {"do": "Read the eval readout in the shape of your bar sheet",
    "detail": "Per slice, against its bar, with the lower bound. Not one percentage. You do not need to "
              "understand the harness; you need the readout in the shape of the artefact you wrote."},
   {"do": "Write down the rejection rule",
    "detail": "Any slice below its bar rejects the change, however good the headline. Written down "
              "once, it stops being re-argued per release."},
   {"do": "Make a drift alert re-open the release gate",
    "detail": "Automatically. This is what turns a chart into a control, and it is a one-line policy "
              "decision that you own."},
 ],
 "ai": [
   {"tool": "Chat LLM",
    "use": "Paste a release summary and your bar sheet and ask: which slices are below bar, and what "
           "does the overall number hide? It is reliable at the comparison and it never gets bored.",
    "caution": "Give it the lower bounds, not just the scores, or it will tell you a 40-case slice has "
               "passed."},
   {"tool": "Claude Code",
    "use": "Have it produce the per-slice readout from the harness output automatically, in the shape "
           "of your bar sheet, so the readout arrives already comparable.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Before a release gate, ask it to list every way this change could regress a slice that was "
           "not tested. A cheap pre-mortem.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The gate decision itself. A gate is defined by a name on it. A model cannot hold "
           "accountability, so it cannot hold a gate.",
    "caution": None},
 ],
 "artifact": {
   "name": "Gate decision record",
   "good": "Three named decisions per release with the evidence attached, rather than a stream of "
           "approvals nobody can defend.",
   "owner": "Product manager"},
 "template": {
   "title": "Gate decision record", "lang": "markdown",
   "body": """# Gate · <intent | plan | release> · <feature> · <date>

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
"""},
 "prompts": [
   {"title": "Per-slice release readout",
    "when": "QA hands you a score and you need to decide",
    "body": """Compare this evaluation output against my acceptance bars.

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
RESULTS: <paste>"""},
   {"title": "Audit my own approvals",
    "when": "You suspect you are signing things you cannot judge",
    "body": """Here are the approvals I gave last month: <paste list>.

For each, tell me:
- Which of the five gates it belongs to: intent / plan / behaviour / release / expansion.
- Whether a product manager can evaluate it, or whether it needs engineering or QA judgement.
- If I could not evaluate it: who should have signed, and what I should have been asked instead.

Then give me the short script I can use to hand the wrong ones back."""},
 ],
 "example": {
   "title": "SkyWays · the readout that stopped a release",
   "body": "The overall golden-set score rose from 79% to 84% and the team wanted to ship. The readout "
           "in bar-sheet shape showed codeshare had fallen from 81% to 77%, against a bar of 80. The "
           "headline had improved because the easy high-volume slice improved, and averaging hid a real "
           "regression on the slice that carried all the risk. The change was rejected in four minutes, "
           "because the artefact arrived in the shape of the decision rather than in the shape of the "
           "harness."},
 "pitfalls": [
   "Approving what you cannot evaluate. It feels cooperative and it devalues every gate you hold.",
   "Accepting a single accuracy number. The slice that carries the risk is always the one the average "
   "hides.",
   "Treating a gate as a meeting. A gate is a name and an evidence line; the meeting is optional.",
 ],
 "done_when": "Every release has three named decisions with evidence attached, and you have been removed "
              "from the two sign-offs that were never yours.",
},
{
 "n": 7, "id": "launch", "phase": "Launch",
 "title": "Shadow, then five percent, then widen",
 "when": "The end of P2 into P3",
 "purpose": (
   "Never switch on with nothing to compare against. A shadow run puts the agent beside the live "
   "process, deciding and logged but taking no action, for a window fixed in advance. Then five "
   "percent of real traffic, then wider — and the widening is earned by live evidence rather than by a "
   "date. If it does not match the humans, you learned that for free."),
 "activities": [
   {"do": "Put a shadow window in the plan before any switch-on date exists",
    "detail": "Fourteen days is a common default. Fixing it early stops it being negotiated away when a "
              "launch date is under pressure."},
   {"do": "Set the threshold, and the money exception",
    "detail": "95% agreement per slice is a reasonable default. Money actions are excluded from "
              "automatic agreement and stay gated regardless of what the shadow shows."},
   {"do": "Compare per slice, decision by decision",
    "detail": "Overall agreement of 96% can sit on top of 64% on refunds. The headline is the trap."},
   {"do": "Read every disagreement in the first week",
    "detail": "Personally. The disagreements are the cheapest product research you will ever get, and "
              "half of them are the humans being wrong, which is also a finding."},
   {"do": "Rehearse the rollback before the cut-over",
    "detail": "Not during. With a flag-driven shadow path the rollback is the flag, and you should have "
              "watched someone throw it."},
   {"do": "Widen on evidence, slice by slice",
    "detail": "Compute how long each share needs: days = cases needed / (share × cases per day). A "
              "small share is the safe place to start and a slow place to learn, which is why you widen."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it build the nightly comparison: agreement per slice, the disagreement list ranked by "
           "cost, and a chart. This is a reporting job, done once, run every night.",
    "caution": "Insist the comparison is per slice from the start. Retrofitting slices onto an "
               "aggregate comparison means re-running the window."},
   {"tool": "Chat LLM",
    "use": "Cluster the disagreements and name the themes. Forty disagreements usually collapse into "
           "four causes, and the clustering is exactly what a model is good at.",
    "caution": "Read the raw disagreements yourself first, at least in week one. The clusters are more "
               "useful once you know what the edges look like."},
   {"tool": "Chat LLM",
    "use": "Compute the widening schedule from cases-needed and traffic share, and tell you the date "
           "each slice could widen if evidence holds.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The cut-over decision, and any decision to exclude a slice from gating. Those are yours.",
    "caution": None},
 ],
 "artifact": {
   "name": "Cut-over decision",
   "good": "A comparison per slice over a fixed window, a threshold met or not met, a rehearsed "
           "rollback, and a widening schedule with conditions rather than dates.",
   "owner": "Product manager"},
 "template": {
   "title": "Shadow run and cut-over decision", "lang": "markdown",
   "body": """# Cut-over decision · <feature>
_Shadow window: <start> to <end> (<n> days) · Decided: <date> · By: <name>_

## Agreement, per slice
| Slice | Decisions compared | Agreed | Agreement | Threshold | Met? |
|-------|--------------------|--------|-----------|-----------|------|
| <same-day> | <n> | <n> | <n>% | 95% | |
| <codeshare> | <n> | <n> | <n>% | 95% | |
| <refund> | <n> | <n> | <n>% | n/a — stays gated | |

**Money actions are excluded from automatic agreement and remain gated regardless.**

## Disagreements — the themes
| Theme | Count | Agent right / desk right | Action |
|-------|-------|--------------------------|--------|
| | | | |

## Rollback
- Mechanism: <the flag>
- Rehearsed on <date> by <name>; time to revert: <n> minutes
- Who can throw it without asking: <names>

## Widening schedule — conditions, not dates
| Share | Cases needed | Days at this share | Widen when |
|-------|--------------|--------------------|-----------|
| 5% | <n> | <n> | live lower bound >= bar on <slice> |
| 25% | <n> | <n> | as above, plus zero <class> incidents |
| 100% | | | |

## Decision
<cut over to 5% on <date> | extend the shadow by <n> days | do not proceed, because ...>
"""},
 "prompts": [
   {"title": "Nightly shadow comparison spec",
    "when": "Setting up the shadow run",
    "body": """Write the spec for a nightly job comparing an agent's shadow decisions against the
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

Our slices: <list>. Our data: <where the decisions are logged>."""},
   {"title": "Cluster the disagreements",
    "when": "You have a week of shadow output",
    "body": """Here are <n> cases where the agent and the human desk disagreed.

1. Cluster them into at most 6 themes. Name each theme in plain words.
2. For each theme: how many cases, and is the AGENT or the DESK more often right? Say
   which and why — do not assume the human is the ground truth.
3. Rank the themes by estimated cost of being wrong, not by frequency.
4. For the top theme, tell me whether the fix is the spec, the prompt, the tools, or the
   bar — and what specifically I would change.

DISAGREEMENTS:
<paste>"""},
   {"title": "Widening schedule arithmetic",
    "when": "Shadow passed and you need a credible plan",
    "body": """Compute a widening schedule.

For each slice give me: cases needed to prove the bar, then days of live evidence at 5%,
25% and 100% of traffic.

cases needed = 1.96^2 * p * (1-p) / (p - bar)^2
days = cases needed / (share x cases per day)

Then write the schedule as CONDITIONS, never dates: "widen to 25% when the live lower
bound on <slice> holds at or above <bar> for <n> consecutive days".

Flag any slice where 5% would take more than 30 days — those need a bigger starting
share or a different approach, and I need to know now.

Slices, observed scores, bars, cases/day: <paste>"""},
 ],
 "example": {
   "title": "SkyWays · what seven days bought",
   "body": "The full plan needed ten weeks and the sponsor had six, so the shadow window was cut from "
           "fourteen days to seven — but only on the simple slice, and with every disagreement read. "
           "Seven days at 144 same-day cases a day is about a thousand decisions, which bounds a 97% "
           "slice tightly. Codeshare stayed at 76% against a bar of 80 and did not ship, and nobody "
           "pretended otherwise. The sponsor heard it as a trade rather than a delay: sixty percent of "
           "the load in six weeks, proven, with codeshare next."},
 "pitfalls": [
   "Cutting over at fifty percent. Half your users meet the first-day failure, and first-day failures "
   "are the ones that get remembered.",
   "A three-day shadow as a formality. It contains no weekend and no disruption day, so it buys false "
   "confidence at full price.",
   "Reading only the aggregate agreement. The slice with the money in it is small, and small slices "
   "disappear into averages.",
 ],
 "done_when": "You can tell the sponsor what share of traffic the agent handles, what evidence earned "
              "it, and how fast you can take it back.",
},
{
 "n": 8, "id": "learn", "phase": "Learn",
 "title": "Report two numbers and turn incidents into the next frame",
 "when": "P3, every cycle, forever",
 "purpose": (
   "This is the step that decides whether the programme survives. A first cycle can genuinely save "
   "time and cost more, and that is survivable — if it arrives from you rather than from finance. "
   "Then production becomes the source of the next P0: drift is a KPI you watch, and an incident is a "
   "brief you write, not a name you find."),
 "activities": [
   {"do": "Take the baseline before the pilot",
    "detail": "An afternoon's work, and worthless afterwards. This is the single most commonly skipped "
              "step in the whole role, and it is unrecoverable once the pilot has started."},
   {"do": "Report time saved and money spent, together, always",
    "detail": "Plus two rows that keep them honest: review hours added, and re-runs. The programme is "
              "cancelled on the number you hid, never on the one you showed."},
   {"do": "State the trajectory, not just the point",
    "detail": "Cost turns positive from cycle two as the review load falls. Say so in cycle one, with "
              "the expected number, so cycle two is a confirmation rather than a surprise."},
   {"do": "Chart one output mix weekly",
    "detail": "The one that would embarrass you if it drifted. A probabilistic system changes behaviour "
              "when the world shifts under it, with no deploy and no error."},
   {"do": "Set the drift alert, and wire it to the release gate",
    "detail": "Five percent week over week as a starting default. The wiring is what makes it a control "
              "rather than a chart nobody opens."},
   {"do": "Rewrite every incident as a brief",
    "detail": "Pain, evidence, the missing enforced control, the fix, the value. A postmortem that "
              "produces a name has not finished; one that produces a control has."},
   {"do": "Run the maturity self-check, honestly",
    "detail": "Six controls, present or absent. Your level is how many you have; your next step is the "
              "first one you do not. It replaces the tool-count metric, which rewards the least mature "
              "behaviour available."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Build the two-number report from the engineering ledger automatically, every cycle, with "
           "the review and re-run rows included by construction so they cannot be quietly dropped.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Draft the steering-committee narrative from the numbers. Ask it for the version a sceptical "
           "CFO would ask questions about, then answer those questions before the meeting.",
    "caution": "Do not let it choose which numbers to feature. That selection is the integrity of the "
               "report and it is yours."},
   {"tool": "Chat LLM",
    "use": "Turn a postmortem transcript into the five-part brief, forcing the missing-control question. "
           "It is good at holding the format when the room wants to talk about blame.",
    "caution": "Check that its 'missing control' is genuinely enforceable. It will happily propose a "
               "better prompt, which is a request, not a control."},
   {"tool": "Do not delegate",
    "use": "Deciding what to report. Everything else in this step can be drafted; the choice of what "
           "the sponsor sees is the job.",
    "caution": None},
 ],
 "artifact": {
   "name": "Two-number report · drift readout · next-P0 brief",
   "good": "One page the sponsor reads in a minute, with both numbers, the trajectory, and the honest "
           "rows. Plus a brief that turns the last incident into the next thing you build.",
   "owner": "Product manager"},
 "template": {
   "title": "Two-number report and next-P0 brief", "lang": "markdown",
   "body": """# Cycle <n> · <feature> · <date>

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
**Pain** — <what happened, as a measurement>
**Evidence** — <trace id, date, link>
**Finding** — the enforced control that was missing: <name it>
**Fix** — <the control, where it will live>
**Value** — <this class of incident becomes impossible, not less likely>
"""},
 "prompts": [
   {"title": "Build the two-number report",
    "when": "End of cycle, from the engineering ledger",
    "body": """Build a two-number cycle report from this ledger.

MUST include, in this order:
1. Person-days per story: baseline vs now, and % change
2. Token spend per story
3. Review hours added per story (this keeps number 1 honest — never omit it)
4. Re-runs per story (the leak signal)
5. A net line: "saved X person-days, spent $Y plus Z review hours"

Then:
- State the trajectory: what happens to the review load next cycle and why.
- Flag any number where the baseline was taken AFTER the pilot started, because that
  number is not defensible and I need to say so rather than be caught.

Do NOT drop a row because it is unflattering. Do not editorialise.

LEDGER:
<paste>"""},
   {"title": "Postmortem to next-P0 brief",
    "when": "After an incident, while the room is still arguing",
    "body": """Turn this incident into a P0 brief. Use EXACTLY this structure:

**Pain** — what happened, as a measurement (amount, count, who was affected)
**Evidence** — the trace or log reference
**Finding** — the ENFORCED CONTROL that, if present, would have made this IMPOSSIBLE
**Fix** — where that control will live (a tool signature, a gate, a permission)
**Value** — what class of incident becomes impossible

Rules:
- Do not name a person. Do not name the input that triggered it.
- "A better prompt" is NOT a control — a prompt is a request that a model can be talked
  past. If your finding is a prompt change, you have not found the control yet.
- Distinguish detection (an alert) from prevention (a cap). Say which yours is.
- If several layers failed, list each as ENFORCED / A REQUEST / ABSENT.

INCIDENT:
<paste>"""},
   {"title": "The sceptical CFO rehearsal",
    "when": "Before the steering meeting",
    "body": """You are a sceptical CFO. Here is my cycle report: <paste>.

Ask me the five hardest questions you would ask, in the order you would ask them.
Prioritise:
- anything where the baseline is weak or was taken late
- the gap between the saving and the spend
- whether the saving is real or has moved cost somewhere I am not measuring
- what happens to the spend at 10x volume

For each question, tell me what a good answer looks like and what a bad one sounds like.
Do not be polite."""},
 ],
 "example": {
   "title": "SkyWays · day ninety",
   "body": "The report said 40 to 45 percent fewer person-days and a token bill of $4,200, on one line, "
           "with the review hours and the re-run count beside them. The review row was up, and it was in "
           "the report, with the reason and the expected fall. The programme continued — not because the "
           "numbers were flattering, but because both of them came from the team. The counterfactual is "
           "well documented elsewhere: every cycle showing time saved, none showing spend, and a CFO "
           "arriving at a budget review with a number nobody in the programme had seen."},
 "pitfalls": [
   "Taking the baseline after the pilot started. Unrecoverable, and everyone can tell.",
   "Withholding the cost number while it is still bad, meaning to show it once it improves. That is the "
   "exact sequence that gets programmes cancelled, and it is usually done by people trying to protect them.",
   "Counting AI tool adoption as maturity. It rewards the least mature behaviour available; nine tools "
   "with no gates is level one.",
 ],
 "done_when": "Your sponsor has never learned a number about this programme from someone other than you.",
},
]
