import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
import hashlib
import math
from io import BytesIO
from collections import Counter

# ═════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pattern — Feed Audit",
    page_icon="https://cdn.prod.website-files.com/64fdbed8246bf837f498e3f0/6568ba5b9c2ae21778952712_Favicon%2032x32.png",
    layout="wide",
    initial_sidebar_state="collapsed",
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

LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="191" height="38" viewBox="0 0 191 38" fill="none"><g clip-path="url(#clip0)"><path d="M23.1323 0.277129L0.336866 22.8367C-0.0379489 23.2076 -0.0379491 23.809 0.336866 24.1799L5.95075 29.7357C6.32557 30.1067 6.93326 30.1067 7.30808 29.7357L30.1035 7.1762C30.4783 6.80526 30.4783 6.20385 30.1035 5.83292L24.4896 0.277128C24.1148 -0.0938081 23.5071 -0.0938066 23.1323 0.277129Z" fill="#009BFF"/><path d="M32.5193 9.56975L19.1171 22.8332C18.7423 23.2042 18.7423 23.8056 19.1171 24.1765L24.731 29.7323C25.1058 30.1032 25.7135 30.1032 26.0884 29.7323L39.4905 16.4688C39.8654 16.0979 39.8654 15.4965 39.4905 15.1255L33.8767 9.56975C33.5018 9.19881 32.8942 9.19881 32.5193 9.56975Z" fill="#009BFF"/><path d="M72.0318 17.9793C72.0318 24.7983 66.8064 30.0154 60.5177 30.0154C56.9126 30.0154 54.1845 28.5504 52.4273 26.1703V37.4408C52.4273 37.5892 52.3677 37.7314 52.2618 37.8363C52.1558 37.9411 52.0121 38 51.8622 38H47.9977C47.8478 38 47.7041 37.9411 47.5981 37.8363C47.4921 37.7314 47.4326 37.5892 47.4326 37.4408V7.09944C47.4326 6.95113 47.4921 6.8089 47.5981 6.70403C47.7041 6.59916 47.8478 6.54025 47.9977 6.54025H51.8622C52.0121 6.54025 52.1558 6.59916 52.2618 6.70403C52.3677 6.8089 52.4273 6.95113 52.4273 7.09944V9.83398C54.1781 7.40976 56.9126 5.94482 60.5177 5.94482C66.8064 5.94482 72.0318 11.2075 72.0318 17.9793ZM67.0388 17.9793C67.0388 13.7263 63.8936 10.6578 59.733 10.6578C55.5724 10.6578 52.4273 13.7247 52.4273 17.9793C52.4273 22.2339 55.5708 25.3008 59.733 25.3008C63.8952 25.3008 67.0388 22.2355 67.0388 17.9793Z" fill="#FCFCFC"/><path d="M98.4814 7.09944V28.8608C98.4814 29.0091 98.4219 29.1513 98.3159 29.2562C98.2099 29.361 98.0662 29.42 97.9164 29.42H94.0534C93.9035 29.42 93.7598 29.361 93.6538 29.2562C93.5479 29.1513 93.4883 29.0091 93.4883 28.8608V26.1246C91.7375 28.5504 89.003 30.0154 85.3963 30.0154C79.1076 30.0154 73.8838 24.7527 73.8838 17.9793C73.8838 11.1619 79.1076 5.94482 85.3963 5.94482C89.003 5.94482 91.7311 7.40976 93.4883 9.7883V7.09944C93.4883 6.95113 93.5479 6.8089 93.6538 6.70403C93.7598 6.59916 93.9035 6.54025 94.0534 6.54025H97.9164C98.0662 6.54025 98.2099 6.59916 98.3159 6.70403C98.4219 6.8089 98.4814 6.95113 98.4814 7.09944ZM93.4883 17.9793C93.4883 13.7263 90.3432 10.6578 86.1826 10.6578C82.022 10.6578 78.8768 13.7247 78.8768 17.9793C78.8768 22.2339 82.022 25.3008 86.1826 25.3008C90.3432 25.3008 93.4883 22.2355 93.4883 17.9793Z" fill="#FCFCFC"/><path d="M139.785 25.4851C142.343 25.4851 144.31 24.4345 145.472 23.0168C145.557 22.9161 145.675 22.8489 145.806 22.8272C145.937 22.8055 146.071 22.8309 146.185 22.8986L149.33 24.718C149.398 24.7567 149.458 24.8092 149.504 24.8721C149.551 24.9351 149.584 25.007 149.6 25.0833C149.617 25.1596 149.617 25.2384 149.6 25.3147C149.584 25.391 149.551 25.463 149.505 25.5261C147.356 28.3378 144.023 30.0154 139.74 30.0154C132.11 30.0154 127.166 24.844 127.166 17.9793C127.166 11.206 132.113 5.94482 139.373 5.94482C146.263 5.94482 150.979 11.436 150.979 18.025C150.965 18.7152 150.904 19.4036 150.794 20.0853H132.387C133.173 23.6547 136.087 25.4851 139.785 25.4851ZM145.935 16.0576C145.241 12.1196 142.328 10.4294 139.323 10.4294C135.578 10.4294 133.034 12.6252 132.342 16.0576H145.935Z" fill="#FCFCFC"/><path d="M191.055 15.3712V28.8612C191.055 29.0095 190.996 29.1517 190.89 29.2566C190.784 29.3615 190.64 29.4204 190.49 29.4204H186.627C186.477 29.4204 186.334 29.3615 186.228 29.2566C186.122 29.1517 186.062 29.0095 186.062 28.8612V15.8753C186.062 12.3973 184.026 10.5669 180.883 10.5669C177.599 10.5669 175.011 12.4886 175.011 17.1559V28.8612C175.011 28.9348 174.997 29.0076 174.968 29.0756C174.94 29.1435 174.898 29.2052 174.845 29.2572C174.793 29.3091 174.73 29.3503 174.661 29.3783C174.593 29.4063 174.519 29.4206 174.445 29.4204H170.582C170.432 29.4204 170.288 29.3615 170.182 29.2566C170.076 29.1517 170.017 29.0095 170.017 28.8612V7.09988C170.017 6.95158 170.076 6.80934 170.182 6.70447C170.288 6.5996 170.432 6.54069 170.582 6.54069H174.446C174.521 6.54048 174.594 6.55479 174.663 6.5828C174.732 6.61081 174.794 6.65197 174.847 6.70392C174.899 6.75586 174.941 6.81758 174.97 6.88552C174.998 6.95347 175.013 7.02632 175.013 7.09988V9.46267C176.538 7.08256 179.035 5.93896 182.175 5.93896C187.356 5.94527 191.055 9.4233 191.055 15.3712Z" fill="#FCFCFC"/><path d="M165.186 6.12744C162.274 6.12744 159.456 7.27261 158.065 10.3805V7.09934C158.065 6.95103 158.006 6.8088 157.9 6.70393C157.794 6.59906 157.65 6.54014 157.5 6.54014H153.637C153.487 6.54014 153.344 6.59906 153.238 6.70393C153.132 6.8088 153.072 6.95103 153.072 7.09934V28.8607C153.072 29.009 153.132 29.1512 153.238 29.2561C153.344 29.3609 153.487 29.4198 153.637 29.4198H157.5C157.65 29.4198 157.794 29.3609 157.9 29.2561C158.006 29.1512 158.065 29.009 158.065 28.8607V17.8878C158.065 12.7637 161.823 11.4815 165.186 11.4815H166.926C167.076 11.4815 167.22 11.4226 167.326 11.3177C167.432 11.2129 167.491 11.0706 167.491 10.9223V6.68821C167.491 6.61464 167.477 6.54176 167.449 6.47373C167.42 6.40571 167.379 6.34387 167.326 6.29178C167.274 6.23969 167.211 6.19836 167.143 6.17016C167.074 6.14196 167 6.12744 166.926 6.12744H165.186Z" fill="#FCFCFC"/><path d="M112.505 11.2989C112.579 11.2991 112.653 11.2848 112.721 11.2568C112.79 11.2287 112.853 11.1876 112.905 11.1356C112.958 11.0837 113 11.022 113.028 10.954C113.057 10.8861 113.071 10.8132 113.071 10.7397V7.0994C113.071 7.02584 113.057 6.95299 113.028 6.88504C113 6.8171 112.958 6.75538 112.905 6.70343C112.853 6.65149 112.79 6.61033 112.721 6.58232C112.653 6.55431 112.579 6.54 112.505 6.54021H106.561V0.554469C106.56 0.408335 106.501 0.268486 106.397 0.164857C106.293 0.0612278 106.152 0.00205319 106.004 0H102.133C101.984 0 101.84 0.0589149 101.734 0.163784C101.628 0.268653 101.568 0.410887 101.568 0.559194V22.6718C101.568 27.369 103.857 29.6247 108.634 29.6247H112.506C112.656 29.6243 112.799 29.5652 112.905 29.4604C113.011 29.3557 113.071 29.2137 113.071 29.0655V25.6001C113.071 25.5265 113.057 25.4537 113.028 25.3857C113 25.3178 112.958 25.256 112.905 25.2041C112.853 25.1521 112.79 25.111 112.721 25.083C112.653 25.055 112.579 25.0407 112.505 25.0409H109.533C107.255 25.0409 106.561 24.4549 106.561 22.2827V11.2989H112.505Z" fill="#FCFCFC"/><path d="M126.061 11.2989C126.211 11.2989 126.354 11.24 126.46 11.1351C126.566 11.0302 126.626 10.888 126.626 10.7397V7.0994C126.626 6.9511 126.566 6.80886 126.46 6.70399C126.354 6.59912 126.211 6.54021 126.061 6.54021H120.124V0.554469C120.123 0.406981 120.063 0.265959 119.957 0.16211C119.851 0.0582605 119.708 -5.26628e-06 119.559 3.57006e-10H115.696C115.546 3.57006e-10 115.402 0.0589149 115.296 0.163784C115.19 0.268653 115.131 0.410887 115.131 0.559194V22.6718C115.131 27.369 117.418 29.6247 122.196 29.6247H126.069C126.218 29.6239 126.361 29.5646 126.467 29.4599C126.572 29.3552 126.632 29.2134 126.632 29.0655V25.6001C126.632 25.5264 126.617 25.4536 126.588 25.3858C126.559 25.318 126.516 25.2565 126.463 25.205C126.41 25.1535 126.347 25.1128 126.278 25.0855C126.209 25.0581 126.135 25.0446 126.061 25.0456H123.089C120.812 25.0456 120.118 24.4596 120.118 22.2874V11.2989H126.061Z" fill="#FCFCFC"/></g><defs><clipPath id="clip0"><rect width="191" height="38" fill="white"/></clipPath></defs></svg>'''

SCORE_COLORS = {"Excellent": SEA, "Good": BLUE, "Average": "#FFC107", "Below Average": "#FF9800", "Insufficient": "#FF5252"}
SCORE_MAP = {"Excellent": 5, "Good": 4, "Average": 3, "Below Average": 2, "Insufficient": 1}
WEIGHTING_MAP = {"Must have": 3, "Good to have": 2, "Bonus": 1}


# ═════════════════════════════════════════════════════════════════════════════
# 3. CSS INJECTION — ANIMATIONS & PREMIUM STYLING
# ═════════════════════════════════════════════════════════════════════════════

def _inject_css():
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400;500;600;700;800&display=swap');

    /* ── Keyframe Animations ─────────────────────────────────────────── */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(24px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to   {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50%      {{ transform: scale(1.04); }}
    }}
    @keyframes shimmer {{
        0%   {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    @keyframes countUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes drawCircle {{
        from {{ stroke-dashoffset: 314; }}
    }}
    @keyframes glowPulse {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(0, 155, 255, 0.0); }}
        50%      {{ box-shadow: 0 0 30px rgba(0, 155, 255, 0.15); }}
    }}
    @keyframes barGrow {{
        from {{ width: 0%; }}
    }}
    @keyframes ripple {{
        0%   {{ transform: scale(0.8); opacity: 1; }}
        100% {{ transform: scale(2.4); opacity: 0; }}
    }}
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-12px); max-height: 0; }}
        to   {{ opacity: 1; transform: translateY(0); max-height: 500px; }}
    }}
    @keyframes checkPop {{
        0%   {{ transform: scale(0); }}
        60%  {{ transform: scale(1.3); }}
        100% {{ transform: scale(1); }}
    }}

    /* ── Base ─────────────────────────────────────────────────────────── */
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

    /* ── Gradient buttons ────────────────────────────────────────────── */
    .stButton > button {{
        background: {GRADIENT};
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        padding: 0.6rem 1.6rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 155, 255, 0.25);
        color: white;
        border: none;
    }}
    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* ── Metric cards — glassmorphism + animation ────────────────────── */
    [data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.2rem;
        animation: fadeInUp 0.6s ease-out both;
        transition: all 0.3s ease;
    }}
    [data-testid="stMetric"]:hover {{
        border-color: rgba(0, 155, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 155, 255, 0.08);
    }}

    /* Stagger metric animations */
    [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] {{ animation-delay: 0.05s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] {{ animation-delay: 0.12s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] {{ animation-delay: 0.19s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] {{ animation-delay: 0.26s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(5) [data-testid="stMetric"] {{ animation-delay: 0.33s; }}

    /* ── Section headers ─────────────────────────────────────────────── */
    .section-header {{
        border-left: 3px solid {BLUE};
        padding-left: 12px;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        color: {LIGHT};
        animation: slideInLeft 0.5s ease-out both;
    }}

    /* ── Score badges ────────────────────────────────────────────────── */
    .score-badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        animation: fadeIn 0.4s ease both;
    }}
    .score-excellent {{ background: rgba(76, 195, 174, 0.15); color: {SEA}; }}
    .score-good {{ background: rgba(0, 155, 255, 0.15); color: {BLUE}; }}
    .score-average {{ background: rgba(255, 193, 7, 0.15); color: #FFC107; }}
    .score-below-average {{ background: rgba(255, 152, 0, 0.15); color: #FF9800; }}
    .score-insufficient {{ background: rgba(255, 82, 82, 0.15); color: #FF5252; }}

    /* ── Hero score — animated ring ──────────────────────────────────── */
    .hero-ring {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.5rem 0;
        animation: fadeInUp 0.7s ease-out both;
    }}
    .hero-ring svg {{ filter: drop-shadow(0 0 20px rgba(0,155,255,0.2)); }}
    .hero-ring .ring-label {{
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }}
    .hero-ring .ring-grade {{
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }}

    /* ── Recommendation cards ────────────────────────────────────────── */
    .rec-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.65rem;
        animation: fadeInUp 0.5s ease-out both;
        transition: all 0.3s ease;
        cursor: default;
    }}
    .rec-card:hover {{
        background: rgba(255,255,255,0.04);
        border-color: rgba(255,255,255,0.1);
        transform: translateX(4px);
    }}
    .rec-card.high {{ border-left: 3px solid #FF5252; }}
    .rec-card.medium {{ border-left: 3px solid #FFC107; }}
    .rec-card.low {{ border-left: 3px solid {SEA}; }}
    .rec-impact {{
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.35rem;
    }}
    .rec-impact.high {{ color: #FF5252; }}
    .rec-impact.medium {{ color: #FFC107; }}
    .rec-impact.low {{ color: {SEA}; }}

    /* ── Category cards ──────────────────────────────────────────────── */
    .cat-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        animation: fadeInUp 0.6s ease-out both;
        transition: all 0.3s ease;
    }}
    .cat-card:hover {{
        border-color: rgba(0,155,255,0.2);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }}
    .cat-pct {{
        font-size: 2.2rem;
        font-weight: 800;
        font-family: 'Wix Madefor Display', sans-serif;
    }}
    .cat-name {{
        font-size: 0.78rem;
        color: #777;
        margin-top: 0.3rem;
    }}

    /* ── GMC field checklist ──────────────────────────────────────────── */
    .gmc-field-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 16px;
        border-radius: 10px;
        margin-bottom: 4px;
        animation: fadeInUp 0.4s ease-out both;
        transition: background 0.2s ease;
    }}
    .gmc-field-row:hover {{ background: rgba(255,255,255,0.03); }}
    .gmc-icon {{
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
        animation: checkPop 0.4s ease both;
    }}
    .gmc-icon.pass {{ background: rgba(76,195,174,0.15); color: {SEA}; }}
    .gmc-icon.fail {{ background: rgba(255,82,82,0.15); color: #FF5252; }}
    .gmc-icon.warn {{ background: rgba(255,193,7,0.15); color: #FFC107; }}
    .gmc-field-name {{
        flex: 1;
        font-size: 0.9rem;
        color: {LIGHT};
        font-weight: 500;
    }}
    .gmc-field-detail {{
        font-size: 0.78rem;
        color: #666;
        text-align: right;
    }}

    /* ── Progress bar (animated) ─────────────────────────────────────── */
    .anim-bar-track {{
        background: rgba(255,255,255,0.06);
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
        width: 100%;
    }}
    .anim-bar-fill {{
        height: 100%;
        border-radius: 6px;
        animation: barGrow 1s cubic-bezier(0.4, 0, 0.2, 1) both;
    }}

    /* ── Issue card (GMC) ────────────────────────────────────────────── */
    .issue-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        animation: fadeInUp 0.5s ease-out both;
        transition: all 0.25s ease;
    }}
    .issue-card:hover {{
        background: rgba(255,255,255,0.04);
        transform: translateX(3px);
    }}
    .issue-card .issue-icon {{
        font-size: 1.1rem;
        margin-top: 1px;
        flex-shrink: 0;
    }}
    .issue-card .issue-body {{ flex: 1; }}
    .issue-card .issue-count {{
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 20px;
        white-space: nowrap;
    }}
    .issue-card .issue-count.error {{
        background: rgba(255,82,82,0.12);
        color: #FF5252;
    }}
    .issue-card .issue-count.warning {{
        background: rgba(255,193,7,0.12);
        color: #FFC107;
    }}

    /* ── Upload area ─────────────────────────────────────────────────── */
    .upload-hero {{
        text-align: center;
        padding: 4rem 2rem 3rem;
        animation: fadeInUp 0.8s ease-out both;
    }}
    .upload-hero .upload-icon {{
        font-size: 4rem;
        opacity: 0.2;
        animation: pulse 3s ease-in-out infinite;
    }}
    .upload-hero h2 {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {LIGHT};
        margin: 1rem 0 0.4rem;
    }}
    .upload-hero p {{
        color: #555;
        font-size: 0.9rem;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    .upload-formats {{
        display: flex;
        gap: 8px;
        justify-content: center;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }}
    .upload-formats span {{
        font-size: 0.7rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(0,155,255,0.08);
        color: {BLUE};
        letter-spacing: 0.5px;
    }}

    /* ── GMC Readiness meter ─────────────────────────────────────────── */
    .readiness-meter {{
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        animation: fadeInUp 0.6s ease-out both;
    }}
    .readiness-meter .big-status {{
        font-size: 1.8rem;
        font-weight: 800;
        font-family: 'Wix Madefor Display', sans-serif;
    }}
    .readiness-meter .sub-text {{
        font-size: 0.78rem;
        color: #666;
        margin-top: 0.3rem;
    }}

    /* ── Fill rate row ───────────────────────────────────────────────── */
    .fill-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        animation: fadeInUp 0.4s ease-out both;
    }}
    .fill-row .fill-name {{
        width: 180px;
        font-size: 0.85rem;
        color: {LIGHT};
        font-weight: 500;
        flex-shrink: 0;
    }}
    .fill-row .fill-track {{
        flex: 1;
        background: rgba(255,255,255,0.06);
        border-radius: 6px;
        height: 10px;
        overflow: hidden;
    }}
    .fill-row .fill-bar {{
        height: 100%;
        border-radius: 6px;
        animation: barGrow 0.8s cubic-bezier(0.4, 0, 0.2, 1) both;
        transition: width 0.3s ease;
    }}
    .fill-row .fill-pct {{
        width: 50px;
        text-align: right;
        font-size: 0.82rem;
        font-weight: 600;
        color: {LIGHT};
    }}
    .fill-row .fill-badge {{
        width: 100px;
        text-align: center;
    }}

    /* ── Hide Streamlit chrome ───────────────────────────────────────── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* ── Tabs ────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-highlight"] {{
        background: {GRADIENT};
        border-radius: 3px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {LIGHT};
        padding: 12px 18px;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {BLUE};
    }}
    .stTabs [data-baseweb="tab-border"] {{
        background-color: rgba(255,255,255,0.06);
    }}

    /* ── Download button ─────────────────────────────────────────────── */
    .stDownloadButton > button {{
        background: transparent;
        border: 1px solid rgba(255,255,255,0.12);
        color: {LIGHT};
        border-radius: 10px;
        transition: all 0.3s ease;
    }}
    .stDownloadButton > button:hover {{
        border-color: {BLUE};
        color: {BLUE};
        background: rgba(0,155,255,0.05);
        box-shadow: 0 4px 20px rgba(0,155,255,0.1);
    }}

    /* ── Headings ────────────────────────────────────────────────────── */
    .stApp h1 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 800; color: {LIGHT}; }}
    .stApp h2 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 700; color: {LIGHT}; }}
    .stApp h3 {{ font-family: 'Wix Madefor Display', sans-serif; font-weight: 600; color: {LIGHT}; }}

    /* ── Expander ────────────────────────────────────────────────────── */
    .streamlit-expanderHeader {{
        font-weight: 600;
        font-size: 0.9rem;
        color: {LIGHT};
    }}
    [data-testid="stExpander"] {{
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        background: rgba(255,255,255,0.02);
    }}

    /* ── Divider ─────────────────────────────────────────────────────── */
    hr {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
    }}

    /* ── Stagger animations for issue cards ──────────────────────────── */
    .issue-card:nth-child(1) {{ animation-delay: 0.0s; }}
    .issue-card:nth-child(2) {{ animation-delay: 0.06s; }}
    .issue-card:nth-child(3) {{ animation-delay: 0.12s; }}
    .issue-card:nth-child(4) {{ animation-delay: 0.18s; }}
    .issue-card:nth-child(5) {{ animation-delay: 0.24s; }}
    .issue-card:nth-child(6) {{ animation-delay: 0.30s; }}
    .issue-card:nth-child(7) {{ animation-delay: 0.36s; }}
    .issue-card:nth-child(8) {{ animation-delay: 0.42s; }}

    .gmc-field-row:nth-child(1) {{ animation-delay: 0.0s; }}
    .gmc-field-row:nth-child(2) {{ animation-delay: 0.04s; }}
    .gmc-field-row:nth-child(3) {{ animation-delay: 0.08s; }}
    .gmc-field-row:nth-child(4) {{ animation-delay: 0.12s; }}
    .gmc-field-row:nth-child(5) {{ animation-delay: 0.16s; }}
    .gmc-field-row:nth-child(6) {{ animation-delay: 0.20s; }}
    .gmc-field-row:nth-child(7) {{ animation-delay: 0.24s; }}
    .gmc-field-row:nth-child(8) {{ animation-delay: 0.28s; }}
    .gmc-field-row:nth-child(9) {{ animation-delay: 0.32s; }}
    .gmc-field-row:nth-child(10) {{ animation-delay: 0.36s; }}
    .gmc-field-row:nth-child(11) {{ animation-delay: 0.40s; }}
    .gmc-field-row:nth-child(12) {{ animation-delay: 0.44s; }}

    .rec-card:nth-child(1) {{ animation-delay: 0.0s; }}
    .rec-card:nth-child(2) {{ animation-delay: 0.06s; }}
    .rec-card:nth-child(3) {{ animation-delay: 0.12s; }}
    .rec-card:nth-child(4) {{ animation-delay: 0.18s; }}
    .rec-card:nth-child(5) {{ animation-delay: 0.24s; }}
    .rec-card:nth-child(6) {{ animation-delay: 0.30s; }}
    .rec-card:nth-child(7) {{ animation-delay: 0.36s; }}
    .rec-card:nth-child(8) {{ animation-delay: 0.42s; }}
    .rec-card:nth-child(9) {{ animation-delay: 0.48s; }}
    .rec-card:nth-child(10) {{ animation-delay: 0.54s; }}

    .fill-row:nth-child(1) {{ animation-delay: 0.0s; }}
    .fill-row:nth-child(2) {{ animation-delay: 0.04s; }}
    .fill-row:nth-child(3) {{ animation-delay: 0.08s; }}
    .fill-row:nth-child(4) {{ animation-delay: 0.12s; }}
    .fill-row:nth-child(5) {{ animation-delay: 0.16s; }}
    .fill-row:nth-child(6) {{ animation-delay: 0.20s; }}
    .fill-row:nth-child(7) {{ animation-delay: 0.24s; }}
    .fill-row:nth-child(8) {{ animation-delay: 0.28s; }}
    .fill-row:nth-child(9) {{ animation-delay: 0.32s; }}
    .fill-row:nth-child(10) {{ animation-delay: 0.36s; }}
    .fill-row:nth-child(11) {{ animation-delay: 0.40s; }}
    .fill-row:nth-child(12) {{ animation-delay: 0.44s; }}
    .fill-row:nth-child(13) {{ animation-delay: 0.48s; }}
    .fill-row:nth-child(14) {{ animation-delay: 0.52s; }}
    .fill-row:nth-child(15) {{ animation-delay: 0.56s; }}
    .fill-row:nth-child(16) {{ animation-delay: 0.60s; }}
    .fill-row:nth-child(17) {{ animation-delay: 0.64s; }}
    .fill-row:nth-child(18) {{ animation-delay: 0.68s; }}
    .fill-row:nth-child(19) {{ animation-delay: 0.72s; }}
    .fill-row:nth-child(20) {{ animation-delay: 0.76s; }}
</style>
""", unsafe_allow_html=True)


# ── HTML Helpers ─────────────────────────────────────────────────────────

def score_badge(label: str) -> str:
    cls = label.lower().replace(" ", "-")
    return f'<span class="score-badge score-{cls}">{label}</span>'


def svg_ring(pct: float, size=140, stroke=8, color=BLUE):
    """Animated SVG ring gauge."""
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - pct / 100)
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="{stroke}"/>
      <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}"
              stroke-dasharray="{circ}" stroke-dashoffset="{offset}" stroke-linecap="round"
              transform="rotate(-90 {size/2} {size/2})"
              style="animation: drawCircle 1.2s cubic-bezier(0.4,0,0.2,1) both; transition: stroke-dashoffset 0.6s ease;"/>
      <text x="{size/2}" y="{size/2 + 1}" text-anchor="middle" dominant-baseline="middle"
            fill="{LIGHT}" font-family="Wix Madefor Display, sans-serif" font-weight="800"
            font-size="{size * 0.22}px" style="animation: countUp 0.8s ease-out 0.4s both;">{pct:.0f}%</text>
    </svg>'''


