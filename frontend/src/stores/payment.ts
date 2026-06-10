import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";

export interface Payment {
    id: number;
    project: number,
    project_details: {
        id: number;
        title: number;
    };
    amount: string;
    payment_method: string;
    transaction_id: string;
    created_at: string;
}

export const usePaymentStore = defineStore('payments', {
    state: () => ({
        payments: [] as Payment[],
        loading: false,
    }),

    actions: {
        async load() {
            this.loading = true;
            try {
                const response = await axios.get(`${API_BASE_URI}/payment/`);
                this.payments = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        async remove(id: number) {
            try {
                await axios.delete(`${API_BASE_URI}/payment/${id}/`);
                this.payments = this.payments.filter(p => p.id !== id);
            } catch (error) {
                console.error(error);
            }
        },
    },
});
