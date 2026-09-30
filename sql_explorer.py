# ══════════════════════════════════════════════════════════════
# sql_explorer.py
# The "SQL Market Data" page of sidneyppratt.com.
#
# Every table on this page comes from a SQL query (saved in the
# sql/queries folder) run against a SQLite database of daily
# prices (sql/trading.db).
#
# app.py shows this page by calling render() when "SQL Market
# Data" is picked in the top menu. The sidebar, the top menu, and
# all the styling (cards, buttons, colors) come from app.py, so
# this page automatically matches the rest of the site.
#
# This file never touches the AI Finance models. It uses its own
# button keys and its own memory setting ("sql_view").
# ══════════════════════════════════════════════════════════════

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# ── File locations ────────────────────────────────────────────
# Path(__file__).parent is the folder this file lives in (the
# website's main folder), so these paths work on your laptop, in
# Codespaces, and on Render.
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "sql" / "trading.db"
QUERY_DIR = BASE_DIR / "sql" / "queries"

# Same signal colors the AI Finance models use.
GREEN = "#2E7D32"
AMBER = "#E65100"
RED = "#C62828"
DARK = "#1a1a1a"

# Plain-English names for each ticker, shown next to the symbol
# in every table so visitors know what each asset is.
ASSET_NAMES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet (Google)",
    "JPM": "JPMorgan Chase",
    "XOM": "Exxon Mobil",
    "SPY": "S&P 500 ETF",
    "QQQ": "Nasdaq 100 ETF",
    "TLT": "20+ Year Treasury Bond ETF",
    "LQD": "Investment-Grade Corporate Bond ETF",
    "HYG": "High-Yield Corporate Bond ETF",
    "MBB": "Mortgage-Backed Securities ETF",
    "GLD": "Gold ETF",
}
BOND_FUNDS = ["TLT", "LQD", "MBB", "HYG"]

# The page's section buttons, in the order they appear.
SECTIONS = [
    "Performance vs. S&P 500",
    "Trend Status",
    "Biggest Moves",
    "Volume Spikes",
    "Crossover Signals",
]


# ══════════════════════════════════════════════════════════════
# DATABASE HELPERS
# ══════════════════════════════════════════════════════════════

# Read the SQL text from a .sql file. Not cached, so edits to a
# query file are picked up right away.
def load_sql(filename):
    return (QUERY_DIR / filename).read_text()


# Run SQL against the database and return the results as a table.
# Results are remembered for one hour (ttl=3600) so the page is
# fast. The memory is keyed on the SQL text, so a changed query
# always runs fresh. This is the ONE place that connects to the
# database, so a future switch to PostgreSQL only changes this.
@st.cache_data(ttl=3600, show_spinner=False)
def run_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# ══════════════════════════════════════════════════════════════
# FORMATTING HELPERS
# ══════════════════════════════════════════════════════════════

# "2026-09-28" -> "Sep 28, 2026"
def nice_date(text):
    d = pd.to_datetime(text)
    return f"{d:%b} {d.day}, {d.year}"


# 48.3 -> "+48.3%"   -8.0 -> "-8.0%"
def pct(x, places=1):
    return f"{x:+.{places}f}%"


# Green for gains, red for losses.
def gain_color(x):
    return GREEN if x >= 0 else RED


# Add an "Asset" column with the plain-English name, right after
# the ticker column.
def add_asset_names(df):
    df = df.copy()
    df.insert(1, "asset", df["ticker"].map(ASSET_NAMES).fillna(""))
    return df


# Height that shows every row with no scrolling:
# (rows + 1 header row) x 35 pixels, plus 3 for the border.
def table_height(df):
    return (len(df) + 1) * 35 + 3


# Turn a list of tickers into readable text: "A, B, and C"
def list_words(items):
    items = list(items)
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


# ══════════════════════════════════════════════════════════════
# LAYOUT HELPERS (use the site's existing card styles)
# ══════════════════════════════════════════════════════════════

# The green "Latest results" card, same design as the AI Finance
# models. rows = list of (label, value, color).
def results_card(as_of, rows):
    row_html = "".join(
        f'<div class="rc-row"><span class="rc-label">{label}</span>'
        f'<span class="rc-value" style="color:{color};">{value}</span></div>'
        for label, value, color in rows)
    st.markdown(
        f'<div class="results-card">'
        f'<div class="rc-head"><b>Latest results</b>'
        f'<span class="rc-date">As of {as_of}</span></div>'
        f'{row_html}'
        f'<div class="rc-foot">Full table, explanation &amp; SQL below ↓</div>'
        f'</div>',
        unsafe_allow_html=True)