def animated_bar(pct: float, color: str, delay: float = 0):
    """Inline animated progress bar."""
    return (f'<div class="anim-bar-track">'
            f'<div class="anim-bar-fill" style="width:{pct:.0f}%;background:{color};animation-delay:{delay:.2f}s;"></div>'
            f'</div>')


def _color_for_rate(r: float) -> str:
    if r >= 1.0: return SEA
    if r >= 0.8: return BLUE
    if r >= 0.5: return "#FFC107"
    if r > 0.2: return "#FF9800"
    return "#FF5252"


# ═════════════════════════════════════════════════════════════════════════════
# 4. COLUMN DETECTION ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def find_col(df: pd.DataFrame, term: str) -> str | None:
    cols = {c.lower().strip(): c for c in df.columns}
    if term.lower() in cols:
        return cols[term.lower()]
    for k, v in cols.items():
        if term.lower() in k:
            return v
    return None


# ═════════════════════════════════════════════════════════════════════════════
# 5. SCORING ENGINE
# ═════════════════════════════════════════════════════════════════════════════

AUDIT_ATTRS = [
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
# 6. GMC VALIDATION ENGINE (enhanced)
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def run_gmc_validation(_df_hash, df):
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

    if desc_col:
        descs = df[desc_col].astype(str)
        too_long_d = (descs.str.len() > 5000).sum()
        if too_long_d > 0:
            issues.append({"severity": "warning", "field": "description", "count": int(too_long_d),
                           "message": f"{too_long_d:,} descriptions exceed 5,000 characters"})

    if price_col:
        prices = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        zero_price = (prices == 0).sum() + prices.isna().sum()
        if zero_price > 0:
            issues.append({"severity": "error", "field": "price", "count": int(zero_price),
                           "message": f"{zero_price:,} products with invalid or zero price"})

    if avail_col:
        valid_avail = {"in stock", "out of stock", "preorder", "backorder", "in_stock", "out_of_stock"}
        invalid = ~df[avail_col].astype(str).str.lower().str.strip().isin(valid_avail) & df[avail_col].notna() & (df[avail_col].astype(str).str.strip() != "")
        n = invalid.sum()
        if n > 0:
            issues.append({"severity": "error", "field": "availability", "count": int(n),
                           "message": f"{n:,} products with invalid availability value"})

    if cond_col:
        valid_cond = {"new", "refurbished", "used"}
        invalid_c = ~df[cond_col].astype(str).str.lower().str.strip().isin(valid_cond) & df[cond_col].notna() & (df[cond_col].astype(str).str.strip() != "")
        n = invalid_c.sum()
        if n > 0:
            issues.append({"severity": "warning", "field": "condition", "count": int(n),
                           "message": f"{n:,} products with non-standard condition value"})

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

    if id_col:
        dups = df[id_col].dropna().astype(str)
        dup_count = dups.duplicated().sum()
        if dup_count > 0:
            issues.append({"severity": "error", "field": "id", "count": int(dup_count),
                           "message": f"{dup_count:,} duplicate product IDs (will cause overwrite conflicts)"})

    if gtin_col and brand_col:
        has_brand = df[brand_col].astype(str).str.strip().ne("") & df[brand_col].notna()
        missing_gtin = df[gtin_col].isna() | (df[gtin_col].astype(str).str.strip() == "")
        n = (has_brand & missing_gtin).sum()
        if n > 0:
            issues.append({"severity": "warning", "field": "gtin", "count": int(n),
                           "message": f"{n:,} branded products missing GTIN (reduces impression eligibility)"})

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


@st.cache_data(show_spinner=False)
def gmc_field_status(_df_hash, df):
    """Per-field readiness status for the GMC checklist."""
    fields = [
        ("Product ID", "id", True),
        ("Title", "title", True),
        ("Description", "description", True),
        ("Price", "price", True),
        ("Product Link", "link", True),
        ("Image Link", "image link", True),
        ("Availability", "availability", False),
        ("Condition", "condition", False),
        ("Brand", "brand", False),
        ("GTIN", "gtin", False),
        ("Google Product Category", "google product category", False),
        ("Product Type", "product type", False),
    ]
    statuses = []
    total = len(df)
    for name, term, required in fields:
        col = find_col(df, term)
        if col is None:
            statuses.append({
                "name": name, "required": required,
                "status": "fail" if required else "warn",
                "detail": "Column not found",
                "fill_rate": 0.0,
            })
        else:
            rate = _fill_rate(df, col)
            if rate >= 0.99:
                status = "pass"
            elif rate >= 0.8:
                status = "warn" if required else "pass"
            else:
                status = "fail" if required else "warn"
            missing = int(total * (1 - rate))
            detail = "100% filled" if rate >= 1.0 else f"{rate:.0%} filled ({missing:,} missing)"
            statuses.append({
                "name": name, "required": required,
                "status": status, "detail": detail,
                "fill_rate": rate,
            })
    return statuses


# ═════════════════════════════════════════════════════════════════════════════
# 7. CONTENT ANALYSIS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_titles(_df_hash, df):
    col = find_col(df, "title")
    if col is None:
        return None
    titles = df[col].astype(str)
    lengths = titles.str.len()

    brand_col = find_col(df, "brand")
    color_col = find_col(df, "color")
    size_col = find_col(df, "size")
    material_col = find_col(df, "material")
    gender_col = find_col(df, "gender")

    components = {}
    for comp_name, comp_col in [("Brand", brand_col), ("Color", color_col), ("Size", size_col),
                                 ("Material", material_col), ("Gender", gender_col)]:
        if comp_col:
            vals = df[comp_col].astype(str).str.strip()
            components[comp_name] = sum(
                1 for t, v in zip(titles, vals)
                if v and v.lower() != "nan" and v.lower() in t.lower()
            ) / max(len(df), 1)

    all_words = " ".join(titles).lower().split()
    stop = {"the","a","an","and","or","for","with","in","of","to","is","by","on","at","from","&","-","--","/",""}
    word_freq = Counter(w.strip(".,()[]") for w in all_words if w.strip(".,()[]") not in stop and len(w.strip(".,()[]")) > 1)

    dup_titles = titles[titles.duplicated(keep=False) & (titles.str.strip() != "")]

    return {
        "avg_len": round(lengths.mean()),
        "lengths": lengths,
        "components": components,
        "top_words": word_freq.most_common(30),
        "dup_count": dup_titles.nunique(),
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
# 8. PRICING ANALYSIS
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
        result["avg_discount"] = round(((prices[has_sale] - sale_prices[has_sale]) / prices[has_sale] * 100).mean(), 1) if has_sale.any() else 0
    return result


# ═════════════════════════════════════════════════════════════════════════════
# 9. IMAGE ANALYSIS
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
# 10. TAXONOMY ANALYSIS
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
# 11. RECOMMENDATIONS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def generate_recommendations(results, gmc_issues, title_data, desc_data, pricing, images, taxonomy, df):
    recs = []
    errors = [i for i in gmc_issues if i["severity"] == "error"]
    if errors:
        for e in errors[:3]:
            recs.append(("high", e["message"], "Fix this before uploading to Merchant Center to avoid disapprovals."))

    gtin_issue = next((i for i in gmc_issues if "gtin" in i["field"].lower() and "missing" in i["message"].lower()), None)
    if gtin_issue:
        recs.append(("high", f"{gtin_issue['count']:,} branded products missing GTIN",
                      "Adding GTINs typically improves impression share by 20-40% for branded products."))

    if title_data:
        if title_data["avg_len"] < 80:
            recs.append(("high", f"Average title length is only {title_data['avg_len']} characters (target: 120+)",
                          "Add brand, color, size, material, and product type to titles. Longer, attribute-rich titles improve click-through rate."))
        if title_data["dup_count"] > 0:
            recs.append(("medium", f"{title_data['dup_count']} duplicate titles detected across {title_data['dup_total']:,} products",
                          "Duplicate titles cause products to compete against each other. Differentiate with unique attributes."))
        for comp, rate in title_data.get("components", {}).items():
            if rate < 0.5:
                recs.append(("medium", f"Only {rate:.0%} of titles contain {comp.lower()}",
                              f"Adding {comp.lower()} to titles improves relevance matching and ad quality."))

    if desc_data:
        if desc_data["avg_len"] < 200:
            recs.append(("medium", f"Average description length is only {desc_data['avg_len']} characters",
                          "Rich descriptions (500+ chars) improve product discoverability in Shopping and free listings."))
        if desc_data["same_as_title"] > 0:
            recs.append(("medium", f"{desc_data['same_as_title']:,} products have description identical to title",
                          "Descriptions should expand on the title with unique selling points, specs, and benefits."))

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

    cl_result = next((r for r in results if r["Attribute"] == "Custom Labels"), None)
    if cl_result and cl_result["Fill Rate"] < 0.6:
        recs.append(("low", f"Only {cl_result['Fill Rate']:.0%} of custom label slots are in use",
                      "Use custom labels for bid segmentation: margin tiers, seasonality, best-sellers, price buckets, new arrivals."))

    if images and images["has_additional_pct"] < 0.5:
        recs.append(("low", f"Only {images['has_additional_pct']:.0%} of products have additional images",
                      "Products with multiple images see 10-15% higher conversion rates in Shopping."))

    if taxonomy:
        for label, data in taxonomy.items():
            if data["avg_depth"] < 3:
                recs.append(("low", f"{label} average depth is {data['avg_depth']} levels",
                              "Deeper categorization (3+ levels) improves Google's ability to match products to relevant queries."))

    seen = set()
    unique_recs = []
    for r in recs:
        key = r[1][:60]
        if key not in seen:
            seen.add(key)
            unique_recs.append(r)
    unique_recs.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x[0], 3))
    return unique_recs


