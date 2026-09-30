# ============================================================
# create_db.py
# Creates the SQLite database (trading.db) and the prices table
# that stores daily stock price data.
# ============================================================

# Load SQLite, the database system built into Python.
import sqlite3

# Open the database file. If trading.db doesn't exist yet,
# this creates it in the project folder.
conn = sqlite3.connect("trading.db")

# Create the prices table, which holds one row per stock per day.
# IF NOT EXISTS means running this script again won't cause an error.
#   ticker  - the stock symbol, like AAPL (text, required)
#   date    - the trading day, as YYYY-MM-DD (text, required)
#   open    - price at the start of the day (decimal)
#   high    - highest price of the day (decimal)
#   low     - lowest price of the day (decimal)
#   close   - price at the end of the day (decimal)
#   volume  - number of shares traded (whole number)
# PRIMARY KEY (ticker, date) allows only one row per stock per day,
# which prevents duplicate data and makes searches fast.
conn.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        ticker  TEXT    NOT NULL,
        date    TEXT    NOT NULL,
        open    REAL,
        high    REAL,
        low     REAL,
        close   REAL,
        volume  INTEGER,
        PRIMARY KEY (ticker, date)
    )
""")

# Save the change permanently, then close the database.
conn.commit()
conn.close()

# Show a message so we know the script finished successfully.
print("Database created: trading.db")