# Section title + italic subtitle on the left, results card on
# the right, then a divider. Same layout as the models.
def section_header(title, subtitle, as_of, card_rows):
    title_col, card_col = st.columns([3, 2])
    with title_col:
        st.markdown(f"## {title}")
        st.markdown(f"*{subtitle} | Sidney Pratt*")
    with card_col:
        results_card(as_of, card_rows)
    st.markdown("---")


# A light blue card for fixed explanations (Overview, How to
# Read This Table, SQL Techniques Used).
def static_card(heading, body_html):
    st.markdown(
        f'<div class="static-section"><h3>{heading}</h3>'
        f'<p>{body_html}</p></div>',
        unsafe_allow_html=True)


# A gray card for text that is written from the latest data and
# changes as the data updates ("What the Data Shows").
def dynamic_card(heading, body_html):
    st.markdown(
        f'<div class="dynamic-section"><h3>{heading}</h3>'
        f'<p>{body_html}</p></div>',
        unsafe_allow_html=True)


# The table itself. `labels` gives friendly column headers, and
# `formats` sets how numbers look ("dollar", "%.1f%%", etc.).
# The SQL keeps its original column names; only the display
# changes.
def show_table(df, labels, formats=None):
    formats = formats or {}
    config = {}
    for col, label in labels.items():
        if col in formats:
            config[col] = st.column_config.NumberColumn(
                label, format=formats[col])
        else:
            config[col] = st.column_config.Column(label)
    st.dataframe(df, hide_index=True, column_config=config,
                 height=table_height(df), width="stretch")


# The collapsible "Show the SQL" box under each table.
def show_sql(sql):
    with st.expander("Show the SQL"):
        st.code(sql, language="sql")


