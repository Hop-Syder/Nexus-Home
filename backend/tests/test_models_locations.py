"""Model-level validation of the location hierarchy for Nexus-Home."""

import pytest


@pytest.mark.requirement("DB_LOCATION_HIERARCHY")
@pytest.mark.django_db
def test_location_hierarchy_creation(base_location):
    """Ensure countries, departments, communes, arrondissements et zones chain correctly."""
    country = base_location["country"]
    department = base_location["department"]
    commune = base_location["commune"]
    arrondissement = base_location["arrondissement"]
    zone = base_location["zone"]

    assert department.country == country
    assert commune.department == department
    assert arrondissement.commune == commune
    assert zone.arrondissement == arrondissement
    assert zone.name == "Fidjrossè"
    assert "Fidjrosse" in zone.synonyms


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
