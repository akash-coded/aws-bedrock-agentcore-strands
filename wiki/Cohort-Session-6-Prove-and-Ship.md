# Session 6 · Prove and ship

*How accurate must it be, how is that proven with a sample size, and how does it reach production without a leap?*

Part of the [Cohort Kit](Cohort-Kit). Ninety minutes. The evidence session: by the end the room can
say whether a score has proven a bar, knows how many cases that takes, has a cut-over schedule with
the days each traffic share needs, and can read a token bill.

**Pre-reading** (about 40 minutes)

- [How accurate must an agent be?](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/how-accurate-must-an-ai-agent-be/) — the bar, derived, and why it is a business number
- [Prove the agent meets its bar](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/prove-ai-accuracy/) — a score is not proof: the lower bound and the cases it needs
- [Shadow mode and cut-over](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/shadow-mode-and-cutover/) — evidence arrives at the speed of traffic
- [Why the AI bill is 4× the estimate](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-agent-costs/) — the habits that multiply, and which to fix first

**Bring.** The bar from session 2 with its damage and saving. The candidate's expected daily
traffic. If the team already runs a model anywhere, last month's token bill.

**You will leave with.** The golden-set size the bar needs, a cut-over schedule by traffic share,
and a decomposed estimate of the running bill with the largest habit named.

## Run-sheet

| Minutes | Block | Do this | Material |
| --- | --- | --- | --- |
| 0–10 | Recap | *Why is 94% an incomplete sentence? What does shadow mode produce that a test set cannot? Which of the four cost habits is charged on every turn?* | — |
| 10–35 | The idea | The Day 45 episode: eighty-two point four against a bar of eighty, and why that has not proven anything yet. The confidence calculator live with the episode's 412 of 500, then with 82 of 100, so the room watches the bound move with the sample. Then the cut-over calculator for one traffic share | [Day 45 · the score](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/story) · [Golden-set confidence calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/confidence) · [Cut-over evidence calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/cutover) |
| 35–65 | Exercise | Pairs do **B3 and B4 · lower bounds** on the team's bar with two sample sizes, then play **the bill blowout simulation**: 4.4 times the estimate with flat traffic and finance wants an answer by Friday. Then **D3 · which factor to fix first** on the simulation's numbers | [B3, B4](Exercises-and-Answers#set-b--arithmetic) · [The bill blowout](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/bill) · [D3](Exercises-and-Answers#set-d--delivery) · [How to prove the bar](How-to-Prove-the-Bar) |
| 65–80 | Decision | The room fixes **the golden-set size** for the bar at the confidence the sponsor will accept, **the cut-over schedule** (shares and the days each needs at expected traffic), and names the one cost habit it will control from the first bolt | [Templates · QA](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#qa) · [Bill leak calculator](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/leaks) · [How to control the token bill](How-to-Control-the-Token-Bill) |
| 80–90 | Close | Homework named. One sentence each: *how many cases does your bar need, and where will they come from?* | — |

## Facilitator notes

- **The convention is z = 1.96, a 95% two-sided bound,** everywhere in the manual, the playbook and
  the wiki. Day 45's 412 of 500 gives 79.1% against a bar of 80, and needs 968 cases to prove it. Use
  those numbers; the room will check them.
- **The cost of proving grows quadratically as the score approaches the bar.** A score a whisker
  above the bar is the most expensive result there is. Somebody will ask why not lower the bar; the
  answer is session 2's damage figure, not this session.
- **The bill simulation's wrong paths are all plausible.** "Buy a cheaper model" is the one most
  rooms pick first. Let them, and read the consequence together.
- **Ten-minute version:** the Day 45 episode, the calculator with 412 of 500, then B3 on the team's bar.

## Homework

**The golden-set plan**: where the cases come from, how they are labelled, how many, and who owns the
set, in the QA lead's [template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#qa).
If the candidate's traffic is known, the cut-over schedule goes in the DevOps
[template](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#devops) beside it.

## Next

**[Session 7 · Govern and scale](Cohort-Session-7-Govern-and-Scale)** — what holds, what gates,
what drifts, and how an organisation adopts this without rejecting it. Back to
[Session 5](Cohort-Session-5-Plan-and-Review).
