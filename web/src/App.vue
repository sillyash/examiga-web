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
  align-items: center;
}

.site-header {
  width: 100%;
}

.site-footer {
  width: 100%;
}

main {
  flex: 1 0 auto;
  padding: 1rem;
  width: 70%;
}
</style>
