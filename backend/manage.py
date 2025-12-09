"""Entry point for Django administrative tasks within the Nexus-Home backend."""
import os
import sys


def main() -> None:
    """Execute Django administrative commands with a preconfigured settings module."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - defensive guard
        raise ImportError(
            "Django must be installed to run management commands."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
