import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
from io import BytesIO

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pattern — Feed Audit Tool",
    page_icon="https://cdn.prod.website-files.com/64fdbed8246bf837f498e3f0/6568ba5b9c2ae21778952712_Favicon%2032x32.png",
    layout="wide",
)

# ─── Pattern branding CSS ─────────────────────────────────────────────────────
PATTERN_BLUE = "#009BFF"
PATTERN_PURPLE = "#770BFF"
GRADIENT = f"linear-gradient(135deg, {PATTERN_PURPLE}, {PATTERN_BLUE})"

PATTERN_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 675 135.7" width="180" height="36">
  <path fill="#009BFF" d="M44.5,0L0,135.7h47.3L91.8,0H44.5z"/>
  <path fill="#009BFF" d="M89.1,0L44.5,135.7h47.3L136.3,0H89.1z"/>
  <path fill="#F2F2F2" d="M194.5,33.9c-9.7,0-18,3.4-24.4,10v-8.3h-22.6v101.1h23.5V96.3c6.3,6.1,14.3,9.3,23.5,9.3c20.1,0,36.4-16.5,36.4-35.9S214.6,33.9,194.5,33.9z M191.2,84.6c-10.3,0-18.7-7.6-18.7-15c0-7.5,8.4-14.6,18.7-14.6c10.3,0,18.7,7.2,18.7,14.6C209.9,77,201.5,84.6,191.2,84.6z"/>
  <path fill="#F2F2F2" d="M284.3,35.5v8.3c-6.4-6.6-14.7-10-24.4-10c-20.1,0-36.4,16.5-36.4,35.9s16.3,35.9,36.4,35.9c9.2,0,17.1-3.2,23.5-9.3v7.6h23.5V35.5H284.3z M263.2,84.6c-10.3,0-18.7-7.6-18.7-15c0-7.5,8.4-14.6,18.7-14.6c10.3,0,18.7,7.2,18.7,14.6C281.9,77,273.5,84.6,263.2,84.6z"/>
  <path fill="#F2F2F2" d="M345.3,12.7v22.8h-16.6v20h16.6v48.4h23.5V55.5h16.6v-20h-16.6V12.7H345.3z"/>
  <path fill="#F2F2F2" d="M423.8,12.7v22.8h-16.6v20h16.6v48.4h23.5V55.5h16.6v-20h-16.6V12.7H423.8z"/>
  <path fill="#F2F2F2" d="M522.4,34c-21.3,0-38.7,16.1-38.7,35.8s17.4,35.8,38.7,35.8c14,0,25.7-6.7,32.5-17.2l-18.7-10.8c-2.9,4.6-7.7,7.2-13.5,7.2c-7.2,0-13.3-3.8-15.8-9.8h52.8c0.5-2.6,0.8-5.3,0.8-5.3C560.5,49.8,543.7,34,522.4,34z M507.6,62.1c2.5-5.5,8.3-8.9,14.8-8.9c6.5,0,12.3,3.4,14.8,8.9H507.6z"/>
  <path fill="#F2F2F2" d="M604.2,33.9c-8,0-15.5,3.4-19.9,9.3v-7.6h-22.6v68.3h23.5V69.3c0-8.2,6.2-14.4,14.3-14.4c8.1,0,13.6,5.6,13.6,13.3v35.7H636.6V64.5C636.6,47.3,622.6,33.9,604.2,33.9z"/>
