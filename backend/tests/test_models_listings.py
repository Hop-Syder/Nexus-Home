"""Model validation checks for listings to enforce pricing and readability rules."""

import pytest
from django.core.exceptions import ValidationError


@pytest.mark.requirement("LISTING_MODEL_VALIDATION")
@pytest.mark.django_db
def test_listing_price_cannot_be_negative(base_location, super_admin):
    """Reject listings with negative pricing to avoid inconsistent catalog data."""
    location = base_location
    from core.models import Listing

    listing = Listing(
        title="Test negative price",
        description="desc",
        price=-1000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="BASIQUE",
        is_meuble=False,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=location["zone"],
        whatsapp_phone="+22990000000",
        status="DRAFT",
        created_by=super_admin,
    )

    with pytest.raises(ValidationError):
        listing.full_clean()


@pytest.mark.requirement("LISTING_MODEL_STR")
@pytest.mark.django_db
def test_listing_str_uses_title(published_listing):
    """Ensure __str__ returns the human friendly title for admin readability."""
    assert str(published_listing) == "Chambre meublée à Fidjrossè"


@pytest.mark.requirement("LISTING_MODEL_SLUG")
@pytest.mark.django_db
def test_slug_is_generated_and_unique(base_location, super_admin):
    """Slug values should auto-populate and avoid collisions for duplicate titles."""
    from core.models import Listing

    location = base_location

    first = Listing.objects.create(
        title="Chambre test",  # identical titles must not collide
        description="desc",
        price=1000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="BASIQUE",
        is_meuble=False,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=location["zone"],
        whatsapp_phone="+22900000000",
        status="PUBLISHED",
        created_by=super_admin,
    )

    second = Listing.objects.create(
        title="Chambre test",  # intentionally same to verify suffix
        description="desc",
        price=2000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="BASIQUE",
        is_meuble=False,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=location["zone"],
        whatsapp_phone="+22900000001",
        status="PUBLISHED",
        created_by=super_admin,
    )

    assert first.slug
    assert second.slug
    assert first.slug != second.slug


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
