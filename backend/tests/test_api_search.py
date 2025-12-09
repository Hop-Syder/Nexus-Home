"""Full-text search behavior validation for public listings API."""

import pytest
from django.urls import reverse


@pytest.mark.requirement("SEARCH_FULLTEXT")
@pytest.mark.django_db
def test_search_returns_relevant_results(api_client, published_listing):
    """Searching with synonyms should return the published listing."""
    url = reverse("listings-list")
    response = api_client.get(url, {"q": "chambre meublée fidjrosse"})
    assert response.status_code == 200
    payload = response.json()
    results = payload.get("results", payload)
    assert any(item["id"] == published_listing.id for item in results)


@pytest.mark.requirement("LOCATION_SEARCH")
@pytest.mark.django_db
def test_zone_search_returns_synonym_matches(api_client, base_location):
    """Zone search should return matches for name and stored synonyms with context."""
    url = reverse("locations-search")
    response = api_client.get(url, {"q": "Fidjrosse"})
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert any(item["id"] == base_location["zone"].id for item in payload)
    sample = payload[0]
    assert "commune_name" in sample and "arrondissement_name" in sample


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
