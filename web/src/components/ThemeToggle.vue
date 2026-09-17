<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

const { theme, toggleTheme } = useTheme()
</script>

<template>
  <button type="button" class="theme-toggle" @click="toggleTheme">
    {{ theme === 'day' ? '🌙 Night' : '☀️ Day' }}
  </button>
</template>

<style scoped>
.theme-toggle {
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text);
  padding: 0.4em 0.8em;
  font: inherit;
  cursor: pointer;
}
</style>
