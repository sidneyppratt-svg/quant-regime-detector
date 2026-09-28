import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas_datareader.data as web
import datetime
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Sidney Pratt | Quant Research",
    page_icon="📈",
    layout="wide"
)


# ── Live data helpers ─────────────────────────────────────────
# Models run automatically on page load. Downloads are saved for
# one hour so switching pages is fast; "Refresh the Model" clears
# the saved copy and pulls fresh data.
@st.cache_data(ttl=3600, show_spinner=False)
def cached_yf_download(tickers, **kwargs):
    return yf.download(tickers, **kwargs)

@st.cache_data(ttl=3600, show_spinner=False)
def cached_fred(series, start, end):
    return web.DataReader(series, "fred", start, end)

def ordinal(x):
    """53 -> '53rd', 11 -> '11th'."""
    n = int(round(x))
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def refresh_data():
    cached_yf_download.clear()
    cached_fred.clear()

SIGNAL_GREEN = "#2E7D32"
SIGNAL_AMBER = "#E65100"
SIGNAL_RED   = "#C62828"
SIGNAL_TEXT  = "#1a1a1a"

def results_card(as_of, rows):
    """rows: list of (label, value, color)."""
    row_html = "".join(
        f'<div class="rc-row"><span class="rc-label">{label}</span>'
        f'<span class="rc-value" style="color:{color};">{value}</span></div>'
        for label, value, color in rows)
    return (f'<div class="results-card">'
            f'<div class="rc-head"><b>Latest results</b>'
            f'<span class="rc-date">As of {as_of}</span></div>'
            f'{row_html}'
            f'<div class="rc-foot">Full results, analysis &amp; charts below ↓</div>'
            f'</div>')

