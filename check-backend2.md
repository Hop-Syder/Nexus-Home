# Check Backend 2 🛡️

## 🎯 Objectif
Cadre de validation complet pour le backend **Django + DRF** de Nexus-Home : modèles, API publique, API admin, permissions, recherche full-text et hiérarchie de localisation, exécuté avec **pytest-django** sur Postgres/Supabase.

## 🧰 Prérequis
- Python 3.11+
- PostgreSQL/Supabase accessible (lecture/écriture de test)
- Variables d'environnement configurées :
  - `DJANGO_SETTINGS_MODULE` (ex. `backend.settings`)
  - `DATABASE_URL` ou `SUPABASE_DB_URL`
- Paquets : `pytest`, `pytest-django`, `pytest-cov`, `Django`, `djangorestframework` (installés via `requirements-dev.txt`).

## 📁 Structure de tests
- `backend/tests/conftest.py` → fixtures Django/DRF (APIClient, comptes super admin & assistant, localisation, annonce publiée).
- `backend/tests/test_models_locations.py` → intégrité de la hiérarchie Pays → Département → Commune → Arrondissement → Zone (synonymes inclus).
- `backend/tests/test_models_listings.py` → validations Listing (prix non négatif, rendu `__str__`).
- `backend/tests/test_api_auth.py` → login admin (token attendu) + échec credentials invalides.
- `backend/tests/test_api_listings_public.py` → recherche texte, filtres commune/zone/prix/type, contact WhatsApp.
- `backend/tests/test_api_listings_admin.py` → CRUD, publication, blocage assistant.
- `backend/tests/test_api_permissions.py` → interdiction d'accès admin en anonyme, gestion des users interdite aux assistants.
- `backend/tests/test_api_search.py` → couverture full-text/synonymes.

## 🛡️ Garde-fous & bonnes pratiques
- Données de test créées via fixtures : rollback auto par `pytest-django`.
- Aucun secret en dur : tout passe par variables d'environnement.
- URLs d'API à adapter dans `urls.py` pour exposer les routes :
  - public : `listings-list`, `listings-detail`
  - admin : `admin-listings-list`, `admin-listings-detail`, `admin-listings-validate`, `admin-users-list`
  - auth : `auth-login`
- Statuts d'annonces attendus : `DRAFT`, `PENDING`, `PUBLISHED`.

## ⏱️ Commandes de vérification
```bash
# 1) Installer les dépendances dev
pip install -r requirements-dev.txt

# 2) Exporter vos variables d'env
export DJANGO_SETTINGS_MODULE="backend.settings"  # adapter à votre projet
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# 3) Lancer le check backend complet avec marquage requirement
pytest -v backend/tests --maxfail=1 --disable-warnings

# 4) Rapport de couverture (optionnel)
pytest -v backend/tests --cov=core --cov-report=term-missing
```

## 📍 Mapping exigences → tests
- **USER_SEARCH_TEXT** : `test_api_listings_public.py::test_user_can_search_by_text`
- **USER_FILTERS_BASIC** : `test_api_listings_public.py::test_user_can_filter_by_location_and_price`
- **USER_WHATSAPP_BUTTON** : `test_api_listings_public.py::test_listing_detail_exposes_whatsapp_contact`
- **NO_ONLINE_PAYMENT** : à couvrir par la sécurisation des routes (aucun endpoint paiement)
- **ADMIN_LOGIN** : `test_api_auth.py::test_super_admin_can_login` + interdiction anonyme `test_api_permissions.py`
- **ADMIN_CRUD_LISTINGS** : `test_api_listings_admin.py::test_super_admin_can_create_and_delete_listing`
- **ADMIN_VALIDATE_LISTINGS** : `test_api_listings_admin.py::test_super_admin_can_publish_listing`
- **ADMIN_ASSISTANT_LIMITED** : `test_api_listings_admin.py::test_assistant_cannot_publish_or_delete_listing`
- **DB_LOCATION_HIERARCHY** : `test_models_locations.py::test_location_hierarchy_creation`
- **SEARCH_FULLTEXT** : `test_api_search.py::test_search_returns_relevant_results`

## 🛠️ Débogage rapide
- 📦 **Import introuvable** : vérifiez que vos apps Django (`core`, etc.) sont dans `INSTALLED_APPS` et que `DJANGO_SETTINGS_MODULE` pointe vers le bon fichier.
- 🏛️ **Base inaccessible** : contrôlez `DATABASE_URL` et les rôles Postgres (l'utilisateur doit avoir `CREATE/DROP` sur la DB de test).
- 🔐 **Auth KO** : confirmez que les utilisateurs de fixtures ne sont pas modifiés par un signal, ou définissez des mots de passe cohérents avec votre backend.
- ⚠️ **Routes 404** : exposez les URL nommées listées plus haut via vos fichiers `urls.py` ou ajustez les noms dans les tests.

---
# ──────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────
