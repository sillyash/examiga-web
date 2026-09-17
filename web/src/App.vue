<template>
  <AppHeader />

  <main>
    <RouterView />
  </main>

  <AppFooter />
</template>

<script lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
  },
}
</script>

<style scoped>
:global(#app) {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 2px solid var(--color-border);
}

main {
  flex: 1 0 auto;
  padding: 1rem;
}
</style>
