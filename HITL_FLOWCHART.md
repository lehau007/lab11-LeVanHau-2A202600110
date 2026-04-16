# HITL Decision Points - Visual Flowchart

## Overview

This document provides visual flowcharts for the 3 HITL decision points designed in TODO 13.

---

## Decision Point 1: High-Value Money Transfer (Human-in-the-Loop)

```
┌─────────────────────────────────────────────────────────────┐
│  Customer Request: Transfer Money                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Check Amount │
              └──────┬───────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    < 100M VND              ≥ 100M VND
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ Check Recipient │    │ BLOCK & ESCALATE│
└────────┬────────┘    │ to Human Agent  │
         │             └─────────────────┘
    ┌────┴────┐                 │
    │         │                 ▼
    ▼         ▼          ┌──────────────────┐
 Known    New/Intl       │ Human Agent:     │
 Account   Account       │ 1. Verify ID     │
    │         │          │ 2. Call customer │
    ▼         ▼          │ 3. Check history │
┌────────┐ ┌────────┐   │ 4. Fraud check   │
│ AUTO   │ │ BLOCK  │   └────────┬─────────┘
│ APPROVE│ │ ESCALATE│           │
└────────┘ └────┬───┘      ┌─────┴─────┐
                │          │           │
                └──────────┤           │
                           ▼           ▼
                      ┌─────────┐ ┌─────────┐
                      │ APPROVE │ │ REJECT  │
                      └─────────┘ └─────────┘
```

**Trigger**: Transfer amount ≥ 100,000,000 VND OR international transfer

**HITL Model**: Human-in-the-Loop (blocking - transaction cannot proceed without human approval)

**Context Provided to Human**:
- Transfer amount and currency
- Destination account details (name, bank, country)
- Customer account history (tenure, typical transaction patterns)
- Recent transaction history (last 30 days)
- Fraud risk score from ML model
- Customer verification status (KYC level)
- Source of funds declaration (if required)

**Example Scenario**:
> Customer "Nguyen Van A" requests to transfer 250,000,000 VND to a new international account in Singapore that they've never sent money to before. The system immediately blocks the transaction and routes it to a human agent. The agent:
> 1. Calls the customer to verify the transaction
> 2. Asks about the purpose (business payment, family support, etc.)
> 3. Checks if the amount is consistent with customer's income/business
> 4. Verifies the recipient details
> 5. Approves or rejects based on holistic assessment

---

## Decision Point 2: Sensitive Personal Data Changes (Human-on-the-Loop)

```
┌─────────────────────────────────────────────────────────────┐
│  Customer Request: Change Personal Information               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Analyze Change Request│
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   Single Change          Multiple Changes
   (email OR phone)       (email AND phone)
         │                       │
         ▼                       ▼
   ┌──────────┐           ┌──────────┐
   │ Check    │           │ HIGH     │
   │ Context  │           │ RISK     │
   └────┬─────┘           └────┬─────┘
        │                      │
   ┌────┴────┐                 │
   │         │                 │
   ▼         ▼                 │
Same      New Device/          │
Device    Location             │
   │         │                 │
   ▼         ▼                 ▼
┌──────┐ ┌────────────────────────┐
│ALLOW │ │ ALLOW but FLAG for     │
│      │ │ Human Review (24h)     │
└──────┘ └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │ Human Analyst:     │
         │ 1. Review activity │
         │ 2. Check IP/device │
         │ 3. Call old phone  │
         │ 4. Verify identity │
         └────────┬───────────┘
                  │
            ┌─────┴─────┐
            │           │
            ▼           ▼
       ┌─────────┐ ┌─────────┐
       │ CONFIRM │ │ REVERT  │
       │ CHANGES │ │ & LOCK  │
       └─────────┘ └─────────┘
```

**Trigger**: Request to change email, phone number, address, or security questions - especially if multiple changes requested simultaneously

**HITL Model**: Human-on-the-Loop (non-blocking - changes take effect immediately but human reviews within 24 hours)

**Context Provided to Human**:
- Requested changes (old → new values)
- Current customer information
- Login location and IP address
- Device fingerprint (new vs known device)
- Time since last similar change
- Authentication method used (password, 2FA, biometric)
- Recent account activity (last 7 days)

**Example Scenario**:
> Customer logs in from a new device (never seen before) and requests to change both email address and phone number. The AI processes the request immediately (changes take effect), but flags it for human review. Within 24 hours, a human analyst:
> 1. Reviews the login pattern (new device, unusual location)
> 2. Checks if there were other suspicious activities
> 3. Calls the customer at their OLD phone number to verify
> 4. If customer confirms: no action needed
> 5. If customer denies or unreachable: revert changes and lock account

---

## Decision Point 3: Edge-Case Loan Application (Human-as-Tiebreaker)

