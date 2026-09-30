-- ============================================================
-- 04_volume_spikes.sql
-- Finds days when a ticker traded at least twice its normal
-- volume, compared with its average over the prior 20 days.
-- ============================================================

-- STAGE 1: For every ticker and day, calculate the average volume
-- over the 20 trading days BEFORE that day (about one month).
WITH vol AS (
    SELECT ticker,
           date,
           close,
           volume,

           -- ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING is the
           -- "window frame": average only the 20 rows before this
           -- one. It stops at 1 PRECEDING (yesterday) on purpose,
           -- so today's volume doesn't inflate its own baseline.
           AVG(volume) OVER (
               PARTITION BY ticker
               ORDER BY date
               ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING
           ) AS avg_vol_20
    FROM prices
)

-- STAGE 2: Keep only the days where volume was more than
-- 2x the 20-day average, newest first.
SELECT ticker,
       date,
       ROUND(close, 2)              AS close,
       volume,
       CAST(avg_vol_20 AS INTEGER)  AS avg_vol_20,  -- whole number
       ROUND(volume / avg_vol_20, 1) AS vol_ratio   -- times normal volume
FROM vol
WHERE volume > 2 * avg_vol_20
ORDER BY date DESC
LIMIT 30;