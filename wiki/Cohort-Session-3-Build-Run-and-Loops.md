# Session 3 · Build, run and the loops

*How is it built in proven slices, run in production, and kept honest by the eight loops?*

Part of the [Cohort Kit](Cohort-Kit). Ninety minutes. The session that turns the spec into a plan:
by the end the room has a bolt order for the first slice, knows which loops close by themselves and
which three nobody is waiting on, and has the evidence pack for the P1 to P2 hand-off written out.

**Pre-reading** (about 40 minutes)

- [P2 · Build and prove](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/p2-build-and-prove/) — bolts, the golden set, and proving each slice before the next
- [P3 · Run and learn](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/p3-run-and-learn/) — shadow, cut-over, the two numbers, and what the model changes about operations
- [The eight loops](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-eight-loops/) — which loops close themselves and which need an owner
- [The evidence pack](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/the-evidence-pack/) — the minimum set of artefacts at each hand-off

**Bring.** The spec from session 2's homework, with the reviewer's mark on the one thing that could
not be built as written.

**You will leave with.** A bolt plan for the first slice, a named owner for each of the three loops
that does not close itself, and the P1 to P2 evidence pack as a checklist.

## Run-sheet

| Minutes | Block | Do this | Material |
| --- | --- | --- | --- |
| 0–10 | Recap | *What is a bolt? What closes the trust loop? Which three loops need an owner? What crosses the P1 to P2 hand-off?* | — |
| 10–35 | The idea | The loop map on screen: ask the room which loops the team already runs, under other names. Then the Day 30 episode, where the first bolt ships by four in the afternoon, and the evidence page, so the room sees what "done" looks like | [Loop map](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/loopmap) · [Day 30 · the first bolt](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/story) · [The evidence pack](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/evidence) |
| 35–65 | Exercise | Pairs do **D1 · ordering bolts by dependency** on the team's spec, then **D4 · a bolt that cannot be built alone**. Then **B2 · chained probability** on the candidate's own step count, so the room feels why short chains matter before anyone proposes a long one | [D1, D4](Exercises-and-Answers#set-d--delivery) · [B2](Exercises-and-Answers#set-b--arithmetic) · [Sprint-to-bolt planner](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/bolts) |
| 65–80 | Decision | The room fixes **the first three bolts, in order**, each with the check that proves it; names an owner for the drift, cost and learning loops; and ticks the P1 to P2 evidence pack against what actually exists | [The minimum artefact set](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/governance/gv-artefacts) · [Templates · engineering](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#engineering) |
| 80–90 | Close | Homework named. One sentence each: *which loop does your team currently not run, and who should own it?* | — |

## Facilitator notes

- **A bolt is not a small story.** The test is "can it be built alone and proven alone". The room
  will propose bolts that depend on two others; D4 exists to catch that. Draw the dependency arrows
  on the board.
- **B2 lands hardest on the architects.** Four steps at 90% is 66% end to end. If the candidate's
  design has six model calls in a row, this is where somebody says so. Let them.
- **The three loops nobody is waiting on** are drift, cost and learning. Every team has an owner for
  the build loop and none for these. Names on the board, not roles.
- **Ten-minute version:** the loop map with the room naming what it already does, then D1 on the spec.

## Homework

**The bolt plan** for the first slice, in the engineering lead's
[template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#engineering),
with the proof for each bolt written before the bolt. If the team has a repository, the first bolt
is opened as a ticket with the proof in its description.

## Next

**[Session 4 · Methods decoded](Cohort-Session-4-Methods-Decoded)** — where AI-DLC, AIDD, BMAD and
spec-driven development actually sit, and how much process each change needs. Back to
[Session 2](Cohort-Session-2-Frame-and-Spec).
