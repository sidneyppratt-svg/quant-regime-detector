# Multi-Asset Market Regime Detector
### Cross-Asset Quantitative Research Tool | Sidney Pratt

---

## Overview
This model uses unsupervised machine learning to detect whether markets
are in a RISK-ON or RISK-OFF regime by analyzing four asset classes
simultaneously — US Equities (SPY), Investment Grade Bonds (AGG),
High Yield Credit (HYG), and Gold (GLD).

Rather than looking at one asset in isolation, the model finds hidden
patterns across all four asset classes at once — the same way
professional portfolio managers and cross-asset traders think about
markets. Built on 12 years of real daily price data from 2014 to 2026.

---

## Key Features
- Live multi-asset price data downloaded fresh on every run
- Gaussian Mixture Model — unsupervised machine learning
- Simultaneous analysis of four asset classes
- RISK-ON and RISK-OFF regime classification
- 21-day rolling return smoothing to filter daily noise
- Full backtest of a SPY strategy using regime signals
- Regime detection timeline with key event annotations

---

## Why It Matters
Markets do not move in isolation. When stress hits it shows up across
multiple asset classes at the same time — stocks fall, credit widens,
and gold spikes simultaneously. A model that watches only one asset
misses the full picture.

This model detects those cross-asset stress patterns using machine
learning — no rules, no assumptions. The algorithm finds the patterns
itself from 12 years of real data.

- **Cross-asset traders** watch all four of these simultaneously
- **Portfolio managers** use regime signals to adjust allocations
- **Risk managers** use RISK-OFF signals to reduce exposure before
  drawdowns deepen

---

## Methodology
The model downloads daily price data for SPY, AGG, HYG, and GLD.
It calculates 21-day rolling mean returns for each asset — smoothing
out daily noise so the model sees trends rather than randomness.

A Gaussian Mixture Model (GMM) — an unsupervised machine learning
algorithm — is then fit to the four-dimensional return data. The GMM
finds two hidden clusters in the data without being told what to look
for. The cluster with higher average SPY returns is labeled RISK-ON.
The cluster with lower average SPY returns is labeled RISK-OFF.

The backtest goes long SPY during RISK-ON and moves to cash during
RISK-OFF using the prior day signal to avoid lookahead bias.

**This methodology does not change regardless of the date range selected.**

---

## Asset Classes Covered

| Asset | Ticker | What It Represents |
|-------|--------|--------------------|
| US Equities | SPY | S&P 500 — broad US stock market |
| Investment Grade Bonds | AGG | High quality corporate and government bonds |
| High Yield Credit | HYG | Riskier corporate bonds — junk bonds |
| Gold | GLD | Safe haven asset — spikes during stress |

---

## Dynamic Results
*The following update every time the model is run based on selected dates.*

**Signal** — Current regime classification: RISK-ON or RISK-OFF based
on the latest 21-day rolling returns across all four asset classes.

**Strategy Signal** — Stay INVESTED in SPY or MOVE TO CASH based on
current regime.

**Results** — Total return, annualized return, volatility, Sharpe ratio,
and max drawdown for both the AI strategy and buy and hold SPY.

**Summary & Key Findings** — Plain language explanation of what the
current regime means and what the four asset classes are signaling.

**What to Watch** — Specific indicators to monitor given the current
regime across equities, credit, and gold.

**Historical Context** — Key RISK-OFF periods identified by the model
including COVID March 2020 and Fed rate hikes 2022.

**Charts** — Two charts: portfolio growth comparing AI strategy vs
buy and hold, and regime detection timeline showing SPY price
overlaid with RISK-ON and RISK-OFF periods.

---

## Tools & Technologies
- **Python** — core programming language
- **yfinance** — live multi-asset price data
- **scikit-learn** — Gaussian Mixture Model
- **pandas & numpy** — data processing and calculations
- **matplotlib** — chart generation
- **Streamlit** — live interactive web application
- **Google Colab** — development environment

---

## Full Research Notebook
View the complete Multi-Asset Market Regime Detector including all
code, charts, backtest results, and analysis:

github.com/sidneyppratt-svg/quant-regime-detector

---

## About
Sidney Pratt is a Finance and Economics student at Western Michigan
University and an ACHA D1 hockey player building a quantitative
research portfolio targeted at fixed income trading internships.

sidneyppratt.com | github.com/sidneyppratt-svg
