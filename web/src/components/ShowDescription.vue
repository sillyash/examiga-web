<template>
  <article
    class="ticket"
    :class="{ 'is-sold-out': tourDate.is_sold_out, 'is-past': isPast, 'menu-open': menuOpen }"
  >
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

    <div
      v-if="!isPast"
      ref="calendar"
      class="ticket-calendar"
      @keydown.esc="closeMenu"
      @focusout="onCalendarFocusOut"
    >
      <button
        ref="calendarToggle"
        type="button"
        class="calendar-toggle"
        aria-haspopup="menu"
        :aria-expanded="menuOpen"
        :aria-controls="menuId"
        @click="toggleMenu"
      >
        <span class="calendar-plus" aria-hidden="true">+</span>
        <span class="calendar-label">{{ $t('ticket.addToCalendar') }}</span>
      </button>

      <ul v-if="menuOpen" :id="menuId" ref="calendarMenu" class="calendar-menu" role="menu">
        <li role="none">
          <a
            role="menuitem"
            :href="googleCalendarUrl"
            target="_blank"
            rel="noopener noreferrer"
            @click="closeMenu"
          >
            {{ $t('ticket.calendarGoogle') }}
          </a>
        </li>
        <li role="none">
          <button type="button" role="menuitem" @click="downloadIcs">
            {{ $t('ticket.calendarIcs') }}
          </button>
        </li>
      </ul>
    </div>
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

  data() {
    return {
      menuOpen: false,
    }
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

    menuId(): string {
      return `calendar-menu-${this.tourDate.id}`
    },

    // Event fields shared by the Google link and the .ics file. No set time yet →
    // all-day event; otherwise assume a 2h set. End dates are exclusive in both formats.
    calendarEvent() {
      const { time, venue, city, address, notes, info_url } = this.tourDate
      const start = new Date(this.parsedDate)
      const end = new Date(this.parsedDate)
      if (time) {
        const [hours = 0, minutes = 0] = time.split(':').map(Number)
        start.setHours(hours, minutes)
        end.setTime(start.getTime() + 2 * 60 * 60 * 1000)
      } else {
        end.setDate(end.getDate() + 1)
      }
      const allDay = !time
      return {
        title: `EX-AMIGA @ ${venue}`,
        location: [venue, address ?? city].join(', '),
        details: [notes, info_url].filter(Boolean).join('\n\n'),
        start: calendarStamp(start, allDay),
        end: calendarStamp(end, allDay),
        allDay,
      }
    },

    googleCalendarUrl(): string {
      const { title, location, details, start, end } = this.calendarEvent
      const params = new URLSearchParams({
        action: 'TEMPLATE',
        text: title,
        dates: `${start}/${end}`,
        location,
        details,
      })
      return `https://calendar.google.com/calendar/render?${params}`
    },
  },

  mounted() {
    document.addEventListener('pointerdown', this.onDocumentPointerDown)
  },

  beforeUnmount() {
    document.removeEventListener('pointerdown', this.onDocumentPointerDown)
  },

  methods: {
    toggleMenu() {
      if (this.menuOpen) {
        this.closeMenu()
        return
      }
      this.menuOpen = true
      // Move focus into the menu so keyboard users land on the first option.
      this.$nextTick(() => {
        const menu = this.$refs.calendarMenu as HTMLElement | undefined
        menu?.querySelector<HTMLElement>('[role="menuitem"]')?.focus()
      })
    },

    closeMenu() {
      if (!this.menuOpen) return
      this.menuOpen = false
      ;(this.$refs.calendarToggle as HTMLElement | undefined)?.focus()
    },

    onDocumentPointerDown(event: PointerEvent) {
      const calendar = this.$refs.calendar as HTMLElement | undefined
      if (this.menuOpen && !calendar?.contains(event.target as Node)) {
        this.menuOpen = false
      }
    },

    // Tabbing out of the menu closes it. A null relatedTarget (e.g. Safari not focusing
    // buttons on click) is left to the pointerdown listener, so it can't eat the click.
    onCalendarFocusOut(event: FocusEvent) {
      const next = event.relatedTarget as Node | null
      const calendar = this.$refs.calendar as HTMLElement | undefined
      if (next && !calendar?.contains(next)) {
        this.menuOpen = false
      }
    },

    // Builds a one-event .ics file for Apple Calendar / Outlook / Thunderbird and
    // hands it to the browser (opens the calendar app on mobile, downloads on desktop).
    downloadIcs() {
      const { title, location, details, start, end, allDay } = this.calendarEvent
      const dateValue = allDay ? ';VALUE=DATE' : ''

      const lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//EX-AMIGA//Shows//EN',
        'BEGIN:VEVENT',
        `UID:tour-date-${this.tourDate.id}@examiga`,
        `DTSTAMP:${new Date().toISOString().replace(/[-:]|\.\d{3}/g, '')}`,
        `DTSTART${dateValue}:${start}`,
        `DTEND${dateValue}:${end}`,
        `SUMMARY:${escapeIcs(title)}`,
        `LOCATION:${escapeIcs(location)}`,
        ...(details ? [`DESCRIPTION:${escapeIcs(details)}`] : []),
        ...(this.tourDate.info_url ? [`URL:${this.tourDate.info_url}`] : []),
        'END:VEVENT',
        'END:VCALENDAR',
      ]

      const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar;charset=utf-8' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `examiga-${this.tourDate.date}.ics`
      // Firefox wants the link in the document, and revoking the URL right after
      // click() can cancel the download, so wait a tick.
      document.body.appendChild(link)
      link.click()
      link.remove()
      setTimeout(() => URL.revokeObjectURL(link.href), 0)

      this.closeMenu()
    },
  },
}

