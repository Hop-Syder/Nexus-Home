/**
 * requirements-check.js
 * Script de conformité pour vérifier l’avancement des exigences Nexus-Home.
 * Mettre à jour `implementationStatus` puis exécuter `node requirements-check.js`.
 */

const requirements = [
  { id: "USER_SEARCH_TEXT", label: "Recherche texte côté utilisateur", category: "Frontend User" },
  { id: "USER_FILTERS_BASIC", label: "Filtres (commune, quartier, type, budget, meublé, durée)", category: "Frontend User" },
  { id: "USER_WHATSAPP_BUTTON", label: "Bouton WhatsApp sur chaque annonce", category: "Frontend User" },
  { id: "NO_ONLINE_PAYMENT", label: "Aucun paiement en ligne intégré", category: "Règle métier" },
  { id: "ADMIN_LOGIN", label: "Login admin sécurisé", category: "Frontend Admin" },
  { id: "ADMIN_CRUD_LISTINGS", label: "Admin peut créer/modifier/supprimer des annonces", category: "Frontend Admin" },
  { id: "ADMIN_VALIDATE_LISTINGS", label: "Admin peut valider une annonce (PUBLISHED)", category: "Rôles & Permissions" },
  { id: "ADMIN_ASSISTANT_LIMITED", label: "Admin assistant avec droits limités", category: "Rôles & Permissions" },
  { id: "DB_LOCATION_HIERARCHY", label: "Modèle de données localisation (pays, dep, commune, arr, zone)", category: "Backend / DB" },
  { id: "SEARCH_FULLTEXT", label: "Recherche full-text sur annonces", category: "Backend / Search" },
];

// Mettre à jour ces statuts à chaque sprint : "done", "partial" ou "todo".
const implementationStatus = {
  USER_SEARCH_TEXT: "done",
  USER_FILTERS_BASIC: "done",
  USER_WHATSAPP_BUTTON: "done",
  NO_ONLINE_PAYMENT: "done",
  ADMIN_LOGIN: "done",
  ADMIN_CRUD_LISTINGS: "done",
  ADMIN_VALIDATE_LISTINGS: "done",
  ADMIN_ASSISTANT_LIMITED: "done",
  DB_LOCATION_HIERARCHY: "done",
  SEARCH_FULLTEXT: "done",
};

function summarize(statuses) {
  return Object.values(statuses).reduce(
    (acc, current) => {
      const key = current || "todo";
      const nextValue = acc[key] + 1;
      return { ...acc, [key]: nextValue };
    },
    { done: 0, partial: 0, todo: 0 },
  );
}

function formatStatusLabel(status) {
  if (status === "done") return "✅ DONE";
  if (status === "partial") return "🟡 PARTIAL";
  return "❌ TODO";
}

function checkCompliance(currentRequirements, statuses) {
  const summary = summarize(statuses);
  console.log("=== Vérification des exigences ===\n");

  currentRequirements.forEach((requirement) => {
    const status = statuses[requirement.id] || "todo";
    const label = formatStatusLabel(status);
    console.log(`${label} [${requirement.category}] ${requirement.label}`);
  });

  console.log("\n=== Résumé ===");
  console.log(`✅ Complété : ${summary.done}`);
  console.log(`🟡 Partiel   : ${summary.partial}`);
  console.log(`❌ À faire   : ${summary.todo}`);
}

checkCompliance(requirements, implementationStatus);

// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
