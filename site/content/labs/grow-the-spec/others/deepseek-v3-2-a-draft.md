**PRODUCT REQUIREMENTS DOCUMENT · Rebooking Assistant**  
**Owner:** Priya (Product) · **Version:** Final · **Date:** [Current Date]  

---

### **1. Problem**  
During operational disruptions, passengers experience excessive wait times—averaging **38 minutes**—for rebooking decisions. This impacts ~**240 cases daily** (11% codeshare), incurring an average measured cost of **$9.40 per case** (Q2 ticket export data). Manual processes burden contact-centre agents and degrade customer experience.

---

### **2. Objective**  
Create an automated assistant that provides stranded passengers with viable alternative flight options and executes rebookings upon acceptance. This will drastically reduce wait times, automate simple cases, and free agents to handle only complex exceptions.

**Success Metrics:**  
- Reduction in average rebooking decision time (>50%).  
- Increase in automated resolution rate (target: >70% of cases without agent).  
- Maintain error rate below 2%.

---

### **3. Target Users**  
- **Primary:** Passengers whose flights are cancelled or delayed past a connection window.  
- **Secondary:** Contact-centre agents, who intervene when the assistant cannot complete the rebooking.

---

### **4. Core Requirements**  

**4.1 Flight Search & Ranking**  
- System must source and rank available alternatives within **2 minutes** of disruption detection.  
- Prioritize: same-day flights > next available flights > partner options.  
- Default to highest ranked option; passenger may view alternatives.

**4.2 Automated Rebooking**  
- Execute same-day changes on own-metal flights automatically upon passenger acceptance.  
- For partner (codeshare) flights, rebook where API access and fare rules allow.  
- Provide clear summary of changes prior to confirmation.

**4.3 Refund Handling**  
- When no sensible flight exists within a 24-hour window, offer a refund option.  
- Refund offers will be capped (exact limit TBD—see Open Questions).  

**4.4 Escalation Path**  
- Hand off seamlessly to a live agent when:  
  - System confidence is below predefined threshold.  
  - Complex itineraries (multi-passenger linked records, premium cabins).  
  - Passenger requests agent assistance.

---

### **5. What “Good” Looks Like**  
- Passenger receives rebooking proposal in <5 minutes.  
- Majority of cases resolved without agent intervention.  
- High customer satisfaction (CSAT) and low processing errors.

---

### **6. Out of Scope**  
- Compensation/Voucher claims for delays.  
- Group bookings (>6 passengers).  
- Irregular operations outside of cancellations & missed connections.

---

### **7. Open Questions / Constraints**  
- **Finance:** Exact refund cap per case pending approval.  
- **Compliance:** Logging/audit requirements for automated changes still under review.  
- **Tech:** Codeshare partner API availability for certain carriers may limit automation rate.

---

### **8. Implementation Notes**  
- Initial rollout limited to direct and key partner routes.  
- Integration required with: Reservations (PSS), disruption detection system, and agent desktop tool.  
- UI must be mobile-responsive and accessible.

---

**Approvals:**  
Product: ____________________ · Tech: ____________________ · Legal/Compliance: ____________________