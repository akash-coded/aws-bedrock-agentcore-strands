"""Forward-deployed engineer · Deliver, steps 5-8. Imported by build_content.py.

Deliver is days 1 to 97 at SkyWays: the case itself, then a week of handover. Every example has two
halves. *In the case* is the canon, unchanged; *Your move* is what the forward-deployed engineer does
with it. {{id}} puts a recorded quotation on the page and [[id]] cites a source, both kept in
fde_sources.py, so no step types a quotation of its own.
"""

STEPS_B = [
{
 "n": 5, "id": "mobilise", "phase": "Mobilise", "stage": "deliver", "level": "MVP",
 "hats": ["platform", "product"],
 "question": "Is the first slice still right, on real access?",
 "title": "Start every lead-time item on day one, and measure the before",
 "when": "Deliver's first day, before any code, and every morning until the list is clear",
 "purpose": (
   "The calendar is set by things you do not control: model access in the region their data must stay "
   "in, data access, the security review, change approvals. Each sits in someone else's queue, so file "
   "them all on day one, with names and dates, and count each one done only when its test passes. The same "
   "week, take the baseline from their records: every later claim divides by it, and it cannot be taken "
   "once the pilot starts. The MVP begins here, with one question: does the slice the proof chose still "
   "hold on real access?"),
 "activities": [
   {"do": "File every lead-time request on day one, each with a name and a date",
    "detail": "Model access in their region, the security review, data access and the privacy review of "
              "the fields you will read, network routes, a change slot for cut-over, the experts' hours. "
              "Each gets an owner on their side and a date after which the plan moves. Chase by name, and "
              "escalate on the date, not on a feeling."},
   {"do": "Count access as granted when one call passes, not when someone says yes",
    "detail": "One real call per item, as the production identity, through their network, in the right "
              "region, run every morning until it passes. Identity, region and network cause most "
              "first-week surprises, and the walking skeleton of step 7 is built on whatever passes first."},
   {"do": "Take the baseline this week, from their records",
    "detail": "Cases a day, minutes to a decision, cost per case and cases reopened, from at least four "
              "normal weeks before the engagement, counted by a method their ops lead signs. Once the "
              "pilot starts the mix changes and people work differently, and the before is gone. OpenAI "
              "asks its Deployment Leads to {{S2-measurement}}: this is the pre."},
   {"do": "Re-check the proof on real access",
    "detail": "The proof ran on an export. Production brings a slower interface, a rate cap, a field that "
              "turns out to be free text. In the words of OpenAI's head of FDE, what the customer describes "
              "in scoping {{S24-ground}}. If real access changes the first slice's economics, re-cut it "
              "now, in writing, with the sponsor."},
   {"do": "Keep one log of risks, assumptions, issues and dependencies with their project manager",
    "detail": "One list, read in fifteen minutes a week with whoever can unblock. Two logs, yours and "
              "theirs, disagree within a week, always about a date. Tell the sponsor bad news the day you "
              "know it: trust is lost to surprise, not to bad news."},
   {"do": "Agree how you will work with their team, on one page",
    "detail": "Where the code lives and who merges, who pairs with whom, a daily stand-up and a weekly "
              "note to the sponsor, how to reach the risk owner, and which data may go into which AI tool, "
              "in their policy's words. Pin it in their repository before the first commit."},
 ],
 "internal": (
   "Inside your own company access feels like a favour away, so nobody files the requests. File them "
   "anyway, with owners and dates: an internal security review can take as long as an external one, and "
   "a favour lapses the week its giver is busy. Take the baseline as carefully as for a paying client, "
   "because the unit's head will be asked by their own finance team what it saved."),
 "say": [
   {"to": "Day one, to their project manager",
    "words": "Today I need three names and three dates: data access, model access in your region, and the "
             "security review."},
   {"to": "A request is late, to the person who can approve it",
    "words": "Data access was due on Tuesday. Every day it waits moves the shadow run by a day. Can you "
             "approve it by Friday, or tell me who can?"},
   {"to": "The sponsor wants to skip the baseline",
    "words": "If we do not measure the before this week, nobody will ever be able to say what this saved. "
             "It takes two days, and it cannot be done once the pilot starts."},
 ],
 "ai": [
   {"tool": "Claude Code or Codex, in a sandbox on their account",
    "use": "Write the one-call tests from the access list, one per item, so *granted* means a call that "
           "passed rather than an email.",
    "caution": "Run them as the service identity, from their network, in their region. A test that passes "
               "with your own credentials proves only that you have access."},
   {"tool": "Chat model",
    "use": "Turn the statement of work's dependencies into requests in plain words, longest lead time "
           "first, each with the date after which the plan moves.",
    "caution": "It does not know their process. Every form, queue and approver it names is a guess to "
               "check with their project manager."},
   {"tool": "Do not delegate",
    "use": "The baseline's method, and who signs it. Every value claim for the life of the system divides "
           "by it, so their ops lead agrees how it was counted before anyone sees an after.",
    "caution": None},
 ],
 "artifact": {
   "name": "Day-one access list and baseline",
   "short": "Access list and baseline",
   "good": "One page, read every morning: each lead-time item with an owner, a late-from date and a test "
           "that runs, what real access changed about the first slice, and a baseline from records before "
           "anything changed, its method signed by their ops lead.",
   "owner": "Forward-deployed engineer, with their project manager"},
 "template": {
   "title": "Day-one access list and baseline", "lang": "markdown",
   "body": """# Day-one access list and baseline · <customer> · <engagement>
_Opened <day 1> · Kept by <FDE> with <their project manager> · Read every morning until every row passes_

## 1. Lead-time items, longest first
| # | Item | Owner at <customer> | Requested | Late from | Status | The test that proves it |
|---|------|---------------------|-----------|-----------|--------|-------------------------|
| 1 | Model access in <the region their data must stay in>, by inference profile | <name> | <date> | <date> | <requested> | One call from <their account>, in <region>, logged |
| 2 | Security review of <the design> | <name> | | | | Written approval, with its conditions |
| 3 | Privacy review of the fields it reads, writes and logs | <name> | | | | Approval naming each field, its class and how long it is kept |
| 4 | Read access to <system>, as the service identity | <name> | | | | Read one <record> by id, as that identity |
| 5 | Network route from <runtime> to <system> | <name> | | | | The same read, from inside <runtime> |
| 6 | Their repository, a CI runner, an environment to deploy to | <name> | | | | One merge that runs their pipeline green |
| 7 | <n> hours of their experts' labelling, booked | <name> | | | | Invitations, accepted |
| 8 | A change slot for cut-over | <name> | | | | The slot, on their change calendar |
| 9 | The AI tools their policy approves, and the account each runs on | <name> | | | | Their written list |

A row is done when its test passes, not when someone says yes.
Past its late-from date the plan moves by the same days, and <their sponsor> hears it that day.

## 2. What real access changed
| Assumption from the proof | What the live system shows | Effect on the first slice | Decided by, date |
|---------------------------|----------------------------|---------------------------|------------------|
| <the export matched production> | <...> | <none · re-cut · a new risk> | <name, date> |

## 3. The baseline, from records before the engagement began
| Measure | Value | Cases | Source | Period | How it was counted |
|---------|-------|-------|--------|--------|--------------------|
| <cases a day> | | | <export, system> | <weeks> | |
| <minutes to a decision> | | | | | |
| <cost per case> | | | | | |
| <cases reopened within 7 days> | | | | | |

Signed as the baseline by <their ops lead>, <date>. The same count is repeated after go-live.
"""},
 "prompts": [
   {"title": "Turn the dependencies into requests someone can approve",
    "when": "Day 1, before the kick-off ends",
    "body": """Here is the dependency table from our statement of work with <customer>, and the
plan's dates: <paste>.

Turn each dependency into the request its approver will receive:
| # | The request, in one sentence | Approver (role) | Form or queue | What they will ask first | Late from |

RULES:
- One approver per row. Two approvals are two rows.
- Longest usual lead time first: security review, data access and model access in the
  region their data must stay in usually lead.
- Late from is the last date that does not move the plan, worked back from <the shadow start>.
- Draft a two-line message for each: what, by when, and what slips if it is late.
- Mark every form, queue or approver you are guessing as CHECK. Never invent their process."""},
   {"title": "Write the one-call test that proves each access works",
    "when": "Each time someone says access is granted",
    "body": """For each access item below, write a smoke test that makes ONE real call with the
identity, network path and region the production system will use, and prints PASS or
FAIL with the reason.

ITEMS: <paste the access list>
THEIR STACK: <language, cloud account, region, how identities are issued>

RULES:
- Use the service identity, never mine. A test that passes as me proves nothing.
- Name the region and the inference profile in the model call, and fail if either differs.
- Read one record and check one field I can verify by eye. Write nothing.
- Secrets come from <their secrets store>, never from the code.
- Exit non-zero on any FAIL, so it can run in their pipeline every morning.

Then list the items one call cannot prove, and the nearest proof for each."""},
 ],
 "example": {
   "title": "SkyWays · days 1 to 13, the region nobody requested",
   "body": "**In the case:** in the first two days the pain was measured from the Q2 ticket export: 240 "
           "cases a day, 38 minutes to a rebooking decision, $9.40 a case, 11% of them codeshare. Model "
           "access was granted in `us-east-1` in week one, so everybody assumed the account had it, and "
           "nobody requested `eu-west-1`, where the passengers' data must stay, until the first call "
           "failed on day 13. Six days went, against a plan that allowed none. **Your move:** the access "
           "list names `eu-west-1` on day 1, beside a one-call test from their account that runs every "
           "morning. It fails on day 2, when a missing region costs a request, not a week. The baseline "
           "goes on the same page, signed by their ops lead, because day 90 divides by it."},
 "pitfalls": [
   "Counting a yes in an email as access. The first real call, weeks later, finds the identity, the "
   "region or the network, and the plan pays for it in days.",
   "Building in your own sandbox while the requests wait. The code grows around your account's defaults, "
   "and moving it into theirs becomes a project of its own.",
   "Taking the baseline after the pilot starts. The mix has changed and people work differently when "
   "watched, so every value claim rests on a guess.",
 ],
 "done_when": "Every lead-time item has an owner, a late-from date and a test that runs each morning, and "
              "the baseline is signed by their ops lead with its method beside it.",
},
{
 "n": 6, "id": "sign", "phase": "Sign", "stage": "deliver", "level": "MVP",
 "hats": ["architect", "product"],
 "question": "What exactly, under whose authority?",
 "title": "Get their risk owner to sign every limit before you build past it",
 "when": "Deliver's first two weeks, before any tool can write anything",
 "purpose": (
   "Three documents decide everything after this: the spec, a pass mark for each kind of case, and the "
   "authority budget, which says what the system may do alone and the limit on each action. You draft "
   "all three, because you can see the system. They sign them, because the risk is theirs. A limit you "
   "set because their risk team was slow becomes your limit on the day it is wrong. And a signature is "
   "half the step: each limit then lives in the tool that would break it, with a test, or it is a "
   "sentence a model can be talked past."),
 "activities": [
   {"do": "Run the requirements as a mob, with their experts in the room",
    "detail": "AI-DLC's [Mob Elaboration](../../learn/what-is-ai-dlc/): a model proposes requirements and "
              "asks its questions aloud, and their experts answer. Record every answer with its author's "
              "name. The names make the decisions theirs, and a credited read-back the next day stops the "
              "same question coming back."},
   {"do": "Write the spec with the five fields a requirements document leaves out",
    "detail": "What the model decides and what code decides; what it may do alone; how right it must be, "
              "per kind of case; what happens when it cannot decide; what is logged. If the spec leaves one "
              "open, a coding agent fills it by default."},
   {"do": "Draft the authority budget, one row per action",
    "detail": "The action, its level, its cap, the approver above the cap, and where the cap is enforced. "
              "Band each by what one wrong call could damage, never by the size of the change. The "
              "[architect's step 6](../../solution-architect/#bound) has the method in full."},
   {"do": "Get each line signed by the person who owns that risk",
    "detail": "Limits by their risk owner, often compliance or finance; pass marks by their expert lead; "
              "the spec by their product owner. A sponsor's signature on a limit they do not own is one "
              "that nobody defends in the incident review."},
   {"do": "Set each pass mark from their costs, so the arithmetic is theirs too",
    "detail": "If a wrong answer costs four times what a right one saves, it must be right four times in "
              "five. Use their figures, the complaint and the investigation included, and the bar stops "
              "being your opinion. A person approving each refund lowers what a wrong one costs, and moves "
              "that bar further than any model can."},
   {"do": "Put every cap in the tool that would break it, with a test",
    "detail": "The refund cap is a typed parameter that raises above it, and the approval is a token the "
              "model cannot mint. Two tests, over the cap and without approval, both raise. The sentence in "
              "the prompt stays, marked as policy."},
   {"do": "Build nothing past an unsigned decision",
    "detail": "That is [the hard gate](../../learn/the-hard-gate/). Every other open question runs beside "
              "the build behind a placeholder with an owner and a date. If the programme cannot wait, the "
              "unsigned action runs in shadow, deciding and acting on nothing, until it is signed."},
 ],
 "internal": (
   "Inside your own company a nod from a colleague in a corridor feels like enough. Get it written, and "
   "signed by whoever owns the risk in the business unit, not by your own manager: when the incident "
   "comes, the signature is what keeps it a decision rather than a blame. Your platform's default limits "
   "are not their limits either, until someone in the unit has signed them."),
 "say": [
   {"to": "Asked to pick a sensible number for now",
    "words": "I can draft the number, but I cannot own it. If I set the refund limit myself, the first "
             "incident review will find that nobody on your side decided it. Who signs refunds today?"},
   {"to": "Their compliance team needs three more weeks",
    "words": "Everything else can go live on its own evidence. Refunds run in shadow, deciding and paying "
             "nothing, until your compliance officer signs the limit. Then it is one line of configuration."},
   {"to": "The risk owner asks how the limit is kept",
    "words": "It is in the refund tool itself, not in the model's instructions. Above the limit the tool "
             "refuses unless your approver has confirmed, and a test proves that on every change."},
 ],
 "ai": [
   {"tool": "A model in the mob session",
    "use": "Propose requirements and ask the clarifying questions aloud, so their experts answer in the "
           "room and each answer carries a name.",
    "caution": "It proposes with confidence. Nothing it says is a requirement until one of their people "
               "agrees, by name."},
   {"tool": "Claude Code or Codex, in their repository",
    "use": "Generate the typed signatures and the two refusal tests for every capped action from the "
           "signed budget, each citing its signed line in a comment.",
    "caution": "Check that it raises rather than clamps, and reads the cap from config rather than a "
               "literal. Both look fine in a diff."},
   {"tool": "Do not delegate",
    "use": "Every limit, every pass mark, and who signs them. A model will offer a sensible cap. A "
           "sensible cap that nobody signed is the one that fails in production, and so is the one you "
           "chose yourself.",
    "caution": None},
 ],
 "artifact": {
   "name": "Signed spec and authority budget",
   "short": "Signed spec and limits",
   "good": "Every action with its level, its cap, its approver and the test that enforces it; every pass "
           "mark with the costs that set it; each line signed by the person who owns that risk; and no "
           "line that is only written.",
   "owner": "Forward-deployed engineer drafts; their risk owner and expert lead sign"},
 "template": {
   "title": "Signed spec and authority budget", "lang": "markdown",
   "body": """# Signed spec and authority budget · <customer> · <system>
_Version <n> · <date> · Drafted by <FDE> · Nothing is built past a line that is not signed_

## 1. The five decisions a requirements document leaves out
| Decision | What we will build | Signed by | Date |
|----------|--------------------|-----------|------|
| What the model decides, and what code decides | <the model ranks options; code computes every fare and refund> | <product owner> | |
| What it may do alone | <section 3> | <risk owner> | |
| How right it must be | <a pass mark per kind of case, section 2> | <expert lead> | |
| What happens when it cannot decide | <the case goes to a person, with its reasons> | <ops lead> | |
| What is logged | <every call, tool use, approver and model version> | <risk owner> | |

## 2. A pass mark per kind of case
| Kind of case | Share of cases | A right answer saves | A wrong one costs | Pass mark | Signed by |
|--------------|----------------|----------------------|-------------------|-----------|-----------|
| <same-day change> | <n%> | <$n> | <$n> | <cost ÷ (cost + saving)> | <expert lead> |

The pass mark is met by the lower bound, never by the score.

## 3. Authority budget, one row per action
| Action | Level | Cap | Approver above it | Enforced in | Refusal test | Enforced, or only written? | Signed by, date |
|--------|-------|-----|-------------------|-------------|--------------|----------------------------|-----------------|
| <search flights> | alone | none | none | a read-only identity | <no write scope> | | |
| <rebook, same day> | alone, monitored | <same day, own flights> | none | <rebook(): refuses other days and partners> | <a partner rebook raises> | | |
| <rebook, partner flight> | alone, with a veto window | <one booking> | <desk lead, within <n> min> | <held in a queue for <n> min> | <a held rebook cannot run early> | | |
| <issue refund> | named approver, every time | <$400> | <approver role> | <issue_refund(amount): typed, raises over the cap> | <over the cap raises; no approval raises> | | |
| <change passenger identity> | never | none | none | no tool exists | <absent from the schema> | | |

Levels: drafts only · alone, with a veto window · alone, monitored · named approver every time · never.
A veto window names how long the action waits and who may cancel it. Monitored names who reviews,
within what time, and the switch they throw. Without those, the level is only a word.
A line that is only written has not passed. Nothing is built past it.

## 4. Open decisions that run beside the build
| Decision | Placeholder meanwhile | Owner | Settled by |
|----------|-----------------------|-------|------------|
| <model tier per slice> | <mid tier behind the gateway> | <name> | <date> |
"""},
 "prompts": [
   {"title": "Find the decisions nobody has signed",
    "when": "The day before the sign-off meeting",
    "body": """Below are our spec, the pass marks and the authority budget for <system> at
<customer>, with the signatures collected so far. <paste>

List every decision they rely on that nobody has signed:
| Decision | Where it is assumed | The role at <customer> that carries the risk | HARD or soft | Placeholder, if soft |

HARD if any answer is no: can it be reversed cheaply once building starts? can the build
go on behind a placeholder? does it have a named owner and a date? does everything
downstream survive if the answer changes?

RULES:
- A default is a decision. "Hands over when unsure" sets a threshold someone must own.
- Any limit on money, identity or a message to a customer is HARD.
- Name the role that carries the risk, not the most senior person in the room."""},
   {"title": "Turn the signed budget into refusal tests",
    "when": "The day a line is signed, before the tool can be called",
    "body": """Here is the signed authority budget: <paste>. Here are the tool signatures in their
repository: <paste>.

For every action at "named approver" or "never", write:
1. the typed signature, its cap a bounded parameter read from <config file>;
2. a test that a call over the cap RAISES;
3. a test that a call with no approval, or a forged one, RAISES;
4. for "never": a test that no tool in the schema can perform the action.

RULES:
- Raise. Never clamp to the cap, never log and carry on.
- Every number comes from config, with a comment citing the signed line and its date.
- Leave the prompt's sentence where it is, marked as policy.

Then list each row the code cannot express, so I take it back to whoever signed it."""},
   {"title": "Credit every decision in the mob's notes to whoever made it",
    "when": "The evening after each mob session",
    "body": """Here are my notes from today's requirements session with <customer>'s experts: <paste>.

Produce two lists:
1. DECIDED: each decision in one sentence, with the name and role of whoever made it,
   in their own words where the notes have them.
2. OPEN: each question not answered, with who should answer it, and by when.

RULES:
- Credit whoever decided, not whoever proposed. If the notes do not say, write UNKNOWN.
- Never merge two people's requirements into one line without both names.
- A proposal the model made that nobody accepted is OPEN.

Then draft the read-back email to everyone who attended, decisions first, each with its name."""},
 ],
 "example": {
   "title": "SkyWays · days 6 to 82, a limit signed and never enforced",
   "body": "**In the case:** on day 6 compliance signed the first line: a named approver for every refund "
           "over $400. On day 15 a thirty-page requirements document became a one-page spec, a pass mark "
           "per kind of case and the authority budget, and five decisions turned out never to have been "
           "made. The team crossed with the budget written and only partly enforced: the cap lived in the "
           "prompt, the refund tool accepted any amount, and on day 82 a $2,000 refund went out that was "
           "not owed. **Your move:** the budget names where each cap lives, the refund tool's amount "
           "parameter, with a test that a $401 refund without an approver is refused. Its last column "
           "reads *only written* until that test is green, and nothing past the refund action is built "
           "until it reads *enforced*."},
 "pitfalls": [
   "Choosing a limit yourself because their risk team is slow. It unblocks you this week, and makes the "
   "loss yours on the day the limit is wrong.",
   "A signature from someone who does not own the risk. The sponsor signs happily, and in the incident "
   "review the risk owner says nobody asked.",
   "A cap that lives in the prompt and the design. It reads as a control in every review and stops "
   "nothing.",
   "Treating every open question as hard. The build waits behind eleven meetings when three decisions "
   "needed signatures and the other eight needed only a placeholder, an owner and a date.",
 ],
 "done_when": "Every action has a signed line with its cap, its approver and the test that enforces it, "
              "every pass mark is signed by their expert lead, and no line reads only written.",
},
{
 "n": 7, "id": "build", "phase": "Build", "stage": "deliver", "level": "MVP, then build",
 "hats": ["engineer", "qa"],
 "question": "Does it meet their bar, slice by slice?",
 "title": "Build in their stack, and prove it on their cases beside their staff",
 "when": "From the first day of the build until the shadow run reads clean",
 "purpose": (
   "Build where they will maintain it, with their engineers, and prove it on their cases, not yours. The "
   "first slice is the MVP: the thinnest version one group of their users can rely on, held to a signed "
   "pass mark. Then every slice in scope meets its own bar, held by a harness in their pipeline that the "
   "merge cannot pass, so the proof outlives your stay. Last, it runs beside their staff, deciding and "
   "acting on nothing, because the rules that matter most are often written nowhere."),
 "activities": [
   {"do": "Put one context file in their repository, AGENTS.md",
    "detail": "Their stack, the commands that build and test it, what never to touch, and each rule learnt "
              "the hard way. Codex reads it, and so does Claude Code when the repository has no CLAUDE.md "
              "[[S27]]: one set of rules for your agents and theirs, and it stays when you go."},
   {"do": "Build a walking skeleton through their real system first",
    "detail": "Their identity, their data path, one record on a screen, no model. It proves the plumbing "
              "on the first day of the build, while a credentials or network problem costs hours."},
   {"do": "Write the floor, then the model calls, then a checker after the risky ones",
    "detail": "Fares, eligibility and refunds are code with unit tests. The model ranks and drafts on top, "
              "and an independent checker follows only the steps where a wrong answer is costly and easy "
              "to miss: the [engineering lead's steps 3 to 5](../../engineering/#floor)."},
   {"do": "Wrap their systems as tools, each with its own least-privilege identity",
    "detail": "Reads open, writes gated, one identity per tool, so a model that has been talked past still "
              "reaches only what the job needs. A tool that returns an empty result on error reads to the "
              "model as *nothing applies*: make every tool fail loudly."},
   {"do": "Build the golden set from their past cases, labelled by their experts",
    "detail": "Redacted, from their history, tagged by the slices they care about. First measure how often "
              "two of their experts agree: that is the ceiling on any pass mark, and if it sits below the "
              "signed bar, go back to step 6 before building. Report every slice with its sample size and "
              "lower bound, never one average."},
   {"do": "Make the harness a check their merge cannot pass",
    "detail": "In their pipeline, cheapest checks first, failing any slice below its bar however good the "
              "average. A comment on a pull request is read in a quiet week and clicked past in a release "
              "week, the week it exists for."},
   {"do": "Run the shadow beside their staff, and read the disagreements with them",
    "detail": "The system decides a copy of every live case, off the live path, and acts on none; a model "
              "version change restarts the window. Each afternoon, go through the disagreements with the "
              "people who made the real decisions: a cluster is usually one rule nobody wrote down."},
   {"do": "Pair with their engineers on every change",
    "detail": "Their engineer drives as often as you do, and reviews what your coding agent wrote. AWS "
              "describes the customer's engineers moving {{S20-operators}}: these are the co-builder "
              "weeks, and by the shadow run they ship a change without you."},
 ],
 "internal": (
   "Inside your own company you will be tempted to build in your platform's repository, on your "
   "pipeline, for now. Build where the business unit will maintain it, under their checks, from the "
   "first commit: a move later is a migration nobody budgets for. Hold their bar, not your platform's "
   "default, and let their experts label the cases even when your team knows the data better."),
 "say": [
   {"to": "Fourteen shadow disagreements, all on one shift",
    "words": "These fourteen disagreements are one rule. Who on the evening shift can tell us why?"},
   {"to": "The score clears the bar, and the room wants to launch",
    "words": "The score is above the bar and its lower bound is not, so it is probably good enough and not "
             "yet proven. We run beside your desk from today, and the evidence decides the launch."},
   {"to": "A senior expert who distrusts it",
    "words": "You know what a right answer looks like better than anyone here. Will you label the cases we "
             "test it against, and show us where it is wrong?"},
 ],
 "ai": [
   {"tool": "Claude Code or Codex, in their repository",
    "use": "Build each slice from a story file on a branch, with their engineer reviewing, and have it "
           "write the tool tests and the harness steps in the same pass as the code.",
    "caution": "In a repository you did not write, run headless sessions bare and keep every key out of a "
               "CI job that runs their code [[S27]]. Two people read any change that moves money."},
   {"tool": "A different model, as checker and judge",
    "use": "Check the risky steps, and judge tone and policy on the golden set, pinned to a version that "
           "every run records.",
    "caution": "Calibrate it against their experts' labels on a sample before anyone quotes a judged "
               "score."},
   {"tool": "Do not delegate",
    "use": "The labels, and the reading of the shadow's disagreements. What counts as right is their "
           "experts' call, and the rule behind fourteen disagreements is found by asking the people who "
           "made the decisions.",
    "caution": None},
 ],
 "artifact": {
   "name": "Evidence pack, and the harness in their pipeline",
   "short": "Evidence pack",
   "good": "One index page: every artefact with its owner on their side and its date, every slice with "
           "its lower bound against its signed pass mark, the shadow's disagreements read and turned into "
           "rules, and every control marked enforced or only written.",
   "owner": "Forward-deployed engineer, with their engineering lead"},
 "template": {
   "title": "Evidence pack", "lang": "markdown",
   "body": """# Evidence pack · <customer> · <system>
_One page, every link current · Kept by <FDE> with <their engineering lead> · Reviewed every <Friday>_

## Built
| Artefact | Where it lives | Owner at <customer> | Version | Last changed |
|----------|----------------|---------------------|---------|--------------|
| AGENTS.md | <repo>/AGENTS.md | <their engineering lead> | | |
| Walking skeleton, and its test | <path> | | | |
| Tools, one identity each | <path>, <identity names> | | | |
| Model version, pinned | <config path> | | | |
| Signed spec and authority budget | <link> | <their risk owner> | | |
| First change their engineer shipped alone | <pull request> | <their engineer> | | |

## Proven, per slice
| Slice | Cases | Labelled by | Experts agree | Score | Lower bound | Pass mark | Verdict |
|-------|-------|-------------|---------------|-------|-------------|-----------|---------|
| <same-day change> | <n> | <two of their experts> | <n%> | | | <signed> | <pass · not yet proven · fail> |

PASS only when the lower bound is at or above the pass mark.

## Shadow, beside their staff
| Window, fixed in advance | Slice | Cases | Agreement | Disagreements read | Rules found, and who explained them | Added to |
|--------------------------|-------|-------|-----------|--------------------|-------------------------------------|----------|
| <dates> | | | | <n of n> | <the rule · name, role> | <spec · golden set · tool> |

Money actions are reported apart and stay gated, whatever this table says.

## Enforced, or only written?
| Control | Should live in | The check you run | Result |
|---------|----------------|-------------------|--------|
| <refund cap> | <issue_refund(), typed parameter> | <the refusal test, in CI> | <enforced · ONLY WRITTEN> |
| Pass marks block the merge | <a required check on main> | <read the branch protection rule> | |
| Shadow never writes | <the nightly job> | <the assertion, last green> | |
"""},
 "prompts": [
   {"title": "Write the AGENTS.md for their repository",
    "when": "The first day you have their repository",
    "body": """Read this repository and draft its AGENTS.md: the one context file that every coding
agent on this team reads, theirs and mine. Under 60 lines, in this order:
1. What the system does, in two sentences.
2. The commands that build, test and run it, each one I have run.
3. Never touch: each path, with its reason.
4. Rules learnt here, one line each, naming the review or incident that taught it.
5. Limits live in tool signatures, never in prompts. Name the config file that holds
   the caps; do not repeat their numbers here.
6. What data may go into which tool, in their policy's words: <paste>.

RULES:
- Only what the repository or my notes show. Mark every guess TO CHECK.
- No secrets, no customer data, no names of their staff.
- Their conventions win over mine: linter, test layout, branch rules."""},
   {"title": "Group the day's shadow disagreements",
    "when": "Each afternoon of the shadow run, before you sit with their staff",
    "body": """Below are today's shadow cases where the system's decision differed from the one
<customer>'s staff made: the case, both decisions, the system's reasons, the time and
the shift. <paste, redacted>

Group them by the most likely single cause:
| Cause, in one sentence | Cases | Time, shift or partner pattern | What to ask the staff who decided |

RULES:
- Prefer one cause that explains many cases to many that explain one each.
- Look at time, shift, partner and route before wording: rules that live in people's
  heads usually depend on when and who.
- Never mark the staff decision as wrong. The job is to find out what they know.
- Leave the cases that fit no group on their own."""},
   {"title": "Diff the sandbox and their environment",
    "when": "It passes in your sandbox and fails in theirs",
    "body": """The system passes in my sandbox and fails in <customer>'s environment. Before anything
changes, list every difference that could explain it.

SANDBOX: <identity, region, model and version, network, data sample, tool versions, limits>
THEIRS: <the same, as far as known>
THE FAILURE: <the case, the logs, the trace>

| Layer | Sandbox | Theirs | Could it cause this? | The one check that settles it |

RULES:
- Cover data, identity, region and model access, network, tool timeouts and rate
  limits, model version and config.
- Check every tool's error path first: an empty result on error reads to the model
  as "nothing applies".
- Cheapest check first. No prompt change until every layer above it is ruled out."""},
 ],
 "example": {
   "title": "SkyWays · days 30 to 60, fourteen disagreements and one rule",
   "body": "**In the case:** on day 30 a walking skeleton read a booking and showed it by four in the "
           "afternoon. On day 45, 412 of the 500 golden cases were right: "
           "82.4% against a bar of 80%, with a lower bound of 79.1%. The room read it as a pass. The "
           "verdict was *probably above the bar, not yet proven*, and the shadow started that afternoon "
           "instead of the launch. Its fourteen disagreements with the desk were one rule nobody had "
           "written: the evening shift never uses one partner after 18:00, because its transfer desk "
           "closes. **Your move:** on day 45 you hold the room to the condition Ines signed before day 1: "
           "if the lower bound falls short, the shadow runs first. So the shadow is the plan, not a "
           "setback. You read its disagreements with the desk each afternoon, and when fourteen turn out to "
           "be one rule you credit whoever on the evening shift explained it. The rule goes into the spec "
           "and the partner tool, and the fourteen cases into the golden set, where the harness holds every "
           "later change to them."},
 "pitfalls": [
   "A golden set you wrote yourself. It holds the cases you can imagine and scores well: at SkyWays twelve "
   "invented cases scored 94%, and none of them was codeshare.",
   "A harness that comments instead of blocking. At SkyWays a red slice was merged past the comment on "
   "the Thursday before the pilot.",
   "Polishing a slice nobody uses. Build means every slice in scope at its bar, not a favourite slice at "
   "99%.",
 ],
 "done_when": "Every slice in scope has a lower bound at or above its signed pass mark, or a written "
              "reason it stays in shadow; the harness blocks their merge; and one of their engineers has "
              "shipped a change without you.",
},
{
 "n": 8, "id": "hand-over", "phase": "Hand over", "stage": "deliver", "level": "Deploy",
 "hats": ["platform"],
 "question": "Does it run without you?",
 "title": "Widen by evidence, then hand it to the person who will run it",
 "when": "From the week before cut-over to the day your access ends",
 "purpose": (
   "Deploy is thinking at the size of their organisation: owners, operations and the contract, not the "
   "code. Widen one action at a time on evidence, never on a date, with money actions gated throughout. "
   "Meanwhile make yourself unnecessary: every switch timed, every runbook rehearsed by the person who "
   "will use it, every loop owned on their side. The handover is real when that person has signed, your "
   "access has ended, and nothing breaks."),
 "activities": [
   {"do": "Widen one action at a time, on evidence, never on a date",
    "detail": "Shadow, then 5%, then wider, then all, per action, each step naming the evidence that "
              "earned it and the risk owner who agreed. Widening raises the share, never the level: a money "
              "action keeps its named approver at every share. Each step's length is arithmetic: cases "
              "needed ÷ (share × cases a day)."},
   {"do": "Time every switch with a stopwatch before cut-over",
    "detail": "Someone on their side, not the author, throws each one while you watch: the kill switch, a "
              "flag back to shadow, a prompt rollback, a model rollback. The times go into the runbook "
              "with the date. A rollback nobody has timed is a belief."},
   {"do": "Write runbooks for the five things that will happen",
    "detail": "A drift alert, a cost spike, a tool outage, a model change, a disputed refund. Each says how "
              "to tell, what to switch, whom to call and how to know it is over, and the person who will "
              "use it runs it once, end to end."},
   {"do": "Name an owner on their side for every loop",
    "detail": "The operator, the on-call rota, the cost owner, the drift owner, and whoever turns incidents "
              "into the next brief. Cost, incidents and drift feed back into design, so nobody downstream "
              "chases them unless a named person owns each."},
   {"do": "Have the handover signed by the person who will run it",
    "detail": "Their operator, the person who will be paged, signs that they can run it; their sponsor "
              "signs, separately, that it was delivered as the statement of work says. AWS lists what a "
              "customer should hold at the end: {{S20-handover}}. The checklist is that list, with a name "
              "beside every line."},
   {"do": "End your access on the agreed date",
    "detail": "Write the date into the checklist and keep it. The support period comes from the "
              "[statement of work](../frame/#t-scope), not from goodwill on the day: a fortnight on call to "
              "their operator, not to the system, so every question goes through the person who now owns it."},
 ],
 "internal": (
   "Inside your own company the risk is the opposite: you never leave, because you are a message away "
   "and the unit never learns to run it. Put the end date in the charter and keep it. If the unit cannot "
   "staff an operator, that is a finding for its head, not a reason to become their team for good "
   "without anyone deciding it."),
 "say": [
   {"to": "The sponsor wants to widen on a date",
    "words": "We widen when the evidence says so. At 5% of 240 cases a day, the 500 cases we need take 42 "
             "days. At 20% they take eleven, and one passenger in five meets a system not yet proven. Your "
             "risk owner chooses."},
   {"to": "Handing over, to their operator",
    "words": "From Friday this is yours to run. For two weeks I am on call to you, not to the system: you "
             "call me, and you decide."},
   {"to": "Asked to stay on after the handover",
    "words": "I can stay, but then it is not handed over. Who on your side will run it? If nobody can yet, "
             "that is the first decision to take, and it is yours."},
 ],
 "ai": [
   {"tool": "Claude Code or Codex, over the code and the dashboards",
    "use": "Draft each runbook from the code, the alerts and the timed rehearsals, so every command in it "
           "is one that exists.",
    "caution": "A drafted runbook reads well and has never been run. It stays a draft until their on-call "
               "has followed it in a rehearsal."},
   {"tool": "Chat model, as their operator on a bad night",
    "use": "Read the handover pack cold and list the questions their operator would ask at two in the "
           "morning with nobody to call.",
    "caution": None},
   {"tool": "Do not delegate",
    "use": "Each widening, and the judgement that their operator is ready. You bring the evidence and "
           "their risk owner decides. Readiness is seen when they throw the switches, not read in a "
           "summary.",
    "caution": None},
 ],
 "artifact": {
   "name": "Handover pack",
   "short": "Handover pack",
   "good": "Signed by the person who will run it, after they have thrown every switch and followed every "
           "runbook without you: an owner for every loop, the switches with their times, where each action "
           "stands and why, the open risks with owners, and the date your access ends.",
   "owner": "Forward-deployed engineer, until the person who will run it signs"},
 "template": {
   "title": "Handover pack", "lang": "markdown",
   "body": """# Handover pack · <customer> · <system>
_From <FDE> · To <the person who will run it> · Signed <date> · Our access ends <date>_
Repository and its AGENTS.md <link> · How to deploy <link> · The evidence pack <link>

## 1. Owners, by name
| Loop | Owner | Backup | How often |
|------|-------|--------|-----------|
| Runs the system | <operator> | <name> | daily |
| On call | <rota> | | |
| Cost per case, alert at <3x> the signed figure | <name> | | weekly |
| Drift, per slice | <name> | | weekly |
| The saving beside the spend, on one line | <name> | | each cycle |
| Incidents become next briefs | <name> | | each incident |

## 2. Switches, timed before cut-over
| Switch | What it does | Time | Thrown by, in rehearsal | Date |
|--------|--------------|------|-------------------------|------|
| Kill switch | every case to the desk, with its context | <40 s> | <name> | |
| Flag to shadow, per action | decides, acts on nothing | <2 min> | | |
| Prompt rollback | the previous version, on the next case | <3 min> | | |
| Model rollback | redeploys the runtime; the harness re-runs | <11 min> | | |

## 3. Runbooks, each run once by its owner
| Event | How you can tell | First switch | Run by, date |
|-------|------------------|--------------|--------------|
| Drift alert | | | |
| Cost spike | | | |
| A tool is down | | | |
| The model version changes | | | |
| A disputed refund | | | |

## 4. Where each action stands
| Action | Shadow · 5% · wider · all | The evidence for it | What earns the next step |
|--------|---------------------------|---------------------|--------------------------|

## 5. Open risks
| Risk | Owner | Review by |
|------|-------|-----------|

## 6. Accepted
I can run this system without <FDE>, and I accept it from <date>.
<the person who will run it> · <role> · <date>
Delivered as <statement of work, section> says: <their sponsor> · <date>
<FDE> is on call to <name> until <date>, for questions, not for the system.
"""},
 "prompts": [
   {"title": "Draft the runbook for a drift alert from the code and the dashboards",
    "when": "Before the rehearsal, one runbook at a time",
    "body": """Draft the runbook for a drift alert on <system>, for <their operator>, who did not
build it. You have the alert's definition, the dashboard queries, the switches with
their rehearsed times, and the code paths the alert names: <paste>.

Sections, in this order, one page at most:
1. What fired, and what it means, in their words, not ours.
2. Real shift or noise: the slice, the sample size, the window to compare against.
3. The first switch to throw, and its rehearsed time.
4. Who to tell, by role, and what to send them.
5. How to know it is over, and what goes into the next brief.

RULES:
- Copy every command from the code or the rehearsal notes. Mark anything inferred TO CHECK.
- No step may need the person who built it. If one does, list it at the top as a gap."""},
   {"title": "Find what the handover pack does not cover",
    "when": "A week before the handover is signed",
    "body": """Here is the handover pack for <system> at <customer>, and everything that has happened
in the system so far: incidents, alerts, changes and questions from their staff. <paste>

Read the pack as their operator on the first night alone, and list every gap:
| Situation | Where the pack should cover it | What is missing | Who at <customer> should own it |

Then answer yes or no, with the evidence:
- Does every loop (running, on call, cost, drift, incidents, the next brief) have a named owner?
- Has every switch been thrown, and timed, by someone other than its author?
- Can every runbook be followed without contacting us?
- Is the date our access ends written down?

Do not soften a gap because it is unlikely. Unlikely is what runbooks are for."""},
 ],
 "example": {
   "title": "SkyWays · days 45 to 97, four switches and a signature",
   "body": "**In the case:** before cut-over the on-call engineer threw all four switches with a "
           "stopwatch: kill switch 40 seconds, flag to shadow 2 minutes, prompt rollback 3 minutes, model "
           "rollback 11 minutes. At cut-over the flag went to 5% for same-day changes only; partner "
           "rebooking stayed in shadow another fortnight. On day 82 a $2,000 refund went out that was not "
           "owed, and the room asked only which switch: refunds went back to gated in two minutes while "
           "the rest kept running. **Your move:** the incident goes into the handover pack, not around it. "
           "The control, the six new golden cases and the next brief each get an owner on their side. On "
           "day 97 Lena, their platform lead, signs the checklist as the person who will run it, and your "
           "access ends that day."},
 "pitfalls": [
   "Widening on a date. The calendar says week six, the evidence says not yet, and the share that widens "
   "is the one nobody can defend after the first incident.",
   "Handing over to the sponsor instead of the operator. The sponsor signs and is never paged; the person "
   "who is paged meets the system at its first alert.",
   "Runbooks nobody has run. They read well and fail at the first step their author knew by heart.",
 ],
 "done_when": "Their operator has thrown every switch and run every runbook without you, every loop has a "
              "named owner on their side, the checklist is signed by the person who will run it, and your "
              "access ended on the agreed date.",
},
]
