# Brief: hand-drawn sketches for the tutorial

You are an explainer illustrator and learning designer. You will add hand-drawn sketches to a set of lessons in the
tutorial of "SkyWays, the agentic manual" (repo: `.`).
The sketches are drawn in code with an engine that already exists. Your lessons are listed in the message that sent
you here. Do not commit, do not push, do not run git commands that change state.

Below, `SP` means `handoff/round-8/notes`.

## Why (the owner's words)

"To improve the explainability of things and make it easier to comprehend and grasp, use this skill for annotated
hand-drawn illustrations to add impressive, relevant, contextual, adding more hints and information kind of
illustrations to the tutorial. Not just one per tutorial, try to add as and wherever and whenever you feel there is a
need, it adds value." The skill they mean is Ian's Xiaohei illustration style: a white sheet, black hand-drawn line, a
small black worker who performs the core action, and a few handwritten notes in red, orange and blue.

## Read these first, in this order

1. `site/content/learn/sketches/README.md` (what a sketch is for, the rules the build checks, the pens)
2. `site/pages/sketch.py` (the engine: every primitive and prop, with docstrings; read all of it)
3. The three finished examples: `site/content/learn/sketches/p0-frame.py`, `the-hard-gate.py`,
   `how-accurate-must-an-ai-agent-be.py`, and how they look: `SP/sk/mine.jpg` (open it with the Read tool).
4. The style you are matching, for line density, white space and how much the worker does (open with the Read tool):
   `SP/ext/ian-xiaohei-illustrations-en/examples/images/01-two-breakpoints.png` and `08-trust-bridge.png`, and the
   skill's `SP/ext/ian-xiaohei-illustrations-en/ian-xiaohei-illustrations/references/composition-patterns.md`.

## What the council decided (these are not up for debate)

- **No quota.** One to three sketches per lesson; zero is allowed and is the right answer for a question bank or an
  exercise sheet unless one idea really turns. A lesson never has more than four drawn pictures counting its flow map
  and figures (`{{map:…}}`, `{{figure:…}}`, `{{board:…}}` and so on are pictures; so is a mermaid block).
- **Where a sketch goes.** After the paragraph that states a turn: a sentence you could rewrite as "you would think X;
  in fact Y". Three good slots: the ache (after the paragraph that closes "Sound familiar?"), the turn (in the steps),
  the cost ("Why it matters"). Never beside the flow map, never touching a table, a code block or another picture,
  never straight under a heading, never inside "Try it", the FAQ, the role table or the sources. Two sketches in one
  lesson have at least a heading or three paragraphs between them. If the paragraph already holds a metaphor, draw
  that one.
- **Two removal tests.** Remove the worker: if the picture still works, the worker was decoration; redraw with the
  worker doing the verb (carrying, twisting, pushing, catching, stuck in it), about a third of the sheet's height or
  more. Remove the sketch: if the reader loses nothing the paragraph did not already give, cut the sketch.
- **One metaphor each, none twice.** Turn the abstract idea into a physical action (get stuck, leak, sort, wring,
  weigh, post, unpack) and the system into a low-tech object (a drawer, a pipe, a letterbox, a scale, a well, a
  ladder). The pair (`verb`, `prop`) must be unique across the whole tutorial and other illustrators are working on
  other lessons at the same time, so be specific to YOUR paragraph: prefer the odd, exact object the paragraph
  suggests over a generic funnel, bridge, gate, ladder or conveyor. Already used, do not reuse: a gutter from a
  meeting table, a cloud wrung over a jug, a turnstile with a coin box, a cardboard box in a kitchen, a plank over a
  log, a mattress under plates, a dust sheet over lumps.
- **Words on the sheet.** Two to five labels (six is the hard limit), one to five short words each, in plain words a
  newcomer knows. Numbers must be quoted exactly from the lesson; never invent a number, a name or a result. Prefer
  the plain word to the house word ("pass mark" for "bar", "kind of case" for "slice") unless the paragraph the sketch
  follows has just defined the house word. No dashes anywhere.
- **Pens.** `ink` draws the scene and names objects. `point` (red) is the thing that matters or fails: one or two
  marks. `path` (orange) is the route or flow: usually one dashed arrow. `aside` (blue) is a side note, and the model
  when it appears as the `bot` (a box with one eye). The worker is a person on the team; the `bot` is the AI.
- **Caption and alt.** The caption is real type under the sheet: one or two plain sentences, 26 words at most, that
  make the point on their own and are true to the lesson. The `alt` describes the scene in one or two sentences.

