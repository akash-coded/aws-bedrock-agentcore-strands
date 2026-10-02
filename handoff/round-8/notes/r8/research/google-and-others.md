# Fact sheet: Google tools and other tools for building software with AI agents

Checked on 2 October 2026. Every statement below comes from a page opened in this session on an official source. Each entry ends with the source address and either the page's own date or the date of the check. Where a page carries no date, the entry says "checked 2 Oct 2026".

How the checking was done: pages were opened with a web fetch tool that returns a summary, and the pages that carry the most weight (the Gemini model list, pricing, terms, AI Studio quickstart, Build mode, Google AI plans, Firebase Studio, Jules limits, the Agent Platform overview and rename table, the Spec Kit and Gemini CLI READMEs) were also read as raw page text. Numbers that were only seen through a summary are marked "(summary only)".

Big changes since early 2026 that a reader with older knowledge will get wrong:

- Gemini CLI stopped serving free, Google AI Pro and Google AI Ultra users on 18 June 2026. Its replacement for those users is Antigravity CLI.
- Firebase Studio is closing on 22 March 2027 and has taken no new users since 22 June 2026.
- NotebookLM was renamed Gemini Notebook on 16 July 2026.
- Vertex AI is now Gemini Enterprise Agent Platform. Agent Engine is now Agent Runtime.
- GitHub Copilot coding agent is now Copilot cloud agent (April 2026).
- The current Gemini line is the 3.x family. The 2.0 models are shut down and 2.5 is closed to new users.

---

## 1. Google AI Studio

Google AI Studio is a browser tool for trying Gemini models, shaping prompts, and turning a working prompt into code or a small app. Using it costs nothing in every region where it is offered, but the free use has data consequences (see 1.9).

### 1.1 The prompt playground: chat prompts, system instructions, run settings

- What it is: the default screen. You type a system instruction, chat with a chosen model, and change settings in a side panel called Run settings (model parameters, safety settings, and switches for tools).
- Who uses it for what: a product manager drafts the system instruction for an agent role and checks tone and refusals before any code exists. An engineer finds the model and settings that give stable output, then exports them. A QA lead reproduces a bad answer by replaying the same instruction and input.
- Limits and traps: every turn of the chat is sent again with the next message, so long sessions grow until they hit the model's token limit. System instructions can be edited after the chat starts, which makes it easy to lose track of which instruction produced which answer. The quickstart's sample output still shows a 2.5 model name, so screenshots in the docs lag the product.
- Source: https://ai.google.dev/gemini-api/docs/ai-studio-quickstart (page dated 30 Jul 2026)

### 1.2 Structured output

- What it is: a setting that makes the model answer in JSON that follows a schema you give it. In the SDKs the schema can be written as a Pydantic or Zod type.
- Who uses it for what: an architect fixes the contract between an agent step and the code that consumes it (for example a triage record with fixed fields). QA writes checks against that schema.
- Limits and traps: only part of JSON Schema is supported, and very large or deeply nested schemas can be rejected. The output is valid JSON, but the values can still be wrong, so the application must check meaning itself. On Gemini 3 models it can be combined with Search, URL context, code execution, file search and function calling.
- Source: https://ai.google.dev/gemini-api/docs/structured-output (page dated 23 Sep 2026)

### 1.3 Tools in the playground

Grounding with Google Search
- What it is: the model runs web searches and returns an answer with citations that mark which span of text each source supports.
- Use: a product manager or analyst tests whether an agent that must answer about current facts can cite them. An engineer inspects the citation data before designing how to show sources.
- Limits and traps: on Gemini 3 models billing is per search query the model runs, and one prompt can trigger several. On the paid tier the pricing page lists 5,000 search requests a month free across Gemini 3.x models, then 14 US dollars per 1,000. Free tier allowances are smaller and differ by model.
- Sources: https://ai.google.dev/gemini-api/docs/google-search (23 Sep 2026); https://ai.google.dev/gemini-api/docs/pricing (1 Oct 2026)

Code execution
- What it is: the model writes Python and runs it in a Google sandbox, then uses the result in its answer.
- Use: an engineer or analyst checks arithmetic, parses a CSV, or draws a chart during prompt design, without setting up a runtime.
- Limits and traps: Python only. The run time limit is 30 seconds. You cannot install your own libraries. It cannot hand back arbitrary files. There is no separate fee, but the generated code and its output are billed as tokens.
- Source: https://ai.google.dev/gemini-api/docs/code-execution (23 Sep 2026)

URL context
- What it is: the model fetches the pages you name and reads them as part of the prompt.
- Use: a product manager or architect asks questions against a public spec, a vendor document or a competitor page without pasting it in.
- Limits and traps: up to 20 URLs per request and up to 34 MB per URL. Pages must be public. It does not read paywalled pages, YouTube videos, Google Docs or Sheets, or audio and video files. Fetched content is billed as input tokens.
- Source: https://ai.google.dev/gemini-api/docs/url-context (23 Sep 2026)

Function calling is also a switch in Run settings (quickstart page above). Grounding with Google Maps and file search exist as API tools; their behaviour inside the AI Studio screen was not checked.

### 1.4 Compare mode

- What it is: a side by side view that sends one prompt, with optional system instructions, to more than one model so you can compare answers and speed.
- Use: an architect or engineer chooses between a larger and a smaller model for one agent step. A sponsor sees the quality and latency difference in one screen.
- Limits and traps: the only official page found is a Google Developers Blog post from 17 October 2024, which says the Compare button sits at the top right of a prompt. Whether the button is in the same place in the October 2026 interface is not verified. It is a by-eye comparison, not a scored evaluation.
- Source: https://developers.googleblog.com/compare-mode-in-google-ai-studio/ (17 Oct 2024)

### 1.5 Saving, sharing and Get code

