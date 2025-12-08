# SON – Suivi Opérationnel des Normes QA

## 🎯 Objectif
Centraliser les points de contrôle qualité et la marche à suivre pour vérifier la conformité du backend/DB par rapport au cahier des charges Nexus-Home (recherche, rôles, localisation, WhatsApp, absence de paiement en ligne).

## 📁 Structure des fichiers QA
- `tests/conftest.py` : fixtures HTTP + DB communes (base URL et DSN Supabase via variables d'environnement).
- `tests/test_requirements_api.py` : exigences fonctionnelles côté API publique (recherche, filtres, WhatsApp, absence de paiement).
- `tests/test_requirements_admin.py` : exigences admin (auth, CRUD, publication, restrictions assistant).
- `tests/test_requirements_db.py` : exigences base de données (hiérarchie localisation, FTS, colonnes FK).
- `backend/tests/` : batterie complète pytest-django pour le backend Django/DRF (fixtures DRF, modèles, permissions, recherche) documentée dans `check-backend2.md`.

## 🛡️ Considérations de sécurité
- Ne jamais commit les secrets : configure `API_BASE_URL`, `SUPABASE_DB_URL`, `SUPER_ADMIN_EMAIL`, `SUPER_ADMIN_PASSWORD`, `ASSISTANT_EMAIL`, `ASSISTANT_PASSWORD` dans l'environnement d'exécution uniquement.
- Les tests DB sont en lecture et utilisent un utilisateur avec droits minimum nécessaires.
- Les appels HTTP utilisent un timeout par défaut pour éviter les blocages.

## ✅ Tests à effectuer (pytest)
1. `pip install -r requirements-dev.txt` (ou `pip install pytest requests psycopg2-binary`).
2. Exporter les variables d'environnement listées plus haut.
3. Lancer `pytest -v` à la racine du dépôt pour les checks HTTP/DB distants.
4. Lancer `pytest -v backend/tests --maxfail=1 --disable-warnings` pour les checks Django/DRF locaux décrits dans `check-backend2.md`.
5. Vérifier les tests `skip` : ils indiquent des variables manquantes ou absence de données seed (annonce publiée).

## 🚀 Instructions d'exécution rapides
```bash
# Exemple minimal
export API_BASE_URL="http://localhost:8000/api/v1"
export SUPABASE_DB_URL="postgresql://user:pass@host:5432/dbname"
export SUPER_ADMIN_EMAIL="admin@example.com"
export SUPER_ADMIN_PASSWORD="change-me"
export ASSISTANT_EMAIL="assistant@example.com"
export ASSISTANT_PASSWORD="change-me"
pytest -v
```

## 🧭 Points de vigilance
- Les IDs utilisés dans les tests (commune_id=1, zone_id=1) doivent correspondre à des données existantes ou à adapter selon vos fixtures.
- Les statuts d'annonces attendus : `DRAFT`, `PENDING`, `PUBLISHED`. Ajustez si votre API diffère.
- Les tests considèrent l'absence d'endpoints de paiement comme obligatoire (404/405 attendus sur `/payments`, `/checkout`, `/stripe`, `/pay`).

---
# ──────────────────────────────────
# Hop-Syder Développeur
# Full Stack & Data Scientist – Nexus Partners
# 📧 daoudaabassichristian@gmail.com
# 🌐 ceo.nexuspartners.xyz
# ──────────────────────────────────
