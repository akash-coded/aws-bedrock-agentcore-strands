# Changelog

Notable changes to this curriculum. Dates are when the change landed on `main`.

The format is loosely [Keep a Changelog](https://keepachangelog.com/). This is teaching material rather
than a released library, so there are no semantic versions — but breaking changes to structure are called
out, because people bookmark deep links.

---

## 2026-10-02 · The labs open, the game speaks plainly, and a page never meets an old stylesheet

The labs are new: one job of the airline's project, done by hand. How a lab is written, and its one rule
(a recording is a recording), are in [`site/content/labs/README.md`](site/content/labs/README.md); the
record of the round is in [`site/EXPERIENCE.md`](site/EXPERIENCE.md) and, for the game,
[`site/GAME.md`](site/GAME.md).

### Added
- **The labs**, at `/labs/`. A lab is a bench: on the left the work, one beat after another; on the right
  the document the work makes, which shows what a person decided and what a model guessed. The player
  assembles a prompt from parts, runs it, reads the reply, marks what is wrong in it, makes the calls only a
  person can make, and leaves with the document to download. One lab is open, **Grow the spec** (P1, twelve
  minutes): a product manager's one page becomes a spec a coding agent can build from, without letting a
  model make the five decisions nobody has made. Three more are listed as being built: the system prompt
  from the spec, proving the bar, and reviewing a change a coding agent wrote. The engine is in
  [`site/labs/`](site/labs/), the pages and the check in [`site/pages/labs.py`](site/pages/labs.py), and
  each lab is one script in [`site/content/labs/`](site/content/labs/)
- **Every reply in a lab is a recording**: a real model's answer to the exact prompt the lab shows, saved
  when the lab was written, with the model's name and the date on it and a line that says the reader's own
  will differ. Nothing is fetched and no model is called. The build refuses a recording with no model or
  date, and one whose prompt is not what the lab's parts join into, byte for byte, so a prompt cannot be
  edited after its reply was recorded. Every prompt has a copy button, for trying it on the reader's own model
- **A lab reads as a document without script**: each step, the prompt the book uses, every recording with
  its model and date, the faults to notice, the call the book makes and why, and the document as the book
  leaves it
- [`site/tools/lab.test.mjs`](site/tools/lab.test.mjs) plays a lab by real clicks in headless Chrome, on
  every path its script has. It checks that the prompt the page assembles is the one recorded, that marking
  every fault scores full and marking none scores nothing, that a reload comes back to the same beat, that
  the focus moves to each new beat, that nothing scrolls sideways on a phone, and that without script every
  recording is on the page
- [`site/tools/workbench.test.mjs`](site/tools/workbench.test.mjs) drives the workbench in headless Chrome,
  in eight sections: every route at 1440 and 390 wide in both themes, with no script error, its title in
  the first screen, no sideways scroll and text at 4.5:1; the dark default and the theme stored under the
  site's own key; the top bar; a link from the game or a lesson that lands on the part of a page it names;
  all seventeen calculators, the evidence pack across a reload, a decision walk to its end, and state
  saved by the earlier version; no old name, mascot, rank or points counter, and nothing that moves on its
  own; the ten pictures `simshots.mjs` captures; and the file opened alone from disk, with no network
- [`site/tools/herosheet.mjs`](site/tools/herosheet.mjs) lays the hero out at twelve moments of one lap, at
  four widths, in both themes, on sheets for a person to look at before a release. The gate measures the
  hero; this is for the eye
- [`site/tools/sim.test.mjs`](site/tools/sim.test.mjs) checks more of the words and the rules: every
  headline names what it is about, and no headline, context line or question points at someone it has not
  named; the heading says it is a game before it gives the name; every day after the first leans on an
  earlier day and on a document an earlier day files, and "So far" quotes that day and never joins two; a
  document waits for its task; a question can be asked of a sound plan as well as an unsound one, and shows
  only evidence; and a late run never reports the saving of one on time.
  [`site/tools/playtest.mjs`](site/tools/playtest.mjs) has an eleventh section, what an audit found by
  looking, each kept as a check and run with motion allowed: the title's first screen says what the game is
  and how to start; a day's question and its first option are on the first screen; the header does not
  move between days; on Day 75 only the labels of what is left are shown; on Day 82 nothing sits on
  anything else down to 320 wide; a figure plays only as the answer to a press, and only on screen; a pin
  flies only to a day strip that can be seen; a document goes on file when its task is done; Day 15's three
  documents line up; the sponsor may ask about any plan; and a day offers one way to leave the run
- The labs are in the drawer under Play, in the search and in the sitemap, and the home page's simulator
  band has a quiet link to them
- Four more passes in [`site/tools/accept.mjs`](site/tools/accept.mjs), thirteen in all: the top bar fits
  at five widths, the floating buttons stay off the words, every local stylesheet and script is asked for
  by its version ("versions"), and with every stylesheet blocked no mark in a sketch falls back to solid
  black ("no stylesheet"). The passes that run page by page now include the two lab pages

### Changed
- **The hero is one canvas on one clock** ([`site/theme/hero.js`](site/theme/hero.js)): a turning Earth, a
  fine spiral around it, and one aircraft that climbs the spiral. The front of each turn is the journey, P0
  to P3; the back, behind the Earth, is the way back to Frame. Each turn sits one step above the last, and
  the whole spiral sinks as the aircraft climbs, so it climbs for ever without leaving the picture. Only the
  turn being flown is in the phase hues, with its one sign-off; the turns already flown are grey. The flight
  used to be drawn over the globe in SVG and CSS, as a thick ribbon. The Earth turns once in 75 seconds
  (it was once a minute), and a lap takes 27: steady in front of the Earth, quick behind it. The aircraft
  has three shapes where it had four, easing from one to the next: a paper dart in P0, the outline of an
  airliner in P1, the airliner drawn solid from the sign-off on, a jet in P3, and the dart again by the time
  it comes round from behind the Earth. The phase names sit in one line under the picture, and the line
  marks the phase the aircraft is in. The only entrance left is the Earth's: it spins down to its steady
  turn in the first second or two, once in a sitting, and the path and the aircraft are simply there. The
  gate's hero pass now checks, at twelve moments of a lap and four widths, that the line under the picture
  names the phase the aircraft is in
- **Nothing waits to be scrolled to.** The home page's bands no longer rise into place as the reader
  reaches them (`.rv` is gone from [`site/theme/base.css`](site/theme/base.css)), so the gate's third pass is
  now "nothing waits for an animation": 700ms after load nothing on the whole page is hidden
- **No view transitions.** Pages change without the cross-fade, and the top bar's pill no longer travels
  from one page to the next
- **The home page's simulator band shows one real day of the game**: Day 45 as a card, with the QA room
  drawn in pixels, the day's headline, its context, its question and its three answers with their price in
  days, each of which opens Day 45 in the game. The words come from `days.json`, and the day is `SIM_DAY` in
  [`site/render.py`](site/render.py). The card takes the place of the three moments of the game shown in turn,
  their pause control and the band's three numbers. The band's link to the workbench gave way to the link
  to the labs; the workbench stays in the drawer and the footer
- **Stylesheets and scripts carry their version.** The build gives every local stylesheet and script a page
  asks for a `?v=` taken from a hash of the file's content (`stamp()` in [`site/build.py`](site/build.py)).
  GitHub Pages lets a browser keep a file for ten minutes, so a reader who arrived just after a release could
  get the new page with the old stylesheet. A changed file now has a new address. The pristine tool in
  `app/` is left alone
- **The game in a newcomer's words.** Every headline and context line in
  [`site/play/days.json`](site/play/days.json) names what it is about (the AI assistant, six airline
  managers, the project team) and points at nobody it has not named, and every question says who is to act:
  "What does Maya report?" is now "What should the QA lead report about the score?".
  [`site/tools/sim.test.mjs`](site/tools/sim.test.mjs) checks all three
- **Each day names the call it leans on.** Every day after the first has a `leans` entry, which "So far"
  follows: the earlier day to quote, the document whose state says what that call left, and, where that
  document's own sentence would say nothing about today, one that does. It used to be worked out from the
  document the day needs, or else the day before
- **The game says what it is before its name.** The page's heading is "A game: run a ninety-day AI
  project." above "Ninety Days, the SkyWays simulator" (`what`); the opening lines name the fictional
  airline, the AI assistant, the ninety days and the thirteen decisions (`premise`); and the title screen
  opens on `pitch`: a game takes ten to fifteen minutes, and every decision shows its price in days before
  it is chosen. `game.js` reads `pitch`, and `pages/play.py` the other two
- **A question about a colleague's plan shows the evidence.** In one role, and for the sponsor, every plan
  now offers "Ask to see the evidence" while questions are left, sound or not, so the offer gives nothing
  away; the sponsor's used to appear only when the plan was not the method's. Asking (`ask` in
  [`site/play/sim.js`](site/play/sim.js)) costs one question whatever it shows. It shows the document the
  plan works from and whether it is on file, and what the plan would put on file; on Day 90, the slide as
  planned. It never says what the plan costs later. Then the player lets the plan stand or asks for another
  option at no further cost, and the sponsor chooses what to send the team back to do. Before, a question in
  one role opened the other options with no evidence and was spent only on a change, and the sponsor's sent
  the team straight to the method's option
- **Two rules in `sim.js`.** An option that opens a hands-on task files its documents when the task is
  done, not when the option is pressed. And the verdict's saving follows the run: every day late is a day
  the assistant was not live, out of the 45 between Day 45 and Day 90, and a kind of case that went live
  below its bar, or before it was proven, was done again by people
- **The workbench is dark by default**, like the manual, and shares its theme setting (`manual-theme`), so a
  reader who chose light in the manual gets light there too. Its page title is "The SkyWays workbench", and
  "SkyWays Architect" is gone from its metadata, its frame and its contact subject line
- **The workbench has its own top bar**: the mark, its menus with the tutorial at the head of the Learn
  list, the search, the evidence pack, a quiet link to the manual, one filled pill to the game and the theme
  toggle. So the frame no longer adds a strip above the tool or a Manual pill to its bar, and the footer
  still links back to the manual. The mascot, the ranks, the points counter and the exploration card are
  gone
- **Fewer sketches, and each carries its own paint.** 77 in 48 lessons, down from 98 in 52, cut by the two
  tests of removal in the folder's [README](site/content/learn/sketches/README.md): take the worker out, and
  take the sketch out. Every mark now carries its paint as plain attributes, so a sketch still looks right
  when the stylesheet is missing, late or an older copy
- **"Manual" for "playbook"** where the lessons name this site: "this playbook" is "this manual" in their
  text and their sources tables. "Playbook" stays where it means a playbook

### Fixed
- In the workbench's dark theme the hard gate's label (`.xrt-gl.hard b`, and three more selectors that share
  its rule) was mixed from a fixed 86% of the gate's red and read at about 3.5:1. It now mixes at the theme's
  own strength (`--ht`), as the workbench's other coloured labels do, and clears 4.5:1

## 2026-10-02 · Pictures that explain, a hero that moves, and screens that stand alone

A fifth council (five advisors, five reviewers) set this round; its record is in
[`site/EXPERIENCE.md`](site/EXPERIENCE.md) and, for the game, [`site/GAME.md`](site/GAME.md).

### Added
- **Hand-drawn sketches in the lessons.** 98 of them across 52 lessons: one metaphor on a sheet
  of paper, a small black worker doing the thing the paragraph just said, a few handwritten notes, a caption in
  real type. Drawn in code by [`site/pages/sketch.py`](site/pages/sketch.py) from one file per lesson in
  [`site/content/learn/sketches/`](site/content/learn/sketches/), placed with `{{sketch:name}}`. The build checks
  that no metaphor is used twice, that handwriting is 13px or more on a phone, and that every sketch has a caption.
  The style is adapted from Ian's Xiaohei illustrations (MIT), credited in the folder's README
- **A funnel in the lifecycle figure.** Four methods each give the SkyWays PDLC one idea; four lines run into one
  point, and the P0 to P3 loop is drawn out of it. The caption says the methods stay: you still pick one
- **A top-bar slot that knows where the reader is.** It never points at the page it is on. In the manual it offers
  the simulator; in a lesson, "Play this day" when the game has a day that lesson is the reading for, and "Apply
  it" beside it; in the game, the lesson behind the day on screen. Between pages the pill's shape travels and its
  words swap
- **A sixth task in the game**, on Day 6: which of six "musts" can nobody move inside ninety days
- **A link to each day of the game**: `/simulator/#day-45` opens Day 45 with the earlier days played by the book,
  and never overwrites a run in progress
- Four more passes in [`site/tools/accept.mjs`](site/tools/accept.mjs): a 320px phone, print, the top bar, and
  the hero (one switch holds every looping animation; the globe's drawing stays inside its budget with the
  processor slowed four times; the page does not shift as it is scrolled)

### Changed
- **The hero.** The globe is blue, turns once a minute and is drawn on every frame (it was once in four minutes
  at thirty frames a second); its dots are filled in a dozen passes instead of thirteen hundred. The flight is a
  thick ribbon in the phase hues, and its way back climbs behind the globe, so the next round starts one level
  up: a spiral. The aircraft is a paper dart in P0, a plan in P1, an airliner in P2 and a jet in P3, and each
  phase's label carries its aircraft. The entrance plays once in a sitting
- **"Sign-off" for "hard gate"** on the home page and in the game. The lesson keeps its name, and the legend joins
  the two
- **The home page's words.** One heading and one short paragraph per band, in plain sentences. No heading starts
  with "Or"; "spine" is gone from the page; the table's last row says what this manual adds in words a newcomer has
- **Every day of the game opens cold**: a headline that is a sentence, one line of where the project is, and a
  "So far" line that quotes the earlier call today depends on
- **The game has colour**: each room takes its owner's hue, and the sky outside tells the phase, from dawn to dusk
- The home page's tutorial band shows one sketch from a lesson, as a sample, and its simulator band shows three
  moments of the game in turn (Day 1 at dawn, Day 45 in the afternoon, Day 90 at dusk), with a pause control
- "AIDD" is spelled one way everywhere, the workbench included

### Fixed
- On a 320px screen the floating mail button no longer sits on a line of the game's dialogue

## 2026-10-02 · The simulator is a game: Ninety Days

The simulator was a reference tool to read. It is now a simulation to play, and the tool is kept behind
it as the workbench. A council of five advisors and five reviewers set the direction; the record and the
rules are in [`site/GAME.md`](site/GAME.md).

### Added
- **Ninety Days**, at `/simulator/`. Thirteen dated days stand for the ninety. Each day is a short scene,
  one call with its price in days shown, and on five days a hands-on task. A shortcut leaves a sealed
  debt on a later day, which comes back with the player's own choice quoted. Doing everything properly
  does not fit the runway, so the date has to move once, and moving it with documents on file costs no
  trust
- **Three ways to play**: the whole team; one role, with four questions to ask of colleagues who have
  habits of their own; and the organisation, where the sponsor picks three rules and watches the days run
- **A head office drawn in code**: seven rooms on four floors at night, a cast of twelve, the day's room
  lit and shown close up, walls that show the state of the build. No image files. Everything read or
  pressed is page text and real controls; the canvases are hidden from a screen reader
- **One thing nobody asks about.** The refund limit sits in the prompt from Day 30. Looking in on the
  Platform room shows it. On Day 82 the refund is refused, or paid
- [`site/tools/sim.test.mjs`](site/tools/sim.test.mjs) walks every path through the rules, and
  [`site/tools/playtest.mjs`](site/tools/playtest.mjs) plays every mode to its verdict in a browser

### Changed
- **The earlier tool is the workbench**, at `/workbench/`, unedited apart from its two planes, which now
  face the way they fly. **Breaking for deep links only in name:** every `/simulator/#/…` and `/#/…` route
  is forwarded to `/workbench/#/…` before the page paints, so bookmarks and the wiki keep working
- The home page's simulator band shows the game, and links to the workbench beside it. The menu, the
  Library list, the footer and the search index carry both
- The acceptance gate includes the simulator and asks its canvas how many frames it drew: none under
  reduced motion, and a pause control whenever it moves

---

## 2026-10-02 · The reason first, then the spine, then the methods on it; extended BMAD

The strands figure that replaced the method table was harder to read than the table. Both ideas are kept,
each in its own picture.

### Changed
- **A band that says why.** "Agent projects fail quietly. A phase ended on a date instead of on evidence."
  Under it the SkyWays PDLC as one line that closes into a loop: above the line the question each phase
  asks, below it the line a team hears when the question was skipped, each from that phase's own lesson
- **The method table is back**, with its bars in the phase hues and each name beside its row. Its last row
  is no longer a fifth bar: it is what the spine adds in each phase that no method carries
- **Extended BMAD.** BMAD's last step, "learn and adjust", is run here as a Run & Learn stage with three
  hand-offs: QA's drift report, the product manager's two-number report, and the incident written up as
  the next brief. It is this manual's extension and is marked as one wherever it appears: a hollow bar in
  the home page's table, a cell on the frameworks page's plug board, a part in the merge figure, a section
  and an FAQ entry in the BMAD lesson, and the BMAD row of the "one lifecycle for every method" table

---

## 2026-10-02 · Many names, one spine: section two redrawn, and dark by default

A third council judged a request for a new home section: the method names a reader has heard, resolved
into one roadmap. All five advisors said to rebuild section two and add no band; the reviews changed how
it is drawn. The record is in [`site/EXPERIENCE.md`](site/EXPERIENCE.md).

### Changed
- **Section two is one figure.** The SkyWays PDLC is a thick line in the four phase hues that closes into
  a loop, with a station at the start of each phase, the hard gate before the third and the four phase questions inside. AI-DLC,
  BMAD, spec-driven development and AIDD are thin neutral strands beside it: solid where a method has a
  stage, dashed where it touches the phase. The table it replaces drew AI-DLC and the SkyWays PDLC as the
  same bar; the lifecycle and a building method now have different marks
- **The heading answers with the lessons' own answer**: whichever method fits your team, on one spine
- **The question and its picture share one screen** at 1440 by 900: the paragraph sits beside the heading
- **On a phone each name sits beside its strand**, the spine comes first, and the four questions are a
  list under it. Under 600px the methods' one-line glosses are dropped and the gate is a bar, named in the key
- **Three ways in, as one sentence**: "Start from the job you do." "Or play the ninety days yourself."
  "Or learn it in order." The tutorial band now shows its eight tracks; the shelf keeps four tiles
- **Forward deployed engineers have a row** on the home page, and anyone not on the list gets one link to
  the tutorial's nineteen starting points
- **Dark is the default.** A page opens dark whatever the system setting; light is chosen with the toggle
  and remembered. Printing always uses the light theme
- **One name, said once.** The first lesson and the tutorial's start page now say that the SkyWays PDLC and
  the agentic PDLC are the same lifecycle; the method page says so in its first line. The home page's title
  no longer says "every agentic PDLC"
- The terms lesson answers "What about the agentic STLC?" and points to the QA lead's eight steps
- The frameworks page sits under Libraries in its breadcrumb, and its kicker names what it holds
- The footer says the worked case is set at a fictional airline also called SkyWays
- [`site/tools/accept.mjs`](site/tools/accept.mjs) checks the new figure, including parts hidden by a clip

---

## 2026-10-01 · The inside pages to the same standard, and motion with a job

A second council judged a list of nineteen proposals for the inner pages and for motion. It kept the ones
that take something away or that explain something, and refused the ones that only decorate. The rules it
left behind are in [`site/DESIGN.md`](site/DESIGN.md) under Motion, and there is now a gate that checks them:
[`site/tools/accept.mjs`](site/tools/accept.mjs).

### Changed
- **Text is out of its boxes.** On the leadership page, the mental models, the track lists and the tutorial's
  tracks, paragraphs sit under a hairline instead of inside a bordered card. Boxes are kept for code, tables,
  diagrams, calculators and verdicts
- **The leadership page keeps your place.** Its thirteen sections are numbered, spaced, and listed down the
  left on a wide screen with the current one marked; on a phone the list folds under the title
- **A role step is one surface.** Its table, artefact and example are ruled instead of boxed, and its head
  links straight to its template and its prompts. "Expand all" moved beside the steps' heading, and on a phone
  the page opens on the role's name instead of a strip of step names
- **Every reference page ends on one way on**: templates, prompts, mental models, frameworks, the picture pack
- **Reading text stops near 75 characters a line** in lessons, whatever the column's width
- **Words a stranger trips on.** "P0 to P3" is introduced as four phases and linked to the method where a
  leader first meets it; "PDLC" is spelled out on the home and method pages; the mental models say that
  SkyWays is the fictional airline the manual works through
- **The share image for the home page is the home page**: the headline beside the Earth and the flight. Every
  card now carries the mark, and the method page has its own

### Motion, each with a reason
- **One page hands over to the next.** Where the browser supports it, pages cross-fade with the top bar held
  still, and a lesson's title travels from its row in the track list to the head of the lesson; a role's name
  does the same from the home page
- **Things that are sequences arrive in order, once**: the hero's words, a role's eight steps, the four
  methods drawing along the phases, the parts of a figure the first time it is scrolled to
- **A step opens to its height** on a wide screen; **Copy draws a tick** and tells a screen reader
- **A pause control** on the two things that keep moving, the hero's flight and the tower on the method page

### Removed
- **Perpetual motion.** Diagram connectors marched forever at 1.1 seconds, off the site's own duration scale
  and with no way to stop them, and the guide blinked and pinged on every page. Connectors now move only while
  the reader scrolls past them, and the guide blinks when it is reached for

### Fixed
- **What an earlier dash sweep left behind**: ten "yours to own" and "not yours" lines at the top of four role
  pages read "The **expansion** gate) have we earned wider use?"; four maturity levels and two table cells on
  the leadership page had the same damage. Each is a lead and its gloss again, joined by a colon
- The rail marked the section before the one you jumped to, because an anchor was offset twice; it now marks
  the section whose top last passed the upper third of the window
- "Copied" made the copy button grow to twice its size for a second and a half (it shared a class name with
  the step's "Done when" box)
- A QA step said it happens in P0 under a P1 badge; it is P1
- The hard gate lesson's summary line read as if three hand-offs halt the build; it is three decisions at one
- The hover titles on a step's phase badge had lost their punctuation in an earlier sweep
- A page opened in a background tab could arm its scroll reveal with no clock running; it no longer arms there

### Refused, on purpose
- Numbers that count up, cursor spotlights and glows, a circular theme reveal, hub cities and extra arcs on the
  globe, text that slides in on reading pages, and a second drawing of the role route

---

## 2026-10-01 · The front of the site, rebuilt around one screen

The home page was doing the whole site's job several times over: it explained the method five times,
offered five ways to pick a role and listed its inventory three times, in about 2,500 words. It is now
six bands and about 600 words, 5,800px tall on a desktop where it was 7,300 and 7,000px on a phone where it
was 15,500. The plan came from a five-advisor council with anonymous peer review, and from two benchmarks:
ten product home pages and seventeen manuals, courses, libraries and simulators. The rules that came out of
them are written down in [`site/DESIGN.md`](site/DESIGN.md) and [`site/EXPERIENCE.md`](site/EXPERIENCE.md).

### Changed
- **The hero.** "One manual for building software with AI agents", one sentence on what is inside it, two
  buttons, and one line of counts signed by the author. Beside it, a dotted Earth turns once every four
  minutes with one flight around it: four legs in the phase colours, P0 to P3, and the hard gate between
  design and build. The globe is a canvas drawn from a lattice built at build time, with no library and no
  download; it stops off screen and is drawn once for a reader who asked for reduced motion
- **"Which agentic method should your team follow?" is section two, and it is answered.** Four methods as
  bars along the four phases, the SkyWays PDLC as the whole line, in a real table
- **One way to pick a role.** Six rows, five roles and the sponsor, each reading from where you start to
  where you end up. The nine chips, the five cards, the matrix and the start table are gone from the home page
- **The simulator is shown as itself**, its own opening screen in a frame, with one button
- **A name and a mark.** Every page carries the SkyWays ring and plane, the same mark as the simulator, with
  "The agentic manual" beside it. The top bar went from twelve links to five places and the simulator; Roles
  and Library open as short lists, and the drawer still holds every page and the search
- **Landing pages open on their content.** A page's name, one line and a row of counts. The "For / Use it to
  / How" strip is folded behind one line, the "On this page" boxes and lists that repeated the side rail are
  gone from the role and library pages, and nothing pops up on arrival: the walkthrough is a small button,
  bottom left, on wide screens only
- **The tutorial's landing page leads with its eight tracks** and two buttons: start with lesson one, or
  start from your role
- Headings on the leadership, mental models, picture pack and role pages lost their stock phrases

### Added
- **[`/method/`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/method/)**: the SkyWays PDLC on one
  page. The phase board, the eight loops, the role by phase matrix and the delegation board, each under the
  question it answers

### Moved, with the old links kept working
- The four boards kept their ids. Links to `/#pdlc`, `/#loops`, `/#by-role` and `/#delegation` are forwarded
  to `/method/` by the home page, as the simulator's old routes already are

### Fixed
- The phase label over each group of steps on a role page was pinned to the top left corner of the window,
  because its class name was also the reading-progress bar's. The labels now sit over their groups
- A visually hidden column label inside a scrolling table widened the frameworks page by 12px on a phone
- A track page on a phone opened with the whole lesson list above its title; the list now starts folded there,
  as it already did on a lesson
- The closed contact drawer's shadow drew a grey band down the right edge of every page
- Text on a solid hue (the role-step phase tags, the prompt posters' headers, two board captions) takes the ink
  made for it in both themes; several of these sat near 3.8:1
- Pressing `/` now lands on the search box every time; the drawer's first link used to take the focus first

---

## 2026-09-25 · Geist, and pages that open in the right mode at once

### Changed
- **Body text is Geist, code is Geist Mono; headings stay Instrument Sans.** All three are served from this
  site as one variable file per family instead of the Google Fonts stylesheet, which was a render-blocking
  request to a third party on every page. The two faces the first paint needs are preloaded
- **No more flash of the other theme.** A reader's saved theme is applied by a two-line script in the head
  before the first paint. Until now the deferred script applied it after the page had already painted in the
  system mode, so a light-theme reader on a dark system saw every page open dark for a moment
- The frame stylesheet moved from the end of the body into the head, so nothing is restyled after it appears

## 2026-09-25 · Every page checked against the writing and design skills

### Changed
- **No dashes in prose anywhere on the site.** 1,358 em and en dashes across the 64 lessons, the five role
  journeys, the leadership page, the mental models and the frameworks data became commas, full stops, colons or
  parentheses, chosen by what the dash was doing: a paired aside becomes commas, or parentheses when it holds a
  list; a dash after a short lead becomes a colon; a dash before a new clause becomes a full stop; a numeric range
  reads "1 to 15". Dashes that are data, an empty table cell, stay
- **Contrasts and stock words.** "The platform question is not different in kind. It is different in when" and
  "the decision is not which assistant, it is that…" now state the point; "leverage" and "deep dive" are gone
- **Measured design rules.** Every transition on the manual sits on the motion-token scale (150, 250, 350 or 400
  milliseconds) with the smooth-out easing; every tap target on a phone is at least 44 pixels tall, including
  copy buttons, the theme toggle, the menu, the drawer's groups and links, the tour buttons and the stepper dots;
  no label is under 11 pixels

### Kept on purpose
- The interview banks' "The insight" and "Red flag" labels and the glossary-style definition lists: labels that
  carry structure, not decoration
- Contrasts that correct a real belief, such as "show blocked decisions, not just blocked work"
- The body font, Inter, which the taste skill would replace; changing it is a visible design decision, left to
  the author

## 2026-09-25 · The home page in plain sentences

### Changed
- **The hero asks one question and answers it in two sentences.** "Which agentic method should your team
  follow?", then: the four named methods each cover part of the product lifecycle, and the SkyWays PDLC joins
  the best of them into one method, P0 to P3, that this manual shows every role how to run. The by-line and
  its bold labels are gone; the chair list reads "Start from your chair"
- **Every card and strip on the home page reads as a sentence** with its own shape, instead of a fragment, a
  colon and a list repeated six times; the footer loses its dash
- Copy on this site is now checked against the humanizer and no-ai-slop writing patterns, and layout and
  motion against the taste, UI/UX and transitions skills, before it ships

## 2026-09-25 · The simulator's last cleanups, and the two sites pointing at each other

### Changed
- **The concept map reads at Fit.** Eight loop panels packed into three columns under a legend bar, one
  concept per row, every name visible at the default zoom in the map's own pane; lines carry the colour of
  the loop they start in, and hovering a loop or a concept lights its lines
- **The walk-through's parts.** The button that moves to the next part is now distinct from "Next scenario"
  and says which part it opens ("Move to part 2 of 10 · Choose the method"); every part carries its own
  part number with previous and next buttons under its title; the ten-stops strip wraps its labels instead
  of clipping them, and drops to two rows of five below 1500 pixels
- **The context layers as nested sets.** Shared holds Domain holds Product holds Task, tinted by depth, with
  what each layer reaches; the "who inherits" exercise highlights the nested sets, and the new-product
  scenario shows the same picture
- **Learn is now Tutorial** in the manual's nav, crumbs and the simulator's manual menu; the address stays
  `/learn/`

### Added
- **Under the manual's hero:** "Prefer to learn by playing?", with the simulator as a button
- **Under the simulator's hero:** "Prefer to read?" to the manual and "Want to learn it like a course?" to
  the tutorial

## 2026-09-25 · Every page, for the reader in front of it

### Changed
- **The hero asks the question the site answers.** "So many agentic methods. Which one should your team
  follow?", then the one-stop answer and the SkyWays Consultancy line. The chair list closes its sentence,
  Pip sits under the picture, and the stats band answers "What is on this site?"
- **Board keys span the row.** The key under each home board is now a strip: a label and cells that share
  one line, instead of a column beside the title that left blank paper above the heading
- **Mental models, rewritten for readers.** Twelve imperatives ("Keep every chain of model steps short",
  "Gate by reversibility, not by accuracy", "Put every hard limit in code, not in the prompt") in place of
  slogans. Every card now shows, in order: in plain words, the SkyWays case, what it predicts, the mistake it
  prevents, the subtlety, and the test. Cards are tinted by the cost of ignoring the rule, yellow to red, and
  every "where it does its work" link opens in a new tab. The toggle that hid half of each card is gone
- **Templates, with a way in.** The page opens with what the templates are for, how to use one in three steps,
  and a pain register filled in for SkyWays. Every template carries its phase badge, P0 to P3, and a block
  saying when to use it, what you produce and who owns it, where to start, what good looks like, and the step
  that explains it. Role sections are titled plainly and link to the role and to its prompts
- **The leadership page, written for executives.** For the C-suite, entrepreneurs and business owners: why
  the economics and the risk moved; five things that change; every team transformed, function by function,
  with the effort level it needs and the gain to expect; where the money is, efficiency or cost or both; what
  the four frameworks mean in leadership terms; LLMs across the board at three levels; and the ninety-day
  rollout. Every claim shows what it means and how it works side by side; nothing sits behind a toggle
- **Role pages.** "Yours to own" is tinted green and "Not yours" red; the head pairs with its counts; the
  read-next list is a row of cards
- **Every link into the wiki opens in a new tab**, so a reader keeps their place in the manual
- **Layout, measured.** A page audit flags any block that sits alone in its row with content under 72 percent
  of the width. Home, models, templates, prompts, pictures, frameworks, the roles and leadership all pass at
  1440 and 1100 pixels; the footer no longer floats below a quarter-page of empty paper; the closed contact
  drawer no longer widens the page at some viewports

## 2026-09-25 · The home page, re-swept

### Changed
- **Every head spans the row.** The home page's four boards open with two columns: the title and thesis on
  the left, a boxed key on the right (what the hard gate is; the eight loops named as chips; how to read the
  role chart; why the red column comes first). The notes that used to sit under the boards, half a page wide
  with nothing beside them, are folded into those keys. The stats band is a six-cell grid across the page
- **The spine is named.** "P0 to P3: the SkyWays PDLC loop", four phases that run as a spiral rather than a
  line. Each phase header is a link to its lesson, shows a hover card that says what the phase decides and
  what you leave it with, and carries its key in a larger size
- **The loops board says what the picture shows.** "Eight loops that run every team's workflow, P0 to P3":
  five carry work forward, three bring production back, and the key lists all eight with their phases
- **The hook band's photo is a scene.** An animated control tower: four planes fly a loop of four runway
  segments, P0 to P3, past one hard gate, under a radar sweep. Reduced motion stops everything and keeps the
  planes in place; a browser without motion paths hides them rather than piling them in a corner
- **Copy in full sentences.** "Three ways you can use this"; the running case and the lifecycle line as two
  cards; "Pick the chair you sit in" in one sentence with no unexplained ninety days; the six library cards
  benefit-first (templates you can use today, prompts you can paste into your LLM, the SkyWays PDLC
  Simulator, how to invest in AI projects, pictures that explain agentic concepts, the methods merged and
  written down). "What this is, and what it is not" is gone; the sources link stays in the footer
- **The frameworks page, rebuilt.** The four-methods picture first; every section head paired with an aside
  (the simulator links, what the SkyWays PDLC adds, the three lineage pills); headings as sentences ("Why long
  chains of steps fail, and what to do about it"; "Where each framework came from, and how much to trust it")
- **The footer** credits SkyWays Consultancy for both products, conceptualised and built by Akash Das, and the
  dead space under the simulator's footer is gone

### Added
- **How the four methods merge into the SkyWays PDLC**, a new picture on the frameworks page and in the pack:
  the parts of SDD, BMAD, AI-DLC and AIDD placed in the phase each serves, flowing into the spine, with the row
  of devices the SkyWays PDLC adds
- The tower scene and the merge picture in the picture pack; the four boards re-captured with their new heads

## 2026-09-25 · The picture pack

### Added
- **The picture pack** at `/pictures/`: every diagram of the method and the simulator as an image, with a
  title, a caption, alt text, the page it comes from, a download, and light and dark versions. Six groups:
  the method, roles, decisions and how-tos, lesson maps, the simulator, posters. The page carries an
  ImageGallery of ImageObjects with licence, creator and credit, and the sitemap lists every picture under
  it, so image search can find them. Linked from the menu, the home page and the mental models page
- **Two posters on the prompt templates page**, also in the pack: "The anatomy of a prompt template" (the
  job, the inputs, do, the output shape, then the check, with one prompt taken apart) and "116 prompt
  templates, five roles, one glance" (every role's steps with the prompt each ships with)
- **The simulator's pictures** captured for the pack by `site/tools/simshots.mjs`: the flight plan, the line
  or the loop, the spine, the methods, the roles, the three efforts, the same task three ways, the concept
  map, the Loop Map and the gates
- The screenshot sheet now captures every registered picture, not only the ones a lesson embeds

## 2026-09-25 · Search and assistant discoverability; prompt templates

### Changed
- **The sitemap dates each page by the commit that last changed its sources**, not by the day it was built,
  so a page that did not change no longer claims it did. The Pages workflow fetches full history for this
- **SkyWays Consultancy is the publisher** in the structured data on every page and the site node; lessons
  carry dateModified and their own social image; every page has og:image:alt and links an Atom feed of the
  lessons at `/feed.xml`
- **"Prompts to paste" is "Prompt templates"** in the menu, the page and the search index
- **The contact form sends `subject` and `from_name`**, the fields Web3Forms reads, alongside the ones it
  already sent

## 2026-09-25 · The manual's home and role pages, polished; the contact button; back to top

### Fixed
- **The contact button on both sites showed as an empty circle**: its envelope was hidden on desktop by a
  phone-only rule. It is a navy button with a white envelope now, and grows its label on hover
- **"Where the model helps, and where it must not" laid its lanes out wrongly**: the lanes' container shared
  the class of the rail links, whose numbering pseudo-element became a grid cell and pushed the three lanes
  out of place, leaving beige gaps. The container has its own class; the three lanes sit across each band
- **On the mental models page the picture pinned to the top while its text scrolled**, and the reading
  switch sat far away in a bar at the top. The picture scrolls with its card, and every card carries its
  own "The model / The subtlety" switch; the bar no longer floats
- Four page descriptions were over the length search engines show in full

### Added
- **A back-to-top control** at the bottom left of every page on both sites, appearing after the first screen
- **A hook band after the first scroll of the manual's home page**: "Agentic product development, reimagined",
  the positioning line, and a licensed photograph of a control tower with its credit; and a hook line,
  "Your all-in-one agentic PDLC", above the PDLC board
- **The role pages open with a roadmap**: "Your eight steps, in the agentic era", the steps grouped by the
  phase each belongs to, with an icon per step and a line that says the job has not changed
- The loops board is titled "Eight loops: the feedback that turns four phases into a cycle"
- A robots meta tag asks for large image previews and full snippets

## 2026-09-25 · AA contrast and labels on every route

### Fixed
- **Every route of the simulator now passes axe at WCAG AA**, checked in one sweep over all twenty routes. Before,
  twelve failed: hue colours used for small text (step numbers, lane labels, phase badges, kickers, the
  playbooks' "on Monday" headings, the learn path's unit numbers, the compare page's spine, the guide's paths,
  episode principles) and hue badges under white text (chosen chips, phase pills, figure numbers, slot
  numbers). Each is darkened by a fixed mix towards navy at the rule that wins for it, so the hues stay
  recognisable. Six range sliders on the playbook pages have labels; the episode slot labels are headings, so
  the order no longer skips a level; four number columns have a hidden header
- The previous entry's claim that the governance and loop map pages were clean was wrong; they are now
- **Two layout faults found on the way**: the compare page's spine drew its four phase headers as tall grey
  boxes, because the `ph` class also names the phase cards elsewhere; and on the process page the lane labels
  ("Draft it with a model") wrapped into four lines in a 43px column, because the bold line beneath sized the
  header's first column. Both read as intended now

## 2026-09-25 · Three efforts, one method

### Added
- **"Which agent, for which task"**, a new page under Practise. An agent is not one thing: most tasks deserve a
  chat, some a platform, a few code, and the method scales with the effort. The page lays the three tiers
  side by side (who builds, time to a result, what you build it with, what it fits and is not for, how much
  of the SkyWays PDLC applies, and the tricks that make each tier work), shows one task built three ways,
  decides a task of yours in five questions, and sets a scored exercise: six departments, six tasks each,
  with the reason and the trick behind every answer. A first-try answer pays three points on the flight plan
- **A "Three efforts, one method" strip on the simulator's home page**, after the method, with the three
  tiers and a way into the exercise

### Fixed
- Table headers that were empty, and card headings that skipped a level, on the evidence, governance, loop
  map and episode pages

## 2026-09-25 · Every page says what it holds; every tool says how to use it

### Changed
- **Page heads in three cells.** The opener under every page title now reads as "What is here", "How to
  use it" and "You leave with", each with an icon, the jump chips under the first and the numbered steps
  under the second; the bot and "Show me around" stay beside them. Eighteen pages carry a "leave with" line
- **Every tool has "How to use this tool"**: a button under the tool's introduction opens what it is for and
  which phase it belongs to, three steps, and the worked example: the SkyWays inputs the tool opened with
  and how it read them, with a button to put those numbers back after you have typed your own
- **The evidence page fills its width**: a hand-off strip at the top (what you hold, and the four hand-offs
  with how many artefacts each owes and where they come from), your pack under it, and the four artefact
  tables in two columns

### Fixed
- In the governance page's gate scene the "placeholder · owner · date" chip crossed the lane's title

## 2026-09-25 · The simulator's home page tells the method in order

### Changed
- **"The method, in order"** replaces the three pictures. It reads top to bottom: a traditional lifecycle as a
  line beside the SkyWays PDLC as a loop, with the five published methods drawn plugging into the loop where
  each speaks; why the field has no standard and what this one proposes; the four phases as a strip with the
  gates between them and what each leaves you with; where each method sits on the spine; and who does what,
  where every chip now carries the step it opens ("Problem in three numbers" reads "State the problem in
  cases, minutes and money" underneath)
- **"What you will be able to do afterwards" is six tabs, one per role**, with that role's four outcomes, a
  route button and a link to its playbook, instead of six cards of text
- **Your route has its own page.** The boarding-pass router and the guided path moved to `#/route`; the
  hero's "I am" chips, the rail and the walkthrough links go there, and `#/start/<role>` forwards to it
- **"Why an airline on its worst day" moved to the story page**, where the worked case is introduced, with a
  rail entry

### Fixed
- Contrast on the figure title pills, the roles grid headers and the chosen outcome tab

## 2026-09-25 · The worked case as a flight plan

### Changed
- **The ninety days are named for what they are**: the worked case. Every idea in the simulator is shown on
  one product, an airline's rebooking assistant, and thirteen days of it are worked in full. The home page,
  the story page, the menu and the tours say so
- **The tower is a flight plan.** The route reads P0 to P3 left to right on a desktop and top to bottom on a
  phone, under the sky with the plane and the sun; the four legs stand on the runway, the gates between legs
  are drawn and labelled, and the control tower is Day 90 at the end. One renderer serves the home page's
  compact panel (thirteen stop chips, side-quest counts, your rank and progress) and the full route page
  (each stop with its opening line, the side quests on each leg). The rail lists the route from the runway
- **The route page** adds "Around the airport" for the five places off the main line, draws the three ways
  to fly instead of describing them, puts the gates in their own section, and makes every entry in the key
  a link: the cast open their playbooks, the legs their part of the route, the marks their reference

### Fixed
- Three role headers in "Who does what, when" and the amber phase pills failed contrast; the soft-gate badge
  is a darker green

## 2026-09-25 · SkyWays Consultancy, the PDLC Simulator, and a nav that says what it is

### Changed
- **Positioning.** The manual and the tool are products of SkyWays Consultancy: the framework is the SkyWays
  PDLC and the tool is the SkyWays PDLC Simulator. The tool's brand, title and footer say so; the hero on both
  home pages carries the line "the best of every agentic way of working, in one operating model"; the manual's
  nav link and buttons say Simulator; the disclaimer says the worked case is set at a fictional airline that
  shares the name
- **The Manual link sits at the right end of the simulator's nav**, where the manual keeps its Simulator link,
  and Home comes first. The strip above reads as one sentence
- **Menus and pills say what they are**: "By role" and "Resources" replace "Roles" and "Reference"; the Pack
  pill says "Evidence pack" and the star says "Points"; Search and Copy link are icons only
- **The nav's tiers were re-cut** after the labels grew, and it fits at every width from 901px to 1920px

### Fixed
- **Switching the hero between light and dark made it vanish**: the rebuild looked for a block the climb had
  replaced. It anchors on the climb now

## 2026-09-25 · The home page, shorter, and checked on a phone

### Changed
- **The six tiles under the hero are gone**; the hero's buttons and the climb cover their destinations, and
  the desktop page is a screen shorter
- **On phones the six role rows of "Who does what, when" and the six cards of "What you will be able to do"
  open on a tap**, the first of each open by default, with a hint line and a chevron; chips sit left-aligned;
  the method marks and the rail strip's links are touch-sized. The phone page is 2,500px shorter and
  nothing overflows

## 2026-09-25 · The roles and the methods, readable

### Changed
- **"Who does what, when" and "Where each method plugs in" are HTML grids on the start page**, not scaled
  drawings: 13px chips and cells that wrap, real links on every chip, the hard gate drawn between P1 and
  P2, and on phones a stack per role and per method with the phase named above each group and the silent
  cells left out. The drawings themselves were also redrawn larger for the process and compare pages, and
  the one remaining drawing on the start page, the traditional-versus-agentic picture, scrolls sideways on
  phones instead of shrinking to nothing

## 2026-09-25 · The playbook's front: the hero back, a nav that fits, a tower that starts on the ground

### Fixed
- **The start page had lost its hero, its six tiles and its ninety-days timeline** since round three: a
  wrapper that adds icons to the role cards looked for an `h4` that the heading-order fix had turned into
  an `h3`, threw, and the page's error handling logged it to the console and carried on with the fallback
  lede and the episodes table. The wrapper accepts either heading; the verification now reads console
  errors on every route, not only thrown exceptions
- **The top nav overflowed at every width between 960px and 1600px**, by up to 264px, and cut off its
  last controls. It now yields by tier: the tagline goes below 1700px, the Search, Concepts and Copy
  labels below 1440px, the Home and Manual labels below 1300px, the Pack label and the Copy button below
  1100px, the Concepts button and the Contact label below 1024px, and the phone menu takes over at 900px.
  The Pack and Contact controls carry icons so their labels can go
- **The Manual chip lost its icon below 1300px** along with its label; the icon always shows

### Changed
- **The tower opens on the ground floor.** On a desktop the tower sits in a viewport that starts scrolled
  to the ground, so P0 is the first floor you meet; climbing is scrolling up inside it or taking the lift
  beside it, which also shows which floor you are on. The rail lists the floors from the ground up and its
  links scroll the tower. On phones, where the ground was already first, the page scrolls as before and
  the lift is a row above the tower
- **The ninety days sit on the home page as a climb**: a compact tower with the thirteen rooms on their
  four floors, each floor's side-quest count, the ground floor's "Begin at Day 1", and your rank and
  progress beside it. It replaces the second lede and the episodes board; the rail and the tour say
  "as a climb"

## 2026-09-25 · The walkthrough on phones, and a build that runs on the system Python

### Fixed
- **The walkthrough's column grew with its widest content on phones**: a two-button segment, a code sample
  or a four-column table pushed the column past the viewport, so situation boxes and tables were clipped at
  the right edge on eight scenarios. The column is now capped at the viewport (`minmax(0,1fr)`); tables
  scroll inside their box; code samples scroll inside theirs
- **The "full architecture cycle" scenario lost its Review step's tier segment** on every width: the segment
  was generated with the id `w7tr`, the same id as the step trace, so the trace overwrote it. The trace has
  its own id and the Review row can be set again; the page has no duplicate ids
- **The stage strips rule reached every illustration in the tool**; it is scoped to the walkthrough's
  stages. On the learn page the progress block, on the guide page the cheat-sheet tables and a ledger
  value, on the engineering page a JSON sample, and on the toolkit the hidden selects behind the quick-fill
  segments no longer reach past a phone's viewport
- **`site/build.py` ran only on Python 3.12+** because two f-strings used 3.12-only syntax; the build, the
  wiki checker and the export scripts now run on the system's Python 3.9, and the build says so if it is
  given anything older

### Changed
- **Touch targets on phones**: switches are 46×27 and the whole gate row toggles them; sliders have a 26px
  thumb on a 6px track; the scenario tab row is a single strip that keeps the current tab in view; scenario
  padding is tighter; the smallest badges are 11px

## 2026-09-25 · The scenarios speak to your role; the tower's rooms carry their openers

### Changed
- **Every scenario ends with a line written for your role.** The walkthrough's 35 decision scenarios each
  carry four short lines, one per role, grounded in that scenario's mechanic; before, the same stage-level
  paragraph repeated under every scenario. The stage's "Your Monday" list is shown once, as a card under the
  deck, with a prompt to choose a role when none is chosen
- **Situations lead with the situation.** Twelve scenarios that opened with an instruction ("Pick a layer…")
  now open with the state of the world, then the instruction. The role picker and the bring-your-own-feature
  scenario are labelled "Start here" and "Optional" rather than "The situation"
- **The site-map scenario** in the walkthrough's first stage describes the site as it is now: the story, the
  simulations and tools, the playbooks and the reference, instead of a layout the site no longer has
- **The tower's rooms** show each episode's opening line under the title, so a room says what happens in it
  before you enter; the HUD's points line sets the best streak on its own line

### Fixed
- **A ledger question read "How do I get a good write an architecture decision record out of my
  assistant?"**; it now reads "How do I get my assistant to write an architecture decision record well?"
- **The compound-scenario tab** was stretched to a three-column grid, because its class collided with the
  tool's comparison-table class. It is a normal pill again
- **The stage strips on phones** were scaled to a six-point font; they now keep their size and scroll
  sideways inside their card

## 2026-09-25 · Round three: phones, the tower, the scenarios, the last accessibility items

### Fixed
- **Accessibility, the tool's own items**: heading order on the start, simulations, concepts, reference,
  story and tower pages (cards use h3 under their h2; the story and the tower carry an h2); the design ledger
  is keyboard-scrollable; every page's rail is a labelled landmark, as are the tower's wings; the ledger
  score, the role bar, the episode labels, the storey badges, the room day badge, the landing titles and all
  text links pass AA. Axe is clean on the start, concepts, simulations, walkthrough and tower pages
- **The tower's room badges** showed as blank blue blocks: the day text used a colour that matched its
  background. Fixed, with a cleared state on rooms and a "next rank at N rooms" line in the HUD
- **The walkthrough on phones** no longer shows its title twice; **the site's hero picture on phones** no
  longer overlaps its caption with the scroll hint; the orient card stacks below 480px

### Changed
- **Scenarios read as decisions**: a numbered title, a labelled situation, a labelled "why it matters",
  uppercase takeaway labels, pill tabs with a filled current tab, rounded buttons with a forward arrow
- **Simulations on phones** show the walks as a phase list instead of the process map, which was
  unreadable at that width
- **The tower on phones** stacks each floor with its side quests above and below it

## 2026-09-25 · The playbook, taken further: navigation, the map as levels, simulations by role

### Changed
- **The way back sits in the navigation.** The floating "Back to the manual" pill is gone; a Manual chip
  sits beside Home, a first row in the phone menu, and the strip above the tool names its links. The contact
  control is a quiet round button that grows its label on hover; the attribution stays in the footer
- **One pill system.** Every pill and chip shares a height, border and hover; the home hero's role chips
  and the router's chips no longer differ in size
- **The rail groups its links under their phase**, each group a tinted card; the walkthrough's rail becomes a
  sticky strip of steps on phones
- **The concept map reads as three levels**: all loops, a loop, a concept. A click on a loop flies to it and
  the panel lists its concepts; a click on a concept frames it with what it builds on and leads to and reads
  it; a breadcrumb and Esc step back up. Plain scrolling scrolls the page; zoom needs ⌘ or Ctrl. The panel is
  never half empty: at the top level it lists the eight loops with counts. "The same map, read by role" is now
  "By role", as labels, with a button that shows that role on the map
- **The concept dialog has a picture.** The empty state shows the ring of eight loops; a tap on one narrows
  the list. Every concept ends with "Where it sits", the same ring with its loop lit
- **Simulations say what they are.** The cockpit photo is gone. The page opens with how a simulation works in
  four steps, a process map placing all nine walks on the four phases, and the walks grouped by role with
  phase, day, decision count and time. Each walk's card names whose chair you sit in and the phase, explains
  the loop on the first step, letters its options and never overflows
- **The walkthrough has a front**: title, one line, the four role chips and a numbered stepper of the ten
  stops; every stage's role bar carries the chips too, so "change role" never sends you back to the start
- **Reference imagery is larger**; "open" says "Go to it" with an arrow
- **The manual's home page** links straight to Simulations, Toolkit, the Concept map and the ninety days

## 2026-09-25 · The playbook, made foolproof and guided: five UX passes

All in `site/app/SkyWays-Architect.html` (the tool) and `site/frame/`, verified headlessly per pass and on
the live site.

### Fixed
- **Tours** no longer start on their own; a tour locks the page, has an X, progress dots and a count,
  focuses Next, ends on Done, Esc, X, the backdrop or navigation, and cannot be left dangling
- **Every modal** (search, concepts, contact) has the same X in the same place and locks the page behind
  it; Esc and navigation close them all
- **Contrast**: one link colour that passes AA everywhere but dark surfaces; hue-filled badges, segmented
  controls, phase headings, confidence marks and cheat-sheet titles darkened; the frame's footer is a
  labelled section so the tool keeps its single contentinfo landmark

### Added
- **The bot everywhere the tour is**: the opener under each title is Sky speaking, with the page's stops
  as numbered chips that scroll to and flash their target, the how-to line, and "Show me around" with
  its stop count; the hero's tour button carries the bot too
- **Six tiles** under the home hero, one per way in, with icons, counts and a check once visited
- **Quick-fill toolkits**: every short select is a segmented control, every number has a slider sized
  from its own default, Reset restores the SkyWays case, actions carry icons and roles
- **A zoomable concept map**: eight loop panels, every concept a pill, relations as curves; wheel, pinch,
  drag, fly-to-loop, click-to-read in a side panel, role dimming, deep links, keyboard, reduced motion
- **Shapes in the reference**: a drawn shape beside each of the 22 frameworks and in each cheat sheet's header
- **Your exploration**: the guide shows the six ways in with what you have opened and a progress bar
- **Nav and rail**: current section marked, a clearer index, Copy link and Concepts with icons, a larger
  labelled Home, button roles (primary, secondary, ghost, bot)

## 2026-09-24 · The playbook's hidden-menu collapse; icons on the way in and the way back

### Fixed
- **The playbook collapsed to a hundred-pixel column once the menu was hidden.** The tool's own
  `body.rail-off .dd` rule kept a two-column grid while hiding the rail with `display:none`, so `main`
  auto-placed into the empty 0px column. The framed and frameless copies both did it. One CSS rule in
  `site/app/SkyWays-Architect.html` now gives the hidden-menu state a single column and places `main`
  in it; verified on seven routes, menu shown and hidden, framed and frameless. Carry this patch
  forward when the tool is next replaced with a new export

- **With the menu hidden the page hugged the left edge, the tool's "Show menu" button sat under its own
  nav while the strip was in view, and the frame's pills could cover the rail's last link and the footer's
  legal row.** The hidden-menu column is now centred (the same rule in the tool); frame.js publishes the
  strip's visible height as `--sw-top` and frame.css adds it to the button's offset; the rail and the footer
  get bottom padding; the contact pill sits above the tool's bottom-right corner rather than in it. Checked
  with a box-overlap sweep at 2000, 1440, 1280 and 390 wide, menu shown and hidden, at the top, just past
  the strip and at the end of the page

- **On phones both pills are icon-only circles** (a back arrow bottom-left, an envelope bottom-right), 44px
  each, with their labels kept for assistive tech, so the bottom band of a phone screen stays clear

### Changed
- **The way back carries an arrow.** The strip's "Back to the agentic manual" and the fixed pill now lead
  with a back-arrow icon; the strip's manual links end in a forward chevron; on phones the strip stays
  one line
- **Every link into the playbook carries an icon for what it opens** — a calculator, a simulation, the
  gates, the loop map, a comparison, the evidence pack, a role's steps, an episode — drawn as
  currentColor masks in `theme/base.css`, so lessons, role pages, mental models and the leadership page
  get them without markup changes. The focused pointers under the frameworks pictures are now a
  labelled row of chips with the icon and a go arrow; the header's Playbook link uses the same mark

## 2026-09-24 · The wiki reorganised; the way back from the playbook

### Changed
- **The wiki is five sections** — Start, Method and reference, Course and labs, Cohort kit, Community
  and maintenance — and the sidebar follows them. The 55 full lesson mirrors are retired: the tutorial
  lives on the site only, and the wiki keeps a thin index (Start Here and one page per track, each
  linking its lessons) plus the pointer line on every reference page a lesson introduces
- **The playbook has a way back.** Every framed playbook page now carries a strip above the tool
  (back to the manual, plus Learn, Roles, Templates, Prompts, Mental models), a fixed pill at the bottom
  left, and a footer section for the manual. All of it is in the frame layer (`site/frame/`), not the tool
- **Focused links into the playbook** from the manual: each picture on the frameworks page, five mental
  models and three rows of the leadership page's "where to send people" table now open the calculator,
  simulation or governance view that exercises the same idea. One dead link on the mental-models page fixed

### Added
- **The course companion** (`site/course_export.py`) — a wiki page per module, generated from its README
  with every link made absolute, plus the tutorial lesson that frames it, the playbook tool that exercises
  it and where its errors and questions are collected; a hub page; a labs companion with the catalog and
  which module teaches each lab; a marked block in the sidebar
- **The cohort kit** — eight ninety-minute sessions that turn the tutorial into a programme for a team,
  each with pre-reading, a run-sheet, exercises from the bank and the playbook, a decision and homework;
  a session template; the track pages link their sessions
- **Field Notes** and **Roadmap** pages; the wiki-edit backport now recognises every generator and names
  the source from the page's own footer

## 2026-09-24 · A content, search and social pass

Audited against published skills for AI-search optimisation, schema, site architecture and copy
editing (coreyhaines31/marketingskills), and Google's own guidance to write for people.

### Added
- **Search** — a box in the drawer menu, and `/` from anywhere: every lesson, track, role, role step,
  mental model, manual page and wiki page, from a `search.json` written at build time. Keyboard
  through the results; Enter opens the first
- **A social card per page** — 76 1200×630 cards drawn in the site's grammar (`pages/ogcards.py`,
  `tools/ogshots.mjs`), so a shared link shows the page's own title and line, not one generic image
- **On lesson pages**: a copy button on every code block (the ten-minute-workflow prompts), a link
  on every heading, and a thin reading-progress line at the top
- `robots.txt` names the AI crawlers it welcomes; `llms.txt` now indexes the role journeys, the
  reference pages and the playbook as well as the tutorial; the home page carries `WebSite`
  structured data and the author is one `Person` entity, with `sameAs`, on every page; role pages
  link to the lesson for that role

### Changed
- Seven lesson titles trimmed to 60 characters and eleven descriptions to 160, per the house rules
  the build already states; every lesson's date reflects today's changes; "in order to" and
  "utilise" gone from the prose. Nothing else in the lessons was rewritten: the audit found no
  clichés, little passive voice, and a register worth keeping

## 2026-09-24 · The site gets a front door, a guide, and pictures drawn to one grammar

### Added
- **A home page that sets the scene** — a hero that says who the manual is for (forward-deployed
  engineers, product managers and FDPMs, architects, engineers, QA, platform, sponsors, organisations,
  interview candidates) with one entrance per chair, the positioning in one line (every agentic
  delivery method, one manual, by role), the spine drawn as a picture beside it, and a background that
  reads as a system in both themes
- **Pip, the guide** — a small drawn character with a speech bubble on the home page and a
  **walkthrough on every kind of page**: one highlighted element at a time, what it is and what to do
  with it. Offered once per kind of page on a first visit, never a takeover, always available from the
  **Show me around** button. Keyboard-driven, respects reduced motion, stores only which tours were seen
- **An opening strip on every page** — who it is for, what to use it for, and how, in three short
  cells, so no page starts with a wall of prose
- **Wayfinding** — a home button, breadcrumbs under the header on every page, and a **Menu** drawer
  with every page by category (start, roles, leadership, libraries, play, elsewhere), collapsible per
  category and usable without script
- **[`site/pages/bb.py`](site/pages/bb.py) and [`illos.py`](site/pages/illos.py)** — a port of the
  ByteByteGo illustration grammar (title pills, solid label columns, white nodes with flat icons,
  dashed flows that move, callouts, "Best for" lists) as build-time SVG that follows the theme. Five
  pictures drawn with it: the spine in one picture, traditional against agentic PDLC, the R1–R5 risk
  ladder, chained probability, and four methods on one spine as a plug board. They replace the three
  hand-drawn diagrams on the frameworks page and are embedded in five lessons, with wiki screenshots
- **Every lesson's opening map redrawn in the same grammar** — the 44 mermaid flowcharts at the top of
  the lessons are now specs in [`site/pages/mapspecs.py`](site/pages/mapspecs.py), drawn by
  [`maps.py`](site/pages/maps.py) in five shapes (bands, flow, pairs, funnel, fan) with icons, a
  solid label column per band and a callout that says what the picture proves. The site draws them
  live in both themes; the wiki shows screenshots
- **The wiki's own pictures, in the same grammar** — the 45 mermaid diagrams on the hand-written
  reference pages (decision trees, how-tos, role pages, the formulas map, the mental-models map, the
  error index, the study-plan chooser) and the five generated journey arcs are now drawn by
  [`site/pages/wikimaps.py`](site/pages/wikimaps.py) and placed by
  [`site/wiki_pictures.py`](site/wiki_pictures.py) as light/dark screenshots served from the site.
  Eleven of them reuse a lesson's map or a board rather than drawing the same thing twice. The role
  pages gain a hub picture: what arrives on the desk, from whom, and what leaves it, to whom

### Changed
- **The mental models page** — the model/subtlety toggle used to sit above a twelve-tile index, so
  switching it changed nothing on screen. It now sits with the cards, says what is showing, and the
  readings that appear settle in visibly; the same feedback applies to the leadership page's lens
- **Templates and prompts** — the two libraries now say what they are and are not (documents you
  write versus messages you send), show the difference side by side, and every block names the step
  that produces it and when to use it
- **"Simulator" is now "Playbook"** in the navigation, cards and footer: it is the whole method as an
  interactive playbook, and the framed copy at `/simulator/` is the one linked
- **Sizes** — the smallest text on the boards, cards, rails and glyphs raised by half a point to a
  point; mermaid diagrams in lessons draw at 15px and grow up to a third to fill the column
- The tutorial's start page and lessons carry the opening strip, breadcrumbs via the shared shell, and
  the walkthrough

## 2026-09-22 · A page for the board, an intuition layer, and an interaction engine

### Added
- **[The agentic operating protocol](https://akash-coded.github.io/aws-bedrock-agentcore-strands/protocol/)** — the manual for whoever funds the work
  rather than does it. What actually changes and what does not, who does what, the four decisions
  nobody can make for them, how to know it is working, ninety days of rollout, tooling by level,
  seven things to escalate on, and a first thirty days that needs no budget approval
- **[Mental models](https://akash-coded.github.io/aws-bedrock-agentcore-strands/models/)** — twelve drawn shapes that make the rest predictable, each with
  what it predicts, the mistake it prevents, the part that is easy to miss, and a landed-when test.
  Mirrored to the wiki as [Mental Models](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Mental-Models) from the same data
- **An interaction engine** ([`site/theme/engine.js`](site/theme/engine.js)) — declarative and
  dependency-free. A **lens control** switches any explainer between what a decision means and the
  mechanism underneath; **live calculators** derive the acceptance bar, the value line, a score's
  lower bound, the bill decomposition, days of evidence, queue time and cache break-even; a
  **self-check** scores itself and names the next control to build; a **stepper** walks a sequence.
  All of it degrades — with JavaScript off both lenses show, calculators display their worked
  defaults and every stepper panel prints
- Every calculator is tested against the figures the wiki states and reproduces all of them

### Changed — the wiki, to journey depth
- Nine **how-to** pages and four **spine** pages rewritten: per move, what you actually do, where a
  model helps with exactly one thing never delegated, a template, a prompt and a testable done-when
- [Formulas and Calculators](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Formulas-and-Calculators) now carries a worked example and a
  *when it misleads* note against every formula, plus a runnable file that reproduces every figure
- **[`wiki/check.py`](wiki/check.py)** gates the wiki, which never had one: links, anchors, balanced
  details and fences, mermaid types, table separators, and python or json inside a fence

### Fixed
- The bill decomposition, in my own earlier writing: the cache factor omitted **f**, the share of
  spend in the cacheable prefix, and the retry factor treated attempts as retries. With f left out
  that factor reads 2.55 instead of 1.30 and sends you after the wrong leak
- The flip test on the framework decision: borrow survives a portability weight of 2, ties at 1, and
  loses only when portability leaves the matrix — narrower than "four points between first and last"
- The harness-only review lane reported a raw zero; it now reports the rule-of-three bound, so no
  escapes in twelve merges reads as "the true rate could still be 25%"

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
