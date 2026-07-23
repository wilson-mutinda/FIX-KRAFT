import MediaManager from '@/components/media/MediaManager.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'
import BlogDetail from '@/pages/BlogDetail.vue'
import BlogPage from '@/pages/BlogPage.vue'
import Contact from '@/pages/Contact.vue'
import Home from '@/pages/Home.vue'
import Process from '@/pages/Process.vue'
import Projects from '@/pages/Projects.vue'
import RequirementsPage from '@/pages/RequirementsPage.vue'
import Services from '@/pages/Services.vue'
import { useAuthStore } from '@/stores/auth'
import AdminBlog from '@/views/admin/AdminBlog.vue'
import AdminClients from '@/views/admin/AdminClients.vue'
import AdminInquiries from '@/views/admin/AdminInquiries.vue'
import AdminPayments from '@/views/admin/AdminPayments.vue'
import AdminProjects from '@/views/admin/AdminProjects.vue'
import AdminQuotations from '@/views/admin/AdminQuotations.vue'
import AdminServices from '@/views/admin/AdminServices.vue'
import AdminTestimonials from '@/views/admin/AdminTestimonials.vue'
import Dashboard from '@/views/admin/Dashboard.vue'
import Messages from '@/views/admin/Messages.vue'
import Settings from '@/views/admin/Settings.vue'
import ProjectDetail from '@/views/ProjectDetail.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/blog', name: 'blog', component: BlogPage },
    { path: '/blog/:slug', name: 'blog-detail', component: BlogDetail },
    { path: '/process', name: 'process', component: Process },
    { path: '/services', name: 'services', component: Services },
    { path: '/contact', name: 'contact', component: Contact },
    { path: '/projects', name: 'projects', component: Projects },
    { path: '/projects/:id', name: 'project-detail', component: ProjectDetail },
    { path: '/requirements/:token', name: 'requirements', component: RequirementsPage, meta: { requiresAuth: false } },
    { path: '/admin', component: AdminLayout, meta: { requiresAuth: true }, children: [
      { path: '', component: Dashboard },
      { path: 'projects', component: AdminProjects },
      { path: 'services', component: AdminServices },
      { path: 'messages', component: Messages },
      { path: 'settings', component: Settings },
      { path: 'media', component: MediaManager },
      { path: 'inquiries', component: AdminInquiries },
      { path: 'clients', component: AdminClients },
      { path: 'payments', component: AdminPayments },
      { path: 'quotations', component: AdminQuotations },
      { path: 'blog', component: AdminBlog },
      { path: 'testimonials', component: AdminTestimonials },
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
