/**
 * Public landing and search page: highlights the key promise and displays listings with filters.
 */
import { useEffect, useState } from 'react';
import ListingCard from '../components/ListingCard';
import SearchBar from '../components/SearchBar';
import { fetchListings } from '../lib/api';

const EMPTY_STATE = {
  heading: 'Aucune annonce trouvée',
  body: 'Essaye un autre quartier ou élargis la fourchette de prix.',
};

export default function HomePage() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadListings = async (filters = {}) => {
    setLoading(true);
    setError(null);
    const { results, error: fetchError } = await fetchListings(filters);
    if (fetchError) {
      setError(fetchError);
    }
    setListings(results || []);
    setLoading(false);
  };

  useEffect(() => {
    loadListings();
  }, []);

  return (
    <div style={{ display: 'grid', gap: '1rem' }}>
      <section className="card">
        <h2 style={{ marginTop: 0 }}>Trouvez votre logement à Cotonou</h2>
        <p style={{ marginTop: 0, color: 'var(--text-muted)' }}>
          Recherche tolérante, filtres rapides, bouton WhatsApp direct. Pensé pour tous, de 18 à 90 ans.
        </p>
        <SearchBar onSearch={loadListings} />
      </section>

      {loading ? <p>Chargement des annonces…</p> : null}
      {error ? <p style={{ color: 'tomato' }}>{error}</p> : null}

      {!loading && listings.length === 0 ? (
        <div className="card">
          <h3 style={{ marginTop: 0 }}>{EMPTY_STATE.heading}</h3>
          <p style={{ marginTop: 0, color: 'var(--text-muted)' }}>{EMPTY_STATE.body}</p>
        </div>
      ) : null}

      <div className="grid grid-3">
        {listings.map((listing) => (
          <ListingCard key={listing.id} listing={listing} />
        ))}
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
