# Nexus-Home Plan exécutable

## 🎯 Objectif du document
Planifier les étapes A→Z pour livrer une marketplace de location (user + admin) avec recherche rapide, filtres précis et contact WhatsApp sans paiement en ligne, tout en intégrant le plan final validé et le design system confortable 18–90 ans.

## 📁 Structure cible (rappel)
- **frontend/** : Next.js (apps user/admin), Tailwind, validations Zod.
- **backend/** : Django + DRF, modules accounts/listings/locations/media/logs.
- **docs/** : architecture, décisions techniques et guides QA/design.
- **plan.md** : ce plan d'exécution fusionné.

## ✅ Plan final validé (cadre à respecter)
- **Stack figée** : Django + DRF, PostgreSQL (Supabase), Next.js + Tailwind, Docker (frontend Vercel, backend VPS/Render/Railway + Supabase). Ne pas changer sans ordre explicite.
- **Fonctionnalités V1 obligatoires** :
  - Côté user : home + listings avec recherche `q`, filtres (commune/ville, zone/quartier, type logement, prix min/max, meublé, durée), fiche détail avec localisation hiérarchique, galerie, CTA WhatsApp pré-rempli, aucun paiement en ligne.
  - Côté admin : login, rôles `SUPER_ADMIN` et `ADMIN_ASSISTANT`, CRUD annonces, statuts `DRAFT|PENDING|PUBLISHED|REJECTED`, assistants limités (pas de publish/suppression/gestion admins), création assistants par super admin.
- **Données** : tables pays/département/commune/arrondissement/zone (avec synonyms JSON et type), listings avec localisation complète, coordonnées optionnelles, whatsapp_phone, views_count, created_by/validated_by.
- **API REST `/api/v1`** : endpoints publics `GET /listings`, `GET /listings/{slug}` ; admin auth/login ; admin listings CRUD + validate/reject ; localisation endpoints complets + search ; pas d’endpoint paiement.
- **Recherche** : full-text PostgreSQL (title, description, localisation) avec index GIN ; requêtes tolérantes pour 3–4 mots clés (ex: "chambre meublée fidjrossè").
- **Tests** : pytest/pytest-django avec marqueurs requirement ; objectif = tous les tests requirement verts (models, API user/admin, rôles, search, localisation, FTS).

## 🧭 Roadmap détaillée
### Phase 0 — Préparation
- [ ] Valider le domaine et les sous-domaines (`app`, `admin`).
- [x] Créer les dépôts/monorepo et configurer les environnements (.env exemples sécurisés).
- [x] Mettre en place la CI lint + tests (GitHub Actions) et Docker Compose de base (frontend, backend, postgres/Supabase proxy).

### Phase 1 — MVP fonctionnel
- [x] Backend :
  - [x] Initialiser Django/DRF, créer modèles Users (roles), Listings, Locations, Media selon le modèle validé.
  - [x] Exposer API auth (login/logout/me) et CRUD annonces avec statuts (`DRAFT`, `PENDING`, `PUBLISHED`, `REJECTED`).
  - [x] Endpoints localisation (countries, departments, communes, arrondissements, zones) + recherche libre `q` (full-text + filtres).
  - [x] Validation des entrées via serializers, permissions rôle (Super Admin / Admin Assistant), logging d’audit minimal.
- [x] Frontend User :
  - [x] Pages Home, Listings (liste + filtres), Listing detail avec CTA WhatsApp prérempli et message contextualisé.
  - [x] Recherche texte + filtres basiques (ville, zone, type, prix, meublé, durée) + auto-complétion simple.
  - [x] Accessibilité (ARIA, labels, contrastes) et performance (SSR/SSG) ; pas de paiement en ligne.
- [x] Frontend Admin :
  - [x] Authentification et session sécurisée.
  - [x] Dashboard synthétique (statuts des annonces).
  - [x] Table des annonces avec création/édition et workflow de validation (boutons visibles selon rôle) ;
  - [x] Upload médias pour les annonces (API sécurisée + upload assistant sous contrôle et suppression réservée au super admin).

### Phase 1.1 — Vérification de conformité MVP
- [x] Préparer la **commission de vérification** (voir `docs/commission-verification.md`) et désigner les rôles.
- [x] Exécuter `node requirements-check.js` à chaque fin de sprint et mettre à jour les statuts.
- [ ] Lancer `pytest -v` (tests requirement) avec les variables d'env configurées ; corriger tout échec avant livraison (bloqué sur ce dépôt par l'accès PyPI en CI locale).
- [ ] Documenter les écarts et actions correctives dans le backlog.

### Phase 2 — Expérience & recherche avancées
- [x] Auto-complétion et suggestions sur la barre de recherche (zones, types, prix).
- [x] Synonymes/fautes courantes sur zones (Fidjrossè/Fidjrosse) et types de logement.
- [ ] Filtres enrichis : standing, distance/plage (si coordonnées dispo), disponibilité.
- [ ] Statistiques admin : vues par annonce, top zones, conversion WhatsApp (clics).
- [ ] Gestion des rôles affinée (permissions par action) et journalisation détaillée.

### Phase 3 — Scalabilité & extension
- [ ] Multi-ville/pays (activer le champ country, nouveaux départements/communes).
- [ ] Favoris et comptes utilisateurs publics (optionnel).
- [ ] Vue carte (PostGIS + clustering) et filtre par rayon.
- [ ] Notifications propriétaires (email/WhatsApp Business API) après validation.
- [ ] Optimisation SEO (sitemaps, OpenGraph) et observabilité (traces, logs structurés, métriques).

## 🎨 Design system confortable (18–90 ans)
- **Palette claire douce** : fond global `#F5F5F7`, cartes `#FFFFFF`, texte principal `#1F2933`, texte secondaire `#6B7280`, accent `#2563EB` (hover `#1D4ED8`), bordures `#E5E7EB`.
- **Palette sombre douce** : fond global `#020617/#020817`, cartes `#0B1120/#111827`, texte principal `#F9FAFB`, secondaire `#9CA3AF`, accent `#60A5FA` (hover `#3B82F6`), bordures `#1F2937`.
- **À éviter** : fond blanc pur ou noir pur pleine page, couleurs fluo saturées en fond, texte gris clair sur fond clair/sombre, reliance exclusive rouge/vert.
- **Typographie** : Inter/Roboto/System, base 16–18px, line-height 1.5–1.7, titres 26–32px (H1), 22–24px (H2), 18–20px (H3) ; éviter tout-majuscule, justification, polices fantaisie.
- **Layouts** : espace généreux, cartes annonces avec photo, prix, type, localisation, CTA "Voir plus" + bouton WhatsApp (icône + texte), boutons ≥40px de hauteur, bord arrondi léger.
- **Thème choisi par l’utilisateur** : onboarding avec sélection clair/sombre, persistance via localStorage, toggle accessible (🌓) en header ; même structure entre thèmes.
- **Accessibilité & confort** : largeur de texte 60–80 caractères, feedback visuel sur actions, zones cliquables larges, icônes toujours accompagnées de texte, pas d’animations agressives ni d’autoplay audio.

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
