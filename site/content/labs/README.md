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
- a dash in the lab's own words (recorded replies are left as the model wrote them).

Re-running a prompt gives a different reply. That is the point: the player is told so on every recording,
and the debrief invites them to paste the prompt into their own model and compare.

## The beats

| kind | what the player does | keys |
| --- | --- | --- |
| `note` | reads, goes on | `say`, `button`, `gives` (files that land on the desk), `patch` |
| `compose` | assembles a prompt from `parts`, runs it | `title`, `parts`: `{"text"}` fixed, `{"file", "lead"}` a desk file in full, `{"id", "label", "options": [{"id", "label", "text", "book"}]}` a slot |
| `run` | reads a recorded reply | `of` (the compose beat), `reply`: an id, or a map `{"slot=option": id, "*": id}` |
| `mark` | marks the faults in a reply, checks | `of`, `doc` (the reply), `ask`; the reply's `flags`, `sound`, `read` |
| `choose` | makes a call | `ask`, `options`: `[{"id", "label", "detail", "right", "after", "patch"}]` |
| `compare` | the same thing in two forms, picks one | `ask`, `cols`: `[{"id", "label", "body", "reply", "pick", "right", "after", "patch"}]` |
| `file` | the document joins the pack | `say` |

`when` on any beat gates it on earlier picks: `{"ask.what": "draft"}` (a slot), `{"call": ["keep", "self"]}`
(a call). The lab's paths should all reach `file`; `site/tools/lab.test.mjs` plays each one.

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
