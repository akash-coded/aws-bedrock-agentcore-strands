# OpenAI fact sheet: ChatGPT, Codex, the developer platform and the model line-up

Checked on 2 October 2026. Every statement below comes from an official OpenAI page opened in this session. Nothing is taken from memory.

## How this was checked

- Help centre pages (help.openai.com) and chatgpt.com/pricing were opened in a browser and read as raw page text. Dates shown as "updated" are the help centre's own stamp, converted from "N days ago".
- Documentation pages on learn.chatgpt.com and developers.openai.com carry no visible date, so they are marked "checked 2 Oct 2026". Most were read through a fetch tool that condenses the page. The numbers that matter most were then re-read on the raw page: plan prices and usage tables, approval policies, config precedence, the model catalogue, the deprecations list, hook events, GitHub review, the Codex SDK and `codex exec`. One summary was caught inventing an approval policy that the raw page does not list, so treat any figure not on that re-read list as needing a second look (see section 5, item 13).
- openai.com blog posts refused the fetch tool and were not opened. Nothing here relies on them.
- "Claude equivalent" is filled in only where I am certain. Blank means "not stated", not "none exists".

## Read this first: what has changed

These points break most older training material.

1. ChatGPT now has three experiences: Chat (quick conversation), Work (an agent that finishes multi-step tasks and produces files) and Codex (software development). Work launched on 9 July 2026. The desktop app holds all three.
2. "ChatGPT agent" (agent mode) is gone. The help page says "ChatGPT agent is no longer available" and points to Work.
3. Custom GPTs are being retired in favour of plugins. Personal plans can no longer create or publish new GPTs. Retirement for affected Enterprise workspaces is planned for 11 December 2026.
4. Canvas has been withdrawn from the current chat models. Shared documents now live in ChatGPT Space as Pages.
5. The Codex documentation moved. developers.openai.com/codex now redirects to learn.chatgpt.com/docs, which covers ChatGPT Work and Codex together.
6. On the API side: the Assistants API was shut down on 26 August 2026. Agent Builder, the Evals platform (with its graders) and reusable prompt objects are deprecated and shut down on 30 November 2026. Self-serve fine-tuning is being wound down. The Videos API and Sora 2 were removed on 24 September 2026.
7. The flagship models are GPT-6 Astra, GPT-6.1 Sol and GPT-6 Luna. GPT-5.5 leaves ChatGPT, Work and Codex on 14 October 2026 (the API is not affected).

Sources: https://help.openai.com/en/articles/6825453-chatgpt-release-notes (updated 1 to 2 Oct 2026); https://help.openai.com/en/articles/11752874-chatgpt-agent (updated about 15 Sep 2026); https://developers.openai.com/api/docs/deprecations (checked 2 Oct 2026); https://learn.chatgpt.com/docs/models (checked 2 Oct 2026).

---

## 1. ChatGPT (web, desktop, mobile)

### 1.1 Chat, Work and Codex

- What it is: Chat answers questions and drafts. Work is an agent for longer tasks that end in a deliverable: a document, spreadsheet, presentation, report or Site. It can use files, plugins, a browser, code execution, subagents and scheduled tasks. Codex is the coding view.
- Where: Work runs on web and mobile (in the cloud) for paid plans except Free and Go, and in the desktop app where the plan includes it. On desktop it can also use local files and desktop apps with permission. Codex is a separate view in the desktop app with its own history.
- Use when building an agent system: a product manager hands Work a research brief and gets back a sourced comparison deck. An architect asks it to turn a design discussion into a decision record. A sponsor asks for a weekly status report built from Slack and Drive.
- Limits and traps:
  - Work and Codex share one usage allowance and credit pool. A long Work task eats into coding budget.
  - The models in Work and Codex (GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna, GPT-6 Astra) are not the models in Chat. Chat uses GPT-5.6 Sol on paid plans and GPT-5.6 Luna on Free and Go, plus Pro options.
  - Work history and Codex history are separate. A local chat runs on your computer, but messages and task context may still be stored in the cloud.
  - Admins control Work Cloud, Work Local, Codex Local and Codex Cloud as four separate switches. Enterprise and Edu had Work off by default during a two-week preview.
  - Astra can pause a task for a safety review when it suspects it has misread the instructions.
- Claude equivalent: Claude chat for Chat; Claude Cowork for Work; Claude Code for Codex.
- Sources: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex (updated 2 Oct 2026); https://learn.chatgpt.com/docs/get-started-with-work and https://learn.chatgpt.com/docs/use-chatgpt (checked 2 Oct 2026).

### 1.2 Projects

- What it is: a container that keeps related chats, files and instructions together so every chat in it starts with the same context. In the desktop app and Codex, a project can instead point at one or more local folders.
- Use: a product manager keeps the requirements, interview notes and decision log for one agent in a project and shares it with the team. A QA lead keeps the test charter and known-defect list there so every review chat reads them.
- Details checked:
  - Project instructions apply only inside the project and override global custom instructions.
  - Sources can be uploaded files, pasted text, a saved chat response, or a link to a Google Drive file or folder or a Slack channel.
  - Memory can be "default" or "project-only". Shared projects always use project-only memory.
  - Sharing gives each person chat access or edit access. Sharing is available on every plan, subject to workspace settings.
  - File and collaborator limits: Free 5 files and 5 collaborators; Go and Plus 25 files and 10 collaborators; Pro 40 files and 100 collaborators; Business, Enterprise and Edu 40 files and up to 100 collaborators.
  - Local projects in Codex find `AGENTS.md` and other configuration files in the folder automatically. A project can attach several folders with one marked as primary.
- Traps: a scheduled task created inside a project cannot read the project's files. Chats made with a GPT cannot be moved into a project. The Google Drive app does not sync ahead of time inside a project. Deleting a file in a shared project removes it for everyone. Syncing chat history does not copy a local folder to another computer.
- Claude equivalent: Claude Projects.
- Sources: https://help.openai.com/en/articles/10169521-projects-in-chatgpt (updated about 20 Sep 2026); https://help.openai.com/en/articles/8555545-file-uploads-faq (updated about 12 Sep 2026); https://learn.chatgpt.com/docs/projects (checked 2 Oct 2026).

### 1.3 Custom GPTs (being retired)

- What it is: a configured version of ChatGPT with its own instructions, knowledge files, capabilities and either connected apps or custom API actions (not both).
- Status: OpenAI plans to retire GPTs and move people to plugins. Free, Go, Plus and Pro accounts cannot create or publish new GPTs. Existing GPTs keep working until the retirement date. For affected Enterprise workspaces that date is planned as 11 December 2026, and the page says other plans are expected to follow the same timeline. A migration flow was targeted for 17 September 2026 and may not have reached every account.
- What migration carries: instructions (they become a skill), knowledge files and connected apps. What it does not carry: custom actions (rebuild them), the chosen model, some conversation starters, and sharing settings in bulk migrations. The creator or a workspace owner or admin can migrate a published GPT.
- Use: for a manual on building agents, treat GPTs as legacy. Teach the plugin and skill route instead.
- Traps: GPTs never used memory or custom instructions. A migrated plugin may answer differently from the GPT it replaces, so test before switching. Scheduled tasks do not support GPTs.
- Claude equivalent: Skills and plugins.
- Sources: https://help.openai.com/en/articles/8554407-gpts-in-chatgpt (updated about 29 Sep 2026); https://learn.chatgpt.com/docs/migrate-custom-gpts (checked 2 Oct 2026).

### 1.4 Plugins, skills, apps (connectors) and MCP

- What they are:
  - An app (older name: connector) links ChatGPT to one outside service such as Slack or Google Drive, to read data or take actions.
  - A skill is a folder of reusable instructions and supporting files for one kind of task.
  - A plugin is the installable bundle. It can hold skills, apps (built on MCP servers), app templates for admins, hooks for the Codex runtime, and extensions: sidebar views, panels, forms, and viewers or editors for file types.
- The Plugin Directory replaced the App Directory on 9 July 2026 and is shared by ChatGPT and Codex. In ChatGPT you call a plugin or skill with `@`; in Codex with `$`.
- Use: a platform engineer packages the team's "write a pull request description" skill and the GitHub and Linear apps into one plugin and sets it to Installed for the engineering role. A product manager builds a "weekly update" plugin by talking to `@plugin-creator`. An architect wraps an internal API as an MCP app so agents can query it.
- Building your own MCP app: developer mode lets Business, Enterprise and Edu workspaces on ChatGPT web add a custom MCP server, test it as a draft and publish it to the workspace. Full MCP support including write actions is described as rolling out in beta. A Secure MCP Tunnel lets a private MCP server be reached without opening inbound ports.
- App permissions: Always ask, Allow read actions, Allow low-risk actions (the default), and Allow all actions for eligible apps.
- Limits and traps:
  - Installing a plugin does not authorise its apps. Each person still connects their own account unless an admin manages the connection.
  - A plugin that includes a local MCP app works only in the desktop app, not on web or mobile.
  - Only admins and owners can publish a custom MCP app. On Business, a published app cannot be edited; you recreate and republish it. On Enterprise and Edu, new actions from a refreshed server are off until an admin enables them.
  - If the OAuth provider does not issue refresh tokens (`offline_access`), the connection drops when the first token expires.
  - Untrusted MCP servers are a prompt injection and data leak risk. The "OpenAI Verified" badge does not replace your own vendor review.
  - Not every app works in deep research, and deep research uses read actions only.
  - The plugins page says the Codex IDE extension does not support plugins, and that some plugins are unavailable when signed in with an API key.
