# Product Requirements Document · Rebooking Assistant
Owner: Priya (Product) · Version 1.0

## 1. Problem Statement
Disrupted passengers currently wait an average of 38 minutes for a rebooking decision. With 240 daily cases (11% complex codeshares) and a measured operational cost of $9.40 per case, the current manual process is inefficient, expensive, and damages customer satisfaction.

## 2. Objectives
- Reduce average passenger wait time from 38 minutes to under 10 minutes.
- Decrease operational cost by achieving >70% automation rate (no agent touch).
- Maintain accuracy with a rebooking error rate of <1%.

## 3. Target Users
- **Passengers:** Customers with cancelled flights or missed connections due to delays.
- **Agents:** Contact-centre staff who handle complex exceptions and escalations.

## 4. Functional Requirements
**4.1. Eligibility & Search**
- System must identify stranded passengers automatically upon flight cancellation/delay events.
- Algorithm must rank available alternatives by arrival time, minimizing connection friction.
- Must validate new flight eligibility (same-day, same-origin/destination).

**4.2. Execution (Automation)**
- Automatically rebook passengers on confirmed alternative flights.
- Send updated boarding pass and itinerary via email/SMS immediately upon rebooking.
- **Scope:** Fully automatable for all airline-operated flights.

**4.3. Partner & Codeshare Logic**
- Attempt rebooking on partner flights where interline agreements permit.
- If partner API is unavailable or rules are restrictive, route to agent queue immediately.

**4.4. Refunds**
- Offer a full refund or travel voucher when no same-day flight options exist.
- Refund offer triggers only when passenger-originated request or system detects >4 hour delay.

## 5. Non-Functional Requirements
- **Latency:** Search and offer generation must complete within 5 seconds.
- **Availability:** 99.9% uptime during operational hours.
- **Handover:** Context (search history, reason for failure) must populate agent screen upon escalation.

## 6. Constraints & Exclusions
- **Out of Scope:** Compensation claims (EU261/cash compensation), group bookings (>9 pax).
- **Limits:** Refunds capped according to Finance policy (pending confirmation).

## 7. Success Metrics (KPIs)
- **Primary:** Reduction in avg. time-to-solution (Target: <10 mins).
- **Secondary:** % of cases fully automated (Target: >70%).
- **Tertiary:** Agent override rate (Target: <5%).

## 8. Open Issues & Risks
- **Finance:** Pending decision on maximum refund cap amount.
- **Compliance:** Awaiting requirements for data logging retention period.