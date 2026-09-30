-- ============================================================
-- 02_daily_returns.sql
-- Calculates the daily percentage change in closing price
-- for one ticker, using the LAG window function.
-- ============================================================

SELECT ticker,
       date,
       ROUND(close, 2) AS close,

       -- LAG(close) gets the closing price from the previous row.
       -- PARTITION BY ticker: treat each ticker separately, so one
       --   stock never compares against another stock's prices.
       -- ORDER BY date: put rows in date order, so "previous row"
       --   means the prior trading day.
       ROUND(LAG(close) OVER (PARTITION BY ticker ORDER BY date), 2)
           AS prev_close,

       -- Daily % change = (today - yesterday) / yesterday x 100
       -- 100.0 (with the decimal) forces decimal math so results
       -- aren't rounded down to whole numbers.
       ROUND(
           100.0 * (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
                 / LAG(close) OVER (PARTITION BY ticker ORDER BY date),
       2) AS pct_change

FROM prices
WHERE ticker = 'TLT'   -- change this to look at a different ticker
ORDER BY date DESC      -- newest days first
LIMIT 20;               -- show only the 20 most recent days