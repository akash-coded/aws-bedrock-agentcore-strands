---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-02
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
  hand: "Patrick Hand, on a sketch's sheet of paper and nowhere else"
  scale: {hero: "clamp(42px, 6vw, 78px)", page-h1: "32px to 58px (50px inside a column), by viewport width", band-h2: "clamp(29px, 3.5vw, 46px)", lede: "clamp(17px, 1.5vw, 19.5px)"}
rounded: {control: 11px, button-large: 13px, tile: 20px, pill: 999px, frame: 16px}
spacing:
  band: "clamp(72px, 9.5vw, 128px) above and below every home section"
  measure: "46 to 56 characters for a lede, never the full row"
  wrap: 1280px
motion: {durations: [150ms, 250ms, 350ms, 400ms, 600ms], easing: "cubic-bezier(.22,1,.36,1)", spring: "--spring, a linear() curve that passes its mark by 2.8% and comes home", stagger: "40ms in a list, 60 to 110ms between the parts of a figure", reduced: "everything still: the globe drawn once, one aircraft parked at each phase"}
components: [header, header-slot, hero-scene, section-head, lifecycle-figure, method-table, role-rows, day-card, late-start-briefing, track-list, lesson-sketch, shelf-tile, page-head, folded-howto, section-rail, numbered-section, ruled-columns, step, lab-comparison-table, next-up, pause-control]
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

Near black is the page a reader opens. Warm paper is the light theme, chosen with the toggle and
remembered; paper is always printed light. One ink ramp (ink, ink2, soft). Colour is spent on meaning only:

- The four phase hues mean P0, P1, P2 and P3 wherever they appear: the hero's flight, the lifecycle
  figure, the method table's bars, the boards, the role roadmap. A phase never changes hue between pages.
- Rose means the sign-off (the lessons' hard gate), and what is owed.
- The globe is blue, sea and land, with a blue limb. It never wears a phase hue: those belong to the
  ribbon flown round it.
- A sketch has three pens of its own beside its ink: red for the point, orange for the path, blue for
  the aside. They live on the sketch's sheet of paper and mean nothing off it.
- A role's accent tints its own page and its row on the home page.
- Indigo is the plane in the mark.

Large display text may continue in a grey second sentence (ink mixed 48% into the page). That grey is
for display sizes only; it measures 3.4:1 to 3.8:1, which passes for large text and fails for body text.

## Typography

Headings are sentences with a verb or a question in them, set in sentence case at weight 600 to 620.
A band with a paragraph has one heading and one paragraph, side by side on a wide screen; a band without
one may run its heading into a grey continuation at the same size. Handwriting appears only inside a
sketch, at 13px or more on a phone. Body text stops near 54
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
- Reading text is capped near 75 characters a line, whatever the column's width. On a lesson that is one
  508px measure for the title, the lede, the paragraphs, the lists and the headings; boards, tables, code
  and drawn figures run to the column's wide edge. So a lesson has two right edges and no third, and a
  caption starts on its figure's own edge. From 1256px wide the room beside the text is a margin column of
  280 to 300px: the contents beside the title, each sketch level with the paragraph it draws, the "Try it"
  card. Narrower, they return to the flow.
- A lesson's opening map takes at most 70% of a 1440 by 900 screen, 630px for its figure. It fits by using
  the width (more cells across, the bands as cards side by side, a side list beside the end), never by
  smaller type. Where even that is too tall, its words are cut.
- In a lesson's table, a column whose body cells are all numbers, amounts or percentages (one unit they
  all share, such as "a day", allowed) is set right, its header with it, in figures of one width. Text
  columns stay left. On a phone, where a table of three or more columns stacks, every cell reads left
  under its name.
- In the tutorial's rail a track's rows start on its heading's left edge, so the current lesson's
  highlight does too. Every row's number and title sit in the same two columns.
- A landing page opens with its name, one line, one row of counts, then its content. Anything that
  explains how to use the page is folded behind one line.
- The hero is asymmetric: words left, picture right, the picture allowed to run off the edge. On a
  phone the words come first and the picture follows.
- A band whose heading has a paragraph sets the two side by side on a wide screen, so the question and
  its picture start on the same screen at 1440 by 900.

## Motion

Nothing moves without a job. A screen may carry one ambient motion, with its own pause control (the hero's
flight; the three moments of the game taking turns in their frame); everything else plays once and ends
within about two seconds. A thing may move only if the movement does one of three jobs:

1. **It answers something the reader did.** A button pressed, a list opened, a step unfolded, "Copied".
2. **It says where the reader is.** The rail marking the current section, one page handing over to the
   next, a title travelling from its row in a list to the head of its own page.
3. **It shows a thing that is itself a sequence.** The four phases in order, a role's eight steps, the
   methods drawing along the line, the parts of a figure in the order they were drawn.

Two classes of motion, with different rules.

