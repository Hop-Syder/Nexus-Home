/**
 * Admin workspace for login and listing management with explicit role boundaries.
 * Provides token-based authentication, creation of draft listings, publishing actions,
 * and defensive error handling to avoid silent failures for non-technical operators.
 */
import { useEffect, useMemo, useState } from 'react';
import {
  clearAdminToken,
  createAdminListing,
  deleteListing,
  fetchAdminListings,
  fetchCommunes,
  fetchZones,
  loadStoredAdminToken,
  loginAdmin,
  publishListing,
  rejectListing,
} from '../../lib/api';

const EMPTY_FORM = {
  title: '',
  description: '',
  price: '',
  type_logement: 'CHAMBRE',
  commune: '',
  zone: '',
  whatsapp_phone: '',
  status: 'DRAFT',
};

const STATUS_LABELS = {
  DRAFT: 'Brouillon',
  PENDING: 'En attente',
  PUBLISHED: 'Publié',
  REJECTED: 'Rejeté',
};

function LoginPanel({ onAuthenticated, error }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const { token, error: loginError } = await loginAdmin(email, password);
    if (loginError || !token) {
      onAuthenticated(null, loginError || "Impossible de se connecter.");
      return;
    }
    onAuthenticated(token, null);
  };

  return (
    <form className="card" onSubmit={handleSubmit} style={{ display: 'grid', gap: '0.75rem' }}>
      <h2 style={{ marginTop: 0 }}>Connexion admin</h2>
      <p style={{ marginTop: 0, color: 'var(--text-muted)' }}>
        Connecte-toi avec ton compte Admin ou Admin assistant pour gérer les annonces.
      </p>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label htmlFor="password">Mot de passe</label>
        <input
          id="password"
          name="password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      {error ? (
        <p style={{ color: 'tomato', margin: 0 }}>Authentification refusée : {error}</p>
      ) : null}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button type="submit" className="button-primary" aria-label="Se connecter">
          Se connecter
        </button>
      </div>
    </form>
  );
}

