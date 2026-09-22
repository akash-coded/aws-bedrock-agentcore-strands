"""DevOps and platform · head and steps 1-3. Imported by build_content.py."""

HEAD = {
    "id": "devops",
    "name": "DevOps and platform",
    "short": "OPS",
    "accent": "#6B4E8A",
    "tagline": "From a laptop to production, repeatably",
    "arc": ["Baseline", "Access", "Environments", "Pipeline", "Deploy", "Observe", "Protect", "Recover"],
    "intro": [
        "Your job has not changed. Accounts, pipelines, deployments, permissions, recovery — the list "
        "is the same list, and most of what you already know transfers intact. Three things underneath "
        "it are new, and every step below is one of them working through. The **model version is part "
        "of the environment**, so an environment can change behaviour with no deploy and no diff. The "
        "**bill moves with behaviour** rather than with traffic, so capacity planning becomes cost "
        "instrumentation. And **text is an attack surface**, so an input is now something that can "
        "instruct.",
        "The second thing that changes is the order. A budget alarm is worth little in month three and "
        "a great deal in week one. Model access sits in somebody else's approval queue, so it is a "
        "lead-time item started on day one rather than a task scheduled for the week you need it. And "
        "the evaluation harness has to be a required status check *before* the first release is under "
        "time pressure, because that is the week it would otherwise quietly be made optional.",
        "Eight steps. Each one ends in something committed to a repository rather than configured in a "
        "console, because the capability you are actually building is the ability to destroy an "
        "environment and get it back.",
    ],
    "owns": [
        "The **landing zone** — accounts, isolation, and a tag scheme that makes cost attributable per feature",
        "The **model gateway** — one layer every call passes through, with a per-call log nobody can route around",
        "The pipeline, including the evaluation harness as a required status check rather than a comment",
        "Three deployable artefacts and three rollback paths: the code, the prompt, and the model version",
        "The **enforced** controls — execution role scope, egress, caps in tool signatures — as distinct "
        "from the requested ones",
        "The kill switch, the containment caps, and the rehearsed recovery times",
    ],
    "not_yours": [
        "The **acceptance bar** per slice. The product manager derives it and QA curates the cases; your "
        "job is to make the gate unarguable, not to set it",
        "**Prompt content.** You version it, deploy it and roll it back. You do not write it",
        "Which slices exist and what a wrong answer costs in each — that is the business's answer, and it "
        "is the input to your caps rather than your output",
        "The behaviour, release and expansion gates. You supply the evidence and the rollback; somebody "
        "else signs",
    ],
    "ai_stance": (
        "Use a model where there is a schema to be right against and a cheap way to check. It is "
        "genuinely strong at CloudFormation, workflow YAML, IAM policy shapes and the first draft of a "
        "script, and it is confidently wrong about your account boundaries, your regions, your quotas "
        "and what a permission actually reaches. The pattern that works: the model writes the change, a "
        "machine judges it — `cfn-lint`, `cdk diff`, a plan output, IAM Access Analyzer, a test — and "
        "you read the diff rather than the prose. Anything that widens a permission, opens an egress "
        "path or touches a production boundary is read line by line by a person, because a model cannot "
        "estimate a blast radius it has never had to unwind. Where a step below says *do not delegate*, "
        "that is the reason."
    ),
    "reads": [
        ["How the whole lifecycle fits together", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Agentic-PDLC"],
        ["The gateway control, in the simulator", "app/SkyWays-Architect.html#/governance/gv-gateway"],
        ["Every lever on the token bill", "https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill"],
    ],
}

STEPS_A = [
{
 "n": 1, "id": "baseline", "phase": "Baseline",
 "title": "Stand up the account, the tags and the budget first",
 "when": "Week one, alongside discovery, before any resource exists",
 "purpose": (
   "The platform question for an agentic workload is not different in kind from any other. It is "
   "different in *when*. Two of the things this workload needs bill for **existing** rather than for "
   "use — an OpenSearch Serverless collection holds capacity while it exists, and an AgentCore runtime "
   "holds an environment — so the ordinary habit of standing something up to try it and tidying up "
   "later produces a fixed monthly charge with no feature attached to it. Four things go in before the "
   "first feature branch: an account boundary, a tag scheme that attributes cost per feature, "
   "infrastructure as code, and a budget alarm."),
 "activities": [
   {"do": "Separate the accounts before you separate the stacks",
    "detail": "One account per environment, under Organizations or Control Tower. It is a blast-radius "
              "boundary and a billing boundary at the same time, and it is the only one of the two that "
              "cannot be retrofitted cheaply. An experiment in the production account is a quota and a "
              "bill you will be untangling in month three."},
   {"do": "Tag per feature, not per team",
    "detail": "`Feature`, `Environment`, `Owner`, `CostCentre`. Teams re-org and features do not. The "
              "question you will be asked is *what did rebooking cost last month*, and a team tag "
              "cannot answer it for any month before the re-org."},
   {"do": "Activate the cost allocation tags in the payer account the same day",
    "detail": "A tag on a resource is invisible to Cost Explorer until that user-defined tag key is "
              "activated in the management account, and the data starts flowing from activation. A "
              "backfill request exists; do not plan around it. A tag activated in month three does not "
              "label months one and two."},
   {"do": "Put every resource in CDK or CloudFormation from the very first one",
    "detail": "Not because click-ops is untidy. Because the first thing you will genuinely need is to "
              "delete an environment entirely and rebuild it, and the console has no undo. Teardown is "
              "the feature you are buying."},
   {"do": "Create the budget and its alarm before anything that costs money",
    "detail": "An actual `AWS::Budgets::Budget` with an SNS action and a named owner, not a calendar "
              "reminder. Put the threshold at the forecast the product manager defended, with a "
              "notification on actual spend and a second on *forecast*, which is the one that gives you "
              "a fortnight's warning instead of a bill."},
   {"do": "Keep a written register of what bills for existing",
    "detail": "Collections, runtimes, provisioned throughput, NAT gateways, idle endpoints. Each with "
              "an owner and a teardown command, in the repository, reviewed weekly. Nothing goes quiet "
              "when the traffic does, so the only control is a list somebody reads."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Generate the landing-zone stack from a written statement of your boundaries, and have it run "
           "`cfn-lint` and `cdk diff` itself. The review you then do is of a diff rather than of prose, "
           "which is the difference between checking and reading.",
    "caution": "It will invent a region and a partition. Check every hard-coded region and every `arn:aws:` "
               "against the residency answer you actually have."},
   {"tool": "Claude Code, read-only credentials",
    "use": "Point it at an existing account and have it produce two lists: resources with no `Feature` "
           "tag, and resources belonging to no stack. Those two lists are the whole of the cost problem "
           "in most inherited accounts.",
    "caution": "Give it a role that cannot delete or modify anything. An audit script that tidies up as "
               "it goes is how a shared dev environment disappears on a Friday."},
   {"tool": "Chat LLM",
    "use": "Draft the tag dictionary and its allowed values, then ask it which of your four cost "
           "questions the scheme still cannot answer. It is reliable at finding the question with no "
           "tag behind it.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The account boundary, and what is allowed to live in production. Blast radius is a business "
           "fact — which failures you can survive and who has to explain them — and a model has no way "
           "to estimate it.",
    "caution": None},
 ],
 "artifact": {
   "name": "Landing zone stack and cost baseline",
   "good": "One repository that creates an empty, near-zero-cost environment from nothing and destroys "
           "it again, a budget alarm that fires before a human notices, and a tag on every resource "
           "naming the feature that pays for it.",
   "owner": "Platform engineer"},
 "template": {
   "title": "Cost baseline, deployed before anything else", "lang": "yaml",
   "body": """# baseline.yaml - deploy BEFORE anything that can cost money.
# aws cloudformation deploy --template-file baseline.yaml --stack-name <feature>-baseline \\
#   --parameter-overrides Feature=<feature> MonthlyBudgetUsd=<n> AlertEmail=<alias> \\
#   --tags Feature=<feature> Environment=<env> Owner=<name> CostCentre=<code>
#
# Always-on register (these bill for EXISTING, not for use). Reviewed weekly,
# each with an owner and a teardown command:
#   OpenSearch Serverless collections, AgentCore runtimes, provisioned
#   throughput, NAT gateways, idle endpoints.
AWSTemplateFormatVersion: "2010-09-09"
Description: Cost baseline for one feature. Creates nothing that serves traffic.

Parameters:
  Feature:
    Type: String
    Description: The feature that pays for everything tagged with it. Never a team name.
    AllowedPattern: "[a-z0-9-]{3,32}"
  MonthlyBudgetUsd:
    Type: Number
    Description: The forecast that was defended, not a round number.
  AlertEmail:
    Type: String

Resources:
  BudgetAlerts:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: {Fn::Sub: "${Feature}-budget"}

  # Without this policy the budget cannot publish, and the silence looks healthy.
  BudgetAlertsPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      Topics: [{Ref: BudgetAlerts}]
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: {Service: budgets.amazonaws.com}
            Action: sns:Publish
            Resource: {Ref: BudgetAlerts}

  FeatureBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: {Fn::Sub: "${Feature}-monthly"}
        BudgetType: COST
        TimeUnit: MONTHLY
        BudgetLimit: {Amount: {Ref: MonthlyBudgetUsd}, Unit: USD}
        CostFilters:
          # Activate this tag key in the payer account on the same day. Cost data
          # starts at activation; it does not go back and label last month.
          TagKeyValue: ["user:Feature$<feature>"]
      NotificationsWithSubscribers:
        - Notification: {NotificationType: ACTUAL, ComparisonOperator: GREATER_THAN,
                         Threshold: 80, ThresholdType: PERCENTAGE}
          Subscribers: [{SubscriptionType: SNS, Address: {Ref: BudgetAlerts}},
                        {SubscriptionType: EMAIL, Address: {Ref: AlertEmail}}]
        # Forecast, not actual. This one arrives with a fortnight to act in.
        - Notification: {NotificationType: FORECASTED, ComparisonOperator: GREATER_THAN,
                         Threshold: 100, ThresholdType: PERCENTAGE}
          Subscribers: [{SubscriptionType: SNS, Address: {Ref: BudgetAlerts}}]
"""},
 "prompts": [
   {"title": "Baseline stack from a boundary statement",
    "when": "Nothing exists yet and you are about to create the first resource",
    "body": """You are writing the baseline infrastructure for a new agentic feature. Nothing
exists yet.

Produce ONE CloudFormation template (or a CDK stack, if this repository already has
one) that creates only the cost baseline: the budget, its alarm path, and the
parameters everything else will inherit. No workload resources.

RULES:
- A FORECASTED notification as well as an ACTUAL one. Put the reason in a comment.
- Every resource carries Feature, Environment, Owner, CostCentre. Feature is the cost
  boundary and it is never a team name.
- No hard-coded account id, region or ARN partition. Parameters or pseudo-parameters.
- Run cfn-lint (or cdk synth) yourself. Do not hand me a template you have not linted.

OUTPUT SHAPE: the template, then the lint output, then the exact deploy command for
<environment>, then a list of anything you had to assume.

OUR BOUNDARIES:
<paste: accounts, regions, who pays, the residency answer, who gets the alert>"""},
   {"title": "Find what is billing for existing",
    "when": "You inherited an account, or the bill has a line nobody can name",
    "body": """Audit this account for resources that bill for EXISTING rather than for use.

Look for at least: OpenSearch Serverless collections, AgentCore runtimes, provisioned
throughput, NAT gateways, idle load balancers, allocated addresses, unattached volumes,
old snapshots.

OUTPUT SHAPE - one table, sorted by monthly cost, highest first:
| Resource | Type | Created | Last used (or "unknown") | Feature tag? | ~$/month | Safe to delete? |

RULES:
- READ ONLY. Do not delete, stop or modify anything, and do not write me a script that
  can. Use read-only calls.
- "Safe to delete" is a question for a human. Write UNKNOWN unless there is evidence in
  the account itself, and say what the evidence was.
- List separately every resource with no Feature tag. That list is the real finding.
- Finish with the one resource I should deal with today, and why it is that one."""},
   {"title": "Does this tag scheme answer the questions",
    "when": "Before you activate cost allocation tags, because activation is not retroactive",
    "body": """Review this tag scheme against the only four questions it will ever be asked.

THE QUESTIONS:
1. What did <feature> cost last month, across every service?
2. Which resources belong to an environment we are about to destroy?
3. Who do I call about this resource at 02:00?
4. Which resources are billing with no owner at all?

RULES:
- Judge each tag only by whether it serves one of those four. Do not add tags for tidiness.
- Flag any tag whose value changes when the org chart changes. Those cannot answer
  question 1 for any month before the change.
- Say which keys must be activated as cost allocation tags in the payer account, and
  state plainly what happens to the months before activation.

OUTPUT SHAPE: keep / change / drop per tag, one line of reasoning each. Then the four
questions with "answerable: yes/no" against your revised scheme.

SCHEME: <paste>"""},
 ],
 "example": {
   "title": "SkyWays · the line item nobody could name",
   "body": "In week two an engineer stood up an OpenSearch Serverless collection to try retrieval over "
           "the fare rules. It was never wired into anything, and it was never switched off. On day 75 "
           "the bill came in at 4.4 times its estimate; that multiple was traced to four ordinary habits "
           "compounding, and the collection was not even part of it — it was a separate line that took "
           "an afternoon to attribute, because it carried no `Feature` tag and belonged to no stack. "
           "Two controls would have made it a two-minute question: a tag activated in week one, and a "
           "weekly read of the always-on register."},
 "pitfalls": [
   "Standing up a collection or a runtime to try something, and relying on remembering to remove it. Both "
   "bill for existing, so a forgotten experiment is a fixed monthly cost attached to no feature and no owner.",
   "Tagging by team. The re-org lands in nine months and the question *what did rebooking cost* becomes "
   "permanently unanswerable for every month before it.",
   "Activating cost allocation tags late. The tags were there all along, the cost data was not, and the "
   "first three months of spend can never be attributed — which is exactly the period you will be asked about.",
 ],
 "done_when": "You can destroy a whole environment and rebuild it from the repository, and Cost Explorer "
              "can tell you what one feature cost last month without anyone opening a spreadsheet.",
},
{
 "n": 2, "id": "access", "phase": "Access",
 "title": "Get model access, then put every call behind one gateway",
 "when": "The request on day one; the gateway before the second team calls Bedrock directly",
 "purpose": (
   "Two things happen here and they move at different speeds. Model access in Bedrock is granted per "
   "model, **per region**, on request, and the approval sits in somebody else's queue — which makes it "
   "a lead-time item started on day one, not a task scheduled for the week you need it. The gateway is "
   "a build: one layer every model call passes through, so routing, budgets, fallbacks and a per-call "
   "log exist in one place instead of in four codebases. Without the per-call log you cannot diagnose "
   "a bill. You can only argue about it."),
 "activities": [
   {"do": "Request model access on day one, per model and per region",
    "detail": "Access granted in `us-east-1` is not access in `eu-west-1`. Some models ask for a use "
              "case before approval and some approvals are not instant. Put the requests in before the "
              "architecture is finished; withdrawing an unused request costs nothing and waiting on a "
              "missing one costs a week."},
   {"do": "Use the inference profile ID, not the bare model ID",
    "detail": "Many current models are only callable through a cross-region inference profile, whose "
              "identifier carries a geography prefix — `us.`, `eu.`, `apac.` — in front of the model ID. "
              "A bare ID returns a validation error telling you to retry with an inference profile. "
              "This is the single most common first-day error, and it reads like a permissions problem, "
              "so teams spend the morning in IAM."},
   {"do": "Read the quotas that actually apply to this account",
    "detail": "Requests and tokens per minute are per account, per region, per model, and the account "
              "default is not the published headline. Get the real numbers from Service Quotas on day "
              "one. An increase is another lead-time item with another queue."},
   {"do": "Put one gateway in front of everything",
    "detail": "LiteLLM is the common choice: an OpenAI-compatible endpoint in front of Bedrock, so "
              "routing, retries, fallback and budgets are configuration rather than code. The value is "
              "not the abstraction. It is that there is one place to change a model and one place that "
              "sees every call."},
   {"do": "Make the per-call log non-optional",
    "detail": "Request id, feature, environment, model version, input tokens, output tokens, **cached "
              "tokens**, latency, cost, case id. Without the cached-token column the cache is a belief "
              "rather than a measurement. Without the feature column the bill is one number."},
   {"do": "Write routing and fallback as policy, not as a try/except",
    "detail": "Cheap tier for classification and extraction, the capable tier for the judgement call, a "
              "named fallback when a region throttles. In the gateway config, reviewed like code, "
              "identical in every environment. A retry policy buried in application code is a cost "
              "multiplier nobody can find."},
   {"do": "Issue a gateway key per feature, with its own budget",
    "detail": "Not a key per person and not one shared key. A virtual key per feature makes the budget "
              "enforceable at the call rather than at the month end, and it splits the bill on exactly "
              "the same boundary as your resource tags."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Have it write a probe that calls every model you believe you have access to, in every region "
           "you plan to use, trying the bare ID and then the profile ID, and prints a matrix. Ten "
           "minutes of work that settles a week of guessing.",
    "caution": "One-word prompt, `max_tokens` of 1, no retries. A probe that writes a paragraph per "
               "model per region is a bill of its own."},
   {"tool": "Claude Code",
    "use": "Generate the gateway config from the access matrix, and have it diff the config against the "
           "grants you actually hold so an aspirational model cannot reach production.",
    "caution": "It will happily emit a bare model ID. Grep the config for any model string without a "
               "geography prefix before you deploy it, and make that grep a CI step."},
   {"tool": "Chat LLM",
    "use": "Draft the access-request justification per model: what it is for, what data reaches it, what "
           "the volume will be. The reviewer's questions are predictable and the answers are the same "
           "ones your architecture review needs anyway.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "Which models are permitted for which data. That is a residency and contract question about "
           "your own organisation, and a model reading your config cannot know that a partner's fare "
           "data is not allowed to leave a geography.",
    "caution": None},
 ],
 "artifact": {
   "name": "Model access matrix and gateway config",
   "good": "A committed table of model, region, status and date requested, and one gateway config used "
           "by every environment whose per-call log already has a feature column and a cached-token "
           "column in it.",
   "owner": "Platform engineer"},
 "template": {
   "title": "Model gateway config", "lang": "yaml",
   "body": """# litellm-config.yaml - the one layer every model call goes through.
# litellm --config litellm-config.yaml --port 4000
#
# Every `model` below is an INFERENCE PROFILE id. A bare id with no geography
# prefix fails with a validation error telling you to retry with a profile.
# That error reads like a permissions problem and is not one.

model_list:
  - model_name: judge              # capable tier: the judgement call
    litellm_params:
      model: bedrock/eu.anthropic.<model-id>
      aws_region_name: <eu-west-1>
      timeout: 60
  - model_name: judge-secondary    # same model, second region, SEPARATE access grant
    litellm_params:
      model: bedrock/eu.anthropic.<model-id>
      aws_region_name: <eu-central-1>
      timeout: 60
  - model_name: classify           # cheap tier: routing, extraction, tagging
    litellm_params:
      model: bedrock/eu.anthropic.<small-model-id>
      aws_region_name: <eu-west-1>
      timeout: 30

router_settings:
  routing_strategy: simple-shuffle
  num_retries: 2                   # capped. Uncapped retries are a silent 1.4x.
  allowed_fails: 3
  cooldown_time: 30
  fallbacks:
    # Same geography only. A fallback that crosses a residency boundary is a breach.
    - judge: ["judge-secondary"]

litellm_settings:
  drop_params: false
  cache: true
  cache_params:
    type: redis
    ttl: 3600
  success_callback: ["s3"]         # EVERY call, not a sample
  failure_callback: ["s3"]

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  alerting: ["slack"]
  # One virtual key per FEATURE, each with its own budget, so the bill splits on
  # the same boundary as the resource tags:
  #   litellm --create-key --models judge,classify --max-budget <n> \\
  #     --budget-duration 30d --key-alias <feature>-prod
  max_budget: <n>
  budget_duration: 30d
"""},
 "prompts": [
   {"title": "Probe what this account can actually call",
    "when": "Day one, before anyone designs around a particular model",
    "body": """You are helping a platform engineer establish which Bedrock models this account
can actually invoke, before anyone designs around one.

Write and run a script that, for every (model, region) pair below:
- calls with the BARE model id first, then with the inference profile id carrying the
  geography prefix for that region (us. / eu. / apac.)
- records the exact error class for each attempt

OUTPUT SHAPE - one table and nothing else:
| Model | Region | Bare id | Profile id | Verdict | Error |

Verdict is exactly one of: GRANTED / NOT GRANTED / PROFILE REQUIRED / QUOTA / UNKNOWN.

RULES:
- max_tokens = 1 and a one-word prompt. A probe that writes a paragraph per pair is a
  bill of its own.
- Do not retry on a throttle. Record QUOTA and move on.
- Create, modify and delete nothing. Read and invoke only.
- Show me the script before you run it.

PAIRS: <paste model ids and regions>"""},
   {"title": "Gateway config from the access matrix",
    "when": "The matrix is settled and the second team is about to start calling Bedrock",
    "body": """Write a LiteLLM proxy config from the access matrix below.

RULES:
- Every `model` string must be an inference profile id whose geography prefix matches
  its region. If a row in the matrix gives only a bare id, stop and tell me which row.
- Name models by ROLE, not by vendor: `judge` (capable tier), `classify` (cheap tier),
  plus a same-geography twin of each for fallback.
- Fallbacks never cross a residency boundary. Put the reason in a comment on each.
- num_retries capped, with a comment stating the worst-case cost multiplier it implies.
- success_callback and failure_callback on every call, not a sample.
- No secret values anywhere. Environment references only.

OUTPUT SHAPE: the YAML, then a short checklist of what I must verify before deploying,
then the one grep command that proves no bare model id got through.

MATRIX: <paste>"""},
   {"title": "Triage a first-day Bedrock failure",
    "when": "The first call fails and someone has already opened the IAM console",
    "body": """A Bedrock call is failing. Work through these IN ORDER and tell me which it is,
with the single command that confirms or eliminates each:

1. The model access grant is missing in THIS region (it is per model, per region)
2. The call used a bare model id where an inference profile id is required
3. The IAM policy does not allow that action on that resource
4. A quota: requests or tokens per minute for this model in this region
5. Something else - say precisely what

RULES:
- Do not suggest widening an IAM policy until 1 and 2 are both ruled out.
- Do not suggest a retry as a fix for anything.
- Quote the part of the error that distinguishes your answer from the next candidate.

End with the one-line change that fixes the most likely cause, and how I will know.

ERROR, VERBATIM, plus the call site and region:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · the six days nobody had planned",
   "body": "The architecture was signed on day 12 and the first call was written on day 13, in "
           "`eu-west-1`, with a bare model ID. Two hours went into IAM before somebody read the error "
           "properly and saw it was asking for an inference profile. The larger cost was underneath: "
           "access had been granted in `us-east-1` in week one, so everyone assumed the account had it, "
           "and nobody had requested `eu-west-1` at all. Six days. The plan had allowed zero. Once the "
           "gateway went in, the same class of mistake became a one-line config change rather than four "
           "codebases and a guess about which one was still wrong."},
 "pitfalls": [
   "Treating model access as a task rather than a lead-time item. It sits in someone else's queue, so a "
   "plan that schedules it as a day's work in week four discovers the truth in week five.",
   "The bare model ID. It fails with something that reads like a permissions error, so the team spends the "
   "morning widening IAM policies — which then ship, over-permissive, and are never narrowed again.",
   "Letting one team call Bedrock directly 'just for now'. The per-call log then has a hole in it, and the "
   "hole is always exactly the team whose spend you were asked to explain.",
 ],
 "done_when": "Every model call in every environment goes through one endpoint, and you can produce "
              "yesterday's cost split by feature from its log without asking anybody for anything.",
},
{
 "n": 3, "id": "environments", "phase": "Environments",
 "title": "Make the environments comparable, model version included",
 "when": "P1, before the harness has anything meaningful to run against",
 "purpose": (
   "Environment parity is an old discipline with a new member. For a deterministic system, parity means "
   "the same code, the same configuration and the same data shape. For a probabilistic one the **model "
   "version is part of the environment**, and an unpinned model changes behaviour with no deploy, no "
   "error and no line in any diff. So every environment pins its model, and a model upgrade becomes a "
   "deployment that re-runs the harness. Two other things break parity here in ways they do not "
   "elsewhere: secrets, which must never reach a prompt, a context file or a trace; and evaluation "
   "data, which must be real cases rather than invented ones."),
 "activities": [
   {"do": "Pin the model version per environment, in the manifest",
    "detail": "The full versioned identifier, never a floating alias. An alias that moves silently is "
              "the same failure as `latest` on a container image, except that the symptom is a score "
              "drop with no deploy to blame and three hours spent reading an empty diff."},
   {"do": "Treat a model upgrade as a deployment",
    "detail": "Its own pull request, its own harness run, its own rollback path, its own note in the "
              "release record. The new version is better on average and *different on your slices*, and "
              "average is not what you ship."},
   {"do": "Promote the model through environments in the same order as the code",
    "detail": "Evaluation first, then staging, then production. A production model version ahead of the "
              "one the harness ran against means your gate measured something you are not running, and "
              "nobody will notice until the numbers stop matching the complaints."},
   {"do": "Keep secrets out of prompts, context files and traces",
    "detail": "Three leak paths an ordinary application does not have: a prompt is logged, a context "
              "file is committed, and a trace is read by people outside the team. Store in AWS Secrets "
              "Manager and resolve at runtime with "
              "`{{resolve:secretsmanager:<secret-id>:SecretString:<json-key>}}`, so the value is never "
              "in the template, the repository, the log or your shell history."},
   {"do": "Seed the evaluation environment with real cases, redacted",
    "detail": "Mask field by field and keep the shape, the volume and the mess. Invented cases are drawn "
              "from what somebody imagined the input looks like, which is precisely the distribution the "
              "system already handles well."},
   {"do": "Give each environment a different failure mode for real actions",
    "detail": "Dev holds no credential for the partner API at all; evaluation uses a recorded double; "
              "staging writes to a sandbox tenant; only production can move money. If dev *can* reach "
              "the real endpoint, one day at 23:40 it will."},
 ],
 "ai": [
   {"tool": "Claude Code",
    "use": "Write the redaction pass over a production export: masked field by field with the format "
           "preserved, plus a manifest of exactly which fields it touched. The manifest is the "
           "reviewable artefact, and it is the part a person signs.",
    "caution": "Read the field manifest, not the output. A redactor that missed a column produces output "
               "that looks perfectly clean, because the column it missed looks like data."},
   {"tool": "Claude Code",
    "use": "Have it diff two environment manifests and report every difference, not only the ones you "
           "asked about: model version, region, temperature, tool list, timeout, cap. Then make that "
           "diff a CI step.",
    "caution": None},
   {"tool": "Chat LLM",
    "use": "Ask what could differ between two environments that a manifest diff would *not* catch — a "
           "quota, a data volume, a warm cache, a partner sandbox that behaves differently under load.",
    "caution": "Its list is a prompt for your own list, not a checklist. It does not know your partners "
               "and it will not mention the one that matters."},
   {"tool": "Do not delegate",
    "use": "Confirming that a redacted export is safe to put in an evaluation environment. Somebody with "
           "accountability reads the rows, because the cost of being wrong is a regulator rather than a "
           "re-run.",
    "caution": None},
 ],
 "artifact": {
   "name": "Environment manifest set",
   "good": "One diffable file per environment, with the model version pinned and dated, every secret as "
           "a runtime reference rather than a value, and a named source for the seed data.",
   "owner": "Platform engineer"},
 "template": {
   "title": "Environment manifest", "lang": "yaml",
   "body": """# environments/prod.yaml - one file per environment. CI diffs these on every PR.
# Nothing in here is a value that must stay secret. Secrets are references.
environment: prod
region: <eu-west-1>
account: "123456789012"

model:
  # PINNED. A floating alias changes behaviour with no deploy and no diff.
  primary: eu.anthropic.<model-id>
  cheap: eu.anthropic.<small-model-id>
  judge: eu.anthropic.<judge-model-id>    # pinned separately; see step 4
  temperature: 0.0
  max_tokens: 1024
  # Bump in its own pull request. The harness re-runs. Rollback path in step 8.
  pinned_on: <YYYY-MM-DD>
  pinned_by: <name>

gateway:
  endpoint: <https://gateway.internal.example/v1>
  key_alias: <feature>-prod
  monthly_budget_usd: <n>

secrets:
  # Runtime resolution only. Never a value here, never in a prompt, never in a
  # context file, never in a trace.
  partner_api_key: "{{resolve:secretsmanager:<feature>/prod/partner-api:SecretString:api_key}}"
  desk_webhook: "{{resolve:secretsmanager:<feature>/prod/desk:SecretString:url}}"

data:
  seed: none                  # prod runs on prod data
  vector_index: <collection-name>
  # eval.yaml instead reads:
  #   seed: s3://<bucket>/seed/<yyyy-mm-dd>-redacted-400.jsonl
  #   redaction_manifest: docs/redaction-<yyyy-mm-dd>.md   (signed by <name>)

actions:
  # What this environment is permitted to actually do.
  partner_api: live           # dev: absent, eval: recorded double, staging: sandbox
  issue_refund: gated         # named approver; cap enforced in the tool signature
  email_passenger: live

limits:
  max_loops: 5
  max_tokens_per_case: <n>
  max_cost_per_case_usd: <n>

flags:
  shadow_only: false
  canary_percent: 5
"""},
 "prompts": [
   {"title": "Redact a production export for the evaluation environment",
    "when": "Seeding evaluation, before anyone writes a case by hand",
    "body": """Redact this production export so it can be used as evaluation seed data.

RULES:
- MASK, never drop. Preserve type, length class and format: a 16-digit card becomes
  ************4471, an email becomes a****@e******.com, a date keeps its shape.
- Keep the mess. Typos, truncation, mixed casing, empty fields and duplicate records
  are the distribution. Do not clean anything.
- Free-text fields are the hard part. List every one and tell me what you found in it,
  rather than deciding for me whether it is safe.
- Do not invent rows and do not drop rows. The row count must match exactly.

OUTPUT SHAPE:
1. The redaction script.
2. A MANIFEST: one row per field - name, classification, what was done to it, and an
   example before/after using synthetic values, never real ones.
3. A list of fields you were unsure about, with the question you need answered.

The manifest is what a human signs. Write it for that reader.

SCHEMA / SAMPLE: <paste>"""},
   {"title": "Diff two environment manifests like a reviewer",
    "when": "Before every promotion, and whenever a score moves with no deploy",
    "body": """Compare these two environment manifests.

OUTPUT SHAPE - one table:
| Field | <env A> | <env B> | Intended difference? | Could it change behaviour? |

RULES:
- Report EVERY difference, including ones I did not ask about and ones that look
  cosmetic. Whitespace and ordering can be excluded; nothing else can.
- Put model version, judge version, temperature, max_tokens, tool list and the caps at
  the TOP of the table regardless of file order. Those are the behaviour-bearing ones.
- For any field that is a floating alias rather than a pinned version, say so loudly
  and separately. That is the finding, not a row.
- Finish with: the one difference most likely to explain a score gap between these two
  environments, and the command that would confirm it.

MANIFEST A: <paste>
MANIFEST B: <paste>"""},
   {"title": "A model upgrade as a change record",
    "when": "A newer model version is available and somebody wants it",
    "body": """Write the change record for upgrading <feature> from <model version A> to
<model version B>. Treat it as a deployment, not a configuration tweak.

It must state:
1. Which environments change, in what order, and what gates between them.
2. What re-runs: the full golden set, the judge calibration set, the injection suite.
   Give the expected cost and wall-clock time of that run.
3. What the rollback is, exactly - which file, which command, and how long it takes.
4. Which slices are most likely to move, and why. Be specific about the slice, not
   about the model.
5. What evidence would make us abandon the upgrade rather than debug it.

RULES:
- Do not claim the new version is better. That is what the harness is for.
- "It should be a drop-in" is not an entry in this document.

CONTEXT: <paste the current manifest, the slice list and the last harness readout>"""},
 ],
 "example": {
   "title": "SkyWays · twelve invented cases",
   "body": "The first evaluation environment was seeded with twelve cases somebody wrote by hand on a "
           "Friday. Every one had a single passenger, a single delayed leg, a same-day alternative and "
           "no partner airline. The harness returned 94% and the team believed it for a fortnight. "
           "Codeshare — 11% of real traffic and the slice carrying all the risk — was not in the seed at "
           "all, because nobody imagines a mess they have not read. Re-seeding from a redacted export of "
           "400 real cases took a day and dropped the score to 79%, which was the first honest number "
           "the project had."},
 "pitfalls": [
   "A floating model alias in one environment. The score moves with no deploy, and the first three hours "
   "go into reading a diff that is empty, because the thing that changed was not in the repository.",
   "A secret in a prompt or a context file. It is now in the trace store, in the log aggregator and in the "
   "request that left your account, and rotating it is the easy part of what follows.",
   "Seeding evaluation with invented cases. They are drawn from what somebody imagined the input looks "
   "like, so the harness measures the system against the easy half of its own traffic and reports it as a score.",
 ],
 "done_when": "A diff between any two environment manifests shows only differences you can name and "
              "defend, and the pinned model version is one of the lines it shows.",
},
]
