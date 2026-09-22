# Changelog

Notable changes to this curriculum. Dates are when the change landed on `main`.

The format is loosely [Keep a Changelog](https://keepachangelog.com/). This is teaching material rather
than a released library, so there are no semantic versions — but breaking changes to structure are called
out, because people bookmark deep links.

---

## 2026-09-22 · The site becomes a manual you enter by role

### Changed
- **The site is rebuilt around roles.** It was one enormous document whose front door opened into the
  middle of a story. Now home picks a role, each role is its own page, and the simulator moves to
  [`/simulator/`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/) with a pristine copy at `/app/` whose bytes are verified unchanged
  at every build
- Old deep links of the form `.../#/toolkit/cache` — 44 of them in this repo, plus bookmarks — are
  **forwarded** to the simulator before the page renders, rather than broken

### Added
- **Five role journeys**, forty steps, **264 sub-steps**. Each role gets its own arc, because the shape
  of the work differs: [PM](https://akash-coded.github.io/aws-bedrock-agentcore-strands/product-manager/) Discover→Learn, [architect](https://akash-coded.github.io/aws-bedrock-agentcore-strands/solution-architect/)
  Elicit→Evolve, [engineering](https://akash-coded.github.io/aws-bedrock-agentcore-strands/engineering/) Prepare→Operate, [QA](https://akash-coded.github.io/aws-bedrock-agentcore-strands/qa/) Define→Watch,
  [DevOps](https://akash-coded.github.io/aws-bedrock-agentcore-strands/devops/) Baseline→Recover
- At **every** step: the sub-steps, where a model helps and the one thing not to delegate, the artefact,
  a fill-in template, copy-paste prompts, a worked SkyWays example, three pitfalls and a testable done-when
- **[40 templates](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/)** and **[116 prompts](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/)**, each with a copy button,
  also collected on their own pages
- **[Frameworks and acronyms](https://akash-coded.github.io/aws-bedrock-agentcore-strands/frameworks/)** — four named methods side by side, an acronym decoder,
  every framework with its lineage and confidence mark, and three inline SVG diagrams
- **DevOps and platform** is new material: the platform baseline, model access as a lead-time item,
  CI for a system that is right a share of the time, and rolling back a prompt
- Five **[reading copies](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Journey-Product-Manager)** on the wiki, generated from the same content
  so the two cannot drift

### How it is built
Content is JSON authored in Python under [`site/content/roles/`](site/content/roles/), rendered to
static HTML by [`render.py`](site/render.py) and to wiki markdown by
[`wiki_export.py`](site/wiki_export.py). The build fails on a missing field, a duplicate id, a gap in
the numbering, an empty template — and on any `python`, `json` or `yaml` template that does not parse.

---

## 2026-09-22 · The operating playbook, and a wiki that teaches it

### Changed
- **[The SkyWays playbook](https://akash-coded.github.io/aws-bedrock-agentcore-strands/)** replaces the architect's demo on GitHub Pages. Fifteen pages in place
  of five: thirteen dated episodes, a loop map, nine simulations, seventeen calculators, a governance
  section, an evidence pack and a concept map of 55 ideas. The tool is published byte-for-byte from
  [`site/app/`](site/app/) as before, and the build still refuses if its bytes change
- Site metadata, the social image and the README screenshot follow the new title; the frame's attribution
  line now takes the tool's name from [`site/frame/config.js`](site/frame/config.js)

### Added — the playbook as a wiki
Twenty-three new [wiki](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki) pages carrying the same method in writing, with mermaid diagrams,
decision trees, worked arithmetic and exercises with answers:

- **The spine** — [The Agentic PDLC](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Agentic-PDLC), [The Eight Loops](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Eight-Loops),
  [Gates and Governance](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Gates-and-Governance), [The Evidence Pack](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/The-Evidence-Pack)
- **Five role pages**, eighteen steps each — [product manager](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Product-Manager),
  [solution architect](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Solution-Architect), [engineering lead](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Engineering-Lead),
  [QA lead](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-QA-Lead) and a new [sponsor](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Role-Sponsor) page for whoever signs the budget
- **Nine how-tos** — [NFR workshop](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Run-an-NFR-Workshop),
  [agent on paper](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Design-an-Agent-on-Paper),
  [build, buy or borrow](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Choose-Build-Buy-or-Borrow),
  [bolts](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Cut-Sprints-into-Bolts), [review by risk band](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Review-by-Risk-Band),
  [prove the bar](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Prove-the-Bar), [the token bill](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Control-the-Token-Bill),
  [the security boundary](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Hold-the-Security-Boundary),
  [the missing-control postmortem](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/How-to-Run-a-Missing-Control-Postmortem)
- **Reference** — [Playbook Glossary](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Playbook-Glossary),
  [Formulas and Calculators](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators) with every formula worked,
  [eleven Decision Trees](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Decision-Trees), [Anti-Patterns](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Anti-Patterns),
  [Sources and Confidence](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Sources-and-Confidence)
- **[Scenario Library](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scenario-Library)** — the thirteen SkyWays episodes plus **twenty-four cases**
  from healthcare, banking, insurance, retail, logistics, manufacturing, telecoms, energy, the public sector
  and an internal helpdesk, grouped by the loop each one exercises, so the method can be tested against a
  change of domain. One of them exists to show the playbook losing: a helpdesk where most of its ceremony is
  the wrong answer
- **[24 exercises with worked answers](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Exercises-and-Answers)**, including five interview questions
- A **method-first study plan** — one week, no code, no AWS account — in [Study Plans](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Study-Plans)

Every figure carries a confidence mark: **documented** (a vendor's published documentation, dated),
**established** (a named, published practice) or **working method** (this playbook's own default, to tune).

---

## 2026-09-04 · SkyWays Architect on GitHub Pages

### Added
- **[SkyWays Architect](https://akash-coded.github.io/aws-bedrock-agentcore-strands/)** now lives on the project site: the agentic PDLC as an interactive
  simulator — six architect decisions, thirty-eight scenarios, role deep dives P0 to P3. The tool is published
  byte-for-byte from [`site/app/`](site/app/); [`site/build.py`](site/build.py) layers attribution, the licence
  and disclaimer, the ideas invitation and a contact form around it at build time, and refuses to build if the
  tool's own bytes changed
- A **contact form** with three delivery modes: the visitor's mail app (default, nothing to configure), the
  [contact relay](site/contact-relay/) — Lambda Function URL, DynamoDB, SES and a private GitHub mirror, as
  CloudFormation with offline tests — or a hosted form service
- **Ideas thread** [#101](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101) as the open door for suggestions, corrections and disagreements
- A private `akash-coded/inbox` repository where mirrored messages become issues, one per message
- `Pages` workflow: builds and deploys on every push that touches `site/`; a frameless copy of the tool is
  served at [`app/SkyWays-Architect.html`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html)

### Also
- **Discussions pinned** to GitHub's maximum of four, one per job: the
  [discussion map](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/65) (where to
  post what), the [exercise and lab index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64)
  (find content), the [Simulator Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75)
  (do something) and the [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101)
  (contribute). Release notes gave up its slot to the Arena; the changelog already carries it. The ideas
  thread is renamed for the new tool

### Needs your hands
- The relay is not deployed. Run `site/contact-relay/deploy.sh` in your own AWS account, click the SES
  verification link, paste the Function URL into `site/frame/config.js`. Until then the form opens the
  visitor's mail app, which works everywhere

---

## 2026-09-02 · Drills, assignments, and the boards that read the Arena

### Added
- **`/leaderboard`**, **`/progress`**, and a **weekly digest** posted to Announcements — all built from the ledger
- **Drills** — nineteen bite-sized, bot-graded items under `labs/drills/` in two laps in four kinds (implement, fix, blank,
  predict), chained across every track and ending at the first full lab
- **Skill-aware replies** — each Arena reply names the skill demonstrated, what to read, and the next item;
  misses get the drill's own diagnosis and one nudge, written per drill
- **`/assign`** for maintainers, with per-learner briefs and tracked assignments
- **A ledger in every bot reply**, making Discussions the source of truth for attempts
- **A live [Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard) wiki page**, rebuilt every six hours and after every Arena run
- Boards: **Hands-on Tracker** (#9), **Repo Pulse** (#10), and **Agentic PDLC · Lifecycle Reference** (#8)
- **Codespaces**: one-click environment, `lab` command with completion, VS Code tasks, welcome page
- `labctl grade --json` and drill support in the runner and `verify`
- Four runnable public gists: the [history invariant](https://gist.github.com/akash-coded/12cd36b5e5ced3e0c5414af3abffa221), an [honest tool result](https://gist.github.com/akash-coded/e3748d8f0accfedf0a2509ee16195d51), a [release gate](https://gist.github.com/akash-coded/908a2f096a89de29d3b3221244773a1b), and an [H× calculator](https://gist.github.com/akash-coded/407c5e9ddcca84afe7099439591d3ec2)

### Needs a secret
- The two live boards are synced only when `PROJECT_TOKEN` exists — a **classic** PAT with the `project`
  scope, because neither `GITHUB_TOKEN` nor a fine-grained PAT can access user-owned Projects v2.
  [Setup](docs/setup/project-token.md). The scoreboard works without it.

## 2026-09-01 · The field guide

### Added
- **[Field guide](cheatsheets/)** — 77 reference pages
  - 17 original frameworks with a procedure and an output: Autonomy Ladder, Token Tax Ledger, Handoff
    Multiplier, Abstention Budget, Grounding Triangle, Blast Radius Grid, Evidence Ladder, Failure
    Signature Catalog, Cost Cliff Map, Silent Degradation Watchlist, Context Budget Ledger, Three Clocks,
    Tool Surface Audit, Reversibility Test, Demo-to-Production Gap, Scope Fence, Value Trace, and the
    Agent Readiness Scorecard that composes them
  - 10 quick-reference sheets: Converse API, Strands, LangChain/LangGraph, AgentCore, RAG, IAM,
    observability, model selection, MCP/A2A, prompting
  - 9 runbooks for incidents and operations
  - 4 strategic playbooks
  - 6 interview guides, both sides of the table
  - 17 role-based how-tos across engineers, PMs, architects, business analysts, QA and engineering managers
- **[Extension roadmap](docs/extension-roadmap.md)** and its [public board](https://github.com/users/akash-coded/projects/6) — five phases, 22 specified items
- Index pages for `modules/`, `docs/`, `projects/`, `docs/concepts/`, `docs/setup/`, `docs/reference/`
- Every module README now links the field-guide pages relevant to it
- Social preview image, and its source
- `freshness.yml` — weekly link check that opens an issue when something rots
- `welcome.yml` — first-time contributor guidance
- `NOTICE.md` — third-party attribution

### Fixed
- **Licence.** The restructure commit had overwritten `LICENSE` with an MIT-0 file copied from a bundled
  AWS sample, wrongly attributing copyright to Amazon. The project's own MIT licence is restored.
- `bedrock-agentcore` moved from a pinned `==1.14.0` to a patched `>=1.18.1` floor across four requirements
  files; `mcp` lockfile bumped. Cleared 6 high-severity advisories.
- CI runs on Python 3.12 — the notebook-generator scripts under `labs/rag-labs/build/` use 3.12 f-string
  syntax. The labs themselves still run on 3.11.

---

## 2026-09-01 · Restructure

### Changed — **breaking for deep links**
- 118 flat root files reorganised into **16 topic modules** under `modules/`, each with
  `slides/ notebooks/ exercises/ solutions/ activities/ src/`. Any link to a root-level file from before
  this date will 404 — the [curriculum index](modules/) is the place to re-find things.

### Added
- ~200 previously unpublished files imported from the source material: **every exercise solution**, all of
  Module 04 (Agent Builder), Module 09 (LLM memory), Module 14 (end-to-end production), the full
  [`ragkit`](modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit/) retrieval library, and the Module
  07/08/10 exercise and solution sets
- `docs/` — START-HERE, 5 learning paths, architecture HLD plus 16 per-module LLDs, portable-vs-AWS
  concept maps, 7 sample PRDs, setup and troubleshooting guides
- README with the curriculum map and reference architecture
- `CONTRIBUTING`, `CODE_OF_CONDUCT`, `SECURITY`, `CITATION.cff`, `.gitignore`, `requirements.txt`
- Issue, PR and discussion templates; `validate.yml` CI

### Removed
- Client branding from filenames, markdown, notebooks and the XML inside 31 PowerPoint/Excel files
- A real AWS account ID (replaced with the placeholder `123456789012`)
- Leaked local filesystem paths (replaced with `/workspace/`)
- AgentCore deploy logs, traces, a vendored 5,300-file dependency cache, and build output

---

## Before 2026-09-01

61 commits of course material published as it was delivered across three professional cohorts. Preserved
in history; the file layout from that period no longer exists on `main`.
