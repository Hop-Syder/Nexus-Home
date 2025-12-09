# Backend Django REST Framework

## 🎯 Objectif
Fournir une API sécurisée pour la marketplace Nexus-Home : gestion des annonces, localisations hiérarchiques (pays → département → commune → arrondissement → zone/quartier), médias, utilisateurs et rôles (super admin vs admin assistant), avec recherche full-text performante.

## 🚧 Architecture applicative
- `apps/locations` : tables pays/départements/communes/arrondissements/zones + synchro de synonymes pour la recherche
- `apps/listings` : annonces, types de logement, équipements, disponibilité, tarification, soft delete
- `apps/users` : utilisateurs internes + rôles/permissions, audit log
- `apps/media` : gestion des fichiers (S3 compatible), génération de vignettes (MVP: stockage local sécurisé)
- `apps/search` : configuration tsvector, index GIN, éventuellement passerelle Meilisearch
- `config/` : settings Django (sécurité, CORS, DRF, logging), urls, wsgi/asgi

## 🔐 Sécurité & conformité
- Auth : Django auth + tokens DRF (MVP) ou JWT (djoser/dj-rest-auth) avec cookies httpOnly ; option 2FA pour l’admin
- Permissions : Groupes `SUPER_ADMIN` (plein droit) et `ADMIN_ASSISTANT` (pouvoir limité). Guards par vue + filtres par objet si besoin
- Validation : Serializers DRF + validators personnalisés ; sanitation des champs texte
- Protection : rate limiting (throttling DRF), CORS restrictif, sécurité headers (CSP, HSTS), rotation des secrets via env
- Audit : middleware de journalisation des actions critiques (validation, suppression, changement de rôle)

## 🗄️ Modèle de données (aperçu)
- `Country`, `Department`, `Commune`, `District` (arrondissement), `Zone` (quartier/repère, avec synonymes)
- `Listing` : titre, description, type, prix, durée, meublé, disponibilité, localisation FK, lat/long, statut (draft/published/archived)
- `MediaAsset` : fichier, légende, ordre, horodatage ; stockage local configurable via `DJANGO_MEDIA_ROOT`/`DJANGO_MEDIA_URL`
- `User` : profil interne, rôle, journal d’actions

## 🌐 Endpoints clés (v1)
- Public :
- `GET /api/v1/listings` + `/api/v1/listings/{slug}` (slug unique, auto-généré)
  - Localisations : `/api/v1/locations/countries|departments|communes|arrondissements|zones`
  - Auto-complétion : `/api/v1/locations/search?q=` pour proposer les zones/quartiers (synonymes inclus)
- Admin :
  - `POST /api/v1/auth/login` (token)
  - `GET/POST/PUT/DELETE /api/v1/admin/listings`
- Actions : `POST /api/v1/admin/listings/{id}/validate` et `/reject` (réservé super admin)
  - Médias : `POST /api/v1/admin/listings/{id}/media` (upload image) et `DELETE /api/v1/admin/listings/{id}/media/{media_id}` (suppression super admin)
  - Statistiques : `GET /api/v1/admin/stats/overview` (compteurs, vues) et `GET /api/v1/admin/stats/top-zones?limit=5`

## 🧪 Tests recommandés
- Unitaires sur serializers, permissions, services (upload, recherche)
- Intégration API : auth, CRUD annonces, filtres (prix, localisation, meublé), recherche full-text, rôles
- Sécurité : throttling, CORS, accès admin, injection XSS/SQL bloquées
- Suite backend complète : `pytest -v backend/tests --ds=<votre_module_settings>` (fixtures DRF + modèles décrits dans `check-backend2.md`).

## 🛠️ Démarrage (Docker)
1. Créer `.env` depuis `.env.example` (DB, SECRET_KEY, JWT, S3).
2. Définir `DATABASE_URL` (Supabase/PostgreSQL) pour activer la recherche full-text et les index GIN ; sinon SQLite est utilisé pour le dev local.
3. `docker compose up --build api` pour lancer l’API et Postgres.
4. `docker compose exec api python manage.py migrate` puis `createsuperuser`.
5. Importer les données de localisation de base (script management command à prévoir).
6. Vérifier l’API publique : `http://localhost:8000/api/v1/listings/`.
7. Vérifier le stockage média local : `DJANGO_MEDIA_ROOT` doit être inscriptible (volume Docker recommandé).

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
