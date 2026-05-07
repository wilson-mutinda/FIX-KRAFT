import { defineStore } from "pinia";
import { ref } from "vue";

export const useServicesStore = defineStore('services', () => {
    
    const services = ref<any[]>([])

    const load = () => {
        const saved = localStorage.getItem('services')
        if (saved) services.value = JSON.parse(saved)
    }

    const save = () => {
        localStorage.setItem('services', JSON.stringify(services.value))
    }

    const update = (service: any) => {
        const index = services.value.findIndex(s => s.id === service.id)

        if (index !== -1) {
            services.value[index] = service
            save()
        }
    }

    return {
        services,
        load,
        update
    }
})