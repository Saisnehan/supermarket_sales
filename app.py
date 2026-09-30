import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SuperMarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN TOKENS  — change here to retheme the whole app
# ══════════════════════════════════════════════════════════════════════════════
PRIMARY   = "#1d4ed8"   # brand blue
SECONDARY = "#0ea5e9"   # accent sky-blue
SUCCESS   = "#16a34a"
WARNING   = "#d97706"
DANGER    = "#dc2626"
NEUTRAL   = "#64748b"
BG_CARD   = "#ffffff"
BG_PAGE   = "#f1f5f9"
BORDER    = "#e2e8f0"
TEXT_MAIN = "#0f172a"
TEXT_MUTE = "#64748b"

# Consistent Plotly palette used across every chart
CHART_PALETTE = [
    "#1d4ed8", "#0ea5e9", "#6366f1", "#8b5cf6",
    "#06b6d4", "#0284c7", "#3b82f6", "#a78bfa",
]

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* ── Root / Page ─────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {{
    background: {BG_PAGE};
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    color: {TEXT_MAIN};
}}
[data-testid="stAppViewContainer"] > .main {{
    padding-top: 0.5rem;
}}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: #0f172a !important;
    border-right: 1px solid #1e293b;
}}
[data-testid="stSidebar"] * {{
    color: #cbd5e1 !important;
}}
[data-testid="stSidebar"] .sidebar-title {{
    color: #f8fafc !important;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.4rem 0 0.2rem;
}}
[data-testid="stSidebar"] .sidebar-section {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b !important;
    margin: 1rem 0 0.3rem;
}}
[data-testid="stSidebar"] hr {{
    border-color: #1e293b !important;
    margin: 0.7rem 0;
}}
[data-testid="stSidebar"] label {{
    font-size: 0.82rem !important;
    color: #94a3b8 !important;
}}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background: {PRIMARY} !important;
}}
[data-testid="stSidebar"] .sidebar-meta {{
    background: #1e293b;
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    font-size: 0.78rem;
    color: #94a3b8 !important;
    margin-top: 0.5rem;
    line-height: 1.7;
}}
[data-testid="stSidebar"] .sidebar-meta span {{
    color: #e2e8f0 !important;
    font-weight: 600;
}}

/* ══════════════════════════════════════════════════════════════
   TAB NAVIGATION BAR
   Strategy: target every possible element Base Web can inject
   inside tab buttons using the universal child selector (*),
   combined with forced colour inheritance on the button itself.
   This defeats Base Web's CSS custom-property colour injection
   without relying on any specific inner element name.
══════════════════════════════════════════════════════════════ */

/* 1 ── Strip container */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    gap: 3px !important;
    background: #e8edf2 !important;
    border-radius: 10px 10px 0 0 !important;
    border: 1px solid {BORDER} !important;
    border-bottom: 3px solid {PRIMARY} !important;
    padding: 0.5rem 0.5rem 0 !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {{
    display: none !important;
}}

/* 2 ── Every inactive tab button */
[data-testid="stTabs"] [data-baseweb="tab"] {{
    border-radius: 6px 6px 0 0 !important;
    padding: 0.6rem 1.05rem !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #1e293b !important;
    background: #dde3ec !important;
    border-bottom: 3px solid transparent !important;
    white-space: nowrap !important;
    letter-spacing: 0.01em !important;
    transition: background 0.15s !important;
    /* Force colour inheritance down the entire subtree */
    -webkit-text-fill-color: #1e293b !important;
}}

/* 3 ── Universal child selector: every element inside inactive tab */
[data-testid="stTabs"] [data-baseweb="tab"] * {{
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    opacity: 1 !important;
    visibility: visible !important;
}}

/* 4 ── Hover on inactive tab */
[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
    background: #c7d4e8 !important;
    color: {PRIMARY} !important;
    -webkit-text-fill-color: {PRIMARY} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:hover * {{
    color: {PRIMARY} !important;
    -webkit-text-fill-color: {PRIMARY} !important;
    opacity: 1 !important;
}}

/* 5 ── Active (selected) tab button */
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: {PRIMARY} !important;
    border-bottom: 3px solid #93c5fd !important;
    font-weight: 700 !important;
}}
[data-testid="stTabs"] [aria-selected="true"] * {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    visibility: visible !important;
}}

/* 6 ── Active tab hover */
[data-testid="stTabs"] [aria-selected="true"]:hover {{
    background: #1e40af !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}}
[data-testid="stTabs"] [aria-selected="true"]:hover * {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}}

/* 7 ── Tab panel (unchanged) */
[data-testid="stTabs"] [data-baseweb="tab-panel"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.5rem !important;
}}

/* ── KPI cards ───────────────────────────────────────────────────────────── */
.kpi-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.2rem 1rem 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    height: 100%;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: {PRIMARY};
    border-radius: 12px 12px 0 0;
}}
.kpi-icon  {{ font-size: 1.6rem; margin-bottom: 0.3rem; display: block; }}
.kpi-value {{
    font-size: 1.75rem;
    font-weight: 800;
    color: {TEXT_MAIN};
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}}
.kpi-label {{
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {TEXT_MUTE};
}}
.kpi-card.accent-green::before  {{ background: {SUCCESS}; }}
.kpi-card.accent-sky::before    {{ background: {SECONDARY}; }}
.kpi-card.accent-violet::before {{ background: #7c3aed; }}
.kpi-card.accent-amber::before  {{ background: {WARNING}; }}
.kpi-card.accent-red::before    {{ background: {DANGER}; }}

/* ── Section headings ────────────────────────────────────────────────────── */
.sec-head {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    font-weight: 700;
    color: {TEXT_MAIN};
    margin: 0.4rem 0 0.9rem;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {BORDER};
}}
.sec-head .dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    background: {PRIMARY};
    flex-shrink: 0;
}}

