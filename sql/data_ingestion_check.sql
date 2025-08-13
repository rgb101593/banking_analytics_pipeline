-- --- Basic Counts & Samples ---
-- Confirm final row counts match expectations (roughly)
SELECT COUNT(*) AS customer_count FROM customers;
SELECT COUNT(*) AS account_count FROM accounts;
SELECT COUNT(*) AS transaction_count FROM transactions;

-- Check a sample of data from each table
SELECT * FROM customers LIMIT 5;
SELECT * FROM accounts LIMIT 5;
SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 5; -- See recent

-- --- Data Integrity & Quality Checks ---
-- Check for unexpected NULLs in critical columns
SELECT 'customers' AS table_name, 'customer_id' AS column_name, COUNT(*) AS null_count FROM customers WHERE customer_id IS NULL
UNION ALL
SELECT 'accounts', 'account_id', COUNT(*) FROM accounts WHERE account_id IS NULL
UNION ALL
SELECT 'transactions', 'transaction_id', COUNT(*) FROM transactions WHERE transaction_id IS NULL
UNION ALL
SELECT 'transactions', 'account_id', COUNT(*) FROM transactions WHERE account_id IS NULL
UNION ALL
SELECT 'transactions', 'transaction_date', COUNT(*) FROM transactions WHERE transaction_date IS NULL;

-- Check distinct values and potential anomalies in categorical columns
SELECT account_type, COUNT(*) AS count FROM accounts GROUP BY account_type ORDER BY count DESC;
SELECT transaction_type, COUNT(*) AS count FROM transactions GROUP BY transaction_type ORDER BY count DESC;
-- Check for any unexpected merchant category codes (should mostly be 4 digits or '0000')
SELECT merchant_category_code, COUNT(*) AS count FROM transactions GROUP BY merchant_category_code ORDER BY count DESC LIMIT 10;

-- --- Basic Data Profiling ---
-- Summary statistics for numerical columns (using SQL)
SELECT
  COUNT(amount) AS count,
  AVG(amount) AS average,
  MIN(amount) AS minimum,
  MAX(amount) AS maximum,
  STDDEV(amount) AS stddev
FROM transactions;

-- Date range check
SELECT MIN(transaction_date) AS earliest_date, MAX(transaction_date) AS latest_date FROM transactions;

-- --- Relationship Checks (Basic) ---
-- Ensure account_ids in transactions exist in accounts (basic simulation, DB FKs are better)
SELECT COUNT(*) AS orphaned_transactions
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

-- Ensure customer_ids in accounts exist in customers (basic simulation)
SELECT COUNT(*) AS orphaned_accounts
FROM accounts a
LEFT JOIN customers c ON a.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
