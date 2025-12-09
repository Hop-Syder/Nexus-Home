/**
 * Search bar with concise filters; prioritizes clarity for non-technical users and seniors.
 * Accepts pre-fetched location options to avoid manual typing errors.
 */
import { useState } from 'react';

const DEFAULT_FILTERS = {
  q: '',
  commune_id: '',
  zone_id: '',
  type_logement: '',
  price_min: '',
  price_max: '',
  is_meuble: '',
  duree: '',
};

export default function SearchBar({ onSearch, communeOptions = [], zoneOptions = [], onZoneSearch }) {
  const [filters, setFilters] = useState(DEFAULT_FILTERS);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));
    if (name === 'zone_id' && onZoneSearch) {
      onZoneSearch(value);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSearch(filters);
  };

  const handleReset = () => {
    setFilters(DEFAULT_FILTERS);
    onSearch(DEFAULT_FILTERS);
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
      <div className="grid grid-3">
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
          <label htmlFor="zone_id">Zone / Quartier</label>
          <input
            id="zone_id"
            name="zone_id"
            placeholder="Fidjrossè"
            list="zone-suggestions"
            value={filters.zone_id}
            onChange={handleChange}
            aria-label="Zone ou quartier"
          />
          {zoneOptions.length > 0 ? (
            <datalist id="zone-suggestions">
              {zoneOptions.map((zone) => (
                <option key={`${zone.id}-${zone.name}`} value={zone.id}>
                  {zone.name}
                </option>
              ))}
            </datalist>
          ) : null}
        </div>
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
      <div className="grid grid-3">
        <div>
          <label htmlFor="is_meuble">Meublé ?</label>
          <select id="is_meuble" name="is_meuble" value={filters.is_meuble} onChange={handleChange}>
            <option value="">Indifférent</option>
            <option value="true">Meublé</option>
            <option value="false">Non meublé</option>
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
