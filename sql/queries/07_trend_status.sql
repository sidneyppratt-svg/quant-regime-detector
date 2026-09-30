-- ============================================================
-- 07_trend_status.sql
-- Shows each ticker's CURRENT trend based on its moving
-- averages, the date of its last crossover, and how far the
-- price is above or below its 200-day average.
-- ============================================================

-- STAGE 1: Calculate the 50-day and 200-day moving averages
-- for every day (same as 05_ma_crossovers.sql).
WITH ma AS (
    SELECT ticker,
           date,
           close,
           AVG(close) OVER (
               PARTITION BY ticker ORDER BY date
               ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
           ) AS ma50,
           AVG(close) OVER (
               PARTITION BY ticker ORDER BY date
               ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
           ) AS ma200,
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date) AS day_num
    FROM prices
),

-- STAGE 2: Keep days with a full 200 days of history and
-- attach yesterday's averages (same as before).
with_prev AS (
    SELECT *,
           LAG(ma50)  OVER (PARTITION BY ticker ORDER BY date) AS prev_ma50,
           LAG(ma200) OVER (PARTITION BY ticker ORDER BY date) AS prev_ma200
    FROM ma
    WHERE day_num >= 200
),

-- STAGE 3: Find the date of each ticker's MOST RECENT crossover.
-- MAX(date) picks the latest one out of all its crossovers.
crosses AS (
    SELECT ticker,
           MAX(date) AS last_cross_date
    FROM with_prev
    WHERE (prev_ma50 <= prev_ma200 AND ma50 > ma200)
       OR (prev_ma50 >= prev_ma200 AND ma50 < ma200)
    GROUP BY ticker
),

-- STAGE 4: Keep only each ticker's row for the latest date
-- in the database, which is its current status.
latest AS (
    SELECT *
    FROM with_prev
    WHERE date = (SELECT MAX(date) FROM prices)
)

-- STAGE 5: Combine the current status with the last crossover date.
-- LEFT JOIN keeps EVERY ticker from "latest", even one with no
-- crossover in the data (its last_cross_date shows as empty).
-- A regular JOIN would drop that ticker completely.
SELECT l.ticker,
       ROUND(l.close, 2) AS close,
       ROUND(l.ma50, 2)  AS ma50,
       ROUND(l.ma200, 2) AS ma200,
       CASE WHEN l.ma50 > l.ma200 THEN 'Uptrend'
            ELSE 'Downtrend'
       END AS trend,
       c.last_cross_date,
       -- How far today's price is above (+) or below (-) its
       -- 200-day average, as a percentage.
       ROUND(100.0 * (l.close - l.ma200) / l.ma200, 1) AS pct_vs_ma200
FROM latest l
LEFT JOIN crosses c ON c.ticker = l.ticker
ORDER BY pct_vs_ma200 DESC;