<template>
  <form class="contact-form" novalidate @submit.prevent="submit">
    <h2>{{ $t('contactForm.title') }}</h2>

    <label for="contact-name">{{ $t('contactForm.nameLabel') }}</label>
    <input
      id="contact-name"
      v-model="name"
      type="text"
      autocomplete="name"
      placeholder="Casey54"
      :aria-invalid="Boolean(fieldErrors.name)"
    />
    <p v-if="fieldErrors.name" class="error">{{ $t(fieldErrors.name) }}</p>

    <label for="contact-email">{{ $t('contactForm.emailLabel') }}</label>
    <input
      id="contact-email"
      v-model="email"
      type="email"
      autocomplete="email"
      :placeholder="$t('contactForm.emailPlaceholder')"
      :aria-invalid="Boolean(fieldErrors.email)"
    />
    <p v-if="fieldErrors.email" class="error">{{ $t(fieldErrors.email) }}</p>

    <label for="contact-inquiry-type">{{ $t('contactForm.inquiryLabel') }}</label>
    <select
      id="contact-inquiry-type"
      v-model="inquiryType"
      :aria-invalid="Boolean(fieldErrors.inquiryType)"
    >
      <option value="" disabled>{{ $t('contactForm.choose') }}</option>
      <!-- Values stay in English: they become the email subject sent to the band. -->
      <option value="Booking">{{ $t('contactForm.inquiry.booking') }}</option>
      <option value="Press">{{ $t('contactForm.inquiry.press') }}</option>
      <option value="Fan mail">{{ $t('contactForm.inquiry.fanMail') }}</option>
      <option value="Other">{{ $t('contactForm.inquiry.other') }}</option>
    </select>
    <p v-if="fieldErrors.inquiryType" class="error">{{ $t(fieldErrors.inquiryType) }}</p>

    <label for="contact-message">{{ $t('contactForm.messageLabel') }}</label>
    <textarea
      id="contact-message"
      v-model="message"
      rows="4"
      :placeholder="$t('contactForm.messagePlaceholder')"
      :aria-invalid="Boolean(fieldErrors.message)"
    ></textarea>
    <p v-if="fieldErrors.message" class="error">{{ $t(fieldErrors.message) }}</p>

    <div class="form-footer">
      <p v-if="opened" class="thanks" role="status">{{ $t('contactForm.opening') }}</p>
      <button type="submit">{{ $t('contactForm.send') }}</button>
    </div>
  </form>
</template>

<script lang="ts">
export default {
  name: 'ContactForm',

  data() {
    return {
      name: '',
      email: '',
      inquiryType: '',
      message: '',
      opened: false,
      // field -> i18n key of its error, translated in the template
      fieldErrors: {} as Record<string, string>,
    }
  },

  methods: {
    submit() {
      this.opened = false
      this.fieldErrors = {}

      if (!this.name.trim()) this.fieldErrors.name = 'contactForm.errors.name'
      if (!this.email.trim()) this.fieldErrors.email = 'contactForm.errors.email'
      if (!this.inquiryType) this.fieldErrors.inquiryType = 'contactForm.errors.inquiryType'
      if (!this.message.trim()) this.fieldErrors.message = 'contactForm.errors.message'
      if (Object.keys(this.fieldErrors).length > 0) return

      const subject = encodeURIComponent(this.inquiryType)
      const body = encodeURIComponent(
        `Name: ${this.name.trim()}\nEmail: ${this.email.trim()}\n\n${this.message.trim()}`,
      )
      window.location.href = `mailto:contact@examigaband.com?subject=${subject}&body=${body}`
      this.opened = true
    },
  },
}
</script>

<style scoped>
.contact-form {
  display: flex;
  flex-direction: column;
  max-width: 30rem;
  margin: 1.5rem auto 3rem;
  padding: 1rem 1.25rem;
  background: var(--color-surface);
  border: 3px solid var(--color-border);
  box-shadow: 6px 6px 0 var(--color-accent);
  transition:
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

h2 {
  margin: 0 0 0.5rem;
}

label {
  margin-top: 0.5rem;
}

input,
select,
textarea {
  font: inherit;
  font-size: 1.25rem;
  padding: 0.25rem 0.5rem;
  color: var(--color-text);
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: 0;
  transition:
    background-color var(--theme-transition-duration) ease,
    border-color var(--theme-transition-duration) ease;
}

textarea {
  resize: vertical;
}

input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  outline: 3px dashed var(--color-accent);
  outline-offset: 2px;
}

[aria-invalid='true'] {
  border-color: var(--color-accent);
}

.error {
  margin: 0.25rem 0 0;
  color: var(--color-accent);
  font-size: 1.15rem;
}

.thanks {
  margin: 0;
}

.form-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem 1rem;
  margin-top: 0.75rem;
}

button {
  font: inherit;
  padding: 0.1rem 0.8rem;
  color: var(--color-text);
  background: transparent;
  border: 2px solid var(--color-border);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;
}

button:hover,
button:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}
</style>
