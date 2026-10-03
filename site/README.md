# The site: the agentic manual on GitHub Pages

**Live:** https://akash-coded.github.io/aws-bedrock-agentcore-strands/

The site is an operating manual for the agentic era, by role: a home page that says what it is in one
screen, the method on one page at `/method/`, one journey page per role, a guide for the forward-deployed
engineer in four pages at `/forward-deployed-engineer/` (a hub and one page for each of its three stages,
Frame, Deliver and Evolve), the libraries of templates and prompts, the operating protocol for leadership,
twelve mental models, the frameworks decoder, a 55-lesson tutorial under `/learn/`, the simulator at
`/simulator/` (Ninety Days, a game of one airline's ninety-day build), the labs at `/labs/` (one job of the same
project done by hand, with a real model's recorded replies), the Tool guides at `/tools/` (seven jobs across
the vendors' tools, each fact dated and sourced) and the workbench at `/workbench/` (the same case in depth,
with its calculators). It is an original work and the intellectual property of **Akash Das**, open-sourced
under the repository's [MIT Licence](../LICENSE) for knowledge and experience sharing.

## How the site is put together

| Path | What it is |
| --- | --- |
| [`build.py`](build.py) | Builds `_site/`: renders the manual, copies the tool byte for byte, injects the site frame into the `/workbench/` copy, publishes the game's files from `play/` and the labs' engine from `labs/`, writes the sitemap and `robots.txt`. Refuses to build if the tool's own bytes changed. Every stylesheet it writes ships without its comments (`lean()`): they stay in the source for the next person to edit it, and cost a reader nothing. Then `stamp()` gives every local stylesheet and script a page asks for a `?v=` taken from the file's content, so a browser never pairs a new page with an old file it kept (GitHub Pages lets it keep one for ten minutes); the pristine tool in `app/` is left alone. `--shots` also writes the screenshot sheet the wiki uses. |
| [`render.py`](render.py) | The page shell (the mark and five-place top bar, the drawer menu, breadcrumbs, footer, structured data, the walkthrough hook), the home page's order and its hero, roles and simulator bands, and the method, role, library and frameworks pages. `shell` takes the list of scripts a page asks for; the home page leaves out `engine.js`, which nothing on it uses. `check_words` stops the build on a dash, a refused word or an American spelling in what a reader meets on the home page. |
| [`play/`](play/), [`GAME.md`](GAME.md) | **The simulator: Ninety Days.** [`days.json`](play/days.json) (every word and number), [`sim.js`](play/sim.js) (the rules: a pure function from a state and an action to the next state), [`art.js`](play/art.js) (the pictures, drawn in code), [`game.js`](play/game.js) and [`game.css`](play/game.css) (the page). The page itself is rendered by [`pages/play.py`](pages/play.py). `GAME.md` says what the game is for, its rules and how it is tested. |
| [`labs/`](labs/), [`pages/labs.py`](pages/labs.py), [`content/labs/`](content/labs/) | **The labs.** [`lab.js`](labs/lab.js) and [`lab.css`](labs/lab.css) (the engine and its look, loaded only on lab pages: a bench with the work on the left and the document it makes on the right), and one script per lab in `content/labs/` (`<slug>.py`, with the lab's documents, prompts and recorded replies in a folder of the same name; `_set.py` lists the labs still to come, which the front page shows as being built). Two labs are open, Grow the spec and Write the system prompt from the spec, and two are listed as being built. The pages, `/labs/` and one per lab, are rendered by `pages/labs.py`, which also checks every script: a reply names its model and date, and carries the prompt the lab's parts join into, byte for byte. A compose beat can send its prompt as a system prompt with a message: the parts marked `user` are the message, sent as the user's turn, and the rest is the system prompt. The page labels and copies the two halves apart, the recording carries both, and the check holds both to the parts. A lab can name, as `starts`, the desk file that must be, byte for byte, the document the lab before it files, and the build refuses the lab if it drifts. Each lab page has a reading version for a page without script. A debrief can set other models' replies to the same prompts beside the lab's own (`debrief.others`, the files in `<slug>/others/`): the check holds each reply to the lab's rule (model, maker, date and the exact prompt) and each table cell to the words of its reply it quotes. The replies have a page of their own, `/labs/<slug>/others/`, which the debrief's fold reads in when it is first opened, so the lab page stays inside its byte budget. That page is the one thing a lab ever fetches. [`content/labs/README.md`](content/labs/README.md) is the authoring guide. |
| [`pages/tools.py`](pages/tools.py), [`content/tools/`](content/tools/) | **The Tool guides.** `/tools/`, a table of seven jobs a team does with AI across Claude, ChatGPT and Codex, and Google, and one page per manual at `/tools/<slug>/` (Claude at the desk, Claude in the repo, ChatGPT and Codex, Google AI Studio and Jules). Every fact a page states about a tool is a sentence in [`content/tools/tools.json`](content/tools/tools.json), with the address it came from and the date it was checked. `pages/tools.py` holds the manuals' words, renders the pages and checks the file: it refuses a fact with no source or date, a model name, a price, a dash or an American spelling, a manual whose marks and list of facts disagree, and a manual that names no family or links something that is not an address, and sixty days after a fact's check it warns and the page shows the date in amber. Each manual names its family, and may list the pages its closing paragraph sends a reader to for prices, limits and models, in place of the family's. A cell in the table links to the manual that uses its fact, or else to the first manual with a fact about the same tool. Inline code over 24 characters may wrap at spaces or inside a hyphenated word, and an option's leading dashes stay with their word, so a long command cannot push a phone's page sideways. [`content/tools/README.md`](content/tools/README.md) is the authoring guide. |
| [`pages/fde.py`](pages/fde.py), [`theme/fde.css`](theme/fde.css) | **The forward-deployed engineer guide.** Its hub and its three stage pages, Frame, Deliver and Evolve, from the staged role in `content/roles/forward-deployed-engineer.json`, the hub's words in `content/roles/_src/fde_hub.py` and the dated sources in `fde_sources.py`. `figure(role, open_stage)` draws the framework picture in both forms: every row open on the hub, its own row open on a stage page. A step is the role pages' `step_html` with the guide's additions drawn round it: hats and altitude chips, "If your client is inside your own company" and "Say it like this". It checks the sources, the hub's words and the stage pages' own words, and stops the build on a problem. `fde.css` is loaded by those four pages only, as `lab.css` is by the labs, and held to 2 KB gzipped. |
| [`DESIGN.md`](DESIGN.md), [`EXPERIENCE.md`](EXPERIENCE.md) | How the pages look, and how they work: tokens, layout rules, the information architecture, the reader journeys and the benchmarks behind them. Read these before changing a page's structure. |
| [`pages/`](pages/) | One module per kind of page or picture: [`globe.py`](pages/globe.py) (the home page's hero: the land as a lattice of dots, the markup, and the same picture held still for the social card), [`spine.py`](pages/spine.py) (the home page's method map: the five names as shapes on the SkyWays PDLC's four phases, from `content/library/frameworks.json`, whose notes and sources it checks when the site is built), [`chooser.py`](pages/chooser.py) (the home page's chooser: which methods your team should use, as three yes-or-no questions), [`people.py`](pages/people.py) (the home page's tutorial band: four people from the game's team, their drawings, and the check that holds each answer to the sentence its lesson says), [`homelib.py`](pages/homelib.py) (the home page's library: three tools on their own materials and six shelves, every count counted when the site is built), [`consult.py`](pages/consult.py) (the home page's close: the consultancy's four offers in `OFFERS`, read by the band and by the organisation's `makesOffer`, so the two cannot drift), [`boards.py`](pages/boards.py) and [`dg.py`](pages/dg.py) (the HTML boards on the method page), [`figures.py`](pages/figures.py) (a step's worked-example SVGs, and three a lesson draws: one slide and two alarms, the postmortem's five layers, four ways back; a small one is marked `fig sm` and set at the text's width), [`bb.py`](pages/bb.py) and [`illos.py`](pages/illos.py) (the ByteByteGo-grammar pictures: the spine, traditional vs agentic, the risk ladder, chained probability, four methods on one spine), [`maps.py`](pages/maps.py) and [`mapspecs.py`](pages/mapspecs.py) (every lesson's opening map, as a spec drawn in five shapes: bands, flow, pairs, funnel, fan. A lesson's map is held to 70% of a 1440 by 900 screen: one over it is laid out tighter, step by step, using the width and never smaller type, the first layout that fits is drawn, and a map still over at its tightest is named in the build's output), [`wikimaps.py`](pages/wikimaps.py) (the pictures on the hand-written wiki pages and the five journey arcs, from the same engine), [`models.py`](pages/models.py), [`protocol.py`](pages/protocol.py), [`calcs.py`](pages/calcs.py), [`learn.py`](pages/learn.py) (the tutorial: the lesson page, its guide and folds, the title's two tones), [`_kit.py`](pages/_kit.py) (the opening strip, lenses, calculators, self-checks, steppers, a page's walkthrough steps). |
| [`content/`](content/) | The words: `roles/*.json` (generated from `roles/_src/`, see [`SCHEMA.md`](content/SCHEMA.md)), `learn/` (the tutorial's lessons and curriculum), `library/frameworks.json` (the methods, with each one's reach across the four phases for the home page's map, and each note's sources and the date they were read). `roles/_src/build_content.py` builds the roles and checks them, and `test_build_content.py` tests the checks. A role whose HEAD has `stages`, the forward-deployed engineer's guide, runs P0 to P3 once inside each of its three stages; it is written in `fde_a.py`, `fde_b.py` and `fde_c.py`, its hub's words are in `fde_hub.py`, and `fde_sources.py` holds its 30 dated sources and 53 quotations, which its words name as `{{S24-ground}}` and `[[S12]]` and never type. |
| [`theme/`](theme/) | [`base.css`](theme/base.css) (one stylesheet; dark by default, light when the reader chooses it; held to 32 KB gzipped as shipped; the home page's band rules sit in one block per band, from `/* home · H3 map */` to `/* end of home · H8 */`), [`fde.css`](theme/fde.css) (the FDE guide's four pages only), [`site.js`](theme/site.js) (theme, copy buttons, the section rail and the lesson guide's mark), [`engine.js`](theme/engine.js) (lenses, calculators, self-checks, steppers, boards; not loaded on the home page), [`guide.js`](theme/guide.js) (the drawer menu, the top bar's two lists, the per-page walkthrough, and a lesson's folds: closed under 1280px, the course opened at the current lesson), [`hero.js`](theme/hero.js) (the home page's picture, in one canvas on one clock: a turning Earth, a spiral around it, and one flight through the four phases staged like a launch, which names each phase and comes to rest in one named still), [`learn.js`](theme/learn.js) (mermaid, drawn in the reader's theme). Every behaviour is progressive enhancement: the pages read without script. |
| [`app/SkyWays-Architect.html`](app/SkyWays-Architect.html) | **The workbench, pristine.** A single self-contained file with no external dependencies: thirteen episodes in depth, nine step-through simulations, seventeen calculators, the role playbooks. Published unchanged at `app/` and, with the site frame, at `workbench/`. It lived at `simulator/` until the game took that address; its old routes are forwarded. |
| [`frame/`](frame/) | The layer around the tool: [`config.js`](frame/config.js) (links, contact delivery), [`frame.js`](frame/frame.js) (attribution, licence and disclaimer, ideas invitation, contact drawer, which an element opens with `data-sw-open`, on a topic when it names one: the home page's close opens it as `data-sw-open="consultancy"`), [`frame.css`](frame/frame.css). Everything is prefixed `sw-` and appended to the end of `<body>`. |
| [`tools/`](tools/) | [`sim.test.mjs`](tools/sim.test.mjs) (the game's rules, walked without a browser: every path, every role, every set of sponsor's rules, and every start the page offers, from each of which some line must still end funded) and [`playtest.mjs`](tools/playtest.mjs) (the game played by real clicks in headless Chrome, to the verdict, in every mode; it opens a late start's briefing, reloads it and presses through it), [`lab.test.mjs`](tools/lab.test.mjs) (a lab played by real clicks in headless Chrome on every path its script has: the prompt the page assembles is the one recorded, the marking scores right, a reload comes back to the same beat, and without script the page reads as a document; its tenth section checks a debrief that shows other models' replies: both tables at 1440, 1024, 390 and 320, the fold reading in six replies exactly as their files, and the tables in the reading version; it has a profile for each lab, with its recordings, its paths and the document each path must leave, fails a lab without one, and runs once per lab's address), [`accept.mjs`](tools/accept.mjs) (the acceptance gate, twenty passes over a page of every kind, the lab pages, the Tool guides and the FDE guide among them: no script, reduced motion, nothing waits, scrolled through, a phone, a small phone, the bar fits, print, the top bar, floating buttons, versions, no stylesheet, the hero, the measure, two right edges, the game's first paint, the bytes (`base.css` under 32 KB gzipped as shipped, the game's three scripts under 46 KB, `theme/hero.js` under 10 KB, the FDE guide's stylesheet under 2 KB and its hub under 22 KB, the home page's HTML under 21 KB, and every page's HTML under 25 KB or the size it is held to), every lesson (its map at most 630px tall at 1440 by 900, and the frame: the measure, one left edge and two right ones, the guide on screen marking the section being read, the title in two lines with its grey at 3:1 or more, the six gaps, and at 390 no table that scrolls and no fold under 44px), the home page's bands (each band's own checks at 1440 by 900 and 390 by 844), and the FDE guide (on its four pages at four widths in both themes: the framework's links, hues and fit, contrast in its parts, its modes, every link landing); run it, and `ui.test.mjs`, before a layout or motion change ships), [`ui.test.mjs`](tools/ui.test.mjs) (the site's parts as a keyboard user, a phone and a pair of eyes meet them: council 10's twenty-one page states, a page of every kind with the drawer's search and the 404, at 1440, 1024, 390 and 320 in both themes, 168 runs in one Chrome with three tabs. No focus ring is cut by the box that holds it; every control is 44px tall on a phone, the stepper's dots 24px apart with 24px to touch; every text is 4.5:1 or more, measured from the screen's pixels where a gradient or a picture is behind it; a ring on a code box is 3:1; no code box scrolls sideways; the role rows sit on their heading's column; the top bar sits on the page's column on a phone; a rail's heading is level with the page's eyebrow; Copy copies each prompt and template byte for byte; the 404 wears the site's eyebrow and ring. A fault another parcel owns is listed in it with its owner, and printed, not failed), [`workbench.test.mjs`](tools/workbench.test.mjs) (the workbench driven in headless Chrome: every route at two widths in both themes, its top bar, its calculators, state saved by its earlier version, and the file opened alone from disk; its ninth section holds the floor the manual keeps: the opening picture's labels at 11px or more from 320 to 1920 wide, its sign-off and the control tower's words at 4.5:1, every focus ring 3:1 against what is behind it, and on a phone a top bar whose controls are 44px tall and all on screen), [`herosheet.mjs`](tools/herosheet.mjs) (the hero at twelve moments of its flight, the rest among them, read from its own times, at five widths in both themes, each frame captioned with the tag's words, for a person to look at before a release), [`roomshot.mjs`](tools/roomshot.mjs) (a room of the game drawn at one times as the game draws it on a day, for the home page's still pictures; `--check` redraws both and compares them pixel by pixel), [`perf.mjs`](tools/perf.mjs) (the performance sheet: bytes, first and largest paint, the hero's frame, seventy seconds on a slowed phone and a scroll, on the build before a round and on the round), [`shoot.mjs`](tools/shoot.mjs) (screenshots every embeddable picture, light and dark, for the wiki), [`ogshots.mjs`](tools/ogshots.mjs) (one 1200×630 social card per page, from `pages/ogcards.py`), [`simshots.mjs`](tools/simshots.mjs), [`check_diagrams.py`](tools/check_diagrams.py) (renders every mermaid diagram and fails on what a reader would notice). Each tool that drives Chrome asks the system for a free port, so two runs never share a browser; `ui.test.mjs` picks one of four hundred at random. |
| [`assets/`](assets/) | Favicon, the default social preview image, `og/` (a social card per page), `pictures/` (the picture pack's workbench pictures and the home page's two rooms of the game) and `learn/` (the wiki's screenshots of the site's pictures). |
| [`contact-relay/`](contact-relay/) | Optional AWS backend for the contact form: Lambda Function URL, DynamoDB, SES, and a private GitHub mirror. Infrastructure as code, one command to deploy. |
| [`404.html`](404.html) | Custom not-found page, in the site's eyebrow and focus ring. |
| [`../.github/workflows/pages.yml`](../.github/workflows/pages.yml) | Runs the contact relay's and the role builder's offline tests, then builds and deploys, on every push that touches `site/`. |
| [`../.github/workflows/wiki-sync.yml`](../.github/workflows/wiki-sync.yml) | Seeds the GitHub wiki from `wiki/*.md` by running `wiki/sync.sh`, unchanged, with GitHub's own token, because a cloud session's git proxy will not carry a credential for the wiki's repository. It runs only when started by hand (Actions, Wiki sync, Run workflow), because a sync overwrites the wiki; the script still refuses to run over a page someone edited in the browser since the last seed. |

<!-- RC-B: confirm against the merged code: accept.mjs's pass count and its pass 17 lines (H10: home 21 KB,
first visit 176 KB, no style block, frame.js), pass 13 and herosheet (H2), hero.js (H1), perf.mjs (H11), the
ui.test.mjs checks U3 and U4 add, and anything FX changes. -->

The frameless tool is also published, unchanged, at
[`app/SkyWays-Architect.html`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html)
for full-screen sessions and embedding.

## Wayfinding

Every page opens the same way: where you are (the mark, the top bar, the breadcrumbs), the page's name,
one line, and a row of counts. Then the content. The instructions for a page (who it is for, what to use
it for, how) are folded behind one line under the title, with a **Show me around** button inside: a
walkthrough that highlights one element at a time. The drawer offers the same walkthrough as **Show me
around this page**. Those are the only two ways in: nothing pops up on arrival, nothing floats over the
page, and nothing is stored for it.
The site keeps these in the reader's browser, in `localStorage`: the theme and the reading lens
(`manual-theme`, `manual-lens`), the game's run in progress and best ending (`skyways.ninety` and the keys
under it), each lab's progress (`skyways.lab.<slug>`) and the documents filed from the labs
(`skyways.labs.pack`). The workbench keeps its own, its evidence pack among them. For the length of a visit,
`sessionStorage` remembers that the home page's picture has already arrived. The **menu** at the top left
is a drawer with every page by category and the search; on a phone it is the navigation.

## Search, and what machines read

The drawer's search box (also `/` on any page) looks through `search.json`, written at build time by
`render.search_index`: every lesson, track, role, role step, mental model, manual page and hand-written wiki page,
and the FDE guide's hub, three stages and twelve steps (each step at its stage page), with a title, one line and a
kind. `llms.txt` indexes the tutorial, the role journeys (with their markdown twins on the wiki), the FDE guide
and its three stages, the reference pages and the playbook for AI assistants; `llms-full.txt` carries every lesson
in full; `robots.txt` says the AI crawlers are welcome. Every lesson has a markdown twin at `index.md` and FAQ,
breadcrumb and article structured data; the home page is a `WebSite`, beside an `Organization`, SkyWays
Consultancy, whose `makesOffer` lists the close's four offers in the page's own words; the author is one `Person`
entity throughout. The twin, and each lesson's part of `llms-full.txt`, writes the page's label once, "In short.",
at the start of the summary.

## The pictures

A third kind of picture sits beside the two below: the **sketches** in the lessons, drawn by
[`pages/sketch.py`](pages/sketch.py) from one small file per lesson in
[`content/learn/sketches/`](content/learn/sketches/). A sketch is one metaphor on a sheet of paper: a small
black worker doing the thing the paragraph just said, a few handwritten notes, a caption in real type.
About thirty lessons have one, one a lesson at most; the build refuses a second, and a sketch placed
outside its own lesson. In a lesson it follows the paragraph it draws, at the text's width (584px, its
handwriting about 28px). The FDE guide's hub shows the hat stand from *What is an FDE?* beside its section on
hats, and the home page's tutorial band draws four card-sized cuts of lesson sketches with the same engine. The
engine writes each stroke's first point in whole units and every later point from the one before it, so a
sketch takes about a third fewer bytes than it did and draws exactly the same pixels. A lesson's markdown
twin shows it as a screenshot from `tools/shoot.mjs`, with the caption under it.
The style is adapted from Ian's Xiaohei illustrations (MIT); the handwriting is Patrick Hand (OFL), the
site's one extra font, self-hosted in `assets/fonts/`. The rules a sketch keeps, the build's checks and the
credit are in [`content/learn/sketches/README.md`](content/learn/sketches/README.md).

