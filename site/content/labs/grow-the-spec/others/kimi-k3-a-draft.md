# PRD · Rebooking Assistant

**Owner:** Priya (Product) · **Status:** Draft for review · **Reviewers:** Contact-centre Ops, Finance, Compliance

## 1. Problem
Passengers disrupted by a cancellation or a missed connection wait an average of **38 minutes** for a rebooking decision. Volume is **~240 cases/day**, of which **11% involve codeshare segments**, and handling costs **$9.40/case** (Q2 ticket export) — roughly $2,250/day. Long waits drive poor CSAT and repeated contact; agents spend most of their time on routine changes.

## 2. Goals & success metrics
Baseline → target, measured on resolved cases. *Targets are proposals pending Ops sign-off.*

| Metric | Baseline | Target (proposed) |
|---|---|---|
| Median time from disruption detection to confirmed decision | 38 min | < 10 min |
| Cases resolved with no agent | ~0% | ≥ 70% |
| Error rate (wrong booking / wrongful refund) | — | < 1% of automated cases |
| Cost per case | $9.40 | ≤ $4.00 |
| Codeshare cases rebooked automatically or handed off cleanly | — | 100% (no dead ends) |

## 3. Users
- **Primary:** passengers whose flight is cancelled or delayed enough to break a connection.
- **Secondary:** contact-centre agents, who receive handoffs with full context and handle only cases the assistant cannot finish.

## 4. Scope
**In:** automated alternative-search, same-day rebooking on own flights, codeshare rebooking where partner systems allow, refund offer when no sensible alternative exists, agent handoff. **Out:** compensation claims (e.g., EU261), group bookings.

## 5. Functional requirements
- **FR-1 Eligibility.** Detect passengers on cancelled flights or delays that will cause a missed connection; trigger outreach proactively (app / SMS / email).
- **FR-2 Search & rank.** Search own + partner inventory; rank by earliest arrival, respecting cabin, minimum connection times, and baggage feasibility.
- **FR-3 Offer.** Present up to 3 options with trade-offs (arrival time, connections, cabin) plus a refund option.
- **FR-4 Rebook (own metal).** On explicit passenger acceptance, rebook and reissue for same-day travel on own flights; send confirmation with the new itinerary.
- **FR-5 Codeshare.** Rebook via partner where we hold ticketing authority; otherwise hand off with full context (covers the 11% of cases with codeshare segments).
- **FR-6 Refund.** Offer a refund when no sensible alternative exists, capped at **[amount TBD — Finance]**. "Sensible alternative" (max arrival delay, max connections) needs an Ops definition.
- **FR-7 Handoff.** Route to the agent queue with case summary, options already shown, and the passenger's responses; the passenger never repeats information.
- **FR-8 Audit.** Log every offer, choice, and ticket/refund action (who/what/when). Final logging list pending Compliance.

## 6. Non-functional
Options returned within 60s of eligibility; resilient during irregular-operations peaks (≥10× normal case volume); integrates with reservation/ticketing and notification systems.

## 7. Guardrails & risks
- No ticket change or refund without explicit passenger confirmation — a wrong rebooking is the costliest failure mode.
- Codeshare failures must never dead-end; clean handoff is mandatory (protects agent load).
- Refund exposure controlled by the cap plus full audit trail.

## 8. Rollout
1. **Pilot:** own-metal same-day rebooking only (~89% of cases), with agent spot-review of automated decisions.
2. Add codeshare handling and refund offers.
3. Add proactive outreach. Exit criteria per phase: error rate < 1%, CSAT at or above agent-handled baseline.

## 9. Open questions
1. Refund cap amount — **Finance** (blocking FR-6).
2. Required logging and retention — **Compliance**, no response yet (blocking FR-8; escalate).
3. Definition of "sensible alternative" — **Ops**.
4. Auto-handoff triggers for special-service passengers (unaccompanied minors, mobility assistance) — **Ops**.
5. Sign-off on Section 2 targets — **Ops + Finance**.

*Word count is calibrated to fit one page; tighten Sections 5–6 first if space runs short.*