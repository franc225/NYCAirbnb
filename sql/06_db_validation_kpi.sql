/* =============================================================================
   06_db_validation_kpi.sql
   Purpose:
     1) Validate star schema integrity in nycairbnb.db (SQLite)
     2) Provide core BI KPI queries (tool-agnostic)
   Tables:
     fact_listing_2019, dim_host, dim_location, dim_room_type, dim_listing
============================================================================= */

-- -----------------------------------------------------------------------------
-- A) DATABASE / SCHEMA CHECKS
-- -----------------------------------------------------------------------------

-- A1) Check tables exist
SELECT name AS table_name
FROM sqlite_master
WHERE type = 'table'
  AND name IN ('fact_listing_2019','dim_host','dim_location','dim_room_type','dim_listing')
ORDER BY name;

-- A2) Row counts (basic sanity)
SELECT 'fact_listing_2019' AS table_name, COUNT(*) AS row_count FROM fact_listing_2019
UNION ALL SELECT 'dim_host', COUNT(*) FROM dim_host
UNION ALL SELECT 'dim_location', COUNT(*) FROM dim_location
UNION ALL SELECT 'dim_room_type', COUNT(*) FROM dim_room_type
UNION ALL SELECT 'dim_listing', COUNT(*) FROM dim_listing;

-- A3) Null foreign keys in fact (should be 0)
SELECT
  SUM(CASE WHEN listing_key   IS NULL THEN 1 ELSE 0 END) AS null_listing_key,
  SUM(CASE WHEN host_key      IS NULL THEN 1 ELSE 0 END) AS null_host_key,
  SUM(CASE WHEN location_key  IS NULL THEN 1 ELSE 0 END) AS null_location_key,
  SUM(CASE WHEN room_type_key IS NULL THEN 1 ELSE 0 END) AS null_room_type_key
FROM fact_listing_2019;

-- A4) Orphan FK checks (fact keys not found in dimensions) - should be 0
SELECT 'host_key_orphans' AS check_name, COUNT(*) AS orphan_count
FROM fact_listing_2019 f
LEFT JOIN dim_host d ON f.host_key = d.host_key
WHERE d.host_key IS NULL
UNION ALL
SELECT 'location_key_orphans', COUNT(*)
FROM fact_listing_2019 f
LEFT JOIN dim_location d ON f.location_key = d.location_key
WHERE d.location_key IS NULL
UNION ALL
SELECT 'room_type_key_orphans', COUNT(*)
FROM fact_listing_2019 f
LEFT JOIN dim_room_type d ON f.room_type_key = d.room_type_key
WHERE d.room_type_key IS NULL
UNION ALL
SELECT 'listing_key_orphans', COUNT(*)
FROM fact_listing_2019 f
LEFT JOIN dim_listing d ON f.listing_key = d.listing_key
WHERE d.listing_key IS NULL;

-- A5) Uniqueness checks in dimensions (should be 0 duplicates)
SELECT 'dim_host.host_key_duplicates' AS check_name, COUNT(*) AS dup_count
FROM (
  SELECT host_key FROM dim_host GROUP BY host_key HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'dim_location.location_key_duplicates', COUNT(*)
FROM (
  SELECT location_key FROM dim_location GROUP BY location_key HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'dim_room_type.room_type_key_duplicates', COUNT(*)
FROM (
  SELECT room_type_key FROM dim_room_type GROUP BY room_type_key HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'dim_listing.listing_key_duplicates', COUNT(*)
FROM (
  SELECT listing_key FROM dim_listing GROUP BY listing_key HAVING COUNT(*) > 1
);

-- A6) Measure sanity checks (counts of invalid rows; should be 0)
SELECT
  SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END) AS price_le_0,
  SUM(CASE WHEN price > 1000 THEN 1 ELSE 0 END) AS price_gt_1000,
  SUM(CASE WHEN availability_365 < 0 OR availability_365 > 365 THEN 1 ELSE 0 END) AS availability_out_of_range,
  SUM(CASE WHEN estimated_booked_days < 0 OR estimated_booked_days > 365 THEN 1 ELSE 0 END) AS booked_days_out_of_range,
  SUM(CASE WHEN ABS((price * estimated_booked_days) - estimated_revenue) > 0.000001 THEN 1 ELSE 0 END) AS revenue_formula_mismatch,
  SUM(CASE WHEN price_percentile < 0 OR price_percentile > 1 THEN 1 ELSE 0 END) AS price_pct_out_of_range,
  SUM(CASE WHEN revenue_percentile < 0 OR revenue_percentile > 1 THEN 1 ELSE 0 END) AS revenue_pct_out_of_range
FROM fact_listing_2019;

-- -----------------------------------------------------------------------------
-- B) CORE KPI QUERIES
-- -----------------------------------------------------------------------------

