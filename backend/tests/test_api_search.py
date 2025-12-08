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


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
