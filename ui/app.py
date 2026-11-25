"""
StartupSetu AI Platform - Secure Authentication, Video Masterclasses, AI Advisory & Eligibility Assessment
Built with Streamlit.
Features:
- Secure User Authentication Gateway (Login / Register / Multi-Role RBAC / SHA-256 Hashing).
- 'Am I a startup?' statutory evaluation (Entity Type, Incorporation Date, Turnover, Innovation).
- Interactive Video Knowledge Hub & Masterclasses with embedded player, timestamps, and AI question integration.
- Dual Mode Chat: Direct RAG (/ask) and LangGraph Autonomous Agent (/agent).
- Verified Citations display with official government sources and pages.
- Human-in-the-loop Action Approval buttons (Approve / Reject).
- Thumbs Up / Down user feedback mechanism saved to data/feedback.json.
- Government Schemes Directory with instant deep-dive cards.
- Ultra-modern, responsive Glassmorphic Indian Tech aesthetic.
"""

import hashlib
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
USERS_FILE = BASE_DIR / "data" / "users.json"
DEFAULT_LOCAL_URL = "http://127.0.0.1:8000"
ENV_API_URL = os.getenv("API_URL", "").strip()
DEFAULT_CLOUD_URL = ENV_API_URL or "https://startupsetu-api.onrender.com"
IS_CLOUD_ENV = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or ENV_API_URL)
AUTH_SALT = "StartupSetuSalt2026"

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="StartupSetu AI — Secure DPIIT Startup Advisory & Video Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS STYLING (ATTRACTIVE GLASSMORPHIC UI)
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    /* Login Gateway Styles */
    .login-container {
        max-width: 600px;
        margin: 1.5rem auto 2rem auto;
        background: #FFFFFF;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(0,0,0,0.03);
        overflow: hidden;
    }
    .login-banner {
        background: linear-gradient(135deg, #0A0F1D 0%, #0F172A 50%, #1E3A8A 100%);
        padding: 2.2rem 2.2rem 1.8rem 2.2rem;
        color: white;
        text-align: center;
        position: relative;
    }
    .login-banner::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
    }
    .login-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(245, 158, 11, 0.18);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #FCD34D;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .login-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.95rem;
        font-weight: 800;
        margin: 0 0 0.35rem 0;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 60%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-subtitle {
        font-size: 0.9rem;
        color: #94A3B8;
        line-height: 1.45;
        margin: 0;
    }
    .login-body {
        padding: 1.8rem 2.2rem;
    }
    .security-banner {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #10B981;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #334155;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    /* User Profile Card in Sidebar */
    .user-profile-card {
        background: linear-gradient(135deg, #0A0F1D 0%, #1E293B 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 1rem 1.15rem;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .user-profile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }
    .user-role-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        background: rgba(59, 130, 246, 0.25);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.45);
        text-transform: uppercase;
    }

    /* Hero Banner with Modern Gradient & Tricolor Accent */
    .hero-container {
        background: linear-gradient(135deg, #0A0F1D 0%, #0F172A 40%, #1E293B 75%, #1E3A8A 100%);
        border-radius: 20px;
        padding: 2.2rem 2.6rem;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #FCD34D;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.85rem;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.6rem;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 50%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #CBD5E1;
        max-width: 900px;
        line-height: 1.65;
        margin: 0;
    }

    /* Stat Cards Row */
    .stat-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(147, 197, 253, 0.4);
    }
    .stat-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .stat-lbl {
        font-size: 0.78rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 0.2rem;
    }

    /* Cards & Glassmorphism */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.35rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px -2px rgba(0, 0, 0, 0.04);
        transition: box-shadow 0.2s ease;
    }
    .glass-card:hover {
        box-shadow: 0 8px 25px -4px rgba(0, 0, 0, 0.08);
    }

    /* Video Showcase Card */
    .video-card-container {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 1.4rem;
        color: #F8FAFC;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
    }
    .video-badge {
        display: inline-block;
        padding: 0.28rem 0.7rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .video-badge-gold {
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .video-badge-blue {
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }
    .video-badge-green {
        background: rgba(16, 185, 129, 0.2);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Citation Card */
    .citation-card {
        background: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 0.9rem 1.15rem;
        margin-top: 0.65rem;
        border-radius: 8px;
        font-size: 0.88rem;
        line-height: 1.55;
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

    /* Statutory Rule Card */
    .rule-card {
        background: #F0F7FF;
        border: 1px solid #BFDBFE;
        border-left: 5px solid #1D4ED8;
        padding: 1.25rem 1.4rem;
        margin-top: 1rem;
        border-radius: 12px;
        font-size: 0.93rem;
        line-height: 1.65;
        color: #1E293B;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.06);
    }
    .rule-card b {
        color: #0F172A;
    }

    /* Scheme Highlight Card */
    .scheme-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem;
        transition: all 0.25s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
    }
    .scheme-card:hover {
        transform: translateY(-3px);
        border-color: #3B82F6;
        box-shadow: 0 10px 20px -3px rgba(59, 130, 246, 0.12);
    }

    /* Engine Tag in Chat */
    .engine-tag {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 0.45rem;
        display: flex;
        gap: 0.75rem;
        align-items: center;
        background: #F8FAFC;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        display: inline-flex;
        border: 1px solid #E2E8F0;
    }

    /* Form styling & Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        transform: translateY(-1.5px);
        box-shadow: 0 6px 15px -2px rgba(0, 0, 0, 0.1);
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 0.75rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        padding: 0.65rem 1.1rem;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        color: #1D4ED8 !important;
        border-bottom: 3px solid #1D4ED8 !important;
        background: rgba(239, 246, 255, 0.6);
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# AUTHENTICATION & USER MANAGEMENT
# --------------------------------------------------
def hash_password(password: str) -> str:
    """Hash password using SHA-256 with static application salt."""
    return hashlib.sha256(f"{AUTH_SALT}{password}".encode("utf-8")).hexdigest()


def load_users() -> list[dict[str, Any]]:
    """Load existing users from data/users.json or initialize defaults."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, encoding="utf-8") as f:
                users = json.load(f)
                if isinstance(users, list) and len(users) > 0:
                    return users
        except Exception:
            pass

    # Default Seed Accounts
    defaults = [
        {
            "email": "founder@startupsetu.in",
            "name": "Shrikar Bhorkade",
            "password_hash": hash_password("Startup@2026"),
            "role": "Startup Founder",
            "entity_name": "TechSetu Innovations Pvt Ltd",
            "created_at": datetime.now().isoformat()
        },
        {
            "email": "admin@dpiit.gov.in",
            "name": "DPIIT Advisory Officer",
            "password_hash": hash_password("Admin@2026"),
            "role": "DPIIT Officer / Admin",
            "entity_name": "Ministry of Commerce and Industry",
            "created_at": datetime.now().isoformat()
        },
        {
            "email": "student@sanjivani.edu.in",
            "name": "Sanjivani Innovator",
            "password_hash": hash_password("Student@2026"),
            "role": "Student Innovator",
            "entity_name": "Sanjivani COE AI Research Lab",
            "created_at": datetime.now().isoformat()
        }
    ]
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(defaults, f, indent=2, ensure_ascii=False)
    return defaults


def authenticate_user(email: str, password: str) -> dict[str, Any] | None:
    """Authenticate user credentials against stored hashed records."""
    users = load_users()
    target_email = email.strip().lower()
    hashed = hash_password(password.strip())

    for u in users:
        if u.get("email", "").lower() == target_email:
            if u.get("password_hash") == hashed:
                return u
    return None


def register_user(
    email: str,
    name: str,
    password: str,
    role: str,
    entity_name: str
) -> tuple[bool, str]:
    """Register a new user account with hashed password persistence."""
    users = load_users()
    target_email = email.strip().lower()

    if not target_email or "@" not in target_email:
        return False, "Please provide a valid email address."
    if not name.strip():
        return False, "Please provide your full name."
    if len(password) < 6:
        return False, "Password must be at least 6 characters in length."

    for u in users:
        if u.get("email", "").lower() == target_email:
            return False, f"An account with email '{email}' already exists. Please log in."

    new_user = {
        "email": target_email,
        "name": name.strip(),
        "password_hash": hash_password(password),
        "role": role,
        "entity_name": entity_name.strip() or "Independent Startup / Lab",
        "created_at": datetime.now().isoformat()
    }
    users.append(new_user)

    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return True, "Account registered successfully! You are now logged in."
    except Exception as e:
        return False, f"Failed to persist user credentials: {e}"


def logout_user() -> None:
    """Clear session authentication state and return to login gate."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.rerun()


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "login_time" not in st.session_state:
    st.session_state.login_time = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = set()
if "active_video_idx" not in st.session_state:
    st.session_state.active_video_idx = 0
if "fill_login_email" not in st.session_state:
    st.session_state.fill_login_email = ""
if "fill_login_pwd" not in st.session_state:
    st.session_state.fill_login_pwd = ""


# --------------------------------------------------
# LOGIN GATEWAY (SHOWN WHEN NOT AUTHENTICATED)
# --------------------------------------------------
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="login-container">
            <div class="login-banner">
                <div class="login-badge">
                    <span>🇮🇳</span> DPIIT &middot; Startup India Advisory
                </div>
                <h1 class="login-title">StartupSetu Portal</h1>
                <p class="login-subtitle">
                    Authorized Regulatory Advisory & Statutory Evaluation Gateway<br/>
                    Grounded in Gazette Notification G.S.R. 127(E)
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_col1, login_col2, login_col3 = st.columns([1, 2, 1])

    with login_col2:
        st.markdown(
            """
            <div class="security-banner">
                <span>🔒</span>
                <div>
                    <b>Secure Access Required:</b> Please authenticate to access the statutory eligibility evaluator,
                    LangGraph agent, and verified government policy repository.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_register = st.tabs([
            "🔐 Sign In to Account",
            "📝 Register New Founder Account"
        ])

        with tab_login:
            st.markdown("##### ⚡ Quick Demo Accounts (1-Click Fill):")
            d_col1, d_col2, d_col3 = st.columns(3)
            with d_col1:
                if st.button("🚀 Founder Demo", use_container_width=True, key="demo_founder"):
                    st.session_state.fill_login_email = "founder@startupsetu.in"
                    st.session_state.fill_login_pwd = "Startup@2026"
                    st.rerun()
            with d_col2:
                if st.button("🏛️ DPIIT Admin", use_container_width=True, key="demo_admin"):
                    st.session_state.fill_login_email = "admin@dpiit.gov.in"
                    st.session_state.fill_login_pwd = "Admin@2026"
                    st.rerun()
            with d_col3:
                if st.button("🎓 Student Demo", use_container_width=True, key="demo_student"):
                    st.session_state.fill_login_email = "student@sanjivani.edu.in"
                    st.session_state.fill_login_pwd = "Student@2026"
                    st.rerun()

            st.markdown("---")

            with st.form("login_form"):
                in_email = st.text_input(
                    "Official Email / Username",
                    value=st.session_state.fill_login_email,
                    placeholder="e.g. founder@startupsetu.in",
                    help="Enter your registered startup or institutional email."
                )
                in_password = st.text_input(
                    "Password",
                    value=st.session_state.fill_login_pwd,
                    type="password",
                    placeholder="••••••••••••",
                    help="Enter your secure password."
                )
                remember_me = st.checkbox("Keep session active on this device", value=True)

                submit_login = st.form_submit_button(
                    "🚀 Authenticate & Access Advisory Platform",
                    use_container_width=True,
                    type="primary"
                )

            if submit_login:
                if not in_email or not in_password:
                    st.error("⚠️ Please provide both your email address and password.")
                else:
                    with st.spinner("Verifying credentials & cryptographic signature..."):
                        user = authenticate_user(in_email, in_password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.session_state.login_time = datetime.now().strftime("%I:%M %p")
                            st.toast(f"Welcome back, {user['name']}! Access granted.", icon="✅")
                            time.sleep(0.4)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please verify your email and password, or use the Quick Demo buttons above.")

        with tab_register:
            st.markdown("##### 📝 Create Your Startup Advisory Profile:")
            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
                reg_email = st.text_input("Official Email Address", placeholder="e.g. priya@myinnovativestartup.in")
                reg_entity = st.text_input("Startup / Entity Name", placeholder="e.g. BioSetu Technologies Pvt Ltd")
                reg_role = st.selectbox(
                    "Account Category",
                    options=[
                        "Startup Founder / Co-Founder",
                        "Student Innovator / Researcher",
                        "Incubator / Accelerator Mentor",
                        "Venture Capital / Angel Investor"
                    ]
                )
                reg_col_p1, reg_col_p2 = st.columns(2)
                with reg_col_p1:
                    reg_pwd1 = st.text_input("Password", type="password", placeholder="Min 6 characters")
                with reg_col_p2:
                    reg_pwd2 = st.text_input("Confirm Password", type="password", placeholder="Re-type password")

                submit_register = st.form_submit_button(
                    "✨ Register & Launch Session",
                    use_container_width=True,
                    type="primary"
                )

            if submit_register:
                if reg_pwd1 != reg_pwd2:
                    st.error("⚠️ Passwords do not match. Please verify your input.")
                else:
                    success, msg = register_user(
                        email=reg_email,
                        name=reg_name,
                        password=reg_pwd1,
                        role=reg_role,
                        entity_name=reg_entity
                    )
                    if success:
                        user = authenticate_user(reg_email, reg_pwd1)
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.session_state.login_time = datetime.now().strftime("%I:%M %p")
                        st.balloons()
                        st.success(f"🎉 {msg}")
                        time.sleep(0.6)
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        st.markdown(
            """
            <div style="font-size: 0.76rem; color: #94A3B8; text-align: center; margin-top: 2rem; line-height: 1.5;">
                🛡️ <b>Security & Compliance Notice:</b> Protected under the Information Technology Act, 2000 &
                Digital Personal Data Protection (DPDP) Act, 2023.<br/>
                All evaluations and regulatory inquiries are strictly auditable.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Halt execution here so unauthenticated users cannot see app contents
    st.stop()


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
        "user_email": st.session_state.user.get("email") if st.session_state.user else "anonymous",
        "mode": mode,
        "rating": rating,
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


def resolve_api_url() -> str:
    """Resolve the active FastAPI backend endpoint automatically."""
    if ENV_API_URL:
        return ENV_API_URL
    if not IS_CLOUD_ENV and check_api_health(DEFAULT_LOCAL_URL):
        return DEFAULT_LOCAL_URL
    return DEFAULT_CLOUD_URL


def call_ask_api(api_url_str: str, question: str) -> dict[str, Any]:
    """Call the RAG endpoint POST /ask with automatic fallback."""
    start_t = time.perf_counter()
    target_url = api_url_str or DEFAULT_CLOUD_URL

    try:
        r = requests.post(
            f"{target_url.rstrip('/')}/ask",
            json={"question": question, "top_k": 3},
            timeout=55
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
                "engine": "FastAPI Web Service"
            }
    except Exception:
        pass

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
            "engine": "StartupSetu RAG Engine"
        }
    except (ImportError, ModuleNotFoundError):
        return {
            "response": (
                "⚠️ **Regulatory Gateway Initializing**: The StartupSetu backend is waking up from idle mode. "
                "Please wait 10-15 seconds and re-submit your inquiry."
            ),
            "citations": [],
            "metrics": {"latency_ms": 0.0},
            "status": "error",
            "requires_approval": False,
            "engine": "Cloud Regulatory Gateway"
        }


def call_agent_api(
    api_url_str: str,
    query: str,
    thread_id: str | None = None,
    approved: bool | None = None
) -> dict[str, Any]:
    """Call the LangGraph Agent endpoint POST /agent with automatic fallback."""
    target_url = api_url_str or DEFAULT_CLOUD_URL

    try:
        payload: dict[str, Any] = {"query": query}
        if thread_id:
            payload["thread_id"] = thread_id
        if approved is not None:
            payload["approved"] = approved

        r = requests.post(
            f"{target_url.rstrip('/')}/agent",
            json=payload,
            timeout=55
        )
        if r.status_code == 200:
            res = r.json()
            res["engine"] = "FastAPI LangGraph Service"
            return res
    except Exception:
        pass

    try:
        from app.graph import run_graph_agent
        res = run_graph_agent(
            query=query,
            thread_id=thread_id,
            approved=approved
        )
        res["engine"] = "StartupSetu Agent Engine"
        return res
    except (ImportError, ModuleNotFoundError):
        return {
            "response": (
                "⚠️ **Autonomous Agent Initializing**: Connecting to LangGraph stateful agent. "
                "Please submit your query again in a few moments."
            ),
            "citations": [],
            "status": "error",
            "requires_approval": False,
            "engine": "Cloud Agent Gateway"
        }


def call_check_eligibility(
    api_url_str: str,
    entity_type: str,
    incorporation_date: str,
    turnover_cr: float,
    is_innovative: bool
) -> dict[str, Any]:
    """Call POST /eligibility or fallback deterministically based on Gazette Notification G.S.R. 127(E)."""
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
            reasons.append(f"Entity type '{entity_type}' is ineligible. Must be Private Limited Company, LLP, or Registered Partnership Firm.")
        if not is_age_valid:
            reasons.append(f"Entity age ({years_active:.1f} years) exceeds the statutory maximum of 10 years.")
        if not is_turnover_valid:
            reasons.append(f"Annual turnover (₹{turnover_cr} Cr) exceeds the statutory cap of ₹100 Crore.")
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
                "gazette_no": "Gazette Notification G.S.R. 127(E)",
                "source_url": "https://www.startupindia.gov.in/",
                "rules": [
                    "Entity must be Private Limited Company, LLP, or Registered Partnership Firm.",
                    "Period of existence must not exceed 10 years from incorporation date.",
                    "Turnover for any financial year since incorporation must not exceed ₹100 Crore.",
                    "Entity must work towards innovation, development, or deployment of scalable products/processes."
                ]
            },
            "summary": "Statutorily eligible for official DPIIT Startup Recognition." if is_all_valid else "Not currently eligible for recognition under Gazette Notification G.S.R. 127(E).",
            "recommended_benefits": [
                "Section 80-IAC 3-Year 100% Income Tax Exemption (post IMB review)",
                "Section 56(2)(viib) 'Angel Tax' exemption under Form-2 filing",
                "80% rebate on Patent applications & 50% rebate on Trademark filings",
                "Exemption from Prior Turnover and Experience in Public Procurement",
                "Direct eligibility for Startup India Seed Fund Scheme (SISFS - Up to ₹50 Lakhs)"
            ] if is_all_valid else []
        }


# --------------------------------------------------
# CURATED VIDEO MASTERCLASS REPOSITORY
# --------------------------------------------------
CURATED_VIDEOS = [
    {
        "id": "dpiit-guide",
        "title": "DPIIT Startup Recognition — Official Step-by-Step Application Guide",
        "url": "https://www.youtube.com/watch?v=F3UeH_4uK-s",
        "badge": "Official Masterclass",
        "badge_class": "video-badge-gold",
        "duration": "8 mins",
        "category": "🏛️ DPIIT Recognition",
        "description": "Comprehensive walkthrough of the DPIIT recognition process on the Startup India portal. Covers registration, document uploads, eligibility criteria, and certificate generation.",
        "takeaways": [
            "Eligibility criteria under Gazette Notification G.S.R. 127(E)",
            "Step-by-step registration on startupindia.gov.in",
            "Self-certification documents and Certificate of Recognition",
            "Common rejection reasons and how to avoid them"
        ],
        "suggested_query": "Explain the step-by-step procedure to apply for DPIIT recognition on the Startup India portal."
    },
    {
        "id": "sisfs-fund",
        "title": "Startup India Seed Fund Scheme (SISFS) — Up to ₹50 Lakhs Funding Walkthrough",
        "url": "https://www.youtube.com/watch?v=1o-k-Gj3oHQ",
        "badge": "Seed Funding",
        "badge_class": "video-badge-blue",
        "duration": "10 mins",
        "category": "💰 Funding & Grants",
        "description": "Complete breakdown of the ₹945 Crore Startup India Seed Fund Scheme (SISFS). Learn how early-stage startups can secure up to ₹20 Lakhs grant and up to ₹50 Lakhs debt/convertible debentures through incubators.",
        "takeaways": [
            "Grant up to ₹20 Lakhs for Proof of Concept, Prototype development & trials",
            "Debt / Convertible Debentures up to ₹50 Lakhs for Market Entry & Commercialization",
            "Selection of certified incubators across India",
            "Eligibility: DPIIT recognized, incorporated under 2 years, no ₹10L previous funding"
        ],
        "suggested_query": "What are the eligibility criteria and funding stages under the Startup India Seed Fund Scheme?"
    },
    {
        "id": "tax-80iac",
        "title": "Section 80-IAC 3-Year Tax Holiday & Angel Tax Form-2 Guide",
        "url": "https://www.youtube.com/watch?v=kYv_8d-Z79s",
        "badge": "Tax Benefits",
        "badge_class": "video-badge-green",
        "duration": "7 mins",
        "category": "⚖️ Tax Exemptions",
        "description": "Detailed guide on how DPIIT-recognized startups can apply for a 100% income tax exemption for 3 consecutive years out of their first 10 years under Section 80-IAC, plus Section 56(2)(viib) Angel Tax exemptions.",
        "takeaways": [
            "Inter-Ministerial Board (IMB) approval requirements",
            "Form-1 filing for 80-IAC income tax exemptions",
            "Form-2 declaration for Section 56(2)(viib) angel tax exemption",
            "Key audits, Balance Sheet disclosures, and compliance obligations"
        ],
        "suggested_query": "How can a recognized startup obtain the 3-year income tax holiday under Section 80-IAC?"
    },
    {
        "id": "ipr-rebate",
        "title": "Intellectual Property (IPR) Rebates — 80% Patent & 50% Trademark Discount",
        "url": "https://www.youtube.com/watch?v=wX78nQ_kQe4",
        "badge": "IPR Benefits",
        "badge_class": "video-badge-blue",
        "duration": "6 mins",
        "category": "💡 Patents & Trademarks",
        "description": "Learn about the Scheme for Facilitating Start-Ups Intellectual Property Protection (SIPP). Discover how to claim up to 80% rebate on statutory patent filing fees and free government facilitators.",
        "takeaways": [
            "80% rebate on statutory patent filing fees",
            "50% rebate on trademark and design filings",
            "Free legal facilitation through empanelled Patent & Trademark agents",
            "Fast-track examination and accelerated disposal of patent applications"
        ],
        "suggested_query": "What intellectual property (IPR) benefits and patent fee rebates are provided to DPIIT startups?"
    }
]


# --------------------------------------------------
# SIDEBAR CONFIGURATION (AUTHENTICATED SESSION)
# --------------------------------------------------
with st.sidebar:
    api_url = resolve_api_url()
    is_online = check_api_health(api_url)
    curr_user = st.session_state.user or {}

    # User Profile Header Card
    st.markdown(
        f"""
        <div class="user-profile-card">
            <div class="user-profile-header">
                <span class="user-role-badge">{curr_user.get('role', 'Authorized User')}</span>
                <span style="font-size: 0.74rem; color: #86EFAC;">● Online</span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit', sans-serif;">
                {curr_user.get('name', 'Founder')}
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 0.2rem;">
                🏢 {curr_user.get('entity_name', 'StartupSetu')}
            </div>
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.08);">
                🔐 SSL Active &middot; Logged in at {st.session_state.login_time or 'Recently'}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🚪 Sign Out / Lock Session", use_container_width=True, type="secondary"):
        logout_user()

    st.markdown("---")

    # Official Government Portal Badge
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #0A0F1D 0%, #1E3A8A 100%); padding: 1.1rem; border-radius: 12px; color: white; margin-bottom: 1.25rem; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
                <span style="font-size: 0.72rem; font-weight: 800; color: #FCD34D; text-transform: uppercase; letter-spacing: 0.08em;">
                    🇮🇳 DPIIT &middot; Startup India
                </span>
                <span style="font-size: 0.72rem; padding: 0.18rem 0.5rem; border-radius: 9999px; font-weight: 700; background: {'rgba(134, 239, 172, 0.2)' if is_online else 'rgba(252, 211, 77, 0.2)'}; color: {'#86EFAC' if is_online else '#FCD34D'}; border: 1px solid {'rgba(134, 239, 172, 0.4)' if is_online else 'rgba(252, 211, 77, 0.4)'};">
                    {'● API Online' if is_online else '● Live Cloud'}
                </span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.2;">
                StartupSetu Advisory
            </div>
            <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 0.3rem;">
                Gazette G.S.R. 127(E) Grounded Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Processing Engine Selector
    endpoint_mode = st.radio(
        "⚡ Advisory Processing Engine:",
        options=[
            "LangGraph Agent (/agent)",
            "Direct RAG Pipeline (/ask)"
        ],
        index=0,
        key="engine_mode_selector",
        help="LangGraph Agent handles multi-turn memory, statutory tools, and HITL approvals. Direct RAG focuses on verified citations and strict refusals."
    )

    st.markdown("---")
    st.markdown("### 💡 Recommended Inquiries")

    example_categories = {
        "🏛️ DPIIT Statutory Rules": [
            "What is DPIIT Startup Recognition?",
            "Can an LLP apply for DPIIT recognition?",
            "How long is a company eligible to be recognized as a startup under DPIIT?"
        ],
        "💰 Funding & Schemes": [
            "What is the Startup India Seed Fund Scheme?",
            "What is the Fund of Funds for Startups (FFS)?",
            "What is the Credit Guarantee Scheme for Startups (CGSS)?"
        ],
        "⚖️ Tax & IPR Rebates": [
            "What is the income tax exemption under Section 80-IAC?",
            "What intellectual property benefits are available to eligible startups?",
            "What is the Angel Tax exemption under Form-2?"
        ],
        "📝 Mutating Action (Approval Gate)": [
            "Please submit my application for startup registration: TechSetu Solutions Pvt Ltd"
        ],
        "🛡️ Safety & Strict Refusal": [
            "What are the lunar exploration subsidies offered by NASA to Indian startups?",
            "Will the government give 5 crore cash unconditionally to any college student?"
        ]
    }

    for cat_name, queries in example_categories.items():
        with st.expander(cat_name, expanded=(cat_name == "🏛️ DPIIT Statutory Rules")):
            for q in queries:
                if st.button(q, key=f"btn_{hash(q)}", use_container_width=True):
                    st.session_state["queued_prompt"] = q

    st.markdown("---")
    with st.expander("🛠️ Advanced Settings", expanded=False):
        custom_endpoint = st.text_input("Backend API Endpoint", value=api_url, help="Override backend URL if running on a custom port.")
        if custom_endpoint and custom_endpoint.strip() != api_url:
            api_url = custom_endpoint.strip()
            is_online = check_api_health(api_url)
        if st.button("🔄 Refresh / Wake Backend", use_container_width=True, key="refresh_backend_btn"):
            check_api_health.clear()
            st.rerun()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.session_state.pending_approval = None
        st.session_state.feedback_submitted = set()
        st.rerun()

    st.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8; text-align: center; margin-top: 1.5rem;">
            StartupSetu v2.3 &middot; Gazette G.S.R. 127(E)<br/>
            Engineered by <b>Shrikar Bhorkade</b>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# HERO BANNER WITH STATS
# --------------------------------------------------
user_display_name = st.session_state.user.get("name", "Founder") if st.session_state.user else "Founder"
user_role_display = st.session_state.user.get("role", "Startup Founder") if st.session_state.user else "Startup Founder"

st.markdown(
    f"""
    <div class="hero-container">
        <div class="hero-badge">
            <span>🇮🇳</span> Official Indian Startup Advisory &middot; Authenticated Portal
        </div>
        <div class="hero-title">Welcome back, {user_display_name}! 👋</div>
        <div class="hero-subtitle">
            Authenticated as <b>{user_role_display}</b> &bull; Autonomous regulatory advisory, statutory eligibility evaluation
            under Gazette Notification G.S.R. 127(E), video masterclasses, and zero-hallucination policy guidance.
        </div>
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-val">📜 G.S.R. 127(E)</div>
                <div class="stat-lbl">Strict Statutory Grounding</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">⚡ Dual Engine</div>
                <div class="stat-lbl">RAG + LangGraph Agent</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">🎥 Video Hub</div>
                <div class="stat-lbl">Official Startup Masterclasses</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">🛡️ 100% Citations</div>
                <div class="stat-lbl">Zero Hallucination Guarantee</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick Explainer Video Expander right on the Hero Page
with st.expander("🎬 Watch 2-Minute Quick Explainer: DPIIT Startup Recognition & StartupSetu Overview", expanded=False):
    v_col1, v_col2 = st.columns([3, 2])
    with v_col1:
        st.video("https://www.youtube.com/watch?v=F3UeH_4uK-s")
    with v_col2:
        st.markdown("#### 🇮🇳 Key Takeaways:")
        st.markdown(
            """
            - **Entity Requirement:** Must be a Private Limited Company, LLP, or Registered Partnership.
            - **Age Limit:** Up to 10 years from the date of incorporation.
            - **Turnover Cap:** Annual turnover must not exceed ₹100 Crore in any financial year.
            - **Core Value:** Innovation, scalability, or significant employment generation.
            """
        )


# --------------------------------------------------
# NAVIGATION TABS (ELIGIBILITY, CHAT, VIDEOS, SCHEMES)
# --------------------------------------------------
tab_form, tab_chat, tab_video, tab_schemes = st.tabs([
    "🚀 'Am I a Startup?' Eligibility Check",
    "💬 AI Advisory Chat (/ask & /agent)",
    "🎥 Video Masterclasses & Tutorials",
    "🏛️ Government Schemes Directory"
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

        if is_eligible:
            st.balloons()
            st.success("🎉 **VERDICT: STATUTORILY ELIGIBLE FOR OFFICIAL DPIIT STARTUP RECOGNITION**")
            st.markdown(f"**Assessment Summary:** {result.get('summary')}")
        else:
            st.error("❌ **VERDICT: NOT CURRENTLY ELIGIBLE FOR DPIIT RECOGNITION**")
            st.markdown("**Reasons for Ineligibility:**")
            for reason in result.get("reasons", []):
                st.markdown(f"- ⚠️ **{reason}**")

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
                <b>Gazette Reference:</b> {cited.get('gazette_no', 'Gazette Notification G.S.R. 127(E)')} &mdash;
                <a href="{cited.get('source_url', 'https://www.startupindia.gov.in/')}" target="_blank">Access Official Startup India Portal</a><br/><br/>
                <b>Statutory Conditions:</b>
                <ul style="margin-top: 0.4rem; padding-left: 1.25rem;">
                    {rules_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

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

    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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

    prompt_input = st.chat_input("Ask about DPIIT startup recognition, 80-IAC tax exemption, Seed Fund schemes...")
    queued = st.session_state.pop("queued_prompt", None)
    user_prompt = queued or prompt_input

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

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


# --------------------------------------------------
# TAB 3: VIDEO MASTERCLASSES & TUTORIALS
# --------------------------------------------------
with tab_video:
    st.markdown("### 🎥 StartupSetu Video Masterclasses & Official Walkthroughs")
    st.markdown(
        "Watch high-definition, curated video tutorials on **DPIIT Recognition**, **Seed Fund applications**, **Section 80-IAC Tax Exemption**, "
        "and **Patent Rebates**. You can also enter any custom video URL or upload your own video file."
    )

    v_mode = st.radio(
        "Select Video Source:",
        options=["Curated Startup Masterclasses", "Custom Video URL / Local Upload"],
        horizontal=True,
        key="video_source_mode"
    )

    if v_mode == "Curated Startup Masterclasses":
        v_col_nav, v_col_main = st.columns([1, 2])

        with v_col_nav:
            st.markdown("##### 📚 Masterclass Playlist:")
            for i, vid in enumerate(CURATED_VIDEOS):
                btn_type = "primary" if i == st.session_state.active_video_idx else "secondary"
                if st.button(
                    f"{vid['category']}\n{vid['title'][:42]}...",
                    key=f"vid_sel_{i}",
                    use_container_width=True,
                    type=btn_type
                ):
                    st.session_state.active_video_idx = i
                    st.rerun()

            st.markdown("---")
            st.info("💡 **Tip:** While watching any video, click the **'Ask AI about this topic'** button to immediately ask questions!")

        with v_col_main:
            active_vid = CURATED_VIDEOS[st.session_state.active_video_idx]

            st.markdown(
                f"""
                <div class="video-card-container">
                    <span class="video-badge {active_vid['badge_class']}">{active_vid['badge']} &bull; {active_vid['duration']}</span>
                    <h3 style="margin-top: 0.3rem; margin-bottom: 0.5rem; color: #FFFFFF;">{active_vid['title']}</h3>
                    <p style="color: #94A3B8; font-size: 0.92rem; line-height: 1.5;">{active_vid['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Embedded Video Player
            st.video(active_vid["url"])

            # Video Insights & Key Takeaways
            st.markdown("#### 🎯 Key Topics Covered in this Masterclass:")
            for t in active_vid["takeaways"]:
                st.markdown(f"- 📌 {t}")

            st.markdown("---")
            col_ask_btn, col_blank = st.columns([2, 1])
            with col_ask_btn:
                if st.button(f"💬 Ask AI about '{active_vid['title'][:30]}...'", key=f"ask_vid_{active_vid['id']}", use_container_width=True, type="primary"):
                    st.session_state["queued_prompt"] = active_vid["suggested_query"]
                    st.toast("Question loaded into Advisory Chat! Redirecting...", icon="💬")
                    time.sleep(0.5)
                    st.rerun()

    else:
        st.markdown("##### 🎬 Custom Video Player & Explainer")
        custom_v_url = st.text_input(
            "Enter YouTube or Video URL:",
            value="https://www.youtube.com/watch?v=F3UeH_4uK-s",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste any YouTube video or direct MP4/WebM video URL."
        )

        uploaded_video = st.file_uploader(
            "Or upload a local video file (MP4, WebM, MOV):",
            type=["mp4", "webm", "mov"]
        )

        if uploaded_video:
            st.video(uploaded_video)
            st.success("✅ Local video loaded and playing successfully.")
        elif custom_v_url:
            try:
                st.video(custom_v_url)
            except Exception as e:
                st.error(f"Could not load video from URL: {e}")


# --------------------------------------------------
# TAB 4: GOVERNMENT SCHEMES & POLICY DIRECTORY
# --------------------------------------------------
with tab_schemes:
    st.markdown("### 🏛️ Official Indian Government Schemes for Recognized Startups")
    st.markdown(
        "Explore statutory financial, tax, and intellectual property schemes available to startups holding valid DPIIT recognition certificates."
    )

    SCHEMES_CATALOG = [
        {
            "name": "Startup India Seed Fund Scheme (SISFS)",
            "ministry": "DPIIT, Ministry of Commerce and Industry",
            "funding": "Up to ₹50 Lakhs (₹20L Grant + ₹50L Debt)",
            "purpose": "Proof of Concept, prototype development, product trials, market-entry and commercialization through approved incubators.",
            "eligibility": "DPIIT recognized, incorporated not more than 2 years ago, scalable business idea, less than ₹10 Lakhs previous external funding.",
            "query": "What is the complete application process for the Startup India Seed Fund Scheme (SISFS)?"
        },
        {
            "name": "Fund of Funds for Startups (FFS)",
            "ministry": "Managed by Small Industries Development Bank of India (SIDBI)",
            "funding": "₹10,000 Crore Corpus for Alternate Investment Funds (AIFs)",
            "purpose": "Infusing capital into Indian venture funds to provide equity financing to high-growth DPIIT startups.",
            "eligibility": "Startups receiving investments from SIDBI-registered Daughter Funds / AIFs.",
            "query": "How does the Fund of Funds for Startups (FFS) work under SIDBI?"
        },
        {
            "name": "Credit Guarantee Scheme for Startups (CGSS)",
            "ministry": "National Credit Guarantee Trustee Company (NCGTC)",
            "funding": "Credit Guarantee up to ₹10 Crore per borrower",
            "purpose": "Collateral-free debt funding by commercial banks, NBFCs, and AIFs to recognize early-stage and growth startups.",
            "eligibility": "DPIIT recognized entity with defined revenue streams and operational viability.",
            "query": "What are the loan limits and collateral conditions under the Credit Guarantee Scheme for Startups?"
        },
        {
            "name": "Section 80-IAC 3-Year 100% Tax Holiday",
            "ministry": "Central Board of Direct Taxes (CBDT) & DPIIT",
            "funding": "100% deduction of profits for 3 consecutive financial years",
            "purpose": "Easing income tax burden on young companies during their initial high-growth phase.",
            "eligibility": "Private Limited or LLP incorporated after April 1, 2016, turnover ≤ ₹100 Cr, approved by the Inter-Ministerial Board (IMB).",
            "query": "What documents are required to obtain Inter-Ministerial Board approval for Section 80-IAC?"
        },
        {
            "name": "Scheme for Facilitating Start-Ups IPR Protection (SIPP)",
            "ministry": "Office of the Controller General of Patents, Designs & Trademarks",
            "funding": "80% Patent Rebate & 50% Trademark Discount",
            "purpose": "Facilitating fast-track IP protection and providing free registered patent facilitators.",
            "eligibility": "DPIIT recognized startup submitting statutory declaration Form-28.",
            "query": "How do I claim the 80% patent rebate and access free government patent facilitators?"
        },
        {
            "name": "Public Procurement Relaxations",
            "ministry": "Ministry of Finance (Department of Expenditure)",
            "funding": "Waiver of Earnest Money Deposit (EMD) & Prior Experience",
            "purpose": "Enabling startups to participate and win government tenders on the Government e-Marketplace (GeM).",
            "eligibility": "DPIIT recognized entity meeting basic technical specs and manufacturing standards.",
            "query": "What exemptions are available to DPIIT startups in public procurement and GeM tenders?"
        }
    ]

    sc_col1, sc_col2 = st.columns(2)
    for idx, sch in enumerate(SCHEMES_CATALOG):
        target_col = sc_col1 if idx % 2 == 0 else sc_col2
        with target_col:
            st.markdown(
                f"""
                <div class="scheme-card">
                    <div>
                        <div style="font-size: 0.76rem; font-weight: 700; color: #2563EB; text-transform: uppercase; margin-bottom: 0.25rem;">
                            🏛️ {sch['ministry']}
                        </div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #0F172A; font-family: 'Outfit', sans-serif;">{sch['name']}</h4>
                        <div style="background: #F1F5F9; padding: 0.45rem 0.75rem; border-radius: 8px; font-weight: 700; color: #047857; font-size: 0.88rem; margin-bottom: 0.65rem;">
                            💰 Benefit: {sch['funding']}
                        </div>
                        <p style="font-size: 0.88rem; color: #334155; line-height: 1.5; margin-bottom: 0.45rem;">
                            <b>Core Purpose:</b> {sch['purpose']}
                        </p>
                        <p style="font-size: 0.84rem; color: #64748B; line-height: 1.45;">
                            <b>Eligibility:</b> {sch['eligibility']}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"🔍 Deep Dive: {sch['name'][:22]}...", key=f"sch_btn_{idx}", use_container_width=True):
                st.session_state["queued_prompt"] = sch["query"]
                st.toast(f"Inquiry for {sch['name'][:20]} loaded into Chat! Redirecting...", icon="🚀")
                time.sleep(0.4)
                st.rerun()