- Claude equivalent: connectors (MCP), Agent Skills and plugins.
- Sources: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt (updated 2 Oct 2026); https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt (updated 2 Oct 2026); https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt (updated Sep 2026); https://learn.chatgpt.com/docs/skills-and-plugins, https://learn.chatgpt.com/docs/plugins, https://developers.openai.com/api/docs/guides/secure-mcp-tunnels (checked 2 Oct 2026).

### 1.5 Custom instructions, personality and memory

- What it is: custom instructions are standing guidance you write. Memory is what ChatGPT keeps from past chats and other sources and applies by itself.
- Details checked:
  - Custom instructions exist on all plans. Free and Go can save 1,500 characters; Plus, Pro, Business, Enterprise and Edu can save 5,000 (raised on 15 July 2026).
  - Memory can draw on past chats, saved memories, custom instructions, Library files and connected apps such as Gmail, depending on plan and region. A memory summary shows what it holds, and a Sources line under a reply shows what was used.
  - Temporary chats can be personalised or not, chosen at the start. They never create memories.
  - In Work and Codex there is a personality setting (Friendly, Pragmatic or None) and, in Work on the web, a writing style feature that learns from your connected mail or documents.
  - In Codex, the standing instructions live in `AGENTS.md` files. Codex "memories" are separate: generated files under `~/.codex/memories/`. An opt-in Computer History feature on macOS turns app activity into memories and a timeline.
- Use: an engineer puts team conventions in `AGENTS.md`, not in memory, so they are versioned and reviewed. A sponsor uses custom instructions to ask for short answers with risks first.
- Traps: deleting a chat does not delete a saved memory made from it. Turning memory off does not delete past chats. In regulated and Healthcare workspaces, improved memory is off by default and is not covered by a BAA. On personal accounts, remembered content can be used for training unless that setting is turned off. The docs warn against relying on memory for rules that must always apply.
- Claude equivalent: project instructions and memory in Claude; `CLAUDE.md` in Claude Code.
- Sources: https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions (updated about Aug 2026); https://help.openai.com/en/articles/8590148-memory-in-chatgpt (updated about 20 Sep 2026); https://learn.chatgpt.com/docs/personalize and https://learn.chatgpt.com/docs/customization/memories (checked 2 Oct 2026).

### 1.6 Canvas (withdrawn) and its successors: writing blocks, Space and Pages

- Status of canvas: the model release notes say that from 28 May 2026 canvas is not available in GPT-5.5 Instant or GPT-5.5 Thinking. Writing and code now appear in the chat as writing blocks and code blocks. Paid users could keep using canvas through legacy models for a limited time. The old canvas help article now returns "page doesn't exist".
- Sources disagree: the Capabilities Overview (updated about August 2026), the Projects article and the Record article still describe canvas as a current tool. Treat canvas as legacy.
- Space and Pages: Space (announced 29 September 2026) holds Pages, files and shared work. A Page is a document that you and ChatGPT both edit, with comments and child pages. Collaborators each use their own ChatGPT. Space replaces Library for accounts that have it; Projects stay separate.
- Availability: eligible Pro, Business and Enterprise users on desktop and web. Enterprise sharing is an opt-in preview.
- Use: a product manager keeps the agent's requirements as a Page the team edits together. An architect keeps the decision log there.
- Traps: sharing a Page does not share your private chats or memory, but anything written into the Page is visible to everyone who can view it.
- Claude equivalent: Artifacts (for canvas).
- Sources: https://help.openai.com/en/articles/9624314-model-release-notes (updated Sep 2026); https://help.openai.com/en/articles/9260256-chatgpt-capabilities-overview (updated about Aug 2026); https://help.openai.com/en/articles/6825453-chatgpt-release-notes (29 Sep 2026 entry); https://learn.chatgpt.com/docs/space (checked 2 Oct 2026).

### 1.7 Search and deep research

- Search: ChatGPT looks things up on the web and cites sources. It is on every plan, even when signed out. It runs automatically or on request.
- Deep research: a longer run that plans, reads many sources and writes a structured report with citations. You can review and edit the plan first, limit it to named sites, interrupt it, and export the report as Markdown, Word or PDF. Sources can be the public web, uploaded files and connected apps.
- Use: a product manager runs deep research for a competitor and vendor scan before choosing an agent framework. An architect uses it to gather the official limits of each service into one cited table.
- Limits and traps:
  - Citations can be wrong, stale or incomplete. Open the source before relying on it.
  - Deep research quotas differ by plan and are shown in an in-product counter; the help page gives no numbers.
  - Deep research uses only read actions of apps, and only apps that support it.
  - Search queries may be rewritten using memory and sent to partner search providers, along with a rough location.
  - In Work and Codex, web search defaults to a cached index for local chats; live search must be turned on (`web_search = "live"` or `--search`). Web results are untrusted input.
- Claude equivalent: web search and Research.
- Sources: https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt (updated Sep 2026); https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt (updated about 22 Sep 2026); https://learn.chatgpt.com/docs/web-search (checked 2 Oct 2026).

### 1.8 Agent mode, now ChatGPT Work: browser and computer use

- What it is: the old agent mode has been replaced by Work. Work can browse with a cloud browser (web and mobile) or the desktop app's built-in browser, sign in to sites through a secure form the model cannot read, and on desktop operate apps through computer use.
- Details checked: a browser extension links Chrome, Edge, Brave, Opera and Vivaldi to the desktop app. "Site tools" (WebMCP) let ChatGPT use actions a website offers, in the built-in desktop browser only. Computer use works on macOS and Windows in supported regions, asks before using each app, and cannot drive terminals, ChatGPT itself or admin prompts. The Atlas browser stopped working on 9 August 2026.
- Use: a QA lead has Work walk through a staging site's sign-up flow and report what broke. An engineer uses the built-in browser against a local dev server.
- Traps: when the agent drives a signed-in browser it acts as you. Keep tasks narrow and stay present for sensitive steps. Computer use, browser control and Record & Replay are limited by region. On Windows the target app must stay in the foreground.
- Claude equivalent: Claude in Chrome and computer use.
- Sources: https://help.openai.com/en/articles/11752874-chatgpt-agent (updated about 15 Sep 2026); https://learn.chatgpt.com/docs/browser, https://learn.chatgpt.com/docs/computer-use (checked 2 Oct 2026); https://help.openai.com/en/articles/6825453-chatgpt-release-notes (9 Jul, 25 Aug and 31 Aug 2026 entries).

### 1.9 Scheduled tasks, event triggers and Team Tasks

- What it is: ChatGPT runs a prompt once, on a repeating schedule, or when something happens in a connected app.
- Details checked:
  - Active task limits: 3 on Free and Go, 5 on Plus, 10 on Business and Edu, 15 on Pro and Enterprise.
  - Free users can run a task at most once a day in loose time windows. Hourly and exact times need a paid plan.
  - Event-triggered tasks run in Work and react to a new Gmail message, a new Slack channel message or GitHub pull request activity. They need Plus or above. Enterprise, Edu and Healthcare admins must switch them on. They are not on Free, Go or FedRAMP workspaces.
  - Tasks can be shared as a link; the recipient gets an independent copy and uses their own connections.
  - In the desktop app, Codex tasks can run in the local project folder (the app and computer must stay on) or in a separate Git worktree.
  - Team Tasks run in the cloud under a team's service account and shared workspace connections, and are billed in workspace credits.
- Use: a platform engineer schedules a nightly dependency and failing-test summary. A QA lead triggers a review task on every pull request. A sponsor gets a Monday digest of customer updates.
- Traps:
  - Unattended tasks run with the default sandbox and, where policy allows, with no approval prompts. In read-only mode anything that needs to write or use the network fails. Full access is risky for an unattended job.
  - Event triggers can be created or edited only on web or mobile, not in the desktop app, CLI or IDE.
  - Several events arriving together may be handled in one run.
  - Tasks do not support voice chats or GPTs. A Slack trigger needs `@ChatGPT` added to each channel.
  - Any task pinned to GPT-5.5 must be changed before 14 October 2026.
  - Team Tasks do not inherit the creator's memory or custom instructions.
- Claude equivalent: scheduled tasks and routines in Claude Code.
- Sources: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt (updated 2 Oct 2026); https://learn.chatgpt.com/docs/automations and https://learn.chatgpt.com/docs/enterprise/teams (checked 2 Oct 2026).

### 1.10 Code execution and data analysis

- What it is: ChatGPT writes and runs Python in a stateful notebook to analyse uploaded data and draw charts.
- Details checked: works with spreadsheets (.xls, .xlsx, .csv), PDFs and text or data files (.json, .xml, .yaml, .txt, .md). Interactive charts exist for bar, line, pie and scatter; other types come back as images. Files can be attached from Google Drive, OneDrive and SharePoint where connected.
- Use: a QA lead uploads an evaluation results CSV and asks for pass rate by scenario. A product manager analyses support ticket exports to size a problem.
- Traps: the Python environment cannot reach the internet. Values in scanned PDFs and image tables are not read reliably. A large or messy file may be analysed only in part. Check the generated code and assumptions before quoting a number.
- Claude equivalent: code execution and file analysis.
- Source: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt (updated about Aug 2026).

