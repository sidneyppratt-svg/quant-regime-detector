# ============================================================
# load_data.py
# Downloads 5 years of daily price data from Yahoo Finance
# and saves it into the prices table in trading.db.
# Safe to rerun anytime to refresh the data.
# ============================================================

# Load SQLite (the database) and yfinance (downloads stock prices).
import sqlite3
import yfinance as yf

# The tickers to download, grouped by asset type.
TICKERS = [
    # Individual stocks
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "JPM", "XOM",
    # Stock market ETFs
    "SPY",   # S&P 500 (the overall market benchmark)
    "QQQ",   # Nasdaq 100 (large tech companies)
    # Bond and credit ETFs
    "TLT",   # 20+ year US Treasury bonds
    "LQD",   # Investment-grade corporate bonds
    "HYG",   # High-yield (junk) corporate bonds
    "MBB",   # Mortgage-backed securities
    # Commodity ETF
    "GLD",   # Gold
]

# Open the database created in Step 7.
conn = sqlite3.connect("trading.db")

# Keep a count of how many rows are loaded in total.
total_rows = 0

# Go through the tickers one at a time.
for ticker in TICKERS:
    print(f"Downloading {ticker}...")

    # try/except means that if one ticker fails, the script prints
    # the problem and moves on instead of stopping completely.
    try:
        # Download 5 years of daily prices.
        # auto_adjust=True corrects past prices for stock splits and
        # dividends, so a split doesn't look like a sudden crash.
        df = yf.Ticker(ticker).history(period="5y", auto_adjust=True)

        # NEW: Remove any rows with missing prices. Yahoo sometimes
        # sends a row for the current day before its data is final,
        # with blank (NaN) prices. dropna() drops those rows.
        df = df.dropna(subset=["Open", "High", "Low", "Close"])

        # Skip this ticker if nothing came back.
        if df.empty:
            print(f"  No data for {ticker}, skipping")
            continue

        # yfinance stores the date as the table's index (row labels).
        # reset_index() turns it into a regular Date column.
        df = df.reset_index()

        # Convert each row into the exact order of the prices table:
        # (ticker, date, open, high, low, close, volume)
        rows = [
            (
                ticker,
                row.Date.strftime("%Y-%m-%d"),  # date as YYYY-MM-DD text
                float(row.Open),
                float(row.High),
                float(row.Low),
                float(row.Close),
                int(row.Volume),
            )
            for row in df.itertuples()
        ]

        # Insert all rows at once. The ? marks are placeholders that
        # Python fills in safely. INSERT OR REPLACE overwrites a row if
        # that ticker and date already exist, so rerunning never
        # creates duplicates.
        conn.executemany(
            "INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )

        # Save this ticker's data before moving to the next one.
        conn.commit()
        total_rows += len(rows)
        print(f"  Loaded {len(rows)} rows")

    except Exception as error:
        print(f"  Problem with {ticker}: {error}")

# NEW: Clean up any incomplete rows already in the database
# (like the ones saved on the first run). In SQL, a missing
# value is called NULL, and IS NULL finds those rows.
cursor = conn.execute(
    "DELETE FROM prices "
    "WHERE open IS NULL OR high IS NULL OR low IS NULL OR close IS NULL"
)
conn.commit()
print(f"Removed {cursor.rowcount} incomplete rows.")

# Close the database and show a summary.
conn.close()
print(f"Done. {total_rows} rows loaded in total.")