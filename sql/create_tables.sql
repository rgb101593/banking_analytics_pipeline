CREATE TYPE account_type_enum AS ENUM ('Savings', 'Checking', 'Credit');
CREATE TYPE transaction_type_enum AS ENUM ('Deposit', 'Withdrawal', 'Transfer_In', 'Transfer_Out', 'Payment');

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    region VARCHAR(50), -- e.g., Qatar_North, Qatar_South, Doha_Central
    account_open_date DATE NOT NULL
);

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL REFERENCES customers(customer_id),
    account_type account_type_enum NOT NULL, -- Using the enum type
    balance NUMERIC(15, 2) DEFAULT 0.00 CHECK (balance >= 0) -- Basic integrity check
);

-- Transactions table (Core Transactional Data)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL REFERENCES accounts(account_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type transaction_type_enum NOT NULL, -- Using the enum type
    amount NUMERIC(15, 2) NOT NULL CHECK (amount > 0), -- Basic integrity check
    description TEXT,
    merchant_category_code VARCHAR(10) -- Behavioral data element (e.g., '5411' for Grocery Stores)
);

-- Indexes for performance on large datasets (advanced)
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id);

-- Comments for clarity
COMMENT ON TABLE transactions IS 'Core banking transaction log';
COMMENT ON COLUMN transactions.merchant_category_code IS 'MCC code for categorizing spending behavior';
COMMENT ON COLUMN accounts.balance IS 'Current account balance (assumed to be updated periodically)';