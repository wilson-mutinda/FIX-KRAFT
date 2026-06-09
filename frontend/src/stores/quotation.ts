import axios from "axios";
import { defineStore } from "pinia";

export interface Quotation {
    id: number;
    quotation_number: string;
    amount: string;
    description: string;
    valid_until: string;
    status: 'pending' | 'approved' | 'rejected';
    inquiry: number;
    inquiry_details: {
        id: number;
        service?: string;
        client_details?: {
            name: string;
            email: string;
        };
    };
    created_at: string;
}

export const useQuotationStore = defineStore('quotations',  {
    state: () => ({
        quotations: [] as Quotation[],
        loading: false,
    }),

    actions: {
        async load() {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/quotation/');
                this.quotations = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        async remove(id: number) {
            try {
                await axios.delete(`http://127.0.0.1:8000/api/quotation/${id}/`);
                this.quotations = this.quotations.filter(q => q.id !== id);
            } catch (error) {
                console.error(error);
            }
        },

        async update(id: number, data: Partial<Quotation>) {
            try {
                const response = await axios.patch(`http://127.0.0.1:8000/${id}/`, data);
                const index = this.quotations.findIndex(q => q.id === id);

                if (index !== -1) {
                    this.quotations[index] = { ...this.quotations[index], ...response.data };
                }
                return response.data;
            } catch (error) {
                console.error(error);
                throw error;
            }
        },
    },
});
