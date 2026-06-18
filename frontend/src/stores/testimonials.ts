import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export interface Testimonial {
    id: number;
    client_name: string;
    logo: string | null;
    website_url: string | null;
    testimonial_text: string;
    client_role: string;
    display_order: number;
    is_active: boolean;
}

export const useTestimonialStore = defineStore('testimonials', () => {
    const testimonials = ref<Testimonial[]>([])
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
            const res = await api.get('/testimonials/')
            testimonials.value = res.data
        } catch (err) {
            console.error('Failed to load testimonials', err)
        } finally {
            loading.value = false
        }
    }

    const create = async (data: any) => {
        const res = await api.post('/testimonials/', data)
        testimonials.value.unshift(res.data)
        return res.data
    }

    const update = async (id: number, data: any) => {
        const res = await api.patch(`/testimonials/${id}/`, data)
        const index = testimonials.value.findIndex(t => t.id === id)
        if (index !== -1) testimonials.value[index] = res.data
        return res.data
    }

    const remove = async (id: number) => {
        await api.delete(`/testimonials/${id}`)
        testimonials.value = testimonials.value.filter(t => t.id !== id)
    }

    return {
        testimonials, loading, load, create, update, remove
    }
})