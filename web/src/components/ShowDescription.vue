<template>
  <article class="ticket" :class="{ 'is-sold-out': tourDate.is_sold_out, 'is-past': isPast }">
    <div class="ticket-stub">
      <span class="stub-month">{{ month }}</span>
      <span class="stub-day">{{ day }}</span>
      <span class="stub-weekday">{{ weekday }}</span>
      <span v-if="time" class="stub-time">{{ time }}</span>
    </div>

    <div class="ticket-body">
      <h2 class="venue">{{ tourDate.venue }}</h2>
      <p class="city">~ {{ tourDate.city }} ~</p>
      <p v-if="tourDate.address" class="address">
        <a :href="mapUrl">{{ tourDate.address }}</a>
      </p>
      <p v-if="tourDate.notes" class="notes">“{{ tourDate.notes }}”</p>

      <div class="ticket-footer">
        <a
          v-if="tourDate.info_url"
          class="info-link"
          :href="tourDate.info_url"
          target="_blank"
          rel="noopener noreferrer"
        >
          {{ $t('ticket.moreInfo') }}
        </a>
        <span v-if="isPast" class="status">{{ $t('ticket.seeYou') }}</span>
        <span v-else-if="tourDate.is_sold_out" class="status">{{ $t('ticket.soldOutMsg') }}</span>
        <a
          v-else-if="tourDate.ticket_url"
          class="tickets-link"
          :href="tourDate.ticket_url"
          target="_blank"
          rel="noopener noreferrer"
        >
          {{ $t('ticket.getTickets') }}
        </a>
        <span v-else class="status">{{ $t('ticket.atDoor') }}</span>
      </div>

      <span v-if="tourDate.is_sold_out" class="stamp" :aria-label="$t('ticket.soldOutLabel')">{{
        $t('ticket.soldOutStamp')
      }}</span>
    </div>

    <button v-if="!isPast" type="button" class="ticket-calendar" @click="addToCalendar">
      <span class="calendar-plus" aria-hidden="true">+</span>
      <span class="calendar-label">{{ $t('ticket.addToCalendar') }}</span>
    </button>
  </article>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import type { TourDate } from '@/api'

export default {
  name: 'ShowDescription',

  props: {
    tourDate: {
      type: Object as PropType<TourDate>,
      required: true,
    },
  },

  computed: {
    // Parse "YYYY-MM-DD" as a local date: `new Date('2026-10-12')` would be read as
    // UTC midnight and can show up as the previous day in negative timezones.
    parsedDate(): Date {
      const [year = 0, month = 1, day = 1] = this.tourDate.date.split('-').map(Number)
      return new Date(year, month - 1, day)
    },

    locale(): string {
      return this.$i18n.locale
    },

    month(): string {
      return this.parsedDate.toLocaleDateString(this.locale, { month: 'short' }).replace('.', '')
    },

    day(): string {
      return String(this.parsedDate.getDate()).padStart(2, '0')
    },

    weekday(): string {
      return this.parsedDate.toLocaleDateString(this.locale, { weekday: 'short' }).replace('.', '')
    },

    // "HH:MM:SS" from the API, formatted per locale ("20:30" in fr, "8:30 PM" in en).
    time(): string | null {
      if (!this.tourDate.time) return null
      const [hours = 0, minutes = 0] = this.tourDate.time.split(':').map(Number)
      const at = new Date(this.parsedDate)
      at.setHours(hours, minutes)
      return at.toLocaleTimeString(this.locale, { hour: 'numeric', minute: '2-digit' })
    },

    // geo: URI so the device opens whatever maps app it has set up.
    mapUrl(): string {
      return `geo:0,0?q=${encodeURIComponent(this.tourDate.address ?? '')}`
    },

    isPast(): boolean {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      return this.parsedDate < today
    },
  },

  methods: {
    // Builds a one-event .ics file and hands it to the browser, which passes it on to
    // the device's calendar app (or just downloads it on desktop).
    addToCalendar() {
      const { id, date, time, venue, city, address, notes, info_url } = this.tourDate
      const day = date.replaceAll('-', '')

      // No set time yet → all-day event. Times are "floating" (no timezone), so they're
      // read as local time on the fan's device.
      const when = time
        ? [`DTSTART:${day}T${time.replaceAll(':', '')}`, 'DURATION:PT2H']
        : [`DTSTART;VALUE=DATE:${day}`]

      const lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//EX-AMIGA//Shows//EN',
        'BEGIN:VEVENT',
        `UID:tour-date-${id}@examiga`,
        `DTSTAMP:${new Date().toISOString().replace(/[-:]|\.\d{3}/g, '')}`,
        ...when,
        `SUMMARY:${escapeIcs(`EX-AMIGA @ ${venue}`)}`,
        `LOCATION:${escapeIcs([venue, address ?? city].join(', '))}`,
        ...(notes ? [`DESCRIPTION:${escapeIcs(notes)}`] : []),
        ...(info_url ? [`URL:${info_url}`] : []),
        'END:VEVENT',
        'END:VCALENDAR',
      ]

      const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar;charset=utf-8' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `examiga-${date}.ics`
      link.click()
      URL.revokeObjectURL(link.href)
    },
  },
}

// Escape text for an iCalendar TEXT value (RFC 5545 §3.3.11).
function escapeIcs(text: string): string {
  return text.replace(/[\\;,]/g, (char) => `\\${char}`).replace(/\n/g, '\\n')
}
</script>

