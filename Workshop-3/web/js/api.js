// js/api.js
// Centraliza las URLs de los servicios y helpers para llamadas con JWT.

// URL del servicio de autenticación (Spring Boot)
const AUTH_API_URL = 'http://localhost:8080/api/auth';

// URL del servicio core (FastAPI)
const CORE_API_URL = 'http://localhost:8000/api/core';

// Token falso para desarrollo cuando no hay auth-service real.
// IMPORTANTE: solo se usa porque en el core-service tienes DISABLE_AUTH=true.
// Token de prueba para que el core-service esté contento con el header Authorization
const DEMO_TOKEN = 'demo-token';

async function coreRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${DEMO_TOKEN}`,
    ...(options.headers || {}),
  };

  const res = await fetch(`${CORE_API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const text = await res.text();
    console.error('Core API error:', res.status, text);
    throw new Error(`Core API error: ${res.status}`);
  }

  return res.json();
}

// Helper genérico para llamar al core-service con Authorization
async function apiFetch(url, options = {}) {
  const headers = options.headers || {};
  const token = getToken();

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  });

  return response;
}

// Login contra auth-service
async function loginRequest(email, password) {
  const res = await fetch(`${AUTH_API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    throw new Error('Login failed');
  }

  // Se espera: { access_token, user: { email, role } }
  return res.json();
}

// Registro de usuario con código de acceso único
async function registerRequest(email, password, accessCode) {
  const res = await fetch(`${AUTH_API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      password,
      access_code: accessCode,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Registration failed');
  }

  return res.json();
}

// Obtiene estadísticas generales para el dashboard
async function getOverviewStats() {
  const res = await apiFetch(`${CORE_API_URL}/stats/overview`);
  if (!res.ok) {
    throw new Error('Error fetching stats');
  }
  return res.json();
}

// Obtiene sesiones recientes (para actividad)
async function getRecentSessions(limit = 5) {
  const res = await apiFetch(
    `${CORE_API_URL}/sessions?limit=${limit}&order=desc`
  );
  if (!res.ok) {
    throw new Error('Error fetching sessions');
  }
  return res.json();
}

// Obtiene estado de slots
async function getSlots() {
  const res = await apiFetch(`${CORE_API_URL}/slots`);
  if (!res.ok) {
    throw new Error('Error fetching slots');
  }
  return res.json();
}

// Registra entrada de vehículo
async function registerEntry(plate) {
  const res = await apiFetch(`${CORE_API_URL}/entries`, {
    method: 'POST',
    body: JSON.stringify({ plate }),
  });
  if (!res.ok) {
    const msg = await res.text();
    console.error('Entry error:', res.status, msg);
    throw new Error('Error registering entry');
  }
  return res.json();
}

// Registra salida de vehículo
async function registerExit(plate) {
  const res = await apiFetch(`${CORE_API_URL}/exits`, {
    method: 'POST',
    body: JSON.stringify({ plate }),
  });
  if (!res.ok) {
    const msg = await res.text();
    console.error('Exit error:', res.status, msg);
    throw new Error('Error registering exit');
  }
  return res.json();
}