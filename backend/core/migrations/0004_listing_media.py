"""Add media attachments for listings to support galleries and thumbnails."""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Introduce ListingMedia with ordering and lookup indexes."""

    dependencies = [
        ("core", "0003_auto_slug_unique"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListingMedia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.ImageField(upload_to="listing_media/")),
                ("caption", models.CharField(blank=True, max_length=255)),
                ("position", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media",
                        to="core.listing",
                    ),
                ),
            ],
            options={
                "ordering": ["position", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="listingmedia",
            index=models.Index(fields=["listing", "position"], name="core_listin_listing_a78da5_idx"),
        ),
    ]


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
