# src/ingestion/generate_sample_data.py
"""
Script to generate sample banking data (customers, accounts, transactions)
and save it as CSV files in the data/raw directory.
Includes sys.path modification to resolve 'src' import issues when run directly.
"""

# --- START OF PATH MODIFICATION ---
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- END OF PATH MODIFICATION ---

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
from pathlib import Path

# --- Configuration ---
NUM_CUSTOMERS = 500
NUM_ACCOUNTS_PER_CUSTOMER = 1.5
NUM_TRANSACTIONS_PER_ACCOUNT_PER_MONTH = 10
MONTHS_OF_DATA = 12
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Helper Functions ---
def generate_customer_data(n_customers):
    """Generate sample customer data."""
    regions = ['Qatar_North', 'Qatar_South', 'Qatar_East', 'Qatar_West', 'Doha_Central']
    start_date = datetime.now() - timedelta(days=365*3)
    end_date = datetime.now() - timedelta(days=30)

    customers = []
    for i in range(1, n_customers + 1):
        customer_id = f"CUST_{i:05d}"
        customer_name = f"Customer {i}"
        region = random.choice(regions)
        account_open_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        customers.append({
            'customer_id': customer_id,
            'customer_name': customer_name,
            'region': region,
            'account_open_date': account_open_date.date()
        })
    return pd.DataFrame(customers)

def generate_account_data(customer_df, avg_accounts_per_customer):
    """Generate sample account data linked to customers."""
    account_types = ['Savings', 'Checking', 'Credit']
    accounts = []
    account_counter = 1

    for _, customer in customer_df.iterrows():
        num_accounts = max(1, int(np.random.normal(avg_accounts_per_customer, 0.7)))
        for _ in range(num_accounts):
            account_id = f"ACC_{account_counter:07d}"
            customer_id = customer['customer_id']
            account_type = random.choices(account_types, weights=[0.5, 0.4, 0.1])[0]
            if account_type == 'Savings':
                base_balance = np.random.lognormal(mean=9, sigma=0.8)
            elif account_type == 'Checking':
                base_balance = np.random.lognormal(mean=8, sigma=1.0)
            else: # Credit
                base_balance = -np.random.lognormal(mean=7, sigma=1.2)
            balance = round(max(0, base_balance) if account_type != 'Credit' else base_balance, 2)

            accounts.append({
                'account_id': account_id,
                'customer_id': customer_id,
                'account_type': account_type,
                'balance': balance
            })
            account_counter += 1
    return pd.DataFrame(accounts)

