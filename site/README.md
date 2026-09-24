# The site: the agentic manual on GitHub Pages

**Live:** https://akash-coded.github.io/aws-bedrock-agentcore-strands/

The site is an operating manual for the agentic era, by role: a home page that opens with the four-phase
spine, one journey page per role, the libraries of templates and prompts, the operating protocol for
leadership, twelve mental models, the frameworks decoder, a 55-lesson tutorial under `/learn/`, and the
SkyWays playbook (an interactive simulator of one airline's ninety-day build) at `/simulator/`. It is an
original work and the intellectual property of **Akash Das**, open-sourced under the repository's
[MIT Licence](../LICENSE) for knowledge and experience sharing.

## How the site is put together

| Path | What it is |
| --- | --- |
| [`build.py`](build.py) | Builds `_site/`: renders the manual, copies the tool byte for byte, injects the site frame into the `/simulator/` copy, writes the sitemap and `robots.txt`. Refuses to build if the tool's own bytes changed. `--shots` also writes the screenshot sheet the wiki uses. |
| [`render.py`](render.py) | The page shell (header with the categorised drawer menu, breadcrumbs, footer, structured data, the walkthrough hook) and the home, role, library and frameworks pages. |
| [`pages/`](pages/) | One module per kind of page or picture: [`boards.py`](pages/boards.py) and [`dg.py`](pages/dg.py) (the HTML boards on the home page), [`figures.py`](pages/figures.py) (a step's worked-example SVGs), [`bb.py`](pages/bb.py) and [`illos.py`](pages/illos.py) (the ByteByteGo-grammar pictures: the spine, traditional vs agentic, the risk ladder, chained probability, four methods on one spine), [`maps.py`](pages/maps.py) and [`mapspecs.py`](pages/mapspecs.py) (every lesson's opening map, as a spec drawn in five shapes: bands, flow, pairs, funnel, fan), [`wikimaps.py`](pages/wikimaps.py) (the pictures on the hand-written wiki pages and the five journey arcs, from the same engine), [`models.py`](pages/models.py), [`protocol.py`](pages/protocol.py), [`calcs.py`](pages/calcs.py), [`learn.py`](pages/learn.py) (the tutorial), [`_kit.py`](pages/_kit.py) (the opening strip, lenses, calculators, self-checks, steppers, Pip the guide). |
| [`content/`](content/) | The words: `roles/*.json` (generated from `roles/_src/`), `learn/` (the tutorial's lessons and curriculum), `library/frameworks.json`. |
| [`theme/`](theme/) | [`base.css`](theme/base.css) (one stylesheet, light and dark), [`site.js`](theme/site.js) (theme, copy buttons, the steps rail), [`engine.js`](theme/engine.js) (lenses, calculators, self-checks, steppers, boards), [`guide.js`](theme/guide.js) (the drawer menu, the per-page walkthrough narrated by Pip), [`learn.js`](theme/learn.js) (mermaid, drawn in the reader's theme). Every behaviour is progressive enhancement: the pages read without script. |
| [`app/SkyWays-Architect.html`](app/SkyWays-Architect.html) | **The tool, pristine.** A single self-contained file with no external dependencies. Published unchanged at `app/` and, with the site frame, at `simulator/`. |
| [`frame/`](frame/) | The layer around the tool: [`config.js`](frame/config.js) (links, contact delivery), [`frame.js`](frame/frame.js) (attribution, licence and disclaimer, ideas invitation, contact drawer), [`frame.css`](frame/frame.css). Everything is prefixed `sw-` and appended to the end of `<body>`. |
| [`tools/`](tools/) | [`shoot.mjs`](tools/shoot.mjs) (screenshots every embeddable picture, light and dark, for the wiki), [`ogshots.mjs`](tools/ogshots.mjs) (one 1200×630 social card per page, from `pages/ogcards.py`), [`simshots.mjs`](tools/simshots.mjs), [`check_diagrams.py`](tools/check_diagrams.py) (renders every mermaid diagram and fails on what a reader would notice). |
| [`assets/`](assets/) | Favicon, the default social preview image, `og/` (a social card per page) and `learn/` (the wiki's screenshots of the site's pictures). |
| [`contact-relay/`](contact-relay/) | Optional AWS backend for the contact form: Lambda Function URL, DynamoDB, SES, and a private GitHub mirror. Infrastructure as code, one command to deploy. |
| [`404.html`](404.html) | Custom not-found page. |
| [`../.github/workflows/pages.yml`](../.github/workflows/pages.yml) | Builds and deploys on every push that touches `site/`. |

The frameless tool is also published, unchanged, at
[`app/SkyWays-Architect.html`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html)
for full-screen sessions and embedding.

## Wayfinding

Every page opens the same way: the title, then a strip that says **who the page is for, what to use it
for, and how**, with a **Show me around** button. The button starts a walkthrough — Pip, the guide,
highlights one element at a time and says what it does. The walkthrough is offered once per kind of
page on a first visit (the choice is remembered in `localStorage`, nothing else is stored), and is
always available from the bottom-left button. The **Menu** at the top left is a drawer with every page
by category; **breadcrumbs** sit under the header on every page but the home page.

## Search, and what machines read

The drawer's search box (also `/` on any page) looks through `search.json`, written at build time by
`render.search_index`: every lesson, track, role, role step, mental model, manual page and hand-written
wiki page, with a title, one line and a kind. `llms.txt` indexes the tutorial, the role journeys (with
their markdown twins on the wiki), the reference pages and the playbook for AI assistants;
`llms-full.txt` carries every lesson in full; `robots.txt` says the AI crawlers are welcome. Every
lesson has a markdown twin at `index.md` and FAQ, breadcrumb and article structured data; the home
page is a `WebSite`; the author is one `Person` entity throughout.

## The pictures

Two picture systems, one grammar (the `explainer-illustrations` skill): the HTML **boards** in
`pages/boards.py` for wide, text-heavy comparisons that must wrap and read aloud, and the SVG
**illustrations** in `pages/illos.py`, drawn with the primitives in `pages/bb.py` — a title row with
pills, panels with a solid label column, white nodes with flat icons, dashed flows that move, callouts
and "Best for" lists. Colours are `--bb-*` tokens, so a picture follows the theme. A lesson embeds one
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
