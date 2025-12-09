"""
Database verification for localization hierarchy, listing foreign keys, and full-text search readiness.
Ensures Supabase/PostgreSQL structures align with Nexus-Home discovery expectations.
"""

import pytest


@pytest.mark.requirement("DB_LOCATION_HIERARCHY")
def test_location_tables_exist(db_conn):
    """Confirm that core location and listing tables are present in the public schema."""
    cursor = db_conn.cursor()
    tables = ["countries", "departments", "communes", "arrondissements", "zones", "listings"]
    for table_name in tables:
        cursor.execute("SELECT to_regclass(%s);", (f"public.{table_name}",))
        result = cursor.fetchone()[0]
        assert result is not None, f"Table manquante : {table_name}"


@pytest.mark.requirement("DB_LOCATION_HIERARCHY")
def test_listings_have_location_fk_columns(db_conn):
    """Validate presence of expected foreign key columns on listings for spatial queries."""
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'listings';
        """
    )
    columns = {row[0] for row in cursor.fetchall()}
    expected = {"country_id", "department_id", "commune_id", "arrondissement_id", "zone_id"}
    missing = expected - columns
    assert not missing, f"Colonnes manquantes sur listings: {missing}"


@pytest.mark.requirement("SEARCH_FULLTEXT")
def test_fulltext_search_index_exists(db_conn):
    """Detect a GIN index with a tsvector definition to support full-text search."""
    cursor = db_conn.cursor()
    cursor.execute(
        """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE tablename = 'listings';
        """
    )
    indexes = cursor.fetchall()
    found_index = False
    for index_name, index_definition in indexes:
        if "USING gin" in index_definition and "to_tsvector" in index_definition:
            found_index = True
            break

    assert found_index, "Aucun index full-text (GIN + to_tsvector) trouvé sur listings"


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
