/**
 * Simple help/FAQ page to reassure users and surface WhatsApp-first guidance.
 * Keeps content concise for all ages while pointing to search and contact flows.
 */
import Link from 'next/link';

export default function HelpPage() {
  return (
    <div className="card" style={{ display: 'grid', gap: '0.75rem' }}>
      <h1 style={{ margin: 0 }}>Comment utiliser la plateforme</h1>
      <p style={{ margin: 0, color: 'var(--text-muted)' }}>
        Cette page résume les étapes clés pour trouver rapidement un logement et contacter le propriétaire.
      </p>

      <div>
        <h2 style={{ marginBottom: '0.25rem' }}>1. Rechercher</h2>
        <p style={{ marginTop: 0 }}>
          Depuis l’accueil, tape quelques mots-clés (ex&nbsp;: « chambre meublée Fidjrossè ») et lance la recherche.
          Utilise ensuite les filtres pour préciser la commune, le quartier, le budget ou la durée souhaitée.
        </p>
      </div>

      <div>
        <h2 style={{ marginBottom: '0.25rem' }}>2. Affiner avec les filtres</h2>
        <p style={{ marginTop: 0 }}>
          La page <Link href="/listings">/listings</Link> affiche tous les filtres : commune, zone/quartier, type de
          logement, prix minimum/maximum, meublé ou non, et durée (jour, mois, année). Les filtres restent dans l’URL
          pour partager facilement tes recherches.
        </p>
      </div>

      <div>
        <h2 style={{ marginBottom: '0.25rem' }}>3. Contacter sur WhatsApp</h2>
        <p style={{ marginTop: 0 }}>
          Chaque annonce propose un bouton «&nbsp;Contacter sur WhatsApp&nbsp;» qui ouvre une conversation avec un
          message pré-rempli. Aucune carte bancaire n’est demandée : tout se passe directement avec le propriétaire ou
          le gestionnaire.
        </p>
      </div>

      <div>
        <h2 style={{ marginBottom: '0.25rem' }}>4. Confort visuel</h2>
        <p style={{ marginTop: 0 }}>
          Tu peux choisir un thème clair ou sombre depuis le sélecteur de thème ou lors du premier passage sur
          l’onboarding. Les textes sont volontairement lisibles et les boutons larges pour convenir à tous les âges.
        </p>
      </div>

      <div className="card" style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}>
        <strong>Besoin d’aide&nbsp;?</strong>
        <p style={{ marginTop: '0.25rem', marginBottom: 0 }}>
          Si tu ne trouves pas ce que tu cherches, vérifie tes filtres ou essaie un autre quartier. Tu peux toujours
          revenir à la page d’accueil et relancer une recherche plus simple.
        </p>
      </div>
    </div>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
