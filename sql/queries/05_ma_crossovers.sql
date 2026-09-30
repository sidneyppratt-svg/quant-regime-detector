-- ============================================================
-- 05_ma_crossovers.sql
-- Finds the days when a ticker's 50-day moving average crossed
-- above or below its 200-day moving average.
--   Golden cross: 50-day crosses ABOVE 200-day (bullish signal)
--   Death cross:  50-day crosses BELOW 200-day (bearish signal)
-- ============================================================

-- STAGE 1: Calculate both moving averages for every day.
WITH ma AS (
    SELECT ticker,
           date,
           close,

           -- 50-day moving average: average close over this day
           -- and the 49 days before it (50 days total).
           AVG(close) OVER (
               PARTITION BY ticker ORDER BY date
               ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
           ) AS ma50,

           -- 200-day moving average: this day plus the 199 before it.
           AVG(close) OVER (
               PARTITION BY ticker ORDER BY date
               ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
           ) AS ma200,

           -- Number each ticker's days 1, 2, 3... in date order,
           -- so we can tell which days have a full 200 days of history.
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date) AS day_num
    FROM prices
),

-- STAGE 2: Drop the early days that don't have 200 days of
-- history yet, then attach YESTERDAY's averages to each row.
with_prev AS (
    SELECT *,
           LAG(ma50)  OVER (PARTITION BY ticker ORDER BY date) AS prev_ma50,
           LAG(ma200) OVER (PARTITION BY ticker ORDER BY date) AS prev_ma200
    FROM ma
    WHERE day_num >= 200
)

-- STAGE 3: Keep only the days where the relationship flipped,
-- and label each one.
SELECT ticker,
       date,
       ROUND(close, 2) AS close,
       ROUND(ma50, 2)  AS ma50,
       ROUND(ma200, 2) AS ma200,

       -- CASE works like "if/else": if the 50-day is now above,
       -- it's a golden cross; otherwise it's a death cross.
       CASE WHEN ma50 > ma200 THEN 'Golden cross'
            ELSE 'Death cross'
       END AS signal
FROM with_prev
WHERE (prev_ma50 <= prev_ma200 AND ma50 > ma200)   -- crossed above
   OR (prev_ma50 >= prev_ma200 AND ma50 < ma200)   -- crossed below
ORDER BY date DESC
LIMIT 30;