import streamlit as st

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Sidney Pratt | Quant Research",
    page_icon="📈",
    layout="wide"
)

# ── Custom styling ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0C2340; }
    .block-container { padding-top: 2rem; }
    h1 { color: #9FE1CB; }
    h2 { color: #9FE1CB; }
    h3 { color: white; }
    p  { color: white; }
    .stButton>button {
        background-color: #0F6E56;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-size: 16px;
    }
    .metric-card {
        background-color: #142B4A;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 0.5px solid #1D9E75;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Sidney Pratt")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Home",
        "👤 About",
        "📄 Resume",
        "🤖 AI Research",
        "📬 Contact"
    ])

# ══════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════
if page == "🏠 Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/300x300.png?text=Sidney+Pratt",
                  width=250)
    with col2:
        st.markdown("# Sidney Pratt")
        st.markdown("### Finance & Economics Student | ACHA D1 Hockey Player | AI Quant Researcher | World Explorer")
        st.markdown("---")
        st.markdown("""
        📍 San Francisco, CA  
        🎓 Western Michigan University — Finance & Economics  
        📧 sidneypratt@gmail.com  
        🔗 [LinkedIn](https://linkedin.com/in/sidney-pratt) | [GitHub](https://github.com/sidneyppratt-svg)
        """)
        st.markdown("---")
        st.markdown("""
        > *Finance and Economics student combining quantitative research, 
        AI tools, and real-world market experience to build the next 
        generation of trading strategies.*
        """)