# ═════════════════════════════════════════════════════════════════════════════
# 12. REPORT GENERATION
# ═════════════════════════════════════════════════════════════════════════════

def generate_excel_report(results, gmc_issues, recs, df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_data = [{
            "Category": r["Category"], "Attribute": r["Attribute"],
            "Weighting": r["Weighting"], "Found": "Yes" if r["Found"] else "No",
            "Fill Rate": f"{r['Fill Rate']:.0%}", "Score": r["Score"],
            "Weighted Score": f"{r['Weighted']} / {r['Potential']}",
        } for r in results]
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Audit Scores", index=False)
        if gmc_issues:
            pd.DataFrame(gmc_issues).to_excel(writer, sheet_name="GMC Issues", index=False)
        if recs:
            rec_data = [{"Priority": r[0].upper(), "Issue": r[1], "Action": r[2]} for r in recs]
            pd.DataFrame(rec_data).to_excel(writer, sheet_name="Recommendations", index=False)
        df.head(500).to_excel(writer, sheet_name="Feed Sample", index=False)
    return output.getvalue()


# ═════════════════════════════════════════════════════════════════════════════
# 13. CHART BUILDERS
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
        fill="toself", fillcolor="rgba(0,155,255,0.08)",
        line=dict(color=BLUE, width=2.5), marker=dict(size=7, color=BLUE),
        hovertemplate="%{theta}<br>Score: %{r:.0f}%<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, showlegend=False,
                      polar=dict(bgcolor="rgba(0,0,0,0)",
                                 radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=9, color="#444")),
                                 angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=12, color=LIGHT, weight="bold"))),
                      margin=dict(l=70, r=70, t=30, b=30), height=400)
    return fig


