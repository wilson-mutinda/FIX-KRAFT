import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

import { useAuthStore } from './auth'
import { API_BASE_URI } from '@/config/api'

const API_URL = '${API_BASE_URI}'

export const useProjectsStore = defineStore('projects', () => {

    const projects = ref<any[]>([])

    const loading = ref(false)

    const auth = useAuthStore()

    // AXIOS INSTANCE
    const api = axios.create({
        baseURL: API_BASE_URI
    })

    // TOKEN INTERCEPTOR
    api.interceptors.request.use((config) => {

        if (auth.accessToken) {

            config.headers.Authorization =
                `Bearer ${auth.accessToken}`
        }

        return config
    })

    // LOAD PROJECTS
    const load = async () => {

        loading.value = true

        try {

            const res = await api.get('/projects/')

            projects.value = res.data

        } catch (err) {

            console.error(
                'Failed to load projects',
                err
            )

        } finally {

            loading.value = false
        }
    }

    // CREATE PROJECT
    const addProject = async (project: any) => {

        const formData = new FormData()

        formData.append(
            'title',
            project.title
        )

        formData.append(
            'technologies',
            project.technologies
        )

        formData.append(
            'image',
            project.image
        )

        const res = await api.post(
            '/projects/',
            formData,
            {
                headers: {
                    'Content-Type':
                        'multipart/form-data'
                }
            }
        )

        projects.value.unshift(res.data)

        return res.data
    }

    // UPDATE PROJECT
    const updateProject = async (
        id: number,
        project: any
    ) => {

        const formData = new FormData()

        formData.append(
            'title',
            project.title
        )

        formData.append(
            'technologies',
            project.technologies
        )

        // ONLY APPEND IMAGE IF FILE
        if (
            project.image &&
            typeof project.image !== 'string'
        ) {

            formData.append(
                'image',
                project.image
            )
        }

        const res = await api.patch(
            `/projects/${id}/`,
            formData,
            {
                headers: {
                    'Content-Type':
                        'multipart/form-data'
                }
            }
        )

        const index =
            projects.value.findIndex(
                p => p.id === id
            )

        if (index !== -1) {

            projects.value[index] =
                res.data
        }

        return res.data
    }

    // DELETE PROJECT
    // const deleteProject = async (
    //     id: number
    // ) => {

    //     await api.delete(
    //         `/projects/${id}/`
    //     )

    //     projects.value =
    //         projects.value.filter(
    //             p => p.id !== id
    //         )
    // }

    const deleteProject = async (
        id: number
    ) => {

        console.log(auth.accessToken)

        await api.delete(
            `/projects/${id}/`
        )

        projects.value =
            projects.value.filter(
                p => p.id !== id
            )
    }

    const getById = (id: number) => {
            return projects.value.find(p => p.id === id)
        }

    return {
        projects,
        loading,
        load,
        addProject,
        updateProject,
        deleteProject,
        getById
    }
})