# Sketches

About thirty lessons carry a sketch, one each. A lesson that has one has a file here named for its slug,
with a `SKETCHES` list of one entry: the hand-drawn picture, placed in the lesson with `{{sketch:name}}`
on a line of its own. A lesson whose idea a picture does not help has no file and no sketch.

```python
from pages.sketch import Sk

def pebbles(s: Sk):
    s.ground(540, 50, 1150, tufts=3)
    ...

SKETCHES = [
    {"name": "four-pebbles-one-rock", "idea": "the bar is where right answers just pay for wrong ones",
     "verb": "balance", "prop": "plank over a log",
     "alt": "A plank balances on a log. A rock sits on one end. A worker lowers a fourth pebble onto the other "
            "end, and the plank comes level.",
     "caption": "The bar for partner flights is 80% because one wrong answer weighs as much as four right ones.",
     "draw": pebbles},
]
```

## What a sketch is for

A lesson's map shows the process. A sketch shows the one idea in it that turns: a sentence you could
rewrite as "you would think X; in fact Y". It goes straight after the paragraph that says so.

The test, with the caption covered: a stranger who sees only the drawing can state its point, and its
labels are the case's own nouns and numbers (a refund, $400, fifteen agents, a pass mark of 80%) rather
than general words. A label has to carry its meaning without the lesson: "thirteen points" reads as story
points to a stranger, and "one line: the refund cap" does not say that money leaves.

Then two tests of removal. Take the worker out: if the picture still works, the worker was decoration, so
redraw it with the worker doing the verb. Take the sketch out: if the reader loses nothing the paragraph
did not already give, cut the sketch.

Four things the hat stand taught (`six-hats-one-head`, the 31st sketch), each found on outside readers who
had not seen the caption: a label beside the worker becomes who the worker is; labels stacked close read as
one title; a label in a coloured pen becomes the subject; a hat drawn as a dome, with no brim, peak or bobble,
reads as a dish.

Keep them few: one a lesson at most, about thirty in all, in the lessons whose idea is abstract, where a
picture helps most. A question bank or an exercise sheet has none.

## Where it sits

In a lesson a sketch follows the paragraph it draws, in the flow, at the text's width: 584px from 901px wide,
where its handwriting is about 28px, and the column's width on a phone. Nothing sits beside the text.

Two pages outside the lessons draw with the same engine. The forward-deployed engineer guide's hub shows
`six-hats-one-head` beside its section 02, by the sketch's name (`site/pages/fde.py`): beside the heading from
1240px wide, after the paragraph below that. The home page's tutorial band draws four card-sized cuts of lesson
sketches, one beside each of its four people (`site/pages/people.py`): the worker and one prop, two labels at
most of five words or fewer, handwriting at 64 units (13px on the narrowest card), 7 KB gzipped for the four
together, all checked when the site is built. In the dark theme every sketch, on every page, sits on the toned
paper with the deeper pens.

## The rules the build checks

- One sketch a lesson at most, and only its own: a file has one entry, a lesson has one `{{sketch:...}}`
  line, and the line names the sketch drawn for that lesson. Every entry is placed exactly once. A
  `{{sketch:...}}` that names no sketch stops the build as an unknown visual.
- One metaphor per sketch, and no metaphor twice: the pair (`verb`, `prop`) is unique across the
  tutorial, and no prop is used more than three times.
- Two to six labels, five words at most each, written at 58 units or more: 58 units is 13.5px in a 320px
  phone's 280px column and about 28px at 1440. The lint refuses a label under 54 units, 12.6px in that column.
- A caption in real type under every sketch: one or two plain sentences that make the point alone.
- An `alt` that describes the scene in one sentence.
- It sits after a paragraph, never straight under a heading, and never touching a table, a code block or
  another picture.
- No dashes in any text. 6,500 bytes compressed at most.

## How the thirty were chosen

In October 2026 the 77 sketches were cut to 30. Each drawing went, caption covered, to three vision models
acting as strangers, with one question: what point is this drawing making? Each answer was judged against
the caption (agrees, partly agrees, misses). Each sketch was then scored on that, on whether its labels
are the case's own, and on whether its lesson would lose something without it, and the best one in each
lesson that earned a place was kept. Most misses came from a label only the lesson explains.

## The pens

`ink` draws the scene. `point` (red) marks the thing that matters or fails. `path` (orange) is the route:
dashed, with a head. `aside` (blue) is a side note, and the model when it appears as a box with one eye.
`faint` is pencil.

## Credit

The style is adapted from **Ian's Xiaohei illustrations**
(<https://github.com/helloianneo/ian-xiaohei-illustrations>, MIT; English adaptation by tojileon): a white
sheet, black hand-drawn line, a small black worker who does the core action, and a few handwritten notes
in red, orange and blue. Those pictures are generated as images. These are drawn in code, in
`site/pages/sketch.py`, so the worker here is a relative of Xiaohei, not a copy of any of Ian's drawings.
The handwriting is Patrick Hand (SIL Open Font Licence).
