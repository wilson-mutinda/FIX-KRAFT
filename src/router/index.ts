import MediaManager from '@/components/media/MediaManager.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'
import Contact from '@/pages/Contact.vue'
import Home from '@/pages/Home.vue'
import Process from '@/pages/Process.vue'
import Projects from '@/pages/Projects.vue'
import Services from '@/pages/Services.vue'
import { useAuthStore } from '@/stores/auth'
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
    { path: '/admin', component: AdminLayout, meta: { requiresAuth: true }, children: [
      { path: '', component: Dashboard },
      { path: 'projects', component: AdminProjects },
      { path: 'services', component: AdminServices },
      { path: 'messages', component: Messages },
      { path: 'settings', component: Settings },
      { path: 'media', component: MediaManager }
    ]},
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register }

  ],

  // SCROLL BEHAVIOUR TO TOP
  scrollBehavior() {
    return { top: 0, behavior: 'smooth'}
  }
})

router.beforeEach((to, from, next) => {

  const auth = useAuthStore()

  // CHECK IF ROUTE NEEDS AUTH
  const requiresAuth = to.matched.some(
    record => record.meta.requiresAuth
  )

  // IF NOT LOGGED IN
  if (requiresAuth && !auth.isAuthenticated) {
    next('/login')

  }

  // IF ALREADY LOGGED IN
  else if (
    (to.path === '/login' || to.path === '/register') && auth.isAuthenticated
  ) {
    next('/admin')

  }
  else {
    next()
  }
})

export default router
