<template>
  <section class="hero">
    <img class="hero-photo" src="/logo.jpg" :alt="$t('home.photoAlt')" />
    <p class="tagline">{{ $t('home.tagline') }}</p>
    <div class="hero-links">
      <RouterLink to="/shows" class="cta">{{ $t('home.toShows') }}</RouterLink>
      <RouterLink to="/guestbook" class="cta">{{ $t('home.toGuestbook') }}</RouterLink>
    </div>
  </section>

  <section>
    <h2>{{ $t('home.nextShow') }}</h2>
    <p v-if="showsLoading" class="status">{{ $t('shows.loading') }}</p>
    <p v-else-if="showsError" class="status">{{ $t('shows.loadError') }}</p>
    <template v-else>
      <ShowDescription v-if="nextShow" :tour-date="nextShow" />
      <p v-else class="status">{{ $t('shows.none') }}</p>
      <p class="more">
        <RouterLink to="/shows">{{ $t('home.allShows') }}</RouterLink>
      </p>
    </template>
  </section>

  <section class="about">
    <h2>{{ $t('home.whoWeAre') }}</h2>
    <p>{{ $t('home.bio') }}</p>
    <ul class="members">
      <li v-for="member in members" :key="member.name">
        <span class="member-name">{{ member.name }}</span> —
        {{ member.roles.map((role) => $t(`home.roles.${role}`)).join(', ') }}
      </li>
    </ul>
    <p>
      <strong>{{ $t('home.influencesLabel') }}</strong> {{ influences.join(', ') }}
    </p>
  </section>

  <!-- Hidden if the guestbook can't load: it's a teaser, the Guestbook page has the errors. -->
  <section v-if="shoutouts.length > 0">
    <h2>{{ $t('home.fromGuestbook') }}</h2>
    <ShoutoutCard v-for="shoutout in shoutouts" :key="shoutout.id" :shoutout="shoutout" />
    <p class="more">
      <RouterLink to="/guestbook">{{ $t('home.toGuestbook') }}</RouterLink>
    </p>
  </section>
</template>

<script lang="ts">
import ShowDescription from '@/components/ShowDescription.vue'
import ShoutoutCard from '@/components/ShoutoutCard.vue'
import { getShoutouts, getTourDates, type Shoutout, type TourDate } from '@/api'

// How many of the latest shoutouts to preview on the home page.
const SHOUTOUT_PREVIEW_COUNT = 3

// Names aren't translated, so they live here once instead of in both locale files.
// Roles are keys under `home.roles` in the locale files.
type Role = 'vocals' | 'guitar' | 'bass' | 'drums'

const MEMBERS: { name: string; roles: Role[] }[] = [
  { name: 'TODO name', roles: ['vocals', 'guitar'] },
  { name: 'TODO name 2', roles: ['guitar'] },
  { name: 'TODO name 3', roles: ['bass'] },
  { name: 'TODO name 4', roles: ['drums'] },
]

// Bands that inspired us, shown as "for fans of: …".
const INFLUENCES = ['American Football', "Cap'n Jazz", 'TODO']

// Today as "YYYY-MM-DD" in local time, comparable as a string with TourDate.date
// (same as in Shows.vue).
function todayIso(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${now.getFullYear()}-${month}-${day}`
}

export default {
  name: 'HomeView',

  components: {
    ShowDescription,
    ShoutoutCard,
  },

  data() {
    return {
      nextShow: null as TourDate | null,
      showsLoading: true,
      showsError: false,
      shoutouts: [] as Shoutout[],
      members: MEMBERS,
      influences: INFLUENCES,
    }
  },

  mounted() {
    this.loadNextShow()
    this.loadShoutouts()
  },

  methods: {
    // The API returns shows soonest first, so the first upcoming one is the next show.
    async loadNextShow() {
      try {
        const today = todayIso()
        const shows = await getTourDates()
        this.nextShow = shows.find((show) => show.date >= today) ?? null
      } catch (err) {
        console.error(err)
        this.showsError = true
      } finally {
        this.showsLoading = false
      }
    },

    async loadShoutouts() {
      try {
        const page = await getShoutouts()
        this.shoutouts = page.shoutouts.slice(0, SHOUTOUT_PREVIEW_COUNT)
      } catch (err) {
        console.error(err)
      }
    },
  },
}
</script>

<style scoped>
section {
  max-width: 34rem;
  margin: 0 auto;
}

section + section {
  margin-top: 3rem;
}

h2 {
  border-bottom: 2px dashed var(--color-border);
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero-photo {
  width: min(100%, 20rem);
  height: auto;
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-accent);
  transform: rotate(-1deg);
}

.tagline {
  margin: 1.5rem 0 1rem;
  font-size: 1.75rem;
}

.hero-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem 1rem;
}

.cta {
  padding: 0.1rem 0.8rem;
  color: var(--color-text);
  border: 2px solid var(--color-border);
  text-decoration: none;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.cta:hover,
.cta:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

.about {
  overflow-wrap: anywhere;
}

.members {
  padding-left: 1.25rem;
}

.member-name {
  color: var(--color-accent);
}

.status {
  text-align: center;
  opacity: 0.8;
}

.more {
  text-align: right;
}

.more a {
  color: var(--color-text);
}

@media (prefers-reduced-motion: reduce) {
  .hero-photo {
    transform: none;
  }
}
</style>
