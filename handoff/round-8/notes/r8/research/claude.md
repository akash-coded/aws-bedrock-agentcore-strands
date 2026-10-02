# Claude: every way a professional can use it today

Fact sheet for the manual. Checked on 2 October 2026.

## How to read this sheet

- Every statement about Claude comes from an official page opened on 2 October 2026 (Anthropic's platform docs, Claude Code docs, help centre, pricing page, release notes). The source address follows each entry. Where a page shows its own date, that date is given; otherwise the date is the check date.
- Status words are the vendor's own: GA (generally available), beta, research preview, experimental. They are repeated here because they change what you can promise a team.
- "Nearest equivalent" lines are from the researcher's prior knowledge and were NOT checked in this session. Another researcher covers those products. Blank means not known for certain.
- Section 6 lists where official pages disagree. Section 7 lists what could not be verified.

## Six things that changed and will catch people out

1. Chat and Cowork are merging into one product. Since 16 September 2026 the agent features (long tasks in the cloud, files, scheduled work, browser and computer access) are rolling into ordinary conversations, starting with Pro and Max.
2. Claude Code starts in auto mode. From v2.1.283 a second model (a classifier) approves most actions in place of the person, in the terminal and VS Code, on every plan and provider.
3. Custom slash commands are now skills. The old commands folder still works but skills are the format to teach.
4. Claude Code reads AGENTS.md by itself (from v2.1.277) when a repository has no CLAUDE.md.
5. The Console Workbench is retired. Its replacement, the playground, has no saved prompts, no prompt versions and no evaluation tab.
6. The model names are new. The current line-up is Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 4.5. Extended thinking with a token budget is gone on current models; thinking is adaptive and steered by an effort setting.

---

## 1. Claude in chat (web, desktop and mobile apps)

### 1.1 One Claude: chat and Cowork merged

- What it is: Cowork was the separate agent mode for knowledge work (multi-step tasks, files, browser, sub-agents). It is being folded into normal chat, so the person describes the outcome and Claude picks the tools. Tasks run in a cloud environment on Anthropic's servers and reach the person's machine through the desktop app only when local files, the browser or computer use are needed.
- Use it for: a product manager asks for a competitor brief with a spreadsheet and a deck and leaves it running; a sponsor gets a weekly status report built from Slack and Drive; a QA lead has a test report compiled from a results folder.
- Limits and traps: rolling out gradually, Pro and Max first; Enterprise gets at least 30 days' notice. In the merged experience the GitHub integration, conversation branching and Dispatch for new users are missing, and incognito chats fall back to the old experience. Cloud task execution is labelled beta. Multi-step tasks use far more of the plan allowance than a chat.
- Nearest equivalent: ChatGPT agent mode; Gemini agent features (not checked).
- Sources: https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude (updated over 2 weeks ago); https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork (updated 1 Oct 2026); https://support.claude.com/en/articles/12138966-release-notes (entry 16 Sep 2026).

### 1.2 Projects

- What it is: a workspace with its own chats, uploaded knowledge and project instructions. On paid plans, when the knowledge nears the context limit, Claude switches to retrieval (RAG) and can hold about ten times more. Each project has its own memory, kept apart from other projects.
- Use it for: a product manager keeps the PRD, research notes and glossary in one project so every chat starts with them; an architect keeps the decision records and standards; a team shares a "how we write specs" project.
- What is shared with a team: Team and Enterprise only. A project is private (invited people) or public to the organisation. Roles are can view, can edit and owner. Collaborators see the knowledge and the instructions. Chats stay private unless a chat is shared by its own link, and a shared chat is a snapshot.
- Limits and traps: Free accounts get five projects. Project instructions are advice to the model, not enforcement. Permission changes can take up to five minutes. Group sharing on Enterprise is beta. This "Projects" is not the same thing as Claude Code projects (2.6).
- Nearest equivalent: ChatGPT Projects and custom GPTs; Gemini Gems and NotebookLM (not checked).
- Sources: https://support.claude.com/en/articles/9517075-what-are-projects ; https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing ; https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects ; https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context (checked 2 Oct 2026).

### 1.3 Artifacts, and the Slides, Design and Docs templates

- What it is: a self-contained thing Claude makes beside the chat: a document, an HTML page, a React component, a diagram, a small tool. Since September 2026 three templates (Slides, Design, Docs) open in their own editors and export to PowerPoint, PDF or Word. An artifact can call Claude itself, call the viewer's connectors, and store up to 20 MB of text data.
- Use it for: a product manager builds a clickable prototype or a prioritisation board; an architect draws a system diagram; a sponsor gets a live dashboard that reads Jira through each viewer's own connector.
- Limits and traps: needs code execution and file creation switched on. A page is static, with no backend. When an artifact calls Claude or a connector, the usage and the permissions are the viewer's, not the author's. On Enterprise the templates are off until an owner turns each on. Public sharing is off by default on Team and Enterprise.
- Nearest equivalent: ChatGPT Canvas; Gemini Canvas (not checked).
- Sources: https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them (updated over a week ago); https://code.claude.com/docs/en/artifacts (checked 2 Oct 2026).

### 1.4 Skills

- What it is: a folder with a SKILL.md file (name, description, instructions) plus optional scripts and reference files. Claude sees only the name and description until a task matches, then loads the rest. Anthropic ships skills for Excel, Word, PowerPoint and PDF.
- Use it for: packaging "how we write a user story", "our test-plan template", "our release checklist" once, so every person and every agent follows the same steps. A platform engineer publishes them to the organisation.
- Limits and traps: needs code execution enabled. A skill can run code and install packages, so treat a third-party skill like installing software. Owners on Team and Enterprise can provision skills to everyone; Enterprise can scan uploaded skills. Skills enabled in the account sync one way into Claude Code (v2.1.273 or later) roughly every ten minutes. See section 6 for a disagreement between the platform docs and the help centre on sharing and syncing.
- Nearest equivalent: custom GPT instructions and actions; Gemini Gems (not checked, and neither loads on demand in the same way).
- Sources: https://support.claude.com/en/articles/12512176-what-are-skills ; https://support.claude.com/en/articles/12512180-use-skills-in-claude (both updated over a week ago); https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (checked 2 Oct 2026).

### 1.5 Connectors and MCP in the apps

- What it is: a connector gives Claude access to another system through the Model Context Protocol (MCP). There are web connectors from the directory (Slack, Drive, Linear and others), desktop extensions that run locally in the desktop app, and custom connectors that point at any remote MCP server. Some connectors render an interactive panel in the chat.
- Use it for: reading tickets and writing them back; pulling a design from Figma; letting Research read internal documents. A platform engineer exposes an internal API as a remote MCP server and adds it for the organisation.
- Limits and traps: a custom connector is called from Anthropic's cloud, so the server must be reachable from the public internet (or the firewall must allow Anthropic's address ranges). A server behind a VPN will not connect. Free accounts get one custom connector. On Team and Enterprise an owner enables a connector first, each member then signs in, and the owner can limit read, write and delete actions for the whole organisation. Connectors respect the user's own permissions in the source system. Unverified servers are a prompt injection risk; the help page advises switching off write tools while using Research.
- Nearest equivalent: ChatGPT connectors and apps; Gemini extensions and Workspace integration (not checked).
- Sources: https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities (updated 2 Oct 2026); https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp (updated 2 Oct 2026).

