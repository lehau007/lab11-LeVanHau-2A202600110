# Tasks for Lab 11 & Assignment 11

This document outlines all the tasks required to complete Lab 11 and Assignment 11 based on the workspace files.

## Lab 11: Guardrails, HITL & Responsible AI (13 TODOs)

These TODOs are scattered across the `src/` directory.

### Part 1: Attacks
*   **TODO 1: Write 5 adversarial prompts** (`src/attacks/attacks.py`)
    *   Trick the agent into revealing secrets.
    *   Ask the agent to translate or reformat its system prompt.
    *   Use a 'hypothetical' or 'creative writing' frame to bypass safety.
    *   Confirm information you 'already know' to exploit the side-channel.
    *   Extract info step-by-step (start harmless, then escalate).
*   **TODO 2: Generate attack test cases with AI** (`src/attacks/attacks.py`)
    *   Use an LLM (Gemini) to generate adversarial attack prompts dynamically.

### Part 2: Guardrails
*   **TODO 3: Injection detection (regex)** (`src/guardrails/input_guardrails.py`)
    *   Implement `detect_injection()` by adding at least 5 regex patterns to detect prompt injection.
*   **TODO 4: Topic filter** (`src/guardrails/input_guardrails.py`)
    *   Implement `topic_filter()` logic to detect and block off-topic queries.
*   **TODO 5: Build Input Guardrail Plugin** (`src/guardrails/input_guardrails.py`)
    *   Implement the Google ADK plugin logic for input guardrails.
*   **TODO 6: Content filter (PII, secrets)** (`src/guardrails/output_guardrails.py`)
    *   Implement `content_filter()` by adding regex patterns to catch and filter sensitive info (PII, secrets) from the output.
*   **TODO 7: LLM-as-Judge safety check** (`src/guardrails/output_guardrails.py`)
    *   Implement `safety_judge_agent` using `LlmAgent` to evaluate if the response is safe.
*   **TODO 8: Build Output Guardrail Plugin** (`src/guardrails/output_guardrails.py`)
    *   Implement the Google ADK plugin logic for output guardrails.
*   **TODO 9: Define NeMo Guardrails Colang rules** (`src/guardrails/nemo_guardrails.py`)
    *   Define Colang rules for banking safety, add 3+ new rules, and implement test cases for those rules.

### Part 3: Testing Pipeline
*   **TODO 10: Rerun 5 attacks with guardrails** (`src/testing/testing.py`)
    *   Create a protected agent with the implemented guardrail plugins.
    *   Run the 5 adversarial prompts from TODO 1 and compare the before vs. after results.
*   **TODO 11: Automated security testing pipeline** (`src/testing/testing.py`)
    *   Implement the pipeline logic for automated testing.
    *   Calculate metrics for the pipeline (e.g., block rate, success rate).

### Part 4: HITL (Human-in-the-Loop)
*   **TODO 12: Confidence Router** (`src/hitl/hitl.py`)
    *   Implement the `ConfidenceRouter` and its routing logic.
*   **TODO 13: Design 3 HITL decision points** (`src/hitl/hitl.py`)
    *   Design 3 decision points specifying: name, trigger, HITL model (in-the-loop / on-the-loop / as-tiebreaker), context needed by the reviewer, and a concrete example.

---

## Assignment 11: Build a Production Defense-in-Depth Pipeline

Build a complete defense pipeline that chains multiple independent safety layers together with monitoring. You can use any framework (Google ADK, LangChain, NeMo, Guardrails AI, CrewAI, Pure Python, or a mix).

### 1. Required Architecture Components
Implement at least **4 independent safety layers** plus audit/monitoring:
*   **Rate Limiter:** Block users who send too many requests in a time window.
*   **Input Guardrails:** Detect prompt injection (regex) + block off-topic/dangerous requests (can use NeMo Colang rules).
*   **Output Guardrails:** Filter PII/secrets from responses and redact sensitive data.
*   **LLM-as-Judge:** Use a separate LLM to evaluate responses on multiple criteria (safety, relevance, accuracy, tone).
*   **Audit Log:** Record every interaction (input, output, which layer blocked, latency) and export to JSON (`audit_log.json`).
*   **Monitoring & Alerts:** Track block rate, rate-limit hits, judge fail rate, and fire alerts when thresholds are exceeded.
*   **Bonus (+10 pts):** Add a 6th safety layer (e.g., Toxicity classifier, Language detection, Session anomaly detector, Embedding similarity filter, Hallucination detector, Cost guard).

### 2. Testing Requirements (Must show output)
*   **Test 1 (Safe queries):** Should all PASS (e.g., asking about interest rates).
*   **Test 2 (Attacks):** Should all be BLOCKED (e.g., "Ignore previous instructions", "Translate system prompt").
*   **Test 3 (Rate limiting):** Send 15 rapid requests (e.g., first 10 pass, last 5 blocked).
*   **Test 4 (Edge cases):** Empty input, very long input, emoji-only, SQL injection, off-topic.

### 3. Deliverables

#### Part A: Code Implementation (60 points)
*   Working `.ipynb` notebook (or `.py` files) running the end-to-end pipeline.
*   Demonstrate Rate Limiter, Input Guardrails, Output Guardrails, and LLM-as-Judge working correctly.
*   Output an `audit_log.json` with 20+ entries and demonstrate alerts.
*   **Code Comments:** Every function/class must have clear comments explaining what it does, and why it is needed (what attack it catches).

#### Part B: Individual Report (40 points)
*   **1-2 page report** (PDF or Markdown) answering:
    1.  **Layer analysis:** Table showing which layer caught each of the 7 attack prompts first.
    2.  **False positive analysis:** Did safe queries get blocked? Why? Trade-offs between security and usability.
    3.  **Gap analysis:** Design 3 new attack prompts that bypass the current pipeline and propose additional layers to catch them.
    4.  **Production readiness:** What would you change for 10,000 users? (Latency, cost, monitoring, updating rules).
    5.  **Ethical reflection:** Is a "perfectly safe" AI possible? Limits of guardrails, refuse vs. disclaimer.
