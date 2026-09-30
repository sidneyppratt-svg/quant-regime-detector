-- ============================================================
-- 03_biggest_moves.sql
-- Finds the 20 largest single-day price moves (up or down)
-- across all tickers, using a CTE.
-- ============================================================

-- STAGE 1: The CTE.
-- WITH returns AS (...) creates a temporary named result called
-- "returns" that exists only while this query runs. Here it
-- calculates the daily % change for every ticker and every day.
WITH returns AS (
    SELECT ticker,
           date,
           close,
           100.0 * (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
                 / LAG(close) OVER (PARTITION BY ticker ORDER BY date)
               AS pct_change
    FROM prices
)

-- STAGE 2: The main query.
-- Reads from "returns" as if it were a regular table, then
-- filters and sorts the results.
SELECT ticker,
       date,
       ROUND(close, 2)      AS close,
       ROUND(pct_change, 2) AS pct_change
FROM returns
WHERE pct_change IS NOT NULL   -- skip each ticker's first day (no previous day)
ORDER BY ABS(pct_change) DESC  -- biggest moves first, up or down
LIMIT 20;                      -- top 20 only