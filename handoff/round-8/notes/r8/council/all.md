# Council 7: the five advisors' answers, anonymised


---

# Response A

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


---

# Response B

I opened every screenshot named and all seven sketch sheets, and took fresh shots of `/learn/p0-frame/` at three widths (`SP/r8/infodesign/`). The brief's lesson shots caught the build mid-edit; that fault is gone.

## Q4. The home page's picture

Keep the table; rebuild its cells. It sorts methods by length, so AI-DLC looks complete. The difference is of kind: all four say how to build with AI; none says what the product's own model may decide. Draw two lanes.

- **X axis:** P0, P1, the rose sign-off rule, P2, P3, in the phase hues.
- **Lane one, "Building it: how the team and its coding agents work":** four rows. Each bar stays and gains three to six words under it, from the frameworks page: "bolts of hours or days", "the spec is the artefact". An empty cell is a dashed outline holding the word "silent". Under each name: "Best when: ..." and "Too heavy for: ...".
- **Lane two, "Deciding it: how right it must be, and what it may do alone":** the row "All four methods" is four dashed cells, each "silent". That row is the point: one gap under every method. The row "SkyWays PDLC adds" fills them with a different mark, a diamond for a decision, with today's words and one case number in mono: "refunds over $400 need a person", "partner flights: 80", "82.4 scored, 79.1 proven", "net minus $1,128".
- **One control:** chips, "My team uses: ...". A pick dims the other rows and writes: "BMAD covers Frame to Build. You still owe Run & Learn and the four decisions."
- **At 390:** each method is a block: name, best when, four squares, its words.

## Q5. Lessons and sketches

Measured at 1440: text ends at 1026, the column at 1336, so 310px is empty. A sketch is 634 by 359, its handwriting 30.7px beside 16.5px body text. On a phone it is 350 wide, handwriting 16.9px, and looks right. It is drawn at phone scale and blown up 1.8 times.

- **1440:** lesson list 248, text 634, margin 280, gaps 40 and 30. The margin holds, beside its paragraph: the sketch at 280 by 145 (handwriting 13.5px), caption under it; plain-word notes ("bar: the pass mark"). "On this page" tops the margin, unboxed. Tables and diagrams span text plus margin.
- **1024:** list 248, text 656. The sketch is 340 wide, caption to its right.
- **390:** one column, sketch 350 wide.

Role pages open with one strip showing the whole page. Give each lesson a phase strip (its phase lit, its artefact named) in place of three stacked boxes.

**Sketches.** Test: cover the caption. Can a stranger say the point, and are the labels the lesson's own nouns and numbers? Three kinds pass:
1. Quantity, with the case's numbers: four-pebbles-one-rock.
2. Where a thing sits: a-sign-or-a-sizer.
3. A against B, with real names: the-builder-and-the-one-inside.

Borrowed worlds fail, because the reader translates twice: pumpkins, scarecrows, the compass, wring-the-vibe. About 30 of 77 survive. One sketch a lesson. Swap the home page's compass for four-pebbles-one-rock.

## Q3. The Leadership page

Thirteen sections at one weight, six tables, no picture. The promise, four decisions only the sponsor can make, is section 8, nine screens down. Three good controls sit below it.

Five sections instead:
1. **First screen:** title, one sentence, then the decision strip: the phase line with four diamonds, the home page's mark. Each holds the question, "Ask for" and "Healthy answer".
2. **The decisions, opened.** One: the three-question funnel as a control (three picks give rule, person or agent). Two: the R1 to R5 authority ladder. Three: the pass mark calculator. Four: the value calculator, and the report as paired bars (8.0 to 4.6 person-days beside $0 to $310).
3. **Is it working:** the maturity check, drawn as six rungs.
4. **Ninety days:** one timeline with the sponsor's dates.
5. **Seven things to escalate on:** stays a list.

"Five things that change" become the decisions' reasons. Team tables go to `/method/`, tool tables to the tool pages.

## Q1. Simulations

One engine, a bench of three panes: thread (prompt and reply), artefact (document, diagram or grid), tray (choices). Stacked on a phone.

Seven, each handing its artefact on: **Frame it** (PM, P0; trap: the vivid pain wins). **Grow the spec** (PM, P1, a Claude project; trap: prose a model cannot check). **Draw the system** (architect, P1; trap: the limit in the prompt). **Tune the prompt** (engineer, a playground grid; trap: tuning to cases you can see). **Build a bolt** (engineer, P2, Claude Code or Codex; trap: self-rated risk). **Prove it** (QA, P2; trap: the average). **Run it** (sponsor, P3; trap: a saving without its cost).

