# Nexus-Home Plan exécutable

## 🎯 Objectif du document
Planifier les étapes A→Z pour livrer une marketplace de location (user + admin) avec recherche rapide, filtres précis et contact WhatsApp sans paiement en ligne. Chaque étape est organisée pour un backlog actionnable.

## 📁 Structure cible (rappel)
- **frontend/** : Next.js (apps user/admin), Tailwind, validations Zod.
- **backend/** : Django + DRF, modules accounts/listings/locations/media/logs.
- **docs/** : architecture et décisions techniques.
- **plan.md** : ce plan d'exécution.

## 🧭 Roadmap détaillée
### Phase 0 — Préparation
- [ ] Valider le domaine et les sous-domaines (`app`, `admin`).
- [ ] Créer les dépôts/monorepo et configurer les environnements (.env exemples sécurisés).
- [ ] Mettre en place la CI lint + tests (GitHub Actions) et Docker Compose de base (frontend, backend, postgres).

### Phase 1 — MVP fonctionnel
- [ ] Backend :
  - [ ] Initialiser Django/DRF, créer modèles Users (roles), Listings, Locations, Media.
  - [ ] Exposer API auth (login/logout/me) et CRUD annonces avec statuts (`DRAFT`, `PENDING`, `PUBLISHED`, `REJECTED`).
  - [ ] Endpoints localisation (countries, departments, communes, arrondissements, zones) + recherche libre `q`.
  - [ ] Validation des entrées via serializers, permissions rôle (Super Admin / Admin Assistant), logging d’audit minimal.
- [ ] Frontend User :
  - [ ] Pages Home, Listings (liste + filtres), Listing detail avec CTA WhatsApp prérempli.
  - [ ] Recherche texte + filtres basiques (ville, zone, type, prix, meublé, durée).
  - [ ] Accessibilité (ARIA, labels, contrastes) et performance (SSR/SSG).
- [ ] Frontend Admin :
  - [ ] Authentification et session sécurisée.
  - [ ] Dashboard synthétique (statuts des annonces).
  - [ ] Table des annonces avec création/édition, upload médias, workflow de validation (boutons visibles selon rôle).

### Phase 1.1 — Vérification de conformité MVP
- [ ] Préparer la **commission de vérification** (voir `docs/commission-verification.md`) et désigner les rôles.
- [ ] Exécuter `node requirements-check.js` à chaque fin de sprint et mettre à jour les statuts.
- [ ] Documenter les écarts et actions correctives dans le backlog.

### Phase 2 — Expérience & recherche avancées
- [ ] Auto-complétion et suggestions sur la barre de recherche (zones, types, prix).
- [ ] Synonymes/fautes courantes sur zones (Fidjrossè/Fidjrosse) et types de logement.
- [ ] Filtres enrichis : standing, distance/plage (si coordonnées dispo), disponibilité.
- [ ] Statistiques admin : vues par annonce, top zones, conversion WhatsApp (clics).
- [ ] Gestion des rôles affinée (permissions par action) et journalisation détaillée.

### Phase 3 — Scalabilité & extension
- [ ] Multi-ville/pays (activer le champ country, nouveaux départements/communes).
- [ ] Favoris et comptes utilisateurs publics (optionnel).
- [ ] Vue carte (PostGIS + clustering) et filtre par rayon.
- [ ] Notifications propriétaires (email/WhatsApp Business API) après validation.
- [ ] Optimisation SEO (sitemaps, OpenGraph) et observabilité (traces, logs structurés, métriques).

## 🛡️ Sécurité & conformité
- Validation systématique des inputs (front + back), aucune donnée sensible en dur.
- Sessions sécurisées (cookies httpOnly) ou JWT avec rotation, mots de passe hashés.
- Rôles et permissions appliqués sur chaque endpoint et action UI ; rate limiting public.
- Stockage médias via bucket S3-compatible avec URLs signées pour opérations sensibles.
- Journalisation des actions admin et sauvegardes régulières PostgreSQL.

## 🚀 Lancement (local proposé)
1. Copier `.env.example` vers `.env` et renseigner secrets (DB, JWT, stockage).
2. `docker compose up --build` pour lancer Postgres, backend, frontend.
3. `docker compose exec api python manage.py migrate` puis `createsuperuser`.
4. Accéder aux apps : `http://localhost:3000` (user) et `/admin` (dashboard).

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
