import { API_BASE_URI } from "@/config/api";
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
                const response = await axios.get(`${API_BASE_URI}/quotation/`);
                this.quotations = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        async remove(id: number) {
            try {
                await axios.delete(`${API_BASE_URI}/quotation/${id}/`);
                this.quotations = this.quotations.filter(q => q.id !== id);
            } catch (error) {
                console.error(error);
            }
        },

        async update(id: number, data: Partial<Quotation>) {
            try {
                const response = await axios.patch(`${API_BASE_URI}/quotation/${id}/`, data);
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
