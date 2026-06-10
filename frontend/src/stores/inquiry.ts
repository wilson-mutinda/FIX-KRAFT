import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";

export const useInquiryStore = defineStore('inquiries', {

    state: () => ({
        inquiries: [] as any[],
        loading: false
    }),

    actions: {

        // LOAD
        async load() {
            this.loading = true

            try {
                const response = await axios.get(
                    `${API_BASE_URI}/inquiries/`
                )

                this.inquiries = response.data
            } catch (error) {
                console.error(error)
            } finally {
                this.loading = false
            }
        },

        // DELETE
        async remove(id: number) {
            try {
                await axios.delete(
                    `${API_BASE_URI}/inquiries/${id}/`
                )
                this.inquiries = this.inquiries.filter(
                    item => item.id !== id
                )
            } catch (error) {
                console.error(error)
            }
        },

        // UPDATE STATUS
        async updateStatus(id: number, status: string) {
            try {
                await axios.patch(
                    `${API_BASE_URI}/inquiries/${id}/`,
                    {
                        status
                    }
                )

                // update locally
                const inquiry = this.inquiries.find(
                    item => item.id === id
                )

                if (inquiry) {
                    inquiry.status = status
                }
            } catch (error) {
                console.error(error)
            }
        }
    }
})
