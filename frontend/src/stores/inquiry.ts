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
                    'http://127.0.0.1:8000/api/inquiries/'
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
                    `http://127.0.0.1:8000/api/inquiries/${id}/`
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
                    `http://127.0.0.1:8000/api/inquiries/${id}/`,
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
