import axios from 'axios'

export const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export async function createRun(query: string) {
  const res = await axios.post(`${API_BASE}/api/v1/runs`, { query })
  return res.data
}

export async function getSources() {
  const res = await axios.get(`${API_BASE}/api/v1/sources`)
  return res.data
}

export function reportUrl(path: string) {
  return `${API_BASE}${path}`
}
