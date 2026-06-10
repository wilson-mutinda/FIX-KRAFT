const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// No trailing slash
const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
export const API_BASE_URI = `${cleanBase}/api`;
