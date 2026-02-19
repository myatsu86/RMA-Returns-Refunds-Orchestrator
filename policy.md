# RMA Warranty Policy

This document defines the business rules for handling Returns, Refunds, and Warranty Replacements (RMA).

The policy engine evaluates requests in a predefined order to determine eligibility.

---

## 📌 Policy Overview

The system supports the following policy decisions:

- `REFUND_ELIGIBLE`
- `REPLACEMENT_ELIGIBLE`
- `REJECTED`

---

# 🟢 Policy 1 — Direct Store Return (Refund Eligible)

### Condition
- Purchase source is **Seagate Store**
- Request is within **30 days of delivery date**
- Product condition is **like-new**

### Outcome
- Full refund approved
- Refund processed within **30 days** of physical receipt
- Typically appears on original payment method within **7 days** after processing

### Requirements
- Customer must use **Seagate-provided return shipping label**
- Product must be in **original / like-new condition**
- No custom modifications allowed

---

# 🟡 Policy 2 — Post-30-Day Store Purchase (Warranty Only)

### Condition
- Purchase source is **Seagate Store**
- Request is **beyond 30 days** from delivery date

### Outcome
- Refund denied
- Eligible for **warranty replacement only** (if still within warranty period)

---

# 🔵 Policy 3 — Warranty Replacement (RMA)

### Condition
- Product is **within warranty period** (validated by serial number)
- **Hardware failure confirmed**

### Outcome
- Replace with:
  - New unit OR
  - Factory-certified replacement unit
- Customer pays **inbound shipping**
- Seagate covers **outbound replacement shipping**

### Requirements
- RMA number must be issued before return shipment
- Product must be in **standard configuration**
  - No custom labels
  - No non-standard parts
- Customer is solely responsible for:
  - Data backup
  - Data deletion before return

---

# 🔴 Policy 4 — Out of Warranty

### Condition
- Product is beyond warranty period
- AND beyond 30-day return window

### Outcome
- Request rejected
- No refund
- No replacement

---

# ⚠️ Policy 5 — Data Responsibility (Universal Policy)

This policy applies to **ALL return and RMA requests**.

### Rules
- Seagate bears **zero liability for data loss**
- Customer must:
  - Back up all data
  - Wipe the drive before shipping
- Customer must acknowledge data responsibility
  - Required at request creation time
  - Request cannot proceed without acknowledgment

---

# 🧠 Policy Evaluation Order

The rules engine evaluates policies in the following order:

1. **Data Responsibility Acknowledgment (Policy 5)**
   - If not acknowledged → `REJECTED`

2. **Policy 1 — Refund Check (Within 30 Days)**

3. **Policy 2 — Post-30-Day Store Check**

4. **Policy 3 — Warranty Replacement**

5. **Policy 4 — Out of Warranty Fallback**

---

# 🎯 Design Principles

- Deterministic rule evaluation
- Audit trail per policy decision
- Clear separation of refund vs warranty logic
- Compliance-first data protection handling

---

## 📌 Example Decision Outputs

| Scenario | Decision |
|----------|----------|
| Store purchase + 10 days + like-new | REFUND_ELIGIBLE |
| Store purchase + 45 days + under warranty | REPLACEMENT_ELIGIBLE |
| Under warranty + hardware failure | REPLACEMENT_ELIGIBLE |
| Out of warranty | REJECTED |
| Data not acknowledged | REJECTED |

---

