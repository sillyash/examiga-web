<template>
  <form class="contact-form" novalidate @submit.prevent="submit">
    <h2>send us a message ✎</h2>

    <label for="contact-name">your name</label>
    <input
      id="contact-name"
      v-model="name"
      type="text"
      autocomplete="name"
      placeholder="Casey54"
      :aria-invalid="Boolean(fieldErrors.name)"
    />
    <p v-if="fieldErrors.name" class="error">{{ fieldErrors.name }}</p>

    <label for="contact-email">your email</label>
    <input
      id="contact-email"
      v-model="email"
      type="email"
      autocomplete="email"
      placeholder="you@example.com"
      :aria-invalid="Boolean(fieldErrors.email)"
    />
    <p v-if="fieldErrors.email" class="error">{{ fieldErrors.email }}</p>

    <label for="contact-inquiry-type">inquiry type</label>
    <select
      id="contact-inquiry-type"
      v-model="inquiryType"
      :aria-invalid="Boolean(fieldErrors.inquiryType)"
    >
      <option value="" disabled>choose one…</option>
      <option value="Booking">Booking</option>
      <option value="Press">Press</option>
      <option value="Fan mail">Fan mail</option>
      <option value="Other">Other</option>
    </select>
    <p v-if="fieldErrors.inquiryType" class="error">{{ fieldErrors.inquiryType }}</p>

    <label for="contact-message">your message</label>
    <textarea
      id="contact-message"
      v-model="message"
      rows="4"
      placeholder="say hi to the band ♡"
      :aria-invalid="Boolean(fieldErrors.message)"
    ></textarea>
    <p v-if="fieldErrors.message" class="error">{{ fieldErrors.message }}</p>

    <div class="form-footer">
      <p v-if="opened" class="thanks" role="status">opening your email client…</p>
      <button type="submit">send</button>
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
      fieldErrors: {} as Record<string, string>,
    }
  },

  methods: {
    submit() {
      this.opened = false
      this.fieldErrors = {}

      if (!this.name.trim()) this.fieldErrors.name = 'tell us who you are ♡'
      if (!this.email.trim()) this.fieldErrors.email = 'we need an email to reply to'
      if (!this.inquiryType) this.fieldErrors.inquiryType = 'pick an inquiry type'
      if (!this.message.trim()) this.fieldErrors.message = "what's up?"
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
