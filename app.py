import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import datetime

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
    Using machine learning to find
