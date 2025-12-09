/**
 * Listing filters panel dedicated to the /listings page with URL-friendly state and guardrails
 * for seniors and non-technical users. Keeps the form short and reuses the backend constraints.
 */
import { useEffect, useMemo, useState } from 'react';

const DEFAULT_FILTERS = {
  q: '',
  commune_id: '',
  zone_id: '',
  zone_query: '',
  type_logement: '',
  price_min: '',
  price_max: '',
  is_meuble: '',
  duree: '',
};

function sanitizeFilters(rawFilters = {}) {
  return { ...DEFAULT_FILTERS, ...rawFilters };
}

function isMeaningfulString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

export default function FiltersPanel({
  initialFilters = {},
  communeOptions = [],
  zoneSuggestions = [],
  onZoneSearch,
  onApply,
}) {
  const [filters, setFilters] = useState(() => sanitizeFilters(initialFilters));

  // Keep the local form in sync with URL-driven filters.
  useEffect(() => {
    setFilters(sanitizeFilters(initialFilters));
  }, [initialFilters]);

  const hasActiveFilters = useMemo(() => {
    return Object.entries(filters).some(([key, value]) => key !== 'zone_query' && isMeaningfulString(value));
  }, [filters]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));

    if (name === 'zone_query' && onZoneSearch) {
      const trimmed = value.trim();
      if (trimmed.length >= 2) {
        onZoneSearch(trimmed);
      } else {
        onZoneSearch('');
      }
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onApply(filters);
  };

  const handleReset = () => {
    setFilters(DEFAULT_FILTERS);
    onApply(DEFAULT_FILTERS);
  };

  return (
    <form className="card" onSubmit={handleSubmit} style={{ display: 'grid', gap: '0.75rem' }}>
      <div>
        <label htmlFor="q">Recherche (3–4 mots suffisent)</label>
        <input
          id="q"
          name="q"
          placeholder="chambre meublée Fidjrossè"
          value={filters.q}
          onChange={handleChange}
          aria-label="Recherche par mots-clés"
        />
      </div>

      <div className="grid grid-2">
        <div>
          <label htmlFor="commune_id">Commune / Ville</label>
          <select id="commune_id" name="commune_id" value={filters.commune_id} onChange={handleChange}>
            <option value="">Toutes</option>
            {communeOptions.map((commune) => (
              <option key={commune.id} value={commune.id}>
                {commune.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="zone_query">Zone / Quartier</label>
          <input
            id="zone_query"
            name="zone_query"
            placeholder="Fidjrossè, Cadjèhoun…"
            value={filters.zone_query}
            onChange={handleChange}
            aria-label="Zone ou quartier (saisie libre)"
          />
          {zoneSuggestions.length > 0 ? (
            <div style={{ marginTop: '0.35rem' }}>
              <label htmlFor="zone_id">Suggestions</label>
              <select
                id="zone_id"
                name="zone_id"
                value={filters.zone_id}
                onChange={handleChange}
                aria-label="Suggestions de zones"
              >
                <option value="">Toutes</option>
                {zoneSuggestions.map((zone) => (
                  <option key={zone.id} value={zone.id}>
                    {zone.name} · {zone.arrondissement?.name || 'Arrondissement'}
                  </option>
                ))}
              </select>
            </div>
          ) : null}
        </div>
      </div>

      <div className="grid grid-2">
        <div>
          <label htmlFor="type_logement">Type de logement</label>
          <select id="type_logement" name="type_logement" value={filters.type_logement} onChange={handleChange}>
            <option value="">Tous</option>
            <option value="CHAMBRE">Chambre</option>
            <option value="STUDIO">Studio</option>
            <option value="APPARTEMENT">Appartement</option>
            <option value="VILLA">Villa</option>
          </select>
        </div>
        <div>
          <label htmlFor="is_meuble">Meublé ?</label>
          <select id="is_meuble" name="is_meuble" value={filters.is_meuble} onChange={handleChange}>
            <option value="">Indifférent</option>
            <option value="true">Meublé</option>
            <option value="false">Non meublé</option>
          </select>
        </div>
      </div>

      <div className="grid grid-3">
        <div>
          <label htmlFor="price_min">Prix min</label>
          <input id="price_min" name="price_min" type="number" value={filters.price_min} onChange={handleChange} />
        </div>
        <div>
          <label htmlFor="price_max">Prix max</label>
          <input id="price_max" name="price_max" type="number" value={filters.price_max} onChange={handleChange} />
        </div>
        <div>
          <label htmlFor="duree">Durée</label>
          <select id="duree" name="duree" value={filters.duree} onChange={handleChange}>
            <option value="">Toutes</option>
            <option value="JOUR">Jour</option>
            <option value="MOIS">Mois</option>
            <option value="ANNEE">Année</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button type="submit" className="button-primary" aria-label="Lancer la recherche">
          🔍 Rechercher
        </button>
        <button type="button" className="button-secondary" onClick={handleReset} aria-label="Réinitialiser les filtres">
          Réinitialiser
        </button>
        {hasActiveFilters ? <span className="badge">Filtres actifs</span> : <span className="badge">Filtres par défaut</span>}
      </div>
    </form>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
