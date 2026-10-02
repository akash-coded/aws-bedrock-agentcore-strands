# Writing a lab

A lab is a bench: on the left the work, one beat after another; on the right the document the work makes.
The player assembles a prompt from parts, runs it, reads a recorded reply, marks what is wrong in it, and
makes the calls only a person can make. Each lab files one document, and the next lab starts from it.

One file per lab, `<slug>.py`, with a `LAB` dict. The engine is `site/labs/lab.js` and `lab.css`; the
page is rendered by `site/pages/labs.py`, which also checks the script and writes the reading version for a
page without script. `_set.py` lists the labs still to come; they show on the front page as "being built".

## The one rule: a recording is a recording

A reply is a real model's answer to the exact prompt the lab shows, saved when the lab was written, with
the model's name and the date. Keep the prompt in `prompt-<id>.txt` and the reply in `rec-<id>.md` in the
lab's folder, and give the reply `prompt=` as well as `text=`. The build refuses:

- a reply with no `model` or no `date` of the form `2 October 2026`;
- a reply whose `prompt` is not what the lab's parts join into, byte for byte, for the option that leads to it
  (so a prompt cannot be edited after the reply was recorded);
- a `flags` or `sound` entry that does not match exactly one line of the reply;
- a lab with no `mark` beat, a call with no option marked `right`, or a last beat that is not `file`;
- a desk file named by the lab's `starts` that is not, byte for byte, the document the lab before it files
  when played by the book (so the chain from one lab to the next cannot drift);
- a dash in the lab's own words (recorded replies are left as the model wrote them).

**A system prompt.** When the lab is about a system prompt, a compose beat sends one: its parts marked
`"user": True` are the message, and the rest is the system prompt. The page shows the two apart, labelled, and
copies each. Keep the system prompt in `system-<id>.txt` and give the reply `system=` as well as `prompt=`; the
build holds both to the parts. Tools go into the system prompt as text, the way a framework describes them to
the model, and the reply writes its calls as lines; say so on the page, because no tool ran.

Re-running a prompt gives a different reply. That is the point: the player is told so on every recording,
and the debrief invites them to paste the prompt into their own model and compare.

## The beats

| kind | what the player does | keys |
| --- | --- | --- |
| `note` | reads, goes on | `say`, `button`, `gives` (files that land on the desk), `patch` |
| `compose` | assembles a prompt from `parts`, runs it | `title`, `parts`: `{"text"}` fixed, `{"file", "lead"}` a desk file in full, `{"id", "label", "options": [{"id", "label", "text", "book"}]}` a slot; `"user": True` on a part sends it as the message, beside the rest as a system prompt |
| `run` | reads a recorded reply | `of` (the compose beat), `reply`: an id, or a map `{"slot=option": id, "*": id}` |
| `mark` | marks the faults in a reply, checks | `of`, `doc` (the reply), `ask`; the reply's `flags`, `sound`, `read` |
| `choose` | makes a call | `ask`, `options`: `[{"id", "label", "detail", "right", "after", "patch"}]` |
| `compare` | the same thing in two forms, picks one | `ask`, `cols`: `[{"id", "label", "body", "reply", "pick", "right", "after", "patch"}]` |
| `file` | the document joins the pack | `say` |

`when` on any beat gates it on earlier picks: `{"ask.what": "draft"}` (a slot), `{"call": ["keep", "self"]}`
(a call). The lab's paths should all reach `file`; `site/tools/lab.test.mjs` plays each one. The test has a
profile for each lab (`LABS`): the recordings its prompts must join into, the paths to play and what each must
leave in the document. A new lab adds its profile; a lab without one fails the test.

## The document

`artefact` names the file, its `versions` (chips) and its `sections` (`id`, `head`). A `patch` is a list of
`{"id", "body", "state"}` or `{"version": n}`; the state is `empty`, `draft` (from a document a person wrote),
`guessed` (a model's text standing in for a decision), `open` (NOT DECIDED, with an owner) or `decided`. The
right side colours them: teal for decided, rose for guessed and open. A patch can sit on a beat, on an option,
or on a reply. The document the player downloads is the sections with a body, in order.

## Words

The lab's own words follow the site's voice (`site/DESIGN.md`): plain sentences, no dash, the airline case
throughout. Every `after` says what the book does and why, in two or three sentences; a wrong call is told
what it costs, not that it is wrong. The `debrief` has a `title` that is the lesson in one line, the `trap`
(what the three wrong turns had in common), the `habit` (what to do next time) and, if it helps, a `tool`
paragraph on doing it with the reader's own model.

## Recording other models

A debrief can show that its point holds beyond one model. In Grow the spec, three models from other makers
answered two of the lab's prompts on the day it was recorded, and the debrief sets their replies beside the
lab's own (`debrief.others`).

- **How they were called.** The prompt file, byte for byte, as the only user message: no system prompt, the
  model's default settings, one call each. Grow the spec's went through Amazon Bedrock on 2 October 2026. Where
  the lab's own recording was sent a system prompt, the other models get the same system prompt and the same
  message (Write the system prompt from the spec), and each reply carries `system=` too.
- **Where they go.** `<slug>/others/<model>-<prompt>.md`, exactly as the model wrote it, never tidied. In the
  script each is a dict with `id`, `model`, `maker`, `date`, `of` (the lab's own recording whose prompt it
  answers), `text`, and `prompt` (the prompt file, loaded the way `_rec` loads it).
- **The part.** `debrief.others` has a `title`, a `lead`, `tables`, a `close`, the `fold` label and the
  `replies`. A table has `of`, a `caption` and a `corner` (the name of its first column); its columns are the
  lab's own recording, then each reply with the same `of`, in script order. A row has `h`, an optional `note`,
  one entry in `cells` for each column and, for each cell, a `quote`: the words of that reply the cell is built
  from, or `None` where the cell says a thing is missing. A row with `count` holds, in each cell, the number of
  times that reply writes the string.
- **What the build refuses.** A reply without a model, a maker or a date like `2 October 2026`; a reply whose
  prompt is not the one the lab shows for its `of`; an empty cell, or a row without a cell for each column; a
  quote that is not in its reply word for word; a number in a cell that is not in the words it quotes; a count
  that is not the count. The replies and the quotes are the models' words, so the dash rule leaves them alone.
  Everything else in the part is the lab's own words and keeps to it.
- **Where it shows.** The part is drawn once, in the reading version, and the engine copies it into the
  debrief. The replies have a page of their own, `/labs/<slug>/others/`, with each prompt as the lab shows it
  and the lab's own recordings for the first column. The fold reads the replies in from that page when it is
  opened, and without script it links to it, which keeps the lab's page inside the byte budget the acceptance
  gate holds it to. `site/tools/lab.test.mjs` checks the tables at 1440, 1024, 390 and 320, and that each reply
  in the fold is its file as written.
