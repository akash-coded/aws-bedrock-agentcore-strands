---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-03
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
  accent: "a page's own: slate by default, a role's colour on its page, sky on the FDE guide (78% sky on the light page)"
  sketch-paper: {light: "#FFFFFF", dark: "#D0CBBF"}  # a sketch's sheet, with deeper pens in the dark theme
typography:
  display: "Instrument Sans, 600 to 620, tracking -0.035em to -0.045em"
  body: "Geist, 400, 16 to 19.5px, line-height 1.55 to 1.62; a lesson's body 19px on 1.58 (17px on a phone)"
  mono: "Geist Mono, 500, 12.5px: eyebrows, counts, codes"
  hand: "Patrick Hand: on a sketch's sheet of paper, and on the home page's method map, where it says who made each method and when (16px or more, in ink2, eight notes at most)"
  scale: {hero: "clamp(40px, 5.1vw, 70px)", page-h1: "clamp(34px, 4.6vw, 58px); clamp(32px, 4vw, 50px) inside a column", band-h2: "clamp(29px, 3.5vw, 46px)", page-h2: "clamp(21px, 2.2vw, 27px) at 620", lesson-h1: "clamp(30px, 3.6vw, 46px)", lesson-h2: "30px (24px on a phone)", lede: "clamp(17px, 1.5vw, 19.5px)"}
rounded: {inner: 11px, box: 16px, tile: 20px, pill: 999px}
buttons: {small: 36px, default: 43px, large: 51px, phone: "44px or more"}
spacing:
  band: "clamp(72px, 9.5vw, 128px) above and below every home section"
  measure: "46 to 56 characters for a lede, never the full row"
  lesson: "text 584px, pictures 944px, the guide 240px from 1280px; six gaps: 8, 16, 18, 24, 32 and 64px"
  wrap: 1280px
motion: {durations: [150ms, 250ms, 350ms, 400ms, 600ms], easing: "cubic-bezier(.22,1,.36,1)", spring: "the hero's aircraft at a phase boundary: up 20% and back in 0.42s", stagger: "the hero's rest names, a quarter of a second apart; nothing else arrives in order", reduced: "everything still: the hero's rest frame, its four forms parked in their phases and named, drawn once"}
components: [header, header-slot, hero-scene, section-head, method-map, chooser, role-rows, people-card, day-card, late-start-briefing, lesson-sketch, flagship-card, library-tile, consultancy-close, page-head, folded-howto, section-rail, lesson-guide, numbered-section, ruled-columns, step, fde-framework, altitude-table, fde-step-blocks, fde-stage-brief, lab-comparison-table, next-up, pause-control, focus-ring]
---
<!-- RC-B: confirm the front matter against the merged code: the radii and button sizes (U3), page-h2 (U3). -->

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
with one strong picture per section. It is signed by its author in the hero's last line and the footer, and
the home page closes on his consultancy's offer to apply it.

SkyWays is three things, and the page always says which. **SkyWays** alone is the publisher and the method
(the SkyWays PDLC). The airline in the worked case is always "a fictional airline" on first mention.
**SkyWays Consultancy**, the author's consultancy, is written in full every time, and never enters the
game's fiction.

## Colours

Near black is the page a reader opens. Warm paper is the light theme, chosen with the toggle and
remembered; paper is always printed light. One ink ramp (ink, ink2, soft). Colour is spent on meaning only:

- The four phase hues mean P0, P1, P2 and P3 wherever they appear: the hero's flight (its path, its tag's
  code and the aircraft itself: a slate dart, an indigo drawing, a teal airliner, an amber jet, in outline
  until the sign-off and solid after it), the method map's column heads and question rules, the chooser's
  rule over the SkyWays PDLC, the boards, the role roadmap, and the FDE framework's columns. A phase never
  changes hue between pages. Methods stay neutral on the map, and the FDE guide's stages stay in ink.