### 1.11 File and image handling

- Limits checked: 512 MB per file; 2 million tokens per text or document file; about 50 MB for a CSV or spreadsheet; 20 MB per image; 25 GB per user and 100 GB per organisation; 80 files every 3 hours, and 3 uploads a day on Free.
- Document images: only ChatGPT Enterprise reads images inside PDFs (visual retrieval). Other plans extract the text and drop the images.
- Library: Google Drive, Box, Dropbox and SharePoint can be browsed and attached without re-uploading (web first, mobile later). Library files and folders can be shared with Viewer or Editor access.
- Images: ChatGPT can read uploaded images and generate or edit images. ChatGPT Images 2.5 arrived on 8 September 2026. In Work and Codex, image generation uses the allowance about 3 to 5 times faster than a text turn.
- Use: an architect uploads a diagram and asks for a critique. A product manager generates a first mock-up of an agent's interface.
- Traps: failed uploads can count against the rate cap. A file uploaded into someone else's shared folder belongs to the folder owner.
- Sources: https://help.openai.com/en/articles/8555545-file-uploads-faq (updated about 12 Sep 2026); https://help.openai.com/en/articles/6825453-chatgpt-release-notes (8, 9 and 10 Sep 2026 entries); https://learn.chatgpt.com/docs/pricing (checked 2 Oct 2026).

### 1.12 Record and the Meetings plugin

- Record (older feature): transcribes and summarises a meeting or voice note in the older macOS desktop app. Available to Plus, Pro, Business, Enterprise and Edu. Capped at 4 hours a session. Off by default for Enterprise and Edu. Notes are saved as a canvas.
- Meetings plugin (new, beta): takes notes from microphone and system audio on a Mac with no bot joining the call, then saves a summary and action items as a Page in Space. Available in the macOS desktop app for Pro and Business; Enterprise is a limited alpha. Sessions stop at four hours. Audio is deleted once notes are ready.
- Use: a product manager records a requirements workshop and has Work turn the action items into tickets.
- Traps: you must get consent from everyone; the in-app reminder does not notify other people. Transcripts can be wrong. Record works best in English. Sharing a meeting page shares the notes, not the transcript.
- Sources: https://help.openai.com/en/articles/20001546-the-meetings-plugin-in-chatgpt (updated 1 Oct 2026); https://help.openai.com/en/articles/11487532-chatgpt-record (updated 2 Oct 2026).

### 1.13 Workspace agents, dots and Sites

- Workspace agents: shared agents built in ChatGPT with a builder, tools, apps, custom MCP servers, skills and files. They run in ChatGPT, in Slack, on a schedule or from an API call. Available on Business, Enterprise and Edu; off by default for Enterprise at launch.
  - Traps: the API trigger only queues a run. It returns 202 with no body and no run ID, and the result cannot be fetched through the API. Agent files are limited to 512 MB each and 10 GB per agent. "Connector Action Constraints" limit what the agent may ask an app to do, not what the app returns. An agent-owned connection should use a service account.
- Dots: an always-on agent on GPT-6 Astra with its own cloud computer and browser that keeps working between conversations. Rolling out gradually to Pro tiers (not in the EEA, Switzerland or the UK at launch) and Business Premium; Enterprise is a beta that is off by default. Adults only.
- Sites: ChatGPT builds and hosts a small website or app. Public beta on Plus, Pro, Business, Enterprise and Edu. Storage includes a relational database capped at 10 GB. Not for health data or card data. A deleted Site cannot be restored. Regional limits apply in the EEA, Switzerland and the UK.
- Use: a platform engineer triggers a workspace agent from an internal workflow. A sponsor gets a hosted dashboard of pilot metrics as a Site.
- Claude equivalent: not stated.
- Sources: https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business (updated about 26 Sep 2026); https://learn.chatgpt.com/docs/dots, https://learn.chatgpt.com/docs/sites (checked 2 Oct 2026); https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan (updated 2 Oct 2026).

### 1.14 Plan differences that matter for a team

| Plan | Price (USD) | What matters |
|---|---|---|
| Free | $0 | GPT-5.6 Luna in Chat. Limited Codex and limited Work on desktop only. 3 scheduled tasks. |
| Go | $8 a month | Same models as Free with higher limits. May show ads. No event-triggered tasks. |
| Plus | $20 a month | GPT-5.6 Sol at Medium and High in Chat. Work on desktop, web and mobile. Codex in CLI, IDE, web and iOS, with Codex Cloud. Limited Astra in Work and Codex. Can buy credits. |
| Pro | $100, $200 or $500 a month | Adds Extra High and Pro models in Chat, including GPT-6 Pro (Astra). No five-hour limit in Work and Codex at present. Ultrafast only on the $500 tier. |
| Business | Standard $25 a user monthly or $20 annual; Premium $125 or $100 | Shared workspace, minimum 2 seats, SAML SSO, admin roles, no training on workspace data. Premium has 5 times Standard usage and no five-hour limit. Developer mode for custom MCP apps. |
| Enterprise and Edu | Sales | Adds SCIM, role-based access control, domain verification, key management, Compliance API, data residency, usage analytics. Codex-only seats billed by usage. Many new features start switched off. |

- Local message estimates per five hours on Plus and Standard Business: Astra 5 to 45; GPT-6.1 Sol 15 to 160; GPT-6 Sol 15 to 150; Luna 350 to 3,000. Weekly limits may also apply. Cloud tasks can cost more than local ones.
- Fast mode uses included limits at 2.5 times the Standard rate (2 times when paying with credits). Astra Ultrafast uses 8 times (6 times with credits).
- Chat context windows on the pricing page: Instant 27K on Free, 54K on Go and Plus, 128K on Pro; reasoning 256K on Go and Plus, 400K on Pro.
- A ChatGPT subscription does not include API usage. Signing in to Codex with an API key bills at API rates and has no cloud features.
- A contract (not self-serve Business) is needed for zero data retention, a BAA, invoices or purchase orders.
- Sources: https://learn.chatgpt.com/docs/pricing (checked 2 Oct 2026); https://chatgpt.com/pricing (checked 2 Oct 2026); https://help.openai.com/en/articles/8792828-chatgpt-business-overview (updated about 29 Sep 2026); https://help.openai.com/en/articles/8265053-what-is-chatgpt-enterprise (updated about 29 Sep 2026); https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt (updated 2 Oct 2026).

---

## 2. Codex

Codex is OpenAI's coding agent. It is included in every ChatGPT plan, with limits that vary. The clients are the ChatGPT desktop app (Codex mode), the Codex CLI, the IDE extension and Codex on the web, plus Codex Cloud for delegated tasks.

### 2.1 Codex CLI