# ══════════════════════════════════════════════════════════════
# SECTION 1 — PERFORMANCE VS. S&P 500
# ══════════════════════════════════════════════════════════════
def section_performance(as_of):
    sql = load_sql("06_vs_spy.sql")
    df = add_asset_names(run_sql(sql))

    # Key numbers for the results card and the summary.
    top = df.iloc[0]
    bottom = df.iloc[-1]
    spy_return = df.loc[df["ticker"] == "SPY", "return_1y"].iloc[0]
    others = df[df["ticker"] != "SPY"]
    beat = int((others["vs_spy"] > 0).sum())

    section_header(
        "1-Year Performance vs. S&P 500",
        "Relative Performance Analysis", as_of,
        [("Top performer", f"{top['ticker']} {pct(top['return_1y'])}",
          gain_color(top["return_1y"])),
         ("Weakest", f"{bottom['ticker']} {pct(bottom['return_1y'])}",
          gain_color(bottom["return_1y"])),
         ("S&P 500 (SPY) return", pct(spy_return), gain_color(spy_return)),
         ("Beat the S&P 500", f"{beat} of {len(others)} assets", DARK)])

    static_card("Overview",
        "This table ranks every asset by its total return over the past "
        "year and compares it with the S&amp;P 500, using SPY as the "
        "benchmark. A return on its own says little: a stock that gained "
        "15% in a year when the market gained 25% actually lagged. "
        "Measuring against a benchmark is standard practice on every "
        "trading desk, and the gap between an asset's return and the "
        "benchmark's is the starting point for measuring "
        "<b>alpha</b>.")

    # Plain-language summary written from the current results.
    text = (
        f"<b>{ASSET_NAMES.get(top['ticker'], top['ticker'])} "
        f"({top['ticker']})</b> led with a one-year return of "
        f"<b>{pct(top['return_1y'])}</b>, beating the S&amp;P 500 by "
        f"{top['vs_spy']:.1f} percentage points. "
        f"<b>{ASSET_NAMES.get(bottom['ticker'], bottom['ticker'])} "
        f"({bottom['ticker']})</b> was the weakest at "
        f"<b>{pct(bottom['return_1y'])}</b>. "
        f"The S&amp;P 500 returned {pct(spy_return)}, and {beat} of the "
        f"other {len(others)} assets beat it.")
    bonds = df[df["ticker"].isin(BOND_FUNDS)]
    if len(bonds) >= 2:
        best_b, worst_b = bonds.iloc[0], bonds.iloc[-1]
        text += (
            f"<br><br>Among the bond funds, {best_b['ticker']} did best "
            f"({pct(best_b['return_1y'])}) and {worst_b['ticker']} did "
            f"worst ({pct(worst_b['return_1y'])}). Bond funds holding "
            f"longer-maturity bonds, like TLT, are the most sensitive to "
            f"changes in interest rates, a measure called "
            f"<b>duration</b>. When rates rise, long-duration bonds fall "
            f"the most.")
    dynamic_card("What the Data Shows", text)

    static_card("How to Read This Table",
        "<b>Ticker / Asset</b> — the trading symbol and what it is.<br>"
        "<b>Start Price</b> — the closing price on the first trading day "
        "in the one-year window.<br>"
        "<b>End Price</b> — the closing price on the latest trading day "
        "in the database.<br>"
        "<b>1-Year Return</b> — the percentage change from start price "
        "to end price. Prices are adjusted for stock splits, dividends, "
        "and bond interest payments, so this is the total return.<br>"
        "<b>vs. S&amp;P 500</b> — the asset's return minus SPY's return, "
        "in percentage points. Positive means it beat the market; "
        "negative means it lagged.")

    show_table(df,
        {"ticker": "Ticker", "asset": "Asset",
         "start_price": "Start Price", "end_price": "End Price",
         "return_1y": "1-Year Return", "vs_spy": "vs. S&P 500"},
        {"start_price": "dollar", "end_price": "dollar",
         "return_1y": "%.1f%%", "vs_spy": "%.1f%%"})

    static_card("SQL Techniques Used",
        "<b>CTEs (WITH ... AS)</b> — break the query into readable stages: "
        "find the date range, calculate returns, then compare.<br>"
        "<b>Subquery</b> — finds the latest date in the database so the "
        "one-year window always matches the data.<br>"
        "<b>Self-join</b> — joins the prices table to itself twice to put "
        "each asset's start and end prices side by side.<br>"
        "<b>CROSS JOIN</b> — attaches SPY's return to every row so it can "
        "be subtracted.")

    show_sql(sql)