- What it is: a prompt can be saved to return to later and shared with other people. The Get code button turns the current prompt and settings into Gemini API code in a language you choose.
- Use: a product manager hands an engineer a saved prompt instead of a screenshot. The engineer takes the Get code output as the first version of the call in the code base.
- Limits and traps: the docs do not say where saved prompts are stored. Posts on Google's developer forum describe storage in the owner's Google Drive and problems after moving files to a shared drive, but that is forum content and is listed as not verified. The docs do not list the Get code languages.
- Source: https://ai.google.dev/gemini-api/docs/ai-studio-quickstart (30 Jul 2026)

### 1.6 Build mode (app building)

- What it is: you describe an app and AI Studio generates a working project with a live preview. By default it is a web app with a React front end and a Node.js server side. It can also generate a native Android app in Kotlin and Jetpack Compose with an emulator in the browser. The agent doing the work is the Antigravity Agent, the same agent harness used in Google Antigravity.
- Use: a product manager or designer makes a clickable prototype of an agent's user interface in an afternoon. An engineer builds a thin demo around a prompt, then moves it to GitHub. A sponsor gets something to click.
- What it offers: start from a prompt, from a gallery app, or by importing a GitHub repository. Edit by chat, by editing code in the Code tab, or by annotation mode, where you mark part of the screen and say what to change. Server side secrets are kept in Settings. Firebase Firestore and sign-in, and Google Workspace APIs, can be wired in by the agent. Two-way sync with a GitHub repository, ZIP download, and deployment to Cloud Run are built in.
- Limits and traps: when you share an app, its API calls count against your own limits, and paid models can cost you money. Cloud Run charges can apply after deployment. A Google Cloud Starter Tier lets eligible accounts publish up to 2 full-stack apps without a billing account (summary only). The Code Assistant in Build mode is named as a benefit of paid Google AI plans. Generated code needs the same review as any other code.
- Sources: https://ai.google.dev/gemini-api/docs/aistudio-build-mode (20 Aug 2026); https://ai.google.dev/gemini-api/docs/aistudio-deploying (28 Sep 2026); https://ai.google.dev/gemini-api/docs/google-ai-plans (18 Aug 2026)

### 1.7 Live (real time) features

- What it is: AI Studio has a real time streaming prompt type that fronts the Live API, which holds a low latency spoken conversation and can take audio, images and text as a continuous stream. The user can interrupt the model, tools and function calls work during the conversation, and both sides can be transcribed.
- Use: a product manager or designer tries a voice agent's persona before any build. An engineer tests tool calls in a spoken session. QA probes interruption handling.
- Limits and traps: without context compression an audio-only session is limited to 15 minutes and a session with video to 2 minutes. A single connection lasts about 10 minutes unless session resumption is set up. For a browser or mobile client that connects directly, Google recommends short-lived tokens in place of an API key. The current default Live models are Gemini 3.8 Live and Gemini 3.8 Live Extended Thinking. The docs page does not name screen sharing, so that is not verified for the current interface.
- Sources: https://ai.google.dev/gemini-api/docs/live (15 Sep 2026); https://ai.google.dev/gemini-api/docs/live-api/session-management (15 Sep 2026)

### 1.8 Agents in the Playground

- What it is: a screen for trying managed agents without writing API calls. The agent runs in a Linux sandbox. Its behaviour is set by files in a .agents folder (AGENTS.md for instructions, SKILL.md files for skills). Sources can be mounted from inline files, Cloud Storage or GitHub. Tools include Google Search, URL context, code execution and file tools.
- Use: an architect or platform engineer learns what a managed agent setup looks like before committing to the Interactions API. An engineer prototypes an agent with skills and downloads the environment.
- Limits and traps: one prompt can consume an unbounded number of tokens because the agent keeps planning and acting until it is done or you stop it. The environment is fixed once the first message is sent. Agent access in AI Studio is not covered by Google AI plans and needs a paid API key. The underlying Antigravity Agent (antigravity-preview-09-2026) is in preview.
- Sources: https://ai.google.dev/gemini-api/docs/aistudio-agents (18 Aug 2026); https://ai.google.dev/gemini-api/docs/antigravity-agent (checked 2 Oct 2026); https://ai.google.dev/gemini-api/docs/managed-agents-quickstart (1 Oct 2026)

### 1.9 Free tier limits, plans and what the data is used for

- Cost: AI Studio use is free of charge in all available regions (pricing page, 1 Oct 2026).
- Rate limits: limits are counted per project, not per key, on three measures: requests per minute, tokens per minute and requests per day (daily counts reset at midnight Pacific time). Tiers are Free, Tier 1 (billing linked), Tier 2 and Tier 3 (reached by spend and time). The docs do not publish the free numbers. They tell you to read your own limits inside AI Studio. Any fixed free tier number quoted in a manual will go stale.
- Plans: Google AI Pro and Ultra subscriptions raise the daily quota and unlock paid models inside the AI Studio web interface only. They do not pay for API calls made with a key. Quota resets daily.
- Data: under the Gemini API terms, content sent to unpaid services, which include AI Studio and the free API tier, can be used to improve Google products, and human reviewers may read it after it is separated from your account and key. The terms tell users not to send sensitive, confidential or personal information to unpaid services. On paid services prompts and responses are not used to improve products. Users in the European Economic Area, Switzerland and the United Kingdom get the paid-service data terms even on free use.
- Trap: a team that prototypes in the free tier with real customer data has sent that data under the unpaid terms. Use synthetic data, or a project with billing on.
- Workspace: AI Studio is on by default for Google Workspace editions, admins can turn it off per organisational unit, and education users under 18 are blocked.
- Access errors: a 403 usually means an unsupported region or a terms problem.
- Sources: https://ai.google.dev/gemini-api/docs/pricing (1 Oct 2026); https://ai.google.dev/gemini-api/docs/rate-limits (2 Sep 2026); https://ai.google.dev/gemini-api/docs/google-ai-plans (18 Aug 2026); https://ai.google.dev/gemini-api/terms (effective 23 Mar 2026); https://ai.google.dev/gemini-api/docs/workspace (28 Apr 2026); https://ai.google.dev/gemini-api/docs/troubleshoot-ai-studio (9 Sep 2026)

