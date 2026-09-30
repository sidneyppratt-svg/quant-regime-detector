-- ============================================================
-- 00_latest_date.sql
-- Finds the most recent date in the database, so the page can
-- show visitors how current the data is.
-- ============================================================

SELECT MAX(date) AS latest_date
FROM prices;