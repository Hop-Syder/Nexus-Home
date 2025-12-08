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
        ]
        read_only_fields = ["id"]

    def validate_price(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


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
