<template>
  <h1 class="page-title">{{ title }}</h1>

  <div class="page-content">
    <slot />
  </div>
</template>

<script lang="ts">
export default {
  name: 'PageLayout',
  props: {
    title: {
      type: String,
      required: true,
    },
  },
}
</script>

<style scoped>
.page-content {
  padding: 0 1.5rem;
}
</style>
