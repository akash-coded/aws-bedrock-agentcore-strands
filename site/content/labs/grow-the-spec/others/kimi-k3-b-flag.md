**1 · Title**
Rebooking assistant — self-serve rebooking for disrupted SkyWays passengers (Owner: Priya, v1).

**2 · Value**
Cut the rebooking decision from a 38-minute average to minutes; most of the 240 cases/day closed with no agent. Measured baseline: $9.40/case (Q2 ticket export). 11% of cases are codeshare.

**3 · Acceptance criteria**
- Passenger sees ranked alternative flights within 30 seconds.
- Same-day SkyWays rebooking completes when the passenger accepts.
- Rebooks onto a partner (codeshare) flight when no SkyWays seat exists.
- Offers a refund when no acceptable flight exists; refunds over $400 only with a named person's approval.
- Hands the case to a contact-centre agent when it cannot finish.
- Goals as stated: decision in "minutes, not 38"; "most" cases need no agent — PRD gives no number for either.
- Out of scope: compensation claims, group bookings.

**4 · The model's role**
NOT DECIDED: for each of the five steps — ranking alternatives, same-day rebook, codeshare rebook, refund offer, hand-off decision — which does a model decide and which are exact code? The PRD describes behaviors but assigns none to a model or to deterministic code. PRD names no owner for this question; an owner must be assigned.

**5 · Autonomy**
- Show ranked options: acts alone — PRD flow has no approval step.
- Same-day SkyWays rebook: passenger approves (executes "when the passenger accepts").
- Codeshare rebook: NOT DECIDED: PRD says it rebooks onto a partner when no SkyWays seat exists, but does not say whether passenger acceptance or any other approval is required. Who should answer: no owner named in PRD.
- Refund ≤ $400: NOT DECIDED: PRD says it "offers" a refund and Finance caps it at $400 — it does not say whether the system executes alone at/under the cap or whose acceptance completes it. Who should answer: no owner named in PRD.
- Refund > $400: requires approval from "a named person" — NOT DECIDED: who that named person is. Who should answer: no owner named in PRD (the cap is Finance's).
- Hand-off to agent: acts alone — PRD: hands over "when it cannot finish."

**6 · The bar**
NOT DECIDED: how right it must be, overall or per kind of case (SkyWays rebook / codeshare / refund / hand-off) — stated open question: "one number, or one for each kind of case?" Who should answer: Priya, with Maya (QA).

**7 · Fallback**
- Cannot decide / cannot finish: hand the case to a contact-centre agent (stated in PRD).
- Fare engine down: NOT DECIDED: what happens to the case. Who should answer: Arjun (architecture) — stated open question.
- Other tool failures: NOT DECIDED: PRD addresses only the fare engine; behavior when any other tool fails is unspecified. Who should answer: no owner named in PRD.

**8 · Records**
NOT DECIDED: what is logged for each action (options shown, rebook, codeshare rebook, refund offer/approval, hand-off) and how long records are kept — stated open question. Who should answer: compliance (no reply yet).