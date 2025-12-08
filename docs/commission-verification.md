# Commission de Vérification de Conformité – Nexus-Home

## 🎯 Objectif
Établir une méthode formelle pour vérifier que chaque livraison respecte les exigences fonctionnelles et techniques :
- Marketplace location à Cotonou sans paiement en ligne
- Contact via bouton WhatsApp
- Interfaces distinctes User/Admin avec rôles (Super Admin, Admin Assistant)
- Recherche rapide avec filtres et hiérarchie de localisation (pays > département > commune > arrondissement > zone/quartier)

## 👥 Rôles de la commission
- **Responsable produit** : valide la couverture des besoins métier et l’absence de paiement en ligne.
- **Tech lead / Dev** : confirme l’implémentation des exigences techniques (API, recherche, sécurité).
- **QA / Vérificateur** : exécute la checklist, documente les écarts, suit les actions correctives.

## ✅ Checklists principales
### A. Fonctionnalités utilisateur (Frontend User)
- [ ] Annonces récentes visibles sur la page d’accueil.
- [ ] Recherche texte disponible.
- [ ] Filtres : commune/ville, quartier/zone, type de logement, budget min/max, meublé, durée.
- [ ] Pertinence maintenue avec 3–4 mots clés (ex. « chambre meublée fidjrossè »).
- [ ] Fiche annonce : titre, prix, type, localisation, description, photos.
- [ ] Bouton WhatsApp par annonce avec message prérempli.
- [ ] Aucun paiement en ligne affiché ni proposé.

### B. Fonctionnalités admin (Frontend Admin)
- [ ] Accès sécurisé par login.
- [ ] Dashboard avec totaux et statuts des annonces.
- [ ] Actions Admin : créer, modifier, supprimer, publier une annonce ; créer un admin assistant.
- [ ] Actions Admin Assistant : créer/éditer (DRAFT/PENDING) ; pas de publication, pas de suppression, pas de gestion des admins.

### C. Modèle de données & localisation
- [ ] Annonce liée à pays, département, commune/ville, arrondissement, zone/quartier.
- [ ] Table dédiée aux zones/quartiers avec synonymes gérés.

### D. Technique
- [ ] Frontend Next.js opérationnel (user + admin).
- [ ] API REST structurée (Django/DRF) avec PostgreSQL.
- [ ] Recherche full-text activée.
- [ ] Versionnage Git actif, environnements distincts (dev/staging/prod).

### E. Expérience utilisateur & performance
- [ ] Responsive mobile.
- [ ] Textes lisibles (contrastes, tailles adaptées 18–90 ans).
- [ ] Parcours principal en ≤ 4 clics.
- [ ] Chargement des listes d’annonces ≤ 2–3 s sur connexion moyenne.

## 🧪 Procédure d’exécution
1. Mettre à jour les statuts dans `requirements-check.js` (done/partial/todo) selon l’état réel.
2. Lancer `node requirements-check.js` et conserver la sortie dans le compte-rendu de sprint.
3. Cocher cette checklist et noter chaque écart avec une action corrective et un propriétaire.
4. Bloquer la release si une exigence critique reste en « todo » sans dérogation approuvée.

## 📄 Traçabilité
- Archiver les rapports de la commission (sortie du script + checklist) dans `docs/reports/YYYY-MM-DD/`.
- Journaliser les décisions de dérogation avec date, responsable, justification et échéance de correction.

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
