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
    .data-source-section {
        background-color: #F0FFF4;
        border: 1px solid #A8D5B5;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .data-source-section h3 { color: #1B5E20 !important; margin-bottom: 0.5rem; }
    .data-source-section p { color: #1a1a1a !important; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="profile-placeholder">SP</div>
    <p style="text-align:center; color:#CCCCCC; font-size:11px;
    margin-bottom:0.5rem;">Photo coming soon</p>
    """, unsafe_allow_html=True)
    st.markdown("## Sidney Pratt")
    st.markdown("*Economics & Finance*")
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
# TOP NAV — always visible, left aligned
# ══════════════════════════════════════════════════════════════
page = st.radio("", ["About", "Resume", "AI Research"],
    horizontal=True,
    label_visibility="collapsed")

st.markdown("<hr style='margin-top:0.3rem; margin-bottom:1rem;'>",
    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ABOUT (opening page)
# ══════════════════════════════════════════════════════════════
if page == "About":
    st.markdown("# Sidney Pratt")
    st.markdown("""
    <div style="margin-bottom:0.75rem;">
        <span class="tag">Finance & Economics</span>
        <span class="tag">ACHA D1 Hockey</span>
        <span class="tag">AI Researcher</span>
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
        "Mortgage Market Monitor",
        "Hockey Pathway Navigator",
    ])

