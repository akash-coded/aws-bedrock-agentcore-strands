"""QA lead · steps 7-8."""

STEPS_C = [
{
 "n": 7, "id": "shadow", "phase": "Shadow",
 "title": "Run beside the desk before you run instead of it",
 "when": "The end of P2, after the behaviour gate and before any live traffic",
 "purpose": (
   "The golden set proves the agent is right about cases **you curated**. A shadow run proves "
   "something different and harder: that it agrees with the live desk on today's traffic, including "
   "the storm day, the partner outage and the fare class that only appears in August. The agent "
   "decides beside the desk, every decision is logged, and it never acts — and *shadow never writes* "
   "is a test in the pipeline rather than an intention in a document. If it does not match, you found "
   "that out for free, which is the entire point of the rung."),
 "activities": [
   {"do": "Fix the window before you start it",
    "detail": "Fourteen days is a working default. A window chosen after the run is a window chosen to "
              "include the good fortnight, and everyone in the room will know it."},
   {"do": "Make 'shadow never writes' an assertion that fails the job",
    "detail": "Not a code review comment and not a configuration flag somebody set once. A shadow path "
              "that can write is a production path with a modest name."},
   {"do": "Compare decision by decision, nightly, per slice",
    "detail": "Nightly because a fortnight of unread comparisons is a fortnight wasted, and per slice "
              "because overall agreement of 96% sits comfortably on top of 64% on refunds."},
   {"do": "Exclude money actions from automatic agreement",
    "detail": "They stay gated whatever the shadow shows. Every other default in this step is yours to "
              "tune; this one is not, because the bar that would justify ungating them is not reachable."},
   {"do": "Read every disagreement yourself in the first week",
    "detail": "Half of them are the desk being wrong, which is a finding you can act on. The other "
              "half are the cases the golden set never had, which is where next month's cases come from."},
   {"do": "Compute the days before anyone promises a date",
    "detail": "days = cases needed ÷ (traffic share × cases per day). At 240 cases a day and 5% you "
              "see twelve a day, so a 500-case slice takes 42 days. The division takes ten seconds and "
              "it is almost never done before the date is announced."},
   {"do": "Widen slice by slice on live evidence",
    "detail": "Which is why a cut-over *widens* rather than sitting at five percent forever: a small "
              "share is the safe place to start and a slow place to learn."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Build the nightly comparison: agreement per slice, the disagreement list ranked by the "
           "cost of the difference, and the assertion that fails the job if a write is detected.",
    "caution": "Insist on the per-slice split from the first night. Retrofitting slices onto an "
               "aggregate comparison means re-running the window, and the window is the expensive part."},
   {"tool": "Chat LLM",
    "use": "Cluster a week of disagreements into themes and name them in plain words. Forty "
           "disagreements usually collapse into four causes, and clustering is what a model is for.",
    "caution": "Do not let it assume the desk is ground truth. Make it mark every theme agent-right, "
               "desk-right or genuinely ambiguous, and treat the third pile as rubric work rather than "
               "as defects."},
   {"tool": "Claude Code",
    "use": "Compute the widening schedule: cases needed per slice, days at 5%, 25% and 100%, and the "
           "condition that would let each step happen.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The agreement threshold, and any decision to leave a slice out of the comparison. Both are "
           "the expansion gate wearing a different hat, and the second one is how a slice quietly "
           "stops being measured.",
    "caution": None},
 ],
 "artifact": {
   "name": "Shadow comparison + expansion-gate evidence",
   "good": "Agreement per slice over a window fixed in advance, money actions reported separately and "
           "never counted toward it, a disagreement list a person has read, and a widening schedule in "
           "days derived from traffic rather than dates chosen in a meeting.",
   "owner": "QA lead"},
 "template": {
   "title": "Shadow comparison and expansion-gate evidence", "lang": "markdown",
   "body": """# Shadow run · <feature>
_Window: <start> to <end> (<n> days, fixed on <date> before the run) · Owner: <name>_

## Agreement, per slice
| Slice | Decisions compared | Agreed | Agreement | Threshold | Met? |
|-------|--------------------|--------|-----------|-----------|------|
| <same-day> | <n> | <n> | <n>% | 95% | |
| <codeshare> | <n> | <n> | <n>% | 95% | |
| <refund> | <n> | <n> | <n>% | n/a — excluded, stays gated | — |

**Money actions are excluded from automatic agreement and remain gated regardless of
what this table says.** Every other threshold here is tunable; that one is not.

Any slice under <n> compared decisions is **unproven**, not failed. Say which.

## Shadow never writes
| Assertion | Where it runs | Last green |
|-----------|---------------|-----------|
| no write call from the shadow path | <the nightly job> | <date> |
| shadow decisions land in <the log>, not <the ledger> | <the nightly job> | <date> |

## Disagreements — themes, not cases
| Theme | Count | Agent right / desk right / ambiguous | What it changes |
|-------|-------|--------------------------------------|-----------------|
| <theme> | <n> | <which> | <golden cases / rubric line / spec defect / nothing> |

Read in full by <name> for the first <n> days. Ambiguous themes are rubric work.

## Days of evidence, per share
days = cases needed ÷ (traffic share × cases per day) · cases per day = <n>

| Slice | Cases needed | At 5% | At 25% | At 100% |
|-------|--------------|-------|--------|---------|
| <codeshare> | <n> | <n> days | <n> days | <n> days |

Any slice needing more than <30> days at 5% needs a bigger starting share or a hold,
and that is a decision to take now rather than in week five.

## Widening — conditions, never dates
| Step | Condition |
|------|-----------|
| to 5% | threshold met on <slices>; rollback rehearsed on <date> by <name> |
| to 25% | live lower bound ≥ bar on <slice> for <n> consecutive days |
| to 100% | as above, plus zero <class> incidents and the injection suite green |

## Verdict
<open the expansion gate for <slices> | extend the window by <n> days | do not proceed, because ...>
"""},
 "prompts": [
   {"title": "Specify the nightly comparison",
    "when": "Setting the shadow run up, before night one",
    "body": """Write the specification for a nightly job that compares an agent's shadow decisions
against the live human desk.

It MUST output, PER SLICE and never only overall:
- decisions compared, agreed, agreement %
- a ranked list of disagreements: the input, the agent's decision, the desk's decision,
  and the estimated cost of the difference
- a flag on any slice whose agreement fell against the previous night
- the count of decisions per slice, so a slice with too few is reported as UNPROVEN
  rather than as a percentage

CONSTRAINTS:
- money actions are reported separately and NEVER counted toward automatic agreement
- the agent must not write: include an assertion that FAILS the job if any write call is
  detected from the shadow path, and say where that assertion runs
- the window is fixed in advance; the job must record the window it belongs to
- output is one markdown file and one CSV

Our slices: <list>. Our decisions are logged at: <where>. Cases per day: <n>."""},
   {"title": "Cluster the disagreements without assuming the desk is right",
    "when": "You have a week of shadow output and forty disagreements",
    "body": """Here are <n> cases where the agent and the human desk disagreed.

1. Cluster them into at most 6 themes. Name each in plain words, no jargon.
2. For each theme, mark it AGENT RIGHT / DESK RIGHT / GENUINELY AMBIGUOUS, with the
   reason. Do NOT treat the desk as ground truth — say so when the desk was wrong.
3. Rank the themes by the estimated cost of being wrong, not by how often they occur.
4. For each theme, say what it changes: a golden case, a rubric line, a spec defect,
   or nothing.
5. For the GENUINELY AMBIGUOUS pile, write the rubric sentence that would settle each
   one. That pile is rubric work, not defects.

OUTPUT: the table, then the five golden cases I should add first.

DISAGREEMENTS:
<paste>"""},
   {"title": "Compute the widening schedule",
    "when": "The shadow passed and somebody wants a date",
    "body": """Compute how long live evidence takes to arrive, per slice and per traffic share.

cases needed = 1.96^2 * p * (1-p) / (p - bar)^2
days = cases needed / (traffic share x cases per day)

For each slice give me: cases needed, then days at 5%, 25% and 100%.

Then:
- Flag every slice where 5% would take more than 30 days. Those need a larger starting
  share or a hold that lowers the bar, and I need to know now rather than in week five.
- Write the schedule as CONDITIONS, never dates: "widen to 25% when the live lower bound
  on <slice> holds at or above <bar> for <n> consecutive days".
- State plainly which slices will never accumulate enough live cases at any share, and
  what that means for them.

Show the arithmetic for one slice so I can check it.

SLICES, SCORES, BARS, TRAFFIC SHARE PER SLICE, CASES PER DAY:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · 96% that was not a pass",
   "body": "The shadow run cleared its threshold — **96%** agreement over fourteen days against a 95% "
           "default — and the room wanted the expansion gate opened. Inside that 96%, the agent had "
           "disagreed with the desk on **four of eleven** refund decisions, which is **64%** agreement "
           "on the slice that moves money. Two things were wrong and only one of them was the number. "
           "Eleven cases cannot conclude anything about refunds in either direction, so the honest "
           "word was *unproven* rather than *failed*; and refunds should never have been inside the "
           "automatic agreement figure at all, because money actions stay gated regardless. The "
           "low-risk slices widened on the evidence they had, refunds stayed gated, and refund cases "
           "kept accumulating at the rate the traffic allowed."},
 "pitfalls": [
   "Reading the aggregate. The slice with the money in it is the small one, and small slices disappear "
   "into averages exactly when it matters most.",
   "A three-day window as a formality. It holds no weekend and no disruption day, so it buys false "
   "confidence at full price — and worse than no shadow run, because a number is quotable.",
   "Promising a cut-over date before doing the division. At 5% of 240 cases a day you see twelve a "
   "day, so a 500-case slice needs 42 days, and nobody who promised a fortnight had run the numbers.",
 ],
 "done_when": "Agreement is reported per slice over a window fixed in advance, 'shadow never writes' is "
              "a passing test in the nightly job, and every widening step has a day count derived from "
              "traffic rather than a date chosen in a meeting.",
},
{
 "n": 8, "id": "watch", "phase": "Watch",
 "title": "Watch for drift, and turn incidents into controls",
 "when": "P3, every week, forever",
 "purpose": (
   "Two defects reach production that no suite catches. **Drift** is behaviour changing with no "
   "deploy, no error and no alert, until a customer complains three months later that the assistant "
   "offers credits instead of refunds. And an **incident** is the system telling you which control "
   "was missing — but only if the room asks the right question, because the wrong question produces a "
   "name in five minutes and fifty-five minutes of that person's defence while the refund tool still "
   "accepts any amount. Both of these close back into the golden set, which is what stops the same "
   "failure arriving twice."),
 "activities": [
   {"do": "Chart one output mix weekly",
    "detail": "The one that would embarrass the team if it moved: refund versus credit, propose versus "
              "escalate. One chart with a threshold, watched like a conversion rate. Not a dashboard "
              "with forty panels that nobody opens."},
   {"do": "Set two thresholds, not one",
    "detail": "5% week over week catches a jump. It never fires on a slide of under two points a week "
              "— and under two points a week moves thirteen points in seven weeks. Watch the level "
              "against a frozen baseline as well as the step."},
   {"do": "Wire the drift alert to the release gate",
    "detail": "Automatically, with no human deciding to. That single piece of wiring is the difference "
              "between a control and a chart, and it is one line of policy."},
   {"do": "Ask the one question first, in the postmortem",
    "detail": "*Which enforced control would have made this impossible?* Not who wrote the prompt. The "
              "second question is the only one that produces a fix, and blameless framing is not a "
              "courtesy — it is the only framing under which people tell you what happened."},
   {"do": "Classify every claimed layer as enforced, a request, or absent",
    "detail": "Without flattering yourself. A rule that exists only in a prompt is a request, and a "
              "model can be talked past a request. Two layers that fail together are one layer."},
   {"do": "Test the fix with: does it close the path, or lower the probability?",
    "detail": "Both have a place and only one ends the incident class. A better-worded prompt lowers "
              "the probability; a typed bounded parameter closes the path. An alert is detection, "
              "which is not prevention, and the table is where that distinction stays visible."},
   {"do": "Drop the autonomy level until a shadow run re-earns it, and feed six cases forward",
    "detail": "A fix is a claim until it has been proven. One level down for a fortnight costs a "
              "little speed and buys the evidence that makes the restoration credible."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Build the weekly drift readout from the trace: the week-over-week step, the level against "
           "the frozen baseline, and both thresholds evaluated in the same job.",
    "caution": "Have it read the trace, not the application logs. The trace is the redacted record of "
               "what was decided; the logs are whatever happened to be printed, and they change when "
               "somebody tidies up."},
   {"tool": "Chat LLM",
    "use": "Turn a postmortem transcript into the layer table, forcing the enforced / request / absent "
           "classification. It holds the format while the room wants to talk about blame.",
    "caution": "Check every row it marked *enforced*. It will accept a prompt sentence as a control, "
               "because a prompt sentence reads exactly like a rule — which is also why the room "
               "believed it."},
   {"tool": "Chat LLM",
    "use": "Draft the six golden cases the incident owes, as data lines with expected outcomes and "
           "reason codes, ready to paste into the set.",
    "caution": "Make it write the expected outcome as the refusal plus the reason code. A case whose "
               "expectation is *behaves sensibly* is not a test, and it will be green forever."},
   {"tool": "Do not delegate",
    "use": "Whether a proposed fix closes the path. That single judgement is the difference between an "
           "incident class ending and the same incident returning next quarter with different wording "
           "on a different tool.",
    "caution": None},
 ],
 "artifact": {
   "name": "Drift readout + missing-control postmortem",
   "good": "One chart with two live thresholds and an alert wired to the release gate, plus a "
           "postmortem that leaves the room as an enforced control, a lowered autonomy record, an "
           "amended decision record and six new golden cases.",
   "owner": "QA lead"},
 "template": {
   "title": "Drift readout and missing-control postmortem", "lang": "markdown",
   "body": """# Drift · <feature> · week <n>
_Baseline frozen <date> from <source> · Owner: <name>_

| Output mix watched | Baseline | Last week | This week | w/w step | vs baseline |
|--------------------|----------|-----------|-----------|----------|-------------|
| <% refund vs credit> | <n>% | <n>% | <n>% | <n>pp | <n>pp |
| <% propose vs escalate> | <n>% | <n>% | <n>% | <n>pp | <n>pp |

**Two thresholds, because one is not enough.**
- Step: alert at **5pp** week over week. Catches a jump.
- Level: alert at **10pp** against the frozen baseline. Catches the slow slide that a
  week-over-week rule never fires on — under 2pp a week moves 13pp in seven weeks.

A drift alert **re-opens the release gate automatically**. Last triggered: <date / never>.
Baseline re-frozen only by <name>, and never to make an alert go away.

---
# Incident · <id> · <date>

**1 · The question**
Which **enforced** control would have made this impossible?
(Not: who wrote the prompt. That question costs an hour and changes nothing.)

**2 · Layers claimed, honestly classified**
| Layer | Claimed | Reality: enforced / a request / absent | Would it have stopped it? |
|-------|---------|----------------------------------------|---------------------------|
| <input marked as data> | yes | <absent> | no |
| <the prompt's policy> | yes | **a request** | no |
| <a $400 cap> | yes | <absent from the code> | **yes** |
| <a named approver> | yes | <absent from the code> | **yes** |
| <an alert on the trace> | yes | <absent> | no — it reports afterwards |

Two layers that fail together are one layer. A rule that lives only in a prompt is a
request, and a model can be talked past a request.

**3 · The fix**
| Proposal | Closes the path, or lowers the probability? |
|----------|--------------------------------------------|
| <reword the prompt> | lowers the probability — the next attempt is worded differently |
| <add an alert> | neither — that is detection, not prevention |
| **<cap and confirmation token in the tool signature>** | **closes the path** |

**4 · Autonomy**
| Action | Level now | Level after | Condition to restore |
|--------|-----------|-------------|----------------------|
| <issue_refund> | <2> | <1> | <a 14-day shadow run at or above threshold> |

**5 · Feed forward** — four artefacts leave the room
- **Golden cases:** <6> new, in <slice>, each with its expected refusal and reason code
- **Injection payloads:** the string, tried from every entry point
- **Amended decision record:** <ADR-nnn> now defines *enforced* as **in the tool signature**
- **P0 brief:** pain · evidence · the missing enforced control · fix · value
"""},
 "prompts": [
   {"title": "The weekly drift readout",
    "when": "Every Monday, from the trace",
    "body": """Build this week's drift readout from the trace at <path>.

For each output mix I name, report:
- this week's share, last week's share, and the week-over-week step in percentage points
- the share at the frozen baseline of <date>, and the gap against it in points
- whether either threshold is breached: 5pp week over week, or 10pp against baseline

RULES:
- Read the trace, not the application logs. Say which fields you used.
- Normalise by volume: a mix moving because total volume halved is a different finding,
  and I want it called out separately.
- Do NOT smooth the series. Smoothing is how a slow slide becomes invisible.
- If a week has fewer than <n> decisions, report it as thin rather than as a percentage.

OUTPUT: the table, then a one-line verdict per mix, then — if anything breached — the
sentence I will send to re-open the release gate.

MIXES TO WATCH: <list>."""},
   {"title": "Run the missing-control postmortem",
    "when": "In the room, while somebody is opening the commit history",
    "body": """Turn this incident into a missing-control postmortem. Use EXACTLY this structure
and do not add sections.

1 · THE QUESTION: which ENFORCED control would have made this impossible?
2 · LAYERS: one row per layer the design CLAIMED to have.
    | Layer | Claimed | enforced / a request / absent | Would it have stopped it? |
3 · FIX: for each proposal, does it CLOSE THE PATH or LOWER THE PROBABILITY?
4 · AUTONOMY: level now, level after, and the condition that restores it.
5 · FEED FORWARD: golden cases, injection payloads, the decision record to amend,
    and the five-part P0 brief (pain · evidence · finding · fix · value).

RULES:
- Do not name a person. Do not quote the input that triggered it.
- A rule that exists only in a prompt is A REQUEST, never enforced. Apply this without
  exception, including where the prompt is very clearly worded.
- Two layers that fail together count as ONE layer. Merge them and say so.
- An alert is detection, not prevention. Mark it as such and keep it in the table.
- If NO layer would have stopped it, say that in one sentence rather than softening it.

INCIDENT:
<paste>"""},
   {"title": "Turn the incident into golden cases",
    "when": "The postmortem is finished and the fix is not a test yet",
    "body": """Write the golden cases this incident owes. Six is the working default.

For each case output one JSON line with: id, slice, source (the incident id), input
(redacted), expect (action + reason code), and a note saying what it protects.

Cover, at minimum:
- the exact case that happened, with every identifier removed
- the same case just under the cap, and just over it
- the same case with the confirmation absent
- the same attempt arriving through a DIFFERENT entry point
- the case that would have been the near miss nobody reported

RULES:
- The expected outcome is a refusal or an escalation with a REASON CODE. Never
  "behaves sensibly" and never a sentence of prose.
- Tag every case with the slice whose bar it belongs to. If it belongs to no existing
  slice, say so — the incident may have revealed that the slice list is wrong.
- Do not invent facts the write-up does not contain. Mark them <unknown>.

INCIDENT AND FIX:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · thirteen points in seven weeks, and one question in one hour",
   "body": "The refund-versus-credit mix was 61/39 in week one and 48/52 in week eight. No deploy, no "
           "error and no alert, because the alert was set at 5% week over week and the slide averaged "
           "**1.9 points a week** — so it never fired once while the behaviour moved thirteen points. "
           "The chart had been on the wall the whole time. Then on day 82 a **$2,000** refund went out "
           "that was not owed and somebody opened the commit history. Redirected to *which enforced "
           "control would have made this impossible?*, the same hour produced a layer table: **five** "
           "layers claimed, **none** enforced, two of them living only in the prompt. Either the cap "
           "or the approver, enforced, would have made the refund impossible. Out of the room came a "
           "typed cap, a confirmation token, refunds dropped one autonomy level until a fourteen-day "
           "shadow run re-earned it, and six new golden cases."},
 "pitfalls": [
   "A week-over-week threshold with no level check. The slide too slow to trip the alert is the one "
   "that runs longest, and thirteen points of mix change over seven weeks never fires a 5% weekly rule.",
   "A drift chart nobody opens. It becomes a control the moment an alert re-opens the release gate "
   "automatically, and it is decoration every day before that.",
   "A postmortem that produces a name. The refund tool still accepts any amount, and the same attack "
   "works next quarter on the next tool that moves money.",
 ],
 "done_when": "One output mix is charted weekly against both thresholds, a breach re-opens the release "
              "gate without anyone deciding to, and the last incident left the room as an enforced "
              "control plus six new golden cases.",
},
]
