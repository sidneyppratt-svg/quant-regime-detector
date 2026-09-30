-- ============================================================
-- 06_vs_spy.sql
-- Calculates each ticker's return over the past year and
-- compares it with SPY (the S&P 500 benchmark).
-- ============================================================

-- STAGE 1: Find each ticker's first and last trading day
-- within the past year.
-- CHANGED: "The past year" is now measured back from the LATEST
-- DATE IN THE DATABASE instead of today's date. On the website,
-- the data only updates when refreshed, so this keeps the
-- one-year window lined up with the data that's actually there.
-- The subquery finds the latest date, and DATE(..., '-1 year')
-- subtracts one year from it.
WITH bounds AS (
    SELECT ticker,
           MIN(date) AS start_date,
           MAX(date) AS end_date
    FROM prices
    WHERE date >= (SELECT DATE(MAX(date), '-1 year') FROM prices)
    GROUP BY ticker
),

-- STAGE 2: Look up the closing prices on those two dates and
-- calculate the one-year return.
-- This joins the prices table to itself twice (a "self-join"):
--   s = the row for the START date
--   e = the row for the END date
perf AS (
    SELECT b.ticker,
           s.close AS start_price,
           e.close AS end_price,
           100.0 * (e.close - s.close) / s.close AS return_pct
    FROM bounds b
    JOIN prices s ON s.ticker = b.ticker AND s.date = b.start_date
    JOIN prices e ON e.ticker = b.ticker AND e.date = b.end_date
)

-- STAGE 3: Attach SPY's return to every row with CROSS JOIN,
-- then subtract it to see which assets beat the market.
SELECT p.ticker,
       ROUND(p.start_price, 2)                 AS start_price,
       ROUND(p.end_price, 2)                   AS end_price,
       ROUND(p.return_pct, 1)                  AS return_1y,
       ROUND(p.return_pct - spy.return_pct, 1) AS vs_spy
FROM perf p
CROSS JOIN (SELECT return_pct FROM perf WHERE ticker = 'SPY') spy
ORDER BY p.return_pct DESC;   -- best performers first