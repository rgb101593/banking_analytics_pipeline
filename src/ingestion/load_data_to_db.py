from __future__ import annotations

# src/ingestion/load_data_to_db.py
"""
Script to load generated CSV data into the PostgreSQL database tables.
Uses pandas and SQLAlchemy (with psycopg3) for efficient data transfer.
Includes sys.path modification to resolve 'src' import issues when run directly.
"""

# --- START OF PATH MODIFICATION ---
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- END OF PATH MODIFICATION ---

import logging
from pathlib import Path
from typing import Tuple, List

import pandas as pd
from sqlalchemy.engine import Engine

# Import our connection utility
from src.database.db_connection import get_database_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
RAW_DATA_DIR: Path = Path("data/raw")
CHUNK_SIZE: int = 5000 # Reduced chunk size for better error isolation
TABLES_LOAD_ORDER: List[str] = ["customers", "accounts", "transactions"]

def load_csv_to_table(csv_file_path: Path, table_name: str, engine: Engine, if_exists: str = 'append') -> None:
    """
    Loads data from a CSV file into a specified database table.
    """
    if not csv_file_path.exists():
        logger.error(f"CSV file not found: {csv_file_path}")
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    logger.info(f"Loading data from {csv_file_path} into table '{table_name}' (mode: {if_exists})...")

    try:
        parse_dates_cols = []
        if table_name == 'customers':
            parse_dates_cols = ['account_open_date']
        elif table_name == 'transactions':
            parse_dates_cols = ['transaction_date']

        # Read CSV in chunks with explicit date parsing
        # low_memory=False can help with dtype inference on large files
        chunk_iter = pd.read_csv(
            csv_file_path,
            chunksize=CHUNK_SIZE,
            parse_dates=parse_dates_cols,
            low_memory=False
        )

        rows_loaded = 0
        for i, chunk in enumerate(chunk_iter, 1):
            logger.debug(f"Loading chunk {i} of '{table_name}' (size: {len(chunk)})...")
            
            # --- CRITICAL FIXES BEFORE INSERTION ---
            
            # 1. Ensure date columns are datetime64
            for date_col in parse_dates_cols:
                if date_col in chunk.columns:
                    chunk[date_col] = pd.to_datetime(chunk[date_col], errors='coerce')

            # 2. Explicitly handle merchant_category_code to prevent any numeric issues
            if 'merchant_category_code' in chunk.columns:
                # Force to string, handling potential NaNs if any slipped through
                chunk['merchant_category_code'] = chunk['merchant_category_code'].fillna('0000').astype(str)
                # Optional: Add explicit validation/check for suspiciously short codes
                # Though the generation script should prevent this now.

            # 3. Ensure other critical string columns are object dtype
            critical_string_cols = ['transaction_id', 'account_id', 'transaction_type', 'description']
            for col in critical_string_cols:
                if col in chunk.columns:
                     chunk[col] = chunk[col].astype('object')

            logger.debug(f"Chunk {i} dtypes after pre-processing:\n{chunk.dtypes}")
            # logger.debug(f"Chunk {i} sample:\n{chunk.head()}") # Uncomment for detailed debugging

            try:
                # Load chunk to database
                # Specifying dtype for merchant_category_code explicitly might help, 
                # though pre-processing should be sufficient.
                # dtype={'merchant_category_code': 'str'} could be added to to_sql if needed.
                chunk.to_sql(table_name, con=engine, if_exists=if_exists, index=False, method='multi')
                rows_loaded += len(chunk)
                logger.debug(f"Chunk {i} loaded successfully.")
            except Exception as chunk_error:
                logger.error(f"Error loading chunk {i} into '{table_name}': {chunk_error}", exc_info=True)
                # Log the problematic chunk data for inspection
                logger.error(f"Problematic chunk {i} data sample:\n{chunk.head()}")
                logger.error(f"Problematic chunk {i} dtypes:\n{chunk.dtypes}")
                raise # Re-raise to stop the process for this table

        logger.info(f"Data loading completed for '{table_name}'. Total rows loaded: {rows_loaded}")

    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error during loading process for '{table_name}': {e}", exc_info=True)
        raise

def get_files_and_tables() -> List[Tuple[Path, str]]:
    """Defines the mapping between CSV files and database tables."""
    return [
        (RAW_DATA_DIR / "customers.csv", "customers"),
        (RAW_DATA_DIR / "accounts.csv", "accounts"),
        (RAW_DATA_DIR / "transactions.csv", "transactions"),
    ]

def main() -> None:
    """Main function to orchestrate the data loading process."""
    logger.info("Starting data loading process...")
    try:
        engine = get_database_engine()
        logger.info("Database engine acquired.")

        files_and_tables = get_files_and_tables()

        for csv_file_path, table_name in files_and_tables:
            # Use 'replace' to ensure a clean state for each run
            load_csv_to_table(csv_file_path, table_name, engine, if_exists='replace')

        logger.info("All data loading processes completed successfully.")

    except Exception as e:
        logger.critical(f"An unrecoverable error occurred during the data loading process: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