---

## 2. Jules (Google's asynchronous coding agent)

- What it is: a coding agent that works on a GitHub repository in a cloud virtual machine while you do something else. The docs still call it experimental.
- How a task is given: choose a repository and branch, write a prompt, and optionally attach images (PNG or JPEG, 5 MB in total). A task can also be started by adding the label "jules" to a GitHub issue, from the Jules Tools command line, or through the API. Scheduled tasks and suggested tasks (scans for TODO comments and similar) also exist.
- How it is reviewed: Jules writes a plan first. You approve it, or edit it through chat. If you leave the page, the plan is approved automatically after a timer, and a "planning critic" step reviews plans that are approved that way (changelog, 26 Jan 2026). You can send feedback or pause while it works. At the end it gives a summary and the changed files, creates a branch, and you open a pull request from it.
- GitHub connection: you sign in to GitHub and install the Jules app on all or selected repositories. It works with GitHub only.
- Environment: a fresh Ubuntu machine per task with common tool chains installed. A setup script can be run once and saved as a snapshot to speed up later tasks. Long-running processes such as a dev server are not supported.
- Plans and limits (raw page text): free plan 15 tasks per rolling 24 hours and 3 at once; Jules in Pro 100 and 15; Jules in Ultra 300 and 60. Paid plans come through Google AI Pro or Ultra and are offered only to personal @gmail.com accounts. Users must be 18 or older.
- CLI and API: Jules Tools installs with npm install -g @google/jules. It has jules login, jules remote new, jules remote list and jules remote pull, plus a terminal dashboard. The Jules API is in alpha at https://jules.googleapis.com/v1alpha/ with sources, sessions and activities, and an API key (up to 3 per account).
- Other features in the changelog: MCP server support (2 Feb 2026), a CI fixer for failing GitHub Actions and a choice of commit author (19 Feb 2026).
- Who uses it for what: an engineer hands off bounded chores (dependency bumps, tests, small fixes) and reviews pull requests. A platform engineer wires the API or the issue label into a ticket flow. QA asks for missing tests on a branch.
- Traps: the newest changelog entry is dated 9 March 2026 (Gemini 3.1 Pro for Pro plan users) and the limits page still names Gemini 2.5 Pro and Gemini 3 Pro, although the Gemini API model page lists Gemini 3 Pro Preview as shut down. Treat the model named on the Jules pages as out of date. The auto-approve timer means an unread plan can still run. The machine has internet access, so keep secrets out of the repository. The FAQ says private repositories are not used for training.
- Sources: https://jules.google/docs/ ; https://jules.google/docs/running-tasks/ ; https://jules.google/docs/review-plan/ ; https://jules.google/docs/environment/ ; https://jules.google/docs/usage-limits/ ; https://jules.google/docs/faq/ ; https://jules.google/docs/cli/reference/ ; https://jules.google/docs/changelog/ (all checked 2 Oct 2026, no page dates); https://developers.google.com/jules/api (page dated 10 Nov 2025)

---

## 3. Gemini CLI, Gemini in the IDE, Gemini Notebook, Agent Platform and ADK

### 3.1 Gemini CLI and Antigravity CLI

- What they are: Gemini CLI is Google's open source (Apache 2.0) terminal coding agent, with file, shell, web fetch and Google Search tools, MCP support, GEMINI.md context files, a headless mode with JSON output, and a GitHub Action. Antigravity CLI (the command is agy) is the newer terminal agent on the Antigravity platform.
- What changed: a Google Developers Blog post of 19 May 2026 announced that Gemini CLI would stop serving consumer plans. The Gemini CLI docs site now carries a notice that for unpaid tier and Google One users it was replaced by Antigravity CLI on 18 June 2026. The Gemini Code Assist docs say the same for Code Assist for individuals, Google AI Pro and Ultra. Organisations with Gemini Code Assist Standard or Enterprise keep Gemini CLI. The quota page also still lists a Gemini API key route and a Vertex AI route for Gemini CLI.
- Antigravity CLI facts: installed by a script from antigravity.google on macOS, Linux and Windows. Sign-in is by Google account, or by a Gemini API key set in its settings file for headless and CI use. On first run it can import Gemini CLI extensions, skills and settings.
- Who uses it for what: an engineer runs an agent against a local repository. A platform engineer runs it headless in CI for review or triage jobs.
- Traps: the Gemini CLI README on GitHub still advertises a free tier with a personal Google account (60 requests a minute, 1,000 a day), which conflicts with the notice on the docs site. Trust the notice. The repository is still active (latest release v0.62.0, 29 Sep 2026). Whether Antigravity CLI is open source is not stated on the pages read.
- Sources: https://github.com/google-gemini/gemini-cli (checked 2 Oct 2026); https://geminicli.com/docs/ (checked 2 Oct 2026); https://geminicli.com/docs/resources/quota-and-pricing/ (dated 18 Jun 2026); https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli (19 May 2026); https://antigravity.google/docs/cli/overview/ and https://antigravity.google/docs/cli/install/ (checked 2 Oct 2026)

### 3.2 Google Antigravity (desktop app and IDE)

