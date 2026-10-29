# Cynbit LeadPilot AI

AI-assisted **lead qualification and follow-up drafting** for a software / AI services business.
Built as the AI/ML Engineer Intern assessment for Cynbit ("Identify an AI Opportunity").

Paste a customer inquiry, and the app:
1. **Extracts** structured data (category, requirements, budget, timeline, urgency, contact) using an LLM with validated JSON output.
2. **Scores** the lead with transparent, rule-based points (per-factor breakdown, no black box).
3. **Flags** missing information deterministically.
4. **Drafts** a personalised follow-up email for human review (never auto-sent).

If no API key is set or the LLM fails, a rule-based extractor keeps the app working.

## Deliverables

| Deliverable | File |
|---|---|
| AI Opportunity Report | [AI_OPPORTUNITY_REPORT.md](AI_OPPORTUNITY_REPORT.md) |
| Working PoC | `app.py` + `src/` (Streamlit) |
| Technical Approach Report | [TECHNICAL_APPROACH.md](TECHNICAL_APPROACH.md) |

## Quick start (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then put your GROQ_API_KEY in .env (optional)
streamlit run app.py
```

Free Groq API key: https://console.groq.com . Without a key the app runs in rule-based mode.

## Run tests

```powershell
python -m pytest -q
```

## Project structure

```
app.py                      Streamlit UI
src/models.py               Pydantic schema + deterministic missing-info check
src/analyzer.py             LLM extraction (Groq) + rule-based fallback
src/scoring.py              Explainable lead scoring
src/email_gen.py            Follow-up email drafting
src/storage.py              SQLite persistence
src/samples.py              Synthetic demo inquiries (not real data)
tests/                      Pytest unit tests
```

## Honest limitations

- The lead score is a **prioritisation heuristic**, not a conversion prediction. It is not validated on real sales data; thresholds are assumptions.
- Demo data is synthetic. No real customer data is used.
- The rule-based fallback is English-only and regex-based; it is less accurate than the LLM path.
- Emails are drafts and require human review.

## Deploy (Streamlit Community Cloud)

1. Push this repo to GitHub (public).
2. https://share.streamlit.io -> New app -> select repo, branch `main`, file `app.py`.
3. App settings -> Secrets: `GROQ_API_KEY = "your_key"`.
