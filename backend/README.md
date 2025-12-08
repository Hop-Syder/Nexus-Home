# Backend Django REST Framework

## 🎯 Objectif
Fournir une API sécurisée pour la marketplace Nexus-Home : gestion des annonces, localisations hiérarchiques (pays → département → commune → arrondissement → zone/quartier), médias, utilisateurs et rôles (super admin vs admin assistant), avec recherche full-text performante.

## 🚧 Architecture applicative
- `apps/locations` : tables pays/départements/communes/arrondissements/zones + synchro de synonymes pour la recherche
- `apps/listings` : annonces, types de logement, équipements, disponibilité, tarification, soft delete
- `apps/users` : utilisateurs internes + rôles/permissions, audit log
- `apps/media` : gestion des fichiers (S3 compatible), génération de vignettes
- `apps/search` : configuration tsvector, index GIN, éventuellement passerelle Meilisearch
- `config/` : settings Django (sécurité, CORS, DRF, logging), urls, wsgi/asgi

## 🔐 Sécurité & conformité
- Auth : Django auth + JWT (djoser/dj-rest-auth) avec cookies httpOnly ; option 2FA pour l’admin
- Permissions : Groupes `SUPER_ADMIN` (plein droit) et `ADMIN_ASSISTANT` (pouvoir limité). Guards par vue + filtres par objet si besoin
- Validation : Serializers DRF + validators personnalisés ; sanitation des champs texte
- Protection : rate limiting (throttling DRF), CORS restrictif, sécurité headers (CSP, HSTS), rotation des secrets via env
- Audit : middleware de journalisation des actions critiques (validation, suppression, changement de rôle)

## 🗄️ Modèle de données (aperçu)
- `Country`, `Department`, `Commune`, `District` (arrondissement), `Zone` (quartier/repère, avec synonymes)
- `Listing` : titre, description, type, prix, durée, meublé, disponibilité, localisation FK, lat/long, statut (draft/published/archived)
- `MediaAsset` : fichier, type, ordre, taille, dimensions ; stockage S3 avec URLs signées pour l’admin
- `User` : profil interne, rôle, journal d’actions

## 🧪 Tests recommandés
- Unitaires sur serializers, permissions, services (upload, recherche)
- Intégration API : auth, CRUD annonces, filtres (prix, localisation, meublé), recherche full-text, rôles
- Sécurité : throttling, CORS, accès admin, injection XSS/SQL bloquées

## 🛠️ Démarrage (Docker)
1. Créer `.env` depuis `.env.example` (DB, SECRET_KEY, JWT, S3).
2. `docker compose up --build api` pour lancer l’API et Postgres.
3. `docker compose exec api python manage.py migrate` puis `createsuperuser`.
4. Importer les données de localisation de base (script management command à prévoir).
5. Vérifier l’API : `http://localhost:8000/api/health/`.

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