- What it is: Google's agent-first development product. The docs describe three surfaces: Antigravity 2.0, a desktop app for running and supervising agents; Antigravity CLI; and Antigravity IDE. Agents produce artifacts such as implementation plans, walkthroughs and screenshots for a person to review, can drive Chrome, and can be extended with rules, skills, MCP servers and workflows.
- Who uses it for what: an engineer runs several agent tasks and reviews their plans and walkthroughs. An architect reads the plan artifact before code is written.
- Models listed: Gemini 3.8 Flash, 3.7 Flash, 3.6 Flash and 3.1 Pro, plus Claude Sonnet 4.6, Claude Opus 4.6 and GPT-OSS-120b. The third-party models are not offered on enterprise plans (summary only).
- Limits and traps: quota is by capacity, not a fixed count. The free tier refreshes weekly. Pro and Ultra refresh every five hours within weekly limits, and can buy AI credits for overage. The plans page says bring-your-own-key is not supported for the plans it describes (summary only).
- Sources: https://antigravity.google/docs/getting-started ; https://antigravity.google/docs/overview/ ; https://antigravity.google/docs/models/ ; https://antigravity.google/docs/plans/ (all checked 2 Oct 2026)

### 3.3 Gemini Code Assist (IDE extensions)

- What it is: Google Cloud's coding assistant for VS Code, JetBrains IDEs, Cloud Workstations, Cloud Shell Editor and Android Studio, sold as Standard and Enterprise editions. It has an agent mode that can use system tools and MCP servers. Enterprise adds code customisation from private repositories.
- Use: an enterprise engineer who must stay inside Google Cloud terms gets completion, chat and agent mode with source citations and indemnity.
- Trap: the individual, Pro and Ultra tiers stopped being served on 18 June 2026. Those users are pointed to Antigravity.
- Source: https://docs.cloud.google.com/gemini/docs/codeassist/overview (24 Sep 2026)

### 3.4 Gemini in Android Studio

- What it is: the assistant inside Android Studio. Agent Mode takes a goal, plans, edits several files, builds the project to check its fix, and can deploy to a device, take screenshots and read Logcat. Changes are proposed for you to accept or reject. It supports MCP servers, AGENTS.md files, rules, skills, and a choice of local or remote model, including your own API key.
- Use: a mobile engineer building the Android client of an agent product fixes build errors, writes unit tests, and runs UI test journeys.
- Limits: the free tier for individuals has a small context window. A business tier adds quota, admin controls and data residency. An .aiexclude file keeps files out of context.
- Sources: https://developer.android.com/studio/gemini/overview (25 Aug 2026); https://developer.android.com/studio/gemini/agent-mode (14 Jul 2026)

### 3.5 Firebase Studio

- What it is: a browser development environment (the successor to Project IDX) with an app prototyping agent. It is still labelled Preview.
- Status: it closes on 22 March 2027. New workspaces and sign-ups have been disabled since 22 June 2026. Existing workspaces can be used and moved to Google AI Studio or Antigravity. Apps already deployed to Firebase keep running, and core Firebase products are not affected.
- Advice for the manual: do not teach it as a tool to adopt. Mention it only for teams that must migrate.
- Source: https://firebase.google.com/docs/studio (1 Oct 2026)

### 3.6 Gemini Notebook (formerly NotebookLM)

- What it is: a research assistant that answers only from the sources you load (PDFs, web pages, YouTube videos, audio, Google Docs and Slides) and marks each answer with citations. It also produces briefings, study guides, audio and video overviews and mind maps. Since the rename on 16 July 2026, a notebook can also write and run code on a cloud computer for data analysis. That feature went first to Ultra and some Workspace customers, with Pro to follow.
- Who uses it for what: a product manager loads interview notes, the PRD and policy documents and asks questions with citations. An architect loads vendor documents and standards. A sponsor listens to an audio overview of a long design document. QA loads the requirements and asks what is untested.
- Limits (help page, summary only): Standard 100 notebooks, 50 sources each, 50 chats a day; Plus 200, 100, 200; Pro 500, 300, 500; Ultra 500 notebooks and 500 or 600 sources. A source can hold up to 500,000 words or 200 MB. The same page says limits changed from 2 September 2026, so check the live table.
- Data: for personal accounts, content is not used to train foundation models unless you send feedback, in which case reviewers may see it. For Workspace and education accounts, uploads, queries and answers are not reviewed by people and not used for training.
- Traps: it does not act on a repository and is not a retrieval system for a shipped product. Answers are only as good as the sources loaded.
- Sources: https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ (16 Jul 2026); https://support.google.com/notebooklm/answer/16164461 ; https://support.google.com/notebooklm/answer/16213268 ; https://support.google.com/notebooklm/answer/16269187 ; https://support.google.com/gemininotebook/answer/17004255 (help pages checked 2 Oct 2026)

### 3.7 Gemini Enterprise Agent Platform (formerly Vertex AI and Vertex AI Agent Builder)

Vertex AI has been renamed Gemini Enterprise Agent Platform, and the old Agent Builder address now opens the Agent Platform overview. The docs sort it into four groups. Build: Agent Development Kit, Agent Studio (a low-code canvas, formerly Vertex AI Studio), Agent Garden (prebuilt agents), Model Garden, RAG Engine, Vector Search and a Managed Agents API. Scale: Agent Runtime (formerly Agent Engine), Sessions, Memory Bank and Code Execution. Govern: Agent Registry, Agent Identity, Agent Gateway and policies, with Model Armor. Optimize: agent evaluation (including evaluation of live traffic and simulated multi-turn users), tracing, and prompt optimisation. An architect uses it to decide where agents run and how identity and tool calls are governed on Google Cloud. A platform engineer deploys an ADK agent to Agent Runtime and wires the registry and gateway. QA uses the evaluation and simulation services. Trap: older material uses the Vertex names, so use the rename table to map them. The overview page does not state which parts are generally available and which are preview, so that is not verified here.
- Sources: https://docs.cloud.google.com/agent-builder/overview (1 Oct 2026); https://docs.cloud.google.com/gemini-enterprise-agent-platform/vertex-ai-name-changes (1 Oct 2026)

### 3.8 Agent Development Kit (ADK)

