import { createApp, watch } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import '@/assets/main.css'
import App from '@/App.vue'
import router from '@/router'
import en from '@/locales/en.json'
import fr from '@/locales/fr.json'

type Locale = 'fr' | 'en'

const LOCALE_STORAGE_KEY = 'examiga-locale'

// Saved choice first, then the browser language; the band is French, so French is the default.
function getInitialLocale(): Locale {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY)
  if (stored === 'fr' || stored === 'en') return stored
  return navigator.language.startsWith('en') ? 'en' : 'fr'
}

const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: 'en',
  messages: { fr, en },
})

watch(
  () => i18n.global.locale.value,
  (value) => {
    document.documentElement.lang = value
    localStorage.setItem(LOCALE_STORAGE_KEY, value)
  },
  { immediate: true },
)

const app = createApp(App)

app.use(i18n)
app.use(createPinia())
app.use(router)

app.mount('#app')
