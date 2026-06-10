import { API_BASE_URI } from "@/config/api"
import axios from "axios"
import { defineStore } from "pinia"
import { ref } from "vue"

// const API_URL = 'http://127.0.0.1:8000/api'

export const useCategoryStore = 
    defineStore(
        'categories',
        () => {

            const categories = ref<any[]>([])

            const api = axios.create({
                baseURL: API_BASE_URI
            })

            // LOAD
            const load = async () => {
                const res = await api.get(
                    '/media-categories/'
                )

                categories.value = res.data
            }

            return {
                categories,
                load
            }
        }
    )