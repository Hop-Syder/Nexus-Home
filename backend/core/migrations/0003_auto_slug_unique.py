"""Ensure listings have unique slugs and enforce a uniqueness constraint."""
from django.db import migrations, models
from django.utils.text import slugify


def _generate_candidate(existing_slugs: set[str], base: str, fallback: str) -> str:
    """Generate a slug that does not collide with already processed entries."""

    candidate = base or fallback
    suffix = 1

    while candidate in existing_slugs:
        suffix += 1
        candidate = f"{base}-{suffix}" if base else f"{fallback}-{suffix}"

    return candidate


def populate_slugs(apps, schema_editor):
    Listing = apps.get_model("core", "Listing")
    existing_slugs: set[str] = set()

    for listing in Listing.objects.all().order_by("id"):
        provided_slug = slugify(listing.slug or "")
        base_slug = slugify(listing.title or "")[:240]
        fallback = "listing"

        if provided_slug:
            candidate = _generate_candidate(existing_slugs, provided_slug, fallback)
        else:
            candidate = _generate_candidate(existing_slugs, base_slug, fallback)

        listing.slug = candidate
        listing.save(update_fields=["slug"])
        existing_slugs.add(candidate)


def noop_reverse(apps, schema_editor):
    # Slugs remain useful even if the migration is reversed; no action needed.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_listings_fts_index"),
    ]

    operations = [
        migrations.RunPython(populate_slugs, noop_reverse),
        migrations.AlterField(
            model_name="listing",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]

# ────────────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ────────────────────────────────────────