Two picture systems, one grammar (the `explainer-illustrations` skill): the HTML **boards** in
`pages/boards.py` for wide, text-heavy comparisons that must wrap and read aloud, and the SVG
**illustrations** in `pages/illos.py`, drawn with the primitives in `pages/bb.py` (a title row with
pills, panels with a solid label column, white nodes with flat icons, dashed flows that move, callouts
and "Best for" lists). Colours are `--bb-*` tokens, so a picture follows the theme. A lesson embeds one
with `{{frameworks:<name>}}`, and its own opening map with `{{map:<slug>}}` (the spec lives in
`pages/mapspecs.py`); the wiki shows a screenshot of each, produced by `tools/shoot.mjs`.

The hand-written wiki pages carry pictures too: [`wiki_pictures.py`](wiki_pictures.py) swaps each page's
mermaid fence for a marker-owned `<picture>` block (`<!-- picture:key -->`), drawn from `pages/wikimaps.py`
or reusing a lesson's map, and regenerates the block on every run. The journey pages get theirs from
`wiki_export.py`, and the Mental Models page from `export_models.py`, both with `wiki_pictures.picture()`.
Order: `build.py --shots`, `tools/shoot.mjs`, `wiki_export.py`, `wiki_pictures.py`, `export_models.py`
(the Mental Models page, from `pages/models.py` and the words kept for the wiki alone in
`content/library/mental-models-wiki.md`; `--check` says whether the page is current), `learn_export.py`
(the tutorial's index and track pages; the lessons themselves live only on the site), `course_export.py`
(a companion page per module, the hub and the labs page, from `modules/` and `labs/`),
`wiki/check.py --strict`, then, once the site has deployed, the Wiki sync workflow (Actions, Wiki sync,
Run workflow), which runs `wiki/sync.sh` with GitHub's own token. The posters, the wiki's journey pages and
the wiki export each list the five roles they draw, so the FDE guide, a staged role, is left out of them on
purpose.

## Updating the tool

Replace `site/app/SkyWays-Architect.html` with the new export and push. That is the whole procedure; the
frame, metadata and contact form are layered on at build time.

## Preview locally

```bash
python3.12 site/build.py
python3 -m http.server -d site/_site 8000
```

Then open http://localhost:8000/. Add `?contact` to the URL to open the contact drawer directly. The build
needs Python 3.12, as the Pages workflow uses (3.11 cannot read one of the labs' f-strings).

Before a change to layout, CSS, motion or a page's markup ships, run the gate and the parts test against
that server (`node site/tools/accept.mjs http://localhost:8000/` and
`node site/tools/ui.test.mjs http://localhost:8000/`); after a change to a role source, run
`python3.12 site/content/roles/_src/test_build_content.py`.

## The contact form

The form has three delivery modes, chosen in [`frame/config.js`](frame/config.js):

| `contact.endpoint` | What happens when a visitor presses Send |
| --- | --- |
| empty (default) | The visitor's own mail app opens with the message addressed and ready. Works everywhere, needs nothing. |
| the relay's Function URL | The message is e-mailed to the owner, stored in DynamoDB, and mirrored as an issue in the private `akash-coded/inbox` repository. See [`contact-relay/`](contact-relay/). |
| a Formspree or Web3Forms URL | The hosted service e-mails the owner. Set `accessKey` for Web3Forms. |

The visitor is told which mode is active, in the drawer's consent line. Messages are never published. A
message sent from the home page's close is headed "[SkyWays Consultancy] enquiry from" its sender. If you
deploy the relay, add `consultancy` to `TOPICS` in `contact-relay/src/handler.py` first, or the relay files
such an enquiry as "other".
<!-- RC-B: FX item 9 adds the topic to the relay; if it landed, drop the last sentence. -->

## Attribution and reuse

Keep the copyright notice and attribution when you reuse the tool or any part of it. Ideas, corrections and
disagreements belong in the [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101);
the ones that ship are credited in the [changelog](../CHANGELOG.md).