ADK is Google's open source framework for writing agents in code. It is offered for Python, TypeScript, Go, Java and Kotlin, and its docs moved to adk.dev. It gives you LLM agents, workflow agents (sequence, loop, parallel), graph workflows (new in ADK 2.0), tools (your functions, MCP, OpenAPI), agent-to-agent calls over the A2A protocol, sessions, memory, artifacts, callbacks, a web interface for development, an evaluation framework and tracing. It is built for Gemini but works with other models through adapters, and it deploys to Cloud Run, GKE or Agent Runtime. An engineer writes the agent. QA writes evaluation sets that run in CI. An architect decides which steps are fixed code in a graph and which are left to the model. Amazon Bedrock AgentCore Runtime lists Google ADK among the frameworks it can host, so ADK agents are not tied to Google Cloud. Trap: the 2.0 graph feature was seen announced for TypeScript; version numbers for the other languages were not checked.
- Sources: https://adk.dev/ and https://adk.dev/get-started/about/ (checked 2 Oct 2026)

---

## 4. Other tools a seasoned team uses

### 4.1 Amazon Bedrock playgrounds

The Bedrock console has playgrounds for text and chat and for images, where you pick a model, set inference configuration and run prompts. The user guide page for playgrounds is now a stub that points to the console itself, and it notes that custom models are not supported there. AWS announced a new console experience on 5 June 2026 (updated 13 July 2026), organised around projects and the Responses, Chat Completions and Messages APIs, with side by side comparison of up to 3 models. Agents, Knowledge Bases and Guardrails stay in the existing console. The Bedrock chat playground inside SageMaker Unified Studio documents a Compare mode for up to 3 models or shared apps and shows input tokens, output tokens and latency for each run. A product manager or engineer uses these to choose a model for an agent step. A sponsor can watch the comparison. Trap: there are now three places with a "playground" and they do not behave the same.
- Sources: https://docs.aws.amazon.com/bedrock/latest/userguide/playgrounds.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-console.html ; https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/bedrock-explore-chat-playground.html (checked 2 Oct 2026); https://aws.amazon.com/blogs/aws/try-the-new-console-experience-in-amazon-bedrock-optimized-for-anthropic-and-openai-compatible-apis/ (5 Jun 2026)

### 4.2 Amazon Bedrock Prompt management and prompt optimisation

Prompt management stores prompts as resources with variables, variants and versions. You edit a draft in the prompt builder, compare variants side by side (the comparison view holds 3), and create a version, which is a snapshot for production. Code calls a version by passing its ARN as the model ID to Converse or InvokeModel with values for the variables, or uses it in a prompt node in a Bedrock flow. This gives a team a reviewed, versioned prompt artefact outside the code base. A platform engineer controls who may change it. Traps: when you call a managed prompt through Converse you cannot also pass a system prompt, inference configuration, tool configuration or extra model fields; test values for variables are not saved. Two optimisers exist. Simple optimisation rewrites one short prompt (about 1,000 tokens or less) for one model. Advanced Prompt Optimization runs a loop driven by your evaluation: up to 10 prompt templates per job, up to 100 samples per template, up to 5 models, scored by a judge rubric, a Lambda function or plain-language criteria. It returns before and after prompts with scores, latency and cost estimates. Jobs can take from about 15 minutes to hours.
- Sources: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html ; .../prompt-management-test.html ; .../prompt-management-deploy.html ; .../prompt-management-optimize.html ; .../advanced-prompt-optimization-how.html (checked 2 Oct 2026)

### 4.3 Amazon Bedrock evaluations

Bedrock evaluations score models and retrieval sources as jobs. The kinds are: programmatic jobs with built-in or your own prompt datasets, jobs rated by human workers, jobs where a second model acts as judge and explains each score, and RAG evaluations of knowledge bases against ground truth. A judge job can also score answers you bring from a model outside Bedrock. Results show in the console and the full report lands in an S3 bucket you name. A QA lead owns the dataset and the metrics. An architect uses the report to pick a model. Traps: these jobs score single prompt and response pairs or retrieval, not multi-step agent traces (that is AgentCore Evaluations). Judge models are limited to a published list. Custom metrics have their own, different list.
- Sources: https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html (checked 2 Oct 2026)

### 4.4 Amazon Bedrock AgentCore (and Strands Agents)

AgentCore is AWS's set of services for running agents in production with any framework and any model. The overview lists: Harness (a managed agent loop set up by configuration, each session in its own microVM; generally available, built on Strands, with no separate charge), Runtime (serverless hosting for agents and tools with session isolation; supports Strands, LangGraph, CrewAI, LlamaIndex, Google ADK and OpenAI Agents SDK, and the MCP and A2A protocols), Memory (short and long term), Gateway (turns APIs and Lambda functions into MCP tools and connects existing MCP servers), Identity (works with existing identity providers), Code Interpreter, Browser, Observability (OpenTelemetry traces in CloudWatch), Evaluations (judge-based scoring of sessions, traces and spans from Strands or LangGraph agents, run online, on demand, in batch or on datasets, with built-in and custom evaluators), Optimization (recommendations for prompts and tool descriptions plus A/B tests through Gateway), Policy (rules checked at Gateway before every tool call, written in plain language or in a Cedar-compatible language), Registry (an approved catalogue of agents, MCP servers, tools and skills) and Payments (small payments by agents to paid endpoints). A platform engineer runs Runtime, Gateway, Identity and Policy. QA owns Evaluations. An architect uses Registry and Policy as the governance design. Limits: up to 1,000 evaluation configurations per region by default. The overview notes AgentCore may use and store your content to improve the service for your own use. Strands Agents is the open source SDK from AWS, in Python and TypeScript, for the agent loop, tools, MCP and multi-agent patterns, with an evaluation package (Strands Evals); its site lists AgentCore among its deployment targets.
- Sources: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html ; .../harness.html ; .../evaluations.html ; .../built-in-evaluators-overview.html ; https://strandsagents.com/ (checked 2 Oct 2026)

