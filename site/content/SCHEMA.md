# Content schema

Every role journey on the site is one JSON file in [`roles/`](roles/), rendered to static HTML by
[`../render.py`](../render.py). No content lives in the renderer, and no HTML lives in the content.

Authoring is done in Python (`roles/_src/<role>.py`) and dumped to JSON, because templates and prompts
are multi-line strings and hand-escaping them in JSON is how mistakes get in.

```
site/content/roles/_src/product_manager_a.py   ← you edit this, and _b.py and _c.py: a role is three files
site/content/roles/product-manager.json        ← generated, committed, read by the renderer
```

Rebuild all roles with `python site/content/roles/_src/build_content.py`, which also checks them, and run
`python site/content/roles/_src/test_build_content.py` after changing a check (CI runs it on every push).

## Role object

| Field | Type | What it is |
| --- | --- | --- |
| `id` | slug | URL segment, e.g. `product-manager` |
| `name` | string | Display name |
| `short` | string | 2 to 4 letters for the rail and chips |
| `accent` | hex | The role's colour, used for headings, rails and diagrams |
| `tagline` | string | The arc in one line, e.g. "From a vibe to a number you can defend" |
| `arc` | list | The step names in order, shown as the journey diagram |
| `intro` | list | Paragraphs of orientation. Markdown-lite |
| `owns` / `not_yours` | list | What this role is accountable for, and what it must stop signing |
| `ai_stance` | string | The one paragraph on how this role should use AI at all |
| `reads` | list | `[label, href]` pairs to the wiki and the workbench |
| `steps` | list | The journey. See below |

## Step object

| Field | Type | What it is |
| --- | --- | --- |
| `n` | int | 1-based |
| `id` | slug | Anchor, e.g. `discover` |
| `phase` | string | Short label on the arc diagram |
| `title` | string | What the step achieves, as a verb phrase |
| `when` | string | Where it falls in a real project |
| `purpose` | string | One paragraph. Why this step exists |
| `activities` | list | `{do, detail}`: the sub-steps. This is the "X, Y, Z" of the role's day |
| `ai` | list | `{tool, use, caution}`: where a model helps, and where it must not be trusted |
| `artifact` | object | `{name, good, owner}`: what the step produces |
| `template` | object | `{title, lang, body}`: a fill-in skeleton, rendered with a copy button |
| `prompts` | list | `{title, when, body}`: copy-paste prompts, rendered with copy buttons |
| `example` | object | `{title, body}`: the running case, worked |
| `pitfalls` | list | Strings. Each is a real failure, not a platitude |
| `done_when` | string | A testable line. If you cannot test it, it is not a done-when |

## A staged role

The forward-deployed engineer's guide is a role in three stages: Frame the engagement, Deliver the system and
Evolve the relationship. Each stage asks P0 to P3 of its own object, so the guide has twelve steps, written in
three files: `fde_a.py` (the HEAD and steps 1 to 4), `fde_b.py` (5 to 8) and `fde_c.py` (9 to 12). The builder
checks each file on its own while the others are missing, and builds the role once all three are there. A role
is staged when its HEAD has `stages`; the five other roles build byte for byte as before.

| Field | Where | What it is |
| --- | --- | --- |
| `stages` | HEAD | Three objects in the order frame, deliver, evolve, each `{id, name, object, question, span, people, signed, signer}`: the framework picture's rows and the signature that ends each stage |
| `brief` | a stage, optional | `{long, people, think, ends, wrong}`: the five ruled rows of "the stage in brief" on its stage page |
| `stage` | step | `frame`, `deliver` or `evolve`. Inside a stage the phases run P0, P1, P2, P3, once each and in order, and stage k holds steps 4k-3 to 4k |
| `level` | step | None, or the altitude the step works at: `POC` (Frame only), or `MVP`, `Build`, `Deploy` or `"MVP, then build"` (Deliver only) |
| `hats` | step | One or more of `product`, `architect`, `engineer`, `qa`, `platform`, `consultant`, each once |
| `internal` | step | Two to four sentences: what changes when the client is inside your own company |
| `say` | step | Two or three `{to, words}`: the situation, and the words to say in it |
| `question` | step | The one question the step answers, ending in a question mark |
| `artifact.short` | step | The artefact's short name, which the framework picture draws |

Nobody's words are typed in quotation marks. In prose, `{{S24-ground}}` puts a recorded quotation on the page
and `[[S12]]` cites a source; both name records in `roles/_src/fde_sources.py`, which holds the guide's 30
sources and 53 quotations, each with its address and the date it was checked (a date more than sixty days old
turns amber, as in the Tool guides). The hub's words are data too, in `roles/_src/fde_hub.py`. The words of the
HEAD, the steps and the hub are held to the house rules (no model name, no dash, no American spelling, none of
the refused words); a quotation is held to its record instead.

The case runs on in the guide. Frame's examples are set in the three weeks before day 1 and are illustrative:
one week's export (1,640 tickets, about 234 a day) becomes the project's measured 240, the proof's 200 cases hold
22 codeshare (11%), and every lower bound uses the site's rule. Deliver's examples come in two halves, "In the
case:", the canon unchanged, and "Your move:". Evolve's, after day 97, are the guide's own (the cargo team's
damaged-baggage claims as the next frame, the partner lookup's three copies, day 180's review), and none of them
appears in the game, the workbench or the five role pages.

## Markdown-lite

The renderer supports, inside any prose string: `**bold**`, `` `code` `` and `[text](href)`.
Nothing else. Lists are arrays, not `-` lines. This keeps the content portable to the wiki.

## The running case

Every role works the same case (**SkyWays**, an airline building a rebooking assistant for disrupted
passengers), so a reader can switch roles and stay oriented. The
[workbench](https://akash-coded.github.io/aws-bedrock-agentcore-strands/workbench/)
walks the same case as thirteen dated episodes.

## Confidence

Any figure that is a vendor's documented number carries its date in the prose. Any threshold that is
this manual's default says so. See
[Sources and Confidence](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Sources-and-Confidence).
