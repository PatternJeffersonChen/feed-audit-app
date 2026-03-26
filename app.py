import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import hashlib
from io import BytesIO
from collections import Counter

# ═════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pattern — Feed Audit",
    page_icon="https://cdn.prod.website-files.com/64fdbed8246bf837f498e3f0/6568ba5b9c2ae21778952712_Favicon%2032x32.png",
    layout="wide",
)

# ═════════════════════════════════════════════════════════════════════════════
# 2. BRAND CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════
BLUE = "#009BFF"
VIOLET = "#770BFF"
SEA = "#4CC3AE"
DARK = "#090A0F"
LIGHT = "#FCFCFC"
GRADIENT = f"linear-gradient(135deg, {VIOLET}, {BLUE})"

# Official Pattern logo SVG — wordmark paths recolored to white for dark bg
LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="191" height="38" viewBox="0 0 191 38" fill="none"><g clip-path="url(#clip0)"><path d="M23.1323 0.277129L0.336866 22.8367C-0.0379489 23.2076 -0.0379491 23.809 0.336866 24.1799L5.95075 29.7357C6.32557 30.1067 6.93326 30.1067 7.30808 29.7357L30.1035 7.1762C30.4783 6.80526 30.4783 6.20385 30.1035 5.83292L24.4896 0.277128C24.1148 -0.0938081 23.5071 -0.0938066 23.1323 0.277129Z" fill="#009BFF"/><path d="M32.5193 9.56975L19.1171 22.8332C18.7423 23.2042 18.7423 23.8056 19.1171 24.1765L24.731 29.7323C25.1058 30.1032 25.7135 30.1032 26.0884 29.7323L39.4905 16.4688C39.8654 16.0979 39.8654 15.4965 39.4905 15.1255L33.8767 9.56975C33.5018 9.19881 32.8942 9.19881 32.5193 9.56975Z" fill="#009BFF"/><path d="M72.0318 17.9793C72.0318 24.7983 66.8064 30.0154 60.5177 30.0154C56.9126 30.0154 54.1845 28.5504 52.4273 26.1703V37.4408C52.4273 37.5892 52.3677 37.7314 52.2618 37.8363C52.1558 37.9411 52.0121 38 51.8622 38H47.9977C47.8478 38 47.7041 37.9411 47.5981 37.8363C47.4921 37.7314 47.4326 37.5892 47.4326 37.4408V7.09944C47.4326 6.95113 47.4921 6.8089 47.5981 6.70403C47.7041 6.59916 47.8478 6.54025 47.9977 6.54025H51.8622C52.0121 6.54025 52.1558 6.59916 52.2618 6.70403C52.3677 6.8089 52.4273 6.95113 52.4273 7.09944V9.83398C54.1781 7.40976 56.9126 5.94482 60.5177 5.94482C66.8064 5.94482 72.0318 11.2075 72.0318 17.9793ZM67.0388 17.9793C67.0388 13.7263 63.8936 10.6578 59.733 10.6578C55.5724 10.6578 52.4273 13.7247 52.4273 17.9793C52.4273 22.2339 55.5708 25.3008 59.733 25.3008C63.8952 25.3008 67.0388 22.2355 67.0388 17.9793Z" fill="#FCFCFC"/><path d="M98.4814 7.09944V28.8608C98.4814 29.0091 98.4219 29.1513 98.3159 29.2562C98.2099 29.361 98.0662 29.42 97.9164 29.42H94.0534C93.9035 29.42 93.7598 29.361 93.6538 29.2562C93.5479 29.1513 93.4883 29.0091 93.4883 28.8608V26.1246C91.7375 28.5504 89.003 30.0154 85.3963 30.0154C79.1076 30.0154 73.8838 24.7527 73.8838 17.9793C73.8838 11.1619 79.1076 5.94482 85.3963 5.94482C89.003 5.94482 91.7311 7.40976 93.4883 9.7883V7.09944C93.4883 6.95113 93.5479 6.8089 93.6538 6.70403C93.7598 6.59916 93.9035 6.54025 94.0534 6.54025H97.9164C98.0662 6.54025 98.2099 6.59916 98.3159 6.70403C98.4219 6.8089 98.4814 6.95113 98.4814 7.09944ZM93.4883 17.9793C93.4883 13.7263 90.3432 10.6578 86.1826 10.6578C82.022 10.6578 78.8768 13.7247 78.8768 17.9793C78.8768 22.2339 82.022 25.3008 86.1826 25.3008C90.3432 25.3008 93.4883 22.2355 93.4883 17.9793Z" fill="#FCFCFC"/><path d="M139.785 25.4851C142.343 25.4851 144.31 24.4345 145.472 23.0168C145.557 22.9161 145.675 22.8489 145.806 22.8272C145.937 22.8055 146.071 22.8309 146.185 22.8986L149.33 24.718C149.398 24.7567 149.458 24.8092 149.504 24.8721C149.551 24.9351 149.584 25.007 149.6 25.0833C149.617 25.1596 149.617 25.2384 149.6 25.3147C149.584 25.391 149.551 25.463 149.505 25.5261C147.356 28.3378 144.023 30.0154 139.74 30.0154C132.11 30.0154 127.166 24.844 127.166 17.9793C127.166 11.206 132.113 5.94482 139.373 5.94482C146.263 5.94482 150.979 11.436 150.979 18.025C150.965 18.7152 150.904 19.4036 150.794 20.0853H132.387C133.173 23.6547 136.087 25.4851 139.785 25.4851ZM145.935 16.0576C145.241 12.1196 142.328 10.4294 139.323 10.4294C135.578 10.4294 133.034 12.6252 132.342 16.0576H145.935Z" fill="#FCFCFC"/><path d="M191.055 15.3712V28.8612C191.055 29.0095 190.996 29.1517 190.89 29.2566C190.784 29.3615 190.64 29.4204 190.49 29.4204H186.627C186.477 29.4204 186.334 29.3615 186.228 29.2566C186.122 29.1517 186.062 29.0095 186.062 28.8612V15.8753C186.062 12.3973 184.026 10.5669 180.883 10.5669C177.599 10.5669 175.011 12.4886 175.011 17.1559V28.8612C175.011 28.9348 174.997 29.0076 174.968 29.0756C174.94 29.1435 174.898 29.2052 174.845 29.2572C174.793 29.3091 174.73 29.3503 174.661 29.3783C174.593 29.4063 174.519 29.4206 174.445 29.4204H170.582C170.432 29.4204 170.288 29.3615 170.182 29.2566C170.076 29.1517 170.017 29.0095 170.017 28.8612V7.09988C170.017 6.95158 170.076 6.80934 170.182 6.70447C170.288 6.5996 170.432 6.54069 170.582 6.54069H174.446C174.521 6.54048 174.594 6.55479 174.663 6.5828C174.732 6.61081 174.794 6.65197 174.847 6.70392C174.899 6.75586 174.941 6.81758 174.97 6.88552C174.998 6.95347 175.013 7.02632 175.013 7.09988V9.46267C176.538 7.08256 179.035 5.93896 182.175 5.93896C187.356 5.94527 191.055 9.4233 191.055 15.3712Z" fill="#FCFCFC"/><path d="M165.186 6.12744C162.274 6.12744 159.456 7.27261 158.065 10.3805V7.09934C158.065 6.95103 158.006 6.8088 157.9 6.70393C157.794 6.59906 157.65 6.54014 157.5 6.54014H153.637C153.487 6.54014 153.344 6.59906 153.238 6.70393C153.132 6.8088 153.072 6.95103 153.072 7.09934V28.8607C153.072 29.009 153.132 29.1512 153.238 29.2561C153.344 29.3609 153.487 29.4198 153.637 29.4198H157.5C157.65 29.4198 157.794 29.3609 157.9 29.2561C158.006 29.1512 158.065 29.009 158.065 28.8607V17.8878C158.065 12.7637 161.823 11.4815 165.186 11.4815H166.926C167.076 11.4815 167.22 11.4226 167.326 11.3177C167.432 11.2129 167.491 11.0706 167.491 10.9223V6.68821C167.491 6.61464 167.477 6.54176 167.449 6.47373C167.42 6.40571 167.379 6.34387 167.326 6.29178C167.274 6.23969 167.211 6.19836 167.143 6.17016C167.074 6.14196 167 6.12744 166.926 6.12744H165.186Z" fill="#FCFCFC"/><path d="M112.505 11.2989C112.579 11.2991 112.653 11.2848 112.721 11.2568C112.79 11.2287 112.853 11.1876 112.905 11.1356C112.958 11.0837 113 11.022 113.028 10.954C113.057 10.8861 113.071 10.8132 113.071 10.7397V7.0994C113.071 7.02584 113.057 6.95299 113.028 6.88504C113 6.8171 112.958 6.75538 112.905 6.70343C112.853 6.65149 112.79 6.61033 112.721 6.58232C112.653 6.55431 112.579 6.54 112.505 6.54021H106.561V0.554469C106.56 0.408335 106.501 0.268486 106.397 0.164857C106.293 0.0612278 106.152 0.00205319 106.004 0H102.133C101.984 0 101.84 0.0589149 101.734 0.163784C101.628 0.268653 101.568 0.410887 101.568 0.559194V22.6718C101.568 27.369 103.857 29.6247 108.634 29.6247H112.506C112.656 29.6243 112.799 29.5652 112.905 29.4604C113.011 29.3557 113.071 29.2137 113.071 29.0655V25.6001C113.071 25.5265 113.057 25.4537 113.028 25.3857C113 25.3178 112.958 25.256 112.905 25.2041C112.853 25.1521 112.79 25.111 112.721 25.083C112.653 25.055 112.579 25.0407 112.505 25.0409H109.533C107.255 25.0409 106.561 24.4549 106.561 22.2827V11.2989H112.505Z" fill="#FCFCFC"/><path d="M126.061 11.2989C126.211 11.2989 126.354 11.24 126.46 11.1351C126.566 11.0302 126.626 10.888 126.626 10.7397V7.0994C126.626 6.9511 126.566 6.80886 126.46 6.70399C126.354 6.59912 126.211 6.54021 126.061 6.54021H120.124V0.554469C120.123 0.406981 120.063 0.265959 119.957 0.16211C119.851 0.0582605 119.708 -5.26628e-06 119.559 3.57006e-10H115.696C115.546 3.57006e-10 115.402 0.0589149 115.296 0.163784C115.19 0.268653 115.131 0.410887 115.131 0.559194V22.6718C115.131 27.369 117.418 29.6247 122.196 29.6247H126.069C126.218 29.6239 126.361 29.5646 126.467 29.4599C126.572 29.3552 126.632 29.2134 126.632 29.0655V25.6001C126.632 25.5264 126.617 25.4536 126.588 25.3858C126.559 25.318 126.516 25.2565 126.463 25.205C126.41 25.1535 126.347 25.1128 126.278 25.0855C126.209 25.0581 126.135 25.0446 126.061 25.0456H123.089C120.812 25.0456 120.118 24.4596 120.118 22.2874V11.2989H126.061Z" fill="#FCFCFC"/></g><defs><clipPath id="clip0"><rect width="191" height="38" fill="white"/></clipPath></defs></svg>'''

SCORE_COLORS = {"Excellent": SEA, "Good": BLUE, "Average": "#FFC107", "Below Average": "#FF9800", "Insufficient": "#FF5252"}
SCORE_MAP = {"Excellent": 5, "Good": 4, "Average": 3, "Below Average": 2, "Insufficient": 1}
WEIGHTING_MAP = {"Must have": 3, "Good to have": 2, "Bonus": 1}

# ═════════════════════════════════════════════════════════════════════════════
# 3. AUTHENTICATION
# ═════════════════════════════════════════════════════════════════════════════

def _write_client_secret_json():
    """Generate client_secret.json from st.secrets for streamlit-google-auth."""
    import json, os
    path = "/tmp/client_secret.json"
    if not os.path.exists(path):
        payload = {
            "web": {
                "client_id": st.secrets["google_oauth"]["client_id"],
                "client_secret": st.secrets["google_oauth"]["client_secret"],
                "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        with open(path, "w") as f:
            json.dump(payload, f)
    return path


def check_auth():
    """Gate access to @pattern.com users via Google OAuth or email fallback."""
    if st.session_state.get("authenticated"):
        return True

    # Check if Google OAuth secrets are configured
    has_oauth = False
    try:
        _ = st.secrets["google_oauth"]["client_id"]
        _ = st.secrets["google_oauth"]["client_secret"]
        has_oauth = True
    except Exception:
        pass

    if has_oauth:
        try:
            from streamlit_google_auth import Authenticate
            secret_path = _write_client_secret_json()
            redirect_uri = st.secrets["google_oauth"].get("redirect_uri", "http://localhost:8501")
            cookie_key = st.secrets["google_oauth"].get("cookie_key", "pattern_feed_audit_key")

            authenticator = Authenticate(
                secret_credentials_path=secret_path,
                cookie_name="pattern_feed_audit",
                cookie_key=cookie_key,
                redirect_uri=redirect_uri,
            )
            authenticator.check_authentification()

            if st.session_state.get("connected"):
                email = st.session_state.get("user_info", {}).get("email", "")
                if email.endswith("@pattern.com"):
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = st.session_state.get("user_info", {}).get("name", email)
                    return True
                else:
                    _inject_css()
                    st.markdown(f'<div style="text-align:center;margin:4rem 0 1rem;">{LOGO_SVG}</div>', unsafe_allow_html=True)
                    st.error(f"Access restricted to @pattern.com accounts. You signed in as **{email}**.")
                    authenticator.logout()
                    st.stop()
            else:
                _show_login_page(authenticator)
                st.stop()
        except ImportError:
            _show_password_gate()
            st.stop()
    else:
        # Fallback: email gate (no OAuth configured)
        _show_password_gate()
        st.stop()

    return False


def _show_login_page(authenticator=None):
    _inject_css()
    st.markdown(f'<div style="text-align:center;margin:4rem 0 1rem;">{LOGO_SVG}</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;color:#FCFCFC;">Product Feed Audit</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Sign in with your Pattern account to continue</p>', unsafe_allow_html=True)
    if authenticator:
        authenticator.login()


def _show_password_gate():
    _inject_css()
    st.markdown(f'<div style="text-align:center;margin:4rem 0 1rem;">{LOGO_SVG}</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;color:#FCFCFC;">Product Feed Audit</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Enter your Pattern email to continue</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email", placeholder="you@pattern.com", label_visibility="collapsed")
        if st.button("Sign In", use_container_width=True):
            if email and email.strip().lower().endswith("@pattern.com"):
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email.strip().lower()
                st.rerun()
            elif email:
                st.error("Access restricted to @pattern.com accounts")
            else:
                st.warning("Please enter your email")


# ═════════════════════════════════════════════════════════════════════════════
# 4. CSS INJECTION
# ═════════════════════════════════════════════════════════════════════════════

def _inject_css():
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background-color: {DARK};
        font-family: 'Wix Madefor Display', 'Source Sans Pro', sans-serif;
    }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li {{
        color: {LIGHT};
    }}
    section[data-testid="stSidebar"] {{
        background-color: #0E1117;
    }}

    /* Gradient buttons */
    .stButton > button {{
        background: {GRADIENT};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 15px;
        padding: 0.55rem 1.5rem;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0, 155, 255, 0.3);
        color: white;
        border: none;
    }}

    /* Metric cards — glassmorphism */
    [data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.2rem;
    }}

    /* Section headers */
    .section-header {{
        border-left: 3px solid {BLUE};
        padding-left: 12px;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        color: {LIGHT};
    }}

    /* Score badges */
    .score-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }}
    .score-excellent {{ background: rgba(76, 195, 174, 0.15); color: {SEA}; }}
    .score-good {{ background: rgba(0, 155, 255, 0.15); color: {BLUE}; }}
    .score-average {{ background: rgba(255, 193, 7, 0.15); color: #FFC107; }}
    .score-below-average {{ background: rgba(255, 152, 0, 0.15); color: #FF9800; }}
    .score-insufficient {{ background: rgba(255, 82, 82, 0.15); color: #FF5252; }}

    /* Overall score */
    .hero-score {{
        text-align: center;
        padding: 1.5rem;
    }}
    .hero-score .number {{
        font-size: 4.5rem;
        font-weight: 800;
        background: {GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        font-family: 'Wix Madefor Display', sans-serif;
    }}
    .hero-score .label {{
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Recommendation cards */
    .rec-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
    }}
    .rec-card.high {{ border-left: 3px solid #FF5252; }}
    .rec-card.medium {{ border-left: 3px solid #FFC107; }}
    .rec-card.low {{ border-left: 3px solid {SEA}; }}
    .rec-impact {{
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }}
    .rec-impact.high {{ color: #FF5252; }}
    .rec-impact.medium {{ color: #FFC107; }}
    .rec-impact.low {{ color: {SEA}; }}

    /* Category cards */
    .cat-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }}
    .cat-pct {{
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Wix Madefor Display', sans-serif;
    }}
    .cat-name {{
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.2rem;
    }}

    /* Hide Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Tabs */
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {BLUE};
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {LIGHT};
        padding: 10px 16px;
    }}

    /* Download button */
    .stDownloadButton > button {{
        background: transparent;
        border: 1px solid rgba(255,255,255,0.15);
        color: {LIGHT};
        border-radius: 8px;
    }}
    .stDownloadButton > button:hover {{
        border-color: {BLUE};
        color: {BLUE};
    }}

    /* Headings */
    .stApp h1 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 800; color: {LIGHT}; }}
    .stApp h2 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 700; color: {LIGHT}; }}
    .stApp h3 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 600; color: {LIGHT}; }}
</style>
""", unsafe_allow_html=True)


def score_badge(label: str) -> str:
    cls = label.lower().replace(" ", "-")
    return f'<span class="score-badge score-{cls}">{label}</span>'


# ═════════════════════════════════════════════════════════════════════════════
# 5. COLUMN DETECTION ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def find_col(df: pd.DataFrame, term: str) -> str | None:
    """Find column matching term (case-insensitive, supports partial & wildcard)."""
    cols = {c.lower().strip(): c for c in df.columns}
    if term.lower() in cols:
        return cols[term.lower()]
    for k, v in cols.items():
        if term.lower() in k:
            return v
    return None


# ═════════════════════════════════════════════════════════════════════════════
# 6. SCORING ENGINE
# ═════════════════════════════════════════════════════════════════════════════

AUDIT_ATTRS = [
    # (display, category, weighting, search_term, logic)
    ("Size", "Customer-Facing Attributes", "Good to have", "size", "fill"),
    ("Sale Price", "Customer-Facing Attributes", "Good to have", "sale price", "fill"),
    ("Regular Price", "Customer-Facing Attributes", "Must have", "price", "fill"),
    ("Product Condition", "Customer-Facing Attributes", "Good to have", "condition", "condition"),
    ("Material", "Customer-Facing Attributes", "Good to have", "material", "fill"),
    ("Gender", "Customer-Facing Attributes", "Good to have", "gender", "fill"),
    ("Color", "Customer-Facing Attributes", "Good to have", "color", "fill"),
    ("Brand Name", "Customer-Facing Attributes", "Must have", "brand", "fill"),
    ("Age Group", "Customer-Facing Attributes", "Good to have", "age group", "fill"),
    ("Product Type", "Internal Attributes", "Must have", "product type", "fill"),
    ("Product Link", "Internal Attributes", "Must have", "link", "fill"),
    ("Product ID", "Internal Attributes", "Must have", "id", "fill"),
    ("Google Product Category", "Internal Attributes", "Good to have", "google product category", "fill"),
    ("GTIN", "Internal Attributes", "Must have", "gtin", "fill"),
    ("Custom Labels", "Internal Attributes", "Good to have", "custom label", "custom_label"),
    ("Availability", "Internal Attributes", "Good to have", "availability", "availability"),
    ("Additional Image Links", "Internal Attributes", "Good to have", "additional image link", "fill"),
    ("Product Title", "Key Shopping Content", "Must have", "title", "fill"),
    ("Product Description", "Key Shopping Content", "Must have", "description", "fill"),
    ("Image URL", "Key Shopping Content", "Must have", "image link", "fill"),
]


def _fill_rate(df, col):
    total = len(df)
    if total == 0:
        return 0.0
    filled = df[col].apply(lambda x: (isinstance(x, str) and len(x.strip()) > 0) or (pd.notna(x) and not isinstance(x, str))).sum()
    return filled / total


def _rate_to_score(r):
    if r >= 1.0: return "Excellent"
    if r >= 0.8: return "Good"
    if r >= 0.5: return "Average"
    if r > 0.2: return "Below Average"
    return "Insufficient"


@st.cache_data(show_spinner=False)
def run_audit(_df_hash, df):
    results = []
    for name, cat, weight, term, logic in AUDIT_ATTRS:
        col = find_col(df, term)
        found = col is not None
        rate = 0.0
        label = "Insufficient"

        if logic == "custom_label":
            cnt = sum(1 for i in range(5) for c in df.columns if f"custom label {i}" in c.lower() or f"custom_label_{i}" in c.lower())
            # Deduplicate: count unique label indices found
            found_indices = set()
            for i in range(5):
                for c in df.columns:
                    if f"custom label {i}" in c.lower() or f"custom_label_{i}" in c.lower():
                        found_indices.add(i)
                        break
            rate = len(found_indices) / 5
            found = rate > 0
            label = _rate_to_score(rate)
        elif found:
            if logic == "fill":
                rate = _fill_rate(df, col)
            elif logic == "condition":
                rate = df[col].astype(str).str.lower().str.strip().eq("new").sum() / max(len(df), 1)
            elif logic == "availability":
                rate = df[col].astype(str).str.lower().str.strip().eq("in stock").sum() / max(len(df), 1)
            label = _rate_to_score(rate)

        nw = WEIGHTING_MAP.get(weight, 1)
        ns = SCORE_MAP.get(label, 1)
        results.append({
            "Category": cat, "Attribute": name, "Weighting": weight,
            "Found": found, "Fill Rate": rate, "Score": label,
            "Num Weight": nw, "Num Score": ns,
            "Weighted": nw * ns, "Potential": nw * 5,
        })
    return results


# ═════════════════════════════════════════════════════════════════════════════
# 7. GMC VALIDATION ENGINE
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def run_gmc_validation(_df_hash, df):
    """Simulate Google Merchant Center validation — flag likely disapprovals."""
    issues = []
    total = len(df)

    id_col = find_col(df, "id")
    title_col = find_col(df, "title")
    desc_col = find_col(df, "description")
    price_col = find_col(df, "price")
    link_col = find_col(df, "link")
    img_col = find_col(df, "image link")
    avail_col = find_col(df, "availability")
    cond_col = find_col(df, "condition")
    brand_col = find_col(df, "brand")
    gtin_col = find_col(df, "gtin")

    # Required field checks
    required = {"id": id_col, "title": title_col, "description": desc_col,
                "price": price_col, "link": link_col, "image_link": img_col}
    for field, col in required.items():
        if col is None:
            issues.append({"severity": "error", "field": field, "count": total,
                           "message": f"Column '{field}' not found — required by Google Merchant Center"})
        else:
            missing = df[col].isna() | (df[col].astype(str).str.strip() == "")
            n = missing.sum()
            if n > 0:
                issues.append({"severity": "error", "field": field, "count": int(n),
                               "message": f"{n:,} products missing required field '{field}'"})

    # Title length checks
    if title_col:
        titles = df[title_col].astype(str)
        too_long = (titles.str.len() > 150).sum()
        if too_long > 0:
            issues.append({"severity": "warning", "field": "title", "count": int(too_long),
                           "message": f"{too_long:,} titles exceed 150 characters (will be truncated)"})
        too_short = (titles.str.len() < 25).sum()
        if too_short > 0:
            issues.append({"severity": "warning", "field": "title", "count": int(too_short),
                           "message": f"{too_short:,} titles under 25 characters (poor discoverability)"})

    # Description length
    if desc_col:
        descs = df[desc_col].astype(str)
        too_long_d = (descs.str.len() > 5000).sum()
        if too_long_d > 0:
            issues.append({"severity": "warning", "field": "description", "count": int(too_long_d),
                           "message": f"{too_long_d:,} descriptions exceed 5,000 characters"})

    # Price checks
    if price_col:
        prices = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        zero_price = (prices == 0).sum() + prices.isna().sum()
        if zero_price > 0:
            issues.append({"severity": "error", "field": "price", "count": int(zero_price),
                           "message": f"{zero_price:,} products with invalid or zero price"})

    # Invalid availability
    if avail_col:
        valid_avail = {"in stock", "out of stock", "preorder", "backorder", "in_stock", "out_of_stock"}
        invalid = ~df[avail_col].astype(str).str.lower().str.strip().isin(valid_avail) & df[avail_col].notna() & (df[avail_col].astype(str).str.strip() != "")
        n = invalid.sum()
        if n > 0:
            issues.append({"severity": "error", "field": "availability", "count": int(n),
                           "message": f"{n:,} products with invalid availability value"})

    # Invalid condition
    if cond_col:
        valid_cond = {"new", "refurbished", "used"}
        invalid_c = ~df[cond_col].astype(str).str.lower().str.strip().isin(valid_cond) & df[cond_col].notna() & (df[cond_col].astype(str).str.strip() != "")
        n = invalid_c.sum()
        if n > 0:
            issues.append({"severity": "warning", "field": "condition", "count": int(n),
                           "message": f"{n:,} products with non-standard condition value"})

    # HTTPS check on links
    if link_col:
        http_only = df[link_col].astype(str).str.startswith("http://").sum()
        if http_only > 0:
            issues.append({"severity": "warning", "field": "link", "count": int(http_only),
                           "message": f"{http_only:,} product links use HTTP instead of HTTPS"})

    if img_col:
        http_img = df[img_col].astype(str).str.startswith("http://").sum()
        if http_img > 0:
            issues.append({"severity": "warning", "field": "image_link", "count": int(http_img),
                           "message": f"{http_img:,} image URLs use HTTP instead of HTTPS"})

    # Duplicate IDs
    if id_col:
        dups = df[id_col].dropna().astype(str)
        dup_count = dups.duplicated().sum()
        if dup_count > 0:
            issues.append({"severity": "error", "field": "id", "count": int(dup_count),
                           "message": f"{dup_count:,} duplicate product IDs (will cause overwrite conflicts)"})

    # GTIN missing for branded products
    if gtin_col and brand_col:
        has_brand = df[brand_col].astype(str).str.strip().ne("") & df[brand_col].notna()
        missing_gtin = df[gtin_col].isna() | (df[gtin_col].astype(str).str.strip() == "")
        n = (has_brand & missing_gtin).sum()
        if n > 0:
            issues.append({"severity": "warning", "field": "gtin", "count": int(n),
                           "message": f"{n:,} branded products missing GTIN (reduces impression eligibility)"})

    # Sale price > regular price
    sale_col = find_col(df, "sale price")
    if sale_col and price_col:
        sp = pd.to_numeric(df[sale_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        rp = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        bad = ((sp >= rp) & sp.notna() & rp.notna() & (rp > 0)).sum()
        if bad > 0:
            issues.append({"severity": "error", "field": "sale_price", "count": int(bad),
                           "message": f"{bad:,} products where sale price >= regular price"})

    issues.sort(key=lambda x: (0 if x["severity"] == "error" else 1, -x["count"]))
    return issues


# ═════════════════════════════════════════════════════════════════════════════
# 8. CONTENT ANALYSIS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_titles(_df_hash, df):
    col = find_col(df, "title")
    if col is None:
        return None
    titles = df[col].astype(str)
    lengths = titles.str.len()
    avg_len = lengths.mean()

    # Component detection
    brand_col = find_col(df, "brand")
    color_col = find_col(df, "color")
    size_col = find_col(df, "size")
    material_col = find_col(df, "material")
    gender_col = find_col(df, "gender")

    components = {}
    if brand_col:
        brands = df[brand_col].astype(str).str.strip()
        components["Brand"] = sum(1 for t, b in zip(titles, brands) if b and b.lower() != "nan" and b.lower() in t.lower()) / max(len(df), 1)
    if color_col:
        colors = df[color_col].astype(str).str.strip()
        components["Color"] = sum(1 for t, c in zip(titles, colors) if c and c.lower() != "nan" and c.lower() in t.lower()) / max(len(df), 1)
    if size_col:
        sizes = df[size_col].astype(str).str.strip()
        components["Size"] = sum(1 for t, s in zip(titles, sizes) if s and s.lower() != "nan" and s.lower() in t.lower()) / max(len(df), 1)
    if material_col:
        materials = df[material_col].astype(str).str.strip()
        components["Material"] = sum(1 for t, m in zip(titles, materials) if m and m.lower() != "nan" and m.lower() in t.lower()) / max(len(df), 1)
    if gender_col:
        genders = df[gender_col].astype(str).str.strip()
        components["Gender"] = sum(1 for t, g in zip(titles, genders) if g and g.lower() != "nan" and g.lower() in t.lower()) / max(len(df), 1)

    # Word frequency
    all_words = " ".join(titles).lower().split()
    stop = {"the","a","an","and","or","for","with","in","of","to","is","by","on","at","from","&","-","–","/",""}
    word_freq = Counter(w.strip(".,()[]") for w in all_words if w.strip(".,()[]") not in stop and len(w.strip(".,()[]")) > 1)

    # Duplicates
    dup_titles = titles[titles.duplicated(keep=False) & (titles.str.strip() != "")]
    dup_count = dup_titles.nunique()

    return {
        "avg_len": round(avg_len),
        "lengths": lengths,
        "components": components,
        "top_words": word_freq.most_common(30),
        "dup_count": dup_count,
        "dup_total": len(dup_titles),
        "short_count": int((lengths < 40).sum()),
        "long_count": int((lengths > 150).sum()),
    }


@st.cache_data(show_spinner=False)
def analyze_descriptions(_df_hash, df):
    col = find_col(df, "description")
    if col is None:
        return None
    descs = df[col].astype(str)
    lengths = descs.str.len()
    title_col = find_col(df, "title")
    same_as_title = 0
    if title_col:
        same_as_title = (df[title_col].astype(str).str.strip() == descs.str.strip()).sum()
    dup_count = descs[descs.duplicated(keep=False) & (descs.str.strip() != "")].nunique()
    return {
        "avg_len": round(lengths.mean()),
        "lengths": lengths,
        "same_as_title": int(same_as_title),
        "dup_count": dup_count,
    }


# ═════════════════════════════════════════════════════════════════════════════
# 9. PRICING ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_pricing(_df_hash, df):
    price_col = find_col(df, "price")
    sale_col = find_col(df, "sale price")
    if price_col is None:
        return None

    prices = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
    result = {"prices": prices.dropna(), "zero_count": int((prices == 0).sum()), "missing_count": int(prices.isna().sum())}

    if sale_col:
        sale_prices = pd.to_numeric(df[sale_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        has_sale = sale_prices.notna() & (sale_prices > 0) & (prices > 0) & (sale_prices < prices)
        result["on_sale_count"] = int(has_sale.sum())
        result["on_sale_pct"] = has_sale.sum() / max(len(df), 1)
        if has_sale.any():
            discounts = ((prices[has_sale] - sale_prices[has_sale]) / prices[has_sale] * 100)
            result["avg_discount"] = round(discounts.mean(), 1)
        else:
            result["avg_discount"] = 0
    return result


# ═════════════════════════════════════════════════════════════════════════════
# 10. IMAGE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_images(_df_hash, df):
    img_col = find_col(df, "image link")
    add_img_col = find_col(df, "additional image link")
    if img_col is None:
        return None

    missing_img = (df[img_col].isna() | (df[img_col].astype(str).str.strip() == "")).sum()
    has_additional = 0
    if add_img_col:
        has_additional = (df[add_img_col].notna() & (df[add_img_col].astype(str).str.strip() != "")).sum()

    # Check for duplicate images
    imgs = df[img_col].astype(str).str.strip()
    dup_imgs = imgs[imgs.duplicated(keep=False) & (imgs != "")].nunique()

    return {
        "missing": int(missing_img),
        "has_additional": int(has_additional),
        "has_additional_pct": has_additional / max(len(df), 1),
        "dup_images": dup_imgs,
        "total": len(df),
    }


# ═════════════════════════════════════════════════════════════════════════════
# 11. TAXONOMY ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_taxonomy(_df_hash, df):
    pt_col = find_col(df, "product type")
    gpc_col = find_col(df, "google product category")
    result = {}

    for label, col in [("Product Type", pt_col), ("Google Product Category", gpc_col)]:
        if col is None:
            continue
        vals = df[col].astype(str).str.strip()
        filled = vals[vals.ne("") & vals.ne("nan")]
        depths = filled.str.count(">") + 1
        result[label] = {
            "fill_rate": len(filled) / max(len(df), 1),
            "avg_depth": round(depths.mean(), 1) if len(depths) > 0 else 0,
            "max_depth": int(depths.max()) if len(depths) > 0 else 0,
            "unique_count": filled.nunique(),
            "top_values": filled.value_counts().head(10).to_dict(),
            "depth_dist": depths.value_counts().sort_index().to_dict(),
        }
    return result


# ═════════════════════════════════════════════════════════════════════════════
# 12. RECOMMENDATIONS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def generate_recommendations(results, gmc_issues, title_data, desc_data, pricing, images, taxonomy, df):
    recs = []
    total = len(df)

    # GMC errors = highest priority
    errors = [i for i in gmc_issues if i["severity"] == "error"]
    if errors:
        for e in errors[:3]:
            recs.append(("high", e["message"],
                         "Fix this before uploading to Merchant Center to avoid disapprovals."))

    # Missing GTINs
    gtin_issue = next((i for i in gmc_issues if "gtin" in i["field"].lower() and "missing" in i["message"].lower()), None)
    if gtin_issue:
        recs.append(("high", f"{gtin_issue['count']:,} branded products missing GTIN",
                      "Adding GTINs typically improves impression share by 20-40% for branded products."))

    # Title optimization
    if title_data:
        if title_data["avg_len"] < 80:
            recs.append(("high", f"Average title length is only {title_data['avg_len']} characters (target: 120+)",
                          "Add brand, color, size, material, and product type to titles. Longer, attribute-rich titles improve click-through rate."))
        if title_data["dup_count"] > 0:
            recs.append(("medium", f"{title_data['dup_count']} duplicate titles detected across {title_data['dup_total']:,} products",
                          "Duplicate titles cause products to compete against each other. Differentiate with unique attributes."))
        # Component gaps
        for comp, rate in title_data.get("components", {}).items():
            if rate < 0.5:
                recs.append(("medium", f"Only {rate:.0%} of titles contain {comp.lower()}",
                              f"Adding {comp.lower()} to titles improves relevance matching and ad quality."))

    # Description
    if desc_data:
        if desc_data["avg_len"] < 200:
            recs.append(("medium", f"Average description length is only {desc_data['avg_len']} characters",
                          "Rich descriptions (500+ chars) improve product discoverability in Shopping and free listings."))
        if desc_data["same_as_title"] > 0:
            recs.append(("medium", f"{desc_data['same_as_title']:,} products have description identical to title",
                          "Descriptions should expand on the title with unique selling points, specs, and benefits."))

    # Missing attributes
    for r in results:
        if not r["Found"] and r["Weighting"] == "Must have":
            recs.append(("high", f"Required attribute '{r['Attribute']}' not found in feed",
                          "This field is required by Google Merchant Center."))
        elif not r["Found"] and r["Weighting"] == "Good to have":
            recs.append(("low", f"Optional attribute '{r['Attribute']}' not found in feed",
                          "Adding this attribute improves product matching and filter eligibility."))
        elif r["Found"] and r["Fill Rate"] < 0.5 and r["Weighting"] == "Must have":
            recs.append(("high", f"'{r['Attribute']}' has only {r['Fill Rate']:.0%} fill rate",
                          "Low fill rate on required fields leads to disapprovals for affected products."))

    # Custom labels
    cl_result = next((r for r in results if r["Attribute"] == "Custom Labels"), None)
    if cl_result and cl_result["Fill Rate"] < 0.6:
        recs.append(("low", f"Only {cl_result['Fill Rate']:.0%} of custom label slots are in use",
                      "Use custom labels for bid segmentation: margin tiers, seasonality, best-sellers, price buckets, new arrivals."))

    # Images
    if images and images["has_additional_pct"] < 0.5:
        recs.append(("low", f"Only {images['has_additional_pct']:.0%} of products have additional images",
                      "Products with multiple images see 10-15% higher conversion rates in Shopping."))

    # Taxonomy depth
    if taxonomy:
        for label, data in taxonomy.items():
            if data["avg_depth"] < 3:
                recs.append(("low", f"{label} average depth is {data['avg_depth']} levels",
                              "Deeper categorization (3+ levels) improves Google's ability to match products to relevant queries."))

    # Deduplicate
    seen = set()
    unique_recs = []
    for r in recs:
        key = r[1][:60]
        if key not in seen:
            seen.add(key)
            unique_recs.append(r)

    # Sort: high first, then medium, then low
    order = {"high": 0, "medium": 1, "low": 2}
    unique_recs.sort(key=lambda x: order.get(x[0], 3))
    return unique_recs


# ═════════════════════════════════════════════════════════════════════════════
# 13. REPORT GENERATION
# ═════════════════════════════════════════════════════════════════════════════

def generate_excel_report(results, gmc_issues, recs, df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Summary
        summary_data = []
        for r in results:
            summary_data.append({
                "Category": r["Category"], "Attribute": r["Attribute"],
                "Weighting": r["Weighting"], "Found": "Yes" if r["Found"] else "No",
                "Fill Rate": f"{r['Fill Rate']:.0%}", "Score": r["Score"],
                "Weighted Score": f"{r['Weighted']} / {r['Potential']}",
            })
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Audit Scores", index=False)

        # GMC Issues
        if gmc_issues:
            pd.DataFrame(gmc_issues).to_excel(writer, sheet_name="GMC Issues", index=False)

        # Recommendations
        if recs:
            rec_data = [{"Priority": r[0].upper(), "Issue": r[1], "Action": r[2]} for r in recs]
            pd.DataFrame(rec_data).to_excel(writer, sheet_name="Recommendations", index=False)

        # Raw data sample
        df.head(500).to_excel(writer, sheet_name="Feed Sample", index=False)

    return output.getvalue()


# ═════════════════════════════════════════════════════════════════════════════
# 14. CHART BUILDERS
# ═════════════════════════════════════════════════════════════════════════════

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Wix Madefor Display, Source Sans Pro, sans-serif", color="#888"),
)


def chart_radar(results):
    cats = {}
    for r in results:
        cats.setdefault(r["Category"], []).append(r["Weighted"] / max(r["Potential"], 1) * 100)
    names = list(cats.keys())
    vals = [sum(v) / len(v) for v in cats.values()]
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=names + [names[0]],
        fill="toself", fillcolor="rgba(0,155,255,0.1)",
        line=dict(color=BLUE, width=2), marker=dict(size=6, color=BLUE),
    ))
    fig.update_layout(**CHART_LAYOUT, showlegend=False,
                      polar=dict(bgcolor="rgba(0,0,0,0)",
                                 radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9, color="#555")),
                                 angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=11, color=LIGHT))),
                      margin=dict(l=60, r=60, t=30, b=30), height=380)
    return fig


def chart_bars(results, value_key="Weighted", max_key="Potential", x_title="Score %"):
    attrs = [r["Attribute"] for r in results]
    pcts = [r[value_key] / max(r[max_key], 1) * 100 for r in results]
    colors = [SCORE_COLORS.get(r["Score"], "#FF5252") for r in results]
    fig = go.Figure(go.Bar(
        y=attrs, x=pcts, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{p:.0f}%" for p in pcts], textposition="outside",
        textfont=dict(color=LIGHT, size=10),
    ))
    fig.update_layout(**CHART_LAYOUT, xaxis=dict(range=[0, 110], title=x_title, gridcolor="rgba(255,255,255,0.04)"),
                      yaxis=dict(tickfont=dict(color=LIGHT, size=10), autorange="reversed"),
                      margin=dict(l=170, r=50, t=10, b=30), height=max(350, len(attrs) * 28))
    return fig


def chart_fill_rates(results):
    attrs = [r["Attribute"] for r in results]
    rates = [r["Fill Rate"] * 100 for r in results]
    colors = []
    for r in rates:
        if r >= 100: colors.append(SEA)
        elif r >= 80: colors.append(BLUE)
        elif r >= 50: colors.append("#FFC107")
        elif r > 20: colors.append("#FF9800")
        else: colors.append("#FF5252")
    fig = go.Figure(go.Bar(
        y=attrs, x=rates, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{r:.0f}%" for r in rates], textposition="outside",
        textfont=dict(color=LIGHT, size=10),
    ))
    fig.update_layout(**CHART_LAYOUT, xaxis=dict(range=[0, 110], title="Fill Rate %", gridcolor="rgba(255,255,255,0.04)"),
                      yaxis=dict(tickfont=dict(color=LIGHT, size=10), autorange="reversed"),
                      margin=dict(l=170, r=50, t=10, b=30), height=max(350, len(attrs) * 28))
    return fig


def chart_histogram(series, title="", target=None, target_label=""):
    fig = go.Figure(go.Histogram(x=series, nbinsx=40, marker=dict(color=BLUE, line=dict(width=0))))
    if target:
        fig.add_vline(x=target, line_dash="dash", line_color=SEA, annotation_text=target_label, annotation_font_color=SEA)
    fig.update_layout(**CHART_LAYOUT, xaxis=dict(title=title, gridcolor="rgba(255,255,255,0.04)"),
                      yaxis=dict(title="Products", gridcolor="rgba(255,255,255,0.04)"),
                      margin=dict(l=50, r=20, t=20, b=40), height=280)
    return fig


# ═════════════════════════════════════════════════════════════════════════════
# 15. MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

_inject_css()
check_auth()

# ── Header ─────────────────────────────────────────────────────────────────
user_email = st.session_state.get("user_email", "")
st.markdown(
    f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">'
    f'<div>{LOGO_SVG}</div>'
    f'<div style="font-size:0.8rem;color:#555;">{user_email}</div>'
    f'</div>',
    unsafe_allow_html=True,
)
st.markdown('<h1 style="margin-top:0;margin-bottom:0.2rem;">Product Feed Audit</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#666;margin-bottom:1.5rem;">Upload a feed to get a comprehensive quality score, GMC readiness check, and prioritised recommendations.</p>', unsafe_allow_html=True)

# ── File Upload ────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload your product feed", type=["csv", "tsv", "xlsx", "xls", "txt"],
                            help="CSV, TSV, or Excel. Headers in first row.", label_visibility="collapsed")

if uploaded is None:
    st.markdown(
        '<div style="text-align:center;padding:5rem 2rem;color:#444;">'
        '<p style="font-size:3.5rem;margin-bottom:0.5rem;opacity:0.5;">&#x2191;</p>'
        '<p style="font-size:1.1rem;color:#666;">Drop a product feed file above to begin</p>'
        '<p style="font-size:0.85rem;color:#444;">Supports Google Merchant Center exports, Shopify feeds, WooCommerce feeds, and any CSV/Excel product file.</p>'
        '</div>', unsafe_allow_html=True)
    st.stop()

# ── Parse file ─────────────────────────────────────────────────────────────
try:
    name = uploaded.name.lower()
    if name.endswith((".csv", ".txt")):
        raw = uploaded.read()
        uploaded.seek(0)
        sample = raw[:4096].decode("utf-8", errors="replace")
        sep = "\t" if "\t" in sample else ","
        df = pd.read_csv(BytesIO(raw), sep=sep, dtype=str, on_bad_lines="skip")
    elif name.endswith(".tsv"):
        df = pd.read_csv(uploaded, sep="\t", dtype=str, on_bad_lines="skip")
    else:
        df = pd.read_excel(uploaded, dtype=str)
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

df.columns = df.columns.str.strip()
df_hash = hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()

# ── Run all analyses ───────────────────────────────────────────────────────
with st.spinner("Analysing feed..."):
    results = run_audit(df_hash, df)
    gmc_issues = run_gmc_validation(df_hash, df)
    title_data = analyze_titles(df_hash, df)
    desc_data = analyze_descriptions(df_hash, df)
    pricing = analyze_pricing(df_hash, df)
    images = analyze_images(df_hash, df)
    taxonomy = analyze_taxonomy(df_hash, df)
    recs = generate_recommendations(results, gmc_issues, title_data, desc_data, pricing, images, taxonomy, df)

total_weighted = sum(r["Weighted"] for r in results)
total_potential = sum(r["Potential"] for r in results)
overall_pct = total_weighted / max(total_potential, 1) * 100
overall_grade = "Excellent" if overall_pct >= 90 else "Good" if overall_pct >= 70 else "Average" if overall_pct >= 50 else "Below Average" if overall_pct > 30 else "Insufficient"
errors_count = sum(1 for i in gmc_issues if i["severity"] == "error")
warnings_count = sum(1 for i in gmc_issues if i["severity"] == "warning")

# ── Hero metrics ───────────────────────────────────────────────────────────
st.divider()
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="hero-score"><div class="number">{overall_pct:.0f}%</div><div class="label">Overall Score</div></div>', unsafe_allow_html=True)
with c2:
    st.metric("Products", f"{len(df):,}")
with c3:
    st.metric("Attributes Found", f"{sum(1 for r in results if r['Found'])} / {len(results)}")
with c4:
    st.metric("GMC Errors", f"{errors_count}", delta=f"{warnings_count} warnings" if warnings_count else None, delta_color="off")
with c5:
    st.metric("Priority Actions", f"{len(recs)}")

# ── Download report ────────────────────────────────────────────────────────
report_bytes = generate_excel_report(results, gmc_issues, recs, df)
st.download_button("Download Full Report (.xlsx)", data=report_bytes, file_name="feed_audit_report.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ── Tabs ───────────────────────────────────────────────────────────────────
tabs = st.tabs(["Priority Actions", "GMC Readiness", "Scores Overview", "Content Quality", "Pricing & Images", "Fill Rates", "Feed Data"])

# ────────────────────────────────────────────────────────────────────────────
# TAB 1: PRIORITY ACTIONS
# ────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    if not recs:
        st.success("No issues found — your feed looks great!")
    else:
        for priority, message, action in recs:
            st.markdown(
                f'<div class="rec-card {priority}">'
                f'<div class="rec-impact {priority}">{"&#x26A0; " if priority == "high" else ""}{priority} impact</div>'
                f'<div style="color:{LIGHT};font-weight:500;margin-bottom:0.3rem;">{message}</div>'
                f'<div style="color:#888;font-size:0.85rem;">{action}</div>'
                f'</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 2: GMC READINESS
# ────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    if not gmc_issues:
        st.success("No Merchant Center issues detected!")
    else:
        e_count = sum(1 for i in gmc_issues if i["severity"] == "error")
        w_count = sum(1 for i in gmc_issues if i["severity"] == "warning")
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric("Errors", e_count)
        with mc2:
            st.metric("Warnings", w_count)
        with mc3:
            readiness = "Ready" if e_count == 0 else "Not Ready"
            color = SEA if e_count == 0 else "#FF5252"
            st.markdown(f'<div style="padding:1rem;text-align:center;"><span style="font-size:1.5rem;font-weight:700;color:{color};">{readiness}</span><br><span style="color:#888;font-size:0.85rem;">GMC Upload Status</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Issues</div>', unsafe_allow_html=True)
        for issue in gmc_issues:
            icon = "&#x1F534;" if issue["severity"] == "error" else "&#x1F7E1;"
            st.markdown(f'{icon}&nbsp; **{issue["count"]:,}** — {issue["message"]}')

# ────────────────────────────────────────────────────────────────────────────
# TAB 3: SCORES OVERVIEW
# ────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    col_chart, col_cats = st.columns([3, 2])
    with col_chart:
        st.markdown('<div class="section-header">Category Radar</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_radar(results), use_container_width=True)
    with col_cats:
        st.markdown('<div class="section-header">Category Breakdown</div>', unsafe_allow_html=True)
        cat_data = {}
        for r in results:
            cat_data.setdefault(r["Category"], {"w": 0, "p": 0})
            cat_data[r["Category"]]["w"] += r["Weighted"]
            cat_data[r["Category"]]["p"] += r["Potential"]
        for cat, d in cat_data.items():
            pct = d["w"] / max(d["p"], 1) * 100
            grade = "Excellent" if pct >= 90 else "Good" if pct >= 70 else "Average" if pct >= 50 else "Below Average" if pct > 30 else "Insufficient"
            color = SCORE_COLORS[grade]
            st.markdown(f'<div class="cat-card"><div class="cat-pct" style="color:{color};">{pct:.0f}%</div><div class="cat-name">{cat}</div><div style="margin-top:0.3rem;">{score_badge(grade)}</div></div>', unsafe_allow_html=True)
            st.markdown("")

    # Grade banner
    gc = SCORE_COLORS[overall_grade]
    st.markdown(f'<div style="background:rgba({int(gc[1:3],16)},{int(gc[3:5],16)},{int(gc[5:7],16)},0.1);border:1px solid {gc};border-radius:12px;padding:1.2rem;text-align:center;"><span style="font-size:1.1rem;color:{gc};font-weight:700;">Overall: {overall_grade} ({overall_pct:.0f}%)</span><br><span style="color:#666;font-size:0.8rem;">Weighted: {total_weighted} / {total_potential}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Attribute Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_bars(results), use_container_width=True)

    # Detail table
    table = [{
        "Category": r["Category"], "Attribute": r["Attribute"], "Weighting": r["Weighting"],
        "Found": "Yes" if r["Found"] else "No", "Fill Rate": f"{r['Fill Rate']:.0%}",
        "Score": r["Score"], "Weighted": f"{r['Weighted']}/{r['Potential']}",
    } for r in results]
    st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 4: CONTENT QUALITY
# ────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    if title_data:
        st.markdown('<div class="section-header">Title Analysis</div>', unsafe_allow_html=True)
        tc1, tc2, tc3, tc4 = st.columns(4)
        with tc1:
            st.metric("Avg Length", f"{title_data['avg_len']} chars")
        with tc2:
            st.metric("Under 40 chars", f"{title_data['short_count']:,}")
        with tc3:
            st.metric("Over 150 chars", f"{title_data['long_count']:,}")
        with tc4:
            st.metric("Duplicate Titles", f"{title_data['dup_count']:,}")

        st.plotly_chart(chart_histogram(title_data["lengths"], "Title Length (chars)", target=120, target_label="Target (120)"), use_container_width=True)

        # Component presence
        if title_data["components"]:
            st.markdown('<div class="section-header">Title Component Presence</div>', unsafe_allow_html=True)
            comp_df = pd.DataFrame([{"Component": k, "Present in Titles": f"{v:.0%}", "Rate": v} for k, v in title_data["components"].items()])
            fig_comp = go.Figure(go.Bar(
                x=[v for v in title_data["components"].values()],
                y=[k for k in title_data["components"].keys()],
                orientation="h",
                marker=dict(color=[SEA if v >= 0.8 else BLUE if v >= 0.5 else "#FF9800" for v in title_data["components"].values()]),
                text=[f"{v:.0%}" for v in title_data["components"].values()],
                textposition="outside", textfont=dict(color=LIGHT, size=10),
            ))
            fig_comp.update_layout(**CHART_LAYOUT, xaxis=dict(range=[0, 1.15], title="% of titles containing attribute", gridcolor="rgba(255,255,255,0.04)"),
                                   yaxis=dict(tickfont=dict(color=LIGHT)), margin=dict(l=80, r=50, t=10, b=30), height=200)
            st.plotly_chart(fig_comp, use_container_width=True)

        # Top words
        if title_data["top_words"]:
            st.markdown('<div class="section-header">Most Common Title Words</div>', unsafe_allow_html=True)
            words, counts = zip(*title_data["top_words"][:20])
            fig_words = go.Figure(go.Bar(x=list(counts), y=list(words), orientation="h",
                                         marker=dict(color=VIOLET), textposition="outside",
                                         text=list(counts), textfont=dict(color=LIGHT, size=9)))
            fig_words.update_layout(**CHART_LAYOUT, yaxis=dict(autorange="reversed", tickfont=dict(color=LIGHT, size=10)),
                                    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                                    margin=dict(l=120, r=50, t=10, b=20), height=max(300, len(words) * 22))
            st.plotly_chart(fig_words, use_container_width=True)

    if desc_data:
        st.markdown('<div class="section-header">Description Analysis</div>', unsafe_allow_html=True)
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.metric("Avg Length", f"{desc_data['avg_len']} chars")
        with dc2:
            st.metric("Same as Title", f"{desc_data['same_as_title']:,}")
        with dc3:
            st.metric("Duplicate Descriptions", f"{desc_data['dup_count']:,}")
        st.plotly_chart(chart_histogram(desc_data["lengths"], "Description Length (chars)", target=500, target_label="Min target (500)"), use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 5: PRICING & IMAGES
# ────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    if pricing:
        st.markdown('<div class="section-header">Price Distribution</div>', unsafe_allow_html=True)
        pc1, pc2, pc3, pc4 = st.columns(4)
        with pc1:
            st.metric("Avg Price", f"${pricing['prices'].mean():.2f}" if len(pricing["prices"]) > 0 else "N/A")
        with pc2:
            st.metric("Median Price", f"${pricing['prices'].median():.2f}" if len(pricing["prices"]) > 0 else "N/A")
        with pc3:
            st.metric("Missing/Zero", f"{pricing['zero_count'] + pricing['missing_count']:,}")
        with pc4:
            if "on_sale_pct" in pricing:
                st.metric("On Sale", f"{pricing['on_sale_pct']:.0%}", delta=f"Avg {pricing['avg_discount']}% off" if pricing["avg_discount"] else None, delta_color="off")
            else:
                st.metric("Sale Price Column", "Not found")

        if len(pricing["prices"]) > 0:
            st.plotly_chart(chart_histogram(pricing["prices"], "Price ($)"), use_container_width=True)
    else:
        st.info("No price column detected in feed")

    if images:
        st.markdown('<div class="section-header">Image Coverage</div>', unsafe_allow_html=True)
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            st.metric("Missing Primary Image", f"{images['missing']:,}")
        with ic2:
            st.metric("Has Additional Images", f"{images['has_additional_pct']:.0%}")
        with ic3:
            st.metric("Duplicate Image URLs", f"{images['dup_images']:,}")

    # Taxonomy
    if taxonomy:
        for label, data in taxonomy.items():
            st.markdown(f'<div class="section-header">{label} Taxonomy</div>', unsafe_allow_html=True)
            tx1, tx2, tx3 = st.columns(3)
            with tx1:
                st.metric("Unique Categories", f"{data['unique_count']:,}")
            with tx2:
                st.metric("Avg Depth", f"{data['avg_depth']} levels")
            with tx3:
                st.metric("Max Depth", f"{data['max_depth']} levels")

            if data["top_values"]:
                top = list(data["top_values"].items())[:8]
                fig_tax = go.Figure(go.Bar(
                    x=[v for _, v in top], y=[k[:50] for k, _ in top], orientation="h",
                    marker=dict(color=BLUE), text=[str(v) for _, v in top],
                    textposition="outside", textfont=dict(color=LIGHT, size=9),
                ))
                fig_tax.update_layout(**CHART_LAYOUT, yaxis=dict(autorange="reversed", tickfont=dict(color=LIGHT, size=9)),
                                      xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                                      margin=dict(l=250, r=50, t=10, b=20), height=max(200, len(top) * 30))
                st.plotly_chart(fig_tax, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 6: FILL RATES
# ────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-header">Fill Rate Analysis</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_fill_rates(results), use_container_width=True)

    missing = [r for r in results if not r["Found"]]
    low = [r for r in results if r["Found"] and r["Fill Rate"] < 0.5]
    if missing:
        st.warning(f"**{len(missing)} attribute(s) not found:** " + ", ".join(r["Attribute"] for r in missing))
    if low:
        st.warning(f"**{len(low)} attribute(s) below 50% fill:** " + ", ".join(f'{r["Attribute"]} ({r["Fill Rate"]:.0%})' for r in low))
    if not missing and not low:
        st.success("All attributes found with fill rates above 50%!")

# ────────────────────────────────────────────────────────────────────────────
# TAB 7: RAW DATA
# ────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown(f'<div class="section-header">Feed Preview ({min(len(df), 200):,} of {len(df):,} rows)</div>', unsafe_allow_html=True)
    st.dataframe(df.head(200), use_container_width=True, height=500)
    st.markdown('<div class="section-header">Detected Columns</div>', unsafe_allow_html=True)
    st.markdown(", ".join(f"`{c}`" for c in df.columns))