### 1.6 Plugins in the apps

- What it is: one installable bundle of skills, commands, connectors and agents, added from Customize > Plugins. It is saved to the account, so it also appears in Cowork and Claude Code.
- Use it for: giving a whole role its kit in one step, for example a "QA" plugin with test-plan skills and the test-management connector.
- Limits and traps: chat loads skills, commands and connectors only; agents and hooks run only in Cowork and Claude Code. Plugins added from a marketplace URL or uploaded as a file are not reviewed by Anthropic. Owners on Team and Enterprise choose the sources and can make a plugin installed by default or required. Plugins installed from the Claude Code command line stay on that machine.
- Source: https://claude.com/docs/plugins/overview (checked 2 Oct 2026).

### 1.7 Web search and Research

- What it is: web search lets Claude look things up and cite the pages; web fetch reads a page you name. Research is a longer mode in which Claude runs many searches that build on each other, across the web and connected sources, and returns a cited report in minutes.
- Use it for: market and vendor scans, standards and regulation checks, "what changed in this library" questions, a first draft of a build-versus-buy paper.
- Limits and traps: web search works on free and paid accounts; on Team and Enterprise an owner must enable it. Research is paid plans only and needs web search on. Both draw on the usage allowance, Research much faster. Citations make checking possible; they do not make the claim true.
- Nearest equivalent: ChatGPT search and deep research; Gemini Deep Research (not checked).
- Sources: https://support.claude.com/en/articles/10684626-enable-and-use-web-search (updated this week); https://support.claude.com/en/articles/11088861-use-research-on-claude (updated 2 Jun 2026).

### 1.8 Memory, chat search and incognito

- What it is: Claude saves short topics about you and your work as you chat, and you can tell it to remember something. You can read, edit and delete each topic in Settings. Chat search lets Claude look through past conversations. Incognito chats are kept out of history and memory.
- Use it for: not re-explaining your role, stack and preferences. For a team, project memory keeps one product's context apart from another's.
- Limits and traps: on by default for Free, Pro and Max; on Team and Enterprise it is off until an owner allows it and each member turns it on. If an owner switches memory off for the organisation, every member's memories are deleted at once. Chat search is paid plans only. Incognito chats on Team and Enterprise are still retained for a period and appear in owner data exports. Memory is the model's notes, not a record you can rely on for decisions; put decisions in a project file.
- Nearest equivalent: ChatGPT memory and temporary chat; Gemini saved info (not checked).
- Source: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context (updated 1 Oct 2026).

### 1.9 File creation and code execution

- What it is: Claude has a private sandbox where it writes and runs code to produce real files: Excel, PowerPoint, Word, PDF, charts.
- Use it for: turning a CSV of defects into a workbook with pivot tables; a sponsor deck from a status document; data checks during analysis.
- Limits and traps: available on all plans. 30 MB per file. Network access from the sandbox is on by default for Free, Pro and Max and off by default for Team and Enterprise, where an owner chooses between none, package managers only, an allow list, or everything except blocked domains. The help page itself warns that a hidden instruction in a file or page could make Claude run untrusted code or send data out.
- Nearest equivalent: ChatGPT data analysis (code interpreter); Gemini code execution (not checked).
- Source: https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude (updated 6 Aug 2026).

### 1.10 Scheduled and recurring tasks

- What it is: a saved prompt that Claude runs hourly, daily, weekly, on weekdays, or on demand. It runs in the cloud, so the computer can be off. It can use connectors, skills and plugins.
- Use it for: a morning digest of open risks from Jira and Slack; a weekly report; a recurring competitor watch.
- Limits and traps: paid plans. A cloud task cannot be tied to a folder on your computer; a task that needs local files runs locally and then needs the machine awake. Each task sets its own approval mode, so an unattended task acts with whatever you pre-approved.
- Nearest equivalent: ChatGPT scheduled tasks; Gemini scheduled actions (not checked).
- Source: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork (updated this week).

### 1.11 Voice

- What it is: spoken two-way conversation, on mobile, desktop and web. Dictation (speech to text) is a separate, simpler feature.
- Use it for: talking through a design while walking; dictating a long, detailed prompt.
- Limits and traps: beta. All plans. Counts toward normal usage. Can use web search and a few connectors (Gmail, Calendar, Docs, Slack); Free allows one. The Fable model is not available in voice.
- Nearest equivalent: ChatGPT voice mode; Gemini Live (not checked).
- Source: https://support.claude.com/en/articles/11101966-use-voice-mode (updated over 2 weeks ago).

### 1.12 Claude Tag (Claude in Slack for a team)

