import { defineStore } from "pinia"
import { ref } from "vue"

export const useSiteConfig = defineStore('siteConfig', () => {

  // ======================
  // STATE
  // ======================

  // BRANDING
  const logo = ref('/fix-kraft-logo-no-bg.svg')

  // GENERAL
  const siteName = ref('FixKraft Digital')
  const email = ref('info@fixkraftdigital.co.ke')

  // NAV LINKS
  const navLinks = ref([
    { name: 'Home', path: '/' },
    { name: 'Services', path: '/services' },
    { name: 'Projects', path: '/projects' },
    { name: 'Contact', path: '/contact' }
  ])

  // FOOTER
  const phone = ref('+254 748 929 891')
  const location = ref('Nairobi, Kenya')

  // ======================
  // LOAD (🔥 IMPORTANT)
  // ======================

  const load = () => {
    const general = localStorage.getItem('general')
    const nav = localStorage.getItem('nav')
    const footer = localStorage.getItem('footer')
    const savedLogo = localStorage.getItem('logo')

    if (general) {
      const data = JSON.parse(general)
      siteName.value = data.siteName || siteName.value
      email.value = data.email || email.value
    }

    if (nav) {
      navLinks.value = JSON.parse(nav)
    }

    if (footer) {
      const data = JSON.parse(footer)
      phone.value = data.phone || phone.value
      location.value = data.location || location.value
    }

    if (savedLogo) {
      logo.value = savedLogo
    }
  }

  // ======================
  // SAVE FUNCTIONS
  // ======================

  const saveGeneral = () => {
    localStorage.setItem(
      'general',
      JSON.stringify({
        siteName: siteName.value,
        email: email.value
      })
    )
  }

  const saveBranding = () => {
    localStorage.setItem('logo', logo.value)
  }

  const saveNav = () => {
    localStorage.setItem('nav', JSON.stringify(navLinks.value))
  }

  const saveFooter = () => {
    localStorage.setItem(
      'footer',
      JSON.stringify({
        phone: phone.value,
        location: location.value
      })
    )
  }

  // ======================
  // INIT (AUTO LOAD)
  // ======================

  load()

  // ======================
  // EXPORT
  // ======================

  return {
    // state
    logo,
    siteName,
    email,
    navLinks,
    phone,
    location,

    // actions
    load,
    saveGeneral,
    saveBranding,
    saveNav,
    saveFooter
  }
})