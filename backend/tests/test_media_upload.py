"""Media upload API coverage to guarantee admins can manage listing galleries."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import Listing, ListingMedia


def build_test_image(name: str = "test.jpg") -> SimpleUploadedFile:
    """Create a tiny in-memory JPEG to validate upload flows without hitting disk."""

    content = b"\xff\xd8\xff\xe0"  # minimal JPEG header
    return SimpleUploadedFile(name, content, content_type="image/jpeg")


@pytest.mark.requirement("ADMIN_MEDIA_UPLOAD")
@pytest.mark.django_db
def test_assistant_can_upload_media_to_draft_listing(assistant_client, base_location, super_admin):
    listing = Listing.objects.create(
        title="Brouillon avec média",
        description="Test upload image",
        price=10000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="BASIQUE",
        is_meuble=False,
        duree="MOIS",
        country=base_location["country"],
        department=base_location["department"],
        commune=base_location["commune"],
        arrondissement=base_location["arrondissement"],
        zone=base_location["zone"],
        whatsapp_phone="+22991112222",
        status=Listing.STATUS_DRAFT,
        created_by=super_admin,
    )

    response = assistant_client.post(
        f"/api/v1/admin/listings/{listing.id}/media",
        {"file": build_test_image(), "caption": "Vue", "position": 1},
        format="multipart",
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["url"].startswith("http") or body["url"].startswith("/media/")
    assert body["caption"] == "Vue"
    assert ListingMedia.objects.filter(listing=listing).count() == 1


@pytest.mark.requirement("ADMIN_MEDIA_UPLOAD")
@pytest.mark.django_db
def test_assistant_cannot_modify_media_on_published_listing(assistant_client, base_location, super_admin):
    listing = Listing.objects.create(
        title="Publié",
        description="Annonce publiée",
        price=20000,
        currency="XOF",
        type_logement="CHAMBRE",
        standing="MOYEN",
        is_meuble=True,
        duree="MOIS",
        country=base_location["country"],
        department=base_location["department"],
        commune=base_location["commune"],
        arrondissement=base_location["arrondissement"],
        zone=base_location["zone"],
        whatsapp_phone="+22993334444",
        status=Listing.STATUS_PUBLISHED,
        created_by=super_admin,
    )

    response = assistant_client.post(
        f"/api/v1/admin/listings/{listing.id}/media",
        {"file": build_test_image()},
        format="multipart",
    )

    assert response.status_code == 403


@pytest.mark.requirement("ADMIN_MEDIA_UPLOAD")
@pytest.mark.django_db
def test_super_admin_can_delete_media(super_admin_client, base_location, super_admin):
    listing = Listing.objects.create(
        title="Suppression media",
        description="Test delete",
        price=30000,
        currency="XOF",
        type_logement="STUDIO",
        standing="MOYEN",
        is_meuble=True,
        duree="MOIS",
        country=base_location["country"],
        department=base_location["department"],
        commune=base_location["commune"],
        arrondissement=base_location["arrondissement"],
        zone=base_location["zone"],
        whatsapp_phone="+22995556666",
        status=Listing.STATUS_PENDING,
        created_by=super_admin,
    )
    media = ListingMedia.objects.create(listing=listing, file=build_test_image("delete.jpg"))

    response = super_admin_client.delete(
        f"/api/v1/admin/listings/{listing.id}/media/{media.id}"
    )

    assert response.status_code == 204
    assert not ListingMedia.objects.filter(pk=media.id).exists()


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
