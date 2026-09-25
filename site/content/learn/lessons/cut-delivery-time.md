---
title: Cut Delivery from Months to Weeks: What Shrinks, What Won't
short: Cut delivery from months to weeks
wiki: How-to-Cut-Delivery-from-Months-to-Weeks
description: AI makes building fast; delivery is more than building. What compresses, what compresses only by design, what never compresses, with the arithmetic for each.
dek: The claims say days instead of months. Some of it is true. The rest is where your programme will actually spend its time.
level: Intermediate
keywords: reduce time to market AI, faster software delivery with AI, shorten development cycle, AI productivity delivery time, months to weeks, lead time reduction, value stream AI development
updated: 2026-09-24
---

> [!TIP]
> **The answer in one sentence.** AI shortens the time to *build* dramatically, but delivery also
> includes deciding, reviewing, proving and waiting for evidence, so the programmes that go from
> months to weeks are the ones that also redesign those: decisions made per action, review routed by
> risk, work cut so it integrates daily, lead-time items started on day one, while accepting that
> live evidence still arrives at the speed of traffic.

{{map:cut-delivery-time}}

**In this lesson** you'll learn:

- where the time actually goes in an agentic delivery, once building is fast;
- the four waits you can remove by redesign, and the arithmetic for each;
- the two waits you cannot remove, and how to plan around them honestly.

## Sound familiar?

- The agent wrote the feature in two days; the feature launched in three months.
- Every change waits four days for a review, and the answer proposed is another reviewer.
- A launch date was promised before anyone divided the cases needed by the cases seen per day.

AI has moved the bottleneck, not removed it. The time has gone to the parts of delivery that nobody
redesigned.

## Where does the time go?

Vendor claims are real about building. AWS describes AI-DLC delivering tasks "in hours or days that
previously took weeks". But research on AI in software delivery is consistent on the rest: DORA's
2025 report found that AI **amplifies** an organisation's existing strengths and weaknesses, and that
speed without stability produces problems faster; METR's 2025 trial found experienced developers
believed they were faster while measuring slower. The throughput of a delivery system is set by its
slowest step: and once AI writes the code, the slowest step is somewhere else.

## Cut the waits, step by step

### Step 1 · Map the flow and time each wait

List every step from request to live (framing, spec, decision, build, review, test, shadow, cut-over) and measure the waiting as well as the working. The build is usually the smallest number on the map.

### Step 2 · Decide per action, not per system