- What it is: @Claude in Slack acting under the organisation's identity, with admin-set tool access, memory per channel and its own follow-ups. It is replacing the per-user Claude in Slack for Team and Enterprise: the help centre dates the move to 3 August 2026, while the Claude Code docs say each organisation gets its own cutover date. Coding requests become Claude Code cloud sessions.
- Limits and traps: beta, Team and Enterprise only. Claude may follow instructions found in other messages in the thread, so use it only in trusted channels. Pro and Max keep the older per-user integration, which is GitHub only and one pull request per session.
- Sources: https://support.claude.com/en/articles/15594475-what-is-claude-tag ; https://code.claude.com/docs/en/slack (checked 2 Oct 2026).

### 1.13 Plan differences that matter for a team

| Plan | Price shown | What matters |
|---|---|---|
| Free | 0 | Chat, artifacts, connectors, memory, five projects. No Claude Code, no Research. |
| Pro | 20 USD a month (17 if annual) | Claude Code, Cowork, Research. Fable draws on usage credits. |
| Max | from 100 USD a month | 5 times or 20 times Pro usage. |
| Team | standard seat 25 (20 annual), premium seat 125 (100 annual), 2 to 150 seats | Standard is 1.25 times Pro usage per session, premium 6.25 times. SSO, domain capture, role permissions, central billing, spend controls, shared projects, org skills and plugins. |
| Enterprise | 20 USD per seat a month plus all usage at API rates, annual | No fixed allowance. SCIM, audit logs, Compliance API, custom retention, customer-managed keys, HIPAA option, model entitlements. Minimum 20 seats self-serve, 50 through sales. |

- Traps: on Team and Enterprise several features need an owner to switch them on (web search, memory, connectors, Remote Control, Channels). Computer use and Dispatch are Pro and Max only. Managed Code Review is Team and Enterprise only. Enterprise bills every token, so agent-heavy work needs spend limits.
- Sources: https://claude.com/pricing ; https://support.claude.com/en/articles/9266767-what-is-the-team-plan ; https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan (updated 1 Sep 2026); https://code.claude.com/docs/en/feature-availability (checked 2 Oct 2026).

---

## 2. Claude Code

### 2.1 What it is and where it runs

Claude Code is a coding agent that reads a codebase, edits files, runs commands and uses git. The same engine runs on every surface, and repository settings (CLAUDE.md, settings, MCP servers) carry across the local ones. Latest version at the check: 2.1.287, released 1 October 2026.

| Surface | Where the code runs | Good for | Notes |
|---|---|---|---|
| Terminal (CLI) | your machine | full feature set, scripting, servers | only surface with scripting and the Agent SDK |
| VS Code extension | your machine | inline diffs, plan review, checkpoints | VS Code 1.94 or later; also installs in Cursor; a subset of commands |
| JetBrains plugin | your machine | diff viewer, selection sharing | marked Beta; it runs the CLI, which you install separately |
| Desktop app, Code tab | your machine, the cloud, or SSH | parallel sessions, visual diff, app preview, PR monitoring | macOS and Windows; Linux is beta; paid plan needed |
| Web (claude.ai/code) | Anthropic cloud VM | long tasks, repos you have not cloned | GitHub needed to clone and open PRs |
| Mobile app, Code tab | client only | start, watch and steer | no code runs on the phone |

- Accounts: a Claude subscription or a Console (API) account for most surfaces; the CLI and IDE extensions also work through Amazon Bedrock, Google Cloud's Agent Platform (the docs' name for Vertex AI) and Microsoft Foundry.
- Sources: https://code.claude.com/docs/en/overview ; https://code.claude.com/docs/en/platforms ; https://code.claude.com/docs/en/vs-code ; https://code.claude.com/docs/en/jetbrains ; https://code.claude.com/docs/en/desktop ; https://code.claude.com/docs/en/changelog (checked 2 Oct 2026).

### 2.2 Cloud sessions, moving work between surfaces

- What it is: a session on an isolated VM that keeps running after you close the laptop. Start it from the browser, the phone, the desktop app, or `claude --cloud "task"`. Pull it back with `claude --teleport`. A cloud environment sets network access, variables and a setup script.
- Use it for: an engineer hands off a migration and reviews the pull request later; a platform engineer runs several fixes in parallel; plan locally in plan mode, commit the plan, execute in the cloud.
- Limits and traps: Pro, Max, Team, and Enterprise seats that include Claude Code. Not available with API keys or third-party providers, nor with Zero Data Retention. The VM clones the GitHub remote, so unpushed commits are not there. Terminal to cloud is one way from the CLI. Idle sessions lose their VM and background work. Default network access is a trusted allow list. Usage shares the same limits as everything else. Auto-fix can answer review comments under your GitHub name, which can trigger comment-driven automation such as Terraform runs. An organisation IP allow list breaks Anthropic-hosted sessions. Team and Enterprise can run sessions on their own infrastructure (self-hosted environments, public beta).
- Nearest equivalent: Codex cloud tasks; Google Jules (not checked).
- Source: https://code.claude.com/docs/en/claude-code-on-the-web (checked 2 Oct 2026).

### 2.3 Claude Code projects

- What it is: one long conversation in which Claude starts and tracks many parallel cloud sessions (threads) for a body of work, with shared instructions, files and memory.
- Limits and traps: public beta on Pro and Max, rolling out gradually; not on Team or Enterprise. A project belongs to one user and cannot be shared. Up to 200 new threads a day. Uses the plan allowance quickly. Uncommitted work in a paused sandbox can be lost.
- Source: https://code.claude.com/docs/en/claude-projects (checked 2 Oct 2026).

### 2.4 Remote Control, Dispatch, Channels, mobile

- Remote Control: drive a session that is running on your own machine from claude.ai/code or the phone. The machine makes outbound connections only; the transcript is stored on Anthropic's servers while connected. Paid plans, off until an owner enables it on Team and Enterprise, not available with API keys, gateways or third-party providers. The local process must stay alive. An optional Trusted Devices check (beta) ties access to an enrolled device.
- Dispatch: message a task from the phone and the desktop app runs it. Pro and Max only; the help centre says it is a limited beta closed to new users.
- Channels: push events from chat apps or your own webhook into a running CLI session.
- Mobile: a client for cloud sessions and Remote Control; cannot select bypass mode.
- Sources: https://code.claude.com/docs/en/remote-control ; https://code.claude.com/docs/en/mobile ; https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork (checked 2 Oct 2026).

