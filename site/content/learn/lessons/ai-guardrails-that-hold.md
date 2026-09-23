---
title: AI Agent Guardrails That Hold: Why a Prompt Is Not a Control
short: Guardrails that hold
wiki: AI-Agent-Guardrails-That-Hold
description: A limit in a prompt can be talked past; a limit in a tool's signature cannot. Six controls that make an AI agent's boundaries real, with a test for each.
dek: "Never refund more than $400" was in the prompt, the design and the slide deck. It was not in the code, and on day 82 a $2,000 refund went out.
level: Intermediate
keywords: AI agent guardrails, LLM security, prompt injection defence, AI agent permissions, excessive agency, OWASP LLM top 10, least privilege AI agents, tool calling security, human in the loop approval
updated: 2026-09-23
---

> [!TIP]
> **The rule in one sentence.** A limit an AI agent reads in its prompt only lowers the probability
> of crossing it, while a limit enforced in the tool it calls — a typed, bounded parameter that raises,
> a confirmation token the model cannot create, an identity that cannot reach what the job does not
> need — closes the path entirely, so every consequential limit must live in code, with a test that
> proves it refuses.

{{model:g_wall}}

**In this lesson** you'll learn:

- why a rule in a prompt is a request, and what makes a rule a boundary;
- the six controls that hold an agent's boundary, and the test for each;
- how to run an injection suite as a regression test rather than a launch check.

## Sound familiar?

- "We have a cap" — said about a cap that exists only as a sentence in the system prompt.
- The injection tests passed before launch and have not been run since three prompt edits ago.
- A reviewer approved the change because nothing in the diff looked like a rule being removed.

Nothing in a code review flags a limit that lives in a prompt, because it reads exactly like a limit.
The only way to find one is to ask to be shown the line of code that refuses.

## Why is a prompt not a control?

A model follows its instructions most of the time, and any text it reads — a customer's message, an
email, a web page, a partner's API notes field — can contain instructions too. Prompt injection has
held the top spot in OWASP's Top 10 for LLM applications for two editions running, because a model
processes instructions and data in the same channel. So a limit in the prompt is a **request**: it
lowers the probability of crossing it, and can be talked past. A typed parameter that raises is a
**boundary**: it cannot be argued with, whatever the model has been convinced of.

Both belong. The prompt explains the rule so the agent behaves well by default; the code makes the
bad behaviour impossible when the prompt has been talked past.

## The six controls, step by step

### Step 1 · Least authority

Give the agent the smallest identity that can do the job, with reads separated from writes. It cannot
be talked into calling a tool it does not have. This is the defence against what OWASP calls
**excessive agency**. *The test: the agent cannot call what the job does not need.*

### Step 2 · Bounded tools

Put every cap inside the tool's signature — `issue_refund(amount: ≤ 400)` — as a parameter that
raises when exceeded. *The test: an over-cap call raises, in a test that ran today.*

### Step 3 · A human gate on money

Every consequential write takes a **confirmation token** that only a person's approval can create, so
the model cannot mint one. *The test: a call without a valid token raises.*

### Step 4 · Injection defence where input arrives

Tag everything that arrives from outside — messages, documents, retrieved pages — as data, not
instructions, and run an **injection suite** as a regression test: one file of attack strings, every
entry point crossed with every gated tool, run weekly and on every prompt, tool or context change.
*The test: every attack string, from every entry point, moves no money.*

### Step 5 · Traceability

Write one redacted trace row for every consequential action: what was decided, by which model and
prompt version, what it did, and who approved it — with personal data masked. *The test: a passport
number never reaches a trace row, and that is a test too.*

### Step 6 · Classify every layer, in the system

List every layer of defence the design claims and mark each **enforced** (with a file and line),
**a request** (it lives in a prompt or a document), or **absent**. At SkyWays the day-82 postmortem
found five layers claimed and none enforced; two lived only in the prompt. *The test: no consequential
control lives only in a prompt.*

## Where you'll use it

- **In P1**, when the authority budget is set — every cap decided there gets a signature and two tests.
- **In P2**, before the first bolt that writes anything.
- **In every review of a change to a gated tool**, where two named readers check the limit, not the style.

## Why it matters

The most expensive sentence in agentic software is "we have a cap", said about a cap that lives in a
prompt. It passes every review, because it reads like a rule, and it fails all at once — in production,
with money. The six controls turn a decision into a guarantee.

## Try it

Search the agent's repository and you find: the prompt says *"Never issue a credit above $50"*; the
`issue_credit(customer_id, amount)` tool takes any number; and there is a monthly report of large
credits. **Is the $50 limit a boundary, and what would make it one?**

<details><summary>Show the answer</summary>

**No — it is a request.** The prompt asks; the tool accepts any amount; the monthly report finds a breach
weeks after the money has gone. To make it a boundary: change the signature so an amount over $50
raises, add a test that proves it raises and a test that a call without a confirmation token raises,
require a person's approval token above the cap, and add the credit tool to the injection suite. Keep the
sentence in the prompt too — it helps the agent behave well by default.

</details>

## Key takeaways

1. **A prompt is a request; a tool's signature is a boundary** — keep both, and rely only on the second.
2. **Six controls**: least authority, bounded tools, a human gate on money, injection defence, traceability, every layer classified.
3. **Every control has a test** that proves it refuses — run the injection suite as a regression, not once.

## FAQ

### What are guardrails for AI agents?

The controls that stop an agent doing what it should not: limits on what it can access, caps on what
its tools will accept, human approval for consequential actions, defences against instructions hidden
in its inputs, and a record of what it did. The ones that hold are enforced in code, not in the prompt.

### How do you prevent prompt injection?

You cannot stop a model from being persuaded, so design so that persuasion cannot cause harm: treat all
outside text as data, give the agent only the tools the job needs, put limits in tool signatures,
require a person's approval token for money, and run an injection suite on every change.

### Are guardrail products enough on their own?

Managed guardrails — content filters, denied topics, sensitive-data detection — are a useful layer, but
most are classifiers, which are probabilistic too. For money, identity and policy, the boundary has to
be deterministic code that raises, with a test.

### What is excessive agency?

An entry in OWASP's Top 10 for LLM applications: a system that grants a model more functionality,
permission or autonomy than its task needs, so that a manipulated or mistaken model can take harmful
actions. Least authority and bounded tools are the direct defences.

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| Prompt injection (LLM01), excessive agency (LLM06), unbounded consumption (LLM10) | **Borrowed** | OWASP (2025). [Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) |
| Least privilege | **Borrowed** | Saltzer, J. H. & Schroeder, M. D. (1975). The protection of information in computer systems. *Proceedings of the IEEE* 63(9) |
| Layered defences that fail when the holes line up | **Borrowed** | Reason, J. (2000). Human error: models and management. *BMJ* 320 |
| The six controls and "a prompt is a request, a signature is a boundary" | **Original** — this playbook | [How to hold the security boundary](wiki:How-to-Hold-the-Security-Boundary) |
| The SkyWays incident | **Illustrative** — a fictional airline | [Try the injection simulator](sim:#/toolkit/inject) |