# ══════════════════════════════════════════════════════════════
# SECTION 2 — TREND STATUS
# ══════════════════════════════════════════════════════════════
def section_trend(as_of):
    sql = load_sql("07_trend_status.sql")
    df = add_asset_names(run_sql(sql))

    n = len(df)
    up = df[df["trend"] == "Uptrend"]
    down = df[df["trend"] == "Downtrend"]
    top = df.iloc[0]
    bottom = df.iloc[-1]

    # The most recent crossover of any asset.
    crossed = df.dropna(subset=["last_cross_date"])
    recent = (crossed.sort_values("last_cross_date").iloc[-1]
              if len(crossed) else None)

    card = [("In an uptrend", f"{len(up)} of {n}", GREEN),
            ("In a downtrend", f"{len(down)} of {n}", RED)]
    if recent is not None:
        kind = "Golden cross" if recent["trend"] == "Uptrend" else "Death cross"
        card.append(("Latest crossover",
                     f"{recent['ticker']} {kind.lower()}, "
                     f"{nice_date(recent['last_cross_date'])}",
                     GREEN if kind == "Golden cross" else RED))
    section_header("Current Trend Status", "Moving Average Trend Analysis",
                   as_of, card)

    static_card("Overview",
        "A <b>moving average</b> smooths out daily price noise by "
        "averaging recent closing prices. The <b>50-day</b> average "
        "reflects the recent trend (about 2.5 months) and the "
        "<b>200-day</b> average reflects the long-term trend (about 10 "
        "months). When the 50-day is above the 200-day, the asset is "
        "considered to be in an uptrend; when it's below, a downtrend. "
        "Traders use this as a quick read on each market's direction.")

    text = (
        f"<b>{len(up)} of {n}</b> assets are in an uptrend and "
        f"<b>{len(down)}</b> are in a downtrend. ")
    if len(up):
        text += f"Uptrend: {list_words(up['ticker'])}. "
    if len(down):
        text += f"Downtrend: {list_words(down['ticker'])}. "
    text += (
        f"<br><br><b>{top['ticker']}</b> is the most stretched above its "
        f"long-term trend, trading {pct(top['pct_vs_ma200'])} from its "
        f"200-day average, while <b>{bottom['ticker']}</b> is furthest "
        f"below at {pct(bottom['pct_vs_ma200'])}.")
    if recent is not None:
        text += (
            f" The most recent trend change was <b>{recent['ticker']}</b>, "
            f"which had a {kind.lower()} on "
            f"{nice_date(recent['last_cross_date'])}.")
    no_cross = df[df["last_cross_date"].isna()]
    if len(no_cross):
        text += (
            f" {list_words(no_cross['ticker'])} had no crossover in the "
            f"data, meaning its trend has held steady the whole time.")
    dynamic_card("What the Data Shows", text)

    static_card("How to Read This Table",
        "<b>Close</b> — the latest closing price.<br>"
        "<b>50-Day Avg</b> — the average close over the last 50 trading "
        "days.<br>"
        "<b>200-Day Avg</b> — the average close over the last 200 trading "
        "days.<br>"
        "<b>Trend: Uptrend</b> — the 50-day average is above the 200-day. "
        "The moment it crosses above is called a <b>golden cross</b>, "
        "a bullish signal.<br>"
        "<b>Trend: Downtrend</b> — the 50-day average is below the "
        "200-day. The moment it crosses below is called a <b>death "
        "cross</b>, a bearish signal.<br>"
        "<b>Last Crossover</b> — the date the trend last changed. Blank "
        "means no crossover in the data.<br>"
        "<b>% vs. 200-Day</b> — how far the price is above (+) or below "
        "(−) its 200-day average. Large values mean the price has moved "
        "far from its long-term trend.")

    show_table(df,
        {"ticker": "Ticker", "asset": "Asset", "close": "Close",
         "ma50": "50-Day Avg", "ma200": "200-Day Avg", "trend": "Trend",
         "last_cross_date": "Last Crossover",
         "pct_vs_ma200": "% vs. 200-Day"},
        {"close": "dollar", "ma50": "dollar", "ma200": "dollar",
         "pct_vs_ma200": "%.1f%%"})

    static_card("SQL Techniques Used",
        "<b>Window functions with frames</b> — AVG() OVER (ROWS BETWEEN "
        "49 PRECEDING AND CURRENT ROW) calculates rolling averages.<br>"
        "<b>ROW_NUMBER()</b> — skips each asset's first 199 days, which "
        "don't have enough history for a true 200-day average.<br>"
        "<b>LAG()</b> — compares today's averages with yesterday's to "
        "detect the day they crossed.<br>"
        "<b>LEFT JOIN</b> — keeps every asset in the table, even one with "
        "no crossover, instead of silently dropping it.<br>"
        "<b>CASE</b> — labels each asset Uptrend or Downtrend.")

    show_sql(sql)


