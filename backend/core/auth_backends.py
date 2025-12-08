"""Authentication backend that uses email as the user identifier."""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """Authenticate against the User model using the email field."""

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        user_model = get_user_model()
        login_identifier = email or username
        if not login_identifier:
            return None
        try:
            user = user_model.objects.get(email=login_identifier)
        except user_model.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None


# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
