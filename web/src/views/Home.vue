<template>
  <PageLayout :title="$t('pages.home')">
    <!-- home page content -->
  </PageLayout>
</template>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: 'HomeView',
  components: {
    PageLayout,
  },
}
</script>