**The diagram.** One inline SVG, three nested levels: context (the assistant as one box among its neighbours), high level (that box opened: gateway, agent, tools, limits, log), low level (the refund tool: signature, the $400 check, the approver). A tap animates the viewBox to that box in 400ms while its inside fades in. A breadcrumb zooms out. No text under 12px at rest. Reduced motion cuts; no script stacks the three. The player draws by choosing: dashed slots, a tray of pieces, tap slot then piece. A wrong piece is accepted and comes back one level down.

**A prompt run** is labelled "Recorded run, model, date"; the reply arrives whole, no fake typing. **Documents grow** with a format switch (prose, markdown, spec for a model) that counts the lines a model can check.

Build first: Grow the spec, Draw the system, Tune the prompt. Ninety Days stays as story mode, titled "The 90-day project".

## Q2. Tools

Both. In a simulation, a tool card: tool, the move, date checked, source. Manuals for Claude, Claude Code, ChatGPT with Codex, and Google AI Studio; Jules gets a mention. Each opens with a drawn, numbered anatomy of the screen. The build flags any fact older than ninety days.

## Q6. Personality

- A flight manual by someone who has sat in the incident review.
- Voice: calm, exact, numbers before adjectives.
- Look: an instrument panel, phase hues as signal lights.
- One new mark: the diamond, where a person must decide.
- First in: the home page's silent lane, the leadership strip, the lesson margin.

## Q7. Order and risk

Lesson grid and sketch cut; home picture; Leadership; then the engine with three simulations. Later: the other four, more manuals.

Risks: the zoom has unreadable middle states (design each level as a still first); the table gets dense; tool facts go stale.


---

# Response C

**Verdict.** Build one simulation engine and three simulations to a finished standard, three tool manuals with dated sources, and a shorter Leadership page. "No mistakes" and "all of it at once" cannot both be met.

## Q1. The simulations

**One engine, the bench.** Three panes: the situation, the work surface, the artefact that grows. A script is a JSON list of six step kinds: choose, assemble a prompt from parts, run, mark what is wrong in the reply, compare, file.

**An honest run.** Every reply is labelled "Recorded reply, written for this lesson. Your model will answer differently." No fake typing, no fake wait, no copy of a vendor's screen, no scoring of a typed prompt.

**Diagrams.** One SVG, three nested levels: context, high-level design, low-level design. The player picks where each part goes and the picture draws it. Zoom answers a click in 400ms; reduced motion gets three stills. Free-hand drawing is refused: it is a drawing app. This shrinks his ask; the zoom and three levels stay.

**Documents.** One pane; each run adds or strikes lines as a diff. Format is taught where the next reader becomes a coding agent: a recorded agent misreads the prose version and follows the fixed-heading markdown one.

**The set** (who, phase; hands; tool; artefact; trap):

1. **Frame the ask.** PM, P0; merge six interview notes by prompt, mark lines that lost their speaker; project chat; pain register; merging without names.
2. **Grow the spec.** PM, P1; PRD-lite to PRD to agent spec, choose the format; project chat, Spec Kit layout; signed spec; the $400 limit left as a sentence.
3. **Draw the system.** Architect, P1; place parts, mark each step exact or best guess; chat that returns diagram code; three diagrams; the refund cap drawn inside the model's box.
4. **Tune the system prompt.** Engineer, P2; three versions against twelve recorded cases; a model playground; prompt v3 with results; tuning to cases you chose.
5. **Hand work to a coding agent.** Engineer, P2; context file, story file, review by risk; Claude Code or Codex; a reviewed change; trusting the agent's own "low risk".
6. **Prove it by kind of case.** QA, P2; the Day 45 task, reused.
7. **Read the bill.** Platform, P3; the Day 75 and 90 tasks, reused.

**Build first:** 2, then 4, then 3. The owner named all three. 2 is all text and proves the engine; 3 carries the zoom, the riskiest part.

**Ninety Days:** keep it as the story mode, under a plain page title, "The simulator", beside the benches. Close the findings in `SP/r7/audit/simulator.md` first.

## Q2. Tool fluency

**One page, `/tools/`,** sorted by job: think it through, keep project context, test a prompt, change code, act in a browser, run on a schedule. Each row names each family's tool.

**Three manuals:** Claude (chat, Projects, skills, connectors, scheduled tasks, Claude Code in its four forms), ChatGPT with Codex, Google AI Studio. Jules and the rest get a card now, a manual later. This reverses "every feature" and "all possible usages", plainly: a full feature list is wrong within a month.

