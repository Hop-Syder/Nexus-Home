"""Custom DRF permissions enforcing Nexus-Home admin role boundaries."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    """Allow access only to super admins."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == "SUPER_ADMIN")


class IsAdminOrAssistant(BasePermission):
    """Allow authenticated admins or assistants to access admin endpoints."""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {"SUPER_ADMIN", "ADMIN_ASSISTANT"}
        )

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)


class AssistantReadCreateOnly(BasePermission):
    """Block assistants from destructive actions while allowing creation and reads."""

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == "SUPER_ADMIN":
            return True
        if request.user.role == "ADMIN_ASSISTANT":
            return request.method in SAFE_METHODS or request.method in {"POST", "PUT", "PATCH"}
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