## How to work, per lesson

1. Read the whole lesson (`site/content/learn/lessons/<slug>.md`). List its turns. Pick the one to three that a picture
   teaches better than the sentence does. Write down the ones you refuse and why (you will report them).
2. For each: idea, verb, prop, what the worker is doing, the labels and their pens, the caption.
3. Write `site/content/learn/sketches/<slug>.py` in the shape of the examples: one draw function per sketch and a
   `SKETCHES` list with `name`, `idea`, `verb`, `prop`, `alt`, `caption`, `draw` (and `h` if not 600). Names are
   lowercase-hyphenated and unique across the tutorial, so make them specific.
4. Place it: `python3 SP/sk/place.py <slug> <sketch-name> "<the first words of the paragraph it goes after>"` inserts
   `{{sketch:name}}` after that paragraph. This is the only edit you may make to a lesson file. (If you need to move
   it, edit that one line by hand.)
5. Render and LOOK. `python3 SP/sk/sheet.py <your-agent-letter> <slug> [<slug> …]` writes `SP/sk/<letter>.html` with
   each sketch at 760px and at 320px and any broken rule in red. Screenshot it:
   `sed 's/OUT/<letter>/' SP/sk/look.json > SP/sk/look-<letter>.json && node SP/drive.mjs file://SP/sk/<letter>.html SP/sk 1200 900 SP/sk/look-<letter>.json`
   (use the real path for SP) and open `SP/sk/<letter>.jpg` with the Read tool. If the sheet is long, render two or
   three lessons at a time.
6. Fix what you see. Expect three or four rounds per sketch. Common faults: a label lying across a line or across the
   worker; text clipped at the sheet's edge (keep text inside x 40 to 1160 and baselines above `h - 24`); the worker
   small or idle at the edge; everything in a strip along the bottom with a dead top half (lower `h`, or raise the
   scene); too many strokes (the sheet should be mostly empty paper); an arrow that points at nothing; a prop that
   does not read as what it is (simplify it, or name it with an ink label); the 320px version unreadable.
7. Check the rules: `python3 SP/sk/check.py <slug> [<slug> …]` must print `ok`.

## The engine in one screen (read the file for the rest)

Sheet: 1200 wide, 600 high by default (`"h"` from 380 to 675). Origin top left. A typical floor is `s.ground(540)`.
The worker: `s.worker(x, y, s=1.9, look=(dx, dy), arms=[left_target, right_target], legs="stand"|"walk"|"sit"|"none",
lean=deg, squash=1.0)`; `x, y` is the middle of the body, and its feet land about `106*s` below `y` (so on a floor at
540 with `s=1.9`, `y=339`). Give the arms targets on the thing it is doing something to.
Strokes: `stroke`, `line`, `curve`, `rect`, `oval`, `poly`, `blob`, `hatch`, `arrow`, `route` (the dashed orange path),
`burst`, `ring`, `squiggle`, `scribble`. Words: `label(x, y, text, pen, size=58, anchor="middle"|"start"|"end")`
(`|` breaks a line), `note(x, y, text, to=(tx, ty), pen)` (a label with an arrow to the thing). Never write below
size 54.
Props: `doc envelope binder box drawers sack tag sign flag stamp gate turnstile wall door hatchway letterbox ladder
scale seesaw funnel pipe dial lever crank conveyor jug bucket drop clock calendar magnifier lock coin stack rock
pebble marble cloud tangle spool string mattress sheet table shelf bridge cliff plane bot`.
Draw order is paint order: draw the worker before a thing that should cover its feet, after a thing it stands in
front of. Shapes with `fill="p"` are opaque paper and hide what is behind them.

You may NOT edit `site/pages/sketch.py` (it is shared). If you need a prop it lacks, write a small helper function in
your own sketch file from the primitives.

## Files you may touch

Only `site/content/learn/sketches/<slug>.py` for your lessons (new files), and one inserted `{{sketch:…}}` line per
sketch in `site/content/learn/lessons/<slug>.md` for your lessons. Nothing else. Do not run `site/build.py`: other
people are changing the site and the build is not yours to run.

## Report back

For each lesson: the sketches you made (name, the idea, verb + prop, the paragraph it follows, the caption), the
candidates you refused and why, and the path of the last screenshot that shows them. Say plainly which sketches you
think are weakest. Then the output of `check.py` for your lessons.