### 4.5 Kiro (spec-driven development, from AWS)

Kiro is an agentic development environment offered as an IDE, a CLI, a web agent, a mobile app in preview, and Kiro Crew. Its distinguishing feature is specs: for a feature it writes requirements.md (user stories with acceptance criteria), design.md and tasks.md, in that order or design first, and then runs the tasks, in parallel where they do not depend on each other. There is a bugfix spec type and a quick spec that skips the approval stops. Steering files in .kiro/steering (product.md, tech.md, structure.md) carry standing project knowledge, and AGENTS.md files are read too. Hooks, MCP, skills and custom agents are supported. A product manager reviews requirements.md. An architect reviews design.md. An engineer supervises tasks.md. QA takes acceptance criteria from the requirements file. Plans (summary only): Free at 0 dollars with 50 credits, Pro 20 dollars, Pro+ 40, Pro Max 100 and Power 200 per user per month, with extra credits at 0.04 dollars. Traps: every prompt in either mode spends credits and the rate depends on the model, so spec work on a large feature can use a month's credits quickly. The quick spec removes the human review points that are the reason to use specs.
- Sources: https://kiro.dev/docs/ (1 Oct 2026); https://kiro.dev/docs/specs/ (27 Aug 2026); https://kiro.dev/docs/steering/ (25 Sep 2026); https://kiro.dev/pricing/ (checked 2 Oct 2026)

### 4.6 GitHub Spec Kit

Spec Kit is GitHub's open source toolkit (MIT licence in the repository) that gives a coding agent a fixed process and templates. It is not tied to one agent. It needs Python 3.11 or later and uv. You install the specify CLI, run specify init with an integration key for your agent, then call skills in the agent's chat one at a time: /speckit-constitution once per project, then /speckit-specify, /speckit-plan, /speckit-tasks, /speckit-implement and /speckit-converge per feature, repeating implement and converge until it reports convergence. Two add-on processes are installed as extensions: bug fixing (assess, fix, test) and idea assessment, which ends in a go, clarify or stop decision. Artefacts are Markdown files under .specify/. A product manager writes and reviews the specification. An architect owns the constitution and the plan. QA uses the bug process's verdict as evidence. Traps: the skill names changed over time (older write-ups use a dot form such as /speckit.specify), and invocation differs by agent. Latest release seen: v1.0.13, 29 Sep 2026.
- Source: https://github.com/github/spec-kit (README read as raw text, checked 2 Oct 2026)

### 4.7 GitHub Copilot cloud agent (formerly coding agent)

A GitHub-hosted agent that researches a repository, plans, and makes changes on a branch in a short-lived environment run by GitHub Actions. It was renamed on 1 April 2026, when it also gained planning, repository research, and work on a branch without opening a pull request. Tasks come from the agents panel, by assigning an issue to Copilot, from Copilot Chat, from an @copilot comment on a pull request, or from integrations such as Slack, Teams, Jira and Linear. An engineer delegates a well-described issue and reviews the pull request. A platform engineer sets custom instructions, MCP servers, hooks and custom agents. Guard rails in the docs: only people with write access can start it; it pushes only to copilot/ branches or the pull request's branch; the person who asked for the pull request cannot approve it; Actions workflows wait for a person to approve the run; internet access is restricted; commits are signed and co-authored. Limits: one repository and one pull request per task, at most 59 minutes per session, GitHub-hosted repositories only. It is on all paid Copilot plans and uses Actions minutes and AI credits.
- Sources: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent ; https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations (checked 2 Oct 2026); https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/ (1 Apr 2026)

### 4.8 Cursor

Cursor is an AI code editor and coding agent with models from several providers. Rules give the agent standing instructions: project rules as files in .cursor/rules with front matter that says when each applies (always, when relevant, by file pattern, or on request), user rules, team rules set by an admin, and plain AGENTS.md files. Cloud agents run in isolated virtual machines, can be started from the desktop app, the web, iOS, Slack, GitHub, Linear or an API, work on their own branch across one or more repositories, and return a pull request with screenshots, video and logs. An engineer uses the editor agent for interactive work and cloud agents for parallel tasks. A tech lead owns the rules files in version control. Limits and traps: cloud agents need a paid plan, bill at the chosen model's API price, and need an admin to connect source control first. The docs advise keeping a rule under 500 lines. User rules apply only to the agent chat.
- Sources: https://cursor.com/docs ; https://cursor.com/docs/rules ; https://cursor.com/docs/cloud-agent (checked 2 Oct 2026)

### 4.9 Evaluation and prompt-testing tools

- promptfoo: an open source (MIT) command line tool and library for testing prompts, models and RAG pipelines, and for red-team scans. Tests are declared in a config file with test cases and assertions, run locally with promptfoo eval, and viewed with promptfoo view. It fits CI well. An engineer or QA lead keeps the test file next to the code and fails the build on regressions. A security reviewer runs the red-team scan before release. Note: promptfoo announced on 9 March 2026 that it had agreed to be acquired by OpenAI; the repository says it stays open source and MIT licensed. Sources: https://www.promptfoo.dev/docs/intro/ ; https://github.com/promptfoo/promptfoo ; https://www.promptfoo.dev/blog/promptfoo-joining-openai/ (checked 2 Oct 2026)
- Braintrust: a hosted platform for evaluation and observability. An evaluation has three parts: data, a task, and scorers (built-in, model judge or code). Playgrounds are for quick trials, experiments are fixed snapshots to compare, CI runs them on changes, and online scoring grades production traces. A QA lead owns datasets and scorers. A product manager reads experiment comparisons. Self-hosting the data plane is for the Enterprise plan only. Sources: https://www.braintrust.dev/docs ; https://www.braintrust.dev/docs/evaluate ; https://www.braintrust.dev/docs/admin/self-hosting (checked 2 Oct 2026)
- LangSmith: LangChain's platform for tracing, evaluation, prompt engineering and deployment. It works with many frameworks and providers, not only LangChain. Offline evaluation uses datasets, evaluators (human, code, model judge, pairwise) and experiments. Online evaluators grade live traces with sampling. Cloud, hybrid and self-hosted options exist. An engineer reads traces to debug an agent run. QA builds datasets from failed production traces. Sources: https://docs.langchain.com/langsmith/home ; https://docs.langchain.com/langsmith/evaluation (checked 2 Oct 2026)
- Langfuse: an open source platform (MIT, except its enterprise folders) for tracing, prompt management with versions, evaluation, datasets and a playground. It is built on OpenTelemetry and can be self-hosted with Docker Compose, Kubernetes or Terraform, or used as a cloud service. Its repository says it became part of ClickHouse in January 2026. It suits a platform team that must keep traces in its own account. Sources: https://langfuse.com/docs ; https://github.com/langfuse/langfuse (checked 2 Oct 2026)

