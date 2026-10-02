# The practitioner

**Decision.** One "bench" engine, seven labs that pass files on, Ninety Days kept as the story. Refuse: a prompt box that pretends to judge typing, typing effects, hand-written replies, printed prices or limits.

## Q1. The simulations

**One engine.** Three panes: files on hand; the tool (chat, playground, terminal, canvas); the artefact growing, changes marked. A lab is a JSON script of six step kinds: assemble a prompt from parts, run, mark the faulty line in the reply, choose, accept or reject an edit, zoom. Files persist in localStorage; a lab opened cold loads them as `sim.book` does.

**An honest run.** Every reply is real, recorded when the lab was written, stamped "Recorded reply, model, date. Yours will differ." "Run again" shows a second recording that differs.

1. **Frame the pain** (PM, P0, a Claude Project). Load two transcripts and a ticket export, choose a prompt, run, mark the number with no source line. Leaves the pain line (38 minutes, $9.40 a case) and a PRD-lite. Trap: a fluent number nobody can trace.
2. **Grow the spec** (PM, architect, P1, chat). Have the model interview you one question at a time, park open questions with owners, then compare one requirement as prose, as markdown with stable ids and as spec-kit files, and see which a coding agent reads correctly. Leaves `spec.md`. Trap: a gap the model filled silently.
3. **Draw the system** (architect, P1, diagrams from code). Ask for a context diagram in Mermaid, mark the invented box and the missing actor, zoom to the HLD, tag steps exact, best guess or consequential, zoom to the LLD, move the $400 limit into the tool. One SVG, three levels; a click moves the viewBox. Leaves `architecture.md`. Trap: a diagram never checked against the spec.
4. **Write the system prompt** (engineer, P1 to P2, a playground). Assemble v1 from parts (role, tagged context, examples, output shape, what to do when unsure), run eight probe cases, read the grid, make v2 and v3, choose model tier and settings from it. Leaves `system-prompt.md` and a config card. Trap: v3 fixes case 5 and breaks case 2.
5. **Build the golden set** (QA, P1 to P2, an eval runner). Sort cases into three kinds, write the rubric, check a model judge against twenty human labels, read each kind's lower bound. Leaves the set and pass marks. Trap: the average hides 79.1.
6. **Build one slice** (engineer, P2, Claude Code). Write the memory file from the spec, demand a plan before edits, read the diff, find the test the agent weakened to go green, give the diff to a second agent with fresh context. Leaves a reviewed change. Trap: "done" claimed, not shown.
7. **Read the bill** (platform lead, P3, a scheduled headless run). Find the four habits behind 4.4 times, schedule a drift check, catch a passenger note saying "ignore the limit". Leaves the two-number report. Trap: whatever the agent reads can instruct it.

**First three: 4, 2, 3.** The owner named all three; lab 4 uses every step kind, so it proves the engine.

**Ninety Days** stays as the story. `/simulator/` opens on "Run a ninety-day AI project. You make the calls.", labs beneath. Each day links to its lab. Heads name their nouns: "Day 4. Six stakeholders must agree to one list of requirements. None has read it yet."

## Q2. Tool fluency

Both.

1. **A tool card inside a lab**, when the tool is picked up: what it is, why here, two features in use, the other vendors' equivalent, date checked, source.
2. **One map, `/tools/`**, phases across, roles down:
   - **P0.** PM: a chat project holding transcripts and exports; deep research for prior art; a connector to the ticket system.
   - **P1.** PM: chat, the document in a side canvas. Architect: chat that renders diagrams from code; a coding agent to read the old booking system first. Engineer: a playground (Anthropic Console, Google AI Studio, OpenAI) for prompt versions side by side. QA: a spreadsheet, then an eval runner.
   - **P2.** Engineer: Claude Code or Codex in terminal and editor; Jules or a cloud session for unattended chores; a browser agent to test the contact centre screen. QA: evals headless in CI.
   - **P3.** Platform: a scheduled headless run for drift and the weekly bill; connectors to logs. Everyone: chat to draft the postmortem from the trace.
3. **Four manuals:** Claude (chat, Projects, Skills, connectors, scheduled tasks); Claude Code (terminal, VS Code, web, remote, Chrome); ChatGPT and Codex; Google AI Studio and Jules. Mention only: Cursor, Copilot, Kiro, Spec Kit, promptfoo, Bedrock. Each, in 1,200 words: five jobs from the case with the real prompt, what the tool is poor at, three settings that matter (memory file, permissions, context), its traps.

**Staying true.** Every tool fact lives in one `tools.json` with a source link and a checked date; the build warns at sixty days. Link to prices, limits and model names; never print them. Every surface named above moves monthly: each must be checked against the vendor's documentation before publishing.

## Q3. Leadership

Fifteen headings, both controls buried past section eight (`protocol-dark-1440-03`, `-11`). First screen: title, one sentence, and the four decisions only she can make as four cards, each with "ask for" and "a healthy answer". Then the six-control check, the money sliders, the first thirty days, the seven escalations. Move the teams table, who does what and changed against unchanged to `/method/`; both tooling sections to `/tools/`.

## Q4. Home

Keep the table. Write in each bar the artefact that method makes you produce, and in each gap what is missing ("no pass mark"), so the manual's row sits under the gaps it fills. A row opens to the frameworks page's "merged, not stacked" cells.

## Q5. Lessons

Fix first: at 1440 the hard gate lesson prints its diagram twice, once as a list with 600px icons (`lesson-dark-1440-03`, `-07`). Right column: a sticky margin holding the template, the prompt and the lab. A sketch survives only if it draws the case's own object with its number (the $400 limit, the 4.4 snowball), at margin size.

## Q6. Personality

A senior colleague's working notebook. Voice: says what went wrong, with the number. Look: real files, marked changes, dates. Shows first on the bench, in the lesson margin, in the home table.

## Q7. Order and risk

Bugs and cold headings; the engine with lab 4; labs 2 and 3; `/tools/` and both Claude manuals; Leadership; home; lessons. Later: the other labs and manuals, lab results feeding the game. Risks: recorded runs that feel fake; tool facts that rot; seven apps instead of one engine.