The slowest waits are often decisions. At SkyWays three executives argued for two weeks about how much
"the assistant" should do; recast as four actions, each with a reversibility, the decision took twenty
minutes. Nothing about AI shortened that, the structure of the question did. [Autonomy per action](lesson:p0-frame#step-4--set-autonomy-one-action-at-a-time)

### Step 3 · Route review by risk band

Review capacity is fixed by people, so the only lever is how much review each change needs. Queue time
is slots needed divided by slots cleared per day. Nine changes needing two readers each is 18 slots; at
4.5 a day, that is four days. Routing readers by the risk band of what each change touches cut it to 7
slots and **1.6 days**: a 61% cut with nobody reading faster. [Review by risk](lesson:review-ai-generated-code)

### Step 4 · Cut the work so it integrates every day

A plan ordered by priority makes day three wait for day seven. A plan cut by dependency (walking
skeleton first, one unknown per bolt) lets every bolt be built and integrated on its day, so evidence
arrives daily instead of at a sprint demo. [Bolts vs sprints](lesson:bolts-vs-sprints)

### Step 5 · Start the lead-time items on day one

Some waits sit in someone else's queue: model access, which is granted per model and per region, on
request; security reviews; data-export approvals. SkyWays lost six days nobody had planned: model
access had been granted in one region in week one, everyone assumed that covered the account, and
nobody had requested the region the data had to stay in. Request every one in week one, even if the
work that needs it is weeks away.

### Step 6 · Plan honestly around what does not compress

Live evidence arrives at the speed of traffic: **days = cases needed ÷ (share × cases per day)**. At
240 cases a day, 500 cases at a 5% canary takes 42 days, the arithmetic, not the effort. You can
shorten it only by widening the share, which raises exposure, or by needing fewer cases, which only an
honest bar and lower bound can justify. Put the number in the plan instead of promising around it.

## Where you'll use it

- **Before promising a launch date**: compute the evidence days first.
- **When a programme "stalls" after a fast build**: map the waits; the stall is a queue, not a team.
- **When someone proposes hiring more reviewers**: count the slots and route by band first.

## Why it matters

Programmes that take the build speed-up and leave the rest of the flow untouched ship the same date
with more rework. The ones that go from months to weeks redesign the waits, and plan openly around
the two that no redesign removes, which is what keeps the date credible.

## Try it

A programme expects 200 cases a day. It needs 400 cases of live evidence before widening past its
canary, and plans a 10% canary. The build is estimated at two weeks. **What is the shortest honest
time from start of build to widening?**

<details><summary>Show the answer</summary>

**About five weeks, plus the shadow window.** The build takes two weeks, fourteen days. The canary then
needs 400 ÷ (10% × 200) = **20 days** of live traffic, longer than the build, so 34 days in all. With a shadow window fixed in
advance before the canary, the evidence phases are the long pole, not the code. A 20% canary would
halve the 20 days at twice the exposure; the build cannot be made fast enough to matter.

</details>

## Key takeaways

1. AI **compresses building**; delivery is building plus deciding, reviewing, proving and waiting.
2. **Four waits shrink by redesign**: decide per action, route review by band, integrate daily, start lead times on day one.
3. **Live evidence never shrinks by effort**: compute its days and put them in the plan.

## FAQ

### How can AI reduce software delivery time?

By making the building fast, and then only if the rest of the flow is redesigned to match: decisions
framed per action, review routed by risk, work cut so it integrates daily, and lead-time approvals
started early. Without those, faster code joins a longer queue.

### Can AI cut delivery from months to weeks?

Often, for the building and the waits that can be redesigned. What it cannot shorten is the time it
takes live traffic to produce enough evidence that an AI feature is good enough to widen. That is set
by volume and the share of traffic you expose, and should be planned rather than hoped away.

### What is the biggest bottleneck in AI-assisted development?

Usually review. When agents write code quickly, reading it becomes the scarce resource; a review
policy that treats every change as equally dangerous creates a queue that no amount of coding speed
can shorten.

### Why did our AI project take longer than expected?

Most often because the time went to waits the build speed-up did not touch: a decision nobody owned, a
review queue, a model-access request made late, or a canary that needed more live evidence than the
traffic could supply in the time promised.

## Apply it in your role

| If you are… | Do this | The AI-augmented shortcut |
| --- | --- | --- |
| **A forward-deployed engineer** | Time the waits at the customer before promising speed. Access requests, reviews, approvals and evidence windows are usually most of the calendar. | Ask a model to build a wait map from the customer's ticket timestamps. |
| **A product manager or FDPM** | Promise weeks only once the lead-time items started on day one: model access, data access, security review. | Have a model draft the day-one requests, each with an owner and an expected lead time. |
| **A GenAI or agentic AI engineer** | Cut integration waits with daily merges and review routed by risk band. | Ask a coding agent to add the path rule that routes review by band. |

**Across the enterprise.** The biggest compression is organisational. Pre-approved patterns (a landing
zone, a gateway, a security review template) make the second project far faster than the first.

**The ten-minute workflow.** Find where the calendar actually goes:

```text
Here are the timestamps of our last three AI features, from request to production: <paste>. Split the
elapsed time into building, deciding, reviewing, waiting for access and waiting for evidence. Show the
split per feature, and the single wait that saves the most calendar time if it is halved.
```

## Sources and credits

| Idea | Origin | Source |
| --- | --- | --- |
| "Tasks in hours or days that previously took weeks" | **Borrowed** | Raja SP (2025). [AI-Driven Development Life Cycle](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle). AWS |
| AI amplifies strengths and weaknesses; speed without stability | **Borrowed** | DORA (2025). [State of AI-assisted Software Development](https://dora.dev/dora-report-2025/) |
| Believing faster, measuring slower | **Borrowed** | METR (2025). [Measuring the impact of early-2025 AI on experienced open-source developer productivity](https://arxiv.org/abs/2507.09089) |
| The slowest step sets the throughput | **Borrowed** | Goldratt, E. M. & Cox, J. (1984). *The Goal*. North River Press |
| Mapping the waits in a flow | **Borrowed** | Rother, M. & Shook, J. (1999). *Learning to See*. Lean Enterprise Institute |
| Queue time = slots needed ÷ slots per day | **Borrowed** | Little, J. D. C. (1961). *Operations Research* 9(3) |
| Days of live evidence, and the three bands of wait | **Original**: this playbook | [Formulas](wiki:Formulas-and-Calculators#days-of-live-evidence--working-method) |
| The SkyWays figures | **Illustrative**: a fictional airline | [Try the cut-over calculator](sim:#/toolkit/cutover) |
