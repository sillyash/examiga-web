<script setup lang="ts">
import ThemeToggle from '@/components/ThemeToggle.vue'
</script>

<template>
  <header class="site-header">
    <h1>EX-AMIGA</h1>
    <ThemeToggle />
  </header>

  <main>
    <h2>You did it!</h2>
    <p>
      Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
      documentation
    </p>
  </main>
</template>

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
