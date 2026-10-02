# Claude Code cloud sessions for this repository

What a cloud session needs to work on this repository the way the owner's Mac does, and where each piece is
set. Written on 2 October 2026.

## The environment (set once, in the claude.ai/code environment dialog)

Open claude.ai/code, click the cloud icon with the environment's name above the message box, hover over the
environment and click its gear icon.

| Field | Value |
|---|---|
| Network access | **Full** is simplest: the labs and tools work needs vendor documentation. The tighter choice is **Custom** with "Also include default list of common package managers" ticked and the hosts in `allowed-domains.txt` added. |
| Environment variables | The lines in `environment.env`. None is secret, and none may be: anyone who uses the environment can read them. |
| Setup script | The contents of `setup.sh`. It runs as root before Claude starts; when it finishes in under about five minutes the result is cached for later sessions (rebuilt when the script changes, or after about seven days). |

A change to the environment reaches a session that is already running only when its machine is rebuilt. In a
running session, ask Claude to run `bash .claude/cloud/setup.sh` instead.

## At the start of a session

`bash .claude/cloud/session-start.sh` links the skills that `setup.sh` fetched into `.claude/skills/` and
prints what the session has. Run `/reload-skills` after it. The links point outside the repository; keep them
out of commits with these lines in `.gitignore`:

```text
/.claude/skills/*
!/.claude/skills/manual-diagrams/
```

## What a cloud session has, and what it does not

| On the owner's Mac | In a cloud session |
|---|---|
| `~/.claude/CLAUDE.md` and saved preferences | Not available. The round 8 handoff (`handoff/round-8/HANDOFF.md`, section 4) restates them. |
| Personal skills in `~/.claude/skills/` | Not loaded. Those with a public source are fetched at pinned commits by `setup.sh` and linked by `session-start.sh`. Skills enabled on the owner's claude.ai account load by themselves. The owner's own `explainer-diagrams` exists only on the Mac: upload it to claude.ai (Customize in the Desktop app, or the skills settings on claude.ai) to have it everywhere. The Mac's `bedrock-image` needs the AWS CLI's sign-in; here `bedrock-image.py` does its job (see Bedrock). |
| Plugins | Not loaded (neither user plugins nor plugins a repository declares). |
| MCP servers added with `claude mcp add` | Not loaded. Connectors enabled on claude.ai work, once enabled for the session. |
| AWS MCP Server | Add it as a claude.ai connector with the URL `https://aws-mcp.us-east-1.api.aws/mcp` (OAuth with AWS Sign-in; the IAM identity needs the managed policy `AWSMCPSignInOAuthAccessPolicy`). It brings AWS documentation and the AWS skills (`retrieve_skill`). |
| AWS credentials | None, on purpose: the owner's rule is that no secret goes into environment variables or files. AWS SSO cannot run in a cloud session. For Bedrock, see "Bedrock" below. |
| The Browser pane, preview servers | Not available. Use headless Chrome: the check tools in `site/tools/` and `handoff/round-8/tools/` read `$CHROME`. |
| Computer use, Chrome extension, iOS simulator, Apple apps | Not available. |
| GitHub | Through the session's GitHub proxy; no token needed. Pushes to `main` deploy the public site, so ask the owner first. |

## Bedrock: any model, and images (every call is billed to the owner's AWS account)

The owner has a long-term Amazon Bedrock API key with `AmazonBedrockLimitedAccess` and, when the owner adds it,
`AmazonBedrockFullAccess` (every Bedrock action):
any model on `bedrock-runtime` and `bedrock-mantle` (InvokeModel, Converse, the OpenAI-compatible and Messages
APIs), guardrails, web search, batch, evaluation and fine-tuning jobs, provisioned throughput, and the
Marketplace step that switches a third-party model on at its first call. It does not work with other AWS
services, and Bedrock refuses it for Agents for Bedrock, Data Automation and two-way streaming.

The owner puts the key in the environment, in one of two ways. Claude never types, prints or repeats it.

