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
            AI regime detector trained on 12 years of real market
            data.</p>
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
            literature review, and data-driven research in a
            professional setting.</p>
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