**Each manual:** six to eight features, each with "use it when", its phase, one use on the airline case, one trap. No prices, limits or version numbers.

**Staying true:** every fact is a row in one data file, with a source address and a "checked on" date printed beside it. Nothing is written from memory. A row without a source fails the build.

**Inside a simulation:** a tool card says why a practised hand uses this tool here.

## Q3. The Leadership page

Thirteen equal sections over fourteen screens. The first screen is three columns of prose. The four decisions, the page's key moment, are section 8.

New shape, six sections. First screen: title, one line, the four decisions as four rows. Then each decision with its calculator, the report you should receive, ninety days as one line, seven things to escalate, the first thirty days. The teams table, role cards, frameworks and tooling move to their own pages. Old anchors keep working.

## Q4. The home page's case

Keep the table and fill it. Each bar becomes a cell of three to five words from `frameworks.json`; an empty cell says "silent", as on the frameworks page. Bars stay on a phone. The last row, what this manual adds, gets the one raised surface. No new band.

## Q5. Lessons and sketches

At 1440 text stops at 640px beside 300px of empty page. Put a margin column there: "In short", the key numbers, the sketch beside its paragraph.

A sketch survives one test: a fresh reader sees it without caption or lesson and states the point. A thing from the case with its number passes (the $400 ladder). A metaphor that needs its handwriting fails. Expect about forty of 77 to stay.

## Q6. Personality

- Voice: a senior colleague who ran this project and shows the numbers.
- It quotes your choice back when it costs you.
- Look: a flight manual. Checklists, dated facts, phase hues.
- First places: bench feedback, the Leadership first screen, the "checked on" stamps.
- The robot face at bottom left is a mascot. Remove it.

## Q7. Order and risk

1. **Gate first.** `SP/r8/base/lesson-dark-1440-03` to `-07` caught new HTML with an older stylesheet: a diagram's phone form printed with 600px icons. Add checks for a half build, an icon over 64px, a figure showing both forms. Shoot with motion on, in both themes and three browsers. *Check: the gate fails on an old stylesheet.*
2. **Words on what exists:** simulator title, Leadership cut. *Check: a cold reader shown each first screen says what it is for; old anchors resolve.*
3. **Lesson layout, sketch cull.** *Check: the caption test.*
4. **Home table.** *Check: every cell's words exist in `frameworks.json`; fits 375px.*
5. **Bench engine with "Grow the spec".** *Check: every path walked in node; every reply labelled; clicked through at 320 and 1440; the owner sees it.*
6. **Benches 4 and 3.** *Check: the same, plus zoom stills.*
7. **`/tools/` and three manuals.** *Check: a second agent opens every source and confirms each sentence; the rest is cut.*
8. **Performance.** *Check: bytes and first paint per page type, before and after; none worse.*

**Later:** benches 1, 5, 6, 7; more manuals; the workbench's theme.

**Three ways this goes wrong.**
1. Breadth: seven simulations and eight manuals, each most of the way done.
2. Tool facts written from memory.
3. Checks that do not look as the owner looks: one browser, motion off, a build caught halfway.


---

# Response D

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


---

# Response E

