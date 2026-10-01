<template>
  <PageLayout title="Shows">
    <p v-if="loading" class="status">loading shows…</p>

    <p v-else-if="error" class="status">
      couldn't load the shows :( <button type="button" @click="loadShows">try again</button>
    </p>

    <template v-else>
      <section>
        <h2>Upcoming</h2>
        <ShowDescription v-for="show in upcomingShows" :key="show.id" :tour-date="show" />
        <p v-if="upcomingShows.length === 0" class="status">
          no shows planned right now, stay tuned ♡
        </p>
      </section>

      <section v-if="pastShows.length > 0">
        <h2>Past shows</h2>
        <ShowDescription v-for="show in pastShows" :key="show.id" :tour-date="show" />
      </section>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import ShowDescription from '@/components/ShowDescription.vue'
import { getTourDates, type TourDate } from '@/api'

// Today as "YYYY-MM-DD" in local time, comparable as a string with TourDate.date.
function todayIso(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${now.getFullYear()}-${month}-${day}`
}

export default {
  name: 'ShowsView',

  components: {
    PageLayout,
    ShowDescription,
  },

  data() {
    return {
      shows: [] as TourDate[],
      loading: true,
      error: false,
    }
  },

  computed: {
    // The API returns shows soonest first, so upcoming shows are already in order.
    upcomingShows(): TourDate[] {
      const today = todayIso()
      return this.shows.filter((show) => show.date >= today)
    },

    // Most recent past show first.
    pastShows(): TourDate[] {
      const today = todayIso()
      return this.shows.filter((show) => show.date < today).reverse()
    },
  },

  mounted() {
    this.loadShows()
  },

  methods: {
    async loadShows() {
      this.loading = true
      this.error = false
      try {
        this.shows = await getTourDates()
      } catch (err) {
        console.error(err)
        this.error = true
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
section + section {
  margin-top: 3rem;
}

h2 {
  border-bottom: 2px dashed var(--color-border);
}

.status {
  text-align: center;
  opacity: 0.8;
}

.status button {
  font: inherit;
  color: var(--color-text);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  cursor: pointer;
}
</style>
