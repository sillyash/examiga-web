import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Shows from '@/views/Shows.vue'
import Guestbook from '@/views/Guestbook.vue'
import Contact from '@/views/Contact.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/shows', name: 'shows', component: Shows },
    { path: '/guestbook', name: 'guestbook', component: Guestbook },
    // About was merged into Home; keep old links working.
    { path: '/about', redirect: '/' },
    { path: '/contact', name: 'contact', component: Contact },
  ],
})

export default router
