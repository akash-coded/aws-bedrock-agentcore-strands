---
title: What Is the BMAD Method? Five Agents, One Build Loop
short: What is the BMAD Method?
wiki: What-Is-the-BMAD-Method
description: The BMAD Method as it installs today: five named agents, skills in your coding tool, one Build loop that sizes itself. When its trail pays, and when not.
dek: Skills in your coding tool, five named agents and one Build loop that sizes itself: a document trail for audited, multi-team work, and none at all for a one-line fix.
level: Beginner
keywords: BMAD method, BMAD-METHOD, BMAD v6, bmad-build, BMAD agents, breakthrough method of agile AI-driven development, breakthrough method for agile AI-driven development, BMAD vs spec-driven development, BMAD vs AI-DLC, BMAD for Claude Code
updated: 2026-10-08
---

> [!TIP]
> BMAD (the *Breakthrough Method of Agile AI-Driven Development*, from BMad Code) installs named
> commands, called skills, into your AI coding tool. Five named agents turn an idea into a brief, a
> requirements document, an architecture spine, a spec and stories, and one skill, Build, turns each
> story into reviewed code. The process sizes itself: a small change goes straight to Build, and work
> that several teams share gets the full document trail.

{{map:what-is-the-bmad-method}}

**In this lesson** you'll learn:

- what BMAD installs, and what Build does with a change;
- how it grows from one session to a project without changing its unit;
- when its document trail pays, and when BMAD says to skip it.

## Sound familiar?

- A single long AI conversation "designed" the system, and nobody can find where any decision was made.
- An auditor asks who approved the architecture, and the answer is a chat log.
- The coding agent builds each story in isolation, and the pieces do not fit.

BMAD was built against the first two, and its spec and stories are designed to prevent the third.

## What is the BMAD Method?

The BMAD Method is a set of skills that BMad Code's open-source installer adds to your AI coding tool,
where five named agents and one Build skill turn an idea into documents and reviewed code. It is not a
separate app or a fixed line of agents that every change must pass: a change gets only the skills it
needs, down to none.

The agents are the Analyst, the Product Manager, the UX Designer, the Architect and the Developer, and
each skill writes a document the next one reads. This lesson describes v6.12.1, of 4 October 2026.

## How BMAD works, step by step

### Step 1 · Install it, then ask it what to do

`npx bmad-method install` needs Node.js 20.12 or later, and `uv` for Build. It writes one folder per
skill into your tool's skills directory, and `bmad-help` then recommends the next skill.

SkyWays, this manual's fictional airline, starts its rebooking team with `bmad-project-context`: a
verified block in `AGENTS.md` for what the code cannot say, such as that the tests take eleven minutes
and the refund module is frozen.

### Step 2 · One session: Build plans, builds and reviews

Build (`bmad-build`) is the unit everything else repeats. Give it any intent, from a sentence or an
issue to a planned story: it reads the code first, then reports intent gaps, irreversible actions and
its footprint. Clean on all three, it writes a minimal spec and the code in one session; anything
flagged gets a written plan, and your answers, first. Independent reviewers check the diff, and Build
commits with an implementation record. A session is about 500 lines of code, not counting tests.

Showing the wheelchair-assistance flag on SkyWays' rebooking summary is clean on all three, so no
planning document is written.

### Step 3 · An epic: one spec and its stories

An epic is one outcome that needs several sessions. `bmad-spec` writes its contract in five fields
(why, capabilities, constraints, non-goals, the success signal), and Story Breakdown orders its
stories, a Build each: the job this manual's story file does. `bmad-retrospective` then judges the
epic on its evidence: accepted, accepted with open items, or rejected.

SkyWays' goodwill voucher, within a cap, is three stories: the offer, the cap check, the ledger line.
Each passed review alone; the retrospective found the cap checked twice and the ledger line missing on
the retry path.

### Step 4 · A project: the documents the organisation owns

Several epics, or roughly 20 sessions, make a project, and the documents become contracts between
people: the PRD, the UX pair (`DESIGN.md` and `EXPERIENCE.md`), and the Architect's spine, which records
only the decisions two teams would otherwise make differently. Epics and stories follow, then a
readiness gate asks whether a developer could build them without inventing decisions: PASS, CONCERNS
or FAIL. With the brief and the sprint status, that is **six documents** before any code.

BMAD names five sign-off moments: the PRFAQ's verdict, the PRD's validation, the spine's review, the
readiness gate and each retrospective. In a regulated setting their results are the audit trail. For
SkyWays' disruption agent, built by three teams and read by auditors, the spine is also where this
manual adds the authority budget: each tool the agent may call, and its cap.

### Step 5 · Let it size itself, and know the two failures

BMAD's own advice is the smallest amount of it that safely fits: an obvious, low-risk edit you will
review yourself needs no BMAD, and Build is worth it once a bug could escape into production. The
common failure is the opposite: "we are a BMAD shop" puts six documents in front of a typo fix, and
within a month the team skips the trail everywhere, audited work included.

{{sketch:six-binders-one-small-hatch}}

The quieter failure: Build flags an irreversible action, but cannot know your limits. The voucher cap
sat in a slide deck until the authority budget put it in the tool's signature.

## When BMAD pays, and when it does not

| The change | BMAD's own path | This manual adds |
| --- | --- | --- |
| A log field renamed | Trivial: edit it yourself, no BMAD | A spec update, if the field is in it |
| The wheelchair flag | One session: Build | The slice's bar, if a model call is touched |
| The voucher within a cap | Epic: a spec, three stories, a Build each | The cap in the authority budget |
| The agent across three teams, audited | Project: the six documents, the five sign-offs | A bar per slice; the trail kept for the auditor |

