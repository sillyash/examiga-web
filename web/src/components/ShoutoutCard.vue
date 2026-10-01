<template>
  <article class="note">
    <p class="message">{{ shoutout.message }}</p>
    <p class="signature">
      — <span class="name">{{ shoutout.name }}</span> ·
      <time :datetime="shoutout.created_at">{{ date }}</time>
    </p>
  </article>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import type { Shoutout } from '@/api'

export default {
  name: 'ShoutoutCard',

  props: {
    shoutout: {
      type: Object as PropType<Shoutout>,
      required: true,
    },
  },

  computed: {
    date(): string {
      return new Date(this.shoutout.created_at).toLocaleDateString(this.$i18n.locale, {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      })
    },
  },
}
</script>

<style scoped>
.note {
  position: relative;
  max-width: 30rem;
  margin: 2rem auto;
  padding: 1.25rem 1.25rem 0.75rem;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 5px 5px 0 var(--color-border);
  transform: rotate(0.6deg);
  transition:
    transform 0.2s ease,
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

/* Alternate the tilt so the notes look taped up by hand. */
.note:nth-of-type(even) {
  transform: rotate(-0.6deg);
}

.note:hover {
  transform: rotate(0deg);
}

/* A strip of tape holding the note up. */
.note::before {
  content: '';
  position: absolute;
  top: -0.8rem;
  left: 50%;
  width: 5rem;
  height: 1.4rem;
  background: var(--color-accent);
  opacity: 0.75;
  transform: translateX(-50%) rotate(-3deg);
}

.message {
  margin: 0;
  white-space: pre-line;
  overflow-wrap: anywhere;
}

.signature {
  margin: 0.75rem 0 0;
  text-align: right;
  font-size: 1.15rem;
  opacity: 0.8;
}

.name {
  color: var(--color-accent);
}

@media (prefers-reduced-motion: reduce) {
  .note,
  .note:nth-of-type(even),
  .note:hover {
    transform: none;
    transition: none;
  }
}
</style>
