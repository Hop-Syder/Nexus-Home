/**
 * Listing detail page with SSR for better SEO and instant load on shareable slug URLs.
 * Uses a client refresh to keep view counts and live data accurate after navigation without reloads.
 */
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { fetchListingDetail } from '../../lib/api';

export default function ListingDetailPage({ initialListing = null, initialError = null }) {
  const router = useRouter();
  const { slug } = router.query;
  const [listing, setListing] = useState(initialListing);
  const [error, setError] = useState(initialError);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!slug) return;
    const load = async () => {
      setLoading(true);
      const { listing: detail, error: fetchError } = await fetchListingDetail(slug);
      setError(fetchError || null);
      setListing(detail || null);
      setLoading(false);
    };
    load();
  }, [slug]);

  const whatsappLink = listing?.whatsapp_phone
    ? `https://wa.me/${listing.whatsapp_phone.replace(/\D/g, '')}?text=${encodeURIComponent(
        `Bonjour, je suis intéressé par l'annonce ${listing.title || slug}.`
      )}`
    : null;

  if (loading) return <p>Chargement…</p>;
  if (error) return <p style={{ color: 'tomato' }}>{error}</p>;
  if (!listing) return <p>Aucune annonce trouvée.</p>;

  const gallery = Array.isArray(listing.media) ? listing.media : [];
  return (
    <article className="card" style={{ display: 'grid', gap: '0.75rem' }}>
      <header>
        <p className="badge" style={{ margin: 0 }}>
          {listing.type_logement || 'Logement'} · {listing.is_meuble ? 'Meublé' : 'Non meublé'} · {listing.duree || 'Durée non précise'}
        </p>
        <h2 style={{ marginBottom: '0.25rem' }}>{listing.title}</h2>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <strong style={{ fontSize: '1.2rem' }}>{listing.price ? `${listing.price} ${listing.currency || 'XOF'}` : 'Prix à préciser'}</strong>
          <span style={{ color: 'var(--text-muted)' }}>
            {listing.commune?.name || listing.commune || 'Ville inconnue'} · {listing.zone?.name || listing.zone || 'Quartier inconnu'}
          </span>
        </div>
      </header>

      {gallery.length ? (
        <section aria-label="Galerie photos" className="listing-gallery">
          <div className="gallery-grid">
            {gallery.map((media) => (
              <figure key={media.id} className="gallery-item">
                <img src={media.url} alt={media.caption || listing.title} loading="lazy" />
                {media.caption ? <figcaption>{media.caption}</figcaption> : null}
              </figure>
            ))}
          </div>
        </section>
      ) : null}

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

export async function getServerSideProps({ params }) {
  const slug = params?.slug;
  if (!slug) {
    return { notFound: true };
  }

  const { listing, error } = await fetchListingDetail(slug);

  if (!listing) {
    return {
      props: {
        initialListing: null,
        initialError: error || "Cette annonce est introuvable ou n'est plus disponible.",
      },
    };
  }

  return {
    props: {
      initialListing: listing,
      initialError: error || null,
    },
  };
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
