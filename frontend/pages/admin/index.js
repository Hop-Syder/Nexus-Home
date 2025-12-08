/**
 * Minimal admin landing to anchor future dashboards; currently informs users about authentication requirement.
 */
export default function AdminLanding() {
  return (
    <section className="card" style={{ display: 'grid', gap: '0.75rem' }}>
      <h2 style={{ marginTop: 0 }}>Espace admin</h2>
      <p style={{ marginTop: 0, color: 'var(--text-muted)' }}>
        Connecte-toi pour gérer les annonces, valider les brouillons et créer des assistants. L'authentification sera reliée au
        backend Django (JWT/session) dès que disponible côté API.
      </p>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button type="button" className="button-primary" disabled>
          Connexion à venir
        </button>
        <button type="button" className="button-secondary" disabled>
          Tableau de bord en préparation
        </button>
      </div>
    </section>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
