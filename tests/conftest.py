"""
Shared pytest fixtures for API and database verification against the Nexus-Home backend.
Provides HTTP session setup, environment-driven base URL selection, and PostgreSQL connectivity.
"""

import os
from typing import Generator

import psycopg2
import pytest
import requests


def _build_base_url() -> str:
    """Return the API base URL from environment or default to local dev."""
    url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Expose the normalized API base URL for integration-style tests."""
    return _build_base_url()


@pytest.fixture(scope="session")
def http_client(base_url: str) -> requests.Session:
    """Configure an HTTP session with the API base URL attached for convenience."""
    session = requests.Session()
    session.base_url = base_url
    session.headers.update({"Accept": "application/json"})
    return session


@pytest.fixture(scope="session")
def db_conn() -> Generator[psycopg2.extensions.connection, None, None]:
    """Yield a PostgreSQL connection targeting Supabase or the configured DSN."""
    dsn = os.getenv("SUPABASE_DB_URL")
    if not dsn:
        pytest.skip("SUPABASE_DB_URL non défini, impossible de tester la base de données")

    connection = psycopg2.connect(dsn)
    connection.autocommit = True
    try:
        yield connection
    finally:
        connection.close()


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
