---
title: What Is AI-Driven Development (AIDD)? The Daily Craft
short: What is AIDD?
wiki: What-Is-AIDD-AI-Driven-Development
description: AI-driven development (AIDD) is the everyday craft of building software with coding agents: context files, story files, exact code first, and review by risk.
dek: Five habits that decide whether a coding agent makes a team faster or just busier, and the evidence that the habits, not the tool, are what matter.
level: Beginner
keywords: AI-driven development, AIDD, AI coding agent best practices, CLAUDE.md, AGENTS.md, context engineering, how to use Claude Code, Copilot instructions, vibe coding vs AI-driven development
updated: 2026-09-24
---

> [!TIP]
> **AIDD in one sentence.** AI-driven development is the everyday craft of building software with
> coding agents: and in this playbook it means five habits: a **context file** every tool reads, a
> **story file** per unit of work instead of a chat thread, **exact work in tested code** before any
> prompt, **review set by risk** rather than by diff size, and a **harness** that decides what merges.

{{map:what-is-aidd}}

**In this lesson** you'll learn:

- what AIDD means, and why the term has no single owner;
- the five daily habits that make coding agents reliable, with a worked example of each;
- what the evidence says about AI and developer speed, and why it depends on the habits.

## Sound familiar?

- The coding agent keeps ignoring the same convention, however often someone mentions it in chat.
- A session that should have cost a few dollars cost three times that, and produced the wrong thing.
- Everyone feels faster, and nobody can show that anything ships sooner.

All three are habits, not tools. The same agent behaves very differently in a repository that has
them.

## What is AI-driven development?

**AI-driven development (AIDD)** is a broad term for building software with AI tools doing a large
share of the writing, testing and fixing, coding agents such as Claude Code, Cursor, Codex or
GitHub Copilot working inside the repository. Unlike AWS's AI-DLC, it has no single author or
published specification; different writers use it for different things, and one even expands it as
"adaptive intent-driven development".

This playbook uses it for the **day-to-day craft**: the habits that sit underneath any method (AI-DLC, spec-driven development or BMAD) and decide whether a coding agent helps. Mostly they live
in P2, [Build & Prove](lesson:p2-build-and-prove).

## The five habits, step by step

### Step 1 · Write the context file every coding tool reads

Every coding agent reads a file from the repository before it does anything (`CLAUDE.md`,
`AGENTS.md`, `.github/copilot-instructions.md` or `.cursor/rules`) and most teams have not written
one. It is an hour of work and the single biggest quality lever you have, because it is the only
instruction that reaches every session without anyone remembering to type it: the stack, the context
documents to read *by path*, the conventions, commands that have actually been run, and a list of
files never to touch.

Grow it by adding the rule that bit you last week. SkyWays' first file was twenty-two lines. It grew
twice: once after an agent computed a fare in a prompt, *never compute money in a prompt; call the
function*, and once after a mid-task model switch discarded the cache, *one model per task*.

### Step 2 · Build from a story file, not a chat thread

Each unit of work gets one self-contained file, versioned beside the code it produces, in six parts:
context **by reference**, the spec in EARS, the tools with their risk bands, the tests, the
done-when, and the cost. Because it is a file, it is reviewable as a diff and re-runnable next month.

The test of a story file is whether the chat window can stay shut. SkyWays' seventh bolt first pasted
a nine-hundred-line booking model into its context; the session cost three times its estimate and
re-derived a number it should have been given. The second version replaced the paste with two file
paths and one boundary line, and integrated before five.

### Step 3 · Write the exact floor before any prompt

Every number the feature computes and then acts on is a function with a unit test, never a prompt. A
model doing arithmetic fails fluently. SkyWays' agent returned $80 where the ledger said $62, with no
error. The check is mechanical: search the prompts for *calculate*, *compute*, *total* and *sum*, and
act on nothing a prompt returns for them.

### Step 4 · Put an independent checker after the risky model steps

On top of the floor goes the best-guess layer (ranking, drafting, classifying) and after each step
where a wrong answer is expensive, a checker that is **independent**: a different model, or a fresh
context with an adversarial brief. A "review your answer" step inside the same context changes
nothing, because the model agrees with its own reasoning.

### Step 5 · Let the harness and the risk band decide the merge

A merge is decided by two things, neither of them the size of the diff. The **harness** runs the
golden cases for every slice the change touched and rejects it if any falls below its bar. The **risk
band** of the most dangerous tool the change touches sets the review: a read-only change is reviewed
at the end, a change to a money tool gets two named readers every time.
[Code review for AI-generated code](wiki:How-to-Review-by-Risk-Band).

## Where you'll use it

- **In every repository where a coding agent works**: the context file first, on day one.
- **Whenever a session needs a chat thread to finish**: that is a story file that was cut wrong.
- **In every review**: the band of the most dangerous tool touched, not the line count, sets the depth.

