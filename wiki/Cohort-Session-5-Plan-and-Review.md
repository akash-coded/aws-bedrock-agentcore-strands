# Session 5 · Plan and review

*How is the work planned, boarded and reviewed when a model writes most of the code?*

Part of the [Cohort Kit](Cohort-Kit). Ninety minutes. The first of three sessions on running
delivery: by the end the room has a board shaped for agentic work, a review policy by risk band with
the queue arithmetic behind it, and has seen what a four-day review queue does to a team.

**Pre-reading** (about 40 minutes)

- [How to run an agentic AI project](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/how-to-run-an-agentic-ai-project/) — the whole of running delivery in one lesson
- [Bolts vs sprints](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/bolts-vs-sprints/) — planning when the model writes the code
- [A board for agentic work](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/agentic-kanban-board/) — the columns, the limits, and the two columns most boards lack
- [Cut delivery from months to weeks](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/cut-delivery-time/) — where the time actually goes
- [Review AI code by risk](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/review-ai-generated-code/) — review routed by the risk of the action, never by the size of the change

**Bring.** The bolt plan from session 3. The team's current review rules, if any are written down,
and a rough count of pull requests per week and reviewers.

**You will leave with.** A board design, a review policy by risk band, and the queue arithmetic
that justifies it to whoever asks why senior engineers are not reviewing everything.

## Run-sheet

| Minutes | Block | Do this | Material |
| --- | --- | --- | --- |
| 0–10 | Recap | *What is a bolt's definition of done? Which two columns does an agentic board add? What decides the review band: size or action?* | — |
| 10–35 | The idea | The bolts picture, then the Day 60 episode read aloud: nine pull requests, a four-day queue, two reviewers who cannot read any faster. Then the review queue calculator live, with the episode's numbers, so the room sees the queue fall when review is routed by band | [Bolts vs sprints](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/bolts-vs-sprints/) · [Day 60 · the review queue](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/story) · [Review queue calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/queue) |
| 35–65 | Exercise | Pairs play **the review bottleneck simulation**, one decision at a time, and record which options they chose. Then **B5 · queue arithmetic under a review policy** on the team's own pull-request and reviewer counts | [The review bottleneck](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/review) · [B5](Exercises-and-Answers#set-b--arithmetic) · [How to review by risk band](How-to-Review-by-Risk-Band) |
| 65–80 | Decision | The room writes **the review policy**: three bands, what puts a change in each, who reviews each and how fast. Then draws the board: columns, limits, and where the golden-set check sits | [Templates · engineering](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#engineering) · [How to cut sprints into bolts](How-to-Cut-Sprints-into-Bolts) |
| 80–90 | Close | Homework named. One sentence each: *what is the current queue, in days, and what would the band policy make it?* | — |

## Facilitator notes

- **"Every change needs a senior review" is the position the room starts from.** The queue
  arithmetic is what moves it. Do B5 on the team's real numbers; a four-day queue that becomes a
  one-day queue on the whiteboard is persuasive in a way the lesson is not.
- **Band by action, not by size.** Somebody will propose lines-of-code thresholds. The ladder
  picture on the frameworks page is the answer: four hundred lines of help text cannot move money,
  three lines in a refund cap can.
- **The simulation's bad paths are the teaching.** Encourage pairs to take one option they suspect is
  wrong and read the consequence. That is cheaper than learning it on Day 60.
- **Ten-minute version:** the Day 60 episode, then B5 on the team's numbers.

## Homework

**Set up the board** with the agreed columns and limits, and move the first three bolts onto it.
Write the review policy into the repository where reviewers will see it. Session 6 needs the golden
set column to exist.

## Next

**[Session 6 · Prove and ship](Cohort-Session-6-Prove-and-Ship)** — how accurate it must be, how
that is proven with a sample size, and how it reaches production without a leap. Back to
[Session 4](Cohort-Session-4-Methods-Decoded).
