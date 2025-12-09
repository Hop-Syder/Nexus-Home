"""Shared pytest fixtures for Django/DRF compliance checks on Nexus-Home."""

import os
import pytest

# Hard skip if Django or DRF are not available to avoid false negatives during collection.
pytest.importorskip(
    "django",
    reason="Django must be installed to run backend compliance checks.",
)
pytest.importorskip(
    "rest_framework",
    reason="Django REST Framework is required for API client fixtures.",
)
pytest.importorskip(
    "core",
    reason="Core application with domain models must be present for backend tests.",
)

if not os.getenv("DJANGO_SETTINGS_MODULE"):
    pytest.skip(
        "DJANGO_SETTINGS_MODULE must be configured to run Django-backed tests.",
        allow_module_level=True,
    )

from django.contrib.auth import get_user_model  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402

from core.models import (  # noqa: E402
    Arrondissement,
    Commune,
    Country,
    Department,
    Listing,
    Zone,
)

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """Expose a DRF APIClient configured for authenticated and anonymous calls."""
    return APIClient()


@pytest.fixture
def super_admin(db):
    """Create a super admin test user with full privileges."""
    return User.objects.create_user(
        email="admin@test.com",
        password="admin123",
        role="SUPER_ADMIN",
    )


@pytest.fixture
def admin_assistant(db):
    """Create an assistant admin with restricted permissions."""
    return User.objects.create_user(
        email="assistant@test.com",
        password="assistant123",
        role="ADMIN_ASSISTANT",
    )


@pytest.fixture
def base_location(db):
    """Seed a minimal location hierarchy to anchor listing tests."""
    country = Country.objects.create(name="Bénin", code="BJ")
    department = Department.objects.create(country=country, name="Littoral")
    commune = Commune.objects.create(department=department, name="Cotonou")
    arrondissement = Arrondissement.objects.create(
        commune=commune,
        name="13ème Arrondissement",
    )
    zone = Zone.objects.create(
        arrondissement=arrondissement,
        name="Fidjrossè",
        type="QUARTIER",
        synonyms=["Fidjrosse", "Fidjrossé"],
    )
    return {
        "country": country,
        "department": department,
        "commune": commune,
        "arrondissement": arrondissement,
        "zone": zone,
    }


@pytest.fixture
def published_listing(db, base_location, super_admin):
    """Create a published listing available to public search endpoints."""
    location = base_location
    listing = Listing.objects.create(
        title="Chambre meublée à Fidjrossè",
        description="Belle chambre propre, proche de la plage.",
        price=50000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="MOYEN",
        is_meuble=True,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=location["zone"],
        whatsapp_phone="+22990000000",
        status="PUBLISHED",
        created_by=super_admin,
    )
    return listing


@pytest.fixture
def super_admin_client(api_client: APIClient, super_admin: User) -> APIClient:
    """Return an authenticated client bound to the super admin account."""
    api_client.force_authenticate(user=super_admin)
    return api_client


@pytest.fixture
def assistant_client(api_client: APIClient, admin_assistant: User) -> APIClient:
    """Return an authenticated client bound to the assistant admin account."""
    api_client.force_authenticate(user=admin_assistant)
    return api_client


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
