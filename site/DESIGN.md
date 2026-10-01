---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-01
colors:
  bone: {light: "#F7F6F2", dark: "#121316"}        # page
  paper: {light: "#FFFFFF", dark: "#181A1E"}       # raised surface
  ink: {light: "#16150F", dark: "#ECEAE4"}
  ink2: {light: "#44423B", dark: "#C3C0B8"}        # body text
  soft: {light: "#696660", dark: "#93908A"}        # labels, meta, eyebrows
  rule: {light: "#E4E0D6", dark: "#2B2E34"}        # hairlines
  brand: "var(--dg-indigo)"                        # the plane in the mark, nowhere else
  phase:
    P0: "var(--dg-slate)"
    P1: "var(--dg-indigo)"
    P2: "var(--dg-teal)"
    P3: "var(--dg-amber)"
    gate: "var(--dg-rose)"
typography:
  display: "Instrument Sans, 600 to 620, tracking -0.035em to -0.045em"
  body: "Geist, 400, 16 to 19.5px, line-height 1.55 to 1.62"
  mono: "Geist Mono, 500, 12.5px: eyebrows, counts, codes"
  scale: {hero: "clamp(42px, 6vw, 78px)", page-h1: "32px to 58px (50px inside a column), by viewport width", band-h2: "clamp(29px, 3.5vw, 46px)", lede: "clamp(17px, 1.5vw, 19.5px)"}
rounded: {control: 11px, button-large: 13px, tile: 20px, pill: 999px, frame: 16px}
spacing:
  band: "clamp(72px, 9.5vw, 128px) above and below every home section"
  measure: "46 to 56 characters for a lede, never the full row"
  wrap: 1280px
motion: {durations: [150ms, 250ms, 350ms, 400ms], easing: "cubic-bezier(.22,1,.36,1)", stagger: 40ms, reduced: "everything still, globe drawn once"}
components: [header, hero-scene, section-head, coverage-table, role-rows, simulator-frame, shelf-tile, page-head, folded-howto, section-rail, numbered-section, ruled-columns, step, next-up, pause-control]
---

# How the site looks

This is the visual contract for the manual's pages. `EXPERIENCE.md` beside it says how the pages
behave and who they are for. Where a mock, a screenshot or an older page disagrees with these two files,
the files win.

The tokens above are the ones `theme/base.css` already defines. Nothing here introduces a second palette.

## Brand and style

One name in the top left of every page: the mark, the word **SkyWays**, and the product it is, *The
agentic manual*. The mark is an open ring with a paper plane on it, the same one the simulator carries.
It says the whole method in one shape: a loop, flown.

The site should feel like a well made reference book that happens to move: roomy, quiet, typographic,
with one strong picture per section. It is signed once by its author, in the hero's last line and the footer.

SkyWays is two things, and the page always says which. **SkyWays** alone is the publisher and the method
(the SkyWays PDLC). The airline in the worked case is always "a fictional airline" on first mention.

## Colours

Warm paper in the light, near black in the dark, with one ink ramp (ink, ink2, soft). Colour is spent on
meaning only:

- The four phase hues mean P0, P1, P2 and P3 wherever they appear: the hero's flight, the coverage bars,
  the boards, the role roadmap. A phase never changes hue between pages.
- Rose means the hard gate.
- A role's accent tints its own page and its row on the home page.
- Indigo is the plane in the mark.

Large display text may continue in a grey second sentence (ink mixed 48% into the page). That grey is
for display sizes only; it measures 3.4:1 to 3.8:1, which passes for large text and fails for body text.

## Typography

Headings are sentences with a verb or a question in them, set in sentence case at weight 600 to 620.
A band's heading may run straight into a grey continuation at the same size. Body text stops near 54
characters. Small labels (eyebrows, counts, role codes) are Geist Mono in sentence case, never capitals
with wide tracking. No label is under 11px.

## Layout and spacing

- The first screen of the home page holds five things: the eyebrow, the headline, one sentence, two
  buttons, one picture. The meta line under the buttons is the only other text.
- One idea per band: a heading, at most one paragraph of thirty words, one picture or list, one way on.
- Bands are separated by space and a hairline, not by boxes. Cards exist only on the shelf, where each
  one is a destination.
- On a reading page, text sits on the page under a hairline. A box is kept for what is a thing in
  itself: code, a table, a diagram, a calculator, a verdict.
- Reading text is capped near 75 characters a line, whatever the column's width.
- A landing page opens with its name, one line, one row of counts, then its content. Anything that
  explains how to use the page is folded behind one line.
- The hero is asymmetric: words left, picture right, the picture allowed to run off the edge. On a
  phone the words come first and the picture follows.

## Motion

Nothing moves for decoration. A thing may move only if the movement does one of three jobs:

