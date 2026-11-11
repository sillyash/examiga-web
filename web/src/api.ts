// Typed client for the EX-AMIGA API (see ../api/shows/api.py).
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export interface TourDate {
  id: number
  date: string
  // "HH:MM:SS", or null if the set time isn't announced yet
  time: string | null
  city: string
  venue: string
  address: string | null
  ticket_url: string | null
  // event page / socials link for the show
  info_url: string | null
  is_sold_out: boolean
  notes: string | null
}

export interface Shoutout {
  id: number
  name: string
  message: string
  created_at: string
}

// DRF cursor page
export interface ShoutoutPage {
  results: Shoutout[]
  // URL of the next (older) page, or null if there's none left
  next: string | null
}

export interface ShoutoutInput {
  name: string
  message: string
  // honeypot, must stay empty (see ShoutoutForm.vue)
  website?: string
}

export class ApiError extends Error {
  status: number
  // DRF validation errors, e.g. { name: ["..."] }
  details?: Record<string, unknown>

  constructor(status: number, message: string, details?: Record<string, unknown>) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url.startsWith('http') ? url : `${API_BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => undefined)
    throw new ApiError(response.status, body?.detail ?? response.statusText, body)
  }

  return response.json() as Promise<T>
}

/** List all tour dates, soonest first. */
export function getTourDates(): Promise<TourDate[]> {
  return request('/api/tour-dates')
}

/**
 * List fan shoutouts, newest first, 10 at a time. Pass a page's `next` URL to get
 * the next (older) page.
 */
export function getShoutouts(next?: string): Promise<ShoutoutPage> {
  return request(next ?? '/api/shoutouts')
}

/** Leave a shoutout for the band. */
export function createShoutout(shoutout: ShoutoutInput): Promise<Shoutout> {
  return request('/api/shoutouts', {
    method: 'POST',
    body: JSON.stringify(shoutout),
  })
}
