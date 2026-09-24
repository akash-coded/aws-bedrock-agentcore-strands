# Where do I find…?

A lookup table across all four surfaces. If you know what you want but not where it is, start here.

## Concepts

| I want… | It is here |
| --- | --- |
| What an agent actually is, vs a workflow | [Module 00](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/00-agentic-foundations) · [Autonomy Ladder](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/autonomy-ladder.md) |
| How LLMs work, without maths | [Module 01](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/01-llm-and-aws-bridge) · [LLM Intuition Bank](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/2) |
| What transfers off AWS | [Portability matrix](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/concepts/portability-matrix.md) |
| The agentic PDLC, as one simulation | [SkyWays playbook](https://akash-coded.github.io/aws-bedrock-agentcore-strands/) · [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101) |
| A definition of a term | [Glossary](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/concepts/glossary.md) |
| Which AWS service does what | [AWS service map](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/concepts/aws-service-map.md) |


## The playbook: method, roles and process

| I want… | It is here |
| --- | --- |
| The four phases and what each one owes the next | [The Agentic PDLC](The-Agentic-PDLC) |
| Which loop closes where, and who owns it | [The Eight Loops](The-Eight-Loops) |
| The five gates, and which ones are mine | [Gates & Governance](Gates-and-Governance) |
| The documents owed at each hand-off | [The Evidence Pack](The-Evidence-Pack) |
| My whole role, end to end, with a template per step | [PM](Journey-Product-Manager) · [SA](Journey-Solution-Architect) · [Engineering](Journey-Engineering-Lead) · [QA](Journey-QA-Lead) · [DevOps](Journey-DevOps) |
| A prompt I can paste | [Every prompt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/prompts/) |
| A template for an artefact | [Every template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/) |
| What I am accountable for, and what I must not touch | [PM](Role-Product-Manager) · [Architect](Role-Solution-Architect) · [Engineering](Role-Engineering-Lead) · [QA](Role-QA-Lead) · [DevOps](Role-DevOps) · [Sponsor](Role-Sponsor) |
| How to derive an acceptance bar | [Formulas & Calculators](Formulas-and-Calculators) · [How to Prove the Bar](How-to-Prove-the-Bar) |
| Whether a score has actually proven the bar | [How to Prove the Bar](How-to-Prove-the-Bar) |
| Why the token bill left its estimate | [How to Control the Token Bill](How-to-Control-the-Token-Bill) |
| Where a cap should live | [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) |
| How to run the postmortem | [How to Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem) |
| How to run the NFR workshop | [How to Run an NFR Workshop](How-to-Run-an-NFR-Workshop) |
| How many agents this needs | [How to Design an Agent on Paper](How-to-Design-an-Agent-on-Paper) · [Decision Trees](Decision-Trees) |
| How to unblock a review queue | [How to Review by Risk Band](How-to-Review-by-Risk-Band) |
| An intuition I can carry into a case this playbook never covered | [Mental Models](Mental-Models) |
| The whole thing explained to a CEO | [The operating protocol](https://akash-coded.github.io/aws-bedrock-agentcore-strands/protocol/) |
| A term this playbook uses oddly | [Playbook Glossary](Playbook-Glossary) |
| A case from my own industry | [Scenario Library](Scenario-Library) |
| Practice questions, with answers | [Exercises & Answers](Exercises-and-Answers) |
| Whether a number here is a standard or a default | [Sources & Confidence](Sources-and-Confidence) |

---

## The nine how-tos, by symptom

A how-to is a procedure with an owner, a phase and a loop it closes. Each opens with an **At a
glance** block saying when to reach for it and what you leave with. Pick by what is going wrong, not
by what sounds relevant.

<!-- picture:wikimap:where-do-i-find-it -->
<p align="center"><a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-where-do-i-find-it.light.webp"><picture><source media="(prefers-color-scheme: dark)" srcset="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-where-do-i-find-it.dark.webp"><img alt="Six symptoms, each pointing to the how-to page that treats it" src="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-where-do-i-find-it.light.webp" width="100%"></picture></a></p>

<sub>▸ <a href="https://akash-coded.github.io/aws-bedrock-agentcore-strands/assets/learn/wikimap-where-do-i-find-it.light.webp">Open the picture full size</a></sub>
<!-- /picture -->

| Reach for it when | How-to | Owner | Closes |
| --- | --- | --- | --- |
| Somebody is about to open an editor and nobody has written down what the thing may do | [Design an Agent on Paper](How-to-Design-an-Agent-on-Paper) | Solution architect | Spec |
| The NFRs are adjectives, and trade-offs get settled by seniority | [Run an NFR Workshop](How-to-Run-an-NFR-Workshop) | Solution architect | Requirements |
| Somebody has already picked the answer, and the decision must survive them leaving | [Choose Build, Buy or Borrow](How-to-Choose-Build-Buy-or-Borrow) | Solution architect | Decision |
| A score is being offered as proof | [Prove the Bar](How-to-Prove-the-Bar) | QA lead | Trust |
| The plan is ordered by priority, and day three needs something from day seven | [Cut Sprints into Bolts](How-to-Cut-Sprints-into-Bolts) | Engineering lead | Delivery |
| The queue is days long and the policy is two seniors on everything | [Review by Risk Band](How-to-Review-by-Risk-Band) | Engineering lead | Delivery |
| You cannot name the line of code that refuses | [Hold the Security Boundary](How-to-Hold-the-Security-Boundary) | Engineering lead, with the architect | — (the control set every loop assumes) |
| The bill left its estimate and traffic did not | [Control the Token Bill](How-to-Control-the-Token-Bill) | Engineering lead | Cost |
| The draft action list contains a string rather than a control | [Run a Missing-Control Postmortem](How-to-Run-a-Missing-Control-Postmortem) | QA lead | Incident |

## Doing

| I want… | It is here |
| --- | --- |
| To write the agent loop by hand | [Module 05](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/05-agent-loop-no-framework-to-strands) · [AGL-01](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/agent-loop/AGL-01) |
| Converse API syntax | [Cheat sheet](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/quick-reference/bedrock-converse.md) |
| Strands / LangGraph / AgentCore syntax | [Quick reference](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets/quick-reference) |
| To build RAG properly | [Module 10](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/10-rag-opensearch-litellm) · [`ragkit`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit) |
| To deploy an agent as a service | [Module 11](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/11-bedrock-agentcore) · [deploy how-to](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/how-to/engineers/deploy-any-agent-to-agentcore.md) |
| Graded practice | [L.A.B. Simulator](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs) — or [one click in Codespaces](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1) |
| The ideal lifecycle for a project like this | [Agentic PDLC · Lifecycle Reference](https://github.com/users/akash-coded/projects/8) — artefacts and gates mapped to AiDD, BMAD, AI-DLC |
| What is active in the repo right now | [Repo Pulse](https://github.com/users/akash-coded/projects/10) |
| Graded practice with nothing installed | [Simulator Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75) |
| Practice with other people's answers | [Discussion index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64) |

## Deciding

| I want… | It is here |
| --- | --- |
| To decide if this should be an agent | [Autonomy Ladder](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/autonomy-ladder.md) · [PDL-01](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/product/PDL-01) |
| To choose a multi-agent topology | [Handoff Multiplier](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/handoff-multiplier.md) · [how-to](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/how-to/architects/choose-a-topology.md) |
| To decide build vs buy | [Playbook](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/playbooks/build-buy-or-wait.md) |
| To run a design review | [Playbook](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/playbooks/agent-design-review.md) · [Scorecard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/agent-readiness-scorecard.md) |
| To write acceptance criteria | [How-to](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/how-to/product/write-acceptance-criteria.md) |
| A PRD template | [Seven sample PRDs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/docs/prd) |

## When it breaks

| I want… | It is here |
| --- | --- |
| A specific error message | **[Error Index](Error-Index)** |
| The AWS-specific errors | [Troubleshooting](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/troubleshooting.md) |
| To debug from a symptom | [Failure Signature Catalog](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/failure-signature-catalog.md) |
| An incident procedure | [Runbooks](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets/runbooks) |
| Things that break silently | [Silent Degradation Watchlist](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/silent-degradation-watchlist.md) |

## Copy-paste

| I want… | It is here |
| --- | --- |
| The two-line check for the repeating-tool-call bug | [`agent_history_invariant.py`](https://gist.github.com/akash-coded/12cd36b5e5ced3e0c5414af3abffa221) |
| A tool return contract the model cannot misread | [`honest_tool_result.py`](https://gist.github.com/akash-coded/e3748d8f0accfedf0a2509ee16195d51) |
| A release gate in 40 lines that can say no | [`release_gate.py`](https://gist.github.com/akash-coded/908a2f096a89de29d3b3221244773a1b) |
| An H× calculator for a design review | [`handoff_multiplier.py`](https://gist.github.com/akash-coded/407c5e9ddcca84afe7099439591d3ec2) |

## Career

| I want… | It is here |
| --- | --- |
| To prepare for an interview | [Interview guides](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets/interviews) — five roles, both sides |
| To hire for this | [Hiring guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/interviews/as-the-interviewer.md) |
| To teach this to a team | [Training frameworks playbook](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/reference/training-frameworks-playbook.md) |

---

**Not here?** Add a row — [anyone can edit](Contributing-to-this-Wiki). Or ask in [Q&A](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a) and the answer becomes a row.