def chart_bars(results, value_key="Weighted", max_key="Potential"):
    attrs = [r["Attribute"] for r in results]
    pcts = [r[value_key] / max(r[max_key], 1) * 100 for r in results]
    colors = [SCORE_COLORS.get(r["Score"], "#FF5252") for r in results]
    fig = go.Figure(go.Bar(
        y=attrs, x=pcts, orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=[f"{p:.0f}%" for p in pcts], textposition="outside",
        textfont=dict(color=LIGHT, size=10),
        hovertemplate="%{y}: %{x:.0f}%<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, xaxis=dict(range=[0, 115], title_text="Score %", gridcolor="rgba(255,255,255,0.03)"),
                      yaxis=dict(tickfont=dict(color=LIGHT, size=10), autorange="reversed"),
                      margin=dict(l=170, r=60, t=10, b=30), height=max(350, len(attrs) * 30))
    return fig


def chart_histogram(series, title="", target=None, target_label=""):
    fig = go.Figure(go.Histogram(
        x=series, nbinsx=40,
        marker=dict(color=BLUE, line=dict(width=0), cornerradius=3),
        hovertemplate="%{x}: %{y} products<extra></extra>",
    ))
    if target:
        fig.add_vline(x=target, line_dash="dash", line_color=SEA, line_width=2,
                      annotation_text=target_label, annotation_font_color=SEA, annotation_font_size=11)
    fig.update_layout(**CHART_LAYOUT, xaxis=dict(title_text=title, gridcolor="rgba(255,255,255,0.03)"),
                      yaxis=dict(title_text="Products", gridcolor="rgba(255,255,255,0.03)"),
                      margin=dict(l=50, r=20, t=20, b=40), height=280,
                      bargap=0.05)
    return fig


def chart_donut(values, labels, colors, hole_text=""):
    fig = go.Figure(go.Pie(
        values=values, labels=labels,
        hole=0.7, marker=dict(colors=colors, line=dict(width=0)),
        textinfo="percent", textfont=dict(size=11, color=LIGHT),
        hovertemplate="%{label}: %{value}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, showlegend=True,
                      legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font=dict(size=10, color="#888")),
                      margin=dict(l=10, r=10, t=10, b=40), height=280,
                      annotations=[dict(text=hole_text, x=0.5, y=0.5, font=dict(size=14, color=LIGHT, family="Wix Madefor Display", weight="bold"), showarrow=False)] if hole_text else [])
    return fig


# ═════════════════════════════════════════════════════════════════════════════
# 14. MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

_inject_css()

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;animation:fadeIn 0.6s ease both;">'
    f'<div>{LOGO_SVG}</div>'
    f'</div>',
    unsafe_allow_html=True,
)
st.markdown('<h1 style="margin-top:0;margin-bottom:0.2rem;animation:fadeInUp 0.6s ease 0.1s both;">Product Feed Audit</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#555;margin-bottom:1.5rem;animation:fadeInUp 0.6s ease 0.2s both;">Upload a product feed to get a comprehensive quality score, GMC readiness check, and prioritised recommendations.</p>', unsafe_allow_html=True)

