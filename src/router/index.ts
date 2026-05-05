import Contact from '@/pages/Contact.vue'
import Home from '@/pages/Home.vue'
import Process from '@/pages/Process.vue'
import Projects from '@/pages/Projects.vue'
import Services from '@/pages/Services.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/process', name: 'process', component: Process },
    { path: '/services', name: 'services', component: Services },
    { path: '/contact', name: 'contact', component: Contact },
    { path: '/projects', name: 'projects', component: Projects },

  ],
})

export default router
