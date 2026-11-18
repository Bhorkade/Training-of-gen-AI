"""
StartupSetu AI Assistant - Interactive Chat UI
Built with Streamlit for Day 10.
Features:
- Dual Mode: Direct RAG (/ask) and LangGraph Autonomous Agent (/agent)
- Verified Citations display with official government sources and pages
- Human-in-the-loop Action Approval buttons (Approve / Reject)
- Thumbs Up / Down user feedback mechanism saved to data/feedback.json
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
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
        padding: 0.6rem 0.8rem;
        margin-top: 0.5rem;
        border-radius: 4px;
        font-size: 0.88rem;
    }
    .feedback-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.4rem;
        font-size: 0.85rem;
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
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
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


def check_api_health(api_url: str) -> bool:
    """Check if the backend FastAPI service is reachable."""
    try:
        r = requests.get(f"{api_url}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def call_ask_api(api_url: str, question: str) -> dict[str, Any]:
    """Call the RAG endpoint POST /ask."""
    r = requests.post(
        f"{api_url}/ask",
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
    api_url: str,
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

    r = requests.post(f"{api_url}/agent", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


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
        st.warning("○ API Offline - Ensure `uvicorn app.main:app` is running")

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
                        api_url=api_url,
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
                        api_url=api_url,
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
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consulting official policies..."):
            try:
                if "Direct RAG" in endpoint_mode:
                    result = call_ask_api(api_url=api_url, question=user_prompt)
                else:
                    result = call_agent_api(
                        api_url=api_url,
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

                # Record in state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "citations": citations
                })

                # Check if approval needed
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
