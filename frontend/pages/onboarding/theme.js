/**
 * Theme onboarding step to let users choose light or dark comfort mode before browsing listings.
 * Stores the preference for future visits and redirects to the home page.
 */
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { useTheme } from '../../hooks/useTheme';

const THEME_CHOICES = [
  {
    key: 'light',
    title: '🌤️ Thème clair doux',
    body: 'Fond gris clair, textes foncés, idéal pour la journée sans éblouir.',
  },
  {
    key: 'dark',
    title: '🌙 Thème sombre doux',
    body: 'Gris profond et textes clairs pour éviter la fatigue en soirée.',
  },
];

export default function ThemeOnboardingPage() {
  const router = useRouter();
  const { setThemePreference, ready, hasStoredPreference } = useTheme();

  // If a choice already exists, skip the onboarding to avoid forcing a second click.
  useEffect(() => {
    if (!ready) return;
    if (hasStoredPreference) {
      router.replace('/');
    }
  }, [ready, hasStoredPreference, router]);

  const handleSelect = (selectedTheme) => {
    setThemePreference(selectedTheme);
    router.push('/');
  };

  return (
    <section className="card" style={{ display: 'grid', gap: '0.75rem' }}>
      <h2 style={{ margin: 0 }}>Choisis le mode le plus confortable pour tes yeux</h2>
      <p style={{ margin: 0, color: 'var(--text-muted)' }}>
        Tu peux changer d’avis à tout moment depuis le header. On commence avec ton choix préféré pour éviter toute fatigue
        visuelle dès la première page.
      </p>
      <div className="grid grid-2">
        {THEME_CHOICES.map((choice) => (
          <button
            key={choice.key}
            type="button"
            className="card button-reset"
            style={{ textAlign: 'left' }}
            onClick={() => handleSelect(choice.key)}
          >
            <strong>{choice.title}</strong>
            <p style={{ marginBottom: 0, color: 'var(--text-muted)' }}>{choice.body}</p>
          </button>
        ))}
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
