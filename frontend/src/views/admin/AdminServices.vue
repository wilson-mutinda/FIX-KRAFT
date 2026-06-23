<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/admin/PageHeader.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseTextArea from '@/components/ui/BaseTextArea.vue'
import DeleteModal from '@/components/admin/DeleteModal.vue'
import { useServicesStore } from '@/stores/services'

const store = useServicesStore()
const loading = ref(false)
const editingService = ref<any>(null)
const showDeleteModal = ref(false)
const deleteId = ref<number | null>(null)

interface ServiceForm {
    id: number | null
    title: string
    description: string
    features: string
    display_order: number
    is_active: boolean
    image: File | null
}

const form = ref<ServiceForm>({
    id: null,
    title: '',
    description: '',
    features: '',
    display_order: 0,
    is_active: true,
    image: null,
})

const previewImage = ref('')

const resetForm = () => {
    form.value = {
        id: null,
        title: '',
        description: '',
        features: '',
        display_order: 0,
        is_active: true,
        image: null,
    }
    previewImage.value = ''
    editingService.value = null
}

const saveService = async () => {
    loading.value = true
    const formData = new FormData()
    ;(Object.keys(form.value) as Array<keyof ServiceForm>).forEach(key => {
        if (key === 'id' || key === 'image') return
        const val = form.value[key]
        if (val !== null && val !== undefined) {
            formData.append(key, String(val))
        }
    })
    if (form.value.image) {
        formData.append('image', form.value.image)
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

const editService = (item: any) => {
    form.value = {
        id: item.id,
        title: item.title,
        description: item.description || '',
        features: item.features || '',
        display_order: item.display_order || 0,
        is_active: item.is_active,
        image: null,
    }
    previewImage.value = item.image || ''
    editingService.value = item
}

const confirmDelete = (id: number) => {
    deleteId.value = id
    showDeleteModal.value = true
}

const deleteService = async () => {
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
        form.value.image = file
        previewImage.value = URL.createObjectURL(file)
    }
}

onMounted(() => {
    store.load()
})
</script>

<template>
    <div class="space-y-6">
        <PageHeader title="Services" subtitle="Manage services displayed on the homepage" />

        <!-- Form -->
        <div class="bg-white rounded-3xl border p-6 space-y-4">
            <BaseInput v-model="form.title" placeholder="Service title" />
            <BaseTextArea v-model="form.description" placeholder="Short description" rows="3" />
            <BaseTextArea v-model="form.features" placeholder="Features (comma separated, e.g., Responsive, SEO optimized)" rows="2" />
            <div class="flex gap-4 flex-wrap items-center">
                <input type="number" v-model.number="form.display_order" class="border rounded-xl px-4 py-2 w-24" placeholder="Order" />
                <label class="flex items-center gap-2">
                    <input type="checkbox" v-model="form.is_active" />
                    Active
                </label>
            </div>
            <div>
                <label class="block text-sm font-medium mb-1">Image</label>
                <input type="file" accept="image/*" @change="handleImageUpload" />
                <img v-if="previewImage" :src="previewImage" class="mt-2 h-32 w-auto object-cover rounded border" />
            </div>
            <div class="flex gap-3">
                <BaseButton @click="saveService" :disabled="loading">{{ form.id ? 'Update' : 'Create' }} Service</BaseButton>
                <BaseButton variant="secondary" @click="resetForm">Cancel</BaseButton>
            </div>
        </div>

        <!-- List -->
        <div class="bg-white rounded-3xl border overflow-hidden">
            <table class="w-full">
                <thead class="bg-gray-50 border-b">
                    <tr>
                        <th class="px-6 py-3 text-left">Title</th>
                        <th class="px-6 py-3 text-left">Description</th>
                        <th class="px-6 py-3 text-left">Active</th>
                        <th class="px-6 py-3 text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in store.services" :key="item.id" class="border-b">
                        <td class="px-6 py-4 flex items-center gap-2">
                            <img v-if="item.image" :src="item.image" class="h-10 w-10 object-cover rounded" />
                            <span>{{ item.title }}</span>
                        </td>
                        <td class="px-6 py-4 max-w-xs truncate">{{ item.description }}</td>
                        <td class="px-6 py-4">{{ item.is_active ? '✅' : '❌' }}</td>
                        <td class="px-6 py-4">
                            <button @click="editService(item)" class="text-blue-600 mr-3">Edit</button>
                            <button @click="confirmDelete(item.id)" class="text-red-600">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <DeleteModal :show="showDeleteModal" title="Delete Service?" message="This action cannot be undone." @close="showDeleteModal=false" @confirm="deleteService" />
    </div>
</template>
