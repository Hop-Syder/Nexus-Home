/**
 * Listing detail page: shows key facts and preserves WhatsApp CTA for seamless conversion.
 */
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { fetchListingDetail } from '../../lib/api';

export default function ListingDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [listing, setListing] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      setLoading(true);
      const { listing: detail, error: fetchError } = await fetchListingDetail(id);
      if (fetchError) {
        setError(fetchError);
      }
      setListing(detail);
      setLoading(false);
    };
    load();
  }, [id]);

  const whatsappLink = listing?.whatsapp_phone
    ? `https://wa.me/${listing.whatsapp_phone.replace(/\D/g, '')}?text=${encodeURIComponent(
        `Bonjour, je suis intéressé par l'annonce ${listing.title || id}.`
      )}`
    : null;

  if (loading) return <p>Chargement…</p>;
  if (error) return <p style={{ color: 'tomato' }}>{error}</p>;
  if (!listing) return <p>Aucune annonce trouvée.</p>;

  return (
    <article className="card" style={{ display: 'grid', gap: '0.75rem' }}>
      <header>
        <p className="badge" style={{ margin: 0 }}>
          {listing.type_logement || 'Logement'} · {listing.is_meuble ? 'Meublé' : 'Non meublé'} · {listing.duree || 'Durée non précisée'}
        </p>
        <h2 style={{ marginBottom: '0.25rem' }}>{listing.title}</h2>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <strong style={{ fontSize: '1.2rem' }}>{listing.price ? `${listing.price} ${listing.currency || 'XOF'}` : 'Prix à préciser'}</strong>
          <span style={{ color: 'var(--text-muted)' }}>
            {listing.commune?.name || listing.commune || 'Ville inconnue'} · {listing.zone?.name || listing.zone || 'Quartier inconnu'}
          </span>
        </div>
      </header>

      <section>
        <h3>À savoir</h3>
        <p style={{ marginTop: 0 }}>{listing.description || 'Description en cours de rédaction.'}</p>
      </section>

      {whatsappLink ? (
        <a className="button-primary" href={whatsappLink} target="_blank" rel="noopener noreferrer">
          📱 Contacter sur WhatsApp
        </a>
      ) : (
        <p style={{ color: 'var(--text-muted)' }}>Contact WhatsApp non renseigné.</p>
      )}
    </article>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