- What it is: a terminal agent that reads the repository, edits files and runs commands. The CLI, SDK and app server are open source at github.com/openai/codex under Apache-2.0; the repository's main language is Rust.
- Install: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`, or `npm install -g @openai/codex`, or `brew install --cask codex`, or a release binary. A PowerShell installer exists for Windows.
- Sign in with a ChatGPT account (plan usage) or an API key (API prices).
- Features checked: `codex resume`; `--image` for screenshots; `--search` for live web search; `/review`; `/init`, `/status`, `/permissions`, `/model`, `/plugins`, `/hooks`, `/import`, `/fast`, `/goal`; `codex mcp`; `codex cloud`; subagents; worktrees; voice; an agent view. Version 0.160.0 was released on 1 October 2026. Astra needs 0.153.0 or later.
- Use: an engineer runs a refactor with tests as the finish line. A platform engineer scripts it in CI with `codex exec`.
- Traps: the default model depends on the CLI version and config, so pin it. `/status` shows remaining usage. On Windows, `codex doctor` diagnoses start-up and connectivity problems.
- Claude equivalent: Claude Code CLI.
- Sources: https://learn.chatgpt.com/docs/cli, https://learn.chatgpt.com/docs/changelog, https://learn.chatgpt.com/docs/open-source (checked 2 Oct 2026); https://github.com/openai/codex (checked 2 Oct 2026).

### 2.2 IDE extension

- What it is: the same agent inside the editor. It works in VS Code and compatible editors (Cursor, Windsurf, VS Code Insiders). The page also describes Codex being available inside Xcode and JetBrains IDEs through those products' own assistants.
- Use: an engineer selects code, asks for a focused change, reviews the diff in place, and hands a bigger job to the cloud.
- Traps: the extension is closed source. It shares MCP configuration with the CLI and desktop app. Per the plugins page it does not support plugins.
- Claude equivalent: Claude Code IDE extensions.
- Source: https://learn.chatgpt.com/docs/ide (checked 2 Oct 2026).

### 2.3 Desktop app (Codex mode) and worktrees

- What it is: the ChatGPT desktop app for macOS and Windows, with a Linux preview since August 2026. A Codex chat runs Local (in your checkout), in a Worktree (an isolated Git checkout on your machine) or in the Cloud.
- Details checked: worktrees are created under `$CODEX_HOME/worktrees` in a detached HEAD state. About 15 managed worktrees are kept before older ones are removed (not while pinned or in progress). "Handoff" moves a chat between the local checkout and a worktree. The app has a review pane, a built-in browser, a terminal and voice. A Remote tab in the mobile app reaches supported desktop Codex chats.
- Use: an engineer runs three chats in parallel on separate worktrees. A QA lead reviews the diff in the review pane.
- Traps: one branch cannot be checked out in two worktrees. Parallel chats must not edit the same files. Remote access to a desktop chat still depends on that computer being on.
- Sources: https://learn.chatgpt.com/docs/app, https://learn.chatgpt.com/docs/environments/modes, https://learn.chatgpt.com/docs/environments/git-worktrees (checked 2 Oct 2026).

### 2.4 Codex Cloud (delegated tasks)

- What it is: coding tasks run on OpenAI-managed machines. You prepare and publish an environment once (repositories, dependencies, tools, network and secrets). Each task then gets its own isolated workspace and keeps running while your computer sleeps. The new experience was announced on 29 September 2026.
- Details checked:
  - Available to eligible Plus, all Pro tiers, Business, Enterprise, Healthcare and Edu. Not on Free or Go. Off by default for Enterprise workspaces that have not enabled cloud access.
  - Machine size: Plus gets 2 vCPUs, 8 GiB memory, 8 GiB disk; Pro, Business and Enterprise get 4 vCPUs, 16 GiB, 32 GiB. At launch there is no separate machine charge; model usage counts as normal.
  - Internet access is restricted by default. A "Package managers" preset allows common registries and GitHub; you can allow all or add domains.
  - "Network secrets" keep the real credential in a proxy; programs see a placeholder. Private services can be reached over Tailscale.
  - Saved machine state can be recovered for up to 7 days after the last turn.
- Use: an engineer delegates a bug investigation from a phone. A platform engineer publishes a workspace-shared environment so every task starts from the same setup.
- Traps:
  - A new task does not see another task's uncommitted work. Commit to source control.
  - Changing the environment affects new tasks only.
  - The cloud task has none of your local files, browser sign-ins or VPN.
  - Code Review, Security Review and the existing GitHub and Linear integrations still run on "Codex Cloud (Legacy)" during the transition.
  - The environments page lists computer use, browser automation, GitLab and self-hosted GitHub Enterprise Server as not supported in the new experience.
  - Codex in the cloud is not covered by OpenAI's BAA.
  - Sharing an environment can expose prepared files and environment-owned credentials to teammates.
- Claude equivalent: Claude Code on the web.
- Sources: https://help.openai.com/en/articles/20001545-using-codex-cloud (updated 1 Oct 2026); https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan (updated 2 Oct 2026); https://learn.chatgpt.com/docs/cloud, https://learn.chatgpt.com/docs/environments/cloud-environments (checked 2 Oct 2026).

### 2.5 Code review

- What it is: Codex reviews changes locally or on GitHub pull requests.
- Local: `/review` in the CLI or the review pane in the app. Scopes are a diff against a base branch, uncommitted changes, a single commit, or custom instructions. The pane can show several repositories in one project.
- GitHub: comment `@codex review` on a pull request, or turn on Automatic review per repository. The bot posts a normal GitHub review and flags only P0 and P1 issues. `@codex security review` runs a deeper Security Review (research preview). Other `@codex` requests on a pull request start a legacy cloud chat.
- Review rules live in `AGENTS.md` under a `## Code Review Rules` heading, in the file nearest the code they govern.
- Use: a QA lead writes two or three repository-specific rules (a data boundary, a compatibility constraint) and tunes them against real pull requests. An engineer runs `/review` before pushing.
- Traps: leave lint and formatting to CI, not review rules. Setting up automatic review needs push or admin rights on the repository. Signing in with an API key gives no GitHub review. GitLab merge request review is in preview.
- Claude equivalent: `/code-review` in Claude Code and Claude Code GitHub Actions.
- Sources: https://learn.chatgpt.com/docs/code-review, https://learn.chatgpt.com/docs/third-party/github (checked 2 Oct 2026).

### 2.6 Instruction and configuration files (AGENTS.md, config.toml)

- AGENTS.md: plain Markdown instructions that Codex reads before working.
  - Global: `~/.codex/AGENTS.override.md` if present, otherwise `~/.codex/AGENTS.md`.
  - Project: from the Git root down to the current directory, one file per directory, checking `AGENTS.override.md`, then `AGENTS.md`, then names in `project_doc_fallback_filenames`.
  - Files are joined from the root down, so nearer files win. The combined size stops at `project_doc_max_bytes` (32 KiB by default). Empty files are skipped. Nothing below the current directory is read.
- config.toml: `~/.codex/config.toml` for the user, `.codex/config.toml` in a project, `/etc/codex/config.toml` for the system. Command-line flags win, then project config (trusted projects only), then a selected profile, then user config, then cloud-managed defaults, then system config. Common keys: `model`, `model_reasoning_effort`, `approval_policy`, `sandbox_mode`, `web_search`, `personality`, and a `[features]` table.
- Admins enforce limits with `requirements.toml`, delivered through the admin console, macOS MDM or a system file. It can restrict approval policies, sandbox modes, web search modes, MCP servers, rules and hooks.
- Use: an architect writes the root `AGENTS.md` (build, test, conventions, what not to touch). A platform engineer pins allowed sandbox modes for the whole company.
- Traps: marking a project untrusted skips all of its `.codex/` layers, including config, hooks and rules. The 32 KiB cap silently drops the rest. ChatGPT on the web does not read local config files.
- Claude equivalent: `CLAUDE.md` and Claude Code settings files.
- Sources: https://learn.chatgpt.com/docs/agent-configuration/agents-md, https://learn.chatgpt.com/docs/config-file/config-basic, https://learn.chatgpt.com/docs/enterprise/managed-configuration (checked 2 Oct 2026).

### 2.7 Sandboxes, approval modes, auto-review and rules

