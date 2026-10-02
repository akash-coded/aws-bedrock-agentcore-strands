---
title: What Is a Forward Deployed Engineer? The FDE Role, Explained
short: What is an FDE?
wiki: What-Is-a-Forward-Deployed-Engineer-FDE
description: What a forward deployed engineer (FDE) does, where the role came from, how it differs from a solutions architect, and why AI labs now hire FDEs.
dek: One engineer, one customer, many capabilities, and a duty to carry what the customer taught them back into the product.
level: Beginner
keywords: forward deployed engineer, what is a forward deployed engineer, FDE, FDE meaning, forward deployed engineer vs solutions architect, forward deployed product manager, FDPM, OpenAI forward deployed engineer, Anthropic forward deployed engineer, Palantir forward deployed software engineer, deployment strategist, technical deployment lead
updated: 2026-10-03
---

> [!TIP]
> A forward deployed engineer (FDE) is a software engineer who embeds with a
> customer to make a complex product work in the customer's own environment. The FDE owns discovery,
> scoping, build and rollout, and carries the patterns they find back into the product. The role
> began at Palantir in the early 2010s; frontier AI labs such as OpenAI and Anthropic now hire FDEs to put
> models into production with their most strategic customers.

{{map:what-is-a-forward-deployed-engineer}}

**In this lesson** you'll learn:

- what an FDE actually does, in the words of the companies that hire them;
- the job's three stages, Frame, Deliver and Evolve, and how the role differs from a solutions architect;
- who works beside an FDE, and why some weeks nobody does.

## Sound familiar?

- The model works in the demo and nowhere near the customer's systems, data or approvals.
- Every enterprise deal ends in a custom build nobody at the vendor can maintain.
- The product team learns what customers need from sales notes, months late.

The FDE exists because all three are the same problem: the distance between a capable product and a
working deployment.

## What does a forward deployed engineer do?

**Writes production software inside a customer's environment, and owns the whole path to value.**
Palantir, which created the role, framed it against its product engineers: a product engineer's focus is
"one capability, many customers", while a forward deployed engineer's is "one customer, many
capabilities". Six companies that run FDE teams describe the modern version in their own words:

| Company | The work, in its own words | Read |
| --- | --- | --- |
| **OpenAI** | "You will own discovery, technical scoping, system design, build, and production rollout", measured partly by "eval-driven feedback that changes product and model roadmaps" | 2 Oct 2026 |
| **Anthropic** | "Identify and codify repeatable deployment patterns and contribute insights back to our Product and Engineering teams" | 2 Oct 2026 |
| **Palantir** | Its Forward Deployed AI Engineers' responsibilities "look similar to those of a hands-on AI startup CTO" | 2 Oct 2026 |
| **Databricks** | Its AI FDEs own "production rollouts of consumer and internally facing GenAI applications" | 2 Oct 2026 |
| **Ramp** | Its FDEs work with customers "through their entire lifecycle: from when they are prospects in the sales funnel, to implementation and rollout, to long-tail support" | 2 Oct 2026 |
| **AWS** | As a project advances, the customer's engineers move "from observers to co-builders to autonomous operators" | 2 Oct 2026 |

Two threads run through the rows: **the FDE ships to production, not to a demo**, and **the FDE's
second customer is their own product team**. Ramp's and AWS's rows add the span of the job: from a
prospect in a sales funnel to a customer whose own engineers run the system.

## How the role works, stage by stage

**In three stages, named so that their initials spell the role: Frame, Deliver, Evolve.** Each asks
the manual's four questions, P0 to P3, about a different thing: the engagement, the system, the
relationship. Each ends with a signature on the customer's side. The
[forward-deployed engineer guide](site:forward-deployed-engineer/) gives every stage four steps, each
with its template, its prompts and a worked example.

### Stage 1 · Frame the engagement

Days, before a contract or a charter. Measure the pain in the customer's data, not the pitch: cases,
minutes and money, the systems the agent must touch, and who owns the risk. Then write a statement of
work a sceptic would sign, prove it on their cases in days, and read the proof out with the failures
first. An FDE says no more than most engineers: to the flagship first feature, to building past an
unsigned autonomy decision, to meetings that produce no artefact. The stage ends with the go decision,
signed by the customer's sponsor. [Frame the engagement](site:forward-deployed-engineer/frame/)

### Stage 2 · Deliver the system

Weeks. Start every lead-time item on day one (model access, data access, the security review), because
they set the calendar. The code lives in the customer's repository, runs in their environment and uses
their identity model. Their engineers pair on it, their experts label the golden set, their risk owner
signs every limit, and a shadow run compares the agent with their staff: an FDE's claims are the
customer's numbers, not the vendor's. The stage ends with the handover, signed by the person who will
run it. [Deliver the system](site:forward-deployed-engineer/deliver/), and the stage in depth:
[AI-DLC and AIDD in the field](lesson:ai-dlc-for-forward-deployed-engineers)

