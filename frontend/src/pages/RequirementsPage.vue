<script setup lang="ts">
import { API_BASE_URI } from '@/config/api';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const questions = ref<any[]>([])
const answers = ref<Record<string, any>>({})
const loading = ref(false)
const error = ref('')
const success = ref(false)
const submitting = ref(false)
const route = useRoute()
const router = useRouter()
const token = route.params.token as string

const fetchQuestionnaire = async () => {
    try {
        const res = await axios.get(`${API_BASE_URI}/requirements/${token}/`)
        questions.value = res.data.questions

        // Initialize answers with empty values
        questions.value.forEach(q => {
            answers.value[q.id] = ''
        })
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Failed to load questionnaire.'
    } finally {
        loading.value = false
    }
}

const submitForm = async () => {
    // Validate required fields
    const missing = questions.value.filter(q => q.required && !answers.value[q.id])
    if (missing.length) {
        error.value = `Please answer: ${missing.map(q => q.label).join(', ')}`
        return
    }
    submitting.value = true
    error.value = ''

    try {
        await axios.post(`${API_BASE_URI}/requirements/${token}/`, {
            answers: answers.value
        })
        success.value = true
        // Optionally redirect after afew seconds
        setTimeout(() => {
            router.push('/')
        }, 3000);
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Submission failed. Please try again.'
    } finally {
        submitting.value = false
    }
}

onMounted(fetchQuestionnaire)
</script>

<template>
    <div class="max-w-3xl mx-auto px-4 py-10">
        <h1 class="text-3xl font-bold mb-2">Project Requirements</h1>
        <p class="text-gray-600 mb-6">Please help us understand your project better.</p>

        <div v-if="loading" class="text-center py-10">
            <p>Loading Questionnaire...</p>
        </div>

        <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-xl">
            {{ error }}
        </div>

        <div v-else-if="success" class="bg-green-50 text-green-700 p-4 rounded-xl">
            ✅  Thank you! Your requirements have been submitted. You'll be redirected shortly.
        </div>

        <form v-else @submit.prevent="submitForm" method="post" class="space-y-6">
            <div v-for="q in questions" :key="q.id" class="">
                <label class="block font-medium mb-1" for="">
                    {{ q.label }}
                    <span v-if="q.required" class="text-red-500">*</span>
                </label>

                <!-- Textarea -->
                 <textarea 
                    v-if="q.type === 'textarea'"
                    v-model="answers[q.id]"
                    rows="3"
                    class="w-full border rounded-xl px-4 py-3"></textarea>

                <!-- Select -->
                 <select v-else-if="q.type === 'select'" v-model="answers[q.id]" class="w-full border rounded-xl px-4 py-3">
                    <option value="">Select...</option>
                    <option v-for="opt in q.options" :key="opt" :value="opt">{{ opt }}</option>
                 </select>

                 <!-- Checkbox (multi-select) -->
                  <div v-else-if="q.type === 'checkbox'" class="space-y-2">
                    <label v-for="opt in q.options" :key="opt" class="flex items-center gap-2">
                        <input type="checkbox" :value="opt" v-model="answers[q.id]" />
                        <span>{{ opt }}</span>
                    </label>
                  </div>

                  <!-- URL -->
                   <input
                    v-else-if="q.type === 'url'" 
                    v-model="answers[q.id]" 
                    type="url" 
                    placeholder="https://example.com" 
                    class="w-full border rounded-xl px-4 py-3" 
                   />

                   <!-- Text input (fallback) -->
                    <input
                     v-else v-model="answers[q.id]" 
                     type="text" 
                     class="w-full border rounded-xl px-4 py-3" 
                    />
            </div>

            <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>

            <button
             type="submit" 
             :disabled="submitting" 
             class="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary/90 transition disabled:opacity-50"
            >
                {{ submitting ? 'Submitting...' : 'Submit Requirements' }}
            </button>
        </form>

    </div>
</template>