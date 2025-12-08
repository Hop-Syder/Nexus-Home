"""Add GIN index for listing full-text search across title, description, and zone fields."""
from __future__ import annotations

from django.db import migrations
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="listing",
            index=GinIndex(
                SearchVector(
                    "title",
                    "description",
                    "zone__name",
                    "zone__synonyms",
                    config="french",
                ),
                name="listings_fts_idx",
            ),
        ),
    ]


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
