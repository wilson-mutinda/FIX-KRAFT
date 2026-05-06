import { defineStore } from "pinia";

export const useThemeStore = defineStore('theme', {
    state: () => ({
        dark: false,
        primary: '#2563eb'
    }),

    actions: {
        toggleDark() {
            this.dark = !this.dark

            document.documentElement.classList.toggle('dark', this.dark)
        },

        setPrimary(color: string) {
            this.primary = color

            document.documentElement.style.setProperty('--color-primary', color)
        }
    }
})