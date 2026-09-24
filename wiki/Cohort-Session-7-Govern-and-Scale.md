# Session 7 · Govern and scale

*What holds, what gates, what drifts, and how does an organisation adopt this without rejecting it?*

Part of the [Cohort Kit](Cohort-Kit). Ninety minutes. The session for the people who will be asked
"how do we know it is safe": by the end the room can say where a boundary is enforced and where it
is only a prompt, has mapped the gates and who signs, has run a postmortem that names a missing
control, and has scored the team's maturity.

**Pre-reading** (about 40 minutes; the last two are for whoever is rolling this out)

- [Guardrails that hold](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-guardrails-that-hold/) — a prompt is a request; a signature is a boundary
- [The five governance gates](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-governance-gates/) — gates that do not slow delivery, and what may halt a phase
- [Catch AI drift](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-drift-monitoring/) — the defect with no error message
- [AI incident postmortems](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-incident-postmortem/) — find the missing control, not the string
- For the rollout owner: [The maturity model](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/ai-delivery-maturity-model/) · [Rolling it out in 90 days](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/rolling-out-agentic-delivery/) · and, if time allows, [Team structure](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/team-structure-for-agentic-ai/) and [Measuring AI productivity](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/measure-ai-productivity/)

**Bring.** The autonomy decision record from session 2. The list of tools or actions the candidate
agent can take. Any policy document the organisation already has about AI.

**You will leave with.** A gate map with the control each tool carries and who signs at each
hand-off, an injection test list, a postmortem template the team has used once, and a maturity score.

## Run-sheet

| Minutes | Block | Do this | Material |
| --- | --- | --- | --- |
| 0–10 | Recap | *Where is a boundary enforced? What halts a phase, and what runs alongside it? What does drift look like on a dashboard? What is the difference between a postmortem that names a string and one that names a control?* | — |
| 10–35 | The idea | The governance page: hard gates and soft gates, then the RACI on the artefacts, so the room sees that signing is by artefact, not by meeting. Then the Day 82 episode: a $2,000 refund that was not owed, and one hour in the postmortem room | [Hard gates and soft gates](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/governance/gv-gates) · [Who signs](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/governance/gv-raci) · [Day 82 · the incident](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/story) |
| 35–65 | Exercise | Pairs do **C2 · where a boundary is enforced** and **G5 · a cap that is not a control** on the candidate's own tool list. Then play **the incident simulation** and run **E2**: rewrite the postmortem so it names the missing control | [C2](Exercises-and-Answers#set-c--design) · [G5](Exercises-and-Answers#set-g--reading-a-symptom) · [The incident](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/simulations/incident) · [E2](Exercises-and-Answers#set-e--running) · [How to hold the security boundary](How-to-Hold-the-Security-Boundary) |
| 65–80 | Decision | The room maps **the control each tool carries** and who signs at each hand-off; builds the first three injection tests; then answers the maturity self-check's six questions and records the score and the one thing to fix next | [Authority and gate mapper](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/gates) · [Injection test builder](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/inject) · [Maturity self-check](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/maturity) · [Gates and governance](Gates-and-Governance) |
| 80–90 | Close | Homework named. One sentence each: *which control does the team believe it has that is actually a prompt?* | — |

## Facilitator notes

- **"It is in the system prompt" is the answer to test.** C2 and G5 both resolve to the same
  finding: a cap the model is asked to respect is not a control; a cap the tool signature refuses is.
  Have the room find one of each in its own tool list.
- **The postmortem exercise produces a string the first time.** "The model said X" is the symptom. Ask
  "which line of code refuses?" until the answer is a control that was missing, then write that.
- **The maturity score will be low, and that is fine.** The self-check is by control, not by
  ambition. Record it; session 8 sets the plan, and the [rollout lesson](https://akash-coded.github.io/aws-bedrock-agentcore-strands/learn/rolling-out-agentic-delivery/)
  is for whoever owns the ninety days.
- **Ten-minute version:** the hard-gates page, then G5 on the candidate's tools.

## Homework

**The two-number report**, drafted for the candidate as if it had run for a month: the time saved and
the money spent, in the playbook's builder, then in the product manager's
[Learn](https://akash-coded.github.io/aws-bedrock-agentcore-strands/templates/#lt-product-manager-learn)
template. The numbers are projections; the shape is what the sponsor will read every cycle from now on.
[Two-number report builder](https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/#/toolkit/report).

## Next

**[Session 8 · Practice and roles](Cohort-Session-8-Practice-and-Roles)** — what each person in the
room does on Monday. Back to [Session 6](Cohort-Session-6-Prove-and-Ship).