For one team, spec-driven development and the gates usually suffice; add BMAD's document trail when the
work crosses teams or an auditor reads it. [How much process a change needs](lesson:how-much-process-does-a-change-need).

## Extended BMAD: one more hand-off, after launch

BMAD's learn step is the epic's retrospective, and nothing in it watches production. This manual carries
the trail into Run & Learn and calls it **extended BMAD**.

| Hand-off | Who writes it | To |
| --- | --- | --- |
| The retrospective's verdict | The Developer agent | The next epic (BMAD's own) |
| The weekly drift report, slice by slice | The QA lead | The product manager |
| The two-number report | The product manager | The sponsor |
| The incident, as the next brief | The Analyst's brief skill | The next P0 |

The extension is this manual's own and is not part of BMAD as published.

## Why it matters

Prompt-driven AI development leaves decisions nobody can find. BMAD writes them down, and sizes the
ceremony to the change.

## Try it

Your team maintains a payments service. This week: (a) a cross-border payout feature that touches three
teams and is reviewed by compliance; (b) renaming a log field; (c) a retry on one timed-out partner
call. **Which BMAD path does each get?**

<details><summary>Show the answer</summary>

**(a) The project path:** three teams, and the five sign-offs become compliance's review points.
**(b) Trivial:** edit it yourself. **(c) One session with Build:** it is small, but a bug in a payment
retry could reach production.

</details>

## Key takeaways

1. **BMAD** is skills in your coding tool: five named agents and one Build loop.
2. Each skill **writes a document the next one reads**, so decisions stay explicit.
3. It **sizes itself**: use the full trail where people must agree or an auditor reads it, never as an identity.

## FAQ

### What does BMAD stand for?

The Breakthrough Method of Agile AI-Driven Development. Brian Madison created it; BMad Code publishes
it under the MIT licence.

### What are the BMAD agents?

Five in v6.12.1: the Analyst (Mary), the Product Manager (John), the UX Designer (Sally), the Architect
(Winston) and the Developer (Amelia). The scrum master, QA and quick-flow agents of earlier releases
were merged into the Developer in April 2026.

### BMAD vs spec-driven development: which should I use?

They overlap: BMAD now has a five-field spec that Build reads. Use spec-driven development on every
change, and add BMAD's document trail on multi-team or audited work.

### What is extended BMAD?

This manual's name for BMAD carried past launch, with three more hand-offs: the weekly drift report,
the two-number report, and the incident as the next brief.

### Does BMAD work with Claude Code or Cursor?

Yes: it installs into `.claude/skills/` for Claude Code and `.agents/skills/` for Cursor. On 8 October
2026 its docs site already described the next version, with a ticket skill in place of sprint planning:
check which version you installed.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Put the customer's approvals at the five sign-off moments. | Have the Analyst's brief skill draft the brief from your interview notes. |
| **A product manager or FDPM** | Own the PRD; add a bar per slice and an authority budget. | Ask `bmad-prd` to validate it and flag every requirement with no pass mark. |
| **A GenAI or agentic AI engineer** | Add the harness as a `[[workflow.review_layers]]` entry in `_bmad/custom/bmad-build.toml`. | Have the Developer's QA code write the voucher endpoint's API tests. |

**Across the enterprise.** Its five sign-offs leave the audit trail regulated work needs; small changes
still go straight to Build.

**The ten-minute workflow.** Ask for the two decisions the method does not ask for, before the spine:

```text
Run bmad-architecture on this spec: <paste>. Before you draft the spine, ask me, one question at a
time, for two decisions the method does not ask for: the authority budget (each tool the agent may
call, what it may do, its cap, where the cap is enforced) and the bar per slice (for each kind of
case, the damage of a wrong answer, the saving of a right one, the pass mark). Never guess a cap or
a pass mark: leave it blank and ask. Output: the spine, with these as decisions with stable IDs,
then a table of every tool that still has no cap.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The agents, skills, installer and Build | **Borrowed** | BMad Code (2026). [Agents](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/reference/skills-and-agents.md) · [Install](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/start/install-bmad.md) · [Context](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/existing-codebases/set-and-maintain-project-context.md) · [Build](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/build/build-a-change.md). v6.12.1, 4 October |
| The four sizes, the spec, the spine, the sign-offs | **Borrowed** | BMad Code (2026). [Paths](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/plan/choose-a-planning-path.md) · [Spec](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/plan/define-requirements-and-a-specification.md) · [Spine](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/plan/design-ux-and-architecture.md) · [Sign-off](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/plan/plan-inside-an-organization.md) · [Retrospective](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/docs/build/finish-an-epic.md). v6.12.1 |
| The earlier agents | **Borrowed** | [v4.44.3](https://github.com/bmad-code-org/BMAD-METHOD/tree/v4.44.3/bmad-core/agents), 29 October 2025 · [v6.0.0](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.0.0/docs/reference/agents.md), 16 February 2026 · [v6.3.0](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.1/CHANGELOG.md), 9 April 2026 |
| The version, and the next | **Borrowed** | [npm](https://www.npmjs.com/package/bmad-method) `latest` 6.12.1 · [docs](https://docs.bmad-method.org/) · [main](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md). Read 8 October 2026 |
| Six documents; extended BMAD | **Original**: this manual | [The Agentic PDLC](wiki:The-Agentic-PDLC#how-the-named-methods-sit-on-the-spine) |
| The story file as BMAD's story | **Original**: this manual | [Engineering lead, step 2](site:engineering/) |