1. **It answers something the reader did.** A button pressed, a list opened, a step unfolded, "Copied".
2. **It says where the reader is.** The rail marking the current section, one page handing over to the
   next, a title travelling from its row in a list to the head of its own page.
3. **It shows a thing that is itself a sequence.** The four phases in order, a role's eight steps, the
   methods drawing along the line, the parts of a figure in the order they were drawn.

Two classes of motion, with different rules.

**Transitions** answer the reader and take 150, 250, 350 or 400ms on the one easing curve. Opening takes
longer than closing: a list opens in 250ms and leaves at once. Items that arrive in order are 40 to 80ms
apart, and a sequence finishes in under a second. The one long entrance is the hero's flight: its four
legs draw 250ms apart and the picture is complete in two seconds.

**Explanatory motion** shows a sequence. It plays once, the first time the thing is scrolled to, and its
last frame is the complete picture, which is also what a reader with reduced motion gets. Anything that
keeps moving for more than a few seconds (the hero's flight, the tower on the method page) carries a
pause control. Dashes on a connector move only while the reader scrolls past them.

Three rules of choreography. One sequence at a time on a screen: on the home page the words settle,
then the flight draws. An entrance plays once per visit and never again on scrolling back. Every
animation is designed from its final frame backwards, because the final frame is what most readers,
every printer and every reduced-motion reader will see.

Refused, each for a reason: numbers that count up (a true number shown false), cursor glows and spotlights
(nothing on a phone), text that slides in on a reading page (the home page's bands rise once as they are
reached, and that is the only place), a second drawing of a route the page already draws.

## Elevation and depth

Depth is used twice. The hero's globe has a lit side, a limb and a glow in the page's own slate. The
simulator's screenshot sits in a browser frame tilted nine degrees with one long shadow, and straightens
when hovered. Everything else is flat on the page with a 1px hairline.

## Shapes

Buttons are rounded rectangles (11 to 13px). Pills are for things that are tags or the one filled
button in the header. Tiles are 20px. The coverage bars are 3px-cornered so adjoining phases read as one
line.

## Components

| Component | What it is | Where it lives |
| --- | --- | --- |
| Header | Mark and name, five places (two of them short lists), the simulator button, the theme toggle. The drawer holds every page and the search. | `render.shell`, `render._nav` |
| Hero scene | A dotted Earth turning once every four minutes, and one flight around it through P0 to P3 with the hard gate. Decorative: section two says the same in words. | `pages/globe.py`, `theme/hero.js` |
| Section head | Mono eyebrow, a heading that continues in grey, one optional paragraph. | `.sec-h` |
| Coverage table | Four methods as bars along the four phases, the SkyWays PDLC as the whole line. A real table with row and column headers. | `render._coverage` |
| Role rows | One row per role: code, name, where you start, where you end up, counts. A list, not cards. | `.seats` |
| Simulator frame | The real opening screen of the simulator, light and dark. | `.simshot` |
| Shelf tile | A count, a name, one line. Two of the six are double width. | `.shelf .tile` |
| Page head | Eyebrow, name, one line, a row of counts, optionally one or two buttons. | `.phead`, `.pmeta` |
| Folded how-to | "Who this page is for, and how to use it", closed by default. | `pages/_kit.orient` |
| Section rail | The sections of a long page down the left on a wide screen, the current one marked. Role pages and the leadership page. | `.rail`, `site.js` |
| Numbered section | A mono "01" over each heading where the order is real, with 52 to 88px between sections. | `main.numbered` |
| Ruled columns | Paragraphs that used to sit in bordered cards: a hairline above, no box. | `.three`, `.claims`, `.pair`, `.mix`, `.lc` |
| Step | One surface. Its table, artefact and example are ruled, not boxed; its head links straight to its template and prompts. | `render.step_html` |
| Next up | The foot of a reference page: one sentence, one button, and at most one quiet link beside it. | `render.next_up` |
| Pause control | A checkbox, so it works without script; stills whatever holds it. | `render.MOTION_TOGGLE`, `.mpause` |

## Do and do not

Do:

- Cut before you decorate. If a block repeats a link the page already carries, remove the block.
- Give every band a picture that is the thing itself: the method as bars, the roles as rows, the
  simulator as its own screen.
- Keep numbers honest and computed. Lesson, template, prompt and picture counts come from the content
  at build time.
- Measure contrast and overflow; do not judge them from a screenshot.

Do not:

- Put more than two buttons in one view, or more than one routing device on one page.
- Explain the method twice on the home page. The boards live on `/method/`.
- Use a second accent colour, a gradient as decoration, or capitals with wide tracking.
- Greet a reader with a popup. Nothing appears that was not asked for.
- Write a heading that is a category ("Overview", "Features", "Resources").
