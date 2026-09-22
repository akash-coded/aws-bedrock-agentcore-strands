"""Engineering lead · steps 7-8."""

STEPS_C = [
{
 "n": 7, "id": "ship", "phase": "Ship",
 "title": "Build bolt by bolt, and put the shadow path behind a flag",
 "when": "P2, every day",
 "purpose": (
   "One bolt a day, in the architect's dependency order, integrated the same day. That order is not "
   "the backlog's order: the walking skeleton goes first with no model in it, the exact code goes "
   "early because it never blocks, the plug goes before any gated write that needs it, and the proof "
   "goes last because the harness needs something to run against. Then the whole thing goes live "
   "behind a flag as a shadow path that decides and never acts — and the rollback **is** the flag."),
 "activities": [
   {"do": "Start with the walking skeleton, with no model in it",
    "detail": "The thinnest end-to-end path: read a booking, show it. Half a day, and it retires the "
              "largest unknown — whether the pieces connect at all — on day one, which is the "
              "assumption every other bolt is resting on."},
   {"do": "Put the pure exact code early",
    "detail": "It is unit-testable in isolation, so it never blocks and never waits, and it frees "
              "review capacity for the days that need it. It is usually sitting at the end of the "
              "plan because it looked boring."},
   {"do": "Schedule the plug before its consumer",
    "detail": "The classic failure is the rebook bolt on day four and the MCP server it needs on day "
              "six. Checkers go after the steps they check. The proof goes last, because the harness "
              "needs something to run against."},
   {"do": "Say a bolt cannot be built alone BEFORE you start it",
    "detail": "Not at two in the afternoon. A bolt that needs the other half of a feature was cut "
              "horizontally instead of vertically, and the fix belongs with the architect rather "
              "than with whoever discovered it mid-build."},
   {"do": "Keep one unknown per bolt",
    "detail": "Then a day can fail for exactly one reason and you know which one. Two unknowns and "
              "the standup produces a discussion instead of an answer, and the discussion takes the "
              "next morning too."},
   {"do": "Integrate the same day, and review by band",
    "detail": "Same-day integration is what makes the cost of a wrong turn one day instead of two "
              "weeks. The band comes from the most dangerous tool the change touches, via the path "
              "rule, never from the author — every author believes their own change is low risk."},
   {"do": "Run the shadow path behind a flag, and make shadow-never-writes a test",
    "detail": "A test that fails the build if a write tool is reachable while the flag is in shadow "
              "mode, not an intention in a document. Then cut over at five percent, and rehearse the "
              "rollback before the cut-over rather than during it."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Give it the story file with the chat window closed and let it build the bolt. If it has "
           "to ask you something that is not in the file, that question is the finding, and it goes "
           "back into the template tonight.",
    "caution": "Watch for it reaching outside the bolt. An agent that helpfully fixes an adjacent "
               "file has turned a one-unknown day into a two-unknown review, and the reviewer will "
               "not know which half to trust."},
   {"tool": "An editor agent",
    "use": "The same-day integration work: rebases, conflict resolution, the small mechanical "
           "follow-ups that otherwise push integration to tomorrow and break the cadence.",
    "caution": None},
   {"tool": "A cheap tier",
    "use": "Generate the dependency-ordered plan from the bolt list plus a depends-on column, and "
           "flag cycles, plugs scheduled after their consumers, and any item with no dependencies "
           "sitting at the end.",
    "caution": "It orders only what you give it. A dependency you forgot to write down produces a "
               "confident plan with the day-four failure still in it."},
   {"tool": "Do not delegate",
    "use": "The judgement that a bolt cannot be built alone. It is a claim about your repository and "
           "your team's day, and it has to be said out loud to the architect by someone who will own "
           "the consequence of being wrong.",
    "caution": None},
 ],
 "artifact": {
   "name": "Bolt build log",
   "good": "One row per day: the bolt, its one unknown, integrated yes or no, and the harness result "
           "for its slice. Plus the flag, the shadow-never-writes test, and a rollback rehearsal with "
           "a name and a time on it.",
   "owner": "Engineering lead"},
 "template": {
   "title": "Bolt build log", "lang": "markdown",
   "body": r"""# Bolt build log · <feature>
_Architect's cut <10> bolts · Cadence one a day · Owner <name>_

## The order, and the rule that produced it
| Day | Bolt | Depends on | The ONE unknown | Band |
|-----|------|-----------|-----------------|------|
| 1 | <walking skeleton — read a booking, show it. NO MODEL> | — | <do the pieces connect?> | R1 |
| 2 | <fare_difference(), exact, unit-tested> | 1 | <the rounding rule> | R1 |
| 3 | <visa and codeshare eligibility, exact> | 1 | <where the partner rules live> | R1 |
| 4 | <rank_alternatives(), best-guess, measured> | 2 | <can it beat the desk?> | R2 |
| 5 | <independent checker after ranking> | 4 | <which model judges> | R2 |
| 6 | <MCP server, reads open> | 1 | <auth to the booking system> | R2 |
| 7 | <rebook() gated write> | 6 | <idempotency> | R3 |
| 8 | <issue_refund(max 400) + confirmation token> | 7 | <who mints the token> | R4 |
| 9 | <shadow path behind a flag> | 5, 8 | <flag plumbing> | R2 |
| 10 | <golden set and harness in CI> | 9 | <slice tagging> | R1 |

Rules this order obeys, in priority order: skeleton first · pure exact code early ·
checkers after the steps they check · the plug before any gated write that needs it ·
the proof last.

## Daily row
| Day | Bolt | Integrated same day? | Harness, its slice | Note |
|-----|------|---------------------|--------------------|------|
| <1> | <skeleton> | <yes, 16:00> | <n/a> | <...> |
| <2> | | | | |

## Cannot be built alone — raised BEFORE starting, never at 2pm
| Day | Bolt | What is missing | Cause | Who re-cuts |
|-----|------|-----------------|-------|-------------|
| <4> | <rebook> | <the MCP server, scheduled day 6> | <plug after consumer> | <architect> |

## The shadow path
- Flag `<skyways.rebooking.shadow>` — default off, off in production until <date>
- The agent decides and logs. It never acts.
- Test `<test_shadow_never_writes>` fails the build if any write tool is reachable
  while the flag is in shadow mode. This is a test, not an intention.
- Cut-over <5>% of traffic on <date>, <named slice> only
- **Rollback IS the flag.** Rehearsed <date> by <name>. Time to revert <90> seconds.
"""},
 "prompts": [
   {"title": "Order the bolts by dependency, not by priority",
    "when": "The architect has the cut and you need the day order",
    "body": r"""Here are the bolts for <feature>, each with a one-line description and a
depends-on column: <paste>.

Produce a day-by-day order in which every bolt's dependencies come strictly before it.

RULES, applied in this priority order:
1. The walking skeleton first — the thinnest end-to-end path with NO model in it.
2. Pure exact code early. It is testable alone, so it never blocks anyone.
3. Checkers after the steps they check.
4. Any plug (MCP server, connector, adapter) BEFORE the gated write that needs it.
5. The proof — golden set and harness — last.

Then report, separately and before the plan:
- any CYCLE, where two bolts wait on each other. A cycle is always a mis-cut and means
  one of them is really two bolts. Name which one.
- any plug scheduled after its consumer in the order I gave you
- any bolt with NO dependencies that I had scheduled late
- any bolt carrying more than ONE unknown, and how you would split it

If there is no walking skeleton in my list, add one and say what it would cover."""},
   {"title": "Build today's bolt from its file alone",
    "when": "The start of the build day",
    "body": r"""Build this bolt. The story file is the whole brief: <paste file>.

RULES:
- Work only inside the paths the file names. If you find a problem in an adjacent file,
  write it down at the end; do not fix it. A second fix makes the review two unknowns.
- Read context by the paths in section 1. Do not ask me to paste any of them.
- The unit tests named in section 4 are written first and must be seen failing.
- Nothing in section 3 changes: signatures, bands and confirmation parameters are fixed.
- If you need something that is not in the file, STOP and say what it is. Do not
  improvise it, and do not build around it.

OUTPUT, in this order:
1. The failing tests
2. The implementation
3. The command output showing them green
4. A list headed FILE DEFECTS — everything you needed that the story file lacked
5. A list headed OUT OF SCOPE — problems you found and deliberately did not fix"""},
   {"title": "The shadow path and the test that it never writes",
    "when": "Wiring the flag, before any cut-over",
    "body": r"""Implement the shadow path for <feature> behind a feature flag.

Behaviour:
- flag OFF: the live process runs as today. The agent is not invoked.
- flag SHADOW: the agent runs on the same input, decides, and logs its decision beside
  the live one. It performs NO writes of any kind.
- flag LIVE at <5>%: the agent acts for that share of traffic; everything else unchanged.

MUST INCLUDE:
- `test_shadow_never_writes` — fails the build if any write tool is REACHABLE while the
  flag is in shadow mode. Assert on the tool call, not on the agent's output.
- A nightly comparison job producing agreement PER SLICE, never one overall number, with
  money actions reported separately and never counted toward automatic agreement.
- A revert path that is the flag itself, and a rehearsal script that times it.

Do not add a kill switch that is separate from the flag. Two mechanisms means one of
them is untested on the day it is needed, and it will be the other one."""},
 ],
 "example": {
   "title": "SkyWays · day 30, the first bolt ships by four in the afternoon",
   "body": "The first bolt was a walking skeleton: read a booking, show it, no model anywhere in it. "
           "It shipped by four in the afternoon, and what it bought was not the feature but the "
           "answer to the question every other bolt was resting on — whether the pieces connect. The "
           "exact code went on days two and three, so review capacity was free when the ranking bolt "
           "arrived. The one re-cut came on day four and was raised at nine in the morning rather "
           "than at two: `rebook()` needed the MCP server scheduled for day six, a plug ordered after "
           "its consumer. Moving the plug cost an hour. Discovering it mid-build would have cost the "
           "day."},
 "pitfalls": [
   "Scheduling the plug after the thing that needs it. It is the single most common ordering error "
   "and it costs a whole day in the middle of the week, every time.",
   "Discovering at two in the afternoon that a bolt cannot be built alone. The information was "
   "available at nine; what was missing was somebody willing to say the cut was wrong before "
   "spending the day proving it.",
   "A shadow path that writes. It is an intention until it is a test, and the first time it writes it "
   "does so on real bookings, which is the exact risk the shadow run existed to remove.",
 ],
 "done_when": "Every bolt merged on the day it was built, the shadow path has a test that fails the "
              "build if a write is reachable, and somebody other than you has thrown the rollback "
              "flag in a rehearsal with a stopwatch running.",
},
{
 "n": 8, "id": "operate", "phase": "Operate",
 "title": "Cache, route, trace, test the injection, and keep the ledger",
 "when": "P3, from the first day in production onward",
 "purpose": (
   "Production is where the cost, the audit and the security posture are actually settled, and all "
   "three are made of small settings nobody notices until an invoice or an incident arrives. Caching "
   "that hits, routing by complexity with a loop cap, a trace that redacts rather than omits, an "
   "injection suite that runs weekly, and a ledger of effort and tokens the product manager's cost "
   "number is built from. None of it is difficult. All of it gets skipped, and four weeks later the "
   "bill is 4.4 times the estimate with flat traffic."),
 "activities": [
   {"do": "Order the prompt for the cache, and pick the window from traffic shape",
    "detail": "The cache matches an exact prefix, in the order tools then system then messages, up "
              "to the block you mark, so stable content goes first and the request last. Documented "
              "and read September 2026: a five-minute write is 1.25x the input price, a one-hour "
              "write is 2x, a read is 0.1x, and Fable and Mythos 5.1 read at 0.025x. Minimum around "
              "1,024 cacheable tokens, model-scoped, break-even on the second use. Five minutes when "
              "calls are seconds apart; one hour when the gap is twelve minutes, because the cheaper "
              "write paid on every call beats the dearer write paid once."},
   {"do": "Assert the cache is working, and mark hits in the trace",
    "detail": "`assert response.usage.cache_read_input_tokens > 0` on the **second** call, never the "
              "first. And mark hits in the trace, because cache hits return fast and a latency "
              "dashboard that flags very fast responses as suspected failures will get the cache "
              "switched off, which raises the bill by about a third within a day."},
   {"do": "Route by complexity, and cap the loop",
    "detail": "`MAX_LOOPS = 5` in every agent loop, with a per-transaction token cap beside it. The "
              "biggest model on a simple lookup can be up to 160 times the price of the right one, "
              "and one model per task, because a mid-task switch discards the cache."},
   {"do": "Write one redacted row per consequential action",
    "detail": "Mask, do not omit — `passport ****1234`. Timestamp, masked input, tools called, the "
              "decision, the model version, the approver, the cost. Omitting breaks the audit; "
              "logging raw makes the trace store a breach target, usually protected less carefully "
              "than the ledger it mirrors."},
   {"do": "Run the injection suite weekly, and on every prompt, tool or context change",
    "detail": "Every attack string against every gated tool from every entry point, including the "
              "partner API's free-text fields. Assert on the **tool calls** and the trace row, never "
              "on the model's wording — wording changes with the next prompt edit, and then the test "
              "is red for the wrong reason and green for the wrong reason the week after."},
   {"do": "Keep the effort-and-token ledger, per bolt",
    "detail": "Person-hours by activity, tokens by tier, re-runs, defects escaped. Five minutes a "
              "day. Tokens by tier rather than in total, because the tier mix is where routing shows "
              "up, and the re-run column is the leak signal — model switching and vague asks appear "
              "there first."},
   {"do": "Reconcile the spec by diff after a hotfix, never by rewriting it",
    "detail": "A diff keeps the reason the hotfix differed from the spec; a rewrite makes the spec "
              "agree with the code and loses the only record that they ever disagreed, which is the "
              "record the next postmortem needs."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it instrument the per-call log: tokens per call, tier, cache read tokens, retries. "
           "Those four ratios are what turn an invoice into a diagnosis, and without the log you "
           "cannot compute a single one of them.",
    "caution": "Make it remove the request id from the cached block while it is in there. That one "
               "field is the most common silent cache break, and it is always added for a good "
               "reason by somebody who was not thinking about prefixes."},
   {"tool": "A cheap tier",
    "use": "Run the weekly injection suite and the nightly redaction test on it. Both are volume "
           "jobs with deterministic assertions, and there is nothing a frontier model adds.",
    "caution": "The attack strings still need a person to extend them. A suite that has not grown in "
               "three months is testing last quarter's attacks and reporting green."},
   {"tool": "A chat surface",
    "use": "Give it the four ratios month over month and have it multiply them out against the ratio "
           "between the two invoices. If the product matches, you have explained the bill and can "
           "stop looking.",
    "caution": "Do not let it rank the fixes by the biggest ratio change. The order is (factor minus "
               "one) divided by days to fix, and those two orders are different — the retry breaker "
               "is usually the right fix in the wrong position."},
   {"tool": "Do not delegate",
    "use": "What the redaction rules are. Which fields are sensitive is a legal and regulatory "
           "question about your business, and a model asked to guess will mask the obvious "
           "identifiers and leave the booking free-text field alone.",
    "caution": None},
 ],
 "artifact": {
   "name": "Operations set — caching, routing, trace, injection suite, ledger",
   "good": "One reviewed file holding the caching and routing config, a redaction test, a weekly "
           "injection run with a date on it, and a four-column ledger per bolt that the PM's cost "
           "number is built from rather than estimated against.",
   "owner": "Engineering lead"},
 "template": {
   "title": "The production call · cache, route, cap, trace", "lang": "python",
   "body": r"""# src/agent/run.py — cache, route, cap, trace. This file and <config/routing.yaml>
# are reviewed like code: the day-75 bill began with a prompt reordered for clarity.
from decimal import Decimal

from src.errors import LoopCapReached
from src.redact import redact         # masks; never omits
from src.trace import trace

MAX_LOOPS, MAX_TOKENS_PER_TXN = 5, 120_000   # uncapped, a loop burns unnoticed
PRICE_PER_TOKEN = Decimal("<0.000003>")
TIERS = {"simple": "<cheap-model-id>", "standard": "<mid-model-id>",
         "hard": "<frontier-model-id>"}


def build_request(tools, system_blocks, request, ttl="5m"):
    # Exact prefix, order tools -> system -> messages. Stable first, volatile
    # request last, cache marker on the LAST STABLE block. Nothing cached may
    # hold a timestamp or request id. "5m" 1.25x, "1h" 2x, read 0.1x (Sept 2026).
    system = [{"type": "text", "text": text} for text in system_blocks]
    system[-1]["cache_control"] = {"type": "ephemeral", "ttl": ttl}
    return {"tools": tools, "system": system,
            "messages": [{"role": "user", "content": request}]}


def tier_for(case) -> str:
    # Route by complexity. ONE model per task: the cache is model-scoped, so a
    # mid-task switch discards the prefix and you pay the write again.
    if case.needs_partner_rules:
        return "hard"
    return "standard" if case.segments > 1 else "simple"


def handle(case, client, tools, blocks):
    model, spent = TIERS[tier_for(case)], 0
    for _ in range(MAX_LOOPS):
        r = client.messages.create(
            model=model, **build_request(tools, blocks, case.request))
        spent += r.usage.input_tokens + r.usage.output_tokens
        trace.write(action="<propose_rebooking>", model=model,  # version, always
                    input=redact(case.as_dict()),               # passport ****1234
                    tools_called=[t.name for t in r.tool_calls],
                    decision=r.decision, approver=case.approver,
                    cache_read_tokens=r.usage.cache_read_input_tokens,
                    cost=PRICE_PER_TOKEN * spent)
        if r.stop_reason == "end_turn" or spent > MAX_TOKENS_PER_TXN:
            return r.decision
    raise LoopCapReached(f"<propose_rebooking>: {MAX_LOOPS} loops")


# tests/agent/test_operate.py — the two assertions that keep this honest.
def test_the_second_call_reads_from_cache(client, case, tools, blocks):
    handle(case, client, tools, blocks)          # the first call pays the write
    handle(case, client, tools, blocks)
    assert client.last.usage.cache_read_input_tokens > 0    # the SECOND call


def test_a_passport_never_reaches_a_row(rows):
    assert all("<passport_number>" not in str(row) for row in rows)
    assert any("****" in str(row.input) for row in rows)    # masked, not omitted
"""},
 "prompts": [
   {"title": "Diagnose the bill from the per-call log",
    "when": "The invoice has left its estimate and traffic is flat",
    "body": r"""Traffic is flat and the bill is <n>x the estimate. Do not look at the price list.
Here is the per-call log for this month and the month before: <paste or path>.

Compute these four ratios, this month against last:
| Signature | Baseline | Now | Factor |
- tokens per call
- frontier tier share
- cache hit ratio (a FALL is a rise in cost; express it as a factor above 1)
- retries per conversation

Multiply the four factors. Compare the product with the ratio between the two invoices.
- If they match, say so and stop looking. The bill is explained.
- If the product is well below the invoice ratio, something structural changed that is
  not a habit — traffic, a new feature, or a price change. Say which to check.

Then order the fixes by  priority = (factor - 1) / days to fix,  NOT by the biggest
ratio change. Give me the table with the order and the days you assumed.

Finally: name the guards that would have caught this in week one rather than week four."""},
   {"title": "Build the weekly injection suite",
    "when": "Before launch, and it runs weekly forever after",
    "body": r"""Build an injection regression suite for <feature>.

Cross-product: EVERY attack string x EVERY gated tool x EVERY entry point.

Entry points must include, at minimum:
- the passenger's own message
- a partner API response free-text field (the partner is trusted; the field is not)
- an uploaded document, including text that is invisible when rendered
- a free-text field on the booking record
- a retrieved knowledge-base chunk

RULES — these decide whether the suite is worth anything:
- Assert on the TOOL CALLS and on the trace row. Never assert on the model's wording.
  A test that checks the reply contains "I cannot do that" is red for the wrong reason
  after the next prompt edit and green for the wrong reason the week after.
- Every test asserts BOTH that the action did not happen AND that an attempt was
  recorded in the trace.
- The suite runs weekly on a schedule, and on every prompt, tool or context change.

OUTPUT: the test module, the attack-string fixture file, and the CI schedule entry.

OUR GATED TOOLS: <paste signatures>
OUR ENTRY POINTS: <paste>"""},
   {"title": "Reconcile the spec by diff after a hotfix",
    "when": "The hotfix is merged and the room wants to move on",
    "body": r"""A hotfix shipped outside the normal flow. Here is the spec as it stood: <paste>.
Here is what actually merged: <paste diff>.

Produce a RECONCILIATION DIFF, not a rewritten spec.

| Spec clause | What shipped | Same? | Why it differed | Keep the code or keep the spec? |

RULES:
- Never rewrite the spec so it agrees with the code. The rewrite loses the only record
  that they ever disagreed, and that record is what the next postmortem needs.
- For every difference, say whether the SPEC was wrong (amend it, with the reason and
  the date) or the CODE was expedient (raise the follow-up, with the risk it carries
  until then).
- Flag any difference that touches a cap, a confirmation token, a permission or a trace
  field. Those are not tidy-ups; they are changes to a control and need the band.
- List any golden-set case that the hotfix invalidates, and any new case it implies.

Finish with the amended ADR line, if a decision changed, in one sentence."""},
 ],
 "example": {
   "title": "SkyWays · day 75, a bill 4.4 times the estimate with flat traffic",
   "body": "Traffic was flat, so behaviour had changed, and behaviour is only visible per call. Four "
           "ratios explained it: tokens per call 1.6, frontier tier share 1.5, cache hit ratio 1.3, "
           "retries per conversation 1.41 — and they multiply to 4.40. Four separate sensible "
           "decisions made by careful people. The order of the fixes was not the order of the "
           "ratios: retries had risen most in relative terms and contributed the smallest factor, so "
           "the context trim went first at half a day for 1.6x and the breaker went last. Four weeks "
           "had passed before anybody noticed, which is the part worth fixing permanently — an alert "
           "at three times the ratified cost per case, a watched cache hit ratio, and the caching and "
           "routing config in one file reviewed like code."},
 "pitfalls": [
   "A request id inside the cached block. The prefix never matches again, the hit ratio collapses, "
   "nothing errors, and the first symptom is an invoice a month later.",
   "A latency dashboard that flags very fast responses as suspected failures. Cache hits return fast, "
   "hundreds get reported as anomalies, and somebody proposes switching the cache off — which raises "
   "the bill by about a third within a day, because the anomaly was the cache working.",
   "An injection test that asserts on the model's wording. It goes red for the wrong reason after the "
   "next prompt edit and green for the wrong reason the week after, and nobody trusts it by month "
   "three.",
 ],
 "done_when": "A test asserts a cache read above zero on the second call, every agent loop has a cap, "
              "a passport number cannot reach a trace row, and the injection suite has a run dated "
              "this week.",
},
]