### Stage 3 · Evolve the relationship

Months, for as long as the system runs. Turn what the running system taught into the next frame, and
write the patterns up for the people who build the product: the connector built for the third time,
the evaluation that exposed a model gap. Prove the reusable version at the next deployment, and hold a
value review each quarter, the saving beside the spend. The stage ends with the next frame, or a clean
close, signed by the customer's sponsor. [Evolve the relationship](site:forward-deployed-engineer/evolve/)

## How is an FDE different from a solutions architect?

| Role | Mainly produces | Writes production code? | Owns the outcome at the customer? |
| --- | --- | --- | --- |
| **Forward deployed engineer** | Working software in the customer's environment | Yes, most of the time | Yes, through rollout |
| **Solutions architect** | Designs and guidance | Sometimes, as reference code | Advises; the customer builds |
| **Solutions or sales engineer** | Demos and proofs of concept before the sale | Prototype code | Until the deal closes |
| **Consultant** | Delivered projects, often bespoke | Yes | For the contract's scope |

The distinction that matters most is the last column combined with the feedback duty. A consultant can
succeed with bespoke work; an FDE who only ever builds bespoke work has turned a product company into a
services firm. OpenAI's own framing, as reported, distinguishes its FDEs from the professional-services
work of a solutions architect.

## Who works beside an FDE?

**At a larger vendor, a partner; some weeks, nobody.** At a customer you may be the only person from
your side, and then you do every job: you size the pain as a product manager would, draw the system as
an architect, build it as an engineer, prove it as a QA lead, keep it running as a platform team and
lead the room as a consultant.

{{sketch:six-hats-one-head}}

At scale the work is a pair. The FDE owns the *how*; a partner owns the *what* and the *why*, and each
company that runs FDE teams names the partner differently (postings read on 2 October 2026):

| The partner | Company | The split, in their words |
| --- | --- | --- |
| **Deployment Strategist** | Palantir, Databricks | At Databricks, "the 'product manager' for the customer's problem, responsible for the 'why' and 'what'", with the FDEs "responsible for the 'how'" |
| **Technical Deployment Lead** | Anthropic | Owns "product scoping, stakeholder management, value measurement", beside FDEs "who build the technical solution" |
| **AI Solutions Strategist** | Ramp | Its engineers "co-lead customer engagements with an AI Solutions Strategist" |
| **Forward deployed product manager (FDPM)** | Glean, Scale AI | Glean's founding FDEs work "in a pod with Forward Deployed PMs"; Scale's best FDPMs "can tell the difference between a customer's stated request, their actual problem, and what the platform should do" |

The partner's hardest call is sorting every customer request into configuration, a service or a product
capability, and defending that call to the customer and to the product team. Learn both halves: when
the pair is one short, you are both.

## Where you'll use it

- **When hiring or joining an FDE team**, to know which of the three stages the role really owns, and who works beside it.
- **When scoping an enterprise AI deal**, to decide what the FDE owns and what the customer must.
- **When an engagement drifts into bespoke work**, to put the product feedback duty back on the plan.

## Why it matters

Models are capable; deployments are hard. Most of the distance between the two is integration, access,
evidence and trust: work that is specific to one customer and cannot be done from a distance. The FDE is
how a product company closes that distance without becoming a consultancy, provided the patterns flow back.

## Try it

A customer asks their FDE to build a fourth custom integration with their ticketing system, the same as
three the FDE built for other customers. **What should the FDE do, and who else needs to know?**

<details><summary>Show the answer</summary>

**Build it once more only as the reusable version, and take the pattern home.** Three copies of the same
integration are a product gap, not a customer request: the FDE should build it as a configurable
connector (an MCP server, say) and write the case for the product team with the evidence of all four
customers. The FDPM, if there is one, decides whether it becomes product; the customer gets a supported
capability instead of a fourth bespoke fork.

</details>

## Key takeaways

1. **An FDE owns production outcomes at one customer**, in three stages: frame, deliver, evolve.
2. **The second customer is the product team**: repeated work becomes a pattern, then a product.
3. **FDEs say no by design**: to the flagship first, to unsigned autonomy, to bespoke forks.

## FAQ

### What does FDE stand for?

Forward deployed engineer: a software engineer who works embedded with a customer to deploy and adapt a
product in the customer's environment. Palantir's original title was forward deployed software engineer.

### Is a forward deployed engineer a software engineer?

