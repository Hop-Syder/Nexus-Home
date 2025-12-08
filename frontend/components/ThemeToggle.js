/**
 * Accessible theme toggle aligned with the dual palette to reduce eye fatigue across day/night usage.
 */
import { useTheme } from '../hooks/useTheme';

export default function ThemeToggle() {
  const { theme, toggleTheme, ready } = useTheme();

  if (!ready) {
    return <span style={{ color: 'var(--text-muted)' }}>Préparation du thème…</span>;
  }

  return (
    <button
      type="button"
      className="button-secondary"
      aria-label="Changer le thème visuel"
      onClick={toggleTheme}
    >
      {theme === 'light' ? '🌙 Mode sombre doux' : '🌤️ Mode clair doux'}
    </button>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