```
┌─────────────────────────────────────────────────────────────┐
│  Customer: Apply for Business Loan                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ AI Automated Scoring  │
         │ (Credit, Income, DTI) │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   Score ≥ 85%            Score ≤ 60%
   (High Conf)            (Low Conf)
         │                       │
         ▼                       ▼
   ┌──────────┐           ┌──────────┐
   │ AUTO     │           │ AUTO     │
   │ APPROVE  │           │ REJECT   │
   └──────────┘           └──────────┘
   
                     │
                     ▼
              Score 60-85%
              (Medium Conf)
                     │
                     ▼
         ┌───────────────────────┐
         │ ROUTE TO HUMAN        │
         │ LOAN OFFICER          │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Human Loan Officer:   │
         │ 1. Review AI reasoning│
         │ 2. Check business plan│
         │ 3. Analyze cash flow  │
         │ 4. Interview applicant│
         │ 5. Compare similar    │
         │    cases              │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   ┌──────────┐           ┌──────────┐
   │ APPROVE  │           │ REJECT   │
   │ (Human   │           │ (Human   │
   │ Decision)│           │ Decision)│
   └──────────┘           └──────────┘
```

**Trigger**: Loan application with unusual characteristics:
- Very high amount relative to income
- Inconsistent employment history
- Borderline credit score (680-720)
- First-time borrower requesting large amount
- Self-employed with <3 years business history

**HITL Model**: Human-as-Tiebreaker (AI makes recommendation, human makes final decision for borderline cases)

**Context Provided to Human**:
- Loan amount requested
- Applicant income and employment history
- Credit score and credit report summary
- Debt-to-income ratio
- Collateral details (if applicable)
- AI's confidence score and reasoning
- Similar approved/rejected cases for comparison
- Business plan (for business loans)
- Cash flow statements (last 12 months)

**Example Scenario**:
> A self-employed applicant with 2 years of business history applies for a 500,000,000 VND business loan. Credit score is 695 (borderline). The AI's automated scoring gives 72% approval confidence - not high enough to auto-approve (≥85%), not low enough to auto-reject (≤60%). 
>
> The application is routed to a human loan officer who:
> 1. Reviews the AI's reasoning (why 72%?)
> 2. Examines the business plan in detail
> 3. Analyzes cash flow statements for the last 12 months
> 4. Interviews the applicant to understand business viability
> 5. Compares with similar cases (approved/rejected)
> 6. Makes final decision based on holistic assessment
>
> Decision: APPROVE with conditions (lower amount or require additional collateral)

---

## HITL Model Comparison

| Model | Blocking? | When to Use | Example |
|-------|-----------|-------------|---------|
| **Human-in-the-Loop** | ✅ Yes | High-risk, irreversible actions | Money transfers >100M VND |
| **Human-on-the-Loop** | ❌ No | Reversible actions, monitoring | Personal data changes |
| **Human-as-Tiebreaker** | ⏸️ Partial | Borderline AI confidence | Loan applications 60-85% score |

---

## Integration with Confidence Router

The HITL decision points integrate with the `ConfidenceRouter` from TODO 12:

```python
# Example integration
router = ConfidenceRouter()

# High-value transfer (always escalate)
decision = router.route(
    response="Transfer approved",
    confidence=0.95,
    action_type="transfer_money"  # HIGH_RISK_ACTION
)
# Result: action="escalate", requires_human=True

# Personal data change (escalate if low confidence)
decision = router.route(
    response="Email changed",
    confidence=0.75,
    action_type="update_personal_info"  # HIGH_RISK_ACTION
)
# Result: action="escalate", requires_human=True

# Loan application (route based on confidence)
decision = router.route(
    response="Loan application processed",
    confidence=0.72,
    action_type="loan_application"
)
# Result: action="queue_review", requires_human=True
```

---

## Metrics to Track

For each HITL decision point, track:

1. **Volume Metrics**:
   - Total requests
   - Human escalation rate
   - Auto-approval rate
   - Auto-rejection rate

2. **Quality Metrics**:
   - Human override rate (human disagrees with AI)
   - False positive rate (safe requests escalated)
   - False negative rate (risky requests auto-approved)

3. **Efficiency Metrics**:
   - Average human review time
   - Queue wait time
   - SLA compliance (% reviewed within target time)

4. **Outcome Metrics**:
   - Fraud prevented (for transfers)
   - Account takeover prevented (for data changes)
   - Default rate (for loans)

---

## Continuous Improvement

Use HITL data to improve the AI:

1. **Collect human decisions** as training data
2. **Analyze disagreements** between AI and human
3. **Retrain models** with human feedback
4. **Adjust thresholds** based on false positive/negative rates
5. **Update rules** when new attack patterns emerge

**Example**:
> After 3 months, analysis shows that 80% of transfers to Singapore are legitimate business payments. Update the model to reduce false positives for Singapore transfers while maintaining vigilance for other countries.

---

## Regulatory Compliance

HITL design addresses regulatory requirements:

- **Basel III** (Banking): Human oversight for high-risk transactions
- **GDPR** (Privacy): Human review for automated decisions affecting individuals
- **MAS TRM** (Singapore): Technology Risk Management guidelines
- **SBV Circular** (Vietnam): Banking security requirements

---

**Document Version**: 1.0
**Last Updated**: April 16, 2026
**Status**: ✅ Complete
