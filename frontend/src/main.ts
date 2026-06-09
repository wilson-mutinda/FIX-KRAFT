import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'

import App from './App.vue'
import router from './router'

import AOS from 'aos'
import 'aos/dist/aos.css'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// AOS init
router.isReady().then(() => {
    AOS.init({
        duration: 800,
        once: true,
        easing: 'ease-in-out'
    })
})

// NProgress
router.beforeEach((to, from, next) => {
    NProgress.start()
    next()
})

router.afterEach(() => {
    NProgress.done()
})

const theme = useThemeStore()

// Load saved theme
const savedDark = localStorage.getItem('dark') === 'true'
const savedPrimary = localStorage.getItem('primary')

if (savedDark) {
    theme.toggleDark()
}

if (savedPrimary) {
    theme.setPrimary(savedPrimary)
}

// AUTH STORE
const auth = useAuthStore()

// HYDRATE USER SESSION
auth.fetchCurrentUser()

app.mount('#app')
