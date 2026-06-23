import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export interface Service {
    id: number;
    title: string;
    description: string;
    image: string | null;
    features: string;
    display_order: number;
    is_active: boolean;
}

export const useServicesStore = defineStore('services', () => {
    const services = ref<Service[]>([])
    const loading = ref(false)

    // Axios instance with auth interceptor (for admin operations)
    const api = axios.create({
        baseURL: API_BASE_URI
    })

    api.interceptors.request.use((config) => {
        const auth = useAuthStore()
        if (auth.accessToken) {
            config.headers.Authorization = `Bearer ${auth.accessToken}`
        }
        return config
    })

    const load = async () => {
        loading.value = true
        try {
            const res = await api.get('/services/')
            services.value = res.data
        } catch (err) {
            console.error('Failed to load services', err)
        } finally {
            loading.value = false
        }
    }

    const create = async (data: any) => {
        const res = await api.post('/services/', data)
        services.value.unshift(res.data)
        return res.data
    }

    const update = async (id: number, data: any) => {
        const res = await api.patch(`/services/${id}/`, data)
        const index = services.value.findIndex(s => s.id === id)
        if (index !== -1) services.value[index] = res.data
        return res.data
    }

    const remove = async (id: number) => {
        await api.delete(`/services/${id}/`)
        services.value = services.value.filter(s => s.id !== id)
    }

    return {
        services,
        loading,
        load,
        create,
        update,
        remove
    }
})
