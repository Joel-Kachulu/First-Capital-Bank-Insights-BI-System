-- ============================================================
-- FIRST CAPITAL BANK INSIGHTS BI SYSTEM
-- KPI Queries for Business Intelligence
-- ============================================================

-- ============================================================
-- 1. TOTAL DEPOSITS AND WITHDRAWALS PER BRANCH
-- ============================================================
SELECT 
    db.branch_name,
    db.city,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) AS total_deposits_mwk,
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS total_withdrawals_mwk,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) - 
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS net_flow_mwk,
    COUNT(CASE WHEN ft.transaction_type = 'deposit' THEN 1 END) AS deposit_count,
    COUNT(CASE WHEN ft.transaction_type = 'withdrawal' THEN 1 END) AS withdrawal_count
FROM fact_transactions ft
JOIN dim_account da ON ft.account_id = da.account_id
JOIN dim_branch db ON da.branch_id = db.branch_id
GROUP BY db.branch_id, db.branch_name, db.city
ORDER BY total_deposits_mwk DESC;

-- ============================================================
-- 2. TRANSACTION TRENDS BY DAY/WEEK/MONTH
-- ============================================================

-- Daily Trends
SELECT 
    dd.date_key,
    dd.day_name,
    COUNT(*) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk,
    AVG(ft.amount) AS avg_amount_mwk
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
GROUP BY dd.date_key, dd.day_name
ORDER BY dd.date_key DESC
LIMIT 30;

-- Weekly Trends
SELECT 
    dd.year,
    dd.week,
    COUNT(*) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk,
    AVG(ft.amount) AS avg_amount_mwk,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) AS deposits_mwk,
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS withdrawals_mwk
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
GROUP BY dd.year, dd.week
ORDER BY dd.year DESC, dd.week DESC;

-- Monthly Trends
SELECT 
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(*) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk,
    AVG(ft.amount) AS avg_amount_mwk,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) AS deposits_mwk,
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS withdrawals_mwk
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year DESC, dd.month DESC;

-- ============================================================
-- 3. TOP 10 CUSTOMERS BY TRANSACTION VOLUME
-- ============================================================
SELECT 
    dc.customer_id,
    dc.name,
    dc.city,
    COUNT(*) AS transaction_count,
    SUM(ft.amount) AS total_transaction_amount_mwk,
    AVG(ft.amount) AS avg_transaction_amount_mwk,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) AS total_deposits_mwk,
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS total_withdrawals_mwk
FROM fact_transactions ft
JOIN dim_account da ON ft.account_id = da.account_id
JOIN dim_customer dc ON da.customer_id = dc.customer_id
GROUP BY dc.customer_id, dc.name, dc.city
ORDER BY total_transaction_amount_mwk DESC
LIMIT 10;

-- ============================================================
-- 4. RISKY TRANSACTIONS (WITHDRAWALS > MWK 500,000)
-- ============================================================
SELECT 
    ft.transaction_id,
    ft.date_key,
    dc.customer_id,
    dc.name AS customer_name,
    db.branch_name,
    db.city AS branch_city,
    ft.transaction_type,
    ft.amount AS amount_mwk,
    ft.day_of_week
FROM fact_transactions ft
JOIN dim_account da ON ft.account_id = da.account_id
JOIN dim_customer dc ON da.customer_id = dc.customer_id
JOIN dim_branch db ON da.branch_id = db.branch_id
WHERE ft.risk_flag = 1
ORDER BY ft.amount DESC, ft.date_key DESC;

-- Summary of risky transactions
SELECT 
    COUNT(*) AS risky_transaction_count,
    SUM(ft.amount) AS total_risky_amount_mwk,
    AVG(ft.amount) AS avg_risky_amount_mwk,
    MIN(ft.amount) AS min_risky_amount_mwk,
    MAX(ft.amount) AS max_risky_amount_mwk
FROM fact_transactions ft
WHERE ft.risk_flag = 1;

-- Risky transactions by branch
SELECT 
    db.branch_name,
    db.city,
    COUNT(*) AS risky_transaction_count,
    SUM(ft.amount) AS total_risky_amount_mwk
FROM fact_transactions ft
JOIN dim_account da ON ft.account_id = da.account_id
JOIN dim_branch db ON da.branch_id = db.branch_id
WHERE ft.risk_flag = 1
GROUP BY db.branch_id, db.branch_name, db.city
ORDER BY risky_transaction_count DESC;

-- ============================================================
-- 5. BRANCH PERFORMANCE RANKING
-- ============================================================
SELECT 
    db.branch_id,
    db.branch_name,
    db.city,
    COUNT(DISTINCT da.customer_id) AS customer_count,
    COUNT(DISTINCT da.account_id) AS account_count,
    COUNT(ft.transaction_id) AS total_transactions,
    SUM(CASE WHEN ft.transaction_type = 'deposit' THEN ft.amount ELSE 0 END) AS total_deposits_mwk,
    SUM(CASE WHEN ft.transaction_type = 'withdrawal' THEN ft.amount ELSE 0 END) AS total_withdrawals_mwk,
    SUM(ft.amount) AS total_transaction_volume_mwk,
    AVG(ft.amount) AS avg_transaction_amount_mwk,
    COUNT(CASE WHEN ft.risk_flag = 1 THEN 1 END) AS risky_transaction_count,
    RANK() OVER (ORDER BY SUM(ft.amount) DESC) AS performance_rank
FROM dim_branch db
LEFT JOIN dim_account da ON db.branch_id = da.branch_id
LEFT JOIN fact_transactions ft ON da.account_id = ft.account_id
GROUP BY db.branch_id, db.branch_name, db.city
ORDER BY performance_rank;

-- ============================================================
-- 6. ADDITIONAL INSIGHTS
-- ============================================================

-- Account type distribution
SELECT 
    da.account_type,
    COUNT(DISTINCT da.account_id) AS account_count,
    COUNT(ft.transaction_id) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk
FROM dim_account da
LEFT JOIN fact_transactions ft ON da.account_id = ft.account_id
GROUP BY da.account_type;

-- Customer demographics analysis
SELECT 
    dc.gender,
    CASE 
        WHEN dc.age < 30 THEN '18-29'
        WHEN dc.age < 40 THEN '30-39'
        WHEN dc.age < 50 THEN '40-49'
        WHEN dc.age < 60 THEN '50-59'
        ELSE '60+'
    END AS age_group,
    COUNT(DISTINCT dc.customer_id) AS customer_count,
    COUNT(ft.transaction_id) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk
FROM dim_customer dc
LEFT JOIN dim_account da ON dc.customer_id = da.customer_id
LEFT JOIN fact_transactions ft ON da.account_id = ft.account_id
GROUP BY dc.gender, age_group
ORDER BY dc.gender, age_group;

-- Peak transaction days
SELECT 
    dd.day_name,
    COUNT(*) AS transaction_count,
    SUM(ft.amount) AS total_amount_mwk,
    AVG(ft.amount) AS avg_amount_mwk
FROM fact_transactions ft
JOIN dim_date dd ON ft.date_key = dd.date_key
GROUP BY dd.day_name, dd.day_of_week
ORDER BY dd.day_of_week;

