# Round 8 handoff from the local session

Written on 2 October 2026 by the local Desktop session that the cloud session "Site redesign for clarity and
premium feel" was continued from. It adds what the move to the cloud could not carry. Read all of it before
going on, then keep it open: the owner wants no work and no context lost.

## 1. What the move carried, and what it did not

At about 05:28 UTC the owner used **Continue in → Claude Code on the Web** in the Desktop app. The app pushed
the whole local working tree (committed, uncommitted and new files) as branch `main-bljw84`, wrote a summary
of the conversation and started the cloud session from it. The cloud session then finished the first lab and
committed `df2e354` ("The labs open, the game speaks plainly, and a page never meets an old stylesheet").

Checked at about 06:10 UTC, file by file: every file in the local working tree is identical to `df2e354` or
an older version of it (lab.js, lab.css, labs.py, build.py, render.py, accept.mjs and the workbench file are
newer in the cloud). **Nothing from the local session is missing from `main-bljw84`. Keep working there.**

What the move did not carry:

- **The local scratch folder.** Your summary calls it `SP/...`. The parts that matter are in this folder,
  with the same layout: `SP/r7/audit/home.md` is now `handoff/round-8/notes/r7/audit/home.md`. Screenshots
  and build copies were not copied.
- **The owner's global instructions and saved preferences.** They live on the owner's Mac. Section 4 below
  restates them. Follow them as if they were in your instructions.
- **The local tools and skills.** Section 2 sets them up.
- **The four helpers** the local session had started. Moving the session stopped them mid-task. Their edits
  are in `df2e354`; section 3 says where each one stopped.

One thing the move carried by mistake: `.claude/launch.json` (the Desktop app's list of local preview
servers, with local scratch paths in it) was meant to stay untracked and is now committed. Remove it from
the branch with `git rm --cached .claude/launch.json` and add `.claude/launch.json` and `.claude/worktrees/`
to `.gitignore`.

## 2. Set up this machine (once; again if the session's machine is rebuilt)

1. `bash .claude/cloud/setup.sh` installs headless Chrome (Chrome for Testing, behind
   `/usr/local/bin/google-chrome`), the AWS CLI, and the owner's skills that have a public source, at pinned
   commits. About three minutes. It always exits 0 and prints what it did.
2. `export CHROME=/usr/local/bin/google-chrome` unless the environment already sets it. Every check tool
   reads `$CHROME` (the default in them is the Mac path).
3. `bash .claude/cloud/session-start.sh` links those skills into `.claude/skills/` and prints what this
   session has. The links point outside the repository: add `/.claude/skills/*` and
   `!/.claude/skills/manual-diagrams/` to `.gitignore` so they are never committed. Then run `/reload-skills`.

Skills, and where each comes from:

- **Linked by session-start.sh:** humanizer, no-ai-slop-skill, taste and the taste-skill set (brandkit,
  brutalist-skill, gpt-tasteskill, image-to-code-skill, imagegen-frontend-mobile, imagegen-frontend-web,
  minimalist-skill, output-skill, redesign-skill, soft-skill, stitch-skill, taste-skill), ui-ux-pro-max and
  its set (banner-design, brand, design, design-system, slides, ui-styling), transitions-dev,
  transitions-polish, karpathy-guidelines, caveman, ian-xiaohei-illustrations. On the owner's Mac some of
  these load as plugin skills (`taste-skill:redesign-skill`, `ui-ux-pro-max:design`); here they have the
  plain folder names. Their scripts paths in SKILL.md (`${CLAUDE_PLUGIN_ROOT}/...`) mean the skill's own
  folder.
- **On the owner's claude.ai account, so they load by themselves** (as `anthropic-skills:<name>`):
  explainer-illustrations, humanizer, frontend-anti-slop, llm-tic-scrubber, aidd-teaching,
  agentic-testing-architect, lesson-architecture, lesson-strategy, curriculum-detailing, concept-packaging,
  mini-project-designer, cohort-session-kit, study-notes-builder, training-deck-builder, build-contract,
  canvas-design, theme-factory, web-artifacts-builder, skill-creator, docx, pdf, pptx, xlsx, internal-comms,
  session-debrief, import-memory, morning.