function ListingForm({ onSubmit, communes, zones, disabled }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [localError, setLocalError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.title || !form.description || !form.price || !form.commune || !form.zone || !form.whatsapp_phone) {
      setLocalError('Merci de remplir tous les champs obligatoires.');
      return;
    }
    setLocalError('');
    await onSubmit(form, () => setForm(EMPTY_FORM));
  };

  return (
    <form className="card" onSubmit={handleSubmit} style={{ display: 'grid', gap: '0.75rem' }}>
      <h3 style={{ marginTop: 0 }}>Créer une annonce (brouillon)</h3>
      <div className="grid grid-2">
        <div>
          <label htmlFor="title">Titre</label>
          <input id="title" name="title" value={form.title} onChange={handleChange} disabled={disabled} required />
        </div>
        <div>
          <label htmlFor="price">Prix (FCFA)</label>
          <input id="price" name="price" type="number" value={form.price} onChange={handleChange} disabled={disabled} required />
        </div>
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          rows={3}
          value={form.description}
          onChange={handleChange}
          disabled={disabled}
          required
        />
      </div>
      <div className="grid grid-3">
        <div>
          <label htmlFor="type_logement">Type</label>
          <select
            id="type_logement"
            name="type_logement"
            value={form.type_logement}
            onChange={handleChange}
            disabled={disabled}
          >
            <option value="CHAMBRE">Chambre</option>
            <option value="STUDIO">Studio</option>
            <option value="APPARTEMENT">Appartement</option>
            <option value="VILLA">Villa</option>
          </select>
        </div>
        <div>
          <label htmlFor="commune">Commune</label>
          <select id="commune" name="commune" value={form.commune} onChange={handleChange} disabled={disabled} required>
            <option value="">Choisir…</option>
            {communes.map((commune) => (
              <option key={commune.id} value={commune.id}>
                {commune.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="zone">Zone / Quartier</label>
          <select id="zone" name="zone" value={form.zone} onChange={handleChange} disabled={disabled} required>
            <option value="">Choisir…</option>
            {zones.map((zone) => (
              <option key={zone.id} value={zone.id}>
                {zone.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div>
        <label htmlFor="whatsapp_phone">Numéro WhatsApp</label>
        <input
          id="whatsapp_phone"
          name="whatsapp_phone"
          placeholder="+22990000000"
          value={form.whatsapp_phone}
          onChange={handleChange}
          disabled={disabled}
          required
        />
      </div>
      {localError ? <p style={{ color: 'tomato', margin: 0 }}>{localError}</p> : null}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button type="submit" className="button-primary" disabled={disabled} aria-label="Créer une annonce">
          Enregistrer en brouillon
        </button>
      </div>
    </form>
  );
}

function ListingsTable({ listings, onPublish, onReject, onDelete, loading }) {
  if (loading) return <p>Chargement des annonces…</p>;
  if (!listings.length) return <p>Aucune annonce pour le moment.</p>;

  return (
    <div className="card" style={{ overflowX: 'auto' }}>
      <h3 style={{ marginTop: 0 }}>Annonces</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left' }}>Titre</th>
            <th>Statut</th>
            <th>Prix</th>
            <th>Commune</th>
            <th>Zone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {listings.map((listing) => (
            <tr key={listing.id}>
              <td>{listing.title}</td>
              <td style={{ textAlign: 'center' }}>{STATUS_LABELS[listing.status] || listing.status}</td>
              <td style={{ textAlign: 'center' }}>{listing.price}</td>
              <td style={{ textAlign: 'center' }}>{listing.commune?.name || '—'}</td>
              <td style={{ textAlign: 'center' }}>{listing.zone?.name || '—'}</td>
              <td style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                {listing.status !== 'PUBLISHED' ? (
                  <button type="button" className="button-primary" onClick={() => onPublish(listing.id)}>
                    Publier
                  </button>
                ) : null}
                {listing.status !== 'REJECTED' ? (
                  <button type="button" className="button-secondary" onClick={() => onReject(listing.id)}>
                    Rejeter
                  </button>
                ) : null}
                <button type="button" className="button-secondary" onClick={() => onDelete(listing.id)}>
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function AdminWorkspace() {
  const [token, setToken] = useState(null);
  const [loginError, setLoginError] = useState(null);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [communes, setCommunes] = useState([]);
  const [zones, setZones] = useState([]);
  const [actionMessage, setActionMessage] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    const stored = loadStoredAdminToken();
    if (stored) setToken(stored);
    fetchCommunes().then(({ results }) => setCommunes(results || []));
    fetchZones().then(({ results }) => setZones(results || []));
  }, []);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    fetchAdminListings(token, statusFilter ? { status: statusFilter } : {}).then(({ results, error }) => {
      setListings(results || []);
      setActionMessage(error || '');
      setLoading(false);
    });
  }, [token, statusFilter]);

  const handleAuthenticated = (newToken, error) => {
    if (error) {
      setLoginError(error);
      return;
    }
    setLoginError(null);
    setToken(newToken);
  };

  const handleCreateListing = async (form, resetForm) => {
    setLoading(true);
    const { listing, error } = await createAdminListing(token, form);
    if (error) {
      setActionMessage(error);
      setLoading(false);
      return;
    }
    resetForm();
    setListings((current) => [listing, ...current]);
    setActionMessage('Annonce créée en brouillon.');
    setLoading(false);
  };

  const handlePublish = async (id) => {
    setLoading(true);
    const { listing, error } = await publishListing(token, id);
    if (error) {
      setActionMessage(error);
      setLoading(false);
      return;
    }
    setListings((current) => current.map((item) => (item.id === id ? listing : item)));
    setActionMessage('Annonce publiée.');
    setLoading(false);
  };

  const handleReject = async (id) => {
    setLoading(true);
    const { listing, error } = await rejectListing(token, id);
    if (error) {
      setActionMessage(error);
      setLoading(false);
      return;
    }
    setListings((current) => current.map((item) => (item.id === id ? listing : item)));
    setActionMessage('Annonce rejetée.');
    setLoading(false);
  };

  const handleDelete = async (id) => {
    setLoading(true);
    const { error } = await deleteListing(token, id);
    if (error) {
      setActionMessage(error);
      setLoading(false);
      return;
    }
    setListings((current) => current.filter((item) => item.id !== id));
    setActionMessage('Annonce supprimée.');
    setLoading(false);
  };

  const handleLogout = () => {
    clearAdminToken();
    setToken(null);
    setListings([]);
    setActionMessage('Déconnecté.');
  };

  const pageContent = useMemo(() => {
    if (!token) {
      return <LoginPanel onAuthenticated={handleAuthenticated} error={loginError} />;
    }
    return (
      <div style={{ display: 'grid', gap: '1rem' }}>
        <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ margin: 0 }}>Espace admin</h2>
            <p style={{ margin: 0, color: 'var(--text-muted)' }}>
              Gestion des annonces, publication et suppression (selon rôle). Les permissions finales sont appliquées côté API.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
            <label htmlFor="statusFilter" style={{ margin: 0 }}>
              Statut
            </label>
            <select
              id="statusFilter"
              name="statusFilter"
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
            >
              <option value="">Tous</option>
              <option value="DRAFT">Brouillon</option>
              <option value="PENDING">En attente</option>
              <option value="PUBLISHED">Publié</option>
              <option value="REJECTED">Rejeté</option>
            </select>
            <button type="button" className="button-secondary" onClick={handleLogout}>
              Se déconnecter
            </button>
          </div>
        </div>
        <ListingForm onSubmit={handleCreateListing} communes={communes} zones={zones} disabled={loading} />
        <ListingsTable
          listings={listings}
          onPublish={handlePublish}
          onReject={handleReject}
          onDelete={handleDelete}
          loading={loading}
        />
      </div>
    );
  }, [token, loginError, communes, zones, listings, loading, statusFilter]);

  return (
    <div style={{ display: 'grid', gap: '1rem' }}>
      {actionMessage ? <p style={{ color: 'var(--text-muted)' }}>{actionMessage}</p> : null}
      {pageContent}
    </div>
  );
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
