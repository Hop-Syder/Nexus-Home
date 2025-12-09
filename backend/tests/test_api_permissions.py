"""Permission boundaries for admin endpoints and anonymous access."""

import pytest
from django.urls import reverse


@pytest.mark.requirement("ADMIN_LOGIN")
@pytest.mark.django_db
def test_anonymous_user_cannot_access_admin_listings(api_client):
    """Anonymous calls to admin endpoints must be rejected."""
    url = reverse("admin-listings-list")
    response = api_client.get(url)
    assert response.status_code in (401, 403)


@pytest.mark.requirement("ADMIN_ASSISTANT_LIMITED")
@pytest.mark.django_db
def test_assistant_cannot_access_user_management(assistant_client):
    """Assistants must not manage other admin accounts."""
    url = reverse("admin-users-list")
    response = assistant_client.get(url)
    assert response.status_code in (401, 403)


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
