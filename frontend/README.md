# Frontend Next.js

## 🎯 Objectif
Frontend Next.js unique (pages router) prêt pour les interfaces **User** et **Admin** :
- recherche rapide avec filtres, fiche détail avec CTA WhatsApp
- design system doux (thème clair/sombre) pour confort 18–90 ans
- base admin prête à connecter au backend (auth JWT/Session côté Django)

## 📁 Structure
```
frontend/
├── components/        # Layout, thème, cartes, barre de recherche
├── hooks/             # Hooks réutilisables (useTheme)
├── lib/               # Clients API
├── pages/             # Pages Next (user + admin placeholders)
├── styles/            # Design tokens et styles globaux
├── package.json       # Scripts/npm
└── next.config.js
```

## 🚀 Démarrage
1. `cd frontend`
2. `npm install`
3. Créer `.env.local` si besoin : `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1`
4. `npm run dev`

## 🧪 Tests rapides
- `npm run lint` (nécessite eslint installé)

## 🧠 Notes UX
- Thème clair/sombre doux, switch accessible dans le header
- Champs larges, labels explicites, boutons ≥ 40px de hauteur
- CTA WhatsApp prérempli pour limiter la friction

## 🔐 Sécurité côté front
- Aucune clé sensible en dur : utiliser `.env.local`
- Fallback robuste en cas d’échec réseau (affiche un message au lieu de planter)

# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
