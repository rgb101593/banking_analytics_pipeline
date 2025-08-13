# Banking Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A comprehensive data engineering and analytics project demonstrating skills relevant to financial data roles. This repository implements a data pipeline using Dockerized PostgreSQL for storage, showcasing advanced SQL for data extraction and transformation on simulated banking data. Python (Pandas, SQLAlchemy) is used for data processing, feature engineering, and validation. The project emphasizes clean, efficient code, reproducibility, and high data integrity.

**This project directly addresses key requirements for Data Analyst/Engineer roles involving large-scale data handling in the banking sector.**

## 🚀 Key Technologies & Skills Demonstrated

*   **Data Engineering:** Python, Pandas, SQLAlchemy, Psycopg3
*   **Databases:** PostgreSQL (Dockerized), SQL (Advanced Querying)
*   **Environment & Reproducibility:** Docker, Docker Compose, Python Virtual Environments (`venv`), `pyproject.toml`
*   **Data Analysis & Visualization:** Jupyter Notebooks, Matplotlib, Seaborn, Statistical Analysis
*   **Feature Engineering:** Deriving behavioral metrics, categorical encoding, date/time features
*   **Code Quality:** Black (formatting), Flake8 (linting)
*   **Project Structure & Documentation:** Professional `README.md`, modular code organization

## 📁 Project Structure
banking_analytics_pipeline/
│
├── data/ # Data storage
│ ├── raw/ # Generated raw data (CSVs)
│ └── processed/ # (Future) Cleaned/transformed data
│
├── notebooks/ # Jupyter Notebooks (Analysis & Documentation)
│ ├── 01_initial_data_exploration.ipynb
│ ├── 02_advanced_sql_analysis.ipynb
│ ├── 03_data_cleaning_preparation.ipynb
│ └── 04_feature_engineering.ipynb
│
├── src/ # Python source code
│ ├── ingestion/ # Data generation & loading scripts
│ │ ├── generate_sample_data.py
│ │ └── load_data_to_db.py
│ ├── transformation/ # Data cleaning & feature engineering scripts
│ ├── analysis/ # (Future) Deeper analysis scripts
│ ├── database/ # Database connection & utility scripts
│ │ └── db_connection.py
│ └── utils/ # Utility functions (logging, helpers)
│
├── config/ # Configuration files
│ └── .env # (Not committed) Database credentials
│
├── sql/ # Raw SQL scripts
│ └── create_tables.sql
│
├── docker/ # Docker files (if complex setup needed)
│
├── tests/ # (Future) Unit tests
│
├── requirements.txt # Python dependencies
├── pyproject.toml # Project metadata & build config
├── .gitignore # Git ignore rules
├── docker-compose.yml # Docker services orchestration
└── README.md # This file


## 📊 Project Workflow & Highlights

This project simulates a real-world data analytics workflow, divided into key phases:

### Phase 1: Environment & Database Setup

*   **Dockerized PostgreSQL:** Isolated, reproducible database environment using Docker Compose.
*   **Robust Project Structure:** Organized folders for code, data, notebooks, and configuration.
*   **Dependency Management:** `pyproject.toml` and `requirements.txt` for managing Python libraries.
*   **Secure Configuration:** Database credentials managed via `.env` file.

### Phase 2: Data Generation, Ingestion & Initial Exploration

*   **Realistic Data Simulation:** Python script (`generate_sample_data.py`) creates synthetic `customers`, `accounts`, and `transactions` data.
*   **Efficient Data Loading:** Robust Python script (`load_data_to_db.py`) ingests large CSV files into PostgreSQL using Pandas and SQLAlchemy.
*   **Initial Data Profiling:** Jupyter Notebook (`01_initial_data_exploration.ipynb`) performs integrity checks, descriptive statistics, and basic visualizations.

### Phase 3: Advanced Analysis, Cleaning & Feature Engineering

*   **Advanced SQL Analysis (`02_advanced_sql_analysis.ipynb`):**
    *   Detailed numerical profiling (percentiles, stddev).
    *   SQL-based outlier detection (IQR method).
    *   Categorical data distribution analysis.
    *   Time-series trend analysis (monthly transactions).
    *   Data validation checks.
*   **Data Cleaning & Preparation (`03_data_cleaning_preparation.ipynb`):**
    *   Demonstrated outlier treatment (capping/flooring).
    *   Strategies for handling missing values.
    *   Data type optimization and text standardization.
*   **Feature Engineering (`04_feature_engineering.ipynb`):**
    *   **Account-Level Features:** Transaction counts, amounts, recency (`days_since_last_txn`), MCC patterns.
    *   **Customer-Level Features:** Aggregated balances, transaction volumes, account ownership flags.
    *   **Encoding & Date Features:** One-Hot encoding, date part extraction.
    *   **Statistical Analysis & Visualization:** Detailed stats (skewness/kurtosis), distributions (histograms/KDE), relationships (scatter plots, pair plots), group comparisons (box plots).

## ▶️ How to Run

1.  **Prerequisites:**
    *   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    *   [Python 3.7+](https://www.python.org/downloads/)
2.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd banking_analytics_pipeline
    ```
3.  **Set up Environment & Database:**
    *   Create a virtual environment: `python -m venv venv_bank`
    *   Activate it:
        *   **Windows:** `venv_bank\Scripts\activate`
        *   **macOS/Linux:** `source venv_bank/bin/activate`
    *   Install dependencies: `pip install -r requirements.txt`
    *   Create `config/.env` file with your database credentials (use `docker-compose.yml` for reference).
        ```
        DB_USER=bank_user
        DB_PASSWORD=YourSecurePassword
        DB_NAME=banking_analytics_db
        DB_PORT=5432
        DB_HOST=localhost
        ```
    *   Start the database: `docker-compose up -d`
4.  **Run Data Pipeline:**
    *   Generate sample data: `python src/ingestion/generate_sample_data.py`
    *   Load data into DB: `python src/ingestion/load_data_to_db.py`
5.  **Explore Notebooks:**
    *   Start Jupyter Lab: `jupyter lab`
    *   Open and run the notebooks in the `notebooks/` folder in numerical order.

## 👨‍💻 Author

**Robert Buccat**

*   📧 robert.g.b.101593@gmail.com
*   📱 +974 5002 0849
*   📍 Doha, Qatar
*   [GitHub: rgb101593](https://github.com/rgb101593)
