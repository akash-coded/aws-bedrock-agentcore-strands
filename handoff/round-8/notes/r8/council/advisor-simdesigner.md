# Advisor: the learning and simulation designer

## Q1. The simulations

**Verdict.** Ninety Days teaches trade-offs but puts no prompt, reply or document in the player's hands. Keep it as the story mode. Build **Labs** beside it at `/labs/`: ten minutes each, one artefact made by hand, one trap sprung.

**Ninety Days.** Keep the game and every link. The title's h1 becomes "Run a ninety-day AI project in thirteen decisions", with "Ninety Days" as the eyebrow. Heads name every noun: "Day 4. Six stakeholders must approve the merged requirements list. None has read it." Each day links to its lab.

**One engine, many scripts.** `lab.js` plays one JSON script per lab, loaded only on that lab's page. The screen is a desk of three panes (tabs on a phone): the brief and what is on file, the tool, the artefact growing. A script is a list of beats, of seven kinds:

1. `compose`: build a prompt from blocks (role, context, limits, examples, format).
2. `run`: show the saved reply for that combination.
3. `mark`: click the lines that are wrong or guessed. This is the practice; a lab without one is refused.
4. `fix`: choose or type the correction.
5. `grid`: prompt versions against cases.
6. `zoom`: step into a diagram.
7. `file`: the artefact joins the pack (`localStorage`, markdown download) and the next lab opens with it. Opened cold, a lab loads the by-the-book artefact and says so.

Saves replay the action list, as the game does. The trap is the game's rule, smaller: the tempting choice looks fine and is quoted back two beats later.

**An honest prompt run.** Every reply is a real capture, stamped: "Saved reply. Tool, model, date. Yours will differ." Beside it: "Copy the prompt and run it". No typing effect, no fake wait. The build refuses a run without model and date.

**Diagrams.** One SVG, three nested levels. A click on a box eases the viewBox in 400ms, from context to HLD to LLD. Missing parts are placed by two taps, never dragged. Its text source sits beside it: text is what a model reads.

**Documents.** One document with version chips: PRD-lite, PRD, eight-field spec, agent spec. Format is taught at the hand-off to the agent: the same spec as prose, as markdown, and as a context file plus spec plus tasks. The player runs one agent task on each and marks what the agent misread.

**The set.** Each uses what the last one filed.

| Lab | For, phase | Hands do | Tool shown | Leaves with | Trap |
|---|---|---|---|---|---|
| 1 One line with numbers | PM, P0 | Merge six transcripts, mark lost names | Chat with a project | Pain register | The model ranks by vividness |
| 2 Grow the spec | PM, SA, P1 | Shard the PRD, mark guessed fields, pick a format | Chat, spec files | Eight-field spec | Plausible defaults pass as decisions |
| 3 Three heights | SA, P1 | Zoom context, HLD, LLD; place parts | Diagram as text | Diagrams, authority budget | The $400 limit drawn in the prompt |
| 4 Prompt bench | Eng, QA, P1 to P2 | Three system prompts on twelve cases | Model playground | Prompt, config card, twenty cases | Tuned cases pass, held-out cases fail |
| 5 Brief the coding agent | Eng, P2 | Write the context file, review plan and diff | Terminal agent | Story file, reviewed diff | The agent edits the test to pass |
| 6 Read the score | QA, P2 | Split 82.4 by kind | Eval report | Sign-off readout | The average hides a kind of case |
| 7 Find the leak | DevOps, P3 | Read the call log | Trace, bill | Routing config | Buying a cheaper model first |
| 8 Two numbers | Sponsor, P3 | Build the slide | Sheet | Report, next brief | Leaving the cost off |

**First three.** Lab 2: its content is already in `product-manager.json` and it needs four beat kinds, so it proves the engine. Lab 4 adds the grid. Lab 3 adds zoom. Labs 6 to 8 are the game's own tasks, lifted later.

## Q2. Tool fluency

Both; the weight sits in the labs. Teach the job, never the menu.

- **In a lab:** one tool card per beat: why this tool here, one professional habit ("plan before edit"), the parallel elsewhere.
- **`/tools/`:** one matrix. Rows are jobs (draft, hold knowledge, test a prompt, build in a repo, hand off, browse, schedule). Columns are Claude, ChatGPT and Codex, Google.
- **Four manuals:** Claude (chat, projects, skills, connectors, scheduled tasks); Claude Code (terminal, VS Code, remote, Chrome); ChatGPT and Codex; Google AI Studio. Each: five jobs in P0 to P3 with a SkyWays example and its prompt, a ten-minute setup, three traps.
- **Mention only:** Jules, Cursor, Copilot, Kiro, Spec Kit, NotebookLM.
- **Staying true:** every fact lives in `content/tools/tools.json` with its source link and the date checked. Cards and manuals render from it. Past sixty days a page shows "Last checked" in amber and the build warns. No vendor screenshots.

## Q3. Leadership

Thirteen sections, fourteen screens, three making one argument. Its best things (the pass-mark slider, the net-value sliders, the six-control check) start on screen ten. Five sections: the four decisions on the first screen, each with its control; the four questions and the report; the control check; thirty days as a timeline; seven escalations to copy. Move the teams table and role cards to the role pages, frameworks to its page, effort levels to `/tools/`.

## Q4. Home

Keep the table. Let each row open: built for, strong at, silent on, with silent phases hatched and the unanswered question written in the gap. Borrow the frameworks page's per-phase "what each gives". One line above: any method works; four decisions remain yours.

## Q5. Lessons and sketches

A fault: `lesson-dark-1440-04` and `-06` print a diagram's text fallback as a numbered list with a 600px question mark. Layout: contents and a "try it" card go in the right margin; sketches sit there at 280px beside their paragraph. A sketch survives only if it holds the case's own object and number (the ladder at $400, the snowball at 4.4). Pure metaphor goes. Perhaps thirty survive (one sheet judged).

## Q6. Personality

A senior colleague who ran this project and shows the paperwork.  
Voice: exact, dated, admits the cost.  
Look: an operations desk: stamps, dates, "on file".  
Rose: only what is owed.  
Show first: lab stamps, numbered headlines, the pack.

## Q7. Order and risk

1. Faults and the game's words. 2. Leadership. 3. Engine and Lab 2. 4. Lab 4, `tools.json`, two manuals. 5. Lab 3. 6. Home rows. 7. Lesson margin and sketch cull. Later: Labs 1 and 5 to 8.

Risks: labs without a `mark` beat become slideshows; tool facts go stale; eight apps instead of one engine.
