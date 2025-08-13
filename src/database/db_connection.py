# src/database/db_connection.py
"""
Utility module for managing database connections using SQLAlchemy.
Assumes psycopg (psycopg3) is installed and uses the `postgresql+psycopg` driver.
Loads database credentials from environment variables (.env file).
"""

from __future__ import annotations

import os
import logging
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (if present)
load_dotenv()


def _env_int(name: str, default: int) -> int:
    """Read an environment variable and return it as int, with validation."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"Environment variable {name!r} must be an integer, got: {raw!r}")
    if not (1 <= value <= 65535):
        raise ValueError(f"Environment variable {name!r} must be a valid TCP port (1-65535), got: {value}")
    return value


def get_database_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine connected to the PostgreSQL database.

    Environment variables used:
      - DB_USER (required)
      - DB_PASSWORD (required)
      - DB_NAME (required)
      - DB_HOST (optional, default: 'localhost')
      - DB_PORT (optional, default: 5432)

    This function assumes psycopg (psycopg3) is installed and will use the
    SQLAlchemy drivername 'postgresql+psycopg'.
    """
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = _env_int("DB_PORT", 5432)
    db_name = os.getenv("DB_NAME")

    missing = [k for k, v in (("DB_USER", db_user), ("DB_PASSWORD", db_password), ("DB_NAME", db_name)) if not v]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    drivername = "postgresql+psycopg"  # psiocpg3

    # Construct the database URL for SQLAlchemy
    db_url = URL.create(
        drivername=drivername,
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )

    logger.info("Creating database engine for database=%s host=%s port=%s driver=%s", db_name, db_host, db_port, drivername)
    engine = create_engine(db_url, echo=False, future=True)
    return engine


def get_db_session(engine=None) -> Session:
    """
    Create and return a SQLAlchemy Session bound to the given engine.
    If engine is None, a new engine is created using environment variables.
    """
    if engine is None:
        engine = get_database_engine()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    return SessionLocal()


if __name__ == "__main__":
    try:
        engine = get_database_engine()
        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            row = result.fetchone()
            version = row[0] if row else None
            print("Database connection successful!")
            print(f"PostgreSQL version: {version}")
    except Exception as e:
        logger.exception("Error connecting to database: %s", e)
        raise