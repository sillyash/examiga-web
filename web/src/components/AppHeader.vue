<template>
    <header class="site-header">
        <h1>EX-AMIGA</h1>
        <ThemeToggle />
    </header>
</template>

<style scoped>
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
