<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale, t } = useI18n()

function toggleLocale() {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
}
</script>

<template>
  <!-- Shows the language you'd switch to, labelled in the current one. -->
  <button type="button" class="lang-toggle" :aria-label="t('lang.switch')" @click="toggleLocale">
    {{ t('lang.short') }}
  </button>
</template>

<style scoped>
.lang-toggle {
  flex: none;
  width: 2.75rem;
  height: 2.75rem;
  padding: 0;
  font: inherit;
  font-size: 1.4rem;
  line-height: 1;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    color 0.2s ease,
    transform 0.15s ease;
}

.lang-toggle:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.lang-toggle:active {
  transform: scale(0.88);
}
</style>
