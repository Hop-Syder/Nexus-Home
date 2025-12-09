/**
 * User-facing listings page with URL-synced filters, location suggestions, and WhatsApp-first cards.
 * Designed to keep navigation predictable for 18–90 y/o audiences while honoring backend constraints.
 */
import { useRouter } from 'next/router';
import { useEffect, useMemo, useState } from 'react';
import FiltersPanel from '../../components/FiltersPanel';
import ListingCard from '../../components/ListingCard';
import { fetchCommunes, fetchListings, searchZones } from '../../lib/api';

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

function normalizeQueryValue(value) {
  if (Array.isArray(value)) return value[0];
  return value ?? '';
}

function normalizeFiltersFromQuery(query = {}) {
  return {
    ...DEFAULT_FILTERS,
    q: normalizeQueryValue(query.q),
    commune_id: normalizeQueryValue(query.commune_id),
    zone_id: normalizeQueryValue(query.zone_id),
    type_logement: normalizeQueryValue(query.type_logement),
    price_min: normalizeQueryValue(query.price_min),
    price_max: normalizeQueryValue(query.price_max),
    is_meuble: normalizeQueryValue(query.is_meuble),
    duree: normalizeQueryValue(query.duree),
  };
}

function buildQueryFromFilters(filters = {}) {
  const params = {};
  Object.entries(filters).forEach(([key, value]) => {
    if (!value || key === 'zone_query') return;
    params[key] = value;
  });
  return params;
}

export default function ListingsPage() {
  const router = useRouter();
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [listings, setListings] = useState([]);
  const [communeOptions, setCommuneOptions] = useState([]);
  const [zoneSuggestions, setZoneSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Memoized key to avoid reruns when router query is unchanged textually.
  const queryKey = useMemo(() => router.asPath, [router.asPath]);

  const loadListings = async (activeFilters) => {
    setLoading(true);
    setError(null);
    const { results, error: fetchError } = await fetchListings(activeFilters);
    if (fetchError) {
      setError(fetchError);
    }
    setListings(results || []);
    setLoading(false);
  };

  useEffect(() => {
    fetchCommunes().then(({ results }) => setCommuneOptions(results || []));
  }, []);

  // Sync with URL parameters whenever they change.
  useEffect(() => {
    if (!router.isReady) return;
    const nextFilters = normalizeFiltersFromQuery(router.query);
    setFilters(nextFilters);
    loadListings(nextFilters);
  }, [router.isReady, queryKey]);

  const handleZoneSearch = async (query) => {
    if (!query || query.length < 2) {
      setZoneSuggestions([]);
      return;
    }
    const { results } = await searchZones(query);
    setZoneSuggestions(results || []);
  };

  const handleApplyFilters = (nextFilters) => {
    const normalizedFilters = { ...DEFAULT_FILTERS, ...nextFilters };
    setFilters(normalizedFilters);
    const query = buildQueryFromFilters(normalizedFilters);
    router.replace({ pathname: '/listings', query }, undefined, { shallow: true });
  };

  return (
    <div style={{ display: 'grid', gap: '1rem' }}>
      <section className="card" style={{ display: 'grid', gap: '0.5rem' }}>
        <h2 style={{ margin: 0 }}>Annonces disponibles</h2>
        <p style={{ margin: 0, color: 'var(--text-muted)' }}>
          Recherche tolérante, filtres précis, et contact direct sur WhatsApp. Les paramètres restent dans l’URL
          pour simplifier le partage et le retour en arrière.
        </p>
      </section>

      <div className="responsive-columns">
        <div>
          <FiltersPanel
            initialFilters={filters}
            communeOptions={communeOptions}
            zoneSuggestions={zoneSuggestions}
            onZoneSearch={handleZoneSearch}
            onApply={handleApplyFilters}
          />
        </div>
        <div style={{ display: 'grid', gap: '0.75rem' }}>
          {loading ? <p>Chargement des annonces…</p> : null}
          {error ? <p style={{ color: 'tomato' }}>{error}</p> : null}
          {!loading && !error && listings.length === 0 ? (
            <div className="card">
              <h3 style={{ marginTop: 0 }}>Aucune annonce trouvée</h3>
              <p style={{ marginTop: 0, color: 'var(--text-muted)' }}>
                Ajuste tes filtres ou essaie une autre zone pour découvrir plus d’options.
              </p>
            </div>
          ) : null}
          <div className="grid grid-2">
            {listings.map((listing) => (
              <ListingCard key={listing.id} listing={listing} />
            ))}
          </div>
        </div>
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
