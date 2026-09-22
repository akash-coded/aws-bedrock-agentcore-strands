"""DevOps and platform · steps 7-8."""

STEPS_C = [
{
 "n": 7, "id": "protect", "phase": "Protect",
 "title": "Give the agent the smallest identity that can do the job",
 "when": "Before the first write tool exists, and again at every new tool",
 "purpose": (
   "Least privilege is fifty years old — Saltzer and Schroeder set it out in 1975 — and nothing about "
   "an agent changes the principle. What changes is that the thing holding the privilege now decides "
   "for itself what to do with it, and it decides partly on text that arrived from outside. So the "
   "platform does two jobs. The first is ordinary and rigorous: separate identities for reading and "
   "writing, an execution role scoped to the tools this job actually has, egress that cannot reach an "
   "arbitrary endpoint, and a residency answer expressed in configuration. The second is new. Every "
   "ingested text is untrusted, **including a partner's API response**, and the only defence that "
   "holds is that the cap and the confirmation live in the tool contract and the IAM policy rather "
   "than in a prompt."),
 "activities": [
   {"do": "Split read from write",
    "detail": "Two roles, two credentials, two audit trails. The retrieval and reasoning path never "
              "holds a credential that can change anything. Most of an agent's work is reading, so "
              "most of its runtime should be structurally unable to write."},
   {"do": "Scope the execution role to the tools in this job's contract",
    "detail": "Not the service — the operations and the resources. `bedrock:InvokeModel` on the two "
              "inference profile ARNs you pinned, not on `*`. When a tool is removed from the agent, "
              "its permission comes out in the same pull request, or the role only ever grows."},
   {"do": "Put the cap and the approver in the tool contract and the policy",
    "detail": "A refund tool whose signature cannot express an amount above the cap cannot issue one, "
              "whatever it is told. A prompt saying *never refund more than $400* is a request, and a "
              "request can be argued with — by a passenger, by a partner's error text, or by a model "
              "that has reasoned its way somewhere reasonable. This is the whole of the lesson."},
   {"do": "Control egress explicitly",
    "detail": "Private subnets with no route out except through endpoints you named: VPC endpoints for "
              "the AWS services it uses, an allowlist for the partner APIs, everything else refused "
              "and logged. An agent that can reach an arbitrary URL can be told to reach one."},
   {"do": "Treat every ingested text as untrusted, partner responses included",
    "detail": "A passenger message, an uploaded PDF, a web page and a partner API's free-text `remarks` "
              "field are all inputs an attacker can reach. Delimit them, never concatenate them into "
              "instructions, strip control sequences — and assume the model will sometimes follow them "
              "anyway, which is exactly why the cap is the control and this is only the mitigation."},
   {"do": "Answer residency in the configuration, not in a policy document",
    "detail": "Which geography may see which data, expressed as the region of the inference profile, "
              "the region of the collection, and a `Deny` on `aws:RequestedRegion` outside the allowed "
              "set. A residency answer that exists only in a Word document is not an answer, and it "
              "will be tested by a fallback at 03:00."},
   {"do": "Treat denials as signal",
    "detail": "An `AccessDenied` from the agent's role is either a tool the job needs and does not "
              "have, or the first visible symptom of an injection that partly worked. Both want a "
              "human. Alarm on the rate, and never resolve one by widening the policy to make it stop."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Generate the least-privilege policy from the tool contracts, then have it run IAM Access "
           "Analyzer policy validation, and again after a week of real traffic for unused-access "
           "findings. The second pass is where the over-grant actually comes out.",
    "caution": "Never let it widen a policy to make a test pass. Require it to report the exact denied "
               "action and resource instead; that denial is the finding, not the obstacle."},
   {"tool": "Claude Code",
    "use": "Have it write the injection suite into the harness: a partner response with an instruction "
           "in a free-text field, a passenger message impersonating the desk, a PDF with white text. "
           "It fails the build if a cap is ever exceeded.",
    "caution": None},
   {"tool": "Chat LLM, adversarially",
    "use": "Paste a tool contract and ask for ten ways a hostile input could get more out of it than "
           "intended. It is unusually good at this, because it is the same shape as the thing being "
           "attacked.",
    "caution": "Its list is not coverage. Everything it finds becomes a test in the harness, and "
               "everything it missed is still out there tomorrow."},
   {"tool": "Do not delegate",
    "use": "The blast radius of a new permission. What a wrong write costs and who has to unwind it are "
           "facts about your business, and a model will approve a wildcard that reads entirely "
           "reasonable on the page.",
    "caution": None},
 ],
 "artifact": {
   "name": "Execution role policy, egress allowlist and injection suite",
   "good": "A policy a reviewer reads in two minutes, in which every statement names a resource and "
           "maps to a tool in the contract; an egress list with a reason per entry; and a suite of "
           "hostile inputs that runs on every pull request with the cap assertion in it.",
   "owner": "Platform engineer, with the architect on the tool contracts"},
 "template": {
   "title": "Execution role policy · the read identity", "lang": "json",
   "body": """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvokeOnlyThePinnedProfiles",
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": [
        "arn:aws:bedrock:eu-west-1:123456789012:inference-profile/eu.anthropic.<model-id>",
        "arn:aws:bedrock:eu-west-1::foundation-model/anthropic.<model-id>",
        "arn:aws:bedrock:eu-central-1::foundation-model/anthropic.<model-id>"
      ]
    },
    {
      "Sid": "ResidencyEveryOtherRegionIsDenied",
      "Effect": "Deny",
      "Action": "bedrock:*",
      "Resource": "*",
      "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["eu-west-1", "eu-central-1"]}}
    },
    {
      "Sid": "ReadTheIndexTheDataAccessPolicyNarrowsItFurther",
      "Effect": "Allow",
      "Action": "aoss:APIAccessAll",
      "Resource": "arn:aws:aoss:eu-west-1:123456789012:collection/<collection-id>"
    },
    {
      "Sid": "ReadToolsOnlyWriteToolsBelongToTheWriterRole",
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": [
        "arn:aws:lambda:eu-west-1:123456789012:function:<feature>-tool-search-flights",
        "arn:aws:lambda:eu-west-1:123456789012:function:<feature>-tool-fare-rules",
        "arn:aws:lambda:eu-west-1:123456789012:function:<feature>-tool-passenger-record"
      ]
    },
    {
      "Sid": "NoWriteToolOnThisIdentityTheCapLivesInItsSignatureToo",
      "Effect": "Deny",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:eu-west-1:123456789012:function:<feature>-tool-write-*"
    },
    {
      "Sid": "OnlyThroughOurVpcEndpoints",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEqualsIfExists": {"aws:SourceVpce": ["<vpce-id-bedrock>", "<vpce-id-aoss>", "<vpce-id-logs>"]},
        "BoolIfExists": {"aws:ViaAWSService": "false"}
      }
    },
    {
      "Sid": "ObservabilityIsNotOptional",
      "Effect": "Allow",
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:eu-west-1:123456789012:log-group:/<feature>/agent:*"
    }
  ]
}
"""},
 "prompts": [
   {"title": "Derive the policy from the tool contracts",
    "when": "A tool is added, or the role has grown and nobody remembers why",
    "body": """Derive the least-privilege execution role from these tool contracts. Work from the
contracts to the policy, never the other way round.

OUTPUT SHAPE:
1. A table: | Tool | AWS actions it needs | Exact resource ARNs | Read or write? |
2. TWO policies: a read identity and a write identity. Nothing appears in both.
3. Every statement carries a Sid naming the tool it serves.
4. A list of every action currently in our role that maps to NO tool. That list is
   what comes out.

RULES:
- No wildcards in Action or Resource unless the API genuinely has no resource-level
  permission. Where that is true, say which API and cite it, and add a Condition.
- A Deny statement for any region outside <allowed regions>, on aws:RequestedRegion.
- Do not add a permission because a test failed. Report the denied action instead.
- Run IAM Access Analyzer policy validation and paste the findings.

TOOL CONTRACTS: <paste>
CURRENT POLICY: <paste>"""},
   {"title": "Build the prompt-injection suite",
    "when": "Before the agent ingests anything it did not author, which is week one",
    "body": """Write the injection test suite for our harness. Every ingested text is untrusted,
including responses from partners we have contracts with.

Produce cases in these classes, at least three each:
- A partner API response with an instruction inside a free-text field (remarks, notes,
  reason codes)
- A passenger message impersonating the desk, an internal system, or a policy update
- A document with hidden or out-of-band text (white text, metadata, alt text)
- A retrieved index chunk that contains instructions
- A tool error message crafted to redirect the agent

FOR EACH CASE: the input, what the attacker is trying to make happen, the assertion
that must hold.

RULES:
- The assertions are about ENFORCED controls, not about wording. "The refund amount
  never exceeds the cap", "no write tool is called while in shadow", "no request leaves
  the egress allowlist". An assertion about the model's phrasing is not a test.
- At least one case must succeed at manipulating the model and still be contained by
  the cap. That case is the point of the whole suite.
- The suite fails the build. It does not warn.

OUR TOOLS, CAPS AND INGESTION POINTS: <paste>"""},
   {"title": "Find the over-grant from real traffic",
    "when": "A week after go-live, and quarterly thereafter",
    "body": """Compare what this role is ALLOWED to do against what it has actually done.

Use CloudTrail for the last <n> days plus IAM Access Analyzer unused-access findings.

OUTPUT SHAPE:
| Action | Allowed on | Times used | Last used | Verdict |
Verdict: KEEP / NARROW TO <arn> / REMOVE / TOO NEW TO JUDGE.

RULES:
- READ ONLY. Produce the proposed policy as a diff; change nothing.
- An action used zero times is not automatically REMOVE - some are for failure paths
  that have not fired. Mark those TOO NEW TO JUDGE and say what would exercise them.
- Report every AccessDenied separately, with the caller and the time. Each one is
  either a missing permission or an attempt, and I need to know which you think it is.
- Finish with the single narrowing that most reduces blast radius, and what would
  break if it is wrong."""},
 ],
 "example": {
   "title": "SkyWays · the $400 that was only in a prompt",
   "body": "On day 82 the agent issued a $2,000 refund. Nothing was hacked and nothing crashed. The "
           "$400 cap and the named approver had both been decided on day 12, written into the autonomy "
           "record, and repeated clearly in the system prompt. Neither was in the code. The refund "
           "tool's signature accepted any amount, and the execution role could invoke it. A passenger "
           "message and a partner's delay note between them produced a case the model read as "
           "exceptional, and it acted entirely within its permissions and entirely outside its policy. "
           "The fix was two lines in a tool signature and one statement in an IAM policy. The "
           "postmortem's finding was not a person; it was an absent control."},
 "pitfalls": [
   "A cap that lives in the prompt. A prompt is a request, and a request can be argued past — by a "
   "passenger, by a partner's error text, or by the model's own reasoning — and the amount is real money.",
   "One role for the whole agent. The retrieval step then holds write permission for the entire run, so "
   "the blast radius of a single injected instruction is everything the agent could ever do.",
   "Trusting a partner's API response because it arrived over TLS from a company you have a contract with. "
   "The channel is authenticated; the free-text field inside it is typed by somebody you have never met.",
 ],
 "done_when": "A reviewer can read the execution role in two minutes and name, for every statement, which "
              "tool in the contract needs it — and the injection suite runs on every pull request with "
              "the cap assertion in it.",
},
{
 "n": 8, "id": "recover", "phase": "Recover",
 "title": "Rehearse the rollback and cap the runaway",
 "when": "Before cut-over, then after every incident, forever",
 "purpose": (
   "Rollback is a capability, and a capability nobody has used is a belief. Rehearse it before "
   "cut-over, with a stopwatch, and write the measured time down. Two things differ from an ordinary "
   "service. You may need to roll back a **prompt** or a **model version** rather than code, so each "
   "is a versioned artefact with its own path and its own rehearsal. And the failure that costs most "
   "here is not a crash but a runaway: an agent that loops, or spends, or acts, faster than anybody is "
   "watching. That has three controls — a loop cap, a per-transaction token and cost cap, and a kill "
   "switch that degrades to the human desk rather than to an error page."),
 "activities": [
   {"do": "Rehearse every rollback before cut-over, with a stopwatch",
    "detail": "The person who will do it at 02:00 does it once at 14:00 with the runbook open, and the "
              "measured time goes into the runbook. If it takes eleven minutes then the incident is "
              "eleven minutes long, and everybody can plan around a number they have seen."},
   {"do": "Rehearse the prompt and model rollbacks separately",
    "detail": "Three artefacts, three paths. Reverting the container does not revert the prompt version "
              "the flag points at, and it does not revert a model version pinned in a manifest. Most "
              "teams have only ever tested the first, and discover the other two during the incident."},
   {"do": "Cap the loop, the tokens and the spend per transaction",
    "detail": "`MAX_LOOPS=5` as this playbook's default, a token ceiling per case, and a cost ceiling "
              "per case, all enforced in the runtime and all emitting a metric when they trip. A cap "
              "that trips silently is a cap you learn about from the bill, by which time it has been "
              "holding the system together for a month."},
   {"do": "Make the kill switch degrade to the desk, not to an error",
    "detail": "Off means the case goes to a human queue with its context attached, not a 500 and a "
              "passenger with nothing. A kill switch that causes an outage is one the team hesitates "
              "to throw, and the hesitation is most of the cost of the incident."},
   {"do": "Name who can throw it without asking",
    "detail": "A list, with times of day, and no approval step. If the on-call engineer needs a "
              "director at 02:00, the switch has a four-hour latency written into the org chart rather "
              "than into the runbook, and nobody will find it until it matters."},
   {"do": "Know what is stateful and rehearse the restore",
    "detail": "The runtime is disposable. Three things are not: the **trace store**, which is your only "
              "account of what happened; the **golden set**, which is the measurement itself; and the "
              "**vector index**, which is expensive to rebuild and needs its source retained to rebuild "
              "from. Back up those three, test the restore, and let the rest be `cdk deploy`."},
   {"do": "Turn every incident into a control rather than a name",
    "detail": "The postmortem is finished when it names the enforced control that would have made this "
              "class of incident impossible, and where that control will live: a tool signature, a "
              "policy statement, a cap. A better prompt is not a control."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Write the rollback as a script rather than a runbook paragraph, and schedule it to run "
           "against a rehearsal environment weekly. A rollback exercised every week in staging is one "
           "that works in production at 02:00.",
    "caution": "Require a typed confirmation and have it print exactly what it is about to change. A "
               "rollback script that can run unattended is a new and creative way to have an incident."},
   {"tool": "Claude Code",
    "use": "Have it write the cap tests: a case engineered to loop, a case engineered to grow context "
           "without bound, and an assertion that each stops at the cap, emits its metric and lands in "
           "the desk queue.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Turn a postmortem transcript into the five-part brief — pain, evidence, the missing enforced "
           "control, the fix, the value — and hold that format while the room is still looking for a "
           "person to blame.",
    "caution": "Check that its 'control' is genuinely enforceable. It will happily propose a clearer "
               "prompt, which is a request wearing a control's clothes."},
   {"tool": "Do not delegate",
    "use": "Declaring the incident over. Somebody with accountability looks at the state of the world — "
           "what was written, what was refunded, what passengers were told — and says so with their name "
           "on it.",
    "caution": None},
 ],
 "artifact": {
   "name": "Rehearsed recovery runbook and the containment caps",
   "good": "A runbook with measured times rather than estimated ones, four switches that have each been "
           "thrown by the person who will throw them, caps that emit a metric when they trip, and a "
           "named list of people who can stop it without asking anyone.",
   "owner": "Platform engineer, with the on-call rota"},
 "template": {
   "title": "Rollback script, four switches", "lang": "bash",
   "body": """#!/usr/bin/env bash
# rollback.sh - three artefacts, four switches. Rehearsed <date> by <name>:
#   kill    ~40s  every case to the desk queue, with its context. NOT an error.
#   flag    ~2m   one action back to shadow; the other actions keep running.
#   prompt  ~3m   runtime picks up the previous prompt version on the next case.
#   model   ~11m  redeploys the runtime, and the harness must re-run afterwards.
set -euo pipefail

FEATURE="<feature>"
ENVIRONMENT="prod"
REGION="<eu-west-1>"
APP_ID="<appconfig-application-id>"
ENV_ID="<appconfig-environment-id>"
PROFILE_ID="<appconfig-configuration-profile-id>"
STRATEGY_ID="AppConfig.AllAtOnce"

confirm() {
  echo "ABOUT TO: $1"
  read -r -p "Type the environment name to continue: " reply
  [ "$reply" = "$ENVIRONMENT" ] || { echo "aborted"; exit 1; }
}

put_param() {
  aws ssm put-parameter --name "/$FEATURE/$ENVIRONMENT/$1" --value "$2" \\
    --type String --overwrite --region "$REGION" >/dev/null
  echo "set /$FEATURE/$ENVIRONMENT/$1 = $2"
}

case "${1:-}" in
  kill)
    confirm "kill switch ON - every case to the desk queue with its context"
    put_param kill-switch on
    ;;
  flag)
    # Roll FORWARD to a known-good previous configuration version.
    confirm "deploy flag document version ${2:?previous version number required}"
    aws appconfig start-deployment --application-id "$APP_ID" \\
      --environment-id "$ENV_ID" --configuration-profile-id "$PROFILE_ID" \\
      --deployment-strategy-id "$STRATEGY_ID" --configuration-version "$2" \\
      --region "$REGION" --query Id --output text
    ;;
  prompt)
    confirm "pin prompt version ${2:?prompt sha required}"
    put_param prompt-version "$2"
    ;;
  model)
    # Slowest path. Whatever you roll back to, the harness re-runs against it.
    confirm "redeploy runtime pinned to model ${2:?model id required}"
    aws cloudformation deploy --stack-name "$FEATURE-$ENVIRONMENT-runtime" \\
      --template-file infra/runtime.yaml --region "$REGION" \\
      --parameter-overrides "ModelId=$2" --no-fail-on-empty-changeset
    echo "NOW: re-run the harness against $2 before widening any flag."
    ;;
  *)
    echo "usage: $0 {kill|flag <version>|prompt <sha>|model <model-id>}" >&2
    exit 2
    ;;
esac

echo "Done at $(date -u +%FT%TZ). Put the elapsed time in the runbook."
"""},
 "prompts": [
   {"title": "Turn the runbook into a rehearsed script",
    "when": "Two weeks before cut-over, while there is still time to find it does not work",
    "body": """Turn this rollback runbook into a script, then into a rehearsal.

PART 1 - the script. One subcommand per switch: kill, flag, prompt, model.
RULES:
- Each subcommand prints exactly what it will change and requires a typed confirmation.
- Each is idempotent and safe to run twice.
- Each ends by printing the check that proves it worked, as a command I can paste.
- Fail loudly on a missing argument. Never guess a version.

PART 2 - the rehearsal plan.
- Who runs it (the person who will do it at 02:00, not the person who wrote it).
- Which environment, and what makes that environment realistic enough to count.
- What is timed, and where the measured times get written down.
- What would make us say the rehearsal FAILED, decided before we run it.

RULES:
- Do not write a step that says "verify the system is healthy". Say which metric,
  which query, which value.
- If any switch cannot be scripted, say so and explain what makes it manual. That is
  the finding, and it is worth more than a script that pretends.

RUNBOOK: <paste>"""},
   {"title": "Design the containment caps and their tests",
    "when": "Before the first live traffic, because a runaway is fast",
    "body": """Design the containment caps for this agent, and the tests that prove each one.

CAPS REQUIRED:
- MAX_LOOPS (default 5): the agent stops rather than reasoning in circles
- Tokens per case
- Cost per case
- Wall-clock per case

FOR EACH, give me:
1. Where it is enforced. It must be in the runtime, not in the prompt. Say which line.
2. What happens when it trips: the case goes to the desk queue WITH its context, a
   metric is emitted, and the passenger sees something sensible. Never a bare error.
3. The test that proves it: a case engineered to hit that cap, asserting the stop, the
   metric and the destination.
4. How the threshold was chosen, and what evidence would change it.

RULES:
- A cap that trips silently is not a cap. Every trip emits a metric with the case id.
- Say what the caps cost us: which legitimate cases they will refuse, and roughly how
  many per week. If you cannot estimate that, say what to measure first.

OUR AGENT AND ITS TOOLS: <paste>"""},
   {"title": "Work out what is actually stateful",
    "when": "Before you write a DR plan, so it covers the right three things",
    "body": """Given this architecture, tell me what cannot be rebuilt from the repository.

OUTPUT SHAPE:
| Thing | Rebuildable from the repo? | If lost, what breaks | RPO | RTO | Restore test |

RULES:
- Be specific about the ones people forget: the trace store (the only account of what
  happened), the golden set and its labels (the measurement itself), the vector index
  AND the source documents it was built from, the flag configuration history, the
  redaction manifests.
- For the vector index, say whether we can rebuild it and what that costs in time and
  tokens. "We can re-embed" is only true if the sources are retained - check.
- Anything marked rebuildable must have the command that rebuilds it. If nobody has
  run that command, mark it UNPROVEN.
- Finish with the single restore we should test this quarter, and why that one.

ARCHITECTURE: <paste>"""},
 ],
 "example": {
   "title": "SkyWays · eleven minutes, known in advance",
   "body": "Before cut-over the on-call engineer threw all four switches with a stopwatch: kill switch "
           "40 seconds, flag to shadow 2 minutes, prompt rollback 3 minutes, model rollback 11 minutes "
           "because it redeploys the runtime. Those four numbers went into the runbook beside the date. "
           "On day 82, when the $2,000 refund surfaced, the question in the room was never *can we stop "
           "it* — it was *which switch*. Refunds went back to gated in two minutes while the tool "
           "signature was fixed properly over the next two days, and the rest of the assistant kept "
           "running, because the flags were per action. Nobody had to be brave."},
 "pitfalls": [
   "A rollback that has only ever been described. The first attempt happens during an incident, with the "
   "wrong person at the keyboard, and the eleven minutes nobody measured turn into forty.",
   "Rolling back the container and believing you rolled back the behaviour. The prompt version and the "
   "model version are separate artefacts, and the deploy you just reverted may not have touched either.",
   "A kill switch that returns an error. It produces an outage instead of a queue, so the team hesitates "
   "to throw it, and the hesitation is the expensive part of every incident it was built for.",
 ],
 "done_when": "Every rollback path has a measured time in the runbook next to the date it was last "
              "rehearsed, and a case that hits the loop cap or the cost cap ends in the desk queue with "
              "a metric rather than in a retry.",
},
]
