import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import datetime
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Sidney Pratt | Quant Research",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #4A4A4A; }
    [data-testid="stSidebar"] * { color: white !important; }
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
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .card h3 { color: #444444 !important; margin-bottom: 0.5rem; }
    .card p { color: #1a1a1a !important; line-height: 1.6; }
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
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .static-section h3 { color: #1A237E !important; margin-bottom: 0.5rem; }
    .static-section p { color: #1a1a1a !important; line-height: 1.6; }
    .dynamic-section {
        background-color: #F9F9F9;
        border: 1px solid #DDDDDD;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .dynamic-section h3 { color: #444444 !important; margin-bottom: 0.5rem; }
    .dynamic-section p { color: #1a1a1a !important; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="profile-placeholder">SP</div>
    <p style="text-align:center; color:#CCCCCC; font-size:11px;
    margin-bottom:0.5rem;">Photo coming soon</p>
    """, unsafe_allow_html=True)
    st.markdown("## Sidney Pratt")
    st.markdown("*Quant Researcher*")
    st.markdown("---")
    page = st.radio("", ["Home", "About", "Resume", "AI Research"])
    st.markdown("---")
    st.markdown("### Contact")
    st.markdown("""
    <div class="sidebar-contact">
    📧 sidneyppratt@gmail.com<br>
    📍 San Francisco, CA<br>
    🔗 linkedin.com/in/sidney-pratt<br>
    💻 github.com/sidneyppratt-svg<br>
    🌐 sidneyppratt.com
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if page == "Home":
    st.markdown("# Sidney Pratt")
    st.markdown("""
    <div style="margin-bottom:1rem;">
        <span class="tag">Finance & Economics</span>
        <span class="tag">ACHA D1 Hockey</span>
        <span class="tag">AI Researcher</span>
        <span class="tag">World Explorer</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <p style="color:#333333; font-size:16px; line-height:1.8;">
    Finance and Economics student combining quantitative research,
    AI tools, and real-world market experience to build the next
    generation of trading strategies.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="seeking-card">
        <h4>Currently Seeking</h4>
        <p>
        Internship opportunities in:<br>
        - Cross-Asset Trading<br>
        - Quantitative Research<br>
        - Portfolio Management<br>
        - Economic Research<br>
        - Financial Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <h3>Education</h3>
            <p>Western Michigan University<br>
            Finance & Economics<br>GPA: 3.25</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <h3>Experience</h3>
            <p>AIER Intern<br>
            Economic Research<br>Policy Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <h3>Global</h3>
            <p>Mt. Kilimanjaro<br>
            Amazon Rainforest<br>Tanzania Volunteer</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════════════════
elif page == "About":
    st.markdown("# About Me")
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <p>
        Sidney Pratt is a Finance and Economics double major at Western
        Michigan University with a passion for financial markets,
        quantitative research, and innovation. Born and raised in
        San Francisco, Sidney brings a rare combination of academic
        rigor, athletic discipline, and global perspective to everything
        he does.
        </p>
        <p>
        As an ACHA D1 hockey player at Western Michigan University,
        Sidney understands what it takes to perform under pressure,
        work within a team, and push through challenges that most
        people walk away from. Those same qualities show up in his
        academic and professional work.
        </p>
        <p>
        Sidney has already gained real world experience as an intern
        at the American Institute for Economic Research where he
        contributed to economic research, policy analysis, and data
        collection. He has also built live AI tools that detect
        market regimes and credit stress across multiple asset classes
        using over a decade of real market data.
        </p>
        <p>
        Beyond finance Sidney has summited Mount Kilimanjaro in
        Tanzania, worked with conservation rangers protecting the
        Amazon rainforest in Peru, and volunteered at orphanages
        in Africa. These experiences shaped a globally minded,
        adaptable, and deeply curious professional who sees the
        world as a place of opportunity.
        </p>
        <p>
        Sidney is currently seeking internship opportunities in
        cross-asset trading, quantitative research, and portfolio
        management where he can contribute immediately and continue
        growing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## What I Bring to the Table")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Quantitative Skills</h3>
            <p>Python, SQL, financial analysis, machine learning,
            backtesting, and market data analysis. Built live
            AI tools trained on real market data.</p>
        </div>
        <div class="card">
            <h3>Athletic Discipline</h3>
            <p>ACHA D1 Hockey player — understanding of high
            performance, teamwork under pressure, and the discipline
            to show up every day regardless of circumstances.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Research Experience</h3>
            <p>Interned at the American Institute of Economic
            Research — contributing to real economic policy analysis,
            literature review, and data-driven research.</p>
        </div>
        <div class="card">
            <h3>Global Perspective</h3>
            <p>Summited Kilimanjaro, protected the Amazon rainforest,
            and volunteered across Africa. A worldview shaped by
            real experience — not just a classroom.</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RESUME
# ══════════════════════════════════════════════════════════════
elif page == "Resume":
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
        Coursera — Python & SQL for Python
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
            Python<br>SQL<br>Microsoft Office Suite<br>
            Financial Analysis<br>AI Tools & Machine Learning<br>
            Market Forecasting
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
elif page == "AI Research":
    st.markdown("# AI Research")
    st.markdown("""
    <p style="color:#333333; font-size:16px;">
    Using machine learning to find signals in financial markets
    and solve real world problems.
    Each model is built on real data and fully interactive.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    model = st.selectbox("Select a model:", [
        "Yield Curve Monitor",
        "Multi-Asset Market Regime Detector",
        "Credit Spread Monitor",
        "Hockey Pathway Navigator",
    ])

# ══════════════════════════════════════════════════════════════
# MODEL 1 — YIELD CURVE MONITOR
# ══════════════════════════════════════════════════════════════
    if model == "Yield Curve Monitor":
        st.markdown("## Yield Curve Monitor")
        st.markdown("*Fixed Income Relative Value Tool | Sidney Pratt*")
        st.markdown("---")

        # ── STATIC SECTION ─────────────────────────────────────
        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the US Treasury yield curve across four
            maturities — 3-month, 5-year, 10-year, and 30-year — and
            classifies the current regime as Steep, Normal, Flat,
            Inverted, or Deeply Inverted based on the classic
            10Y minus 3M spread.<br><br>
            Built specifically to complement a fixed income relative
            value research portfolio. The yield curve is the single
            most watched indicator across every fixed income trading
            desk — rates, credit, and mortgages.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Live Treasury yield data downloaded fresh on every run<br><br>
            • Regime classification across 5 curve states —
            Steep, Normal, Flat, Inverted, Deeply Inverted<br><br>
            • Plain language interpretation of what the curve is saying<br><br>
            • Dynamic signal and strategy that updates with the regime<br><br>
            • 30-day and 90-day trend detection — steepening or flattening<br><br>
            • Backtest of a TLT bond strategy using curve signals 2003-2026<br><br>
            • Key historical event annotations — 2001, 2006, 2020, 2022-23
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                The yield curve is the most cited indicator in fixed
                income markets. Every rates, credit, and mortgage desk
                watches the 10Y minus 3M spread daily because it predicts
                recessions, Fed policy shifts, and bond market direction
                before they happen.<br><br>
                Every major US recession since 1970 has been preceded
                by a yield curve inversion. The 2022-23 inversion was
                the deepest since the 1980s at -1.70%.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads live US Treasury yields across four maturities
                and calculates the 10Y minus 3M spread — the classic
                Federal Reserve inversion signal. A 21-day rolling average
                smooths daily noise.<br><br>
                Strategy holds TLT during Normal and Steep regimes and
                moves to cash during Flat and Inverted regimes.
                Backtest runs from 2003 to present with no lookahead bias.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Regime Classification</h3>
            <p>
            <b>Steep</b> (above +1.50%) — Strong growth signal →
            <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br>
            <b>Normal</b> (+0.50% to +1.50%) — Healthy economy →
            <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br>
            <b>Flat</b> (-0.50% to +0.50%) — Transition zone →
            <span style="color:#E65100; font-weight:bold;">MOVE TO CASH</span><br><br>
            <b>Inverted</b> (-0.50% to 0%) — Recession warning →
            <span style="color:#C62828; font-weight:bold;">MOVE TO CASH</span><br><br>
            <b>Deeply Inverted</b> (below -0.50%) — High alert →
            <span style="color:#B71C1C; font-weight:bold;">MOVE TO CASH</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Run the Model")
        col1, col2 = st.columns(2)
        with col1:
            yc_start = st.date_input("Start Date",
                value=datetime.date(2000, 1, 1), key="yc_start")
        with col2:
            yc_end = st.date_input("End Date",
                value=datetime.date(2026, 9, 18), key="yc_end")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Yield Curve Monitor"):
            with st.spinner("Downloading Treasury yield data..."):
                tickers = {
                    '3M':  '^IRX',
                    '5Y':  '^FVX',
                    '10Y': '^TNX',
                    '30Y': '^TYX',
                }
                yc_yields = pd.DataFrame()
                for name, ticker in tickers.items():
                    data = yf.download(ticker,
                        start=str(yc_start),
                        end=str(yc_end),
                        auto_adjust=True,
                        progress=False)['Close']
                    yc_yields[name] = data
                yc_yields = yc_yields.dropna()
                yc_yields['10Y_3M']  = yc_yields['10Y'] - yc_yields['3M']
                yc_yields['10Y_5Y']  = yc_yields['10Y'] - yc_yields['5Y']
                yc_yields['30Y_10Y'] = yc_yields['30Y'] - yc_yields['10Y']
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
                trend_90d      = float(yc_yields['10Y_3M'].iloc[-1] -
                                       yc_yields['10Y_3M'].iloc[-63]) \
                                 if len(yc_yields) > 63 else 0.0

            # ── DYNAMIC SECTION ────────────────────────────────
            st.markdown("---")

            # Signal
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

            # Strategy Signal
            st.markdown("### Strategy Signal")
            if current_regime in ['NORMAL', 'STEEP']:
                st.success("HOLD TLT — Long duration bonds are safe "
                           "to hold in this regime.")
            elif current_regime == 'FLAT':
                st.warning("MOVE TO CASH — Curve is in transition zone. "
                           "Reduce long duration bond exposure.")
            else:
                st.error("MOVE TO CASH — Avoid long duration bonds "
                         "during inversion. History shows significant "
                         "drawdown risk.")

            # Results
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
                f"{pct_rank:.0f}th", "vs history")
            s3.metric("30-Day Trend",
                f"{trend_30d:+.2f}%",
                "Steepening" if trend_30d > 0 else "Flattening")
            s4.metric("vs Avg Spread",
                f"{current_spread - avg_spread:+.2f}%",
                f"Avg: {avg_spread:.2f}%")

            # Summary & Key Findings
            st.markdown("---")
            st.markdown("### Summary & Key Findings")

            summaries = {
                'DEEPLY INVERTED': 'The yield curve is deeply inverted — '
                    'one of the most reliable recession warning signals '
                    'in finance. Short term rates are significantly above '
                    'long term rates. Every major US recession since 1970 '
                    'has been preceded by this signal.',
                'INVERTED': 'The yield curve is inverted — short term rates '
                    'exceed long term rates. A classic recession warning. '
                    'Markets are pricing in future Fed rate cuts as the '
                    'economy is expected to slow.',
                'FLAT': 'The yield curve is flat — short and long term rates '
                    'are nearly equal. This is a critical transition zone. '
                    'Direction from here matters enormously — steepening '
                    'is healthy, further flattening is a warning.',
                'NORMAL': 'The yield curve is normal — long term rates are '
                    'above short term rates. This is the healthy baseline '
                    'for a growing economy. Banks are profitable, lending '
                    'is abundant, and the Fed is in a neutral stance.',
                'STEEP': 'The yield curve is steep — long term rates are '
                    'well above short term rates. This typically appears '
                    'after a recession during recovery, or when inflation '
                    'expectations are rising. Historically a strong '
                    'growth signal.',
            }
            st.markdown(f"""
            <div class="dynamic-section">
                <h3>Summary</h3>
                <p>{summaries.get(current_regime, '')}</p>
            </div>
            """, unsafe_allow_html=True)

            # What It Means
            st.markdown("### What It Means")
            plain_english = {
                'DEEPLY INVERTED': [
                    'Normally you get paid more to lock your money away '
                    'for 10 years than for 3 months. Right now that is '
                    'backwards — the 3 month rate is higher than the '
                    '10 year rate.',
                    'This happens when the Fed has raised short term rates '
                    'aggressively to fight inflation. The market now expects '
                    'the Fed to cut rates because the economy will slow.',
                    'This signal has preceded every major US recession since '
                    '1970. The recession typically arrives 12 to 18 months '
                    'after the inversion begins.',
                ],
                'INVERTED': [
                    'Short term borrowing costs are higher than long term '
                    'costs — the opposite of normal. Markets expect the '
                    'economy to slow and the Fed to cut rates.',
                    'Banks borrow short and lend long — an inverted curve '
                    'squeezes their margins, reduces lending, and slows '
                    'economic growth.',
                    'Bond investors are accepting lower 10 year yields '
                    'because they believe growth will slow and '
                    'inflation will fall.',
                ],
                'FLAT': [
                    'Short and long term borrowing costs are almost '
                    'identical. The market is uncertain about the future '
                    'direction of the economy.',
                    'Think of the flat curve as a crossroads. The direction '
                    'it moves next tells you a lot about where the economy '
                    'is headed.',
                    'A flat curve flattening further toward inversion is a '
                    'warning. A flat curve steepening toward normal is '
                    'a healthy signal.',
                ],
                'NORMAL': [
                    'This is how the curve is supposed to look. You earn '
                    'more for lending money for 10 years than for 3 months '
                    '— that extra return compensates for uncertainty '
                    'over time.',
                    'Banks borrow cheap short term and lend at higher long '
                    'term rates — profitable for banks which means more '
                    'lending and economic growth.',
                    'The Fed is likely in a neutral or accommodative stance. '
                    'Growth is positive and inflation is manageable.',
                ],
                'STEEP': [
                    'A steep curve usually appears after a recession when '
                    'the Fed has cut short rates to near zero and the '
                    'economy is recovering — or when inflation '
                    'expectations are rising sharply.',
                    'The market demands much more compensation for lending '
                    'long term — either because it fears inflation or '
                    'expects strong future growth and higher rates.',
                    'Historically a steep curve is one of the best '
                    'environments for economic growth — banks are very '
                    'profitable and lending is abundant.',
                ],
            }
            for point in plain_english.get(current_regime, []):
                st.markdown(f"""
                <div class="dynamic-section"
                style="border-left: 4px solid #1A237E;">
                    <p>{point}</p>
                </div>
                """, unsafe_allow_html=True)

            # What to Watch
            st.markdown("### What to Watch")
            watch_points = {
                'DEEPLY INVERTED': [
                    'Watch for the Fed to start cutting rates — '
                    'that uninverts the curve',
                    'Watch unemployment claims — rising claims '
                    'confirm the recession signal',
                    'Watch credit spreads — if HYG falls sharply '
                    'alongside the inversion that is a double warning',
                    'A rapid steepening from deep inversion often '
                    'signals the recession has already begun',
                ],
                'INVERTED': [
                    'How long the inversion lasts — longer inversions '
                    'historically produce deeper recessions',
                    'Fed meetings — rate cuts are likely coming',
                    'Credit markets for early stress signals',
                    'A rapid steepening often means recession has begun',
                ],
                'FLAT': [
                    'Direction is everything — is the curve steepening '
                    'or flattening from here?',
                    'Fed guidance on future rate moves',
                    'Economic data — strong data steepens, '
                    'weak data flattens further',
                    'A flat curve tipping into inversion is a clear '
                    'warning to reduce duration exposure',
                ],
                'NORMAL': [
                    f'Curve is currently '
                    f'{"steepening" if trend_30d > 0 else "flattening"} '
                    f'({trend_30d:+.2f}% last 30 days) — watch direction',
                    'A steepening normal curve is a bullish economic signal',
                    'Watch for flattening toward zero — early warning sign',
                    'Long duration bonds perform well when rates are '
                    'stable or falling in this regime',
                ],
                'STEEP': [
                    'Inflation data — steep curve driven by inflation '
                    'fears can become risky for bonds',
                    'Fed policy — they may hike short rates which '
                    'gradually flattens the curve',
                    'A steep curve after a recession is one of the '
                    'best growth recovery signals',
                    f'Currently '
                    f'{"steepening" if trend_30d > 0 else "flattening"} '
                    f'({trend_30d:+.2f}% last 30 days)',
                ],
            }
            col1, col2 = st.columns(2)
            for i, point in enumerate(
                    watch_points.get(current_regime, [])):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="dynamic-section"
                    style="padding: 0.8rem 1rem;">
                        <p>➜ {point}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Historical Context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Avg Spread",
                f"{avg_spread:.2f}%", "since selected start")
            h2.metric("Deepest Inversion",
                f"{float(yc_yields['10Y_3M'].min()):.2f}%",
                yc_yields['10Y_3M'].idxmin().strftime('%b %Y'))
            h3.metric("Steepest Curve",
                f"{float(yc_yields['10Y_3M'].max()):.2f}%",
                yc_yields['10Y_3M'].idxmax().strftime('%b %Y'))
            inverted_pct = float(
                (yc_yields['10Y_3M'] < 0).mean() * 100)
            h4.metric("Time Inverted",
                f"{inverted_pct:.1f}%", "of selected period")

            # Charts
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
                ax.grid(axis='x', color='#EEEEEE',
                    linewidth=0.5, alpha=0.5)
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
            axes[0].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=8)
            axes[0].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
            spread_series = yc_yields['10Y_3M']
            smooth_series = yc_yields['spread_smooth']
            axes[1].axhspan(1.50, 6.00,
                color='#1B5E20', alpha=0.08, label='Steep')
            axes[1].axhspan(0.50, 1.50,
                color='#2E7D32', alpha=0.08, label='Normal')
            axes[1].axhspan(-0.50, 0.50,
                color='#F9A825', alpha=0.08, label='Flat')
            axes[1].axhspan(-3.00, -0.50,
                color='#C62828', alpha=0.10, label='Inverted')
            axes[1].axhline(y=0, color='#C62828',
                linewidth=1.5, linestyle='--', alpha=0.8)
            axes[1].plot(spread_series.index, spread_series.values,
                color='#CCCCCC', linewidth=0.6, alpha=0.7)
            axes[1].plot(smooth_series.index, smooth_series.values,
                color='#1A237E', linewidth=2.0,
                label='Spread (21-day avg)', zorder=4)
            axes[1].scatter(yc_yields.index[-1],
                spread_series.iloc[-1],
                color='#1A237E', s=80, zorder=5)
            axes[1].annotate(
                f'  Today: {spread_series.iloc[-1]:.2f}%',
                xy=(yc_yields.index[-1], spread_series.iloc[-1]),
                fontsize=8, color='#1A237E', fontweight='bold')
            axes[1].set_title(
                '10Y minus 3M Spread — Inversion Monitor',
                color='#333333', fontsize=12, fontweight='bold')
            axes[1].set_ylabel('Spread (%)', color='#333333')
            axes[1].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=8)
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
                    where=mask, color=rcolor,
                    alpha=0.7, label=regime)
            axes[2].set_title(
                'Regime Timeline — STEEP to DEEPLY INVERTED',
                color='#333333', fontsize=12, fontweight='bold')
            axes[2].set_yticks([])
            axes[2].set_ylim(0, 1)
            axes[2].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=8,
                loc='lower right', ncol=5)
            plt.tight_layout(pad=2.5)
            st.pyplot(fig)

        # ── FULL RESEARCH NOTEBOOK ─────────────────────────────
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
        st.markdown("## Multi-Asset Market Regime Detector")
        st.markdown("*Cross-Asset Quantitative Research Tool | Sidney Pratt*")
        st.markdown("---")

        # ── STATIC SECTION ─────────────────────────────────────
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
            • Live multi-asset price data downloaded fresh on every run<br><br>
            • Gaussian Mixture Model — unsupervised machine learning<br><br>
            • Simultaneous analysis of four asset classes<br><br>
            • RISK-ON and RISK-OFF regime classification<br><br>
            • 21-day rolling return smoothing to filter daily noise<br><br>
            • Full backtest of a SPY strategy using regime signals<br><br>
            • Regime detection timeline with key event annotations
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                Markets do not move in isolation. When stress hits it
                shows up across multiple asset classes simultaneously —
                stocks fall, credit widens, and gold spikes at the same
                time. A model that watches only one asset misses the
                full picture.<br><br>
                This model detects those cross-asset stress patterns
                using machine learning — no rules, no assumptions.
                The algorithm finds the patterns itself from 12 years
                of real data.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads daily prices for SPY, AGG, HYG, and GLD.
                Calculates 21-day rolling mean returns for each asset
                — smoothing noise to reveal trends.<br><br>
                A Gaussian Mixture Model finds two hidden clusters in
                the four-dimensional return data. The cluster with
                higher average SPY returns is RISK-ON. The cluster
                with lower average SPY returns is RISK-OFF.<br><br>
                Backtest goes long SPY during RISK-ON and cash during
                RISK-OFF using prior day signal — no lookahead bias.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Asset Classes Covered</h3>
            <p>
            <b>SPY — US Equities:</b> S&P 500 — broad US stock market.
            Primary return driver in RISK-ON environments.<br><br>
            <b>AGG — Investment Grade Bonds:</b> High quality corporate
            and government bonds. Safe haven during RISK-OFF.<br><br>
            <b>HYG — High Yield Credit:</b> Riskier corporate bonds.
            Falls sharply during stress — early warning signal.<br><br>
            <b>GLD — Gold:</b> Safe haven asset. Spikes during stress
            and geopolitical uncertainty.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Run the Model")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date",
                value=datetime.date(2014, 1, 1))
        with col2:
            end_date = st.date_input("End Date",
                value=datetime.date(2026, 9, 18))
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run AI Model"):
            with st.spinner("Downloading data and running AI model..."):
                tickers = ['SPY', 'AGG', 'HYG', 'GLD']
                prices = yf.download(tickers,
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
                cum_s, tot_s, ret_s, vol_s, sh_s, dd_s = \
                    get_metrics(strat)
                cum_b, tot_b, ret_b, vol_b, sh_b, dd_b = \
                    get_metrics(bh)
                latest      = smooth['label'].iloc[-1]
                latest_date = smooth.index[-1].strftime('%B %d, %Y')
                risk_off_pct = float(
                    (smooth['label'] == 'RISK-OFF').mean() * 100)

            # ── DYNAMIC SECTION ────────────────────────────────
            st.markdown("---")

            # Signal
            st.markdown("### Signal")
            if latest == 'RISK-ON':
                st.success(f"✅ RISK-ON — As of {latest_date} all four "
                           f"asset classes are behaving normally. "
                           f"Markets are calm.")
            else:
                st.error(f"🚨 RISK-OFF — As of {latest_date} stress "
                         f"detected across multiple asset classes.")

            # Strategy Signal
            st.markdown("### Strategy Signal")
            if latest == 'RISK-ON':
                st.success("STAY INVESTED — Model signals holding SPY. "
                           "Cross-asset conditions support equity exposure.")
            else:
                st.error("MOVE TO CASH — Model signals reducing equity "
                         "exposure. Cross-asset stress detected.")

            # Results
            st.markdown("---")
            st.markdown("### Results")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total Return",
                f"{tot_s:.1%}", f"{tot_s-tot_b:+.1%} vs BH")
            c2.metric("Ann. Return",
                f"{ret_s:.1%}", f"{ret_s-ret_b:+.1%} vs BH")
            c3.metric("Volatility",
                f"{vol_s:.1%}", f"{vol_s-vol_b:+.1%} vs BH")
            c4.metric("Sharpe Ratio",
                f"{sh_s:.2f}", f"{sh_s-sh_b:+.2f} vs BH")
            c5.metric("Max Drawdown",
                f"{dd_s:.1%}", f"{dd_s-dd_b:+.1%} vs BH")

            # Summary & Key Findings
            st.markdown("---")
            st.markdown("### Summary & Key Findings")
            if latest == 'RISK-ON':
                summary = (
                    f"Markets are currently in a RISK-ON regime as of "
                    f"{latest_date}. All four asset classes — equities, "
                    f"investment grade bonds, high yield credit, and gold "
                    f"— are behaving in patterns consistent with calm, "
                    f"risk-seeking market conditions. The AI model flagged "
                    f"RISK-OFF only {risk_off_pct:.1f}% of the time in "
                    f"the selected period — correctly identifying rare "
                    f"but severe stress events."
                )
            else:
                summary = (
                    f"Markets are currently in a RISK-OFF regime as of "
                    f"{latest_date}. The AI model has detected stress "
                    f"patterns across multiple asset classes simultaneously. "
                    f"This signal has historically preceded significant "
                    f"equity drawdowns. The model flagged RISK-OFF "
                    f"{risk_off_pct:.1f}% of the time in the selected "
                    f"period."
                )
            st.markdown(f"""
            <div class="dynamic-section">
                <h3>Summary</h3>
                <p>{summary}</p>
            </div>
            """, unsafe_allow_html=True)

            # What It Means
            st.markdown("### What It Means")
            if latest == 'RISK-ON':
                meanings = [
                    'Stocks are rising or stable, credit spreads are '
                    'tight, and gold is not spiking. All four asset '
                    'classes are moving in patterns the model has '
                    'learned to associate with calm markets.',
                    'The Gaussian Mixture Model found that today\'s '
                    'four-dimensional return pattern matches the '
                    'RISK-ON cluster it identified from 12 years '
                    'of training data.',
                    'RISK-ON does not mean markets cannot fall — it '
                    'means the cross-asset stress signals that '
                    'historically precede major drawdowns are '
                    'not present right now.',
                ]
            else:
                meanings = [
                    'Multiple asset classes are moving in patterns '
                    'the model has learned to associate with stress. '
                    'This could mean stocks falling, credit widening, '
                    'gold spiking, or some combination.',
                    'The Gaussian Mixture Model found that today\'s '
                    'four-dimensional return pattern matches the '
                    'RISK-OFF cluster — the same pattern seen during '
                    'COVID March 2020 and the 2022 rate hike cycle.',
                    'RISK-OFF signals have historically preceded the '
                    'worst equity drawdowns. The model moves to cash '
                    'to avoid these periods.',
                ]
            for point in meanings:
                st.markdown(f"""
                <div class="dynamic-section"
                style="border-left: 4px solid #333333;">
                    <p>{point}</p>
                </div>
                """, unsafe_allow_html=True)

            # What to Watch
            st.markdown("### What to Watch")
            if latest == 'RISK-ON':
                watch = [
                    'HYG — if high yield credit starts falling that '
                    'is the first warning sign of regime change',
                    'VIX — a spike above 25-30 often coincides with '
                    'RISK-OFF regime shifts',
                    'Gold — a sharp rally in gold alongside falling '
                    'stocks is a classic RISK-OFF signal',
                    'Credit spreads — widening spreads between HYG '
                    'and LQD signal building stress',
                ]
            else:
                watch = [
                    'Watch for all four asset classes to stabilize '
                    'together — that signals a potential regime shift back',
                    'VIX — a sustained decline below 20 often '
                    'precedes RISK-ON regime return',
                    'Fed policy — rate cuts or liquidity support '
                    'often trigger RISK-ON regime shifts',
                    'Credit spreads — tightening HYG vs LQD spread '
                    'is an early RISK-ON signal',
                ]
            col1, col2 = st.columns(2)
            for i, point in enumerate(watch):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="dynamic-section"
                    style="padding: 0.8rem 1rem;">
                        <p>➜ {point}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Historical Context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3 = st.columns(3)
            h1.metric("Time RISK-ON",
                f"{100-risk_off_pct:.1f}%", "of selected period")
            h2.metric("Time RISK-OFF",
                f"{risk_off_pct:.1f}%", "of selected period")
            h3.metric("Drawdown Improvement",
                f"{abs(dd_b)-abs(dd_s):.1%}",
                "less max drawdown vs BH")

            # Charts
            st.markdown("---")
            st.markdown("### Charts")
            fig, axes = plt.subplots(2, 1, figsize=(12, 10))
            fig.patch.set_facecolor('#FFFFFF')
            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333')
                ax.xaxis.label.set_color('#333333')
                ax.yaxis.label.set_color('#333333')
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
            events = [
                ('2020-03-01', 'COVID\nCrash'),
                ('2022-02-01', 'Fed Rate\nHikes'),
            ]
            for date_str, label_text in events:
                try:
                    event_date = pd.Timestamp(date_str)
                    idx = smooth.index.get_indexer(
                        [event_date], method='nearest')[0]
                    closest = smooth.index[idx]
                    if smooth.loc[closest, 'label'] == 'RISK-OFF':
                        axes[1].axvline(x=closest,
                            color='#C62828', linewidth=1.2,
                            linestyle='--', alpha=0.8, zorder=2)
                        axes[1].text(closest, 0.88,
                            label_text,
                            fontsize=8, color='#C62828',
                            ha='center', va='top',
                            fontweight='bold',
                            bbox=dict(
                                boxstyle='round,pad=0.3',
                                facecolor='white',
                                edgecolor='#C62828',
                                alpha=0.9))
                except Exception:
                    pass
            axes[1].set_title(
                'Regime Detection — SPY Price with RISK-ON / RISK-OFF',
                color='#333333', fontsize=13, fontweight='bold')
            axes[1].set_yticks([])
            axes[1].set_ylim(0, 1.05)
            axes[1].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=9,
                loc='lower right')
            axes[1].grid(axis='x', color='#DDDDDD',
                linewidth=0.5, alpha=0.5)
            plt.tight_layout(pad=2.0)
            st.pyplot(fig)

        # ── FULL RESEARCH NOTEBOOK ─────────────────────────────
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
# MODEL 3 — CREDIT SPREAD MONITOR
# ══════════════════════════════════════════════════════════════
    elif model == "Credit Spread Monitor":
        st.markdown("## Credit Spread Monitor")
        st.markdown("*Fixed Income Credit Research Tool | Sidney Pratt*")
        st.markdown("---")

        # ── STATIC SECTION ─────────────────────────────────────
        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the credit spread between High Yield
            bonds (HYG) and Investment Grade bonds (LQD) to detect
            building stress in credit markets. The spread is converted
            into a stress score from 1 to 5 using 16 years of real
            daily data from 2010 to 2026.<br><br>
            When investors flee from risky High Yield bonds toward
            safer Investment Grade bonds the spread widens — one of
            the earliest and most reliable warning signals of financial
            stress. This model detects that widening in real time and
            classifies it against historical context.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Live High Yield and Investment Grade bond data on every run<br><br>
            • Credit stress score from 1 (very calm) to 5 (high stress)<br><br>
            • Percentile ranking against full history since 2010<br><br>
            • 21-day rolling spread smoothing to filter daily noise<br><br>
            • Key stress period identification and annotation<br><br>
            • Two chart visualization — raw spread and stress score<br><br>
            • Dynamic signal and interpretation that updates every run
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                Credit spreads are one of the most important leading
                indicators in fixed income markets. When High Yield
                bonds underperform Investment Grade bonds it signals
                investors are pulling back from risk — often weeks or
                months before stress shows up in equity markets.<br><br>
                The 2008 crisis, 2011 EU debt crisis, 2016 oil crash,
                2020 COVID, and 2022 Fed rate hike cycle all showed up
                first in credit spreads.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads daily price data for HYG and LQD. Calculates
                21-day rolling mean returns for each — smoothing noise
                to reveal trends.<br><br>
                The credit spread is LQD returns minus HYG returns
                multiplied by 10,000 to convert to basis points.
                A wider spread means High Yield is underperforming
                Investment Grade — a stress signal.<br><br>
                The spread is ranked as a percentile and converted
                into a stress score from 1 to 5 using equal quintile
                bins.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Stress Score Classification</h3>
            <p>
            <b>Score 1 — Very Calm:</b> Credit markets extremely
            relaxed. Investors comfortable taking risk.<br><br>
            <b>Score 2 — Calm:</b> Normal credit conditions.
            Spreads in line with historical average.<br><br>
            <b>Score 3 — Moderate:</b> Some caution warranted.
            Spreads widening but not at alarming levels.<br><br>
            <b>Score 4 — Elevated:</b>
            <span style="color:#E64A19; font-weight:bold;">
            Credit stress building — watch closely.</span>
            Spreads significantly wider than normal.<br><br>
            <b>Score 5 — High Stress:</b>
            <span style="color:#B71C1C; font-weight:bold;">
            Significant credit risk — reduce exposure.</span>
            Spreads at historically wide levels.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Run the Model")
        col1, col2 = st.columns(2)
        with col1:
            start_date_cs = st.date_input("Start Date",
                value=datetime.date(2010, 1, 1), key="cs_start")
        with col2:
            end_date_cs = st.date_input("End Date",
                value=datetime.date(2026, 9, 18), key="cs_end")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Credit Spread Model"):
            with st.spinner("Downloading data and running model..."):
                cs_tickers = ['HYG', 'LQD', 'SPY']
                cs_prices = yf.download(cs_tickers,
                    start=str(start_date_cs),
                    end=str(end_date_cs),
                    auto_adjust=True)['Close']
                cs_prices  = cs_prices.dropna()
                cs_returns = cs_prices.pct_change().dropna()
                hyg_roll = cs_returns['HYG'].rolling(21).mean()
                lqd_roll = cs_returns['LQD'].rolling(21).mean()
                spread   = (lqd_roll - hyg_roll) * 10000
                spread   = spread.dropna()
                spread_df = pd.DataFrame({
                    'spread': spread,
                    'stress_score': pd.cut(
                        spread.rank(pct=True) * 100,
                        bins=[0, 20, 40, 60, 80, 100],
                        labels=[1, 2, 3, 4, 5]).astype(float),
                    'spread_smooth': spread.rolling(21).mean()
                })
                cs_current_spread = float(spread.iloc[-1])
                cs_current_score  = float(
                    spread_df['stress_score'].iloc[-1])
                cs_current_date   = spread.index[-1].strftime(
                    '%B %d, %Y')
                pct_rank = float(
                    (spread < cs_current_spread).mean() * 100)
                avg_spread_cs = float(spread.mean())
                max_spread_cs = float(spread.max())
                min_spread_cs = float(spread.min())

            # ── DYNAMIC SECTION ────────────────────────────────
            st.markdown("---")

            # Signal
            st.markdown("### Signal")
            if cs_current_score <= 2:
                st.success(f"✅ CALM — As of {cs_current_date} credit "
                           f"markets are relaxed. "
                           f"Spread: {cs_current_spread:.1f} bps")
            elif cs_current_score <= 3:
                st.warning(f"⚠️ MODERATE — As of {cs_current_date} "
                           f"some caution warranted. "
                           f"Spread: {cs_current_spread:.1f} bps")
            else:
                st.error(f"🚨 ELEVATED — As of {cs_current_date} "
                         f"credit stress building. "
                         f"Spread: {cs_current_spread:.1f} bps")

            # Strategy Signal
            st.markdown("### Strategy Signal")
            if cs_current_score <= 2:
                st.success("LOW RISK — Credit conditions support "
                           "normal risk taking. Spreads are calm.")
            elif cs_current_score == 3:
                st.warning("MODERATE CAUTION — Monitor spread direction "
                           "closely. Consider reducing high yield exposure.")
            elif cs_current_score == 4:
                st.error("REDUCE RISK — Elevated stress score. Reduce "
                         "high yield bond exposure and watch for "
                         "further widening.")
            else:
                st.error("HIGH ALERT — Stress score at maximum. "
                         "Significantly reduce credit risk exposure. "
                         "Historical periods at this level have "
                         "produced major drawdowns.")

            # Results
            st.markdown("---")
            st.markdown("### Results")
            m1, m2, m3 = st.columns(3)
            m1.metric("Credit Spread",
                f"{cs_current_spread:.1f} bps")
            m2.metric("Stress Score",
                f"{cs_current_score:.0f} / 5")
            m3.metric("Percentile Rank",
                f"{pct_rank:.0f}th",
                "vs history since 2010")

            # Summary & Key Findings
            st.markdown("---")
            st.markdown("### Summary & Key Findings")
            score_labels = {
                1: 'Very Calm', 2: 'Calm',
                3: 'Moderate', 4: 'Elevated', 5: 'High Stress'
            }
            score_label = score_labels.get(
                int(cs_current_score), 'Unknown')
            summary_cs = (
                f"The credit spread is currently {cs_current_spread:.1f} "
                f"basis points as of {cs_current_date} — "
                f"a stress score of {cs_current_score:.0f}/5 "
                f"({score_label}). This reading is higher than "
                f"{pct_rank:.0f}% of all readings since 2010. "
                f"The average spread over the selected period was "
                f"{avg_spread_cs:.1f} basis points."
            )
            st.markdown(f"""
            <div class="dynamic-section">
                <h3>Summary</h3>
                <p>{summary_cs}</p>
            </div>
            """, unsafe_allow_html=True)

            # What It Means
            st.markdown("### What It Means")
            if cs_current_score <= 2:
                meanings_cs = [
                    'High Yield bonds and Investment Grade bonds are '
                    'moving in line with each other. Investors are '
                    'comfortable lending to riskier companies — '
                    'a sign of healthy credit conditions.',
                    'When the spread is calm it means the market does '
                    'not see elevated default risk in corporate bonds. '
                    'Companies can borrow cheaply which supports '
                    'economic growth.',
                    'Calm credit conditions typically coincide with '
                    'stable or rising equity markets and low financial '
                    'system stress.',
                ]
            elif cs_current_score == 3:
                meanings_cs = [
                    'The spread between High Yield and Investment Grade '
                    'bonds is widening somewhat — investors are becoming '
                    'slightly more cautious about lending to riskier '
                    'companies.',
                    'A moderate stress reading does not necessarily '
                    'signal a crisis but it warrants attention. '
                    'The direction of the spread matters — '
                    'is it widening or narrowing?',
                    'Moderate stress often appears during periods of '
                    'economic uncertainty or Fed policy shifts — '
                    'watch for the spread to either stabilize '
                    'or accelerate from here.',
                ]
            else:
                meanings_cs = [
                    'High Yield bonds are significantly underperforming '
                    'Investment Grade bonds — investors are pulling back '
                    'from risky lending. This is one of the most '
                    'reliable early warning signals in finance.',
                    'When spreads widen sharply it means the market is '
                    'pricing in higher default risk for corporate bonds. '
                    'Companies with weak balance sheets struggle to '
                    'borrow which slows economic activity.',
                    'Elevated and high stress readings have historically '
                    'preceded or coincided with equity market stress. '
                    'The 2008 crisis, 2020 COVID crash, and 2022 rate '
                    'hike cycle all showed elevated credit stress before '
                    'equity markets fully reflected the risk.',
                ]
            for point in meanings_cs:
                st.markdown(f"""
                <div class="dynamic-section"
                style="border-left: 4px solid #333333;">
                    <p>{point}</p>
                </div>
                """, unsafe_allow_html=True)

            # What to Watch
            st.markdown("### What to Watch")
            if cs_current_score <= 2:
                watch_cs = [
                    'Watch for any sudden widening in the spread — '
                    'that is the first warning sign of stress building',
                    'Monitor HYG price directly — a sharp decline '
                    'in HYG is a real time credit stress signal',
                    'Watch equity volatility — VIX spikes often '
                    'accompany credit spread widening',
                    'Fed policy changes — rate hikes can trigger '
                    'spread widening for high yield issuers',
                ]
            elif cs_current_score == 3:
                watch_cs = [
                    'Direction of the spread — widening further '
                    'toward score 4 is a warning to reduce risk',
                    'HYG vs LQD relative performance week over week',
                    'High yield default rates — rising defaults '
                    'accelerate spread widening',
                    'Fed communications — hawkish tone can push '
                    'spreads wider quickly',
                ]
            else:
                watch_cs = [
                    'Watch for spread to peak and start narrowing — '
                    'that signals the worst stress may be passing',
                    'Monitor for contagion to equity markets — '
                    'wide spreads often lead equity declines',
                    'Watch Fed response — emergency rate cuts or '
                    'liquidity support can rapidly tighten spreads',
                    'High yield default rates — the ultimate '
                    'confirmation of whether stress is systemic',
                ]
            col1, col2 = st.columns(2)
            for i, point in enumerate(watch_cs):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="dynamic-section"
                    style="padding: 0.8rem 1rem;">
                        <p>➜ {point}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Historical Context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Current Spread",
                f"{cs_current_spread:.1f} bps")
            h2.metric("Average Spread",
                f"{avg_spread_cs:.1f} bps", "selected period")
            h3.metric("Widest Spread",
                f"{max_spread_cs:.1f} bps",
                spread.idxmax().strftime('%b %Y'))
            h4.metric("Tightest Spread",
                f"{min_spread_cs:.1f} bps",
                spread.idxmin().strftime('%b %Y'))

            # Charts
            st.markdown("---")
            st.markdown("### Charts")
            fig, axes = plt.subplots(2, 1, figsize=(12, 10))
            fig.patch.set_facecolor('#FFFFFF')
            for ax in axes:
                ax.set_facecolor('#F9F9F9')
                ax.tick_params(colors='#333333')
                ax.xaxis.label.set_color('#333333')
                ax.yaxis.label.set_color('#333333')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#CCCCCC')
            axes[0].axhspan(spread_df['spread'].quantile(0.80),
                spread_df['spread'].max(),
                alpha=0.08, color='#D85A30',
                label='High Stress Zone')
            axes[0].axhspan(spread_df['spread'].min(),
                spread_df['spread'].quantile(0.20),
                alpha=0.08, color='#1D9E75',
                label='Low Stress Zone')
            axes[0].plot(spread_df.index, spread_df['spread'],
                color='#CCCCCC', linewidth=0.5, alpha=0.5)
            axes[0].plot(spread_df.index,
                spread_df['spread_smooth'],
                color='#333333', linewidth=2,
                label='Credit Spread (21-day avg)')
            axes[0].scatter(spread_df.index[-1],
                spread_df['spread_smooth'].iloc[-1],
                color='#D85A30', s=80, zorder=5,
                label=f'Today: {cs_current_spread:.1f} bps')
            axes[0].set_title(
                'Credit Spread — HYG vs LQD (Basis Points)',
                color='#333333', fontsize=13, fontweight='bold')
            axes[0].set_ylabel('Spread (bps)', color='#333333')
            axes[0].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=9)
            axes[0].grid(axis='y', color='#DDDDDD', linewidth=0.5)
            stress_smooth = spread_df['stress_score'].rolling(21).mean()
            axes[1].fill_between(stress_smooth.index, 0, stress_smooth,
                where=stress_smooth <= 2,
                color='#1D9E75', alpha=0.5, label='Low (1-2)')
            axes[1].fill_between(stress_smooth.index, 0, stress_smooth,
                where=(stress_smooth > 2) & (stress_smooth <= 3),
                color='#F5A623', alpha=0.5, label='Moderate (3)')
            axes[1].fill_between(stress_smooth.index, 0, stress_smooth,
                where=(stress_smooth > 3) & (stress_smooth <= 4),
                color='#E8722A', alpha=0.5, label='Elevated (4)')
            axes[1].fill_between(stress_smooth.index, 0, stress_smooth,
                where=stress_smooth > 4,
                color='#D85A30', alpha=0.5, label='High (5)')
            axes[1].plot(stress_smooth.index, stress_smooth,
                color='#333333', linewidth=1.5)
            axes[1].axhline(y=cs_current_score,
                color='#D85A30', linestyle='--', linewidth=1.2,
                label=f'Current: {cs_current_score:.0f}/5')
            axes[1].set_title(
                'Credit Stress Score — 21-Day Smoothed',
                color='#333333', fontsize=13, fontweight='bold')
            axes[1].set_ylabel('Stress Score', color='#333333')
            axes[1].set_ylim(0, 5.5)
            axes[1].set_yticks([1, 2, 3, 4, 5])
            axes[1].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=9)
            axes[1].grid(axis='y', color='#DDDDDD', linewidth=0.5)
            plt.tight_layout(pad=2.0)
            st.pyplot(fig)

        # ── FULL RESEARCH NOTEBOOK ─────────────────────────────
        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Credit Spread Monitor including all
            code, charts, stress score analysis, and historical
            period breakdown on GitHub:<br><br>
            github.com/sidneyppratt-svg/credit-spread-monitor
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MODEL 4 — HOCKEY PATHWAY NAVIGATOR
# ══════════════════════════════════════════════════════════════
    elif model == "Hockey Pathway Navigator":
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
        st.dataframe(df_leagues, use_container_width=True,
                     hide_index=True)

        st.markdown("---")
        st.markdown("### Personalized Pathway Finder")
        col1, col2 = st.columns(2)
        with col1:
            player_age = st.number_input("Player Age",
                min_value=6, max_value=22, value=15)
            player_location = st.selectbox("Location", [
                "Midwest",
                "East Coast / Northeast",
                "West Coast",
                "South",
                "Canada",
            ])
        with col2:
            player_level = st.selectbox("Current Level", [
                "Learn to Skate / Mite",
                "Squirt",
                "Peewee AAA",
                "Bantam AAA",
                "Midget Minor",
                "Midget Major",
                "High School Varsity",
                "Prep School",
                "Junior Hockey",
            ])
            player_goal = st.selectbox("Goal", [
                "NCAA D1 or Pro",
                "NCAA D3 or ACHA",
                "Just love the game",
            ])
            player_league = st.selectbox(
                "Current Junior League (if applicable)", [
                    "Not in junior hockey yet",
                    "USHL", "AJHL", "NAHL",
                    "USPHL NCDC", "EHL",
                    "USPHL Premier", "USPHL Elite", "NA3HL",
                ])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Get My Pathway Recommendation"):
            junior_league = None if \
                player_league == "Not in junior hockey yet" \
                else player_league
            league_outcomes = {
                'USHL': {
                    'college':    'NCAA D1 scholarship highly likely',
                    'scholarship':'Full or partial athletic scholarship very common',
                    'cost':       'FREE — teams pay stipends',
                    'realistic':  'Over 90% of USHL players play college hockey. '
                                  'D1 scholarship is the most common outcome.',
                },
                'AJHL': {
                    'college':    'NCAA D1 possible, D3 common',
                    'scholarship':'Athletic scholarship possible at D1',
                    'cost':       'Under $3,000/year — billet family system',
                    'realistic':  'Strong pipeline to US and Canadian college programs.',
                },
                'NAHL': {
                    'college':    'NCAA D1 possible, D3 most common',
                    'scholarship':'Partial athletic scholarship possible',
                    'cost':       '$5,000 - $8,000 per year',
                    'realistic':  'D3 is the most common outcome. '
                                  'D1 offers happen but are not guaranteed.',
                },
                'USPHL NCDC': {
                    'college':    'NCAA D3 most common — small private schools',
                    'scholarship':'NO athletic scholarship. Academic merit aid only.',
                    'cost':       '$8,000 - $12,000 per year',
                    'realistic':  'Most players land at small private NCAA D3 schools. '
                                  'Plan for academic scholarships not athletic scholarships.',
                },
                'EHL': {
                    'college':    'NCAA D3 most common — northeast schools',
                    'scholarship':'NO athletic scholarship. Academic merit aid only.',
                    'cost':       '$8,000 - $12,000 per year',
                    'realistic':  'Most players attend small private D3 schools '
                                  'in New England.',
                },
                'USPHL Premier': {
                    'college':    'NCAA D3 small private schools or ACHA D1',
                    'scholarship':'NO athletic scholarship. Academic merit aid only.',
                    'cost':       '$7,000 - $10,000 per year',
                    'realistic':  'Players typically land at small private D3 '
                                  'schools or ACHA D1 programs.',
                },
                'USPHL Elite': {
                    'college':    'ACHA D1 or very small NCAA D3 schools',
                    'scholarship':'NO athletic scholarship. Academic merit aid only.',
                    'cost':       '$5,000 - $8,000 per year',
                    'realistic':  'Entry level junior league. Moving up to '
                                  'USPHL Premier or USPHL NCDC significantly '
                                  'improves college options.',
                },
                'NA3HL': {
                    'college':    'ACHA D1 or small NCAA D3 schools',
                    'scholarship':'NO athletic scholarship. Academic merit aid only.',
                    'cost':       '$4,000 - $7,000 per year',
                    'realistic':  'Development league. Players who move up to '
                                  'NAHL significantly improve college options.',
                },
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
                recs = [
                    "Focus on skill development and fun above all else.",
                    "Play multiple sports — do not specialize yet.",
                    "Look for quality AAA programs in your area.",
                    "Start researching prep schools if interested.",
                ]
                opps = [
                    "AAA programs in your region",
                    "USA Hockey national tournaments",
                    "Summer development camps",
                    "Prep school information sessions",
                ]
                next_step = "Attend one major showcase and focus on loving the game."
            elif player_age <= 14:
                recs = [
                    "AAA Bantam is the most critical age for junior development.",
                    "USHL scouts begin watching at this level.",
                    "Start building a highlight reel now.",
                    "Attend USHL and NAHL showcases.",
                    "Research prep schools seriously.",
                ]
                opps = [
                    "AAA Bantam Major programs",
                    "Prep school hockey programs",
                    "USHL and NAHL prospect showcases",
                    "USA Hockey Select 15 and Select 16 camps",
                    "Shattuck St. Marys — top prep school pipeline",
                ]
                next_step = "Get on a AAA Bantam team and attend at least one major showcase."
            elif player_age <= 16:
                recs = [
                    "Critical decision point — junior hockey or high school.",
                    "USHL draft eligible at 16 — this is your D1 window.",
                    "NAHL is a strong Tier 2 option.",
                    "USPHL NCDC and EHL lead to D3 not D1 scholarships.",
                    "Email every junior coach with your highlight reel now.",
                ]
                opps = [
                    "USHL Phase 1 and Phase 2 drafts",
                    "NAHL Draft and free agent camps",
                    "USPHL NCDC tryouts",
                    "EHL tryouts",
                    "Prep school for one more development year",
                ]
                next_step = "Email junior coaches directly. Do not wait to be discovered."
            elif player_age <= 18:
                recs = [
                    "Junior hockey should be your priority.",
                    "The league you play in determines your college level.",
                    "USHL and NAHL are your best paths to D1.",
                    "USPHL NCDC and EHL most commonly lead to D3 only.",
                    "Email college coaches directly with your highlight reel.",
                ]
                opps = [
                    "USHL free agent camps",
                    "NAHL free agent camps",
                    "USPHL NCDC tryouts",
                    "EHL tryouts",
                    "AJHL tryouts",
                    "NCAA D3 coaches — email directly",
                ]
                next_step = "Junior hockey now. Email every coach. Cast a wide net."
            else:
                recs = [
                    "ACHA D1 and D2 are great options to keep playing.",
                    "Play at the school that fits you academically.",
                    "Strong academics open more doors at this stage.",
                    "Hockey is a lifelong sport — enjoy every level.",
                ]
                opps = [
                    "ACHA D1 at your college",
                    "ACHA D2 at your college",
                    "Adult recreational leagues",
                    "Intramural hockey",
                ]
                next_step = "Find an ACHA program at a school that fits academically."
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class="card"><h3>Recommendations</h3>
                """, unsafe_allow_html=True)
                for r in recs:
                    st.markdown(f"• {r}")
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class="card"><h3>Opportunities Now</h3>
                """, unsafe_allow_html=True)
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
        st.markdown("### Official League & Team Directories")
        st.markdown("""
        <p style="color:#555555; font-size:14px;">
        Team rosters change every season. Click each league
        below to see current teams directly from the official
        league website. Always verify before making decisions.
        </p>
        """, unsafe_allow_html=True)

        league_links = [
            ("USHL",          "Tier 1 — Top US Junior",
             "FREE",          "https://www.ushl.com/teams"),
            ("AJHL",          "Tier 1 — Top Canadian Junior",
             "Under $3,000",  "https://www.ajhl.ca/teams"),
            ("NAHL",          "Tier 2",
             "$5,000-8,000",  "https://www.nahl.com/teams"),
            ("USPHL NCDC",    "Tier 2 — Top of USPHL",
             "$8,000-12,000", "https://www.usphl.com/ncdc"),
            ("EHL",           "Tier 2 — East Coast",
             "$8,000-12,000", "https://www.ehlhockey.com/teams"),
            ("USPHL Premier", "Tier 3 — Mid USPHL",
             "$7,000-10,000", "https://www.usphl.com/premier"),
            ("USPHL Elite",   "Tier 3 — Entry USPHL",
             "$5,000-8,000",  "https://www.usphl.com/elite"),
            ("NA3HL",         "Tier 3 — Development",
             "$4,000-7,000",  "https://www.na3hl.com/teams"),
        ]
        for league, tier, cost, url in league_links:
            st.markdown(f"""
            <div class="card" style="padding: 1rem 1.5rem;">
                <div style="display:flex; justify-content:space-between;
                align-items:center;">
                    <div>
                        <h3 style="margin-bottom:0.2rem;">{league}</h3>
                        <p style="margin:0; font-size:13px;
                        color:#666666;">{tier} &nbsp;|&nbsp;
                        Annual Cost: {cost}</p>
                    </div>
                    <a href="{url}" target="_blank"
                    style="background-color:#333333; color:white;
                    padding:8px 18px; border-radius:8px;
                    text-decoration:none; font-size:13px;
                    font-weight:bold; white-space:nowrap;">
                    View Teams →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Key Things Nobody Tells You")
        tips = [
            ("USHL is completely FREE",
             "Teams pay player stipends. If drafted you pay nothing."),
            ("USPHL NCDC is inside USPHL",
             "You must be in the USPHL system to play USPHL NCDC."),
            ("Email coaches directly",
             "Do not wait to be discovered. Send your highlight reel now."),
            ("Late bloomers have time",
             "Junior hockey allows play until 20-21. Many commit at 19-20."),
            ("D3 is not a consolation prize",
             "Schools like Middlebury are elite. Academics plus hockey can beat D1."),
            ("Prep school offers financial aid",
             "Do not assume you cannot afford it. Apply before deciding."),
            ("AJHL uses billet families",
             "You live with a host family for free in Canadian junior hockey."),
            ("NA3HL to NAHL is real",
             "Players move up from Tier 3 to Tier 2 and earn D1 offers."),
            ("ACHA lets you choose your school",
             "Play hockey at whatever school fits you best academically."),
        ]
        col1, col2 = st.columns(2)
        for i, (title, desc) in enumerate(tips):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class="card">
                    <h3>• {title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Complete Hockey Pathway Map")
        st.markdown("""
        <p style="color:#555555; font-size:14px;">
        Every pathway from youth hockey to the pros —
        all 10 routes mapped in one visual.
        </p>
        """, unsafe_allow_html=True)
        try:
            img_url = "https://raw.githubusercontent.com/sidneyppratt-svg/hockey-pathway-navigator/main/hockey_pathway_map.png"
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)
        except:
            st.info("Pathway map loading — check back shortly.")

        st.markdown("---")
        st.markdown("### Real Players, Real Paths")
        st.markdown("""
        <p style="color:#555555; font-size:14px;">
        Every path is different and all of them can work.
        Here are real players at every level — from the NHL
        to college hockey — and the exact routes they took
        to get there.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-label">⭐ The NHL Route</div>
        """, unsafe_allow_html=True)

        nhl_players = [
            {
                'name':   'Connor Bedard',
                'team':   'Chicago Blackhawks — #1 Overall Pick 2023',
                'born':   'North Vancouver, BC, Canada — Born 2005',
                'path': [
                    'Youth Hockey — North Vancouver minor hockey',
                    'WHL — Regina Pats (exceptional status at age 15)',
                    'WHL — 71 goals 143 points in 57 games (2022-23)',
                    'NHL Draft — #1 Overall — Chicago Blackhawks 2023',
                    'NHL — Chicago Blackhawks',
                ],
                'key_fact': 'Bedard was granted WHL exceptional status at 15 '
                            'meaning he was so advanced he skipped the normal '
                            'age requirement entirely. His 143 points in one '
                            'WHL season was the most by any player since 1995-96.',
                'lesson': 'The Canadian major junior route (WHL, OHL, QMJHL) '
                          'is a direct path to the NHL Draft without college. '
                          'Players go pro immediately after junior hockey.',
            },
            {
                'name':   'Macklin Celebrini',
                'team':   'San Jose Sharks — #1 Overall Pick 2024',
                'born':   'North Vancouver, BC, Canada — Born 2006',
                'path': [
                    'Youth Hockey — Jr. Sharks program San Jose CA',
                    'Prep School — Shattuck St. Marys Minnesota',
                    'USHL — Chicago Steel',
                    'NCAA D1 — Boston University (Hobey Baker Award)',
                    'NHL Draft — #1 Overall — San Jose Sharks 2024',
                    'NHL — San Jose Sharks',
                ],
                'key_fact': 'Celebrini chose the US college route over Canadian '
                            'major junior. He went to Shattuck St. Marys then '
                            'the USHL with Chicago Steel then Boston University '
                            'where he won the Hobey Baker Award at just 17 — '
                            'the youngest winner ever.',
                'lesson': 'Shattuck St. Marys → USHL → NCAA D1 is one of the '
                          'most powerful pathways in US hockey. This exact route '
                          'has produced multiple number 1 overall picks.',
            },
            {
                'name':   'Will Smith',
                'team':   'San Jose Sharks — #4 Overall Pick 2023',
                'born':   'Lexington, Massachusetts, USA — Born 2005',
                'path': [
                    'Youth Hockey — Lexington MA youth hockey',
                    'Prep School — Saint Sebastians School Boston',
                    'USNTDP — US National Team Development Program Michigan',
                    'NCAA D1 — Boston College (led nation with 71 points)',
                    'NHL Draft — #4 Overall — San Jose Sharks 2023',
                    'NHL — San Jose Sharks',
                ],
                'key_fact': 'Smith took the USNTDP route — only the top 40 '
                            'players in the country aged 16-17 are invited. '
                            'His family moved from Boston to Michigan to make '
                            'it happen. He then led all of college hockey '
                            'with 71 points as a Boston College freshman.',
                'lesson': 'The USNTDP is the pinnacle of US youth hockey. '
                          'If your player gets an invite to Plymouth Michigan '
                          'you go. The family moved across the country and '
                          'it led to a top 5 NHL pick.',
            },
            {
                'name':   'Jack Hughes',
                'team':   'New Jersey Devils — #1 Overall Pick 2019',
                'born':   'Orlando, Florida, USA — Born 2001',
                'path': [
                    'Youth Hockey — multiple cities due to family moves',
                    'USNTDP — US National Team Development Program Michigan',
                    'NHL Draft — #1 Overall — New Jersey Devils 2019',
                    'NHL — New Jersey Devils',
                ],
                'key_fact': 'Jack Hughes went directly from the USNTDP to the '
                            'NHL Draft without college or major junior hockey. '
                            'His performance at the USNTDP was so dominant he '
                            'was considered ready for the NHL at 18. He set '
                            'USNTDP scoring records that still stand today.',
                'lesson': 'The USNTDP can lead directly to the NHL Draft '
                          'without college or major junior. Extremely rare '
                          'but shows there is no single correct path.',
            },
            {
                'name':   'Quinn Hughes',
                'team':   'Vancouver Canucks — #7 Overall Pick 2018',
                'born':   'Orlando, Florida, USA — Born 1999',
                'path': [
                    'Youth Hockey — multiple cities due to family moves',
                    'USNTDP — US National Team Development Program Michigan',
                    'NCAA D1 — University of Michigan (one season)',
                    'NHL Draft — #7 Overall — Vancouver Canucks 2018',
                    'NHL — Vancouver Canucks',
                ],
                'key_fact': 'Quinn Hughes played just one season at the '
                            'University of Michigan before declaring for the '
                            'NHL Draft. He used one year at Michigan to develop '
                            'against older competition then went pro. He has '
                            'since become one of the top offensive defensemen '
                            'in the NHL and a Norris Trophy finalist.',
                'lesson': 'Even one year of NCAA D1 hockey can be enough '
                          'before declaring for the NHL Draft. The University '
                          'of Michigan has produced a remarkable number '
                          'of NHL players.',
            },
        ]

        for player in nhl_players:
            st.markdown(f"""
            <div class="player-card">
                <h3>{player['name']}</h3>
                <p style="color:#666666; font-size:13px;
                margin-bottom:0.5rem;">
                {player['team']}<br>{player['born']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Pathway:**")
            path_html = " → ".join([
                f'<span class="pathway-step">{step}</span>'
                for step in player['path']
            ])
            st.markdown(
                f'<div style="margin-bottom:0.75rem;">{path_html}</div>',
                unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>Key Fact</h3>
                    <p>{player['key_fact']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <h3>Lesson for Families</h3>
                    <p>{player['lesson']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")

        st.markdown("""
        <div class="section-label-college">🎓 The College Route</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#555555; font-size:14px; margin-bottom:1rem;">
        Not everyone takes the NHL path — and that is perfectly fine.
        These players chose academics, chose their school, and kept
        playing the game they love at the college level.
        That is a win by any measure.
        </p>
        """, unsafe_allow_html=True)

        college_players = [
            {
                'name':    'Sidney Pratt',
                'team':    'Western Michigan University — ACHA D1 — #96',
                'born':    'San Francisco, CA, USA — Born 2005',
                'path': [
                    'Youth Hockey — San Francisco Sabercats USHS-CA',
                    'AAA — Golden State Eagles 18U AA 🏆 State Champion',
                    'USPHL Elite — Northern Cyclones 🏆 National Champion 2023-24',
                    'ACHA D1 — Western Michigan University (current)',
                ],
                'key_fact': 'Sidney grew up playing hockey in San Francisco — '
                            'one of the least likely places to produce a serious '
                            'junior hockey player. He earned two championships '
                            'at two different levels — a state title with the '
                            'Golden State Eagles and a national title with the '
                            'Northern Cyclones in 2023-24. He chose Western '
                            'Michigan for his Finance and Economics degree and '
                            'has kept playing ACHA D1 hockey while building '
                            'a career in quantitative finance. He also '
                            'co-founded the Northern Cyclones Financial Club — '
                            'bringing finance and hockey together in a way '
                            'nobody had done before.',
                'lesson':  'ACHA D1 means you choose the school that is right '
                           'for you academically and keep playing hockey. '
                           'No compromises. Sidney chose Western Michigan for '
                           'its Finance program and walked in as a national '
                           'champion. Hockey does not have to end when '
                           'junior hockey does.',
            },
            {
                'name':    'Luke Linart',
                'team':    'Saint Anselm College — NCAA D3 — #28 — Senior',
                'born':    'Holland, Michigan, USA — Born 2001',
                'path': [
                    'AAA Youth — Meijer AAA 15U',
                    'High School — West Ottawa HS (captain, 114 pts in 3 seasons)',
                    'USPHL Premier — Northern Cyclones (38 pts in 44 games)',
                    'NCAA D3 — Saint Anselm College',
                ],
                'key_fact': 'Luke captained West Ottawa High School and scored '
                            '114 points across three varsity seasons. He then '
                            'played USPHL Premier with the Northern Cyclones '
                            'before landing at Saint Anselm College in the '
                            'NE10 conference. As a freshman he won the NE10 '
                            'Championship and earned All-Rookie Team honors. '
                            'He has been an iron man — playing in every single '
                            'Saints game since arriving in 2022 — and carries '
                            'a 4.0 GPA. In 2025-26 he earned NE10 Second Team '
                            'All-Conference as a senior with 29 points in 32 games.',
                'lesson':  'USPHL Premier leads to real NCAA D3 opportunities '
                           'at strong academic schools. Luke went from Northern '
                           'Cyclones to a championship program at Saint Anselm '
                           'while maintaining a 4.0 GPA. The level on the ice '
                           'matters less than how you carry yourself off it.',
            },
            {
                'name':    'Eddie Shepler',
                'team':    'Milwaukee School of Engineering — NCAA D3 — #4',
                'born':    'Livonia, Michigan, USA',
                'path': [
                    'AAA Youth — Compuware 14U, Honeybaked 16U (captain)',
                    'NAHL — Bismarck Bobcats',
                    'NAHL — Minnesota Wilderness',
                    'NAHL — El Paso Rhinos',
                    'NCAA D3 — Milwaukee School of Engineering',
                ],
                'key_fact': 'Eddie spent four full seasons in the NAHL — '
                            'one of the best Tier 2 junior leagues in the US — '
                            'playing 191 games across three different teams. '
                            'He was a captain at the AAA youth level with '
                            'Honeybaked and kept grinding through junior hockey '
                            'until landing at Milwaukee School of Engineering '
                            'where he scored 11 goals in his first NCAA season.',
                'lesson':  'The NAHL is a serious Tier 2 league and four '
                           'seasons there is no small thing. Eddie proves '
                           'that the path to college hockey is not always '
                           'straight — sometimes it takes years of junior '
                           'hockey to find the right fit. The grind pays off.',
            },
        ]

        for player in college_players:
            st.markdown(f"""
            <div class="player-card-college">
                <h3>{player['name']}</h3>
                <p style="color:#666666; font-size:13px;
                margin-bottom:0.5rem;">
                {player['team']}<br>{player['born']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Pathway:**")
            path_html = " → ".join([
                f'<span class="pathway-step-college">{step}</span>'
                for step in player['path']
            ])
            st.markdown(
                f'<div style="margin-bottom:0.75rem;">{path_html}</div>',
                unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>Key Fact</h3>
                    <p>{player['key_fact']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <h3>Lesson for Families</h3>
                    <p>{player['lesson']}</p>
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