## Why it matters

The evidence on AI and developer speed is mixed, and the habits explain why. In a 2025 randomised
trial, experienced open-source developers took **19% longer** with AI tools while believing they were
**20% faster**: a result its authors now describe as historical. DORA's 2025 research found that AI
**amplifies** what a team already is, strong or weak. A coding agent without context, story files and
a harness amplifies the rework; with them, it amplifies the output.

## Try it

A developer says: *"The agent keeps using the old logging library. I tell it in every chat to use the
new one, and it still forgets."* **Which habit fixes this, and how?**

<details><summary>Show the answer</summary>

**The context file.** An instruction typed into a chat reaches one session; a rule in `CLAUDE.md`,
`AGENTS.md` or the Copilot instructions file reaches every session and every engineer, because the
tool reads it before it starts. Add one line under conventions, *use the new logging library; the
old one is removed in version 3*, and, if it keeps happening, a lint rule that fails the build, so
the harness enforces what the file asks for.

</details>

## Key takeaways

1. **AIDD** is the everyday craft of building with coding agents; the term has no single owner.
2. Five habits decide whether it helps: **context file, story file, exact floor, independent checker, harness and risk band**.
3. AI **amplifies** a team's habits, so the habits, not the tool, decide whether a team gets faster.

## FAQ

### What is the difference between AIDD and vibe coding?

Vibe coding accepts whatever the model produces as long as it seems to work. AI-driven development in
this playbook's sense adds the structure that makes the output trustworthy: a context file, a story
file per unit of work, exact work in tested code, independent checking and a harness that gates the
merge.

### What should go in a CLAUDE.md or AGENTS.md file?

The stack; the context documents the agent should read, listed by path rather than pasted; the
conventions that matter; the commands to run, each one of which has actually been run; and the files
it must never touch. Keep it short, commit it, and add the rule that caused last week's mistake.

### Does AI make developers faster?

It depends on the habits around it. A 2025 randomised trial found experienced developers 19% slower
with the AI tools of early 2025, though they believed they were faster; DORA's 2025 research found AI
amplifies a team's existing strengths and weaknesses. Measure it on your own work, with the review
and rework hours counted.

### Is AIDD a methodology like AI-DLC?

No. AI-DLC is a named methodology with phases and rituals; AIDD is the craft underneath any method.
AI-DLC, spec-driven development and BMAD all rely on AIDD habits to work.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Set up the five habits in the customer's repository in week one, context file, story files, exact code first, review by risk, the harness. Their team keeps them after you leave. | Have a coding agent draft the context file from the repository and the customer's standards, then review it with their lead. |
| **A product manager or FDPM** | Write story files, not chat threads: one per bolt, with the spec lines, tools, tests and done-when. | Ask a model to turn a ticket into a story file and list everything it had to guess. |
| **A GenAI or agentic AI engineer** | When the coding agent asks something the story file does not answer, that is a template gap. Fix the template the same day. | Run the agent on the story file with the chat closed, and collect its questions as the finding. |

**Across the enterprise.** Standardise the context file and the story template across repositories. The
same agent then behaves the same way everywhere, and reviews become comparable between teams.

**The ten-minute workflow.** A first context file, drafted from the code:

```text
Read this repository. Draft a context file (CLAUDE.md or AGENTS.md) under 150 lines: what the product
does, the architecture in five bullets, the commands to build and test, conventions, the never-touch
list, and where the specs and decision records live. Mark every line you inferred rather than read.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Context files: CLAUDE.md, AGENTS.md, Copilot instructions, Cursor rules | **Borrowed**: documented, September 2026 | Anthropic, OpenAI, GitHub and Cursor documentation; see [Sources and Confidence](wiki:Sources-and-Confidence) |
| The five habits, the story file and the exact floor | **Original**: this playbook | [Engineering lead](site:engineering/) |
| 19% slower with AI, believing 20% faster | **Borrowed** | METR (2025). [Measuring the impact of early-2025 AI on experienced open-source developer productivity](https://arxiv.org/abs/2507.09089) |
| AI as an amplifier of existing strengths and weaknesses | **Borrowed** | DORA (2025). [State of AI-assisted Software Development](https://dora.dev/dora-report-2025/) |
| "AI Driven Development" as a term | **Borrowed** | Elliott, E. [The AI Driven Development Glossary](https://medium.com/effortless-programming/the-ai-driven-development-glossary-a487616801b6) |
| "Adaptive intent-driven development" as another expansion | **Borrowed** | Ayyagari, B. [From Agile to Adaptive Intent-Driven Development (AIDD)](https://medium.com/@binoy_93931/from-agile-to-adaptive-intent-driven-development-aidd-the-ai-first-paradigm-shift-e07e5c7df1ec). Medium |
| The SkyWays examples | **Illustrative**: a fictional airline | [The simulator](sim:#/) |
