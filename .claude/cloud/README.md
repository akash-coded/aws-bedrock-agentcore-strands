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
| Personal skills in `~/.claude/skills/` | Not loaded. Those with a public source are fetched at pinned commits by `setup.sh` and linked by `session-start.sh`. Skills enabled on the owner's claude.ai account load by themselves. The owner's own `explainer-diagrams` and `bedrock-image` exist only on the Mac: upload them to claude.ai (Customize in the Desktop app, or the skills settings on claude.ai) to have them everywhere. |
| Plugins | Not loaded (neither user plugins nor plugins a repository declares). |
| MCP servers added with `claude mcp add` | Not loaded. Connectors enabled on claude.ai work, once enabled for the session. |
| AWS MCP Server | Add it as a claude.ai connector with the URL `https://aws-mcp.us-east-1.api.aws/mcp` (OAuth with AWS Sign-in; the IAM identity needs the managed policy `AWSMCPSignInOAuthAccessPolicy`). It brings AWS documentation and the AWS skills (`retrieve_skill`). |
| AWS credentials | None, on purpose: the owner's rule is that no secret goes into environment variables or files. AWS SSO cannot run in a cloud session. |
| The Browser pane, preview servers | Not available. Use headless Chrome: the check tools in `site/tools/` and `handoff/round-8/tools/` read `$CHROME`. |
| Computer use, Chrome extension, iOS simulator, Apple apps | Not available. |
| GitHub | Through the session's GitHub proxy; no token needed. Pushes to `main` deploy the public site, so ask the owner first. |

## Files here

- `setup.sh`: the environment's setup script; also safe to run inside a session. Linux only.
- `environment.env`: the environment variables, with a comment on each.
- `allowed-domains.txt`: extra hosts for a Custom network (Chrome for Testing's version list, the Chrome
  package host, Playwright's browser hosts, the published site).
- `session-start.sh`: links the fetched skills and reports what the session has. Does nothing outside a
  cloud session.