Yes. FDEs write production code, usually in the customer's systems and stack, but the job also includes
discovery, scoping, stakeholder work and evaluation, so the balance of the week differs from a product
engineer's.

### What skills does a forward deployed engineer need?

Strong programming, fast learning of unfamiliar systems, discovery with non-technical stakeholders,
evaluation design for AI systems, security and identity basics, and the judgement to say no to work that
cannot be proven or maintained.

### What is the difference between an FDE and an FDPM?

The FDE owns how a capability is built and deployed at a customer; the forward deployed product manager
owns what is built and why, and decides which customer needs become product capabilities.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Keep a pattern log from day one: every problem you solve twice at any customer. | Ask a model each Friday to turn the week's notes into pattern entries with customer evidence. |
| **A product manager or FDPM** | Review the FDE pattern log monthly and decide configuration, service or product for each entry. | Have a model rank the log by customers affected and revenue at stake. |
| **A GenAI or agentic AI engineer** | Treat FDE-built connectors as product prototypes: harden the ones with three users into supported tools. | Ask a coding agent to diff the customer copies and propose the shared interface. |

**Across the enterprise.** Run FDEs as a programme with a feedback budget: a fixed share of every
engagement goes to codifying patterns, and the product roadmap has a standing slot for them.

**The ten-minute workflow.** Keep the pattern log honest:

```text
Here are my notes from this week's customer work: <paste>. Extract every problem I solved, and mark the
ones I have solved before at any customer (check against this log: <paste the log>). For each repeat,
write a pattern entry: the problem, the fix, the customers, and whether it should become configuration,
a reusable service or a product capability.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| The role's origin at Palantir; "one capability, many customers" against "one customer, many capabilities" | **Borrowed** | Orosz, G. (2025, 12 August). [What are Forward Deployed Engineers, and why are they so in demand?](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers) *The Pragmatic Engineer* |
| What OpenAI's FDEs own, and one way they are measured | **Borrowed**: public posting, read 2 October 2026 | [OpenAI: Forward Deployed Engineer (FDE), San Francisco](https://jobs.ashbyhq.com/openai/967f94aa-1706-4dba-ac89-bfbc2c38b688) |
| Anthropic's FDEs carry patterns back to the product; its Technical Deployment Lead | **Borrowed**: public postings, read 2 October 2026 | [Anthropic: Forward Deployed Engineer, London](https://job-boards.greenhouse.io/anthropic/jobs/5423029008) · [Technical Deployment Lead](https://job-boards.greenhouse.io/anthropic/jobs/5017903008) |
| Palantir's FDE likened to a startup CTO; its Deployment Strategists | **Borrowed**: public postings, read 2 October 2026 | [Palantir: Forward Deployed AI Engineer](https://jobs.lever.co/palantir/636fc05c-d348-4a06-be51-597cb9e07488) · [Deployment Strategist](https://jobs.lever.co/palantir/e0ab8226-b928-4e3a-bf87-08fe7b1ea595) |
| Databricks' AI FDEs and its Deployment Strategists | **Borrowed**: public postings, read 2 October 2026 | [Databricks: AI Engineer, Forward Deployed Engineering](https://databricks.com/company/careers/open-positions/job?gh_jid=8546367002) · [Deployment Strategist](https://databricks.com/company/careers/open-positions/job?gh_jid=8463063002) |
| Ramp's FDEs across a customer's lifecycle, beside an AI Solutions Strategist | **Borrowed**: blog post and public posting, read 2 October 2026 | Mehr, L. (2025, 5 August). [Forward Deployed Engineering](https://engineering.ramp.com/post/forward-deployed-engineering) *Ramp Builders* · [Ramp: Software Engineer, Forward Deployed AI Solutions](https://jobs.ashbyhq.com/ramp/b614563f-3ce6-4dca-b5ba-0e5a6c8bda27) |
| The customer's engineers, from observers to operators | **Borrowed**: news article, read 2 October 2026 | Vasquez, F. (2026, 30 June). [AWS's announcement of its forward deployed AI engineers](https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers) *About Amazon* |
| Forward deployed PMs beside FDEs | **Borrowed**: public postings, read 2 October 2026 | [Glean: Founding Forward Deployed Engineer](https://job-boards.greenhouse.io/gleanwork/jobs/4659412005) · [Scale AI: Forward Deployed Product Manager, Enterprise](https://job-boards.greenhouse.io/scaleai/jobs/4673051005) |
| Frame, Deliver and Evolve; some weeks the whole team; the pattern log | **Original**: this manual, on the spans the postings above describe | [The forward-deployed engineer guide](site:forward-deployed-engineer/) |
