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


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