- Sandbox modes: `read-only`, `workspace-write` (edit inside the workspace and run routine commands) and `danger-full-access`. Enforcement is by the operating system: Seatbelt on macOS, bubblewrap with Landlock and seccomp on Linux and WSL2, a native sandbox on Windows. It applies to every command the agent spawns. Network access for commands is off unless enabled. `.git` is protected by default.
- Approval policies: `on-request` (ask when leaving the sandbox), `never`, and a `granular` form that keeps some prompt types interactive and rejects others. The older `untrusted` value is retired, and a config that still sets it can stop the client from starting.
- In the app the same choices appear as Ask for approval (default), Approve for me (auto-review) and Full access.
- Defaults: a version-controlled folder starts in workspace-write with on-request approvals; other folders start read-only. `codex exec` is read-only by default.
- Auto-review: a separate reviewer agent decides approval requests instead of a person. It does not widen the sandbox. It stops after 3 denials in a row, or 10 in the last 50 reviews. The docs say it is not a deterministic security guarantee.
- Rules (experimental): `.rules` files written in Starlark with `prefix_rule()`, deciding `allow`, `prompt` or `forbidden` for command prefixes. Test with `codex execpolicy check`.
- Use: a platform engineer sets read-only plus on-request for exploratory work, workspace-write for CI jobs, and forbids destructive command prefixes by rule.
- Traps: `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) removes both protections, and web search then defaults to live. `--full-auto` is deprecated. If a container is your security boundary, run with `danger-full-access` inside it so Codex does not try to nest a second sandbox. `/goal` does not widen permissions.
- Claude equivalent: Claude Code permission modes and sandboxing.
- Sources: https://learn.chatgpt.com/docs/agent-approvals-security, https://learn.chatgpt.com/docs/sandboxing, https://learn.chatgpt.com/docs/sandboxing/auto-review, https://learn.chatgpt.com/docs/permission-modes, https://learn.chatgpt.com/docs/agent-configuration/rules (checked 2 Oct 2026).

### 2.8 MCP in Codex

- What it is: Codex connects to MCP servers for extra tools and context. It supports local stdio servers and remote streamable HTTP servers, with bearer tokens or OAuth.
- Set-up: `codex mcp add <name> -- <command>` or `codex mcp add <name> --url <url>`; or a `[mcp_servers.<name>]` table in `config.toml`; or Settings in the desktop app. The app, CLI and IDE extension share the configuration.
- Controls: `enabled_tools`, `disabled_tools`, per-tool approval modes, `startup_timeout_sec` (default 10) and `tool_timeout_sec` (default 60).
- Use: an engineer adds the documentation, issue tracker and error tracker servers. An architect exposes an internal design catalogue as an MCP server.
- Traps: the `codex mcp-server` command and its standalone binary have been removed; the app server replaces them for integrations. Cloud tasks may not see local MCP servers. Keep the first 512 characters of a server's instructions self-contained.
- Claude equivalent: MCP in Claude Code.
- Sources: https://learn.chatgpt.com/docs/extend/mcp, https://learn.chatgpt.com/docs/codex-sdk (checked 2 Oct 2026).

### 2.9 Skills, hooks, subagents and plugins

- Skills: a folder with a `SKILL.md` (front matter `name` and `description`, then instructions) and optional `scripts/`, `references/`, `assets/` and `agents/openai.yaml`. Codex looks in `.agents/skills` (current folder, parents and repository root), `$HOME/.agents/skills`, `/etc/codex/skills` and bundled skills. Only names and descriptions load at first; the full file loads when the skill is chosen. Call a skill with `$name` or let Codex pick it. `$skill-creator` drafts one. The format follows the open Agent Skills standard. Record & Replay (macOS, needs computer use, not in the EU, Switzerland or the UK at first) turns a demonstrated workflow into a skill.
- Hooks: scripts or MCP tool calls that run at lifecycle events: SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PreCompact, PostCompact, SubagentStart, SubagentStop, Stop and Interrupt. They are defined in `hooks.json` or `[hooks]` in `config.toml`, at user or project level, or inside a plugin. A hook can block an action, add context or decide a permission request. Non-managed hooks must be reviewed and trusted (`/hooks`) before they run.
- Subagents: Codex can run specialised agents in parallel and merge the results. Built-in types are `default`, `worker` and `explorer`. Custom agents are TOML files in `~/.codex/agents/` or `.codex/agents/`. They inherit the parent's sandbox and permission mode. The Ultra effort level uses subagents.
- Plugins: bundle skills, MCP servers, hooks and extensions for distribution. `/plugins` browses them in the CLI.
- Use: a QA lead ships a "write a regression test first" skill. A platform engineer adds a PreToolUse hook that blocks commits containing secrets. An engineer fans out a codebase survey to explorer subagents.
- Traps: subagent runs cost more tokens than one agent. Hooks do not run in cloud-orchestrated Work. Skill descriptions get truncated when many are installed, so put the trigger words first. Skills should hold one task each.
- Sources disagree: release notes say skills became generally available on 9 July 2026, while the pricing comparison table still labels the row "Skills beta".
- Claude equivalent: Agent Skills (`SKILL.md`), hooks, subagents and plugins in Claude Code.
- Sources: https://learn.chatgpt.com/docs/build-skills, https://learn.chatgpt.com/docs/hooks, https://learn.chatgpt.com/docs/agent-configuration/subagents, https://learn.chatgpt.com/docs/plugins, https://learn.chatgpt.com/docs/extend/record-and-replay (checked 2 Oct 2026).

### 2.10 Automation, scheduled and long-running work

- Scheduled tasks: see 1.9. In Codex they are called automations and can run in a dedicated background worktree.
- Goals: `/goal` in the desktop app, CLI or IDE sets an outcome that also serves as the finish test. A good goal states the outcome, the constraints and how to verify it. Progress can be paused, edited or cleared.
- Use: an engineer sets a migration goal with "the full test suite passes" as the check and lets it run.
- Traps: each chat has its own goal and context. A goal does not expand sandbox or approval rights.
- Source: https://learn.chatgpt.com/docs/long-running-work, https://learn.chatgpt.com/docs/automations (checked 2 Oct 2026).

### 2.11 SDK, headless use and the app server

- `codex exec`: runs Codex without the interactive screen. Progress goes to stderr and the final message to stdout. Flags checked: `--sandbox`, `--json` (a JSON Lines event stream), `--output-schema <file>` (final answer must match a JSON Schema), `-o` (write the last message to a file), `--ephemeral`, `--skip-git-repo-check`, and `codex exec resume`.
- Codex SDK: TypeScript package `@openai/codex-sdk` (Node.js 18 or later) and Python package `openai-codex` (Python 3.10 or later). Both start, continue and resume local Codex threads.
- App server: `codex app-server` speaks JSON-RPC 2.0 over stdio (default), a Unix socket or WebSocket. It is the interface for building a full client with sign-in, history, approvals and streamed events. Its core objects are thread, turn and item.
- GitHub Action: `openai/codex-action@v1` installs the CLI and runs `codex exec` in a workflow. Inputs include `prompt` or `prompt-file`, `sandbox`, `safety-strategy` (default `drop-sudo`), `codex-args` and `output-file`.
- Use: a platform engineer adds a CI job that asks Codex to triage a failing build and writes a structured report. A QA lead uses `--output-schema` to get a machine-readable risk summary.
- Traps: do not set `CODEX_API_KEY` or `OPENAI_API_KEY` as a job-level variable in workflows that run repository code; set it only for the Codex step. Limit who can trigger the workflow and treat pull request text as untrusted. The WebSocket transport is experimental. Windows runners need `safety-strategy: unsafe`.
- Claude equivalent: `claude -p` headless mode, the Claude Agent SDK and Claude Code GitHub Actions.
- Sources: https://learn.chatgpt.com/docs/non-interactive-mode, https://learn.chatgpt.com/docs/codex-sdk, https://learn.chatgpt.com/docs/app-server, https://learn.chatgpt.com/docs/github-action (checked 2 Oct 2026).

### 2.12 Connections to GitHub and other tools

- GitHub: a connected GitHub app gives pull request review (2.5) and repositories for cloud environments. Each person uses their own GitHub connection; access to an environment does not replace repository permissions.
- GitLab: listed as beta in the docs navigation.
- Slack: mention `@ChatGPT` in an enabled channel. For repository work it delegates to a Codex Cloud task using a workspace-shared environment and replies in the thread. Slack Connect channels shared across organisations are not supported. Replies are visible to the whole channel.
- Linear: assign an issue to Codex or mention `@Codex` in a comment. It picks an environment and repository from the issue context and posts progress. Needs a paid plan. For local use, add the Linear MCP server.
- Other: the same plugins and apps as ChatGPT; Amazon Bedrock as a model provider; an import command that brings instruction files, MCP servers, skills, hooks, commands and subagents from Claude Code or Cursor (the desktop app also imports from Claude Cowork).
- Codex Security: a security agent with a desktop plugin, a CLI (`@openai/codex-security`) and a cloud scanner in research preview.
- Compliance: Codex usage from local clients and the cloud is available in the Compliance API for Enterprise.
- Traps: keep secrets out of Slack prompts. After an import, re-check tool permissions, MCP authentication and hooks, because behaviour can differ.
- Sources: https://learn.chatgpt.com/docs/third-party/github, https://learn.chatgpt.com/docs/third-party/slack, https://learn.chatgpt.com/docs/third-party/linear, https://learn.chatgpt.com/docs/import, https://learn.chatgpt.com/docs/security (checked 2 Oct 2026); https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan (updated 2 Oct 2026).

---

## 3. The developer platform

### 3.1 Which surface to build an agent on

| Surface | What it is | Status |
|---|---|---|
| Responses API | The main model API. One call can use built-in tools and loop over tool calls. | Recommended for all new projects. |
| Chat Completions | The older message API. | Still supported. |
| Assistants API | Older stateful API. | Shut down 26 August 2026. |
| Agents SDK | An open source library (MIT) that runs the agent loop in your own application. Python `openai-agents`; TypeScript `@openai/agents` (Node 22 or later). | Current. |
| Agents API | OpenAI runs the agent for you on the Codex harness, with durable sessions and a sandbox. | Public beta since 10 September 2026. |
| ChatKit | An embeddable chat interface. | Current; the self-hosted server route is the recommended one. |
| Agent Builder | A visual workflow canvas. | Deprecated 3 June 2026; shuts down 30 November 2026. |

- Use: an architect picks the Agents API when OpenAI should hold state and run the sandbox, the Agents SDK when the team wants control of deployment, storage and approvals, and the raw Responses API when building the loop by hand.
- Agents API details: the objects are agent (model, instructions, tools, MCP servers), session (a durable run you can steer and continue) and environment (an OpenAI-hosted or self-hosted sandbox). It needs a beta header. Data residency is United States only and zero data retention is not supported.
- Responses API state: `previous_response_id`, replaying items yourself, or the Conversations API. Responses are stored by default; set `store: false` to stop that. With `previous_response_id`, all earlier input tokens are billed again as input.
- Agents SDK concepts: agents, tools, handoffs and agents as tools, guardrails, human approval, sessions, tracing, sandbox agents, realtime and voice agents. The Python README says it also works with over 100 other model providers.
- Agent Builder migration: export the workflow as Agents SDK code, or convert it into a ChatGPT workspace agent. Workflows that depend on strict determinism may not convert faithfully.
- Claude equivalent: Messages API for Responses; Claude Agent SDK for the Agents SDK; Claude Managed Agents for the Agents API.
- Sources: https://developers.openai.com/api/docs/guides/agents, https://developers.openai.com/api/docs/guides/agents-api/overview, https://developers.openai.com/api/docs/guides/agents/sdk, https://developers.openai.com/api/docs/guides/migrate-to-responses, https://developers.openai.com/api/docs/guides/chatkit, https://developers.openai.com/api/docs/guides/agent-builder, https://developers.openai.com/api/docs/guides/agent-builder/migrate-from-agent-builder, https://developers.openai.com/api/docs/changelog (checked 2 Oct 2026); https://github.com/openai/openai-agents-python, https://github.com/openai/openai-agents-js (checked 2 Oct 2026).

### 3.2 AgentKit

- I found no current product page called AgentKit. The name survives only as "Agent Kit", a row on the API pricing page for ChatKit file and image storage ($0.10 per GB-day after 1 GB free a month). Its visual builder (Agent Builder) is deprecated; ChatKit remains. The working equivalent today is the Agents SDK or Agents API plus ChatKit for the interface.
- Sources: https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/docs/deprecations (checked 2 Oct 2026).

### 3.3 Playground and prompt tools

- What exists: the docs still say to use the Playground to develop prompts. Its Generate button drafts prompts, function definitions and JSON schemas from a task description, using meta-prompts. A prompt optimizer in the dashboard rewrites a prompt using a dataset with at least three annotated rows (ratings, critiques or grader results).
- What is ending: reusable prompt objects (prompt IDs with versions and variables, the `v1/prompts` API) were deprecated on 3 June 2026 and shut down on 30 November 2026. The dataset-backed prompt optimizer is being discontinued along with the Evals platform.
- Current guidance: keep prompts in application code, under version control, reviewed in pull requests, with tests and evals run in CI. Use the `developer` role or `instructions` for rules and the `user` role for input. Pin production to a dated model snapshot.
- Use: an engineer moves prompts into a typed helper in the repository. A QA lead adds fixtures and checks next to them.
- Traps: `instructions` applies to one request only and is not carried forward by `previous_response_id`. Always test an optimised prompt before use; it can do worse on some inputs.
- Claude equivalent: the prompt generator and prompt improver in the Claude Console.
- Sources: https://developers.openai.com/api/docs/guides/prompting, https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object, https://developers.openai.com/api/docs/guides/prompt-engineering, https://developers.openai.com/api/docs/guides/prompt-generation, https://developers.openai.com/api/docs/guides/prompt-optimizer (checked 2 Oct 2026).

### 3.4 Evals and graders

- Status: the Evals platform (dashboard and API) was deprecated on 3 June 2026. Existing evals become read-only on 31 October 2026 and the platform shuts down on 30 November 2026. The graders documented for eval workflows are part of that. OpenAI's stated migration path is Promptfoo, an open source command-line tool and library, with a cookbook guide; evals are recreated by hand in a `promptfooconfig.yaml` file.
- What the grader types were: string check, text similarity, score model (a model gives a number), label model (a model picks a label), Python code, and a multigrader that combines them (used in reinforcement fine-tuning).
- Still described as available: trace grading in the dashboard (Logs, then Traces) for runs made with the Agents SDK, and datasets for annotating outputs.
- Sources disagree: the "evaluation getting started" page still presents datasets, graders and evals as the way to work, and the cookbook says dataset review and prompt iteration stay in the platform, while the deprecations page ends the Evals platform and the prompt optimizer page says the dataset-backed optimiser is ending. Whether Datasets survives after 30 November 2026 is not clear.
- Self-serve fine-tuning is also winding down: new organisations cannot start jobs, and active customers cannot create new jobs after 6 January 2027.
- Use: a QA lead should build the agent's eval suite in a tool that lives with the code (the route OpenAI now points to) and use trace grading for quick diagnosis only.
- Traps: do not start new work on the Evals API. Model graders can be gamed, so compare against human review.
- Sources: https://developers.openai.com/api/docs/deprecations, https://developers.openai.com/api/docs/guides/evals, https://developers.openai.com/api/docs/guides/graders, https://developers.openai.com/api/docs/guides/evaluation-getting-started, https://developers.openai.com/api/docs/guides/agent-evals, https://developers.openai.com/cookbook/examples/evaluation/moving-from-openai-evals-to-promptfoo (checked 2 Oct 2026).

### 3.5 Tools in the Responses API

| Tool | What it does | Limits and traps |
|---|---|---|
| Function calling | The model asks your code to run a function. | Strict mode makes arguments match the schema. With GPT-6, tools can be marked `async` so the model keeps working while your function runs. |
| Web search (`web_search`) | Searches the web and cites sources. | $10 per 1,000 calls plus tokens. Up to 100 allowed or blocked domains. Search context capped at 128k tokens. `external_web_access: false` gives cache-only mode. Citations must be shown as clickable links. `web_search_preview` is legacy. |
| File search | Retrieval over your files in a vector store. | See 3.9. |
| Remote MCP (`mcp`) | Calls tools on a remote MCP server. | No per-call fee, only tokens. `require_approval` and `allowed_tools` control it. `connector_id` (built-in connectors such as Gmail and SharePoint) is deprecated for models released after 1 September 2026. The OAuth token is not stored and must be sent each time. A malicious server can read anything in context. |
| Tool search | Loads tool definitions only when needed. | GPT-5.4 and later. Group tools in namespaces of fewer than about 10 functions. |
| Programmatic tool calling | The model writes JavaScript that calls your tools in a fresh V8 runtime, so loops and filtering happen outside the context window. | No network, file system or packages in that runtime. Prefer direct calls for writes and anything needing approval. |
| Shell | Runs commands in an OpenAI-hosted container or in your own runtime. | Needs the Responses API. Hosted containers have no outbound network unless an org allowlist and a request policy allow it. `domain_secrets` keep credentials out of the model's view. |
| Code interpreter | Runs Python in a container. | Memory tiers 1, 4, 16 or 64 GB. Container expires after 20 minutes idle and its data is lost. Containers cost from $0.03 per 20-minute session at 1 GB. |
| Computer use | See 3.10. | |
| Apply patch, image generation, skills | File edits as patches; GPT Image generation; `SKILL.md` bundles uploaded to `/v1/skills` and mounted in a shell container. | Skill bundle limits: 50 MB zip, 500 files, 25 MB uncompressed. Treat skills as privileged code; do not let end users attach arbitrary ones. |

- Use: an engineer starts with function calling and MCP, adds tool search when the tool list grows, and uses programmatic tool calling for bulk read-only data work. An architect decides which tools need `require_approval`.
- Claude equivalent: tool use, web search tool, code execution tool, MCP connector, tool search tool, programmatic tool calling, Agent Skills.
- Sources: https://developers.openai.com/api/docs/guides/tools, https://developers.openai.com/api/docs/guides/tools-web-search, https://developers.openai.com/api/docs/guides/tools-connectors-mcp, https://developers.openai.com/api/docs/guides/tools-tool-search, https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling, https://developers.openai.com/api/docs/guides/tools-shell, https://developers.openai.com/api/docs/guides/tools-code-interpreter, https://developers.openai.com/api/docs/guides/tools-skills, https://developers.openai.com/api/docs/guides/latest-model, https://developers.openai.com/api/docs/pricing (checked 2 Oct 2026).

### 3.6 Structured output

- What it is: the model's reply is forced to match a JSON Schema you supply. In the Responses API set `text.format` to `type: "json_schema"` with `strict: true`. Function calls have the same strict option.
- Use: an engineer makes every agent hand-off and every extraction a typed object. A QA lead asserts on fields instead of parsing prose.
- Traps: only a subset of JSON Schema is supported. The first request with a new schema is slower. A refusal comes back as a separate `refusal` field, and a reply cut off by `max_output_tokens` is marked incomplete, so handle both. JSON mode gives valid JSON but does not check the schema.
- Claude equivalent: structured outputs.
- Source: https://developers.openai.com/api/docs/guides/structured-outputs (checked 2 Oct 2026).

### 3.7 Prompt caching

- What it is: repeated prompt prefixes are billed at a lower rate.
- GPT-5.6 and later: caching is automatic, and you can also mark up to four explicit breakpoints per request. The minimum is 1,024 input tokens. A cache write costs 1.25 times normal input; a cache read costs 0.1 times (0.05 times on GPT-6.1 Sol). Lifetime is set by `prompt_cache_options.ttl`, which accepts only "30m".
- Earlier models: automatic only, no write fee, and `prompt_cache_retention` of `in_memory` or `24h`.
- Usage shows `cached_tokens` and `cache_write_tokens`. A Prompt Caching dashboard and cache diagnostics exist.
- Use: an architect orders prompts as fixed instructions and tools first, changing content last. A platform engineer watches the cache hit rate per agent.
- Traps: the whole prefix must match, so changing the model, tools, schema, reasoning effort or verbosity breaks the cache. Loading a new tool set breaks it from that point. Above about 15 requests a minute, traffic can spill to machines without the cached prefix. Migrating from GPT-5.5 or earlier means replacing `prompt_cache_retention` with the new option.
- Claude equivalent: prompt caching.
- Source: https://developers.openai.com/api/docs/guides/prompt-caching (checked 2 Oct 2026).

### 3.8 Batch, Flex, Fast mode and background mode

- Batch API: half price, results within 24 hours. Up to 50,000 requests and 200 MB per file, one model per batch, separate rate limit pool. Covers Responses, Chat Completions, embeddings, moderations and image endpoints.
- Flex processing (beta): `service_tier: "flex"` gives Batch prices on normal calls, with slower answers and possible "resource unavailable" errors that are not charged.
- Fast mode: `service_tier: "fast"` (called priority processing until 30 July 2026) gives faster, steadier responses at a higher price; for GPT-5.6 Sol it is twice the standard rate. Not available with EU data residency for GPT-6 models. Ultrafast is a further tier for GPT-6 Astra only.
- Background mode: `background: true` runs a long response asynchronously; you poll, stream with resume, or cancel. Response data is kept on disk for about 10 minutes, which matters for zero data retention.
- Use: a QA lead runs the nightly eval set through Batch or Flex. A platform engineer puts user-facing agents on Fast and back-office ones on Flex.
- Traps: raise client timeouts for Flex. Fast mode has a ramp limit once traffic passes 1 million input tokens a minute. Batch output order differs from input order; match on `custom_id`.
- Claude equivalent: Message Batches API (for Batch).
- Sources: https://developers.openai.com/api/docs/guides/batch, https://developers.openai.com/api/docs/guides/flex-processing, https://developers.openai.com/api/docs/guides/fast-mode, https://developers.openai.com/api/docs/guides/background (checked 2 Oct 2026).

### 3.9 Reasoning settings and long conversations

- `reasoning.effort`: values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh` and `max`, depending on the model. GPT-6 Astra and GPT-6.1 Sol accept `low` to `max` and reject `none`. GPT-6 Luna accepts `none` to `max`. The default is `medium`.
- `reasoning.mode`: `standard` or `pro` on GPT-5.6 and GPT-6 models. Pro spends more work on hard tasks.
- Reasoning tokens are billed as output and take context space. The guide suggests leaving at least 25,000 tokens for reasoning and output when starting out.
- Reasoning summaries are available through a `summary` setting. For stateless use, reasoning items carry `encrypted_content` that you pass back.
- New with GPT-6: change effort mid-conversation with a `configuration_update` item without losing the cache; steer a running turn over a WebSocket connection; asynchronous misalignment monitoring on Astra.
- Compaction: set `context_management` with a `compact_threshold` and the server shrinks the context when it passes the threshold, or call `/responses/compact` yourself. The compacted item is encrypted and not human-readable.
- Use: an architect sets effort per agent role (low for routing, high for planning). An engineer turns on compaction for long sessions.
- Traps: with reasoning on, remove `temperature`, `top_p` and `top_logprobs`. Encrypted reasoning can be reused only within the same model family. Do not prune the output of the compact endpoint.
- Claude equivalent: extended thinking and effort settings.
- Sources: https://developers.openai.com/api/docs/guides/reasoning, https://developers.openai.com/api/docs/guides/latest-model, https://developers.openai.com/api/docs/guides/compaction, https://developers.openai.com/api/docs/models (checked 2 Oct 2026).