/* ── Alert / callout boxes ───────────────────────────────────────────────── */
.alert-box {{
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    line-height: 1.5;
}}
.alert-icon {{ font-size: 1.1rem; flex-shrink: 0; margin-top: 0.05rem; }}
.alert-success {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; }}
.alert-warning {{ background: #fffbeb; border: 1px solid #fde68a; color: #b45309; }}
.alert-error   {{ background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; }}
.alert-info    {{ background: #eff6ff; border: 1px solid #bfdbfe; color: #1d4ed8; }}

/* ── DQ status badges ────────────────────────────────────────────────────── */
.badge {{
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    line-height: 1.4;
}}
.badge-ok   {{ background: #dcfce7; color: #15803d; }}
.badge-warn {{ background: #fef9c3; color: #854d0e; }}
.badge-err  {{ background: #fee2e2; color: #b91c1c; }}

/* ── Insight bullets ─────────────────────────────────────────────────────── */
.insight-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    background: #f8fafc;
    border: 1px solid {BORDER};
    border-left: 3px solid {PRIMARY};
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.86rem;
    color: {TEXT_MAIN};
    line-height: 1.5;
}}
.insight-item strong {{ color: {PRIMARY}; }}
.insight-num {{
    background: {PRIMARY};
    color: #fff;
    width: 20px; height: 20px;
    border-radius: 50%;
    font-size: 0.68rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 0.1rem;
}}

/* ── Recommendation cards ────────────────────────────────────────────────── */
.rec-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
}}
.rec-tag {{
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    background: #eff6ff;
    color: {PRIMARY};
    margin-bottom: 0.4rem;
}}
.rec-title {{ font-weight: 700; color: {TEXT_MAIN}; font-size: 0.9rem; margin-bottom: 0.25rem; }}
.rec-body  {{ color: {TEXT_MUTE}; font-size: 0.83rem; line-height: 1.5; }}

/* ── DQ metric tile ─────────────────────────────────────────────────────── */
.dq-tile {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
}}
.dq-tile .dq-val  {{ font-size: 1.6rem; font-weight: 800; line-height: 1.1; }}
.dq-tile .dq-lbl  {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
                      color: {TEXT_MUTE}; margin-top: 0.25rem; }}

/* ── Footer ──────────────────────────────────────────────────────────────── */
.app-footer {{
    text-align: center;
    padding: 1.2rem 0 0.5rem;
    margin-top: 2rem;
    border-top: 1px solid {BORDER};
    font-size: 0.78rem;
    color: {TEXT_MUTE};
    letter-spacing: 0.01em;
}}

/* ── Misc helpers ────────────────────────────────────────────────────────── */
.spacer   {{ height: 0.8rem; }}
.spacer-s {{ height: 0.4rem; }}
div[data-testid="stDataFrameResizable"] {{ border-radius: 8px; overflow: hidden; }}
footer {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER — chart theme applied to every figure
# ══════════════════════════════════════════════════════════════════════════════
def apply_theme(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color=TEXT_MAIN),
        margin=dict(l=16, r=16, t=46, b=16),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(size=11),
        ),
        title_font=dict(size=13, color=TEXT_MAIN, family="Inter, Segoe UI, sans-serif"),
        xaxis=dict(gridcolor="#f1f5f9", linecolor=BORDER, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#f1f5f9", linecolor=BORDER, tickfont=dict(size=11)),
    )
    return fig


def sec(icon, title):
    """Render a polished section heading."""
    st.markdown(
        f'<div class="sec-head"><span class="dot"></span>{icon} {title}</div>',
        unsafe_allow_html=True,
    )


def kpi(col, icon, value, label, accent=""):
    col.markdown(
        f"""<div class="kpi-card {accent}">
              <span class="kpi-icon">{icon}</span>
              <div class="kpi-value">{value}</div>
              <div class="kpi-label">{label}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def alert(kind, icon, text):
    st.markdown(
        f'<div class="alert-box alert-{kind}"><span class="alert-icon">{icon}</span><span>{text}</span></div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  LOAD DATA  (unchanged logic)
# ══════════════════════════════════════════════════════════════════════════════
CSV_PATH = "SuperMarket_Sales_data.csv"


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    df.columns = df.columns.str.strip()

    # 1. Parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 2. Numeric coercion
    for col in ["Quantity", "Unit Price", "Sales", "Rating"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Re-calculate Sales = Qty × Unit Price
    df["Calculated Sales"] = df["Quantity"] * df["Unit Price"]
    mask = df["Sales"].isna() | (
        (df["Sales"] - df["Calculated Sales"]).abs()
        / df["Calculated Sales"].replace(0, np.nan)
        > 0.01
    )
    df.loc[mask, "Sales"] = df.loc[mask, "Calculated Sales"]

    # 4. Derived columns
    df["Month"]    = df["Date"].dt.to_period("M").astype(str)
    df["Month_dt"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Day"]      = df["Date"].dt.day_name()

    return df


# ── Load with graceful error handling ────────────────────────────────────────
if not os.path.isfile(CSV_PATH):
    st.error(
        f"**Dataset not found.**  \n"
        f"Expected file `{CSV_PATH}` in the project folder.  \n"
        "Please place the CSV file alongside `app.py` and reload."
    )
    st.stop()

with st.spinner("Loading dataset…"):
    df_raw = load_data(CSV_PATH)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR  — filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="sidebar-title">🛒 Sales Analytics</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">📍 Location</p>', unsafe_allow_html=True)
    cities = sorted(df_raw["City"].dropna().unique())
    sel_cities = st.multiselect("City", cities, default=cities, label_visibility="collapsed",
                                placeholder="All cities")

    st.markdown('<p class="sidebar-section">🏷️ Product</p>', unsafe_allow_html=True)
    categories = sorted(df_raw["Category"].dropna().unique())
    sel_cats = st.multiselect("Category", categories, default=categories,
                              label_visibility="collapsed", placeholder="All categories")

    st.markdown('<p class="sidebar-section">👥 Customer</p>', unsafe_allow_html=True)
    genders = sorted(df_raw["Gender"].dropna().unique())
    sel_gender = st.multiselect("Gender", genders, default=genders,
                                label_visibility="collapsed", placeholder="All genders")

    cust_types = sorted(df_raw["Customer Type"].dropna().unique())
    sel_cust = st.multiselect("Customer Type", cust_types, default=cust_types,
                              label_visibility="collapsed", placeholder="All types")

    st.markdown('<p class="sidebar-section">💳 Payment</p>', unsafe_allow_html=True)
    payments = sorted(df_raw["Payment"].dropna().unique())
    sel_pay = st.multiselect("Payment Method", payments, default=payments,
                             label_visibility="collapsed", placeholder="All methods")

    st.markdown('<p class="sidebar-section">📅 Date Range</p>', unsafe_allow_html=True)
    min_date = df_raw["Date"].min().date()
    max_date = df_raw["Date"].max().date()
    date_range = st.date_input(
        "Date", value=(min_date, max_date),
        min_value=min_date, max_value=max_date,
        label_visibility="collapsed",
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    # Reset button
    if st.button("↺  Reset All Filters", use_container_width=True):
        sel_cities  = cities
        sel_cats    = categories
        sel_gender  = genders
        sel_cust    = cust_types
        sel_pay     = payments
        date_range  = (min_date, max_date)
        st.rerun()

    # Dataset meta
    active_filters = sum([
        sorted(sel_cities) != sorted(cities),
        sorted(sel_cats)   != sorted(categories),
        sorted(sel_gender) != sorted(genders),
        sorted(sel_cust)   != sorted(cust_types),
        sorted(sel_pay)    != sorted(payments),
    ])
    filter_label = (
        f"<span style='color:#facc15'>⚡ {active_filters} filter(s) active</span>"
        if active_filters else "<span style='color:#4ade80'>✓ No filters applied</span>"
    )
    st.markdown(
        f'<div class="sidebar-meta">'
        f'<b>Dataset</b><br>'
        f'<span>SuperMarket_Sales_data.csv</span><br>'
        f'<b>Total rows</b><br><span>{len(df_raw):,}</span><br>'
        f'{filter_label}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  APPLY FILTERS  (unchanged logic)
# ══════════════════════════════════════════════════════════════════════════════
df = df_raw.copy()
if sel_cities:
    df = df[df["City"].isin(sel_cities)]
if sel_cats:
    df = df[df["Category"].isin(sel_cats)]
if sel_gender:
    df = df[df["Gender"].isin(sel_gender)]
if sel_cust:
    df = df[df["Customer Type"].isin(sel_cust)]
if sel_pay:
    df = df[df["Payment"].isin(sel_pay)]
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["Date"] >= start) & (df["Date"] <= end)]

# Guard: empty dataframe after filtering
if df.empty:
    st.warning(
        "⚠️ **No data matches the current filters.**  \n"
        "Try widening your selection in the sidebar."
    )
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="
    background: {TEXT_MAIN};
    border-radius: 12px;
    padding: 1.4rem 2rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
">
  <div style="font-size:2.4rem;line-height:1">🛒</div>
  <div>
    <div style="font-size:1.5rem;font-weight:800;color:#f8fafc;letter-spacing:-0.02em;line-height:1.1">
      SuperMarket Sales Analytics
    </div>
    <div style="font-size:0.85rem;color:#94a3b8;margin-top:0.3rem;font-weight:400">
      Interactive Business Intelligence Dashboard &nbsp;·&nbsp; {len(df):,} transactions in view
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📋 Overview",
    "🔍 Data Quality",
    "💰 Sales Analysis",
    "📊 Category & Product",
    "🏙️ Branch & City",
    "👥 Customer Insights",
    "💳 Payment Analysis",
    "📅 Time Trends",
    "💡 Business Decisions",
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    sec("", "Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)
    kpi(k1, "💰", f"₹{df['Sales'].sum():,.0f}",        "Total Revenue",         "")
    kpi(k2, "📦", f"{int(df['Quantity'].sum()):,}",     "Units Sold",            "accent-sky")
    kpi(k3, "🧾", f"{len(df):,}",                       "Transactions",          "accent-green")
    kpi(k4, "📈", f"₹{df['Sales'].mean():,.2f}",        "Avg Order Value",       "accent-violet")
    kpi(k5, "⭐", f"{df['Rating'].mean():.2f}",          "Avg Customer Rating",   "accent-amber")

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        sec("📄", "Sample Data — First 20 Rows")
        show_df = df.head(20).copy()
        show_df["Date"]       = show_df["Date"].dt.strftime("%d %b %Y")
        show_df["Sales"]      = show_df["Sales"].map("₹{:,.2f}".format)
        show_df["Unit Price"] = show_df["Unit Price"].map("₹{:,.2f}".format)
        st.dataframe(
            show_df.drop(columns=["Calculated Sales", "Month_dt"], errors="ignore"),
            use_container_width=True, height=390,
        )

    with c2:
        sec("🔎", "Column Summary")
        summary = pd.DataFrame({
            "Column":   df.columns.tolist(),
            "Type":     [str(df[c].dtype) for c in df.columns],
            "Non-Null": [int(df[c].notna().sum()) for c in df.columns],
            "Nulls":    [int(df[c].isna().sum()) for c in df.columns],
            "Unique":   [df[c].nunique() for c in df.columns],
        })
        st.dataframe(summary, use_container_width=True, height=390)

    sec("📐", "Descriptive Statistics")
    num_cols = ["Quantity", "Unit Price", "Sales", "Rating"]
    stats = df[num_cols].describe().round(2).T.reset_index()
    stats.rename(columns={"index": "Metric"}, inplace=True)
    st.dataframe(stats, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — DATA QUALITY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    sec("🔍", "Data Quality Report")

    total_cells   = df_raw.shape[0] * df_raw.shape[1]
    missing_cells = int(df_raw.isna().sum().sum())
    dup_rows      = int(df_raw.duplicated().sum())
    sales_mismatch = int(((df_raw["Sales"] - df_raw["Calculated Sales"]).abs() > 0.01).sum())
    completeness  = 100 - 100 * missing_cells / total_cells

    dq1, dq2, dq3, dq4 = st.columns(4)
    for col, icon, lbl, val, col_css in [
        (dq1, "✅", "Missing Cells",     str(missing_cells),
         SUCCESS if missing_cells == 0 else DANGER),
        (dq2, "🔁", "Duplicate Rows",   str(dup_rows),
         SUCCESS if dup_rows == 0 else WARNING),
        (dq3, "🧮", "Sales Mismatches", str(sales_mismatch),
         SUCCESS if sales_mismatch == 0 else WARNING),
        (dq4, "📊", "Data Completeness", f"{completeness:.1f}%",
         SUCCESS),
    ]:
        col.markdown(
            f'<div class="dq-tile">'
            f'  <div style="font-size:1.6rem">{icon}</div>'
            f'  <div class="dq-val" style="color:{col_css}">{val}</div>'
            f'  <div class="dq-lbl">{lbl}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sec("📉", "Missing Values per Column")
        miss = df_raw.isna().sum().reset_index()
        miss.columns = ["Column", "Missing"]
        fig_miss = px.bar(
            miss, x="Column", y="Missing",
            color="Missing", color_continuous_scale=["#bbf7d0", "#dc2626"],
            text="Missing", title="Missing Values by Column",
        )
        fig_miss.update_traces(textposition="outside")
        fig_miss.update_layout(coloraxis_showscale=False, showlegend=False)
        apply_theme(fig_miss, 300)
        st.plotly_chart(fig_miss, use_container_width=True)

    with c2:
        sec("🧮", "Sales Recalculation Validation")
        diff = (df_raw["Sales"] - df_raw["Calculated Sales"]).abs()
        fig_diff = px.histogram(
            diff, nbins=30,
            title="Distribution of |Recorded Sales − Qty × Unit Price|",
            labels={"value": "Absolute Difference (₹)", "count": "Frequency"},
            color_discrete_sequence=[PRIMARY],
        )
        apply_theme(fig_diff, 300)
        st.plotly_chart(fig_diff, use_container_width=True)

    sec("📋", "Column Data Types & Status")
    dtype_df = df_raw.dtypes.reset_index()
    dtype_df.columns = ["Column", "Data Type"]
    dtype_df["Data Type"] = dtype_df["Data Type"].astype(str)
    status_map = {
        "Invoice ID": "✓ Identifier",    "Date": "✓ Datetime",
        "Branch": "✓ Categorical",        "City": "✓ Categorical",
        "Customer Type": "✓ Categorical", "Gender": "✓ Categorical",
        "Product": "✓ Categorical",       "Category": "✓ Categorical",
        "Quantity": "✓ Numeric",          "Unit Price": "✓ Numeric",
        "Payment": "✓ Categorical",       "Rating": "✓ Numeric",
        "Sales": "✓ Numeric",
    }
    dtype_df["Status"] = dtype_df["Column"].map(status_map).fillna("⚠ Check")
    st.dataframe(dtype_df, use_container_width=True)

    st.markdown('<div class="spacer-s"></div>', unsafe_allow_html=True)
    if missing_cells == 0 and dup_rows == 0:
        alert("success", "✅",
              "<strong>Dataset is clean.</strong> No missing values or duplicate rows found. "
              "Sales values match Quantity × Unit Price within rounding tolerance.")
    else:
        if missing_cells > 0:
            alert("error", "✕",
                  f"<strong>{missing_cells} missing cells detected.</strong> "
                  "These were automatically corrected during data loading.")
        if dup_rows > 0:
            alert("warning", "⚠",
                  f"<strong>{dup_rows} duplicate rows found.</strong> "
                  "Consider removing them before further analysis.")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — SALES ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    sec("💰", "Sales Summary")

    total_sales = df["Sales"].sum()
    total_qty   = df["Quantity"].sum()
    avg_sale    = df["Sales"].mean()
    max_sale    = df["Sales"].max()
    min_sale    = df["Sales"].min()
    median_sale = df["Sales"].median()

    s1, s2, s3 = st.columns(3)
    kpi(s1, "💰", f"₹{total_sales:,.2f}",    "Total Revenue",       "")
    kpi(s2, "📦", f"{int(total_qty):,}",      "Total Units Sold",    "accent-sky")
    kpi(s3, "📈", f"₹{avg_sale:,.2f}",        "Average Sale Value",  "accent-violet")

    s4, s5, s6 = st.columns(3)
    kpi(s4, "🔺", f"₹{max_sale:,.2f}",        "Highest Single Sale", "accent-green")
    kpi(s5, "🔻", f"₹{min_sale:,.2f}",        "Lowest Single Sale",  "accent-red")
    kpi(s6, "⚖️", f"₹{median_sale:,.2f}",     "Median Sale Value",   "accent-amber")

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sec("📊", "Transaction Sales Distribution")
        fig_hist = px.histogram(
            df, x="Sales", nbins=40,
            color_discrete_sequence=[PRIMARY],
            title="Distribution of Transaction Sales (₹)",
            labels={"Sales": "Sale Value (₹)", "count": "Frequency"},
        )
        apply_theme(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        sec("📦", "Sales Spread by Category")
        fig_box = px.box(
            df, x="Category", y="Sales",
            color="Category",
            color_discrete_sequence=CHART_PALETTE,
            title="Sales Distribution per Category",
            labels={"Sales": "Sale Value (₹)"},
        )
        fig_box.update_layout(showlegend=False)
        apply_theme(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    sec("🧮", "Sales = Quantity × Unit Price — Validation Sample")
    calc_df = df[["Invoice ID", "Product", "Quantity", "Unit Price",
                  "Calculated Sales", "Sales"]].head(15).copy()
    calc_df["Unit Price"]       = calc_df["Unit Price"].map("₹{:,.2f}".format)
    calc_df["Calculated Sales"] = calc_df["Calculated Sales"].map("₹{:,.2f}".format)
    calc_df["Sales"]            = calc_df["Sales"].map("₹{:,.2f}".format)
    calc_df = calc_df.rename(columns={
        "Calculated Sales": "Qty × Unit Price",
        "Sales": "Recorded Sales",
    })
    st.dataframe(calc_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — CATEGORY & PRODUCT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    cat_agg = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Sales", "count"),
            Avg_Sale=("Sales", "mean"),
            Total_Qty=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

    sec("📊", "Revenue by Category")
    c1, c2 = st.columns(2)
    with c1:
        fig_cat_bar = px.bar(
            cat_agg, x="Category", y="Total_Sales",
            color="Category",
            color_discrete_sequence=CHART_PALETTE,
            text=cat_agg["Total_Sales"].map("₹{:,.0f}".format),
            title="Total Revenue by Category",
            labels={"Total_Sales": "Total Revenue (₹)", "Category": ""},
        )
        fig_cat_bar.update_traces(textposition="outside", textfont_size=10)
        fig_cat_bar.update_layout(showlegend=False)
        apply_theme(fig_cat_bar)
        st.plotly_chart(fig_cat_bar, use_container_width=True)

    with c2:
        fig_cat_pie = px.pie(
            cat_agg, names="Category", values="Total_Sales",
            title="Revenue Share by Category",
            color_discrete_sequence=CHART_PALETTE,
            hole=0.38,
        )
        fig_cat_pie.update_traces(
            textposition="inside", textinfo="percent+label",
            textfont_size=11,
        )
        apply_theme(fig_cat_pie)
        st.plotly_chart(fig_cat_pie, use_container_width=True)

    sec("📋", "Category Summary Table")
    disp_cat = cat_agg.copy()
    disp_cat["Total_Sales"] = disp_cat["Total_Sales"].map("₹{:,.2f}".format)
    disp_cat["Avg_Sale"]    = disp_cat["Avg_Sale"].map("₹{:,.2f}".format)
    disp_cat["Avg_Rating"]  = disp_cat["Avg_Rating"].map("{:.2f} ⭐".format)
    disp_cat.columns = ["Category", "Total Sales", "Transactions",
                        "Avg Sale", "Total Qty Sold", "Avg Rating"]
    st.dataframe(disp_cat, use_container_width=True)

    sec("🏆", "Top 10 Products by Revenue")
    prod_agg = (
        df.groupby("Product")
        .agg(Total_Sales=("Sales", "sum"), Transactions=("Sales", "count"),
             Avg_Rating=("Rating", "mean"))
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )
    fig_prod = px.bar(
        prod_agg, x="Total_Sales", y="Product",
        orientation="h",
        color="Total_Sales", color_continuous_scale=["#bfdbfe", PRIMARY],
        text=prod_agg["Total_Sales"].map("₹{:,.0f}".format),
        title="Top 10 Products — Total Revenue",
        labels={"Total_Sales": "Total Revenue (₹)", "Product": ""},
    )
    fig_prod.update_traces(textposition="outside", textfont_size=10)
    fig_prod.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
    )
    apply_theme(fig_prod, 400)
    st.plotly_chart(fig_prod, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — BRANCH & CITY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    city_agg = (
        df.groupby(["City", "Branch"])
        .agg(Total_Sales=("Sales", "sum"), Transactions=("Sales", "count"),
             Avg_Sale=("Sales", "mean"), Avg_Rating=("Rating", "mean"))
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

    sec("🏙️", "City & Branch Performance")
    c1, c2 = st.columns(2)
    with c1:
        fig_city = px.bar(
            city_agg, x="City", y="Total_Sales",
            color="Branch", barmode="group",
            color_discrete_sequence=CHART_PALETTE,
            text=city_agg["Total_Sales"].map("₹{:,.0f}".format),
            title="Total Revenue by City & Branch",
            labels={"Total_Sales": "Total Revenue (₹)"},
        )
        fig_city.update_traces(textposition="outside", textfont_size=10)
        apply_theme(fig_city)
        st.plotly_chart(fig_city, use_container_width=True)

    with c2:
        city_total = city_agg.groupby("City")["Total_Sales"].sum().reset_index()
        fig_city_pie = px.pie(
            city_total, names="City", values="Total_Sales",
            title="City-wise Revenue Share",
            color_discrete_sequence=CHART_PALETTE,
            hole=0.38,
        )
        fig_city_pie.update_traces(
            textposition="inside", textinfo="percent+label", textfont_size=11,
        )
        apply_theme(fig_city_pie)
        st.plotly_chart(fig_city_pie, use_container_width=True)

    sec("📋", "Branch Performance Table")
    disp_city = city_agg.copy()
    disp_city["Total_Sales"] = disp_city["Total_Sales"].map("₹{:,.2f}".format)
    disp_city["Avg_Sale"]    = disp_city["Avg_Sale"].map("₹{:,.2f}".format)
    disp_city["Avg_Rating"]  = disp_city["Avg_Rating"].map("{:.2f} ⭐".format)
    disp_city.columns = ["City", "Branch", "Total Sales", "Transactions",
                         "Avg Sale", "Avg Rating"]
    st.dataframe(disp_city, use_container_width=True)

    sec("⭐", "Average Customer Rating by City")
    rating_city = (df.groupby("City")["Rating"].mean()
                     .reset_index()
                     .sort_values("Rating", ascending=False))
    fig_rat = px.bar(
        rating_city, x="City", y="Rating",
        color="Rating", color_continuous_scale=["#fca5a5", "#bbf7d0"],
        text=rating_city["Rating"].map("{:.2f}".format),
        title="Average Customer Rating by City",
        labels={"Rating": "Avg Rating ⭐"},
    )
    fig_rat.update_traces(textposition="outside", textfont_size=11)
    fig_rat.update_layout(coloraxis_showscale=False)
    apply_theme(fig_rat, 300)
    st.plotly_chart(fig_rat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — CUSTOMER INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    sec("👥", "Customer Demographics & Behaviour")

    gender_agg = df.groupby("Gender").agg(
        Total_Sales=("Sales", "sum"), Transactions=("Sales", "count")
    ).reset_index()
    cust_agg = df.groupby("Customer Type").agg(
        Total_Sales=("Sales", "sum"), Transactions=("Sales", "count")
    ).reset_index()
    gc_agg = df.groupby(["Gender", "Customer Type"])["Sales"].sum().reset_index()

    c1, c2, c3 = st.columns(3)
    with c1:
        fig_g = px.pie(
            gender_agg, names="Gender", values="Total_Sales",
            title="Revenue by Gender",
            color_discrete_sequence=[PRIMARY, SECONDARY],
            hole=0.38,
        )
        fig_g.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        apply_theme(fig_g, 300)
        st.plotly_chart(fig_g, use_container_width=True)

    with c2:
        fig_ct = px.pie(
            cust_agg, names="Customer Type", values="Total_Sales",
            title="Revenue by Customer Type",
            color_discrete_sequence=[SUCCESS, WARNING],
            hole=0.38,
        )
        fig_ct.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        apply_theme(fig_ct, 300)
        st.plotly_chart(fig_ct, use_container_width=True)

    with c3:
        fig_gc = px.bar(
            gc_agg, x="Gender", y="Sales", color="Customer Type",
            barmode="group",
            color_discrete_sequence=[PRIMARY, SECONDARY],
            title="Revenue: Gender × Customer Type",
            labels={"Sales": "Total Revenue (₹)"},
        )
        apply_theme(fig_gc, 300)
        st.plotly_chart(fig_gc, use_container_width=True)

    sec("🏷️", "Category Preference by Gender")
    cat_gender = df.groupby(["Category", "Gender"])["Sales"].sum().reset_index()
    fig_cg = px.bar(
        cat_gender, x="Category", y="Sales", color="Gender",
        barmode="group",
        color_discrete_sequence=[PRIMARY, SECONDARY],
        title="Category Revenue Split by Gender",
        labels={"Sales": "Total Revenue (₹)"},
    )
    apply_theme(fig_cg)
    st.plotly_chart(fig_cg, use_container_width=True)

    sec("⭐", "Rating Distribution by Customer Type")
    fig_rating = px.histogram(
        df, x="Rating", color="Customer Type",
        nbins=20, barmode="overlay", opacity=0.75,
        color_discrete_sequence=[PRIMARY, SECONDARY],
        title="Rating Distribution — Member vs Normal",
        labels={"Rating": "Customer Rating", "count": "Frequency"},
    )
    apply_theme(fig_rating, 320)
    st.plotly_chart(fig_rating, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — PAYMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    pay_agg = (
        df.groupby("Payment")
        .agg(Total_Sales=("Sales", "sum"), Transactions=("Sales", "count"),
             Avg_Sale=("Sales", "mean"))
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )

    sec("💳", "Payment Method Performance")
    c1, c2 = st.columns(2)
    with c1:
        fig_pay = px.bar(
            pay_agg, x="Payment", y="Total_Sales",
            color="Payment",
            color_discrete_sequence=CHART_PALETTE,
            text=pay_agg["Total_Sales"].map("₹{:,.0f}".format),
            title="Total Revenue by Payment Method",
            labels={"Total_Sales": "Total Revenue (₹)", "Payment": ""},
        )
        fig_pay.update_traces(textposition="outside", textfont_size=10)
        fig_pay.update_layout(showlegend=False)
        apply_theme(fig_pay)
        st.plotly_chart(fig_pay, use_container_width=True)

    with c2:
        fig_pay_pie = px.pie(
            pay_agg, names="Payment", values="Transactions",
            title="Transaction Share by Payment Method",
            color_discrete_sequence=CHART_PALETTE,
            hole=0.38,
        )
        fig_pay_pie.update_traces(
            textposition="inside", textinfo="percent+label", textfont_size=11,
        )
        apply_theme(fig_pay_pie)
        st.plotly_chart(fig_pay_pie, use_container_width=True)

    sec("📊", "Payment Method Usage Across Categories")
    pay_cat = df.groupby(["Category", "Payment"])["Sales"].count().reset_index()
    pay_cat.columns = ["Category", "Payment", "Count"]
    fig_pc = px.bar(
        pay_cat, x="Category", y="Count", color="Payment",
        barmode="stack",
        color_discrete_sequence=CHART_PALETTE,
        title="Payment Method Distribution by Category (Transaction Count)",
        labels={"Count": "Transactions", "Category": ""},
    )
    apply_theme(fig_pc)
    st.plotly_chart(fig_pc, use_container_width=True)

    sec("📋", "Payment Method Summary Table")
    disp_pay = pay_agg.copy()
    disp_pay["Total_Sales"] = disp_pay["Total_Sales"].map("₹{:,.2f}".format)
    disp_pay["Avg_Sale"]    = disp_pay["Avg_Sale"].map("₹{:,.2f}".format)
    disp_pay.columns = ["Payment Method", "Total Revenue", "Transactions", "Avg Sale"]
    st.dataframe(disp_pay, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — TIME TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    monthly = (
        df.groupby("Month_dt")
        .agg(Total_Sales=("Sales", "sum"), Transactions=("Sales", "count"),
             Avg_Sale=("Sales", "mean"))
        .reset_index()
        .sort_values("Month_dt")
    )

    sec("📅", "Monthly Revenue & Transaction Trend")
    fig_month = make_subplots(specs=[[{"secondary_y": True}]])
    fig_month.add_trace(
        go.Bar(
            x=monthly["Month_dt"].astype(str), y=monthly["Total_Sales"],
            name="Total Revenue (₹)", marker_color=PRIMARY, opacity=0.8,
        ),
        secondary_y=False,
    )
    fig_month.add_trace(
        go.Scatter(
            x=monthly["Month_dt"].astype(str), y=monthly["Transactions"],
            name="Transactions", mode="lines+markers",
            line=dict(color=SECONDARY, width=2.5),
            marker=dict(size=7, color=SECONDARY),
        ),
        secondary_y=True,
    )
    fig_month.update_layout(
        title="Monthly Revenue & Transaction Volume",
        paper_bgcolor="white", plot_bgcolor="white",
        height=400,
        font=dict(family="Inter, Segoe UI, sans-serif", size=12),
        margin=dict(l=16, r=16, t=46, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, borderwidth=1),
        xaxis=dict(gridcolor="#f1f5f9", linecolor=BORDER, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#f1f5f9", linecolor=BORDER, tickfont=dict(size=11)),
    )
    fig_month.update_yaxes(title_text="Total Revenue (₹)", secondary_y=False)
    fig_month.update_yaxes(title_text="Transaction Count", secondary_y=True)
    st.plotly_chart(fig_month, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        sec("📆", "Sales by Day of Week")
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]
        dow = df.groupby("Day")["Sales"].agg(["sum", "count", "mean"]).reset_index()
        dow.columns = ["Day", "Total_Sales", "Transactions", "Avg_Sale"]
        dow["Day"] = pd.Categorical(dow["Day"], categories=dow_order, ordered=True)
        dow = dow.sort_values("Day")
        fig_dow = px.bar(
            dow, x="Day", y="Total_Sales",
            color="Total_Sales", color_continuous_scale=["#bfdbfe", PRIMARY],
            text=dow["Total_Sales"].map("₹{:,.0f}".format),
            title="Total Revenue by Day of Week",
            labels={"Total_Sales": "Total Revenue (₹)", "Day": ""},
        )
        fig_dow.update_traces(textposition="outside", textfont_size=9)
        fig_dow.update_layout(coloraxis_showscale=False)
        apply_theme(fig_dow, 350)
        st.plotly_chart(fig_dow, use_container_width=True)

    with c2:
        sec("🌡️", "Category × Month Sales Heatmap")
        cat_monthly = df.groupby(["Month", "Category"])["Sales"].sum().reset_index()
        cat_pivot = (
            cat_monthly.pivot(index="Category", columns="Month", values="Sales")
            .fillna(0)
        )
        fig_heat = px.imshow(
            cat_pivot.round(0),
            color_continuous_scale=["#eff6ff", PRIMARY],
            title="Category × Month Revenue Heatmap (₹)",
            labels={"color": "Revenue (₹)"},
            aspect="auto",
        )
        fig_heat.update_layout(
            height=350, paper_bgcolor="white",
            font=dict(family="Inter, Segoe UI, sans-serif", size=11),
            margin=dict(l=16, r=16, t=46, b=16),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    sec("📋", "Monthly Summary Table")
    disp_monthly = monthly.copy()
    disp_monthly["Month"]       = disp_monthly["Month_dt"].dt.strftime("%B %Y")
    disp_monthly["Total_Sales"] = disp_monthly["Total_Sales"].map("₹{:,.2f}".format)
    disp_monthly["Avg_Sale"]    = disp_monthly["Avg_Sale"].map("₹{:,.2f}".format)
    disp_monthly = disp_monthly[["Month", "Total_Sales", "Transactions", "Avg_Sale"]]
    disp_monthly.columns = ["Month", "Total Revenue", "Transactions", "Avg Sale"]
    st.dataframe(disp_monthly, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 9 — BUSINESS DECISIONS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    # Recompute key metrics for insights (unchanged logic)
    top_cat        = df.groupby("Category")["Sales"].sum().idxmax()
    top_city       = df.groupby("City")["Sales"].sum().idxmax()
    top_pay        = df.groupby("Payment")["Sales"].sum().idxmax()
    top_product    = df.groupby("Product")["Sales"].sum().idxmax()
    low_rating_cat = df.groupby("Category")["Rating"].mean().idxmin()
    best_day       = df.groupby("Day")["Sales"].sum().idxmax()
    member_rev     = df[df["Customer Type"] == "Member"]["Sales"].sum()
    normal_rev     = df[df["Customer Type"] == "Normal"]["Sales"].sum()
    mem_pct        = (member_rev / (member_rev + normal_rev) * 100
                      if (member_rev + normal_rev) > 0 else 0)

    sec("📌", "Key Business Insights")

    insights = [
        (f"Best-performing category: <strong>{top_cat}</strong>",
         "Focus marketing spend, shelf space, and procurement on this category."),
        (f"Top revenue city: <strong>{top_city}</strong>",
         "Strong regional demand — consider expanding branch capacity or inventory."),
        (f"Most preferred payment: <strong>{top_pay}</strong>",
         "Prioritise a seamless checkout experience for this payment channel."),
        (f"Top-selling product: <strong>{top_product}</strong>",
         "Maintain stock levels and explore bundle or cross-sell promotions."),
        (f"Lowest-rated category: <strong>{low_rating_cat}</strong>",
         "Investigate product quality, supplier performance, or pricing strategy."),
        (f"Peak sales day: <strong>{best_day}</strong>",
         "Schedule promotions, flash sales, and additional staff on this day."),
        (f"Member revenue share: <strong>{mem_pct:.1f}%</strong>",
         ("Loyalty programme is performing well — continue rewarding members."
          if mem_pct > 50
          else "Run enrolment campaigns to convert Normal shoppers into Members.")),
    ]

    for i, (heading, body) in enumerate(insights, 1):
        st.markdown(
            f'<div class="insight-item">'
            f'  <div class="insight-num">{i}</div>'
            f'  <div><div style="font-weight:600;margin-bottom:0.2rem">{heading}</div>'
            f'  <div style="color:{TEXT_MUTE};font-size:0.82rem">{body}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    sec("🏆", "Strategic Recommendations")

    recs = [
        ("Boost Top Category",
         "Strategy",
         f"Double down on <strong>{top_cat}</strong> with seasonal promotions, "
         "bundled deals, and dedicated shelf space to maximise revenue from the "
         "highest-grossing category."),
        ("Expand in High-Revenue City",
         "Growth",
         f"<strong>{top_city}</strong> is the strongest market. Consider opening "
         "a second branch, increasing inventory, or launching city-specific loyalty offers."),
        ("Improve Low-Rated Category",
         "Quality",
         f"<strong>{low_rating_cat}</strong> has the lowest average customer rating. "
         "Conduct a product-quality audit, review supplier contracts, and gather feedback."),
        ("Loyalty Programme Optimisation",
         "Retention",
         f"Members contribute {mem_pct:.1f}% of revenue. "
         + ("Reward members with exclusive discounts to retain them."
            if mem_pct > 50
            else "Run enrolment campaigns to convert Normal customers to Members.")),
        ("Payment Infrastructure",
         "Operations",
         f"<strong>{top_pay}</strong> is the dominant channel. Ensure zero downtime, "
         "fast processing, and cashback tie-ups to enhance checkout experience."),
        ("Peak-Day Staffing & Promotions",
         "Planning",
         f"<strong>{best_day}</strong> records the highest footfall. Deploy flash sales, "
         "extra cashiers, and targeted social-media ads every week on this day."),
        ("Cross-Sell & Upsell Strategy",
         "Revenue",
         "Use category and gender purchase data to design cross-sell bundles "
         "(e.g. Dairy + Snacks combo packs) and upsell premium alternatives at checkout."),
        ("Inventory Management",
         "Supply Chain",
         "Align restocking cycles with the monthly sales trend — stock up before "
         "peak months and reduce slow-moving SKUs identified in the heatmap analysis."),
    ]

    col_l, col_r = st.columns(2)
    for i, (title, tag, body) in enumerate(recs):
        target = col_l if i % 2 == 0 else col_r
        target.markdown(
            f'<div class="rec-card">'
            f'  <div class="rec-tag">{tag}</div>'
            f'  <div class="rec-title">{title}</div>'
            f'  <div class="rec-body">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    sec("📊", "Performance Scorecard")

    avg_rating      = df["Rating"].mean()
    rev_per_txn     = df["Sales"].sum() / len(df) if len(df) > 0 else 0
    top_month_sales = df.groupby("Month_dt")["Sales"].sum().max() if not df.empty else 0

    sc1, sc2, sc3, sc4 = st.columns(4)
    kpi(sc1, "⭐", f"{avg_rating:.2f} / 5.0",       "Overall Avg Rating",
        "accent-green" if avg_rating >= 4.0 else "accent-amber" if avg_rating >= 3.0 else "accent-red")
    kpi(sc2, "💳", f"₹{rev_per_txn:,.2f}",           "Revenue / Transaction",  "accent-sky")
    kpi(sc3, "🏆", f"₹{top_month_sales:,.0f}",        "Peak Month Revenue",     "accent-violet")
    kpi(sc4, "🏷️", f"{df['Category'].nunique()}",     "Product Categories",     "")


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="app-footer">'
    "SuperMarket Sales Analytics &nbsp;·&nbsp; "
    "Data-driven insights for better business decisions"
    "</div>",
    unsafe_allow_html=True,
)
