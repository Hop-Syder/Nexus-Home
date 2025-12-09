"""Domain models for users, locations, and listings powering the Nexus-Home API."""
from __future__ import annotations

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Custom manager enforcing email-based authentication and role defaults."""

    def create_user(self, email: str, password: str | None = None, role: str = "ADMIN_ASSISTANT", **extra_fields) -> "User":
        if not email:
            raise ValueError("Users must have an email address.")
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        user = self.create_user(email=email, password=password, role="SUPER_ADMIN", **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Internal platform users with role-based privileges."""

    ROLE_SUPER_ADMIN = "SUPER_ADMIN"
    ROLE_ADMIN_ASSISTANT = "ADMIN_ASSISTANT"
    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, "Super Admin"),
        (ROLE_ADMIN_ASSISTANT, "Admin Assistant"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_ADMIN_ASSISTANT)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class Country(models.Model):
    """Countries supported by the marketplace (starts with Benin)."""

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    """Administrative department tied to a country (e.g., Littoral)."""

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.name} ({self.country.code})"


class Commune(models.Model):
    """City/commune within a department."""

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="communes")
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Arrondissement(models.Model):
    """Arrondissement nested under a commune."""

    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="arrondissements")
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Zone(models.Model):
    """Neighborhood or point of interest used for fine-grained searches."""

    TYPE_CHOICES = [
        ("QUARTIER", "Quartier"),
        ("REPERE", "Point de repère"),
        ("ZONE", "Zone"),
    ]

    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    synonyms = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return self.name


class Listing(models.Model):
    """Rental listing with hierarchical location and publication lifecycle."""

    STATUS_DRAFT = "DRAFT"
    STATUS_PENDING = "PENDING"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_REJECTED = "REJECTED"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_PENDING, "En attente"),
        (STATUS_PUBLISHED, "Publié"),
        (STATUS_REJECTED, "Rejeté"),
    ]

    TYPE_CHOICES = [
        ("CHAMBRE", "Chambre"),
        ("STUDIO", "Studio"),
        ("APPARTEMENT", "Appartement"),
        ("VILLA", "Villa"),
    ]

    DUREE_CHOICES = [("JOUR", "Jour"), ("MOIS", "Mois"), ("ANNEE", "Année")]
    STANDING_CHOICES = [("BASIQUE", "Basique"), ("MOYEN", "Moyen"), ("HAUT", "Haut")]

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, max_length=255, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="XOF")
    type_logement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    standing = models.CharField(max_length=20, choices=STANDING_CHOICES)
    is_meuble = models.BooleanField(default=False)
    duree = models.CharField(max_length=10, choices=DUREE_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="listings")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="listings")
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT, related_name="listings")
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.PROTECT, related_name="listings")
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="listings")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    whatsapp_phone = models.CharField(max_length=32)
    whatsapp_clicks = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_listings")
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="validated_listings",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            GinIndex(
                SearchVector(
                    "title",
                    "description",
                    "zone__name",
                    "zone__synonyms",
                    config="french",
                ),
                name="listings_fts_idx",
            )
        ]

    def clean(self) -> None:
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

        # Ensure a non-empty, unique slug is always present even when admin inputs are sparse.
        if not self.slug:
            self.slug = self._generate_unique_slug()
        elif Listing.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
            self.slug = self._generate_unique_slug()

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug or Listing.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self) -> str:
        """Create a stable slug from the title and ensure uniqueness without leaking DB errors."""

        base_slug = slugify(self.title or "listing")[:240]
        candidate = base_slug or "listing"
        suffix = 1

        while Listing.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
            suffix += 1
            candidate = f"{base_slug}-{suffix}" if base_slug else f"listing-{suffix}"

        return candidate


class ListingMedia(models.Model):
    """Media assets attached to listings, enabling galleries and thumbnails."""

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="media",
    )
    file = models.ImageField(upload_to="listing_media/")
    caption = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]
        indexes = [models.Index(fields=["listing", "position"])]

    def __str__(self) -> str:
        return f"Media for {self.listing.title}"


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
