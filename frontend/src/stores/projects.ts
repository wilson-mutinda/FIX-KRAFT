import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export interface Project {
    id: number;
    title: string;
    description: string;
    image: string | null;
    technologies: string;
    project_url?: string;
    github_url?: string;
    featured: boolean;
    slug?: string;
    status: string;
    overview?: string;
    problem?: string;
    solution?: string;
    results?: string;
    features?: string;
    tech_stack?: string;
    gallery?: string;
    hero_image?: string | null;
    created_at: string;
}

export const useProjectsStore = defineStore('projects', () => {
    const projects = ref<Project[]>([])
    const loading = ref(false)

    // Public API (no auth)
    const publicApi = axios.create({
        baseURL: API_BASE_URI
    })

    // Admin API (with auth)
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
            const res = await publicApi.get('/projects/')
            projects.value = res.data
        } catch (err) {
            console.error('Failed to load projects', err)
        } finally {
            loading.value = false
        }
    }

    const create = async (data: any) => {
        const res = await api.post('/projects/', data)
        projects.value.unshift(res.data)
        return res.data
    }

    const update = async (id: number, data: any) => {
        const res = await api.patch(`/projects/${id}/`, data)
        const index = projects.value.findIndex(p => p.id === id)
        if (index !== -1) projects.value[index] = res.data
        return res.data
    }

    const remove = async (id: number) => {
        await api.delete(`/projects/${id}/`)
        projects.value = projects.value.filter(p => p.id !== id)
    }

    return {
        projects,
        loading,
        load,
        create,
        update,
        remove
    }
})