# ══════════════════════════════════════════════════════════════
# SECTION 3 — BIGGEST SINGLE-DAY MOVES
# ══════════════════════════════════════════════════════════════
def section_moves(as_of):
    sql = load_sql("03_biggest_moves.sql")
    df = add_asset_names(run_sql(sql))

    top = df.iloc[0]
    gains = int((df["pct_change"] > 0).sum())
    losses = len(df) - gains
    most = df["ticker"].value_counts()

    section_header("Biggest Single-Day Moves", "Market Event Analysis",
        as_of,
        [("Largest move",
          f"{top['ticker']} {pct(top['pct_change'])}, "
          f"{nice_date(top['date'])}", gain_color(top["pct_change"])),
         ("Up days / down days", f"{gains} / {losses}", DARK),
         ("Appears most often",
          f"{most.index[0]} ({most.iloc[0]} times)", DARK)])

    static_card("Overview",
        "The 20 largest one-day price changes, up or down, across every "
        "asset over the past five years. Big single-day moves usually "
        "come from company news like earnings reports, or from events "
        "that move the whole market at once, such as policy "
        "announcements or economic data. Telling those two apart is a "
        "key idea in cross-asset trading: a <b>single-company</b> move "
        "is about that company, while a <b>market-wide</b> move shows up "
        "in many assets on the same day.")

    text = (
        f"The largest move was <b>{top['ticker']}</b> on "
        f"<b>{nice_date(top['date'])}</b> at <b>{pct(top['pct_change'], 2)}"
        f"</b>. Of the 20 biggest moves, {gains} were gains and {losses} "
        f"were losses. <b>{most.index[0]}</b> appears most often, "
        f"{most.iloc[0]} times.")
    shared = df.groupby("date")["ticker"].apply(list)
    shared = shared[shared.apply(len) >= 2]
    if len(shared):
        shared = shared.loc[shared.apply(len).sort_values(ascending=False).index]
        text += "<br><br>Dates where several assets moved together, a sign of a market-wide event: "
        text += "; ".join(
            f"<b>{nice_date(d)}</b> ({list_words(t)})"
            for d, t in shared.head(3).items()) + "."
    dynamic_card("What the Data Shows", text)

    static_card("How to Read This Table",
        "<b>Date</b> — the trading day of the move.<br>"
        "<b>Close</b> — the closing price that day, adjusted for later "
        "stock splits.<br>"
        "<b>Daily Change</b> — the percentage change from the previous "
        "trading day's close. The table is sorted by the size of the "
        "move, so large drops and large gains are ranked together.")

    show_table(df,
        {"ticker": "Ticker", "asset": "Asset", "date": "Date",
         "close": "Close", "pct_change": "Daily Change"},
        {"close": "dollar", "pct_change": "%.2f%%"})

    static_card("SQL Techniques Used",
        "<b>LAG() window function</b> — looks back one row to get the "
        "previous day's close for the same asset.<br>"
        "<b>PARTITION BY</b> — keeps each asset separate, so one asset "
        "never compares against another's prices.<br>"
        "<b>CTE</b> — calculates every daily change first, so the outer "
        "query can filter and sort on it.<br>"
        "<b>ABS()</b> — sorts by the size of the move regardless of "
        "direction.")

    show_sql(sql)


# ══════════════════════════════════════════════════════════════
# SECTION 4 — VOLUME SPIKES
# ══════════════════════════════════════════════════════════════
def section_volume(as_of):
    sql = load_sql("04_volume_spikes.sql")
    df = add_asset_names(run_sql(sql))

    biggest = df.sort_values("vol_ratio", ascending=False).iloc[0]
    newest = df.iloc[0]
    most = df["ticker"].value_counts()

    section_header("Unusual Volume Spikes", "Trading Activity Analysis",
        as_of,
        [("Largest spike",
          f"{biggest['ticker']} {biggest['vol_ratio']:.1f}x normal", AMBER),
         ("Most recent spike",
          f"{newest['ticker']}, {nice_date(newest['date'])}", DARK),
         ("Spikes most often", f"{most.index[0]} ({most.iloc[0]} times)",
          DARK)])

    static_card("Overview",
        "The 30 most recent days when an asset traded at least "
        "<b>twice its normal volume</b>, compared with its average over "
        "the previous 20 trading days. Volume is the number of shares "
        "traded. Heavy trading often signals news, large institutional "
        "buying or selling, or the start of a bigger move, and a price "
        "move on heavy volume is usually taken more seriously than the "
        "same move on light volume. Some spikes come from the market "
        "calendar instead of news: index rebalancing days and quarterly "
        "options expiration days force large, scheduled trades.")

    text = (
        f"The largest spike in this list was <b>{biggest['ticker']}</b> on "
        f"<b>{nice_date(biggest['date'])}</b>, trading "
        f"<b>{biggest['vol_ratio']:.1f} times</b> its normal volume. "
        f"<b>{most.index[0]}</b> spiked most often, {most.iloc[0]} times "
        f"in the 30 most recent spikes.")
    shared = df.groupby("date")["ticker"].apply(list)
    shared = shared[shared.apply(len) >= 3].sort_index(ascending=False)
    if len(shared):
        text += ("<br><br>Days when three or more assets spiked together, "
                 "often a scheduled market event or market-wide news: ")
        text += "; ".join(
            f"<b>{nice_date(d)}</b> ({list_words(t)})"
            for d, t in shared.head(3).items()) + "."
    dynamic_card("What the Data Shows", text)

    static_card("How to Read This Table",
        "<b>Date</b> — the trading day of the spike.<br>"
        "<b>Close</b> — the closing price that day.<br>"
        "<b>Volume</b> — shares traded that day (M = millions).<br>"
        "<b>20-Day Avg Volume</b> — the average daily volume over the 20 "
        "trading days before the spike. Today's volume is left out of "
        "its own average so it can't hide the spike.<br>"
        "<b>Volume Ratio</b> — the day's volume divided by the average. "
        "3.0x means three times the normal amount traded.")

    show_table(df,
        {"ticker": "Ticker", "asset": "Asset", "date": "Date",
         "close": "Close", "volume": "Volume",
         "avg_vol_20": "20-Day Avg Volume", "vol_ratio": "Volume Ratio"},
        {"close": "dollar", "volume": "compact", "avg_vol_20": "compact",
         "vol_ratio": "%.1fx"})

    static_card("SQL Techniques Used",
        "<b>Window frame</b> — AVG() OVER (ROWS BETWEEN 20 PRECEDING AND "
        "1 PRECEDING) builds a rolling 20-day average that slides forward "
        "day by day.<br>"
        "<b>Avoiding lookahead bias</b> — the frame stops at yesterday, "
        "so the day being measured isn't part of its own baseline.<br>"
        "<b>CAST</b> — converts the average to a whole number of "
        "shares.<br>"
        "<b>CTE</b> — calculates the averages first, then filters to "
        "days above twice normal.")

    show_sql(sql)


