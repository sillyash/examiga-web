<template>
  <PageLayout :title="$t('pages.contact')">
    <div class="content">
      <div class="contact-methods">
        <a
          class="contact-link"
          href="https://www.instagram.com/examigaband/"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Instagram"
        >
          <svg
            viewBox="0 0 24 24"
            width="28"
            height="28"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <rect x="2" y="2" width="20" height="20" rx="5" />
            <circle cx="12" cy="12" r="4.5" />
            <circle cx="17.5" cy="6.5" r="1.1" fill="currentColor" stroke="none" />
          </svg>
          <p>Instagram</p>
        </a>

        <a
          class="contact-link"
          href="https://www.tiktok.com/@examigaband"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="TikTok"
        >
          <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
            <path
              d="M16.5 2h-3v13.2a3.2 3.2 0 1 1-2.2-3V8.9a6.4 6.4 0 1 0 5.2 6.3V9.1a6 6 0 0 0 4.5 1.8V7.7A4.5 4.5 0 0 1 16.5 2z"
            />
          </svg>
          <p>TikTok</p>
        </a>

        <a
          class="contact-link"
          href="mailto:contact@examigaband.com"
          :aria-label="$t('contact.email')"
        >
          <svg
            viewBox="0 0 24 24"
            width="28"
            height="28"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <rect x="2" y="4" width="20" height="16" rx="2" />
            <path d="m3 6 9 7 9-7" />
          </svg>
          <p>contact@examigaband.com</p>
        </a>

        <a class="contact-link" href="tel:+33629276127" :aria-label="$t('contact.phone')">
          <svg
            viewBox="0 0 24 24"
            width="28"
            height="28"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 3 5a1 1 0 0 1 1-1z"
            />
          </svg>
          <p>+33 6 29 27 61 27</p>
        </a>
      </div>

      <ContactForm />
    </div>
  </PageLayout>
</template>

<style scoped>
.contact-methods {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.contact-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 1rem 1.25rem;
  min-width: 9rem;
  color: var(--color-text);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  text-decoration: none;
  text-align: center;
  transition:
    color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease,
    background-color var(--theme-transition-duration) ease;
}

.contact-link:hover,
.contact-link:focus-visible {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.contact-link:focus-visible {
  outline: 3px dashed var(--color-accent);
  outline-offset: 2px;
}

.contact-link p {
  margin: 0;
  word-break: break-word;
}
</style>

<script lang="ts">
import PageLayout from '@/components/PageLayout.vue'
import ContactForm from '@/components/ContactForm.vue'
export default { name: 'ContactView', components: { PageLayout, ContactForm } }
</script>
