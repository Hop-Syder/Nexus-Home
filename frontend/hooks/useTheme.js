/**
 * Theme hook that persists the light/dark choice in localStorage and updates the document root attribute.
 * This is intentionally simple to stay compatible with SSR and avoid hydration mismatches.
 */
import { useEffect, useState } from 'react';

const DEFAULT_THEME = 'light';
const THEMES = ['light', 'dark'];

export function useTheme() {
  const [theme, setTheme] = useState(DEFAULT_THEME);
  const [ready, setReady] = useState(false);

  // Sync theme from storage on mount.
  useEffect(() => {
    try {
      const storedTheme = window.localStorage.getItem('theme');
      const validTheme = THEMES.includes(storedTheme) ? storedTheme : DEFAULT_THEME;
      setTheme(validTheme);
      document.documentElement.setAttribute('data-theme', validTheme);
    } catch (error) {
      // Storage may be unavailable; keep default but avoid breaking rendering.
      document.documentElement.setAttribute('data-theme', DEFAULT_THEME);
    } finally {
      setReady(true);
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(nextTheme);
    try {
      window.localStorage.setItem('theme', nextTheme);
    } catch (error) {
      // Non-blocking: localStorage may be disabled in private mode.
    }
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  return { theme, toggleTheme, ready };
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