# ══════════════════════════════════════════════════════════════
# SECTION 5 — CROSSOVER SIGNALS
# ══════════════════════════════════════════════════════════════
def section_crossovers(as_of):
    sql = load_sql("05_ma_crossovers.sql")
    df = add_asset_names(run_sql(sql))

    newest = df.iloc[0]
    golden = int((df["signal"] == "Golden cross").sum())
    death = len(df) - golden
    most = df["ticker"].value_counts()

    section_header("Moving Average Crossover Signals",
        "Trend Signal History", as_of,
        [("Most recent signal",
          f"{newest['ticker']} {newest['signal'].lower()}, "
          f"{nice_date(newest['date'])}",
          GREEN if newest["signal"] == "Golden cross" else RED),
         ("Golden crosses", str(golden), GREEN),
         ("Death crosses", str(death), RED)])

    static_card("Overview",
        "The 30 most recent days when an asset's 50-day moving average "
        "crossed its 200-day moving average. A <b>golden cross</b> "
        "(50-day crossing above) is read as bullish, and a <b>death "
        "cross</b> (crossing below) as bearish. These are some of the "
        "most widely watched signals in markets, but they have two known "
        "weaknesses: they are <b>slow</b>, often arriving after much of "
        "a move has already happened, and they produce <b>whipsaws</b>, "
        "repeated false signals when a price moves sideways.")

    first_date = df["date"].min()
    text = (
        f"Since <b>{nice_date(first_date)}</b>, these 30 signals include "
        f"<b>{golden} golden crosses</b> and <b>{death} death crosses</b>. "
        f"The most recent was a {newest['signal'].lower()} in "
        f"<b>{newest['ticker']}</b> on {nice_date(newest['date'])}.")
    flippers = most[most >= 3]
    if len(flippers):
        text += (
            f"<br><br>{list_words(flippers.index)} crossed three or more "
            f"times in this period. Frequent back-and-forth crossings are "
            f"a sign of <b>whipsaw</b>: when a price moves sideways, the "
            f"two averages sit close together and cross repeatedly.")
    dynamic_card("What the Data Shows", text)

    static_card("How to Read This Table",
        "<b>Date</b> — the day the crossover happened.<br>"
        "<b>Close</b> — the closing price that day.<br>"
        "<b>50-Day Avg / 200-Day Avg</b> — the two moving averages. On a "
        "crossover day they are very close, because they just crossed.<br>"
        "<b>Signal</b> — <b>Golden cross</b> means the 50-day moved above "
        "the 200-day (bullish); <b>Death cross</b> means it moved below "
        "(bearish).")

    show_table(df,
        {"ticker": "Ticker", "asset": "Asset", "date": "Date",
         "close": "Close", "ma50": "50-Day Avg", "ma200": "200-Day Avg",
         "signal": "Signal"},
        {"close": "dollar", "ma50": "dollar", "ma200": "dollar"})

    static_card("SQL Techniques Used",
        "<b>Three-stage CTE</b> — calculate the averages, attach "
        "yesterday's values, then keep only crossover days.<br>"
        "<b>Window frames</b> — build the 50-day and 200-day rolling "
        "averages.<br>"
        "<b>LAG()</b> — compares yesterday's averages with today's. If "
        "their order flipped, a crossover happened.<br>"
        "<b>CASE</b> — labels each signal golden or death cross.")

    show_sql(sql)


