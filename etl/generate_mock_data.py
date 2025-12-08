"""
Mock Data Generation Script for First Capital Bank Insights BI System
Generates realistic customer, branch, account, and transaction data
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker with Malawi locale
fake = Faker(['en_US'])
Faker.seed(42)
random.seed(42)

# Malawi cities and branches
BRANCHES = [
    {'branch_id': 1, 'branch_name': 'Lilongwe Main', 'city': 'Lilongwe'},
    {'branch_id': 2, 'branch_name': 'Blantyre Central', 'city': 'Blantyre'},
    {'branch_id': 3, 'branch_name': 'Mzuzu Branch', 'city': 'Mzuzu'},
    {'branch_id': 4, 'branch_name': 'Zomba Branch', 'city': 'Zomba'},
    {'branch_id': 5, 'branch_name': 'Mangochi Branch', 'city': 'Mangochi'}
]

CITIES = ['Lilongwe', 'Blantyre', 'Mzuzu', 'Zomba', 'Mangochi']
ACCOUNT_TYPES = ['savings', 'current']
TRANSACTION_TYPES = ['deposit', 'withdrawal', 'transfer']

def generate_customers(n=200):
    """Generate customer data"""
    customers = []
    for i in range(1, n + 1):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            name = fake.name_male()
        else:
            name = fake.name_female()
        
        customers.append({
            'customer_id': i,
            'name': name,
            'gender': gender,
            'age': random.randint(18, 75),
            'city': random.choice(CITIES),
            'join_date': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(customers)

def generate_branches():
    """Generate branch data"""
    return pd.DataFrame(BRANCHES)

def generate_accounts(n=300, n_customers=200):
    """Generate account data"""
    accounts = []
    account_id = 1
    
    # Ensure each customer has at least one account
    for customer_id in range(1, n_customers + 1):
        accounts.append({
            'account_id': account_id,
            'customer_id': customer_id,
            'branch_id': random.choice([1, 2, 3, 4, 5]),
            'account_type': random.choice(ACCOUNT_TYPES),
            'open_date': fake.date_between(start_date='-4y', end_date='today').strftime('%Y-%m-%d')
        })
        account_id += 1
    
    # Add additional accounts for some customers
    while account_id <= n:
        accounts.append({
            'account_id': account_id,
            'customer_id': random.randint(1, n_customers),
            'branch_id': random.choice([1, 2, 3, 4, 5]),
            'account_type': random.choice(ACCOUNT_TYPES),
            'open_date': fake.date_between(start_date='-4y', end_date='today').strftime('%Y-%m-%d')
        })
        account_id += 1
    
    return pd.DataFrame(accounts)

def generate_transactions(n=3000, n_accounts=300):
    """Generate transaction data"""
    transactions = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, n + 1):
        account_id = random.randint(1, n_accounts)
        trans_type = random.choice(TRANSACTION_TYPES)
        
        # Realistic amounts in MWK
        if trans_type == 'deposit':
            amount = random.randint(5000, 2000000)  # 5,000 to 2,000,000 MWK
        elif trans_type == 'withdrawal':
            amount = random.randint(10000, 1000000)  # 10,000 to 1,000,000 MWK
        else:  # transfer
            amount = random.randint(5000, 500000)  # 5,000 to 500,000 MWK
        
        # Random date within last year
        days_ago = random.randint(0, 365)
        trans_date = (start_date + timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        transactions.append({
            'transaction_id': i,
            'account_id': account_id,
            'date': trans_date,
            'type': trans_type,
            'amount': amount
        })
    
    return pd.DataFrame(transactions)

def main():
    """Main function to generate all datasets"""
    print("Generating mock data for First Capital Bank...")
    
    # Create output directory
    os.makedirs('../data/raw', exist_ok=True)
    
    # Generate datasets
    print("Generating customers...")
    customers_df = generate_customers(200)
    customers_df.to_csv('../data/raw/customers.csv', index=False)
    print(f"✓ Generated {len(customers_df)} customers")
    
    print("Generating branches...")
    branches_df = generate_branches()
    branches_df.to_csv('../data/raw/branches.csv', index=False)
    print(f"✓ Generated {len(branches_df)} branches")
    
    print("Generating accounts...")
    accounts_df = generate_accounts(300, 200)
    accounts_df.to_csv('../data/raw/accounts.csv', index=False)
    print(f"✓ Generated {len(accounts_df)} accounts")
    
    print("Generating transactions...")
    transactions_df = generate_transactions(3000, 300)
    transactions_df.to_csv('../data/raw/transactions.csv', index=False)
    print(f"✓ Generated {len(transactions_df)} transactions")
    
    print("\n✅ All mock data generated successfully!")
    print("Files saved to: data/raw/")

if __name__ == '__main__':
    main()

