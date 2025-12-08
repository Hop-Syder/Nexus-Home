"""Initial schema for Nexus-Home core models."""
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [("auth", "0012_alter_user_first_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("role", models.CharField(choices=[("SUPER_ADMIN", "Super Admin"), ("ADMIN_ASSISTANT", "Admin Assistant")], default="ADMIN_ASSISTANT", max_length=32)),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("code", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "country",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="departments", to="core.country"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Commune",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "department",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="communes", to="core.department"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Arrondissement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "commune",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="arrondissements", to="core.commune"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Zone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "type",
                    models.CharField(
                        choices=[("QUARTIER", "Quartier"), ("REPERE", "Point de repère"), ("ZONE", "Zone")], max_length=20
                    ),
                ),
                ("synonyms", models.JSONField(blank=True, default=list)),
                (
                    "arrondissement",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="zones", to="core.arrondissement"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Listing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(blank=True, max_length=255)),
                ("description", models.TextField()),
                ("price", models.PositiveIntegerField()),
                ("currency", models.CharField(default="XOF", max_length=10)),
                (
                    "type_logement",
                    models.CharField(
                        choices=[("CHAMBRE", "Chambre"), ("STUDIO", "Studio"), ("APPARTEMENT", "Appartement"), ("VILLA", "Villa")],
                        max_length=20,
                    ),
                ),
                (
                    "standing",
                    models.CharField(choices=[("BASIQUE", "Basique"), ("MOYEN", "Moyen"), ("HAUT", "Haut")], max_length=20),
                ),
                ("is_meuble", models.BooleanField(default=False)),
                ("duree", models.CharField(choices=[("JOUR", "Jour"), ("MOIS", "Mois"), ("ANNEE", "Année")], max_length=10)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("whatsapp_phone", models.CharField(max_length=32)),
                (
                    "status",
                    models.CharField(
                        choices=[("DRAFT", "Brouillon"), ("PENDING", "En attente"), ("PUBLISHED", "Publié"), ("REJECTED", "Rejeté")],
                        default="DRAFT",
                        max_length=15,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("views_count", models.PositiveIntegerField(default=0)),
                (
                    "arrondissement",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="listings", to="core.arrondissement"),
                ),
                (
                    "commune",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="listings", to="core.commune"),
                ),
                (
                    "country",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="listings", to="core.country"),
                ),
                (
                    "department",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="listings", to="core.department"),
                ),
                (
                    "zone",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="listings", to="core.zone"),
                ),
                (
                    "created_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_listings", to="core.user"),
                ),
                (
                    "validated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="validated_listings",
                        to="core.user",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
