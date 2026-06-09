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
                    'http://127.0.0.1:8000/api/clients/'
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
                    `http://127.0.0.1:8000/api/clients/${id}/`
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