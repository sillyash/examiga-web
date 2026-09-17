// Typed client for the EX-AMIGA API (see ../api/app.py and ../api/schemas.py).
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export interface TourDate {
  id: number
  date: string
  city: string
  venue: string
  ticket_url: string | null
  is_sold_out: boolean
  notes: string | null
}

export interface Shoutout {
  id: number
  name: string
  message: string
  created_at: string
}

export interface ShoutoutInput {
  name: string
  message: string
}

export class ApiError extends Error {
  status: number
  // marshmallow validation errors, e.g. { json: { name: ["..."] } }
  details?: Record<string, unknown>

  constructor(status: number, message: string, details?: Record<string, unknown>) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => undefined)
    throw new ApiError(response.status, body?.message ?? response.statusText, body?.detail)
  }

  return response.json() as Promise<T>
}

/** List all tour dates, soonest first. */
export function getTourDates(): Promise<TourDate[]> {
  return request('/api/tour-dates')
}

/** List all fan shoutouts, newest first. */
export function getShoutouts(): Promise<Shoutout[]> {
  return request('/api/shoutouts')
}

/** Leave a shoutout for the band. */
export function createShoutout(shoutout: ShoutoutInput): Promise<Shoutout> {
  return request('/api/shoutouts', {
    method: 'POST',
    body: JSON.stringify(shoutout),
  })
}