def generate_transaction_data(account_df, months_of_data, avg_txns_per_account_per_month):
    """Generate sample transaction data linked to accounts."""
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer_In', 'Transfer_Out', 'Payment']
    # Ensure all MCC codes are explicitly strings
    mcc_codes = {
        'Grocery': '5411', 'Gas_Station': '5541', 'Restaurant': '5812',
        'Online_Retail': '5964', 'Entertainment': '7996', 'ATM_Withdrawal': '6010',
        'Transfer': '6012', 'Service_Payment': '4814', 'Unknown': '0000'
    }
    txn_probs = {
        'Savings': {'Deposit': 0.4, 'Withdrawal': 0.2, 'Transfer_In': 0.15, 'Transfer_Out': 0.15, 'Payment': 0.1},
        'Checking': {'Deposit': 0.2, 'Withdrawal': 0.3, 'Transfer_In': 0.1, 'Transfer_Out': 0.1, 'Payment': 0.3},
        'Credit': {'Deposit': 0.1, 'Withdrawal': 0.05, 'Transfer_In': 0.05, 'Transfer_Out': 0.05, 'Payment': 0.75}
    }

    transactions = []
    txn_counter = 1

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months_of_data)

    for _, account in account_df.iterrows():
        account_id = account['account_id']
        account_type = account['account_type']
        account_balance = account['balance']

        total_txns = int(np.random.normal(avg_txns_per_account_per_month * months_of_data, 3))
        total_txns = max(5, total_txns)

        txn_dates = [start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        ) for _ in range(total_txns)]
        txn_dates.sort()

        running_balance = account_balance
        for txn_date in txn_dates:
            txn_id = f"TXN_{txn_counter:010d}"

            txn_type = random.choices(
                list(txn_probs[account_type].keys()),
                weights=list(txn_probs[account_type].values())
            )[0]

            if txn_type in ['Deposit', 'Transfer_In']:
                amount = round(np.random.lognormal(mean=6, sigma=1.2), 2)
            elif txn_type in ['Withdrawal', 'Transfer_Out', 'Payment']:
                max_outflow = max(10, running_balance * 0.5) if running_balance > 0 else 1000
                amount = round(min(max_outflow, np.random.lognormal(mean=5.5, sigma=1.3)), 2)
                amount = max(1.0, amount)
            else: # Fallback (shouldn't happen with current txn_probs)
                 amount = round(np.random.lognormal(mean=5, sigma=1.0), 2)

            if txn_type in ['Deposit', 'Transfer_In']:
                running_balance += amount
            elif txn_type in ['Withdrawal', 'Transfer_Out', 'Payment']:
                running_balance -= amount

            # --- CORRECTED LOGIC ORDER ---
            # Assign MCC code based on transaction type (simplified)
            # The 'Payment' check MUST come before the 'else: # Deposit' block
            if txn_type == 'Withdrawal':
                mcc_desc = 'ATM_Withdrawal'
            elif txn_type in ['Transfer_In', 'Transfer_Out']:
                mcc_desc = 'Transfer'
            elif txn_type == 'Payment': # <-- This was misplaced before
                 mcc_desc = random.choices(
                    ['Grocery', 'Gas_Station', 'Restaurant', 'Online_Retail', 'Entertainment', 'Service_Payment'],
                    weights=[0.2, 0.15, 0.2, 0.2, 0.1, 0.15]
                )[0]
            else: # This now correctly handles only 'Deposit'
                mcc_desc = 'Unknown' # Deposits often don't have MCC

            # --- ROBUST MCC HANDLING ---
            # Get the code string from the dictionary
            raw_mcc_code = mcc_codes.get(mcc_desc, '0000') # Default to '0000' string
            # Ensure it's a string and explicitly pad/convert if necessary
            # This should prevent any numeric coercion issues
            merchant_category_code = f"{raw_mcc_code}" # f-string ensures string type

            description = f"{txn_type.replace('_', ' ')} at {mcc_desc.replace('_', ' ')}"

            # Append transaction data with guaranteed string types for critical fields
            transactions.append({
                'transaction_id': txn_id,
                'account_id': account_id,
                'transaction_date': txn_date,
                'transaction_type': txn_type,
                'amount': amount,
                'merchant_category_code': merchant_category_code, # Guaranteed string
                'description': description
            })
            txn_counter += 1

    df_transactions = pd.DataFrame(transactions)
    
    # --- FINAL SAFETY: Ensure column dtype is object (string) ---
    # Explicitly convert critical string columns
    string_cols = ['transaction_id', 'account_id', 'transaction_type', 'merchant_category_code', 'description']
    for col in string_cols:
        if col in df_transactions.columns:
            df_transactions[col] = df_transactions[col].astype('object') # 'object' is pandas string type
    
    # Ensure date column is datetime
    df_transactions['transaction_date'] = pd.to_datetime(df_transactions['transaction_date'])
    
    return df_transactions

# --- Main Execution ---
if __name__ == "__main__":
    print("Generating sample customer data...")
    df_customers = generate_customer_data(NUM_CUSTOMERS)
    customer_file = RAW_DATA_DIR / "customers.csv"
    df_customers.to_csv(customer_file, index=False)
    print(f"Saved customer data to {customer_file}")

    print("Generating sample account data...")
    df_accounts = generate_account_data(df_customers, NUM_ACCOUNTS_PER_CUSTOMER)
    account_file = RAW_DATA_DIR / "accounts.csv"
    df_accounts.to_csv(account_file, index=False)
    print(f"Saved account data to {account_file}")

    print("Generating sample transaction data...")
    df_transactions = generate_transaction_data(df_accounts, MONTHS_OF_DATA, NUM_TRANSACTIONS_PER_ACCOUNT_PER_MONTH)
    
    print("Transaction DataFrame dtypes before saving:")
    print(df_transactions.dtypes)
    print("Sample transaction data:")
    print(df_transactions.head())
    
    transaction_file = RAW_DATA_DIR / "transactions.csv"
    # Save with date_format to ensure consistent format in CSV
    df_transactions.to_csv(transaction_file, index=False, date_format='%Y-%m-%d %H:%M:%S')
    print(f"Saved transaction data to {transaction_file}")

    print("Data generation complete.")
