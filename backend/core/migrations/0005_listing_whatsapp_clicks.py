"""Add WhatsApp click counter to listings for conversion tracking."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_listing_media"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="whatsapp_clicks",
            field=models.PositiveIntegerField(default=0),
        ),
    ]


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