### 2.5 Building blocks

**CLAUDE.md, AGENTS.md, rules and auto memory**
- What: CLAUDE.md is a plain file of instructions loaded at the start of every session. Scopes: organisation (managed), user, project (in git), local (not in git). Files up the directory tree are all added together; files in subfolders load when Claude reads there. `.claude/rules/` holds topic files that can be limited to file paths. Auto memory is notes Claude writes for itself per repository, on the local machine. If a repository has AGENTS.md and no CLAUDE.md, Claude reads AGENTS.md.
- Use: the team's build commands, conventions and "never do X" list, reviewed like code. An architect owns it.
- Traps: it is context, not enforcement; it arrives as a message after the system prompt. Aim under 200 lines per file. Imports with `@path` do not save context. Only the first 200 lines or 25 KB of the memory index load. Adding a CLAUDE.local.md stops AGENTS.md loading unless you change the setting. To force a rule, use a hook or a permission rule. `/doctor prompt-audit` finds stale or conflicting instructions.
- Equivalent: AGENTS.md in Codex; GEMINI.md in Gemini CLI (not checked).
- Source: https://code.claude.com/docs/en/memory

**Skills and commands**
- What: same SKILL.md format as 1.4, stored in `~/.claude/skills/` (personal), `.claude/skills/` (project), a plugin, or managed settings. Invoked by Claude when the description matches, or by you as `/name`. Old `.claude/commands/*.md` files still work but are the deprecated form. Built-in commands (`/init`, `/compact`, `/context`, `/model`, `/mcp`, `/rewind`, `/doctor`, `/code-review` and others) sit beside bundled skills. Frontmatter can restrict tools, set the model, run the skill in a separate subagent, or stop Claude calling it on its own.
- Use: `/write-spec`, `/review-pr`, `/deploy-staging` as shared, versioned procedures.
- Traps: every skill description costs context in every session (about 1 percent of the window is budgeted; long descriptions are cut). A loaded skill stays in context. Skills that must only run when a person asks need `disable-model-invocation`. Shell snippets inside a skill run before Claude sees it.
- Source: https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/commands

**Subagents**
- What: a helper with its own context window, system prompt and tool list, defined as a markdown file in `.claude/agents/`. It returns a summary. Built in: Explore (read only), Plan, general-purpose. A fork is a subagent that inherits the whole conversation (`/subtask`).
- Use: keep search and log noise out of the main session; a read-only reviewer; a test runner that reports only failures. QA and architecture roles can each be a subagent file in the repo.
- Traps: a subagent does not see the conversation, so the brief is everything. In interactive sessions subagents run in the background by default. Default caps are 20 at once and three layers of nesting. Their edits are usually not undone by rewind. Each one multiplies token use.
- Source: https://code.claude.com/docs/en/sub-agents

**Hooks**
- What: your own commands that Claude Code runs at fixed points (before a tool call, after an edit, at session start, when Claude stops, and about thirty other events). Types: shell command, HTTP call, MCP tool, a one-shot model check, or an agent check (experimental). A PreToolUse hook can block an action.
- Use: the place for rules that must always hold: format after edit, block edits to protected files, refuse `git push` to main, log every command for audit. A platform engineer ships them in managed settings.
- Traps: hooks run with your privileges. A deny from a PreToolUse hook holds even in bypass mode, but exit code 0 does not approve anything. Hooks run in parallel. Stop hooks fire on every reply, not only when the task is done.
- Source: https://code.claude.com/docs/en/hooks-guide

**Plugins, marketplaces and mods**
- What: a plugin is a folder of skills, agents, hooks and MCP servers installed as one unit. A marketplace is a git repository with a catalogue file, not a hosted store. Scopes: user, project (committed, so the team gets it), local. A mod is a plugin with JavaScript hooks that can draw panels in the interface (added in v2.1.287).
- Use: one team kit, versioned, installed with one command; organisations can allow or block marketplaces and force-install plugins.
- Traps: a plugin runs code as you. Every enabled plugin adds descriptions to every session. Cloud sessions do not load plugins from your local settings. `claude plugin eval` tests a plugin against cases and a baseline.
- Source: https://code.claude.com/docs/en/plugins/overview ; https://code.claude.com/docs/en/whats-new/index

**MCP servers**
- What: Claude Code connects to MCP servers over HTTP, stdio, WebSocket or the older SSE (deprecated). Scopes: local, project (`.mcp.json` in git), user. Connectors from your claude.ai account appear too. Tool search defers loading tool definitions until needed. Claude Code can itself act as a server (`claude mcp serve`).
- Traps: project servers need approval once, but a `claude -p` run shows no trust dialog. Large tool results are cut at 25,000 tokens by default. Servers that fetch outside content are an injection route. Organisations can allow-list or deny servers.
- Source: https://code.claude.com/docs/en/mcp

**Permission modes, plan mode and auto mode**
- What: Manual (config value `default`) asks before edits and commands. `acceptEdits` allows edits and simple file commands. `plan` lets Claude research and propose, with edits blocked until you approve. `auto` lets a classifier model review actions instead of you. `dontAsk` denies anything not pre-approved. `bypassPermissions` skips checks. Allow, ask and deny rules sit on top; deny rules hold in every mode.
- Use: plan mode for design review before code; `dontAsk` with an exact allow list for CI; bypass only inside a container or VM.
- Traps: auto is now the starting mode in the terminal and VS Code (v2.1.283 and later), on all plans; an owner can switch it off with `disableAutoMode`. The docs say auto mode cuts prompts but does not guarantee safety. Auto needs recent models (older ones such as Sonnet 4.5 and Haiku are not supported). After 3 blocks in a row or 20 in a session it falls back to asking. Setting `auto` in a project settings file has no effect.
- Source: https://code.claude.com/docs/en/permission-modes

