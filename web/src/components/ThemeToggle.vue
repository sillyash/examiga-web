<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

const { theme, toggleTheme } = useTheme()
</script>

<template>
  <button
    type="button"
    class="theme-toggle"
    :aria-label="theme === 'day' ? 'Switch to night theme' : 'Switch to day theme'"
    @click="toggleTheme"
  >
    <Transition name="flip" mode="out-in">
      <svg
        v-if="theme === 'day'"
        key="sun"
        class="theme-icon"
        viewBox="0 0 24 24"
        width="22"
        height="22"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <circle cx="12" cy="12" r="4" />
        <line x1="12" y1="1" x2="12" y2="4" />
        <line x1="12" y1="20" x2="12" y2="23" />
        <line x1="1" y1="12" x2="4" y2="12" />
        <line x1="20" y1="12" x2="23" y2="12" />
        <line x1="4.22" y1="4.22" x2="6.34" y2="6.34" />
        <line x1="17.66" y1="17.66" x2="19.78" y2="19.78" />
        <line x1="4.22" y1="19.78" x2="6.34" y2="17.66" />
        <line x1="17.66" y1="6.34" x2="19.78" y2="4.22" />
      </svg>
      <svg v-else key="moon" class="theme-icon" viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
        <path d="M20 12a8 8 0 1 1-8-8 6 6 0 0 0 8 8z" />
      </svg>
    </Transition>
  </button>
</template>

<style scoped>
.theme-toggle {
  flex: none;
  width: 2.75rem;
  height: 2.75rem;
  padding: 0;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  background: var(--color-surface);
  color: var(--color-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    color 0.2s ease,
    transform 0.15s ease;
}

.theme-toggle:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.theme-toggle:active {
  transform: scale(0.88);
}

.theme-icon {
  display: block;
}

.flip-enter-active,
.flip-leave-active {
  transition:
    transform 0.35s ease,
    opacity 0.35s ease;
}

.flip-enter-from {
  transform: rotate(-120deg) scale(0.4);
  opacity: 0;
}

.flip-leave-to {
  transform: rotate(120deg) scale(0.4);
  opacity: 0;
}
</style>
