"""
API-level requirement checks for public listing discovery and WhatsApp contact flows.
Ensures core user-facing capabilities remain compliant with marketplace constraints.
"""

from typing import Dict, Optional

import pytest

DEFAULT_TIMEOUT_SECONDS = 10


def _build_url(http_client, path: str) -> str:
    """Join the base URL from the session with a path segment."""
    return f"{http_client.base_url}{path}"


def _get(http_client, path: str, **params):
    """Perform a GET request with standard timeout and JSON expectation."""
    return http_client.get(_build_url(http_client, path), params=params, timeout=DEFAULT_TIMEOUT_SECONDS)


def _extract_first_listing_id(payload: Dict) -> Optional[int]:
    """Return the first listing identifier from a paginated response if present."""
    results = payload.get("results")
    if isinstance(results, list) and results:
        first_item = results[0]
        return first_item.get("id")
    return None


@pytest.mark.requirement("USER_SEARCH_TEXT")
def test_user_can_search_listings(http_client):
    """Users must access listings via text-based queries."""
    response = _get(http_client, "/listings", q="chambre")
    assert response.status_code == 200
    payload = response.json()
    assert "results" in payload
    assert isinstance(payload["results"], list)


@pytest.mark.requirement("USER_FILTERS_BASIC")
def test_user_can_filter_by_commune_zone_and_price(http_client):
    """Listings must support structured filters for locality, price, and housing type."""
    params = {
        "commune_id": 1,
        "zone_id": 1,
        "price_min": 10000,
        "price_max": 100000,
        "type_logement": "CHAMBRE",
    }
    response = _get(http_client, "/listings", **params)
    assert response.status_code == 200
    payload = response.json()
    for item in payload.get("results", []):
        assert item.get("price") is None or 10000 <= item["price"] <= 100000
        assert item.get("type_logement") in (None, "CHAMBRE")


@pytest.mark.requirement("USER_WHATSAPP_BUTTON")
def test_listing_detail_contains_whatsapp_contact(http_client):
    """Each listing detail must expose a WhatsApp contact link or phone."""
    initial = _get(http_client, "/listings", status="PUBLISHED", page_size=1)
    assert initial.status_code == 200
    first_listing_id = _extract_first_listing_id(initial.json())
    if first_listing_id is None:
        pytest.skip("Aucune annonce publiée disponible pour vérifier le contact WhatsApp")

    detail_response = _get(http_client, f"/listings/{first_listing_id}")
    assert detail_response.status_code == 200
    listing = detail_response.json()
    whatsapp_value = listing.get("whatsapp_link") or listing.get("whatsapp_phone")
    assert whatsapp_value, "Aucune information WhatsApp trouvée sur l'annonce"

    if isinstance(whatsapp_value, str) and whatsapp_value.startswith("http"):
        assert "wa.me" in whatsapp_value or "api.whatsapp.com" in whatsapp_value


@pytest.mark.requirement("NO_ONLINE_PAYMENT")
def test_no_online_payment_endpoints(http_client):
    """Ensure no payment-centric endpoints are exposed on the public API."""
    forbidden_paths = ["/payments", "/checkout", "/stripe", "/pay"]
    for path in forbidden_paths:
        response = _get(http_client, path)
        assert response.status_code in {404, 405}, f"Endpoint suspect trouvé : {path}"


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
