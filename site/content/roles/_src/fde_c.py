"""Forward-deployed engineer · Evolve the relationship, steps 9 to 12. Imported by build_content.py.

Evolve asks the manual's four questions about the relationship: what comes next here (P0), what goes
back to the product (P1), whether the reusable version works next time (P2), and whether the
relationship is healthy (P3). It ends with the next frame, or a clean close, signed by the client's
sponsor.

The case after day 97, when Lena signed the handover and your access ended, is illustrative and
agrees with the canon: the day-82 refund, the fourteen shadow disagreements and their evening rule,
the four partner queries in one call, and day 90's line (40 to 45 percent fewer person-days, a
$4,200 token bill, 96 review hours with under 30 promised for the next cycle). New here, and nowhere
else: the partner's winter hours, the cargo team's damaged-baggage claims, the partner lookup's
three copies (nine, six and five days) and its connector (two days at cargo), and day 180's review.

Marks: {{id}} puts a recorded quotation from fde_sources.py on the page, [[id]] cites a source.
Neither goes in a title, question, say, template or prompt.
"""

STEPS_C = [
{
 "n": 9, "id": "reframe", "phase": "Reframe", "stage": "evolve", "level": None,
 "hats": ["product", "consultant"],
 "question": "What should come next, here?",
 "title": "Turn what the running system taught into the next frame",
 "when": "Evolve, in the month after handover, then whenever a new ask arrives",
 "purpose": (
   "A system that works attracts asks. Within weeks of the handover every team that watched the "
   "shadow wants one, and the next engagement gets chosen by whoever asks loudest, or most senior. "
   "Choose it from evidence instead: what the first month in production taught, read with the "
   "person who now runs it, and every new ask put through the questions that qualified the first "
   "engagement. The answer is one recommended frame, and a no in writing for the rest. Anthropic "
   "asks its FDEs to {{S6-relationships}}. Find them in the evidence, and take only the ones it "
   "qualifies."),
 "activities": [
   {"do": "Read the first month with their operator, on their screen",
    "detail": "Your access ended at the handover, as it should: it is their system now, and you are "
              "on call to its operator, not to it. A month on, go through the incidents, the near "
              "misses, the drift readout, the two numbers and the override log together, then keep "
              "that hour every month. Every case the desk corrects by hand is an incident nobody "
              "filed."},
   {"do": "Turn each incident and near miss into a brief that ends in a control",
    "detail": "Pain, evidence, the enforced control that was missing, the fix and where it now lives, "
              "in the shape the [product manager's step 8](../../product-manager/#learn) uses. Never "
              "a person. Each control becomes a rule the next frame starts with, written down before "
              "it starts."},
   {"do": "Write down every ask, in the asker's words",
    "detail": "Asks arrive in corridors and in emails to your sponsor. Record who asked, the pain as "
              "they put it, and the last time it hurt. An ask you did not write down gets answered "
              "by someone else, and the answer carries your name."},
   {"do": "Qualify each ask with step 1's questions",
    "detail": "As [step 1](../frame/#qualify) does: a week of their tickets, enough to qualify and "
              "not to size. A genuine judgement call, the volume to carry evaluation, and, action by "
              "action, whether a wrong answer can be undone. Then the three disqualifiers: no path "
              "for their data to a model inside their policy and region, no one who can sign the "
              "risk, no one to run it after you. Most asks fail one, and the brief says which."},
   {"do": "Rank by value and by reuse, then ask who would run it",
    "detail": "Value is the volume times what a case costs today, read against what their sponsor "
              "is measured on this year. Reuse is how much of the first system carries over: "
              "connectors, the golden set's shape, the authority budget, the harness, the runbooks. "
              "A frame that lands on the operator still learning the first system breaks both, so "
              "name who would run the new one."},
   {"do": "Put every no in writing, as their sponsor's decision",
    "detail": "A no said in a corridor comes back next month as a yes somebody else gave. Write each "
              "one in the brief with its reason and the condition that would turn it into a yes, and "
              "let the asker hear it as their sponsor's ranking, not as your gate. At a vendor a yes "
              "is a new contract too, so your account lead sees the brief before their sponsor does."},
 ],
 "internal": (
   "Inside your company the asks arrive from every business unit at once, often through your own "
   "management chain. Keep one ranked list, owned by the platform's sponsor and open to every "
   "asker, so the ranking is theirs and you are not the referee. A no to a peer's team then comes "
   "from the list and its reasons, never from you in passing."),
 "say": [
   {"to": "A senior leader whose ask did not make the list",
    "words": "Your ask is on the list, and here is why it is not first: there is no way to read the "
             "rostering data yet. When there is, it moves up, and you will hear it from me first."},
   {"to": "Their operator, on the first month's evidence",
    "words": "Show me what your team corrects by hand. Every correction is an incident nobody filed, "
             "and it is the best evidence we have about what to build next."},
   {"to": "Their operator, asking you for one small change",
    "words": "It is your system now, so it goes on your team's backlog. I will pair with your "
             "engineer for an hour, and the change is theirs to make and to keep."},
 ],
 "ai": [
   {"tool": "Chat model, as their analyst",
    "use": "In a tool their policy approves, give it the month's incident notes, the drift readout "
           "and the override log, redacted, and ask for every pattern in them, each with its count, "
           "an example and the hour it happens.",
    "caution": "It ranks what is frequent, not what is dangerous. One near miss on a payment outweighs "
               "a hundred cosmetic overrides, and only you and their operator can say which is which."},
   {"tool": "Chat model, as the sceptic",
    "use": "Paste the ranked asks and have it argue for the one you ranked last and against the one "
           "you ranked first. If its case for the last one holds, your ranking was about who asked.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The ranking, and every no. A model ranks the text you pasted; it cannot weigh who will run "
           "the system, which sponsor will defend it, or what a no costs the relationship.",
    "caution": None},
 ],
 "artifact": {
   "name": "Next-frame brief",
   "short": "Next-frame brief",
   "good": "Two pages. The month's evidence, each incident as a brief that ends in a control, every "
           "ask qualified with its numbers, one ranked list, one recommended frame with the rules it "
           "starts with, and a written no, with its condition, for each of the rest.",
   "owner": "Forward-deployed engineer, with their operator; their sponsor decides"},
 "template": {
   "title": "Next-frame brief", "lang": "markdown",
   "body": """# Next-frame brief · <customer> · <system> · <date>
_Drafted by <FDE> with <their operator> · For <their sponsor> · Covers <dates since handover>_

## 1. What the running system taught
| Evidence | Source, dates | What it says |
|----------|---------------|--------------|
| The two numbers | <report> | <the saving beside the spend> |
| Drift | <readout> | <the output mix against its thresholds> |
| Overrides and corrections by hand | <their log> | <count, the commonest kind, when> |
| Open risks | <their risk log> | <what is still not controlled, and its owner> |

## 2. Incidents and near misses, each ending in a control
| # | What happened | The enforced control that was missing | Where it lives now | Rule for the next frame |
|---|---------------|---------------------------------------|--------------------|-------------------------|
| 1 | <...> | <a control, never a person> | <tool, parameter, test> | <...> |

## 3. The asks, qualified
| Team | The ask, in their words | Pain, measured | Per day | Judgement call · volume · can be undone | Disqualifier | Reuses |
|------|-------------------------|----------------|---------|-----------------------------------------|--------------|--------|
| <team> | <...> | <cost, from which export> | <n> | <yes · yes · partly> | <none, or which> | <what carries over> |

## 4. Ranked
| Rank | Ask | Value | Reuse | Risk | Who would run it, and what they run already |
|------|-----|-------|-------|------|----------------------------------------------|

## 5. Recommended next frame
<the ask> · sponsor <name> · risk owner <name> · operator <name>
**Rules it starts with:** <each control from section 2>

## 6. Not now, in writing
| Ask | Why not | What would change it | Told to, on |
|-----|---------|----------------------|-------------|

**Decision:** <next frame | not yet | none> · <their sponsor> · <date>
"""},
 "prompts": [
   {"title": "Read the first month as their operator would",
    "when": "A month after handover, with the operator's logs",
    "body": """Below is the first month of <system> in production at <customer>, redacted: the
incident notes, the drift readout, the two-number report, and the operator's log of
overrides and corrections made by hand.

1. List every incident and near miss. Count each correction made by hand that nobody
   filed as an incident too, and flag any stretch where corrections were likely made
   but nothing was recorded.
2. For each, write a brief: what happened; the evidence (trace id, date); the ENFORCED
   control that was missing; the fix and where it would live (tool, parameter, test);
   the rule it gives the next piece of work.
3. Then the patterns: the commonest override, and the hour and the team it comes from.

RULES:
- A finding is a control, never a person. Training and a clearer prompt are not
  controls. If that is all you can find, write CONTROL NOT FOUND.
- Order by harm, not by count. One near miss on a payment outranks many cosmetic fixes.
- Quote the evidence. Do not infer an incident the logs do not show.

EVIDENCE:
<paste>"""},
   {"title": "Rank the new asks by value and by reuse",
    "when": "Before you recommend a next frame",
    "body": """These asks arrived after <system> went live, each with the team, the ask in their
words and what I measured: <paste>.

The first system already has: <connectors, the golden set and harness, the authority
budget, runbooks, the shadow and its flags>.

For each ask:
1. The three AI-fit answers: is it a genuine judgement call, is there the volume to
   carry evaluation, and, action by action, can a wrong answer be undone?
2. The three disqualifiers: no path for their data to a model inside their policy and
   region, no one who can sign the risk, no one to run it after you.
3. Value: volume x what a case costs today. Mark every number MEASURED or ASSUMED.
4. Reuse: what carries over from the first system, and what must be built new.
5. Who would run it, and whether they already run something we built.

Rank them. For each ask you do not recommend, write the no in two sentences: the
reason, and what would change it.

Recommend one next frame at most. Do not rank by volume alone, and never by who asked."""},
 ],
 "example": {
   "title": "SkyWays · the month after handover",
   "body": "Your access ended on day 97, and for a fortnight you were on call to Lena, not to the "
           "system. At the month's end you went through it together, on Lena's screen. It held day "
           "82's brief, whose finding was a control: caps live in the tool's signature. It also held "
           "a near miss nobody had filed. The partner behind the shadow's evening rule moved its "
           "transfer desk's close to 17:00 for winter; the rule was a constant set at 18:00, and the "
           "desk overrode three wrong proposals in a week. That became a brief too: the hours come "
           "from the partner's own data, with a test. Four teams that had watched the shadow sent "
           "asks. Your first ranking went by volume and put the loyalty team's points questions on "
           "top; step 1's questions took them off, because a balance lookup needs no judgement. Crew "
           "rostering had no data path, so it went on the not-yet list with its condition. The cargo "
           "team's damaged-baggage claims ranked first on value and reuse: about 30 a day, a payout "
           "nobody can take back, and a partner lookup on every codeshare bag. Ines signed it as the "
           "next frame, which starts again at step 1."},
 "pitfalls": [
   "Ranking by who asked. The most senior ask wins the first meeting and fails the third, when "
   "nobody can be found to run it.",
   "Starting the next frame on the team still learning the first system. Both systems get half an "
   "operator, and the first one's drift goes unwatched.",
   "Leaving the incidents' rules in the last engagement's folder. The next frame starts without "
   "them, and its first cap goes back into a prompt.",
 ],
 "done_when": "Their sponsor can read the brief and say what comes next and why, every asker has an "
              "answer in writing, and each control the first system taught is a rule the next frame "
              "starts with.",
},
{
 "n": 10, "id": "codify", "phase": "Codify", "stage": "evolve", "level": None,
 "hats": ["product"],
 "question": "What comes back to the product?",
 "title": "Write the pattern up for the people who build the product",
 "when": "Evolve, logged from day one and written up in the month after handover",
 "purpose": (
   "Your second customer is your own product team. Solved twice is a pattern; solved three times is "
   "a product gap. Sort each repeat into configuration, a reusable service or a product capability, "
   "write it up with every customer's evidence, and let the product's owner decide. Skip this, and "
   "a product company slowly becomes one that maintains a large bespoke system for every customer, "
   "indefinitely [[S23]]. OpenAI asks its FDEs to {{S1-codify}}."),
 "activities": [
   {"do": "Keep a pattern log from day one",
    "detail": "One line each time you build something you have built before: what, where, how many "
              "days. Without it the third copy looks like the first. What could hurt another customer "
              "this week, such as a cap that lived only in a prompt, goes home the day you find it, "
              "not at handover."},
   {"do": "Sort each repeat, and write down the reason",
    "detail": "**Configuration**: the product already does it, and a customer needed a setting. "
              "**Reusable service**: the same code would serve several customers, owned by your "
              "practice. **Product capability**: every customer will need it, so the product should "
              "own it. The reason is what the product owner will argue with. Scale AI hires "
              "forward-deployed product managers for this judgement: people who {{S19-difference}}."},
   {"do": "Write the request with every customer's evidence, redacted",
    "detail": "The days each copy took, the defects each had, what keeping them cost, and what a "
              "shared version would have prevented. One customer's evidence reads as a feature "
              "request; three customers' reads as a gap. No customer's name, data or terms leaves "
              "its own row."},
   {"do": "Check who owns each copy before you propose a shared one",
    "detail": "Read each statement of work's clause on who owns what you built. Where the customer "
              "owns their copy, the shared version is written fresh from the pattern, never "
              "assembled from their code, and the entry says so."},
   {"do": "Send model gaps to research with the failing cases",
    "detail": "A gap in the model, not in your code, goes to the people who train it: the slice, the "
              "score and its lower bound, ten failing cases labelled by the customer's experts, and "
              "what you tried that did not fix it [[S1]]."},
   {"do": "Hand the decision to its owner, and record it",
    "detail": "The product owner decides, or the forward-deployed product manager where there is "
              "one. In a consultancy the entry goes to the practice's asset library; inside a "
              "company, to the platform's backlog. Record the answer with its condition, *not yet* "
              "included."},
 ],
 "internal": (
   "Inside your company the product team may be the platform team down the corridor, and the pull "
   "is to fix the repeat yourself in their code. Write the entry anyway, with every business unit's "
   "evidence, and let the platform's owner decide. A shared component nobody agreed to own becomes "
   "your team's for good."),
 "say": [
   {"to": "The product owner, asking for a capability",
    "words": "We have built this three times, for three customers. Here is what each copy cost and "
             "what broke. I am not asking for a feature for one of them; I am asking whether the "
             "product should own it, and I will take not yet with a condition."},
   {"to": "A customer asking where their lessons go",
    "words": "What goes home is the pattern, never your data, your code or your terms. The next "
             "customer gets a better product, and so do you, at your next upgrade."},
 ],
 "ai": [
   {"tool": "Coding agent, across your own repositories",
    "use": "Point it at the code your company may keep from past engagements and ask for every "
           "function that does the same job, with a table of how each copy differs.",
    "caution": "Only code your contracts let you keep. A customer's repository you no longer have "
               "the right to read goes into no tool."},
   {"tool": "Chat model, as the product owner",
    "use": "Paste the draft entry and have it refuse the request as a busy product owner would, with "
           "the three questions it needs answered before a yes. Answer them in the entry.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The sort, and what counts as evidence. A model files every repeat as a product capability "
           "because the write-up says it matters. Whether it is configuration, a service or a gap "
           "is a judgement about the product, and its owner will test yours.",
    "caution": None},
 ],
 "artifact": {
   "name": "Pattern entry",
   "short": "Pattern entry",
   "good": "One page: the problem in one sentence, where it occurred, what each copy cost to build "
           "and to keep, the sort with its reason, the evidence, the ask, who decides, and the answer "
           "with its condition. No customer's name or data outside its own row.",
   "owner": "Forward-deployed engineer; the product owner or FDPM decides"},
 "template": {
   "title": "Pattern entry", "lang": "markdown",
   "body": """# Pattern entry · <pattern> · <date>
_Logged by <FDE> · Decides <product owner or FDPM> · Status <proposed | accepted | not yet | refused>_

## 1. The problem, in one sentence
<what keeps having to be built, and for whom>

## 2. Where it occurred
| Customer | When | Built how | Days | Defects since | Who owns the copy |
|----------|------|-----------|------|---------------|-------------------|
| <A, redacted> | <date> | <bespoke, in their repository> | <n> | <n> | <them, under the statement of work> |

## 3. The sort
<Configuration | reusable service | product capability>, because <reason>.

## 4. The evidence
- To build: <days for each copy>
- To keep: <the last change that broke every copy, and what each fix cost>
- What a shared version would have prevented: <...>

## 5. The ask
<what, owned by whom, by when, and the cheapest version that would do>

## 6. Model gaps found on the way
| Slice | Behaviour | Score, lower bound, n | Failing cases | Sent to, on |
|-------|-----------|-----------------------|---------------|-------------|

## 7. The decision
<accepted | not yet, until <condition> | refused, because <reason>> · <who> · <date>
"""},
 "prompts": [
   {"title": "Find every problem I solved twice",
    "when": "At handover, from your pattern log",
    "body": """Here is my pattern log and, from my last <n> engagements, the function signatures
and test results I may keep, customer names removed: <paste>.

Find every problem I solved more than once. For each:
| Problem in one sentence | Engagements | How each copy differs | Days each took | What broke later |

Then sort each into exactly one of:
  CONFIGURATION       the product does it; a customer needed a setting
  REUSABLE SERVICE    the same code would serve several customers
  PRODUCT CAPABILITY  every customer will need it, and the product should own it
with the reason in one line.

RULES:
- Twice is a pattern. Three times is a product gap. Say which each is.
- Do not merge two problems because their code looks alike. Merge them only if one
  interface would serve both customers.
- Mark any copy whose ownership you cannot tell from what I gave you.
- Do not reproduce any code. Describe behaviour."""},
   {"title": "Write the product request with each customer's evidence",
    "when": "Before the entry goes to the product owner",
    "body": """Write a product request for <pattern> from this evidence: <paste the log rows, the
days, the defects and the history of what broke>.

1. The problem in one sentence, as the product owner would say it.
2. One row per customer: when, how it was built, days, defects, the last change that
   broke it.
3. The ask: what, who would own it, and the cheapest version that would do.
4. What a no costs: the next copy's days, and the next break.

RULES:
- No customer's name, data, prices or terms. Call them customer A, B and C.
- Every number carries its source. Mark anything you inferred as INFERRED.
- Do not argue that it matters. Show what it cost."""},
   {"title": "Send a model gap to research with the failing cases",
    "when": "An evaluation fails for a reason your code cannot fix",
    "body": """Our evaluation found a gap in the model, not in our code. Write the note to research.

1. The behaviour in one sentence, and the slice it occurs in.
2. The score and its lower bound, with n.
3. Ten failing cases, redacted, each with the input, the output, and the right answer
   as the customer's experts labelled it.
4. What we tried that did not fix it: prompt changes, examples, a checker.
5. What we ship meanwhile, so nobody waits on a fix.

Describe the behaviour and the evidence. Do not guess at the cause inside the model.

FAILING CASES AND SCORES:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · the third partner lookup",
   "body": "Codeshare needed seats on four partner airlines, looked up in one call. It was the third "
           "such lookup you had written: the first two were for two other airline customers and took "
           "nine days and six; this one took five. Your first entry described SkyWays' copy with "
           "SkyWays' evidence, and the product owner read it as one customer's feature request. The "
           "second carried all three, redacted: the days, the week one partner changed its interface "
           "and all three copies broke and were fixed three times, and the winter hours, which only "
           "a lookup reading the partner's own data prevents. It asked for a supported connector "
           "instead of the fourth copy the cargo frame was about to need. The answer was not yet as "
           "product: build it as a shared service the practice owns, and product takes it when two "
           "deployments run it unchanged. The model gap went separately, to research: ten failing "
           "cases where the assistant stated a partner's usual policy as fact."},
 "pitfalls": [
   "Writing the pattern up with one customer's evidence. It reads as that customer's feature "
   "request, and it is triaged as one.",
   "Fixing the repeat yourself, in a shared repository nobody agreed to own. It works until you "
   "move on, and then it is a fourth copy with no owner.",
   "Sending research a complaint instead of cases. A gap in adjectives is feedback; ten labelled "
   "failures with a lower bound is a defect someone can act on.",
 ],
 "done_when": "The product owner has answered, in writing, on every repeat you have solved three "
              "times, and every model gap your evaluations found has reached research with its "
              "failing cases.",
},
{
 "n": 11, "id": "reuse", "phase": "Reuse", "stage": "evolve", "level": None,
 "hats": ["engineer"],
 "question": "Does the reusable version work next time?",
 "title": "Prove the reusable version at the next deployment",
 "when": "Evolve, built between engagements and proved at the next one that needs it",
 "purpose": (
   "A reusable asset is a claim until someone who is not you has used it on a real deployment, and "
   "you have timed it. Build the configurable version with tests and a written interface, use it at "
   "the next deployment, and measure the days to first value against the bespoke copy. Then retire "
   "the copies, or you will keep four things alive where there were three. OpenAI asks its "
   "forward-deployed software engineers to {{S3-abstractions}}. This step adds the measurement."),
 "activities": [
   {"do": "Write the shared version, interface and tests first",
    "detail": "An MCP server, a skill or an evaluation template, configured per customer and never "
              "forked. Write its interface and tests from the pattern entry before any code. Start from "
              "the cleanest copy only if your contracts let you; where a customer owns theirs, write it "
              "fresh from the copies' behaviour."},
   {"do": "Write the README with its limits at the top",
    "detail": "For an engineer who has never met you: the limits, the interface, the configuration, "
              "and a sandbox to try it in. The limits lead because they are what the next deployment "
              "trips on."},
   {"do": "Let someone else wire it at the next deployment, and time it",
    "detail": "If you wire it yourself you measure your memory, not the asset. Stay on call and off "
              "the keyboard, and count the days from the first commit to the first case it serves. "
              "If no deployment comes within a quarter, run it on the copies' recorded inputs, and "
              "write down that this proves less."},
   {"do": "Fix gaps in the asset, never in a copy",
    "detail": "The next deployment will need something the asset lacks. Add it behind the same "
              "interface with a test, and release a version. A fix made only in their copy is the "
              "fork this step exists to stop, and Ramp's FDE team says why: {{S18-pollute}}."},
   {"do": "Retire the bespoke copies on dates their owners agree",
    "detail": "Each copy moves onto the asset through its own customer's change control, after a "
              "side-by-side run on the same inputs. Until the last one moves you maintain both, so "
              "the dates go on the sheet."},
   {"do": "Agree the handoff with its long-term owner, early",
    "detail": "Who owns it after your practice: the product team or the platform team. Agree what "
              "{{S4-handoff}} means before you build: deployments running it unchanged, a README a "
              "stranger has followed, an on-call on their side."},
 ],
 "internal": (
   "Inside your company the asset usually ends up the platform team's, and the risk is that it "
   "never leaves yours. Agree the handoff criteria with the platform's owner before you build it, "
   "and put the date in both teams' plans. A business unit that must ask you for every change will "
   "build its own copy instead."),
 "say": [
   {"to": "The next team, before they start",
    "words": "Use the connector as it is for a week before you change anything. If it cannot do what "
             "you need, tell me: the fix goes into the connector, not into your copy."},
   {"to": "A customer whose own copy is to be retired",
    "words": "Your lookup moves onto the shared connector in your next change window. We run both "
             "side by side on the same cases for a week first, and from then on you get every fix "
             "the other deployments find."},
 ],
 "ai": [
   {"tool": "Coding agent, from the pattern entry",
    "use": "Give it the interface, the tests and each copy's recorded behaviour as cases, and have it "
           "write the asset until they pass. Then have it draft the README for an engineer who has "
           "never met you.",
    "caution": "Give it behaviour, not code. Handed three customers' copies, it will rebuild the "
               "cleanest one line by line, and that copy may belong to its customer."},
   {"tool": "Coding agent, at the next deployment",
    "use": "Run the asset and the bespoke copy it replaces on the same recorded inputs, and list every "
           "case where their answers differ, before the copy is retired.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "What the asset does not cover, and the date each copy retires. The first is a promise to "
           "the next team and the second a promise to each customer; both are yours to keep.",
    "caution": None},
 ],
 "artifact": {
   "name": "Asset proof sheet",
   "short": "Asset proof sheet",
   "good": "One page per asset and version: its owner and long-term owner, where it runs and who "
           "wired it, the days to first value against the bespoke copy, defects found and fixed in "
           "the asset, what it does not cover, what the measurement does not prove, and a "
           "retirement date for each copy.",
   "owner": "Forward-deployed engineer, until its long-term owner accepts it"},
 "template": {
   "title": "Asset proof sheet", "lang": "markdown",
   "body": """# Asset proof sheet · <asset> · v<n> · <date>
_Owner <FDE> · Long-term owner <team> · Handed over when <criteria>_

## 1. What it is
<MCP server | skill | evaluation template> · interface <link> · configured by <file>

## 2. Where it runs
| Deployment | Version | Wired by | Days to first value | The bespoke copy took | Defects, each fixed in the asset |
|------------|---------|----------|---------------------|-----------------------|----------------------------------|
| <deployment> | <v1> | <who, not you> | <n> | <n> | <n> |

## 3. What it does not cover
<...>

## 4. What the measurement does not prove
<who wired it, what they knew already, what the first copy's days included>

## 5. What it costs to keep
<hours a month for the asset> against <hours a month the copies took>

## 6. The bespoke copies
| Copy | Customer | Side-by-side run | Moves on | Retired |
|------|----------|------------------|----------|---------|

## 7. Ready for handoff
| Criterion | Met? | Evidence |
|-----------|------|----------|
| <n> deployments running it unchanged for <period> | | |
| The README followed by someone who never met the author | | |
| An on-call on the long-term owner's side | | |
"""},
 "prompts": [
   {"title": "Diff three customer copies and propose the shared interface",
    "when": "Before you write the asset",
    "body": """Below is the BEHAVIOUR of three implementations of <capability>, from three
customers, as recorded inputs and outputs, with how each is configured: <paste>.

Propose one interface that would serve all three.

1. The operations, with their parameters and return types.
2. For each difference between the copies: a setting, an extension point, or a real
   difference that stays outside the asset. Say which, and why.
3. The tests: one per behaviour the three agree on, and one per difference.
4. What the interface deliberately does not do.

RULES:
- Work from the behaviour. Do not reproduce any customer's code.
- Prefer fewer operations. Each one you add is one the next team must learn.
- If one copy does something the others would break on, flag it. Do not average it."""},
   {"title": "Write the asset's README for an engineer who has never met you",
    "when": "Before the next deployment, then tested by someone who has not seen it",
    "body": """Write the README for <asset>, for an engineer at a new deployment who has never met
me and cannot ask me anything. From: the interface <paste>, the configuration <paste>,
the tests <paste>, the known limits <paste>.

Sections, in this order:
1. What it does not do. Lead with this.
2. What it does, in three sentences.
3. Wiring it in an afternoon: each step, the exact commands, the sandbox.
4. Configuration: every setting, its default, and when to change it.
5. When it fails: each error, what it means, what to do.
6. How to ask for a change: the asset changes, never a copy.

RULES:
- Every command must run. Mark any you could not check as UNCHECKED.
- No customer's name or data in an example. Use the sandbox's."""},
 ],
 "example": {
   "title": "SkyWays · two days against nine",
   "body": "The connector reached version 1 with tests, a README and a sandbox partner, written fresh "
           "from the pattern because each airline owned its own copy. At the cargo deployment the "
           "cargo team's engineer wired it, with you on call and off the keyboard: two days, against "
           "nine for the first copy. What carried over was the slow part: each partner's "
           "authentication, rate limits, error codes and outages. The first day found a gap: a claim "
           "needs the carrier that flew a "
           "leg already flown, and rebooking only ever looked ahead. You added that read to the connector "
           "in half a day, with a test, instead of writing a cargo copy. SkyWays' own lookup moved "
           "onto the connector in Lena's next change window, after a week side by side, and the two "
           "older copies got dates in their own customers' change control. The sheet said what two "
           "days does not prove: the cargo engineer had sat beside the shadow and already knew the "
           "partners."},
 "pitfalls": [
   "Wiring it yourself at the next deployment and calling the speed a saving. You measured that "
   "you remember how; the next team still cannot.",
   "Patching the new customer's copy because the asset's release is a day away. That copy is now "
   "the fifth, and the asset is behind its own users.",
   "Building the asset and never retiring the copies. You now keep four things alive where there "
   "were three, and the saving is spent on the old ones.",
 ],
 "done_when": "Someone who is not you has wired it at a real deployment, the days are measured "
              "against the bespoke copy, every gap it showed is fixed in the asset, and each old "
              "copy has a retirement date its customer agreed.",
},
{
 "n": 12, "id": "review", "phase": "Review", "stage": "evolve", "level": None,
 "hats": ["consultant", "product"],
 "question": "Is the relationship healthy, and what did we learn?",
 "title": "Hold the value review, and keep the relationship honest",
 "when": "Evolve, every quarter while the system runs, and once more at the close",
 "purpose": (
   "Relationships end badly in two ways: the sponsor stops believing your numbers, or nobody "
   "notices the system has stopped earning its cost. A quarterly review prevents both, if you hold "
   "it before anyone asks, put the saving and the spend on one line, and ask what a vendor rarely "
   "asks: what would you stop? Bad news you bring early costs little; the same news found by them "
   "costs the relationship. OpenAI asks its Deployment Leads to {{S2-measurement}}; Databricks "
   "asks its strategists to use their {{S15-advisor}}."),
 "activities": [
   {"do": "Put the saving and the spend on one line",
    "detail": "The two numbers as the [product manager's step 8](../../product-manager/#learn) builds "
              "them, against the baseline taken before the pilot, with review hours and re-runs "
              "beside them. The sponsor should never hear a number about this system first from "
              "anyone but you."},
   {"do": "Show drift, incidents and the controls they produced",
    "detail": "The output mix against both its thresholds, every model or prompt change with the "
              "harness run that cleared it, and each incident with the control it produced and where "
              "that control lives now. A quarter with no incident says so, and lists its near "
              "misses."},
   {"do": "Ask their sponsor what they would stop",
    "detail": "A report nobody reads, a meeting that outlived its reason, a slice that costs more "
              "than it saves. Stopping something is the cheapest value a review can find, and asking "
              "is how a sponsor learns you are not only selling."},
   {"do": "Check who champions it, and who runs it, now",
    "detail": "Write down who backed it at the start and who does today. Champions move on, and a "
              "system loses its defender before it loses its users, so keep three people on their "
              "side who have seen the evidence, never one. Do the same for the operator: a successor "
              "who has not thrown every switch is a handover not yet done."},
   {"do": "Propose the next frame only from the next-frame brief",
    "detail": "Step 9's brief, ranked, or nothing. A proposal without a measured pain is a sales "
              "call."},
   {"do": "Hold your own retrospective, apart from the review",
    "detail": "With your team, not theirs, while it is fresh: what went wrong, written as a change to "
              "your practice's playbook, such as a template line, a check or a default. A "
              "retrospective that changes nothing was a meeting."},
   {"do": "Close cleanly when the work is done",
    "detail": "Every access of yours removed and confirmed, the evidence archived where their "
              "operator will look, open risks handed to a named owner, and a reference asked for. A "
              "clean close is a good ending, not a lost account."},
 ],
 "internal": (
   "Inside your company the review is where a project quietly becomes permanent, or quietly loses "
   "its sponsor. Hold it anyway, with the business unit's head and with finance in the room. Your "
   "next budget will be set from these numbers, so they should come from you first."),
 "say": [
   {"to": "A quarter where it cost more than it saved",
    "words": "This quarter it cost more than it saved. Here is why, and what changes before the "
             "next one. If that does not turn it round, my recommendation will be to switch it off."},
   {"to": "The question a vendor rarely asks",
    "words": "What would you stop? If something we built or report is not worth its cost to you, I "
             "would rather hear it here than at renewal."},
   {"to": "A sponsor who wants the next one sooner",
    "words": "We can frame it next. I will bring the measured pain, who would run it and what it "
             "reuses, and you decide on that, not on how well this one went."},
 ],
 "ai": [
   {"tool": "Chat model, as their finance controller",
    "use": "Paste the draft and ask for the five questions their finance controller will ask, and "
           "the weakest claim, with the evidence that would hold it.",
    "caution": "Paste only what their policy lets you paste. Their finance figures do not go into a "
               "tool nobody approved."},
   {"tool": "Coding agent, over the ledger and the bill",
    "use": "Rebuild the quarter's two numbers from the raw ledger and the bill, so every figure in "
           "the review has a query and a date range beside it.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "The stop question, the champion check and whether to propose a next frame. Each is a "
           "judgement about people and trust, and the sponsor is reading you, not the slide.",
    "caution": None},
 ],
 "artifact": {
   "name": "Quarterly value review",
   "short": "Quarterly value review",
   "good": "Two pages, sent before anyone asks: the two numbers on one line with their baseline, "
           "drift, incidents and their controls, adoption, what the sponsor would stop, the champion and "
           "the operator then and now, the next frame or a clean close, and actions with owners.",
   "owner": "Forward-deployed engineer, with their sponsor and their operator"},
 "template": {
   "title": "Quarterly value review", "lang": "markdown",
   "body": """# Value review · <customer> · <system> · Q<n> <year>
_Held <date> · With <their sponsor>, <their operator>, <their finance lead> · Drafted by <FDE>_

## 1. The two numbers, on one line
| | Baseline, <date>, before the pilot | This quarter | Change |
|---|---|---|---|
| <person-days per case> | <n> | <n> | <n>% |
| Token spend | none | $<n> | |
| Review hours | <n> | <n> | |
| Re-runs | none | <n> | |
**Net:** saved <n> person-days, spent $<n> and <n> review hours · **Next quarter:** <trajectory, and why>

## 2. Drift, changes and incidents
| What | When | Cleared by, or the control it produced | Where it lives |
|------|------|----------------------------------------|----------------|
| <drift, against both thresholds> | | | |
| <a model or prompt change> | | <the harness run> | |
| <an incident or near miss> | | <the enforced control> | |

## 3. Adoption
<who uses it, overrides by team or shift, the change since last quarter>

## 4. What would you stop?
<their answer, in their words> · stopped by <name> on <date>

## 5. People
| | At the start | Now | If changed: what we will show them |
|---|---|---|---|
| Champion | | | |
| Operator | | | |
| Sponsor | | | |

## 6. Next
[ ] The next frame: <the ranked next-frame brief, with its evidence>
[ ] Keep running as it is
[ ] A clean close: access removed <date> · archive <where> · open risks to <name> · a reference

## 7. Actions
| Action | Owner | By |
|--------|-------|----|

_Signed by <their sponsor> · <date>_
"""},
 "prompts": [
   {"title": "Draft the quarter's review, the saving beside the spend",
    "when": "A week before the review, from the ledger and the bill",
    "body": """Draft a quarterly value review for <system> at <customer> from: the ledger <paste>,
the model bill <paste>, the drift readout <paste>, the incident briefs <paste>, and the
baseline taken before the pilot <paste, with its date and method>.

In this order:
1. The two numbers on one line: the saving against the baseline and the spend, with
   review hours and re-runs beside them. The net, and next quarter's trajectory.
2. Drift against both thresholds: week on week, and against the frozen baseline.
3. Each model or prompt change, with the harness run that cleared it; each incident,
   with the control it produced and where that control lives.
4. Adoption: use and overrides, by team or shift.
5. Three questions for the sponsor, the first of them: what would you stop?

RULES:
- Never show the saving without the spend, or the spend without the saving.
- Every number carries its source and its date range.
- If the baseline was taken after the pilot began, say so in the first line.
- Do not recommend a next frame. That comes from the next-frame brief."""},
   {"title": "Find the weakest claim in this review",
    "when": "The day before you send it",
    "body": """Below is the value review I will present to <customer>'s sponsor and finance lead.

Read it as their finance controller, who will check every number against their own
ledger. List, most damaging first:
| The claim | Why it would not survive the check | The evidence that would hold it | Or the honest wording |

Then name:
- the number they are most likely to have from another source;
- any saving that counts work their own staff still do;
- any place the review reads as a sales pitch.

Do not soften a finding. Do not rewrite the review.

REVIEW:
<paste>"""},
 ],
 "example": {
   "title": "SkyWays · day 90's line, kept each quarter",
   "body": "Day 90's slide was the first value review: 40 to 45 percent fewer person-days and a token "
           "bill of $4,200, on one line, with review hours up and the reason they would fall. The "
           "programme continued because both numbers came from the team. Day 180's review kept the "
           "line: 44 percent fewer person-days, $5,100 of tokens for the quarter, and review time "
           "down from 96 hours to 26, under the 30 that day 90 had promised. Then came what Evolve "
           "adds. The champion check found the gap: the contact-centre head, who had backed the "
           "assistant "
           "since the shadow, had moved on, the new head had never seen the evidence, and overrides "
           "on the evening shift had doubled. You walked the new head through the fourteen "
           "disagreements and the evening rule, and overrides fell back within a fortnight. Asked "
           "what she would stop, Ines named the daily disagreement meeting, which had found nothing "
           "new in a month. She signed a clean close of the rebooking engagement, and the relationship "
           "went on in the cargo frame."},
 "pitfalls": [
   "Holding the review only when renewal is near. The sponsor reads it as a sales call, and "
   "believes the numbers less for it.",
   "Missing that the champion has gone. The system runs, the review is on time, and nobody on "
   "their side will argue for it when the budget is cut.",
   "Dragging the engagement on because closing feels like losing the account. They are paying "
   "for an FDE the system no longer needs, and they know it.",
 ],
 "done_when": "Their sponsor has heard the saving and the spend from you before anyone asked, has "
              "said what they would stop, and has signed the next frame or a clean close.",
},
]
