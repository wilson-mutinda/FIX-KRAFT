import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'

import App from './App.vue'
import router from './router'

import AOS from 'aos'
import 'aos/dist/aos.css'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

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

app.mount('#app')
