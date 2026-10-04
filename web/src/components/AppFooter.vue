<template>
  <footer class="site-footer">
    <p>{{ $t('footer.rights', { year: new Date().getFullYear() }) }}</p>
  </footer>
</template>

<style scoped>
.site-footer {
  padding: 1rem;
  text-align: center;
  border-top: 2px solid var(--color-border);
}

.site-footer p {
  margin: 0;
}
</style>
