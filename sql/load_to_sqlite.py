"""
Helper script to load cleaned CSV data into SQLite database
Useful for testing and portfolio demonstration
"""

import sqlite3
import pandas as pd
import os

def create_sqlite_database():
    """Create SQLite database and load star schema"""
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect('../data/first_capital_bank.db')
    cursor = conn.cursor()
    
    print("Creating star schema tables...")
    
    # Read SQL schema file
    with open('01_create_star_schema.sql', 'r') as f:
        sql_script = f.read()
    
    # SQLite doesn't support all PostgreSQL syntax, so we'll create simplified version
    # Drop tables if exist
    cursor.execute("DROP TABLE IF EXISTS fact_transactions")
    cursor.execute("DROP TABLE IF EXISTS dim_account")
    cursor.execute("DROP TABLE IF EXISTS dim_customer")
    cursor.execute("DROP TABLE IF EXISTS dim_branch")
    cursor.execute("DROP TABLE IF EXISTS dim_date")
    
    # Create dimension tables
    cursor.execute("""
        CREATE TABLE dim_customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            city TEXT,
            join_date TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE dim_branch (
            branch_id INTEGER PRIMARY KEY,
            branch_name TEXT NOT NULL,
            city TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE dim_account (
            account_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            account_type TEXT,
            open_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY (branch_id) REFERENCES dim_branch(branch_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE dim_date (
            date_key TEXT PRIMARY KEY,
            year INTEGER,
            quarter INTEGER,
            month INTEGER,
            month_name TEXT,
            week INTEGER,
            day_of_week INTEGER,
            day_name TEXT,
            is_weekend INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE fact_transactions (
            transaction_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            date_key TEXT NOT NULL,
            transaction_type TEXT,
            amount REAL,
            transaction_month TEXT,
            risk_flag INTEGER,
            day_of_week TEXT,
            week INTEGER,
            FOREIGN KEY (account_id) REFERENCES dim_account(account_id),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
        )
    """)
    
    print("✓ Tables created")
    
    # Load data from CSV files
    print("\nLoading data from CSV files...")
    
    # Load customers
    customers_df = pd.read_csv('../data/clean/customers.csv')
    customers_df.to_sql('dim_customer', conn, if_exists='append', index=False)
    print(f"✓ Loaded {len(customers_df)} customers")
    
    # Load branches
    branches_df = pd.read_csv('../data/clean/branches.csv')
    branches_df.to_sql('dim_branch', conn, if_exists='append', index=False)
    print(f"✓ Loaded {len(branches_df)} branches")
    
    # Load accounts
    accounts_df = pd.read_csv('../data/clean/accounts.csv')
    accounts_df.to_sql('dim_account', conn, if_exists='append', index=False)
    print(f"✓ Loaded {len(accounts_df)} accounts")
    
    # Generate and load date dimension
    from datetime import datetime, timedelta
    dates = []
    start_date = datetime.now() - timedelta(days=730)  # 2 years
    for i in range(730):
        date = start_date + timedelta(days=i)
        dates.append({
            'date_key': date.strftime('%Y-%m-%d'),
            'year': date.year,
            'quarter': (date.month - 1) // 3 + 1,
            'month': date.month,
            'month_name': date.strftime('%B'),
            'week': date.isocalendar()[1],
            'day_of_week': date.weekday(),
            'day_name': date.strftime('%A'),
            'is_weekend': 1 if date.weekday() >= 5 else 0
        })
    
    dates_df = pd.DataFrame(dates)
    dates_df.to_sql('dim_date', conn, if_exists='append', index=False)
    print(f"✓ Generated {len(dates_df)} date records")
    
    # Load transactions
    transactions_df = pd.read_csv('../data/clean/transactions.csv')
    # Map 'date' column to 'date_key' and 'type' to 'transaction_type'
    transactions_df = transactions_df.rename(columns={'date': 'date_key', 'type': 'transaction_type'})
    transactions_df.to_sql('fact_transactions', conn, if_exists='append', index=False)
    print(f"✓ Loaded {len(transactions_df)} transactions")
    
    # Create indexes
    print("\nCreating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_account ON fact_transactions(account_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_transactions(date_key)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_type ON fact_transactions(transaction_type)")
    print("✓ Indexes created")
    
    # Verify data
    print("\n" + "=" * 60)
    print("Data Verification:")
    print("=" * 60)
    for table in ['dim_customer', 'dim_branch', 'dim_account', 'dim_date', 'fact_transactions']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ SQLite database created successfully!")
    print("=" * 60)
    print(f"Database location: data/first_capital_bank.db")
    print("\nYou can now query the database using SQLite or connect Power BI to it.")

if __name__ == '__main__':
    # Check if cleaned data exists
    if not os.path.exists('../data/clean/customers.csv'):
        print("❌ Error: Cleaned data not found!")
        print("Please run the ETL pipeline first:")
        print("  python ../run_pipeline.py")
        exit(1)
    
    create_sqlite_database()

