<template>
  <header class="site-header">
    <div id="branding">
      <img src="/logo.jpg" alt="EX-AMIGA Logo" width="100" height="100" />
      <h1>EX-AMIGA</h1>
    </div>

    <div id="navbar">
      <RouterLink to="/" class="nav-link">Home</RouterLink>
      <RouterLink to="/shows" class="nav-link">Shows</RouterLink>
      <RouterLink to="/guestbook" class="nav-link">Guestbook</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
      <RouterLink to="/contact" class="nav-link">Contact</RouterLink>
    </div>

    <ThemeToggle />
  </header>
</template>

<style scoped>
#branding {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.site-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.site-header > .theme-toggle {
  justify-self: end;
}

#navbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1rem;
}

.nav-link {
  font-weight: bold;
  font-size: 1.7rem;
  color: var(--color-accent);
  text-decoration: underline;
}

.nav-link.router-link-exact-active {
  color: var(--color-text);
  text-decoration: none;
}

@media (max-width: 700px) {
  .site-header {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 1rem;
  }

  .site-header > .theme-toggle {
    justify-self: center;
  }
}
</style>

<script lang="ts">
import ThemeToggle from '@/components/ThemeToggle.vue'

export default {
  name: 'AppHeader',
  components: {
    ThemeToggle,
  },
}
</script>
