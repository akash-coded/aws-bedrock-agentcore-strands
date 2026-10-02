**1 Title**
Rebooking assistant

**2 Value**
Reduces average rebooking time from 38 minutes to a few minutes; lowers cost from $9.40 per case; handles 240 daily cases including codeshares with minimal agent involvement.

**3 Acceptance criteria**
1. Passenger sees ranked alternative flight options within 30 seconds.
2. Assistant rebooks same-day changes on SkyWays flights when accepted by passenger.
3. Assistant rebooks onto partner (codeshare) flights when no SkyWays seat exists.
4. Assistant offers a refund (capped at $400) when no acceptable flight exists.
5. Assistant hands the case to a human agent when it cannot finish.
6. Compensation claims and group bookings are not handled.

**4 The model's role**
NOT DECIDED: Which specific steps involve a probabilistic model decision versus exact code execution? (Owner: Priya/product to define technical design).

**5 Autonomy**
NOT DECIDED: For each rebooking action (SkyWays, codeshare, refund under $400), may the assistant act alone, or is approval required from the passenger or a human agent? (Owner: Priya/product to define operational rules).

**6 The bar**
NOT DECIDED: How often must the assistant be right before launch, and is this a single metric or distinct accuracy targets for each kind of case (SkyWays, codeshare, refund)? (Owner: Priya with Maya (QA)).

**7 Fallback**
NOT DECIDED: What happens to a case when the fare engine is down? (Owner: Arjun (architecture)).
*Note: The PRD explicitly states the assistant hands the case to an agent when it cannot finish, but does not specify if this applies to specific tool failures like the fare engine.*

**8 Records**
NOT DECIDED: What specific data must be logged for each action, and for how long must it be retained? (Owner: Compliance).