# ── File Upload ────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload your product feed", type=["csv", "tsv", "xlsx", "xls", "txt"],
                            help="CSV, TSV, or Excel. Headers in first row.", label_visibility="collapsed")

if uploaded is None:
    st.markdown(
        f'<div class="upload-hero">'
        f'<div class="upload-icon">&#x2B06;</div>'
        f'<h2>Drop your product feed above</h2>'
        f'<p>Get instant insights on feed quality, Merchant Center readiness, title optimisation, pricing analysis, and actionable recommendations to improve your Shopping performance.</p>'
        f'<div class="upload-formats">'
        f'<span>CSV</span><span>TSV</span><span>XLSX</span><span>XLS</span><span>TXT</span>'
        f'</div>'
        f'</div>', unsafe_allow_html=True)
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
    field_statuses = gmc_field_status(df_hash, df)
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

# ── Hero Section ───────────────────────────────────────────────────────────
st.markdown("---")

h1, h2, h3, h4, h5 = st.columns([1.2, 1, 1, 1, 1])
with h1:
    gc = SCORE_COLORS[overall_grade]
    st.markdown(
        f'<div class="hero-ring">'
        f'{svg_ring(overall_pct, size=150, stroke=9, color=gc)}'
        f'<div class="ring-label">Overall Score</div>'
        f'<div class="ring-grade" style="color:{gc};">{overall_grade}</div>'
        f'</div>', unsafe_allow_html=True)