# ══════════════════════════════════════════════════════════════
# MODEL 1 — YIELD CURVE MONITOR
# ══════════════════════════════════════════════════════════════
    if model == "Yield Curve Monitor":
        st.markdown("## Yield Curve Monitor")
        st.markdown("*Fixed Income Relative Value Tool | Sidney Pratt*")
        st.markdown("---")

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

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Treasury Yields:</b> Live US Treasury yields downloaded
            directly from Yahoo Finance — tickers ^IRX (3-Month),
            ^FVX (5-Year), ^TNX (10-Year), ^TYX (30-Year).<br><br>
            <b>Accuracy:</b> These are real market prices and match the
            US Treasury website exactly. Updated every trading day.<br><br>
            <b>Key Spread:</b> 10Y minus 3M — the Federal Reserve's own
            preferred inversion signal used in the NY Fed recession
            probability model.<br><br>
            <b>Backtest:</b> TLT ETF historical price data from Yahoo Finance.
            All calculations performed in Python using pandas and numpy.
            No lookahead bias — prior day signal drives today's position.
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
            <p><b>STEEP</b> (10Y minus 3M above +1.50%) — Long-term rates are significantly higher than short-term rates. The market expects strong future economic growth. Banks earn wide margins borrowing short and lending long. Historically the best environment for bonds and equities. → <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br><b>NORMAL</b> (+0.50% to +1.50%) — The curve has its typical upward slope. Short-term rates are lower than long-term rates as expected. The economy is healthy with no recession signals. The most common regime. → <span style="color:#2E7D32; font-weight:bold;">HOLD TLT</span><br><br><b>FLAT</b> (-0.50% to +0.50%) — Short and long-term rates are nearly equal. The market is uncertain about the future. Banks earn little margin. Often a transition zone between healthy and inverted. A warning sign that the economy may be slowing. → <span style="color:#E65100; font-weight:bold;">MOVE TO CASH</span><br><br><b>INVERTED</b> (-0.50% to 0%) — Short-term rates are higher than long-term rates. This is abnormal and historically the most reliable recession predictor. Means the market expects the Fed will cut rates sharply in the future because the economy is slowing. Every major US recession since 1970 was preceded by an inversion. → <span style="color:#C62828; font-weight:bold;">MOVE TO CASH</span><br><br><b>DEEPLY INVERTED</b> (below -0.50%) — The most extreme inversion level. Short-term rates are significantly above long-term rates. The Fed has tightened aggressively and the market expects a hard landing. The 2022-23 inversion reached -1.70% — the deepest since the 1980s Volcker era. High alert. → <span style="color:#B71C1C; font-weight:bold;">MOVE TO CASH</span></p>
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
                value=datetime.date.today(), key="yc_end")
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
                st.success("HOLD TLT — Long duration bonds are safe to hold in this regime.")
            elif current_regime == 'FLAT':
                st.warning("MOVE TO CASH — Curve is in transition zone. Reduce long duration bond exposure.")
            else:
                st.error("MOVE TO CASH — Avoid long duration bonds during inversion.")

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
        st.markdown("## Multi-Asset Market Regime Detector")
        st.markdown("*Cross-Asset Quantitative Research Tool | Sidney Pratt*")
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

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>SPY (US Equities):</b> S&P 500 ETF — Yahoo Finance.
            Real closing prices adjusted for dividends and splits.<br><br>
            <b>AGG (Investment Grade Bonds):</b> iShares Core US Aggregate
            Bond ETF — Yahoo Finance. Real closing prices.<br><br>
            <b>HYG (High Yield Credit):</b> iShares iBoxx High Yield
            Corporate Bond ETF — Yahoo Finance. Real closing prices.<br><br>
            <b>GLD (Gold):</b> SPDR Gold Shares ETF — Yahoo Finance.
            Real closing prices.<br><br>
            <b>Accuracy:</b> All four data sources are real market prices
            from Yahoo Finance. ETF prices are adjusted for dividends and
            splits. These match Bloomberg terminal closing prices exactly.<br><br>
            <b>Model:</b> Gaussian Mixture Model from scikit-learn.
            Unsupervised — no labels used during training.
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
            <h3>Regime Classification</h3>
            <p><b>RISK-ON</b> — Investors are comfortable taking risk. All four asset classes are behaving normally — stocks are rising, high yield credit is performing well, and there is no unusual demand for safe havens like gold or government bonds. This is the environment where equity exposure makes sense and credit spreads are calm. The model signals stay invested in equities.<br><br><b>RISK-OFF</b> — Investors are pulling back from risk. Stress is showing up across multiple asset classes simultaneously — stocks falling, high yield credit underperforming investment grade, and demand rising for safe havens like gold and government bonds. This is the environment where capital preservation matters more than returns. The model signals move to cash.<br><br><b>What makes this model different:</b> Most indicators watch one asset. This model watches four at once. A single bad day in stocks does not trigger RISK-OFF. What triggers it is when stocks, credit, and safe haven assets all move together in a stress pattern — exactly what happens during real market crises.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Asset Classes Covered</h3>
            <p><b>SPY — US Equities:</b> S&P 500 ETF — the broadest measure of US stock market performance. Rises in RISK-ON, falls sharply in RISK-OFF. The primary return driver in this model.<br><br><b>AGG — Investment Grade Bonds:</b> High quality corporate and government bonds. Often rises during RISK-OFF as investors flee to safety. Acts as the counter-weight to equities.<br><br><b>HYG — High Yield Credit:</b> Riskier corporate bonds from companies with lower credit ratings. Falls sharply during stress because investors demand more compensation for default risk. Often the first asset to show cracks before stocks fall.<br><br><b>GLD — Gold:</b> The classic safe haven. Spikes during geopolitical stress, inflation fears, and financial crises. When gold and bonds both rise while stocks fall, that is a strong RISK-OFF signal.</p>
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
                value=datetime.date.today())
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
                cum_s, tot_s, ret_s, vol_s, sh_s, dd_s = get_metrics(strat)
                cum_b, tot_b, ret_b, vol_b, sh_b, dd_b = get_metrics(bh)
                latest      = smooth['label'].iloc[-1]
                latest_date = smooth.index[-1].strftime('%B %d, %Y')
                risk_off_pct = float(
                    (smooth['label'] == 'RISK-OFF').mean() * 100)

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
                st.success("STAY INVESTED — Model signals holding SPY. "
                           "Cross-asset conditions support equity exposure.")
            else:
                st.error("MOVE TO CASH — Model signals reducing equity "
                         "exposure. Cross-asset stress detected.")

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
# MODEL 3 — CREDIT SPREAD MONITOR (FRED OAS — Bloomberg Accurate)
# ══════════════════════════════════════════════════════════════
    elif model == "Credit Spread Monitor":
        st.markdown("## Credit Spread Monitor")
        st.markdown("*Fixed Income Credit Research Tool | Sidney Pratt*")
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the ICE BofA US High Yield Option-Adjusted
            Spread (OAS) — the professional benchmark used by Bloomberg
            and every major credit desk in the world. The spread is
            converted into a stress score from 1 to 5 using 16 years
            of real daily data from 2010 to present.<br><br>
            When high yield credit spreads widen it signals investors
            are demanding more compensation for credit risk — one of
            the earliest and most reliable warning signals in fixed
            income markets. This model detects that widening in real
            time and classifies it against historical context.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Real ICE BofA OAS spread pulled live from FRED on every run<br><br>
            • Credit stress score from 1 (very calm) to 5 (high stress)<br><br>
            • Percentile ranking against full history since 2010<br><br>
            • OAS regime classification — Tight, Normal, Wide, Very Wide<br><br>
            • 21-day rolling spread smoothing to filter daily noise<br><br>
            • Three chart visualization — OAS over time, stress score, HYG vs LQD<br><br>
            • Dynamic signal and interpretation that updates every run
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Primary Data:</b> ICE BofA US High Yield Option-Adjusted Spread
            (FRED series: BAMLH0A0HYM2) — pulled directly from the Federal
            Reserve Economic Data (FRED) database via the pandas-datareader
            library on every run.<br><br>
            <b>Accuracy:</b> This is the exact same OAS series displayed on
            Bloomberg terminals and used by every major credit desk. Published
            daily by the Federal Reserve Bank of St. Louis. 100% accurate —
            not a proxy or approximation.<br><br>
            <b>HYG & LQD:</b> ETF closing prices from Yahoo Finance used for
            the relative performance chart only — not for the OAS calculation.<br><br>
            <b>Stress Score:</b> Current OAS ranked as a percentile against all
            historical readings since 2010, then divided into five equal quintile
            bins (score 1-5). Methodology is objective and repeatable.
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
                indicators in fixed income markets. When OAS widens it
                signals investors are demanding more compensation for
                default risk — often weeks or months before stress shows
                up in equity markets.<br><br>
                The 2008 crisis, 2011 EU debt crisis, 2016 oil crash,
                2020 COVID crash, and April 2025 tariff shock all showed
                up first in credit spreads before hitting equity markets.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="static-section">
                <h3>Methodology</h3>
                <p>
                Downloads the ICE BofA OAS spread directly from FRED
                (BAMLH0A0HYM2). This is the option-adjusted spread
                between US high yield bonds and US Treasuries —
                the professional benchmark.<br><br>
                The spread is ranked as a percentile against all
                historical readings and converted into a stress score
                from 1 to 5 using equal quintile bins.<br><br>
                A 21-day rolling average smooths daily noise.<br><br>
                <b>Methodology never changes regardless of date range.</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Stress Score & OAS Regime Classification</h3>
            <p>The OAS (Option-Adjusted Spread) is the extra yield investors demand to hold high yield bonds instead of risk-free Treasuries. Think of it as the market's price for corporate default risk. When the OAS is low investors are relaxed. When it spikes investors are scared and demanding more compensation.<br><br><b>Score 1 — VERY CALM (OAS below 2.50%):</b> Investors are extremely comfortable lending to risky companies. Default risk is being priced at historically low levels. Credit markets are healthy. Seen during strong economic expansions with low unemployment and rising corporate earnings.<br><br><b>Score 2 — CALM (OAS 2.50% to 3.00%):</b> Credit conditions are normal. Spreads are near their long-run average. No signs of stress. A good environment for holding high yield bonds.<br><br><b>Score 3 — MODERATE (OAS 3.00% to 3.50%):</b> Spreads are starting to widen above average. Investors are becoming more cautious. Worth monitoring whether this is a temporary move or the start of a trend toward stress.<br><br><b>Score 4 — ELEVATED (OAS 3.50% to 5.00%):</b> <span style="color:#E64A19; font-weight:bold;">Credit stress is building. Investors are demanding significantly more compensation for default risk. This level has historically preceded recessions and market downturns. Consider reducing exposure to high yield bonds and risk assets.</span><br><br><b>Score 5 — HIGH STRESS (OAS above 5.00%):</b> <span style="color:#B71C1C; font-weight:bold;">Crisis-level spreads. The market is pricing in a significant wave of corporate defaults. This territory was seen during the 2008 financial crisis, COVID March 2020, and the 2016 oil price collapse. Reduce credit risk exposure immediately.</span></p>
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
                value=datetime.date.today(), key="cs_end")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Credit Spread Model"):
            with st.spinner("Downloading ICE BofA OAS spread from FRED..."):

                # Pull real OAS spread from FRED
                oas = web.DataReader("BAMLH0A0HYM2", "fred",
                    str(start_date_cs), str(end_date_cs))
                oas.columns = ["OAS_Spread"]

                # HYG and LQD for relative performance chart
                cs_prices = yf.download(['HYG', 'LQD'],
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
                    elif score == 4: return "CAUTION — Reduce high yield exposure"
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
                st.success(f"RISK-ON — {cur_signal}")
            elif cur_score == 3:
                st.warning(f"NEUTRAL — {cur_signal}")
            else:
                st.error(f"CAUTION — {cur_signal}")

            # Results
            st.markdown("---")
            st.markdown("### Results")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("OAS Spread",    f"{cur_oas:.2f}%")
            m2.metric("OAS (bps)",     f"{cur_bps:.0f} bps")
            m3.metric("Stress Score",  f"{cur_score:.0f} / 5 — {cur_label}")
            m4.metric("Percentile",    f"{cur_pct:.0f}th since 2010")

            # Historical Context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Historical Avg",   f"{avg_oas:.2f}%", "since 2010")
            h2.metric("vs Average",       f"{cur_oas - avg_oas:+.2f}%")
            h3.metric("All-Time High",    f"{max_oas:.2f}%", max_date)
            h4.metric("All-Time Low",     f"{min_oas:.2f}%", min_date)

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
        st.markdown("## Mortgage Market Monitor")
        st.markdown("*Fixed Income Mortgage Research Tool | Sidney Pratt*")
        st.markdown("---")

        st.markdown("""
        <div class="static-section">
            <h3>Overview</h3>
            <p>
            This model tracks the official Freddie Mac 30-year fixed
            mortgage rate, the mortgage spread over the 10-year Treasury
            yield, and the refinancing environment using real data pulled
            directly from the Federal Reserve (FRED).<br><br>
            The mortgage spread — the gap between the 30-year mortgage
            rate and the 10-year Treasury yield — is the key signal
            watched by every mortgage trading desk. When the spread
            widens it signals stress in the MBS market. When it narrows
            it signals lender competition and tight credit conditions.
            Built on 16 years of real daily data from 2010 to present.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="static-section">
            <h3>Key Features</h3>
            <p>
            • Official Freddie Mac 30-year mortgage rate pulled live from FRED<br><br>
            • Mortgage spread calculated against the 10-year Treasury yield<br><br>
            • Spread regime classification — Tight, Normal, Wide, Very Wide<br><br>
            • Refinancing environment signal — Minimal, Some, Active, Wave<br><br>
            • Prepayment risk classification — Low, Moderate, High<br><br>
            • Percentile ranking against full history since 2010<br><br>
            • Three chart visualization — rates, spread regime, MBB vs AGG
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="data-source-section">
            <h3>Data Sources</h3>
            <p>
            <b>Primary Data:</b> Freddie Mac Primary Mortgage Market Survey
            (FRED series: MORTGAGE30US) — the official 30-year fixed mortgage
            rate published weekly by the Federal Reserve Bank of St. Louis.<br><br>
            <b>Accuracy:</b> This is the exact same mortgage rate reported by
            Bloomberg, CNBC, and every major financial news source. 100%
            accurate — not a proxy or approximation.<br><br>
            <b>Treasury Yields:</b> 10-year (^TNX) and 30-year (^TYX) yields
            from Yahoo Finance — match the US Treasury website exactly.<br><br>
            <b>MBB & AGG:</b> ETF closing prices from Yahoo Finance used for
            the relative performance chart only.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="static-section">
                <h3>Why It Matters</h3>
                <p>
                The mortgage spread is the primary signal watched by
                every mortgage trading desk. It determines whether MBS
                are cheap or expensive relative to Treasuries, drives
                prepayment modeling assumptions, and signals stress in
                the housing finance system before it shows up elsewhere.<br><br>
                The November 2022 spike to 3.39% — the widest since the
                2008 crisis — showed how rapidly the spread can move
                during Fed rate hike cycles. Every mortgage desk
                watched that spread daily.
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
            <p>The mortgage spread is the gap between the official 30-year mortgage rate and the 10-year Treasury yield. It represents the extra cost borrowers pay above the risk-free rate to compensate lenders for prepayment risk, credit risk, and servicing costs. A wider spread means mortgages are more expensive relative to Treasuries — a signal of stress or uncertainty in the housing finance market.<br><br><b>TIGHT (below 1.50%):</b> Lenders are competing aggressively for mortgage business. The extra cost of a mortgage above Treasuries is historically low. MBS are expensive relative to Treasuries — investors are accepting less compensation than usual for mortgage risk. Good for new homebuyers but less attractive for MBS investors buying at tight levels.<br><br><b>NORMAL (1.50% to 2.00%):</b> Mortgage risk is priced appropriately relative to Treasuries. The spread is in its historical average range. Lenders are earning a fair margin. Normal prepayment modeling assumptions apply. The most common regime — the market is functioning as expected.<br><br><b>WIDE (2.00% to 2.50%):</b> <span style="color:#E65100; font-weight:bold;">Lenders are demanding more compensation above Treasuries. This can reflect uncertainty about prepayment speeds, tighter bank balance sheets, or broader fixed income stress. MBS are cheap relative to Treasuries. Could be a buying opportunity if the widening is technical — worth monitoring closely.</span><br><br><b>VERY WIDE (above 2.50%):</b> <span style="color:#B71C1C; font-weight:bold;">Significant stress in the mortgage market. Lenders are demanding crisis-level compensation above Treasuries. This territory was seen during the 2008 financial crisis, COVID March 2020, and the November 2022 rate shock when the Fed was hiking aggressively. MBS are very cheap but duration risk is high.</span><br><br><b>MINIMAL REFI:</b> Current mortgage rates are not significantly below where they were 12 months ago. Most borrowers have little financial incentive to refinance. Prepayment speeds are near baseline — MBS duration is close to its stated maturity.<br><br><b>SOME REFI:</b> Rates have fallen modestly. Some borrowers who were well above the current rate may refinance. Prepayment speeds are slightly above baseline.<br><br><b>ACTIVE REFI:</b> Rates have fallen meaningfully — more than 0.75% below a year ago. A meaningful portion of existing mortgages are in the money to refinance. Prepayment speeds are elevated. MBS duration is shortening.<br><br><b>REFI WAVE:</b> <span style="color:#B71C1C; font-weight:bold;">Rates have fallen more than 1.50% below a year ago. A large portion of the existing mortgage market can benefit from refinancing. Prepayment speeds are accelerating rapidly. MBS holders receive principal back much faster than expected — duration collapses. A major risk for MBS investors who bought at higher prices.</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Run the Model")
        col1, col2 = st.columns(2)
        with col1:
            start_date_mm = st.date_input("Start Date",
                value=datetime.date(2010, 1, 1), key="mm_start")
        with col2:
            end_date_mm = st.date_input("End Date",
                value=datetime.date.today(), key="mm_end")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Run Mortgage Market Monitor"):
            with st.spinner("Downloading official Freddie Mac mortgage rate from FRED..."):

                # Official Freddie Mac 30-Year Fixed Mortgage Rate from FRED
                mortgage = web.DataReader("MORTGAGE30US", "fred",
                    str(start_date_mm), str(end_date_mm))
                mortgage.columns = ["Mortgage_Rate"]

                # Treasury yields and ETFs from Yahoo Finance
                tnx = yf.download("^TNX", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                tyx = yf.download("^TYX", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                mbb = yf.download("MBB", start=str(start_date_mm),
                    end=str(end_date_mm), auto_adjust=True,
                    progress=False)["Close"]
                agg = yf.download("AGG", start=str(start_date_mm),
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
                    f"MBS duration is close to its stated maturity.")
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
            m4.metric("Percentile since 2010",  f"{pct_rank_mm:.0f}th")

            s1, s2, s3 = st.columns(3)
            s1.metric("Spread Regime",          cur_regime_mm)
            s2.metric("Refi Environment",       cur_refi_mm)
            s3.metric("Prepayment Risk",        cur_prepay_mm)

            # Historical context
            st.markdown("---")
            st.markdown("### Historical Context")
            h1, h2, h3, h4 = st.columns(4)
            h1.metric("Historical Avg",    f"{avg_spread_mm:.2f}%", "since 2010")
            h2.metric("vs Average",        f"{cur_spread_mm - avg_spread_mm:+.2f}%")
            h3.metric("All-Time High",     f"{max_spread_mm:.2f}%", max_date_mm)
            h4.metric("All-Time Low",      f"{min_spread_mm:.2f}%", min_date_mm)

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

# ══════════════════════════════════════════════════════════════
# MODEL 5 — HOCKEY PATHWAY NAVIGATOR
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
        st.markdown("<br>", unsafe_allow_html=True)
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
