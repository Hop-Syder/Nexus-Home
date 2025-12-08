/**
 * Lightweight API helper to query the Django backend while staying defensive against network failures.
 */
const DEFAULT_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

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

export async function fetchListings(params = {}) {
  const url = buildUrl('/listings', params);
  const data = await fetchJson(url);
  if (!data) {
    return { results: [], error: 'Impossible de récupérer les annonces.' };
  }
  return { results: data.results || data, error: null };
}

export async function fetchListingDetail(id) {
  if (!id) return { listing: null, error: 'Identifiant manquant.' };
  const url = buildUrl(`/listings/${id}`);
  const data = await fetchJson(url);
  if (!data) {
    return { listing: null, error: "Impossible de récupérer l'annonce." };
  }
  return { listing: data, error: null };
}
// ──────────────────────────────────
// Hop-Syder Développeur
// Full Stack & Data Scientist – Nexus Partners
// 📧 daoudaabassichristian@gmail.com
// 🌐 ceo.nexuspartners.xyz
// ──────────────────────────────────