// Escape text for an iCalendar TEXT value (RFC 5545 §3.3.11).
function escapeIcs(text: string): string {
  return text.replace(/[\\;,]/g, (char) => `\\${char}`).replace(/\n/g, '\\n')
}

// "YYYYMMDD" or "YYYYMMDDTHHMMSS" from the local date fields. No trailing Z: times are
// "floating", so both Google and .ics read them as the fan's local time.
function calendarStamp(date: Date, allDay: boolean): string {
  const pad = (n: number) => String(n).padStart(2, '0')
  const day = `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}`
  if (allDay) return day
  return `${day}T${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}`
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
  width: 5.5rem;
  border-left: 3px dashed var(--color-border);
}

.calendar-toggle {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 1rem 0.5rem;
  font: inherit;
  line-height: 1;
  text-transform: uppercase;
  color: var(--color-text);
  background: transparent;
  border: none;
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.calendar-toggle:hover,
.calendar-toggle:focus-visible,
.calendar-toggle[aria-expanded='true'] {
  background: var(--color-text);
  color: var(--color-surface);
}

.ticket-calendar::before,
.ticket-calendar::after {
  content: '';
  position: absolute;
  z-index: 1;
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

/* Each ticket's tilt transform makes its own stacking context: lift the open one so the
   menu isn't covered by the next ticket. */
.ticket.menu-open {
  z-index: 2;
}

.calendar-menu {
  position: absolute;
  top: calc(100% + 3px);
  right: -3px;
  z-index: 2;
  min-width: 13rem;
  margin: 0;
  padding: 0;
  list-style: none;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-border);
}

.calendar-menu [role='menuitem'] {
  display: block;
  width: 100%;
  padding: 0.4rem 0.75rem;
  font: inherit;
  text-align: left;
  text-decoration: none;
  color: var(--color-text);
  background: transparent;
  border: none;
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.calendar-menu li + li {
  border-top: 2px dashed var(--color-border);
}

.calendar-menu [role='menuitem']:hover,
.calendar-menu [role='menuitem']:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
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
    flex-basis: 100%;
    border-left: none;
    border-top: 3px dashed var(--color-border);
  }

  .calendar-toggle {
    flex-direction: row;
    gap: 0.5rem;
    padding: 0.4rem;
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
