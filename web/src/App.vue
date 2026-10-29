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
import { getCurrentInstance } from 'vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
  },
  mounted() {
    // Source - https://stackoverflow.com/q/75864713
    // Posted by DrKlonk
    // Retrieved 2026-10-29, License - CC BY-SA 4.0
    const version = getCurrentInstance()?.appContext.config.globalProperties.versionNumber
    console.info(`examiga-web version v${version}`)
  }
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

@media (max-width: 700px) {
  main {
    width: 85%
  }
}
</style>
