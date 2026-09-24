# Roadmap

*What this project is, where it is going, and how to move it. Updated when something ships, not on a calendar.*

Last revised: **2026-09-24**.

## What it is, in one paragraph

An open manual for delivering software that has a model inside it: the agentic PDLC as a
[tutorial](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/) and a
[playbook](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/) on the site, a
[sixteen-module course](Course-Companion) with auto-graded [labs](Labs-Companion) in the repository,
and this wiki as the reference, the cohort kit and the community layer between them. It is one
person's work, open-sourced under MIT, and it improves through the people who use it.

## Shipped

| When | What |
| --- | --- |
| 2026-09 | The wiki reorganised into five sections; the tutorial's lesson mirrors retired in favour of a thin index; the [course companion](Course-Companion), [labs companion](Labs-Companion) and [cohort kit](Cohort-Kit) added |
| 2026-09 | Every lesson and reference picture redrawn in one visual grammar, light and dark; the playbook replaced with its current release, with a way back to the manual from every page |
| 2026-09 | The tutorial: 55 lessons in eight tracks on the site, with search, social cards, structured data and `llms.txt` |
| 2026-09 | The manual's front door: a page per role, templates, prompts, mental models, the leadership protocol, a guided walkthrough on every page |
| 2026-09 | Google Search Console verified for the site; the wiki is not indexable by design, so everything meant to be found lives on the site |
| 2026-08 | Ten L.A.B. labs built with Learn → Apply → Break phases; nineteen drills graded by a bot in the [Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75) |

## In progress

- **Recordings.** Walkthrough recordings per module are being published progressively; each module
  page says *link pending* until its recording is up. Track them in the
  [video index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/reference/video-index.md).
- **The labs pathway.** Ten of forty-one labs are built. The remaining thirty-one are specified in the
  [pathway](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md#the-complete-pathway)
  and open for contribution; [how to author one](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/CONTRIBUTING-A-LAB.md).
- **Contact, without a mail app.** The playbook's contact form currently opens the visitor's mail
  client. A hosted relay is next, so a message can be sent from the page.
- **A custom domain for the site.** The site stays at its GitHub Pages address until a domain is
  chosen; when it moves, every existing link redirects.

## Next, in order

1. **Run the cohort kit once, for real,** and rewrite the sessions from what happened. The
   [eight sessions](Cohort-Kit) are designed, not yet field-tested; the first [field note](Field-Notes)
   from a facilitator changes them more than another draft would.
2. **Close the loop from the playbook back to the lessons.** Each calculator in the playbook should
   name the lesson that derives its formula, the way each lesson now names the calculator.
3. **The remaining labs,** in pathway order, starting with the tracks that have one lab each.
4. **A printable edition** of the tutorial, one PDF per track, for the readers who asked for it.

## Not planned

- **A second language.** Translations drift the moment the source moves; the tutorial changes weekly.
- **Accounts, progress tracking or certificates on the site.** The [Scoreboard](Scoreboard) already
  records lab progress from the Arena, with nothing to sign up for.
- **A hosted model or any AWS resource run for readers.** Every lab is offline; the course expects your
  own account, with the [cost controls](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md) set first.

## How to move it

- **Pitch an idea** in the [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101).
  Every suggestion is read; the ones that ship are credited.
- **Fix a page.** Hand-written wiki pages are edited in the browser. Generated ones say at the top
  where their source is.
- **Author a lab** or **record a walkthrough** for a module that lacks one; both are listed above.
- **Write a [field note](Field-Notes)** after you run any of this on a real project.

---

**Also:** [Maintainer Runbook](Maintainer-Runbook) for how the repository is run · [Editing this wiki](Contributing-to-this-Wiki) · [Where do I find…?](Where-do-I-find-it)