### 3.10 File search

- What it is: hosted retrieval. You upload files into a vector store and the model searches them by meaning and keyword, then cites the passages.
- Details checked: configure with `type: "file_search"` and `vector_store_ids`. `max_num_results` trims results. Metadata `filters` narrow the search. Raw results are returned only if you ask with `include`. Price: $2.50 per 1,000 calls plus $0.10 per GB a day after the first GB.
- Use: an engineer gives a support agent the product manuals. A QA lead checks that citations point to the right file.
- Traps: fewer results means cheaper and faster but weaker answers. The page read here does not state the per-store file limits.
- Sources: https://developers.openai.com/api/docs/guides/tools-file-search, https://developers.openai.com/api/docs/pricing (checked 2 Oct 2026).

### 3.11 Computer use

- What it is: the model operates a screen. Your code sends a screenshot, the model returns actions (click, type, scroll, drag, key press, wait), your code performs them and returns a new screenshot. Supported on `gpt-6-astra` and `gpt-6.1-sol`. For Astra, having the model write code to drive the interface is described as the preferred route, with the structured `computer` tool as an alternative.
- In the Agents API (added 29 September 2026): add `computer_use` to the tools and use an OpenAI-hosted environment with a desktop and network enabled. Each new website origin needs approval, and sign-in goes through a separate flow that keeps credentials out of the model input.
- Use: a QA lead automates an end-to-end check of a web interface that has no API.
- Traps: screen content is untrusted and can carry injected instructions. Run in an isolated browser or virtual machine with an allow list. Keep a person in the loop for purchases, deletions and data sharing. Origin approval does not confirm individual actions. The old `computer-use-preview` model was shut down on 23 July 2026.
- Claude equivalent: computer use tool.
- Sources: https://developers.openai.com/api/docs/guides/tools-computer-use, https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use, https://developers.openai.com/api/docs/deprecations (checked 2 Oct 2026).

