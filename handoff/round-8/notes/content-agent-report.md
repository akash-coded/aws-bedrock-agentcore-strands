REPORT: content repair (dash-sweep damage, old names, long summaries)

All three jobs are done inside my file limits. No git state was changed. Nothing was written to site/_site. No dash was put back anywhere; I also removed the last em/en dashes that were still sitting in lessons and role content (listed separately below).

Size of the change: 55 lesson files, start-here.md, curriculum.py, frameworks.json, 15 role source files plus the 5 generated role JSON files, 26 hand-written wiki pages, and the 5 generated Journey wiki pages (regenerated from the role JSON, see section 1d).

Machine-readable versions of every change (scratchpad working data, not report files):
- handoff/round-8/notes/r7/editor/job1_lessons.txt (TSV: job, lesson, before, after; job = 1, 2, 3 or D for leftover dashes)
- .../scratchpad/r7/editor/job_roles.txt (TSV: job, role, JSON path, before, after)
- .../scratchpad/r7/editor/applied.jsonl (every replacement in frameworks.json, role sources and wiki pages: file, old, new, job)
- Snapshots from before my edits: .../scratchpad/r7/editor/base_lessons/, base_roles/, base_src/

====================================================================
1. JOB 1: DASH-SWEEP DAMAGE
====================================================================

1a. How I searched

- Found the sweep: commit d845ae1 (1,358 dashes replaced), with follow-ups 9f4f86a and 0c379b2. I built a token-level diff of every dash replacement site across the sweep (1,643 sites in content) and looked at each one as it stands today. Roles were reviewed as row lists; every lesson was read in full beside its row list.
- Symptom scans over today's content: unbalanced brackets per line and per paragraph, fields that are only punctuation, " ,", ", .", ",,", "?.", "?,", "?:", " :", ": and", two colons in one sentence, and "**Label** (" / "**Label**)" at line ends.
- Final rescan after all edits: no symptom hits in lesson prose; the only hits in role JSON are code ("AWS::Budgets::Budget", "fare_difference()").

1b. What the damage looked like
- Bracket pairs made from two unrelated dashes on consecutive lines: "**Pain** (<...> / **Evidence**) <...>", "## Spec ( ... ## Tools) ...", "`<src/tools/refund/**>` (two named reviewers ... `<migrations/>`) never edit".
- Data cells that were a lone dash turned into ": ", " (" or ") " (frameworks.json "From" cells).
- A colon where a comma belonged ("never of its size" clauses) and a comma where a colon or brackets belonged (comma splices and unmarked asides).
- "?." on the role page: activity names ending in "?" get a full stop appended by render.py.

1c. Repairs: library and curriculum

site/content/library/frameworks.json (acronym table, "From" cell)
| Row | Broken | Repaired |
| AIDD | ": " | "No single owner" |
| BMAD | ": " | "BMad Code" (the credit the BMAD lesson already gives; please confirm) |
| RACI | " (" | "No single source" |
| SDD | ") " | "No single owner" |
| p^n | ": " | "Basic probability" |
These five cells held a lone dash before the sweep, so the new words are mine. They are the one place in Job 1 where I had to supply content. Owner's eye wanted.

site/content/learn/curriculum.py
| "works in the agentic PDLC, product, programme, archit... sponsor and the executive: what" | "works in the agentic PDLC (product, programme, archit... sponsor and the executive): what" |

