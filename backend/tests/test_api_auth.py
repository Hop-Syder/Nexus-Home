"""Authentication coverage for admin login flows."""

import pytest
from django.urls import reverse


@pytest.mark.requirement("ADMIN_LOGIN")
@pytest.mark.django_db
def test_super_admin_can_login(api_client, super_admin):
    """Validate that a super admin receives an access token."""
    login_url = reverse("auth-login")
    payload = {"email": "admin@test.com", "password": "admin123"}
    response = api_client.post(login_url, payload, format="json")
    assert response.status_code == 200
    body = response.json()
    assert any(key in body for key in ["access", "access_token"]) is True


@pytest.mark.django_db
def test_invalid_credentials_are_rejected(api_client):
    """Invalid credentials should never authenticate."""
    login_url = reverse("auth-login")
    payload = {"email": "unknown@test.com", "password": "wrong"}
    response = api_client.post(login_url, payload, format="json")
    assert response.status_code in (400, 401)


# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
