"""
Administrative API compliance tests covering authentication, CRUD, and role restrictions.
Validates that super admin and assistant behaviors align with published governance rules.
"""

import os
from typing import Dict

import pytest

DEFAULT_TIMEOUT_SECONDS = 10


def _build_url(http_client, path: str) -> str:
    """Join the base URL from the session with a path segment."""
    return f"{http_client.base_url}{path}"


def _post(http_client, path: str, json: Dict, headers: Dict = None):
    """Perform a POST request with a standard timeout and JSON body."""
    return http_client.post(
        _build_url(http_client, path),
        json=json,
        headers=headers,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def _delete(http_client, path: str, headers: Dict = None):
    """Perform a DELETE request with timeout and optional headers."""
    return http_client.delete(_build_url(http_client, path), headers=headers, timeout=DEFAULT_TIMEOUT_SECONDS)


def _headers(token: str) -> Dict[str, str]:
    """Construct authorization headers for bearer-token protected endpoints."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def super_admin_token(http_client):
    """Authenticate a super admin using environment credentials."""
    email = os.getenv("SUPER_ADMIN_EMAIL")
    password = os.getenv("SUPER_ADMIN_PASSWORD")
    if not email or not password:
        pytest.skip("SUPER_ADMIN_EMAIL ou SUPER_ADMIN_PASSWORD non configurés")
    response = _post(http_client, "/auth/login", {"email": email, "password": password})
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token, "Aucun token renvoyé pour le super admin"
    return token


@pytest.fixture(scope="session")
def assistant_token(http_client):
    """Authenticate an admin assistant using environment credentials."""
    email = os.getenv("ASSISTANT_EMAIL")
    password = os.getenv("ASSISTANT_PASSWORD")
    if not email or not password:
        pytest.skip("ASSISTANT_EMAIL ou ASSISTANT_PASSWORD non configurés")
    response = _post(http_client, "/auth/login", {"email": email, "password": password})
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token, "Aucun token renvoyé pour l'assistant"
    return token


@pytest.mark.requirement("ADMIN_LOGIN")
def test_admin_can_login(super_admin_token):
    """Super admin authentication must return a valid bearer token."""
    assert isinstance(super_admin_token, str)
    assert len(super_admin_token) > 10


@pytest.mark.requirement("ADMIN_CRUD_LISTINGS")
def test_super_admin_can_create_and_delete_listing(http_client, super_admin_token):
    """Super admin must create and delete listings successfully."""
    payload = {
        "title": "Test listing QA",
        "description": "Annonce de test",
        "price": 50000,
        "type_logement": "CHAMBRE",
        "commune_id": 1,
        "zone_id": 1,
        "whatsapp_phone": "+22900000000",
    }
    create_response = _post(http_client, "/admin/listings", payload, headers=_headers(super_admin_token))
    assert create_response.status_code == 201
    listing = create_response.json()
    listing_id = listing.get("id")
    assert listing_id is not None

    delete_response = _delete(http_client, f"/admin/listings/{listing_id}", headers=_headers(super_admin_token))
    assert delete_response.status_code in {200, 204}


@pytest.mark.requirement("ADMIN_VALIDATE_LISTINGS")
def test_super_admin_can_publish_listing(http_client, super_admin_token):
    """Super admin must transition listings into the published state."""
    draft_payload = {
        "title": "Annonce à valider",
        "description": "Brouillon",
        "price": 30000,
        "type_logement": "CHAMBRE",
        "commune_id": 1,
        "zone_id": 1,
        "whatsapp_phone": "+22900000000",
        "status": "DRAFT",
    }
    create_response = _post(http_client, "/admin/listings", draft_payload, headers=_headers(super_admin_token))
    assert create_response.status_code == 201
    listing_id = create_response.json().get("id")
    assert listing_id is not None

    validate_response = _post(http_client, f"/admin/listings/{listing_id}/validate", {}, headers=_headers(super_admin_token))
    assert validate_response.status_code == 200
    assert validate_response.json().get("status") == "PUBLISHED"


@pytest.mark.requirement("ADMIN_ASSISTANT_LIMITED")
def test_admin_assistant_cannot_publish_or_delete_listing(http_client, assistant_token, super_admin_token):
    """Admin assistants must be blocked from publishing or deleting listings."""
    payload = {
        "title": "Annonce test assistant",
        "description": "Test limitation",
        "price": 25000,
        "type_logement": "CHAMBRE",
        "commune_id": 1,
        "zone_id": 1,
        "whatsapp_phone": "+22900000000",
        "status": "PENDING",
    }
    create_response = _post(http_client, "/admin/listings", payload, headers=_headers(super_admin_token))
    assert create_response.status_code == 201
    listing_id = create_response.json().get("id")
    assert listing_id is not None

    validate_response = _post(http_client, f"/admin/listings/{listing_id}/validate", {}, headers=_headers(assistant_token))
    assert validate_response.status_code in {401, 403}

    delete_response = _delete(http_client, f"/admin/listings/{listing_id}", headers=_headers(assistant_token))
    assert delete_response.status_code in {401, 403}


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