- **Environment variable** (the owner's choice on 2 October 2026): `AWS_BEARER_TOKEN_BEDROCK` in the
  environment's variables. Every session can read it. boto3 uses it by itself; curl and other HTTP clients
  send it as `Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK`; OpenAI-compatible SDKs take it as their API
  key with the base URL `https://bedrock-runtime.<region>.amazonaws.com/openai/v1`. A session that is already
  running sees a new variable only after its machine restarts.
- **API credential, type Bearer** (sessions never see the key; Pro and Max plans): in the environment's
  settings, API credentials, Add credential. Allowed websites: one wildcard per Region in use, which covers
  every Bedrock endpoint there, plus the OpenAI-compatible hosts: `*.us-east-1.amazonaws.com`,
  `*.us-west-2.amazonaws.com`, `*.ap-south-1.amazonaws.com`, `*.eu-west-1.amazonaws.com`, `*.api.aws`.
  Custom header `Authorization`, prefix `Bearer`, value the key. Plain HTTP and the helpers below need
  nothing more; SDKs also need the variable above. Avoid `*.amazonaws.com` for a Bearer key: the key would
  then go to every AWS host, and unauthenticated downloads from AWS hosts inside a session can fail.
- **API credential, type AWS SigV4** (every AWS service, not only Bedrock): an IAM user's access key pair,
  allowed websites `*.amazonaws.com`. The proxy strips the request's signature and signs it again with the
  stored key, so the AWS CLI and SDKs work with placeholder credentials: the environment's variables set
  `AWS_ACCESS_KEY_ID=placeholder`, `AWS_SECRET_ACCESS_KEY=placeholder` and `AWS_REGION`, and do not set
  `AWS_BEARER_TOKEN_BEDROCK`. The Bearer credential for the Bedrock key then keeps only `*.api.aws`, so the
  two never cover the same host. An HTTP 502 whose reason starts `injection failed` means the proxy could
  not sign that hostname (for example `ec2.amazonaws.com`, which has no Region in it).

The helpers here work either way:

- `python3 .claude/cloud/bedrock-ask.py --check [--region us-east-1]`: free; says whether the key arrives.
- `python3 .claude/cloud/bedrock-ask.py --model <model or inference profile id> "question" [--region ...]
  [--max-tokens 1024]`: one Converse call. Always set the token limit.
- `python3 .claude/cloud/bedrock-image.py --check`, then `--prompt "..." --out picture.png
  [--model core|ultra|sd35]`: one image with a Stability model in us-west-2.

Before any billed call, say which model, how many calls and why, and wait for the owner's yes.

If the owner ever wants a key that can only make images, give the key's IAM user this inline policy instead
of `AmazonBedrockLimitedAccess`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "MakeImagesWithThreeStabilityModels",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-west-2::foundation-model/stability.stable-image-core-v1:1",
        "arn:aws:bedrock:us-west-2::foundation-model/stability.stable-image-ultra-v1:1",
        "arn:aws:bedrock:us-west-2::foundation-model/stability.sd3-5-large-v1:0"
      ]
    },
    {
      "Sid": "UseThisKeyWithBedrock",
      "Effect": "Allow",
      "Action": "bedrock:CallWithBearerToken",
      "Resource": "*"
    },
    {
      "Sid": "FirstCallActivatesTheModel",
      "Effect": "Allow",
      "Action": ["aws-marketplace:Subscribe", "aws-marketplace:ViewSubscriptions"],
      "Resource": "*",
      "Condition": { "StringEquals": { "aws:CalledViaLast": "bedrock.amazonaws.com" } }
    }
  ]
}
```

To stop: remove the variable or the credential from the environment, and delete the key in the Bedrock
console.

## Files here

- `setup.sh`: the environment's setup script; also safe to run inside a session. Linux only.
- `bedrock-ask.py`: asks any Bedrock model one question (see Bedrock above).
- `bedrock-image.py`: makes one image with a Stability model (see Bedrock above).
- `environment.env`: the environment variables, with a comment on each.
- `allowed-domains.txt`: extra hosts for a Custom network (Chrome for Testing's version list, the Chrome
  package host, Playwright's browser hosts, the published site).
- `session-start.sh`: links the fetched skills and reports what the session has. Does nothing outside a
  cloud session.
