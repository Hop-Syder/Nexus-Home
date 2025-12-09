"""Backend stats API coverage for admin overview and top zones."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_stats_requires_authentication(api_client):
    """Anonymous calls should be rejected to protect internal insights."""

    overview_url = reverse("admin-stats-overview")
    response = api_client.get(overview_url)
    assert response.status_code in {401, 403}


@pytest.mark.requirement("ADMIN_STATS_OVERVIEW")
def test_overview_counts_lifecycle(super_admin_client, base_location, super_admin):
    """Ensure lifecycle counters and view totals surface expected aggregates."""

    from core.models import Listing

    location = base_location
    Listing.objects.create(
        title="Publiée",
        description="",
        price=10000,
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
        status=Listing.STATUS_PUBLISHED,
        views_count=7,
        whatsapp_clicks=3,
        created_by=super_admin,
    )
    Listing.objects.create(
        title="En attente",
        description="",
        price=20000,
        currency="XOF",
        type_logement="STUDIO",
        standing="MOYEN",
        is_meuble=True,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=location["zone"],
        whatsapp_phone="+22991111111",
        status=Listing.STATUS_PENDING,
        views_count=0,
        created_by=super_admin,
    )

    overview_url = reverse("admin-stats-overview")
    response = super_admin_client.get(overview_url)
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert payload["published"] == 1
    assert payload["pending"] == 1
    assert payload["draft"] == 0
    assert payload["rejected"] == 0
    assert payload["views"] == 7
    assert payload["whatsapp_clicks"] == 3


@pytest.mark.requirement("ADMIN_STATS_TOP_ZONES")
def test_top_zones_rank_by_published(super_admin_client, base_location, super_admin):
    """Verify the ranking endpoint orders zones by published listing volume."""

    from core.models import Listing, Zone

    location = base_location
    second_zone = Zone.objects.create(
        arrondissement=location["arrondissement"],
        name="Agla",
        type="QUARTIER",
        synonyms=["Agla"],
    )

    # zone1 gets two published listings, zone2 gets one
    for idx in range(2):
        Listing.objects.create(
            title=f"Annonce zone 1 {idx}",
            description="",
            price=30000,
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
            whatsapp_phone="+22993333333",
            status=Listing.STATUS_PUBLISHED,
            created_by=super_admin,
        )

    Listing.objects.create(
        title="Annonce zone 2",
        description="",
        price=35000,
        currency="XOF",
        type_logement="STUDIO",
        standing="MOYEN",
        is_meuble=True,
        duree="MOIS",
        country=location["country"],
        department=location["department"],
        commune=location["commune"],
        arrondissement=location["arrondissement"],
        zone=second_zone,
        whatsapp_phone="+22994444444",
        status=Listing.STATUS_PUBLISHED,
        created_by=super_admin,
    )

    ranking_url = reverse("admin-stats-top-zones")
    response = super_admin_client.get(ranking_url, {"limit": 5})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert results[0]["zone_name"] == location["zone"].name
    assert results[0]["listing_count"] == 2
    assert results[1]["zone_name"] == second_zone.name
    assert results[1]["listing_count"] == 1


@pytest.mark.requirement("ADMIN_STATS_TOP_ZONES")
def test_top_zones_respects_limit(super_admin_client, base_location, super_admin):
    """Ensure the limit parameter is bounded to avoid heavy queries."""

    from core.models import Listing

    location = base_location
    for idx in range(6):
        Listing.objects.create(
            title=f"Annonce {idx}",
            description="",
            price=25000,
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
            whatsapp_phone="+22995555555",
            status=Listing.STATUS_PUBLISHED,
            created_by=super_admin,
        )

    ranking_url = reverse("admin-stats-top-zones")
    response = super_admin_client.get(ranking_url, {"limit": 1})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["listing_count"] == 6
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
