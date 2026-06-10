import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";

export const useClientStore = defineStore('clients', {
    state: () => ({
        clients: [] as any[],
        loading: false
    }),

    actions: {
        async load() {
            this.loading = true

            try {
                const response = await axios.get(
                    '${API_BASE_URI}/clients/'
                )

                this.clients = response.data

            } catch (error) {
                console.error(error)
            } finally {
                this.loading = false
            }
        },

        async remove(id: number) {
            try {
                await axios.delete(
                    `${API_BASE_URI}/clients/${id}/`
                )

                this.clients = this.clients.filter(
                    item => item.id !== id
                )
            } catch (error) {
                console.error(error)
            }
        }
    }
})