-- B1) Global KPI summary (average + robust percentiles)
SELECT
  COUNT(*) AS listings,
  ROUND(AVG(price), 2) AS avg_price,
  ROUND(AVG(estimated_booked_days), 2) AS avg_booked_days,
  ROUND(AVG(estimated_revenue), 2) AS avg_est_revenue,
  -- "Median-like" approximation using percentile ranks (nearest to 0.50)
  (SELECT price FROM fact_listing_2019 ORDER BY ABS(price_percentile - 0.50) LIMIT 1) AS approx_median_price,
  (SELECT estimated_booked_days FROM fact_listing_2019 ORDER BY ABS(revenue_percentile - 0.50) LIMIT 1) AS approx_median_booked_days,
  (SELECT estimated_revenue FROM fact_listing_2019 ORDER BY ABS(revenue_percentile - 0.50) LIMIT 1) AS approx_median_revenue,
  -- p95 (nearest to 0.95)
  (SELECT price FROM fact_listing_2019 ORDER BY ABS(price_percentile - 0.95) LIMIT 1) AS approx_p95_price,
  (SELECT estimated_revenue FROM fact_listing_2019 ORDER BY ABS(revenue_percentile - 0.95) LIMIT 1) AS approx_p95_revenue
FROM fact_listing_2019;

-- B2) Borough performance (median-like revenue + listing counts)
SELECT
  dl.neighbourhood_group AS borough,
  COUNT(*) AS listings,
  ROUND(AVG(f.price), 2) AS avg_price,
  ROUND(AVG(f.estimated_booked_days), 2) AS avg_booked_days,
  ROUND(AVG(f.estimated_revenue), 2) AS avg_est_revenue,
  -- median-like revenue: pick row near 0.50 within borough using revenue_percentile
  (SELECT f2.estimated_revenue
   FROM fact_listing_2019 f2
   JOIN dim_location dl2 ON f2.location_key = dl2.location_key
   WHERE dl2.neighbourhood_group = dl.neighbourhood_group
   ORDER BY ABS(f2.revenue_percentile - 0.50)
   LIMIT 1) AS approx_median_revenue
FROM fact_listing_2019 f
JOIN dim_location dl ON f.location_key = dl.location_key
GROUP BY dl.neighbourhood_group
ORDER BY avg_est_revenue DESC;

-- B3) Room type performance
SELECT
  dr.room_type,
  COUNT(*) AS listings,
  ROUND(AVG(f.price), 2) AS avg_price,
  ROUND(AVG(f.estimated_booked_days), 2) AS avg_booked_days,
  ROUND(AVG(f.estimated_revenue), 2) AS avg_est_revenue
FROM fact_listing_2019 f
JOIN dim_room_type dr ON f.room_type_key = dr.room_type_key
GROUP BY dr.room_type
ORDER BY avg_est_revenue DESC;

-- B4) Top 10 neighborhoods by total estimated revenue
SELECT
  dl.neighbourhood_group,
  dl.neighbourhood,
  ROUND(SUM(f.estimated_revenue), 0) AS total_est_revenue,
  COUNT(*) AS listings
FROM fact_listing_2019 f
JOIN dim_location dl ON f.location_key = dl.location_key
GROUP BY dl.neighbourhood_group, dl.neighbourhood
ORDER BY total_est_revenue DESC
LIMIT 10;

-- B5) High performers (Top 5% revenue)
SELECT
  dl.neighbourhood_group AS borough,
  COUNT(*) AS listings_top_5pct
FROM fact_listing_2019 f
JOIN dim_location dl ON f.location_key = dl.location_key
WHERE f.revenue_percentile >= 0.95
GROUP BY dl.neighbourhood_group
ORDER BY listings_top_5pct DESC;

-- B6) Price segmentation (simple BI buckets)
SELECT
  CASE
    WHEN price < 100 THEN 'Budget (<100)'
    WHEN price BETWEEN 100 AND 200 THEN 'Standard (100-200)'
    WHEN price BETWEEN 201 AND 400 THEN 'Premium (201-400)'
    ELSE 'Luxury (401+)'
  END AS price_segment,
  COUNT(*) AS listings,
  ROUND(AVG(price), 2) AS avg_price,
  ROUND(AVG(estimated_revenue), 2) AS avg_est_revenue
FROM fact_listing_2019
GROUP BY price_segment
ORDER BY avg_est_revenue DESC;

-- -----------------------------------------------------------------------------
-- C) OPTIONAL: QUICK JOIN SMOKE TEST (returns a few rows)
-- -----------------------------------------------------------------------------
SELECT
  dl.neighbourhood_group,
  dl.neighbourhood,
  dr.room_type,
  dh.host_id,
  f.price,
  f.estimated_booked_days,
  f.estimated_revenue
FROM fact_listing_2019 f
JOIN dim_location dl ON f.location_key = dl.location_key
JOIN dim_room_type dr ON f.room_type_key = dr.room_type_key
JOIN dim_host dh ON f.host_key = dh.host_key
LIMIT 20;