**1 Title**  
Rebooking Assistant

**2 Value**  
Reduce average rebooking decision time from 38 minutes to minutes for 240 daily disrupted passengers, lowering per-case cost from $9.40.

**3 Acceptance criteria**  
- Passenger sees ranked alternative flight options within 30 seconds.  
- Can rebook onto a same-day SkyWays flight upon passenger acceptance.  
- Can rebook onto a codeshare partner flight when no SkyWays seat exists.  
- Can offer a refund (capped at $400) when no acceptable flight exists.  
- Hands case to contact-centre agent when it cannot finish.  
- Does not handle compensation claims or group bookings.

**4 The model's role (which steps a model decides, which are exact code)**  
NOT DECIDED: Which specific decisions (e.g., ranking flights, selecting partner flight, refund eligibility) are made by a model vs. determined by exact code? Owner: Priya/Architecture.

**5 Autonomy (for each action: may it act alone, or who approves)**  
- Offer ranked alternative flights: May act alone.  
- Rebook same-day SkyWays flight: May act alone upon passenger acceptance.  
- Rebook onto partner codeshare flight: NOT DECIDED: May it act alone, or is manual approval required? Owner: Priya.  
- Offer refund up to $400: May act alone.  
- Offer refund above $400: NOT DECIDED: Which named person must approve? Owner: Priya.  
- Hand case to agent: May act alone.

**6 The bar (how often it must be right, for each kind of case)**  
NOT DECIDED: One overall accuracy target, or separate targets for each case type (e.g., SkyWays rebooking, partner rebooking, refund)? Owner: Priya with Maya (QA).

**7 Fallback (what happens when it cannot decide or a tool fails)**  
- When it cannot finish: Hands case to contact-centre agent.  
- When fare engine is down: NOT DECIDED: What is the fallback action or state? Owner: Arjun (architecture).

**8 Records (what is written down for each action)**  
NOT DECIDED: What specific data must be logged for each action, and what is the retention period? Owner: Compliance.