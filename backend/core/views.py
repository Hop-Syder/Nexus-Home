"""DRF views implementing public listings and admin workflows for Nexus-Home."""
from __future__ import annotations

from django.contrib.auth import login
from django.db import models
from django.db.models import Q, Count, Sum
from django.db import connection
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Arrondissement, Commune, Country, Department, Listing, ListingMedia, Zone
from .permissions import AssistantReadCreateOnly, IsAdminOrAssistant, IsSuperAdmin
from .serializers import (
    ArrondissementSerializer,
    CommuneSerializer,
    CountrySerializer,
    DepartmentSerializer,
    ListingAdminSerializer,
    ListingMediaSerializer,
    ListingSerializer,
    LoginSerializer,
    StatsOverviewSerializer,
    TopZoneSerializer,
    ZoneSerializer,
    ZoneSearchSerializer,
)


class LoginView(generics.GenericAPIView):
    """Authenticate admin users and return a persistent token for API access."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)

        # Use DRF's Token model to issue an API-friendly credential without leaking session details.
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"access_token": token.key, "token_type": "bearer"})


class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only access to published listings with lightweight filters."""

    serializer_class = ListingSerializer
    queryset = Listing.objects.filter(status=Listing.STATUS_PUBLISHED).prefetch_related(
        "media", "zone", "commune"
    )
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        q = params.get("q")
        if q:
            if connection.vendor == "postgresql":
                search_vector = SearchVector(
                    "title",
                    "description",
                    "zone__name",
                    "zone__synonyms",
                    config="french",
                )
                search_query = SearchQuery(q, config="french")
                qs = (
                    qs.annotate(search_rank=SearchRank(search_vector, search_query))
                    .filter(search_vector=search_query)
                    .order_by("-search_rank")
                )
            else:
                lowered = q.lower()
                qs = qs.filter(
                    Q(title__icontains=lowered)
                    | Q(description__icontains=lowered)
                    | Q(zone__name__icontains=lowered)
                    | Q(zone__synonyms__icontains=lowered)
                )
        price_min = params.get("price_min")
        price_max = params.get("price_max")
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if params.get("commune_id"):
            qs = qs.filter(commune_id=params.get("commune_id"))
        if params.get("zone_id"):
            qs = qs.filter(zone_id=params.get("zone_id"))
        if params.get("type_logement"):
            qs = qs.filter(type_logement=params.get("type_logement"))
        if params.get("standing"):
            qs = qs.filter(standing=params.get("standing"))
        if params.get("is_meuble"):
            qs = qs.filter(is_meuble=params.get("is_meuble") in {"true", "1", "True"})
        if params.get("duree"):
            qs = qs.filter(duree=params.get("duree"))
        return qs

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        Listing.objects.filter(pk=listing.pk).update(views_count=models.F("views_count") + 1)
        serializer = self.get_serializer(listing)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[AllowAny], url_path="whatsapp-click")
    def whatsapp_click(self, request, *args, **kwargs):
        """Track WhatsApp CTA usage to inform conversion metrics without blocking the user."""

        listing = self.get_object()
        Listing.objects.filter(pk=listing.pk).update(
            whatsapp_clicks=models.F("whatsapp_clicks") + 1
        )
        listing.refresh_from_db(fields=["whatsapp_clicks"])
        return Response({"whatsapp_clicks": listing.whatsapp_clicks})


class AdminListingViewSet(viewsets.ModelViewSet):
    """Admin CRUD endpoints with role-aware restrictions and validation actions."""

    serializer_class = ListingAdminSerializer
    queryset = Listing.objects.all()
    permission_classes = [IsAdminOrAssistant, AssistantReadCreateOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        new_status = serializer.validated_data.get("status")
        if self.request.user.role == "ADMIN_ASSISTANT" and new_status == Listing.STATUS_PUBLISHED:
            raise PermissionDenied("Assistants cannot publish listings.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "ADMIN_ASSISTANT":
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[IsSuperAdmin])
    def validate(self, request, pk=None):
        listing = self.get_object()
        listing.status = Listing.STATUS_PUBLISHED
        listing.validated_by = request.user
        listing.save(update_fields=["status", "validated_by"])
        serializer = self.get_serializer(listing)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsSuperAdmin])
    def reject(self, request, pk=None):
        listing = self.get_object()
        listing.status = Listing.STATUS_REJECTED
        listing.validated_by = request.user
        listing.save(update_fields=["status", "validated_by"])
        serializer = self.get_serializer(listing)
        return Response(serializer.data)


