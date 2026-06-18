<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseTextArea from '@/components/ui/BaseTextArea.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import { useTestimonialStore } from '@/stores/testimonials'

const store = useTestimonialStore()
const loading = ref(false)
const editingTestimonial = ref<any>(null)
const showDeleteModal = ref(false)
const deleteId = ref<number | null>(null)

interface TestimonialForm {
    id: number | null
    client_name: string
    client_role: string
    testimonial_text: string
    website_url: string
    display_order: number
    is_active: boolean
    logo: File | null
}

const form = ref<TestimonialForm>({
    id: null,
    client_name: '',
    client_role: '',
    testimonial_text: '',
    website_url: '',
    display_order: 0,
    is_active: true,
    logo: null,
})

const previewImage = ref('')

const resetForm = () => {
    form.value = {
        id: null,
        client_name: '',
        client_role: '',
        testimonial_text: '',
        website_url: '',
        display_order: 0,
        is_active: true,
        logo: null,
    }
    previewImage.value = ''
    editingTestimonial.value = null
}

const saveTestimonial = async () => {
    loading.value = true
    const formData = new FormData()
    ;(Object.keys(form.value) as Array<keyof TestimonialForm>).forEach(key => {
        if (key === 'id' || key === 'logo') return
        const val = form.value[key]
        if (val !== null && val !== undefined) {
            formData.append(key, String(val))
        }
    })
    if (form.value.logo) {
        formData.append('logo', form.value.logo)
    }
    if (form.value.id) {
        await store.update(form.value.id, formData)
    } else {
        await store.create(formData)
    }
    resetForm()
    await store.load()
    loading.value = false
}

const editTestimonial = (item: any) => {
    form.value = {
        id: item.id,
        client_name: item.client_name,
        client_role: item.client_role || '',
        testimonial_text: item.testimonial_text,
        website_url: item.website_url || '',
        display_order: item.display_order || 0,
        is_active: item.is_active,
        logo: null,
    }
    previewImage.value = item.logo || ''
    editingTestimonial.value = item
}

const confirmDelete = (id: number) => {
    deleteId.value = id
    showDeleteModal.value = true
}

const deleteTestimonial = async () => {
    if (deleteId.value) {
        await store.remove(deleteId.value)
        await store.load()
    }
    showDeleteModal.value = false
}

const handleImageUpload = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    if (file) {
        form.value.logo = file
        previewImage.value = URL.createObjectURL(file)
    }
}

onMounted(() => {
    store.load()
})
</script>

<template>
    <div class="space-y-6">
        <PageHeader title="Testimonials" subtitle="Manage client testimonials that appear on the homepage" />

        <!-- Form -->
        <div class="bg-white rounded-3xl border p-6 space-y-4">
            <div class="grid md:grid-cols-2 gap-4">
                <BaseInput v-model="form.client_name" placeholder="Client / Company name" />
                <BaseInput v-model="form.client_role" placeholder="Role / Title (e.g., Managing Partner)" />
            </div>
            <BaseInput v-model="form.website_url" placeholder="Website URL (e.g., https://abdirodgers.co.ke)" />
            <BaseTextArea v-model="form.testimonial_text" placeholder="Their testimonial text..." rows="4" />
            <div class="flex gap-4 flex-wrap items-center">
                <input type="number" v-model.number="form.display_order" class="border rounded-xl px-4 py-2 w-24" placeholder="Order" />
                <label class="flex items-center gap-2">
                    <input type="checkbox" v-model="form.is_active" />
                    Active
                </label>
            </div>
            <div>
                <label class="block text-sm font-medium mb-1">Logo / Image</label>
                <input type="file" accept="image/*" @change="handleImageUpload" />
                <img v-if="previewImage" :src="previewImage" class="mt-2 h-16 w-16 object-cover rounded-full border" />
            </div>
            <div class="flex gap-3">
                <BaseButton @click="saveTestimonial" :disabled="loading">{{ form.id ? 'Update' : 'Create' }} Testimonial</BaseButton>
                <BaseButton variant="secondary" @click="resetForm">Cancel</BaseButton>
            </div>
        </div>

        <!-- List -->
        <div class="bg-white rounded-3xl border overflow-hidden">
            <table class="w-full">
                <thead class="bg-gray-50 border-b">
                    <tr>
                        <th class="px-6 py-3 text-left">Client</th>
                        <th class="px-6 py-3 text-left">Role</th>
                        <th class="px-6 py-3 text-left">Text</th>
                        <th class="px-6 py-3 text-left">Active</th>
                        <th class="px-6 py-3 text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in store.testimonials" :key="item.id" class="border-b">
                        <td class="px-6 py-4 flex items-center gap-2">
                            <img v-if="item.logo" :src="item.logo" class="h-8 w-8 object-cover rounded-full" />
                            <span>{{ item.client_name }}</span>
                        </td>
                        <td class="px-6 py-4">{{ item.client_role }}</td>
                        <td class="px-6 py-4 max-w-xs truncate">{{ item.testimonial_text }}</td>
                        <td class="px-6 py-4">{{ item.is_active ? '✅' : '❌' }}</td>
                        <td class="px-6 py-4">
                            <button @click="editTestimonial(item)" class="text-blue-600 mr-3">Edit</button>
                            <button @click="confirmDelete(item.id)" class="text-red-600">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <DeleteModal :show="showDeleteModal" title="Delete Testimonial?" message="This action cannot be undone." @close="showDeleteModal=false" @confirm="deleteTestimonial" />
    </div>
</template>