- Rose means the sign-off (the lessons' hard gate), what is owed, and the signature that ends each of the
  FDE guide's three stages.
- The globe is blue, sea and land, with a blue limb. It never wears a phase hue: those belong to the
  flight round it.
- A sketch has three pens of its own beside its ink: red for the point, orange for the path, blue for
  the aside. They live on the sketch's sheet of paper and mean nothing off it. In the dark theme the sheet
  is toned (`#D0CBBF`) and the pens deepened, on every page, so its notes keep 4.5:1.
- A role's accent tints its own page and its row on the home page. The FDE guide's accent is sky, mixed
  toward the ink to 78% on the light page, where sky alone reads about 4.2:1 as small text; it never appears
  inside the framework picture.
- Indigo is the plane in the mark.

Large display text may continue in a grey second sentence (ink mixed 48% into the page). That grey is
for display sizes only; it measures 3.4:1 to 3.8:1, which passes for large text and fails for body text.
A lesson's title does the same: the lesson's name in ink, the rest of its search title, after the first
": " or "? ", in the grey. It is 30px at its smallest, so it stays large text (3.8:1 dark, 3.7:1 light).

## Typography

Headings are sentences with a verb or a question in them, set in sentence case at weight 600 to 620.
A band with a paragraph has one heading and one paragraph, side by side on a wide screen; a band without
one may run its heading into a grey continuation at the same size. Body text stops near 54 characters on a
landing page and near 75 in a lesson. Small labels (eyebrows, counts, role codes) are Geist Mono in sentence
case; no text is set in capitals by the stylesheet. No label is under 11px.

Handwriting appears in two places: on a sketch's sheet of paper, at 13px or more on a phone, and on the
home page's method map, where it says who made each method and when. Off paper it is in ink2 only, never in
a sketch's pens, 16px or more at every width, and eight notes at most.

A heading's size follows its body: an inner page's h2 is about 1.6 times its text, 27px at 1440 over a 16
to 16.5px body, and a lesson's is 30px over 19px. A lesson is set for reading: the body 19px on a 1.58
leading from 901px wide and 17px on a phone; the title 46px on 1.08 across the column, in two lines on a wide
screen; the lede 22px, balanced so it never ends on a word or two; section heads 30px (24 on a phone); step
heads 21px at 620 with their tracking opened to -0.004em and their word spaces widened, so "Step 1 · Ask"
never closes up (19 on a phone); "In short" and "Try it" 18px (the body's size on a phone); captions and
table cells 15px. A heading under 24px is never tracked tighter than -0.005em. A hyphenated word in a title
never breaks across a line.
<!-- RC-B: confirm the inner-page h2 (27px at 620) and "no capitals by the stylesheet" against U3. -->

## Layout and spacing

- The first screen of the home page holds five things: the eyebrow, the headline, one sentence, two
  buttons, one picture. The meta line under the buttons is the only other text.
- One idea per band: a heading, at most one paragraph of thirty words, one picture or list, one way on.
- Bands are separated by space and a hairline, not by boxes. On the home page a card exists only where it
  is a destination, in the library; the close is the page's one framed panel that is not a destination
  card, because it is the only offer.
- On a reading page, text sits on the page under a hairline. A box is kept for what is a thing in
  itself: code, a table, a diagram, a calculator, a verdict.
- Reading text is capped near 75 characters a line, whatever the column's width. A lesson reads in one column from
  the page's left edge: text at one measure (584px, about seventy-five characters of the 19px body), and boards,
  drawn figures, code and tables of three columns or more to the column's edge, 944px, as the title does from
  1280px wide. So a lesson has one left edge and two right ones, and a caption starts on its figure's own edge.
  Nothing floats: a sketch follows the paragraph it draws, at the text's width, and "Try it" is a card where the
  lesson reaches it. From 1280px wide a guide sits on the right, sticky, 240px and 48px from the column: the track
  and the lesson's place in it, the previous and next lessons, the lesson's sections with the one being read
  marked, the course folded. Between 1280 and 1320px the guide gives way first, to 214px, so the column keeps
  938px and every wide board stays drawn. Narrower, the column is centred, and the guide's two lists are two folds
  side by side under the meta line.
- A reading page keeps its navigation on the right; a reference page (the roles, leadership, the libraries,
  the Tool guides, the FDE guide) keeps its section rail on the left. The tutorial's front page and its track
  pages keep the course on the left, because there the course is the content.
- Blocks in a lesson sit at six gaps: 8px under a step head, 16 under a section head and between a step head
  and a box, 18 between paragraphs, 24 from a section head to its first step head, 32 between text and a box
  either way and above a step head, 64 above a section.
- A drawn figure runs to the picture column; a small one, a few bars and no notes, keeps to the text's
  width. A figure draws no number its lesson's text does not state (ten older placements still do: see
  `EXPERIENCE.md`, Open items).
- A lesson's opening map takes at most 70% of a 1440 by 900 screen, 630px for its figure. It fits by using
  the width (more cells across, the bands as cards side by side, a side list beside the end), never by
  smaller type. Where even that is too tall, its words are cut.
- In a lesson's table, a column whose body cells are all numbers, amounts or percentages (one unit they
  all share, such as "a day", allowed) is set right, its header with it, in figures of one width. Text
  columns stay left. On a phone, where a table of three or more columns stacks, every cell reads left
  under its name, and no table scrolls sideways.