**Sandbox, checkpoints, worktrees**
- Sandbox: the operating system limits which files and hosts shell commands can reach. macOS, Linux and WSL2; not native Windows. It covers shell commands only, not file tools, MCP servers or hooks. Source: https://code.claude.com/docs/en/sandboxing
- Checkpoints: each prompt snapshots edited files; `/rewind` restores code, conversation or both. Changes made by shell commands, by most subagents and by other sessions are not tracked. It is not version control. Source: https://code.claude.com/docs/en/checkpointing
- Worktrees: `claude --worktree name` gives a session its own checkout and branch under `.claude/worktrees/`, so parallel sessions do not collide. Subagents can each get one (`isolation: worktree`). A worktree is a fresh checkout, so dependencies and ignored files such as `.env` are missing unless listed in `.worktreeinclude`. Source: https://code.claude.com/docs/en/worktrees

**Running several agents**
- Background sessions and agent view (`claude agents`, `--bg`, `/background`): one screen for many local sessions, each moved into its own worktree before it edits. Research preview.
- Agent teams: a lead session with teammates that message each other and share a task list. Experimental and off by default; no worktree isolation; no resume of teammates.
- Dynamic workflows: Claude writes a JavaScript script that runs many subagents and cross-checks results; the bundled one is `/deep-research`. All paid plans and providers. Defaults: 16 agents at once, 1,000 per run. The `ultracode` keyword or setting triggers it. Cost rises fast.
- Cross-session messaging lets sessions pass findings to each other.
- Sources: https://code.claude.com/docs/en/agents ; https://code.claude.com/docs/en/agent-view ; https://code.claude.com/docs/en/agent-teams ; https://code.claude.com/docs/en/workflows

**Scheduled work**

| | Routines | Desktop scheduled tasks | /loop |
|---|---|---|---|
| Runs | cloud | your machine | your open session |
| Machine on | no | yes | yes |
| Shortest interval | 1 hour | 1 minute | 1 minute |
| Local files | no (fresh clone) | yes | yes |
| Prompts for permission | never | per task | as the session |

- Routines also start from an HTTP call or a GitHub event (pull request, release). Research preview. They belong to one user, act as that user on GitHub and in connectors, include every connector by default, and push to `claude/` branches. A green run status means the session ran, not that the task succeeded. `/loop` tasks expire after seven days.
- Use: nightly triage, docs drift checks, deploy verification, alert investigation that opens a draft pull request.
- Sources: https://code.claude.com/docs/en/routines ; https://code.claude.com/docs/en/scheduled-tasks ; https://code.claude.com/docs/en/desktop-scheduled-tasks

**Headless use and CI**
- What: `claude -p "prompt"` runs once and exits. Output as text, JSON (with cost and session id) or a JSON stream; `--json-schema` returns validated structured output. `--bare` skips hooks, skills, plugins, MCP servers, memory and CLAUDE.md so every machine behaves the same, and is described as the future default for `-p`.
- GitHub Actions: `anthropics/claude-code-action@v1` answers `@claude` in issues and pull requests or runs a prompt on any event. Auth by API key, subscription token, or keyless federation; Bedrock, Google Cloud and Foundry are supported. GitLab CI/CD has its own integration.
- Traps: without `--bare`, a `-p` run executes the repository's hooks and connects its MCP servers with no trust prompt. Pass the permission mode you want, since the default can be auto. Commits made with the default GITHUB_TOKEN do not trigger other workflows. Cap turns and set timeouts.
- Equivalent: `codex exec`; Gemini CLI non-interactive mode (not checked).
- Sources: https://code.claude.com/docs/en/headless ; https://code.claude.com/docs/en/github-actions

**Code review and security review**

| Tool | Where | Notes |
|---|---|---|
| `/code-review` | local session | background subagent; `--fix`, `--comment`; follows CLAUDE.md |
| `/code-review ultra` (ultrareview) | cloud | research preview; many agents, findings reproduced; 5 to 10 minutes; three free runs on Pro and Max, then about 5 to 25 USD in usage credits |
| Code Review (managed) | GitHub pull requests | research preview; Team and Enterprise; inline comments by severity; about 15 to 25 USD per review, billed separately; never blocks merge; tuned by REVIEW.md |
| `/security-review`, security-guidance plugin, Claude Security plugin | local | single pass, as-you-write checks, and a multi-agent scan that proposes patches you apply yourself |

- Traps: setting managed review to run after every push multiplies cost. The check run is always neutral, so gating a merge needs your own CI step. Findings are not deterministic between runs.
- Sources: https://code.claude.com/docs/en/code-review ; https://code.claude.com/docs/en/ultrareview ; https://code.claude.com/docs/en/claude-security

**Agent SDK**
- What: Claude Code as a library for Python and TypeScript: the same agent loop, built-in tools, hooks, subagents, MCP, permissions, sessions, skills and plugins, in a process you run.
- Use: an engineer builds a custom agent (a triage bot, a migration runner) without writing the loop; a platform engineer hosts it.
- Traps: API key or cloud provider auth. Anthropic does not allow third-party products to offer claude.ai login unless approved. Products built on it must not be branded as Claude Code. The docs contrast it with the client SDK (you write the loop) and Managed Agents (Anthropic hosts the loop).
- Equivalent: OpenAI Agents SDK; Google Agent Development Kit (not checked).
- Source: https://code.claude.com/docs/en/agent-sdk/overview

### 2.6 What is missing outside a Claude subscription

With an API key or a cloud provider you lose cloud sessions, routines, Remote Control, the desktop app (with exceptions), ultrareview, managed Code Review, the Chrome integration, computer use and artifacts. On Amazon Bedrock the built-in web search is also missing. Source: https://code.claude.com/docs/en/feature-availability (checked 2 Oct 2026).

---

## 3. Claude in Chrome and computer use

### 3.1 Claude in Chrome

- What it is: a browser extension that lets Claude read pages, click, type and move between tabs using your logged-in sessions. It has its own side panel and also serves Claude Code and the desktop app.
- Use it for: QA walks a user flow on a local build and reads console errors; an engineer verifies a UI against a design; filling a web form in a tool with no API; recording a GIF of a flow for a bug report.
- Limits and traps: the extension is GA on paid plans; the side panel is beta. It needs a claude.ai login, not an API key or a third-party provider. It pauses at logins and CAPTCHAs. It acts with your access to every site you are signed into, and the help page states plainly that this is still risky. Enterprise admins can allow or block sites. From Claude Code: `claude --chrome`; keeping it on by default adds tool definitions to every session.
- Nearest equivalent: ChatGPT agent mode and the Atlas browser; Gemini in Chrome (not checked).
- Sources: https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome (updated 26 Aug 2026); https://code.claude.com/docs/en/chrome (checked 2 Oct 2026).