- **Not here:** the owner's own `explainer-diagrams` and `bedrock-image` (they live only on the owner's Mac;
  the owner may upload them to claude.ai), and the AWS skills (`amazon-bedrock`, `aws-*`): use the AWS MCP
  connector's `retrieve_skill` if the owner has enabled that connector for this session, otherwise the AWS
  documentation. There are no AWS credentials here, by the owner's rule, so `bedrock-image` could not run
  anyway (and each image is a paid call that needs the owner's yes).
- **BMAD and the LLM council** were never installed as skills. They are methods the local session applied by
  hand: BMAD-style spine documents (`site/DESIGN.md`, `site/EXPERIENCE.md`, `site/GAME.md`) and councils of
  five advisors, anonymised, five reviewers, a chairman (the councils' papers are in `notes/r7/council/` and
  `notes/r8/council/`).

There is no Browser pane in a cloud session. Look at pages with headless Chrome instead. Serve the build with
`python3 site/build.py && (python3 -m http.server 8811 -d site/_site >/dev/null 2>&1 &)` and use:

- `handoff/round-8/tools/walk.mjs`: a reader's scroll, one screenshot per screen, motion allowed.
  `node handoff/round-8/tools/walk.mjs <outDir> <width> <height> <light|dark> name=http://localhost:8811/...`
  (env `MAX`, `PAUSE`, `FIRST`, `TIMES`, `STEPS` as its header says)
- `handoff/round-8/tools/drive.mjs`: click, type, evaluate and shoot by steps (`MOTION=1` to allow motion)
- `grabcanvas.mjs`, `frames.mjs`, `themecheck.mjs` in the same folder; `notes/r7/figs/check.mjs` and
  `measure.mjs` (the figures helper's checker: text size, collisions, overflow per drawing)
- `site/tools/accept.mjs` (thirteen passes), `herosheet.mjs` (twelve moments of the hero at four widths),
  `sim.test.mjs`, `playtest.mjs`, `lab.test.mjs`, `workbench.test.mjs`, `shoot.mjs`, `simshots.mjs`
- Safari's engine: the local session used a Mac-only WebKit runner. Here, setup.sh installs Playwright with
  WebKit when the network allows `cdn.playwright.dev`; write a small runner that loads `playwright` from the
  global module folder (`npm root -g`) and uses its `webkit` browser.

## 3. The four helpers the move stopped

Their edits are in `df2e354`. None of them wrote a final report.

1. **Game fixes** (findings 1 to 15 and section 2 of `notes/r7/audit/simulator.md`). Fixes applied to
   `site/play/days.json`, `sim.js`, `art.js`, `game.js`, `game.css`; new lints in `site/tools/sim.test.mjs`
   (the title, and headlines read alone) and `playtest.mjs` (checks 10 and 11). It was proving the tests by
   breaking each fix in a copy: mutations 1 to 5 and 8 were caught, 6 and 7 "could not start" because the
   runner was killed for memory. Owed: rerun mutations 6 and 7 one at a time; name three moments worth a
   deeper exercise (its brief asked for this); report.
2. **Workbench upgrade** (steps 0 to 9 in `notes/r7/audit/workbench.md`). Applied to
   `site/app/SkyWays-Architect.html` by scripted edits, plus `site/frame/frame.js`, `frame.css`, `config.js`:
   dark by default, phase hues, mascot, points, ranks, badges and share removed, 93 dead CSS rules dropped,
   the how-to folded. It was waiting on a full `node site/tools/workbench.test.mjs` run when it was killed.
   Owed: run that test and fix what fails; re-shoot the ten workbench pictures (`site/tools/simshots.mjs`);
   it was also to list six link edits for `site/render.py` and `site/pages/protocol.py` (pages that call the
   workbench "simulator"); find them with a search for `simulator/#/`.
3. **Figures and boards** (findings in `notes/r7/audit/manual.md` and `tutorial.md`). Edits in
   `site/theme/base.css` (24), `site/pages/maps.py`, `site/pages/figures.py`. Its checker found 0 faults on
   the shots sheet at 1120 wide. It was measuring the contrast of figure text in the phase hues, both themes:
   teal text on its own 16% tint is 3.6 to 1 in the light theme (below 4.5); amber was not read yet. Owed:
   fix those contrasts, list the pictures to re-shoot, report.
4. **Leadership page** (`/protocol/`, built by `site/pages/protocol.py`). It read the council and the
   content and wrote nothing. Not started. Brief: the owner called the page "a text spaghetti and currently
   directionless". Council 7 verdict: title "Four decisions only the sponsor can make", a phase line with four
   pins, five sections, the reference material folded at the end. Diagnosis from the advisors (Q3 in each of
   `notes/r8/council/advisor-*.md`): thirteen equal sections over fourteen screens; a first screen that is a
   title promising nothing, a sixty-word italic paragraph and three columns of prose. Model it on the role
   pages the owner likes (for example `/product-manager/`: a clean rail, a roadmap picture at the top,
   numbered step cards that open).

The content helper finished. Its report is `notes/content-agent-report.md`. Section 4 there lists fixes in
files it could not touch; none were made yet:

- `site/render.py:644` adds a full stop after an activity name that may already end in `?`.
- `site/pages/learn.py:857-858` still says "in one sentence" (the lessons now say "in short").
- `site/pages/mapspecs.py:509, 514` say "playbook" where the page means the workbench.
- `site/wiki_export.py:173` writes dash cells into the Journey pages; write "none".
- `site/content/learn/README.md` (sweep damage on lines 16 to 18 and 39, "playbook", "the simulator", 13
  dashes) and `site/content/SCHEMA.md` (10 dashes).
- Five role sources link to `../simulator/#/...` and 91 wiki links to `.../simulator/#/...`; they work only
  through the game's redirect and should point at the workbench.
- Generated wiki pages carry old text until `site/learn_export.py` (and `export_models.py`) run again.
- About 1,690 dashes remain in hand-written wiki pages.

Its questions for the owner: the five "From" cells in `frameworks.json` (its own words, BMAD as "BMad Code");
the retitle of the agentic-delivery-simulator lesson to "Agentic AI Workbench: ..." (slug unchanged); the
new workbench line in `wiki/_Sidebar.md`; the "In short" label; summaries that run to four or more short
sentences; role template cells that now say "none", "n/a" or "skip".

## 4. Standing rules (the owner's, from their machine)

### How to work

- Commit or push only when the owner asks. Never push to `main` without asking: a push to `main` that touches
  `site/` deploys the public site (`.github/workflows/pages.yml`). Ask before running `wiki/sync.sh`.
- Subagents and background tasks run on the same model and at the same effort as the main session. The owner
  works at extra-high or max effort and never lower. Pass the model explicitly on every Agent call.
- No paid call without the owner's yes for that task (Bedrock image generation in particular).
- Third-party repositories are read-only references. Only instruction-only skills that have been read go into
  a skills folder; anything with installers or hooks goes to the owner as commands to run.
- Report outcomes faithfully: failing tests with their output, skipped steps as skipped.
- Before reporting any visual change as done, look at it the way the owner will: motion allowed, sampled over
  time for anything that moves, at 1440, 1024, 390 and 320 wide, dark and light. A fresh reviewer looks too.
  (Headless shots under reduced motion once missed an aircraft breaking apart mid-flight; the owner's reply
  was "still making so many mistakes".)
- A "broken" report just after a release may be a cached stylesheet: reproduce with the previous commit's
  CSS before assuming the design is at fault. The build versions every local stylesheet and script
  (`stamp()` in `site/build.py`); keep it, and keep the gate's "versions" and "no stylesheet" passes.

### AWS, from the owner's global instructions

- Prefer the AWS MCP Server for AWS work; if it is unavailable, the AWS CLI.
- Before an AWS task, look for a relevant AWS skill and load it with `retrieve_skill`; prefer its guidance.
- When unsure of an AWS detail (API parameters, permissions, limits, error codes), check the documentation;
  say so when it cannot be confirmed.
- Infrastructure as code (CDK or CloudFormation) over direct CLI commands; follow the Well-Architected
  Framework.
- No em dashes in AWS resource names or descriptions; use hyphens.
- Secret safety, in the owner's words: "MUST load the `aws-secrets-manager` skill first for any secret,
  credential, API key, token, or password task. MUST NOT call `secretsmanager get-secret-value` or
  `batch-get-secret-value`, and MUST NOT hit the Secrets Manager Agent daemon directly. MUST use
  `{{resolve:secretsmanager:secret-id:SecretString:json-key}}` with `asm-exec` so the secret resolves at
  runtime without entering context." On 2 October 2026 the AWS skills registry had no skill by that name
  (the nearest is `creating-secrets-using-best-practices`). Never put a secret in the cloud environment's
  variables or in a file.

### The site: what the owner has taught earlier sessions

- **Depth over pretty.** "Right now it just looks slightly pretty. I need depth too and actual nuances too."
  For every page or simulation ask what the reader does, makes and leaves with before asking how it looks.
  Simulations should give "a feel of all substeps", "simulate running prompts", show choices, techniques and
  the artefacts made. A picture "should be even clearer to understand than words and be relatable"; a
  comparison must show how things differ and where each is weak. Every page uses its width.
- **Plain words, self-contained screens.** One idea per sentence, about twenty words at most, no clever
  sayings or metaphors. Every heading names who and what to someone arriving cold (the owner rejected "Six
  people must agree to one list. None of them has seen it."). Any screen in a sequence carries a one-line
  recap. Labels follow one pattern ("The manual" like "The tutorial"). No em or en dashes in prose. Run the
  humanizer skill on new copy.
- **Keep what works.** When the owner asks to add something, add it; do not replace a section they have not
  criticised, even on a council's advice. Show both or ask first.
- **Taste.** Premium, roomy, few elements, one strong visual per section, cut before decorating. The owner
  likes the theme and colours, rejects "too texty", "too many elements", "cluttery, directionless". They
  would rather react to a bold attempt than choose between options first. Visible identity (the SkyWays
  mark). Read `site/DESIGN.md` and `site/EXPERIENCE.md` before changing page structure.
- **Motion** only for a thing that is itself a movement (the hero flight, the game) or an answer to the
  reader's hand. Nothing moves because it scrolled into view; nothing a reader came to read waits for an
  animation. No view transitions, no spring curve, no entrance animations.
- **Navigation reacts to where the reader is**: a control never links to the page it is on.
- The owner asks for the LLM council, the BMAD approach and the named skills (ui-ux-pro-max, taste,
  humanizer) when planning; use them when asked.

## 5. Council 7 verdicts (the plan for round 8)

1. Real recordings only. Label: "Recorded reply. [model], [date]. Not live. Yours will differ." with "Copy
   the prompt"; each prompt stored beside its recording; no fallback reply. If the model avoids the trap,
   change the lesson, never the reply. (Done in `df2e354` for the first lab.)
2. Labs at `/simulator/labs/<name>/`; "Simulator" opens a first screen with two shelves (the labs and the
   ninety-day project); retitle the game (for example "Run a ninety-day AI project"); `#day-N` links keep
   working. (`df2e354` serves the labs at `/labs/` instead; settle which with the owner.)
3. Seven labs on one engine. First three: **Grow the spec** (trap: a default the model filled in passes as
   a decision), **Tune the system prompt** (trap: tuned cases pass, held-out ones fail; cells as passes out
   of runs), **Draw the system** (trap: the $400 limit sits in the prompt, not the tool; mark the model's
   context diagram, place pieces at HLD, move the limit at LLD; one SVG, viewBox zoom of about 400 to 600 ms,
   each level a still). Order: spec, prompt, draw. Record the prompts first.
4. Tools: a `/tools/` table by job with vendors across; facts in one file under `site/content/tools/`, each
   with its source and the date it was checked; the build warns at 60 days. Two manuals first (Claude at the
   desk, Claude in the repo), ChatGPT and Codex, Google AI Studio and Jules next. No prices, limits or model
   names. Tool cards inside the labs. The research is done: `notes/r8/research/claude.md`, `openai.md`,
   `google-and-others.md` (about 27,000 words, sourced on 2 October 2026; have a second agent check sources).
5. Leadership: see section 3, helper 4.
6. Home page method table: keep it; words under the bars; "silent" in the gaps; "best for" and "weak at";
   one row "All four methods: silent" above the manual's row, with diamonds and case numbers; a "My team
   uses" control with the method names as buttons. Bring out the value proposition; the frameworks page has
   ideas worth borrowing.
7. Sketches: about 30 survive. The test: with the caption covered, a stranger states the point, and the
   labels are the case's own nouns and numbers. At most one per lesson, in a 280 to 300 px right margin at
   wide widths. Home sample: `four-pebbles-one-rock`.
8. Remove the robot face, the name Pip and the floating guide button; keep walkthroughs in the drawer.
9. Voice: a senior colleague who ran this project and shows the numbers. Look: a flight or operations
   manual, mono labels, dated facts, phase hues; a hollow diamond only where a person decides.
10. Role pages: an optional `lab` field so a step links to its lab.
11. Show the owner the first lab before building more. Give the owner a list of what was asked and what is
    not yet built. Measure performance before and after.

## 6. Still to do (as of the move; check against your own task list)

- Finish what the stopped helpers owe (section 3), then look at the game, the workbench and the figures at
  four widths in both themes.
- Show the owner the first lab. Then Tune the system prompt and Draw the system.
- The simulator's first screen with two shelves, the retitled game, role steps linking to labs.
- The home page: method table changes, value proposition, sample sketch.
- Lessons: the right margin layout and the phase strip; cull the sketches to about 30; shoot sketch images
  for the picture pack (`python3 site/build.py --shots`, then `ONLY=sketch- node site/tools/shoot.mjs ...`);
  rebuild the picture and wiki twins.
- Remove the robot face, Pip and the floating guide button.
- The `/tools/` page and the two Claude manuals, from the research notes.
- The Leadership page.
- The content helper's open items (section 3).
- Plan document for the labs and tools (for example `site/LABS.md`); update `site/DESIGN.md`,
  `EXPERIENCE.md`, `GAME.md`, the README, `CHANGELOG.md` and the sketches README; re-shoot `og/home.jpg`,
  changed figures and simulator pictures; regenerate the wiki (`site/learn_export.py`) and run
  `python3 wiki/check.py --strict`.
- Performance: bytes and first paint per page type, before and after (base.css was 147 KB, 34 KB gzipped;
  the home page 12 KB gzipped; the workbench 1.9 MB, 821 KB gzipped).
- Final checks: `sim.test.mjs`, `playtest.mjs`, `accept.mjs`, `workbench.test.mjs`, `lab.test.mjs`,
  `herosheet.mjs`, WebKit; walks at 1440, 1024, 390 and 320 in both themes with motion allowed.
- The final report to the owner: the cause of the "broken" look (a cached stylesheet meeting new pages,
  fixed by versioned files), what was fixed, what was asked against what is built and not built, the skills
  and how they were installed, that image generation is a paid Bedrock call needing their yes, and honest
  limits (no free-hand drawing; not every feature of every tool; Firefox not checked). Ask before any commit
  to `main`, push to `main` or wiki sync.

## 7. What is in this folder

- `notes/r8/research/`: the tool fact sheets (Claude; OpenAI; Google and others), sourced on 2 October 2026.
- `notes/r8/council-brief.md`, `notes/r8/council/`: council 7, its brief, five advisors, the anonymised
  set (`all.md`), the review brief and five reviews. The verdicts are in section 5 above.
- `notes/r7/context.md`: the product, the owner's words and taste, and the look-at-it tools, as briefed to
  round 7's helpers.
- `notes/r7/council/`: council 6 (the fix round): advisors, reviews, `all.md`.
- `notes/r7/audit/`: the round 7 audits of the home page, tutorial, simulator, manual and workbench, with
  their two measuring scripts. The screenshots they cite were not copied.
- `notes/r7/figs/`: the figures helper's checker and measurer.
- `notes/sketch-brief.md`, `notes/sk/check.py`, `notes/sk/sheet.py`: the sketch brief and two sketch tools.
- `notes/content-agent-report.md`: the content helper's full report.
- `tools/`: walk, drive, grabcanvas, frames, themecheck (they read `$CHROME`).
