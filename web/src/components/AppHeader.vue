<template>
  <header class="site-header">
    <RouterLink id="branding" to="/">
      <img src="/logo.jpg" :alt="$t('header.logoAlt')" width="100" height="100" />
      <h1>EX-AMIGA</h1>
    </RouterLink>

    <div id="navbar">
      <RouterLink to="/" class="nav-link">{{ $t('nav.home') }}</RouterLink>
      <RouterLink to="/shows" class="nav-link">{{ $t('nav.shows') }}</RouterLink>
      <RouterLink to="/guestbook" class="nav-link">{{ $t('nav.guestbook') }}</RouterLink>
      <RouterLink to="/about" class="nav-link">{{ $t('nav.about') }}</RouterLink>
      <RouterLink to="/contact" class="nav-link">{{ $t('nav.contact') }}</RouterLink>
    </div>

    <div class="header-toggles">
      <LanguageToggle />
      <ThemeToggle />
    </div>
  </header>
</template>

<style scoped>
#branding {
  display: flex;
  align-items: center;
  gap: 1rem;
  /* It's a home link, but should look like plain branding. */
  color: inherit;
  text-decoration: none;
}

.site-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.header-toggles {
  display: flex;
  gap: 0.5rem;
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

  .header-toggles {
    justify-self: center;
  }
}
</style>

<script lang="ts">
import LanguageToggle from '@/components/LanguageToggle.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'

export default {
  name: 'AppHeader',
  components: {
    LanguageToggle,
    ThemeToggle,
  },
}
</script>