</svg>
"""

st.markdown(f"""
<style>
    /* ── Design tokens from Pattern Streamlit apps ── */

    /* Body / App background — matches design-tokens.json */
    .stApp {{
        background-color: #0E1117;
        font-family: "Source Sans Pro", sans-serif;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #262730;
    }}

    /* Text defaults */
    .stApp, .stApp p, .stApp span, .stApp label {{
        color: #FAFAFA;
    }}

    /* Pattern gradient button */
    .stButton > button {{
        background: {GRADIENT};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        padding: 0.6rem 2rem;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: {GRADIENT};
        opacity: 0.9;
        color: white;
        border: none;
    }}
    .stButton > button:active, .stButton > button:focus {{
        background: {GRADIENT};
        color: white;
        border: none;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        border: 2px dashed #262730;
        border-radius: 12px;
        padding: 1rem;
    }}

    /* Metric cards */
    [data-testid="stMetric"] {{
        background-color: rgba(38, 39, 48, 0.5);
        border: 1px solid #262730;
        border-radius: 12px;
        padding: 1rem;
    }}

    /* Section headers with left accent — matches Agency Scorecard style */
    .section-header {{
        border-left: 4px solid {PATTERN_BLUE};
        padding-left: 12px;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #FAFAFA;
    }}

    /* Score badge */
    .score-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }}
    .score-excellent {{ background-color: rgba(0, 200, 83, 0.2); color: #00C853; }}
    .score-good {{ background-color: rgba(0, 155, 255, 0.2); color: #009BFF; }}
    .score-average {{ background-color: rgba(255, 193, 7, 0.2); color: #FFC107; }}
    .score-below {{ background-color: rgba(255, 152, 0, 0.2); color: #FF9800; }}
    .score-insufficient {{ background-color: rgba(255, 82, 82, 0.2); color: #FF5252; }}

    /* Overall score ring */
    .overall-score {{
        text-align: center;
        padding: 2rem;
    }}
    .overall-score .number {{
        font-size: 4rem;
        font-weight: 800;
        background: {GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }}
    .overall-score .label {{
        font-size: 1rem;
        color: #888;
        margin-top: 0.5rem;
    }}

    /* Hide default streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Expander — border from tokens: rgb(250,250,250), radius 0px */
    [data-testid="stExpander"] {{
        border: 1px solid rgba(250, 250, 250, 0.15);
        border-radius: 0px;
    }}

    /* Tab styling — accent from tokens: #FF4B4B */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #FAFAFA;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: rgba(38, 39, 48, 0.5);
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {PATTERN_BLUE};
    }}

    /* Dataframe styling */
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Headings — from tokens */
    .stApp h1 {{
        font-size: 44px;
        font-weight: 700;
        line-height: 52.8px;
        color: #FAFAFA;
    }}
    .stApp h2 {{
        font-size: 36px;
        font-weight: 600;
        line-height: 43.2px;
        letter-spacing: -0.18px;
        color: #FAFAFA;
    }}
    .stApp h3 {{
        font-size: 28px;
        font-weight: 600;
        line-height: 33.6px;
        letter-spacing: -0.14px;
        color: #FAFAFA;
    }}
</style>
""", unsafe_allow_html=True)


# ─── Logo ──────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="text-align:center; margin-bottom: 0.5rem;">{PATTERN_LOGO_SVG}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 style="text-align:center; margin-top:0;">Product Feed Audit Tool</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="text-align:center; color:#888; margin-top:-0.5rem; margin-bottom:2rem;">'
    "Upload a product feed file to get an automated quality score with actionable insights"
    "</p>",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# SCORING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# Audit attribute definitions
# Each: (display_name, category, weighting, feed_column_search, special_logic)
AUDIT_ATTRIBUTES = [
    # Customer-Facing Attributes
    ("Size", "Customer-Facing Attributes", "Good to have", "size", "fill_rate"),
    ("Sale Price", "Customer-Facing Attributes", "Good to have", "sale price", "fill_rate"),
    ("Regular Price", "Customer-Facing Attributes", "Must have", "price", "fill_rate"),
    ("Product Condition", "Customer-Facing Attributes", "Good to have", "condition", "condition"),
    ("Material", "Customer-Facing Attributes", "Good to have", "material", "fill_rate"),
    ("Gender", "Customer-Facing Attributes", "Good to have", "gender", "fill_rate"),
    ("Color", "Customer-Facing Attributes", "Good to have", "color", "fill_rate"),
    ("Brand Name", "Customer-Facing Attributes", "Must have", "brand", "brand"),
    ("Age Group", "Customer-Facing Attributes", "Good to have", "age group", "fill_rate"),
    # Internal Attributes
    ("Product Type", "Internal Attributes", "Must have", "product type", "fill_rate"),
    ("Product Link", "Internal Attributes", "Must have", "link", "fill_rate"),
    ("Product ID", "Internal Attributes", "Must have", "id", "fill_rate"),
    ("Google Product Category", "Internal Attributes", "Good to have", "google product category", "fill_rate"),
    ("GTIN", "Internal Attributes", "Must have", "gtin", "fill_rate"),
    ("Custom Labels", "Internal Attributes", "Good to have", "custom label", "custom_label"),
    ("Availability", "Internal Attributes", "Good to have", "availability", "availability"),
    ("Additional Image Links", "Internal Attributes", "Good to have", "additional image link", "fill_rate"),
    # Key Shopping Content
    ("Product Title", "Key Shopping Content", "Must have", "title", "fill_rate"),
    ("Product Description", "Key Shopping Content", "Must have", "description", "fill_rate"),
    ("Image URL", "Key Shopping Content", "Must have", "image link", "fill_rate"),
]

WEIGHTING_MAP = {"Must have": 3, "Good to have": 2, "Bonus": 1}
SCORE_MAP = {"Excellent": 5, "Good": 4, "Average": 3, "Below Average": 2, "Insufficient": 1}
SCORE_COLORS = {
    "Excellent": "#00C853",
    "Good": "#009BFF",
    "Average": "#FFC107",
    "Below Average": "#FF9800",
    "Insufficient": "#FF5252",
}


def find_column(df: pd.DataFrame, search_term: str) -> str | None:
    """Find a column in the dataframe matching the search term (case-insensitive, partial match)."""
    cols_lower = {c.lower().strip(): c for c in df.columns}
    # Exact match first
    if search_term.lower() in cols_lower:
        return cols_lower[search_term.lower()]
    # Partial / contains match
    for col_lower, col_orig in cols_lower.items():
        if search_term.lower() in col_lower:
            return col_orig
    return None


def calc_fill_rate(df: pd.DataFrame, col_name: str) -> float:
    """Calculate fill rate: proportion of non-empty cells."""
    total = len(df)
    if total == 0:
        return 0.0
    filled = df[col_name].apply(
        lambda x: isinstance(x, str) and len(x.strip()) > 0 or (pd.notna(x) and not isinstance(x, str))
    ).sum()
    return filled / total


def fill_rate_to_score(rate: float) -> str:
    if rate >= 1.0:
        return "Excellent"
    if rate >= 0.8:
        return "Good"
    if rate >= 0.5:
        return "Average"
    if rate > 0.2:
        return "Below Average"
    return "Insufficient"


def calc_condition_rate(df: pd.DataFrame, col_name: str) -> float:
    """For condition: count cells with value 'new'."""
    total = len(df)
    if total == 0:
        return 0.0
    count = df[col_name].astype(str).str.lower().str.strip().eq("new").sum()
    return count / total


def calc_availability_rate(df: pd.DataFrame, col_name: str) -> float:
    """For availability: count cells with 'in stock'."""
    total = len(df)
    if total == 0:
        return 0.0
    count = df[col_name].astype(str).str.lower().str.strip().eq("in stock").sum()
    return count / total


def calc_custom_label_score(df: pd.DataFrame) -> float:
    """Check how many of custom_label_0 through custom_label_4 exist as columns."""
    found = 0
    for i in range(5):
        for c in df.columns:
            if f"custom label {i}" in c.lower() or f"custom_label_{i}" in c.lower():
                found += 1
                break
    return found / 5


def calc_brand_rate(df: pd.DataFrame, search_term: str) -> float:
    """Find brand column and calculate fill rate with partial matching."""
    col = find_column(df, search_term)
    if col is None:
        return 0.0
    return calc_fill_rate(df, col)


def run_audit(df: pd.DataFrame) -> list[dict]:
    """Run the full audit and return results for each attribute."""
    results = []
    total_products = len(df)

    for display_name, category, weighting, search_term, logic in AUDIT_ATTRIBUTES:
        col = find_column(df, search_term)
        found = col is not None
        fill_rate = 0.0
        score_label = "Insufficient"

        if found:
            if logic == "fill_rate":
                fill_rate = calc_fill_rate(df, col)
                score_label = fill_rate_to_score(fill_rate)
            elif logic == "condition":
                fill_rate = calc_condition_rate(df, col)
                score_label = fill_rate_to_score(fill_rate)
            elif logic == "availability":
                fill_rate = calc_availability_rate(df, col)
                score_label = fill_rate_to_score(fill_rate)
            elif logic == "brand":
                fill_rate = calc_brand_rate(df, search_term)
                score_label = fill_rate_to_score(fill_rate)
            elif logic == "custom_label":
                fill_rate = calc_custom_label_score(df)
                score_label = fill_rate_to_score(fill_rate)
        else:
            # For custom labels, check differently
            if logic == "custom_label":
                fill_rate = calc_custom_label_score(df)
                found = fill_rate > 0
                score_label = fill_rate_to_score(fill_rate)

        num_weight = WEIGHTING_MAP.get(weighting, 1)
        num_score = SCORE_MAP.get(score_label, 1)
        weighted_score = num_weight * num_score
        potential_score = num_weight * 5

        results.append({
            "Category": category,
            "Attribute": display_name,
            "Weighting": weighting,
            "Column Found": found,
            "Fill Rate": fill_rate,
            "Score": score_label,
            "Num Weight": num_weight,
            "Num Score": num_score,
            "Weighted Score": weighted_score,
            "Potential Score": potential_score,
        })

    return results


def calc_title_stats(df: pd.DataFrame) -> dict:
    """Calculate title length stats."""
    col = find_column(df, "title")
    if col is None:
        return {"avg_len": 0, "score": "Insufficient"}
    lengths = df[col].astype(str).apply(len)
    avg = lengths.mean()
    if avg >= 120:
        score = "Excellent"
    elif avg >= 100:
        score = "Good"
    elif avg >= 75:
        score = "Average"
    elif avg > 30:
        score = "Below Average"
    else:
        score = "Insufficient"
    return {"avg_len": round(avg), "score": score}


def calc_description_stats(df: pd.DataFrame) -> dict:
    """Calculate description length stats."""
    col = find_column(df, "description")
    if col is None:
        return {"avg_len": 0, "score": "Insufficient"}
    lengths = df[col].astype(str).apply(len)
    avg = lengths.mean()
    if avg >= 2000:
        score = "Excellent"
    elif avg >= 1000:
        score = "Good"
    elif avg >= 500:
        score = "Average"
    elif avg > 100:
        score = "Below Average"
    else:
        score = "Insufficient"
    return {"avg_len": round(avg), "score": score}


def calc_title_brand_rate(df: pd.DataFrame, brand_name: str | None) -> dict:
    """Check how many titles contain the brand name."""
    title_col = find_column(df, "title")
    if title_col is None or not brand_name:
        return {"rate": 0, "score": "Insufficient"}
    total = len(df)
    if total == 0:
        return {"rate": 0, "score": "Insufficient"}
    count = df[title_col].astype(str).str.contains(brand_name, case=False, na=False).sum()
    rate = count / total
    return {"rate": rate, "score": fill_rate_to_score(rate)}


def score_badge_html(score_label: str) -> str:
    cls = score_label.lower().replace(" ", "-")
    return f'<span class="score-badge score-{cls}">{score_label}</span>'


# ═══════════════════════════════════════════════════════════════════════════════
# RADAR / SPIDER CHART
# ═══════════════════════════════════════════════════════════════════════════════

def create_radar_chart(results: list[dict]) -> go.Figure:
    """Create a radar/spider chart of category scores."""
    # Group by category and average the percentage score
    cat_scores = {}
    for r in results:
        cat = r["Category"]
        pct = (r["Weighted Score"] / r["Potential Score"] * 100) if r["Potential Score"] > 0 else 0
        cat_scores.setdefault(cat, []).append(pct)

    categories = list(cat_scores.keys())
    values = [sum(v) / len(v) for v in cat_scores.values()]
    # Close the polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(0, 155, 255, 0.15)",
        line=dict(color=PATTERN_BLUE, width=2),
        marker=dict(size=6, color=PATTERN_BLUE),
        name="Score",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color="#666"),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="#FAFAFA"),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
            ),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=40, b=40),
        height=400,
    )
    return fig


def create_attribute_bar_chart(results: list[dict]) -> go.Figure:
    """Horizontal bar chart showing each attribute's score percentage."""
    attrs = [r["Attribute"] for r in results]
    pcts = [
        (r["Weighted Score"] / r["Potential Score"] * 100) if r["Potential Score"] > 0 else 0
        for r in results
    ]
    colors = [SCORE_COLORS.get(r["Score"], "#FF5252") for r in results]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=attrs,
        x=pcts,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f'{p:.0f}%' for p in pcts],
        textposition="outside",
        textfont=dict(color="#FAFAFA", size=11),
    ))

    fig.update_layout(
        xaxis=dict(
            range=[0, 110],
            title="Score %",
            title_font=dict(color="#888"),
            tickfont=dict(color="#888"),
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            tickfont=dict(color="#FAFAFA", size=11),
            autorange="reversed",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=180, r=60, t=20, b=40),
        height=max(400, len(attrs) * 30),
    )
    return fig


def create_fill_rate_chart(results: list[dict]) -> go.Figure:
    """Bar chart of fill rates per attribute."""
    attrs = [r["Attribute"] for r in results]
    rates = [r["Fill Rate"] * 100 for r in results]
    colors = []
    for rate in rates:
        if rate >= 100:
            colors.append("#00C853")
        elif rate >= 80:
            colors.append("#009BFF")
        elif rate >= 50:
            colors.append("#FFC107")
        elif rate > 20:
            colors.append("#FF9800")
        else:
            colors.append("#FF5252")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=attrs,
        x=rates,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f'{r:.0f}%' for r in rates],
        textposition="outside",
        textfont=dict(color="#FAFAFA", size=11),
    ))

    fig.update_layout(
        xaxis=dict(
            range=[0, 110],
            title="Fill Rate %",
            title_font=dict(color="#888"),
            tickfont=dict(color="#888"),
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            tickfont=dict(color="#FAFAFA", size=11),
            autorange="reversed",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=180, r=60, t=20, b=40),
        height=max(400, len(attrs) * 30),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# FILE UPLOAD & MAIN UI
# ═══════════════════════════════════════════════════════════════════════════════

uploaded = st.file_uploader(
    "Upload your product feed",
    type=["csv", "tsv", "xlsx", "xls", "txt"],
    help="Supports CSV, TSV, Excel files. Column headers should be in the first row.",
)

if uploaded is not None:
    # ── Read file ──────────────────────────────────────────────────────────
    try:
        name = uploaded.name.lower()
        if name.endswith(".csv") or name.endswith(".txt"):
            # Try different separators
            raw = uploaded.read()
            uploaded.seek(0)
            sample = raw[:4096].decode("utf-8", errors="replace")
            if "\t" in sample:
                df = pd.read_csv(BytesIO(raw), sep="\t", dtype=str, on_bad_lines="skip")
            else:
                df = pd.read_csv(BytesIO(raw), dtype=str, on_bad_lines="skip")
        elif name.endswith(".tsv"):
            df = pd.read_csv(uploaded, sep="\t", dtype=str, on_bad_lines="skip")
        else:
            df = pd.read_excel(uploaded, dtype=str)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    st.success(f"Loaded **{len(df):,}** products with **{len(df.columns)}** columns")

    # ── Optional brand name input ──────────────────────────────────────────
    with st.expander("Advanced Options", icon="\u2699\ufe0f"):
        brand_name = st.text_input(
            "Brand name (for title/description brand checks)",
            placeholder="e.g. Nike, Samsung",
            help="Used to check if titles/descriptions contain the brand name",
        )

    # ── Auto-run audit ─────────────────────────────────────────────────────
    with st.spinner("Analysing feed..."):
        results = run_audit(df)
        title_stats = calc_title_stats(df)
        desc_stats = calc_description_stats(df)
        brand_in_title = calc_title_brand_rate(df, brand_name if brand_name else None)

    total_weighted = sum(r["Weighted Score"] for r in results)
    total_potential = sum(r["Potential Score"] for r in results)
    overall_pct = (total_weighted / total_potential * 100) if total_potential > 0 else 0

    # Determine overall grade
    if overall_pct >= 90:
        overall_grade = "Excellent"
    elif overall_pct >= 70:
        overall_grade = "Good"
    elif overall_pct >= 50:
        overall_grade = "Average"
    elif overall_pct > 30:
        overall_grade = "Below Average"
    else:
        overall_grade = "Insufficient"

    st.divider()

    # ── Top metrics row ────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f'<div class="overall-score">'
            f'<div class="number">{overall_pct:.0f}%</div>'
            f'<div class="label">Overall Score</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.metric("Total Products", f"{len(df):,}")
    with col3:
        st.metric("Columns Detected", f"{len(df.columns)}")
    with col4:
        attrs_found = sum(1 for r in results if r["Column Found"])
        st.metric("Attributes Found", f"{attrs_found} / {len(results)}")

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab_radar, tab_detail, tab_fill, tab_content, tab_data = st.tabs([
        "Radar Overview",
        "Attribute Scores",
        "Fill Rates",
        "Content Quality",
        "Raw Data Preview",
    ])

    # ── Tab 1: Radar ──────────────────────────────────────────────────────
    with tab_radar:
        st.markdown('<div class="section-header">Category Score Overview</div>', unsafe_allow_html=True)

        col_chart, col_summary = st.columns([3, 2])
        with col_chart:
            fig_radar = create_radar_chart(results)
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_summary:
            # Category breakdown
            cat_data = {}
            for r in results:
                cat = r["Category"]
                cat_data.setdefault(cat, {"weighted": 0, "potential": 0})
                cat_data[cat]["weighted"] += r["Weighted Score"]
                cat_data[cat]["potential"] += r["Potential Score"]

            for cat, data in cat_data.items():
                pct = (data["weighted"] / data["potential"] * 100) if data["potential"] > 0 else 0
                if pct >= 90:
                    label = "Excellent"
                elif pct >= 70:
                    label = "Good"
                elif pct >= 50:
                    label = "Average"
                elif pct > 30:
                    label = "Below Average"
                else:
                    label = "Insufficient"
                st.markdown(
                    f'<div class="section-header">{cat}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-size:1.5rem;font-weight:700;color:#FAFAFA;">{pct:.0f}%</span>'
                    f'{score_badge_html(label)}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # Overall grade banner
        grade_color = SCORE_COLORS.get(overall_grade, "#FF5252")
        st.markdown(
            f'<div style="background:rgba({int(grade_color[1:3],16)},{int(grade_color[3:5],16)},{int(grade_color[5:7],16)},0.15);'
            f'border:1px solid {grade_color};border-radius:12px;padding:1.5rem;text-align:center;margin-top:1rem;">'
            f'<span style="font-size:1.2rem;color:{grade_color};font-weight:700;">Overall Grade: {overall_grade} ({overall_pct:.0f}%)</span>'
            f'<br><span style="color:#888;font-size:0.9rem;">Weighted score: {total_weighted} / {total_potential}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Tab 2: Attribute Scores ───────────────────────────────────────────
    with tab_detail:
        st.markdown('<div class="section-header">Attribute Score Breakdown</div>', unsafe_allow_html=True)
        fig_bar = create_attribute_bar_chart(results)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Detailed table
        st.markdown('<div class="section-header">Detailed Scores</div>', unsafe_allow_html=True)
        table_data = []
        for r in results:
            table_data.append({
                "Category": r["Category"],
                "Attribute": r["Attribute"],
                "Weighting": r["Weighting"],
                "Found": "Yes" if r["Column Found"] else "No",
                "Fill Rate": f"{r['Fill Rate']:.0%}",
                "Score": r["Score"],
                "Weighted": f"{r['Weighted Score']} / {r['Potential Score']}",
            })
        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True,
            hide_index=True,
        )

    # ── Tab 3: Fill Rates ─────────────────────────────────────────────────
    with tab_fill:
        st.markdown('<div class="section-header">Fill Rate Analysis</div>', unsafe_allow_html=True)
        fig_fill = create_fill_rate_chart(results)
        st.plotly_chart(fig_fill, use_container_width=True)

        # Missing / low fill rate alerts
        st.markdown('<div class="section-header">Alerts</div>', unsafe_allow_html=True)
        missing = [r for r in results if not r["Column Found"]]
        low_fill = [r for r in results if r["Column Found"] and r["Fill Rate"] < 0.5]

        if missing:
            st.warning(f"**{len(missing)} attribute(s) not found in feed:** "
                       + ", ".join(r["Attribute"] for r in missing))
        if low_fill:
            st.warning(f"**{len(low_fill)} attribute(s) with fill rate below 50%:** "
                       + ", ".join(f'{r["Attribute"]} ({r["Fill Rate"]:.0%})' for r in low_fill))
        if not missing and not low_fill:
            st.success("All attributes found with fill rates above 50%!")

    # ── Tab 4: Content Quality ────────────────────────────────────────────
    with tab_content:
        st.markdown('<div class="section-header">Title & Description Quality</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Avg Title Length", f"{title_stats['avg_len']} chars")
            st.markdown(
                f"Target: 120+ chars &nbsp; {score_badge_html(title_stats['score'])}",
                unsafe_allow_html=True,
            )
        with c2:
            st.metric("Avg Description Length", f"{desc_stats['avg_len']} chars")
            st.markdown(
                f"Target: 2000+ chars &nbsp; {score_badge_html(desc_stats['score'])}",
                unsafe_allow_html=True,
            )
        with c3:
            if brand_in_title["rate"] > 0:
                st.metric("Brand in Titles", f"{brand_in_title['rate']:.0%}")
                st.markdown(
                    f"Target: 100% &nbsp; {score_badge_html(brand_in_title['score'])}",
                    unsafe_allow_html=True,
                )
            else:
                st.info("Enter a brand name in Advanced Options to check brand presence in titles")

        # Title length distribution
        title_col = find_column(df, "title")
        if title_col:
            st.markdown('<div class="section-header">Title Length Distribution</div>', unsafe_allow_html=True)
            lengths = df[title_col].astype(str).apply(len)
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=lengths,
                nbinsx=40,
                marker=dict(color=PATTERN_BLUE, line=dict(width=0)),
            ))
            fig_hist.update_layout(
                xaxis=dict(title="Character Length", title_font=dict(color="#888"), tickfont=dict(color="#888"),
                           gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(title="Products", title_font=dict(color="#888"), tickfont=dict(color="#888"),
                           gridcolor="rgba(255,255,255,0.05)"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=60, r=20, t=20, b=40),
                height=300,
            )
            # Add target line
            fig_hist.add_vline(x=120, line_dash="dash", line_color="#00C853", annotation_text="Target (120)",
                               annotation_font_color="#00C853")
            st.plotly_chart(fig_hist, use_container_width=True)

    # ── Tab 5: Raw Data Preview ───────────────────────────────────────────
    with tab_data:
        st.markdown('<div class="section-header">Feed Preview (first 100 rows)</div>', unsafe_allow_html=True)
        st.dataframe(df.head(100), use_container_width=True, height=500)

        st.markdown('<div class="section-header">Detected Columns</div>', unsafe_allow_html=True)
        col_list = ", ".join(f"`{c}`" for c in df.columns)
        st.markdown(col_list)

else:
    # Placeholder when no file uploaded
    st.markdown(
        '<div style="text-align:center;padding:4rem 2rem;color:#666;">'
        '<p style="font-size:3rem;margin-bottom:0.5rem;">&#x1F4E6;</p>'
        "<p>Upload a product feed file above to get started.</p>"
        '<p style="font-size:0.85rem;">Supports CSV, TSV, and Excel formats. '
        "The tool automatically detects columns like <b>title</b>, <b>description</b>, "
        "<b>price</b>, <b>brand</b>, <b>gtin</b>, <b>image link</b>, and more.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