with h2:
    st.metric("Products Analysed", f"{len(df):,}")
with h3:
    st.metric("Attributes Found", f"{sum(1 for r in results if r['Found'])} / {len(results)}")
with h4:
    st.metric("GMC Errors", f"{errors_count}", delta=f"{warnings_count} warnings" if warnings_count else None, delta_color="off")
with h5:
    st.metric("Priority Actions", f"{len(recs)}")

# ── Download ───────────────────────────────────────────────────────────────
report_bytes = generate_excel_report(results, gmc_issues, recs, df)
st.download_button("Download Full Report (.xlsx)", data=report_bytes, file_name="feed_audit_report.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tabs = st.tabs(["Priority Actions", "GMC Readiness", "Scores Overview", "Content Quality", "Pricing & Images", "Fill Rates", "Feed Data"])

# ────────────────────────────────────────────────────────────────────────────
# TAB 1: PRIORITY ACTIONS
# ────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    if not recs:
        st.markdown(
            f'<div style="text-align:center;padding:3rem;animation:fadeInUp 0.6s ease both;">'
            f'<div style="font-size:3rem;margin-bottom:0.5rem;">&#x2705;</div>'
            f'<div style="font-size:1.2rem;font-weight:700;color:{SEA};">No issues found</div>'
            f'<div style="color:#666;font-size:0.9rem;margin-top:0.3rem;">Your feed looks great — keep it up!</div>'
            f'</div>', unsafe_allow_html=True)
    else:
        high = sum(1 for r in recs if r[0] == "high")
        med = sum(1 for r in recs if r[0] == "medium")
        low = sum(1 for r in recs if r[0] == "low")
        st.markdown(
            f'<div style="display:flex;gap:1.5rem;margin-bottom:1.2rem;animation:fadeIn 0.5s ease both;">'
            f'<span style="color:#FF5252;font-weight:700;font-size:0.85rem;">&#x25CF; {high} High Impact</span>'
            f'<span style="color:#FFC107;font-weight:700;font-size:0.85rem;">&#x25CF; {med} Medium Impact</span>'
            f'<span style="color:{SEA};font-weight:700;font-size:0.85rem;">&#x25CF; {low} Low Impact</span>'
            f'</div>', unsafe_allow_html=True)

        for idx, (priority, message, action) in enumerate(recs):
            icon = "&#x26D4;" if priority == "high" else "&#x26A0;" if priority == "medium" else "&#x1F4A1;"
            st.markdown(
                f'<div class="rec-card {priority}">'
                f'<div class="rec-impact {priority}">{icon} {priority} impact</div>'
                f'<div style="color:{LIGHT};font-weight:600;margin-bottom:0.3rem;font-size:0.92rem;">{message}</div>'
                f'<div style="color:#777;font-size:0.82rem;line-height:1.5;">{action}</div>'
                f'</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 2: GMC READINESS (completely redesigned)
# ────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    # Calculate readiness score
    required_fields = [f for f in field_statuses if f["required"]]
    required_pass = sum(1 for f in required_fields if f["status"] == "pass")
    all_pass = sum(1 for f in field_statuses if f["status"] == "pass")
    readiness_pct = (required_pass / max(len(required_fields), 1)) * 100
    is_ready = errors_count == 0 and readiness_pct >= 80

    # Top row: readiness gauge + summary cards
    g1, g2, g3 = st.columns([1.5, 1, 1])
    with g1:
        status_color = SEA if is_ready else "#FF5252" if errors_count > 0 else "#FFC107"
        status_text = "Ready to Upload" if is_ready else "Not Ready" if errors_count > 0 else "Needs Attention"
        st.markdown(
            f'<div class="readiness-meter" style="border-color:rgba({int(status_color[1:3],16)},{int(status_color[3:5],16)},{int(status_color[5:7],16)},0.2);">'
            f'{svg_ring(readiness_pct, size=160, stroke=10, color=status_color)}'
            f'<div class="big-status" style="color:{status_color};margin-top:0.5rem;">{status_text}</div>'
            f'<div class="sub-text">GMC Readiness Score</div>'
            f'</div>', unsafe_allow_html=True)
    with g2:
        st.markdown(
            f'<div class="cat-card" style="animation-delay:0.1s;">'
            f'<div class="cat-pct" style="color:#FF5252;">{errors_count}</div>'
            f'<div class="cat-name">Errors</div>'
            f'<div style="color:#666;font-size:0.75rem;margin-top:0.4rem;">Will cause disapprovals</div>'
            f'</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown(
            f'<div class="cat-card" style="animation-delay:0.2s;">'
            f'<div class="cat-pct" style="color:#FFC107;">{warnings_count}</div>'
            f'<div class="cat-name">Warnings</div>'
            f'<div style="color:#666;font-size:0.75rem;margin-top:0.4rem;">May reduce performance</div>'
            f'</div>', unsafe_allow_html=True)
    with g3:
        st.markdown(
            f'<div class="cat-card" style="animation-delay:0.15s;">'
            f'<div class="cat-pct" style="color:{SEA};">{all_pass}</div>'
            f'<div class="cat-name">Fields Passing</div>'
            f'<div style="color:#666;font-size:0.75rem;margin-top:0.4rem;">Out of {len(field_statuses)} checked</div>'
            f'</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown(
            f'<div class="cat-card" style="animation-delay:0.25s;">'
            f'<div class="cat-pct" style="color:{LIGHT};">{len(df):,}</div>'
            f'<div class="cat-name">Products Scanned</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("")

    # Field checklist
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown('<div class="section-header">Required Fields</div>', unsafe_allow_html=True)
        required = [f for f in field_statuses if f["required"]]
        html = ""
        for f in required:
            icon_map = {"pass": f"&#x2713;", "fail": "&#x2717;", "warn": "&#x25CB;"}
            icon = icon_map.get(f["status"], "?")
            html += (
                f'<div class="gmc-field-row">'
                f'<div class="gmc-icon {f["status"]}">{icon}</div>'
                f'<div class="gmc-field-name">{f["name"]}'
                f'<span style="font-size:0.7rem;color:#555;margin-left:6px;">REQUIRED</span></div>'
                f'<div class="gmc-field-detail">{f["detail"]}</div>'
                f'</div>'
            )
        st.markdown(html, unsafe_allow_html=True)

    with fc2:
        st.markdown('<div class="section-header">Recommended Fields</div>', unsafe_allow_html=True)
        optional = [f for f in field_statuses if not f["required"]]
        html = ""
        for f in optional:
            icon_map = {"pass": f"&#x2713;", "fail": "&#x2717;", "warn": "&#x25CB;"}
            icon = icon_map.get(f["status"], "?")
            html += (
                f'<div class="gmc-field-row">'
                f'<div class="gmc-icon {f["status"]}">{icon}</div>'
                f'<div class="gmc-field-name">{f["name"]}</div>'
                f'<div class="gmc-field-detail">{f["detail"]}</div>'
                f'</div>'
            )
        st.markdown(html, unsafe_allow_html=True)

    # Issues detail
    if gmc_issues:
        st.markdown("")
        st.markdown('<div class="section-header">Detailed Issues</div>', unsafe_allow_html=True)

        # Severity distribution donut
        dc1, dc2 = st.columns([1, 2])
        with dc1:
            e_cnt = sum(1 for i in gmc_issues if i["severity"] == "error")
            w_cnt = sum(1 for i in gmc_issues if i["severity"] == "warning")
            if e_cnt + w_cnt > 0:
                st.plotly_chart(chart_donut(
                    [e_cnt, w_cnt], ["Errors", "Warnings"],
                    ["#FF5252", "#FFC107"],
                    hole_text=f"{e_cnt + w_cnt}"
                ), use_container_width=True)

        with dc2:
            for issue in gmc_issues:
                sev = issue["severity"]
                icon = "&#x26D4;" if sev == "error" else "&#x26A0;"
                st.markdown(
                    f'<div class="issue-card">'
                    f'<div class="issue-icon">{icon}</div>'
                    f'<div class="issue-body">'
                    f'<div style="color:{LIGHT};font-weight:500;font-size:0.9rem;">{issue["message"]}</div>'
                    f'<div style="color:#555;font-size:0.78rem;margin-top:0.2rem;">Field: {issue["field"]}</div>'
                    f'</div>'
                    f'<div class="issue-count {sev}">{issue["count"]:,} products</div>'
                    f'</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="text-align:center;padding:2rem;animation:fadeInUp 0.6s ease both;">'
            f'<div style="font-size:3rem;margin-bottom:0.5rem;">&#x1F389;</div>'
            f'<div style="font-size:1.1rem;font-weight:700;color:{SEA};">Zero issues detected</div>'
            f'<div style="color:#666;font-size:0.85rem;margin-top:0.3rem;">Your feed is ready for Google Merchant Center</div>'
            f'</div>', unsafe_allow_html=True)

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
        for idx, (cat, d) in enumerate(cat_data.items()):
            pct = d["w"] / max(d["p"], 1) * 100
            grade = "Excellent" if pct >= 90 else "Good" if pct >= 70 else "Average" if pct >= 50 else "Below Average" if pct > 30 else "Insufficient"
            color = SCORE_COLORS[grade]
            st.markdown(
                f'<div class="cat-card" style="animation-delay:{idx * 0.1}s;">'
                f'<div class="cat-pct" style="color:{color};">{pct:.0f}%</div>'
                f'<div class="cat-name">{cat}</div>'
                f'<div style="margin-top:0.5rem;">{animated_bar(pct, color, delay=0.3 + idx * 0.15)}</div>'
                f'<div style="margin-top:0.4rem;">{score_badge(grade)}</div>'
                f'</div>', unsafe_allow_html=True)
            st.markdown("")

    # Grade banner
    gc = SCORE_COLORS[overall_grade]
    st.markdown(
        f'<div style="background:rgba({int(gc[1:3],16)},{int(gc[3:5],16)},{int(gc[5:7],16)},0.08);'
        f'border:1px solid rgba({int(gc[1:3],16)},{int(gc[3:5],16)},{int(gc[5:7],16)},0.2);'
        f'border-radius:14px;padding:1.2rem;text-align:center;animation:fadeInUp 0.6s ease both;">'
        f'<span style="font-size:1.2rem;color:{gc};font-weight:800;">{overall_grade}</span>'
        f'<span style="color:#666;font-size:0.9rem;margin-left:12px;">Weighted: {total_weighted} / {total_potential}</span>'
        f'</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Attribute Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_bars(results), use_container_width=True)

    with st.expander("View detailed score table"):
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

        if title_data["components"]:
            st.markdown('<div class="section-header">Title Component Presence</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:#555;font-size:0.82rem;margin-bottom:0.8rem;">How often each product attribute appears in the title text</p>', unsafe_allow_html=True)

            comp_html = ""
            for comp_name, rate in sorted(title_data["components"].items(), key=lambda x: -x[1]):
                color = _color_for_rate(rate)
                comp_html += (
                    f'<div class="fill-row">'
                    f'<div class="fill-name">{comp_name}</div>'
                    f'<div class="fill-track"><div class="fill-bar" style="width:{rate*100:.0f}%;background:{color};"></div></div>'
                    f'<div class="fill-pct" style="color:{color};">{rate:.0%}</div>'
                    f'</div>'
                )
            st.markdown(comp_html, unsafe_allow_html=True)

        if title_data["top_words"]:
            with st.expander("Most Common Title Words"):
                words, counts = zip(*title_data["top_words"][:20])
                fig_words = go.Figure(go.Bar(x=list(counts), y=list(words), orientation="h",
                                             marker=dict(color=VIOLET, line=dict(width=0), cornerradius=3),
                                             text=list(counts), textposition="outside",
                                             textfont=dict(color=LIGHT, size=9),
                                             hovertemplate="%{y}: %{x} occurrences<extra></extra>"))
                fig_words.update_layout(**CHART_LAYOUT, yaxis=dict(autorange="reversed", tickfont=dict(color=LIGHT, size=10)),
                                        xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
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

            # Price range breakdown
            with st.expander("Price Range Breakdown"):
                p = pricing["prices"]
                ranges = [
                    ("Under $10", (p < 10).sum()),
                    ("$10 - $25", ((p >= 10) & (p < 25)).sum()),
                    ("$25 - $50", ((p >= 25) & (p < 50)).sum()),
                    ("$50 - $100", ((p >= 50) & (p < 100)).sum()),
                    ("$100 - $250", ((p >= 100) & (p < 250)).sum()),
                    ("$250+", (p >= 250).sum()),
                ]
                ranges = [(name, cnt) for name, cnt in ranges if cnt > 0]
                if ranges:
                    names, counts = zip(*ranges)
                    st.plotly_chart(chart_donut(list(counts), list(names),
                                    [VIOLET, BLUE, SEA, "#FFC107", "#FF9800", "#FF5252"][:len(ranges)],
                                    hole_text=f"{len(p):,}"), use_container_width=True)
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

        # Visual coverage bar
        coverage_pct = (images["total"] - images["missing"]) / max(images["total"], 1) * 100
        cov_color = _color_for_rate(coverage_pct / 100)
        st.markdown(
            f'<div style="margin:1rem 0;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="color:#888;font-size:0.82rem;">Primary Image Coverage</span>'
            f'<span style="color:{cov_color};font-weight:700;font-size:0.82rem;">{coverage_pct:.0f}%</span>'
            f'</div>'
            f'{animated_bar(coverage_pct, cov_color)}'
            f'</div>', unsafe_allow_html=True)

        add_pct = images["has_additional_pct"] * 100
        add_color = _color_for_rate(images["has_additional_pct"])
        st.markdown(
            f'<div style="margin:0.5rem 0 1rem;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="color:#888;font-size:0.82rem;">Additional Image Coverage</span>'
            f'<span style="color:{add_color};font-weight:700;font-size:0.82rem;">{add_pct:.0f}%</span>'
            f'</div>'
            f'{animated_bar(add_pct, add_color, delay=0.2)}'
            f'</div>', unsafe_allow_html=True)

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
                with st.expander(f"Top {label} categories"):
                    top = list(data["top_values"].items())[:8]
                    fig_tax = go.Figure(go.Bar(
                        x=[v for _, v in top], y=[k[:50] for k, _ in top], orientation="h",
                        marker=dict(color=BLUE, line=dict(width=0), cornerradius=3),
                        text=[f"{v:,}" for _, v in top], textposition="outside",
                        textfont=dict(color=LIGHT, size=9),
                        hovertemplate="%{y}<br>%{x:,} products<extra></extra>",
                    ))
                    fig_tax.update_layout(**CHART_LAYOUT, yaxis=dict(autorange="reversed", tickfont=dict(color=LIGHT, size=9)),
                                          xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
                                          margin=dict(l=250, r=60, t=10, b=20), height=max(200, len(top) * 32))
                    st.plotly_chart(fig_tax, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 6: FILL RATES (redesigned with animated bars)
# ────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-header">Attribute Fill Rates</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#555;font-size:0.82rem;margin-bottom:1rem;">How completely each attribute is populated across your feed</p>', unsafe_allow_html=True)

    fill_html = ""
    for idx, r in enumerate(sorted(results, key=lambda x: -x["Fill Rate"])):
        rate = r["Fill Rate"]
        color = _color_for_rate(rate)
        weight_tag = ""
        if r["Weighting"] == "Must have":
            weight_tag = '<span style="font-size:0.6rem;background:rgba(255,82,82,0.12);color:#FF5252;padding:1px 6px;border-radius:8px;margin-left:6px;font-weight:600;">REQUIRED</span>'

        fill_html += (
            f'<div class="fill-row">'
            f'<div class="fill-name">{r["Attribute"]}{weight_tag}</div>'
            f'<div class="fill-track"><div class="fill-bar" style="width:{rate*100:.0f}%;background:{color};"></div></div>'
            f'<div class="fill-pct" style="color:{color};">{rate:.0%}</div>'
            f'<div class="fill-badge">{score_badge(r["Score"])}</div>'
            f'</div>'
        )
    st.markdown(fill_html, unsafe_allow_html=True)

    missing = [r for r in results if not r["Found"]]
    low = [r for r in results if r["Found"] and r["Fill Rate"] < 0.5]
    if missing:
        st.markdown("")
        st.warning(f"**{len(missing)} attribute(s) not found:** " + ", ".join(r["Attribute"] for r in missing))
    if low:
        st.warning(f"**{len(low)} attribute(s) below 50% fill:** " + ", ".join(f'{r["Attribute"]} ({r["Fill Rate"]:.0%})' for r in low))
    if not missing and not low:
        st.markdown("")
        st.success("All attributes found with fill rates above 50%!")

# ────────────────────────────────────────────────────────────────────────────
# TAB 7: RAW DATA
# ────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown(f'<div class="section-header">Feed Preview</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#555;font-size:0.82rem;margin-bottom:0.6rem;">Showing {min(len(df), 200):,} of {len(df):,} rows</p>', unsafe_allow_html=True)
    st.dataframe(df.head(200), use_container_width=True, height=500)

    with st.expander(f"Detected Columns ({len(df.columns)})"):
        col_html = " ".join(
            f'<span style="display:inline-block;padding:3px 10px;margin:3px;border-radius:8px;'
            f'background:rgba(0,155,255,0.08);color:{BLUE};font-size:0.78rem;font-weight:500;">{c}</span>'
            for c in df.columns
        )
        st.markdown(col_html, unsafe_allow_html=True)
