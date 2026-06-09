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
                const response = await axios.get('http://127.0.0.1:8000/api/payment/');
                this.payments = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        async remove(id: number) {
            try {
                await axios.delete(`http://127.0.0.1:8000/api/payment/${id}/`);
                this.payments = this.payments.filter(p => p.id !== id);
            } catch (error) {
                console.error(error);
            }
        },
    },
});