<style scoped>
.ticket {
  --notch-size: 0.9rem;

  position: relative;
  display: flex;
  max-width: 34rem;
  margin: 1.5rem auto;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-border);
  transform: rotate(-0.8deg);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

/* Alternate the tilt so a list of tickets looks hand-pinned to a corkboard. */
.ticket:nth-of-type(even) {
  transform: rotate(0.8deg);
}

.ticket:hover,
.ticket:focus-within {
  transform: rotate(0deg) translate(-2px, -2px);
  box-shadow: 8px 8px 0 var(--color-accent);
}

.ticket-stub {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 6rem;
  padding: 1rem 0.75rem;
  background: var(--color-accent);
  color: var(--color-surface);
  border-right: 3px dashed var(--color-border);
  line-height: 1;
  text-transform: uppercase;
}

/* Half-circle "punch holes" where the stub would tear off. */
.ticket-stub::before,
.ticket-stub::after {
  content: '';
  position: absolute;
  right: calc(var(--notch-size) / -2 - 1.5px);
  width: var(--notch-size);
  height: var(--notch-size);
  background: var(--color-bg);
  border: 3px solid var(--color-border);
  border-radius: 50%;
  transition: background-color var(--theme-transition-duration) ease;
}

.ticket-stub::before {
  top: calc(var(--notch-size) / -2 - 3px);
}

.ticket-stub::after {
  bottom: calc(var(--notch-size) / -2 - 3px);
}

.stub-month,
.stub-weekday {
  font-size: 1.4rem;
  letter-spacing: 0.1em;
}

.stub-day {
  font-size: 3.5rem;
}

.stub-time {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  letter-spacing: 0.05em;
}

.ticket-body {
  position: relative;
  flex: 1;
  padding: 0.75rem 1.25rem;
  min-width: 0;
}

.venue {
  margin: 0;
  font-size: 2rem;
  line-height: 1.1;
  overflow-wrap: anywhere;
}

.city {
  margin: 0.25rem 0 0;
  opacity: 0.85;
}

.address {
  margin: 0.25rem 0 0;
  font-size: 0.95rem;
}

.address a {
  color: inherit;
  text-decoration: underline dotted;
}

.notes {
  margin: 0.5rem 0 0;
  overflow-wrap: anywhere;
  font-style: italic;
  font-size: 1.25rem;
}

.ticket-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem 1rem;
  margin-top: 0.75rem;
}

.info-link {
  color: var(--color-text);
}

.tickets-link {
  display: inline-block;
  padding: 0.1rem 0.6rem;
  border: 2px solid var(--color-border);
  color: var(--color-text);
  text-decoration: none;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.tickets-link:hover,
.tickets-link:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

.status {
  opacity: 0.75;
}

/* Right-hand stub, torn off along a dashed line like the date stub on the left. */
.ticket-calendar {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  width: 5.5rem;
  padding: 1rem 0.5rem;
  font: inherit;
  line-height: 1;
  text-transform: uppercase;
  color: var(--color-text);
  background: transparent;
  border: none;
  border-left: 3px dashed var(--color-border);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.ticket-calendar:hover,
.ticket-calendar:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

.ticket-calendar::before,
.ticket-calendar::after {
  content: '';
  position: absolute;
  left: calc(var(--notch-size) / -2 - 1.5px);
  width: var(--notch-size);
  height: var(--notch-size);
  background: var(--color-bg);
  border: 3px solid var(--color-border);
  border-radius: 50%;
  transition: background-color var(--theme-transition-duration) ease;
}

.ticket-calendar::before {
  top: calc(var(--notch-size) / -2 - 3px);
}

.ticket-calendar::after {
  bottom: calc(var(--notch-size) / -2 - 3px);
}

.calendar-plus {
  font-size: 3rem;
}

.calendar-label {
  font-size: 1rem;
  letter-spacing: 0.05em;
}

.stamp {
  position: absolute;
  top: 50%;
  right: 1rem;
  padding: 0.1rem 0.5rem;
  border: 3px double var(--color-accent);
  color: var(--color-accent);
  font-size: 2rem;
  letter-spacing: 0.1em;
  transform: translateY(-50%) rotate(-14deg);
  opacity: 0.85;
  pointer-events: none;
}

.is-sold-out .venue,
.is-sold-out .city {
  opacity: 0.6;
}

.is-past {
  filter: grayscale(1);
  opacity: 0.6;
}

@media (max-width: 480px) {
  .ticket-stub {
    min-width: 4.5rem;
  }

  .stub-day {
    font-size: 2.5rem;
  }

  /* Not enough room for a third column: the calendar stub tears off the bottom instead. */
  .ticket {
    flex-wrap: wrap;
  }

  .ticket-calendar {
    flex-direction: row;
    flex-basis: 100%;
    gap: 0.5rem;
    padding: 0.4rem;
    border-left: none;
    border-top: 3px dashed var(--color-border);
  }

  .ticket-calendar::before,
  .ticket-calendar::after {
    top: calc(var(--notch-size) / -2 - 1.5px);
    bottom: auto;
  }

  .ticket-calendar::before {
    left: calc(var(--notch-size) / -2 - 3px);
  }

  .ticket-calendar::after {
    left: auto;
    right: calc(var(--notch-size) / -2 - 3px);
  }

  .calendar-plus {
    font-size: 1.75rem;
  }

  .venue {
    font-size: 1.6rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticket,
  .ticket:nth-of-type(even),
  .ticket:hover,
  .ticket:focus-within {
    transform: none;
    transition: none;
  }
}
</style>
