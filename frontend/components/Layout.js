/**
 * Layout shell shared across pages to keep navigation, theme switch, and footer consistent.
 */
import Link from 'next/link';
import ThemeToggle from './ThemeToggle';

export default function Layout({ children }) {
  return (
    <div>
      <header>
        <div className="container" style={{ padding: '1.25rem 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
            <div>
              <h1 style={{ margin: '0 0 0.25rem 0' }}>Nexus Home</h1>
              <p style={{ margin: 0, color: 'var(--text-muted)' }}>
                Trouvez ou gérez vos annonces en quelques clics, confort matin/soir.
              </p>
              <nav style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                <Link href="/">Accueil</Link>
                <Link href="/listings">Annonces</Link>
                <Link href="/help">Aide</Link>
              </nav>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>
      <main className="container" style={{ paddingBottom: '2rem' }}>{children}</main>
      <footer>
        <p>Marketplace Cotonou · WhatsApp first · Accessibilité 18–90 ans</p>
      </footer>
    </div>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
