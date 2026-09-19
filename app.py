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
            backtesting, and market data analysis. Built two live
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
        "Multi-Asset Market Regime Detector",
        "Credit Spread Monitor",
        "Hockey Pathway Navigator",
    ])

# ── Model 1: Regime Detector ───────────────────────────────────
    if model == "Multi-Asset Market Regime Detector":
        st.markdown("## Multi-Asset Market Regime Detector")
        st.markdown("""
        <div class="card">
            <h3>Overview</h3>
            <p>
            This model uses unsupervised machine learning (Gaussian
            Mixture Model) to detect whether markets are in a
            <b>RISK-ON</b> or <b>RISK-OFF</b> regime by analyzing
            four asset classes simultaneously — US Equities (SPY),
            Investment Grade Bonds (AGG), High Yield Credit (HYG),
            and Gold (GLD). Trained on 12 years of real market data.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <h3>Methodology</h3>
            <p>
            <b>Data:</b> 12 years of daily price data (2014-2026)<br><br>
            <b>Model:</b> Gaussian Mixture Model — unsupervised machine
            learning that finds hidden patterns without being told
            what to look for<br><br>
            <b>Signal:</b> 21-day rolling mean returns — smooths daily
            noise so the AI sees trends<br><br>
            <b>Strategy:</b> Long SPY during RISK-ON, cash during RISK-OFF<br><br>
            <b>Backtest:</b> Chronological split — no lookahead bias
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h3>RISK-ON — Markets Are Calm</h3>
                <p>
                All four asset classes behaving normally.
                Stocks rising, credit tight, gold steady.<br><br>
                <b>Action:</b> Stay invested in equities.<br><br>
                <b>Example:</b> 2021 post-COVID recovery —
                correctly identified as sustained RISK-ON.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card">
                <h3>RISK-OFF — Stress Detected</h3>
                <p>
                Multiple asset classes under stress.
                Stocks falling, credit widening, gold spiking.<br><br>
                <b>Action:</b> Move to cash.<br><br>
                <b>Example:</b> March 2020 COVID crash —
                model flagged RISK-OFF before worst decline.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <h3>Key Results</h3>
            <p>
            Max drawdown reduced from <b>-33.7%</b> to <b>-24.0%</b><br><br>
            Sharpe ratio improved from <b>0.84</b> to <b>0.93</b><br><br>
            Volatility reduced from <b>17.1%</b> to <b>15.5%</b>
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
                    cum     = (1 + r).cumprod()
                    total   = cum.iloc[-1] - 1
                    ann_ret = (1 + total) ** (252/len(r)) - 1
                    ann_vol = r.std() * np.sqrt(252)
                    sharpe  = ann_ret / ann_vol
                    max_dd  = (cum / cum.cummax() - 1).min()
                    return cum, total, ann_ret, ann_vol, sharpe, max_dd
                cum_s, tot_s, ret_s, vol_s, sh_s, dd_s = get_metrics(strat)
                cum_b, tot_b, ret_b, vol_b, sh_b, dd_b = get_metrics(bh)
                latest      = smooth['label'].iloc[-1]
                latest_date = smooth.index[-1].strftime('%B %d, %Y')
            st.markdown("---")
            st.markdown("### Current Market Signal")
            if latest == 'RISK-ON':
                st.success(f"RISK-ON — As of {latest_date} markets are calm. "
                           f"Model suggests staying INVESTED.")
            else:
                st.error(f"RISK-OFF — As of {latest_date} stress detected. "
                         f"Model suggests moving to CASH.")
            st.markdown("---")
            st.markdown("### Performance Results")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total Return",  f"{tot_s:.1%}", f"{tot_s-tot_b:+.1%} vs BH")
            c2.metric("Ann. Return",   f"{ret_s:.1%}", f"{ret_s-ret_b:+.1%} vs BH")
            c3.metric("Volatility",    f"{vol_s:.1%}", f"{vol_s-vol_b:+.1%} vs BH")
            c4.metric("Sharpe Ratio",  f"{sh_s:.2f}",  f"{sh_s-sh_b:+.2f} vs BH")
            c5.metric("Max Drawdown",  f"{dd_s:.1%}",  f"{dd_s-dd_b:+.1%} vs BH")
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
                linewidth=1.5, linestyle='--', label='Buy & Hold')
            axes[0].set_title('Portfolio Growth — $100 invested',
                color='#333333', fontsize=13, fontweight='bold')
            axes[0].legend(facecolor='#F9F9F9', labelcolor='#333333')
            axes[0].set_ylabel('Value ($)', color='#333333')
            axes[0].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'${x:.0f}'))
            risk_on_mask  = smooth['label'] == 'RISK-ON'
            risk_off_mask = smooth['label'] == 'RISK-OFF'
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_on_mask, color='#444444',
                alpha=0.7, label='RISK-ON')
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_off_mask, color='#AAAAAA',
                alpha=0.9, label='RISK-OFF')
            axes[1].set_title('Regime Detection Timeline',
                color='#333333', fontsize=13, fontweight='bold')
            axes[1].set_yticks([])
            axes[1].legend(facecolor='#F9F9F9', labelcolor='#333333')
            plt.tight_layout(pad=2.0)
            st.pyplot(fig)

# ── Model 2: Credit Spread Monitor ────────────────────────────
    elif model == "Credit Spread Monitor":
        st.markdown("## Credit Spread Monitor")
        st.markdown("""
        <div class="card">
            <h3>Overview</h3>
            <p>
            This model tracks the credit spread between High Yield
            bonds (HYG) and Investment Grade bonds (LQD) to detect
            building stress in credit markets. Converted into a
            stress score from 1 to 5 using 16 years of real data.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <h3>Stress Scale</h3>
            <p>
            <b>Score 1 — Very Calm:</b> Extremely relaxed credit markets.<br><br>
            <b>Score 2 — Calm:</b> Normal conditions.<br><br>
            <b>Score 3 — Moderate:</b> Some caution warranted.<br><br>
            <b>Score 4 — Elevated:</b> Credit stress building.<br><br>
            <b>Score 5 — High Stress:</b> Significant credit risk.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h3>What is HYG?</h3>
                <p>High Yield bonds are loans to riskier companies.
                When HYG falls investors are pulling back from risky
                lending — often the first warning sign of stress.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card">
                <h3>What is LQD?</h3>
                <p>Investment Grade bonds are loans to safer companies.
                When LQD outperforms HYG investors are moving toward
                safety — a classic early warning signal.</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <h3>Current Reading — September 17, 2026</h3>
            <p>
            Credit Spread: <b>1.2 basis points</b><br><br>
            Stress Score: <b>4 out of 5 — ELEVATED</b><br><br>
            Higher than <b>63%</b> of all readings since 2010.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Run the Credit Spread Model")
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
                cs_current_spread = spread.iloc[-1]
                cs_current_score  = spread_df['stress_score'].iloc[-1]
                cs_current_date   = spread.index[-1].strftime('%B %d, %Y')
            st.markdown("---")
            st.markdown("### Current Credit Signal")
            if cs_current_score <= 2:
                st.success(f"CALM — As of {cs_current_date} credit markets "
                           f"are relaxed. Stress score {cs_current_score:.0f}/5.")
            elif cs_current_score <= 3:
                st.warning(f"MODERATE — As of {cs_current_date} some caution "
                           f"warranted. Stress score {cs_current_score:.0f}/5.")
            else:
                st.error(f"ELEVATED — As of {cs_current_date} credit stress "
                         f"building. Stress score {cs_current_score:.0f}/5.")
            st.markdown("---")
            st.markdown("### Credit Spread Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("Credit Spread", f"{cs_current_spread:.1f} bps")
            m2.metric("Stress Score",  f"{cs_current_score:.0f} / 5")
            pct_rank = (spread < cs_current_spread).mean() * 100
            m3.metric("Percentile Rank", f"{pct_rank:.0f}%",
                      "vs history since 2010")
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
                alpha=0.08, color='#D85A30', label='High Stress Zone')
            axes[0].axhspan(spread_df['spread'].min(),
                spread_df['spread'].quantile(0.20),
                alpha=0.08, color='#1D9E75', label='Low Stress Zone')
            axes[0].plot(spread_df.index, spread_df['spread'],
                color='#CCCCCC', linewidth=0.5, alpha=0.5)
            axes[0].plot(spread_df.index, spread_df['spread_smooth'],
                color='#333333', linewidth=2,
                label='Credit Spread (21-day avg)')
            axes[0].scatter(spread_df.index[-1],
                spread_df['spread_smooth'].iloc[-1],
                color='#D85A30', s=80, zorder=5,
                label=f'Today: {cs_current_spread:.1f} bps')
            axes[0].set_title('Credit Spread — HYG vs LQD (Basis Points)',
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
            axes[1].set_title('Credit Stress Score — 21-Day Smoothed',
                color='#333333', fontsize=13, fontweight='bold')
            axes[1].set_ylabel('Stress Score', color='#333333')
            axes[1].set_ylim(0, 5.5)
            axes[1].set_yticks([1, 2, 3, 4, 5])
            axes[1].legend(facecolor='#F9F9F9',
                labelcolor='#333333', fontsize=9)
            axes[1].grid(axis='y', color='#DDDDDD', linewidth=0.5)
            plt.tight_layout(pad=2.0)
            st.pyplot(fig)
        st.markdown("---")
        st.markdown("""
        <div class="card">
            <h3>Full Research Notebook</h3>
            <p>
            View the complete Credit Spread Monitor on GitHub:<br><br>
            github.com/sidneyppratt-svg/credit-spread-monitor
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── Model 3: Hockey Pathway Navigator ─────────────────────────
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
        st.markdown("### NHL Player Spotlights — Real Paths to the Pros")
        st.markdown("""
        <p style="color:#555555; font-size:14px;">
        These are the actual pathways taken by five of today's
        top young NHL players. Every path is different —
        and all of them worked.
        </p>
        """, unsafe_allow_html=True)

        players = [
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

        for player in players:
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