**The map first.** Three verbs: read, do (Simulator), look up (Library). The top bar keeps five places and one pill; refuse a sixth. "Simulator" becomes a section with two shelves: **The project** (today's game) and **Labs** (at `/simulator/labs/<name>/`). `/simulator/` and `#day-45` do not move. Tool manuals are a fifth Library shelf, **Tool guides**, at `/tools/`.

## Q1. Simulations

Keep the game as story mode; retire "Ninety Days" as a heading: the title becomes "Run a ninety-day AI project". Days stay in the story only, because a debt needs a date to land on. Labs are named by verb and artefact. Each opens cold with the previous artefact supplied "by the book".

| Lab | Phase, role | Hands do | Tool shown | Leaves with | Trap |
|---|---|---|---|---|---|
| 1 Frame the pain | P0, PM | attach notes, run a dedupe prompt | Claude Project | pain register | a number the model cannot know |
| 2 Grow the spec | P1, PM | PRD-lite to PRD to agent spec; pick the format | chat canvas | eight-field spec | the $400 limit left in prose |
| 3 Draw the system | P1, architect | tag steps; zoom context, HLD, LLD | diagram as code | three linked diagrams | a box called "AI" |
| 4 Tune the prompt | P1 to P2, QA | three prompts, twelve fixed cases | playground | prompt v3, config card | tuning to cases you saw |
| 5 Build one slice | P2, engineer | context file, plan, read the diff | terminal agent | merged slice | the cap in the prompt |
| 6 Prove it | P2, QA | split the score by kind of case | test harness | evidence page | the average hides the risk |
| 7 Run and report | P3, platform | read the bill, schedule a drift check | usage log, scheduled task | two-number report | saving without spend |

One engine, three panes: **Brief** (one cold sentence), **Bench** (the tool), **Artefact** (always visible, the last change marked). A step is choose, run, read, keep or redo. A reply is labelled "Recorded reply, model and month. Not live", beside "Copy and run it yourself". No fake typing. Diagrams are one SVG in three nested levels; zoom answers a click. Lab 2 shows one spec in three formats and what a coding agent builds from each.

Build 2, 3 and 4 first: the owner named all three, and together they use every pane.

## Q2. Tool fluency

Both, and by job, not by vendor. `/tools/` opens on one table: jobs down the side (draft, build in the repo, test a prompt, repeat a check); Claude, ChatGPT and Codex, Google across. Four manuals earn a page: Claude at the desk (chat, Projects, skills, connectors, scheduled tasks); Claude in the repo (terminal, VS Code, remote sessions, Chrome); ChatGPT and Codex; prompt playgrounds, AI Studio included. Jules, Cursor, Copilot and Kiro get a row and a link out.

Each page: what it is, when not to use it, five moves a professional makes (each linked to the lab step that performs it), a dated facts table. A fact older than ninety days reads "unchecked since" and the build lists it. In a lab the tool is one chip on the Bench, linking to its manual.

## Q3. Leadership

Diagnosis: thirteen sections, fourteen screens, seven tables. The first screen (`protocol-dark-1440-01`) is a title that promises nothing and four blocks of text. The first control is on screen ten. The four decisions the home row promises are section eight. The four questions appear three times. It is an essay with no route.

New shape:

- Title: "Four decisions only the sponsor can make." Line: "Twenty minutes. Leave with four questions for your next review."
- First-screen picture: the P0 to P3 line with four pins where each decision falls. Each pin is a link.
- 1 The four decisions, one card each: the question to ask, a good and a bad answer, one control. D1 sorts five backlog items into rule or AI. D2 is a five-rung ladder picker. D3 and D4 are the existing calculators. "How it works" folds under each.
- 2 How you will know: the six-control check, the two-number report, seven warning signs.
- 3 Ninety days: the existing stepper, one trap each.
- 4 First thirty days, a checklist that prints on one page.
- 5 Send your team: the home page's role rows.

Cut "Why this matters", "Five things that change" (they are the decisions) and the frameworks section (one link). Move the teams table and the three levels to Tool guides.

## Q4. Home

Keep the table. Its bars are mute; give them the frameworks page's words. Under each bar, five words on what the method gives that phase; an empty cell says "silent". Under each name, "Best for" and "Weak at". The last row becomes four filled chips naming what SkyWays adds.

Add one control: "Your team uses: AI-DLC, BMAD, spec-driven, AIDD, none yet". A pick lights that row and writes one sentence: "With AIDD you have the build. You still decide these three." Refuse the sixteen-box merge figure on home; link to it.

## Q5. Lessons

At 1440 the prose is 634px wide and 310px beside it is empty (`r8/product/b/p0-dark-1440-04`). Keep the prose narrow and use the margin for what role pages have: the contents list, the phase strip, and "Do it" (template, prompt, lab). Sketches sit there at 320px, beside their paragraph.

The test: cover the caption; can a stranger say the point? Keep sketches that show the case's own objects and numbers: the $400 cap against the $2,000 refund, four right at $9 against one wrong at $36. Cut metaphors that need decoding: the compass, the river jam. Expect about thirty of 77.

## Q6. Personality

1. Voice: a senior colleague who ran this project and quotes the number. "Show me the cap."
2. It names the price, and says what it will not do.
3. Look: an operations manual read at night. Mono labels, one line, phase hues only.
4. Its recurring cast is the case's numbers: $400, 82.4, 4.4 times.
5. Shows first in: the home page's four overheard lines; every lab's brief and wrong-answer line; the 404 and "Copied". Remove the robot face button.

## Q7. Order and risk

Order: (1) names, titles, the game audit's two broken items; (2) Leadership; (3) the home table; (4) lesson margin and sketch cull; (5) the engine with labs 2, 3, 4; (6) the Tool guides index and two Claude manuals. Later: everything else.

Risks:

1. Seven half labs lose to three complete ones.
2. One stale tool fact discredits every manual.
3. A half-loaded stylesheet. `r8/base/lesson-dark-1440-03` shows a flow figure's phone form at 1440 with 600px icons; my later walk was clean. Size the icons in markup.
