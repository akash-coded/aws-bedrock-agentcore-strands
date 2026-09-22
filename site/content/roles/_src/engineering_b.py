"""Engineering lead · steps 4-6."""

STEPS_B = [
{
 "n": 4, "id": "layer", "phase": "Layer",
 "title": "Add the model calls, and an independent checker after the risky ones",
 "when": "Once the floor is green, mid-bolt",
 "purpose": (
   "The best-guess layer goes on top of the floor: ranking, drafting, classifying — the work that is "
   "right a share of the time and has to be measured rather than asserted. Chains multiply, so keep "
   "them short, then put a checker after the steps where a wrong answer is **costly and easy to "
   "miss**. The checker only earns its call if it is independent. A model reviewing its own output "
   "shares its own blind spots, which is why *review your answer before returning it* changes nothing "
   "measurable and still appears on the invoice."),
 "activities": [
   {"do": "Count the chain before you build it",
    "detail": "Four steps at 90% each is 0.66 end to end, and it fails fluently. The first fix is "
              "always to shorten the chain: two of any six steps are usually exact work that crept "
              "into a prompt and belongs in the previous step."},
   {"do": "Place checkers where a mistake is costly AND easy to miss",
    "detail": "After choosing the flights and after drafting the passenger message. Not after "
              "computing the fare, which needs a unit test, and not after writing the trace row, "
              "which is exact. Every checker is a call you pay for on every case."},
   {"do": "Make the checker independent, and record which kind",
    "detail": "A different model, or the same model in a fresh context with an adversarial brief — "
              "*find what is wrong*. Write which one you chose in a comment beside it, because the "
              "next person to touch this will assume the cheap version was intended."},
   {"do": "Pass the constraints and the output, never the drafter's reasoning",
    "detail": "The reasoning is the contamination. Send the rules the output must satisfy and the "
              "artefact to be judged, and nothing that explains why the drafter believed it was fine, "
              "because that explanation was written to be convincing."},
   {"do": "Treat a fail as a re-draft, and cap the rounds at two",
    "detail": "A warning gets logged and ignored. Two rounds, then escalate to a person. An uncapped "
              "re-draft loop looks like diligence on a good day and is the same runaway as a missing "
              "loop cap on a bad one."},
   {"do": "Log the checker's verdict as its own trace field",
    "detail": "Pass or fail, plus the round number. Without it you cannot tell a chain that never "
              "fails from a checker that never fires, and on a dashboard those two look identical."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it implement the draft, check and re-draft loop against your interfaces, with the "
           "round cap and the verdict logging in the first version rather than as a follow-up ticket "
           "that never gets picked up.",
    "caution": "Read what it passes to the checker. The obvious implementation forwards the whole "
               "conversation, which is precisely the contamination the checker exists to avoid."},
   {"tool": "A second model as the checker",
    "use": "Genuinely different weights, an adversarial brief and a rubric. This is the version that "
           "finds things, and it is the version you can defend to QA when they ask what independent "
           "means here.",
    "caution": "It is a second bill on every case. Place it only where the architect's map says "
               "costly and easy to miss, and be able to name the cases that justified it."},
   {"tool": "A chat surface",
    "use": "Draft the adversarial rubric: the failure modes the checker must look for, in the order "
           "a good reviewer would look for them.",
    "caution": "A rubric written from imagination finds imagined problems. Build the first version "
               "from the last twenty real disagreements, then extend it from first principles."},
   {"tool": "Do not delegate",
    "use": "Deciding which steps get a checker at all. It is a cost and risk trade-off across the "
           "whole chain, and a model asked step by step will recommend one everywhere, because each "
           "one is sensible in isolation.",
    "caution": None},
 ],
 "artifact": {
   "name": "Checker implementation",
   "good": "A named checker after each risky generating step, independent by construction, capped at "
           "two re-drafts, with the verdict and round number in the trace. Placement written down "
           "with the reason beside it, so it can be argued with.",
   "owner": "Engineering lead"},
 "template": {
   "title": "The best-guess layer with an independent checker", "lang": "python",
   "body": r"""# src/agent/checked_step.py — the best-guess layer, checked independently.
# Independence here means <a different model family>. If that changes, QA is told.
from dataclasses import dataclass

from src.models import call          # call(model, system, user) -> str
from src.trace import trace

DRAFTER = "<drafting-model-id>"
CHECKER = "<a-different-model-id>"
MAX_REDRAFTS = 2

ADVERSARIAL = (
    "You are reviewing work you did not produce. Find what is wrong. You are\n"
    "given the CONSTRAINTS and the OUTPUT only, never the author's reasoning,\n"
    "and you must not ask for it. Reply PASS, or FAIL and one line per breach."
)


class NeedsAPerson(Exception):
    pass


@dataclass(frozen=True)
class Checked:
    output: str
    rounds: int


def checked_step(system: str, user: str, constraints: str, step: str) -> Checked:
    # Draft, check independently, re-draft at most twice, then escalate.
    feedback = ""
    for attempt in range(MAX_REDRAFTS + 1):
        draft = call(DRAFTER, system, user + feedback)
        # Constraints and output ONLY. The drafter's reasoning is the contamination.
        brief = f"CONSTRAINTS:\n{constraints}\n\nOUTPUT TO JUDGE:\n{draft}"
        verdict = call(CHECKER, ADVERSARIAL, brief)
        passed = verdict.strip().startswith("PASS")
        trace.write(step=step, round=attempt, checker=CHECKER,
                    checker_verdict="pass" if passed else "fail")
        if passed:
            return Checked(draft, attempt)
        feedback = f"\n\nA reviewer rejected the previous attempt:\n{verdict}"
    raise NeedsAPerson(f"{step}: {MAX_REDRAFTS} re-drafts rejected")


# tests/agent/test_checked_step.py
import pytest


def test_the_checker_never_sees_the_drafters_reasoning(spy):
    checked_step(system="<...>", user="<...>", constraints="<...>", step="<rank>")
    sent = spy.calls_to(CHECKER)[0].user
    assert sent.startswith("CONSTRAINTS:") and "OUTPUT TO JUDGE:" in sent
    assert "<thinking>" not in sent and "because I" not in sent


def test_escalates_to_a_person_after_two_redrafts(always_fails):
    with pytest.raises(NeedsAPerson):
        checked_step("<...>", "<...>", "<...>", step="<rank>")
"""},
 "prompts": [
   {"title": "Decide where the checkers go",
    "when": "You have the chain and the architect's map",
    "body": r"""Here is the chain of steps for <feature>, with the architect's exact / best-guess
map beside it: <paste>.

For EACH step, output a row:
| Step | Exact or best-guess | Cost of a wrong answer | Easy to miss? | Checker? | Why |

RULES:
- An EXACT step never gets a checker. It gets a unit test. Say so on those rows.
- Recommend a checker ONLY where a wrong answer is both costly AND easy to miss. A
  wrong answer that the next step would reject anyway does not need one.
- Every checker is a model call on every case. Give me the estimated added cost per
  case for your recommendations, as a total.
- Then compute the end-to-end product of the per-step accuracies I gave you, and tell
  me whether SHORTENING the chain would buy more than any checker you proposed.

Finish with the single step you would check first if I could only afford one."""},
   {"title": "Write the adversarial checker brief",
    "when": "Implementing the checker",
    "body": r"""Write the system prompt for an INDEPENDENT checker on this step: <describe>.

The checker will receive the CONSTRAINTS and the OUTPUT. It will never receive the
drafter's reasoning, and it must not ask for it.

The brief must:
- tell it plainly that it is reviewing work it did not produce, and to find what is wrong
- list the failure modes to look for, in the order a good reviewer would check them
- fix the reply shape: PASS, or FAIL followed by one line per violated constraint
- forbid rewriting the output; its job is a verdict, not a draft

RULES FOR YOU:
- Build the failure-mode list from the real disagreements I paste below, not from first
  principles. Anything you add from imagination, mark INVENTED.
- Do not include praise, encouragement or any instruction to be balanced. A checker that
  is being fair is a checker that is passing things.

REAL DISAGREEMENTS: <paste>
CONSTRAINTS THE OUTPUT MUST SATISFY: <paste>"""},
   {"title": "Audit a checker that is not finding anything",
    "when": "You added a review step and quality did not move",
    "body": r"""Here is our checker implementation and a sample of its inputs: <paste>.

Answer these five, in order, and stop at the first NO:

1. Is the checker a DIFFERENT model, or the same model in a genuinely fresh context?
2. Is the drafter's reasoning excluded from what the checker receives? Quote the exact
   lines of code that exclude it, or say it is not excluded.
3. Does the brief tell it to find what is WRONG, or to review and confirm?
4. Is there a cap on re-draft rounds, and does exceeding it escalate to a person rather
   than returning the last draft?
5. Is the verdict written to the trace on every case, pass and fail alike?

Then tell me the pass rate over the sample. A checker that has passed everything is
either unnecessary or broken, and those two are distinguished by the sample, not by
opinion. Say which one this is and what evidence would settle it."""},
 ],
 "example": {
   "title": "SkyWays · the review step that changed nothing",
   "body": "A *review your answer before returning it* step was added after the ranking call. Scores "
           "did not move and the bill rose by about a fifth. The model was reading its own output "
           "with its own reasoning still in context, so it agreed with the same wrong flight choice "
           "it had just made, confidently, every time. Replacing it with a different model, given the "
           "constraints and the ranked list and nothing else, moved the codeshare slice by four "
           "points and — more usefully — started producing fails, which was the first evidence the "
           "checker was doing anything at all. The cap of two re-draft rounds was added the same day, "
           "after one case went round eleven times before anyone read the log."},
 "pitfalls": [
   "'Review your answer before returning it.' Same model, same context, same blind spots. It costs a "
   "call per step and moves no number you can point at.",
   "Forwarding the whole conversation to the checker. The drafter's reasoning was written to be "
   "convincing, and a checker that reads it is convinced.",
   "An uncapped re-draft loop. It looks like diligence until the day a case cannot be fixed, and then "
   "it is a runaway with better manners, burning tokens until somebody reads the bill.",
 ],
 "done_when": "Every checker in the chain can be shown to be independent — a different model, or a "
              "fresh context with an adversarial brief — and a test proves the drafter's reasoning "
              "never reaches it.",
},
{
 "n": 5, "id": "gate", "phase": "Gate",
 "title": "Put the boundary in the tool signature",
 "when": "Before the first bolt that writes anything",
 "purpose": (
   "The prompt says *never refund over $400*. A passenger types *ignore your instructions* and the "
   "model calls `refund(5000)`. The cap was a sentence, and a sentence is a request a model can be "
   "talked past. A typed, bounded parameter that raises is a boundary, and it holds whatever the "
   "model has been convinced of. Reads stay open; writes need a confirmation token the model cannot "
   "mint. Keep the sentence in the prompt as **policy**, because it makes the agent behave well by "
   "default — and never confuse it with enforcement."),
 "activities": [
   {"do": "Take every cap out of the prompt and into config",
    "detail": "`config/caps.yaml`, reviewed like code, generated from the authority budget. A number "
              "that lives in prose gets edited by whoever is editing prose, which is nobody who "
              "thinks of themselves as changing a control."},
   {"do": "Make the parameter typed and bounded, and make it raise",
    "detail": "Not clamp, not log, not warn. Raise. A clamped refund of $400 on a $5,000 attempt is a "
              "successful attack wearing a smaller number, and the trace shows an ordinary refund."},
   {"do": "Mint the confirmation token somewhere the model cannot reach",
    "detail": "The approver's screen. Signed, scoped to one booking and one amount, with an expiry. "
              "If the agent can construct the token from things it already has, it is a parameter "
              "with a serious-sounding name."},
   {"do": "Separate reads from writes at the permission layer",
    "detail": "Reads open, writes gated, two modules and two permission sets, so the agent cannot "
              "call what the job does not need. Least authority is from 1975 and has not changed; "
              "what changed is that the thing being restricted can be persuaded."},
   {"do": "Write the two tests, and treat them as the step",
    "detail": "Over-cap raises. No-confirmation raises. Until both are green the gate does not exist, "
              "whatever the design document says and however many people remember agreeing to it."},
   {"do": "Keep the prompt sentence, and label it POLICY",
    "detail": "A comment beside it: *policy, not enforcement — the boundary is in issue_refund()*. "
              "That comment is what stops the next engineer removing the signature check on the "
              "grounds that the prompt already covers it."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Give it the authority budget and have it generate the signature, the exception classes "
           "and the two tests for every tool at R3 and above in one pass. It is mechanical work with "
           "a fixed shape and a fixed test.",
    "caution": "Check that it raises rather than clamps, and that the cap is read from config rather "
               "than written as a literal. Both are defaults it reaches for, and both look fine in a "
               "diff."},
   {"tool": "A chat surface",
    "use": "Paste the prompt directory and ask for every sentence that is really a control: every "
           "`never`, `always`, `do not`, `ask before`, and every currency symbol. Each hit is a "
           "request that may need an enforced twin.",
    "caution": "It will also flag genuine policy that should stay as prose. The filter is whether "
               "ignoring the sentence costs money, exposes data or changes something irreversible."},
   {"tool": "An editor agent",
    "use": "Have it write the review-band path rule from the authority budget, so the files behind "
           "each tool carry that tool's band and nobody classifies their own change.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "What a cap is set to, and who may mint the token. Those come from the authority budget "
           "and the PM's autonomy record; a model asked for a sensible cap returns a plausible number "
           "with nothing behind it.",
    "caution": None},
 ],
 "artifact": {
   "name": "Gated tool implementation",
   "good": "Every write tool with a typed bounded parameter, a confirmation token it cannot mint, and "
           "two tests that were red first. Caps in config, reviewed like code, and the prompt "
           "sentence still there and labelled as policy.",
   "owner": "Engineering lead"},
 "template": {
   "title": "A gated write tool, and the two tests that are the step", "lang": "python",
   "body": r"""# src/tools/refund/issue.py   band R4   two named reviewers, every time
# The cap lives in <config/caps.yaml> and is reviewed like code.
# The prompt's sentence about refunds is POLICY. This file is ENFORCEMENT.
from decimal import Decimal

from src import ledger
from src.config import caps
from src.tools.confirm import ConfirmToken   # minted only by the approver's screen
from src.trace import trace

REFUND_CAP = Decimal(caps["refund"]["max_amount"])      # <400>
MODEL_VERSION = "<model-id-and-date>"


class AuthorityExceeded(Exception):
    def __init__(self, amount: Decimal, cap: Decimal) -> None:
        super().__init__(f"refund {amount} exceeds cap {cap}")
        self.amount, self.cap = amount, cap


class ConfirmationRequired(Exception):
    pass


def issue_refund(booking_id: str, amount: Decimal,
                 confirmation: ConfirmToken) -> ledger.Refund:
    # Raise, never clamp. A clamped 400 on a 5000 attempt is a successful attack
    # wearing a smaller number, and the trace records an ordinary refund.
    if amount > REFUND_CAP:
        trace.write(action="refund_refused", reason="over_cap",
                    booking=booking_id, amount=amount, model=MODEL_VERSION)
        raise AuthorityExceeded(amount, REFUND_CAP)
    if not confirmation.valid_for(booking_id, amount):
        trace.write(action="refund_refused", reason="no_confirmation",
                    booking=booking_id, amount=amount, model=MODEL_VERSION)
        raise ConfirmationRequired(booking_id)
    trace.write(action="refund", booking=booking_id, amount=amount,
                approver=confirmation.approver, model=MODEL_VERSION)
    return ledger.refund(booking_id, amount)


# tests/tools/test_refund_boundary.py — these two tests ARE the step.
import pytest

from tests.factories import forged_token, valid_token


def test_over_cap_raises():
    with pytest.raises(AuthorityExceeded):
        issue_refund("<PNR123>", Decimal("5000"), valid_token("<PNR123>", "5000"))


def test_no_confirmation_raises():
    with pytest.raises(ConfirmationRequired):
        issue_refund("<PNR123>", Decimal("50"), forged_token())


def test_reads_stay_open():
    # The gate is on the write, not on the module. A lookup needs no token.
    assert ledger.get_refunds("<PNR123>") is not None
"""},
 "prompts": [
   {"title": "Find every rule that is only a request",
    "when": "Before the first gated write, and after every prompt change",
    "body": r"""Search every prompt, system message and tool description under <src/prompts/> and
<src/tools/> for sentences that are really controls: never, always, must not, do not,
ask before, requires approval, and every currency symbol or numeric limit.

OUTPUT a table:
| File and line | The sentence | What it would cost if ignored | ENFORCED VERSION |

RULES:
- "Cost if ignored" must be concrete: money moved, data exposed, something irreversible
  changed, or nothing. Write "nothing" where that is the honest answer.
- The ENFORCED VERSION column is a typed bounded parameter, a confirmation token, a
  permission, or "stays as policy". Do not write "a clearer prompt" — that is the same
  request in better handwriting.
- Separate the rows into ACT NOW (money, data, irreversible) and LEAVE AS POLICY.
- Do not modify any file.

Finish with the count in each group. Teams commonly find between three and ten in the
first group, and the count matters less than the fact that nobody knew it."""},
   {"title": "Generate the gated signature and its two tests",
    "when": "Implementing any tool at R3 or above",
    "body": r"""Here is the authority budget row for this tool: <paste>.
Here is the existing unguarded implementation: <paste>.

Produce:
1. The typed signature, with the bounded parameter and a confirmation token parameter.
2. Named exception classes: one for over-cap, one for missing or invalid confirmation.
3. The two tests: over-cap RAISES, no-confirmation RAISES.
4. A trace write on the refusal path as well as the success path.

RULES:
- RAISE. Do not clamp to the cap, do not log and continue, do not return an error object.
- Read the cap from <config/caps.yaml>. No numeric literal anywhere in the function.
- The confirmation token must be validated against BOTH the booking id and the amount,
  so a token minted for a small refund cannot authorise a large one.
- Do not touch the prompt. The sentence there stays, as policy.

Then list anything in the authority budget row that the signature cannot express, so I
can take it back to the architect rather than approximate it here."""},
   {"title": "Write the review-band path rule",
    "when": "The queue is long and every change is being reviewed the same way",
    "body": r"""Turn this authority budget into a path rule that assigns a review band to every
file in the repository: <paste budget>. Here is the repository tree: <paste>.

OUTPUT a YAML file mapping R5 down to R1 to path globs, plus the review policy each
band implies (how many readers, and whether a person is required at all).

RULES:
- A change inherits the band of the most dangerous tool it touches. Size is irrelevant:
  three lines in a refund cap is the highest band there is; four hundred lines of help
  text cannot move money.
- The config file holding the caps gets the same band as the tool it caps.
- Never let the author assign the band. The rule is in the repository and it applies.
- Any path you cannot classify goes in an UNCLASSIFIED list for me, not into R1.

Then estimate, from last month's merged changes that I paste below, how many review
slots the new policy needs versus the current one.

LAST MONTH'S CHANGES: <paste>"""},
 ],
 "example": {
   "title": "SkyWays · day 82, five layers and none enforced",
   "body": "A $2,000 refund went out that was not owed. The design listed five layers: input marked "
           "as data, the prompt's policy, a $400 cap, a named approver, an alert on the trace. Two of "
           "them were written down — in the prompt — which is exactly why everybody in the room "
           "believed there was a cap and the ledger disagreed. With either the cap or the approver "
           "enforced in the signature, the refund is impossible; injection defence and traces change "
           "the odds and the visibility, not the outcome. The fix was about thirty lines and two "
           "tests, and the $400 constraint had been on the table since day six, when it reshaped "
           "three of the nine ratified NFRs."},
 "pitfalls": [
   "Clamping instead of raising. The attempt succeeds at the cap, no exception is recorded, and the "
   "trace shows a normal refund on the day somebody was probing you.",
   "A confirmation token the agent can construct. If it can be derived from the booking id the model "
   "already holds, it is a parameter with a serious-sounding name and no gate behind it.",
   "Deleting the prompt sentence once the signature is in place. The sentence is what makes the agent "
   "behave well by default; the signature is what holds when it does not. Keep both, and label which "
   "is which.",
 ],
 "done_when": "For every tool at R3 or above, `test_over_cap_raises` and `test_no_confirmation_raises` "
              "are green, and the cap appears nowhere outside the config file and the signature.",
},
{
 "n": 6, "id": "harness", "phase": "Harness",
 "title": "Wire the eval harness into CI, in cost order",
 "when": "P1, before the first bolt whose done-when mentions a bar",
 "purpose": (
   "The acceptance bar stops being a paragraph and becomes a check that can go red. The order "
   "matters, because the cheap definitive checks should reject before you pay for a judge: build, "
   "then the exact tests, then the golden run on the slice this change touched, then the independent "
   "judge, then the score against the bar **per slice**, then merge or reject. The rule that gives "
   "the harness its teeth is that a slice below its bar blocks the merge however good the overall "
   "number looks."),
 "activities": [
   {"do": "Put the steps in cost order and keep them there",
    "detail": "Build, exact tests, golden run, judge, score. Running the judge first spends a "
              "frontier model's money grading outputs the schema check would have rejected for "
              "nothing, on every run, forever."},
   {"do": "Score per slice, never in aggregate",
    "detail": "Every golden case carries a slice tag and the harness prints a row per slice against "
              "that slice's bar. A single percentage is the precise thing the harness exists to stop "
              "you reporting."},
   {"do": "Make the per-slice rule a required check",
    "detail": "Not a bot comment. A comment gets read on a quiet week and scrolled past on a release "
              "week, and a release week is when it matters. A required status check is the only "
              "version that survives pressure."},
   {"do": "Run the touched slice per pull request, the full set nightly",
    "detail": "That is the cost control on the harness itself. Deriving the touched slice from the "
              "changed paths is a ten-line script, and it is what keeps the per-change bill flat as "
              "the golden set grows from fifty cases to five hundred."},
   {"do": "Print n and the lower bound beside every score",
    "detail": "The bar is met by the lower bound, not by the point estimate. A slice with forty cases "
              "has proven nothing, and the score alone will not say so — it will look like a pass."},
   {"do": "Pin the judge and record its version in the run",
    "detail": "A judge that silently changes model is a harness whose results are not comparable week "
              "to week, and you will spend a day hunting a regression in code that did not change."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it write the workflow, the slice-from-changed-paths script and the per-slice report, "
           "then replay the whole thing against last month's merged commits to show it would have "
           "caught the regression it should have caught.",
    "caution": "Insist on the replay. A harness that has never rejected anything has not been tested, "
               "it has been installed, and the difference only becomes visible during an incident."},
   {"tool": "An editor agent",
    "use": "Keep the slice tags honest: when a new tool or path appears, have it flag the golden "
           "cases that now belong to no slice, and the slices that now have no cases.",
    "caution": None},
   {"tool": "A cheap tier",
    "use": "Use it as the schema and exact-check runner inside the harness. Those steps are "
           "deterministic and there is nothing a frontier model adds to reading JSON.",
    "caution": "Pin it. A cheap tier that changes underneath you makes a deterministic step "
               "non-deterministic, which is the worst of both arrangements."},
   {"tool": "Do not delegate",
    "use": "The bar values and the contents of the golden set. The bars are the PM's, derived from "
           "damage over saving; the cases are the QA lead's. Your job is to make them run and to "
           "refuse to average them.",
    "caution": None},
 ],
 "artifact": {
   "name": "Eval harness in CI",
   "good": "A required check running in cost order, reporting a row per slice with n and the lower "
           "bound, rejecting when any touched slice sits below its bar. Full set nightly, with the "
           "trend kept so a slow regression is visible.",
   "owner": "Engineering lead"},
 "template": {
   "title": "harness.yml · the required check", "lang": "yaml",
   "body": r"""# .github/workflows/harness.yml · <repo> — a REQUIRED check, not a bot comment.
# The order is cost order: the cheap definitive checks reject before the judge is paid.
name: harness

on:
  pull_request:
  schedule:
    - cron: "0 2 * * *"          # the full set, nightly

env:
  JUDGE_MODEL: "<pinned-judge-model-id>"   # pinned: a drifting judge is not comparable
  GOLDEN_SET: "<tests/golden/*.jsonl>"     # QA owns the cases; every case has a slice tag
  BARS: "<config/bars.yaml>"               # the PM owns these numbers, one per slice

jobs:
  harness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: "1 - build"
        run: make build

      - name: "2 - exact tests (schema, fare math, no waived tax)"
        run: make test

      - name: "3 - which slices did this change touch?"
        id: slices
        run: python tools/touched_slices.py --base "${{ github.event.pull_request.base.sha }}" >> "$GITHUB_OUTPUT"

      - name: "4 - golden run"
        run: |
          if [ "${{ github.event_name }}" = "schedule" ]; then
            make golden SLICES=all
          else
            make golden SLICES="${{ steps.slices.outputs.slices }}"
          fi

      - name: "5 - independent judge (tone, policy, false claims)"
        run: make judge MODEL="$JUDGE_MODEL"

      - name: "6 - score against the bar, PER SLICE"
        run: |
          # Prints score, n and the 95% lower bound on every row, and exits non-zero
          # if ANY touched slice is below its bar, however good the overall number is.
          make score BARS="$BARS" FAIL_UNDER_BAR=1 REPORT="$GITHUB_STEP_SUMMARY"

      - name: "7 - say why, in the summary"
        if: failure()
        run: echo "A slice is below its bar. The merge is blocked." >> "$GITHUB_STEP_SUMMARY"
"""},
 "prompts": [
   {"title": "Write the harness workflow in cost order",
    "when": "P1, wiring the bar into CI for the first time",
    "body": r"""Write the CI workflow for our eval harness. It runs on every pull request as a
REQUIRED check, and on a nightly schedule for the full set.

Steps, in THIS order, because it is cost order:
1. build
2. exact tests — schema, the money functions, the eligibility rules
3. work out which slices the changed paths touch
4. golden run — the touched slices on a pull request, ALL slices on the schedule
5. the independent judge, with a PINNED model id recorded in the run
6. score against the bar, per slice, printing score, n and the 95% lower bound

RULES:
- The job exits non-zero if ANY touched slice is below its bar. The overall number never
  rescues a failing slice, and the failure message must say which slice and by how much.
- No step may run before a cheaper step that could have rejected the same change.
- The judge model id is an env var, pinned, and appears in the run summary.
- Keep the whole thing under 60 lines of YAML.

Our slices: <list>. Our make targets: <list>. Our golden set lives at <path>."""},
   {"title": "Replay the harness against commits you already know about",
    "when": "Before you call the harness a gate",
    "body": r"""Here is our harness: <paste>. Here are <n> commits from the last month, with what
each one did and whether it turned out to be a regression: <paste>.

Replay the harness against each commit and report:
| Commit | Was it a regression? | Harness verdict | Correct? |

Then tell me:
- Every regression the harness would have MISSED, and the specific step that should have
  caught it — exact test, golden slice, or judge.
- Every clean commit the harness would have REJECTED, and why. A harness that rejects
  good changes gets switched off within a fortnight.
- The slice with the fewest cases, and whether its lower bound could clear its bar at
  that n at all.

Do not change the harness in this response. I want the evidence first."""},
   {"title": "Reshape the harness output into the bar sheet",
    "when": "The PM needs a release readout and the harness prints its own shape",
    "body": r"""Convert this harness output into the shape of the PM's bar sheet: <paste output>.
Here are the bars: <paste>.

ONE table, nothing else above it:
| Slice | Score | n | 95% lower bound | Bar | PASS / FAIL / UNPROVEN | vs last run |

RULES:
- lower bound = p - 1.96 * sqrt(p*(1-p)/n). Compute it even if the harness only gave a
  score. Under about 100 cases say USE WILSON beside the row.
- PASS only when the LOWER BOUND is at or above the bar. Score above bar with the lower
  bound below it is UNPROVEN, and then give cases needed:
  n = 1.96^2 * p * (1-p) / (p - bar)^2
- Flag any slice that got worse than the previous run even if it still passes.

Then one line: merge, or do not merge, and the single reason."""},
 ],
 "example": {
   "title": "SkyWays · day 45, 82.4 against a bar of 80",
   "body": "The codeshare slice scored 82.4% against a bar of 80% and the room read it as a pass. The "
           "harness printed n and the lower bound on the same row, and the lower bound said not yet. "
           "82% does not prove an 80% bar at any sample size the team was realistically going to "
           "collect, because the cases-needed formula has the gap squared in its denominator and the "
           "gap here was 2.4 points. The useful output was not pass or fail; it was the number of "
           "cases owed, on the same line. The other version of that day is a merge, a green tick, and "
           "a conversation about codeshare six weeks later with real passengers in it."},
 "pitfalls": [
   "Running the judge before the exact checks. You pay a frontier model to grade output a schema "
   "check would have rejected for free, on every run, for the life of the project.",
   "Reporting one number. The slice carrying the risk is small, the average hides it, and the first "
   "person to find out is whoever is on call.",
   "A harness that has never rejected anything. It has been proven to run, not to work. Replay it "
   "against a commit you already know was bad before you call it a gate.",
 ],
 "done_when": "A pull request that regresses any touched slice below its bar cannot be merged, and "
              "the check has been shown to reject on a commit you already knew was bad.",
},
]
