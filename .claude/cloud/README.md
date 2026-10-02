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
| Personal skills in `~/.claude/skills/` | Not loaded. Those with a public source are fetched at pinned commits by `setup.sh` and linked by `session-start.sh`. Skills enabled on the owner's claude.ai account load by themselves. The owner's own `explainer-diagrams` exists only on the Mac: upload it to claude.ai (Customize in the Desktop app, or the skills settings on claude.ai) to have it everywhere. The Mac's `bedrock-image` needs the AWS CLI's sign-in; here `bedrock-image.py` does its job (see Images). |
| Plugins | Not loaded (neither user plugins nor plugins a repository declares). |
| MCP servers added with `claude mcp add` | Not loaded. Connectors enabled on claude.ai work, once enabled for the session. |
| AWS MCP Server | Add it as a claude.ai connector with the URL `https://aws-mcp.us-east-1.api.aws/mcp` (OAuth with AWS Sign-in; the IAM identity needs the managed policy `AWSMCPSignInOAuthAccessPolicy`). It brings AWS documentation and the AWS skills (`retrieve_skill`). |
| AWS credentials | None, on purpose: the owner's rule is that no secret goes into environment variables or files. AWS SSO cannot run in a cloud session. For images, see "Images" below: a key the session never sees. |
| The Browser pane, preview servers | Not available. Use headless Chrome: the check tools in `site/tools/` and `handoff/round-8/tools/` read `$CHROME`. |
| Computer use, Chrome extension, iOS simulator, Apple apps | Not available. |
| GitHub | Through the session's GitHub proxy; no token needed. Pushes to `main` deploy the public site, so ask the owner first. |

## Images (optional; each image is billed to the owner's AWS account)

On the owner's Mac the `bedrock-image` skill uses the AWS CLI and the owner's own sign-in. A cloud session
has no AWS credentials, so it uses `bedrock-image.py` here instead, with a key the session never sees: the
environment holds the key as an API credential, and Anthropic's proxy adds it to each request to Bedrock
after the request leaves the session's machine. The owner sets it up once; Claude must not do these steps
and must never be shown the key.

1. In the AWS console, Region US West (Oregon): Amazon Bedrock, API keys, the Long-term API keys tab,
   Generate long-term API keys. Choose an expiry (30 days is enough) and Generate. Copy the key; it is
   shown once. Paste it nowhere except step 3.
2. Recommended, before the first image: in IAM, Users, open the user that step 1 created (its name starts
   with `BedrockAPIKey`). On Permissions, remove `AmazonBedrockLimitedAccess` and add an inline policy with
   the JSON below. The key can then only make images with these three models; the Marketplace lines let the
   first call activate a model in the account, and only through Bedrock.
3. At claude.ai/code, open this environment's settings, find API credentials and choose Add credential.
   Name: `Amazon Bedrock images`. Credential type: `Bearer`. Allowed websites:
   `bedrock-runtime.us-west-2.amazonaws.com`. Custom headers: name `Authorization`, prefix `Bearer`, value:
   the key. Choose Connect. (API credentials exist on Pro and Max plans only.)
4. In a session: `python3 .claude/cloud/bedrock-image.py --check` shows whether the key arrives, and makes
   no image. Then, after the owner's yes for each batch:
   `python3 .claude/cloud/bedrock-image.py --prompt "..." --out picture.png [--model core|ultra|sd35]`.

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

To stop it: delete the API credential in the environment's settings, and delete the key (or the user) in
AWS. Prices: https://aws.amazon.com/bedrock/pricing/ (Stability AI).

## Files here

- `setup.sh`: the environment's setup script; also safe to run inside a session. Linux only.
- `bedrock-image.py`: makes one image through the environment's API credential (see Images above).
- `environment.env`: the environment variables, with a comment on each.
- `allowed-domains.txt`: extra hosts for a Custom network (Chrome for Testing's version list, the Chrome
  package host, Playwright's browser hosts, the published site).
- `session-start.sh`: links the fetched skills and reports what the session has. Does nothing outside a
  cloud session.
