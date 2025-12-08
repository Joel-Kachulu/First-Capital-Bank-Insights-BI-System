-- ============================================================
-- FIRST CAPITAL BANK INSIGHTS BI SYSTEM
-- Star Schema Data Model Creation Script
-- ============================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_account;
DROP TABLE IF EXISTS dim_branch;
DROP TABLE IF EXISTS dim_date;

-- ============================================================
-- DIMENSION TABLES
-- ============================================================

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(20),
    age INT,
    city VARCHAR(100),
    join_date DATE
);

-- Dimension: Account
CREATE TABLE dim_account (
    account_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_type VARCHAR(50),
    open_date DATE,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (branch_id) REFERENCES dim_branch(branch_id)
);

-- Dimension: Branch
CREATE TABLE dim_branch (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    city VARCHAR(100)
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN
);

-- ============================================================
-- FACT TABLE
-- ============================================================

-- Fact: Transactions
CREATE TABLE fact_transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    date_key DATE NOT NULL,
    transaction_type VARCHAR(50),
    amount DECIMAL(15, 2),
    transaction_month VARCHAR(10),
    risk_flag INT,
    day_of_week VARCHAR(20),
    week INT,
    FOREIGN KEY (account_id) REFERENCES dim_account(account_id),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX idx_fact_account ON fact_transactions(account_id);
CREATE INDEX idx_fact_date ON fact_transactions(date_key);
CREATE INDEX idx_fact_type ON fact_transactions(transaction_type);
CREATE INDEX idx_fact_risk ON fact_transactions(risk_flag);
CREATE INDEX idx_dim_account_customer ON dim_account(customer_id);
CREATE INDEX idx_dim_account_branch ON dim_account(branch_id);

-- ============================================================
-- COMMENTS
-- ============================================================

COMMENT ON TABLE dim_customer IS 'Customer dimension table';
COMMENT ON TABLE dim_account IS 'Account dimension table';
COMMENT ON TABLE dim_branch IS 'Branch dimension table';
COMMENT ON TABLE dim_date IS 'Date dimension table for time-based analysis';
COMMENT ON TABLE fact_transactions IS 'Transaction fact table with measures and foreign keys';

