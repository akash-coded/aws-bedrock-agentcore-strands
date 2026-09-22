"""DevOps and platform · steps 4-6."""

STEPS_B = [
{
 "n": 4, "id": "pipeline", "phase": "Pipeline",
 "title": "Make the harness a status check the merge cannot bypass",
 "when": "P1 into P2, before the first feature branch and before the first deadline",
 "purpose": (
   "CI for a system that is right *a share of the time* keeps every stage you already have and adds "
   "two: the evaluation harness, and a gate that reads its output per slice. The difference from "
   "ordinary CI is economic rather than technical. Tests are fast and free, so they run on everything; "
   "evaluation is slow and costs real money, so it cannot. The shape that works is the touched slice "
   "on every pull request, the full set nightly, cached model responses so a fixed golden set replays "
   "deterministically, and a required status check — because a gate a person can click past is a "
   "report."),
 "activities": [
   {"do": "Keep the fast, free stages first and unchanged",
    "detail": "Build, lint, types, unit tests, and the **exact** tests over the deterministic parts: "
              "the fare rules, the cap arithmetic, the schema validation. Most bugs in an agentic "
              "system are ordinary bugs, and they should fail in ninety seconds rather than after "
              "twelve minutes of paid evaluation."},
   {"do": "Run only the touched slice on a pull request",
    "detail": "A committed file maps paths to slices, so a change under the codeshare prompt runs the "
              "codeshare set. Ten minutes and a few dollars, not ninety minutes and a few hundred. The "
              "map is reviewed like code, because a wrong map is a silent gap in the gate."},
   {"do": "Run the full set nightly, and on any prompt or model change",
    "detail": "Those two changes touch every slice by definition, so the slice map does not apply to "
              "them. Wire that as a condition in the workflow rather than as a convention, because a "
              "convention is what gets skipped at 18:40 on a Thursday."},
   {"do": "Cache model responses so the golden set replays deterministically",
    "detail": "Key on (model version, prompt hash, input hash). A run over an unchanged golden set with "
              "an unchanged prompt should cost close to nothing and produce the same answer twice. When "
              "it does not, that divergence is itself the finding and you want to know immediately."},
   {"do": "Pin and version the judge",
    "detail": "The judge is a model call too. Pin its version, keep its prompt in the repository, and "
              "re-run the calibration set whenever either changes. An unpinned judge moves every score "
              "at once, which looks exactly like a product regression and costs a week."},
   {"do": "Gate on the per-slice score with its lower bound",
    "detail": "The gate reads the bar sheet the product manager owns and fails when any slice's 95% "
              "lower bound sits below its bar. One overall percentage is how the easy high-volume slice "
              "carries the average while the slice with the money in it ships broken."},
   {"do": "Make it a required status check in branch protection",
    "detail": "Not a job that posts a comment. If a human can merge past it while the room is waiting "
              "for a release, then eventually someone will, and the person who does it will be senior "
              "enough that nobody objects."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it write the workflow, the slice map and the cache key, then prove the cache works by "
           "running the golden set twice and diffing the cost. Two runs and one number is the whole "
           "test, and it takes five minutes.",
    "caution": None},
   {"tool": "Claude Code",
    "use": "Have it build the report step: per slice, score, n, lower bound, bar, pass or fail, "
           "rendered as a job summary rather than buried in a log. The shape of the readout decides "
           "whether anyone reads it.",
    "caution": "Check the lower-bound arithmetic yourself, once, by hand. A gate computing the wrong "
               "interval passes everything, and nothing about it looks broken."},
   {"tool": "Chat LLM, cheap tier",
    "use": "Maintain the file-to-slice map: given a diff, which slices could this plausibly touch? "
           "Useful as a suggestion that a human confirms into the committed map.",
    "caution": "It will under-select. Default to running more slices whenever the mapping is ambiguous, "
               "because the failure mode of running too few is the one that produces no signal at all."},
   {"tool": "Do not delegate",
    "use": "The decision to merge past a red check. There are legitimate reasons to do it, and every "
           "one of them is a named person accepting a named risk in writing.",
    "caution": None},
 ],
 "artifact": {
   "name": "Pipeline definition and the slice map",
   "good": "A pull request that cannot merge with any slice below its bar, a nightly full run, and a "
           "per-slice summary a product manager can read without opening a log or asking a question.",
   "owner": "Platform engineer, with the QA lead on the slice map"},
 "template": {
   "title": "CI with the harness as a required check", "lang": "yaml",
   "body": """# .github/workflows/agent-ci.yml
# Fast and free first. Slow and paid only on what changed.
name: agent-ci

on:
  pull_request:
  schedule:
    - cron: "0 2 * * *"        # the FULL set, nightly
  workflow_dispatch:

permissions:
  id-token: write              # OIDC. No long-lived keys in the repository.
  contents: read

concurrency:
  group: agent-ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -r requirements-dev.txt
      - run: ruff check . && mypy src
      - run: pytest tests/unit tests/exact -q   # caps, fare rules, schemas
      - run: python tools/check_no_bare_model_id.py environments/

  eval:
    needs: fast
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/<feature>-ci-eval
          aws-region: <eu-west-1>
      - name: Which slices did this change touch
        id: slices
        run: |
          # A prompt or model change touches everything, so the map does not apply.
          if [ "${{ github.event_name }}" != "pull_request" ]; then
            echo "slices=all" >> "$GITHUB_OUTPUT"
          else
            python tools/slice_map.py \\
              --diff "origin/${{ github.base_ref }}...HEAD" >> "$GITHUB_OUTPUT"
          fi
      - name: Restore the model response cache
        uses: actions/cache@v4
        with:
          # (model version, prompt hash, input hash). An unchanged golden set must
          # replay for near nothing and answer the same way twice.
          key: evalcache-${{ hashFiles('prompts/**', 'environments/eval.yaml') }}
          path: .evalcache
      - name: Harness
        run: python -m harness run --slices "${{ steps.slices.outputs.slices }}" --cache .evalcache
      - name: Judge, then gate
        run: |
          python -m harness judge --judge-version-from environments/eval.yaml
          python -m harness gate --bars docs/bar-sheet.yaml --summary "$GITHUB_STEP_SUMMARY"
        # gate exits non-zero when ANY slice's 95% lower bound is below its bar.
# Branch protection: `eval` is a REQUIRED status check. A job that only
# comments is a report, and reports do not stop releases.
"""},
 "prompts": [
   {"title": "Build the file-to-slice map",
    "when": "Setting the pipeline up, and again whenever a slice is added",
    "body": """Build the map from repository paths to evaluation slices, so a pull request runs
only the slices it could have affected.

OUTPUT SHAPE - a committed YAML file:
  slices:
    <slice-name>:
      paths: [<glob>, <glob>]
      cases: <path to the case file>
      bar: <n>
  always_full: [<globs that force the FULL set>]

RULES:
- Anything under the prompts directory, the model pin in any environment manifest, the
  judge prompt, or the harness itself goes in always_full. Those touch every slice.
- When a path could belong to two slices, put it in BOTH. Over-running costs money;
  under-running costs a gap in the gate that produces no signal.
- List any path that maps to no slice at all. That list is the gap, and I need it
  explicitly rather than by inference.

Then write the script that resolves a git diff to a slice list, and a test that proves
a change to a prompt returns "all".

OUR SLICES AND LAYOUT: <paste the tree and the slice names>"""},
   {"title": "Per-slice gate readout",
    "when": "The harness runs but nobody can read its output",
    "body": """Write the gate step that turns harness output into a decision.

OUTPUT SHAPE - a markdown job summary, in this exact order:
| Slice | Score | n | 95% lower bound | Bar | PASS / FAIL / UNPROVEN |
then one line: SHIP or DO NOT SHIP, and the single reason.

RULES:
- lower bound = p - 1.96 * sqrt(p*(1-p)/n). Compute it even when only the score was given.
- PASS only when the LOWER BOUND is at or above the bar. Score above the bar with the
  lower bound below it is UNPROVEN, and you must say how many more cases are needed:
  n = 1.96^2 * p * (1-p) / (p - bar)^2.
- Exit non-zero on any FAIL. UNPROVEN does not block, but it is reported at the top.
- Flag any slice that got worse than the previous run even if it still passes.
- Print the cost and wall-clock time of the run as the last line. People need to see it
  to keep believing in it.

Show me the lower-bound function and its unit test first; I want to check that by hand."""},
   {"title": "Cost the pipeline before you switch it on",
    "when": "Before making the harness a required check, so nobody can argue it later",
    "body": """Work out what this pipeline will cost to run, so the number arrives before the
first invoice rather than after it.

Compute and show the arithmetic for:
1. Cost and wall-clock time of ONE full golden-set run, cold cache.
2. The same, warm cache, with the cache hit ratio you expect and why.
3. Cost per pull request at the average touched-slice size.
4. Monthly total at <n> pull requests per day plus one nightly full run.
5. The crossover: at how many pull requests per day does the nightly run stop being
   the dominant cost?

RULES:
- Use the gateway's actual price table, not a remembered figure. Say where you got it.
- Show cached and uncached input tokens as separate terms.
- Give me the single cheapest change that halves number 4, and what it costs in coverage.

INPUTS: <golden set size, tokens per case, model prices, PR volume>"""},
 ],
 "example": {
   "title": "SkyWays · the check that could be clicked past",
   "body": "For three weeks the harness ran on every pull request and posted a comment. Nobody disabled "
           "it and nobody ignored it on principle. Then on the Thursday before the pilot the codeshare "
           "slice came back red, the release was in the calendar, and a senior engineer merged with the "
           "comment open in another tab — reasonably, in the moment, and with every intention of fixing "
           "it on Monday. The fix afterwards was one setting: the harness became a required status "
           "check. The argument that setting ended had been running since the harness was built."},
 "pitfalls": [
   "Running the full evaluation on every push. It is slow and it is paid, so within a fortnight somebody "
   "makes it optional to unblock a release, and an optional gate is not a gate.",
   "Gating on one overall score. The easy slice is the high-volume one, so it lifts the average while the "
   "slice carrying the money fails quietly underneath it.",
   "An unpinned judge. Its version moves, every score moves with it, and a week goes into hunting a product "
   "regression that is actually a change in the measuring instrument.",
 ],
 "done_when": "A pull request with any slice below its bar cannot be merged, and the person who tried can "
              "see which slice and by how much without opening a log.",
},
{
 "n": 5, "id": "deploy", "phase": "Deploy",
 "title": "Ship behind a flag, and treat the prompt as a deployable artefact",
 "when": "The end of P2, at cut-over, and on every change after it",
 "purpose": (
   "The flag is the deployment primitive, because the rollback has to be faster than the incident. Four "
   "states, taken one at a time: **shadow**, where the agent decides on real traffic and acts on "
   "nothing; **5% canary**; **widen on evidence**; then all of it. The flag is also the rollback, which "
   "is why it gets tested rather than believed. The part teams miss is that code is not the only "
   "deployable thing here. A prompt change and a model version change alter behaviour with no build, so "
   "they need the same versioning, the same review and the same rollback path as the binary — and a "
   "prompt change is the most common production change there is."),
 "activities": [
   {"do": "Make shadow a state of the system, not a branch",
    "detail": "Same code path, same inputs, decisions written to the trace store, the write side "
              "disabled by the flag. A separate shadow branch tests the shadow branch, and the first "
              "live call then runs code nobody has exercised."},
   {"do": "Make 'shadow never writes' an automated test",
    "detail": "An assertion in the harness *and* a scheduled canary in production: with the flag in "
              "shadow, any call reaching a write tool fails the build and pages. The sentence in the "
              "runbook is a request; the assertion is the control."},
   {"do": "Blue/green the runtime and keep both warm through the window",
    "detail": "Two versions serving, traffic shifted by the flag rather than by DNS, the old one warm "
              "until the widening finishes. AgentCore runtime versions behind an alias, or two task "
              "sets behind a load balancer — the mechanism matters far less than being able to shift "
              "back in seconds without a deploy."},
   {"do": "Version the prompt and the model as first-class artefacts",
    "detail": "A prompt lives in the repository with a hash, ships as a versioned object, and is "
              "referenced *by version* at runtime. It gets a pull request, a harness run and a rollback "
              "path. Editing a prompt in a console is a behaviour change with no diff and nothing to go "
              "back to."},
   {"do": "Keep one flag per action, not one per feature",
    "detail": "Refunds can go back to gated while same-day rebooking stays at 100%. A single feature "
              "flag forces the whole feature to the caution of its riskiest action, so being careful "
              "about one thing means being slow about everything."},
   {"do": "Record the flag state and the prompt version in every decision",
    "detail": "Otherwise a trace from three weeks ago cannot be explained, because you no longer know "
              "which prompt produced it or whether it was live. This is two fields and it is the "
              "difference between an incident review and an argument."},
   {"do": "Write the widening condition before the cut-over, not during it",
    "detail": "The live lower bound at or above the bar on that slice for n consecutive days, gated "
              "actions still gated. Written while nobody is under pressure, because the conversation "
              "at 5% with a sponsor waiting is not the one in which to invent a threshold."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Write the shadow-never-writes test in both places: an assertion in the harness, and a "
           "scheduled production canary that checks it against the live flag state. Two places, because "
           "the flag can be changed outside a deployment.",
    "caution": None},
   {"tool": "Claude Code",
    "use": "Generate the flag configuration and the code's flag constants from one source, so the two "
           "cannot disagree. Then have it fail the build on an unknown flag key.",
    "caution": "Insist on that build failure. A typo in a flag name reads as `false` at runtime, which "
               "looks exactly like working code that is switched off on purpose."},
   {"tool": "Chat LLM",
    "use": "Given a prompt diff, list what behaviour could change and which slices would show it. Use "
           "it to decide what to watch after the change rather than what to skip before it.",
    "caution": "Run the full set on any prompt change regardless. The point of its list is to predict "
               "where to look, never to reduce what runs."},
   {"tool": "Do not delegate",
    "use": "When to widen. That is the product manager's gate on live evidence. The platform's job is "
           "to make widening a config change and the rollback a faster one.",
    "caution": None},
 ],
 "artifact": {
   "name": "Flag configuration and the deploy path",
   "good": "One flag per action, each with its state, its prompt and model version, its widening "
           "condition and its owner, deployed from the same source as the code — and a rollback a "
           "person has actually thrown.",
   "owner": "Platform engineer, with the product manager on the states"},
 "template": {
   "title": "Feature flags, one per action", "lang": "json",
   "body": """{
  "version": "1",
  "flags": {
    "rebook_same_day": {
      "name": "rebook_same_day",
      "description": "Reversible action. Widens on live evidence per slice, never on a date.",
      "attributes": {
        "mode": {"constraints": {"type": "string", "enum": ["off", "shadow", "canary", "on"], "required": true}},
        "canary_percent": {"constraints": {"type": "number", "minimum": 0, "maximum": 100}},
        "prompt_version": {"constraints": {"type": "string", "required": true}},
        "model_version": {"constraints": {"type": "string", "required": true}},
        "widen_when": {"constraints": {"type": "string", "required": true}},
        "owner": {"constraints": {"type": "string", "required": true}}
      }
    },
    "rebook_partner": {
      "name": "rebook_partner",
      "description": "Reversible with effort. Separate flag so it can stay in shadow while same-day runs live.",
      "attributes": {
        "mode": {"constraints": {"type": "string", "enum": ["off", "shadow", "canary", "on"], "required": true}},
        "canary_percent": {"constraints": {"type": "number", "minimum": 0, "maximum": 100}},
        "prompt_version": {"constraints": {"type": "string", "required": true}},
        "widen_when": {"constraints": {"type": "string", "required": true}},
        "owner": {"constraints": {"type": "string", "required": true}}
      }
    },
    "issue_refund": {
      "name": "issue_refund",
      "description": "Not reversible. The cap and the approver are ENFORCED in the tool signature and the IAM policy; these fields only mirror them for the trace.",
      "attributes": {
        "mode": {"constraints": {"type": "string", "enum": ["off", "shadow", "gated"], "required": true}},
        "cap_usd": {"constraints": {"type": "number", "minimum": 0, "required": true}},
        "approver_role": {"constraints": {"type": "string", "required": true}},
        "owner": {"constraints": {"type": "string", "required": true}}
      }
    }
  },
  "values": {
    "rebook_same_day": {
      "enabled": true,
      "mode": "canary",
      "canary_percent": 5,
      "prompt_version": "<git-sha>",
      "model_version": "eu.anthropic.<model-id>",
      "widen_when": "live lower bound >= 0.86 on same-day for 5 consecutive days",
      "owner": "<name>"
    },
    "rebook_partner": {
      "enabled": true,
      "mode": "shadow",
      "canary_percent": 0,
      "prompt_version": "<git-sha>",
      "widen_when": "codeshare harness lower bound >= 0.80 AND 14 days shadow agreement >= 0.95",
      "owner": "<name>"
    },
    "issue_refund": {
      "enabled": true,
      "mode": "gated",
      "cap_usd": 400,
      "approver_role": "<duty-manager>",
      "owner": "<name>"
    }
  }
}
"""},
 "prompts": [
   {"title": "Write the shadow-never-writes test",
    "when": "Before the shadow run starts, not after the first write",
    "body": """Write the control that makes "shadow never writes" true rather than intended.

Produce TWO things:
1. A harness assertion: run the full golden set with the flag in shadow and fail the
   build if any write tool is reached. It must detect the call at the tool boundary,
   not by inspecting the output.
2. A scheduled production canary: read the LIVE flag state, and if any action is in
   shadow, assert no write has been recorded for that action in the last hour. Page on
   failure.

RULES:
- Test at the boundary the agent actually crosses. A test on a mock passes forever.
- Two places, because the flag can be changed outside a deployment and often is.
- The canary must fail loudly when it cannot read the flag state. Unknown is not pass.
- Include the test that proves the test works: force a write and show both fail.

OUR WRITE TOOLS AND FLAG SOURCE: <paste>"""},
   {"title": "Turn a prompt change into a deployment",
    "when": "Somebody wants to 'just tweak the prompt'",
    "body": """Write the change record for this prompt change. Treat it as a deployment.

It must state:
1. The diff, and in plain words what behaviour is intended to change.
2. Which slices are expected to move, in which direction, and by roughly how much.
3. What runs before merge: the full golden set, the judge calibration set, the
   injection suite. Give the cost and wall-clock time.
4. The version identifier that ships (a hash, not "latest"), and where it is stored.
5. The rollback: which command, which previous version, how many seconds.
6. What in the trace will tell us afterwards which version decided a given case.

RULES:
- "Minor wording change" is not an entry. Every wording change is a behaviour change
  until the harness says otherwise.
- If the change is intended to fix a specific failing case, say which, and say what
  stops it from over-fitting to that case.

PROMPT DIFF: <paste>"""},
   {"title": "Plan the canary and its automatic rollback",
    "when": "Cut-over is scheduled and the flag states need deciding",
    "body": """Plan the canary for <action>, as a config, not as a narrative.

OUTPUT SHAPE:
| State | Share | Entry condition | Exit condition | Who decides | Rollback time |
for each of: shadow, 5%, <n>%, 100%.

Then the AUTOMATIC rollback: the metric, the threshold, the evaluation window, and
what it rolls back TO (a state, not "the previous version").

RULES:
- Every entry condition is evidence, never a date.
- Every state has an owner who can move it without an approval chain.
- Automatic rollback triggers must be things that cannot be explained away at 02:00:
  cost per case, error rate, cap trips, a write while in shadow.
- Say explicitly which actions never enter this ladder because they are gated.
- Give me the single condition most likely to be argued with, and rewrite it so it
  cannot be.

CONTEXT: <slices, bars, cases per day, current flag states>"""},
 ],
 "example": {
   "title": "SkyWays · what the shadow caught and the harness could not",
   "body": "The harness had same-day rebooking at 88% and the shadow run agreed with the human desk on "
           "96% of same-day cases. On fourteen cases it did not, and all fourteen were the same thing: "
           "the agent proposed a partner airline that the evening shift never uses after 18:00, because "
           "that partner's transfer desk closes. The rule was in nobody's spec and nobody's golden set; "
           "it lived in the heads of six people. It cost nothing to discover, because the write side "
           "was off. At cut-over the flag went to 5% for same-day only; partner rebooking stayed in "
           "shadow another fortnight, and refunds never left gated."},
 "pitfalls": [
   "One flag for the whole feature. Refunds then sit at the same setting as showing options, so the only "
   "way to be careful about the dangerous action is to be slow about every safe one.",
   "Shipping a prompt change outside the pipeline. It is a behaviour change with no build, no line in the "
   "release notes and nothing to roll back to — and it is the most common production change an agent gets.",
   "A shadow path that is a separate code branch. It proves the shadow branch works. The first live call "
   "then executes code that has never run against real traffic.",
 ],
 "done_when": "You can move any single action from on to shadow and back in under a minute through a "
              "recorded config change, and every trace says which flag state and prompt version produced it.",
},
{
 "n": 6, "id": "observe", "phase": "Observe",
 "title": "Instrument the three signals a normal stack does not have",
 "when": "Before the shadow run, not after the first surprise",
 "purpose": (
   "Your existing observability answers whether it is up and whether it is fast, and it will keep doing "
   "that. None of it answers the three questions this workload is actually judged on: what a case "
   "costs, what the system did and why, and whether its behaviour is drifting while every dashboard "
   "stays green. Each has a specific trap. Cost per case is meaningless unless cache hits are marked. "
   "The trace must mask rather than omit, or the row that would explain the incident is the row that "
   "was left out. And drift has no error and no deploy behind it, so it is visible only as a chart with "
   "a threshold on it."),
 "activities": [
   {"do": "Emit cost per case, with cache hits marked",
    "detail": "Input tokens, output tokens, **cached tokens**, model version and the derived cost, on "
              "one record keyed by case. Marking the cache hit is not tidiness: a cache hit counted as "
              "a fresh call inflates the bill you report, and a cache hit counted as a wrong answer "
              "gets a working system switched off, which is worse and has happened."},
   {"do": "Write one trace row per consequential action, redacted by masking",
    "detail": "Mask, never omit. `card ****4471` is a row you can reconcile; a missing row is an "
              "incident you cannot explain. Each row carries the case id, the action, the model "
              "version, the prompt version, the tools called, the cap that applied, the approver if "
              "there was one, tokens and cost."},
   {"do": "Use structured metrics rather than log scraping",
    "detail": "Embedded Metric Format on the log line, so the metric and the row that produced it are "
              "the same write and a cost number always has its case beside it. Or OpenTelemetry spans "
              "carrying the same attributes. A regex over a text log breaks the first time somebody "
              "reformats a message, and it breaks silently."},
   {"do": "Chart the output mix weekly and alarm at five percentage points",
    "detail": "The proportions of the decisions the agent makes — refund versus credit versus rebook. A "
              "probabilistic system changes behaviour when the world changes, with no deploy and no "
              "error. Five points week over week is this playbook's default starting threshold, and the "
              "alert re-opens the release gate automatically, which is what turns a chart into a control."},
   {"do": "Alarm on the three failure shapes specific to this workload",
    "detail": "Cost per case above three times the estimate, sustained for an hour — a retry loop or a "
              "context that has grown. Loop-cap trips above baseline — the agent is going in circles "
              "and the cap is quietly doing all the work. Cache hit ratio collapsing — somebody moved a "
              "timestamp to the front of the prompt and every call is now full price."},
   {"do": "Give the product manager the readout in the shape of their bar sheet",
    "detail": "Per slice, with the lower bound, not one number. The dashboard that gets read is the one "
              "shaped like the decision somebody has to make, and the shape is yours to choose."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Write the emitter and its unit tests, including a test that a known cached response produces "
           "cost near zero and `cache_hit true`. That single test is what protects the bill report from "
           "quietly becoming fiction.",
    "caution": None},
   {"tool": "Claude Code",
    "use": "Generate the alarms as infrastructure from a table of thresholds, so the thresholds are "
           "reviewable in one file rather than discovered in a console six months later.",
    "caution": "Check the period and the evaluation window yourself. An alarm on a one-minute period "
               "over sparse overnight traffic fires all night and is muted by Thursday."},
   {"tool": "Chat LLM",
    "use": "Paste a redacted trace row and ask what an incident reviewer could not answer from it. It is "
           "reliable at spotting the missing field, and a missing field is far cheaper to find now than "
           "during the incident.",
    "caution": "Redact before you paste, genuinely. The exercise is about the shape of the row, not its "
               "contents, so there is no reason for real values to be in it."},
   {"tool": "Do not delegate",
    "use": "Deciding what is masked and what is kept. That is a legal and contractual question about "
           "your own data, and the consequence of a wrong guess is either a leak or an incident nobody "
           "can explain.",
    "caution": None},
 ],
 "artifact": {
   "name": "Trace schema, cost record and the alarm set",
   "good": "One record per consequential action that an incident reviewer can read cold twelve weeks "
           "later, a cost per case that stays correct when the cache is working, and alarms whose "
           "thresholds are written where they can be argued with.",
   "owner": "Platform engineer"},
 "template": {
   "title": "Trace and cost emitter", "lang": "python",
   "body": """# trace.py - one write per consequential action: the metric and the row that
# produced it, in the same CloudWatch Logs record (Embedded Metric Format).
# Rule: MASK, never omit. A masked field is a row you can reconcile; a missing
# row is an incident you cannot explain.
import json
import time
from decimal import Decimal

NAMESPACE = "<feature>/agent"

# Per 1k tokens, read from the gateway price table at start-up. Never a guess.
PRICES = {"<model-id>": {"in": Decimal("<n>"), "cached": Decimal("<n>"), "out": Decimal("<n>")}}


def mask(value, keep=4):
    # Keep the shape, lose the content: '************4471', not a dropped column.
    if not value:
        return ""
    return "*" * max(0, len(value) - keep) + value[-keep:]


def cost_usd(model, tokens_in, cached_in, tokens_out):
    p = PRICES[model]
    fresh_in = max(0, tokens_in - cached_in)
    return (Decimal(fresh_in) * p["in"]
            + Decimal(cached_in) * p["cached"]
            + Decimal(tokens_out) * p["out"]) / 1000


def emit(case_id, slice_name, action, model, prompt_version, flag_state,
         tokens_in, cached_in, tokens_out, loops, cap_usd, approver,
         passenger_ref, outcome):
    print(json.dumps({
        "_aws": {
            "Timestamp": int(time.time() * 1000),
            "CloudWatchMetrics": [{
                "Namespace": NAMESPACE,
                "Dimensions": [["Environment", "Slice", "Action"]],
                "Metrics": [{"Name": "CostPerCaseUsd", "Unit": "None"},
                            {"Name": "Loops", "Unit": "Count"},
                            {"Name": "CacheHit", "Unit": "Count"}],
            }],
        },
        "Environment": "<prod>",
        "Slice": slice_name,
        "Action": action,
        "CostPerCaseUsd": float(cost_usd(model, tokens_in, cached_in, tokens_out)),
        "Loops": loops,
        # MARKED. A cache hit counted as a fresh call inflates the bill you report.
        # A cache hit counted as a wrong answer gets a working system switched off.
        "CacheHit": 1 if cached_in > 0 else 0,
        "CachedTokens": cached_in,
        # The row an incident reviewer reads cold, twelve weeks later:
        "case_id": case_id,
        "passenger_ref": mask(passenger_ref),
        "model_version": model,
        "prompt_version": prompt_version,
        "flag_state": flag_state,
        "cap_usd": str(cap_usd),
        "approver": approver or "none",
        "outcome": outcome,
    }))
"""},
 "prompts": [
   {"title": "Design the trace row from an incident you will have to explain",
    "when": "Before the shadow run, while the schema is still cheap to change",
    "body": """Design the trace row by working backwards from the incident.

THE INCIDENT I must be able to explain twelve weeks later:
<paste: e.g. "the agent issued a refund above the cap and nobody knows how">

1. List every question an incident reviewer, a regulator and a finance analyst would
   each ask about that case.
2. For each question, name the field that answers it.
3. Produce the schema: field name, type, masked or plain, retention, and WHICH of the
   questions it exists for. A field that answers no question comes out.
4. Mark every field that carries personal data and state how it is masked. MASK, never
   omit - say what shape survives masking and why that is enough to reconcile.

RULES:
- No field exists "just in case". Each one is justified by a question.
- If a question cannot be answered by any field, say so plainly. That gap is the output
  I am looking for.
- Include model version, prompt version, flag state, the cap that applied and the
  approver. If you think any of those is unnecessary, argue for removing it explicitly."""},
   {"title": "Generate the alarm set from a threshold table",
    "when": "Before cut-over, so the thresholds exist in a file rather than in a console",
    "body": """Turn this threshold table into CloudWatch alarms as infrastructure as code.

ALARMS REQUIRED, at minimum:
- Cost per case above 3x the estimate, sustained for 1 hour
- Loop-cap trips per hour above <n> (the cap is doing work that should not be needed)
- Cache hit ratio below <n>% over 6 hours (a prompt prefix changed and every call is
  now full price)
- Output mix moved more than 5 percentage points week over week

RULES:
- State the statistic, period, evaluation periods, datapoints-to-alarm and
  treat-missing-data for each, and justify each choice in a comment.
- No alarm on a one-minute period over sparse traffic. Say what our traffic actually is
  and size the window to it.
- Every alarm names what the responder should DO. An alarm with no action is a chart.
- The drift alarm must trigger the release-gate re-open, not just a notification. Show
  how that is wired.

OUR THRESHOLDS AND TRAFFIC: <paste>"""},
   {"title": "What can this dashboard not answer",
    "when": "After the dashboard exists and before you rely on it",
    "body": """Here is our observability setup: <paste dashboards, metrics, alarms, trace schema>.

Answer only this: which of these questions can it NOT answer, and what is missing?

1. What did case <id> cost, and was any of it a cache hit?
2. Which model version and prompt version decided case <id>?
3. Has the mix of outcomes changed this week versus last?
4. How many cases hit the loop cap yesterday, and did they end at the desk?
5. Which slice is getting more expensive per case, month over month?
6. Did anything write while an action was in shadow?
7. Who approved the last twenty gated actions?

OUTPUT SHAPE:
| Question | Answerable now? | What is missing | Cost to add |

RULES:
- "It is in the logs somewhere" is a NO. Answerable means one query.
- Rank what is missing by what it would cost us during an incident, not by effort."""},
 ],
 "example": {
   "title": "SkyWays · the four habits, found in an afternoon",
   "body": "On day 75 the bill was 4.4 times its estimate. There was no runaway and no single cause. "
           "There were four ordinary habits multiplying: the whole conversation resent as context on "
           "every turn (1.6x), the capable model used for classification as well as for the judgement "
           "call (1.5x), a cache being missed because a timestamp sat at the front of the prompt "
           "(1.3x), and uncapped retries (1.41x). Multiply those and you get 4.4. Finding it took an "
           "afternoon rather than a fortnight, and only because the per-call log carried tokens, "
           "**cached tokens** and a feature column on every row. Without the cached-token column the "
           "third habit is invisible — and the third habit is the one that is free to fix."},
 "pitfalls": [
   "Counting a cache hit as a fresh call, or worse, as a failure. The first overstates the bill; the second "
   "has got a working system switched off by a team that believed its accuracy had collapsed overnight.",
   "Redacting by omission. The schema passes review, the incident arrives, and the row that would have "
   "explained it is precisely the row that was dropped for safety.",
   "Scraping cost metrics out of text logs. The regex survives until somebody reformats a message, and then "
   "it fails silently: the chart goes flat, which reads as good news.",
 ],
 "done_when": "For any case in the last thirty days you can produce, in one query, what it cost, which "
              "model and prompt version decided it, what it did and who approved it — with nothing "
              "unmasked that should not be.",
},
]
