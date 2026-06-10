import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useAuthStore = defineStore('auth', () => {


    // STATE
    const accessToken = ref(localStorage.getItem('access_token') || '')
    const refreshToken = ref(localStorage.getItem('refresh_token') || '')
    const user = ref<any>(null)

    // BASE API URL
    // const API_URL = 'http://127.0.0.1:8000/api'

    // COMPUTED
    const isAuthenticated = computed(() => !!accessToken.value)

    // LOGIN
    const login = async (username: string, password: string) => {
        try {
            
            const response = await axios.post(`${API_BASE_URI}/token/`, {
                username,
                password
            })

            accessToken.value = response.data.access
            refreshToken.value = response.data.refresh

            localStorage.setItem('access_token', accessToken.value)
            localStorage.setItem('refresh_token', refreshToken.value)

            await fetchCurrentUser()

            return {
                success: true
            }
        } catch (error: any) {
            return { 
                success: false,
                message: error.response?.data || 'Login failed'
            }
        }
    }

    // REGISTER
    const register = async (data: any) => {
        try {
            await axios.post(`${API_BASE_URI}/register/`, data)

            return {
                success: true
            }
        } catch (error: any) {
            return {
                success: false,
                message: error.response?.data || 'Registration failed'
            }
        }
    }

    // FETCH CURRENT USER
    const fetchCurrentUser = async () => {

        if (!accessToken.value) return

        try {
            
            const response = await axios.get(`${API_BASE_URI}/me/`, {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })

            user.value = response.data
        } catch (error) {
            logout()
        }
    }

    // LOGOUT
    const logout = () => {

        accessToken.value = ''
        refreshToken.value = ''
        user.value = null

        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    }

    return {
        accessToken,
        refreshToken,
        user,

        isAuthenticated,

        login,
        register,
        logout,
        fetchCurrentUser
    }
})