### 3.12 Guardrails and approvals

- Agents SDK: input guardrails check the request before the agent runs; output guardrails check the final answer; tool guardrails check a function tool's arguments and results. A guardrail can run blocking or in parallel, and a tripped one stops the run. A tool marked `needsApproval` (TypeScript) or `needs_approval` (Python) pauses the run and returns an interruption plus a state you can store and resume later.
- Platform level: a `safety_identifier` per end user lets OpenAI act on one abusive user instead of the whole organisation. Requests can be delayed for extra checks or blocked.
- Use: an architect puts guardrails at every tool that has side effects. A platform engineer passes a hashed user ID as the safety identifier.
- Traps: agent-level input and output guardrails run only at the start and end of a workflow, not at every step. In manager-style designs, attach guardrails to each tool. OpenAI says it cannot currently unblock a blocked identifier.
- Sources: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals, https://developers.openai.com/api/docs/guides/safety-checks (checked 2 Oct 2026).

### 3.13 Tracing

- Agents SDK: tracing is on by default on the server-side path. A trace records model calls, tool calls, handoffs, guardrails and custom spans, and is viewed in the Traces dashboard. MCP tool calls appear automatically.
- Agents API: traces show agent, generation and tool spans under Logs, then Agents. They can be exported as OpenTelemetry JSON from `GET /v1/agents/sessions/{session_id}/traces`.
- Use: an engineer reads the trace to find which tool call went wrong. A QA lead grades traces. A platform engineer exports them to the company's tracing system.
- Traps: Agents API traces are built after a turn ends, and token counts can arrive late, so a blank value does not mean zero. Export needs to be enabled for the organisation and needs the right key permission.
- Sources: https://developers.openai.com/api/docs/guides/agents/integrations-observability, https://developers.openai.com/api/docs/guides/agents-api/tracing (checked 2 Oct 2026).

### 3.14 Sandbox agents (Agents SDK)

- What it is: an agent paired with an isolated workspace that has a file system, shell, packages, mounted data and snapshots. Available in the Python and TypeScript SDKs. Runs locally, in Docker, or on hosted providers including Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop and Vercel. Built-in capabilities are shell, file system, skills, memory and compaction.
- Use: a platform engineer keeps orchestration in trusted infrastructure and gives the sandbox only narrow credentials.
- Source: https://developers.openai.com/api/docs/guides/agents/sandboxes (checked 2 Oct 2026).

---

## 4. The current model line-up

Names and IDs were read from the API model catalogue and the ChatGPT help centre on 2 October 2026.

### Flagship (API, Work and Codex)

| Model | ID | What it is for | Facts checked |
|---|---|---|---|
| GPT-6 Astra | `gpt-6-astra` | The most capable model: hard reasoning, coding, computer use, end-to-end work. | $10 input and $50 output per million tokens. 1.05M context, 128K output. Knowledge cut-off 30 April 2026. Effort low to max. Released 3 September 2026. |
| GPT-6.1 Sol | `gpt-6.1-sol` | Close to Astra for complex work at lower cost; the default suggestion for long-running agent and coding work. | $2 and $10. Same context and cut-off. Released 29 September 2026. Off by default for Enterprise and Edu. |
| GPT-6 Luna | `gpt-6-luna` | Cheap, fast model for focused, high-volume tasks: extraction, classification, summaries, simple coding. | $0.10 and $0.50. Cut-off 18 May 2026. Effort none to max. |
| GPT-6 Sol | `gpt-6-sol` | The first GPT-6 Sol, for coding and agent workflows; now behind 6.1. | Released 22 September 2026. |

Long-context requests cost more (for Astra, $20 input and $75 output).

### In ChatGPT Chat

- GPT-5.6 Sol powers Instant, Medium, High and Extra High on paid plans. GPT-5.6 Sol Pro and GPT-6 Pro (powered by Astra) are the Pro options. GPT-6 Pro is on Pro $100, Pro $200, Business and Enterprise.
- GPT-5.6 Luna is the default for Free and Go.
- Plus and Pro no longer switch automatically from Instant to thinking; you choose the level.
- GPT-5.5 retires from ChatGPT, Work and Codex on 14 October 2026.

### Other current models in the API catalogue

- GPT-5.6 Sol, Terra and Luna (released 9 July 2026): the previous family; flagship, balanced and low-cost.
- GPT-5.5 and GPT-5.5 Pro; GPT-5.4, 5.4 Pro and 5.4 Mini; GPT-5.2 and 5.2 Pro; GPT-5, 5 Mini, 5 nano and 5 Pro: older general models still listed. Dated GPT-5 and o3 snapshots shut down on 11 December 2026.
- o3 and o3-pro: older reasoning models. GPT-4.1, GPT-4.1 Mini, GPT-4o and GPT-4o Mini: older non-reasoning models.
- GPT-5.6 Cyber, with the aliases Daybreak Red and Daybreak Blue: security work for approved defenders.
- GPT-Rosalind: life sciences reasoning for approved organisations.
- GPT-Image-2.5 Sunburst (most capable) and Flare (fast): image generation and editing. GPT-Image-2 is also listed.
- GPT-Live 1: natural voice conversation ($0.05 a minute). GPT-Realtime-2.1 and 2.1 Mini: realtime voice with reasoning and tools. GPT-Realtime-Translate: live speech translation. GPT-Audio-1.5: audio through Chat Completions.
- GPT-Transcribe (files) and GPT-Live-Transcribe and GPT-Realtime-Whisper (streaming): speech to text. GPT-4o Mini TTS: text to speech.
- gpt-oss-120b and gpt-oss-20b: open-weight models under Apache 2.0.
- text-embedding-3-large and text-embedding-3-small: embeddings. omni-moderation: content moderation.

### Deprecated or removed (do not teach)