# ══════════════════════════════════════════════════════════════
# ABOUT PAGE
# ══════════════════════════════════════════════════════════════
elif page == "👤 About":
    st.markdown("# About Me")
    st.markdown("---")
    st.markdown("""
    Sidney Pratt is a Finance and Economics double major at Western Michigan 
    University with a passion for financial markets, quantitative research, 
    and innovation. Born and raised in San Francisco, Sidney brings a rare 
    combination of academic rigor, athletic discipline, and global perspective 
    to everything he does.

    As an ACHA D1 hockey player at Western Michigan University, Sidney 
    understands what it takes to perform under pressure, work within a team, 
    and push through challenges that most people walk away from. Those same 
    qualities show up in his academic and professional work.

    Sidney has already gained real world experience as an intern at the 
    American Institute for Economic Research where he contributed to economic 
    research, policy analysis, and data collection. He has also built a live 
    AI tool that detects market regimes across four asset classes — stocks, 
    bonds, credit, and gold — using 12 years of real market data.

    Beyond finance Sidney has summited Mount Kilimanjaro in Tanzania, worked 
    with conservation rangers protecting the Amazon rainforest in Peru, and 
    volunteered at orphanages in Africa. These experiences shaped a globally 
    minded, adaptable, and deeply curious professional who sees the world as 
    a place of opportunity.

    Sidney is currently seeking internship opportunities in cross-asset 
    trading, quantitative research, and portfolio management where he can 
    contribute immediately and continue growing.
    """)

    st.markdown("---")
    st.markdown("### Key Highlights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>🎓 Education</h3>
            <p>Finance & Economics<br>Western Michigan University<br>GPA: 3.25</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3>💼 Experience</h3>
            <p>AIER Intern<br>Economic Research<br>Policy Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3>🌍 Global</h3>
            <p>Mt. Kilimanjaro<br>Amazon Rainforest<br>Tanzania Volunteer</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RESUME PAGE
# ══════════════════════════════════════════════════════════════
elif page == "📄 Resume":
    st.markdown("# Resume")
    st.markdown("---")

    st.markdown("### 🎓 Education")
    st.markdown("""
    **Western Michigan University** | Kalamazoo, MI  
    Double Major in Finance and Economics  
    Expected Graduation: May 2029 | GPA: 3.25
    """)

    st.markdown("---")
    st.markdown("### 💼 Experience")
    st.markdown("""
    **Intern | American Institute of Economic Research (AIER)**  
    *February 2026 – April 2026 | Great Barrington, MA*  
    Contributed to economic research and policy analysis through data 
    collection, literature review, and analytical support. Synthesized 
    findings and prepared written materials supporting evidence-based 
    policy discussions.

    **Sales Associate | Next Gen Exposure**  
    *August 2026 – October 2026 | Kalamazoo, MI*  
    Trained in direct-to-consumer sales representing AT&T within a 
    high-traffic Costco environment.

    **Assistant Coach | San Francisco Sabercats Hockey Club**  
    *May 2025 – July 2025 | San Francisco, CA*  
    Supported player development, game strategy, and team coordination.
    """)

    st.markdown("---")
    st.markdown("### 🛠️ Skills")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Technical Skills**
        - Python
        - SQL
        - Microsoft Office Suite
        - Financial Analysis
        - AI Tools & Machine Learning
        - Market Forecasting
        """)
    with col2:
        st.markdown("""
        **Certifications**
        - MIT Professional Education: Forecasting Future Technologies
        - NPR: Economic History Summer School
        - Coursera: Python & SQL
        """)

    st.markdown("---")
    st.markdown("### 🏒 Activities")
    st.markdown("""
    - **ACHA D1 Hockey Team** | Western Michigan University | Sep 2024 – Present
    - **Pi Kappa Alpha Fraternity** | Western Michigan University | Apr 2024 – Present
    - **Northern Cyclones USHL Junior Hockey Financial Club** | Co-Founder | Nov 2023 – Jul 2024
    - **SPuRS** | Advanced Leadership & Services Pillar | Sep 2024 – Oct 2024
    """)

    st.markdown("---")
    st.markdown("### 🌍 Volunteer & International Service")
    st.markdown("""
    - **SF-Marin Food Bank** — Organized food donations and community distribution
    - **Junglekeepers – Tamandua Expeditions** — Amazon rainforest conservation patrols
    - **Kilimanjaro Challenge** — Volunteered at orphanage and summited Mt. Kilimanjaro
    """)

# ══════════════════════════════════════════════════════════════
# AI RESEARCH PAGE
# ══════════════════════════════════════════════════════════════
elif page == "🤖 AI Research":
    st.markdown("# AI Research")
    st.markdown("### Using machine learning to find signals in financial markets")
    st.markdown("---")

    model = st.selectbox("Select a model:", [
        "🌐 Multi-Asset Market Regime Detector",
        "➕ More models coming soon..."
    ])

    if model == "🌐 Multi-Asset Market Regime Detector":
        st.markdown("## Multi-Asset Market Regime Detector")
        st.markdown("""
        This model uses unsupervised machine learning to detect whether 
        markets are in a **RISK-ON** or **RISK-OFF** regime by analyzing 
        four asset classes simultaneously.
        """)

        st.markdown("---")
        st.markdown("### Select Date Range")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date",
                value=__import__('datetime').date(2014, 1, 1))
        with col2:
            end_date = st.date_input("End Date",
                value=__import__('datetime').date(2026, 9, 18))

        if st.button("🚀 Run AI Model"):
            with st.spinner("Downloading market data and running AI model..."):
                import yfinance as yf
                import pandas as pd
                import numpy as np
                from sklearn.mixture import GaussianMixture
                import matplotlib.pyplot as plt

                # Download data
                tickers = ['SPY', 'AGG', 'HYG', 'GLD']
                prices = yf.download(tickers,
                    start=str(start_date),
                    end=str(end_date),
                    auto_adjust=True)['Close']
                prices = prices.dropna()
                returns = prices.pct_change().dropna()
                smooth = returns.rolling(21).mean().dropna()

                # Train model
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

                # Backtest
                spy_returns = returns['SPY'].loc[smooth.index]
                signal = (smooth['label'] == 'RISK-ON').astype(int)
                strat  = signal.shift(1) * spy_returns
                strat  = strat.dropna()
                bh     = spy_returns.loc[strat.index]

                def metrics(r):
                    cum     = (1 + r).cumprod()
                    total   = cum.iloc[-1] - 1
                    ann_ret = (1 + total) ** (252/len(r)) - 1
                    ann_vol = r.std() * np.sqrt(252)
                    sharpe  = ann_ret / ann_vol
                    max_dd  = (cum / cum.cummax() - 1).min()
                    return cum, total, ann_ret, ann_vol, sharpe, max_dd

                cum_s, tot_s, ret_s, vol_s, sh_s, dd_s = metrics(strat)
                cum_b, tot_b, ret_b, vol_b, sh_b, dd_b = metrics(bh)

                # Current signal
                latest = smooth['label'].iloc[-1]
                latest_date = smooth.index[-1].strftime('%B %d, %Y')

                # Display current signal
                st.markdown("---")
                st.markdown("### 🤖 Current Market Signal")
                if latest == 'RISK-ON':
                    st.success(f"✅ RISK-ON — As of {latest_date} markets are calm. Model suggests staying INVESTED.")
                else:
                    st.error(f"⚠️ RISK-OFF — As of {latest_date} market stress detected. Model suggests moving to CASH.")

                # Metrics
                st.markdown("---")
                st.markdown("### 📊 Performance Results")
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Total Return", f"{tot_s:.1%}", f"{tot_s-tot_b:.1%} vs BH")
                col2.metric("Ann. Return",  f"{ret_s:.1%}", f"{ret_s-ret_b:.1%} vs BH")
                col3.metric("Volatility",   f"{vol_s:.1%}", f"{vol_s-vol_b:.1%} vs BH")
                col4.metric("Sharpe Ratio", f"{sh_s:.2f}",  f"{sh_s-sh_b:.2f} vs BH")
                col5.metric("Max Drawdown", f"{dd_s:.1%}",  f"{dd_s-dd_b:.1%} vs BH")

                # Charts
                st.markdown("---")
                st.markdown("### 📈 Charts")

                fig, axes = plt.subplots(2, 1, figsize=(12, 10))
                fig.patch.set_facecolor('#0C2340')

                for ax in axes:
                    ax.set_facecolor('#142B4A')
                    ax.tick_params(colors='white')
                    for spine in ax.spines.values():
                        spine.set_edgecolor('#444441')

                # Equity curve
                (cum_s * 100).plot(ax=axes[0], color='#9FE1CB',
                    linewidth=2, label='AI Strategy')
                (cum_b * 100).plot(ax=axes[0], color='#888780',
                    linewidth=1.5, linestyle='--', label='Buy & Hold')
                axes[0].set_title('Portfolio Growth ($100 invested)',
                    color='white', fontsize=13, fontweight='bold')
                axes[0].legend(facecolor='#142B4A', labelcolor='white')
                axes[0].yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda x, _: f'${x:.0f}'))
                axes[0].set_ylabel('Value ($)', color='white')

                # Regime timeline
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
        st.info("🚧 More AI models coming soon — check back regularly!")

# ══════════════════════════════════════════════════════════════
# CONTACT PAGE
# ══════════════════════════════════════════════════════════════
elif page == "📬 Contact":
    st.markdown("# Contact")
    st.markdown("---")
    st.markdown("""
    ### Get in touch

    📧 **Email:** sidneypratt@gmail.com  
    🔗 **LinkedIn:** [linkedin.com/in/sidney-pratt](https://linkedin.com/in/sidney-pratt)  
    💻 **GitHub:** [github.com/sidneyppratt-svg](https://github.com/sidneyppratt-svg)  
    🌐 **Website:** sidneyppratt.com  
    📍 **Location:** San Francisco, CA
    """)
    st.markdown("---")
    st.markdown("""
    > Currently seeking internship opportunities in:
    > - Cross-Asset Trading
    > - Quantitative Research  
    > - Portfolio Management
    """)
