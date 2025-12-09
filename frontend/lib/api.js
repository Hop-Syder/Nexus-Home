/**
 * Lightweight API helper to query the Django backend while staying defensive against network failures.
 * All helpers validate inputs and guard against missing tokens to avoid confusing runtime errors.
 */
const DEFAULT_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

const ADMIN_TOKEN_KEY = 'nexus-admin-token';

function buildUrl(path, params = {}) {
  const url = new URL(path, DEFAULT_BASE_URL);
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    url.searchParams.append(key, value);
  });
  return url.toString();
}

async function fetchJson(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      throw new Error(`API responded with ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    return null;
  }
}

function sanitizeNumber(value) {
  if (value === undefined || value === null || value === '') {
    return undefined;
  }
  const parsed = Number(value);
  return Number.isNaN(parsed) ? undefined : parsed;
}

function adminHeaders(token) {
  if (!token) return {};
  return { Authorization: `Token ${token}` };
}

export function loadStoredAdminToken() {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem(ADMIN_TOKEN_KEY);
}

export function persistAdminToken(token) {
  if (typeof window === 'undefined' || !token) return;
  window.localStorage.setItem(ADMIN_TOKEN_KEY, token);
}

export function clearAdminToken() {
  if (typeof window === 'undefined') return;
  window.localStorage.removeItem(ADMIN_TOKEN_KEY);
}

export async function fetchListings(params = {}) {
  const url = buildUrl('/listings', {
    ...params,
    page: sanitizeNumber(params.page),
    page_size: sanitizeNumber(params.page_size),
    price_min: sanitizeNumber(params.price_min),
    price_max: sanitizeNumber(params.price_max),
  });
  const data = await fetchJson(url);
  if (!data) {
    return {
      results: [],
      total: 0,
      page: params.page || 1,
      pageSize: params.page_size,
      error: 'Impossible de récupérer les annonces.',
    };
  }

  const results = data.results || data;
  const total = typeof data.count === 'number' ? data.count : results.length;

  return {
    results,
    total,
    page: params.page || 1,
    pageSize: params.page_size,
    error: null,
  };
}

export async function fetchListingDetail(slug) {
  if (!slug) return { listing: null, error: 'Identifiant manquant.' };
  const url = buildUrl(`/listings/${slug}`);
  const data = await fetchJson(url);
  if (!data) {
    return { listing: null, error: "Impossible de récupérer l'annonce." };
  }
  return { listing: data, error: null };
}

export async function loginAdmin(email, password) {
  const url = buildUrl('/auth/login');
  const body = JSON.stringify({ email, password });
  const data = await fetchJson(url, { method: 'POST', body });
  if (!data || !data.access_token) {
    return { token: null, error: "Échec de l'authentification." };
  }
  persistAdminToken(data.access_token);
  return { token: data.access_token, error: null };
}

export async function fetchAdminListings(token, params = {}) {
  const url = buildUrl('/admin/listings', params);
  const data = await fetchJson(url, { headers: adminHeaders(token) });
  if (!data) {
    return { results: [], error: 'Impossible de récupérer les annonces admin.' };
  }
  return { results: data.results || data, error: null };
}

export async function createAdminListing(token, payload) {
  const url = buildUrl('/admin/listings');
  const data = await fetchJson(url, {
    method: 'POST',
    headers: adminHeaders(token),
    body: JSON.stringify({
      ...payload,
      price: sanitizeNumber(payload.price),
      commune: sanitizeNumber(payload.commune),
      zone: sanitizeNumber(payload.zone),
    }),
  });
  if (!data || !data.id) {
    return { listing: null, error: "Création d'annonce impossible." };
  }
  return { listing: data, error: null };
}

export async function publishListing(token, listingId) {
  const url = buildUrl(`/admin/listings/${listingId}/validate`);
  const data = await fetchJson(url, { method: 'POST', headers: adminHeaders(token) });
  if (!data) {
    return { listing: null, error: 'Publication refusée par le serveur.' };
  }
  return { listing: data, error: null };
}

export async function rejectListing(token, listingId) {
  const url = buildUrl(`/admin/listings/${listingId}/reject`);
  const data = await fetchJson(url, { method: 'POST', headers: adminHeaders(token) });
  if (!data) {
    return { listing: null, error: "Rejet refusé par le serveur." };
  }
  return { listing: data, error: null };
}

export async function deleteListing(token, listingId) {
  const url = buildUrl(`/admin/listings/${listingId}`);
  try {
    const response = await fetch(url, { method: 'DELETE', headers: adminHeaders(token) });
    if (!response.ok) {
      throw new Error(`Suppression refusée (${response.status})`);
    }
    return { error: null };
  } catch (error) {
    console.error('Suppression échouée:', error);
    return { error: "Impossible de supprimer l'annonce." };
  }
}

export async function fetchCommunes() {
  const url = buildUrl('/locations/communes');
  const data = await fetchJson(url);
  return data ? { results: data } : { results: [], error: 'Communes introuvables' };
}

export async function fetchZones(arrondissementId) {
  const url = buildUrl('/locations/zones', { arrondissement_id: sanitizeNumber(arrondissementId) });
  const data = await fetchJson(url);
  return data ? { results: data } : { results: [], error: 'Zones introuvables' };
}

export async function searchZones(query) {
  const url = buildUrl('/locations/search', { q: query });
  const data = await fetchJson(url);
  return data ? { results: data } : { results: [], error: 'Aucune zone correspondante' };
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
