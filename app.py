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
