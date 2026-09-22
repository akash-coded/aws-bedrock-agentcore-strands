# Content schema

Every role journey on the site is one JSON file in [`roles/`](roles/), rendered to static HTML by
[`../render.py`](../render.py). No content lives in the renderer, and no HTML lives in the content.

Authoring is done in Python (`roles/_src/<role>.py`) and dumped to JSON, because templates and prompts
are multi-line strings and hand-escaping them in JSON is how mistakes get in.

```
site/content/roles/_src/product-manager.py   ← you edit this
site/content/roles/product-manager.json      ← generated, committed, read by the renderer
```

Rebuild all roles with `python site/content/roles/_src/build_content.py`.

## Role object

| Field | Type | What it is |
| --- | --- | --- |
| `id` | slug | URL segment, e.g. `product-manager` |
| `name` | string | Display name |
| `short` | string | 2–4 letters for the rail and chips |
| `accent` | hex | The role's colour, used for headings, rails and diagrams |
| `tagline` | string | The arc in one line, e.g. "From a vibe to a number you can defend" |
| `arc` | list | The step names in order, shown as the journey diagram |
| `intro` | list | Paragraphs of orientation. Markdown-lite |
| `owns` / `not_yours` | list | What this role is accountable for, and what it must stop signing |
| `ai_stance` | string | The one paragraph on how this role should use AI at all |
| `reads` | list | `[label, href]` pairs to the wiki and the simulator |
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
| `activities` | list | `{do, detail}` — the sub-steps. This is the "X, Y, Z" of the role's day |
| `ai` | list | `{tool, use, caution}` — where a model helps, and where it must not be trusted |
| `artifact` | object | `{name, good, owner}` — what the step produces |
| `template` | object | `{title, lang, body}` — a fill-in skeleton, rendered with a copy button |
| `prompts` | list | `{title, when, body}` — copy-paste prompts, rendered with copy buttons |
| `example` | object | `{title, body}` — the running case, worked |
| `pitfalls` | list | Strings. Each is a real failure, not a platitude |
| `done_when` | string | A testable line. If you cannot test it, it is not a done-when |

## Markdown-lite

The renderer supports, inside any prose string: `**bold**`, `` `code` ``, `[text](href)`, and `—`.
Nothing else. Lists are arrays, not `-` lines. This keeps the content portable to the wiki.

## The running case

Every role works the same case — **SkyWays**, an airline building a rebooking assistant for disrupted
passengers — so a reader can switch roles and stay oriented. The
[simulator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html)
walks the same case as thirteen dated episodes.

## Confidence

Any figure that is a vendor's documented number carries its date in the prose. Any threshold that is
this playbook's default says so. See
[Sources and Confidence](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Sources-and-Confidence).