# ══════════════════════════════════════════════════════════════
# THE PAGE
# ══════════════════════════════════════════════════════════════
def render():
    # ── Page title and introduction (same style as AI Finance) ──
    st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)
    st.markdown("# SQL Market Data Explorer")
    st.markdown("""
    <p style="color:#333333; font-size:16px;">
    Using SQL to turn five years of daily market data into signals and
    insights. Every table is produced by a SQL query against a database
    of stocks and cross-asset ETFs, and the query behind each one is
    shown below it.
    </p>
    <p style="color:#666666; font-size:13px; font-style:italic; font-weight:700; margin-top:-0.4rem;">
    For educational and research purposes only. Not investment advice.
    </p>
    """, unsafe_allow_html=True)

    # Stop with a clear message if the database file is missing.
    if not DB_PATH.exists():
        st.error("The market database (sql/trading.db) wasn't found. "
                 "Add it to the sql folder and redeploy.")
        return

    # The latest date in the database, shown on every results card.
    latest = run_sql(load_sql("00_latest_date.sql"))["latest_date"].iloc[0]
    as_of = nice_date(latest)

    # ── Section buttons (same card style as the model buttons) ──
    cols = st.columns(len(SECTIONS))
    clicked = None
    for col, name in zip(cols, SECTIONS):
        with col:
            key = "btn_sql_" + name.lower().replace(" ", "_").replace(".", "").replace("&", "")
            if st.button(name, key=key, width="stretch"):
                clicked = name

    # Remember which section is open. "sql_view" is this page's own
    # setting, separate from the AI Finance "model" setting.
    if st.session_state.get("sql_view") not in SECTIONS:
        st.session_state.sql_view = SECTIONS[0]
    if clicked:
        st.session_state.sql_view = clicked
    st.markdown("---")

    # ── Show the chosen section ──
    view = st.session_state.sql_view
    if view == "Performance vs. S&P 500":
        section_performance(as_of)
    elif view == "Trend Status":
        section_trend(as_of)
    elif view == "Biggest Moves":
        section_moves(as_of)
    elif view == "Volume Spikes":
        section_volume(as_of)
    elif view == "Crossover Signals":
        section_crossovers(as_of)

    # ── Data sources and full project (shown for every section) ──
    st.markdown("---")
    st.markdown(f"""
    <div class="data-source-section">
        <h3>Data Sources</h3>
        <p>
        <b>Prices:</b> Daily prices from Yahoo Finance for 14 assets —
        seven large US stocks, the S&amp;P 500 and Nasdaq 100 ETFs, four
        bond ETFs covering Treasuries, investment-grade and high-yield
        corporate bonds, and mortgage-backed securities, plus a gold ETF.<br><br>
        <b>Adjustments:</b> Prices are adjusted for stock splits,
        dividends, and interest payments, so returns reflect total
        return.<br><br>
        <b>Database:</b> Five years of daily data stored in a SQLite
        database. Latest trading day included: <b>{as_of}</b>.<br><br>
        All tables are produced by SQL queries; Python and Streamlit
        display the results.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Full SQL Project</h3>
        <p>
        View the database setup, data loader, and every SQL query
        on GitHub, in the sql folder:<br><br>
        github.com/sidneyppratt-svg/quant-regime-detector
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer (same wording style as AI Finance) ──
    st.markdown("---")
    st.markdown("""
    <p style="color:#666666; font-size:12px; line-height:1.5; font-weight:700;">
    <b>Disclaimer:</b> This page is for educational and research
    purposes only and does not constitute investment, financial, or
    trading advice. Signals and statistics are based on historical data
    and simplified assumptions, may contain errors, and do not predict
    future results. Past performance does not guarantee future returns.
    Consult a qualified financial professional before making investment
    decisions.
    </p>
    """, unsafe_allow_html=True)
