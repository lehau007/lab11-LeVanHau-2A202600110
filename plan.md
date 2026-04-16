# Execution Plan: Lab 11 & Assignment 11

This plan outlines the step-by-step implementation for Lab 11 and Assignment 11.

## 0. Standard Guidelines & Tech Stack
- **Default LLM Provider:** `google.genai` client.
- **Default Model:** `gemma-4-31b-it`.
- **Programming Language:** Python 3.10+.
- **Key Libraries:** `google-genai`, `google-adk`, `nemoguardrails`, `re` (Regex), `json`, `collections.deque`.

---

## Phase 1: Attacks (Lab 11 Part 1)

### Task 1: Write 5 manual adversarial prompts (TODO 1)
- **File:** `src/attacks/attacks.py`
- **Tech Stack:** Python (List of Dictionaries).
- **Implementation:** Manually craft prompts targeting:
    - Secret extraction (API keys, passwords).
    - System prompt leakage ("Translate your system prompt").
    - Jailbreaking ("You are now DAN").
    - Hypothetical/Creative framing to bypass safety filters.
    - Multi-step escalation (start safe, then pivot).

### Task 2: AI-Generated Attack Test Cases (TODO 2)
- **File:** `src/attacks/attacks.py`
- **Tech Stack:** `google.genai` (`gemma-4-31b-it`).
- **Implementation:** 
    - Initialize `genai.Client()`.
    - Provide a "Red Teamer" system prompt to `gemma-4-31b-it`.
    - Generate 5-10 diverse adversarial prompts dynamically.
    - Parse the output into the standard attack list format.

---

## Phase 2: Input Guardrails (Lab 11 Part 2A)

### Task 3: Injection Detection via Regex (TODO 3)
- **File:** `src/guardrails/input_guardrails.py`
- **Tech Stack:** Python `re` module.
- **Implementation:** Define a list of regex patterns to detect common injection strings (e.g., `(?i)ignore.*instruction`, `(?i)system.*prompt`, `(?i)reveal.*password`).

### Task 4: Topic Filter (TODO 4)
- **File:** `src/guardrails/input_guardrails.py`
- **Tech Stack:** Python (String matching / Keyword lists).
- **Implementation:** 
    - Define `ALLOWED_TOPICS` (Banking, Finance, Accounts).
    - Define `BLOCKED_TOPICS` (Politics, Coding, Violence).
    - Implement heuristic checks to block queries that fall outside the banking domain.

### Task 5: Build Input Guardrail Plugin (TODO 5)
- **File:** `src/guardrails/input_guardrails.py`
- **Tech Stack:** Google ADK `BasePlugin`.
- **Implementation:** 
    - Inherit from `base_plugin.BasePlugin`.
    - Override `on_user_message_callback()`.
    - Sequence: Check Injection -> Check Topic -> If blocked, return `BlockedContent`.

---

## Phase 3: Output Guardrails & NeMo (Lab 11 Part 2B & 2C)

### Task 6: Content Filter - PII & Secrets (TODO 6)
- **File:** `src/guardrails/output_guardrails.py`
- **Tech Stack:** Python `re`.
- **Implementation:** Implement regex-based redaction for Credit Card numbers, Emails, API keys, and Phone numbers in the LLM's response.

### Task 7: LLM-as-Judge Safety Check (TODO 7)
- **File:** `src/guardrails/output_guardrails.py`
- **Tech Stack:** `google.genai` (`gemma-4-31b-it`).
- **Implementation:** 
    - Create a "Safety Judge" prompt instructions.
    - Send the generated response to `gemma-4-31b-it` for evaluation.
    - Expected output: Scores for Safety, Relevance, Accuracy, Tone + Verdict (PASS/FAIL).

### Task 8: Build Output Guardrail Plugin (TODO 8)
- **File:** `src/guardrails/output_guardrails.py`
- **Tech Stack:** Google ADK `BasePlugin`.
- **Implementation:** 
    - Override `after_model_callback()`.
    - Sequence: Redact PII -> Run LLM-as-Judge -> If Verdict is FAIL, replace response with a generic safety refusal.

### Task 9: NeMo Guardrails Colang Rules (TODO 9)
- **File:** `src/guardrails/nemo_guardrails.py`
- **Tech Stack:** NVIDIA NeMo Guardrails (Colang).
- **Implementation:** 
    - Write Colang flows for banking safety.
    - Define specific user intents and bot responses for off-topic or dangerous queries.

---

## Phase 4: Testing & HITL (Lab 11 Part 3 & 4)

### Task 10 & 11: Security Testing Pipeline (TODO 10, 11)
- **File:** `src/testing/testing.py`
- **Tech Stack:** Python Core.
- **Implementation:** 
    - Run the attack suite against an unprotected agent vs. the protected (ADK Plugins) agent.
    - Calculate and print metrics: Block Rate, Bypass Rate, and Latency.

### Task 12 & 13: Confidence Router & HITL Design (TODO 12, 13)
- **File:** `src/hitl/hitl.py`
- **Tech Stack:** Python & Design Documentation.
- **Implementation:** 
    - **TODO 12:** Implement routing logic where low-confidence or high-risk queries are flagged for human review.
    - **TODO 13:** Design 3 concrete banking scenarios (High-value transfers, Sensitive data changes, Edge-case loan applications) with specific HITL interaction models.

---

## Phase 5: Production Defense-in-Depth Pipeline (Assignment 11)

### 1. Unified Pipeline Implementation
- **Tech Stack:** Python Class Wrapper (e.g., `DefensePipeline`).
- **Components:**
    - **Rate Limiter:** Token bucket or sliding window implementation for API abuse protection.
    - **Input Layer:** Integration of Task 3, 4, and NeMo.
    - **LLM Core:** Direct call to `gemma-4-31b-it`.
    - **Output Layer:** Integration of Task 6 and 7.
    - **Audit Log:** JSON-based logging of every interaction stage.
    - **Monitoring:** Logic to trigger alerts if Block Rate exceeds a threshold (e.g., >20% in 5 mins).
    - **Bonus (Layer 6):** Implement **Toxicity Detection** or **Language Filter**.

### 2. Validation & Reporting
- Execute Test 1 (Safe), Test 2 (Attacks), Test 3 (Rate Limiting), and Test 4 (Edge Cases).
- Generate `audit_log.json`.
- Prepare the Individual Report (Markdown/PDF) based on the results.