### 3.2 Computer use in the apps and Claude Code

- What it is: Claude takes screenshots and controls mouse and keyboard in native apps on your real desktop.
- Use it for: testing a native or Electron app, driving the iOS Simulator, operating a GUI-only tool.
- Limits and traps: Pro and Max only; not Team or Enterprise. Desktop app on macOS and Windows; CLI on macOS only and not in `-p` mode. Off by default. Each app is approved per session; browsers are view only and terminals and IDEs are click only, to steer Claude to the proper tool. It is the slowest and broadest route, so Claude tries connectors, shell and Chrome first. It is not sandboxed. One session at a time holds the screen.
- Sources: https://code.claude.com/docs/en/computer-use ; https://code.claude.com/docs/en/desktop ; https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork (checked 2 Oct 2026).

### 3.3 Computer use and browser use through the API

- What it is: a tool definition that lets your own application run the screenshot and click loop in an environment you provide. The current version (`computer_toolset_20260801`) left beta on 19 August 2026, and a browser use tool launched the same day.
- Limits and traps: you supply the sandboxed desktop and the loop. Use a dedicated VM, no real credentials, a domain allow list and human confirmation for consequential actions. Screenshots fill the context. The new toolsets are not yet on Amazon Bedrock or Microsoft Foundry.
- Sources: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool ; https://platform.claude.com/docs/en/release-notes/overview (checked 2 Oct 2026).

---

## 4. The developer platform

### 4.1 Console and the playground

- What it is: the Console (platform.claude.com) manages keys, workspaces, usage, cost, files, skills and Managed Agents. The playground is a browser page on top of the Messages API for trying a prompt, model settings, tools and structured outputs, viewing the raw request, and exporting code.
- Use it for: an engineer or product manager tries a system prompt against two models before writing code, then exports the call.
- Limits and traps: the Workbench was retired around 18 August 2026. The playground keeps only the current draft in the browser. Saved prompts, prompt versions, evaluations and prompt sharing are not part of it. The release notes of 17 July 2026 say the experimental prompt tools APIs were being retired. The old docs addresses for the Console prompt tools and the evaluation tool now lead to general pages on prompting and on writing your own evaluations. Plan to keep prompts in git and run evaluations in your own harness.
- Nearest equivalent: OpenAI Playground and Evals; Google AI Studio (not checked).
- Sources: https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench (updated 18 Aug 2026); https://platform.claude.com/docs/en/release-notes/overview ; https://platform.claude.com/docs/en/test-and-evaluate/eval-tool (now shows the page on success criteria and evaluations); https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools (now shows prompting best practices).

### 4.2 Tool use

- What it is: you describe functions; Claude returns a structured call. Client tools run in your code (your own tools, plus Anthropic-defined bash, text editor, memory, computer use, browser use). Server tools run at Anthropic (web search, web fetch, code execution, advisor, tool search, MCP connector). The SDK tool runner drives the loop for you.
- Use it for: the core of any agent. An architect decides which actions are tools, which need confirmation and where they execute.
- Limits and traps: tool definitions and results are billed as input tokens, and a hidden tool system prompt adds a few hundred tokens. `strict: true` guarantees the call matches the schema. Fable 5.1 does not accept forced tool choice. Less capable models may guess a missing parameter. Server tools add their own charges.
- Nearest equivalent: function calling in the OpenAI and Gemini APIs (not checked).
- Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview (checked 2 Oct 2026).

### 4.3 Structured outputs

- What it is: the response is constrained to a JSON Schema you supply (`output_config.format`), or tool inputs are constrained with strict tool use. GA.
- Use it for: extraction and classification steps whose output feeds code; agent hand-offs that must parse.
- Limits and traps: no recursive schemas and no numeric or string-length constraints. The first request with a new schema is slower while it compiles; the compiled form is cached for 24 hours. A refusal or hitting `max_tokens` can still produce output that does not match. Cannot be combined with citations. Limits on the number of strict tools and optional parameters apply.
- Source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs (checked 2 Oct 2026).

### 4.4 Prompt caching

- What it is: the unchanged front part of a prompt (tools, system prompt, earlier turns) is stored so later requests read it at a fraction of the price. Automatic mode places the marker for you; up to four explicit markers are allowed. Lifetime is five minutes, or one hour at a higher write price.
- Use it for: every agent loop. It is the main cost lever, so the platform engineer should watch cache read ratios.
- Limits and traps: reads cost 10 percent of input price (5 percent on Opus 5.5, 2.5 percent on Fable 5.1); writes cost 1.25 times (five minutes) or 2 times (one hour). A minimum prompt size applies (512 tokens on the newest models, 4,096 on Haiku 4.5). Changing tools, the model's thinking or effort setting, or anything early in the prompt invalidates what follows. A timestamp near the top defeats caching. Caches are isolated per workspace.
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching (checked 2 Oct 2026).

### 4.5 Message Batches

- What it is: submit up to 100,000 requests (or 256 MB) at once for asynchronous processing at half price.
- Use it for: evaluation runs, bulk classification, nightly backfills.
- Limits and traps: most batches finish within an hour but may take up to 24, after which unfinished requests expire. Results stay for 29 days and come back in any order, so match on `custom_id`. Not available on Amazon Bedrock's new endpoint, Google Cloud or Microsoft Foundry.
- Source: https://platform.claude.com/docs/en/build-with-claude/batch-processing (checked 2 Oct 2026).

### 4.6 Thinking and effort

