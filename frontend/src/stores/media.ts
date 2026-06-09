import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

import { useAuthStore } from "./auth";

const API_URL =
    'http://127.0.0.1:8000/api'

export const useMediaStore =
    defineStore(
        'media',
        () => {

            const media =
                ref<any[]>([])

            const auth =
                useAuthStore()

            const api =
                axios.create({
                    baseURL: API_URL
                })

            // TOKEN INTERCEPTOR
            api.interceptors.request.use(
                (config) => {

                    if (
                        auth.accessToken
                    ) {

                        config.headers.Authorization =
                            `Bearer ${auth.accessToken}`
                    }

                    return config
                }
            )

            // LOAD MEDIA
            const load =
                async () => {

                    const res =
                        await api.get(
                            '/mediahub/'
                        )

                    media.value =
                        res.data
                }

            // UPLOAD
            const upload = async (
                file: File,
                title: string,
                description: string,
                category: number | null
            ) => {
                const formData = new FormData()

                formData.append(
                    'file', file
                )

                formData.append(
                    'title', title
                )

                formData.append(
                    'description', description
                )

                if (category) {
                    formData.append(
                        'category', category.toString()
                    )
                }

                const res = await api.post(
                    '/mediahub/',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                )

                media.value.unshift(
                    res.data
                )
            }

            // DELETE
            const remove =
                async (
                    id: number
                ) => {

                    await api.delete(
                        `/mediahub/${id}/`
                    )

                    media.value =
                        media.value.filter(
                            m => m.id !== id
                        )
                }

            return {
                media,
                load,
                upload,
                remove
            }
        }
    )