RESULTS_LOADING = ('<div class="results-card"><div class="rc-head">'
                   '<b>Latest results</b></div>'
                   '<div class="rc-foot">Loading live data…</div></div>')

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #4A4A4A; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] label { color: #FFFFFF !important; }
    .stMarkdown, .stMarkdown p, label { color: #1a1a1a !important; }
    h1 { color: #333333 !important; font-size: 2.5rem !important; }
    h2 { color: #444444 !important; }
    h3 { color: #555555 !important; }
    [data-testid="metric-container"] {
        background-color: #F5F5F5;
        border: 1px solid #CCCCCC;
        border-radius: 8px;
        padding: 1rem;
    }
    [data-testid="metric-container"] * { color: #1a1a1a !important; }
    .stButton > button {
        background-color: #444444 !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton > button:hover { background-color: #222222 !important; }
    hr { border-color: #CCCCCC !important; }
    .card {
        background-color: #F9F9F9;
        border: 1px solid #DDDDDD;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .card h3 { padding: 0 !important; margin-top: 0 !important; color: #444444 !important; margin-bottom: 0.5rem; }
    .card p { color: #1a1a1a !important; line-height: 1.5; margin-bottom: 1.1rem !important; }
    .card p:last-child { margin-bottom: 0 !important; }
    .tag {
        display: inline-block;
        background-color: #444444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin: 4px;
    }
    .profile-placeholder {
        width: 110px; height: 110px;
        background: linear-gradient(135deg, #666666, #999999);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 36px; color: white;
        margin: 0 auto 0.75rem auto;
        border: 3px solid #AAAAAA;
    }
    .seeking-card {
        background-color: #F9F9F9;
        border: 1px solid #DDDDDD;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
    .seeking-card h4 { color: #444444 !important; margin-bottom: 0.5rem; font-size: 15px; }
    .seeking-card p { color: #333333 !important; font-size: 14px; line-height: 1.8; }
    .sidebar-contact { font-size: 13px; color: white !important; line-height: 2; }
    .player-card {
        background-color: #F0F4F8;
        border: 1px solid #CCCCCC;
        border-left: 5px solid #333333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .player-card h3 { color: #222222 !important; margin-bottom: 0.3rem; }
    .player-card p { color: #333333 !important; line-height: 1.7; }
    .player-card-college {
        background-color: #F5F0FF;
        border: 1px solid #CCCCCC;
        border-left: 5px solid #6644AA;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .player-card-college h3 { color: #222222 !important; margin-bottom: 0.3rem; }
    .player-card-college p { color: #333333 !important; line-height: 1.7; }
    .pathway-step {
        display: inline-block;
        background-color: #333333;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px;
        font-weight: bold;
    }
    .pathway-step-college {
        display: inline-block;
        background-color: #6644AA;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px;
        font-weight: bold;
    }
    .section-label {
        background-color: #333333;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        font-size: 15px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .section-label-college {
        background-color: #6644AA;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        font-size: 15px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .static-section {
        background-color: #F0F4FF;
        border: 1px solid #CCDDFF;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .static-section h3 { padding: 0 !important; margin-top: 0 !important; color: #1A237E !important; margin-bottom: 0.5rem; }
    .static-section p { color: #1a1a1a !important; line-height: 1.5; margin-bottom: 0 !important; }
    .dynamic-section {
        background-color: #F9F9F9;
        border: 1px solid #DDDDDD;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .dynamic-section h3 { padding: 0 !important; margin-top: 0 !important; color: #444444 !important; margin-bottom: 0.5rem; }
    .dynamic-section p { color: #1a1a1a !important; line-height: 1.5; margin-bottom: 0 !important; }
    .data-source-section {
        background-color: #F0FFF4;
        border: 1px solid #A8D5B5;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .data-source-section h3 { padding: 0 !important; margin-top: 0 !important; color: #1B5E20 !important; margin-bottom: 0.5rem; }
    .data-source-section p { color: #1a1a1a !important; line-height: 1.5; margin-bottom: 0 !important; }
    .results-card {
        background-color: #F0FFF4;
        border: 1px solid #A8D5B5;
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        margin-top: 0;
        margin-bottom: 1.25rem;
    }
    .results-card .rc-head {
        display: flex; justify-content: space-between; align-items: baseline;
        color: #1B5E20; font-size: 15px; margin-bottom: 0.4rem;
    }
    .results-card .rc-date { color: #1B5E20; font-size: 12px; opacity: 0.8; }
    .results-card .rc-row {
        display: flex; justify-content: space-between; gap: 1rem;
        padding: 0.2rem 0; border-top: 1px solid #D4EBDB; font-size: 14px;
    }
    .results-card .rc-label { color: #1B5E20; }
    .results-card .rc-value { font-weight: 700; text-align: right; }
    .results-card .rc-foot {
        color: #444444; font-size: 12px; font-weight: 700; margin-top: 0.45rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="profile-placeholder">SP</div>
    <p style="text-align:center; color:#CCCCCC; font-size:11px; margin-bottom:0.5rem;">Photo coming soon</p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div class="sidebar-contact">
    <span style="font-size:18px; font-weight:bold;">Sidney Pratt</span><br>
    Economics & Finance<br>
    Western Michigan University
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Contact")
    st.markdown("""
    <div class="sidebar-contact">
    📧 <a href="mailto:sidneyppratt@gmail.com" style="color:white;">sidneyppratt@gmail.com</a><br>
    🔗 <a href="https://linkedin.com/in/sidney-pratt" target="_blank" style="color:white;">linkedin.com/in/sidney-pratt</a><br>
    💻 <a href="https://github.com/sidneyppratt-svg" target="_blank" style="color:white;">github.com/sidneyppratt-svg</a><br>
    🌐 <a href="https://sidneyppratt.com" target="_blank" style="color:white;">sidneyppratt.com</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TOP NAV — sticky, compact, always visible
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Remove top padding from main block */
    .block-container {
        padding-top: 0.5rem !important;
    }
    /* Tighten radio button spacing */
    div[data-testid="stRadio"] > div {
        gap: 0.5rem;
    }
    div[data-testid="stRadio"] label {
        font-size: 14px !important;
        padding: 4px 12px !important;
        border-radius: 6px !important;
    }
    /* Freeze the nav bar — fixed to top of viewport */
    div[data-testid="stRadio"] {
        position: fixed;
        top: 2.75rem;
        z-index: 9999;
        background-color: #FFFFFF;
        padding: 6px 2rem 6px 2rem;
        border-bottom: 1px solid #DDDDDD;
        left: 21rem;
        right: 0;
    }
    /* Push all main content down below the fixed nav */
    section[data-testid="stMainBlockContainer"] > div:first-child {
        padding-top: 4rem !important;
    }
    /* Style model buttons as full cards */
    div[data-testid="stButton"] button {
        background: #F9F9F9 !important;
        border: 1px solid #444444 !important;
        border-radius: 12px !important;
        color: #333333 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        padding: 1rem 0.75rem !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: none !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
        height: unset !important;
        min-height: unset !important;
        max-height: unset !important;
        line-height: 1.5 !important;
        display: block !important;
        transition: background 0.15s ease, border-color 0.15s ease !important;
    }
    div[data-testid="stButton"] button p {
        white-space: normal !important;
        word-break: break-word !important;
    }
    div[data-testid="stButton"] button:hover {
        background: #EFEFEF !important;
        border-color: #111111 !important;
        box-shadow: none !important;
        color: #111111 !important;
    }
</style>
""", unsafe_allow_html=True)

page = st.radio("", ["About", "Resume", "AI Finance", "Other Projects"],
    horizontal=True,
    label_visibility="collapsed")

st.markdown("<hr style='margin-top:0.2rem; margin-bottom:0rem;'>",
    unsafe_allow_html=True)
st.markdown("<div style='padding-top:2rem;'></div>",
    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ABOUT (opening page)
# ══════════════════════════════════════════════════════════════
if page == "About":
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    st.markdown("# Sidney Pratt")
    st.markdown("""
    <div style="margin-bottom:0.75rem;">
        <span class="tag">Finance & Economics</span>
        <span class="tag">AI Researcher</span>
        <span class="tag">ACHA D1 Hockey</span>
        <span class="tag">World Explorer</span>
    </div>
    """, unsafe_allow_html=True)



    st.markdown("""
    <div class="seeking-card">
        <h4>Currently Seeking</h4>
        <p>
        I am currently seeking an internship with a hedge fund, investment
        firm, or wealth management team where I can learn directly from
        professionals working in the markets. I'm especially interested in
        supporting a trading or investment desk through market research,
        quantitative analysis, portfolio monitoring, and data-driven
        projects. I'm looking for an opportunity where I can contribute,
        learn quickly, and continue developing my understanding of markets
        while applying my skills in finance, economics, Python, and
        quantitative research.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="card">
        <p>
        I'm a Finance and Economics student at Western Michigan University
        with a curiosity for how markets, data, and technology interact.
        I enjoy digging into financial and economic questions, working with
        data in Python and SQL, and building projects that turn complex
        information into something practical and understandable.
        </p>
        <p>
        As I continue developing my Python and quantitative skills, I've
        embraced AI tools such as Claude as part of my learning and
        development process. I use AI to help explore unfamiliar concepts,
        troubleshoot code, refine ideas, and accelerate the process of
        turning an idea into a working project. I see these tools as a way
        to learn faster and build more ambitious projects while continuing
        to develop my own technical foundation and understanding.
        </p>
        <p>
        A big part of who I am comes from experiences outside the classroom.
        As an ACHA D1 hockey player, I've learned the importance of
        discipline, consistency, accountability, and being someone your
        teammates can rely on. My experiences volunteering in places like
        the Peruvian Amazon and Tanzania have also pushed me outside my
        comfort zone and taught me to adapt to new environments and
        perspectives. In Tanzania, I worked with a group to complete the
        challenge of summiting Mount Kilimanjaro, where supporting one
        another through the difficult moments was just as important as
        reaching the summit itself.
        </p>
        <p>
        I've also had the opportunity to explore finance and economics
        through research, quantitative projects, and hands-on work. From
        building financial models that monitor yield curves and credit
        markets to contributing to economic research at the American
        Institute for Economic Research, I've enjoyed finding ways to
        combine analytical thinking with real-world problems.
        </p>
        <p>
        I'm always looking to learn, take on new challenges, and surround
        myself with people who push me to improve. Long term, I'm interested
        in building a career at the intersection of finance, economics,
        technology, and quantitative research.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RESUME
# ══════════════════════════════════════════════════════════════
elif page == "Resume":
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    st.markdown("# Resume")
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <h3>Education</h3>
        <p>
        <b>Western Michigan University</b> | Kalamazoo, MI<br>
        Double Major in Finance and Economics<br>
        Expected Graduation: May 2029 | GPA: 3.25
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3>Certifications</h3>
        <p>
        MIT Professional Education — Forecasting Future Technologies<br>
        NPR — Economic History Summer School<br>
        Coursera — Python & SQL for Finance
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3>Experience</h3>
        <p>
        <b>Intern | American Institute of Economic Research (AIER)</b><br>
        February 2026 – April 2026 | Great Barrington, MA<br>
        Contributed to economic research and policy analysis through
        data collection, literature review, and analytical support.
        Translated findings into written materials and presented
        policy research to the broader team.
        </p>
        <br>
        <p>
        <b>Sales Associate | Next Gen Exposure</b><br>
        August 2026 – October 2026 | Kalamazoo, MI<br>
        Trained in direct-to-consumer sales representing AT&T within
        a high-traffic Costco environment.
        </p>
        <br>
        <p>
        <b>Assistant Coach | San Francisco Sabercats Hockey Club</b><br>
        May 2025 – July 2025 | San Francisco, CA<br>
        Supported player development, game strategy, and team coordination.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Technical Skills</h3>
            <p>
            Python (pandas, NumPy, matplotlib, scikit-learn)<br>
            SQL<br>Microsoft Office Suite<br>
            Streamlit | GitHub<br>
            Financial Analysis<br>AI-Assisted Quantitative Research
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Activities</h3>
            <p>
            ACHA D1 Hockey | Western Michigan University<br>
            Pi Kappa Alpha Fraternity<br>
            Northern Cyclones Financial Club — Co-Founder<br>
            SPuRS Advanced Leadership Pillar
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h3>Volunteer & International Service</h3>
        <p>
        <b>SF-Marin Food Bank</b> — Organized food donations and
        community distribution<br><br>
        <b>Junglekeepers – Tamandua Expeditions</b> — Amazon
        rainforest conservation patrols<br><br>
        <b>Kilimanjaro Challenge</b> — Volunteered at orphanage
        and summited Mt. Kilimanjaro
        </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# AI RESEARCH
# ══════════════════════════════════════════════════════════════
elif page == "AI Finance":
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    st.markdown("# AI Finance")
    st.markdown("""
    <p style="color:#333333; font-size:16px;">
    Using machine learning to find signals in financial markets
    and solve real world problems.
    Each model is built on real data and fully interactive.
    </p>
    <p style="color:#666666; font-size:13px; font-style:italic; font-weight:700; margin-top:-0.4rem;">
    For educational and research purposes only. Not investment advice.
    </p>
    """, unsafe_allow_html=True)

    # Model selection cards — full card is the button
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        m1 = st.button("Yield Curve Monitor",
            key="btn_yc", use_container_width=True)
    with c2:
        m2 = st.button("Regime Detector",
            key="btn_rd", use_container_width=True)
    with c3:
        m3 = st.button("Credit Spread Monitor",
            key="btn_cs", use_container_width=True)
    with c4:
        m4 = st.button("Mortgage Market Monitor",
            key="btn_mm", use_container_width=True)

    # Session state to track which model is open
    finance_models = ["Yield Curve Monitor",
        "Multi-Asset Market Regime Detector",
        "Credit Spread Monitor", "Mortgage Market Monitor"]
    if st.session_state.get("model") not in finance_models:
        st.session_state.model = "Yield Curve Monitor"
    if m1: st.session_state.model = "Yield Curve Monitor"
    if m2: st.session_state.model = "Multi-Asset Market Regime Detector"
    if m3: st.session_state.model = "Credit Spread Monitor"
    if m4: st.session_state.model = "Mortgage Market Monitor"

    model = st.session_state.model
    st.markdown("---")

# ══════════════════════════════════════════════════════════════
# MODEL 1 — YIELD CURVE MONITOR
# ══════════════════════════════════════════════════════════════
    if model == "Yield Curve Monitor":
        title_col, card_col = st.columns([3, 2])
        with title_col:
            st.markdown("## Yield Curve Monitor")
            st.markdown("*Fixed Income Relative Value Tool | Sidney Pratt*")
        with card_col:
            yc_card = st.empty()
            yc_card.markdown(RESULTS_LOADING, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the US Treasury yield curve across four maturities — 3-month,
            5-year, 10-year, and 30-year — and classifies the current regime as Steep, Normal,
            Flat, Inverted, or Deeply Inverted based on the classic 10Y minus 3M spread.
            Built specifically to complement a fixed income relative value research portfolio.
            The yield curve is one of the most closely watched indicators on fixed income
            trading desks — rates, credit, and mortgages.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Live Treasury yield data, refreshed automatically<br>
            • Regime classification across 5 curve states — Steep, Normal, Flat, Inverted, Deeply Inverted<br>
            • Plain language interpretation of what the curve is saying<br>
            • Dynamic signal and strategy that updates with the regime<br>
            • 30-day trend detection — steepening or flattening<br>
            • Percentile ranking and comparison with the long-run average<br>
            • Backtest of a TLT bond strategy, 2003-2026, in the full research notebook
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Treasury Yields:</b> Daily US Treasury yields from Yahoo Finance — tickers
            ^IRX (13-week / 3-Month), ^FVX (5-Year), ^TNX (10-Year), ^TYX (30-Year).<br><br>
            <b>Accuracy:</b> Real market yields from Cboe's Treasury yield indexes. They closely
            track official Treasury rates; small differences from the Treasury Department's
            published curve are normal because of timing and methodology.<br><br>
            <b>Key Spread:</b> 10Y minus 3M — the spread used in the New York Fed's recession
            probability model.<br><br>
            <b>Backtest:</b> TLT ETF price data from Yahoo Finance, in the full research notebook.<br><br>
            All calculations performed in Python using pandas and NumPy.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                The yield curve is one of the most cited indicators in fixed income markets.
                Rates, credit, and mortgage desks track the 10Y minus 3M spread because it has
                historically signaled recessions and shifts in Fed policy.<br><br>
                An inversion of this spread has preceded every US recession since the late 1960s,
                although the time between inversion and recession has varied widely. The 2022-23
                inversion was the deepest since the early 1980s, with the spread falling below -1.50%.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads daily US Treasury yields across four maturities and calculates the
                10Y minus 3M spread.<br><br>
                Each day is classified into a regime using that day's spread. A 21-day rolling
                average is shown on the spread chart to smooth daily noise and show the trend.<br><br>
                The strategy signal holds TLT in Normal and Steep regimes and moves to cash in
                Flat, Inverted, and Deeply Inverted regimes. The full research notebook backtests
                this strategy from 2003 to present, using the prior day's signal to avoid lookahead bias.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Regime Classification</h3>
            <p><b>STEEP</b> (10Y minus 3M above +1.50%) — Long-term rates are significantly higher than short-term rates. The market expects strong future economic growth. Banks earn wide margins borrowing short and lending long. Often seen early in economic recoveries. → <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br><b>NORMAL</b> (+0.50% to +1.50%) — The curve has its typical upward slope. Short-term rates are lower than long-term rates as expected. The economy is healthy with no recession signals. The most common regime. → <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br><b>FLAT</b> (0% to +0.50%) — Short and long-term rates are nearly equal. The market is uncertain about the future. Banks earn little margin. Often a transition zone between healthy and inverted. A warning sign that the economy may be slowing. → <span style="color:#E65100; font-weight:bold;">MOVE TO CASH</span><br><br><b>INVERTED</b> (-0.50% to 0%) — Short-term rates are higher than long-term rates. This is abnormal and historically the most reliable recession predictor. Means the market expects the Fed will cut rates sharply in the future because the economy is slowing. Every major US recession since 1970 was preceded by an inversion. → <span style="color:#C62828; font-weight:bold;">MOVE TO CASH</span><br><br><b>DEEPLY INVERTED</b> (below -0.50%) — The most extreme inversion level. Short-term rates are significantly above long-term rates. The Fed has tightened aggressively and the market expects a hard landing. The 2022-23 inversion fell below -1.50% — the deepest since the early 1980s. High alert. → <span style="color:#B71C1C; font-weight:bold;">MOVE TO CASH</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Refresh the Model")
        col1, col2 = st.columns(2)
        with col1:
            yc_start = st.date_input("Start Date",
                value=datetime.date(2000, 1, 1), key="yc_start")
        with col2:
            yc_end = st.date_input("End Date",
                value=datetime.date.today(), key="yc_end")
        st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)

        if st.button("↻ Refresh the Model", key="refresh_yc"):
            refresh_data()
        if True:  # runs automatically on page load, no click needed
            with st.spinner("Downloading Treasury yield data..."):
                tickers = {
                    '3M':  '^IRX',
                    '5Y':  '^FVX',
                    '10Y': '^TNX',
                    '30Y': '^TYX',
                }
                yc_yields = pd.DataFrame()
                for name, ticker in tickers.items():
                    data = cached_yf_download(ticker,
                        start=str(yc_start),
                        end=str(yc_end),
                        auto_adjust=True,
                        progress=False)['Close']
                    yc_yields[name] = data
                yc_yields = yc_yields.dropna()
                yc_yields['10Y_3M']  = yc_yields['10Y'] - yc_yields['3M']
                yc_yields['spread_smooth'] = \
                    yc_yields['10Y_3M'].rolling(21).mean()

                def classify_regime(spread):
                    if spread < -0.50:   return 'DEEPLY INVERTED'
                    elif spread < 0:     return 'INVERTED'
                    elif spread < 0.50:  return 'FLAT'
                    elif spread < 1.50:  return 'NORMAL'
                    else:                return 'STEEP'

                yc_yields['regime'] = \
                    yc_yields['10Y_3M'].apply(classify_regime)

                current_spread = float(yc_yields['10Y_3M'].iloc[-1])
                current_regime = yc_yields['regime'].iloc[-1]
                current_3m     = float(yc_yields['3M'].iloc[-1])
                current_5y     = float(yc_yields['5Y'].iloc[-1])
                current_10y    = float(yc_yields['10Y'].iloc[-1])
                current_30y    = float(yc_yields['30Y'].iloc[-1])
                current_date   = yc_yields.index[-1].strftime('%B %d, %Y')
                pct_rank       = float(
                    (yc_yields['10Y_3M'] < current_spread).mean() * 100)
                avg_spread     = float(yc_yields['10Y_3M'].mean())
                trend_30d      = float(yc_yields['10Y_3M'].iloc[-1] -
                                       yc_yields['10Y_3M'].iloc[-22]) \
                                 if len(yc_yields) > 22 else 0.0

            _c = SIGNAL_GREEN if current_regime in ['NORMAL', 'STEEP'] else (SIGNAL_AMBER if current_regime == 'FLAT' else SIGNAL_RED)
            yc_card.markdown(results_card(current_date, [
                ("Regime", current_regime, _c),
                ("10Y minus 3M", f"{current_spread:+.2f}%", SIGNAL_TEXT),
                ("Signal", "HOLD TLT" if current_regime in ['NORMAL', 'STEEP'] else "MOVE TO CASH", _c),
            ]), unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Signal")
            if current_regime in ['NORMAL', 'STEEP']:
                st.success(f"✅ {current_regime} — As of {current_date} "
                           f"the yield curve is healthy. "
                           f"10Y minus 3M: {current_spread:+.2f}%")
            elif current_regime == 'FLAT':
                st.warning(f"⚠️ {current_regime} — As of {current_date} "
                           f"the curve is in transition. "
                           f"10Y minus 3M: {current_spread:+.2f}%")
            else:
                st.error(f"🚨 {current_regime} — As of {current_date} "
                         f"the yield curve is inverted. "
                         f"10Y minus 3M: {current_spread:+.2f}%")

            st.markdown("### Strategy Signal")
            if current_regime in ['NORMAL', 'STEEP']:
                st.success("Model signal: HOLD TLT — in this regime the strategy holds long-duration Treasuries (TLT).")
            elif current_regime == 'FLAT':
                st.warning("Model signal: MOVE TO CASH — the curve is in a transition zone, where the strategy steps out of long-duration bonds.")
            else:
                st.error("Model signal: MOVE TO CASH — the strategy steps out of long-duration bonds during inversions.")

            st.markdown("---")
            st.markdown("### Results")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("3-Month Yield",  f"{current_3m:.2f}%")
            m2.metric("5-Year Yield",   f"{current_5y:.2f}%")
            m3.metric("10-Year Yield",  f"{current_10y:.2f}%")
            m4.metric("30-Year Yield",  f"{current_30y:.2f}%")

            s1, s2, s3, s4 = st.columns(4)
            s1.metric("10Y minus 3M",
                f"{current_spread:+.2f}%", "Key spread")
            s2.metric("Percentile",
                ordinal(pct_rank), "vs history")
            s3.metric("30-Day Trend",
                f"{trend_30d:+.2f}%",
                "Steepening" if trend_30d > 0 else "Flattening")
            s4.metric("vs Average",
                f"{current_spread - avg_spread:+.2f}%",
                f"Avg: {avg_spread:.2f}%")

            st.markdown("---")
            st.markdown("### Charts")
            fig, axes = plt.subplots(3, 1, figsize=(13, 13))
            fig.patch.set_facecolor('#FFFFFF')
            fig.suptitle('Yield Curve Monitor',
                fontsize=15, fontweight='bold',
                color='#222222', y=0.99)
            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333', labelsize=9)
                for spine in ax.spines.values():
                    spine.set_edgecolor('#DDDDDD')
                ax.grid(axis='y', color='#EEEEEE', linewidth=0.8)
                ax.grid(axis='x', color='#EEEEEE', linewidth=0.5, alpha=0.5)
            axes[0].plot(yc_yields.index, yc_yields['10Y'],
                color='#1A237E', linewidth=1.5, label='10-Year')
            axes[0].plot(yc_yields.index, yc_yields['3M'],
                color='#B71C1C', linewidth=1.5, label='3-Month')
            axes[0].plot(yc_yields.index, yc_yields['30Y'],
                color='#2E7D32', linewidth=1.0,
                linestyle='--', alpha=0.7, label='30-Year')
            axes[0].fill_between(yc_yields.index,
                yc_yields['3M'], yc_yields['10Y'],
                where=yc_yields['10Y'] >= yc_yields['3M'],
                color='#2E7D32', alpha=0.08, label='Normal')
            axes[0].fill_between(yc_yields.index,
                yc_yields['3M'], yc_yields['10Y'],
                where=yc_yields['10Y'] < yc_yields['3M'],
                color='#C62828', alpha=0.15, label='Inverted')
            axes[0].set_title('Treasury Yields — 3M, 10Y, 30Y',
                color='#333333', fontsize=12, fontweight='bold')
            axes[0].set_ylabel('Yield (%)', color='#333333')
            axes[0].legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)
            axes[0].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
            spread_series = yc_yields['10Y_3M']
            smooth_series = yc_yields['spread_smooth']
            axes[1].axhspan(1.50, 6.00, color='#1B5E20', alpha=0.08, label='Steep')
            axes[1].axhspan(0.50, 1.50, color='#2E7D32', alpha=0.08, label='Normal')
            axes[1].axhspan(-0.50, 0.50, color='#F9A825', alpha=0.08, label='Flat')
            axes[1].axhspan(-3.00, -0.50, color='#C62828', alpha=0.10, label='Inverted')
            axes[1].axhline(y=0, color='#C62828', linewidth=1.5, linestyle='--', alpha=0.8)
            axes[1].plot(spread_series.index, spread_series.values,
                color='#CCCCCC', linewidth=0.6, alpha=0.7)
            axes[1].plot(smooth_series.index, smooth_series.values,
                color='#1A237E', linewidth=2.0,
                label='Spread (21-day avg)', zorder=4)
            axes[1].scatter(yc_yields.index[-1], spread_series.iloc[-1],
                color='#1A237E', s=80, zorder=5)
            axes[1].annotate(
                f'  Today: {spread_series.iloc[-1]:.2f}%',
                xy=(yc_yields.index[-1], spread_series.iloc[-1]),
                fontsize=8, color='#1A237E', fontweight='bold')
            axes[1].set_title('10Y minus 3M Spread — Inversion Monitor',
                color='#333333', fontsize=12, fontweight='bold')
            axes[1].set_ylabel('Spread (%)', color='#333333')
            axes[1].legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)
            axes[1].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
            regime_colors_fill = {
                'STEEP':           '#1B5E20',
                'NORMAL':          '#2E7D32',
                'FLAT':            '#F9A825',
                'INVERTED':        '#E64A19',
                'DEEPLY INVERTED': '#B71C1C',
            }
            for regime, rcolor in regime_colors_fill.items():
                mask = yc_yields['regime'] == regime
                axes[2].fill_between(yc_yields.index, 0, 1,
                    where=mask, color=rcolor, alpha=0.7, label=regime)
            axes[2].set_title('Regime Timeline — STEEP to DEEPLY INVERTED',
                color='#333333', fontsize=12, fontweight='bold')
            axes[2].set_yticks([])
            axes[2].set_ylim(0, 1)
            axes[2].legend(facecolor='#F9F9F9', labelcolor='#333333',
                fontsize=8, loc='lower right', ncol=5)
            plt.tight_layout(pad=2.5)
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Yield Curve Monitor including all code,
            charts, backtest results, and analysis on GitHub:<br><br>
            github.com/sidneyppratt-svg/yield-curve-monitor
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MODEL 2 — MULTI-ASSET MARKET REGIME DETECTOR
# ══════════════════════════════════════════════════════════════
    elif model == "Multi-Asset Market Regime Detector":
        title_col, card_col = st.columns([3, 2])
        with title_col:
            st.markdown("## Multi-Asset Market Regime Detector")
            st.markdown("*Cross-Asset Quantitative Research Tool | Sidney Pratt*")
        with card_col:
            rd_card = st.empty()
            rd_card.markdown(RESULTS_LOADING, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model uses unsupervised machine learning to detect
            whether markets are in a RISK-ON or RISK-OFF regime by
            analyzing four asset classes simultaneously — US Equities
            (SPY), Investment Grade Bonds (AGG), High Yield Credit
            (HYG), and Gold (GLD).<br><br>
            Rather than looking at one asset in isolation the model
            finds hidden patterns across all four asset classes at
            once — the same way professional cross-asset traders
            think about markets. Built on 12 years of real daily
            price data from 2014 to 2026.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Live multi-asset price data, refreshed automatically<br>
            • Gaussian Mixture Model — unsupervised machine learning<br>
            • Simultaneous analysis of four asset classes<br>
            • RISK-ON and RISK-OFF regime classification<br>
            • 21-day rolling return smoothing to filter daily noise<br>
            • Backtest of a SPY strategy using regime signals, compared with buy and hold<br>
            • Portfolio growth chart and regime timeline
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>SPY (US Equities):</b> SPDR S&P 500 ETF — Yahoo Finance.<br><br>
            <b>AGG (Investment Grade Bonds):</b> iShares Core US Aggregate Bond ETF — Yahoo Finance.<br><br>
            <b>HYG (High Yield Credit):</b> iShares iBoxx High Yield Corporate Bond ETF — Yahoo Finance.<br><br>
            <b>GLD (Gold):</b> SPDR Gold Shares ETF — Yahoo Finance.<br><br>
            <b>Accuracy:</b> Real daily market prices from Yahoo Finance, adjusted for dividends and splits.<br><br>
            <b>Model:</b> Gaussian Mixture Model from scikit-learn. Unsupervised — no labels used during training.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                Markets do not move in isolation. When stress hits it often shows up across
                several asset classes at once — stocks fall, credit weakens, and safe havens like
                gold and high-quality bonds attract buyers. A model that watches only one asset
                misses the full picture.<br><br>
                This model looks for those cross-asset patterns using machine learning instead of
                hand-written rules. The algorithm finds the two regimes itself from about 12 years
                of real data.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads daily prices for SPY, AGG, HYG, and GLD and calculates 21-day rolling
                mean returns for each asset to smooth noise.<br><br>
                A Gaussian Mixture Model finds two clusters in the four-dimensional return data.
                The cluster with higher average SPY returns is RISK-ON; the other is RISK-OFF.<br><br>
                The backtest holds SPY during RISK-ON and cash (0% return) during RISK-OFF, using
                the prior day's signal. The Sharpe ratio shown is annual return divided by annual
                volatility, without subtracting a risk-free rate.<br><br>
                <b>Limitations:</b> the model is fit on the full date range, so the backtest is
                in-sample and likely looks better than real-time trading would. It also ignores
                trading costs.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Regime Classification</h3>
            <p><b>RISK-ON</b> — Investors are comfortable taking risk. All four asset classes are behaving normally — stocks are rising, high yield credit is performing well, and there is no unusual demand for safe havens like gold or government bonds. Credit spreads are typically calm in this environment. Model signal: stay invested in SPY.<br><br><b>RISK-OFF</b> — Investors are pulling back from risk. Stress is showing up across multiple asset classes simultaneously — stocks falling, high yield credit underperforming investment grade, and demand rising for safe havens like gold and government bonds. Model signal: move to cash.<br><br><b>What makes this model different:</b> Most indicators watch one asset. This model watches four at once. A single bad day in stocks does not trigger RISK-OFF. What triggers it is when stocks, credit, and safe haven assets all move together in a stress pattern — exactly what happens during real market crises.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Asset Classes Covered</h3>
            <p><b>SPY — US Equities:</b> S&P 500 ETF — the broadest measure of US stock market performance. Rises in RISK-ON, falls sharply in RISK-OFF. The primary return driver in this model.<br><br><b>AGG — Investment Grade Bonds:</b> High quality corporate and government bonds. Often rises during RISK-OFF as investors flee to safety. Acts as the counter-weight to equities.<br><br><b>HYG — High Yield Credit:</b> Riskier corporate bonds from companies with lower credit ratings. Falls sharply during stress because investors demand more compensation for default risk. Can show stress before stocks do.<br><br><b>GLD — Gold:</b> The classic safe haven. Spikes during geopolitical stress, inflation fears, and financial crises. When gold and bonds both rise while stocks fall, that is a strong RISK-OFF signal.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Refresh the Model")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date",
                value=datetime.date(2014, 1, 1))
        with col2:
            end_date = st.date_input("End Date",
                value=datetime.date.today())
        st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)

        if st.button("↻ Refresh the Model", key="refresh_rd"):
            refresh_data()
        if True:  # runs automatically on page load, no click needed
            with st.spinner("Downloading data and running AI model..."):
                tickers = ['SPY', 'AGG', 'HYG', 'GLD']
                prices = cached_yf_download(tickers,
                    start=str(start_date),
                    end=str(end_date),
                    auto_adjust=True)['Close']
                prices = prices.dropna()
                returns = prices.pct_change().dropna()
                smooth = returns.rolling(21).mean().dropna()
                gmm = GaussianMixture(n_components=2,
                    covariance_type='full', random_state=42)
                smooth['regime'] = gmm.fit_predict(
                    smooth[['SPY', 'AGG', 'HYG', 'GLD']])
                equity_by_regime = smooth.groupby('regime')['SPY'].mean()
                risk_on  = int(equity_by_regime.idxmax())
                risk_off = int(equity_by_regime.idxmin())
                smooth['label'] = smooth['regime'].map({
                    risk_on: 'RISK-ON', risk_off: 'RISK-OFF'})
                spy_returns = returns['SPY'].loc[smooth.index]
                signal = (smooth['label'] == 'RISK-ON').astype(int)
                strat  = signal.shift(1) * spy_returns
                strat  = strat.dropna()
                bh     = spy_returns.loc[strat.index]
                def get_metrics(r):
                    r   = r.dropna()
                    cum = (1 + r).cumprod()
                    total   = float(cum.iloc[-1]) - 1
                    ann_ret = float((1 + total) ** (252/len(r)) - 1)
                    ann_vol = float(r.std() * np.sqrt(252))
                    sharpe  = float(ann_ret/ann_vol) if ann_vol > 0 else 0.0
                    max_dd  = float((cum/cum.cummax()-1).min())
                    return cum, total, ann_ret, ann_vol, sharpe, max_dd
                cum_s, tot_s, ret_s, vol_s, sh_s, dd_s = get_metrics(strat)
                cum_b, tot_b, ret_b, vol_b, sh_b, dd_b = get_metrics(bh)
                latest      = smooth['label'].iloc[-1]
                latest_date = smooth.index[-1].strftime('%B %d, %Y')
                risk_off_pct = float(
                    (smooth['label'] == 'RISK-OFF').mean() * 100)

            _c = SIGNAL_GREEN if latest == 'RISK-ON' else SIGNAL_RED
            rd_card.markdown(results_card(latest_date, [
                ("Regime", latest, _c),
                ("Signal", "STAY INVESTED" if latest == 'RISK-ON' else "MOVE TO CASH", _c),
                ("Sharpe (strategy)", f"{sh_s:.2f}", SIGNAL_TEXT),
            ]), unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Signal")
            if latest == 'RISK-ON':
                st.success(f"✅ RISK-ON — As of {latest_date} all four "
                           f"asset classes are behaving normally. Markets are calm.")
            else:
                st.error(f"🚨 RISK-OFF — As of {latest_date} stress "
                         f"detected across multiple asset classes.")

            st.markdown("### Strategy Signal")
            if latest == 'RISK-ON':
                st.success("Model signal: STAY INVESTED — the strategy holds SPY "
                           "when cross-asset conditions look calm.")
            else:
                st.error("Model signal: MOVE TO CASH — the strategy steps out "
                         "of SPY when cross-asset stress is detected.")

            st.markdown("---")
            st.markdown("### Results")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total Return", f"{tot_s:.1%}", f"{tot_s-tot_b:+.1%} vs BH")
            c2.metric("Ann. Return",  f"{ret_s:.1%}", f"{ret_s-ret_b:+.1%} vs BH")
            c3.metric("Volatility",   f"{vol_s:.1%}", f"{vol_s-vol_b:+.1%} vs BH")
            c4.metric("Sharpe Ratio", f"{sh_s:.2f}",  f"{sh_s-sh_b:+.2f} vs BH")
            c5.metric("Max Drawdown", f"{dd_s:.1%}",  f"{dd_s-dd_b:+.1%} vs BH")

            st.markdown("---")
            st.markdown("### Charts")
            fig, axes = plt.subplots(2, 1, figsize=(12, 10))
            fig.patch.set_facecolor('#FFFFFF')
            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#CCCCCC')
            (cum_s * 100).plot(ax=axes[0], color='#333333',
                linewidth=2, label='AI Strategy')
            (cum_b * 100).plot(ax=axes[0], color='#AAAAAA',
                linewidth=1.5, linestyle='--', label='Buy & Hold SPY')
            axes[0].set_title('Portfolio Growth — $100 Invested',
                color='#333333', fontsize=13, fontweight='bold')
            axes[0].legend(facecolor='#F9F9F9', labelcolor='#333333')
            axes[0].set_ylabel('Value ($)', color='#333333')
            axes[0].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'${x:.0f}'))
            risk_on_mask  = smooth['label'] == 'RISK-ON'
            risk_off_mask = smooth['label'] == 'RISK-OFF'
            spy_price = prices['SPY'].loc[smooth.index]
            spy_norm  = (spy_price - spy_price.min()) / \
                        (spy_price.max() - spy_price.min())
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_on_mask,
                color='#2E7D32', alpha=0.25, label='RISK-ON')
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_off_mask,
                color='#C62828', alpha=0.45, label='RISK-OFF')
            axes[1].plot(spy_norm.index, spy_norm.values,
                color='#1A237E', linewidth=1.8,
                label='SPY Price (normalized)', zorder=3)
            axes[1].set_title(
                'Regime Detection — SPY Price with RISK-ON / RISK-OFF',
                color='#333333', fontsize=13, fontweight='bold')
            axes[1].set_yticks([])
            axes[1].set_ylim(0, 1.05)
            axes[1].legend(facecolor='#F9F9F9', labelcolor='#333333',
                fontsize=9, loc='lower right')
            axes[1].grid(axis='x', color='#DDDDDD', linewidth=0.5, alpha=0.5)
            plt.tight_layout(pad=2.0)
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Multi-Asset Market Regime Detector
            including all code, charts, backtest results, and
            analysis on GitHub:<br><br>
            github.com/sidneyppratt-svg/quant-regime-detector
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MODEL 3 — CREDIT SPREAD MONITOR (FRED OAS)
# ══════════════════════════════════════════════════════════════
    elif model == "Credit Spread Monitor":
        title_col, card_col = st.columns([3, 2])
        with title_col:
            st.markdown("## Credit Spread Monitor")
            st.markdown("*Fixed Income Credit Research Tool | Sidney Pratt*")
        with card_col:
            cs_card = st.empty()
            cs_card.markdown(RESULTS_LOADING, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the ICE BofA US High Yield Option-Adjusted Spread (OAS) — a
            widely used benchmark for stress in the high yield bond market. The spread is
            converted into a stress score from 1 to 5 by ranking today's reading against its
            available history.<br><br>
            When high yield credit spreads widen it signals investors are demanding more
            compensation for credit risk — one of the key warning signals in fixed income
            markets.<br><br>
            <b>Data note:</b> since April 2026, FRED only provides the most recent three years
            of this series, so the model's history currently begins in 2023.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Official ICE BofA OAS data from FRED, refreshed automatically<br>
            • Credit stress score from 1 (very calm) to 5 (high stress)<br>
            • Percentile ranking against all readings in the available history<br>
            • OAS regime classification — Tight, Normal, Wide, Very Wide<br>
            • 21-day rolling average to smooth daily noise on the chart<br>
            • Three chart visualization — OAS over time, stress score, HYG vs LQD<br>
            • Dynamic signal and interpretation that updates automatically
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Primary Data:</b> ICE BofA US High Yield Index Option-Adjusted Spread (FRED
            series: BAMLH0A0HYM2), produced by ICE Data Indices and distributed through FRED,
            the St. Louis Fed's economic database, via the pandas-datareader library.<br><br>
            <b>Accuracy:</b> This is the official index data — not a proxy or approximation.<br><br>
            <b>History:</b> Since April 2026, FRED limits this series to a rolling three-year
            window, so percentiles and averages cover roughly the last three years.<br><br>
            <b>HYG & LQD:</b> ETF prices from Yahoo Finance used for the relative performance
            chart only — not for the OAS calculation.<br><br>
            <b>Stress Score:</b> Today's OAS ranked as a percentile against all readings in the
            available history, then split into five equal bins (score 1-5).
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                Credit spreads are one of the most important indicators in fixed income markets.
                When OAS widens it signals investors are demanding more compensation for default
                risk, and credit stress can appear before it shows up in stock prices.<br><br>
                Spreads widened sharply during the 2008 financial crisis, the 2011 euro debt crisis,
                the 2015-16 oil price crash, the March 2020 COVID crash, and the April 2025 tariff shock.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads the ICE BofA OAS directly from FRED (BAMLH0A0HYM2) — the option-adjusted
                spread between US high yield bonds and US Treasuries.<br><br>
                Today's spread is ranked as a percentile against all readings in the available
                history and converted into a stress score from 1 to 5 using five equal bins. The
                spread level is also labeled Tight, Normal, Wide, or Very Wide using fixed thresholds.<br><br>
                A 21-day rolling average smooths daily noise on the chart.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Stress Score & OAS Regime Classification</h3>
            <p>
            The OAS (Option-Adjusted Spread) is the extra yield investors demand to hold high yield bonds instead of Treasuries. Think of it as the market's price for corporate default risk. When the OAS is low investors are relaxed. When it spikes investors are scared and demanding more compensation.<br><br>
            <b>Stress Score (relative):</b> based on where today ranks against the available history.<br><br>
            <b>Score 1 — VERY CALM</b> (bottom 20% of readings): Spreads are among the lowest in the period. Credit markets are relaxed. → <span style="color:#2E7D32; font-weight:bold;">RISK-ON</span><br><br>
            <b>Score 2 — CALM</b> (20th to 40th percentile): Healthy credit conditions with no signs of stress. → <span style="color:#2E7D32; font-weight:bold;">RISK-ON</span><br><br>
            <b>Score 3 — MODERATE</b> (40th to 60th percentile): Middle of the range. Worth monitoring for a trend. → <span style="color:#E65100; font-weight:bold;">NEUTRAL</span><br><br>
            <b>Score 4 — ELEVATED</b> (60th to 80th percentile): Spreads are higher than usual for the period. Investors are getting more cautious. → <span style="color:#C62828; font-weight:bold;">CAUTION</span><br><br>
            <b>Score 5 — HIGH STRESS</b> (top 20% of readings): Spreads are among the widest in the period. → <span style="color:#B71C1C; font-weight:bold;">RISK-OFF</span><br><br>
            <b>OAS Regime (absolute):</b> based on the spread level itself.<br><br>
            <b>TIGHT</b> (below 2.50%): Investors are very comfortable lending to risky companies. Default risk is priced at historically low levels.<br><br>
            <b>NORMAL</b> (2.50% to 3.50%): Typical credit conditions.<br><br>
            <b>WIDE</b> (3.50% to 5.00%): Credit stress is building. Investors are demanding significantly more compensation for default risk.<br><br>
            <b>VERY WIDE</b> (above 5.00%): Crisis-level spreads, seen during the 2008 financial crisis, the 2015-16 oil crash, and March 2020.<br><br>
            <b>Note:</b> because the stress score is relative, a high score means today is high compared with the recent history, even if the spread level itself is still in the Normal range.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Refresh the Model")
        # FRED only provides the last 3 years of this series, so default
        # the start date to exactly three years before today
        _today = datetime.date.today()
        try:
            cs_default_start = _today.replace(year=_today.year - 3)
        except ValueError:   # today is Feb 29
            cs_default_start = _today.replace(year=_today.year - 3, day=28)
        col1, col2 = st.columns(2)
        with col1:
            start_date_cs = st.date_input("Start Date",
                value=cs_default_start, key="cs_start")
        with col2:
            end_date_cs = st.date_input("End Date",
                value=datetime.date.today(), key="cs_end")
        st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)

        if st.button("↻ Refresh the Model", key="refresh_cs"):
            refresh_data()
        if True:  # runs automatically on page load, no click needed
            with st.spinner("Downloading ICE BofA OAS spread from FRED..."):

                # Pull real OAS spread from FRED
                oas = cached_fred("BAMLH0A0HYM2",
                    str(start_date_cs), str(end_date_cs))
                oas.columns = ["OAS_Spread"]

                # HYG and LQD for relative performance chart
                cs_prices = cached_yf_download(['HYG', 'LQD'],
                    start=str(start_date_cs),
                    end=str(end_date_cs),
                    auto_adjust=True)['Close'].dropna()
                cs_prices.columns = ['HYG', 'LQD']

                # Align OAS to trading days
                oas_aligned = oas.reindex(cs_prices.index, method="ffill").dropna()
                df = pd.concat([cs_prices, oas_aligned], axis=1).dropna()

                # Calculations
                df["OAS_bps"]       = df["OAS_Spread"] * 100
                df["OAS_Percentile"] = df["OAS_Spread"].rank(pct=True) * 100
                df["Stress_Score"]   = pd.cut(
                    df["OAS_Percentile"],
                    bins=[0, 20, 40, 60, 80, 100],
                    labels=[1, 2, 3, 4, 5]).astype(float)
                df["OAS_Smooth"]    = df["OAS_Spread"].rolling(21).mean()
                df = df.dropna()

                def classify_oas(oas):
                    if oas < 2.50:   return "TIGHT"
                    elif oas < 3.50: return "NORMAL"
                    elif oas < 5.00: return "WIDE"
                    else:            return "VERY WIDE"

                def classify_signal(score):
                    if score <= 2:   return "RISK-ON — Credit conditions healthy"
                    elif score == 3: return "NEUTRAL — Monitor closely"
                    elif score == 4: return "CAUTION — Spreads elevated vs recent history"
                    else:            return "RISK-OFF — Significant credit stress"

                cur_oas     = float(df["OAS_Spread"].iloc[-1])
                cur_bps     = float(df["OAS_bps"].iloc[-1])
                cur_pct     = float(df["OAS_Percentile"].iloc[-1])
                cur_score   = float(df["Stress_Score"].iloc[-1])
                cur_regime  = classify_oas(cur_oas)
                cur_signal  = classify_signal(cur_score)
                cur_date    = df.index[-1].strftime('%B %d, %Y')
                avg_oas     = float(df["OAS_Spread"].mean())
                max_oas     = float(df["OAS_Spread"].max())
                min_oas     = float(df["OAS_Spread"].min())
                max_date    = df["OAS_Spread"].idxmax().strftime('%B %Y')
                min_date    = df["OAS_Spread"].idxmin().strftime('%B %Y')
                oas_52w_high = float(df["OAS_Spread"].tail(252).max())
                oas_52w_low  = float(df["OAS_Spread"].tail(252).min())

                score_labels = {1:'Very Calm', 2:'Calm',
                    3:'Moderate', 4:'Elevated', 5:'High Stress'}
                cur_label = score_labels.get(int(cur_score), 'Unknown')

            _c = SIGNAL_GREEN if cur_score <= 2 else (SIGNAL_AMBER if cur_score == 3 else SIGNAL_RED)
            cs_card.markdown(results_card(cur_date, [
                ("Stress Score", f"{cur_score:.0f}/5 — {cur_label}", _c),
                ("OAS Spread", f"{cur_bps:.0f} bps", SIGNAL_TEXT),
                ("Signal", cur_signal.split(" — ")[0], _c),
            ]), unsafe_allow_html=True)

            st.markdown("---")

            # Signal
            st.markdown("### Signal")
            if cur_score <= 2:
                st.success(f"✅ {cur_label.upper()} — As of {cur_date} "
                           f"OAS is {cur_oas:.2f}% ({cur_bps:.0f} bps). "
                           f"Credit markets are calm. Stress score {cur_score:.0f}/5.")
            elif cur_score == 3:
                st.warning(f"⚠️ {cur_label.upper()} — As of {cur_date} "
                           f"OAS is {cur_oas:.2f}% ({cur_bps:.0f} bps). "
                           f"Stress score {cur_score:.0f}/5 — monitor closely.")
            else:
                st.error(f"🚨 {cur_label.upper()} — As of {cur_date} "
                         f"OAS is {cur_oas:.2f}% ({cur_bps:.0f} bps). "
                         f"Credit stress building. Stress score {cur_score:.0f}/5.")

            # Strategy Signal
            st.markdown("### Strategy Signal")
            if cur_score <= 2:
                st.success(f"Model signal: {cur_signal}")
            elif cur_score == 3:
                st.warning(f"Model signal: {cur_signal}")
            else:
                st.error(f"Model signal: {cur_signal}")

            # Results
            st.markdown("---")
            st.markdown("### Results")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("OAS Spread",    f"{cur_oas:.2f}%")
            m2.metric("OAS (bps)",     f"{cur_bps:.0f} bps")
            m3.metric("Stress Score",  f"{cur_score:.0f} / 5 — {cur_label}")
            m4.metric("Percentile",    ordinal(cur_pct), f"since {df.index.min().year}")

            # Historical Context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Historical Avg",   f"{avg_oas:.2f}%", f"since {df.index.min().year}")
            h2.metric("vs Average",       f"{cur_oas - avg_oas:+.2f}%")
            h3.metric(f"High Since {df.index.min().year}", f"{max_oas:.2f}%", max_date)
            h4.metric(f"Low Since {df.index.min().year}",  f"{min_oas:.2f}%", min_date)

            w1, w2 = st.columns(2)
            w1.metric("52-Week High OAS", f"{oas_52w_high:.2f}%")
            w2.metric("52-Week Low OAS",  f"{oas_52w_low:.2f}%")

            # Charts
            st.markdown("---")
            st.markdown("### Charts")
            fig = plt.figure(figsize=(14, 14))
            fig.patch.set_facecolor('#FFFFFF')
            gs   = gridspec.GridSpec(3, 1, figure=fig, hspace=0.35)
            axes = [fig.add_subplot(gs[i]) for i in range(3)]

            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333', labelsize=9)
                for spine in ax.spines.values():
                    spine.set_edgecolor('#DDDDDD')
                ax.grid(axis='y', color='#EEEEEE', linewidth=0.8)
                ax.grid(axis='x', color='#EEEEEE', linewidth=0.5, alpha=0.5)

            fig.suptitle("Credit Spread Monitor — ICE BofA OAS (FRED: BAMLH0A0HYM2)",
                fontsize=13, fontweight='bold', color='#222222', y=0.98)

            # Chart 1 — OAS over time
            ax = axes[0]
            ax.axhline(y=avg_oas, color='#666666', linewidth=1,
                linestyle='--', alpha=0.7, label=f'Avg: {avg_oas:.2f}%')
            ax.axhline(y=2.50, color='#2E7D32', linewidth=0.8,
                linestyle=':', alpha=0.6, label='TIGHT threshold (2.50%)')
            ax.axhline(y=3.50, color='#F9A825', linewidth=0.8,
                linestyle=':', alpha=0.6, label='WIDE threshold (3.50%)')
            ax.axhline(y=5.00, color='#C62828', linewidth=0.8,
                linestyle=':', alpha=0.6, label='VERY WIDE threshold (5.00%)')
            ax.plot(df.index, df["OAS_Spread"],
                color='#CCCCCC', linewidth=0.6, alpha=0.6)
            ax.plot(df["OAS_Smooth"].index, df["OAS_Smooth"].values,
                color='#1A237E', linewidth=2, label='OAS (21-day avg)', zorder=4)
            ax.scatter(df.index[-1], float(df["OAS_Smooth"].iloc[-1]),
                color='#1A237E', s=70, zorder=5)
            ax.annotate(f'  Today: {cur_oas:.2f}%',
                xy=(df.index[-1], float(df["OAS_Smooth"].iloc[-1])),
                fontsize=8, color='#1A237E', fontweight='bold')
            ax.set_title('ICE BofA US High Yield OAS Spread (FRED: BAMLH0A0HYM2)',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('OAS Spread (%)', color='#333333')
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))

            # Chart 2 — Stress score over time
            ax = axes[1]
            ax.axhspan(0,   1.5, color='#1B5E20', alpha=0.10, label='1 — Very Calm')
            ax.axhspan(1.5, 2.5, color='#2E7D32', alpha=0.10, label='2 — Calm')
            ax.axhspan(2.5, 3.5, color='#F9A825', alpha=0.10, label='3 — Moderate')
            ax.axhspan(3.5, 4.5, color='#E65100', alpha=0.10, label='4 — Elevated')
            ax.axhspan(4.5, 5.5, color='#C62828', alpha=0.12, label='5 — High Stress')
            ax.plot(df.index, df["Stress_Score"],
                color='#1A237E', linewidth=1.5, zorder=4)
            ax.scatter(df.index[-1], cur_score,
                color='#1A237E', s=70, zorder=5)
            ax.annotate(f'  Today: {cur_score:.0f}/5 — {cur_label}',
                xy=(df.index[-1], cur_score),
                fontsize=8, color='#1A237E', fontweight='bold')
            ax.set_title('Credit Stress Score (1 = Very Calm, 5 = High Stress)',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('Stress Score', color='#333333')
            ax.set_ylim(0, 6)
            ax.set_yticks([1, 2, 3, 4, 5])
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8, ncol=3)

            # Chart 3 — HYG vs LQD relative performance
            ax = axes[2]
            hyg_norm = (df["HYG"] / df["HYG"].iloc[0]) * 100
            lqd_norm = (df["LQD"] / df["LQD"].iloc[0]) * 100
            ax.plot(df.index, hyg_norm,
                color='#C62828', linewidth=1.5, label='HYG (High Yield)')
            ax.plot(df.index, lqd_norm,
                color='#1A237E', linewidth=1.5, label='LQD (Investment Grade)')
            ax.set_title('HYG vs LQD — Total Return Comparison (Base = 100)',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('Indexed Return (Base 100)', color='#333333')
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)

            plt.tight_layout(pad=2.5)
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Credit Spread Monitor including all code,
            charts, OAS analysis, and historical period breakdown on GitHub:<br><br>
            github.com/sidneyppratt-svg/credit-spread-monitor
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MODEL 4 — MORTGAGE MARKET MONITOR
# ══════════════════════════════════════════════════════════════
    elif model == "Mortgage Market Monitor":
        title_col, card_col = st.columns([3, 2])
        with title_col:
            st.markdown("## Mortgage Market Monitor")
            st.markdown("*Fixed Income Mortgage Research Tool | Sidney Pratt*")
        with card_col:
            mm_card = st.empty()
            mm_card.markdown(RESULTS_LOADING, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the official Freddie Mac 30-year fixed
            mortgage rate, the mortgage spread over the 10-year Treasury
            yield, and the refinancing environment, using the official
            mortgage rate from the Federal Reserve (FRED) and market data
            from Yahoo Finance.<br><br>
            The mortgage spread — the gap between the 30-year mortgage
            rate and the 10-year Treasury yield — is the key signal
            closely watched on mortgage trading desks. When the spread
            widens it signals stress in the MBS market. When it narrows
            it signals lender competition and easier credit conditions.
            Built on data from 2010 to present — weekly mortgage rates and daily market data.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Official Freddie Mac 30-year mortgage rate pulled live from FRED<br>
            • Mortgage spread calculated against the 10-year Treasury yield<br>
            • Spread regime classification — Tight, Normal, Wide, Very Wide<br>
            • Refinancing environment signal — Minimal, Some, Active, Wave<br>
            • Prepayment risk classification — Low, Moderate, High<br>
            • Percentile ranking against history (default start 2010)<br>
            • Three chart visualization — rates, spread regime, MBB vs AGG
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Primary Data:</b> Freddie Mac Primary Mortgage Market Survey (FRED series:
            MORTGAGE30US) — the official 30-year fixed mortgage rate, published weekly by
            Freddie Mac and distributed through FRED.<br><br>
            <b>Accuracy:</b> The official survey rate widely cited in financial news — not a
            proxy or approximation. Because it is weekly, each week's rate is carried forward
            to line up with daily market data.<br><br>
            <b>Treasury Yields:</b> 10-year (^TNX) and 30-year (^TYX) yields from Yahoo Finance,
            which closely track official Treasury rates.<br><br>
            <b>MBB & AGG:</b> ETF prices from Yahoo Finance used for the relative performance
            chart and MBB return metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                The mortgage spread is one of the key signals watched on mortgage trading desks.
                It helps show whether MBS are cheap or expensive relative to Treasuries, feeds into
                prepayment assumptions, and can signal stress in the housing finance system.<br><br>
                In late 2022, as the Fed raised rates aggressively, the spread rose above 3% — one of
                its widest levels since the 2008 crisis — showing how quickly it can move during
                rate hike cycles.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads the official Freddie Mac 30-year mortgage rate
                from FRED and the 10-year Treasury yield from Yahoo Finance.
                The mortgage spread is simply the difference between the two.<br><br>
                The spread is classified into four regimes based on
                historical thresholds. The refi signal compares today's
                rate to 12 months ago — a drop of 0.75%+ triggers Active
                Refi, 1.50%+ triggers a Refi Wave.<br><br>
                Prepayment risk is derived from combining the spread
                regime and the refi environment.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Regime Classification</h3>
            <p>The mortgage spread is the gap between the official 30-year mortgage rate and the 10-year Treasury yield. It represents the extra cost borrowers pay above the risk-free rate to compensate lenders for prepayment risk, credit risk, and servicing costs. A wider spread means mortgages are more expensive relative to Treasuries — a signal of stress or uncertainty in the housing finance market.<br><br><b>TIGHT (below 1.50%):</b> Lenders are competing aggressively for mortgage business. The extra cost of a mortgage above Treasuries is historically low. MBS are expensive relative to Treasuries — investors are accepting less compensation than usual for mortgage risk. Good for new homebuyers but less attractive for MBS investors buying at tight levels.<br><br><b>NORMAL (1.50% to 2.00%):</b> Mortgage risk is priced appropriately relative to Treasuries. The spread is in its historical average range. Lenders are earning a fair margin. Normal prepayment modeling assumptions apply. The most common regime — the market is functioning as expected.<br><br><b>WIDE (2.00% to 2.50%):</b> <span style="color:#E65100; font-weight:bold;">Lenders are demanding more compensation above Treasuries. This can reflect uncertainty about prepayment speeds, tighter bank balance sheets, or broader fixed income stress. MBS are cheap relative to Treasuries. Worth monitoring whether the widening is temporary or a sign of deeper stress.</span><br><br><b>VERY WIDE (above 2.50%):</b> <span style="color:#B71C1C; font-weight:bold;">Significant stress in the mortgage market. Lenders are demanding crisis-level compensation above Treasuries. This territory was seen during the 2008 financial crisis, COVID March 2020, and the November 2022 rate shock when the Fed was hiking aggressively. MBS are very cheap but duration risk is high.</span><br><br><b>MINIMAL REFI:</b> Current mortgage rates are not significantly below where they were 12 months ago. Most borrowers have little financial incentive to refinance. Prepayment speeds are near baseline, so MBS behave like longer-duration bonds.<br><br><b>SOME REFI:</b> Rates have fallen modestly. Some borrowers who were well above the current rate may refinance. Prepayment speeds are slightly above baseline.<br><br><b>ACTIVE REFI:</b> Rates have fallen meaningfully — more than 0.75% below a year ago. A meaningful portion of existing mortgages are in the money to refinance. Prepayment speeds are elevated. MBS duration is shortening.<br><br><b>REFI WAVE:</b> <span style="color:#B71C1C; font-weight:bold;">Rates have fallen more than 1.50% below a year ago. A large portion of the existing mortgage market can benefit from refinancing. Prepayment speeds are accelerating rapidly. MBS holders receive principal back much faster than expected — duration collapses. A major risk for MBS investors who bought at higher prices.</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Refresh the Model")
        col1, col2 = st.columns(2)
        with col1:
            start_date_mm = st.date_input("Start Date",
                value=datetime.date(2010, 1, 1), key="mm_start")
        with col2:
            end_date_mm = st.date_input("End Date",
                value=datetime.date.today(), key="mm_end")
        st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)

        if st.button("↻ Refresh the Model", key="refresh_mm"):
            refresh_data()
        if True:  # runs automatically on page load, no click needed
            with st.spinner("Downloading official Freddie Mac mortgage rate from FRED..."):

                # Official Freddie Mac 30-Year Fixed Mortgage Rate from FRED
                mortgage = cached_fred("MORTGAGE30US",
                    str(start_date_mm), str(end_date_mm))
                mortgage.columns = ["Mortgage_Rate"]

                # Treasury yields and ETFs from Yahoo Finance
                tnx = cached_yf_download("^TNX", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                tyx = cached_yf_download("^TYX", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                mbb = cached_yf_download("MBB", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                agg = cached_yf_download("AGG", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]

                prices = pd.concat([tnx, tyx, mbb, agg], axis=1).dropna()
                prices.columns = ["10Y_Treasury", "30Y_Treasury", "MBB", "AGG"]
                mortgage_aligned = mortgage.reindex(
                    prices.index, method="ffill").dropna()
                df_mm = pd.concat([prices, mortgage_aligned], axis=1).dropna()

                # Calculations
                df_mm["Mortgage_Spread"] = \
                    df_mm["Mortgage_Rate"] - df_mm["10Y_Treasury"]
                df_mm["Spread_Smooth"]   = \
                    df_mm["Mortgage_Spread"].rolling(21).mean()
                df_mm = df_mm.dropna()

                def classify_spread_mm(spread):
                    if spread < 1.50:   return "TIGHT"
                    elif spread < 2.00: return "NORMAL"
                    elif spread < 2.50: return "WIDE"
                    else:               return "VERY WIDE"

                def classify_refi_mm(rate, rate_12m):
                    if pd.isna(rate_12m): return "UNKNOWN"
                    drop = rate_12m - rate
                    if drop >= 1.50:   return "REFI WAVE"
                    elif drop >= 0.75: return "ACTIVE REFI"
                    elif drop >= 0.25: return "SOME REFI"
                    else:              return "MINIMAL REFI"

                def prepay_risk_mm(regime, refi):
                    if refi in ["REFI WAVE", "ACTIVE REFI"]: return "HIGH"
                    elif refi == "SOME REFI":                return "MODERATE"
                    elif regime == "TIGHT":                  return "MODERATE"
                    else:                                    return "LOW"

                df_mm["Spread_Regime"] = \
                    df_mm["Mortgage_Spread"].apply(classify_spread_mm)
                rate_12m = df_mm["Mortgage_Rate"].shift(252)
                df_mm["Refi_Signal"] = [
                    classify_refi_mm(row["Mortgage_Rate"], rate_12m.iloc[i])
                    for i, (_, row) in enumerate(df_mm.iterrows())
                ]
                df_mm["Prepay_Risk"] = [
                    prepay_risk_mm(row["Spread_Regime"], row["Refi_Signal"])
                    for _, row in df_mm.iterrows()
                ]

                cur_mort_mm    = float(df_mm["Mortgage_Rate"].iloc[-1])
                cur_10y_mm     = float(df_mm["10Y_Treasury"].iloc[-1])
                cur_30y_mm     = float(df_mm["30Y_Treasury"].iloc[-1])
                cur_spread_mm  = float(df_mm["Mortgage_Spread"].iloc[-1])
                avg_spread_mm  = float(df_mm["Mortgage_Spread"].mean())
                cur_regime_mm  = df_mm["Spread_Regime"].iloc[-1]
                cur_refi_mm    = df_mm["Refi_Signal"].iloc[-1]
                cur_prepay_mm  = df_mm["Prepay_Risk"].iloc[-1]
                cur_date_mm    = df_mm.index[-1].strftime('%B %d, %Y')
                pct_rank_mm    = float(
                    (df_mm["Mortgage_Spread"] < cur_spread_mm).mean() * 100)
                max_spread_mm  = float(df_mm["Mortgage_Spread"].max())
                min_spread_mm  = float(df_mm["Mortgage_Spread"].min())
                max_date_mm    = df_mm["Mortgage_Spread"].idxmax().strftime('%B %Y')
                min_date_mm    = df_mm["Mortgage_Spread"].idxmin().strftime('%B %Y')
                mbb_1m_mm      = float(
                    (df_mm["MBB"].iloc[-1]/df_mm["MBB"].iloc[-21]-1)*100)
                mbb_12m_mm     = float(
                    (df_mm["MBB"].iloc[-1]/df_mm["MBB"].iloc[-252]-1)*100)

            _cs = SIGNAL_GREEN if cur_regime_mm in ["TIGHT", "NORMAL"] else (SIGNAL_AMBER if cur_regime_mm == "WIDE" else SIGNAL_RED)
            _cr = SIGNAL_GREEN if cur_refi_mm in ["MINIMAL REFI", "SOME REFI"] else (SIGNAL_AMBER if cur_refi_mm == "ACTIVE REFI" else SIGNAL_RED)
            mm_card.markdown(results_card(cur_date_mm, [
                ("30Y Mortgage Rate", f"{cur_mort_mm:.2f}%", SIGNAL_TEXT),
                ("Mortgage Spread", f"{cur_regime_mm} ({cur_spread_mm:.2f}%)", _cs),
                ("Refi Signal", cur_refi_mm, _cr),
            ]), unsafe_allow_html=True)

            st.markdown("---")

            # Signal
            st.markdown("### Signal")
            if cur_regime_mm == "TIGHT":
                st.success(f"✅ TIGHT SPREAD — As of {cur_date_mm} the mortgage "
                    f"spread is {cur_spread_mm:.2f}% ({cur_spread_mm*100:.0f} bps). "
                    f"Lenders competing aggressively.")
            elif cur_regime_mm == "NORMAL":
                st.success(f"✅ NORMAL SPREAD — As of {cur_date_mm} the mortgage "
                    f"spread is {cur_spread_mm:.2f}% ({cur_spread_mm*100:.0f} bps). "
                    f"Mortgage risk priced appropriately.")
            elif cur_regime_mm == "WIDE":
                st.warning(f"⚠️ WIDE SPREAD — As of {cur_date_mm} the mortgage "
                    f"spread is {cur_spread_mm:.2f}% ({cur_spread_mm*100:.0f} bps). "
                    f"Lenders demanding more compensation.")
            else:
                st.error(f"🚨 VERY WIDE SPREAD — As of {cur_date_mm} the mortgage "
                    f"spread is {cur_spread_mm:.2f}% ({cur_spread_mm*100:.0f} bps). "
                    f"Significant MBS market stress.")

            # Refi and Prepay signal
            st.markdown("### Refinancing & Prepayment Signal")
            if cur_refi_mm in ["MINIMAL REFI", "SOME REFI"]:
                st.success(f"✅ {cur_refi_mm} — Prepayment Risk: {cur_prepay_mm}. "
                    f"Prepayments are near baseline, so MBS duration stays extended.")
            elif cur_refi_mm == "ACTIVE REFI":
                st.warning(f"⚠️ {cur_refi_mm} — Prepayment Risk: {cur_prepay_mm}. "
                    f"Prepayment speeds above normal. Duration shortening.")
            else:
                st.error(f"🚨 {cur_refi_mm} — Prepayment Risk: {cur_prepay_mm}. "
                    f"Significant prepayment acceleration. Duration shortening rapidly.")

            # Results
            st.markdown("---")
            st.markdown("### Results")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Official 30Y Mortgage", f"{cur_mort_mm:.2f}%")
            m2.metric("10-Year Treasury",       f"{cur_10y_mm:.2f}%")
            m3.metric("Mortgage Spread",        f"{cur_spread_mm:.2f}%")
            m4.metric("Percentile",  ordinal(pct_rank_mm), f"since {df_mm.index.min().year}")

            s1, s2, s3 = st.columns(3)
            s1.metric("Spread Regime",          cur_regime_mm)
            s2.metric("Refi Environment",       cur_refi_mm)
            s3.metric("Prepayment Risk",        cur_prepay_mm)

            # Historical context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Historical Avg",    f"{avg_spread_mm:.2f}%", f"since {df_mm.index.min().year}")
            h2.metric("vs Average",        f"{cur_spread_mm - avg_spread_mm:+.2f}%")
            h3.metric(f"High Since {df_mm.index.min().year}", f"{max_spread_mm:.2f}%", max_date_mm)
            h4.metric(f"Low Since {df_mm.index.min().year}",  f"{min_spread_mm:.2f}%", min_date_mm)

            w1, w2 = st.columns(2)
            w1.metric("MBB 1-Month",  f"{mbb_1m_mm:+.1f}%")
            w2.metric("MBB 12-Month", f"{mbb_12m_mm:+.1f}%")

            # Charts
            st.markdown("---")
            st.markdown("### Charts")
            fig = plt.figure(figsize=(14, 14))
            fig.patch.set_facecolor('#FFFFFF')
            gs   = gridspec.GridSpec(3, 1, figure=fig, hspace=0.35)
            axes = [fig.add_subplot(gs[i]) for i in range(3)]

            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333', labelsize=9)
                for spine in ax.spines.values():
                    spine.set_edgecolor('#DDDDDD')
                ax.grid(axis='y', color='#EEEEEE', linewidth=0.8)
                ax.grid(axis='x', color='#EEEEEE', linewidth=0.5, alpha=0.5)

            fig.suptitle(
                "Mortgage Market Monitor — Freddie Mac via FRED (MORTGAGE30US)",
                fontsize=13, fontweight='bold', color='#222222', y=0.98)

            # Chart 1 — Mortgage rate vs 10Y Treasury
            ax = axes[0]
            ax.plot(df_mm.index, df_mm["10Y_Treasury"],
                color='#1A237E', linewidth=1.5, label='10-Year Treasury')
            ax.plot(df_mm.index, df_mm["Mortgage_Rate"],
                color='#B71C1C', linewidth=1.5,
                label='Official 30Y Mortgage Rate (Freddie Mac)')
            ax.fill_between(df_mm.index,
                df_mm["10Y_Treasury"], df_mm["Mortgage_Rate"],
                color='#E53935', alpha=0.08, label='Mortgage Spread')
            ax.set_title(
                'Official 30-Year Mortgage Rate vs 10-Year Treasury',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('Rate (%)', color='#333333')
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
            ax.annotate(f'  Today: {cur_mort_mm:.2f}%',
                xy=(df_mm.index[-1], cur_mort_mm),
                fontsize=8, color='#B71C1C', fontweight='bold')

            # Chart 2 — Mortgage spread with regime shading
            ax = axes[1]
            ax.axhspan(0,    1.50, color='#1B5E20', alpha=0.08,
                label='Tight (<1.50%)')
            ax.axhspan(1.50, 2.00, color='#2E7D32', alpha=0.08,
                label='Normal (1.50-2.00%)')
            ax.axhspan(2.00, 2.50, color='#F9A825', alpha=0.08,
                label='Wide (2.00-2.50%)')
            ax.axhspan(2.50, 5.00, color='#C62828', alpha=0.10,
                label='Very Wide (>2.50%)')
            ax.axhline(y=avg_spread_mm, color='#666666', linewidth=1,
                linestyle='--', alpha=0.7,
                label=f'Avg: {avg_spread_mm:.2f}%')
            ax.plot(df_mm.index, df_mm["Mortgage_Spread"],
                color='#CCCCCC', linewidth=0.5, alpha=0.6)
            ax.plot(df_mm["Spread_Smooth"].index,
                df_mm["Spread_Smooth"].values,
                color='#1A237E', linewidth=2,
                label='Spread (21-day avg)', zorder=4)
            ax.scatter(df_mm.index[-1],
                float(df_mm["Spread_Smooth"].iloc[-1]),
                color='#1A237E', s=70, zorder=5)
            ax.annotate(f'  Today: {cur_spread_mm:.2f}%',
                xy=(df_mm.index[-1],
                float(df_mm["Spread_Smooth"].iloc[-1])),
                fontsize=8, color='#1A237E', fontweight='bold')
            ax.set_title(
                'Mortgage Spread — TIGHT / NORMAL / WIDE / VERY WIDE',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('Spread (%)', color='#333333')
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333',
                fontsize=8, ncol=3)
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))

            # Chart 3 — MBB vs AGG
            ax = axes[2]
            mbb_norm_mm = (df_mm["MBB"] / df_mm["MBB"].iloc[0]) * 100
            agg_norm_mm = (df_mm["AGG"] / df_mm["AGG"].iloc[0]) * 100
            relative_mm = mbb_norm_mm - agg_norm_mm
            ax.fill_between(df_mm.index, 0, relative_mm,
                where=relative_mm >= 0, color='#2E7D32', alpha=0.4,
                label='MBB outperforming AGG')
            ax.fill_between(df_mm.index, 0, relative_mm,
                where=relative_mm < 0,  color='#C62828', alpha=0.4,
                label='MBB underperforming AGG')
            ax.axhline(y=0, color='#333333', linewidth=1)
            ax.plot(df_mm.index, relative_mm,
                color='#333333', linewidth=0.8, alpha=0.6)
            ax.set_title(
                'MBS ETF (MBB) vs Investment Grade Bonds (AGG) — Relative Performance',
                color='#333333', fontsize=12, fontweight='bold')
            ax.set_ylabel('MBB minus AGG (pts)', color='#333333')
            ax.legend(facecolor='#F9F9F9', labelcolor='#333333', fontsize=8)

            plt.tight_layout(pad=2.5)
            st.pyplot(fig)

        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Mortgage Market Monitor including all code,
            charts, spread analysis, and historical period breakdown
            on GitHub:<br><br>
            github.com/sidneyppratt-svg/mortgage-market-monitor
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Disclaimer shown under every finance model
    st.markdown("---")
    st.markdown("""
    <p style="color:#666666; font-size:12px; line-height:1.5; font-weight:700;">
    <b>Disclaimer:</b> This website and its models are for educational and research
    purposes only and do not constitute investment, financial, or trading advice.
    Model signals are based on historical data and simplified assumptions, may contain
    errors, and do not predict future results. Past performance does not guarantee
    future returns. Consult a qualified financial professional before making
    investment decisions.
    </p>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# OTHER PROJECTS — HOCKEY PATHWAY NAVIGATOR
# ══════════════════════════════════════════════════════════════
elif page == "Other Projects":
    import os
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    st.markdown("# Other Projects")
    st.markdown("""
    <p style="color:#333333; font-size:16px;">
    Projects outside of finance, built with the same Python and data skills.
    </p>
    """, unsafe_allow_html=True)

    # Project selection buttons (same style as AI Finance)
    p1, p2 = st.columns(2)
    with p1:
        pick_rb = st.button("Recipe Builder",
            key="btn_rb", use_container_width=True)
    with p2:
        pick_hn = st.button("Hockey Pathway Navigator",
            key="btn_hn", use_container_width=True)
    if "project" not in st.session_state:
        st.session_state.project = "Recipe Builder"
    if pick_rb: st.session_state.project = "Recipe Builder"
    if pick_hn: st.session_state.project = "Hockey Pathway Navigator"
    st.markdown("---")

    # ══════════════════════════════════════════════════════════
    # RECIPE BUILDER
    # ══════════════════════════════════════════════════════════
    if st.session_state.project == "Recipe Builder":
        import json
        import anthropic

        st.markdown("""
        <style>
        .rb-card {
            background-color: #F9F9F9; border: 1px solid #DDDDDD;
            border-radius: 12px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
        }
        .rb-card h4 { color: #222222 !important; margin: 0 0 0.3rem 0;
            font-size: 16px; padding: 0 !important; }
        .rb-meta { color: #555555; font-size: 13px; margin-bottom: 0.4rem; }
        .rb-why { color: #333333; font-size: 13px; margin-top: 0.5rem; }
        .rb-nut { display: flex; flex-wrap: wrap; gap: 0.35rem; }
        .rb-nut span { background: #FFFFFF; border: 1px solid #DDDDDD;
            border-radius: 6px; padding: 2px 8px; font-size: 13px; color: #1a1a1a; }
        .rb-nut span.key { background: #F0FFF4; border-color: #A8D5B5;
            color: #1B5E20; font-weight: 700; }
        </style>
        """, unsafe_allow_html=True)

        title_col, card_col = st.columns([3, 2])
        with title_col:
            st.markdown("## Recipe Builder")
            st.markdown("*AI-Powered Healthy Recipe Generator | Sidney Pratt*")
        with card_col:
            st.markdown("""
            <div class="results-card">
                <div class="rc-head"><b>How it works</b></div>
                <div class="rc-row"><span class="rc-label">1. Pick a category</span></div>
                <div class="rc-row"><span class="rc-label">2. Claude creates recipes with nutrition</span></div>
                <div class="rc-row"><span class="rc-label">3. Open one and adjust the servings</span></div>
            </div>
            """, unsafe_allow_html=True)

        # Each category: instructions for Claude + a plain-English note
        RB_CATEGORIES = {
            "Game Day Energy": {
                "rules": "Pre-game meals for an athlete, eaten 3-4 hours before a "
                         "game. Carb-focused (at least 45g carbs per serving), "
                         "moderate protein (15-30g), lower fat (under 20g), low "
                         "fiber and nothing greasy or heavy, so it digests easily.",
                "note": "Carb-focused meals with moderate protein and lower fat, so "
                        "they digest easily. Eat 3–4 hours before a game to top up "
                        "your energy stores.",
                "key": ["Carbs", "Protein"]},
            "After Game Recovery": {
                "rules": "Post-game recovery meals for an athlete. At least 30g "
                         "protein and 40g carbs per serving to repair muscle and "
                         "refill energy. Include some colorful vegetables or fruit.",
                "note": "Protein to help repair muscle plus carbs to refill energy. "
                        "Best eaten within a couple of hours after a game or hard practice.",
                "key": ["Protein", "Carbs"]},
            "High Protein": {
                "rules": "At least 35g protein per serving from whole foods such as "
                         "chicken, fish, lean beef, eggs, Greek yogurt, tofu, or beans. "
                         "Keep it balanced with vegetables.",
                "note": "Meals with 35g+ of protein per serving, useful for strength "
                        "training and staying full longer.",
                "key": ["Protein"]},
            "Low Calorie": {
                "rules": "Under 450 calories per serving but still satisfying: at "
                         "least 20g protein and lots of vegetables for volume.",
                "note": "Lighter meals under about 450 calories per serving that still "
                        "include protein, so they stay filling.",
                "key": ["Calories", "Protein"]},
            "Vegetarian": {
                "rules": "Fully vegetarian (no meat, poultry, or fish; no fish sauce "
                         "or gelatin). At least 18g protein per serving from beans, "
                         "lentils, tofu, tempeh, eggs, dairy, or whole grains.",
                "note": "Meat-free meals with solid protein from beans, lentils, tofu, "
                        "eggs, dairy, and whole grains.",
                "key": ["Protein"]},
            "Healthy Balanced": {
                "rules": "An everyday balanced plate: lean protein (20g+), whole "
                         "grains or starchy vegetables, plenty of vegetables, healthy "
                         "fats, 500-700 calories, at least 6g fiber, little added sugar.",
                "note": "A balance of protein, fiber, and moderate calories with little "
                        "added sugar. A solid everyday meal.",
                "key": ["Protein", "Fiber"]},
            "Blood Sugar Friendly": {
                "rules": "Meals suited to steadier blood sugar: 45g carbs or less per "
                         "serving from whole grains, beans, and vegetables (no refined "
                         "white flour or white rice as the main carb), at least 6g "
                         "fiber, 20g+ protein, healthy fats, and no added sugar, "
                         "honey, syrups, or sugary sauces.",
                "note": "Moderate carbs, plenty of fiber, protein, and little sugar, "
                        "which helps keep blood sugar steadier. Nutrition values are "
                        "AI estimates: do not use them to calculate insulin doses, and "
                        "follow the advice of your doctor or dietitian.",
                "key": ["Carbs", "Fiber"]},
            "Easy 3-Ingredient": {
                "rules": "Super simple healthy recipes built from exactly 3 main "
                         "ingredients. Salt, pepper, cooking oil, water, and dried "
                         "herbs or spices do not count toward the 3; list them "
                         "separately as pantry basics. Under 20 minutes, beginner "
                         "friendly, with a real source of protein or fiber.",
                "note": "Just three main ingredients plus pantry basics like oil, "
                        "salt, and spices. Quick, cheap, and hard to mess up, which "
                        "makes them great for busy days.",
                "key": ["Protein", "Calories"]},
            "Soups": {
                "rules": "Healthy, filling soups or stews with plenty of vegetables "
                         "and at least 15g protein per serving, under 600 calories, "
                         "moderate sodium (use herbs, spices, and low-sodium broth). "
                         "Mention in the why note how well it keeps for meal prep.",
                "note": "Filling, vegetable-rich soups with protein. Most keep well in "
                        "the fridge for a few days, which makes them great for meal prep.",
                "key": ["Calories", "Protein"]},
        }

        RB_SYSTEM = (
            "You are a registered-dietitian-style recipe developer. Create realistic, "
            "tasty, home-cookable recipes using common grocery-store ingredients. "
            "Nutrition values must be your best per-serving estimates. "
            "Respond with ONLY valid JSON, no markdown fences and no extra text, in "
            "exactly this shape: "
            '{"recipes": [{"title": str, "time_minutes": int, "servings": int, '
            '"calories": int, "protein_g": int, "carbs_g": int, "fiber_g": int, '
            '"fat_g": int, "why": str (one sentence on why it fits the category), '
            '"ingredients": [{"amount": number or null, "unit": str, "item": str}], '
            '"steps": [str]}]}'
        )

        @st.cache_data(ttl=3600, show_spinner=False)
        def rb_generate(category, batch):
            """Ask Claude for 3 recipes. Cached 1 hour to save credits."""
            client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY
            prompt = (
                f"Category: {category}\n"
                f"Requirements: {RB_CATEGORIES[category]['rules']}\n"
                "Create 3 different recipes. Vary the cuisines and main "
                "ingredients across the three, and keep each under 45 minutes. "
                f"(Variation set #{batch}: avoid the most obvious choices.)"
            )
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=3000,
                system=RB_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            text = "".join(b.text for b in msg.content if b.type == "text")
            text = text.strip().replace("```json", "").replace("```", "")
            text = text[text.find("{"): text.rfind("}") + 1]
            return json.loads(text)

        def rb_fmt_amount(x):
            if x is None: return ""
            try: x = float(x)
            except (TypeError, ValueError): return str(x)
            if abs(x - round(x)) < 0.05: return str(int(round(x)))
            return f"{x:.2f}".rstrip("0").rstrip(".")

        # Category buttons: three rows of three
        cats = list(RB_CATEGORIES.keys())
        if "rb_category" not in st.session_state:
            st.session_state.rb_category = cats[0]
        if "rb_batch" not in st.session_state:
            st.session_state.rb_batch = 0
        for row in (cats[0:3], cats[3:6], cats[6:9]):
            cols = st.columns(3)
            for col, cat in zip(cols, row):
                with col:
                    if st.button(cat, key=f"rb_{cat}", use_container_width=True):
                        st.session_state.rb_category = cat
                        st.session_state.rb_batch = 0

        category = st.session_state.rb_category
        info = RB_CATEGORIES[category]

        head_l, head_r = st.columns([3, 1])
        with head_l:
            st.markdown(f"### {category}")
        with head_r:
            if st.button("↻ Show Different Recipes", key="rb_new",
                         use_container_width=True):
                st.session_state.rb_batch += 1

        st.markdown(f"""
        <div class="data-source-section">
            <h3>Why this works</h3>
            <p>{info['note']}</p>
        </div>
        """, unsafe_allow_html=True)

        if not os.environ.get("ANTHROPIC_API_KEY"):
            st.warning("Recipe generation isn't connected yet. Add "
                       "ANTHROPIC_API_KEY where this site is hosted.")
            st.stop()

        with st.spinner("Claude is creating recipes... (about 15 seconds)"):
            try:
                data = rb_generate(category, st.session_state.rb_batch)
                error = None
            except anthropic.AuthenticationError:
                error = "The Claude API key wasn't accepted. Check the ANTHROPIC_API_KEY setting where this site is hosted."
            except anthropic.BadRequestError as e:
                if "credit" in str(e).lower():
                    error = "Recipe credits have run out for now. Please check back later."
                else:
                    error = "Couldn't create recipes right now. Please try again."
            except anthropic.RateLimitError:
                error = "Too many requests at once. Please wait a minute and try again."
            except (json.JSONDecodeError, ValueError):
                error = "The recipes came back in an unexpected format. Click Show Different Recipes to try again."
            except Exception:
                error = "Couldn't reach the recipe generator right now. Please try again in a minute."

        if error:
            st.error(error)
            st.stop()

        recipes = data.get("recipes", [])
        if not recipes:
            st.info("No recipes came back. Click Show Different Recipes to try again.")
            st.stop()

        nut_fields = {"Calories": ("calories", " cal"), "Protein": ("protein_g", "g protein"),
                      "Carbs": ("carbs_g", "g carbs"), "Fiber": ("fiber_g", "g fiber")}
        order = info["key"] + [n for n in nut_fields if n not in info["key"]]

        cols = st.columns(3)
        for i, rec in enumerate(recipes):
            with cols[i % 3]:
                chips = ""
                for n in order:
                    field, unit = nut_fields[n]
                    val = rec.get(field)
                    if val is None: continue
                    cls = "key" if n in info["key"] else ""
                    chips += f'<span class="{cls}">{rb_fmt_amount(val)}{unit}</span>'
                st.markdown(f"""
                <div class="rb-card">
                    <h4>{rec.get('title', 'Recipe')}</h4>
                    <div class="rb-meta">⏱ {rec.get('time_minutes', '?')} min
                    &nbsp;|&nbsp; Serves {rec.get('servings', '?')}
                    &nbsp;|&nbsp; per serving (est.)</div>
                    <div class="rb-nut">{chips}</div>
                    <div class="rb-why">{rec.get('why', '')}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("View recipe"):
                    try: base = int(rec.get("servings") or 1)
                    except (TypeError, ValueError): base = 1
                    want = st.number_input("Servings", min_value=1, max_value=20,
                        value=base, step=1,
                        key=f"serv_{category}_{st.session_state.rb_batch}_{i}")
                    factor = want / base
                    st.markdown("**Ingredients**")
                    lines = []
                    for ing in rec.get("ingredients", []):
                        amt = ing.get("amount")
                        try: scaled = rb_fmt_amount(float(amt) * factor)
                        except (TypeError, ValueError): scaled = ""
                        line = f"- {scaled} {ing.get('unit', '')} {ing.get('item', '')}"
                        lines.append(" ".join(line.split()))
                    st.markdown("\n".join(lines) if lines else "_No ingredients listed._")
                    steps = rec.get("steps", [])
                    if steps:
                        st.markdown("**Steps**")
                        st.markdown("\n".join(f"{n}. {s}" for n, s in enumerate(steps, 1)))

        st.markdown("---")
        st.markdown("""
        <p style="color:#555555; font-size:13px;">
        Recipes are generated by Claude (Anthropic). Nutrition values are AI
        estimates per serving and may not be exact. Always check ingredients
        for allergies.
        </p>
        """, unsafe_allow_html=True)
        st.stop()

    # ══════════════════════════════════════════════════════════
    # HOCKEY PATHWAY NAVIGATOR (continues below)
    # ══════════════════════════════════════════════════════════

    st.markdown("## Hockey Pathway Navigator")
    st.markdown("""
    <p style="color:#333333; font-size:16px;">
    Every hockey pathway from youth to the pros —
    personalized recommendations, honest cost breakdowns,
    and realistic college outcomes for every junior league.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Overview</h3>
        <p>
        Hockey pathways are confusing. Families spend thousands
        of dollars on junior hockey without understanding what
        college level that league realistically leads to, whether
        athletic scholarships are even available, or what
        opportunities they may be missing entirely.<br><br>
        This tool gives honest clear answers. Built by a player
        who lived this experience firsthand as an ACHA D1 hockey
        player at Western Michigan University and a member of the
        Northern Cyclones junior program.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Junior League Cost & College Outcome Guide")
    league_data = [
        ("USHL",          "Tier 1", "FREE",
         "NCAA D1 scholarship",     "✅ Yes"),
        ("AJHL",          "Tier 1", "Under $3,000",
         "NCAA D1 possible",        "✅ Possible"),
        ("NAHL",          "Tier 2", "$5,000-8,000",
         "NCAA D1 or D3",           "⚠️ Partial possible"),
        ("USPHL NCDC",    "Tier 2", "$8,000-12,000",
         "NCAA D3 small private",   "❌ Academic aid only"),
        ("EHL",           "Tier 2", "$8,000-12,000",
         "NCAA D3 small private",   "❌ Academic aid only"),
        ("USPHL Premier", "Tier 3", "$7,000-10,000",
         "NCAA D3 or ACHA D1",      "❌ Academic aid only"),
        ("USPHL Elite",   "Tier 3", "$5,000-8,000",
         "ACHA D1 or small D3",     "❌ Academic aid only"),
        ("NA3HL",         "Tier 3", "$4,000-7,000",
         "ACHA D1 or small D3",     "❌ Academic aid only"),
    ]
    header = ["League", "Tier", "Annual Cost",
              "Typical College Outcome", "Athletic Scholarship"]
    df_leagues = pd.DataFrame(league_data, columns=header)
    st.dataframe(df_leagues, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Personalized Pathway Finder")
    col1, col2 = st.columns(2)
    with col1:
        player_age = st.number_input("Player Age",
            min_value=6, max_value=22, value=15)
        player_location = st.selectbox("Location", [
            "Midwest", "East Coast / Northeast",
            "West Coast", "South", "Canada",
        ])
    with col2:
        player_level = st.selectbox("Current Level", [
            "Learn to Skate / Mite", "Squirt", "Peewee AAA",
            "Bantam AAA", "Midget Minor", "Midget Major",
            "High School Varsity", "Prep School", "Junior Hockey",
        ])
        player_goal = st.selectbox("Goal", [
            "NCAA D1 or Pro", "NCAA D3 or ACHA", "Just love the game",
        ])
        player_league = st.selectbox(
            "Current Junior League (if applicable)", [
                "Not in junior hockey yet",
                "USHL", "AJHL", "NAHL",
                "USPHL NCDC", "EHL",
                "USPHL Premier", "USPHL Elite", "NA3HL",
            ])
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    if st.button("Get My Pathway Recommendation"):
        junior_league = None if \
            player_league == "Not in junior hockey yet" \
            else player_league
        league_outcomes = {
            'USHL': {'college': 'NCAA D1 scholarship highly likely',
                'scholarship': 'Full or partial athletic scholarship very common',
                'cost': 'FREE — teams pay stipends',
                'realistic': 'Over 90% of USHL players play college hockey. D1 scholarship is the most common outcome.'},
            'AJHL': {'college': 'NCAA D1 possible, D3 common',
                'scholarship': 'Athletic scholarship possible at D1',
                'cost': 'Under $3,000/year — billet family system',
                'realistic': 'Strong pipeline to US and Canadian college programs.'},
            'NAHL': {'college': 'NCAA D1 possible, D3 most common',
                'scholarship': 'Partial athletic scholarship possible',
                'cost': '$5,000 - $8,000 per year',
                'realistic': 'D3 is the most common outcome. D1 offers happen but are not guaranteed.'},
            'USPHL NCDC': {'college': 'NCAA D3 most common — small private schools',
                'scholarship': 'NO athletic scholarship. Academic merit aid only.',
                'cost': '$8,000 - $12,000 per year',
                'realistic': 'Most players land at small private NCAA D3 schools.'},
            'EHL': {'college': 'NCAA D3 most common — northeast schools',
                'scholarship': 'NO athletic scholarship. Academic merit aid only.',
                'cost': '$8,000 - $12,000 per year',
                'realistic': 'Most players attend small private D3 schools in New England.'},
            'USPHL Premier': {'college': 'NCAA D3 small private schools or ACHA D1',
                'scholarship': 'NO athletic scholarship. Academic merit aid only.',
                'cost': '$7,000 - $10,000 per year',
                'realistic': 'Players typically land at small private D3 schools or ACHA D1 programs.'},
            'USPHL Elite': {'college': 'ACHA D1 or very small NCAA D3 schools',
                'scholarship': 'NO athletic scholarship. Academic merit aid only.',
                'cost': '$5,000 - $8,000 per year',
                'realistic': 'Entry level junior league. Moving up to USPHL Premier significantly improves options.'},
            'NA3HL': {'college': 'ACHA D1 or small NCAA D3 schools',
                'scholarship': 'NO athletic scholarship. Academic merit aid only.',
                'cost': '$4,000 - $7,000 per year',
                'realistic': 'Development league. Players who move up to NAHL significantly improve options.'},
        }
        st.markdown("---")
        st.markdown("### Your Personalized Pathway Report")
        if junior_league and junior_league in league_outcomes:
            li = league_outcomes[junior_league]
            st.markdown(f"""
            <div class="card">
                <h3>Your Junior League — {junior_league}</h3>
                <p>
                <b>Annual Cost:</b> {li['cost']}<br><br>
                <b>College Outlook:</b> {li['college']}<br><br>
                <b>Scholarship:</b> {li['scholarship']}<br><br>
                <b>Reality Check:</b> {li['realistic']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        if player_age <= 12:
            recs = ["Focus on skill development and fun above all else.",
                "Play multiple sports — do not specialize yet.",
                "Look for quality AAA programs in your area.",
                "Start researching prep schools if interested."]
            opps = ["AAA programs in your region",
                "USA Hockey national tournaments",
                "Summer development camps",
                "Prep school information sessions"]
            next_step = "Attend one major showcase and focus on loving the game."
        elif player_age <= 14:
            recs = ["AAA Bantam is the most critical age for junior development.",
                "USHL scouts begin watching at this level.",
                "Start building a highlight reel now.",
                "Attend USHL and NAHL showcases.",
                "Research prep schools seriously."]
            opps = ["AAA Bantam Major programs",
                "Prep school hockey programs",
                "USHL and NAHL prospect showcases",
                "USA Hockey Select 15 and Select 16 camps",
                "Shattuck St. Marys — top prep school pipeline"]
            next_step = "Get on a AAA Bantam team and attend at least one major showcase."
        elif player_age <= 16:
            recs = ["Critical decision point — junior hockey or high school.",
                "USHL draft eligible at 16 — this is your D1 window.",
                "NAHL is a strong Tier 2 option.",
                "USPHL NCDC and EHL lead to D3 not D1 scholarships.",
                "Email every junior coach with your highlight reel now."]
            opps = ["USHL Phase 1 and Phase 2 drafts",
                "NAHL Draft and free agent camps",
                "USPHL NCDC tryouts", "EHL tryouts",
                "Prep school for one more development year"]
            next_step = "Email junior coaches directly. Do not wait to be discovered."
        elif player_age <= 18:
            recs = ["Junior hockey should be your priority.",
                "The league you play in determines your college level.",
                "USHL and NAHL are your best paths to D1.",
                "USPHL NCDC and EHL most commonly lead to D3 only.",
                "Email college coaches directly with your highlight reel."]
            opps = ["USHL free agent camps", "NAHL free agent camps",
                "USPHL NCDC tryouts", "EHL tryouts", "AJHL tryouts",
                "NCAA D3 coaches — email directly"]
            next_step = "Junior hockey now. Email every coach. Cast a wide net."
        else:
            recs = ["ACHA D1 and D2 are great options to keep playing.",
                "Play at the school that fits you academically.",
                "Strong academics open more doors at this stage.",
                "Hockey is a lifelong sport — enjoy every level."]
            opps = ["ACHA D1 at your college", "ACHA D2 at your college",
                "Adult recreational leagues", "Intramural hockey"]
            next_step = "Find an ACHA program at a school that fits academically."

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="card"><h3>Recommendations</h3>""",
                unsafe_allow_html=True)
            for r in recs:
                st.markdown(f"• {r}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="card"><h3>Opportunities Now</h3>""",
                unsafe_allow_html=True)
            for o in opps:
                st.markdown(f"• {o}")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <h3>Your Next Step</h3>
            <p>{next_step}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="card">
        <h3>Full Research Notebook & Team Directory</h3>
        <p>
        View the complete Hockey Pathway Navigator including
        all 10 pathways, full league and team directory,
        and personalized recommendation engine on GitHub:<br><br>
        github.com/sidneyppratt-svg/hockey-pathway-navigator
        </p>
    </div>
    """, unsafe_allow_html=True)
