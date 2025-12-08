"""
ETL Pipeline for First Capital Bank Insights BI System
Loads raw CSV files, cleans data, and saves to clean folder
"""

import pandas as pd
import os
from datetime import datetime

def load_raw_data():
    """Load all raw CSV files"""
    print("Loading raw data files...")
    
    customers = pd.read_csv('../data/raw/customers.csv')
    branches = pd.read_csv('../data/raw/branches.csv')
    accounts = pd.read_csv('../data/raw/accounts.csv')
    transactions = pd.read_csv('../data/raw/transactions.csv')
    
    print("✓ All raw files loaded")
    return customers, branches, accounts, transactions

def clean_column_names(df):
    """Standardize column names to lowercase with underscores"""
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

def clean_customers(df):
    """Clean customer data"""
    print("Cleaning customers data...")
    df = clean_column_names(df)
    
    # Handle missing values
    df['name'] = df['name'].fillna('Unknown')
    df['gender'] = df['gender'].fillna('Unknown')
    df['age'] = df['age'].fillna(df['age'].median())
    df['city'] = df['city'].fillna('Unknown')
    
    # Standardize date format
    df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
    df['join_date'] = df['join_date'].dt.strftime('%Y-%m-%d')
    
    # Ensure age is reasonable
    df['age'] = df['age'].clip(lower=18, upper=100)
    
    print(f"✓ Cleaned {len(df)} customer records")
    return df

def clean_branches(df):
    """Clean branch data"""
    print("Cleaning branches data...")
    df = clean_column_names(df)
    
    # Handle missing values
    df['branch_name'] = df['branch_name'].fillna('Unknown Branch')
    df['city'] = df['city'].fillna('Unknown')
    
    print(f"✓ Cleaned {len(df)} branch records")
    return df

def clean_accounts(df):
    """Clean account data"""
    print("Cleaning accounts data...")
    df = clean_column_names(df)
    
    # Handle missing values
    df['account_type'] = df['account_type'].fillna('savings')
    df['branch_id'] = df['branch_id'].fillna(1)
    
    # Standardize account type
    df['account_type'] = df['account_type'].str.lower()
    df['account_type'] = df['account_type'].replace({
        'savings': 'savings',
        'current': 'current',
        'checking': 'current'
    })
    
    # Standardize date format
    df['open_date'] = pd.to_datetime(df['open_date'], errors='coerce')
    df['open_date'] = df['open_date'].dt.strftime('%Y-%m-%d')
    
    print(f"✓ Cleaned {len(df)} account records")
    return df

def clean_transactions(df):
    """Clean transaction data and add calculated fields"""
    print("Cleaning transactions data...")
    df = clean_column_names(df)
    
    # Handle missing values
    df['type'] = df['type'].fillna('deposit')
    df['amount'] = df['amount'].fillna(0)
    
    # Standardize transaction type
    df['type'] = df['type'].str.lower()
    df['type'] = df['type'].replace({
        'deposit': 'deposit',
        'withdrawal': 'withdrawal',
        'withdraw': 'withdrawal',
        'transfer': 'transfer'
    })
    
    # Standardize date format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['transaction_month'] = df['date'].dt.to_period('M').astype(str)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Ensure amount is positive
    df['amount'] = df['amount'].abs()
    
    # Add risk flag: withdrawals > MWK 500,000
    df['risk_flag'] = ((df['type'] == 'withdrawal') & (df['amount'] > 500000)).astype(int)
    
    # Add transaction day of week
    df['date_dt'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date_dt'].dt.day_name()
    df['week'] = df['date_dt'].dt.isocalendar().week
    df = df.drop('date_dt', axis=1)
    
    print(f"✓ Cleaned {len(df)} transaction records")
    print(f"  - Risk-flagged transactions: {df['risk_flag'].sum()}")
    return df

def save_clean_data(customers, branches, accounts, transactions):
    """Save cleaned data to clean folder"""
    print("\nSaving cleaned data...")
    
    os.makedirs('../data/clean', exist_ok=True)
    
    customers.to_csv('../data/clean/customers.csv', index=False)
    branches.to_csv('../data/clean/branches.csv', index=False)
    accounts.to_csv('../data/clean/accounts.csv', index=False)
    transactions.to_csv('../data/clean/transactions.csv', index=False)
    
    print("✓ All cleaned files saved to data/clean/")

def main():
    """Main ETL pipeline function"""
    print("=" * 60)
    print("FIRST CAPITAL BANK - ETL PIPELINE")
    print("=" * 60)
    print()
    
    # Load raw data
    customers, branches, accounts, transactions = load_raw_data()
    
    # Clean data
    customers_clean = clean_customers(customers)
    branches_clean = clean_branches(branches)
    accounts_clean = clean_accounts(accounts)
    transactions_clean = clean_transactions(transactions)
    
    # Save cleaned data
    save_clean_data(customers_clean, branches_clean, accounts_clean, transactions_clean)
    
    print("\n" + "=" * 60)
    print("✅ ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

if __name__ == '__main__':
    main()

