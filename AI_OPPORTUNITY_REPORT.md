# AI Opportunity Report: Cynbit

**Author:** Ashwary Kumawat  |  **Role:** AI/ML Engineer Intern applicant

> **Scope note.** This analysis is based on Cynbit's publicly described positioning: software development, AI agents / LLM automation, document processing, CRM automation, and SaaS products, plus the AI/ML internship description (chatbots, prompt engineering, document extraction).
> `[VERIFY BEFORE SUBMITTING: confirm each service and product named below against cynbit.in and edit anything that does not match.]`
> Impact figures are **illustrative hypotheses** to be validated with Cynbit's own data, not measured results.

## 1. Executive summary

Cynbit sells custom software and AI automation. Like most service businesses, its growth depends on how quickly and accurately it turns **incoming inquiries into scoped proposals**. This is repetitive, language-heavy work that LLMs handle well. I evaluated four AI opportunities and chose **lead qualification and proposal assistance (LeadPilot AI)** for the proof of concept because it is high-value, buildable without private data, and directly showcases the AI-agent / automation services Cynbit offers.

## 2. Opportunities evaluated

| # | Use case | Who benefits | Core AI technique | Data needed | Value | Feasibility | Risk |
|---|---|---|---|---|---|---|---|
| 1 | **AI lead qualification and follow-up drafting** (chosen) | Sales / founders | LLM structured extraction, rule-based scoring, generation | Inquiry text (synthetic OK to start) | High | High | Low-Med |
| 2 | **Document extraction** (invoices, contracts, forms) as a client-facing service and internal tool | Cynbit clients, ops | OCR + LLM extraction with schema validation | Sample documents with labels | High | Med | Med (accuracy, privacy) |
| 3 | **AI review analysis for Revio** `[VERIFY: product name and purpose]` | Revio users | Sentiment, aspect-based topic extraction, summarisation | Customer reviews | Med-High | Med | Med |
| 4 | **Intelligent learning assistant for Cynbit Studio** `[VERIFY: product name and purpose]` | Learners / trainers | RAG over course content, quiz generation | Course material | Medium | Med | Med (hallucination) |

### 2.1 Lead qualification (chosen)
- **Problem:** Inquiries vary in clarity, budget, urgency and fit. Manual triage is slow and inconsistent, and slow replies lose leads.
- **Solution:** extract structured fields, score with transparent rules, flag missing info, draft a reply.
- **Hypothesised outcomes (to validate):** lower triage time per lead; faster first response; more consistent prioritisation.
- **Why now:** structured-output LLMs are cheap and reliable enough for extraction; low-cost providers make per-inquiry cost negligible.

### 2.2 Document extraction
Strong market demand (invoices, KYC, contracts) and directly named in the internship scope. Higher effort: needs OCR, layout handling, labelled data and an accuracy benchmark (field-level F1). Best as a **second-phase** product line.

### 2.3 Review analysis (Revio) `[VERIFY]`
Aspect-based sentiment and automatic theme summaries turn raw reviews into actionable insights (e.g. "delivery delays up 20% this month"). Needs enough review volume and multilingual handling.

### 2.4 Learning assistant (Cynbit Studio) `[VERIFY]`
RAG-based tutor over course content with citations, plus auto-generated quizzes. Needs strong grounding and evaluation to avoid wrong answers.

## 3. Prioritisation

Scored 1-5 (5 = best; for Risk, 5 = lowest risk). Weights are my assumptions.

| Criterion (weight) | Lead qual. | Doc extraction | Review analysis | Learning assistant |
|---|---|---|---|---|
| Business value (35%) | 4 | 5 | 3 | 3 |
| Feasibility in days (25%) | 5 | 3 | 3 | 3 |
| Data availability (20%) | 4 | 2 | 3 | 3 |
| Risk (10%) | 4 | 3 | 3 | 3 |
| Alignment with services (10%) | 5 | 5 | 3 | 3 |
| **Weighted total** | **4.35** | **3.70** | **3.00** | **3.00** |

Lead qualification wins mainly on feasibility and data availability while still delivering clear value.

## 4. Success metrics (how Cynbit would measure it)

- **Extraction accuracy:** field-level accuracy against human-labelled inquiries (target set after a baseline).
- **Triage time:** minutes per lead before vs after.
- **Time to first response.**
- **Score usefulness:** correlation between tier and eventual outcome, measured only once real history exists.
- **Draft acceptance rate:** share of AI email drafts sent with minor or no edits.

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| LLM hallucination | Strict schema, "never invent" prompt, null for unknowns, Pydantic validation, human review |
| Prompt injection via inquiry text | Inquiry wrapped as data, instructed to ignore embedded commands, outputs validated |
| Privacy of client data | Minimise data sent, avoid storing secrets, consider self-hosted / private models for sensitive clients |
| Score treated as truth | Explainable breakdown; labelled as heuristic; validate on real outcomes before relying on it |
| Vendor dependency | Provider isolated in one module; rule-based fallback exists |

## 6. Roadmap

1. **Now (PoC):** this repository.
2. **Weeks 1-2:** collect ~100 real (anonymised) inquiries, label them, measure extraction accuracy.
3. **Weeks 3-4:** integrate with CRM (webhook or API), add human-in-the-loop approval and send.
4. **Month 2+:** calibrate scoring against real win/loss outcomes; add proposal-draft generation; start document extraction as a second module.

## 7. Recommendation

Build **LeadPilot AI** first. It delivers visible value quickly, is safe to pilot (human-in-the-loop), and the same extraction + validation pattern is reusable for the document-extraction product line.