- In the tutorial's rail a track's rows start on its heading's left edge, so the current lesson's
  highlight does too. Every row's number and title sit in the same two columns.
- A landing page opens with its name, one line, one row of counts, then its content. Anything that
  explains how to use the page is folded behind one line. One page head serves every landing page, in two
  variants (full width and inside a column), with one eyebrow 16px above the title in the page's accent.
- The hero is asymmetric: words left, picture right, the picture allowed to run off the edge. On a
  phone the words come first and the picture follows.
- A band whose heading has a paragraph sets the two side by side on a wide screen, so the question and
  its picture start on the same screen at 1440 by 900.
- On a phone the top bar sits on the page's 20px column: the menu icon starts on it and the theme circle
  ends on it.
<!-- RC-B: confirm the one page head and its eyebrow against U4. -->

## Motion

Nothing moves without a job. A screen may carry one ambient motion, with its own pause control (the hero's
flight; the tower on the method page; the game's building); everything else plays once and ends within about
two seconds. A thing may move only if the movement does one of three
jobs:

1. **It answers something the reader did.** A button pressed, a list opened, a step unfolded, "Copied", the
   day card turning to face a reader who points at it.
2. **It says where the reader is.** The rail, or a lesson's guide, marking the section being read.
3. **It shows a thing that is itself a sequence.** The four phases in order, as the hero flies them.

Two classes of motion, with different rules.

**Transitions** answer the reader and take 150, 250, 350 or 400ms on the one easing curve; one long line
may take 600ms to draw. Opening takes longer than closing: a list opens in 250ms and leaves at once. The
day card turns to face the reader in 400ms on hover or keyboard focus inside it, and never moves on its own.
A spring is for a small thing that changes shape, and never moves text or a height: in the hero, the aircraft
at each phase boundary. The hero's entrance, the launch and the camera's pull-back, plays once in a sitting;
a reader who comes back finds the whole Earth.

**Explanatory motion** shows a sequence, and its last frame is the complete picture, which is also what a
reader with reduced motion, a printer and a reader without script get. Anything that keeps moving for more
than a few seconds carries a pause control, and the hero also comes to rest by itself. Dashes on a connector
move only while the reader scrolls past them, in a browser with scroll timelines. Everything else on a page
is complete when the reader reaches it: no band, figure, map or sketch waits to be scrolled to.

The hero runs on one clock (`theme/hero.js`, which reports its own moments in `window.GlobeTimes`). A round
is 28.55 seconds. In front of the Earth each phase takes five seconds at the flight's pace, and the flight
slows to under a third of that pace for about 1.3 seconds either side of the sign-off's bar, so P1 and P2
take 6.3 seconds each; the way back, behind the Earth, takes about six. The Earth turns once in 75 seconds. A
first visit in a sitting launches: the dart waits 0.9 seconds close on the Earth's edge, at 1.55 times the
whole view, then flies as the camera pulls back, reaching the whole Earth as the drawing is signed; the
stage's edges fade while the camera is close. At each boundary the aircraft springs (up 20% and back in 0.42
seconds), changes form and hue and leaves a trace of the form it had, and a tag beside it names the phase,
says what the thing has become and asks the phase's question. In its second round (its first on a later
visit) it eases to a stop in the middle of Run & Learn, the forms are named a quarter of a second apart, and
drawing stops, 49.8 seconds into a first visit and 21.5 into a later one: the rest frame, which is also all
that reduced motion draws. The pause control holds the flight, the camera, the forms and the tag together.
At most sixty frames a second; in no frame a blur, a filter, a new gradient, a pixel read back, or text set
or measured.

