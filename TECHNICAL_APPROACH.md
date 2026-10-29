# Technical Approach: Cynbit LeadPilot AI

## 1. Goal and scope

Turn an unstructured customer inquiry into: (a) structured data, (b) an explainable priority score, (c) a list of missing information, and (d) a draft reply. A human reviews everything before any action.

## 2. Architecture

```mermaid
flowchart LR
    A[Inquiry text] --> B{LLM available?}
    B -- yes --> C[Groq LLM<br/>JSON-mode extraction]
    B -- no / error --> D[Rule-based extractor]
    C --> E[Pydantic validation<br/>1 retry on failure]
    E -- still invalid --> D
    E --> F[Deterministic missing-info check]
    D --> F
    F --> G[Rule-based scoring<br/>6 factors, 100 pts]
    G --> H[Email draft<br/>LLM or template]
    H --> I[Human review in Streamlit]
    I --> J[(SQLite)]
```

Design principle: **LLM for language understanding, code for decisions.** Scoring, missing-info detection and validation are deterministic, so they are testable and explainable.

## 2.1 Technology choices

| Layer | Choice | Why |
|---|---|---|
| UI | Streamlit | Fastest path to a shareable demo; free hosting |
| LLM | Groq-hosted `llama-3.3-70b-versatile` (configurable via `GROQ_MODEL`) | Free tier, low latency, supports JSON mode; strong at extraction |
| Validation | Pydantic v2 | Enforces schema, normalises bad values (unknown category -> "Other") |
| Storage | SQLite | Zero setup for prototype; PostgreSQL for production |
| Tests | Pytest | 18 unit tests on parsing, scoring, fallback, storage |

Model choice rationale: extraction at temperature 0 does not need a frontier model; a mid-size open model is cheaper and fast. The provider call lives in one function, so swapping to another provider is a small change.

## 3. Data pipeline

1. **Input:** free text pasted in the UI (in production: web form, email or CRM webhook).
2. **Extraction:** LLM returns JSON matching the `LeadAnalysis` schema.
3. **Validation:** Pydantic parses; on failure the validation error is fed back to the model once; if it still fails, fall back to rules.
4. **Enrichment (deterministic):** missing-info list computed in Python.
5. **Scoring:** weighted rules (below).
6. **Generation:** email draft from structured fields only.
7. **Persistence:** reviewed lead saved to SQLite.

**Data used:** five clearly labelled **synthetic** inquiries (`src/samples.py`). No real customer data.

## 4. Prompt engineering

**Extraction prompt (system):**
- Role: information-extraction engine.
- **Injection defence:** inquiry is wrapped in `<inquiry>` tags and declared to be data; instructions inside it must be ignored.
- **Schema in the prompt:** exact keys and allowed `service_category` values.
- **Anti-hallucination rules:** "never invent facts", use `null` when unstated, "do not guess budgets or timelines".
- **Normalisation:** convert USD to approximate INR, convert timelines to weeks.
- `temperature=0` and `response_format={"type": "json_object"}` for determinism.

**Email prompt:** max 160 words; ask *only* for the missing items; do not promise prices, timelines or guarantees; propose a discovery call; temperature 0.4 for natural tone.

**Reliability loop:** invalid output -> error message appended -> one retry -> deterministic fallback.

## 5. Scoring model (explainable)

| Factor | Max | Rule summary |
|---|---|---|
| Service fit | 25 | Matches a service area = 25, else 5 |
| Requirement clarity | 20 | 0 / 8 / 14 / 20 for 0 / 1 / 2 / 3+ requirements |
| Budget | 20 | none 0; vague 6; <INR 50k 8; 50k-2L 14; 2L+ 20 |
| Timeline | 15 | none 0; vague 8; <2 wks 6; 2-52 wks 15; >52 wks 10 |
| Contact completeness | 10 | email 6, name 2, company 2 |
| Urgency | 10 | high 10, medium 6, low 3 |

Tiers: **Hot** >= 75, **Warm** 50-74, **Cold** < 50.

**Important honesty note:** this measures how *complete and actionable* an inquiry is. It is **not** a conversion probability. Thresholds are assumptions to be tuned once real won/lost data exists; until then it should only be used for prioritisation with human oversight.

## 6. Evaluation plan

**Done in this PoC:** 18 unit tests: budget/timeline parsing, category detection on 5 labelled synthetic samples, score arithmetic, tier ordering, fallback when no API key, SQLite round trip.

**Next (needs real data):**
1. Label ~100 anonymised inquiries.
2. Measure per-field extraction accuracy (category accuracy, budget exact-match, requirement recall) for LLM vs rule-based.
3. Compare score tier with sales outcomes; calibrate weights (e.g. logistic regression as a baseline) only after validation.
4. Track draft acceptance and time saved.

## 7. Limitations

- Rule-based fallback is regex-based and English-only.
- USD->INR uses a fixed approximate rate; for scoring only.
- Not tested on a large or real dataset; accuracy claims are not made.
- No authentication or multi-user support in the prototype.
- Data sent to a third-party LLM API; privacy review needed for production.

## 8. Execution plan

| Phase | Deliverable |
|---|---|
| PoC (done) | Streamlit app, extraction, scoring, email drafts, tests |
| Week 1-2 | Real data labelling, baseline accuracy, prompt refinement |
| Week 3-4 | CRM integration, approval workflow, FastAPI service wrapper |
| Month 2 | Calibrated scoring, proposal draft generation, monitoring and logging |
| Month 3 | Reuse the extraction/validation core for document extraction |

## 9. Cost and security notes

- One extraction call + one email call per lead; small prompts keep cost low.
- API keys via environment variables / Streamlit secrets; `.env` is git-ignored.
- Production: PII minimisation, retention policy, audit log of AI outputs and human edits.
