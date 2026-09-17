<template>
  <AppHeader />

  <main>
    <p>A</p>
  </main>
</template>

<script lang="ts">
import AppHeader from '@/components/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
  },
}
</script>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 2px solid var(--color-border);
}

main {
  padding: 1rem;
}
</style>
