import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
import hashlib
import math
import json
from io import BytesIO
from collections import Counter

# ═════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pattern — Feed Audit",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 30'><path d='M23.1 0.3L0.3 22.8c-0.4 0.4-0.4 1 0 1.3l5.6 5.6c0.4 0.4 1 0.4 1.4 0L30.1 7.2c0.4-0.4 0.4-1 0-1.3L24.5 0.3C24.1-0.1 23.5-0.1 23.1 0.3z' fill='%23009BFF'/><path d='M32.5 9.6L19.1 22.8c-0.4 0.4-0.4 1 0 1.3l5.6 5.6c0.4 0.4 1 0.4 1.4 0l13.4-13.3c0.4-0.4 0.4-1 0-1.3l-5.6-5.6C33.5 9.2 32.9 9.2 32.5 9.6z' fill='%23009BFF'/></svg>",
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
AMBER = "#FFC107"
ORANGE = "#FF9800"
RED = "#FF5252"

LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="191" height="38" viewBox="0 0 191 38" fill="none"><g clip-path="url(#clip0)"><path d="M23.1323 0.277129L0.336866 22.8367C-0.0379489 23.2076 -0.0379491 23.809 0.336866 24.1799L5.95075 29.7357C6.32557 30.1067 6.93326 30.1067 7.30808 29.7357L30.1035 7.1762C30.4783 6.80526 30.4783 6.20385 30.1035 5.83292L24.4896 0.277128C24.1148 -0.0938081 23.5071 -0.0938066 23.1323 0.277129Z" fill="#009BFF"/><path d="M32.5193 9.56975L19.1171 22.8332C18.7423 23.2042 18.7423 23.8056 19.1171 24.1765L24.731 29.7323C25.1058 30.1032 25.7135 30.1032 26.0884 29.7323L39.4905 16.4688C39.8654 16.0979 39.8654 15.4965 39.4905 15.1255L33.8767 9.56975C33.5018 9.19881 32.8942 9.19881 32.5193 9.56975Z" fill="#009BFF"/><path d="M72.0318 17.9793C72.0318 24.7983 66.8064 30.0154 60.5177 30.0154C56.9126 30.0154 54.1845 28.5504 52.4273 26.1703V37.4408C52.4273 37.5892 52.3677 37.7314 52.2618 37.8363C52.1558 37.9411 52.0121 38 51.8622 38H47.9977C47.8478 38 47.7041 37.9411 47.5981 37.8363C47.4921 37.7314 47.4326 37.5892 47.4326 37.4408V7.09944C47.4326 6.95113 47.4921 6.8089 47.5981 6.70403C47.7041 6.59916 47.8478 6.54025 47.9977 6.54025H51.8622C52.0121 6.54025 52.1558 6.59916 52.2618 6.70403C52.3677 6.8089 52.4273 6.95113 52.4273 7.09944V9.83398C54.1781 7.40976 56.9126 5.94482 60.5177 5.94482C66.8064 5.94482 72.0318 11.2075 72.0318 17.9793ZM67.0388 17.9793C67.0388 13.7263 63.8936 10.6578 59.733 10.6578C55.5724 10.6578 52.4273 13.7247 52.4273 17.9793C52.4273 22.2339 55.5708 25.3008 59.733 25.3008C63.8952 25.3008 67.0388 22.2355 67.0388 17.9793Z" fill="#FCFCFC"/><path d="M98.4814 7.09944V28.8608C98.4814 29.0091 98.4219 29.1513 98.3159 29.2562C98.2099 29.361 98.0662 29.42 97.9164 29.42H94.0534C93.9035 29.42 93.7598 29.361 93.6538 29.2562C93.5479 29.1513 93.4883 29.0091 93.4883 28.8608V26.1246C91.7375 28.5504 89.003 30.0154 85.3963 30.0154C79.1076 30.0154 73.8838 24.7527 73.8838 17.9793C73.8838 11.1619 79.1076 5.94482 85.3963 5.94482C89.003 5.94482 91.7311 7.40976 93.4883 9.7883V7.09944C93.4883 6.95113 93.5479 6.8089 93.6538 6.70403C93.7598 6.59916 93.9035 6.54025 94.0534 6.54025H97.9164C98.0662 6.54025 98.2099 6.59916 98.3159 6.70403C98.4219 6.8089 98.4814 6.95113 98.4814 7.09944ZM93.4883 17.9793C93.4883 13.7263 90.3432 10.6578 86.1826 10.6578C82.022 10.6578 78.8768 13.7247 78.8768 17.9793C78.8768 22.2339 82.022 25.3008 86.1826 25.3008C90.3432 25.3008 93.4883 22.2355 93.4883 17.9793Z" fill="#FCFCFC"/><path d="M139.785 25.4851C142.343 25.4851 144.31 24.4345 145.472 23.0168C145.557 22.9161 145.675 22.8489 145.806 22.8272C145.937 22.8055 146.071 22.8309 146.185 22.8986L149.33 24.718C149.398 24.7567 149.458 24.8092 149.504 24.8721C149.551 24.9351 149.584 25.007 149.6 25.0833C149.617 25.1596 149.617 25.2384 149.6 25.3147C149.584 25.391 149.551 25.463 149.505 25.5261C147.356 28.3378 144.023 30.0154 139.74 30.0154C132.11 30.0154 127.166 24.844 127.166 17.9793C127.166 11.206 132.113 5.94482 139.373 5.94482C146.263 5.94482 150.979 11.436 150.979 18.025C150.965 18.7152 150.904 19.4036 150.794 20.0853H132.387C133.173 23.6547 136.087 25.4851 139.785 25.4851ZM145.935 16.0576C145.241 12.1196 142.328 10.4294 139.323 10.4294C135.578 10.4294 133.034 12.6252 132.342 16.0576H145.935Z" fill="#FCFCFC"/><path d="M191.055 15.3712V28.8612C191.055 29.0095 190.996 29.1517 190.89 29.2566C190.784 29.3615 190.64 29.4204 190.49 29.4204H186.627C186.477 29.4204 186.334 29.3615 186.228 29.2566C186.122 29.1517 186.062 29.0095 186.062 28.8612V15.8753C186.062 12.3973 184.026 10.5669 180.883 10.5669C177.599 10.5669 175.011 12.4886 175.011 17.1559V28.8612C175.011 28.9348 174.997 29.0076 174.968 29.0756C174.94 29.1435 174.898 29.2052 174.845 29.2572C174.793 29.3091 174.73 29.3503 174.661 29.3783C174.593 29.4063 174.519 29.4206 174.445 29.4204H170.582C170.432 29.4204 170.288 29.3615 170.182 29.2566C170.076 29.1517 170.017 29.0095 170.017 28.8612V7.09988C170.017 6.95158 170.076 6.80934 170.182 6.70447C170.288 6.5996 170.432 6.54069 170.582 6.54069H174.446C174.521 6.54048 174.594 6.55479 174.663 6.5828C174.732 6.61081 174.794 6.65197 174.847 6.70392C174.899 6.75586 174.941 6.81758 174.97 6.88552C174.998 6.95347 175.013 7.02632 175.013 7.09988V9.46267C176.538 7.08256 179.035 5.93896 182.175 5.93896C187.356 5.94527 191.055 9.4233 191.055 15.3712Z" fill="#FCFCFC"/><path d="M165.186 6.12744C162.274 6.12744 159.456 7.27261 158.065 10.3805V7.09934C158.065 6.95103 158.006 6.8088 157.9 6.70393C157.794 6.59906 157.65 6.54014 157.5 6.54014H153.637C153.487 6.54014 153.344 6.59906 153.238 6.70393C153.132 6.8088 153.072 6.95103 153.072 7.09934V28.8607C153.072 29.009 153.132 29.1512 153.238 29.2561C153.344 29.3609 153.487 29.4198 153.637 29.4198H157.5C157.65 29.4198 157.794 29.3609 157.9 29.2561C158.006 29.1512 158.065 29.009 158.065 28.8607V17.8878C158.065 12.7637 161.823 11.4815 165.186 11.4815H166.926C167.076 11.4815 167.22 11.4226 167.326 11.3177C167.432 11.2129 167.491 11.0706 167.491 10.9223V6.68821C167.491 6.61464 167.477 6.54176 167.449 6.47373C167.42 6.40571 167.379 6.34387 167.326 6.29178C167.274 6.23969 167.211 6.19836 167.143 6.17016C167.074 6.14196 167 6.12744 166.926 6.12744H165.186Z" fill="#FCFCFC"/><path d="M112.505 11.2989C112.579 11.2991 112.653 11.2848 112.721 11.2568C112.79 11.2287 112.853 11.1876 112.905 11.1356C112.958 11.0837 113 11.022 113.028 10.954C113.057 10.8861 113.071 10.8132 113.071 10.7397V7.0994C113.071 7.02584 113.057 6.95299 113.028 6.88504C113 6.8171 112.958 6.75538 112.905 6.70343C112.853 6.65149 112.79 6.61033 112.721 6.58232C112.653 6.55431 112.579 6.54 112.505 6.54021H106.561V0.554469C106.56 0.408335 106.501 0.268486 106.397 0.164857C106.293 0.0612278 106.152 0.00205319 106.004 0H102.133C101.984 0 101.84 0.0589149 101.734 0.163784C101.628 0.268653 101.568 0.410887 101.568 0.559194V22.6718C101.568 27.369 103.857 29.6247 108.634 29.6247H112.506C112.656 29.6243 112.799 29.5652 112.905 29.4604C113.011 29.3557 113.071 29.2137 113.071 29.0655V25.6001C113.071 25.5265 113.057 25.4537 113.028 25.3857C113 25.3178 112.958 25.256 112.905 25.2041C112.853 25.1521 112.79 25.111 112.721 25.083C112.653 25.055 112.579 25.0407 112.505 25.0409H109.533C107.255 25.0409 106.561 24.4549 106.561 22.2827V11.2989H112.505Z" fill="#FCFCFC"/><path d="M126.061 11.2989C126.211 11.2989 126.354 11.24 126.46 11.1351C126.566 11.0302 126.626 10.888 126.626 10.7397V7.0994C126.626 6.9511 126.566 6.80886 126.46 6.70399C126.354 6.59912 126.211 6.54021 126.061 6.54021H120.124V0.554469C120.123 0.406981 120.063 0.265959 119.957 0.16211C119.851 0.0582605 119.708 -5.26628e-06 119.559 3.57006e-10H115.696C115.546 3.57006e-10 115.402 0.0589149 115.296 0.163784C115.19 0.268653 115.131 0.410887 115.131 0.559194V22.6718C115.131 27.369 117.418 29.6247 122.196 29.6247H126.069C126.218 29.6239 126.361 29.5646 126.467 29.4599C126.572 29.3552 126.632 29.2134 126.632 29.0655V25.6001C126.632 25.5264 126.617 25.4536 126.588 25.3858C126.559 25.318 126.516 25.2565 126.463 25.205C126.41 25.1535 126.347 25.1128 126.278 25.0855C126.209 25.0581 126.135 25.0446 126.061 25.0456H123.089C120.812 25.0456 120.118 24.4596 120.118 22.2874V11.2989H126.061Z" fill="#FCFCFC"/></g><defs><clipPath id="clip0"><rect width="191" height="38" fill="white"/></clipPath></defs></svg>'''

SCORE_COLORS = {"Excellent": SEA, "Good": BLUE, "Average": AMBER, "Below Average": ORANGE, "Insufficient": RED}
SCORE_MAP = {"Excellent": 5, "Good": 4, "Average": 3, "Below Average": 2, "Insufficient": 1}
WEIGHTING_MAP = {"Must have": 3, "Good to have": 2, "Bonus": 1}


# ═════════════════════════════════════════════════════════════════════════════
# 3. CSS INJECTION
# ═════════════════════════════════════════════════════════════════════════════

def _inject_css():
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400;500;600;700;800&display=swap');

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to   {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes drawCircle {{
        from {{ stroke-dashoffset: 440; }}
    }}
    @keyframes barGrow {{
        from {{ width: 0%; }}
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50%      {{ transform: scale(1.03); }}
    }}
    @keyframes checkPop {{
        0%   {{ transform: scale(0); }}
        60%  {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); }}
    }}

    /* ── Base ─────────────────────────────────────────── */
    .stApp {{
        background: {DARK};
        font-family: 'Wix Madefor Display', 'Source Sans Pro', sans-serif;
    }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li {{ color: {LIGHT}; }}
    section[data-testid="stSidebar"] {{ background: #0E1117; }}

    /* ── Buttons ──────────────────────────────────────── */
    .stButton > button {{
        background: {GRADIENT};
        color: white; border: none; border-radius: 10px;
        font-weight: 600; font-size: 15px; padding: 0.6rem 1.6rem;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,155,255,0.25);
        color: white; border: none;
    }}

    /* ── Metric cards ─────────────────────────────────── */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px; padding: 1.2rem;
        animation: fadeInUp 0.5s ease-out both;
        transition: all 0.3s ease;
    }}
    [data-testid="stMetric"]:hover {{
        border-color: rgba(0,155,255,0.15);
        transform: translateY(-2px);
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"] {{ animation-delay: 0.05s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] {{ animation-delay: 0.10s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] {{ animation-delay: 0.15s; }}
    [data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"] {{ animation-delay: 0.20s; }}

    /* ── Section headers ──────────────────────────────── */
    .sh {{
        border-left: 3px solid {BLUE}; padding-left: 12px;
        margin: 1.8rem 0 0.6rem; font-size: 1.05rem;
        font-weight: 700; color: {LIGHT};
        animation: slideInLeft 0.4s ease-out both;
    }}

    /* ── Glass card ────────────────────────────────────── */
    .glass {{
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px; padding: 1.4rem;
        animation: fadeInUp 0.5s ease-out both;
        transition: all 0.3s ease;
    }}
    .glass:hover {{
        border-color: rgba(0,155,255,0.12);
        transform: translateY(-2px);
    }}

    /* ── Narrative card ────────────────────────────────── */
    .narrative {{
        background: rgba(0,155,255,0.04);
        border: 1px solid rgba(0,155,255,0.1);
        border-radius: 16px; padding: 1.6rem 1.8rem;
        animation: fadeInUp 0.6s ease-out 0.2s both;
        line-height: 1.7; font-size: 0.92rem; color: #ccc;
    }}
    .narrative strong {{ color: {LIGHT}; }}
    .narrative .highlight {{ color: {BLUE}; font-weight: 700; }}
    .narrative .warn {{ color: {AMBER}; font-weight: 600; }}
    .narrative .bad {{ color: {RED}; font-weight: 600; }}
    .narrative .good {{ color: {SEA}; font-weight: 600; }}

    /* ── Score ring ────────────────────────────────────── */
    .ring-wrap {{
        display: flex; flex-direction: column; align-items: center;
        padding: 1rem 0; animation: fadeInUp 0.6s ease-out both;
    }}
    .ring-wrap svg {{ filter: drop-shadow(0 0 24px rgba(0,155,255,0.15)); }}
    .ring-label {{
        font-size: 0.75rem; color: #555; margin-top: 0.6rem;
        text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500;
    }}
    .ring-grade {{ font-size: 1rem; font-weight: 700; margin-top: 0.15rem; }}

    /* ── GMC field row ─────────────────────────────────── */
    .gmc-row {{
        display: flex; align-items: center; gap: 12px;
        padding: 10px 14px; border-radius: 10px; margin-bottom: 3px;
        animation: fadeInUp 0.35s ease-out both;
        transition: background 0.2s ease;
    }}
    .gmc-row:hover {{ background: rgba(255,255,255,0.03); }}
    .gmc-dot {{
        width: 26px; height: 26px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px; flex-shrink: 0;
        animation: checkPop 0.35s ease both;
    }}
    .gmc-dot.pass {{ background: rgba(76,195,174,0.15); color: {SEA}; }}
    .gmc-dot.fail {{ background: rgba(255,82,82,0.15); color: {RED}; }}
    .gmc-dot.warn {{ background: rgba(255,193,7,0.15); color: {AMBER}; }}
    .gmc-name {{ flex: 1; font-size: 0.88rem; color: {LIGHT}; font-weight: 500; }}
    .gmc-detail {{ font-size: 0.76rem; color: #555; text-align: right; }}

    /* ── Fill bar row ──────────────────────────────────── */
    .fb-row {{
        display: flex; align-items: center; gap: 12px;
        padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.03);
        animation: fadeInUp 0.35s ease-out both;
    }}
    .fb-name {{ width: 170px; font-size: 0.84rem; color: {LIGHT}; font-weight: 500; flex-shrink: 0; }}
    .fb-track {{ flex: 1; background: rgba(255,255,255,0.05); border-radius: 5px; height: 8px; overflow: hidden; }}
    .fb-bar {{ height: 100%; border-radius: 5px; animation: barGrow 0.8s cubic-bezier(0.4,0,0.2,1) both; }}
    .fb-pct {{ width: 45px; text-align: right; font-size: 0.8rem; font-weight: 600; }}
    .fb-tag {{ width: 90px; text-align: center; }}

    /* ── Score badge ───────────────────────────────────── */
    .badge {{
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-weight: 600; font-size: 0.72rem;
    }}
    .badge-excellent {{ background: rgba(76,195,174,0.12); color: {SEA}; }}
    .badge-good {{ background: rgba(0,155,255,0.12); color: {BLUE}; }}
    .badge-average {{ background: rgba(255,193,7,0.12); color: {AMBER}; }}
    .badge-below-average {{ background: rgba(255,152,0,0.12); color: {ORANGE}; }}
    .badge-insufficient {{ background: rgba(255,82,82,0.12); color: {RED}; }}

    /* ── Rec cards ─────────────────────────────────────── */
    .rec {{
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.5rem;
        animation: fadeInUp 0.4s ease-out both;
        transition: all 0.25s ease;
    }}
    .rec:hover {{ background: rgba(255,255,255,0.04); transform: translateX(3px); }}
    .rec.high {{ border-left: 3px solid {RED}; }}
    .rec.medium {{ border-left: 3px solid {AMBER}; }}
    .rec.low {{ border-left: 3px solid {SEA}; }}
    .rec-tag {{
        font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.8px; margin-bottom: 0.3rem;
    }}
    .rec-tag.high {{ color: {RED}; }}
    .rec-tag.medium {{ color: {AMBER}; }}
    .rec-tag.low {{ color: {SEA}; }}

    /* ── Issue cards (GMC) ─────────────────────────────── */
    .issue {{
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.4rem;
        display: flex; align-items: flex-start; gap: 12px;
        animation: fadeInUp 0.4s ease-out both;
        transition: all 0.25s ease;
    }}
    .issue:hover {{ background: rgba(255,255,255,0.04); transform: translateX(3px); }}
    .issue-count {{
        font-size: 0.7rem; font-weight: 700; padding: 2px 9px;
        border-radius: 20px; white-space: nowrap;
    }}
    .issue-count.error {{ background: rgba(255,82,82,0.1); color: {RED}; }}
    .issue-count.warning {{ background: rgba(255,193,7,0.1); color: {AMBER}; }}

    /* ── Upload hero ───────────────────────────────────── */
    .upload-hero {{
        text-align: center; padding: 4rem 2rem 3rem;
        animation: fadeInUp 0.7s ease-out both;
    }}
    .upload-hero .icon {{
        font-size: 3.5rem; opacity: 0.15;
        animation: pulse 3s ease-in-out infinite;
    }}
    .upload-hero h2 {{
        font-size: 1.5rem; font-weight: 700; color: {LIGHT};
        margin: 0.8rem 0 0.3rem;
    }}
    .upload-hero p {{ color: #444; font-size: 0.88rem; max-width: 480px; margin: 0 auto; line-height: 1.6; }}
    .upload-tags {{
        display: flex; gap: 7px; justify-content: center;
        margin-top: 1rem; flex-wrap: wrap;
    }}
    .upload-tags span {{
        font-size: 0.68rem; font-weight: 600; padding: 3px 11px;
        border-radius: 20px; background: rgba(0,155,255,0.07); color: {BLUE};
    }}

    /* ── Chrome ────────────────────────────────────────── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="manage-app-button"] {{display: none;}}
    .stAppDeployButton {{display: none;}}
    ._profileContainer_gzau3_53 {{display: none;}}
    [data-testid="stStatusWidget"] {{display: none;}}
    ._container_gzau3_1 {{display: none;}}
    .viewerBadge_container__r5tak {{display: none;}}
    .styles_viewerBadge__CvC9N {{display: none;}}

    .stTabs [data-baseweb="tab-highlight"] {{ background: {GRADIENT}; border-radius: 3px; }}
    .stTabs [data-baseweb="tab"] {{
        color: {LIGHT}; padding: 12px 18px; font-weight: 500;
        transition: color 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {BLUE}; }}
    .stTabs [data-baseweb="tab-border"] {{ background: rgba(255,255,255,0.05); }}

    .stDownloadButton > button {{
        background: transparent; border: 1px solid rgba(255,255,255,0.1);
        color: {LIGHT}; border-radius: 10px; transition: all 0.3s ease;
    }}
    .stDownloadButton > button:hover {{
        border-color: {BLUE}; color: {BLUE};
        background: rgba(0,155,255,0.04);
    }}

    .stApp h1,.stApp h2,.stApp h3 {{
        font-family: 'Wix Madefor Display', sans-serif; color: {LIGHT};
    }}
    .stApp h1 {{ font-weight: 800; }}
    .stApp h2 {{ font-weight: 700; }}
    .stApp h3 {{ font-weight: 600; }}

    [data-testid="stExpander"] {{
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px; background: rgba(255,255,255,0.015);
    }}
    hr {{ border: none; border-top: 1px solid rgba(255,255,255,0.05); }}

    /* stagger animations */
    .gmc-row:nth-child(1) {{ animation-delay: 0s; }}
    .gmc-row:nth-child(2) {{ animation-delay: .03s; }}
    .gmc-row:nth-child(3) {{ animation-delay: .06s; }}
    .gmc-row:nth-child(4) {{ animation-delay: .09s; }}
    .gmc-row:nth-child(5) {{ animation-delay: .12s; }}
    .gmc-row:nth-child(6) {{ animation-delay: .15s; }}
    .gmc-row:nth-child(7) {{ animation-delay: .18s; }}
    .gmc-row:nth-child(8) {{ animation-delay: .21s; }}
    .gmc-row:nth-child(9) {{ animation-delay: .24s; }}
    .gmc-row:nth-child(10) {{ animation-delay: .27s; }}
    .gmc-row:nth-child(11) {{ animation-delay: .30s; }}
    .gmc-row:nth-child(12) {{ animation-delay: .33s; }}
</style>
""", unsafe_allow_html=True)


# ── HTML helpers ─────────────────────────────────────────────────────────

def badge(label: str) -> str:
    cls = label.lower().replace(" ", "-")
    return f'<span class="badge badge-{cls}">{label}</span>'


def svg_ring(pct, size=140, stroke=9, color=BLUE):
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - pct / 100)
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="{stroke}"/>'
        f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}"'
        f' stroke-dasharray="{circ}" stroke-dashoffset="{offset}" stroke-linecap="round"'
        f' transform="rotate(-90 {size/2} {size/2})"'
        f' style="animation:drawCircle 1.2s cubic-bezier(0.4,0,0.2,1) both;"/>'
        f'<text x="{size/2}" y="{size/2+1}" text-anchor="middle" dominant-baseline="middle"'
        f' fill="{LIGHT}" font-family="Wix Madefor Display,sans-serif" font-weight="800"'
        f' font-size="{size*0.22}px">{pct:.0f}%</text></svg>'
    )


def _color(r):
    if r >= 1.0: return SEA
    if r >= 0.8: return BLUE
    if r >= 0.5: return AMBER
    if r > 0.2: return ORANGE
    return RED


# ═════════════════════════════════════════════════════════════════════════════
# 4. COLUMN DETECTION
# ═════════════════════════════════════════════════════════════════════════════

def find_col(df, term):
    cols = {c.lower().strip(): c for c in df.columns}
    if term.lower() in cols: return cols[term.lower()]
    for k, v in cols.items():
        if term.lower() in k: return v
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
    if total == 0: return 0.0
    filled = df[col].apply(lambda x: (isinstance(x, str) and len(x.strip()) > 0) or (pd.notna(x) and not isinstance(x, str))).sum()
    return filled / total


def _rate_to_score(r):
    if r >= 1.0: return "Excellent"
    if r >= 0.8: return "Good"
    if r >= 0.5: return "Average"
    if r > 0.2: return "Below Average"
    return "Insufficient"


@st.cache_data(show_spinner=False)
def run_audit(_h, df):
    results = []
    for name, cat, weight, term, logic in AUDIT_ATTRS:
        col = find_col(df, term)
        found = col is not None
        rate = 0.0
        label = "Insufficient"
        if logic == "custom_label":
            idxs = set()
            for i in range(5):
                for c in df.columns:
                    if f"custom label {i}" in c.lower() or f"custom_label_{i}" in c.lower():
                        idxs.add(i); break
            rate = len(idxs) / 5
            found = rate > 0
            label = _rate_to_score(rate)
        elif found:
            if logic == "fill": rate = _fill_rate(df, col)
            elif logic == "condition": rate = df[col].astype(str).str.lower().str.strip().eq("new").sum() / max(len(df), 1)
            elif logic == "availability": rate = df[col].astype(str).str.lower().str.strip().eq("in stock").sum() / max(len(df), 1)
            label = _rate_to_score(rate)
        nw = WEIGHTING_MAP.get(weight, 1)
        ns = SCORE_MAP.get(label, 1)
        results.append({"Category": cat, "Attribute": name, "Weighting": weight,
                        "Found": found, "Fill Rate": rate, "Score": label,
                        "Num Weight": nw, "Num Score": ns,
                        "Weighted": nw * ns, "Potential": nw * 5})
    return results


# ═════════════════════════════════════════════════════════════════════════════
# 6. GMC VALIDATION
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def run_gmc_validation(_h, df):
    issues = []
    total = len(df)
    id_col = find_col(df, "id"); title_col = find_col(df, "title")
    desc_col = find_col(df, "description"); price_col = find_col(df, "price")
    link_col = find_col(df, "link"); img_col = find_col(df, "image link")
    avail_col = find_col(df, "availability"); cond_col = find_col(df, "condition")
    brand_col = find_col(df, "brand"); gtin_col = find_col(df, "gtin")

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
                               "message": f"{n:,} products missing required '{field}'"})

    if title_col:
        titles = df[title_col].astype(str)
        n = (titles.str.len() > 150).sum()
        if n: issues.append({"severity": "warning", "field": "title", "count": int(n),
                             "message": f"{n:,} titles exceed 150 characters"})
        n = (titles.str.len() < 25).sum()
        if n: issues.append({"severity": "warning", "field": "title", "count": int(n),
                             "message": f"{n:,} titles under 25 characters"})
    if desc_col:
        n = (df[desc_col].astype(str).str.len() > 5000).sum()
        if n: issues.append({"severity": "warning", "field": "description", "count": int(n),
                             "message": f"{n:,} descriptions exceed 5,000 characters"})
    if price_col:
        prices = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        n = int((prices == 0).sum() + prices.isna().sum())
        if n: issues.append({"severity": "error", "field": "price", "count": n,
                             "message": f"{n:,} products with invalid or zero price"})
    if avail_col:
        valid = {"in stock", "out of stock", "preorder", "backorder", "in_stock", "out_of_stock"}
        inv = ~df[avail_col].astype(str).str.lower().str.strip().isin(valid) & df[avail_col].notna() & (df[avail_col].astype(str).str.strip() != "")
        n = inv.sum()
        if n: issues.append({"severity": "error", "field": "availability", "count": int(n),
                             "message": f"{n:,} products with invalid availability value"})
    if cond_col:
        inv = ~df[cond_col].astype(str).str.lower().str.strip().isin({"new","refurbished","used"}) & df[cond_col].notna() & (df[cond_col].astype(str).str.strip() != "")
        n = inv.sum()
        if n: issues.append({"severity": "warning", "field": "condition", "count": int(n),
                             "message": f"{n:,} non-standard condition values"})
    if link_col:
        n = df[link_col].astype(str).str.startswith("http://").sum()
        if n: issues.append({"severity": "warning", "field": "link", "count": int(n),
                             "message": f"{n:,} links use HTTP instead of HTTPS"})
    if img_col:
        n = df[img_col].astype(str).str.startswith("http://").sum()
        if n: issues.append({"severity": "warning", "field": "image_link", "count": int(n),
                             "message": f"{n:,} image URLs use HTTP instead of HTTPS"})
    if id_col:
        n = df[id_col].dropna().astype(str).duplicated().sum()
        if n: issues.append({"severity": "error", "field": "id", "count": int(n),
                             "message": f"{n:,} duplicate product IDs"})
    if gtin_col and brand_col:
        has_brand = df[brand_col].astype(str).str.strip().ne("") & df[brand_col].notna()
        miss_gtin = df[gtin_col].isna() | (df[gtin_col].astype(str).str.strip() == "")
        n = (has_brand & miss_gtin).sum()
        if n: issues.append({"severity": "warning", "field": "gtin", "count": int(n),
                             "message": f"{n:,} branded products missing GTIN"})
    sale_col = find_col(df, "sale price")
    if sale_col and price_col:
        sp = pd.to_numeric(df[sale_col].astype(str).str.replace(r"[^\d.]","",regex=True), errors="coerce")
        rp = pd.to_numeric(df[price_col].astype(str).str.replace(r"[^\d.]","",regex=True), errors="coerce")
        n = ((sp >= rp) & sp.notna() & rp.notna() & (rp > 0)).sum()
        if n: issues.append({"severity": "error", "field": "sale_price", "count": int(n),
                             "message": f"{n:,} products where sale price >= regular price"})
    issues.sort(key=lambda x: (0 if x["severity"]=="error" else 1, -x["count"]))
    return issues


@st.cache_data(show_spinner=False)
def gmc_field_status(_h, df):
    fields = [
        ("Product ID", "id", True), ("Title", "title", True),
        ("Description", "description", True), ("Price", "price", True),
        ("Product Link", "link", True), ("Image Link", "image link", True),
        ("Availability", "availability", True), ("Condition", "condition", True),
        ("Brand", "brand", True), ("GTIN", "gtin", True),
        ("Google Product Category", "google product category", False),
        ("Product Type", "product type", False),
    ]
    statuses = []
    total = len(df)
    for name, term, req in fields:
        col = find_col(df, term)
        if col is None:
            statuses.append({"name": name, "required": req,
                             "status": "fail" if req else "warn",
                             "detail": "Not found", "fill_rate": 0.0})
        else:
            rate = _fill_rate(df, col)
            missing = int(total * (1 - rate))
            if rate >= 0.95: status = "pass"
            elif rate >= 0.7: status = "warn"
            else: status = "fail"
            detail = "100% filled" if rate >= 1.0 else f"{rate:.0%} filled ({missing:,} missing)"
            statuses.append({"name": name, "required": req,
                             "status": status, "detail": detail, "fill_rate": rate})
    return statuses


# ═════════════════════════════════════════════════════════════════════════════
# 7. TITLE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def analyze_titles(_h, df):
    col = find_col(df, "title")
    if col is None: return None
    titles = df[col].astype(str)
    lengths = titles.str.len()
    components = {}
    for comp, cc in [("Brand","brand"),("Color","color"),("Size","size"),("Material","material"),("Gender","gender")]:
        c = find_col(df, cc)
        if c:
            vals = df[c].astype(str).str.strip()
            components[comp] = sum(1 for t, v in zip(titles, vals) if v and v.lower() != "nan" and v.lower() in t.lower()) / max(len(df), 1)
    words = " ".join(titles).lower().split()
    stop = {"the","a","an","and","or","for","with","in","of","to","is","by","on","at","from","&","-","--","/",""}
    wf = Counter(w.strip(".,()[]") for w in words if w.strip(".,()[]") not in stop and len(w.strip(".,()[]")) > 1)
    dup = titles[titles.duplicated(keep=False) & (titles.str.strip() != "")]
    return {
        "avg_len": round(lengths.mean()), "lengths": lengths,
        "components": components, "top_words": wf.most_common(25),
        "dup_count": dup.nunique(), "dup_total": len(dup),
        "short_count": int((lengths < 40).sum()),
        "long_count": int((lengths > 150).sum()),
        "optimal_count": int(((lengths >= 60) & (lengths <= 150)).sum()),
    }


@st.cache_data(show_spinner=False)
def analyze_descriptions(_h, df):
    col = find_col(df, "description")
    if col is None: return None
    descs = df[col].astype(str)
    lengths = descs.str.len()
    tc = find_col(df, "title")
    same = (df[tc].astype(str).str.strip() == descs.str.strip()).sum() if tc else 0
    dup = descs[descs.duplicated(keep=False) & (descs.str.strip() != "")].nunique()
    return {"avg_len": round(lengths.mean()), "lengths": lengths,
            "same_as_title": int(same), "dup_count": dup}


# ═════════════════════════════════════════════════════════════════════════════
# 8. NARRATIVE & RECOMMENDATIONS ENGINE
# ═════════════════════════════════════════════════════════════════════════════

def build_narrative(overall_pct, overall_grade, cat_data, results, gmc_issues, title_data, field_statuses):
    """Build a story-driven narrative: score > why > what's dragging it down > what to fix."""
    parts = []

    # Opening
    gc = SCORE_COLORS[overall_grade]
    if overall_pct >= 90:
        parts.append(f'Your feed scored <span class="good">{overall_pct:.0f}%</span> — <span class="good">Excellent</span>. This is a strong, well-optimised feed ready for competitive Shopping performance.')
    elif overall_pct >= 70:
        parts.append(f'Your feed scored <span class="highlight">{overall_pct:.0f}%</span> — <span class="highlight">Good</span>. There\'s a solid foundation here, but targeted improvements could unlock significantly more impressions and clicks.')
    elif overall_pct >= 50:
        parts.append(f'Your feed scored <span class="warn">{overall_pct:.0f}%</span> — <span class="warn">Average</span>. There are meaningful gaps that are likely costing you impression share, click-through rate, and revenue.')
    else:
        parts.append(f'Your feed scored <span class="bad">{overall_pct:.0f}%</span> — this feed needs significant work before it can compete effectively in Google Shopping.')

    # Category breakdown — find weakest
    sorted_cats = sorted(cat_data.items(), key=lambda x: x[1]["pct"])
    weakest = sorted_cats[0]
    strongest = sorted_cats[-1]
    if len(sorted_cats) > 1 and weakest[1]["pct"] < strongest[1]["pct"] - 10:
        parts.append(f'<br><br>The weakest area is <strong>{weakest[0]}</strong> at <span class="warn">{weakest[1]["pct"]:.0f}%</span>, '
                     f'while <strong>{strongest[0]}</strong> is performing best at <span class="good">{strongest[1]["pct"]:.0f}%</span>.')

    # What's dragging it down
    failing = [r for r in results if r["Score"] in ("Insufficient", "Below Average") and r["Weighting"] == "Must have"]
    if failing:
        names = ", ".join(f'<strong>{r["Attribute"]}</strong>' for r in failing[:4])
        parts.append(f'<br><br>The biggest drag on your score comes from required attributes with low fill: {names}. '
                     f'These directly impact Merchant Center eligibility and impression volume.')

    # GMC summary
    errors = sum(1 for i in gmc_issues if i["severity"] == "error")
    if errors > 0:
        parts.append(f'<br><br>Google Merchant Center validation found <span class="bad">{errors} error{"s" if errors != 1 else ""}</span> '
                     f'that would cause product disapprovals if submitted as-is.')
    else:
        pass_count = sum(1 for f in field_statuses if f["status"] == "pass")
        parts.append(f'<br><br>Good news: <span class="good">{pass_count} of {len(field_statuses)} GMC fields</span> are passing validation. '
                     f'No critical errors detected.')

    # Title insight
    if title_data:
        if title_data["avg_len"] < 80:
            parts.append(f'<br><br>Title quality is a key concern — average length is only <span class="warn">{title_data["avg_len"]} characters</span>. '
                         f'Google recommends 60-150 characters with brand, product type, color, and size for maximum query matching. '
                         f'Well-optimised titles can improve impressions by up to 200%.')
        elif title_data["avg_len"] >= 80:
            parts.append(f'<br><br>Title length averages <span class="good">{title_data["avg_len"]} characters</span> — within the optimal range.')
        missing_comps = [k for k, v in title_data.get("components", {}).items() if v < 0.3]
        if missing_comps:
            parts.append(f' However, titles are frequently missing <span class="warn">{", ".join(missing_comps).lower()}</span> — adding these would improve relevance matching.')

    return " ".join(parts)


def generate_recommendations(results, gmc_issues, title_data, desc_data, field_statuses, df):
    recs = []

    # GMC errors
    for e in [i for i in gmc_issues if i["severity"] == "error"][:3]:
        recs.append(("high", e["message"],
                     "Fix before uploading to Merchant Center — this will cause disapprovals."))

    # Missing GTINs
    gtin_issue = next((i for i in gmc_issues if "gtin" in i["field"].lower() and "missing" in i["message"].lower()), None)
    if gtin_issue:
        recs.append(("high", f"{gtin_issue['count']:,} branded products missing GTIN",
                      "Products with valid GTINs get up to 40% more clicks. Aim for 90%+ GTIN coverage."))

    # Title
    if title_data:
        if title_data["avg_len"] < 80:
            recs.append(("high", f"Average title length is only {title_data['avg_len']} characters",
                          "Use the formula: Brand + Product Type + Key Attribute (Color/Size/Material). Target 60-150 characters. Consider using Feed Rules in Merchant Center to auto-construct titles from attributes."))
        if title_data["dup_count"] > 0:
            recs.append(("medium", f"{title_data['dup_count']:,} duplicate titles across {title_data['dup_total']:,} products",
                          "Duplicate titles cause your products to compete against each other. Add differentiating attributes (color, size) to each variant title."))
        for comp, rate in title_data.get("components", {}).items():
            if rate < 0.4:
                recs.append(("medium", f"Only {rate:.0%} of titles contain {comp.lower()}",
                              f"Adding {comp.lower()} to titles improves query matching. Use a supplemental feed or Feed Rules to append it at scale."))

    # Description
    if desc_data:
        if desc_data["avg_len"] < 200:
            recs.append(("medium", f"Average description is only {desc_data['avg_len']} characters",
                          "Target 500-1,000 characters. Include features, specs, material, dimensions, and use cases. Rich descriptions improve free listing visibility."))
        if desc_data["same_as_title"] > 0:
            recs.append(("medium", f"{desc_data['same_as_title']:,} descriptions identical to title",
                          "Descriptions should expand on the title with unique selling points and secondary keywords."))

    # Required attributes
    for r in results:
        if not r["Found"] and r["Weighting"] == "Must have":
            recs.append(("high", f"Required attribute '{r['Attribute']}' not found",
                          "Missing required attributes cause disapprovals. Use a supplemental feed to add this data."))
        elif r["Found"] and r["Fill Rate"] < 0.5 and r["Weighting"] == "Must have":
            recs.append(("high", f"'{r['Attribute']}' has only {r['Fill Rate']:.0%} fill rate",
                          "Low fill on required fields means those products cannot serve in Shopping."))
        elif not r["Found"] and r["Weighting"] == "Good to have":
            recs.append(("low", f"Recommended attribute '{r['Attribute']}' not in feed",
                          "Adding this improves product matching, filter eligibility, and AI bidding signals."))

    # Custom labels
    cl = next((r for r in results if r["Attribute"] == "Custom Labels"), None)
    if cl and cl["Fill Rate"] < 0.6:
        recs.append(("low", f"Only {cl['Fill Rate']:.0%} of custom label slots used",
                      "Use custom labels for campaign segmentation: margin tiers, seasonality, best-sellers, price buckets, new arrivals."))

    # Dedupe
    seen = set()
    unique = []
    for r in recs:
        key = r[1][:55]
        if key not in seen: seen.add(key); unique.append(r)
    unique.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x[0], 3))
    return unique


def _ai_commentary(overall_pct, cat_data, results, recs, title_data, gmc_issues):
    """Generate AI commentary via Bifrost (Pattern's AI gateway) using OpenAI-compatible API."""
    try:
        bifrost = st.secrets.get("bifrost", {})
        api_key = bifrost.get("api_key", "")
        base_url = bifrost.get("base_url", "")
        model = bifrost.get("model", "anthropic/claude-sonnet-4-20250514")
        if not api_key or not base_url:
            return None
        from openai import OpenAI
        client = OpenAI(base_url=base_url, api_key=api_key)

        cat_summary = "; ".join(f"{k}: {v['pct']:.0f}%" for k, v in cat_data.items())
        top_issues = "; ".join(r[1] for r in recs[:5])
        gmc_errors = sum(1 for i in gmc_issues if i["severity"] == "error")
        title_len = title_data["avg_len"] if title_data else "N/A"

        prompt = f"""You are a Google Shopping feed optimisation expert at a digital agency called Pattern.
Write a concise, client-friendly executive summary (3-4 short paragraphs) for a feed audit report.

Feed stats:
- Overall score: {overall_pct:.0f}%
- Category scores: {cat_summary}
- GMC errors: {gmc_errors}
- Average title length: {title_len} chars
- Top issues: {top_issues}
- Total attributes audited: {len(results)}

Tone: professional, direct, optimistic but honest. Focus on business impact (impressions, clicks, revenue).
Do NOT use markdown headers or bullet points — write flowing paragraphs.
Keep it under 200 words. Use specific numbers from the data above."""

        response = client.chat.completions.create(
            model=model,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception:
        return None


# ═════════════════════════════════════════════════════════════════════════════
# 9. REPORT GENERATION
# ═════════════════════════════════════════════════════════════════════════════

def generate_excel_report(results, gmc_issues, recs, df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame([{
            "Category": r["Category"], "Attribute": r["Attribute"],
            "Weighting": r["Weighting"], "Found": "Yes" if r["Found"] else "No",
            "Fill Rate": f"{r['Fill Rate']:.0%}", "Score": r["Score"],
            "Weighted Score": f"{r['Weighted']} / {r['Potential']}",
        } for r in results]).to_excel(writer, sheet_name="Audit Scores", index=False)
        if gmc_issues:
            pd.DataFrame(gmc_issues).to_excel(writer, sheet_name="GMC Issues", index=False)
        if recs:
            pd.DataFrame([{"Priority": r[0].upper(), "Issue": r[1], "Action": r[2]} for r in recs]).to_excel(writer, sheet_name="Recommendations", index=False)
        df.head(500).to_excel(writer, sheet_name="Feed Sample", index=False)
    return output.getvalue()


# ═════════════════════════════════════════════════════════════════════════════
# 10. CHARTS
# ═════════════════════════════════════════════════════════════════════════════

CL = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
          font=dict(family="Wix Madefor Display, Source Sans Pro, sans-serif", color="#888"))


def chart_radar(cat_data):
    names = list(cat_data.keys())
    vals = [v["pct"] for v in cat_data.values()]
    # Dramatic: fill the full area with vibrant gradient
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=names + [names[0]],
        fill="toself", fillcolor="rgba(0,155,255,0.12)",
        line=dict(color=BLUE, width=3), marker=dict(size=9, color=BLUE, symbol="circle"),
        hovertemplate="%{theta}<br><b>%{r:.0f}%</b><extra></extra>",
    ))
    # Add a "100%" reference ring
    fig.add_trace(go.Scatterpolar(
        r=[100] * (len(names) + 1), theta=names + [names[0]],
        fill=None, line=dict(color="rgba(255,255,255,0.08)", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False,
    ))
    fig.update_layout(
        **CL, showlegend=False,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.04)",
                            tickfont=dict(size=10, color="#444"), tickvals=[25, 50, 75, 100]),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)",
                             tickfont=dict(size=13, color=LIGHT)),
        ),
        margin=dict(l=80, r=80, t=40, b=40), height=420,
    )
    return fig


def chart_histogram(series, title="", target=None, target_label=""):
    fig = go.Figure(go.Histogram(
        x=series, nbinsx=40,
        marker=dict(color=BLUE, line=dict(width=0)),
        hovertemplate="%{x}: %{y} products<extra></extra>",
    ))
    if target:
        fig.add_vline(x=target, line_dash="dash", line_color=SEA, line_width=2,
                      annotation_text=target_label, annotation_font_color=SEA, annotation_font_size=11)
    fig.update_layout(**CL, xaxis=dict(title_text=title, gridcolor="rgba(255,255,255,0.03)"),
                      yaxis=dict(title_text="Products", gridcolor="rgba(255,255,255,0.03)"),
                      margin=dict(l=50, r=20, t=20, b=40), height=260, bargap=0.05)
    return fig


# ═════════════════════════════════════════════════════════════════════════════
# 11. MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

_inject_css()

# Header
st.markdown(
    f'<div style="display:flex;align-items:center;margin-bottom:0.4rem;animation:fadeIn 0.5s ease both;">'
    f'<div>{LOGO_SVG}</div></div>',
    unsafe_allow_html=True)
st.markdown('<h1 style="margin:0 0 0.15rem;animation:fadeInUp 0.5s ease 0.1s both;">Product Feed Audit</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#555;margin-bottom:1.2rem;animation:fadeInUp 0.5s ease 0.15s both;">Upload a product feed for a comprehensive quality assessment and optimisation roadmap.</p>', unsafe_allow_html=True)

# Upload
uploaded = st.file_uploader("Upload your product feed", type=["csv","tsv","xlsx","xls","txt"],
                            help="CSV, TSV, or Excel with headers in first row.", label_visibility="collapsed")

if uploaded is None:
    st.markdown(
        f'<div class="upload-hero">'
        f'<div class="icon">&#x2B06;</div>'
        f'<h2>Drop your product feed above</h2>'
        f'<p>Get a full quality score, GMC readiness check, title optimisation analysis, and an actionable improvement roadmap.</p>'
        f'<div class="upload-tags"><span>CSV</span><span>TSV</span><span>XLSX</span><span>XLS</span><span>TXT</span></div>'
        f'</div>', unsafe_allow_html=True)
    st.stop()

# Parse
try:
    name = uploaded.name.lower()
    if name.endswith((".csv",".txt")):
        raw = uploaded.read(); uploaded.seek(0)
        sep = "\t" if "\t" in raw[:4096].decode("utf-8", errors="replace") else ","
        df = pd.read_csv(BytesIO(raw), sep=sep, dtype=str, on_bad_lines="skip")
    elif name.endswith(".tsv"):
        df = pd.read_csv(uploaded, sep="\t", dtype=str, on_bad_lines="skip")
    else:
        df = pd.read_excel(uploaded, dtype=str)
except Exception as e:
    st.error(f"Could not read file: {e}"); st.stop()

df.columns = df.columns.str.strip()
df_hash = hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()

# Run analyses
with st.spinner("Analysing your feed..."):
    results = run_audit(df_hash, df)
    gmc_issues = run_gmc_validation(df_hash, df)
    field_statuses = gmc_field_status(df_hash, df)
    title_data = analyze_titles(df_hash, df)
    desc_data = analyze_descriptions(df_hash, df)
    recs = generate_recommendations(results, gmc_issues, title_data, desc_data, field_statuses, df)

total_w = sum(r["Weighted"] for r in results)
total_p = sum(r["Potential"] for r in results)
overall_pct = total_w / max(total_p, 1) * 100
overall_grade = "Excellent" if overall_pct >= 90 else "Good" if overall_pct >= 70 else "Average" if overall_pct >= 50 else "Below Average" if overall_pct > 30 else "Insufficient"
errors_count = sum(1 for i in gmc_issues if i["severity"] == "error")
warnings_count = sum(1 for i in gmc_issues if i["severity"] == "warning")

cat_data = {}
for r in results:
    cat_data.setdefault(r["Category"], {"w": 0, "p": 0})
    cat_data[r["Category"]]["w"] += r["Weighted"]
    cat_data[r["Category"]]["p"] += r["Potential"]
for k in cat_data:
    cat_data[k]["pct"] = cat_data[k]["w"] / max(cat_data[k]["p"], 1) * 100
    cat_data[k]["grade"] = "Excellent" if cat_data[k]["pct"] >= 90 else "Good" if cat_data[k]["pct"] >= 70 else "Average" if cat_data[k]["pct"] >= 50 else "Below Average" if cat_data[k]["pct"] > 30 else "Insufficient"

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("---")
h1, h2, h3, h4 = st.columns([1.3, 1, 1, 1])
with h1:
    gc = SCORE_COLORS[overall_grade]
    st.markdown(
        f'<div class="ring-wrap">'
        f'{svg_ring(overall_pct, size=160, stroke=10, color=gc)}'
        f'<div class="ring-label">Overall Score</div>'
        f'<div class="ring-grade" style="color:{gc};">{overall_grade}</div>'
        f'</div>', unsafe_allow_html=True)
with h2:
    st.metric("Products", f"{len(df):,}")
with h3:
    st.metric("Attributes", f"{sum(1 for r in results if r['Found'])} / {len(results)}")
with h4:
    gmc_label = f"{errors_count} error{'s' if errors_count != 1 else ''}" if errors_count else "All clear"
    st.metric("GMC Status", gmc_label, delta=f"{warnings_count} warnings" if warnings_count else None, delta_color="off")

# ── NARRATIVE ─────────────────────────────────────────────────────────
narrative = build_narrative(overall_pct, overall_grade, cat_data, results, gmc_issues, title_data, field_statuses)

# Try AI commentary
ai_text = _ai_commentary(overall_pct, cat_data, results, recs, title_data, gmc_issues)
if ai_text:
    st.markdown(f'<div class="narrative">{ai_text}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="narrative">{narrative}</div>', unsafe_allow_html=True)

# Download
report_bytes = generate_excel_report(results, gmc_issues, recs, df)
st.download_button("Download Full Report (.xlsx)", data=report_bytes, file_name="feed_audit_report.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SCORING GUIDE
# ═════════════════════════════════════════════════════════════════════════════
with st.expander("How does scoring work?"):
    st.markdown(f"""
<div style="font-size:0.88rem;line-height:1.7;color:#bbb;">

<strong style="color:{LIGHT};">What this audit measures</strong><br>
We analyse <strong>20 product feed attributes</strong> across three categories that determine your Google Shopping performance:

<div style="display:flex;gap:2rem;margin:0.8rem 0;flex-wrap:wrap;">
<div><span style="color:{BLUE};font-weight:700;">Customer-Facing</span><br><span style="color:#666;font-size:0.8rem;">Brand, color, size, material, gender, price, condition</span></div>
<div><span style="color:{VIOLET};font-weight:700;">Internal Attributes</span><br><span style="color:#666;font-size:0.8rem;">Product ID, link, GTIN, custom labels, availability, images</span></div>
<div><span style="color:{SEA};font-weight:700;">Key Shopping Content</span><br><span style="color:#666;font-size:0.8rem;">Title, description, image URL</span></div>
</div>

<strong style="color:{LIGHT};">How scores are calculated</strong><br>
Each attribute gets a <strong>fill rate</strong> (what % of products have this data), which maps to a grade:

<div style="display:flex;gap:12px;margin:0.6rem 0;flex-wrap:wrap;">
<span class="badge badge-excellent">100% = Excellent</span>
<span class="badge badge-good">80%+ = Good</span>
<span class="badge badge-average">50%+ = Average</span>
<span class="badge badge-below-average">20%+ = Below Average</span>
<span class="badge badge-insufficient">&lt;20% = Insufficient</span>
</div>

Grades are then <strong>weighted by importance</strong>: "Must have" attributes (like title, price, GTIN) count <strong>3x</strong> more than "Bonus" attributes. The overall score is the weighted average across all 20 attributes.

<br><strong style="color:{LIGHT};">What does a good score look like?</strong><br>
<span style="color:{SEA};font-weight:600;">90%+</span> — Excellent. Competitive feed ready for Performance Max.<br>
<span style="color:{BLUE};font-weight:600;">70–89%</span> — Good foundation. Targeted fixes can significantly improve impressions.<br>
<span style="color:{AMBER};font-weight:600;">50–69%</span> — Average. Missing attributes are costing you impression share and clicks.<br>
<span style="color:{RED};font-weight:600;">Below 50%</span> — Needs significant work. Likely losing to competitors with richer feeds.

<br><strong style="color:{LIGHT};">Why does this matter?</strong><br>
Google's AI systems (including Performance Max) use your product data to decide <em>which products to show, to whom, and at what bid</em>. Incomplete feeds are penalised with fewer impressions regardless of how competitive your bids are. Products with valid GTINs alone get up to <strong>40% more clicks</strong>.
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tabs = st.tabs(["Overview", "GMC Readiness", "Title & Content", "Recommendations", "Feed Data"])

# ──────────────────────────────────────────────────────────────────────
# TAB 1: OVERVIEW
# ──────────────────────────────────────────────────────────────────────
with tabs[0]:
    # Category cards + radar
    st.markdown('<div class="sh">Category Breakdown</div>', unsafe_allow_html=True)
    col_r, col_c = st.columns([3, 2])
    with col_r:
        st.plotly_chart(chart_radar(cat_data), use_container_width=True)
    with col_c:
        for idx, (cat, d) in enumerate(cat_data.items()):
            color = SCORE_COLORS[d["grade"]]
            st.markdown(
                f'<div class="glass" style="animation-delay:{idx*0.1}s;margin-bottom:0.6rem;">'
                f'<div style="display:flex;align-items:center;justify-content:space-between;">'
                f'<div style="font-size:0.88rem;font-weight:600;">{cat}</div>'
                f'<div style="font-size:1.6rem;font-weight:800;color:{color};font-family:Wix Madefor Display,sans-serif;">{d["pct"]:.0f}%</div>'
                f'</div>'
                f'<div style="margin-top:0.5rem;background:rgba(255,255,255,0.05);border-radius:5px;height:6px;overflow:hidden;">'
                f'<div style="height:100%;width:{d["pct"]:.0f}%;background:{color};border-radius:5px;animation:barGrow 0.8s cubic-bezier(0.4,0,0.2,1) both;animation-delay:{0.3+idx*0.15}s;"></div>'
                f'</div>'
                f'<div style="margin-top:0.4rem;text-align:right;">{badge(d["grade"])}</div>'
                f'</div>', unsafe_allow_html=True)

    # Attribute fill rates
    st.markdown('<div class="sh">Attribute Coverage</div>', unsafe_allow_html=True)
    fill_html = ""
    for idx, r in enumerate(sorted(results, key=lambda x: -x["Fill Rate"])):
        rate = r["Fill Rate"]; color = _color(rate)
        tag = '<span style="font-size:0.58rem;background:rgba(255,82,82,0.1);color:#FF5252;padding:1px 6px;border-radius:8px;margin-left:5px;font-weight:600;">REQUIRED</span>' if r["Weighting"] == "Must have" else ""
        fill_html += (
            f'<div class="fb-row">'
            f'<div class="fb-name">{r["Attribute"]}{tag}</div>'
            f'<div class="fb-track"><div class="fb-bar" style="width:{rate*100:.0f}%;background:{color};"></div></div>'
            f'<div class="fb-pct" style="color:{color};">{rate:.0%}</div>'
            f'<div class="fb-tag">{badge(r["Score"])}</div>'
            f'</div>')
    st.markdown(fill_html, unsafe_allow_html=True)

    with st.expander("View detailed score table"):
        st.dataframe(pd.DataFrame([{
            "Category": r["Category"], "Attribute": r["Attribute"], "Weighting": r["Weighting"],
            "Found": "Yes" if r["Found"] else "No", "Fill Rate": f"{r['Fill Rate']:.0%}",
            "Score": r["Score"], "Weighted": f"{r['Weighted']}/{r['Potential']}",
        } for r in results]), use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────
# TAB 2: GMC READINESS
# ──────────────────────────────────────────────────────────────────────
with tabs[1]:
    pass_count = sum(1 for f in field_statuses if f["status"] == "pass")
    warn_count = sum(1 for f in field_statuses if f["status"] == "warn")
    fail_count = sum(1 for f in field_statuses if f["status"] == "fail")
    readiness_pct = pass_count / max(len(field_statuses), 1) * 100

    if errors_count == 0 and fail_count == 0:
        readiness_label = "Ready"
        readiness_color = SEA
    elif errors_count <= 2 and fail_count <= 1:
        readiness_label = "Almost Ready"
        readiness_color = AMBER
    else:
        readiness_label = "Needs Work"
        readiness_color = RED

    # Top row
    g1, g2, g3 = st.columns([1.4, 1, 1])
    with g1:
        st.markdown(
            f'<div class="glass" style="text-align:center;padding:1.5rem;">'
            f'{svg_ring(readiness_pct, size=160, stroke=10, color=readiness_color)}'
            f'<div style="font-size:1.5rem;font-weight:800;color:{readiness_color};margin-top:0.5rem;font-family:Wix Madefor Display,sans-serif;">{readiness_label}</div>'
            f'<div style="font-size:0.75rem;color:#555;margin-top:0.2rem;">GMC Readiness</div>'
            f'</div>', unsafe_allow_html=True)
    with g2:
        st.metric("Errors", errors_count)
        st.metric("Warnings", warnings_count)
    with g3:
        st.metric("Fields Passing", f"{pass_count} / {len(field_statuses)}")
        st.metric("Products", f"{len(df):,}")

    st.markdown("")

    # Field checklist — two columns
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown('<div class="sh">Required Fields</div>', unsafe_allow_html=True)
        html = ""
        for f in [f for f in field_statuses if f["required"]]:
            icon = {"pass": "&#x2713;", "fail": "&#x2717;", "warn": "&#x25CB;"}.get(f["status"], "?")
            html += (f'<div class="gmc-row"><div class="gmc-dot {f["status"]}">{icon}</div>'
                     f'<div class="gmc-name">{f["name"]}</div>'
                     f'<div class="gmc-detail">{f["detail"]}</div></div>')
        st.markdown(html, unsafe_allow_html=True)
    with fc2:
        st.markdown('<div class="sh">Recommended Fields</div>', unsafe_allow_html=True)
        html = ""
        for f in [f for f in field_statuses if not f["required"]]:
            icon = {"pass": "&#x2713;", "fail": "&#x2717;", "warn": "&#x25CB;"}.get(f["status"], "?")
            html += (f'<div class="gmc-row"><div class="gmc-dot {f["status"]}">{icon}</div>'
                     f'<div class="gmc-name">{f["name"]}</div>'
                     f'<div class="gmc-detail">{f["detail"]}</div></div>')
        st.markdown(html, unsafe_allow_html=True)

    # Issues
    if gmc_issues:
        st.markdown('<div class="sh">Issues Found</div>', unsafe_allow_html=True)
        for issue in gmc_issues:
            sev = issue["severity"]
            icon = "&#x26D4;" if sev == "error" else "&#x26A0;"
            st.markdown(
                f'<div class="issue">'
                f'<div style="font-size:1rem;margin-top:1px;">{icon}</div>'
                f'<div style="flex:1;">'
                f'<div style="color:{LIGHT};font-weight:500;font-size:0.88rem;">{issue["message"]}</div>'
                f'<div style="color:#444;font-size:0.75rem;margin-top:0.15rem;">Field: {issue["field"]}</div>'
                f'</div>'
                f'<div class="issue-count {sev}">{issue["count"]:,} products</div>'
                f'</div>', unsafe_allow_html=True)
    elif not gmc_issues:
        st.markdown(
            f'<div style="text-align:center;padding:2rem;animation:fadeInUp 0.5s ease both;">'
            f'<div style="font-size:2.5rem;margin-bottom:0.4rem;">&#x2705;</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:{SEA};">No issues detected</div>'
            f'<div style="color:#555;font-size:0.82rem;margin-top:0.2rem;">Your feed is ready for Google Merchant Center</div>'
            f'</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# TAB 3: TITLE & CONTENT
# ──────────────────────────────────────────────────────────────────────
with tabs[2]:
    if title_data:
        st.markdown('<div class="sh">Title Analysis</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#555;font-size:0.82rem;margin-bottom:0.8rem;">Titles are the single most impactful attribute — they determine which queries trigger your products and where you rank.</p>', unsafe_allow_html=True)

        tc1, tc2, tc3, tc4 = st.columns(4)
        with tc1: st.metric("Avg Length", f"{title_data['avg_len']} chars")
        with tc2: st.metric("In Optimal Range", f"{title_data['optimal_count']:,}")
        with tc3: st.metric("Too Short (<40)", f"{title_data['short_count']:,}")
        with tc4: st.metric("Duplicates", f"{title_data['dup_count']:,}")

        st.plotly_chart(chart_histogram(title_data["lengths"], "Title Length (characters)", target=80, target_label="Min target"), use_container_width=True)

        if title_data["components"]:
            st.markdown('<div class="sh">Title Component Presence</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#555;font-size:0.82rem;margin-bottom:0.6rem;">Best practice formula: <strong style="color:{LIGHT};">Brand + Product Type + Color + Size + Material</strong></p>', unsafe_allow_html=True)
            html = ""
            for comp, rate in sorted(title_data["components"].items(), key=lambda x: -x[1]):
                c = _color(rate)
                html += (
                    f'<div class="fb-row">'
                    f'<div class="fb-name">{comp}</div>'
                    f'<div class="fb-track"><div class="fb-bar" style="width:{rate*100:.0f}%;background:{c};"></div></div>'
                    f'<div class="fb-pct" style="color:{c};">{rate:.0%}</div>'
                    f'</div>')
            st.markdown(html, unsafe_allow_html=True)

        if title_data["top_words"]:
            with st.expander("Most frequent title words"):
                words, counts = zip(*title_data["top_words"][:20])
                fig = go.Figure(go.Bar(x=list(counts), y=list(words), orientation="h",
                                       marker=dict(color=VIOLET, line=dict(width=0)),
                                       text=list(counts), textposition="outside",
                                       textfont=dict(color=LIGHT, size=9)))
                fig.update_layout(**CL, yaxis=dict(autorange="reversed", tickfont=dict(color=LIGHT, size=10)),
                                  xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
                                  margin=dict(l=120, r=50, t=10, b=20), height=max(280, len(words)*22))
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No title column detected in feed.")

    if desc_data:
        st.markdown('<div class="sh">Description Analysis</div>', unsafe_allow_html=True)
        dc1, dc2, dc3 = st.columns(3)
        with dc1: st.metric("Avg Length", f"{desc_data['avg_len']} chars")
        with dc2: st.metric("Same as Title", f"{desc_data['same_as_title']:,}")
        with dc3: st.metric("Duplicates", f"{desc_data['dup_count']:,}")
        st.plotly_chart(chart_histogram(desc_data["lengths"], "Description Length (characters)", target=500, target_label="Min target"), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────
# TAB 4: RECOMMENDATIONS
# ──────────────────────────────────────────────────────────────────────
with tabs[3]:
    if not recs:
        st.markdown(
            f'<div style="text-align:center;padding:3rem;animation:fadeInUp 0.5s ease both;">'
            f'<div style="font-size:2.5rem;margin-bottom:0.4rem;">&#x2705;</div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:{SEA};">No issues found — your feed looks great!</div>'
            f'</div>', unsafe_allow_html=True)
    else:
        high = sum(1 for r in recs if r[0] == "high")
        med = sum(1 for r in recs if r[0] == "medium")
        low = sum(1 for r in recs if r[0] == "low")
        st.markdown(
            f'<div style="display:flex;gap:1.5rem;margin-bottom:1rem;animation:fadeIn 0.4s ease both;">'
            f'<span style="color:{RED};font-weight:700;font-size:0.82rem;">&#x25CF; {high} High</span>'
            f'<span style="color:{AMBER};font-weight:700;font-size:0.82rem;">&#x25CF; {med} Medium</span>'
            f'<span style="color:{SEA};font-weight:700;font-size:0.82rem;">&#x25CF; {low} Low</span>'
            f'</div>', unsafe_allow_html=True)

        for priority, message, action in recs:
            icon = "&#x26D4;" if priority == "high" else "&#x26A0;" if priority == "medium" else "&#x1F4A1;"
            st.markdown(
                f'<div class="rec {priority}">'
                f'<div class="rec-tag {priority}">{icon} {priority} impact</div>'
                f'<div style="color:{LIGHT};font-weight:600;font-size:0.9rem;margin-bottom:0.25rem;">{message}</div>'
                f'<div style="color:#666;font-size:0.8rem;line-height:1.5;">{action}</div>'
                f'</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# TAB 5: FEED DATA
# ──────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown(f'<div class="sh">Feed Preview</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#555;font-size:0.82rem;margin-bottom:0.5rem;">Showing {min(len(df),200):,} of {len(df):,} rows</p>', unsafe_allow_html=True)
    st.dataframe(df.head(200), use_container_width=True, height=500)
    with st.expander(f"Detected Columns ({len(df.columns)})"):
        st.markdown(" ".join(
            f'<span style="display:inline-block;padding:3px 10px;margin:3px;border-radius:8px;'
            f'background:rgba(0,155,255,0.06);color:{BLUE};font-size:0.76rem;font-weight:500;">{c}</span>'
            for c in df.columns), unsafe_allow_html=True)
