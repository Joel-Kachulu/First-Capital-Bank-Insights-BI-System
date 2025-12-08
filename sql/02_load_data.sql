-- ============================================================
-- FIRST CAPITAL BANK INSIGHTS BI SYSTEM
-- Data Loading Script
-- Loads cleaned CSV data into star schema tables
-- ============================================================

-- Note: This script provides examples for different database systems
-- Choose the appropriate method for your database
-- 
-- For SQLite users: Use the Python script sql/load_to_sqlite.py instead
-- For PostgreSQL: Use COPY command (examples below)
-- For MySQL: Use LOAD DATA INFILE (examples below)
-- For SQL Server: Use BULK INSERT or import wizard

-- ============================================================
-- Load Dimension Tables
-- ============================================================

-- Load dim_customer
-- PostgreSQL example:
-- COPY dim_customer FROM '../data/clean/customers.csv' WITH CSV HEADER;

-- MySQL example:
-- LOAD DATA LOCAL INFILE '../data/clean/customers.csv'
-- INTO TABLE dim_customer
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- Load dim_branch
-- COPY dim_branch FROM '../data/clean/branches.csv' WITH CSV HEADER;

-- Load dim_account
-- COPY dim_account FROM '../data/clean/accounts.csv' WITH CSV HEADER;

-- ============================================================
-- Populate dim_date
-- ============================================================

-- Generate date dimension for the last 2 years
INSERT INTO dim_date (date_key, year, quarter, month, month_name, week, day_of_week, day_name, is_weekend)
SELECT 
    date_key,
    EXTRACT(YEAR FROM date_key) AS year,
    EXTRACT(QUARTER FROM date_key) AS quarter,
    EXTRACT(MONTH FROM date_key) AS month,
    TO_CHAR(date_key, 'Month') AS month_name,
    EXTRACT(WEEK FROM date_key) AS week,
    EXTRACT(DOW FROM date_key) AS day_of_week,
    TO_CHAR(date_key, 'Day') AS day_name,
    CASE WHEN EXTRACT(DOW FROM date_key) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(
    CURRENT_DATE - INTERVAL '2 years',
    CURRENT_DATE,
    '1 day'::interval
) AS date_key;

-- ============================================================
-- Load Fact Table
-- ============================================================

-- Load fact_transactions
-- Note: Map 'date' column to 'date_key' and ensure date_key exists in dim_date
-- COPY fact_transactions (transaction_id, account_id, date_key, transaction_type, amount, transaction_month, risk_flag, day_of_week, week)
-- FROM '../data/clean/transactions.csv' WITH CSV HEADER;

-- ============================================================
-- Data Validation Queries
-- ============================================================

-- Check record counts
SELECT 'dim_customer' AS table_name, COUNT(*) AS record_count FROM dim_customer
UNION ALL
SELECT 'dim_branch', COUNT(*) FROM dim_branch
UNION ALL
SELECT 'dim_account', COUNT(*) FROM dim_account
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'fact_transactions', COUNT(*) FROM fact_transactions;

-- Check for missing foreign keys
SELECT 
    'Missing customer_id in dim_customer' AS issue,
    COUNT(*) AS count
FROM fact_transactions ft
JOIN dim_account da ON ft.account_id = da.account_id
LEFT JOIN dim_customer dc ON da.customer_id = dc.customer_id
WHERE dc.customer_id IS NULL;