1d. Repairs: role content (fixed in site/content/roles/_src/*.py, then regenerated; JSON carries the same text)
One line per replacement, "broken => repaired". Long lines are whole template blocks.

devops_a.py
permissions, recovery, the list is => permissions, recovery: the list is
rather than for use, a classic Open => rather than for use: a classic Open
memory bills by the hour, so the ordinary => memory bills by the hour. So the ordinary
radius is a business fact, which failures you can survive and who has to explain them, and a model => radius is a business fact (which failures you can survive and who has to explain them) and a model
would *not* catch, a quota, a dat => would *not* catch: a quota, a dat
devops_b.py
ts behind a load balancer, the mechanism => ts behind a load balancer: the mechanism
decisions the agent makes, refund versus => decisions the agent makes: refund versus
sustained for an hour, a retry loop => sustained for an hour: a retry loop
-cap trips above baseline, the agent is g => -cap trips above baseline: the agent is g
ache hit ratio collapsing, somebody moved => ache hit ratio collapsing: somebody moved
devops_c.py
vilege is fifty years old, Saltzer and Schroeder set it out in 1975, and nothing => vilege is fifty years old (Saltzer and Schroeder set it out in 1975) and nothing
equest can be argued with, by a passenger => equest can be argued with: by a passenger
That has three controls, a loop cap => That has three controls: a loop cap

engineering_a.py
The **bolt cut** itself, the architect => The **bolt cut** itself: the architect
cceptance bar** per slice, the PM derives => cceptance bar** per slice: the PM derives
g longer stops being read, by the model, => g longer stops being read: by the model,
om what is actually there, the build file => om what is actually there: the build file
- One model per task, the cache is m => - One model per task: the cache is m
- `<src/tools/refund/**>` (two named reviewers, every time. - `<migrations/>`) never edit an => - `<src/tools/refund/**>`: two named reviewers, every time. - `<migrations/>`: never edit an
under `<src/prompts/>`, it re-runs the => under `<src/prompts/>`: it re-runs the
_Last rule added <date>, <the rule that => _Last rule added <date>: <the rule that
could be ENFORCED instead, a lint rule, a => could be ENFORCED instead: a lint rule, a
where the ledger said $62, the line added => where the ledger said $62: the line added
**no: and if no, this is raised NOW => **no. If no, this is raised NOW
rite WITHIN <UNSPECIFIED>, never invent a n => rite WITHIN <UNSPECIFIED>. Never invent a n
engineering_b.py
ng, drafting, classifying: the work that => ng, drafting, classifying. This is the work that
with an adversarial brief, *find what is => with an adversarial brief: *find what is
caught it, exact test, go => caught it: exact test, go
engineering_c.py
tires the largest unknown, whether the pieces connect at all, on day one => tires the largest unknown (whether the pieces connect at all) on day one
never from the author, every author b => never from the author: every author b
he walking skeleton first, the thinnest e => he walking skeleton first: the thinnest e
list headed FILE DEFECTS, everything you => list headed FILE DEFECTS: everything you
list headed OUT OF SCOPE, problems you f => list headed OUT OF SCOPE: problems you f
other bolt was resting on, whether the pi => other bolt was resting on: whether the pi
Mask, do not omit, `passport **** => Mask, do not omit: `passport ****
er on the model's wording, wording change => er on the model's wording: wording change
column is the leak signal, model switchin => column is the leak signal: model switchin
two orders are different, the retry brea => two orders are different: the retry brea
not a habit, traffic, a new => not a habit: traffic, a new
RULES, these decide whether the suite is worth anything: => RULES (these decide whether the suite is worth anything):
ies per conversation 1.41: and they multi => ies per conversation 1.41, and they multi
worth fixing permanently, an alert at th => worth fixing permanently: an alert at th

product_manager_a.py
plus anything that leaks, a lost passeng => plus anything that leaks: a lost passeng
write "not stated", never estimate. => write "not stated". Never estimate.
carries fixed costs, evaluation, ga => carries fixed costs: evaluation, ga
- **Rule in code**, <rejected because ...> - **A person**, <cost at this volume> - **Fully agentic**, <rejected => - **Rule in code**: <rejected because ...> - **A person**: <cost at this volume> - **Fully agentic**: <rejected
verable steps are: <list>: these are gated => verable steps are: <list>. These are gated
a genuine judgement call, could two comp => a genuine judgement call: could two comp
Judgement: yes: which alternativ => Judgement: yes. Which alternativ
Recoverable: **partly**: a proposed reboo => Recoverable: **partly**. A proposed reboo
Ask: is there a genuine judgement call? => Ask whether there is a genuine judgement call
Ask: is the volume high enough? => Ask whether the volume is high enough
Ask: is a wrong answer recoverable? => Ask whether a wrong answer is recoverable
(These three are the "?." fix: render.py appends "." to the first activity name, which printed "judgement call?." on the role page.)
product_manager_b.py
write UNKNOWN, do not estimate. => write UNKNOWN. Do not estimate.
3. What is the DOOR, if we raise it => 3. What is the DOOR: if we raise it
decide each one yourself, the guesses ar => decide each one yourself: the guesses ar
both have a formula, use the formul => both have a formula: use the formul
write "NOT DECIDED, <the question => write "NOT DECIDED: <the question
was cut wrong, send it back b => was cut wrong: send it back b
should come early, it stands alon => should come early: it stands alon
## Spec (the EARS criteria ... ## Tools) signatures ... ## Tests (the golden slice ... ## Done when) one testable l => ## Spec: the EARS criteria ... ## Tools: signatures ... ## Tests: the golden slice ... ## Done when: one testable l
product_manager_c.py
## Disagreements, the themes => ## Disagreements: the themes
which and why, do not assume th => which and why. Do not assume th
ld take more than 30 days, those need a b => ld take more than 30 days: those need a b
**Pain** (<what happened, as a measurement> **Evidence**) <trace id, date, link> **Finding**, the enforced control that was missing: <name it> **Fix**, <the control, where it will live> **Value**, <this class => **Pain**: <what happened, as a measurement> **Evidence**: <trace id, date, link> **Finding** (the enforced control that was missing): <name it> **Fix**: <the control, where it will live> **Value**: <this class
his keeps number 1 honest, never omit it) => his keeps number 1 honest; never omit it)
**Pain** (what happened, as a measurement (amount, count, who was affected) **Evidence**) the trace or log reference **Finding** (the ENFORCED CONTROL that ... IMPOSSIBLE **Fix**) where that con => **Pain**: what happened, as a measurement (amount, count, who was affected) **Evidence**: the trace or log reference **Finding**: the ENFORCED CONTROL that ... IMPOSSIBLE **Fix**: where that con
prompt" is NOT a control, a prompt is a => prompt" is NOT a control: a prompt is a
The programme continued: not because th => The programme continued, not because th

qa_a.py
**behaviour**: does it meet the spec?, and **expansion**, have we earned wider use? The craft => **behaviour** (does it meet the spec?) and **expansion** (have we earned wider use?). The craft
he harness that runs them, all work that => he harness that runs them: all work that
**Exact** work, the fare arithmetic, owes a unit te => **Exact** work (the fare arithmetic) owes a unit te
**Best-guess** work, which alternative suits this passenger, owes a measure => **Best-guess** work (which alternative suits this passenger) owes a measure
**Consequential** work, the refund, owes a require => **Consequential** work (the refund) owes a require
it is the whole value, engineering ma => it is the whole value: engineering ma
not recover from the data, the data recor => not recover from the data: the data recor
desk actually did, that turns the => desk actually did: that turns the
eds the history available, those need a h => eds the history available: those need a h
*after* the exact checks, running it fir => *after* the exact checks: running it fir
checks as ordinary tests, schema validat => checks as ordinary tests: schema validat
se are different problems, the first wast => se are different problems: the first wast
qa_b.py
or a slice with n = 0, a configuratio => or a slice with n = 0: a configuratio
is at or below the bar, no sample size => is at or below the bar: no sample size
clears the new bar, lower bound, not point estimate. => clears the new bar (lower bound, not point estimate).
came in through, say so, that => came in through, say so: that
d for an UNRELATED reason, a timeout, a t => d for an UNRELATED reason: a timeout, a t
**none** of them enforced, two of the fiv => **none** of them enforced: two of the fiv
qa_c.py
## Disagreements, themes, not ca => ## Disagreements: themes, not ca
the desk as ground truth, say so when => the desk as ground truth: say so when
run cleared its threshold, **96%** agreement over fourteen days against a 95% default, and the room => run cleared its threshold (**96%** agreement over fourteen days against a 95% default) and the room
-week rule never fires on, under 2pp a we => -week rule never fires on: under 2pp a we
lowers the probability, the next attem => lowers the probability: the next attem
| neither, that is detect => | neither: that is detect
slice, say so, the incident m => slice, say so: the incident m
confidence at full price, and worse than no => confidence at full price. That is worse than no

solution_architect_a.py
k version, SDK call shape, you specify be => k version, SDK call shape: you specify be
dited to the wrong person, that correctio => dited to the wrong person: that correctio
s a number and a location, a typed parame => s a number and a location: a typed parame
anager sorted the feature. This is a judgem => anager sorted the feature: this is a judgem
prompt-level test catches, $80 when the l => prompt-level test catches: $80 when the l
classification felt hard, that reason is => classification felt hard: that reason is
solution_architect_b.py
| a function, map, step <n> | => | a function (map, step <n>) |
d limit that justifies it, a number, => d limit that justifies it: a number,
function and one checker, **zero hand-of => function and one checker: **zero hand-of
f points and nowhere else, forty records => f points and nowhere else: forty records
itability against latency, logging costs => itability against latency: logging costs
a preference is a failure, rewrite it, or => a preference is a failure: rewrite it, or
one that usually turns up, latency agains => one that usually turns up: latency agains
ed review at month twelve, two weeks of work now to keep a swap => ed review at month twelve. Two weeks of work now keeps a swap
a refund cap is R4, re-read every R1 => a refund cap is R4. Re-read every R1
eholder for each soft one, a stub, an int => eholder for each soft one: a stub, an int
R1 reversible draft or sandbox, review at the end R2 reversible change to real work, review before merge R3 hard to reverse, small blast radius (approve first R4 money, identity or a policy commitment) a NAMED approver, every time R5 irreversible or safety-critical, not delegated => R1 ... sandbox: review at the end R2 ... real work: review before merge R3 ... small blast radius: approve first R4 ... policy commitment: a NAMED approver, every time R5 ... safety-critical: not delegated
solution_architect_c.py
ds most of the real reuse, the booking mo => ds most of the real reuse: the booking mo
efence is removing a step, every step you => efence is removing a step: every step you
worst action it can reach, reject it and ma => worst action it can reach. Reject it and ma
on, output, model version - **Rejected:** <one broad manage_booking(action) tool) any path throu => on, output, model version) - **Rejected:** <one broad manage_booking(action) tool: any path throu
esign decision comes from, a postmortem t => esign decision comes from: a postmortem t
assertion that proves it, cache tokens r => assertion that proves it: cache tokens r
| A model switch mid-task, the cache is model-scoped | => | A model switch mid-task (the cache is model-scoped) |
not from the price list, the prices did => not from the price list: the prices did
**Timeline** (what happened, minute by minute ... consequence **Reconstruct**) for each contr => **Timeline**: what happened ... consequence **Reconstruct**: for each contr
**Finding** (the ENFORCED control that ... IMPOSSIBLE **Not the finding**) the input, the => **Finding**: the ENFORCED control that ... IMPOSSIBLE **Not the finding**: the input, the
**Change** (the typed param => **Change**: the typed param
**Record**) the record num => **Record**: the record num

Generated files: I ran python3 site/content/roles/_src/build_content.py after the source edits; site/content/roles/*.json now reproduce from the sources (see checks). The five wiki Journey pages (wiki/Journey-*.md) are generated from the role JSON by site/wiki_export.py, so I regenerated them in memory with wiki_export.page(role) and kept each page's existing tutorial pointer line under the H1. The diff shows only content lines changed.

1e. Repairs: lessons (site/content/learn/lessons/<name>.md)
333 changed spans. One line per span, "broken => repaired"; a bracket pair shows as two lines.

agentic-ai-engineer-interview-questions
the autonomy ladder, build the lowest rung => the autonomy ladder: build the lowest rung
chained steps multiply, eight steps each right 90 => chained steps multiply: eight steps each right 90
the cost cliffs, loops, retries, swarms => the cost cliffs: loops, retries, swarms
preventing runaway loops: plus a production failure => preventing runaway loops, plus a production failure
's pattern a platform rule, consequential tools carry ... tokens by construction, and interview for it => 's pattern a platform rule (consequential tools carry ... tokens by construction) and interview for it
agentic-ai-for-executives
set the target on outcomes, the two numbers, rather than => set the target on outcomes (the two numbers) rather than
agentic-delivery-cadence
proof runs on two triggers, every change and every we => proof runs on two triggers: every change and every we
ystem mostly fails quietly, behaviour drifts with no => ystem mostly fails quietly: behaviour drifts with no
asks the four questions, which of these are rules, ... what level are we, in about ten minutes => asks the four questions (which of these are rules, ... what level are we) in about ten minutes
ise bill gets one question, which of the four signatu => ise bill gets one question: which of the four signatu
a weekly operations review, the drift chart, the atta => a weekly operations review: the drift chart, the atta
pt, tool or context change, every attack string again => pt, tool or context change: every attack string again
agentic-delivery-simulator
the path that feels faster, the second run is where => the path that feels faster. The second run is where
ict is the same under both, not yet proven. => ict is the same under both: not yet proven.
agentic-kanban-board
rule on the column itself, most tools let you add a description, so nobody => rule on the column itself (most tools let you add a description) so nobody
tool or path it touches: never of its size. => tool or path it touches, never of its size.
in **slots**, not cards, a change needing two readers takes two, and measure => in **slots**, not cards (a change needing two readers takes two) and measure
sion** rather than on work, a soft gate with a placeh => sion** rather than on work: a soft gate with a placeh
| Whether the cut is right, a falling rate means => | Whether the cut is right: a falling rate means
s-only lane with no reader, and count any defects that escape through it, and check => s-only lane with no reader (and count any defects that escape through it), and check
pacity**, counted in slots, read the queue, => pacity**, counted in slots. Read the queue,
Count review in slots, a change needing two readers takes two, and measure => Count review in slots (a change needing two readers takes two) and measure
agentic-pdlc-exercises
the proof arithmetic of P2 (lower bounds, cases needed ... roduction arithmetic of P3) the bill, drift => the proof arithmetic of P2: lower bounds, cases needed ... roduction arithmetic of P3: the bill, drift
(a) has no judgement call, two competent people => (a) has no judgement call: two competent people
bound: 78.6%, below 85%: its score is five points => bound: 78.6%, below 85%. Its score is five points
evidence and bill leaks) each prefilled => evidence and bill leaks), each prefilled
agentic-pdlc-for-business-sponsors
ost of the job is familiar, backing a programme => ost of the job is familiar: backing a programme
you specified in advance, a demo is not evidence | => you specified in advance: a demo is not evidence |
with behaviour, not volume, a bill can multiply => with behaviour, not volume: a bill can multiply
the per-call log shows, tokens per call up, ... retries up, and which decision record => the per-call log shows (tokens per call up, ... retries up) and which decision record
Ask one question, *which enforced control ... impossible?*, and do not accept a name => Ask one question: *which enforced control ... impossible?* Do not accept a name
name who owns governance, if the answer is "we all do" => name who owns governance. If the answer is "we all do"
a demo is not evidence, decide on the three reports => a demo is not evidence. Decide on the three reports
and **which control**: never for a freeze => and **which control**, never for a freeze
owns governance, the one loop no delivery role is accountable for, by insisting => owns governance (the one loop no delivery role is accountable for) by insisting
agentic-pdlc-for-devops
plus a budget alarm: before any resource exist => plus a budget alarm, before any resource exist
pinned** in each manifest, for a probabilistic => pinned** in each manifest: for a probabilistic
| The acceptance bar, you make the gate unargua => | The acceptance bar: you make the gate unargua
| Prompt content, you version, deploy and r => | Prompt content: you version, deploy and r
what a mistake costs, the business's input => what a mistake costs: the business's input
elease and expansion gates, you supply the evidence => elease and expansion gates: you supply the evidence
an access analyser) then read the diff => an access analyser), then read the diff
serving your own models, data pipelines, training => serving your own models: data pipelines, training
agentic-pdlc-for-engineers
every coding tool reads, stack, context layers => every coding tool reads: stack, context layers
| The bolt cut, the architect's; => | The bolt cut: the architect's;
| The acceptance bar, the product manager deriv => | The acceptance bar: the product manager deriv
and the judge rubric. QA's | => and the judge rubric: QA's |
The cut-over and widening, you build the flag; => The cut-over and widening: you build the flag;
agentic-pdlc-for-product-managers
what counts as right: and a coding agent cannot => what counts as right, and a coding agent cannot
You set the cadence, how often evidence arrives; the architect => You set the cadence (how often evidence arrives); the architect
| Not yours, stop signing these | => | Not yours: stop signing these |
aviour and expansion gates. QA's | => aviour and expansion gates: QA's |
temperature, framework, behaviours are yours => temperature, framework: behaviours are yours
The golden set's contents, you set the bar => The golden set's contents: you set the bar
agentic-pdlc-for-program-managers
Put the evidence days, cases needed ÷ cases per day at the canary share, in the plan. => Put the evidence days (cases needed ÷ cases per day at the canary share) in the plan.
| The acceptance bar, the product manager deriv => | The acceptance bar: the product manager deriv
| The decisions themselves, you chase them => | The decisions themselves: you chase them
The risk band of a change, the path rule decides it => The risk band of a change: the path rule decides it
has earned wider use. QA's call | => has earned wider use: QA's call |
| Signing it, the sponsor is accountabl => | Signing it: the sponsor is accountabl
a placeholder, an interface layer, so the build can proceed. => a placeholder (an interface layer) so the build can proceed.
each open decision as hard, settled before its phase closes, or soft, running behind a placeholder with an owner and a date, and chase => each open decision as hard (settled before its phase closes) or soft (running behind a placeholder with an owner and a date), and chase
agentic-pdlc-for-qa
five hundred to trust) each tagged by slice => five hundred to trust), each tagged by slice
never the score, 412 of 500 is 82.4% => never the score. 412 of 500 is 82.4%
| The bar itself, the PM derives it; => | The bar itself: the PM derives it;
| The fix, you name the defect => | The fix: you name the defect
prompt wording, you assert on behaviour | => prompt wording: you assert on behaviour |
nobody can argue with: and the reason a launch => nobody can argue with, and the reason a launch
and did any fall, an overall rise can hide => and did any fall? An overall rise can hide
how was "accurate" judged, by an exact check => how was "accurate" judged: by an exact check
a bar with confidence: more when the score sits => a bar with confidence, and more when the score sits
agentic-pdlc-for-solution-architects
make a target impossible, the $400 refund rule => make a target impossible: the $400 refund rule
work already in flight, if the map is wrong, say so => work already in flight. If the map is wrong, say so
intent and release gates, the product manager's | => intent and release gates: the product manager's |
top-p, framework version, engineering picks => top-p, framework version: engineering picks
and the judge rubric. QA's | => and the judge rubric: QA's |
calculation is arithmetic, a tested function => calculation is arithmetic: a tested function
the limit that forces it, a context that genuinely => the limit that forces it: a context that genuinely
ai-agent-costs
runaway, no single mistake, four sensible decisions => runaway, no single mistake: four sensible decisions
model, attempts, per case) that is the first fix => model, attempts, per case), that is the first fix
a read about **0.1×**: so a prefix used twice => a read about **0.1×**, so a prefix used twice
a bill surprises anyone**: before any budget => a bill surprises anyone**, before any budget
tier, cache, attempts) visible only per call => tier, cache, attempts), visible only per call
ai-delivery-maturity-model
drift nobody saw, so the score is a count => drift nobody saw. So the score is a count
the context file up to date, an afternoon, then re-run its test. => the context file up to date (an afternoon), then re-run its test.
ai-dlc-for-forward-deployed-engineers
each consequential action, money, identity, customer => each consequential action: money, identity, customer
Record who answered what, the customer's decisions => Record who answered what: the customer's decisions
tool signature with tests: but you do not choose => tool signature with tests, but you do not choose
eone else's organisation**: in their data, stack => eone else's organisation**, in their data, stack
in that customer's systems, scoping the real problem => in that customer's systems: scoping the real problem
what FDEs keep rebuilding, the MCP server => what FDEs keep rebuilding: the MCP server
ai-dlc-vs-aidd-vs-agentic-sdlc
question that sorts them, is AI building the softwa => question that sorts them: is AI building the softwa
| A seven-phase lifecycle, foundation, inception => | A seven-phase lifecycle: foundation, inception
| Depends on the author, check which one they mean => | Depends on the author: check which one they mean
building with AI tools, context files, story files, coding agents, review | => building with AI tools (context files, story files, coding agents, review) |
**daily habits**: why the agent keeps ignoring conventions → AIDD's => **daily habits** (why the agent keeps ignoring conventions) → AIDD's
is the everyday craft, check which one people mean. => is the everyday craft. Check which one people mean.
[AIDDLC. AI-Driven Development Lif => [AIDDLC: AI-Driven Development Lif
ai-drift-monitoring
the agent's decisions, its output mix, weekly, against => the agent's decisions (its output mix) weekly, against
ai-governance-gates
two-number report is read: the decisions move => two-number report is read; the decisions move
product manager owns release, is it safe to show a few real users?: on the evidence => product manager owns release (is it safe to show a few real users?) on the evidence
ai-guardrails-that-hold
the authority budget is set, every cap decided there => the authority budget is set: every cap decided there
sentence in the prompt too, it helps the agent behave => sentence in the prompt too: it helps the agent behave
that proves it refuses, run the injection suite => that proves it refuses. Run the injection suite
ai-incident-postmortem
rather than less likely, a cap as a typed parameter ... approval can create, and write the test => rather than less likely (a cap as a typed parameter ... approval can create) and write the test
one autonomy level, refunds from acting alone to needing an approver, and write the evidence => one autonomy level (refunds from acting alone to needing an approver) and write the evidence
built from the incident, SkyWays added six, an **amended => built from the incident (SkyWays added six), an **amended
**Only (3)**: and only once the cap is => **Only (3)**, and only once the cap is
A fix closes the path, a limit in the tool's sig => A fix closes the path: a limit in the tool's sig
ai-product-manager-interview-questions
Big-tech PM loops, Google's is the best known, are commonly => Big-tech PM loops (Google's is the best known) are commonly
outcome targets, time saved and cost per case, instead. => outcome targets (time saved and cost per case) instead.
four questions, per slice, is it right => four questions, per slice: is it right
weighted decision per slice, quality on your slices => weighted decision per slice: quality on your slices
into the workflow, trust: and the evaluation set => into the workflow, trust, and the evaluation set
the evidence you gathered, the bar, the lower bound, ... the shadow run. => the evidence you gathered (the bar, the lower bound, ... the shadow run).
cannot repeat it, an AI-fit record now ... bound now in every report. => cannot repeat it (an AI-fit record now ... bound now in every report).
the FDPM's core call, configuration, service or => the FDPM's core call: configuration, service or
may be one need, for example, an approval step before => may be one need, such as an approval step before
| **Compare**. Google does not publish => | **Compare**: Google does not publish
aws-generative-ai-interview-questions
still has to enforce: authority over actions, ... and cost per task. => still has to enforce (authority over actions, ... and cost per task).
autonomy per action, refunds stay with a named appro => autonomy per action. Refunds stay with a named appro
**Also check**: the right client: => **Also check** the right client:
aged service does not give, custom ranking => aged service does not give: custom ranking
profiles route more widely, a data-residency decision => profiles route more widely. It is a data-residency decision
no lens decides for you, the bar per slice and authority per action, is the senior answer => no lens decides for you (the bar per slice and authority per action) is the senior answer
bolts-vs-sprints
how the ceremonies change, standup, demo, review => how the ceremonies change: standup, demo, review
with no model in it) then the exact code => with no model in it), then the exact code
before the day is spent: not at two in the afterno => before the day is spent, not at two in the afterno
the biggest unknown, whether the pieces connect at all, on day one => the biggest unknown (whether the pieces connect at all) on day one
which uses bolts, cycles of hours or days, in place of sprints => which uses bolts (cycles of hours or days) in place of sprints
that runs end to end, for an agent, typically => that runs end to end: for an agent, typically
cut-delivery-time
set by its slowest step: and once AI writes => set by its slowest step, and once AI writes
about AI shortened that, the structure of the ques => about AI shortened that; the structure of the ques
a 5% canary takes 42 days, the arithmetic, not => a 5% canary takes 42 days: the arithmetic, not
evolution-of-the-pdlc
in sequential phases, requirements, design, cod => in sequential phases: requirements, design, cod
evidence at the gates**: both reappear => evidence at the gates**. Both reappear
a stage to the pipeline, the evaluation harness, and a new member => a stage to the pipeline (the evaluation harness) and a new member
before anything is built, should we build this at all?: and runs until => before anything is built (should we build this at all?) and runs until
forward-deployed-engineer-interview-questions
cases, minutes, money: and who owns the risk => cases, minutes, money, and who owns the risk
for their constraints, private networking, no da => for their constraints: private networking, no da
the customer's lawyers**: never by the model => the customer's lawyers**, never by the model
never autonomous at first, a named approver, caps in the tool signatures, idempotency keys so => never autonomous at first, with a named approver, caps in the tool signatures, and idempotency keys so
evidence it was based on, the records and tool calls, not a paragraph => evidence it was based on (the records and tool calls), not a paragraph
tested asset, an MCP server, a skill, a harness template. => tested asset (an MCP server, a skill, a harness template).
changed a roadmap item, the eval-driven feedback => changed a roadmap item. That is the eval-driven feedback
genai-engineer-interview-questions
the grounding triangle, retrieved, cited, verifie => the grounding triangle: retrieved, cited, verifie
the score is to its bar, the cases needed grow => the score is to its bar: the cases needed grow
to data and operations, every base-model update => to data and operations: every base-model update
the three clocks, model, tool, orchestratio => the three clocks: model, tool, orchestratio
fewer turns: route known paths => fewer turns; route known paths
the orchestration clock, turns multiplied by round trips, is the one => the orchestration clock (turns multiplied by round trips) is the one
plan the fallback, a fallback to a larger => plan the fallback: a fallback to a larger
the model can be tricked, it can, but what is the worst => the model can be tricked (it can) but what is the worst
how-accurate-must-an-ai-agent-be
Damage is not always money, a wrongly refused benefit => Damage is not always money: a wrongly refused benefit
instrument, not friction: and why a bar above => instrument, not friction, and why a bar above
put a hold on credits, a person approves any credit above a threshold, and re-derive => put a hold on credits (a person approves any credit above a threshold) and re-derive
the bar from 98% to 71%: which is often => the bar from 98% to 71%, which is often
how-much-process-does-a-change-need
refund cap is tiny and deep, money leaves => refund cap is tiny and deep: money leaves
report is large and shallow, nothing it touches => report is large and shallow: nothing it touches
**(a) Shallow**: reversible, harmless => **(a) Shallow.** Reversible, harmless
with a named approver**: it is one line => with a named approver.** It is one line
**(c) Deep**: money, several teams => **(c) Deep.** Money, several teams
how-this-tutorial-works
than from words alone, the **multimedia principle**, provided => than from words alone (the **multimedia principle**), provided
who are new to it, the **segmenting principle**, and cutting => who are new to it (the **segmenting principle**), and cutting
than reading it again, the **testing effect**, and the benefit => than reading it again (the **testing effect**), and the benefit
as plain markdown, add `index.md` to its address, for tools => as plain markdown (add `index.md` to its address) for tools
how-to-answer-ai-interview-questions
Each has a different fix, retrieval (chunking => Each has a different fix: retrieval (chunking
state your assumptions**: out loud, as numbers => state your assumptions**, out loud, as numbers
some are failures, the same number with oppo => some are failures: the same number with oppo
how you would find out, what you would measure => how you would find out: what you would measure
measure-ai-productivity
organisation stayed flat, more changes were produce => organisation stayed flat: more changes were produce
where value lands, merged and released => where value lands: merged and released
review time up 0.8 hours: with the reason => review time up 0.8 hours, with the reason
cycle two on the trend, review hours falling => cycle two on the trend: review hours falling
one-lifecycle-for-every-method
artefact agents build from: whether your tool calls => artefact agents build from, whether your tool calls
p0-frame
brings the evidence, requirements from the peo => brings the evidence: requirements from the peo
that rule designs out: and DevOps sets up => that rule designs out. DevOps sets up
a cash refund cannot) so the verdict => a cash refund cannot), so the verdict
costs to **run**, the tokens, and what it costs to **ch => costs to **run** (the tokens) and what it costs to **ch
hand-off is **soft**, a missing number => hand-off is **soft**: a missing number
occasionally wrongly: fluently, with no error. The volume => occasionally wrongly (fluently, with no error). The volume
minus the review load, the share of cases a person ... each check takes. Most => minus the review load (the share of cases a person ... each check takes). Most
p1-design-and-spec
must be exact and small, one screen. => must be exact and small: one screen.
change, touch or commit, a cheap task => change, touch or commit: a cheap task
the golden set now, fifty real cases => the golden set now: fifty real cases
function and one checker, zero hand-offs => function and one checker: zero hand-offs
is genuinely sensitive, where changing it would change a quality target, and have each record => is genuinely sensitive (where changing it would change a quality target) and have each record
because 80% sounds right, each is a sentence => because 80% sounds right: each is a sentence
what a right one saves, refunds and simple questi => what a right one saves: refunds and simple questi
p2-build-and-prove
and a slice tag, fifty to start, five hundred to => and a slice tag. Fifty to start, five hundred to
make it **independent**, a different model => make it **independent**: a different model
was proven before, the lower bound of 86% on 500 cases is about 83%, and now it is not => was proven before (the lower bound of 86% on 500 cases is about 83%) and now it is not
environment on day one, their authentication => environment on day one: their authentication
(1927). *JASA* 22: worked in [Formulas] => (1927). *JASA* 22. Worked in [Formulas]
p3-run-and-learn
a condition, never a date: and the arithmetic => a condition, never a date, and the arithmetic
Watch the **output mix**, the share of each kind of decision, because => Watch the **output mix** (the share of each kind of decision), because
The programme continued: not because the numbers => The programme continued, not because the numbers
widen by arithmetic, days of evidence per share, never by date. => widen by arithmetic (days of evidence per share), never by date.
prove-ai-accuracy
and a slice tag, **fifty to start => and a slice tag: **fifty to start
review-ai-generated-code
**count the escapes**, defects that reach production through it, every week. => **count the escapes** (defects that reach production through it) every week.
8 slots ÷ 4 = 2 days** the three read-only => 8 slots ÷ 4 = 2 days.** The three read-only
enforced by a path rule, two readers on money => enforced by a path rule: two readers on money
rolling-out-agentic-delivery
the artefacts being reused, the second spec takes => the artefacts being reused: the second spec takes
| Approvals, not gates, clicks without evidence | => | Approvals, not gates: clicks without evidence |
≈ 1,475 cases, at twelve a day => ≈ 1,475 cases: at twelve a day
shadow-mode-and-cutover
(rebook, refund, message) each with four states => (rebook, refund, message), each with four states
cleared its threshold, 96% agreement over fourteen days against a 95% default, and inside it => cleared its threshold (96% agreement over fourteen days against a 95% default) and inside it
the evidence that earned it: never a date. => the evidence that earned it, never a date.
stay gated regardless, 30 cases prove nothing => stay gated regardless: 30 cases prove nothing
skyways-case-study
adds one constraint, every refund over $400 => adds one constraint: every refund over $400
and a third scheduled, one per sensitivity point => and a third scheduled: one per sensitivity point
a cap in code) which is the practical => a cap in code), which is the practical
nobody is waiting on, no downstream person => nobody is waiting on: no downstream person
across the whole lifecycle) so nobody downstream => across the whole lifecycle), so nobody downstream
team-structure-for-agentic-ai
rather than opinion**: a slice whose lower bound => rather than opinion**. A slice whose lower bound
is not which assistant, teams can choose their own editor, but that every model call => is not which assistant (teams can choose their own editor) but that every model call
that builds it. Conway's law. => that builds it: Conway's law.
none disappears**: two boundaries move: => none disappears**, and two boundaries move:
if it enables and provides, coaching the method and running the shared platform, rather than => if it enables and provides (coaching the method and running the shared platform) rather than
| **Adapted**. Team Topologies' enabling => | **Adapted**: Team Topologies' enabling
the-eight-loops
point at the change, not a discussion => point at the change: not a discussion
write a name, a person, not a team. => write a name: a person, not a team.
together every cycle**: the saving and the spend. It is => together every cycle** (the saving and the spend). It is
a project into a practice, the first time a bill => a project into a practice: the first time a bill
to several roles at once, the architect's authority => to several roles at once: the architect's authority
and a test, the diff, for whether it did. => and a test (the diff) for whether it did.
the-evidence-pack
start properly without it, the test is not whether => start properly without it: the test is not whether
is written only, it lives in a prompt => is written only: it lives in a prompt
have to invent it, thirty across four hand-o => have to invent it: thirty across four hand-o
the-hard-gate
The rest, SkyWays had eight, run beside the build. => The rest (SkyWays had eight) run beside the build.
of every soft decision, some turn hard as => of every soft decision: some turn hard as
that is hard to reverse) so everything downstream => that is hard to reverse), so everything downstream
jointly own the plan gate, the bolt cut => jointly own the plan gate: the bolt cut
what-is-a-forward-deployed-engineer
chosen for provability, high volume, low damage => chosen for provability: high volume, low damage
what-is-ai-dlc
the breadth of a task, which stages to include, and the depth => the breadth of a task (which stages to include) and the depth
what-is-aidd
testing and fixing, coding agents such as Cla => testing and fixing: coding agents such as Cla
a fare in a prompt, *never compute money in a prompt; call the function*, and once after => a fare in a prompt (*never compute money in a prompt; call the function*) and once after
discarded the cache, *one model per task*. => discarded the cache (*one model per task*).
were **20% faster**: a result its authors => were **20% faster**, a result its authors
under conventions, *use the new logging library ... version 3*, and, if it keeps => under conventions (*use the new logging library ... version 3*) and, if it keeps
repository in week one, context file, story files => repository in week one: context file, story files
what-is-spec-driven-development
writing code with AI, documentation first, and treating that spec => writing code with AI (documentation first) and treating that spec
criteria in **EARS**, *WHEN … THE SYSTEM SHALL …*, the requirements syntax => criteria in **EARS** (*WHEN … THE SYSTEM SHALL …*), the requirements syntax
fallback and the records) and they belong => fallback and the records), and they belong
what-is-the-agentic-pdlc
does part of the work, drafts the reply => does part of the work: drafts the reply
needs a model at all, many do not, and sets how much => needs a model at all (many do not) and sets how much
does not end in a ticket, it ends in a brief => does not end in a ticket; it ends in a brief
instead of a rewrite, a one-way door => instead of a rewrite: a one-way door
is a known anti-pattern, fixing the model's knobs => is a known anti-pattern: fixing the model's knobs
what-is-the-bmad-method
leaves a paper trail, excellent for audited => leaves a paper trail: excellent for audited
self-contained stories, BMAD calls the pieces *shards*, each carrying => self-contained stories (BMAD calls the pieces *shards*), each carrying
and implementation) while its current documen => and implementation), while its current documen
on agile team roles, typically an analyst, ... a developer and QA, each with => on agile team roles (typically an analyst, ... a developer and QA), each with
why-agentic-ai-projects-fail
a confident wrong answer) so a failure can run => a confident wrong answer), so a failure can run
numbers are illustrative, the shapes are real. => numbers are illustrative; the shapes are real.
a cost and the evidence, at SkyWays, 240 disrupted passengers => a cost and the evidence. At SkyWays it read: 240 disrupted passengers
is P1's authority budget, every cap a typed paramet => is P1's authority budget: every cap a typed paramet
to 77% against a bar of 80, the easy, high-volume cas => to 77% against a bar of 80: the easy, high-volume cas
There was no runaway: four ordinary habits => There was no runaway. Four ordinary habits

1f. Leftover dashes replaced (not sweep damage, but the rule is no dashes anywhere)
Lessons, about 40 spans, mostly inside fenced prompt blocks the sweep had skipped. Typical: "Here is our spec — requirements, design and tasks: <paste>" => "Here is our spec (requirements, design and tasks): <paste>"; "R1–R5" => "R1 to R5"; "R4–R5 paths" => "R4 and R5 paths"; one-lifecycle-for-every-method table cells "| — |" => "| none |" (5 cells); "build to measure to learn" (sweep output) => "build-measure-learn"; "machine to human" => "machine-human".
Role templates, 13 cells: bolt log and plan "| — |" => "none"; QA table "—" => "n/a"; architect depth table "—" => "skip" (and the prompt's allowed values now read "full · yes · light · skip"); NFR table => "none"; gate table => "n/a | n/a | n/a | **HARD** | none".
Result: zero em or en dashes in all 55 lessons, start-here.md, curriculum.py, site/content/library and the role JSON. The only three left in my area are in code: two print strings in site/content/roles/_src/build_content.py and one comment in enrich.py. I left code alone.

1g. Looked at and judged fine
- 342 comma and colon sites in lessons where the sweep's choice reads naturally (appositive commas, label colons, "comma + and/which" joins). Skimmed again as a list after editing.
- Comma splices that predate the sweep (the author's own style) were left.
- site/pages/figures.py not opened for editing, as instructed.

====================================================================
2. JOB 2: NAMES, GROUPED BY NAME
====================================================================

2a. "simulator" that means the workbench => "workbench"
Rule I applied: any `sim:#/...` link and any `.../simulator/#/...` deep link is the workbench (the game only forwards those routes).
- Lessons: "[The simulator](sim:#/)" => "[The workbench](sim:#/)" in 14 lessons: agentic-delivery-simulator, agentic-pdlc-for-business-sponsors, agentic-pdlc-for-program-managers, ai-delivery-maturity-model, ai-drift-monitoring, ai-incident-postmortem, how-to-run-an-agentic-ai-project, measure-ai-productivity, p1-design-and-spec, p2-build-and-prove, the-hard-gate, what-is-aidd, what-is-the-agentic-pdlc, why-agentic-ai-projects-fail.
- agentic-delivery-simulator.md: this lesson describes the workbench (13 episodes, 9 simulations, 17 tools; all its links are sim:#/...). I renamed it in words throughout: title "Agentic AI Simulator: Practise 90 Days of Delivery Decisions" => "Agentic AI Workbench: ...", short "The simulator" => "The workbench", description, dek, body, three FAQ headings, image alt text. Slug, wiki key, {{map:...}} key and keywords line untouched. This is a retitle of a search-facing lesson, so it wants the owner's yes.
- agentic-pdlc-exercises.md: "The simulator's toolkit has a calculator" and "the simulator's calculator" => "workbench's" (2).
- ai-guardrails-that-hold.md: "[Try the injection simulator](sim:#/toolkit/inject)" => "[Try the injection test builder](sim:#/toolkit/inject)" (the tool's own name in the workbench).
- skyways-case-study.md: four "simulator" => "workbench" (calculators, "runs the same ninety days", the FAQ answer, the closing line).
- how-this-tutorial-works.md: "The lessons, the playbook and the simulator are free" => "The lessons, the manual, the simulator and the workbench are free".
- curriculum.py: "the simulator, and twelve exercises" => "the workbench, and twelve exercises"; promise "A case, a simulator, twelve problems" => "A case, a workbench, twelve problems".
- Roles: devops reads label "The gateway control, in the simulator" => "...in the workbench"; solution-architect reads label "The same case, step by step, in the simulator" => "...in the workbench".
- Wiki: Formulas-and-Calculators.md "[simulator] (.../simulator/#/episode/bill)" => "[workbench] (...)".
- Every link target containing workbench/ or #/ in site/content/** and wiki/*.md was checked. Words now match in all of them; the targets that are themselves stale are listed in section 4.

2b. "playbook"
- As the site => "manual": lessons 112 spans ("this playbook" 85, "this playbook's" 15, "the playbook's" 12 => "this manual", "this manual's"); start-here.md 2; frameworks.json 8 ("this playbook", "The phase names are the playbook's." and four like it, "The playbook's construction." x2); devops role 2 ("this playbook's default" => "this manual's default").
- Wiki, as the site => "manual": Decision-Trees (2), Exercises-and-Answers (2), Field-Notes (2), Formulas-and-Calculators (2), How-to-Run-a-Missing-Control-Postmortem (2), Role-Sponsor (1), Sources-and-Confidence (4), The-Agentic-PDLC (4), The-Eight-Loops (4), Where-do-I-find-it (3), Playbook-Glossary (4; H1 now "# The manual's glossary"), Home (4: "[SkyWays, the agentic manual]" x2, "The manual on the wiki", "the manual live"), Maintainer-Runbook heading "## The site: SkyWays, the agentic manual", README (2), Roadmap "The manual's contact form", Study-Plans "[live manual]", Scenario-Library (1).
- Wiki, as the tool => "workbench": Cohort-Kit (4), Cohort-Session-Template (4), Cohort-Session-1 (1), -2 (1), -4 (1), -6 (1), -7 (1), -8 (2), Home "lesson and workbench tool", README "lesson and workbench tool", Roadmap (3), Playbook-Glossary "The workbench teaches **55 concepts**".
- Wiki, as the set of method pages => "method": Home "[The method pages]", README "method set" and "method pages" (3), _Sidebar "**The method**", Scenario-Library "the same method applied to healthcare", "let the method lose sometimes".
- Link text "[Playbook Glossary]" => "[Glossary]" (The-Agentic-PDLC, Sources-and-Confidence, Where-do-I-find-it, _Sidebar). Target unchanged.
- _Sidebar.md: "[🛫 The SkyWays playbook] (.../simulator/)" => "[🛫 Ninety Days, the simulator] (.../simulator/)" plus one NEW line "[🧰 The workbench] (.../workbench/)". The added line is the one place I added a link; drop it if unwanted.
- Roadmap.md: "[playbook] (.../simulator/)" => "[simulator] (...)" (words now match the target, which is the game).
- Kept: how-to-run-an-agentic-ai-project title "A Step-by-Step Playbook" and lead "The playbook in short." (the generic noun for that lesson's own steps); shadow-mode "A standard cut-over playbook"; agentic-delivery-simulator "Three playbooks (...)" (role playbooks inside the workbench) and its keywords line.

2c. "spine"
- Changed: frameworks.json "The P0 to P3 spine" => "The four phases, P0 to P3"; curriculum.py promise "The spine, phase by phase" => "The lifecycle, phase by phase"; what-is-the-agentic-pdlc link text "[The named methods on one spine]" => "...on one lifecycle"; Cohort-Session-1 "the spine picture" x2 => "the four-phases picture", "[Four methods, one spine]" => "[Four methods, one lifecycle]" (also Session-4); Cohort-Session-4 "on the spine" x4 => "on the four phases", "The spine is the anchor ... placed on it." => "The four phases are the anchor ... placed on them."; The-Agentic-PDLC intro "This is the spine every other page on this wiki hangs from" => "Every other page on this wiki hangs from them", "The same eight on a spine" => "on one line", "the same spine" => "the same lifecycle"; Playbook-Glossary "The spine" => "The four phases of the SkyWays PDLC".
- Kept as plain metaphor: what-is-the-agentic-pdlc.md "The agentic PDLC is a spine, not a rival method", key takeaway 3, and "Make the phases the roadmap's spine"; wiki/The-Evidence-Pack.md:483 "the real spine rather than a leaf" (about code).
- Kept because it is a link target: the anchor #how-the-named-methods-sit-on-the-spine in six lessons and The-Agentic-PDLC.md, and the heading that makes it (see section 4).

2d. "hard gate" joined to "sign-off"
- Lessons: kept as is.
- Joined once at first use where the page never said sign-off: Cohort-Session-1 "the one hard gate (the sign-off before anything is built)"; Cohort-Session-2 "the one hard gate: the sign-off that decides..."; Home.md "one hard gate (the sign-off before anything is built)"; The-Agentic-PDLC.md "is a hard gate (the sign-off before anything is built)"; Study-Plans.md "The table for the P1 → P2 hard gate (the sign-off before anything is built)"; Playbook-Glossary.md, added one sentence to the hard-gate entry: "The one hard hand-off, P1 → P2, is the sign-off before anything is built."
- Not joined, on purpose: frameworks.json "Hard and soft gates", the PM and architect role content, and wiki pages where "hard gate" is the general class of gate and not the P1 to P2 sign-off (Anti-Patterns, Decision-Trees, Gates-and-Governance, How-to-*, The-Eight-Loops, Cohort-Session-4 and -7). The /frameworks/ page join already exists in render.py.

2e. "AiDD" => "AIDD"
Verified: no "AiDD" anywhere in site/content or wiki. Nothing to change.

====================================================================
3. JOB 3: LESSON SUMMARIES
====================================================================

- 55 lessons. 44 had a single-sentence summary over 30 words: all 44 rewritten. 10 more already had two or three sentences but one of them ran 42 to 71 words; I split those too. 1 left alone (how-this-tutorial-works: two sentences, 40 and 20 words). Total rewritten: 54.
- Same facts and numbers; only joining words changed ("They are", "So", "Then"). In two summaries a list of "whether" clauses became direct questions (forward-deployed-engineer-interview-questions, how-much-process-does-a-change-need).
- Honest count of the result: 3 summaries have 2 sentences, 23 have 3, 16 have 4, 9 have 5, 4 have 6 to 8 (the ones that are a list of questions or items). So about half are over the "two or three" target, because a list of five named things reads better as short sentences than as one long one. Longest remaining sentence is 37 words (the five governance gates with their bracketed questions); seven others sit at 32 to 35.

Three examples:
1. ai-agent-costs. BEFORE (65 words, one sentence): "An AI agent's bill usually grows because four ordinary habits **multiply**: more context sent per call, a larger share on the expensive model, a cache that stops hitting, and more attempts per case, so read the per-call log rather than the price list, confirm the four ratios multiply to the invoice ratio, and fix them in order of **(factor − 1) ÷ days to fix**." AFTER (33, 20, 13): "An AI agent's bill usually grows because four ordinary habits **multiply**: more context sent per call, a larger share on the expensive model, a cache that stops hitting, and more attempts per case. So read the per-call log rather than the price list, and confirm the four ratios multiply to the invoice ratio. Then fix them in order of **(factor − 1) ÷ days to fix**."
2. prove-ai-accuracy. BEFORE (61): "A score on a test set proves an AI agent meets its bar only when the **lower bound** of the score, the bottom of its 95% confidence interval, clears the bar, so report every slice as a score, a sample size and a lower bound, with a verdict of proven, not yet (and how many more cases it owes), or failed." AFTER (31, 14, 16): "A score on a test set proves an AI agent meets its bar only when the **lower bound** of the score (the bottom of its 95% confidence interval) clears the bar. So report every slice as a score, a sample size and a lower bound. Give each a verdict: proven, not yet (and how many more cases it owes), or failed."
3. the-hard-gate. BEFORE (54): "Of the four hand-offs in the agentic PDLC only P1 → P2 halts the build, because the spec, the acceptance bar per slice and the authority budget are what everything downstream is built and measured against, every other open decision runs alongside the build behind a placeholder, with a named owner and a date." AFTER (15, 20, 18): "Of the four hand-offs in the agentic PDLC only P1 → P2 halts the build. The spec, the acceptance bar per slice and the authority budget are what everything downstream is built and measured against. Every other open decision runs alongside the build behind a placeholder, with a named owner and a date."

The label:
- The box label in site/pages/learn.py:448 is already "In short" (ALERT_LABEL), so it needs no change.
- The words "in one sentence" were a bold lead inside each lesson's own summary ("**The answer in one sentence.**"). That is lesson content, so I changed all 52 of them to "... in short." (three lessons already said "The short version." or "The short answer."). No lesson summary says "one sentence" now.
- Side effect to decide: the box now reads "In short" (label) and then "**The answer in short.**" (lead). It repeats. Either is easy to drop; I did not touch learn.py.
- learn.py still says "one sentence" in the tour text (section 4, item 2).

====================================================================
4. FIXES THAT BELONG IN FILES I COULD NOT TOUCH
====================================================================

1. site/render.py:644. `<b>Start with</b><span>{md(first_do)}.</span>` appends a full stop to an activity name. Replace with: add the stop only when the text does not already end in . ? or !, e.g. `{md(first_do)}{'' if first_do.rstrip()[-1:] in '.?!' else '.'}`. (I worked around it in the PM content, but any future activity ending in "?" will print "?." again.)
2. site/pages/learn.py:857. "the answer in one sentence, a picture" => "the answer in a few short sentences, a picture". Line 858: "The green box is the whole lesson in one sentence." => "The green box is the whole lesson in short."
3. site/pages/mapspecs.py:509. title `("The playbook", "n")` => `("The workbench", "n")`. Line 514: alt "...practising with the SkyWays playbook..." => "...the SkyWays workbench...". (This is the map for the agentic-delivery-simulator lesson.)
4. site/wiki_export.py:173 writes "—" cells into the Journey pages (3 remain in wiki/Journey-*.md). Replace the literal with "none".
5. site/content/learn/README.md (not in my list). Lines 16 to 18, sweep damage: "five shapes: `bands` ... or `fan` (one question, its outcomes): with a callout that says" => "... or `fan` (one question, its outcomes). Each has a callout that says". Line 39: "**<Term> in one sentence.** The answer, 40–70 words, first." => "**<Term> in short.** The answer first, in two or three short sentences." Lines 74, 78, 134: "playbook" => "manual". Lines 94, 130, 131, 134: "the simulator" => "the workbench". 13 dashes remain in the file. site/content/SCHEMA.md has 10 dashes.
6. Link targets I was told not to change:
   - Role "reads" targets still point at ../simulator/#/... (5, in site/content/roles/_src/product_manager_a.py:46, devops_a.py:58, engineering_a.py:50, qa_a.py:51, solution_architect_a.py:54). They work only through the game's redirect. Should be ../workbench/#/...
   - 91 wiki deep links of the form .../simulator/#/... (same redirect; should be .../workbench/#/...).
   - wiki/Cohort-Kit.md:15 and wiki/Cohort-Session-Template.md:60: the words now say "workbench" but the target is the bare .../simulator/ (the game). Target should be .../workbench/.
   - Lessons never link to the game (there is no bare `sim:` link). If the game should be reachable from lessons, the natural places are skyways-case-study ("Rehearse it first") and the "Go deeper" line of what-is-the-agentic-pdlc.
7. Old names fixed in identity, not just words: the wiki page file name Playbook-Glossary.md, and the heading "How the named methods sit on the spine" in wiki/The-Agentic-PDLC.md (anchor used by six lessons). Renaming either means changing link targets everywhere at once.
8. Generated wiki pages still carry old text until you regenerate them: Tutorial-* (e.g. "A case, a simulator, twelve problems", "The spine, phase by phase", all the old summaries), Start-Here, Module-*, Mental-Models, and the tutorial and course blocks inside Home.md and _Sidebar.md. Run site/learn_export.py (and export_models.py) after this lands.
9. Hand-written wiki pages were never swept: about 1,690 em and en dashes remain there. I added none and removed only the ones on lines I was editing anyway.
10. site/pages/figures.py: not touched, not reviewed.

====================================================================
5. CHECKS RUN (all after the last edit)
====================================================================

- python3 site/content/roles/_src/build_content.py, then shasum of site/content/roles/*.json before and after: identical. Last lines:
  "devops.json — 8 steps, 53 activities, 24 prompts, 8 templates, 1 figures, 2 calculators (103,050 bytes)"
  "REPRODUCED: role JSON unchanged after regenerating from sources" (my own echo after the diff came back empty)
- python3 site/build.py --out <SP>/r7/contentsite: exit 0, no warnings. First line: "built .../scratchpad/r7/contentsite — 502 files, 38.5 MB". Last lines:
  "learn:  121 files (lessons, tracks, markdown twins, llms.txt)"
  "tool:   app/SkyWays-Architect.html (pristine) + workbench/index.html (framed)"
  "game:   simulator/index.html + play/"
  "files:  stylesheets and scripts carry a content version in 79 pages"
- python3 wiki/check.py --strict: "82 pages · 28,685 lines · 129 templates · 175 prompts · 0 diagrams" then "no problems".
- Forbidden strings (home-directory paths, 12-digit numbers other than 123456789012, the client name the workflow forbids) in the 1,587 lines I added under site/content and wiki: 0.
- Em/en dashes in lessons, start-here.md, curriculum.py, site/content/library, role JSON: 0 (3 remain in role generator code, see 1f).
- Built pages spot-checked earlier in the run: no "judgement call?.", no "**Pain** (", no "Try it in the simulator", no punctuation-only cells on /frameworks/.

Things that want the owner's eye, in one place:
1. The five "From" cells in frameworks.json (my words, especially BMAD => "BMad Code").
2. The retitle of the agentic-delivery-simulator lesson to "Agentic AI Workbench: ..." (slug unchanged).
3. The new "[🧰 The workbench]" line in wiki/_Sidebar.md.
4. "In short" label above leads that now also say "in short".
5. About half the summaries run to four or more short sentences.
6. Role template cells that held a dash now say "none", "n/a" or "skip".