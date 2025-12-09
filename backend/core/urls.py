"""URL routing for public listings, admin actions, and location resources."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminListingViewSet,
    ArrondissementListView,
    CommuneListView,
    CountryListView,
    DepartmentListView,
    ListingMediaUploadView,
    ListingViewSet,
    LoginView,
    ZoneListView,
    ZoneSearchView,
)

router = DefaultRouter()
router.register("listings", ListingViewSet, basename="listings")
router.register("admin/listings", AdminListingViewSet, basename="admin-listings")

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="auth-login"),
    path("", include(router.urls)),
    path(
        "admin/listings/<int:listing_id>/media",
        ListingMediaUploadView.as_view(),
        name="admin-listing-media",
    ),
    path(
        "admin/listings/<int:listing_id>/media/<int:media_id>",
        ListingMediaUploadView.as_view(),
        name="admin-listing-media-detail",
    ),
    path("locations/countries", CountryListView.as_view(), name="locations-countries"),
    path("locations/departments", DepartmentListView.as_view(), name="locations-departments"),
    path("locations/communes", CommuneListView.as_view(), name="locations-communes"),
    path("locations/arrondissements", ArrondissementListView.as_view(), name="locations-arrondissements"),
    path("locations/zones", ZoneListView.as_view(), name="locations-zones"),
    path("locations/search", ZoneSearchView.as_view(), name="locations-search"),
]

# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
