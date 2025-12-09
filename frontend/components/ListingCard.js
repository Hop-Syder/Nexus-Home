/**
 * Listing card designed for quick scanning: clear price, location, and WhatsApp CTA for all audiences.
 */
import Link from 'next/link';
import { trackWhatsappClick } from '../lib/api';

export default function ListingCard({ listing }) {
  if (!listing) {
    return null;
  }

  const primaryMedia = Array.isArray(listing.media) && listing.media.length ? listing.media[0] : null;
  const whatsappLink = listing.whatsapp_phone
    ? `https://wa.me/${listing.whatsapp_phone.replace(/\D/g, '')}?text=${encodeURIComponent(
        `Bonjour, je suis intéressé par l'annonce ${listing.title || listing.id}.`
      )}`
    : null;

  const handleWhatsappClick = async (event) => {
    if (event) event.preventDefault();
    if (!whatsappLink) return;

    // Log the click for conversion tracking without slowing down the user journey.
    const slugOrId = listing.slug || listing.id;
    if (slugOrId) {
      await trackWhatsappClick(slugOrId);
    }

    window.open(whatsappLink, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {primaryMedia ? (
        <div className="listing-card__media" aria-label="Photo principale de l'annonce">
          <img
            src={primaryMedia.url}
            alt={primaryMedia.caption || listing.title}
            loading="lazy"
            style={{ width: '100%', borderRadius: '0.6rem', objectFit: 'cover' }}
          />
        </div>
      ) : null}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
        <span className="badge">{listing.type_logement || 'Logement'}</span>
        <span className="badge">{listing.is_meuble ? 'Meublé' : 'Non meublé'}</span>
        {listing.standing ? <span className="badge">{listing.standing}</span> : null}
        {listing.duree ? <span className="badge">{listing.duree}</span> : null}
      </div>
      <h3 style={{ margin: 0 }}>{listing.title}</h3>
      <p style={{ margin: 0, color: 'var(--text-muted)' }}>{listing.description || 'Description à venir.'}</p>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <strong style={{ fontSize: '1.1rem' }}>{listing.price ? `${listing.price} ${listing.currency || 'XOF'}` : 'Prix à préciser'}</strong>
        <span style={{ color: 'var(--text-muted)' }}>
          {listing.commune?.name || listing.commune || 'Ville inconnue'} · {listing.zone?.name || listing.zone || 'Quartier inconnu'}
        </span>
      </div>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <Link
          className="button-secondary"
          href={`/listings/${listing.slug || listing.id}`}
          aria-label={`Voir les détails de ${listing.title}`}
        >
          Voir plus
        </Link>
        {whatsappLink ? (
          <a
            className="button-primary"
            href={whatsappLink}
            onClick={handleWhatsappClick}
            target="_blank"
            rel="noopener noreferrer"
          >
            📱 Contacter sur WhatsApp
          </a>
        ) : null}
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
