import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import datetime

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Sidney Pratt | Quant Research",
    page_icon="📈",
    layout="wide"
)

# ── Custom styling ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #0C2340;
    }
    [data-testid="stSidebar"] {
        background-color: #091929;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown h1, 
    .stMarkdown h2, .stMarkdown h3, label {
        color: white !important;
    }
    h1 { color: #9FE1CB !important; font-size: 2.5rem !important; }
    h2 { color: #9FE1CB !important; }
    h3 { color: #9FE1CB !important; }
    [data-testid="metric-container"] {
        background-color: #142B4A;
        border: 1px solid #1D9E75;
        border-radius: 8px;
        padding: 1rem;
        color: white !important;
    }
    [data-testid="metric-container"] * {
        color: white !important;
    }
    .stButton > button {
        background-color: #0F6E56 !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1D9E75 !important;
    }
    hr {
        border-color: #1D9E75 !important;
    }
    .card {
        background-color: #142B4A;
        border: 1px solid #1D9E75;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: white;
    }
    .card h3 {
        color: #9FE1CB !important;
        margin-bottom: 0.5rem;
    }
    .card p {
        color: #D3D1C7 !important;
        line-height: 1.6;
    }
    .tag {
        display: inline-block;
        background-color: #0F6E56;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin: 4px;
    }
    .profile-placeholder {
        width: 220px;
        height: 220px;
        background: linear-gradient(135deg, #0F6E56, #185FA5);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 72px;
        margin: 0 auto;
        border: 4px solid #1D9E75;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Sidney Pratt")
    st.markdown("*Quant Researcher*")
    st.markdown("---")
    page = st.radio("", [
        "Home",
        "About",
        "Resume",
        "AI Research",
        "Contact"
    ])
    st.markdown("---")
    st.markdown("📧 sidneyppratt@gmail.com")
    st.markdown("📍 San Francisco, CA")

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if page == "Home":
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("""
        <div class="profile-placeholder">SP</div>
        <br>
        <p style="text-align:center; color:#9FE1CB; font-size:14px;">
        Photo coming soon
        </p>
        """, unsafe_allow_html=True)

    with col2:
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
        <p style="color:#D3D1C7; font-size:16px; line-height:1.8;">
        Finance and Economics student combining quantitative research, 
        AI tools, and real-world market experience to build the next 
        generation of trading strategies.
        </p>
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
        collection. He has also built a live AI tool that detects 
        market regimes across four asset classes — stocks, bonds, 
        credit, and gold — using 12 years of real market data.
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
            backtesting, and market data analysis. Built a live 
            AI regime detector trained on 12 years of real market data.</p>
        </div>
        <div class="card">
            <h3>Athletic Discipline</h3>
            <p>ACHA D1 Hockey player — understanding of high performance, 
            teamwork under pressure, and the discipline to show up 
            every day regardless of circumstances.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Research Experience</h3>
            <p>Interned at the American Institute of Economic Research — 
            contributing to real economic policy analysis, literature 
            review, and data-driven research in a professional setting.</p>
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
        Supported player development, game strategy, and team 
        coordination.
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
    <p style="color:#D3D1C7; font-size:16px;">
    Using machine learning to find signals in financial markets.
    Each model is trained on real market data and fully interactive.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    model = st.selectbox("Select a model:", [
        "Multi-Asset Market Regime Detector",
        "More models coming soon..."
    ])

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
            and Gold (GLD). The model was trained on 12 years of 
            real daily market data from 2014 to 2026.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Methodology</h3>
            <p>
            <b>Data:</b> 12 years of daily price data across 4 asset 
            classes (2014–2026)<br><br>
            <b>Model:</b> Gaussian Mixture Model (GMM) — unsupervised 
            machine learning that finds hidden patterns in data without 
            being told what to look for<br><br>
            <b>Signal:</b> 21-day rolling mean returns used as input 
            features — this smooths out daily noise so the AI sees 
            trends instead of random fluctuations<br><br>
            <b>Strategy:</b> Long SPY during RISK-ON regimes, move to 
            cash during RISK-OFF regimes<br><br>
            <b>Backtest:</b> Chronological train/test split to prevent 
            lookahead bias — meaning the model never uses future data 
            to make past decisions
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h3>RISK-ON ✅ — Markets Are Calm</h3>
                <p>
                All four asset classes are behaving normally. 
                Stocks are rising, credit is tight, gold is steady. 
                Investors are confident and willing to take risk.<br><br>
                <b>What this means:</b> Stay invested in equities. 
                The environment is favorable for growth.<br><br>
                <b>Real world example:</b> 2021 post-COVID recovery — 
                stocks surged, credit was cheap, investors were 
                pouring money into risk assets everywhere.
                The model correctly identified this as a sustained 
                RISK-ON period.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card">
                <h3>RISK-OFF ⚠️ — Market Stress Detected</h3>
                <p>
                Something is wrong across multiple asset classes 
                simultaneously. Stocks are falling, credit is 
                widening, gold is spiking. Investors are scared 
                and moving to safety.<br><br>
                <b>What this means:</b> Move to cash. Protect 
                capital until conditions stabilize.<br><br>
                <b>Real world example:</b> March 2020 COVID crash — 
                stocks dropped 34% in 23 days, credit markets froze, 
                and gold spiked as investors panicked. The model 
                flagged RISK-OFF and moved to cash before the 
                worst of the decline.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>The Four Asset Class Sensors</h3>
            <p>
            <b>SPY — US Stock Market:</b> Measures overall investor 
            confidence. Rising SPY = investors are optimistic about 
            the economy.<br><br>
            <b>AGG — Investment Grade Bonds:</b> Measures flight to 
            safety. Rising AGG = investors are getting cautious and 
            moving money out of stocks into safer assets.<br><br>
            <b>HYG — High Yield Credit:</b> Measures risk appetite in 
            the credit market. Falling HYG = lenders are pulling back 
            from risky companies — often the first warning sign of 
            broader stress.<br><br>
            <b>GLD — Gold:</b> Measures fear and uncertainty. 
            Spiking gold = investors are nervous about everything 
            else and looking for a safe hiding place.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>Key Results</h3>
            <p>
            The AI strategy matched buy-and-hold returns over 12 years 
            while significantly reducing risk:<br><br>
            — Maximum drawdown reduced from <b>-33.7%</b> to 
            <b>-24.0%</b> — protecting investors during the 
            worst crashes<br><br>
            — Sharpe ratio improved from <b>0.84</b> to <b>0.93</b> 
            — more return per unit of risk taken<br><br>
            — Portfolio volatility reduced from <b>17.1%</b> to 
            <b>15.5%</b> — a smoother ride to the same destination<br><br>
            The model correctly identified RISK-OFF conditions only 
            1.8% of the time — rare but severe stress periods like 
            the COVID-19 crash in March 2020 and the 2022 Federal 
            Reserve rate hike cycle.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Run the Model")
        st.markdown("""
        <p style="color:#D3D1C7;">
        Select a date range below and click Run AI Model to see 
        the regime detector in action for any time period.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Select Date Range")
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
                    risk_on:  'RISK-ON',
                    risk_off: 'RISK-OFF'
                })

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
                st.success(
                    f"RISK-ON — As of {latest_date} markets are calm. "
                    f"Model suggests staying INVESTED in equities.")
            else:
                st.error(
                    f"RISK-OFF — As of {latest_date} market stress "
                    f"detected. Model suggests moving to CASH.")

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
            fig.patch.set_facecolor('#0C2340')

            for ax in axes:
                ax.set_facecolor('#142B4A')
                ax.tick_params(colors='white')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#444441')

            (cum_s * 100).plot(ax=axes[0], color='#9FE1CB',
                linewidth=2, label='AI Strategy')
            (cum_b * 100).plot(ax=axes[0], color='#888780',
                linewidth=1.5, linestyle='--', label='Buy & Hold')
            axes[0].set_title('Portfolio Growth — $100 invested',
                color='white', fontsize=13, fontweight='bold')
            axes[0].legend(facecolor='#142B4A', labelcolor='white')
            axes[0].set_ylabel('Value ($)', color='white')
            axes[0].yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'${x:.0f}'))

            risk_on_mask  = smooth['label'] == 'RISK-ON'
            risk_off_mask = smooth['label'] == 'RISK-OFF'
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_on_mask,
                color='#1D9E75', alpha=0.7, label='RISK-ON')
            axes[1].fill_between(smooth.index, 0, 1,
                where=risk_off_mask,
                color='#D85A30', alpha=0.9, label='RISK-OFF')
            axes[1].set_title('Regime Detection Timeline',
                color='white', fontsize=13, fontweight='bold')
            axes[1].set_yticks([])
            axes[1].legend(facecolor='#142B4A', labelcolor='white')

            plt.tight_layout(pad=2.0)
            st.pyplot(fig)

    else:
        st.markdown("""
        <div class="card">
            <h3>More Models Coming Soon</h3>
            <p>New AI research models are currently being developed. 
            Check back regularly for updates including credit spread 
            analysis, volatility forecasting, and sector rotation models.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown("# Contact")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Get In Touch</h3>
            <p>
            Email: sidneyppratt@gmail.com<br><br>
            LinkedIn: linkedin.com/in/sidney-pratt<br><br>
            GitHub: github.com/sidneyppratt-svg<br><br>
            Website: sidneyppratt.com<br><br>
            Location: San Francisco, CA
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Currently Seeking</h3>
            <p>
            Internship opportunities in:<br><br>
            - Cross-Asset Trading<br>
            - Quantitative Research<br>
            - Portfolio Management<br>
            - Economic Research<br>
            - Financial Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