**Transitions** answer the reader and take 150, 250, 350 or 400ms on the one easing curve; one long line
may take 600ms to draw. Opening takes longer than closing: a list opens in 250ms and leaves at once. Items
that arrive in order are 40 to 110ms apart. A spring (`--spring`) is for small things that were pressed or
that change shape: a button under a finger, the pill in the top bar, the aircraft at a phase boundary. It
never moves text or a height. The hero's entrance draws its four legs 250ms apart and is complete in two
seconds; it plays once in a sitting, so a reader who comes back to the home page finds the picture there.
The lifecycle figure is assembled in the order it is read, in 2.2 seconds: four methods arrive, their lines
run into one point, its name appears, the line leaves it phase by phase, then the way back. The method
table's bars then draw along it, row by row.

**Explanatory motion** shows a sequence. It plays once, the first time the thing is scrolled to, and its
last frame is the complete picture, which is also what a reader with reduced motion gets. Anything that
keeps moving for more than a few seconds (the hero's flight, the tower on the method page) carries a
pause control. Dashes on a connector move only while the reader scrolls past them. A sketch is there,
complete; only its handwritten notes arrive, in the order they were written, the first time it is
scrolled to.

The hero runs on one clock. One round takes 32 seconds: 24 in front of the globe at a steady pace, half a
second held at the sign-off, the rest behind it. The globe turns once a minute, drawn on every frame the
display offers. The aircraft changes at each phase boundary on that same clock, so the pause control holds
the flight, the shape and the sign-off's bar together. Where a browser cannot ease one path into another,
four drawings take turns on the same keyframes.

Three rules of choreography. One sequence at a time on a screen: on the home page the words settle,
then the flight draws. An entrance plays once per visit and never again on scrolling back. Every
animation is designed from its final frame backwards, because the final frame is what most readers,
every printer and every reduced-motion reader will see.

Refused, each for a reason: numbers that count up (a true number shown false), cursor glows and spotlights
(nothing on a phone), text that slides in on a reading page (the home page's bands rise once as they are
reached, and that is the only place), a second drawing of a route the page already draws (the hero's next
round is the exception: it is what makes the loop a spiral), any animation library, parallax, a figure
that draws as the page is scrolled (stop halfway and it is half drawn).

## The simulator's picture

The game at `/simulator/` is the one place the site uses pixel art, and it follows the same rules as
everything else: hue means phase, rose means the sign-off and what is owed, words are real type, motion
has a job and can be paused. Its colour comes from light and material: each room's walls take a little of
its owner's hue, and the sky outside tells the phase, one still sky a day, from dawn on Day 1 to dusk on
Day 90 (night, if the run is late). The canvas is the same in both themes. `GAME.md` has the detail.

## Elevation and depth

Depth is used three times. The hero's globe has a lit side, a blue limb and a glow. A sketch sits on a
sheet of paper, the one light surface on a dark page. The
home page's day card casts one long shadow, and in the game the building takes the card's corner and that
shadow. Everything else is flat on the page with a 1px hairline.

## Shapes

Buttons are rounded rectangles (11 to 13px). Pills are for things that are tags or the one filled
button in the header. Tiles are 20px. A method's bars are 3px-cornered with 3px between them, so its stages read as one
line with the phases still countable.

## Components

| Component | What it is | Where it lives |
| --- | --- | --- |
| Header | Mark and name, five places (two of them short lists), the slot, the theme toggle. The toggle is a circle with its left half filled, drawn in SVG at the menu icon's size, line and colour (18px, a 1.5px line). It is never a character: "◐" fell back to a font that drew a dot. The workbench's top bar draws the same. The drawer holds every page and the search. | `render.shell`, `render._nav`, `render.HALF` |
| Header slot | One filled pill and, on a wide screen, one quiet link. The pill never points at the page it is on: in the manual it offers the simulator, in a lesson the day of the game that lesson is the reading for, in the game the lesson behind the day on screen. The quiet link is the next useful place from here ("Apply it", "Manual"). | `render._ctx`, `.ctx` |
| Hero scene | A blue dotted Earth turning once a minute, and one flight round it through P0 to P3: a thick ribbon in the phase hues, the sign-off, and a way back behind the globe that climbs, so the next round starts one level up. The aircraft is a paper dart in P0, a plan in P1, an airliner in P2, a jet in P3, and each phase's label carries its aircraft. Decorative: section two says the same in words. | `pages/globe.py`, `theme/hero.js` |
| Section head | Mono eyebrow, a heading that continues in grey, one optional paragraph. | `.sec-h` |
| Lifecycle figure | On the left, four methods and the one idea the lifecycle keeps from each; four lines run into one point named SkyWays PDLC. Out of it comes one thick line in the phase hues that closes into a loop: a station at the start of each phase, the sign-off just before the third, each phase's aircraft beside its name. Above the line, the question each phase asks; below it, what a team hears when the question was skipped. Its caption says the methods stay: you still pick one. | `pages/spine.py` `figure`, `.spine` |
| Method table | Four methods as bars under the same four phases: solid for a phase covered, dashed for a light touch, hollow for a stage this manual adds (extended BMAD). The last row is words: four decisions no method makes for you. A real table. | `pages/spine.py` `coverage`, `.cover` |
| Role rows | One row per role: code, name, where you start, where you end up, counts. A list, not cards. | `.seats` |
| Day card | One real day of the game: its room in pixels at a whole multiple, bled to the card's edges, the kicker, the headline, the context, the question and the answers with their price in days. Its metrics are the one component the simulator's title and its days in play share: the paper surface, a 20px corner, one 26px inset, three sizes (the 12.5px mono kicker, a headline of up to 25px, 15.5px for what is read) and answers 48px tall with a plain mono price. | `.daycard`; in the game `.nd-day`, `.nd-opt` |
| Late start's briefing | Before the day a late start opens on, one card on the day card's surface, corner and inset. A heading says the earlier days were played the recommended way. Under it the calls, one line a day with who made each and its price in days, and under a day anything else that moved the runway or trust; the documents on file in two columns, each with its day; where the run stands, the meters as the day shows them with trust's number beside its pips. One button opens the day. From about Day 20 the card is taller than a laptop's window, so the button's row sticks to the window's foot, on the card's paper under a hairline, and rests at the card's end. On a phone the calls stack, the documents take one column and the button spans the card. | `play/game.js` `briefScreen`, `.nd-brief` |
| Track list | The tutorial's eight tracks in order: a number, a name, a count, under a hairline. On the home page one sketch from a lesson sits beside it, as a sample, and links to its lesson. | `.jump.tracks`, `.learn-g` |
| Lesson sketch | One metaphor on a sheet of paper: a small black worker doing the thing the paragraph just said, two to six handwritten notes, a caption in real type underneath. At most one in a lesson, and about thirty in all, in the lessons whose idea a picture explains. It sits after the paragraph that turns, never touching a table or another picture. With the caption covered, a stranger can state its point, and its labels are the case's own nouns and numbers. Drawn in code. | `pages/sketch.py`, `content/learn/sketches/` |
| Shelf tile | A count, a name, one line. Four of them: templates, prompts, mental models, pictures. | `.shelf .tile` |
| Page head | Eyebrow, name, one line, a row of counts, optionally one or two buttons. | `.phead`, `.pmeta` |
| Folded how-to | "Who this page is for, and how to use it", closed by default. | `pages/_kit.orient` |
| Section rail | The sections of a long page down the left on a wide screen, the current one marked. Role pages and the leadership page. | `.rail`, `site.js` |
| Numbered section | A mono "01" over each heading where the order is real, with 52 to 88px between sections. | `main.numbered` |
| Ruled columns | Paragraphs that used to sit in bordered cards: a hairline above, no box. | `.three`, `.claims`, `.pair`, `.mix`, `.lc` |
| Step | One surface. Its table, artefact and example are ruled, not boxed; its head links straight to its template and prompts. | `render.step_html` |
| Lab comparison table | The lab's own model and three more, side by side, under a mono caption that names the prompt. The row heads take 24% of the width and the four models share the rest; from 1001 to 1180px, where the lab's bench is narrowest, the type is 13px. On a phone each row is one block, each cell beside its model's name. Each cell is built from words of its reply, and the build holds it to them. | `pages/labs.py` `_others`, `.lab-t` |
| Next up | The foot of a reference page: one sentence, one button, and at most one quiet link beside it. | `render.next_up` |
| Pause control | A checkbox, so it works without script; stills whatever holds it. | `render.MOTION_TOGGLE`, `.mpause` |

## Do and do not

Do:

- Cut before you decorate. If a block repeats a link the page already carries, remove the block.
- Give every band a picture that is the thing itself: the lifecycle as a loop four methods feed, the
  methods as bars on it, the roles as rows, the simulator as its own screen, the tutorial as its tracks and
  one of its sketches.
- Design every moving thing from its last frame backwards, and check that frame in print, without script
  and under reduced motion before the motion is written.
- Say it in words a newcomer has: "sign-off" beside "hard gate", "pass mark" beside "bar". A house word
  appears on a landing page only next to the plain one.
- Give two kinds of thing two kinds of mark. The lifecycle and a building method are not drawn alike: in
  the method table the methods are bars and the spine's row is words.
- Show the reason before the thing. The spine is introduced by what goes wrong without it.
- Keep numbers honest and computed. Lesson, template, prompt and picture counts come from the content
  at build time.
- Measure contrast and overflow; do not judge them from a screenshot.

Do not:

- Put more than two buttons in one view, or more than one routing device on one page.
- Explain the method twice on the home page. It gets two pictures, and each does one job: the lifecycle
  figure says what it is made of and why, the table says where the methods a reader has heard of sit on
  it. The boards live on `/method/`.
- Use a second accent colour, a gradient as decoration, or capitals with wide tracking.
- Point a control at the page it is on.
- Draw a sketch whose worker could be removed without loss, or whose caption only repeats the paragraph
  above it.
- Greet a reader with a popup. Nothing appears that was not asked for.
- Write a heading that is a category ("Overview", "Features", "Resources").
