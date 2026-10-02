# The site: the agentic manual on GitHub Pages

**Live:** https://akash-coded.github.io/aws-bedrock-agentcore-strands/

The site is an operating manual for the agentic era, by role: a home page that says what it is in one
screen, the method on one page at `/method/`, one journey page per role, the libraries of templates and
prompts, the operating protocol for leadership, twelve mental models, the frameworks decoder, a 55-lesson
tutorial under `/learn/`, the simulator at `/simulator/` (Ninety Days, a game of one airline's ninety-day
build), the labs at `/labs/` (one job of the same project done by hand, with a real model's recorded
replies) and the workbench at `/workbench/` (the same case in depth, with its calculators). It is an
original work and the intellectual property of **Akash Das**, open-sourced under the repository's
[MIT Licence](../LICENSE) for knowledge and experience sharing.

## How the site is put together

| Path | What it is |
| --- | --- |
| [`build.py`](build.py) | Builds `_site/`: renders the manual, copies the tool byte for byte, injects the site frame into the `/workbench/` copy, publishes the game's files from `play/` and the labs' engine from `labs/`, writes the sitemap and `robots.txt`. Refuses to build if the tool's own bytes changed. Then `stamp()` gives every local stylesheet and script a page asks for a `?v=` taken from the file's content, so a browser never pairs a new page with an old file it kept (GitHub Pages lets it keep one for ten minutes); the pristine tool in `app/` is left alone. `--shots` also writes the screenshot sheet the wiki uses. |
| [`render.py`](render.py) | The page shell (the mark and five-place top bar, the drawer menu, breadcrumbs, footer, structured data, the walkthrough hook) and the home, method, role, library and frameworks pages. |
| [`play/`](play/), [`GAME.md`](GAME.md) | **The simulator: Ninety Days.** [`days.json`](play/days.json) (every word and number), [`sim.js`](play/sim.js) (the rules: a pure function from a state and an action to the next state), [`art.js`](play/art.js) (the pictures, drawn in code), [`game.js`](play/game.js) and [`game.css`](play/game.css) (the page). The page itself is rendered by [`pages/play.py`](pages/play.py). `GAME.md` says what the game is for, its rules and how it is tested. |
| [`labs/`](labs/), [`pages/labs.py`](pages/labs.py), [`content/labs/`](content/labs/) | **The labs.** [`lab.js`](labs/lab.js) and [`lab.css`](labs/lab.css) (the engine and its look, loaded only on lab pages: a bench with the work on the left and the document it makes on the right), and one script per lab in `content/labs/` (`<slug>.py`, with the lab's documents, prompts and recorded replies in a folder of the same name; `_set.py` lists the labs still to come, which the front page shows as being built). The pages, `/labs/` and one per lab, are rendered by `pages/labs.py`, which also checks every script: a reply names its model and date, and carries the prompt the lab's parts join into, byte for byte. Each lab page has a reading version for a page without script. [`content/labs/README.md`](content/labs/README.md) is the authoring guide. |
| [`pages/tools.py`](pages/tools.py), [`content/tools/`](content/tools/) | **The Tool guides.** `/tools/`, a table of seven jobs a team does with AI across Claude, ChatGPT and Codex, and Google, and one page per manual at `/tools/<slug>/` (Claude at the desk, Claude in the repo). Every fact a page states about a tool is a sentence in [`content/tools/tools.json`](content/tools/tools.json), with the address it came from and the date it was checked. `pages/tools.py` holds the manuals' words, renders the pages and checks the file: it refuses a fact with no source or date, a model name, a price, a dash or an American spelling, and a manual whose marks and list of facts disagree, and sixty days after a fact's check it warns and the page shows the date in amber. [`content/tools/README.md`](content/tools/README.md) is the authoring guide. |
| [`DESIGN.md`](DESIGN.md), [`EXPERIENCE.md`](EXPERIENCE.md) | How the pages look, and how they work: tokens, layout rules, the information architecture, the reader journeys and the benchmarks behind them. Read these before changing a page's structure. |
| [`pages/`](pages/) | One module per kind of page or picture: [`globe.py`](pages/globe.py) (the home page's hero: the land as a lattice of dots, the markup, and the same picture held still for the social card), [`spine.py`](pages/spine.py) (the home page's two pictures of the method: the SkyWays PDLC as a spine that closes into a loop, and the table of methods along it), [`boards.py`](pages/boards.py) and [`dg.py`](pages/dg.py) (the HTML boards on the method page), [`figures.py`](pages/figures.py) (a step's worked-example SVGs), [`bb.py`](pages/bb.py) and [`illos.py`](pages/illos.py) (the ByteByteGo-grammar pictures: the spine, traditional vs agentic, the risk ladder, chained probability, four methods on one spine), [`maps.py`](pages/maps.py) and [`mapspecs.py`](pages/mapspecs.py) (every lesson's opening map, as a spec drawn in five shapes: bands, flow, pairs, funnel, fan), [`wikimaps.py`](pages/wikimaps.py) (the pictures on the hand-written wiki pages and the five journey arcs, from the same engine), [`models.py`](pages/models.py), [`protocol.py`](pages/protocol.py), [`calcs.py`](pages/calcs.py), [`learn.py`](pages/learn.py) (the tutorial), [`_kit.py`](pages/_kit.py) (the opening strip, lenses, calculators, self-checks, steppers, a page's walkthrough steps). |
| [`content/`](content/) | The words: `roles/*.json` (generated from `roles/_src/`), `learn/` (the tutorial's lessons and curriculum), `library/frameworks.json`. |
| [`theme/`](theme/) | [`base.css`](theme/base.css) (one stylesheet; dark by default, light when the reader chooses it), [`site.js`](theme/site.js) (theme, copy buttons, the steps rail), [`engine.js`](theme/engine.js) (lenses, calculators, self-checks, steppers, boards), [`guide.js`](theme/guide.js) (the drawer menu, the top bar's two lists, the per-page walkthrough), [`hero.js`](theme/hero.js) (the home page's picture, in one canvas on one clock: a turning Earth, a fine spiral around it and one aircraft climbing it), [`learn.js`](theme/learn.js) (mermaid, drawn in the reader's theme). Every behaviour is progressive enhancement: the pages read without script. |
| [`app/SkyWays-Architect.html`](app/SkyWays-Architect.html) | **The workbench, pristine.** A single self-contained file with no external dependencies: thirteen episodes in depth, nine step-through simulations, seventeen calculators, the role playbooks. Published unchanged at `app/` and, with the site frame, at `workbench/`. It lived at `simulator/` until the game took that address; its old routes are forwarded. |
| [`frame/`](frame/) | The layer around the tool: [`config.js`](frame/config.js) (links, contact delivery), [`frame.js`](frame/frame.js) (attribution, licence and disclaimer, ideas invitation, contact drawer), [`frame.css`](frame/frame.css). Everything is prefixed `sw-` and appended to the end of `<body>`. |
| [`tools/`](tools/) | [`sim.test.mjs`](tools/sim.test.mjs) (the game's rules, walked without a browser: every path, every role, every set of sponsor's rules) and [`playtest.mjs`](tools/playtest.mjs) (the game played by real clicks in headless Chrome, to the verdict, in every mode), [`lab.test.mjs`](tools/lab.test.mjs) (a lab played by real clicks in headless Chrome on every path its script has: the prompt the page assembles is the one recorded, the marking scores right, a reload comes back to the same beat, and without script the page reads as a document), [`accept.mjs`](tools/accept.mjs) (the acceptance gate, seventeen passes over a page of every kind, the lab pages and the Tool guides among them: no script, reduced motion, nothing waits, scrolled through, a phone, a small phone, the bar fits, print, the top bar, floating buttons, versions, no stylesheet, the hero, the measure, two right edges, the game's first paint and the bytes; run it before a layout or motion change ships), [`workbench.test.mjs`](tools/workbench.test.mjs) (the workbench driven in headless Chrome: every route at two widths in both themes, its top bar, its calculators, state saved by its earlier version, and the file opened alone from disk), [`herosheet.mjs`](tools/herosheet.mjs) (the hero at twelve moments of a lap, at four widths, in both themes, on sheets for a person to look at before a release), [`shoot.mjs`](tools/shoot.mjs) (screenshots every embeddable picture, light and dark, for the wiki), [`ogshots.mjs`](tools/ogshots.mjs) (one 1200×630 social card per page, from `pages/ogcards.py`), [`simshots.mjs`](tools/simshots.mjs), [`check_diagrams.py`](tools/check_diagrams.py) (renders every mermaid diagram and fails on what a reader would notice). |
| [`assets/`](assets/) | Favicon, the default social preview image, `og/` (a social card per page) and `learn/` (the wiki's screenshots of the site's pictures). |
| [`contact-relay/`](contact-relay/) | Optional AWS backend for the contact form: Lambda Function URL, DynamoDB, SES, and a private GitHub mirror. Infrastructure as code, one command to deploy. |
| [`404.html`](404.html) | Custom not-found page. |
| [`../.github/workflows/pages.yml`](../.github/workflows/pages.yml) | Builds and deploys on every push that touches `site/`. |

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
`render.search_index`: every lesson, track, role, role step, mental model, manual page and hand-written
wiki page, with a title, one line and a kind. `llms.txt` indexes the tutorial, the role journeys (with
their markdown twins on the wiki), the reference pages and the playbook for AI assistants;
`llms-full.txt` carries every lesson in full; `robots.txt` says the AI crawlers are welcome. Every
lesson has a markdown twin at `index.md` and FAQ, breadcrumb and article structured data; the home
page is a `WebSite`; the author is one `Person` entity throughout.

## The pictures

A third kind of picture sits beside the two below: the **sketches** in the lessons, drawn by
[`pages/sketch.py`](pages/sketch.py) from one small file per lesson in
[`content/learn/sketches/`](content/learn/sketches/). A sketch is one metaphor on a sheet of paper: a small
black worker doing the thing the paragraph just said, a few handwritten notes, a caption in real type.
On a lesson from 1256px wide it sits in the margin column beside the text, 280 to 300px wide and level
with the paragraph it draws; narrower, it follows its paragraph.
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
`wiki_export.py`. Order: `build.py --shots`, `tools/shoot.mjs`, `wiki_export.py`, `wiki_pictures.py`,
`learn_export.py` (the tutorial's index and track pages; the lessons themselves live only on the site),
`course_export.py` (a companion page per module, the hub and the labs page, from `modules/` and `labs/`),
`wiki/check.py --strict`, then `wiki/sync.sh` once the site has deployed.

## Updating the tool

Replace `site/app/SkyWays-Architect.html` with the new export and push. That is the whole procedure; the
frame, metadata and contact form are layered on at build time.

## Preview locally

```bash
python site/build.py
python -m http.server -d site/_site 8000
```

Then open http://localhost:8000/. Add `?contact` to the URL to open the contact drawer directly.

## The contact form

The form has three delivery modes, chosen in [`frame/config.js`](frame/config.js):

| `contact.endpoint` | What happens when a visitor presses Send |
| --- | --- |
| empty (default) | The visitor's own mail app opens with the message addressed and ready. Works everywhere, needs nothing. |
| the relay's Function URL | The message is e-mailed to the owner, stored in DynamoDB, and mirrored as an issue in the private `akash-coded/inbox` repository. See [`contact-relay/`](contact-relay/). |
| a Formspree or Web3Forms URL | The hosted service e-mails the owner. Set `accessKey` for Web3Forms. |

The visitor is told which mode is active, in the drawer's consent line. Messages are never published.

## Attribution and reuse

Keep the copyright notice and attribution when you reuse the tool or any part of it. Ideas, corrections and
disagreements belong in the [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101);
the ones that ship are credited in the [changelog](../CHANGELOG.md).
