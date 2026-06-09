<template>
    <div class="max-w-7xl mx-auto px-6 py-10">
        <h1 class="text-3xl font-bold mb-8">My Dashboard</h1>
        <div v-if="loading" class="">Loading...</div>
            <div v-else class="">
                <section class="mb-10">
                    <h2 class="text-xl font-semibold mb-4">My Inquiries</h2>
                    <div v-if="inquiries.length === 0" class="text-gray-500">No inquiries yet.</div>
                    <div v-for="inq in inquiries" :key="inq.id" class="border p-4 rounded-lg mb-3">
                        <p><strong>Service: </strong>{{ inq.service }}</p>
                        <p><strong>Status: </strong>{{ inq.status }}</p>
                        <p><strong>Message: </strong>{{ inq.message }}</p>
                    </div>
                </section>

                <section>
                    <h2 class="text-xl font-semibold mb-4">My Quotations</h2>
                    <div v-if="quotations.length === 0" class="text-gray-500">No quotations yet.</div>
                    <div v-for="q in quotations" :key="q.id" class="border p-4 rounded-lg mb-3">
                        <p><strong>Quotation #:</strong>{{ q.quotation_number }}</p>
                        <p><strong>Amount:</strong>KSh {{ parseFloat(q.amount).toLocaleString() }}</p>
                        <p><strong>Status:</strong>{{ q.status }}</p>
                        <a :href="`/api/quotation/${q.id}/download-pdf/`" class="text-blue-600 text-sm">Download PDF</a>
                    </div>
                </section>
            </div>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';


// const inquiries = ref([])
interface Inquiry {
    id: number;
    service: string;
    status: string;
    message: string;
    created_at: string;
}

// const quotations = ref([])
interface Quotation {
    id: number;
    quotation_number: string;
    amount: string;
    status: string;
}

const inquiries = ref<Inquiry[]>([])
const quotations = ref<Quotation[]>([])
const loading = ref(true)

onMounted(async () => {
    try {
        const [inqRes, quotRes] = await Promise.all([
            axios.get('/api/inquiries/my_inquiries/'),
            axios.get('/api/quotation/my_quotations/')
        ])
        inquiries.value = inqRes.data
        quotations.value = quotRes.data
    } catch (error) {
        console.error('Failed to load client data', error)
    } finally {
        loading.value = false
    }
})
</script>