class ListingMediaUploadView(generics.GenericAPIView):
    """Handle secure uploads of listing media for admins and assistants."""

    permission_classes = [IsAdminOrAssistant]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ListingMediaSerializer

    def post(self, request, listing_id: int, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=listing_id)
        if request.user.role == "ADMIN_ASSISTANT" and listing.status == Listing.STATUS_PUBLISHED:
            raise PermissionDenied("Assistants cannot modifier les médias d'une annonce publiée.")

        upload = request.FILES.get("file")
        if upload is None:
            return Response({"detail": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST)

        caption = request.data.get("caption", "")
        position_raw = request.data.get("position", "0")
        try:
            position = max(0, int(position_raw))
        except (TypeError, ValueError):
            position = 0

        media = ListingMedia.objects.create(
            listing=listing,
            file=upload,
            caption=caption,
            position=position,
        )
        serializer = ListingMediaSerializer(media, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, listing_id: int, media_id: int, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=listing_id)
        media = get_object_or_404(ListingMedia, pk=media_id, listing=listing)
        if request.user.role == "ADMIN_ASSISTANT":
            return Response(status=status.HTTP_403_FORBIDDEN)

        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountryListView(generics.ListAPIView):
    """Expose supported countries (defaults to Bénin)."""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DepartmentListView(generics.ListAPIView):
    """Expose departments filtered by country when provided."""

    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        country_id = self.request.query_params.get("country_id")
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class CommuneListView(generics.ListAPIView):
    """Expose communes filtered by department when requested."""

    serializer_class = CommuneSerializer

    def get_queryset(self):
        queryset = Commune.objects.all()
        department_id = self.request.query_params.get("department_id")
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class ArrondissementListView(generics.ListAPIView):
    """Expose arrondissements filtered by commune when available."""

    serializer_class = ArrondissementSerializer

    def get_queryset(self):
        queryset = Arrondissement.objects.all()
        commune_id = self.request.query_params.get("commune_id")
        if commune_id:
            queryset = queryset.filter(commune_id=commune_id)
        return queryset


class ZoneListView(generics.ListAPIView):
    """Expose zones filtered by arrondissement for precision."""

    serializer_class = ZoneSerializer

    def get_queryset(self):
        queryset = Zone.objects.all()
        arrondissement_id = self.request.query_params.get("arrondissement_id")
        if arrondissement_id:
            queryset = queryset.filter(arrondissement_id=arrondissement_id)
        return queryset


class ZoneSearchView(generics.ListAPIView):
    """Return zone suggestions with contextual breadcrumbs for auto-complete."""

    serializer_class = ZoneSearchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        raw_query = (self.request.query_params.get("q") or "").strip()
        if len(raw_query) < 2:
            # Avoid returning everything when the query is missing or too short to keep the endpoint cheap and safe.
            return Zone.objects.none()

        normalized = raw_query.lower()
        base_queryset = Zone.objects.select_related(
            "arrondissement__commune__department__country"
        ).filter(Q(name__icontains=normalized) | Q(synonyms__icontains=normalized))

        limit_param = self.request.query_params.get("limit", "20")
        try:
            limit = max(1, min(int(limit_param), 50))
        except ValueError:
            limit = 20

        # Enforce a bounded result set to prevent expensive queries while keeping suggestions quick for users.
        return base_queryset.order_by("name")[:limit]


class AdminStatsOverviewView(generics.GenericAPIView):
    """Return lifecycle and engagement stats for admins and assistants."""

    permission_classes = [IsAdminOrAssistant]
    serializer_class = StatsOverviewSerializer

    def get(self, request, *args, **kwargs):
        aggregates = Listing.objects.aggregate(
            total=Count("id"),
            published=Count("id", filter=Q(status=Listing.STATUS_PUBLISHED)),
            pending=Count("id", filter=Q(status=Listing.STATUS_PENDING)),
            draft=Count("id", filter=Q(status=Listing.STATUS_DRAFT)),
            rejected=Count("id", filter=Q(status=Listing.STATUS_REJECTED)),
            views=Sum("views_count"),
            whatsapp_clicks=Sum("whatsapp_clicks"),
        )
        aggregates["views"] = aggregates["views"] or 0
        aggregates["whatsapp_clicks"] = aggregates["whatsapp_clicks"] or 0
        serializer = self.get_serializer(aggregates)
        return Response(serializer.data)


class AdminTopZonesView(generics.GenericAPIView):
    """Return the most active zones to inform supply and moderation focus."""

    permission_classes = [IsAdminOrAssistant]
    serializer_class = TopZoneSerializer

    def get(self, request, *args, **kwargs):
        raw_limit = request.query_params.get("limit", "5")
        try:
            limit = max(1, min(int(raw_limit), 20))
        except ValueError:
            limit = 5

        ranking = (
            Listing.objects.filter(status=Listing.STATUS_PUBLISHED)
            .values(
                "zone_id",
                "zone__name",
                "zone__arrondissement__commune__name",
            )
            .annotate(listing_count=Count("id"))
            .order_by("-listing_count", "zone__name")[:limit]
        )

        payload = [
            {
                "zone_id": row["zone_id"],
                "zone_name": row["zone__name"],
                "commune_name": row["zone__arrondissement__commune__name"],
                "listing_count": row["listing_count"],
            }
            for row in ranking
        ]

        serializer = self.get_serializer(payload, many=True)
        return Response(serializer.data)


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
