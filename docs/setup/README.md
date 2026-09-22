# Setup

Do these in order. The first one has a waiting step, so start it early.

| | | |
| --- | --- | --- |
| 1️⃣ | **[AWS account setup](aws-account-setup.md)** | Model access is per model, **per region**, and requested manually — approval is not always instant |
| 2️⃣ | **[Cost controls](cost-controls.md)** | Budget alarm and the teardown checklist. **Read before you create anything** |
| 3️⃣ | **[Local environment](local-environment.md)** | Python, virtual environments, per-module requirements, notebook hygiene |
| 🔑 | **[Board sync token](project-token.md)** | Maintainers only: the one secret this repository needs. It turns on two boards — [check, rotate, revoke](#secrets-and-who-needs-them) |
| 📮 | **[Contact relay](../../site/contact-relay/README.md)** | Maintainers only: the AWS backend for the site's contact form, one command to deploy |
| 🧯 | **[Troubleshooting](troubleshooting.md)** | The errors this curriculum actually produces, in the order you meet them |

---

## The three things that catch everyone

**1. Model access is not on by default.** It is granted per model, per region, on request. An empty model
list is a permissions state, not an outage.

**2. Many models need an inference profile ID, not the bare model ID.** The ID carries a geography prefix
(`us.`, `eu.`, …). This is the single most common first-day error.

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```

**3. Two things bill for *existing*, not for use.** OpenSearch Serverless collections and AgentCore
runtimes. They are what people leave running by accident.
[Teardown checklist](cost-controls.md#teardown-checklist).

## No AWS account yet?

Start with [Module 00](../../modules/00-agentic-foundations/),
[Module 01](../../modules/01-llm-and-aws-bridge/) and
[Module 15](../../modules/15-agentic-product-lifecycle/) — none need one. So do
[`rag_by_hand.py`](../../modules/10-rag-opensearch-litellm/src/rag_by_hand.py) and
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py).

## Secrets, and who needs them

**Learners need none of this.** Nothing in the curriculum, the labs or the field guide requires a
secret. This section is for whoever maintains the repository.

There are exactly two, and only the first one is in use today.

### 1 · `PROJECT_TOKEN` — the board sync

| | |
| --- | --- |
| **Lives in** | Repository *Settings → Secrets and variables → Actions* |
| **Powers** | [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) and [Repo Pulse](https://github.com/users/akash-coded/projects/10) |
| **Does not power** | The [Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard), `/leaderboard`, `/progress`, the weekly digest or the PDLC board — all work without it |
| **Kind of token** | A **classic** PAT with the **`project` scope only** |
| **Read by** | [`Pulse & Scoreboard`](../../.github/workflows/pulse.yml), every six hours and after every Arena run |

It cannot be anything else. `GITHUB_TOKEN` has no access to Projects v2, and a fine-grained PAT has no
permission covering **user-owned** projects — these boards belong to a user account. The classic
`project` scope covers every project on the account and cannot be narrowed, which is why the token
carries no other scope and a short expiry.

**Checking it is alive.** A secret listing only proves the secret exists, not that the token behind it
still works. Read the last run:

```bash
gh run view --log $(gh run list --workflow=pulse.yml --limit 1 --json databaseId --jq '.[0].databaseId') | grep -E "tracker board|pulse board|Boards not synced"
```

`tracker board: N rows` and `pulse board: N live items` means it is working.

**When it expires the run does not fail.** The sync warns, the scoreboard still publishes, and only
the two boards stop refreshing — deliberately, so an expired token cannot take the scoreboard down
with it. The failure is therefore quiet, and the signal is a board that has stopped moving while the
Arena is still taking submissions. Check it quarterly.

**Rotating** takes two minutes: generate a replacement (classic, `project` only, 90 days), then store
it at the prompt so it never enters shell history.

```bash
gh secret set PROJECT_TOKEN
```

Never pass a token with `--body`, and never paste one into a file, an issue or a chat. If one is ever
exposed, revoke first and rotate second — revoking is instant and the boards degrade gracefully.

First-time setup is [`project-token.md`](project-token.md). The full operational detail, including
revoking, is in the [Maintainer Runbook](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Maintainer-Runbook#the-board-sync-token).

### 2 · The contact relay's mirror token — not in use

Only needed if you deploy the [contact relay](../../site/contact-relay/README.md), and only for the
optional step that mirrors form messages into a private repository as issues.

Unlike the first one it is a **fine-grained** PAT, scoped to the single `inbox` repository with
*Issues: read and write* and nothing else, and it lives in **AWS Secrets Manager** in your own
account rather than in GitHub. The relay reads it at run time; if it lapses the relay keeps e-mailing
and simply stops mirroring.

The relay is not deployed, so this secret does not exist yet.

---

## Verify you are ready

Run [`00_Bedrock_Onboarding.ipynb`](../../modules/02-bedrock-essentials/notebooks/00_Bedrock_Onboarding.ipynb).
It checks access, invokes a model and prints token usage. Clean run means you are set up.

---

[⬅️ Docs](../) · [▶️ START-HERE](../START-HERE.md) · [🧯 Troubleshooting](troubleshooting.md)
