# Frontend Next.js

## 🎯 Objectif
Fournir deux fronts Next.js :
- **User** (apps/user) : recherche ultra rapide avec filtres, fiches annonces, CTA WhatsApp pré-rempli, accessibilité AA.
- **Admin** (apps/admin) : dashboard sécurisé pour valider/modifier/supprimer les annonces, gérer les assistants et suivre l’activité.

## 🧩 Architecture
- Monorepo Next.js 14 en TypeScript, router app/
- UI : Tailwind CSS + shadcn/ui, design system minimal (boutons, cards, inputs, toasts, modals)
- Formulaires : React Hook Form + Zod (validation côté client + messages accessibles)
- State : server components + React Query/Server Actions pour les mutations si usage API REST ; cache contrôlé
- Auth : NextAuth (JWT ou cookies) avec rôles (super admin / assistant) ; routes protégées pour admin
- Accessibilité : labels, aria-*, focus ring, contrastes ; tests via @testing-library/react et axe

## 🔍 Recherche & filtres
- Barre de recherche avec auto-complétion (appel API `/locations/search`)
- Filtres clés : commune/ville, quartier/zone, prix min/max, type, meublé, durée, disponibilité
- Résultats paginés avec cartes optimisées (images WebP), CTA WhatsApp : `https://wa.me/<phone>?text=<message>`

## 🧪 Tests recommandés
- `npm run lint` (eslint) + `npm run type-check` (tsc)
- Tests unitaires (vitest/jest) sur composants de filtres et cartes d’annonces
- E2E (playwright) : parcours recherche → fiche → bouton WhatsApp ; login admin → validation annonce

## 🚀 Démarrage (proposition)
1. `cd frontend && npm install`
2. Créer `.env.local` (NEXTAUTH_SECRET, API_URL, WHATSAPP_DEFAULT_PHONE, etc.)
3. `npm run dev` pour lancer user/admin ; prévoir `npm run lint` et `npm run test`

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
