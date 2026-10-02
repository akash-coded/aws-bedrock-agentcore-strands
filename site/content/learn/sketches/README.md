# Sketches

One file per lesson, named for the lesson's slug. Each has a `SKETCHES` list; each entry is one
hand-drawn picture, placed in the lesson with `{{sketch:name}}` on a line of its own.

```python
from pages.sketch import Sk

def wring(s: Sk):
    s.ground(520)
    ...

SKETCHES = [
    {"name": "wring-the-vibe", "idea": "a vibe cannot be sized; squeeze it until numbers come out",
     "verb": "wring", "prop": "cloud over a jug",
     "alt": "A worker twists a small cloud like a wet towel over a measuring jug; three marks on the jug carry numbers.",
     "caption": "Two days of work turned \"make rebooking smarter\" into one line with numbers in it.",
     "draw": wring},
]
```

## What a sketch is for

A lesson's map shows the process. A sketch shows the one idea in it that turns: a sentence you could
rewrite as "you would think X; in fact Y". It goes straight after the paragraph that says so.

Two tests, both of removal. Take the worker out: if the picture still works, the worker was decoration,
so redraw it with the worker doing the verb. Take the sketch out: if the reader loses nothing the
paragraph did not already give, cut the sketch.

## The rules the build checks

- One metaphor per sketch, and no metaphor twice: the pair (`verb`, `prop`) is unique across the
  tutorial, and no prop is used more than three times.
- Two to six labels, five words at most each, written at 54 units or more (13px on a phone).
- A caption in real type under every sketch: one or two plain sentences that make the point alone.
- An `alt` that describes the scene in one sentence.
- It sits after a paragraph, never straight under a heading, and never touching a table, a code block or
  another picture.
- No dashes in any text. 6,500 bytes compressed at most.

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
