"""Public API verification for search, filters, and WhatsApp contact."""

import pytest
from django.urls import reverse


def _listings_response(api_client, **params):
    url = reverse("listings-list")
    return api_client.get(url, params)


@pytest.mark.requirement("USER_SEARCH_TEXT")
@pytest.mark.django_db
def test_user_can_search_by_text(api_client, published_listing):
    """Users should retrieve the published listing when searching with matching keywords."""
    response = _listings_response(api_client, q="chambre fidjrossè")
    assert response.status_code == 200
    payload = response.json()
    results = payload.get("results", payload)
    assert any(item["id"] == published_listing.id for item in results)


@pytest.mark.requirement("USER_FILTERS_BASIC")
@pytest.mark.django_db
def test_user_can_filter_by_location_and_price(api_client, published_listing):
    """Filtering by commune, zone, price and type must constrain results."""
    response = _listings_response(
        api_client,
        commune_id=published_listing.commune_id,
        zone_id=published_listing.zone_id,
        price_min=40000,
        price_max=60000,
        type_logement="CHAMBRE",
    )
    assert response.status_code == 200
    payload = response.json()
    results = payload.get("results", payload)
    assert results
    for item in results:
        assert 40000 <= item["price"] <= 60000
        assert item["type_logement"] == "CHAMBRE"


@pytest.mark.requirement("USER_WHATSAPP_BUTTON")
@pytest.mark.django_db
def test_listing_detail_exposes_whatsapp_contact(api_client, published_listing):
    """Every listing detail should surface a WhatsApp contact method."""
    detail_url = reverse("listings-detail", args=[published_listing.id])
    response = api_client.get(detail_url)
    assert response.status_code == 200
    payload = response.json()
    whatsapp_contact = payload.get("whatsapp_link") or payload.get("whatsapp_phone")
    assert whatsapp_contact
    if isinstance(whatsapp_contact, str):
        assert "wa.me" in whatsapp_contact or "api.whatsapp.com" in whatsapp_contact or whatsapp_contact.startswith(
            "+"
        )


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