- What it is: the model reasons before answering. On Fable 5.1, Opus 5.5 and Sonnet 5.5 this is adaptive thinking: the model decides how much, and you steer with `effort` (low, medium, high, xhigh, max). The older mode with a fixed token budget returns an error on these models. Haiku 4.5 still uses the older mode and has no effort setting.
- Use it for: tuning cost against quality per step of an agent, for example low for a sub-task, high for planning.
- Limits and traps: thinking tokens are billed as output and count toward `max_tokens` even when hidden; the text returned is a summary and is omitted by default. Thinking cannot be turned off on Fable 5.1 or Opus 5.5. Opus 5.5 defaults to medium effort, the others to high, so a migrated call may behave one level lower. Changing top-level effort mid-conversation breaks the prompt cache; a per-message effort change (beta) keeps it. `temperature`, `top_p` and `top_k` are rejected on Opus 4.7 and later.
- Sources: https://platform.claude.com/docs/en/build-with-claude/thinking ; https://platform.claude.com/docs/en/build-with-claude/effort ; https://platform.claude.com/docs/en/about-claude/model-deprecations (checked 2 Oct 2026).

### 4.7 Files API

- What it is: upload a file once and refer to it by id; download files that skills or code execution produce. GA since 19 August 2026.
- Limits and traps: 500 MB per file, 1 TB per organisation. Files are visible to the whole workspace, not to one end user, so never accept a file id from a user, and use one workspace per tenant. Uploaded files cannot be downloaded again. Not on Amazon Bedrock or Google Cloud. Not eligible for Zero Data Retention.
- Source: https://platform.claude.com/docs/en/build-with-claude/files (checked 2 Oct 2026).

### 4.8 Citations

- What it is: Claude answers from documents you pass and returns the exact passages behind each claim (text, PDF, or your own chunks). GA on all platforms.
- Use it for: answers over policies, requirements or contracts where a reviewer must check the source.
- Limits and traps: cannot be combined with structured outputs. Scanned PDFs without text are not citable. The quoted text is not billed as output.
- Source: https://platform.claude.com/docs/en/build-with-claude/citations (checked 2 Oct 2026).

### 4.9 Code execution, Agent Skills and the MCP connector

- Code execution tool: a server-side container (5 GiB memory, 5 GiB disk, no internet, lasts up to 30 days). Free when used with the current web search or web fetch tools; otherwise 1,550 free hours a month per organisation, then 0.05 USD per container hour. Not on Bedrock or Google Cloud.
- Agent Skills through the API: the same skill format, uploaded via the Skills API and run in the code execution container; shared across the workspace; no network and no package installs at run time.
- MCP connector: call remote MCP servers straight from the Messages API. Beta. Tools only (no prompts or resources); the server must be public over HTTPS. Not on Bedrock or Google Cloud.
- Sources: https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool ; https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview ; https://platform.claude.com/docs/en/agents-and-tools/mcp-connector (checked 2 Oct 2026).

### 4.10 Claude Managed Agents

