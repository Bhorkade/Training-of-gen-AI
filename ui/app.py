"""
StartupSetu AI Platform - Interactive Chat UI & Eligibility Assessment
Built with Streamlit.
Features:
- 'Am I a startup?' st.form: Direct evaluation of Entity Type, Incorporation Date, Turnover, and Innovation.
- Result display with the cited DPIIT statutory rule (Notification G.S.R. 127(E)).
- Dual Mode Chat: Direct RAG (/ask) and LangGraph Autonomous Agent (/agent).
- Zero-Downtime Architecture: Automatic in-process fallback when FastAPI backend is not running.
- Verified Citations display with official government sources and pages.
- Human-in-the-loop Action Approval buttons (Approve / Reject).
- Thumbs Up / Down user feedback mechanism saved to data/feedback.json.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

FEEDBACK_FILE = BASE_DIR / "data" / "feedback.json"
DEFAULT_LOCAL_URL = "http://127.0.0.1:8000"
ENV_API_URL = os.getenv("API_URL", "").strip()
DEFAULT_CLOUD_URL = ENV_API_URL or "https://startupsetu-api.onrender.com"
IS_CLOUD_ENV = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or ENV_API_URL)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="StartupSetu AI — DPIIT Startup Advisory Platform",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS STYLING
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E3A8A 100%);
        border-radius: 16px;
        padding: 2rem 2.2rem;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #FCD34D;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.02rem;
        color: #94A3B8;
        max-width: 850px;
        line-height: 1.6;
        margin: 0;
    }

    /* Cards & Components */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .citation-card {
        background: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 0.85rem 1.1rem;
        margin-top: 0.6rem;
        border-radius: 6px;
        font-size: 0.88rem;
        line-height: 1.5;
        border: 1px solid #E2E8F0;
        border-left-width: 4px;
    }
    .citation-card a {
        color: #2563EB;
        font-weight: 600;
        text-decoration: none;
    }
    .citation-card a:hover {
        text-decoration: underline;
    }
    .rule-card {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 5px solid #1D4ED8;
        padding: 1.2rem;
        margin-top: 1rem;
        border-radius: 10px;
        font-size: 0.92rem;
        line-height: 1.65;
        color: #1E293B;
    }
    .rule-card b {
        color: #0F172A;
    }

    /* Status Pill */
    .status-badge-online {
        display: block;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        background: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
        margin-bottom: 0.4rem;
        text-align: center;
    }
    .status-badge-offline {
        display: block;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        background: #FEF3C7;
        color: #92400E;
        border: 1px solid #FCD34D;
        margin-bottom: 0.4rem;
        text-align: center;
    }
    .status-badge-standalone {
        display: block;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #CBD5E1;
        margin-bottom: 0.4rem;
        text-align: center;
    }

    /* Engine Tag in Chat */
    .engine-tag {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 0.35rem;
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    /* Form styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FEEDBACK PERSISTENCE
# --------------------------------------------------
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


# --------------------------------------------------
# RESILIENT API CALLERS WITH ZERO-DOWNTIME FALLBACKS
# --------------------------------------------------
@st.cache_data(ttl=10, show_spinner=False)
def check_api_health(api_url_str: str) -> bool:
    """Check if the backend FastAPI service is reachable."""
    if not api_url_str or "direct" in api_url_str.lower():
        return False
    try:
        r = requests.get(f"{api_url_str.rstrip('/')}/health", timeout=2.5)
        return r.status_code == 200
    except Exception:
        return False


def call_ask_api(api_url_str: str, question: str) -> dict[str, Any]:
    """
    Call the RAG endpoint POST /ask with automatic cloud fallback and in-process resilience.
    Never crashes with an unhandled exception.
    """
    start_t = time.perf_counter()

    # 1. Try configured FastAPI endpoint if reachable
    if api_url_str and not api_url_str.lower().startswith("direct"):
        try:
            r = requests.post(
                f"{api_url_str.rstrip('/')}/ask",
                json={"question": question, "top_k": 3},
                timeout=35
            )
            if r.status_code == 200:
                data = r.json()
                latency = round((time.perf_counter() - start_t) * 1000, 2)
                return {
                    "response": data.get("answer", ""),
                    "citations": data.get("citations", []),
                    "metrics": data.get("metrics", {"latency_ms": latency}),
                    "status": "completed",
                    "requires_approval": False,
                    "engine": f"FastAPI ({api_url_str})"
                }
        except Exception:
            pass  # Seamless fallback to in-process or cloud fallback

    # 2. Resilient In-Process Direct RAG Execution
    try:
        from app.rag import rag_answer
        data = rag_answer(question=question, top_k=3)
        latency = round((time.perf_counter() - start_t) * 1000, 2)
        return {
            "response": data.get("answer", ""),
            "citations": data.get("citations", []),
            "metrics": {
                "latency_ms": latency,
                "cached": False,
                "in_process": True
            },
            "status": "completed",
            "requires_approval": False,
            "engine": "Direct In-Process RAG Engine"
        }
    except (ImportError, ModuleNotFoundError) as err:
        # 3. If in-process packages are missing (e.g. lightweight UI container), attempt cloud fallback
        if api_url_str != DEFAULT_CLOUD_URL:
            try:
                r = requests.post(
                    f"{DEFAULT_CLOUD_URL.rstrip('/')}/ask",
                    json={"question": question, "top_k": 3},
                    timeout=35
                )
                if r.status_code == 200:
                    data = r.json()
                    latency = round((time.perf_counter() - start_t) * 1000, 2)
                    return {
                        "response": data.get("answer", ""),
                        "citations": data.get("citations", []),
                        "metrics": data.get("metrics", {"latency_ms": latency}),
                        "status": "completed",
                        "requires_approval": False,
                        "engine": f"Cloud API Fallback ({DEFAULT_CLOUD_URL})"
                    }
            except Exception:
                pass
        return {
            "response": (
                f"⚠️ **Backend Offline / Waking Up**: The backend API at `{api_url_str or DEFAULT_CLOUD_URL}` "
                f"is currently waking up from sleep, and direct in-process engine is missing local dependencies ({err}). "
                "Please allow ~30 seconds for the cloud server to spin up and click **'🔄 Test / Ping Connection'** in the sidebar."
            ),
            "citations": [],
            "metrics": {"latency_ms": 0.0},
            "status": "error",
            "requires_approval": False,
            "engine": "Resilience Safe Handler"
        }


def call_agent_api(
    api_url_str: str,
    query: str,
    thread_id: str | None = None,
    approved: bool | None = None
) -> dict[str, Any]:
    """
    Call the LangGraph Agent endpoint POST /agent with automatic fallback.
    Never throws an unhandled exception or module error.
    """
    # 1. Try FastAPI endpoint if reachable
    if api_url_str and not api_url_str.lower().startswith("direct"):
        try:
            payload: dict[str, Any] = {"query": query}
            if thread_id:
                payload["thread_id"] = thread_id
            if approved is not None:
                payload["approved"] = approved

            r = requests.post(
                f"{api_url_str.rstrip('/')}/agent",
                json=payload,
                timeout=40
            )
            if r.status_code == 200:
                res = r.json()
                res["engine"] = f"FastAPI ({api_url_str})"
                return res
        except Exception:
            pass  # Seamless fallback

    # 2. Resilient In-Process Direct LangGraph Execution
    try:
        from app.graph import run_graph_agent
        res = run_graph_agent(
            query=query,
            thread_id=thread_id,
            approved=approved
        )
        res["engine"] = "Direct In-Process LangGraph Engine"
        return res
    except (ImportError, ModuleNotFoundError) as err:
        # 3. If in-process packages are missing (e.g. lightweight UI container), attempt cloud fallback
        if api_url_str != DEFAULT_CLOUD_URL:
            try:
                payload = {"query": query}
                if thread_id:
                    payload["thread_id"] = thread_id
                if approved is not None:
                    payload["approved"] = approved
                r = requests.post(
                    f"{DEFAULT_CLOUD_URL.rstrip('/')}/agent",
                    json=payload,
                    timeout=40
                )
                if r.status_code == 200:
                    res = r.json()
                    res["engine"] = f"Cloud API Fallback ({DEFAULT_CLOUD_URL})"
                    return res
            except Exception:
                pass
        return {
            "response": (
                f"⚠️ **Backend Offline / Waking Up**: The backend API at `{api_url_str or DEFAULT_CLOUD_URL}` "
                f"is currently waking up from sleep, and direct in-process engine is missing local dependencies ({err}). "
                "Please allow ~30 seconds for the cloud server to spin up and click **'🔄 Test / Ping Connection'** in the sidebar."
            ),
            "citations": [],
            "status": "error",
            "requires_approval": False,
            "engine": "Resilience Safe Handler"
        }


def call_check_eligibility(
    api_url_str: str,
    entity_type: str,
    incorporation_date: str,
    turnover_cr: float,
    is_innovative: bool
) -> dict[str, Any]:
    """Call POST /eligibility or fallback directly to check_dpiit_eligibility tool."""
    if api_url_str and not api_url_str.lower().startswith("direct"):
        try:
            r = requests.post(
                f"{api_url_str.rstrip('/')}/eligibility",
                json={
                    "entity_type": entity_type,
                    "incorporation_date": incorporation_date,
                    "annual_turnover_cr": turnover_cr,
                    "is_innovative": is_innovative
                },
                timeout=25
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

    try:
        from app.tools import check_dpiit_eligibility
        return check_dpiit_eligibility(
            entity_type=entity_type,
            incorporation_date=incorporation_date,
            annual_turnover_cr=turnover_cr,
            is_innovative=is_innovative
        )
    except (ImportError, ModuleNotFoundError):
        # Deterministic statutory fallback based directly on Gazette Notification G.S.R. 127(E)
        valid_types = [
            "Private Limited Company",
            "Limited Liability Partnership (LLP)",
            "Registered Partnership Firm"
        ]
        is_type_valid = any(vt.lower() in entity_type.lower() for vt in valid_types)
        try:
            inc_dt = datetime.strptime(incorporation_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            years_active = (today - inc_dt).days / 365.25
            is_age_valid = years_active <= 10.0
        except Exception:
            years_active = 0.0
            is_age_valid = True

        is_turnover_valid = turnover_cr <= 100.0
        is_all_valid = is_type_valid and is_age_valid and is_turnover_valid and is_innovative

        reasons = []
        if not is_type_valid:
            reasons.append(f"Entity type '{entity_type}' is ineligible. Must be Private Limited Company, LLP, or Registered Partnership.")
        if not is_age_valid:
            reasons.append(f"Entity age ({years_active:.1f} years) exceeds statutory maximum of 10 years.")
        if not is_turnover_valid:
            reasons.append(f"Annual turnover (₹{turnover_cr} Cr) exceeds statutory threshold of ₹100 Crore.")
        if not is_innovative:
            reasons.append("Entity must be working towards innovation, development, or deployment of products/services/processes.")

        return {
            "is_eligible": is_all_valid,
            "entity_type": entity_type,
            "years_active": round(years_active, 1),
            "reasons": reasons if not is_all_valid else ["All statutory criteria satisfied under G.S.R. 127(E)."],
            "criteria": {
                "entity_type_valid": is_type_valid,
                "age_under_10_years": is_age_valid,
                "turnover_under_100cr": is_turnover_valid,
                "innovative_scalable": is_innovative
            },
            "cited_rule": {
                "notification": "DPIIT, Ministry of Commerce and Industry",
                "title": "DPIIT Startup Recognition Definition",
                "gazette_no": "G.S.R. 127(E)",
                "source_url": "https://www.startupindia.gov.in/",
                "rules": [
                    "Entity must be Private Limited Company, LLP, or Registered Partnership Firm.",
                    "Period of existence must not exceed 10 years from incorporation date.",
                    "Turnover for any financial year since incorporation must not exceed ₹100 Crore.",
                    "Entity must work towards innovation, development, or deployment of products/services/processes."
                ]
            },
            "summary": "Statutorily eligible for official DPIIT Startup Recognition." if is_all_valid else "Not currently eligible for recognition under Gazette Notification G.S.R. 127(E).",
            "recommended_benefits": [
                "Section 80-IAC 3-Year Income Tax Exemption (post IMB approval)",
                "Section 56(2)(viib) 'Angel Tax' exemption under Form-2",
                "80% rebate on Patent applications and 50% rebate on Trademark filings",
                "Exemption from Prior Turnover and Prior Experience in Public Procurement",
                "Direct eligibility for Startup India Seed Fund Scheme (SISFS)"
            ] if is_all_valid else []
        }


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = set()


# --------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ System Control")

    # Backend Connection Mode Selector
    if IS_CLOUD_ENV:
        profile_options = [
            f"Live Cloud API ({DEFAULT_CLOUD_URL})",
            "Localhost API (http://127.0.0.1:8000)",
            "Direct Engine (Standalone / In-Process)",
            "Custom URL"
        ]
        default_idx = 0
    else:
        profile_options = [
            "Localhost API (http://127.0.0.1:8000)",
            f"Live Cloud API ({DEFAULT_CLOUD_URL})",
            "Direct Engine (Standalone / In-Process)",
            "Custom URL"
        ]
        default_idx = 0

    env_choice = st.selectbox(
        "Connection Profile",
        options=profile_options,
        index=default_idx,
        help="Select whether to use the live Cloud API, local FastAPI server, or embedded direct Python engine."
    )

    if env_choice.startswith("Live Cloud API"):
        api_url = DEFAULT_CLOUD_URL
        is_online = check_api_health(api_url)
    elif env_choice.startswith("Localhost API"):
        api_url = DEFAULT_LOCAL_URL
        is_online = check_api_health(api_url)
    elif env_choice == "Direct Engine (Standalone / In-Process)":
        api_url = "direct"
        is_online = False
    else:
        api_url = st.text_input("Custom API URL", value=DEFAULT_LOCAL_URL)
        is_online = check_api_health(api_url)

    # Status Display Badge
    if api_url == "direct":
        st.markdown(
            '<div class="status-badge-standalone">⚡ Direct Python Engine (Local In-Process)</div>',
            unsafe_allow_html=True
        )
    elif is_online:
        st.markdown(
            f'<div class="status-badge-online">🟢 API Connected: {api_url}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="status-badge-offline">🟡 API Offline / Waking Up: {api_url}</div>',
            unsafe_allow_html=True
        )
        st.caption("ℹ️ Cloud backends sleep after inactivity (~30s to wake up).")

    if st.button("🔄 Test / Ping Connection", use_container_width=True, key="ping_btn"):
        check_api_health.clear()
        st.rerun()

    st.markdown("---")

    # Processing Engine Selector
    endpoint_mode = st.radio(
        "Select Processing Engine:",
        options=[
            "LangGraph Agent (/agent)",
            "Direct RAG Pipeline (/ask)"
        ],
        index=0,
        help="LangGraph Agent handles multi-turn memory, statutory tools, and HITL approvals. Direct RAG focuses on verified citations and strict refusals."
    )

    st.markdown("---")
    st.markdown("### 💡 Recommended Inquiries")

    example_categories = {
        "🏛️ DPIIT Eligibility": [
            "What is DPIIT Startup Recognition?",
            "Can an LLP apply for DPIIT recognition?",
            "How long is a company eligible to be recognized as a startup under DPIIT?"
        ],
        "💰 Funding & Schemes": [
            "What is the Startup India Seed Fund Scheme?",
            "What is the Fund of Funds for Startups?",
            "What is the Credit Guarantee Scheme for Startups?"
        ],
        "⚖️ Tax & IPR Rebates": [
            "What is the income tax exemption under Section 80-IAC?",
            "What intellectual property benefits are available to eligible startups?"
        ],
        "📝 Mutating Action (Approval Gate)": [
            "Please submit my application for startup registration: TechSetu Solutions Pvt Ltd"
        ],
        "🛡️ Safety & Refusal Test": [
            "What are the lunar exploration subsidies offered by NASA to Indian startups?",
            "Will the government give 5 crore cash unconditionally to any college student?"
        ]
    }

    for cat_name, queries in example_categories.items():
        with st.expander(cat_name, expanded=(cat_name == "🏛️ DPIIT Eligibility")):
            for q in queries:
                if st.button(q, key=f"btn_{hash(q)}", use_container_width=True):
                    st.session_state["queued_prompt"] = q

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.session_state.pending_approval = None
        st.session_state.feedback_submitted = set()
        st.rerun()

    st.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8; text-align: center; margin-top: 1.5rem;">
            StartupSetu v2.1 · Gazette G.S.R. 127(E)<br/>
            Engineered by Shrikar Bhorkade
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">
            <span>🇮🇳</span> Official Indian Startup Advisory & Policy Engine
        </div>
        <div class="hero-title">StartupSetu AI Platform</div>
        <div class="hero-subtitle">
            Autonomous regulatory advisory, statutory eligibility evaluation under Gazette Notification G.S.R. 127(E),
            and zero-hallucination policy guidance with verifiable citations for Indian entrepreneurs and founders.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# NAVIGATION TABS
# --------------------------------------------------
tab_form, tab_chat = st.tabs([
    "🚀 'Am I a startup?' Eligibility Form",
    "💬 AI Chat Assistant (/ask & /agent)"
])


# --------------------------------------------------
# TAB 1: 'Am I a startup?' ST.FORM
# --------------------------------------------------
with tab_form:
    st.markdown("### 📋 Official DPIIT Startup Recognition Evaluation")
    st.markdown(
        "Evaluate your entity's compliance against the 4 statutory pillars defined by the **Ministry of Commerce and Industry** "
        "(Gazette Notification G.S.R. 127(E)) for Section 80-IAC tax exemptions, patent rebates, and seed funding access."
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
                help="Under statutory rules, only Private Limited Company, LLP, or Registered Partnership firms qualify for recognition."
            )
            form_date = st.date_input(
                "2. Incorporation Date",
                value=datetime(2023, 6, 1),
                min_value=datetime(2000, 1, 1),
                max_value=datetime.now(),
                help="The period of existence must not exceed 10 years from the date of incorporation."
            )

        with col2:
            form_turnover = st.number_input(
                "3. Annual Turnover (₹ in Crores)",
                min_value=0.0,
                max_value=1000.0,
                value=2.5,
                step=0.5,
                help="Turnover for any financial year since incorporation must not exceed ₹100 Crore."
            )
            form_innovative = st.checkbox(
                "4. Working towards innovation, development or improvement of products/services, or a scalable business model",
                value=True,
                help="The entity must work towards innovation, development, or deployment of technology/processes or a scalable model with high employment potential."
            )

        submit_eligibility = st.form_submit_button(
            "🔍 Evaluate Statutory Eligibility",
            use_container_width=True,
            type="primary"
        )

    if submit_eligibility:
        with st.spinner("Evaluating compliance against Gazette Notification G.S.R. 127(E)..."):
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

        st.markdown("---")

        # Verdict Header
        if is_eligible:
            st.success("🎉 **VERDICT: ELIGIBLE FOR OFFICIAL DPIIT STARTUP RECOGNITION**")
            st.markdown(f"**Assessment Summary:** {result.get('summary')}")
        else:
            st.error("❌ **VERDICT: NOT CURRENTLY ELIGIBLE FOR DPIIT RECOGNITION**")
            st.markdown("**Reasons for Ineligibility:**")
            for reason in result.get("reasons", []):
                st.markdown(f"- ⚠️ **{reason}**")

        # Metrics Breakdown across 4 pillars
        st.markdown("#### 📊 Compliance Breakdown Across 4 Statutory Pillars:")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label="Entity Type Pillar",
                value="Qualified" if criteria.get("entity_type_valid") else "Disqualified",
                delta="Pvt Ltd / LLP / Partnership" if criteria.get("entity_type_valid") else "Non-Compliant"
            )
        with m2:
            st.metric(
                label="Age Pillar (≤ 10 Years)",
                value="Compliant" if criteria.get("age_under_10_years") else "Exceeded",
                delta=f"{years_active} years operational"
            )
        with m3:
            st.metric(
                label="Turnover Pillar (≤ ₹100 Cr)",
                value="Compliant" if criteria.get("turnover_under_100cr") else "Exceeded",
                delta=f"₹{form_turnover} Cr reported"
            )
        with m4:
            st.metric(
                label="Innovation Pillar",
                value="Satisfied" if criteria.get("innovative_scalable") else "Missing",
                delta="Innovative Model" if criteria.get("innovative_scalable") else "Required"
            )

        # Cited DPIIT Statutory Rule Box
        st.markdown("---")
        cited = result.get("cited_rule", {})
        rules_html = "".join(f"<li>{r}</li>" for r in cited.get("rules", []))
        st.markdown(
            f"""
            <div class="rule-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem;">
                    📜 Statutory Authority & Citation Reference
                </div>
                <b>Regulatory Body:</b> {cited.get('notification', 'DPIIT, Ministry of Commerce and Industry')}<br/>
                <b>Notification Framework:</b> {cited.get('title', 'DPIIT Startup Recognition Definition')}<br/>
                <b>Gazette Reference:</b> Gazette Notification G.S.R. 127(E) &mdash;
                <a href="{cited.get('source_url', 'https://www.startupindia.gov.in/')}" target="_blank">Access Official Startup India Portal</a><br/><br/>
                <b>Statutory Conditions:</b>
                <ul style="margin-top: 0.4rem; padding-left: 1.25rem;">
                    {rules_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Recommended Benefits
        benefits = result.get("recommended_benefits", [])
        if benefits:
            st.markdown("#### 🎁 Statutory Benefits Unlocked Upon Recognition:")
            b_cols = st.columns(2)
            for idx, b in enumerate(benefits):
                with b_cols[idx % 2]:
                    st.markdown(f"- ✅ **{b}**")


# --------------------------------------------------
# TAB 2: AI CHAT ASSISTANT (/ask & /agent)
# --------------------------------------------------
with tab_chat:
    active_engine_label = "LangGraph Autonomous Agent (/agent)" if "Agent" in endpoint_mode else "Direct RAG Knowledge Base (/ask)"
    st.markdown(f"### 💬 Interactive Advisory Console &mdash; `{active_engine_label}`")
    st.markdown(
        "Ask questions regarding Indian startup registration, statutory exemptions, Seed Fund schemes, and policy definitions. "
        "Every response is strictly grounded with verifiable government citations."
    )

    # Quick Prompts
    st.markdown("##### ⚡ Quick Queries:")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        if st.button("🏛️ DPIIT 10-Yr Rule", key="chip_dpiit", use_container_width=True):
            st.session_state["queued_prompt"] = "How long is a company eligible to be recognized as a startup under DPIIT?"
            st.rerun()
    with q_col2:
        if st.button("💰 Seed Fund Scheme", key="chip_seed", use_container_width=True):
            st.session_state["queued_prompt"] = "What is the Startup India Seed Fund Scheme?"
            st.rerun()
    with q_col3:
        if st.button("⚖️ 80-IAC Tax Exemption", key="chip_tax", use_container_width=True):
            st.session_state["queued_prompt"] = "What is the income tax exemption under Section 80-IAC?"
            st.rerun()
    with q_col4:
        if st.button("📝 Register Application", key="chip_reg", use_container_width=True):
            st.session_state["queued_prompt"] = "Please submit my application for startup registration: TechSetu Solutions Pvt Ltd"
            st.rerun()

    st.markdown("---")

    # Render Chat History
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Citations Display
            citations = msg.get("citations", [])
            if citations:
                with st.expander(f"📚 Citations & Official Sources ({len(citations)})", expanded=False):
                    for c in citations:
                        title = c.get("title", "Official Government Gazette")
                        source = c.get("source", "https://www.startupindia.gov.in/")
                        page = c.get("page", 1)
                        st.markdown(
                            f"""
                            <div class="citation-card">
                                📄 <b>{title}</b> &mdash; Page {page}<br/>
                                🔗 <a href="{source}" target="_blank">Access Official Government Document</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # Execution Engine & Telemetry Footer
            engine_info = msg.get("engine")
            metrics = msg.get("metrics")
            if msg["role"] == "assistant" and (engine_info or metrics):
                tag_parts = []
                if engine_info:
                    tag_parts.append(f"⚙️ {engine_info}")
                if metrics and metrics.get("latency_ms"):
                    tag_parts.append(f"⚡ {metrics['latency_ms']} ms")
                if metrics and metrics.get("cached"):
                    tag_parts.append("💾 Cached Hit")
                if metrics and metrics.get("total_tokens"):
                    tag_parts.append(f"📊 {metrics['total_tokens']} tokens")
                if tag_parts:
                    st.markdown(f'<div class="engine-tag">{" · ".join(tag_parts)}</div>', unsafe_allow_html=True)

            # Thumbs Up / Down Feedback Widget
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"
                col_up, col_down, col_status = st.columns([1, 1, 6])
                with col_up:
                    if st.button("👍 Helpful", key=f"up_{idx}", disabled=fb_key in st.session_state.feedback_submitted):
                        q_text = st.session_state.messages[idx - 1]["content"] if idx > 0 else "N/A"
                        save_feedback(
                            question=q_text,
                            answer=msg["content"],
                            rating="thumbs_up",
                            mode=endpoint_mode
                        )
                        st.session_state.feedback_submitted.add(fb_key)
                        st.toast("Thank you for your rating! 👍", icon="✅")
                        st.rerun()
                with col_down:
                    if st.button("👎 Poor", key=f"down_{idx}", disabled=fb_key in st.session_state.feedback_submitted):
                        q_text = st.session_state.messages[idx - 1]["content"] if idx > 0 else "N/A"
                        save_feedback(
                            question=q_text,
                            answer=msg["content"],
                            rating="thumbs_down",
                            mode=endpoint_mode
                        )
                        st.session_state.feedback_submitted.add(fb_key)
                        st.toast("Feedback recorded! 👎", icon="📝")
                        st.rerun()
                with col_status:
                    if fb_key in st.session_state.feedback_submitted:
                        st.caption("✓ Feedback recorded")

    # Human-in-the-Loop Action Approval Card
    if st.session_state.pending_approval:
        st.markdown("---")
        st.warning(
            "⚠️ **Human-in-the-Loop Approval Required**\n\n"
            "The autonomous agent has formulated a mutating action that requires explicit human confirmation before persisting to the official database."
        )
        col_app, col_rej = st.columns(2)
        with col_app:
            if st.button("✅ Approve & Persist Action", use_container_width=True, type="primary"):
                with st.spinner("Executing approved action..."):
                    res = call_agent_api(
                        api_url_str=api_url,
                        query="Approved by user",
                        thread_id=st.session_state.thread_id,
                        approved=True
                    )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": res.get("response", "Action completed successfully."),
                        "citations": res.get("citations", []),
                        "engine": res.get("engine", "LangGraph Agent")
                    })
                    st.session_state.pending_approval = None
                    st.rerun()

        with col_rej:
            if st.button("❌ Reject Action", use_container_width=True):
                with st.spinner("Cancelling action..."):
                    res = call_agent_api(
                        api_url_str=api_url,
                        query="Rejected by user",
                        thread_id=st.session_state.thread_id,
                        approved=False
                    )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": res.get("response", "Action was rejected and cancelled."),
                        "citations": [],
                        "engine": res.get("engine", "LangGraph Agent")
                    })
                    st.session_state.pending_approval = None
                    st.rerun()

    # Chat Input Processing
    prompt_input = st.chat_input("Ask about DPIIT startup recognition, 80-IAC tax exemption, Seed Fund schemes...")
    queued = st.session_state.pop("queued_prompt", None)
    user_prompt = queued or prompt_input

    if user_prompt:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Assistant Generation
        with st.chat_message("assistant"):
            with st.spinner("Analyzing verified government records..."):
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
                metrics = result.get("metrics", {})
                engine = result.get("engine", "StartupSetu Engine")

                st.markdown(response_text)

                if citations:
                    with st.expander(f"📚 Citations & Official Sources ({len(citations)})", expanded=True):
                        for c in citations:
                            st.markdown(
                                f"""
                                <div class="citation-card">
                                    📄 <b>{c.get('title', 'Official Gazette')}</b> &mdash; Page {c.get('page', 1)}<br/>
                                    🔗 <a href="{c.get('source', 'https://www.startupindia.gov.in/')}" target="_blank">Access Official Documentation</a>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                # Append to messages
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "citations": citations,
                    "metrics": metrics,
                    "engine": engine
                })

                if result.get("status") == "needs_approval":
                    st.session_state.pending_approval = result.get("pending_action")
                    st.rerun()
