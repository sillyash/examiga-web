<template>
  <form class="sign-form" novalidate @submit.prevent="submit">
    <h2>{{ $t('shoutoutForm.title') }}</h2>

    <label for="shoutout-name">{{ $t('shoutoutForm.nameLabel') }}</label>
    <input
      id="shoutout-name"
      v-model="name"
      type="text"
      :maxlength="nameMax"
      autocomplete="nickname"
      placeholder="Casey54"
      :aria-invalid="Boolean(fieldErrors.name)"
    />
    <p v-if="fieldErrors.name" class="error">{{ fieldErrors.name }}</p>

    <label for="shoutout-message">{{ $t('shoutoutForm.messageLabel') }}</label>
    <textarea
      id="shoutout-message"
      v-model="message"
      rows="4"
      :maxlength="messageMax"
      :placeholder="$t('shoutoutForm.messagePlaceholder')"
      :aria-invalid="Boolean(fieldErrors.message)"
    ></textarea>
    <p class="counter">{{ message.length }}/{{ messageMax }}</p>
    <p v-if="fieldErrors.message" class="error">{{ fieldErrors.message }}</p>

    <!-- Honeypot: invisible to people, bots fill it in and the API rejects them. -->
    <input
      v-model="website"
      class="honeypot"
      type="text"
      name="website"
      tabindex="-1"
      autocomplete="off"
      aria-hidden="true"
    />

    <div class="form-footer">
      <p v-if="error" class="error" role="alert">{{ $t(error) }}</p>
      <p v-else-if="thanked" class="thanks" role="status">{{ $t('shoutoutForm.thanks') }}</p>
      <button type="submit" :disabled="!canSubmit">
        {{ sending ? $t('shoutoutForm.sending') : $t('shoutoutForm.send') }}
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { ApiError, createShoutout } from '@/api'

// Same limits as ShoutoutIn in api/schemas.py.
const NAME_MAX = 80
const MESSAGE_MAX = 500

export default {
  name: 'ShoutoutForm',

  emits: ['posted'],

  data() {
    return {
      name: '',
      message: '',
      website: '',
      sending: false,
      thanked: false,
      // i18n key of the form-level error, translated in the template so it follows the language
      error: '',
      fieldErrors: {} as Record<string, string>,
      nameMax: NAME_MAX,
      messageMax: MESSAGE_MAX,
    }
  },

  computed: {
    canSubmit(): boolean {
      return !this.sending && this.name.trim() !== '' && this.message.trim() !== ''
    },
  },

  methods: {
    async submit() {
      if (!this.canSubmit) return

      this.sending = true
      this.thanked = false
      this.error = ''
      this.fieldErrors = {}
      try {
        const shoutout = await createShoutout({
          name: this.name.trim(),
          message: this.message.trim(),
          website: this.website,
        })
        this.$emit('posted', shoutout)
        // Keep the name so regulars don't have to retype it.
        this.message = ''
        this.thanked = true
      } catch (err) {
        console.error(err)
        // 422 from marshmallow: { json: { name: ["..."], message: ["..."] } }
        const fields = err instanceof ApiError && err.status === 422 && err.details?.json
        if (fields && typeof fields === 'object') {
          for (const [field, messages] of Object.entries(fields)) {
            this.fieldErrors[field] = Array.isArray(messages)
              ? messages.join(' ')
              : String(messages)
          }
        } else if (err instanceof ApiError && err.status === 429) {
          this.error = 'shoutoutForm.rateLimited'
        } else {
          this.error = 'shoutoutForm.sendError'
        }
      } finally {
        this.sending = false
      }
    },
  },
}
</script>

<style scoped>
.honeypot {
  position: absolute;
  left: -9999px;
}

.sign-form {
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
textarea:focus-visible {
  outline: 3px dashed var(--color-accent);
  outline-offset: 2px;
}

[aria-invalid='true'] {
  border-color: var(--color-accent);
}

.counter {
  margin: 0.1rem 0 0;
  text-align: right;
  font-size: 1rem;
  opacity: 0.7;
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

.form-footer .error {
  margin: 0;
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

button:hover:not(:disabled),
button:focus-visible {
  background: var(--color-text);
  color: var(--color-surface);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