How they differ in one line each: promptfoo is a test file run in CI; Braintrust is experiments and scoring as a hosted service; LangSmith is tracing first with evaluation built on traces; Langfuse is the self-hostable open source option. On AWS, AgentCore Evaluations and Bedrock evaluations cover the same ground natively.

---

## 5. The Gemini model line-up (Gemini API models page, dated 1 Oct 2026)

Names and model codes were read from the raw page text.

Stable, general text and reasoning:
- Gemini 3.8 Flash (gemini-3.8-flash): the current top Flash model, aimed at long software tasks, agents and complex business workflows. Input limit 1,048,576 tokens, output 65,536. Generally available since 2 Sep 2026.
- Gemini 3.7 Flash (gemini-3.7-flash): previous generation, for coding and multi-step agent work.
- Gemini 3.6 Flash (gemini-3.6-flash): previous generation, a balance of speed and multimodal ability for everyday tasks.
- Gemini 3.5 Flash (gemini-3.5-flash): labelled legacy; baseline speed for routine high-volume work.
- Gemini 3.5 Flash-Lite (gemini-3.5-flash-lite): the fastest and cheapest 3.5 model, for high throughput.
- Gemini 3.1 Flash-Lite (gemini-3.1-flash-lite): older low-cost model; shutdown announced for 7 May 2027.

Preview:
- Gemini 3.1 Pro (gemini-3.1-pro-preview): the Pro model for hard reasoning and agentic coding. It is still in preview and has no free API tier. The page lists no stable Pro text model in the 3.x family (Nano Banana Pro is an image model).
- Gemini 3 Flash (gemini-3-flash-preview): earlier Flash preview.
- Gemini 3.5 Live Translate (gemini-3.5-live-translate-preview): real time speech to speech translation.
- Gemini Omni Flash (gemini-omni-1.1-flash): video generation and editing with audio. The models page lists it under Preview, while the changelog records general availability on 27 Aug 2026.

Voice and audio:
- Gemini 3.8 Live (gemini-3.8-live): default Live API model for low latency voice agents.
- Gemini 3.8 Live Extended Thinking (gemini-3.8-live-extended-thinking): Live model for when more reasoning is needed during the conversation.
- Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS: text to speech, the first for quality, the second for volume and cost.
- Gemini 3.5 Transcribe (gemini-3.5-transcribe and gemini-3.5-transcribe-live): speech to text with speaker labels and timestamps.
- Gemini 3.1 Flash Live and Gemini 3.1 Flash TTS: legacy previews; the page says to move to the 3.8 models.

Images, video and music:
- Nano Banana 2 (gemini-3.1-flash-image), Nano Banana 2 Lite (gemini-3.1-flash-lite-image), Nano Banana Pro (gemini-3-pro-image): image generation and editing at three speed and quality points.
- Veo 3.1 and Veo 3.1 Lite (preview): video generation. The deprecations page gives 22 Oct 2026 as the shutdown date for Veo 3.1 preview models, with Gemini Omni Flash as the replacement (summary only).
- Lyria 3.5 (stable), Lyria 3 Clip and Lyria 3 Pro (preview), Lyria RealTime (experimental): music generation.

Agents and special tasks:
- Antigravity Agent (antigravity-preview-09-2026): a managed general agent that plans, runs code, manages files and browses inside a sandbox. Preview.
- Gemini Deep Research and Deep Research Max (preview): multi-step research with cited reports.
- Gemini Embedding 2 (gemini-embedding-2-preview on the models page) and Gemini Embedding (gemini-embedding-001): embeddings for search and RAG.
- Gemini Robotics ER 2 and ER 1.6 (preview): reasoning for robots.

Older families:
- Gemini 2.5 Flash, 2.5 Flash-Lite and 2.5 Pro are still served but limited to accounts that already used them. New projects are told to use 3.5 Flash-Lite or 3.8 Flash.
- Shut down: Gemini 2.0 Flash and Flash-Lite (1 Jun 2026), Gemini 3 Pro Preview, Gemini 3.1 Flash-Lite Preview, the Gemini 2.5 Computer Use model, and Imagen 4.

API note: the Interactions API became generally available in June 2026 and is the recommended interface for new projects. generateContent is called legacy but is still supported.

- Sources: https://ai.google.dev/gemini-api/docs/models (1 Oct 2026); https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ; https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview (18 Aug 2026); https://ai.google.dev/gemini-api/docs/changelog ; https://ai.google.dev/gemini-api/docs/deprecations (1 Oct 2026); https://ai.google.dev/gemini-api/docs/interactions-overview (1 Oct 2026)

---

## Things I could not verify

