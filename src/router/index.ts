import AdminLayout from '@/layouts/AdminLayout.vue'
import Contact from '@/pages/Contact.vue'
import Home from '@/pages/Home.vue'
import Process from '@/pages/Process.vue'
import Projects from '@/pages/Projects.vue'
import Services from '@/pages/Services.vue'
import AdminProjects from '@/views/admin/AdminProjects.vue'
import AdminServices from '@/views/admin/AdminServices.vue'
import Dashboard from '@/views/admin/Dashboard.vue'
import Messages from '@/views/admin/Messages.vue'
import Settings from '@/views/admin/Settings.vue'
import ProjectDetail from '@/views/ProjectDetail.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/process', name: 'process', component: Process },
    { path: '/services', name: 'services', component: Services },
    { path: '/contact', name: 'contact', component: Contact },
    { path: '/projects', name: 'projects', component: Projects },
    { path: '/projects/:id', name: 'project-detail', component: ProjectDetail },
    { path: '/admin', component: AdminLayout, children: [
      { path: '', component: Dashboard },
      { path: 'projects', component: AdminProjects },
      { path: 'services', component: AdminServices },
      { path: 'messages', component: Messages },
      { path: 'settings', component: Settings }
    ]}

  ],

  // SCROLL BEHAVIOUR TO TOP
  scrollBehavior() {
    return { top: 0, behavior: 'smooth'}
  }
})

export default router
