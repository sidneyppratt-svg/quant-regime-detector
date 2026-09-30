-- ============================================================
-- 01_check_data.sql
-- Summarizes the data for each ticker to confirm everything
-- loaded correctly.
-- ============================================================

-- In SQL, lines starting with -- are comments (like # in Python).

SELECT ticker,
       COUNT(*)             AS days,        -- number of trading days
       MIN(date)            AS first_date,  -- earliest date
       MAX(date)            AS last_date,   -- most recent date
       ROUND(MIN(close), 2) AS min_close,   -- lowest closing price
       ROUND(MAX(close), 2) AS max_close    -- highest closing price
FROM prices
GROUP BY ticker    -- one summary row per ticker
ORDER BY ticker;   -- sort alphabetically