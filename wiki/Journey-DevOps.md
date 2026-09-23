# DevOps and platform · the journey, end to end

**From a laptop to production, repeatably**

8 steps · 53 sub-steps · 8 templates · 24 prompts

This is the reading copy. The [interactive version](https://akash-coded.github.io/aws-bedrock-agentcore-strands/devops/) has a copy button on every template and prompt, which is what you want when you are actually doing the work.

For the method behind it — the loops, the gates, the formulas — see [Role DevOps](Role-DevOps).

---

Your job has not changed. Accounts, pipelines, deployments, permissions, recovery — the list is the same list, and most of what you already know transfers intact. Three things underneath it are new, and every step below is one of them working through. The **model version is part of the environment**, so an environment can change behaviour with no deploy and no diff. The **bill moves with behaviour** rather than with traffic, so capacity planning becomes cost instrumentation. And **text is an attack surface**, so an input is now something that can instruct.

The second thing that changes is the order. A budget alarm is worth little in month three and a great deal in week one. Model access sits in somebody else's approval queue, so it is a lead-time item started on day one rather than a task scheduled for the week you need it. And the evaluation harness has to be a required status check *before* the first release is under time pressure, because that is the week it would otherwise quietly be made optional.

Eight steps. Each one ends in something committed to a repository rather than configured in a console, because the capability you are actually building is the ability to destroy an environment and get it back.

## The arc

| # | Step | What it produces |
| --- | --- | --- |
| 1 | [**Baseline** — Stand up the account, the tags and the budget first](#1--baseline) | Landing zone stack and cost baseline |
| 2 | [**Access** — Get model access, then put every call behind one gateway](#2--access) | Model access matrix and gateway config |
| 3 | [**Environments** — Make the environments comparable, model version included](#3--environments) | Environment manifest set |
| 4 | [**Pipeline** — Make the harness a status check the merge cannot bypass](#4--pipeline) | Pipeline definition and the slice map |
| 5 | [**Deploy** — Ship behind a flag, and treat the prompt as a deployable artefact](#5--deploy) | Flag configuration and the deploy path |
| 6 | [**Observe** — Instrument the three signals a normal stack does not have](#6--observe) | Trace schema, cost record and the alarm set |
| 7 | [**Protect** — Give the agent the smallest identity that can do the job](#7--protect) | Execution role policy, egress allowlist and injection suite |
| 8 | [**Recover** — Rehearse the rollback and cap the runaway](#8--recover) | Rehearsed recovery runbook and the containment caps |

## What is yours, and what is not

| Yours to own | Not yours — stop signing these |
| --- | --- |
| The **landing zone** — accounts, isolation, and a tag scheme that makes cost attributable per feature | The **acceptance bar** per slice. The product manager derives it and QA curates the cases; your job is to make the gate unarguable, not to set it |
| The **model gateway** — one layer every call passes through, with a per-call log nobody can route around | **Prompt content.** You version it, deploy it and roll it back. You do not write it |
| The pipeline, including the evaluation harness as a required status check rather than a comment | Which slices exist and what a wrong answer costs in each — that is the business's answer, and it is the input to your caps rather than your output |
| Three deployable artefacts and three rollback paths: the code, the prompt, and the model version | The behaviour, release and expansion gates. You supply the evidence and the rollback; somebody else signs |
| The **enforced** controls — execution role scope, egress, caps in tool signatures — as distinct from the requested ones |  |
| The kill switch, the containment caps, and the rehearsed recovery times |  |

## How to use a model in this role

> Use a model where there is a schema to be right against and a cheap way to check. It is genuinely strong at CloudFormation, workflow YAML, IAM policy shapes and the first draft of a script, and it is confidently wrong about your account boundaries, your regions, your quotas and what a permission actually reaches. The pattern that works: the model writes the change, a machine judges it — `cfn-lint`, `cdk diff`, a plan output, IAM Access Analyzer, a test — and you read the diff rather than the prose. Anything that widens a permission, opens an egress path or touches a production boundary is read line by line by a person, because a model cannot estimate a blast radius it has never had to unwind. Where a step below says *do not delegate*, that is the reason.

---

## 1 · Baseline

### Stand up the account, the tags and the budget first

*Week one, alongside discovery, before any resource exists*

The platform question for an agentic workload is not different in kind from any other. It is different in *when*. Two of the things this workload needs bill for **existing** rather than for use — an OpenSearch Serverless collection holds capacity while it exists, and an AgentCore runtime holds an environment — so the ordinary habit of standing something up to try it and tidying up later produces a fixed monthly charge with no feature attached to it. Four things go in before the first feature branch: an account boundary, a tag scheme that attributes cost per feature, infrastructure as code, and a budget alarm.

**What you actually do**

1. **Separate the accounts before you separate the stacks** — One account per environment, under Organizations or Control Tower. It is a blast-radius boundary and a billing boundary at the same time, and it is the only one of the two that cannot be retrofitted cheaply. An experiment in the production account is a quota and a bill you will be untangling in month three.
2. **Tag per feature, not per team** — `Feature`, `Environment`, `Owner`, `CostCentre`. Teams re-org and features do not. The question you will be asked is *what did rebooking cost last month*, and a team tag cannot answer it for any month before the re-org.
3. **Activate the cost allocation tags in the payer account the same day** — A tag on a resource is invisible to Cost Explorer until that user-defined tag key is activated in the management account, and the data starts flowing from activation. A backfill request exists; do not plan around it. A tag activated in month three does not label months one and two.
4. **Put every resource in CDK or CloudFormation from the very first one** — Not because click-ops is untidy. Because the first thing you will genuinely need is to delete an environment entirely and rebuild it, and the console has no undo. Teardown is the feature you are buying.
5. **Create the budget and its alarm before anything that costs money** — An actual `AWS::Budgets::Budget` with an SNS action and a named owner, not a calendar reminder. Put the threshold at the forecast the product manager defended, with a notification on actual spend and a second on *forecast*, which is the one that gives you a fortnight's warning instead of a bill.
6. **Keep a written register of what bills for existing** — Collections, runtimes, provisioned throughput, NAT gateways, idle endpoints. Each with an owner and a teardown command, in the repository, reviewed weekly. Nothing goes quiet when the traffic does, so the only control is a list somebody reads.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Generate the landing-zone stack from a written statement of your boundaries, and have it run `cfn-lint` and `cdk diff` itself. The review you then do is of a diff rather than of prose, which is the difference between checking and reading.<br>⚠ It will invent a region and a partition. Check every hard-coded region and every `arn:aws:` against the residency answer you actually have. |
| **Claude Code, read-only credentials** | Point it at an existing account and have it produce two lists: resources with no `Feature` tag, and resources belonging to no stack. Those two lists are the whole of the cost problem in most inherited accounts.<br>⚠ Give it a role that cannot delete or modify anything. An audit script that tidies up as it goes is how a shared dev environment disappears on a Friday. |
| **Chat LLM** | Draft the tag dictionary and its allowed values, then ask it which of your four cost questions the scheme still cannot answer. It is reliable at finding the question with no tag behind it. |
| **Do not delegate** | The account boundary, and what is allowed to live in production. Blast radius is a business fact — which failures you can survive and who has to explain them — and a model has no way to estimate it. |

**The artefact**

| | |
| --- | --- |
| Produces | **Landing zone stack and cost baseline** |
| Good looks like | One repository that creates an empty, near-zero-cost environment from nothing and destroys it again, a budget alarm that fires before a human notices, and a tag on every resource naming the feature that pays for it. |
| Owner | Platform engineer |

<details><summary><b>Template · Cost baseline, deployed before anything else</b></summary>

```yaml
# baseline.yaml - deploy BEFORE anything that can cost money.
# aws cloudformation deploy --template-file baseline.yaml --stack-name <feature>-baseline \
#   --parameter-overrides Feature=<feature> MonthlyBudgetUsd=<n> AlertEmail=<alias> \
#   --tags Feature=<feature> Environment=<env> Owner=<name> CostCentre=<code>
# Always-on register, reviewed weekly, each with an owner and a teardown command
# (these bill for EXISTING, not for use): OpenSearch Serverless collections,
# AgentCore runtimes, provisioned throughput, NAT gateways, idle endpoints.
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
          # Activate this key in the payer account today: cost data starts at activation.
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
```

</details>

<details><summary><b>Prompt · Baseline stack from a boundary statement</b> — Nothing exists yet and you are about to create the first resource</summary>

```text
You are writing the baseline infrastructure for a new agentic feature. Nothing
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
<paste: accounts, regions, who pays, the residency answer, who gets the alert>
```

</details>

<details><summary><b>Prompt · Find what is billing for existing</b> — You inherited an account, or the bill has a line nobody can name</summary>

```text
Audit this account for resources that bill for EXISTING rather than for use.

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
- Finish with the one resource I should deal with today, and why it is that one.

ACCOUNT AND SCOPE: <paste the profile, the regions, and anything already known to be
deliberate>
```

</details>

<details><summary><b>Prompt · Does this tag scheme answer the questions</b> — Before you activate cost allocation tags, because activation is not retroactive</summary>

```text
Review this tag scheme against the only four questions it will ever be asked.

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

SCHEME: <paste>
```

</details>

**Worked example · SkyWays · the line item nobody could name**

> In week two an engineer stood up an OpenSearch Serverless collection to try retrieval over the fare rules. It was never wired into anything, and it was never switched off. On day 75 the bill came in at 4.4 times its estimate; that multiple was traced to four ordinary habits compounding, and the collection was not even part of it — it was a separate line that took an afternoon to attribute, because it carried no `Feature` tag and belonged to no stack. Two controls would have made it a two-minute question: a tag activated in week one, and a weekly read of the always-on register.

**Pitfalls**

- Standing up a collection or a runtime to try something, and relying on remembering to remove it. Both bill for existing, so a forgotten experiment is a fixed monthly cost attached to no feature and no owner.
- Tagging by team. The re-org lands in nine months and the question *what did rebooking cost* becomes permanently unanswerable for every month before it.
- Activating cost allocation tags late. The tags were there all along, the cost data was not, and the first three months of spend can never be attributed — which is exactly the period you will be asked about.

**Done when** — You can destroy a whole environment and rebuild it from the repository, and Cost Explorer can tell you what one feature cost last month without anyone opening a spreadsheet.

---

## 2 · Access

### Get model access, then put every call behind one gateway

*The request on day one; the gateway before the second team calls Bedrock directly*

Two things happen here and they move at different speeds. Model access in Bedrock is granted per model, **per region**, on request, and the approval sits in somebody else's queue — which makes it a lead-time item started on day one, not a task scheduled for the week you need it. The gateway is a build: one layer every model call passes through, so routing, budgets, fallbacks and a per-call log exist in one place instead of in four codebases. Without the per-call log you cannot diagnose a bill. You can only argue about it.

**What you actually do**

1. **Request model access on day one, per model and per region** — Access granted in `us-east-1` is not access in `eu-west-1`. Some models ask for a use case before approval and some approvals are not instant. Put the requests in before the architecture is finished; withdrawing an unused request costs nothing and waiting on a missing one costs a week.
2. **Use the inference profile ID, not the bare model ID** — Many current models are only callable through a cross-region inference profile, whose identifier carries a geography prefix — `us.`, `eu.`, `apac.` — in front of the model ID. A bare ID returns a validation error telling you to retry with an inference profile. This is the single most common first-day error, and it reads like a permissions problem, so teams spend the morning in IAM.
3. **Read the quotas that actually apply to this account** — Requests and tokens per minute are per account, per region, per model, and the account default is not the published headline. Get the real numbers from Service Quotas on day one. An increase is another lead-time item with another queue.
4. **Put one gateway in front of everything** — LiteLLM is the common choice: an OpenAI-compatible endpoint in front of Bedrock, so routing, retries, fallback and budgets are configuration rather than code. The value is not the abstraction. It is that there is one place to change a model and one place that sees every call.
5. **Make the per-call log non-optional** — Request id, feature, environment, model version, input tokens, output tokens, **cached tokens**, latency, cost, case id. Without the cached-token column the cache is a belief rather than a measurement. Without the feature column the bill is one number.
6. **Write routing and fallback as policy, not as a try/except** — Cheap tier for classification and extraction, the capable tier for the judgement call, a named fallback when a region throttles. In the gateway config, reviewed like code, identical in every environment. A retry policy buried in application code is a cost multiplier nobody can find.
7. **Issue a gateway key per feature, with its own budget** — Not a key per person and not one shared key. A virtual key per feature makes the budget enforceable at the call rather than at the month end, and it splits the bill on exactly the same boundary as your resource tags.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it write a probe that calls every model you believe you have access to, in every region you plan to use, trying the bare ID and then the profile ID, and prints a matrix. Ten minutes of work that settles a week of guessing.<br>⚠ One-word prompt, `max_tokens` of 1, no retries. A probe that writes a paragraph per model per region is a bill of its own. |
| **Claude Code** | Generate the gateway config from the access matrix, and have it diff the config against the grants you actually hold so an aspirational model cannot reach production.<br>⚠ It will happily emit a bare model ID. Grep the config for any model string without a geography prefix before you deploy it, and make that grep a CI step. |
| **Chat LLM** | Draft the access-request justification per model: what it is for, what data reaches it, what the volume will be. The reviewer's questions are predictable and the answers are the same ones your architecture review needs anyway. |
| **Do not delegate** | Which models are permitted for which data. That is a residency and contract question about your own organisation, and a model reading your config cannot know that a partner's fare data is not allowed to leave a geography. |

**The artefact**

| | |
| --- | --- |
| Produces | **Model access matrix and gateway config** |
| Good looks like | A committed table of model, region, status and date requested, and one gateway config used by every environment whose per-call log already has a feature column and a cached-token column in it. |
| Owner | Platform engineer |

<details><summary><b>Template · Model gateway config</b></summary>

```yaml
# litellm-config.yaml - the one layer every model call goes through.
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
  #   litellm --create-key --models judge,classify --max-budget <n> \
  #     --budget-duration 30d --key-alias <feature>-prod
  max_budget: <n>
  budget_duration: 30d
```

</details>

<details><summary><b>Prompt · Probe what this account can actually call</b> — Day one, before anyone designs around a particular model</summary>

```text
You are helping a platform engineer establish which Bedrock models this account
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

PAIRS: <paste model ids and regions>
```

</details>

<details><summary><b>Prompt · Gateway config from the access matrix</b> — The matrix is settled and the second team is about to start calling Bedrock</summary>

```text
Write a LiteLLM proxy config from the access matrix below.

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

MATRIX: <paste>
```

</details>

<details><summary><b>Prompt · Triage a first-day Bedrock failure</b> — The first call fails and someone has already opened the IAM console</summary>

```text
A Bedrock call is failing. Work through these IN ORDER and tell me which it is,
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
<paste>
```

</details>

**Worked example · SkyWays · the six days nobody had planned**

> The architecture was signed on day 12 and the first call was written on day 13, in `eu-west-1`, with a bare model ID. Two hours went into IAM before somebody read the error properly and saw it was asking for an inference profile. The larger cost was underneath: access had been granted in `us-east-1` in week one, so everyone assumed the account had it, and nobody had requested `eu-west-1` at all. Six days. The plan had allowed zero. Once the gateway went in, the same class of mistake became a one-line config change rather than four codebases and a guess about which one was still wrong.

**Pitfalls**

- Treating model access as a task rather than a lead-time item. It sits in someone else's queue, so a plan that schedules it as a day's work in week four discovers the truth in week five.
- The bare model ID. It fails with something that reads like a permissions error, so the team spends the morning widening IAM policies — which then ship, over-permissive, and are never narrowed again.
- Letting one team call Bedrock directly 'just for now'. The per-call log then has a hole in it, and the hole is always exactly the team whose spend you were asked to explain.

**Done when** — Every model call in every environment goes through one endpoint, and you can produce yesterday's cost split by feature from its log without asking anybody for anything.

---

## 3 · Environments

### Make the environments comparable, model version included

*P1, before the harness has anything meaningful to run against*

Environment parity is an old discipline with a new member. For a deterministic system, parity means the same code, the same configuration and the same data shape. For a probabilistic one the **model version is part of the environment**, and an unpinned model changes behaviour with no deploy, no error and no line in any diff. So every environment pins its model, and a model upgrade becomes a deployment that re-runs the harness. Two other things break parity here in ways they do not elsewhere: secrets, which must never reach a prompt, a context file or a trace; and evaluation data, which must be real cases rather than invented ones.

**What you actually do**

1. **Pin the model version per environment, in the manifest** — The full versioned identifier, never a floating alias. An alias that moves silently is the same failure as `latest` on a container image, except that the symptom is a score drop with no deploy to blame and three hours spent reading an empty diff.
2. **Treat a model upgrade as a deployment** — Its own pull request, its own harness run, its own rollback path, its own note in the release record. The new version is better on average and *different on your slices*, and average is not what you ship.
3. **Promote the model through environments in the same order as the code** — Evaluation first, then staging, then production. A production model version ahead of the one the harness ran against means your gate measured something you are not running, and nobody will notice until the numbers stop matching the complaints.
4. **Keep secrets out of prompts, context files and traces** — Three leak paths an ordinary application does not have: a prompt is logged, a context file is committed, and a trace is read by people outside the team. Store in AWS Secrets Manager and resolve at runtime with `{{resolve:secretsmanager:<secret-id>:SecretString:<json-key>}}`, so the value is never in the template, the repository, the log or your shell history.
5. **Seed the evaluation environment with real cases, redacted** — Mask field by field and keep the shape, the volume and the mess. Invented cases are drawn from what somebody imagined the input looks like, which is precisely the distribution the system already handles well.
6. **Give each environment a different failure mode for real actions** — Dev holds no credential for the partner API at all; evaluation uses a recorded double; staging writes to a sandbox tenant; only production can move money. If dev *can* reach the real endpoint, one day at 23:40 it will.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Write the redaction pass over a production export: masked field by field with the format preserved, plus a manifest of exactly which fields it touched. The manifest is the reviewable artefact, and it is the part a person signs.<br>⚠ Read the field manifest, not the output. A redactor that missed a column produces output that looks perfectly clean, because the column it missed looks like data. |
| **Claude Code** | Have it diff two environment manifests and report every difference, not only the ones you asked about: model version, region, temperature, tool list, timeout, cap. Then make that diff a CI step. |
| **Chat LLM** | Ask what could differ between two environments that a manifest diff would *not* catch — a quota, a data volume, a warm cache, a partner sandbox that behaves differently under load.<br>⚠ Its list is a prompt for your own list, not a checklist. It does not know your partners and it will not mention the one that matters. |
| **Do not delegate** | Confirming that a redacted export is safe to put in an evaluation environment. Somebody with accountability reads the rows, because the cost of being wrong is a regulator rather than a re-run. |

**The artefact**

| | |
| --- | --- |
| Produces | **Environment manifest set** |
| Good looks like | One diffable file per environment, with the model version pinned and dated, every secret as a runtime reference rather than a value, and a named source for the seed data. |
| Owner | Platform engineer |

<details><summary><b>Template · Environment manifest</b></summary>

```yaml
# environments/prod.yaml - one file per environment. CI diffs these on every PR.
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
```

</details>

<details><summary><b>Prompt · Redact a production export for the evaluation environment</b> — Seeding evaluation, before anyone writes a case by hand</summary>

```text
Redact this production export so it can be used as evaluation seed data.

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

SCHEMA / SAMPLE: <paste>
```

</details>

<details><summary><b>Prompt · Diff two environment manifests like a reviewer</b> — Before every promotion, and whenever a score moves with no deploy</summary>

```text
Compare these two environment manifests.

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
MANIFEST B: <paste>
```

</details>

<details><summary><b>Prompt · A model upgrade as a change record</b> — A newer model version is available and somebody wants it</summary>

```text
Write the change record for upgrading <feature> from <model version A> to
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

CONTEXT: <paste the current manifest, the slice list and the last harness readout>
```

</details>

**Worked example · SkyWays · twelve invented cases**

> The first evaluation environment was seeded with twelve cases somebody wrote by hand on a Friday. Every one had a single passenger, a single delayed leg, a same-day alternative and no partner airline. The harness returned 94% and the team believed it for a fortnight. Codeshare — 11% of real traffic and the slice carrying all the risk — was not in the seed at all, because nobody imagines a mess they have not read. Re-seeding from a redacted export of 400 real cases took a day and dropped the score to 79%, which was the first honest number the project had.

**Pitfalls**

- A floating model alias in one environment. The score moves with no deploy, and the first three hours go into reading a diff that is empty, because the thing that changed was not in the repository.
- A secret in a prompt or a context file. It is now in the trace store, in the log aggregator and in the request that left your account, and rotating it is the easy part of what follows.
- Seeding evaluation with invented cases. They are drawn from what somebody imagined the input looks like, so the harness measures the system against the easy half of its own traffic and reports it as a score.

**Done when** — A diff between any two environment manifests shows only differences you can name and defend, and the pinned model version is one of the lines it shows.

---

## 4 · Pipeline

### Make the harness a status check the merge cannot bypass

*P1 into P2, before the first feature branch and before the first deadline*

CI for a system that is right *a share of the time* keeps every stage you already have and adds two: the evaluation harness, and a gate that reads its output per slice. The difference from ordinary CI is economic rather than technical. Tests are fast and free, so they run on everything; evaluation is slow and costs real money, so it cannot. The shape that works is the touched slice on every pull request, the full set nightly, cached model responses so a fixed golden set replays deterministically, and a required status check — because a gate a person can click past is a report.

**What you actually do**

1. **Keep the fast, free stages first and unchanged** — Build, lint, types, unit tests, and the **exact** tests over the deterministic parts: the fare rules, the cap arithmetic, the schema validation. Most bugs in an agentic system are ordinary bugs, and they should fail in ninety seconds rather than after twelve minutes of paid evaluation.
2. **Run only the touched slice on a pull request** — A committed file maps paths to slices, so a change under the codeshare prompt runs the codeshare set. Ten minutes and a few dollars, not ninety minutes and a few hundred. The map is reviewed like code, because a wrong map is a silent gap in the gate.
3. **Run the full set nightly, and on any prompt or model change** — Those two changes touch every slice by definition, so the slice map does not apply to them. Wire that as a condition in the workflow rather than as a convention, because a convention is what gets skipped at 18:40 on a Thursday.
4. **Cache model responses so the golden set replays deterministically** — Key on (model version, prompt hash, input hash). A run over an unchanged golden set with an unchanged prompt should cost close to nothing and produce the same answer twice. When it does not, that divergence is itself the finding and you want to know immediately.
5. **Pin and version the judge** — The judge is a model call too. Pin its version, keep its prompt in the repository, and re-run the calibration set whenever either changes. An unpinned judge moves every score at once, which looks exactly like a product regression and costs a week.
6. **Gate on the per-slice score with its lower bound** — The gate reads the bar sheet the product manager owns and fails when any slice's 95% lower bound sits below its bar. One overall percentage is how the easy high-volume slice carries the average while the slice with the money in it ships broken.
7. **Make it a required status check in branch protection** — Not a job that posts a comment. If a human can merge past it while the room is waiting for a release, then eventually someone will, and the person who does it will be senior enough that nobody objects.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Have it write the workflow, the slice map and the cache key, then prove the cache works by running the golden set twice and diffing the cost. Two runs and one number is the whole test, and it takes five minutes. |
| **Claude Code** | Have it build the report step: per slice, score, n, lower bound, bar, pass or fail, rendered as a job summary rather than buried in a log. The shape of the readout decides whether anyone reads it.<br>⚠ Check the lower-bound arithmetic yourself, once, by hand. A gate computing the wrong interval passes everything, and nothing about it looks broken. |
| **Chat LLM, cheap tier** | Maintain the file-to-slice map: given a diff, which slices could this plausibly touch? Useful as a suggestion that a human confirms into the committed map.<br>⚠ It will under-select. Default to running more slices whenever the mapping is ambiguous, because the failure mode of running too few is the one that produces no signal at all. |
| **Do not delegate** | The decision to merge past a red check. There are legitimate reasons to do it, and every one of them is a named person accepting a named risk in writing. |

**The artefact**

| | |
| --- | --- |
| Produces | **Pipeline definition and the slice map** |
| Good looks like | A pull request that cannot merge with any slice below its bar, a nightly full run, and a per-slice summary a product manager can read without opening a log or asking a question. |
| Owner | Platform engineer, with the QA lead on the slice map |

<details><summary><b>Template · CI with the harness as a required check</b></summary>

```yaml
# .github/workflows/agent-ci.yml
# Fast and free first. Slow and paid only on what changed.
name: agent-ci

on:
  pull_request:
  schedule:
    - cron: "0 2 * * *"        # the FULL set, nightly

permissions:
  id-token: write              # OIDC. No long-lived keys in the repository.
  contents: read

jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -r requirements-dev.txt && ruff check . && mypy src
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
        # A prompt or model change touches everything, so the map does not apply.
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            python tools/slice_map.py --diff "origin/${{ github.base_ref }}...HEAD" >> "$GITHUB_OUTPUT"
          else
            echo "slices=all" >> "$GITHUB_OUTPUT"
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
# Branch protection: `eval` is a REQUIRED status check. A job that only comments
# is a report, and a report has never stopped a release.
```

</details>

<details><summary><b>Prompt · Build the file-to-slice map</b> — Setting the pipeline up, and again whenever a slice is added</summary>

```text
Build the map from repository paths to evaluation slices, so a pull request runs
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

OUR SLICES AND LAYOUT: <paste the tree and the slice names>
```

</details>

<details><summary><b>Prompt · Per-slice gate readout</b> — The harness runs but nobody can read its output</summary>

```text
Write the gate step that turns harness output into a decision.

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

Show me the lower-bound function and its unit test first; I want to check that by hand.

HARNESS OUTPUT FORMAT: <paste a sample>
BAR SHEET: <paste>
```

</details>

<details><summary><b>Prompt · Cost the pipeline before you switch it on</b> — Before making the harness a required check, so nobody can argue it later</summary>

```text
Work out what this pipeline will cost to run, so the number arrives before the
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

INPUTS: <golden set size, tokens per case, model prices, PR volume>
```

</details>

**Worked example · SkyWays · the check that could be clicked past**

> For three weeks the harness ran on every pull request and posted a comment. Nobody disabled it and nobody ignored it on principle. Then on the Thursday before the pilot the codeshare slice came back red, the release was in the calendar, and a senior engineer merged with the comment open in another tab — reasonably, in the moment, and with every intention of fixing it on Monday. The fix afterwards was one setting: the harness became a required status check. The argument that setting ended had been running since the harness was built.

**Pitfalls**

- Running the full evaluation on every push. It is slow and it is paid, so within a fortnight somebody makes it optional to unblock a release, and an optional gate is not a gate.
- Gating on one overall score. The easy slice is the high-volume one, so it lifts the average while the slice carrying the money fails quietly underneath it.
- An unpinned judge. Its version moves, every score moves with it, and a week goes into hunting a product regression that is actually a change in the measuring instrument.

**Done when** — A pull request with any slice below its bar cannot be merged, and the person who tried can see which slice and by how much without opening a log.

---

## 5 · Deploy

### Ship behind a flag, and treat the prompt as a deployable artefact

*The end of P2, at cut-over, and on every change after it*

The flag is the deployment primitive, because the rollback has to be faster than the incident. Four states, taken one at a time: **shadow**, where the agent decides on real traffic and acts on nothing; **5% canary**; **widen on evidence**; then all of it. The flag is also the rollback, which is why it gets tested rather than believed. The part teams miss is that code is not the only deployable thing here. A prompt change and a model version change alter behaviour with no build, so they need the same versioning, the same review and the same rollback path as the binary — and a prompt change is the most common production change there is.

**What you actually do**

1. **Make shadow a state of the system, not a branch** — Same code path, same inputs, decisions written to the trace store, the write side disabled by the flag. A separate shadow branch tests the shadow branch, and the first live call then runs code nobody has exercised.
2. **Make 'shadow never writes' an automated test** — An assertion in the harness *and* a scheduled canary in production: with the flag in shadow, any call reaching a write tool fails the build and pages. The sentence in the runbook is a request; the assertion is the control.
3. **Blue/green the runtime and keep both warm through the window** — Two versions serving, traffic shifted by the flag rather than by DNS, the old one warm until the widening finishes. AgentCore runtime versions behind an alias, or two task sets behind a load balancer — the mechanism matters far less than being able to shift back in seconds without a deploy.
4. **Version the prompt and the model as first-class artefacts** — A prompt lives in the repository with a hash, ships as a versioned object, and is referenced *by version* at runtime. It gets a pull request, a harness run and a rollback path. Editing a prompt in a console is a behaviour change with no diff and nothing to go back to.
5. **Keep one flag per action, not one per feature** — Refunds can go back to gated while same-day rebooking stays at 100%. A single feature flag forces the whole feature to the caution of its riskiest action, so being careful about one thing means being slow about everything.
6. **Record the flag state and the prompt version in every decision** — Otherwise a trace from three weeks ago cannot be explained, because you no longer know which prompt produced it or whether it was live. This is two fields and it is the difference between an incident review and an argument.
7. **Write the widening condition before the cut-over, not during it** — The live lower bound at or above the bar on that slice for n consecutive days, gated actions still gated. Written while nobody is under pressure, because the conversation at 5% with a sponsor waiting is not the one in which to invent a threshold.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Write the shadow-never-writes test in both places: an assertion in the harness, and a scheduled production canary that checks it against the live flag state. Two places, because the flag can be changed outside a deployment. |
| **Claude Code** | Generate the flag configuration and the code's flag constants from one source, so the two cannot disagree. Then have it fail the build on an unknown flag key.<br>⚠ Insist on that build failure. A typo in a flag name reads as `false` at runtime, which looks exactly like working code that is switched off on purpose. |
| **Chat LLM** | Given a prompt diff, list what behaviour could change and which slices would show it. Use it to decide what to watch after the change rather than what to skip before it.<br>⚠ Run the full set on any prompt change regardless. The point of its list is to predict where to look, never to reduce what runs. |
| **Do not delegate** | When to widen. That is the product manager's gate on live evidence. The platform's job is to make widening a config change and the rollback a faster one. |

**The artefact**

| | |
| --- | --- |
| Produces | **Flag configuration and the deploy path** |
| Good looks like | One flag per action, each with its state, its prompt and model version, its widening condition and its owner, deployed from the same source as the code — and a rollback a person has actually thrown. |
| Owner | Platform engineer, with the product manager on the states |

<details><summary><b>Template · Feature flags, one per action</b></summary>

```json
{
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
      "enabled": true, "mode": "canary", "canary_percent": 5,
      "prompt_version": "<git-sha>",
      "model_version": "eu.anthropic.<model-id>",
      "widen_when": "live lower bound >= 0.86 on same-day for 5 consecutive days",
      "owner": "<name>"
    },
    "rebook_partner": {
      "enabled": true, "mode": "shadow",
      "prompt_version": "<git-sha>",
      "widen_when": "codeshare harness lower bound >= 0.80 AND 14 days shadow agreement >= 0.95",
      "owner": "<name>"
    },
    "issue_refund": {
      "enabled": true, "mode": "gated",
      "cap_usd": 400,
      "approver_role": "<duty-manager>",
      "owner": "<name>"
    }
  }
}
```

</details>

<details><summary><b>Prompt · Write the shadow-never-writes test</b> — Before the shadow run starts, not after the first write</summary>

```text
Write the control that makes "shadow never writes" true rather than intended.

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

OUR WRITE TOOLS AND FLAG SOURCE: <paste>
```

</details>

<details><summary><b>Prompt · Turn a prompt change into a deployment</b> — Somebody wants to 'just tweak the prompt'</summary>

```text
Write the change record for this prompt change. Treat it as a deployment.

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

PROMPT DIFF: <paste>
```

</details>

<details><summary><b>Prompt · Plan the canary and its automatic rollback</b> — Cut-over is scheduled and the flag states need deciding</summary>

```text
Plan the canary for <action>, as a config, not as a narrative.

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

CONTEXT: <slices, bars, cases per day, current flag states>
```

</details>

**Worked example · SkyWays · what the shadow caught and the harness could not**

> The harness had same-day rebooking at 88% and the shadow run agreed with the human desk on 96% of same-day cases. On fourteen cases it did not, and all fourteen were the same thing: the agent proposed a partner airline that the evening shift never uses after 18:00, because that partner's transfer desk closes. The rule was in nobody's spec and nobody's golden set; it lived in the heads of six people. It cost nothing to discover, because the write side was off. At cut-over the flag went to 5% for same-day only; partner rebooking stayed in shadow another fortnight, and refunds never left gated.

**Pitfalls**

- One flag for the whole feature. Refunds then sit at the same setting as showing options, so the only way to be careful about the dangerous action is to be slow about every safe one.
- Shipping a prompt change outside the pipeline. It is a behaviour change with no build, no line in the release notes and nothing to roll back to — and it is the most common production change an agent gets.
- A shadow path that is a separate code branch. It proves the shadow branch works. The first live call then executes code that has never run against real traffic.

**Done when** — You can move any single action from on to shadow and back in under a minute through a recorded config change, and every trace says which flag state and prompt version produced it.

---

## 6 · Observe

### Instrument the three signals a normal stack does not have

*Before the shadow run, not after the first surprise*

Your existing observability answers whether it is up and whether it is fast, and it will keep doing that. None of it answers the three questions this workload is actually judged on: what a case costs, what the system did and why, and whether its behaviour is drifting while every dashboard stays green. Each has a specific trap. Cost per case is meaningless unless cache hits are marked. The trace must mask rather than omit, or the row that would explain the incident is the row that was left out. And drift has no error and no deploy behind it, so it is visible only as a chart with a threshold on it.

**What you actually do**

1. **Emit cost per case, with cache hits marked** — Input tokens, output tokens, **cached tokens**, model version and the derived cost, on one record keyed by case. Marking the cache hit is not tidiness: a cache hit counted as a fresh call inflates the bill you report, and a cache hit counted as a wrong answer gets a working system switched off, which is worse and has happened.
2. **Write one trace row per consequential action, redacted by masking** — Mask, never omit. `card ****4471` is a row you can reconcile; a missing row is an incident you cannot explain. Each row carries the case id, the action, the model version, the prompt version, the tools called, the cap that applied, the approver if there was one, tokens and cost.
3. **Use structured metrics rather than log scraping** — Embedded Metric Format on the log line, so the metric and the row that produced it are the same write and a cost number always has its case beside it. Or OpenTelemetry spans carrying the same attributes. A regex over a text log breaks the first time somebody reformats a message, and it breaks silently.
4. **Chart the output mix weekly and alarm at five percentage points** — The proportions of the decisions the agent makes — refund versus credit versus rebook. A probabilistic system changes behaviour when the world changes, with no deploy and no error. Five points week over week is this playbook's default starting threshold, and the alert re-opens the release gate automatically, which is what turns a chart into a control.
5. **Alarm on the three failure shapes specific to this workload** — Cost per case above three times the estimate, sustained for an hour — a retry loop or a context that has grown. Loop-cap trips above baseline — the agent is going in circles and the cap is quietly doing all the work. Cache hit ratio collapsing — somebody moved a timestamp to the front of the prompt and every call is now full price.
6. **Give the product manager the readout in the shape of their bar sheet** — Per slice, with the lower bound, not one number. The dashboard that gets read is the one shaped like the decision somebody has to make, and the shape is yours to choose.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Write the emitter and its unit tests, including a test that a known cached response produces cost near zero and `cache_hit true`. That single test is what protects the bill report from quietly becoming fiction. |
| **Claude Code** | Generate the alarms as infrastructure from a table of thresholds, so the thresholds are reviewable in one file rather than discovered in a console six months later.<br>⚠ Check the period and the evaluation window yourself. An alarm on a one-minute period over sparse overnight traffic fires all night and is muted by Thursday. |
| **Chat LLM** | Paste a redacted trace row and ask what an incident reviewer could not answer from it. It is reliable at spotting the missing field, and a missing field is far cheaper to find now than during the incident.<br>⚠ Redact before you paste, genuinely. The exercise is about the shape of the row, not its contents, so there is no reason for real values to be in it. |
| **Do not delegate** | Deciding what is masked and what is kept. That is a legal and contractual question about your own data, and the consequence of a wrong guess is either a leak or an incident nobody can explain. |

**The artefact**

| | |
| --- | --- |
| Produces | **Trace schema, cost record and the alarm set** |
| Good looks like | One record per consequential action that an incident reviewer can read cold twelve weeks later, a cost per case that stays correct when the cache is working, and alarms whose thresholds are written where they can be argued with. |
| Owner | Platform engineer |

<details><summary><b>Template · Trace and cost emitter</b></summary>

```python
# trace.py - one write per consequential action: the metric and the row that
# produced it, in the same CloudWatch Logs record (Embedded Metric Format).
# Rule: MASK, never omit. A masked field is a row you can reconcile; a dropped
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
        "Environment": "<prod>", "Slice": slice_name, "Action": action,
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
```

</details>

<details><summary><b>Prompt · Design the trace row from an incident you will have to explain</b> — Before the shadow run, while the schema is still cheap to change</summary>

```text
Design the trace row by working backwards from the incident.

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
  approver. If you think any of those is unnecessary, argue for removing it explicitly.
```

</details>

<details><summary><b>Prompt · Generate the alarm set from a threshold table</b> — Before cut-over, so the thresholds exist in a file rather than in a console</summary>

```text
Turn this threshold table into CloudWatch alarms as infrastructure as code.

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

OUR THRESHOLDS AND TRAFFIC: <paste>
```

</details>

<details><summary><b>Prompt · What can this dashboard not answer</b> — After the dashboard exists and before you rely on it</summary>

```text
Here is our observability setup: <paste dashboards, metrics, alarms, trace schema>.

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
- Rank what is missing by what it would cost us during an incident, not by effort.
```

</details>

**Worked example · SkyWays · the four habits, found in an afternoon**

> On day 75 the bill was 4.4 times its estimate. There was no runaway and no single cause. There were four ordinary habits multiplying: the whole conversation resent as context on every turn (1.6x), the capable model used for classification as well as for the judgement call (1.5x), a cache being missed because a timestamp sat at the front of the prompt (1.3x), and uncapped retries (1.41x). Multiply those and you get 4.4. Finding it took an afternoon rather than a fortnight, and only because the per-call log carried tokens, **cached tokens** and a feature column on every row. Without the cached-token column the third habit is invisible — and the third habit is the one that is free to fix.

**Pitfalls**

- Counting a cache hit as a fresh call, or worse, as a failure. The first overstates the bill; the second has got a working system switched off by a team that believed its accuracy had collapsed overnight.
- Redacting by omission. The schema passes review, the incident arrives, and the row that would have explained it is precisely the row that was dropped for safety.
- Scraping cost metrics out of text logs. The regex survives until somebody reformats a message, and then it fails silently: the chart goes flat, which reads as good news.

**Done when** — For any case in the last thirty days you can produce, in one query, what it cost, which model and prompt version decided it, what it did and who approved it — with nothing unmasked that should not be.

---

## 7 · Protect

### Give the agent the smallest identity that can do the job

*Before the first write tool exists, and again at every new tool*

Least privilege is fifty years old — Saltzer and Schroeder set it out in 1975 — and nothing about an agent changes the principle. What changes is that the thing holding the privilege now decides for itself what to do with it, and it decides partly on text that arrived from outside. So the platform does two jobs. The first is ordinary and rigorous: separate identities for reading and writing, an execution role scoped to the tools this job actually has, egress that cannot reach an arbitrary endpoint, and a residency answer expressed in configuration. The second is new. Every ingested text is untrusted, **including a partner's API response**, and the only defence that holds is that the cap and the confirmation live in the tool contract and the IAM policy rather than in a prompt.

**What you actually do**

1. **Split read from write** — Two roles, two credentials, two audit trails. The retrieval and reasoning path never holds a credential that can change anything. Most of an agent's work is reading, so most of its runtime should be structurally unable to write.
2. **Scope the execution role to the tools in this job's contract** — Not the service — the operations and the resources. `bedrock:InvokeModel` on the two inference profile ARNs you pinned, not on `*`. When a tool is removed from the agent, its permission comes out in the same pull request, or the role only ever grows.
3. **Put the cap and the approver in the tool contract and the policy** — A refund tool whose signature cannot express an amount above the cap cannot issue one, whatever it is told. A prompt saying *never refund more than $400* is a request, and a request can be argued with — by a passenger, by a partner's error text, or by a model that has reasoned its way somewhere reasonable. This is the whole of the lesson.
4. **Control egress explicitly** — Private subnets with no route out except through endpoints you named: VPC endpoints for the AWS services it uses, an allowlist for the partner APIs, everything else refused and logged. An agent that can reach an arbitrary URL can be told to reach one.
5. **Treat every ingested text as untrusted, partner responses included** — A passenger message, an uploaded PDF, a web page and a partner API's free-text `remarks` field are all inputs an attacker can reach. Delimit them, never concatenate them into instructions, strip control sequences — and assume the model will sometimes follow them anyway, which is exactly why the cap is the control and this is only the mitigation.
6. **Answer residency in the configuration, not in a policy document** — Which geography may see which data, expressed as the region of the inference profile, the region of the collection, and a `Deny` on `aws:RequestedRegion` outside the allowed set. A residency answer that exists only in a Word document is not an answer, and it will be tested by a fallback at 03:00.
7. **Treat denials as signal** — An `AccessDenied` from the agent's role is either a tool the job needs and does not have, or the first visible symptom of an injection that partly worked. Both want a human. Alarm on the rate, and never resolve one by widening the policy to make it stop.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Generate the least-privilege policy from the tool contracts, then have it run IAM Access Analyzer policy validation, and again after a week of real traffic for unused-access findings. The second pass is where the over-grant actually comes out.<br>⚠ Never let it widen a policy to make a test pass. Require it to report the exact denied action and resource instead; that denial is the finding, not the obstacle. |
| **Claude Code** | Have it write the injection suite into the harness: a partner response with an instruction in a free-text field, a passenger message impersonating the desk, a PDF with white text. It fails the build if a cap is ever exceeded. |
| **Chat LLM, adversarially** | Paste a tool contract and ask for ten ways a hostile input could get more out of it than intended. It is unusually good at this, because it is the same shape as the thing being attacked.<br>⚠ Its list is not coverage. Everything it finds becomes a test in the harness, and everything it missed is still out there tomorrow. |
| **Do not delegate** | The blast radius of a new permission. What a wrong write costs and who has to unwind it are facts about your business, and a model will approve a wildcard that reads entirely reasonable on the page. |

**The artefact**

| | |
| --- | --- |
| Produces | **Execution role policy, egress allowlist and injection suite** |
| Good looks like | A policy a reviewer reads in two minutes, in which every statement names a resource and maps to a tool in the contract; an egress list with a reason per entry; and a suite of hostile inputs that runs on every pull request with the cap assertion in it. |
| Owner | Platform engineer, with the architect on the tool contracts |

<details><summary><b>Template · Execution role policy · the read identity</b></summary>

```json
{
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
```

</details>

<details><summary><b>Prompt · Derive the policy from the tool contracts</b> — A tool is added, or the role has grown and nobody remembers why</summary>

```text
Derive the least-privilege execution role from these tool contracts. Work from the
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
CURRENT POLICY: <paste>
```

</details>

<details><summary><b>Prompt · Build the prompt-injection suite</b> — Before the agent ingests anything it did not author, which is week one</summary>

```text
Write the injection test suite for our harness. Every ingested text is untrusted,
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

OUR TOOLS, CAPS AND INGESTION POINTS: <paste>
```

</details>

<details><summary><b>Prompt · Find the over-grant from real traffic</b> — A week after go-live, and quarterly thereafter</summary>

```text
Compare what this role is ALLOWED to do against what it has actually done.

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
  break if it is wrong.
```

</details>

**Worked example · SkyWays · the $400 that was only in a prompt**

> On day 82 the agent issued a $2,000 refund. Nothing was hacked and nothing crashed. The $400 cap and the named approver had both been decided on day 12, written into the autonomy record, and repeated clearly in the system prompt. Neither was in the code. The refund tool's signature accepted any amount, and the execution role could invoke it. A passenger message and a partner's delay note between them produced a case the model read as exceptional, and it acted entirely within its permissions and entirely outside its policy. The fix was two lines in a tool signature and one statement in an IAM policy. The postmortem's finding was not a person; it was an absent control.

**Pitfalls**

- A cap that lives in the prompt. A prompt is a request, and a request can be argued past — by a passenger, by a partner's error text, or by the model's own reasoning — and the amount is real money.
- One role for the whole agent. The retrieval step then holds write permission for the entire run, so the blast radius of a single injected instruction is everything the agent could ever do.
- Trusting a partner's API response because it arrived over TLS from a company you have a contract with. The channel is authenticated; the free-text field inside it is typed by somebody you have never met.

**Done when** — A reviewer can read the execution role in two minutes and name, for every statement, which tool in the contract needs it — and the injection suite runs on every pull request with the cap assertion in it.

---

## 8 · Recover

### Rehearse the rollback and cap the runaway

*Before cut-over, then after every incident, forever*

Rollback is a capability, and a capability nobody has used is a belief. Rehearse it before cut-over, with a stopwatch, and write the measured time down. Two things differ from an ordinary service. You may need to roll back a **prompt** or a **model version** rather than code, so each is a versioned artefact with its own path and its own rehearsal. And the failure that costs most here is not a crash but a runaway: an agent that loops, or spends, or acts, faster than anybody is watching. That has three controls — a loop cap, a per-transaction token and cost cap, and a kill switch that degrades to the human desk rather than to an error page.

**What you actually do**

1. **Rehearse every rollback before cut-over, with a stopwatch** — The person who will do it at 02:00 does it once at 14:00 with the runbook open, and the measured time goes into the runbook. If it takes eleven minutes then the incident is eleven minutes long, and everybody can plan around a number they have seen.
2. **Rehearse the prompt and model rollbacks separately** — Three artefacts, three paths. Reverting the container does not revert the prompt version the flag points at, and it does not revert a model version pinned in a manifest. Most teams have only ever tested the first, and discover the other two during the incident.
3. **Cap the loop, the tokens and the spend per transaction** — `MAX_LOOPS=5` as this playbook's default, a token ceiling per case, and a cost ceiling per case, all enforced in the runtime and all emitting a metric when they trip. A cap that trips silently is a cap you learn about from the bill, by which time it has been holding the system together for a month.
4. **Make the kill switch degrade to the desk, not to an error** — Off means the case goes to a human queue with its context attached, not a 500 and a passenger with nothing. A kill switch that causes an outage is one the team hesitates to throw, and the hesitation is most of the cost of the incident.
5. **Name who can throw it without asking** — A list, with times of day, and no approval step. If the on-call engineer needs a director at 02:00, the switch has a four-hour latency written into the org chart rather than into the runbook, and nobody will find it until it matters.
6. **Know what is stateful and rehearse the restore** — The runtime is disposable. Three things are not: the **trace store**, which is your only account of what happened; the **golden set**, which is the measurement itself; and the **vector index**, which is expensive to rebuild and needs its source retained to rebuild from. Back up those three, test the restore, and let the rest be `cdk deploy`.
7. **Turn every incident into a control rather than a name** — The postmortem is finished when it names the enforced control that would have made this class of incident impossible, and where that control will live: a tool signature, a policy statement, a cap. A better prompt is not a control.

**Where a model helps, and where it must not**

| Tool | Use it for |
| --- | --- |
| **Claude Code** | Write the rollback as a script rather than a runbook paragraph, and schedule it to run against a rehearsal environment weekly. A rollback exercised every week in staging is one that works in production at 02:00.<br>⚠ Require a typed confirmation and have it print exactly what it is about to change. A rollback script that can run unattended is a new and creative way to have an incident. |
| **Claude Code** | Have it write the cap tests: a case engineered to loop, a case engineered to grow context without bound, and an assertion that each stops at the cap, emits its metric and lands in the desk queue. |
| **Chat LLM** | Turn a postmortem transcript into the five-part brief — pain, evidence, the missing enforced control, the fix, the value — and hold that format while the room is still looking for a person to blame.<br>⚠ Check that its 'control' is genuinely enforceable. It will happily propose a clearer prompt, which is a request wearing a control's clothes. |
| **Do not delegate** | Declaring the incident over. Somebody with accountability looks at the state of the world — what was written, what was refunded, what passengers were told — and says so with their name on it. |

**The artefact**

| | |
| --- | --- |
| Produces | **Rehearsed recovery runbook and the containment caps** |
| Good looks like | A runbook with measured times rather than estimated ones, four switches that have each been thrown by the person who will throw them, caps that emit a metric when they trip, and a named list of people who can stop it without asking anyone. |
| Owner | Platform engineer, with the on-call rota |

<details><summary><b>Template · Rollback script, four switches</b></summary>

```bash
#!/usr/bin/env bash
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
  aws ssm put-parameter --name "/$FEATURE/$ENVIRONMENT/$1" --value "$2" \
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
    aws appconfig start-deployment --application-id "$APP_ID" \
      --environment-id "$ENV_ID" --configuration-profile-id "$PROFILE_ID" \
      --deployment-strategy-id "$STRATEGY_ID" --configuration-version "$2" \
      --region "$REGION" --query Id --output text
    ;;
  prompt)
    confirm "pin prompt version ${2:?prompt sha required}"
    put_param prompt-version "$2"
    ;;
  model)
    # Slowest path. Whatever you roll back to, the harness re-runs against it.
    confirm "redeploy runtime pinned to model ${2:?model id required}"
    aws cloudformation deploy --stack-name "$FEATURE-$ENVIRONMENT-runtime" \
      --template-file infra/runtime.yaml --region "$REGION" \
      --parameter-overrides "ModelId=$2" --no-fail-on-empty-changeset
    echo "NOW: re-run the harness against $2 before widening any flag."
    ;;
  *)
    echo "usage: $0 {kill|flag <version>|prompt <sha>|model <model-id>}" >&2
    exit 2
    ;;
esac

echo "Done at $(date -u +%FT%TZ). Put the elapsed time in the runbook."
```

</details>

<details><summary><b>Prompt · Turn the runbook into a rehearsed script</b> — Two weeks before cut-over, while there is still time to find it does not work</summary>

```text
Turn this rollback runbook into a script, then into a rehearsal.

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

RUNBOOK: <paste>
```

</details>

<details><summary><b>Prompt · Design the containment caps and their tests</b> — Before the first live traffic, because a runaway is fast</summary>

```text
Design the containment caps for this agent, and the tests that prove each one.

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

OUR AGENT AND ITS TOOLS: <paste>
```

</details>

<details><summary><b>Prompt · Work out what is actually stateful</b> — Before you write a DR plan, so it covers the right three things</summary>

```text
Given this architecture, tell me what cannot be rebuilt from the repository.

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

ARCHITECTURE: <paste>
```

</details>

**Worked example · SkyWays · eleven minutes, known in advance**

> Before cut-over the on-call engineer threw all four switches with a stopwatch: kill switch 40 seconds, flag to shadow 2 minutes, prompt rollback 3 minutes, model rollback 11 minutes because it redeploys the runtime. Those four numbers went into the runbook beside the date. On day 82, when the $2,000 refund surfaced, the question in the room was never *can we stop it* — it was *which switch*. Refunds went back to gated in two minutes while the tool signature was fixed properly over the next two days, and the rest of the assistant kept running, because the flags were per action. Nobody had to be brave.

**Pitfalls**

- A rollback that has only ever been described. The first attempt happens during an incident, with the wrong person at the keyboard, and the eleven minutes nobody measured turn into forty.
- Rolling back the container and believing you rolled back the behaviour. The prompt version and the model version are separate artefacts, and the deploy you just reverted may not have touched either.
- A kill switch that returns an error. It produces an outage instead of a queue, so the team hesitates to throw it, and the hesitation is the expensive part of every incident it was built for.

**Done when** — Every rollback path has a measured time in the runbook next to the date it was last rehearsed, and a case that hits the loop cap or the cost cap ends in the desk queue with a metric rather than in a retry.

---

## Read next

- [How the whole lifecycle fits together](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Agentic-PDLC)
- [The gateway control, in the simulator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html#/governance/gv-gateway)
- [Every lever on the token bill](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill)

**Other roles:** [Product Manager](Journey-Product-Manager) · [Solution Architect](Journey-Solution-Architect) · [Engineering Lead](Journey-Engineering-Lead) · [QA Lead](Journey-QA-Lead)

- [The manual, interactive](https://akash-coded.github.io/aws-bedrock-agentcore-strands/) · [every template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/) · [every prompt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/) · [frameworks and acronyms](https://akash-coded.github.io/aws-bedrock-agentcore-strands/frameworks/)

