<template>
    <header class="site-header">
        <div id="branding">
            <img src="/logo.jpg" alt="EX-AMIGA Logo" width="100" height="100" />
            <h1>EX-AMIGA</h1>
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
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 2px solid var(--color-border);
}
</style>

<script lang="ts">
import ThemeToggle from '@/components/ThemeToggle.vue'

export default {
    name: 'AppHeader',
    components: {
        ThemeToggle
    },
}
</script>