1. Where AI Studio stores saved prompts. Forum posts on discuss.ai.google.dev say Google Drive, but no docs page opened in this session says so.
2. Whether AI Studio's Compare button and behaviour in October 2026 match the October 2024 blog post, and whether it compares more than two models or different settings.
3. Which languages the Get code button offers.
4. Screen sharing and webcam input in the AI Studio real time screen. Only forum posts describe it.
5. The actual free tier numbers for AI Studio and the API (requests per minute and per day by model). Google publishes them only inside AI Studio.
6. Which model Jules uses today. The limits page and the changelog disagree with the current model list, and the changelog stops at 9 March 2026.
7. Whether Antigravity CLI is open source, and its exact quotas.
8. Which Agent Platform components are generally available and which are preview.
9. ADK version numbers per language, beyond the TypeScript 2.0 notice.
10. The Antigravity plan details, Kiro prices and model names, Notebook limits, Braintrust and LangSmith hosting details, and the Veo shutdown date were seen only through a page summary, not raw text. Treat the numbers as needing a second look before print.
11. The licence of Strands Agents, and the location of Kiro spec files (.kiro/specs), were not confirmed on a page.
12. The current state of the Amazon Bedrock classic console playground (modes, compare, metrics). The user guide page is now a stub.
13. The names of AgentCore's built-in evaluators beyond Builtin.Helpfulness, and AgentCore pricing.
14. Cursor plan names and prices, and its Bugbot review product, were not checked.
15. Status of Android Studio Agent Mode (stable or preview) was unclear on the page.

## Sources used

Google AI Studio and Gemini API
- https://ai.google.dev/gemini-api/docs/ai-studio-quickstart
- https://ai.google.dev/gemini-api/docs/aistudio-build-mode
- https://ai.google.dev/gemini-api/docs/aistudio-deploying
- https://ai.google.dev/gemini-api/docs/aistudio-agents
- https://ai.google.dev/gemini-api/docs/google-ai-plans
- https://ai.google.dev/gemini-api/docs/workspace
- https://ai.google.dev/gemini-api/docs/troubleshoot-ai-studio
- https://ai.google.dev/gemini-api/docs/structured-output
- https://ai.google.dev/gemini-api/docs/google-search
- https://ai.google.dev/gemini-api/docs/code-execution
- https://ai.google.dev/gemini-api/docs/url-context
- https://ai.google.dev/gemini-api/docs/live
- https://ai.google.dev/gemini-api/docs/live-api/session-management
- https://ai.google.dev/gemini-api/docs/antigravity-agent
- https://ai.google.dev/gemini-api/docs/managed-agents-quickstart
- https://ai.google.dev/gemini-api/docs/interactions-overview
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview
- https://ai.google.dev/gemini-api/docs/changelog
- https://ai.google.dev/gemini-api/docs/deprecations
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://ai.google.dev/gemini-api/terms
- https://developers.googleblog.com/compare-mode-in-google-ai-studio/

Jules
- https://jules.google/
- https://jules.google/docs/
- https://jules.google/docs/running-tasks/
- https://jules.google/docs/review-plan/
- https://jules.google/docs/environment/
- https://jules.google/docs/usage-limits/
- https://jules.google/docs/faq/
- https://jules.google/docs/cli/reference/
- https://jules.google/docs/changelog/
- https://developers.google.com/jules/api

Gemini CLI, Antigravity, IDE tools, Firebase Studio
- https://github.com/google-gemini/gemini-cli
- https://geminicli.com/docs/
- https://geminicli.com/docs/resources/quota-and-pricing/
- https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli
- https://antigravity.google/docs/getting-started
- https://antigravity.google/docs/overview/
- https://antigravity.google/docs/cli/overview/
- https://antigravity.google/docs/cli/install/
- https://antigravity.google/docs/models/
- https://antigravity.google/docs/plans/
- https://developers.google.com/gemini-code-assist/docs/overview
- https://docs.cloud.google.com/gemini/docs/codeassist/overview
- https://developer.android.com/studio/gemini/overview
- https://developer.android.com/studio/gemini/agent-mode
- https://firebase.google.com/docs/studio

Gemini Notebook, Agent Platform, ADK
- https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/
- https://support.google.com/notebooklm/answer/16164461
- https://support.google.com/notebooklm/answer/16213268
- https://support.google.com/notebooklm/answer/16269187
- https://support.google.com/notebooklm/answer/15724963
- https://support.google.com/gemininotebook/answer/17004255
- https://docs.cloud.google.com/agent-builder/overview
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/vertex-ai-name-changes
- https://cloud.google.com/products/gemini-enterprise-agent-platform
- https://adk.dev/
- https://adk.dev/get-started/about/

AWS
- https://docs.aws.amazon.com/bedrock/latest/userguide/playgrounds.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started-console.html
- https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/bedrock-explore-chat-playground.html
- https://aws.amazon.com/blogs/aws/try-the-new-console-experience-in-amazon-bedrock-optimized-for-anthropic-and-openai-compatible-apis/
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-test.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-deploy.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-optimize.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompt-optimization-how.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-evaluators-overview.html
- https://strandsagents.com/
- https://kiro.dev/docs/
- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/steering/
- https://kiro.dev/pricing/

GitHub, Cursor, evaluation tools
- https://github.com/github/spec-kit
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
- https://github.blog/changelog/2026-04-01-research-plan-and-code-with-copilot-cloud-agent/
- https://cursor.com/docs
- https://cursor.com/docs/rules
- https://cursor.com/docs/cloud-agent
- https://www.promptfoo.dev/docs/intro/
- https://github.com/promptfoo/promptfoo
- https://www.promptfoo.dev/blog/promptfoo-joining-openai/
- https://www.braintrust.dev/docs
- https://www.braintrust.dev/docs/evaluate
- https://www.braintrust.dev/docs/admin/self-hosting
- https://docs.langchain.com/langsmith/home
- https://docs.langchain.com/langsmith/evaluation
- https://langfuse.com/docs
- https://github.com/langfuse/langfuse

Pages opened that gave nothing usable: https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview and https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes (navigation only through the fetch tool); https://strandsagents.com/latest/ (404).
