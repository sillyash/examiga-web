<template>
  <PageLayout :title="$t('pages.guestbook')">
    <ShoutoutForm @posted="addShoutout" />

    <p v-if="loading" class="status">{{ $t('guestbook.loading') }}</p>

    <p v-else-if="error" class="status">
      {{ $t('guestbook.loadError') }}
      <button type="button" @click="loadShoutouts">{{ $t('common.retry') }}</button>
    </p>

    <template v-else>
      <ShoutoutCard v-for="shoutout in shoutouts" :key="shoutout.id" :shoutout="shoutout" />
      <p v-if="shoutouts.length === 0" class="status">{{ $t('guestbook.empty') }}</p>

      <div v-if="hasMore" class="status">
        <p v-if="loadMoreError">{{ $t('guestbook.loadMoreError') }}</p>
        <button type="button" :disabled="loadingMore" @click="loadMore">
          {{
            loadingMore
              ? $t('guestbook.loadingMore')
              : loadMoreError
                ? $t('common.retry')
                : $t('guestbook.loadMore')
          }}
        </button>
      </div>
    </template>
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import ShoutoutCard from '@/components/ShoutoutCard.vue'
import ShoutoutForm from '@/components/ShoutoutForm.vue'
import { getShoutouts, type Shoutout } from '@/api'

export default {
  name: 'GuestbookView',

  components: {
    PageLayout,
    ShoutoutCard,
    ShoutoutForm,
  },

  data() {
    return {
      shoutouts: [] as Shoutout[],
      hasMore: false,
      loading: true,
      error: false,
      loadingMore: false,
      loadMoreError: false,
    }
  },

  mounted() {
    this.loadShoutouts()
  },

  methods: {
    async loadShoutouts() {
      this.loading = true
      this.error = false
      try {
        const page = await getShoutouts()
        this.shoutouts = page.shoutouts
        this.hasMore = page.has_more
      } catch (err) {
        console.error(err)
        this.error = true
      } finally {
        this.loading = false
      }
    },

    // Next page = the shoutouts posted before the oldest one shown so far.
    async loadMore() {
      const oldest = this.shoutouts.at(-1)
      if (!oldest) return

      this.loadingMore = true
      this.loadMoreError = false
      try {
        const page = await getShoutouts(oldest.id)
        this.shoutouts.push(...page.shoutouts)
        this.hasMore = page.has_more
      } catch (err) {
        console.error(err)
        this.loadMoreError = true
      } finally {
        this.loadingMore = false
      }
    },

    // The list is newest first, so a fresh shoutout goes on top.
    addShoutout(shoutout: Shoutout) {
      this.shoutouts.unshift(shoutout)
    },
  },
}
</script>

<style scoped>
.status {
  text-align: center;
  opacity: 0.8;
}

.status p {
  margin: 0 0 0.5rem;
}

.status button {
  font: inherit;
  padding: 0.1rem 0.8rem;
  color: var(--color-text);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

.status button:hover:not(:disabled),
.status button:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

.status button:disabled {
  cursor: wait;
}
</style>
