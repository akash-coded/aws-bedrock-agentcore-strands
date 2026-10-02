# Writing a tool fact

The tool guides at `/tools/` say which AI tool does which job, and the manuals show the airline's team using
them. Every fact they state about a tool lives in one file, `tools.json`, with the page it came from and the
date it was checked. `site/pages/tools.py` renders the index and the manuals from it, and checks it.

## The one rule: a fact has a source and a date

A fact is one sentence that a reader could check against one vendor page. Take it from the vendor's own
documentation, help centre or changelog, never from memory, and never from a "nearest equivalent" or a
"could not verify" line in a research sheet. If a page shows its own date, the fact is still dated by the day
you checked it.

```json
{"id": "claude-projects", "family": "claude", "surface": "Projects", "job": "hold project knowledge",
 "fact": "A project is a self-contained workspace with its own chats and knowledge base, where you upload documents and set the project's own instructions.",
 "status": null, "source": "https://support.claude.com/en/articles/9517075-what-are-projects", "checked": "2026-10-02",
 "cell": true}
```

| key | what it holds |
| --- | --- |
| `id` | lower case with hyphens, unique; a manual and its marks use it |
| `family` | `claude`, `openai` or `google`; `other` for a tool outside the three (Cursor, Copilot, Kiro, Spec Kit), which gets a row below the table |
| `surface` | the product surface, as the cell names it: "Projects", "Claude Code on the web" |
| `job` | one of the seven in `jobs`: think it through, hold project knowledge, test a prompt, build in the repo, hand off a task, act in a browser, run on a schedule |
| `fact` | one sentence, in the site's voice, ending in a full stop |
| `status` | the vendor's own word where its page gives one: `GA`, `beta`, `public beta`, `preview`, `research preview`, `experimental`; otherwise `null` |
| `source` | the address of the page the sentence came from |
| `checked` | the date you read that page, `2026-10-02` |
| `cell` | `true` on the one fact that names a family's tool for a job in the index table; each of the 21 cells has exactly one |

## Sixty days

A fact goes stale sixty days after `checked`. The build then prints a warning that names the page and the
fact, and the page shows its "Last checked" date in amber. To clear it, open the source, confirm or rewrite
the sentence, and change `checked` to today. To see the warnings before they are due, build with a date of
your choosing: `TOOLS_TODAY=2026-12-15 python3.12 site/build.py`.

## What a fact never says

No prices, no usage limits, no model names: they change monthly, so each family in `families` links to the
vendor's own plans and models pages instead. The build refuses a fact with a price or a model name in it, a
dash, an American spelling, or the words the house style bans.

## Using a fact in a manual

The manuals' words are in `site/pages/tools.py`. In them, `{{id}}` puts the fact's own sentence on the page
with a numbered mark, and `[[id]]` puts the mark alone after a sentence that leans on the fact. The mark leads
to the fact's row in the dated table at the foot of the page. Each manual lists its facts in `facts`; the
build refuses a manual whose marks and list disagree, so the table always holds every fact the page used,
and no sentence of fact appears on a page without its source.

Each manual names its `family`. Its closing paragraph links that family's plans and models pages, or the
pages in the manual's own `links` when the family's pages are not the ones a reader of that manual needs
(the Google manual links Jules's plans, AI Studio's plans and the Gemini models page). A cell in the table at
`/tools/` links to the manual that uses the cell's own fact, or else to the first manual with a fact about
the same tool, the same `family` and `surface`. So when a manual covers a cell's tool from a newer page,
give its facts the cell's `surface`, word for word.

## Reading a vendor's page exactly

Open the page itself, and quote from it. Several vendors publish each documentation page as plain Markdown,
which shows the exact wording without the site around it: OpenAI's docs at `learn.chatgpt.com` and
`developers.openai.com` add `.md` to the address, Google's at `ai.google.dev` add `.md.txt`, and Jules's
pages are at `jules.google/docs/<page>.md`. OpenAI's help centre, `help.openai.com`, refuses this
environment's proxy, so its facts are taken from those two documentation sites or left out.

## Words

The site's voice (`site/DESIGN.md`): plain sentences of about twenty words, British spelling, no dashes, the
airline case throughout. Write what the vendor's page says, and nothing it only implies. Where two of a vendor's own
pages disagree, say so in the fact and cite the page you are quoting.
