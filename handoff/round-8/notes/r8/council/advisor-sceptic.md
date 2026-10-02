# Advisor: the sceptic and scope editor

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
