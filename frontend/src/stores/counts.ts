import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCountsStore = defineStore('counts', () => {
    const inquiriesNew = ref(0)
    const quotationsPending = ref(0)

    const fetchCounts = async () => {
        try {
            const res = await axios.get(`${API_BASE_URI}/counts/`)
            inquiriesNew.value = res.data.inquiries_new
            quotationsPending.value = res.data.quotations_pending
        } catch (error) {
            console.error('Failed to fetch counts', error)
        }
    }
    return { inquiriesNew, quotationsPending, fetchCounts }
})