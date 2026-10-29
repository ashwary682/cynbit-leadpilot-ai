"""Cynbit LeadPilot AI - Streamlit demo.

Run:  streamlit run app.py
"""
import os

import pandas as pd
import streamlit as st

from src.analyzer import analyze_inquiry, get_groq_api_key
from src.email_gen import generate_followup
from src.samples import SAMPLES
from src.scoring import score_lead
from src.storage import list_leads, save_lead

st.set_page_config(page_title="Cynbit LeadPilot AI", page_icon="🧭", layout="wide")

# Streamlit Cloud: sync secrets to env so both local and cloud work identically
secrets_error = None
try:
    if hasattr(st, "secrets"):
        for k in ("GROQ_API_KEY", "GROQ_MODEL"):
            if k in st.secrets and str(st.secrets[k]).strip():
                os.environ[k] = str(st.secrets[k]).strip().strip('"\'')
except Exception as e:
    secrets_error = str(e)

TIER_ICON = {"Hot": "🔥", "Warm": "🌤️", "Cold": "❄️"}


def load_sample():
    idx = st.session_state.get("sample_idx", 0)
    if idx > 0:
        st.session_state["inquiry_text"] = SAMPLES[idx - 1]["text"]


st.title("🧭 Cynbit LeadPilot AI")
st.caption("AI-assisted lead qualification and follow-up drafting. Demo uses synthetic inquiries only.")

with st.sidebar:
    st.header("Settings")
    if secrets_error:
        st.error(
            f"⚠️ Streamlit Secrets error: {secrets_error}\n\n"
            "Secrets in Streamlit Cloud must use TOML format with quotes:\n"
            "```toml\n"
            'GROQ_API_KEY = "gsk_..."\n'
            'GROQ_MODEL = "openai/gpt-oss-120b"\n'
            "```"
        )
    has_key = bool(get_groq_api_key())
    use_llm = st.toggle("Use LLM (Groq)", value=has_key, disabled=not has_key)
    st.write("Mode: **LLM extraction**" if use_llm else "Mode: **rule-based fallback**")
    if not has_key:
        st.info("No GROQ_API_KEY set. The app runs in rule-based mode.")
    st.selectbox(
        "Load a synthetic sample", ["(none)"] + [s["name"] for s in SAMPLES],
        index=0, key="sample_name_ui",
        on_change=lambda: st.session_state.update(
            sample_idx=(["(none)"] + [s["name"] for s in SAMPLES]).index(st.session_state["sample_name_ui"])
        ) or load_sample(),
    )
    st.divider()
    st.caption(
        "The lead score is an explainable prioritisation heuristic. It is not a prediction of "
        "sales conversion and has not been validated on real data."
    )

tab_analyze, tab_saved = st.tabs(["Analyze inquiry", "Saved leads"])

with tab_analyze:
    st.text_area("Customer inquiry", key="inquiry_text", height=200,
                 placeholder="Paste a customer message describing a software or AI project...")
    if st.button("Analyze lead", type="primary"):
        text = st.session_state.get("inquiry_text", "")
        try:
            with st.spinner("Analyzing..."):
                result = analyze_inquiry(text, use_llm=use_llm)
                score = score_lead(result.analysis)
                email = generate_followup(result.analysis, score, use_llm=use_llm)
            st.session_state["result"] = (text, result, score, email)
        except ValueError as e:
            st.warning(str(e))

    if "result" in st.session_state:
        text, result, score, email = st.session_state["result"]
        a = result.analysis
        if result.note:
            st.info(result.note)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lead score", f"{score.total}/100")
        c2.metric("Tier", f"{TIER_ICON[score.tier]} {score.tier}")
        c3.metric("Category", a.service_category)
        c4.metric("Urgency", a.urgency.title())

        left, right = st.columns(2)
        with left:
            st.subheader("Extracted details")
            st.write(f"**Client:** {a.client_name or '-'}  |  **Company:** {a.company or '-'}")
            st.write(f"**Email:** {a.contact_email or '-'}")
            st.write(f"**Budget:** {a.budget_text or '-'}"
                     + (f" (~INR {a.budget_inr:,.0f})" if a.budget_inr else ""))
            st.write(f"**Timeline:** {a.timeline_text or '-'}")
            st.write(f"**Summary:** {a.project_summary or '-'}")
            st.write("**Requirements:**")
            for r in a.requirements or ["(none detected)"]:
                st.write(f"- {r}")
        with right:
            st.subheader("Score breakdown")
            df = pd.DataFrame([{"Factor": i.factor, "Points": f"{i.points}/{i.max_points}", "Why": i.reason}
                               for i in score.items])
            st.dataframe(df, hide_index=True)
            st.subheader("Missing information")
            for m in a.missing_info or ["Nothing critical missing"]:
                st.write(f"- {m}")

        st.subheader("Draft follow-up email (review before sending)")
        edited = st.text_area("Email draft", value=email, height=260, key="email_edit")
        if st.button("Save lead"):
            lead_id = save_lead(text, a, score, edited)
            st.success(f"Saved as lead #{lead_id}")

with tab_saved:
    leads = list_leads()
    if leads:
        st.dataframe(pd.DataFrame(leads), hide_index=True)
    else:
        st.write("No leads saved yet.")