- What it is: Anthropic hosts the agent loop. You define an agent (model, system prompt, tools, MCP servers, skills), an environment (Anthropic's cloud sandbox or your own self-hosted sandbox) and start sessions; you send events and stream results. Built-in tools cover bash, file operations, web search and fetch. It also offers scheduled deployments, permission policies, session budgets, memory stores, webhooks and multi-agent orchestration.
- Use it for: a long-running back-office agent where the team does not want to build and operate the loop, the sandbox and the state.
- Limits and traps: beta; every call needs the `managed-agents-2026-04-01` header. Sessions store history and sandbox state on the server, so it is not eligible for Zero Data Retention or HIPAA coverage. Available on the Claude API and Claude Platform on AWS; not on Bedrock, Google Cloud or Foundry. Memory "dreaming" and MCP tunnels are a narrower research preview.
- Nearest equivalent: left blank (not known for certain).
- Source: https://platform.claude.com/docs/en/managed-agents/overview (checked 2 Oct 2026).

### 4.11 Where Claude is available

| Route | Who operates it | What to know |
|---|---|---|
| Claude API | Anthropic | everything, first |
| Claude Platform on AWS | Anthropic, billed and authenticated through AWS | same API; features usually the same day; includes Managed Agents, Files, Skills, Batch; no fast mode, no HIPAA programme |
| Amazon Bedrock | AWS | Messages API at a Bedrock endpoint for Opus 4.7 and later; Anthropic staff have no access; no structured outputs, Files, server tools, Skills, MCP connector, Batch or Managed Agents on this endpoint; beta headers not accepted; regional endpoints cost 10 percent more |
| Google Cloud's Agent Platform (the page address still says vertex-ai) | Google | has web search and structured outputs; no Files, code execution, Skills, MCP connector, Batch or Managed Agents |
| Microsoft Foundry | Anthropic, hosted on Azure or on Anthropic | no Batch or Managed Agents; when hosted on Azure also no code execution, Skills or Files |

- Trap: the same model does not mean the same platform. An agent design that leans on server tools, skills or Managed Agents will not port to Bedrock or Google Cloud unchanged. Bedrock and Google set their own retirement dates.
- Sources: https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock ; https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws ; https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai ; https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry (checked 2 Oct 2026).

---

## 5. Current models

| Model | API id | Price per million tokens (in / out) | Context / max output | One line |
|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 10 / 50 USD | 1M / 128K | The most capable model open to everyone. For demanding reasoning and agent runs that last hours. Slowest. Released 1 Sep 2026. |
| Claude Opus 5.5 | `claude-opus-5-5` | 4 / 20 USD | 1M / 128K | The recommended starting point for most work: long agentic coding and knowledge work. Released 22 Sep 2026. |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 2 / 10 USD | 1M / 128K | Faster and cheaper for everyday coding, analysis and tool use. Released 28 Sep 2026. |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 1 / 5 USD | 200K / 64K | Fastest and cheapest; real-time, high-volume and sub-agent tasks. Older knowledge cutoff (Feb 2025). |
| Claude Mythos 5.1 | `claude-mythos-5-1` | 10 / 50 USD | 1M / 128K | Same specifications as Fable 5.1, by invitation only (Project Glasswing). |

- Still available (legacy): Fable 5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Opus 4.5, Sonnet 5, Sonnet 4.6. Sonnet 4.5 was deprecated on 30 September 2026 and retires on 30 November 2026. All Claude 3 models are retired on Anthropic's own platforms.
- Traps: ids from the 4.6 generation onward have no date and are fixed snapshots. Batch is half price. Haiku 4.5 carries the earliest retirement floor in the table (it will not be retired before 15 October 2026) and has no successor listed. The docs advise tuning effort before switching model. Fast mode (research preview) exists for some Opus models at a higher price.
- Sources: https://platform.claude.com/docs/en/about-claude/models/overview ; https://platform.claude.com/docs/en/about-claude/models/choosing-a-model ; https://platform.claude.com/docs/en/models/fable-5-1/overview ; https://platform.claude.com/docs/en/models/mythos-5-1/overview ; https://platform.claude.com/docs/en/about-claude/model-deprecations ; https://support.claude.com/en/articles/12138966-release-notes (checked 2 Oct 2026).

---

## 6. Where official pages disagree

1. Skills sharing and sync. The platform docs say custom skills in claude.ai are per user, cannot be managed centrally and do not sync between surfaces. The help centre says owners can provision skills to the whole organisation and that account skills sync one way into Claude Code. The help centre pages look newer.
2. Browsers for the Chrome integration. The Claude Code docs say it works with Chrome and Edge and is detected in other Chromium browsers. The help centre says Chrome only.
3. Computer use status. The Claude Code docs call it a research preview; the help centre calls it a beta.
4. Structured outputs on Bedrock. The structured outputs page lists Amazon Bedrock as supported; the Bedrock page for the new endpoint lists structured outputs as not supported.
5. Default model advice. The Fable 5.1 page says to start most work on Opus 5; the models overview and the choosing guide say Opus 5.5 (the Fable page predates Opus 5.5).
6. Dispatch. The Claude Code docs present it as available on Pro and Max; the help centre says limited beta and closed to new users.
7. Project viewers and chats. One help page says a viewer has read access to contents and chats; the sharing page says chats are private unless shared one by one.
8. Subagent nesting. The subagents page gives three layers by default; the June weekly digest mentioned a cap of five for background chains.

## 7. Things I could not verify

- The price of the Max 20x tier (the pricing page gave only a starting price of 100 USD with a choice of 5x or 20x).
- Whether the Console prompt generator and prompt improver still exist anywhere. The docs addresses redirect and the playground page does not mention them.
- Which model each plan gets by default in Claude Code now that Opus 5.5 and Sonnet 5.5 are out.
- The actual five-hour and weekly usage numbers for any plan.
- Whether Team and Enterprise conversations are excluded from model training (not stated on the pages opened).
- Regional availability of web search and voice.
- Pricing of Managed Agents sessions and of the API web search tool.
- Details of the memory tool, compaction and context editing in the API (only release-note lines were seen).
- GitLab CI/CD, self-hosted environments, Channels and the hooks reference (seen only through other pages).
- Agent SDK package names (the overview links to repositories named claude-agent-sdk-python and claude-agent-sdk-typescript, but the install names were not read).
- Claude Design, Claude Slides, Claude Docs, the Microsoft 365 add-ins and Claude Science beyond passing mentions.
- Every "nearest equivalent" line. None was checked in this session.
- Several help centre pages show only relative dates (for example, updated more than a week ago), so their exact dates are unknown.
- Some pages were read through an automatic summariser; numbers taken that way (skill description limits, MCP output limits, structured output limits) should be rechecked before print.

## 8. Sources opened (all on 2 October 2026)

Models and platform
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
- https://platform.claude.com/docs/en/models/fable-5-1/overview
- https://platform.claude.com/docs/en/models/mythos-5-1/overview
- https://platform.claude.com/docs/en/about-claude/model-deprecations
- https://platform.claude.com/llms.txt
- https://platform.claude.com/docs/en/release-notes/overview
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://platform.claude.com/docs/en/build-with-claude/thinking
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://platform.claude.com/docs/en/build-with-claude/files
- https://platform.claude.com/docs/en/build-with-claude/citations
- https://platform.claude.com/docs/en/managed-agents/overview
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock
- https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws
- https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai
- https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools (redirects to prompting best practices)
- https://platform.claude.com/docs/en/test-and-evaluate/eval-tool (redirects to defining success criteria and evaluations)

Claude Code
- https://code.claude.com/docs/llms.txt
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/platforms
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/plugins/overview
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/worktrees
- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/workflows
- https://code.claude.com/docs/en/vs-code
- https://code.claude.com/docs/en/jetbrains
- https://code.claude.com/docs/en/desktop
- https://code.claude.com/docs/en/desktop-scheduled-tasks
- https://code.claude.com/docs/en/claude-code-on-the-web
- https://code.claude.com/docs/en/claude-projects
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/mobile
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/github-actions
- https://code.claude.com/docs/en/code-review
- https://code.claude.com/docs/en/ultrareview
- https://code.claude.com/docs/en/claude-security
- https://code.claude.com/docs/en/chrome
- https://code.claude.com/docs/en/computer-use
- https://code.claude.com/docs/en/slack
- https://code.claude.com/docs/en/artifacts
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/feature-availability
- https://code.claude.com/docs/en/whats-new/index
- https://code.claude.com/docs/en/changelog

Apps, help centre and pricing
- https://claude.com/pricing
- https://claude.com/docs/plugins/overview
- https://support.claude.com/en/articles/12138966-release-notes
- https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://support.claude.com/en/articles/9517075-what-are-projects
- https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing
- https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects
- https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them
- https://support.claude.com/en/articles/12512176-what-are-skills
- https://support.claude.com/en/articles/12512180-use-skills-in-claude
- https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/articles/10684626-enable-and-use-web-search
- https://support.claude.com/en/articles/11088861-use-research-on-claude
- https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
- https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- https://support.claude.com/en/articles/11101966-use-voice-mode
- https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features
- https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome
- https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork
- https://support.claude.com/en/articles/15594475-what-is-claude-tag
- https://support.claude.com/en/articles/9266767-what-is-the-team-plan
- https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan
- https://support.claude.com/en/articles/8606378-how-do-i-use-the-workbench