- Deprecated on 1 October 2026, off on 1 April 2027: `gpt-5.3-codex`, `gpt-5.1`, `gpt-5.4-nano`.
- Shut down on 23 October 2026: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, `gpt-4.1-nano`, `o1`, `o1-pro`, `o3-mini`, `o4-mini`, `gpt-image-1`.
- Already shut down on 23 July 2026: the GPT-5 and GPT-5.1 Codex models, `gpt-5.2-codex`, `computer-use-preview`, the search preview models and the o3 and o4-mini deep research models.
- `whisper-1` and the GPT-4o transcription models go on 26 February 2027; `tts-1` and `tts-1-hd` on 6 January 2027; older realtime and audio families on 20 January 2027; older image models on 1 December 2026.
- Sora 2 and the Videos API were removed on 24 September 2026.

Sources: https://developers.openai.com/api/docs/models, https://developers.openai.com/api/docs/models/all, https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/docs/deprecations, https://developers.openai.com/api/docs/changelog (checked 2 Oct 2026); https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt (updated 2 Oct 2026); https://learn.chatgpt.com/docs/models (checked 2 Oct 2026).

---

## 5. Things I could not verify

1. The Playground as it looks today. It needs a signed-in API account. The docs still name it and its Generate button, but I did not see the screen.
2. Whether the Datasets tool and trace grading continue after the Evals platform shuts down on 30 November 2026. The pages disagree.
3. The openai.com announcement posts (GPT-6 Astra, GPT-6 Sol and Luna, GPT-6.1 Sol, DevDay 2026 recap). The fetch tool was refused, so they were not opened. The date of DevDay 2026 is therefore not verified; many features carry a 29 September 2026 release-note date.
4. Per-plan ticks in the comparison table on chatgpt.com/pricing. The ticks did not come through as text, so plan claims here rest on the help centre and the Codex pricing page.
5. Deep research quotas per plan. The help page gives no numbers.
6. The end date for canvas on legacy models, and the retirement date for custom GPTs on plans other than Enterprise.
7. A 200-seat cap on ChatGPT Business. It appeared only in a search snippet, not on a page I opened.
8. Whether GitLab works with the new Codex Cloud. The docs list a GitLab integration as beta, but the cloud environments page lists GitLab as not supported in the new experience.
9. How the JetBrains and Xcode integrations work (the IDE page says only that those IDEs provide their own integrations), and the statement that the IDE extension does not support plugins, which came from a condensed summary of the plugins page and was not re-read on the raw page.
10. File search limits per vector store, and exact JSON Schema limits for structured outputs. The condensed pages did not give them.
11. Whether Chat Completions has an end date. The pages say only that it remains supported.
12. The long-context threshold for the higher price band.
13. Most documentation pages were read as condensed summaries. Figures re-read on the raw page are listed under "How this was checked". Other figures (for example hook time-outs, the worktree count of about 15, skill bundle limits, the auto-review circuit breaker numbers, cloud machine sizes) come from the summaries only.
14. Claude equivalents are given only where I am certain; several rows are left blank.

## 6. Sources used

Help centre (opened in a browser, raw text):

- https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- https://help.openai.com/en/articles/9260256-chatgpt-capabilities-overview
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
- https://help.openai.com/en/articles/8590148-memory-in-chatgpt
- https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
- https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt
- https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt
- https://help.openai.com/en/articles/11752874-chatgpt-agent
- https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
- https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
- https://help.openai.com/en/articles/8555545-file-uploads-faq
- https://help.openai.com/en/articles/20001546-the-meetings-plugin-in-chatgpt
- https://help.openai.com/en/articles/11487532-chatgpt-record
- https://help.openai.com/en/articles/9624314-model-release-notes
- https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt
- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://help.openai.com/en/articles/20001545-using-codex-cloud
- https://help.openai.com/en/articles/8792828-chatgpt-business-overview
- https://help.openai.com/en/articles/8265053-what-is-chatgpt-enterprise
- https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business
- https://help.openai.com/en/?q=canvas (search page, used to confirm the canvas article is gone)
- https://chatgpt.com/pricing

ChatGPT and Codex documentation (learn.chatgpt.com; developers.openai.com/codex redirects here):

- https://learn.chatgpt.com/docs
- https://learn.chatgpt.com/docs/use-chatgpt
- https://learn.chatgpt.com/docs/get-started-with-work
- https://learn.chatgpt.com/docs/quickstart
- https://learn.chatgpt.com/docs/whats-new
- https://learn.chatgpt.com/docs/whats-new/september-28-october-2-2026
- https://learn.chatgpt.com/docs/changelog
- https://learn.chatgpt.com/docs/feature-maturity
- https://learn.chatgpt.com/docs/pricing
- https://learn.chatgpt.com/docs/models
- https://learn.chatgpt.com/docs/model-selection
- https://learn.chatgpt.com/docs/agent-configuration/speed
- https://learn.chatgpt.com/docs/projects
- https://learn.chatgpt.com/docs/personalize
- https://learn.chatgpt.com/docs/customization/memories
- https://learn.chatgpt.com/docs/skills-and-plugins
- https://learn.chatgpt.com/docs/plugins
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/migrate-custom-gpts
- https://learn.chatgpt.com/docs/automations
- https://learn.chatgpt.com/docs/long-running-work
- https://learn.chatgpt.com/docs/enterprise/teams
- https://learn.chatgpt.com/docs/enterprise/managed-configuration
- https://learn.chatgpt.com/docs/web-search
- https://learn.chatgpt.com/docs/browser
- https://learn.chatgpt.com/docs/computer-use
- https://learn.chatgpt.com/docs/dots
- https://learn.chatgpt.com/docs/space
- https://learn.chatgpt.com/docs/sites
- https://learn.chatgpt.com/docs/extend/record-and-replay
- https://learn.chatgpt.com/docs/extend/mcp
- https://learn.chatgpt.com/docs/cli
- https://learn.chatgpt.com/docs/ide
- https://learn.chatgpt.com/docs/app
- https://learn.chatgpt.com/docs/cloud
- https://learn.chatgpt.com/docs/environments/modes
- https://learn.chatgpt.com/docs/environments/cloud-environments
- https://learn.chatgpt.com/docs/environments/git-worktrees
- https://learn.chatgpt.com/docs/code-review
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/agent-configuration/rules
- https://learn.chatgpt.com/docs/config-file/config-basic
- https://learn.chatgpt.com/docs/sandboxing
- https://learn.chatgpt.com/docs/sandboxing/auto-review
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://learn.chatgpt.com/docs/permission-modes
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/codex-sdk
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://learn.chatgpt.com/docs/app-server
- https://learn.chatgpt.com/docs/github-action
- https://learn.chatgpt.com/docs/third-party/github
- https://learn.chatgpt.com/docs/third-party/slack
- https://learn.chatgpt.com/docs/third-party/linear
- https://learn.chatgpt.com/docs/import
- https://learn.chatgpt.com/docs/security
- https://learn.chatgpt.com/docs/open-source
- https://developers.openai.com/workspace-agents

API documentation (developers.openai.com; platform.openai.com/docs redirects here):

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/all
- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/deprecations
- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/tracing
- https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use
- https://developers.openai.com/api/docs/guides/agents/sdk
- https://developers.openai.com/api/docs/guides/agents/models
- https://developers.openai.com/api/docs/guides/agents/sandboxes
- https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- https://developers.openai.com/api/docs/guides/agents/integrations-observability
- https://developers.openai.com/api/docs/guides/agent-evals
- https://developers.openai.com/api/docs/guides/agent-builder
- https://developers.openai.com/api/docs/guides/agent-builder/migrate-from-agent-builder
- https://developers.openai.com/api/docs/guides/chatkit
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://developers.openai.com/api/docs/guides/prompting
- https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object
- https://developers.openai.com/api/docs/guides/prompt-engineering
- https://developers.openai.com/api/docs/guides/prompt-generation
- https://developers.openai.com/api/docs/guides/prompt-optimizer
- https://developers.openai.com/api/docs/guides/evaluation-getting-started
- https://developers.openai.com/api/docs/guides/evals
- https://developers.openai.com/api/docs/guides/graders
- https://developers.openai.com/api/docs/guides/tools
- https://developers.openai.com/api/docs/guides/tools-web-search
- https://developers.openai.com/api/docs/guides/tools-file-search
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- https://developers.openai.com/api/docs/guides/tools-skills
- https://developers.openai.com/api/docs/guides/tools-tool-search
- https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling
- https://developers.openai.com/api/docs/guides/tools-shell
- https://developers.openai.com/api/docs/guides/tools-code-interpreter
- https://developers.openai.com/api/docs/guides/tools-computer-use
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/guides/batch
- https://developers.openai.com/api/docs/guides/flex-processing
- https://developers.openai.com/api/docs/guides/fast-mode
- https://developers.openai.com/api/docs/guides/background
- https://developers.openai.com/api/docs/guides/compaction
- https://developers.openai.com/api/docs/guides/reasoning
- https://developers.openai.com/api/docs/guides/deep-research
- https://developers.openai.com/api/docs/guides/safety-checks
- https://developers.openai.com/cookbook/examples/evaluation/moving-from-openai-evals-to-promptfoo

Official repositories:

- https://github.com/openai/codex
- https://github.com/openai/openai-agents-python
- https://github.com/openai/openai-agents-js
