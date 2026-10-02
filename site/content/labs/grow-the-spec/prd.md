# PRD · Rebooking assistant
Owner: Priya (product) · Version 1

## Problem
Disrupted passengers wait an average of 38 minutes for a rebooking decision. 240 cases a day; 11% are codeshare. Measured cost: $9.40 a case (Q2 ticket export).

## Users
Passengers whose flight is cancelled, or delayed past a connection. Contact-centre agents take over when the assistant cannot finish.

## What it does
1. Offers ranked alternative flights. A passenger sees options within 30 seconds.
2. Rebooks a same-day change on a SkyWays flight when the passenger accepts.
3. Rebooks onto a partner (codeshare) flight when no SkyWays seat exists.
4. Offers a refund when no acceptable flight exists. Finance caps a refund at $400 unless a named person approves more.
5. Hands the case to an agent when it cannot finish.

## What good looks like
A passenger gets a decision in minutes, not 38. Most cases need no agent.

## Out of scope
Compensation claims. Group bookings.

## Open questions
- How right must it be before launch: one number, or one for each kind of case? Owner: Priya, with Maya (QA).
- What must be logged for each action, and for how long? Owner: compliance. No reply yet.
- What happens to a case when the fare engine is down? Owner: Arjun (architecture).