Three rules of choreography. One sequence at a time on a screen: on the home page only the flight moves. An
entrance plays once per visit and never again on scrolling back. Every animation is designed from its final
frame backwards, because the final frame is what most readers, every printer and every reduced-motion reader
will see.

Refused, each for a reason: numbers that count up (a true number shown false), cursor glows and spotlights
(nothing on a phone), text that slides in, on any page, and bands that rise as they are reached, a second
drawing of a route the page already draws (the hero's next round is the exception: it is what makes the loop
a spiral), any animation library, parallax, a figure that draws as the page is scrolled (stop halfway and it
is half drawn). Council 10 added: a literal rocket, with stages that fall away and an exhaust plume (dropping
a stage says a phase's work is spent, when each phase leaves a record the next is held to); a camera that
moves every round or follows the scroll; a tag that types itself; glow, bloom and particles; motion on the
method map; a reading-progress ring, slide-in text or parallax on a lesson; a spiral, a rocket or any motion
in the FDE framework, which is read, not watched.

## The simulator's picture

The game at `/simulator/` is the one place the site uses pixel art, and it follows the same rules as
everything else: hue means phase, rose means the sign-off and what is owed, words are real type, motion
has a job and can be paused. Its colour comes from light and material: each room's walls take a little of
its owner's hue, and the sky outside tells the phase, one still sky a day, from dawn on Day 1 to dusk on
Day 90 (night, if the run is late). The canvas is the same in both themes. The home page shows two of its
rooms as still pictures, drawn by the game's own code at one times and shown at whole multiples: Day 45's QA
room on the day card, and the boardroom on Day 90 on the library's simulator card. `GAME.md` has the detail.

## Elevation and depth

Depth is used three times. The hero's globe has a lit side, a blue limb and a glow. A sketch sits on a
sheet of paper, the one light surface on a dark page. The home page's day card stands in perspective over
1000px: turned 9 degrees about its right edge and tipped back 3 under a 1700px perspective, with one long
shadow (a deeper one of its own in the dark theme), a 6px ring of ink and a 1px light edge along its top.
Hover, or focus inside it, turns it to face the reader. It is the one tilted object on the site: the game's
canvas, and the game's own Day 1 card, are never tilted. At 1000px and under, and on paper, it is flat; in
the game the building takes the flat card's corner and shadow. Everything else is flat on the page with a
1px hairline; a library card lifts 3px under the pointer, and casts no shadow.

## Shapes

Three radii and no fourth: 11px for a control and for a box inside a box, 16px for a box on the page, 20px
for a tile, the day card and the close's panel (`--r-in`, `--r-box`, `--r-tile`); Copy keeps 8px inside its
dark header. Buttons come in three heights at 1440, 36, 43 and 51px, and every button is 44px or taller on a
phone. Pills are for things that are tags, the one filled button in the header, and the sign-off's labels on
the method map. The method map's shapes are 36px tall at the inner radius, so a method reads as one span
across the phases it covers.
<!-- RC-B: confirm the radii, the tokens and the button heights against U3. -->

## Components

| Component | What it is | Where it lives |
| --- | --- | --- |
| Header | Mark and name, five places (two of them short lists), the slot, the theme toggle. The toggle is a circle with its left half filled, drawn in SVG at the menu icon's size, line and colour (18px, a 1.5px line). It is never a character: "◐" fell back to a font that drew a dot. The workbench's top bar draws the same. The Roles list names six roles, the forward-deployed engineer's guide among them. The drawer holds every page and the search. | `render.shell`, `render._nav`, `render.HALF` |
| Header slot | One filled pill and, on a wide screen, one quiet link. The pill never points at the page it is on: in the manual it offers the simulator, in a lesson the day of the game that lesson is the reading for, in the game the lesson behind the day on screen. The quiet link is the next useful place from here ("Apply it", "Manual", and on the FDE guide's pages "The lesson", the field guide). | `render._ctx`, `.ctx` |
| Hero scene | A blue dotted Earth turning once every 75 seconds and one flight round it through P0 to P3, staged like a launch: a slate paper dart, an indigo drawing in dashes on blueprint, a solid teal airliner from the sign-off, an amber jet with contrails. A tag on a chip, joined to the aircraft by a hairline, names each phase, what the thing has become and the phase's question. It all but stops on the sign-off. At rest: four forms named on chips, and on a stage 400px or wider the sign-off and the way back. Without script, the disc and the line of names. | `pages/globe.py`, `theme/hero.js` |
| Section head | Mono eyebrow, a heading that continues in grey, one optional paragraph. | `.sec-h` |
| Method map | The SkyWays PDLC as a frame, P0 to P3 across its top, each head carrying the hero's form for its phase in its hue. Each method a shape as long as the phases it covers, its ends in words; a handwritten note says who made it and when, every note sourced and dated in the data, which the build checks. All five meet in the build (the teal wash); under them, the four questions no method reaches, with what a team hears when each was skipped. A CSS grid, not a drawing: every word is real text. | `pages/spine.py` `methods_band`, `.vm` |
| Chooser | Four ruled columns: the pair every team needs, then three yes-or-no questions that each add one method; the SkyWays PDLC's rule in the four phase hues. With nothing chosen both lines show; a choice hides the other line and No greys the name, in CSS only. | `pages/chooser.py` `band`, `.pk` |
| Role rows | One row per role: code, name, where you start, where you end up, counts. A list, not cards: seven rows, six roles (the forward-deployed engineer's guide among them) and the sponsor. The words sit on the band's column; the hover tint reaches 12px past it (4px on a phone) as side shadows, and only the arrow moves. | `.seats` |
| People card | One of four on the home page's tutorial band, in the lifecycle's order: a card-sized sketch (the worker, one prop, one or two handwritten labels), the person's name and job from the game's cast in mono, the question in quotes as an h3, the lesson's answer in one sentence of 24 words or fewer, and a ruled foot with the lesson's minutes and short name. No box. The whole card is one link, to that lesson, never to a role page. Four across from 1181px, two by two from 601, one column at 600 and under, the picture on top. On hover the arrow moves and the rule darkens; nothing lifts. | `pages/people.py`, `.qs`, `.q` |
| Day card | One real day of the game: its room in pixels at a whole multiple, bled to the card's edges, the kicker, the headline, the context, the question and the answers with their price in days. Its metrics are the one component the simulator's title and its days in play share: the paper surface, a 20px corner, one 26px inset, three sizes (the 12.5px mono kicker, a headline of up to 25px, 15.5px for what is read) and answers 48px tall with a plain mono price. On the home page an "Example day" pill sits at the picture's top left (Geist Mono 11.5px on a dark pill, one colour in both themes, printed as it shows), and over 1000px the card stands in perspective. | `.daycard`, `.dc-ex`; in the game `.nd-day`, `.nd-opt` |
| Late start's briefing | Before the day a late start opens on, one card on the day card's surface, corner and inset. A heading says the earlier days were played the recommended way. Under it the calls, one line a day with who made each and its price in days, and under a day anything else that moved the runway or trust; the documents on file in two columns, each with its day; where the run stands, the meters as the day shows them with trust's number beside its pips. One button opens the day. From about Day 20 the card is taller than a laptop's window, so the button's row sticks to the window's foot, on the card's paper under a hairline, and rests at the card's end. On a phone the calls stack, the documents take one column and the button spans the card. | `play/game.js` `briefScreen`, `.nd-brief` |
| Lesson sketch | One metaphor on a sheet of paper: a small black worker doing the thing the paragraph just said, two to six handwritten notes, a caption in real type underneath. At most one in a lesson, 31 in all, in the lessons whose idea a picture explains. It sits in the flow after the paragraph that turns, at the text's width, never touching a table or another picture. With the caption covered, a stranger can state its point, and its labels are the case's own nouns and numbers. Drawn in code. | `pages/sketch.py`, `content/learn/sketches/` |
| Flagship card | One of the library's three tools, the first row: a picture on the material of what it opens, the same in both themes (the workbench's navy panel with its acceptance bar calculator in real type; the lessons' paper with the eight tracks; the game's dusk with the boardroom on Day 90 at whole pixels), a hairline, a mono count, the name, one line and the action. The whole card is the link. | `pages/homelib.py`, `.lib .fl` |
| Library tile | A count, a name a set distance below it, one line, an arrow; six of them in two rows under the tools, 178px tall at 1440 so a row's names align. On a phone, a count and a name, two to a row. The Tool guides' index keeps the older tile for its manuals. | `.lib .shf`; `.tg .tile` |
| Consultancy close | One panel on the page's ground: radius 20, a 1px rule, the raised surface, 64px inside at 1440 and 20px at 600 and under. The eyebrow "SkyWays Consultancy", the heading and its line, four offers as ruled columns (four over 1000px, two from 601, one below), each its name, what we do and "You leave with" (a mono label that runs into its words on a phone), then one filled button and its line. | `pages/consult.py`, `.cx` |
| Page head | Eyebrow, name, one line, a row of counts, optionally one or two buttons. One component in two variants, full width and inside a column, with one eyebrow class in the page's accent. | `.phead`, `.pmeta` |
| Folded how-to | "Who this page is for, and how to use it", closed by default. | `pages/_kit.orient` |
| Section rail | The sections of a long page down the left on a wide screen, the current one marked. Role pages, the leadership page, the libraries, the Tool guides' manuals and the FDE guide: on its hub the guide's eight sections and its three stages, on a stage page all twelve steps by stage, its own four marked as you read and the other eight linking their pages. | `.rail`, `site.js` |
| Lesson guide | The one thing beside a lesson, from 1280px: the track, "Lesson n of N", a bar for each lesson of the track with this one in the accent (a picture, not links), the previous and next lessons, the lesson's sections with the one being read marked, the course folded and opened at the current lesson. Navigation only. Under 1280px its two lists are two folds under the meta line. | `learn._guide`, `.lguide`, `.lfolds` |
| Numbered section | A mono "01" over each heading where the order is real, with 52 to 88px between sections. The FDE guide's hub has eight. | `main.numbered` |
| Ruled columns | Paragraphs that used to sit in bordered cards: a hairline above, no box. | `.three`, `.claims`, `.pair`, `.mix`, `.lc` |
| Step | One surface. Its table, artefact and example are ruled, not boxed; its head links straight to its template and prompts. | `render.step_html` |
| FDE framework | The whole job in one picture: the three stages down the side in ink (Frame, Deliver, Evolve, each with its span and the client's people), the manual's four phases across in their hues, one step in each cell (chip and number, short name, question, artefact), a rose "Signed" pill under each row with what is signed and by whom. A 150px stage column and four equal columns 8px apart, cells at the inner radius with a 3px top edge in the phase's hue; on a phone the stages stack and each stage's four steps sit two by two. On a stage page its own row is open and the others keep their names and four step names, never dimmed. Read, not watched: nothing moves but a 2px lift under the pointer. For a screen reader, three lists of four links. | `pages/fde.py` `figure`, `.fx` |
| Altitude table | The FDE hub's section 03: four columns, POC, MVP, build and deploy, each with the steps that think at it, and nine rows (the question, you think about, code, evidence, you may skip, never skip, your AI tools, ends with, the trap). Stacked on a phone, every cell under its column's name. | `pages/fde.py`, `.fdt` |
| FDE step blocks | A step on a stage page is the role step with the guide's additions: in its head a row of chips, "Hats" then each hat, and its altitude in an ink-bordered chip; after the activities, "If your client is inside your own company" on the accent's 3px edge, and "Say it like this", the situation in mono over the words in quotes, each capped at the step's measure. Deliver's examples are two paragraphs, the case and your move. | `pages/fde.py` `_step`, `.fhat`, `.fint`, `.fsay` |
| FDE stage brief | A stage page's opening: the eyebrow "The FDE guide · stage n of 3", the stage's name and question, its counts, the framework with its row open, then the stage in brief, five ruled rows headed in mono (how long, the client's people, you think at, it ends with, what goes wrong here). | `pages/fde.py` `stage` |
| Lab comparison table | The lab's own model and three more, side by side, under a mono caption that names the prompt. The row heads take 24% of the width and the four models share the rest; from 1001 to 1180px, where the lab's bench is narrowest, the type is 13px. On a phone each row is one block, each cell beside its model's name. Each cell is built from words of its reply, and the build holds it to them. | `pages/labs.py` `_others`, `.lab-t` |
| Next up | The foot of a reference page: one sentence, one button, and at most one quiet link beside it. The FDE stage pages lead to the next stage; Evolve's leads back to Frame, with the hub beside it. | `render.next_up` |
| Pause control | A checkbox, so it works without script; stills whatever holds it. In the hero it sits in the stage's bottom right corner. | `render.MOTION_TOGGLE`, `.mpause` |
| Focus ring | 3px in the page's accent, 2px outside the thing focused. Where the box that holds it clips (a step's rounded corner, a code box, a picture card, a rail, the drawer's list) it is drawn 3px inside; on a code box it takes the dark theme's slate, `#7FA9CC`, in both themes. | `base.css` `:focus-visible` |

<!-- RC-B: confirm the Page head row against U4. -->

The workbench keeps the same floor in its own file: its opening picture sets every label at 15 units and is
drawn only on a card 420px or wider, and narrower the card shows the same four phases as an HTML list; its
focus ring is the manual's; on a phone its top bar's controls are 44px tall, and under 386px the Simulator
pill is its play mark alone.

## Do and do not

Do:

- Cut before you decorate. If a block repeats a link the page already carries, remove the block.
- Give every band a picture that is the thing itself: the methods as shapes on one lifecycle, the chooser's
  rule in words, the roles as rows, the tutorial as four people and their questions, the simulator as one
  real day, the library as the things themselves (the workbench's calculator, the tutorial's contents, a
  room of the game), the consultancy as its offers.
- Design every moving thing from its last frame backwards, and check that frame in print, without script
  and under reduced motion before the motion is written.
- Say it in words a newcomer has: "sign-off" beside "hard gate", "pass mark" beside "bar". A house word
  appears on a landing page only next to the plain one.
- Give two kinds of thing two kinds of mark. On the method map the SkyWays PDLC is the frame and the methods
  are shapes inside it; the lifecycle is never a sixth shape.
- Show the reason before the thing. The map's last row is the four questions no method reaches, each with
  what a team hears when it was skipped.
- Keep numbers honest and computed. Lesson, template, prompt, picture, decision and calculator counts come
  from the content at build time; the handwritten notes on the map come from dated sources.
- Measure contrast and overflow; do not judge them from a screenshot.

Do not:

- Put more than two buttons in one view, or more than one routing device on one page.
- Explain the method twice on the home page. The map says where each method sits and who made it; the
  chooser says which to use, in words. The boards live on `/method/`.
- Use a second accent colour on a page, a gradient as decoration, or capitals.
- Point a control at the page it is on.
- Draw a sketch whose worker could be removed without loss, or whose caption only repeats the paragraph
  above it.
- Greet a reader with a popup. Nothing appears that was not asked for.
- Write a heading that is a category ("Overview", "Features", "Resources").
- Put a logo, a testimonial, a count of clients or years, or a price in the close, or print the contact
  address in a page: without script the close's button goes to the discussions page.
- Colour the FDE guide's stages, or dim a stage page's other rows: hue means phase, and dimming takes the
  labels under 4.5:1.
