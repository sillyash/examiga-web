<template>
  <PageLayout title="Contact">
    <div class="content">
      <div id="#socials">
        <a class="social-link" href="https://www.tiktok.com/@examigaband" target="_blank">
          <img src="@/assets/tiktok.png">
          <p>Tiktok</p>
        </a>
        <a class="social-link" href="https://www.instagram.com/examigaband/" target="_blank">
          <img src="@/assets/instagram.png">
          <p>Instagram</p>
        </a>
      </div>
    </div>
  </PageLayout>
</template>

<style scoped>
#socials {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-content: center;
}

.social-link {
  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;
  align-content: center;
}

.social-link>img {
  height: 3rem;
  min-height: 20px;
  max-height: 60px;

  margin-right: 1rem;
  transition: filter var(--theme-transition-duration) ease-in-out;
}

:root[data-theme='night'] .social-link > img {
  filter: invert(1);
}
</style>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'

export default {
  name: "ContactView",

  components: {
    PageLayout
  }
};
</script>
