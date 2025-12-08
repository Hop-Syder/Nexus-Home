# Architecture et données

## 🎯 But
Décrire l’architecture cible pour Nexus-Home afin d’assurer une base robuste, sécurisée et évolutive.

## 📐 Découpage global
- **Frontend (Next.js)** : apps user/admin, rendu SSR/SSG pour performance et SEO, design system cohérent
- **Backend (Django + DRF)** : API REST sécurisée, validations strictes, throttling, audit log
- **Base de données (PostgreSQL)** : modèles normalisés avec clés étrangères, index tsvector/GIN pour recherche
- **Recherche** : full-text Postgres (V1) puis Meilisearch (V2) pour tolérance aux fautes et auto-complétion
- **Stockage médias** : S3 compatible, conversions WebP, URLs signées pour l’admin, CDN recommandé

## 🗺️ Localisation hiérarchique
1. Country (Bénin en V1, extensible multi-pays)
2. Department
3. Commune / Ville
4. District (Arrondissement)
5. Zone (quartier, repère, plage/goudron, etc.) + table de synonymes
- Chaque `Listing` référence au minimum Commune + Zone ; District est conseillé pour la structure et les stats
- Lat/Long stockés pour futures recherches par rayon et affichage cartographique

## 🔍 Recherche “4 mots précis”
- Générer un champ tsvector combiné : titre, description, zone, commune, type, équipements clés
- Index GIN sur le tsvector + index sur prix, meublé, disponibilité
- Requêtes : texte plein + filtres (prix min/max, type, meublé, durée, disponibilité, zone/commune)
- Tolérance orthographique via dictionnaires/synonymes et normalisation des accents ; upgrade Meilisearch pour le fuzzy

## 🔐 Sécurité et conformité
- Auth admin via cookies httpOnly, rotation refresh tokens, 2FA recommandé
- RBAC : Super Admin vs Admin Assistant (limitation suppression/validation)
- Rate limiting sur endpoints publics et admin ; CORS limité aux origines de confiance
- Validation/sanitation de tout input ; pas de secrets en dur ; backups DB automatisés
- Audit log : chaque action sensible est enregistrée (qui, quoi, quand, avant/après)

## 🔄 Flux clés
- **Publication annonce** : Assistant crée → statut draft → Super Admin valide → publication → soft delete si retrait
- **Contact utilisateur** : depuis fiche → bouton WhatsApp avec message pré-rempli incluant ID annonce
- **Médias** : upload signé S3, génération thumbnail côté worker (Celery/RQ), association ordonnée à l’annonce

## 🧪 Observabilité
- Logging structuré (JSON) ; niveaux INFO/WARN/ERROR
- Traces et métriques (OpenTelemetry optionnel) ; dashboards pour erreurs 5xx et lenteurs requêtes

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
