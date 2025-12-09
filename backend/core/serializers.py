"""Serializers translating Nexus-Home models to API-friendly representations."""
from __future__ import annotations

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import (
    Arrondissement,
    Commune,
    Country,
    Department,
    Listing,
    User,
    Zone,
)


class LoginSerializer(serializers.Serializer):
    """Validate credentials for admin login flows."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials provided.")
        attrs["user"] = user
        return attrs


class ZoneSerializer(serializers.ModelSerializer):
    """Expose minimal zone data for listings and filters."""

    class Meta:
        model = Zone
        fields = ["id", "name", "type", "synonyms"]


class ZoneSearchSerializer(serializers.ModelSerializer):
    """Expose zone suggestions with human-readable breadcrumbs for auto-complete."""

    arrondissement_name = serializers.CharField(source="arrondissement.name", read_only=True)
    commune_name = serializers.CharField(
        source="arrondissement.commune.name", read_only=True
    )
    department_name = serializers.CharField(
        source="arrondissement.commune.department.name", read_only=True
    )
    country_name = serializers.CharField(
        source="arrondissement.commune.department.country.name", read_only=True
    )

    class Meta:
        model = Zone
        fields = [
            "id",
            "name",
            "type",
            "synonyms",
            "arrondissement_name",
            "commune_name",
            "department_name",
            "country_name",
        ]


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for public listing consumption with embedded zone details."""

    zone = ZoneSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "currency",
            "type_logement",
            "standing",
            "is_meuble",
            "duree",
            "commune",
            "zone",
            "whatsapp_phone",
            "status",
        ]
        read_only_fields = ["status"]


class ListingAdminSerializer(serializers.ModelSerializer):
    """Admin serializer enabling CRUD while protecting system-managed fields."""

    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source="country", write_only=True, required=False
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True, required=False
    )
    commune_id = serializers.PrimaryKeyRelatedField(
        queryset=Commune.objects.all(), source="commune", write_only=True, required=False
    )
    arrondissement_id = serializers.PrimaryKeyRelatedField(
        queryset=Arrondissement.objects.all(), source="arrondissement", write_only=True, required=False
    )
    zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(), source="zone", write_only=True, required=False
    )

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "currency",
            "type_logement",
            "standing",
            "is_meuble",
            "duree",
            "country",
            "department",
            "commune",
            "arrondissement",
            "zone",
            "latitude",
            "longitude",
            "whatsapp_phone",
            "status",
            "country_id",
            "department_id",
            "commune_id",
            "arrondissement_id",
            "zone_id",
        ]
        read_only_fields = [
            "id",
            "country",
            "department",
            "commune",
            "arrondissement",
            "zone",
        ]

    def validate_price(self, value: int) -> int:
        """Prevent negative values so pricing logic remains coherent."""

        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def _hydrate_locations(self, attrs: dict) -> dict:
        """Fill missing hierarchical location fields based on the provided zone/arrondissement."""

        instance = getattr(self, "instance", None)

        # Preserve existing instance values when an update only touches a subset of fields.
        if instance:
            for field in ["zone", "arrondissement", "commune", "department", "country"]:
                attrs.setdefault(field, getattr(instance, field))

        zone = attrs.get("zone")
        if zone and not attrs.get("arrondissement"):
            attrs["arrondissement"] = zone.arrondissement

        arrondissement = attrs.get("arrondissement")
        if arrondissement and not attrs.get("commune"):
            attrs["commune"] = arrondissement.commune

        commune = attrs.get("commune")
        if commune and not attrs.get("department"):
            attrs["department"] = commune.department

        department = attrs.get("department")
        if department and not attrs.get("country"):
            attrs["country"] = department.country

        missing = [
            field_name
            for field_name in ["country", "department", "commune", "arrondissement", "zone"]
            if attrs.get(field_name) is None
        ]
        if missing:
            raise serializers.ValidationError(
                {"location": f"Champs localisation manquants: {', '.join(missing)}"}
            )

        return attrs

    def create(self, validated_data: dict) -> Listing:
        """Create listings while auto-populating the location chain from provided IDs."""

        hydrated = self._hydrate_locations(validated_data)
        return super().create(hydrated)

    def update(self, instance: Listing, validated_data: dict) -> Listing:
        """Update listings safely while retaining location consistency."""

        hydrated = self._hydrate_locations(validated_data)
        return super().update(instance, hydrated)


class LocationSerializer(serializers.ModelSerializer):
    """Compact serializer for location levels used by filters."""

    class Meta:
        model = Zone
        fields = ["id", "name", "type"]


class CommuneSerializer(serializers.ModelSerializer):
    """Expose communes for hierarchical selection."""

    class Meta:
        model = Commune
        fields = ["id", "name", "department"]


class CountrySerializer(serializers.ModelSerializer):
    """Expose countries for completeness; defaults to Bénin."""

    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class DepartmentSerializer(serializers.ModelSerializer):
    """Expose departments nested under a country."""

    class Meta:
        model = Department
        fields = ["id", "name", "country"]


class ArrondissementSerializer(serializers.ModelSerializer):
    """Expose arrondissements nested under a commune."""

    class Meta:
        model = Arrondissement
        fields = ["id", "name", "commune"]


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
