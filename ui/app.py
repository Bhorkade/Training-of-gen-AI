"""
StartupSetu AI Assistant - Interactive Chat UI & Eligibility Assessment
Built with Streamlit for Day 10.
Features:
- 'Am I a startup?' st.form: Direct evaluation of Entity Type, Incorporation Date, Turnover, and Innovation.
- Result display with the cited DPIIT statutory rule (Notification G.S.R. 127(E)).
- Dual Mode Chat: Direct RAG (/ask) and LangGraph Autonomous Agent (/agent).
- Verified Citations display with official government sources and pages.
- Human-in-the-loop Action Approval buttons (Approve / Reject).
- Thumbs Up / Down user feedback mechanism saved to data/feedback.json.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

FEEDBACK_FILE = BASE_DIR / "data" / "feedback.json"
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Page Configuration
st.set_page_config(
    page_title="StartupSetu AI - DPIIT Startup Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .citation-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem 1rem;
        margin-top: 0.6rem;
        border-radius: 4px;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .rule-card {
        background-color: #EFF6FF;
        border-left: 4px solid #1D4ED8;
        padding: 1rem;
        margin-top: 0.8rem;
        border-radius: 6px;
        font-size: 0.92rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


def save_feedback(
    question: str,
    answer: str,
    rating: str,
    mode: str,
    feedback_notes: str = ""
) -> bool:
    """Save thumbs up/down user feedback to data/feedback.json."""
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []

    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []

    entry = {
        "id": len(records) + 1,
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "rating": rating,  # "thumbs_up" or "thumbs_down"
        "question": question,
        "answer": answer[:300],
        "notes": feedback_notes
    }
    records.append(entry)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    return True


def check_api_health(api_url_str: str) -> bool:
    """Check if the backend FastAPI service is reachable."""
    try:
        r = requests.get(f"{api_url_str}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def call_ask_api(api_url_str: str, question: str) -> dict[str, Any]:
    """Call the RAG endpoint POST /ask."""
    r = requests.post(
        f"{api_url_str}/ask",
        json={"question": question, "top_k": 3},
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    return {
        "response": data.get("answer", ""),
        "citations": data.get("citations", []),
        "status": "completed",
        "requires_approval": False
    }


def call_agent_api(
    api_url_str: str,
    query: str,
    thread_id: str | None = None,
    approved: bool | None = None
) -> dict[str, Any]:
    """Call the LangGraph Agent endpoint POST /agent."""
    payload: dict[str, Any] = {"query": query}
    if thread_id:
        payload["thread_id"] = thread_id
    if approved is not None:
        payload["approved"] = approved

    r = requests.post(f"{api_url_str}/agent", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def call_check_eligibility(
    api_url_str: str,
    entity_type: str,
    incorporation_date: str,
    turnover_cr: float,
    is_innovative: bool
) -> dict[str, Any]:
    """Call POST /eligibility or fallback directly to check_dpiit_eligibility tool."""
    try:
        r = requests.post(
            f"{api_url_str}/eligibility",
            json={
                "entity_type": entity_type,
                "incorporation_date": incorporation_date,
                "annual_turnover_cr": turnover_cr,
                "is_innovative": is_innovative
            },
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass

    from app.tools import check_dpiit_eligibility
    return check_dpiit_eligibility(
        entity_type=entity_type,
        incorporation_date=incorporation_date,
        annual_turnover_cr=turnover_cr,
        is_innovative=is_innovative
    )


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = set()

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ System Control")
    api_url = st.text_input("Backend API URL", value=DEFAULT_API_URL)

    is_online = check_api_health(api_url)
    if is_online:
        st.success("● API Online (FastAPI)")
    else:
        st.warning("○ API Offline - Running with local direct fallback")

    st.markdown("---")
    endpoint_mode = st.radio(
        "Select Processing Engine:",
        options=["LangGraph Agent (/agent)", "Direct RAG Pipeline (/ask)"],
        index=0,
        help="Choose between autonomous LangGraph agent with tool invocation and approval, or direct RAG document retrieval."
    )

    st.markdown("---")
    st.subheader("💡 Example Queries")
    sample_queries = [
        "What is DPIIT Startup Recognition?",
        "Can a Private Limited Company apply for DPIIT recognition?",
        "Check eligibility: Pvt Ltd incorporated in 2024 with 2 crore turnover",
        "Tell me about the Startup India Seed Fund Scheme",
        "Please submit my application for startup registration",
        "What are the benefits under Section 80-IAC?"
    ]
    for sq in sample_queries:
        if st.button(sq, key=f"btn_{sq}", use_container_width=True):
            st.session_state["queued_prompt"] = sq

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.session_state.pending_approval = None
        st.session_state.feedback_submitted = set()
        st.rerun()

# Main Header
st.markdown('<div class="main-header">StartupSetu AI Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">AI-Powered DPIIT Startup Recognition, Funding Schemes & Official Guidance for Indian Founders</div>',
    unsafe_allow_html=True
)

# Navigation Tabs: Signature 'Am I a startup?' Form & Chat Assistant
tab_form, tab_chat = st.tabs([
    "🚀 'Am I a startup?' Eligibility Form",
    "💬 AI Chat Assistant (/ask & /agent)"
])

# --------------------------------------------------
# TAB 1: 'Am I a startup?' ST.FORM
# --------------------------------------------------
with tab_form:
    st.subheader("📋 'Am I a startup?' — Official DPIIT Recognition Evaluation")
    st.markdown(
        "Evaluate your venture's eligibility for official Government of India DPIIT Startup Recognition, "
        "tax exemptions under Section 80-IAC, patent rebates, and seed funding support."
    )

    with st.form("am_i_a_startup_form"):
        col1, col2 = st.columns(2)
        with col1:
            form_entity = st.selectbox(
                "1. Entity Type",
                options=[
                    "Private Limited Company",
                    "Limited Liability Partnership (LLP)",
                    "Registered Partnership Firm",
                    "Sole Proprietorship",
                    "One Person Company (OPC)"
                ],
                help="Under DPIIT rules, only Private Limited Company, LLP, or Registered Partnership firms qualify."
            )
            form_date = st.date_input(
                "2. Incorporation Date",
                value=datetime(2024, 1, 1),
                min_value=datetime(2000, 1, 1),
                max_value=datetime.now(),
                help="Entity period of existence must not exceed 10 years from the date of incorporation."
            )

        with col2:
            form_turnover = st.number_input(
                "3. Annual Turnover (₹ in Crores)",
                min_value=0.0,
                max_value=1000.0,
                value=1.5,
                step=0.5,
                help="Turnover for any financial year since incorporation must not exceed ₹100 Crore."
            )
            form_innovative = st.checkbox(
                "4. Working towards innovation, development or improvement of products/services, or scalable business model",
                value=True,
                help="Entity must be working towards innovation, development or improvement, or a scalable business model with high employment generation or wealth creation."
            )

        submit_eligibility = st.form_submit_button(
            "🔍 Evaluate Startup Eligibility",
            use_container_width=True,
            type="primary"
        )

    if submit_eligibility:
        with st.spinner("Evaluating against official DPIIT statutory criteria..."):
            result = call_check_eligibility(
                api_url_str=api_url,
                entity_type=form_entity,
                incorporation_date=str(form_date),
                turnover_cr=float(form_turnover),
                is_innovative=form_innovative
            )

        is_eligible = result.get("is_eligible", False)
        criteria = result.get("criteria", {})
        years_active = result.get("years_active", 0)

        # Verdict Header
        if is_eligible:
            st.success("🎉 **VERDICT: ELIGIBLE FOR OFFICIAL DPIIT STARTUP RECOGNITION**")
            st.markdown(f"**Assessment Summary:** {result.get('summary')}")
        else:
            st.error("❌ **VERDICT: NOT CURRENTLY ELIGIBLE FOR DPIIT RECOGNITION**")
            st.markdown("**Reasons for Ineligibility:**")
            for reason in result.get("reasons", []):
                st.markdown(f"- ⚠️ {reason}")

        # Metrics Breakdown
        st.markdown("#### 📊 Evaluation Breakdown across 4 Statutory Pillars:")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label="Entity Type",
                value="Valid" if criteria.get("entity_type_valid") else "Invalid",
                delta="Private Ltd / LLP / Partnership" if criteria.get("entity_type_valid") else "Excluded"
            )
        with m2:
            st.metric(
                label="Age (≤ 10 Years)",
                value="Valid" if criteria.get("age_under_10_years") else "Exceeded",
                delta=f"{years_active} yrs active"
            )
        with m3:
            st.metric(
                label="Turnover (≤ ₹100 Cr)",
                value="Valid" if criteria.get("turnover_under_100cr") else "Exceeded",
                delta=f"₹{form_turnover} Cr"
            )
        with m4:
            st.metric(
                label="Innovation / Scalability",
                value="Satisfied" if criteria.get("innovative_scalable") else "Missing",
                delta="Innovation Pillar" if criteria.get("innovative_scalable") else "Required"
            )

        # Cited DPIIT Rule
        st.markdown("---")
        st.subheader("📜 Cited DPIIT Statutory Rule")
        cited = result.get("cited_rule", {})
        rules_html = "".join(f"<li>{r}</li>" for r in cited.get("rules", []))
        st.markdown(
            f"""<div class="rule-card">
                <b>Statutory Authority:</b> {cited.get('notification', 'DPIIT, Ministry of Commerce and Industry')}<br/>
                <b>Framework Title:</b> {cited.get('title', 'DPIIT Startup Recognition Definition')}<br/>
                <b>Official Gazette Reference:</b> <a href="{cited.get('source_url')}" target="_blank">Access Official DPIIT Recognition Portal</a><br/><br/>
                <b>Statutory Conditions under Gazette Notification G.S.R. 127(E):</b>
                <ul style="margin-top: 0.4rem; padding-left: 1.2rem;">
                    {rules_html}
                </ul>
            </div>""",
            unsafe_allow_html=True
        )

        # Recommended Benefits
        benefits = result.get("recommended_benefits", [])
        if benefits:
            st.markdown("#### 🎁 Government Benefits Available Upon DPIIT Recognition:")
            for b in benefits:
                st.markdown(f"- ✅ **{b}**")


# --------------------------------------------------
# TAB 2: AI CHAT ASSISTANT (/ask & /agent)
# --------------------------------------------------
with tab_chat:
    st.subheader("💬 AI Chat Assistant")
    st.markdown("Interact directly with the StartupSetu RAG knowledge base or autonomous LangGraph agent.")

    # Display Chat History
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Display citations if present
            citations = msg.get("citations", [])
            if citations:
                with st.expander(f"📚 Citations & Official Sources ({len(citations)})", expanded=False):
                    for c in citations:
                        title = c.get("title", "Official Source")
                        source = c.get("source", "#")
                        page = c.get("page", 1)
                        st.markdown(
                            f"""<div class="citation-card">
                            📄 <b>{title}</b> &mdash; Page {page}<br/>
                            🔗 <a href="{source}" target="_blank">Access Official Documentation</a>
                            </div>""",
                            unsafe_allow_html=True
                        )

            # Thumbs up / down feedback widget
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"
                col1, col2, col3 = st.columns([1, 1, 6])
                with col1:
                    if st.button("👍 Helpful", key=f"up_{idx}", disabled=fb_key in st.session_state.feedback_submitted):
                        save_feedback(
                            question=st.session_state.messages[idx - 1]["content"] if idx > 0 else "N/A",
                            answer=msg["content"],
                            rating="thumbs_up",
                            mode=endpoint_mode
                        )
                        st.session_state.feedback_submitted.add(fb_key)
                        st.toast("Thank you for your feedback! 👍", icon="✅")
                        st.rerun()
                with col2:
                    if st.button("👎 Poor", key=f"down_{idx}", disabled=fb_key in st.session_state.feedback_submitted):
                        save_feedback(
                            question=st.session_state.messages[idx - 1]["content"] if idx > 0 else "N/A",
                            answer=msg["content"],
                            rating="thumbs_down",
                            mode=endpoint_mode
                        )
                        st.session_state.feedback_submitted.add(fb_key)
                        st.toast("Feedback recorded! We'll improve this response. 👎", icon="📝")
                        st.rerun()
                with col3:
                    if fb_key in st.session_state.feedback_submitted:
                        st.caption("✓ Feedback saved")

    # Pending Approval Banner for Human-in-the-Loop
    if st.session_state.pending_approval:
        pending = st.session_state.pending_approval
        st.warning("⚠️ **Human Approval Required**\nThe agent requires your confirmation before executing this action.")
        col_app, col_rej = st.columns(2)
        with col_app:
            if st.button("✅ Approve Action", use_container_width=True, type="primary"):
                with st.spinner("Executing approved action..."):
                    try:
                        res = call_agent_api(
                            api_url_str=api_url,
                            query="Approved by user",
                            thread_id=st.session_state.thread_id,
                            approved=True
                        )
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": res.get("response", "Action completed."),
                            "citations": res.get("citations", [])
                        })
                        st.session_state.pending_approval = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error executing approved action: {e}")

        with col_rej:
            if st.button("❌ Reject Action", use_container_width=True):
                with st.spinner("Cancelling action..."):
                    try:
                        res = call_agent_api(
                            api_url_str=api_url,
                            query="Rejected by user",
                            thread_id=st.session_state.thread_id,
                            approved=False
                        )
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": res.get("response", "Action was cancelled."),
                            "citations": []
                        })
                        st.session_state.pending_approval = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error rejecting action: {e}")

    # Process Input Prompt
    prompt_input = st.chat_input("Ask about DPIIT startup recognition, eligibility, or funding schemes...")
    queued = st.session_state.pop("queued_prompt", None)
    user_prompt = queued or prompt_input

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting official policies..."):
                try:
                    if "Direct RAG" in endpoint_mode:
                        result = call_ask_api(api_url_str=api_url, question=user_prompt)
                    else:
                        result = call_agent_api(
                            api_url_str=api_url,
                            query=user_prompt,
                            thread_id=st.session_state.thread_id
                        )
                        if result.get("thread_id"):
                            st.session_state.thread_id = result["thread_id"]

                    response_text = result.get("response", "")
                    citations = result.get("citations", [])

                    st.markdown(response_text)

                    if citations:
                        with st.expander(f"📚 Citations & Official Sources ({len(citations)})", expanded=True):
                            for c in citations:
                                st.markdown(
                                    f"""<div class="citation-card">
                                    📄 <b>{c.get('title')}</b> &mdash; Page {c.get('page', 1)}<br/>
                                    🔗 <a href="{c.get('source', '#')}" target="_blank">Access Official Documentation</a>
                                    </div>""",
                                    unsafe_allow_html=True
                                )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "citations": citations
                    })

                    if result.get("status") == "needs_approval":
                        st.session_state.pending_approval = result.get("pending_action")
                        st.rerun()

                except Exception as err:
                    err_msg = f"Failed to fetch response: {err}"
                    st.error(err_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": err_msg,
                        "citations": []
                    })
