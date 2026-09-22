# How to run a missing-control postmortem

A $2,000 refund went out that was not owed. The room is tense, and somebody has already opened the
commit history to find out who wrote the prompt.

You have one hour. Five moves.

This closes the [incident loop](The-Eight-Loops#incident), which closes into **P0**. A postmortem that
does not produce a brief has not finished.

---

## 1 · Ask the right question first

| The question | What the hour becomes |
| --- | --- |
| "Who wrote this prompt, and who approved it?" | A name within five minutes, and fifty-five minutes of that person's defence. The refund tool still accepts any amount |
| **"Which enforced control would have made this impossible?"** | The room lists the layers, classifies each, and finds the two that were absent |

The second question points at the system. It is also the only one that produces a fix.

> Blameless is not a courtesy. It is the only framing under which people tell you what actually
> happened.

---

## 2 · Classify every layer: enforced, a request, or absent

List the layers the design *claimed* to have. Then be honest about each one.

| Layer | Claimed | Reality | Would it have stopped the money? |
| --- | --- | --- | --- |
| Input marked as data | yes | **absent** | No |
| The prompt's policy | yes | **a request** | No |
| A $400 cap | yes | **absent from the code** | **Yes** |
| A named approver | yes | **absent from the code** | **Yes** |
| An alert on the trace | yes | **absent** | No — it reports afterwards |

Five layers, and **none was enforced**. Two of them were written down — in the prompt. That is why
"we had a cap" felt true to everyone in the room and was not true in the ledger.

**A rule that exists only in a prompt is a request, and a model can be talked past a request.**

The reconstruction that settles it: with *either* the cap or the approver enforced, the refund is
impossible. Both were off. Injection defence and traces would not have stopped the money moving —
they change the odds and the visibility, not the outcome.

---

## 3 · Choose the fix that closes the path

| Proposal | Verdict |
| --- | --- |
| Rewrite the prompt so the cap is unmistakable | Lowers the probability again and leaves the path open. The next attack is worded differently |
| Add an alert so we hear about it faster | Useful, and it is detection, not prevention |
| **A cap and a confirmation token in the tool's signature** | `issue_refund` now raises above $400 and refuses any call without a token only the approver's screen can mint |

The test for a proposed fix: **does it close the path, or does it lower the probability?** Both have a
place. Only one of them ends the incident class.

---

## 4 · Lower the autonomy level, and say why

Refunds were at level 2: the agent acts and a person reviews afterwards.

| Option | Reality |
| --- | --- |
| Stay at level 2, the hole is closed | The fix probably holds, and nobody in the room has tested it. The decision rests on confidence |
| **Down to level 1 until a 14-day shadow run passes** | A fix is a claim until it is proven. One level down costs a little speed for two weeks and buys the evidence that restores the level |

**A fix is a claim until it has been proven.** Dropping a level after an incident is the system
working, not a punishment — and it is what makes the later restoration credible.

---

## 5 · Feed it forward into the next P0

A summary to leadership closes the matter and teaches nothing. The same attack then works on the next
tool that moves money.

Four artefacts leave the room:

| Artefact | Content |
| --- | --- |
| **Golden-set cases** | Six new cases, so the attack becomes a weekly test |
| **An amended ADR** | ADR-003 now states that *enforced* means **in the tool's signature** |
| **A lowered autonomy record** | Level 1 on refunds, with the condition for restoring it |
| **A P0 brief** | Refunds become their own slice, with their own bar and their own hold |

The brief is the output that matters, and it has the same five parts every time:

```
NEXT P0 · refunds as their own slice

Pain       money left the business without an enforced control
Evidence   trace 2026-04-14T09:22Z, refund $2,000, no approver, no cap
Finding    cap and approver both absent from the code; the prompt carried both
Fix        typed bounded parameter + confirmation token; approver on every refund
Value      this class of incident becomes impossible, not less likely
```

---

## The template

```
INCIDENT ·

1 · The question
    Which enforced control would have made this impossible?

2 · Layers            claimed | enforced / request / absent | would it have stopped it?
    ...

3 · Fix               closes the path (not: lowers the probability)

4 · Autonomy          level now | level after | condition to restore

5 · Feed forward      golden cases | amended ADR | autonomy record | P0 brief
```

---

## Try it

**Exercise.** Take your last incident, whatever it was, and rewrite it in this shape. Do not skip the
layer table.

<details>
<summary>What the exercise usually surfaces</summary>

**A control everyone believed was enforced and was a request.** This is the single most common
finding, and it is not a competence problem: a rule written clearly in a prompt reads exactly like a
rule, and nothing in a code review flags it as unenforced.

**A layer counted twice.** "We have the prompt rule and the guidance in the runbook" is one layer, not
two, because they fail together.

**Detection mistaken for prevention.** An alert on the trace is genuinely valuable and it would not
have stopped the money. Put it in the table and mark it honestly; the table is the artefact that keeps
the distinction visible.

If your write-up produces a control, a record and a brief, you ran a postmortem. If it produced a
name, you ran a meeting.
</details>

---

**Next:** [How to Hold the Security Boundary](How-to-Hold-the-Security-Boundary) ·
[Role: Sponsor](Role-Sponsor) · [The Eight Loops](The-Eight-Loops) · [Anti-Patterns](Anti-Patterns)
