"""Admin-side listing workflows including CRUD, publication, and role limits."""

import pytest
from django.urls import reverse


@pytest.mark.requirement("ADMIN_CRUD_LISTINGS")
@pytest.mark.django_db
def test_super_admin_can_create_and_delete_listing(super_admin_client, base_location):
    """Full CRUD should succeed for super admin accounts."""
    url = reverse("admin-listings-list")
    payload = {
        "title": "Annonce admin",
        "description": "desc",
        "price": 40000,
        "currency": "XOF",
        "type_logement": "CHAMBRE",
        "standing": "BASIQUE",
        "is_meuble": False,
        "duree": "MOIS",
        "country": base_location["country"].id,
        "department": base_location["department"].id,
        "commune": base_location["commune"].id,
        "arrondissement": base_location["arrondissement"].id,
        "zone": base_location["zone"].id,
        "whatsapp_phone": "+22991111111",
        "status": "DRAFT",
    }
    create_response = super_admin_client.post(url, payload, format="json")
    assert create_response.status_code == 201
    listing_id = create_response.json()["id"]

    delete_url = reverse("admin-listings-detail", args=[listing_id])
    delete_response = super_admin_client.delete(delete_url)
    assert delete_response.status_code in (200, 204)


@pytest.mark.requirement("ADMIN_VALIDATE_LISTINGS")
@pytest.mark.django_db
def test_super_admin_can_publish_listing(super_admin_client, base_location):
    """Super admin publishes pending listings through a dedicated endpoint."""
    url = reverse("admin-listings-list")
    payload = {
        "title": "Annonce à publier",
        "description": "desc",
        "price": 45000,
        "currency": "XOF",
        "type_logement": "CHAMBRE",
        "standing": "MOYEN",
        "is_meuble": True,
        "duree": "MOIS",
        "country": base_location["country"].id,
        "department": base_location["department"].id,
        "commune": base_location["commune"].id,
        "arrondissement": base_location["arrondissement"].id,
        "zone": base_location["zone"].id,
        "whatsapp_phone": "+22992222222",
        "status": "PENDING",
    }
    create_response = super_admin_client.post(url, payload, format="json")
    assert create_response.status_code == 201
    listing_id = create_response.json()["id"]

    validate_url = reverse("admin-listings-validate", args=[listing_id])
    validation_response = super_admin_client.post(validate_url)
    assert validation_response.status_code == 200
    assert validation_response.json()["status"] == "PUBLISHED"


@pytest.mark.requirement("ADMIN_ASSISTANT_LIMITED")
@pytest.mark.django_db
def test_assistant_cannot_publish_or_delete_listing(
    assistant_client, super_admin_client, base_location
):
    """Assistants must be blocked from publishing or deleting listings."""
    url = reverse("admin-listings-list")
    payload = {
        "title": "Annonce test assistant",
        "description": "desc",
        "price": 30000,
        "currency": "XOF",
        "type_logement": "CHAMBRE",
        "standing": "BASIQUE",
        "is_meuble": False,
        "duree": "MOIS",
        "country": base_location["country"].id,
        "department": base_location["department"].id,
        "commune": base_location["commune"].id,
        "arrondissement": base_location["arrondissement"].id,
        "zone": base_location["zone"].id,
        "whatsapp_phone": "+22993333333",
        "status": "PENDING",
    }
    create_response = super_admin_client.post(url, payload, format="json")
    assert create_response.status_code == 201
    listing_id = create_response.json()["id"]

    validate_url = reverse("admin-listings-validate", args=[listing_id])
    assistant_publish = assistant_client.post(validate_url)
    assert assistant_publish.status_code in (401, 403)

    delete_url = reverse("admin-listings-detail", args=[listing_id])
    assistant_delete = assistant_client.delete(delete_url)
    assert assistant_delete.status_code in (401, 403)


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
