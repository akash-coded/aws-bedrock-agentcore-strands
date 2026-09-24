# Session 2 · Frame and spec

*What is the candidate worth, how often must it be right, and what does a spec an agent can be built from look like?*

Part of the [Cohort Kit](Cohort-Kit). Ninety minutes. The arithmetic session: by the end the room
has a value line, a bar derived from damage and saving, an autonomy decision, and has seen the one
hard gate that decides whether anything gets built.

**Pre-reading** (about 35 minutes)

- [P0 · Frame](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/p0-frame/) — is an AI agent worth building: the pain register, the AI-fit verdict, the value line, the autonomy decision
- [P1 · Design and spec](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/p1-design-and-spec/) — a spec an agent can build from, and the decisions it deliberately leaves to the builder
- [The one hard gate](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-hard-gate/) — why the spec, the bar and the guardrails are settled before P2 opens, and nothing else is

**Bring.** The pain register from session 1's homework, with numbers. Last quarter's figures for
cases per day and cost per wrong case, if the team has them.

**You will leave with.** A value line for the candidate, a bar with the damage and saving it came
from, an autonomy decision record, and the list of what the hard gate needs before the build starts.

## Run-sheet

| Minutes | Block | Do this | Material |
| --- | --- | --- | --- |
| 0–10 | Recap | *What are the four P0 artefacts? What are the three things the hard gate needs? What is a decision left to the builder?* | — |
| 10–35 | The idea | Walk the P0 map from the lesson, then the hard-gate picture. In the playbook, run the value line calculator on SkyWays' numbers live, then the acceptance bar calculator, so the room sees the bar move when the damage figure moves | [P0 · Frame](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/p0-frame/) · [The hard gate](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-hard-gate/) · [Value line](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/value) · [Acceptance bar](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bar) |
| 35–65 | Exercise | Pairs do **A3 · the value line** and **B1 · deriving a bar** on the team's candidate, using the pain register. Then every pair puts its bar on the board. The spread is the exercise: find the assumption that differs | [A3, B1](Exercises-and-Answers#set-b--arithmetic) · [Formulas](Formulas-and-Calculators) |
| 65–80 | Decision | The room settles **one damage figure and one saving figure**, derives the bar from them, and records the autonomy level for the riskiest action with the kind of door it is. Then lists what the hard gate still needs | [Autonomy decision record](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/autonomy) · [Hard or soft gate classifier](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/gateclass) · [Templates · Frame and Specify](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#lt-product-manager-frame) |
| 80–90 | Close | Homework named. One sentence each: *what does the bar make you want to change about the candidate?* | — |

## Facilitator notes

- **The bar will come out high.** A refund with $600 of damage needs about 98% to break even. The
  lesson the room needs is the [lever](https://akash-coded.github.io/aws-bedrock-agentcore-strands/models/#lever):
  a person on the charge drops the damage, and the same step needs 71%. Do not let the room conclude
  "we cannot build this"; let it conclude "not at that autonomy level".
- **Spread on the board is good.** If every pair has the same bar, somebody copied. Ask which
  assumption differs before checking against the worked answer; the assumption is the session.
- **"Decisions left to the builder"** is the part of P1 people skip. Have the room name three for the
  candidate. If it cannot, the spec is a wish list.
- **Ten-minute version:** the hard gate in one sentence, the bar formula on the whiteboard with the
  SkyWays numbers, then straight to B1 on the candidate.

## Homework

**The spec**, in the product manager's [Specify](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#lt-product-manager-specify)
template, with the decisions left to the builder marked as such, and the bar with its damage and
saving beside it. The engineer or architect in the room reviews it before session 3 and marks one
thing the builder could not build from as written.

## Next

**[Session 3 · Build, run and the loops](Cohort-Session-3-Build-Run-and-Loops)** — how it is built
in proven slices, run in production, and kept honest by the eight loops. Back to
[Session 1](Cohort-Session-1-Kick-off).
