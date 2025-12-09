# Nexus-Home Marketplace Blueprint

## 🎯 Description du Projet
Plateforme web moderne pour trouver et gérer des annonces de locations de chambres ou appartements à Cotonou. La web-app sépare clairement les parcours utilisateur (recherche, filtres rapides, contact WhatsApp) et administrateur (validation, édition, gestion des assistants) pour offrir une expérience fluide sur mobile et desktop, sans paiement en ligne.

## 📁 Structure des Fichiers (proposée)
```
Nexus-Home/
├── frontend/                 # Next.js (router pages) pour User + Admin
│   ├── components/           # Layout, thèmes, cartes, filtres
│   ├── hooks/                # Hooks communs (useTheme)
│   ├── lib/                  # Client API (NEXT_PUBLIC_API_BASE_URL)
│   ├── pages/                # Pages publiques + placeholder admin
│   ├── styles/               # Design tokens confort 18–90 ans
│   └── README.md             # Consignes d'architecture et setup
├── backend/                  # API Django REST Framework
│   ├── core/                 # Modules (listings, locations, users, media, logs)
│   ├── backend/              # Paramètres Django, sécurité, logging
│   └── README.md             # Setup backend, migrations, sécurité
├── docs/
│   └── architecture.md       # Design technique, données, API, sécurité
├── plan.md                   # Plan d'exécution priorisé (tâches phases 0-3)
├── docs/commission-verification.md # Checklist de conformité (user/admin/search/localisation)
├── requirements-check.js     # Script Node pour suivre l'état des exigences
└── README.md                 # Vue d'ensemble, instructions communes
```

## 🧱 Stack recommandée
- **Frontend** : Next.js 14, TypeScript, Tailwind CSS (+ shadcn/ui), React Hook Form + Zod, NextAuth (ou auth cookie JWT)
- **Backend** : Django 5 + Django REST Framework, django-filter, djoser (ou dj-rest-auth) pour auth API
- **Base de données** : PostgreSQL (+ PostGIS pour filtres par distance optionnels)
- **Recherche** : V1 PostgreSQL full-text (tsvector + index GIN) ; V2 Meilisearch si besoin d’auto-complétion tolérante
- **Stockage média** : S3 compatible (minio / Cloud), génération thumbnails WebP, CDN conseillé
- **CI/CD** : GitHub Actions (lint, tests, build), déploiement Docker sur VPS/Render/Fly.io ; frontend possible sur Vercel/Netlify

## 🛡️ Considérations de Sécurité
- Validation systématique des entrées (Zod côté front, DRF + serializers côté back)
- Authentification forte pour l’admin (mots de passe hashés, 2FA recommandé), sessions/httpOnly cookies
- Rôles et permissions : Super Admin (plein droit) / Admin Assistant (pouvoir limité) via Groups/Permissions Django
- Protection API publique : rate limiting, CORS contrôlé, logs d’audit pour chaque action sensible
- Secrets uniquement via variables d’environnement (.env), jamais en dur ; rotation régulière
- Stockage des médias avec liens signés pour l’admin si modification/suppression

## 📌 Fonctionnalités prioritaires
- Recherche rapide : mots-clés + filtres (ville/commune, arrondissement, quartier/zone, prix, type, meublé, durée)
- Fiches annonces : photos optimisées, localisation hiérarchique, bouton WhatsApp pré-rempli
- Admin : workflow de validation/rejet, édition versionnée, suppression sécurisée (soft delete), journalisation et filtres par statut
- Gestion des assistants : droits restreints (pas de suppression définitive, validation réservée au super admin)
- Préparation cartographie : stockage latitude/longitude pour future vue carte et recherche par rayon

## 🌐 API REST (v1)
- Public :
  - `GET /listings` (texte + filtres) ; `GET /listings/{id}`
  - Localisation hiérarchique : `GET /locations/countries`, `/departments`, `/communes`, `/arrondissements`, `/zones`
  - Auto-complétion : `GET /locations/search?q=` (zones/quartiers avec contexte commune/arrondissement)
- Admin :
  - `POST /auth/login`
  - `GET/POST/PUT/DELETE /admin/listings` + actions `POST /admin/listings/{id}/validate|reject`
  - Règles : assistants ne publient ni ne suppriment ; seul le super admin valide/rejette.

## 🗺️ Plan d'exécution
- Les tâches détaillées par phase (préparation, MVP, recherche avancée, scalabilité) et le design system confort 18–90 ans sont dans `plan.md` pour pilotage backlog et cohérence UX.

## 🧾 Vérification de conformité
- La checklist formelle se trouve dans `docs/commission-verification.md` (rôles, critères user/admin, technique, UX).
- Le suivi automatisé se fait via `node requirements-check.js` (statuts done/partial/todo à tenir à jour chaque sprint).
- Le dossier `tests/` fournit des tests pytest prêts à exécuter pour contrôler API, rôles et schéma Supabase/PostgreSQL ; voir `son.md` pour la marche à suivre et les variables d'environnement.
- Le guide `check-backend2.md` détaille le protocole pytest-django pour valider le backend Django/DRF (fixtures, routes, mapping des exigences, commandes).

## ✅ Tests à Effectuer
- Frontend : lint (eslint), type-check (tsc), tests unitaires (vitest/jest), tests e2e (playwright) sur parcours recherche/WhatsApp CTA
- Backend : tests unitaires sur serializers/permissions, tests d’intégration API (auth, listings, filtres, recherche full-text)
- Sécurité : vérification CORS, rate limiting, accès admin protégé, couverture des rôles
- Qualité backend/DB : `pytest -v` avec `API_BASE_URL`, `SUPABASE_DB_URL`, `SUPER_ADMIN_EMAIL`, `SUPER_ADMIN_PASSWORD`, `ASSISTANT_EMAIL`, `ASSISTANT_PASSWORD` configurés (tests non destructifs hors créations/suppressions temporaires)

## 🧪 Intégration Continue
- GitHub Actions (`.github/workflows/ci.yml`) exécute automatiquement :
  - les tests backend Django (`pytest backend/tests tests`) en Python 3.11 avec la configuration SQLite par défaut (pas de secrets requis) ;
  - l’audit des exigences métier via `node requirements-check.js` pour vérifier l’état des livrables.
- Avant de pousser, lancer localement `pytest backend/tests tests` et `node requirements-check.js` pour aligner les résultats avec ceux du pipeline.
- Les environnements distants doivent fournir `DATABASE_URL` pour activer Postgres/GIN ; GitHub Actions utilisera la configuration SQLite embarquée pour garder les tests rapides.

## 🚀 Instructions d'Exécution (Docker Compose)
1. Copier `.env.example` en `.env` et renseigner secrets (DB, JWT, stockage S3 si besoin).
2. Installer Docker & Docker Compose.
3. Lancer la stack :

```bash
docker-compose up --build
```

4. Appliquer les migrations Django : `docker-compose exec backend python manage.py migrate`.
5. Créer un superuser : `docker-compose exec backend python manage.py createsuperuser`.
6. Accéder :
   - Frontend utilisateur/admin : `http://localhost:3000`
   - API publique : `http://localhost:8000/api/v1`
   - Postgres : `localhost:5432` (pour outils SQL locaux)

7. Arrêter la stack : `docker-compose down` (ajouter `-v` pour réinitialiser les données locales Postgres).

## 📄 Contribuer
- Nommage explicite, fonctions courtes, pas de duplication (DRY)
- Commentaires centrés sur le **pourquoi** ; aucun secret en dur
- Respect PEP8 / ESLint ; privilégier async/await, hooks React, validations d’inputs systématiques

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
