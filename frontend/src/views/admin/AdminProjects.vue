<script setup lang="ts">
import DeleteModal from '@/components/admin/DeleteModal.vue';
import PageHeader from '@/components/admin/PageHeader.vue';
import BaseButton from '@/components/ui/BaseButton.vue';
import BaseInput from '@/components/ui/BaseInput.vue';
import BaseTextArea from '@/components/ui/BaseTextArea.vue';
import { useProjectsStore } from '@/stores/projects';
import { onMounted, ref } from 'vue';

const store = useProjectsStore()
const loading = ref(false)
const editingProject = ref<any>(null)
const showDeleteModal = ref(false)
const deleteId = ref<number | null>(null)

interface ProjectForm {
  id: number | null
  title: string
  description: string
  technologies: string
  project_url: string
  github_url: string
  featured: boolean
  image: File | null
  status: string
  overview: string
  problem: string
  solution: string
  results: string
  features: string
  tech_stack: string
  gallery: string
  hero_image: File | null
}

const form = ref<ProjectForm>({
  id: null,
  title: '',
  description: '',
  technologies: '',
  project_url: '',
  github_url: '',
  featured: false,
  image: null,
  status: 'planning',
  overview: '',
  problem: '',
  solution: '',
  results: '',
  features: '',
  tech_stack: '',
  gallery: '',
  hero_image: null,
})

const previewImage = ref('')
const previewHeroImage = ref('')

const resetForm = () => {
  form.value = {
    id: null,
    title: '',
    description: '',
    technologies: '',
    project_url: '',
    github_url: '',
    featured: false,
    image: null,
    status: 'planning',
    overview: '',
    problem: '',
    solution: '',
    results: '',
    features: '',
    tech_stack: '',
    gallery: '',
    hero_image: null,
  }
  previewImage.value = ''
  previewHeroImage.value = ''
  editingProject.value = null
}

const saveProject = async () => {
  loading.value = true
  const formData = new FormData()
  ;(Object.keys(form.value) as Array<keyof ProjectForm>).forEach(key => {
    if (key === 'id' || key === 'image' || key === 'hero_image') return
    const val = form.value[key]
    if (val !== null && val !== undefined) {
      formData.append(key, String(val))
    }
  })
  if (form.value.image) {
    formData.append('image', form.value.image)
  }
  if (form.value.hero_image) {
    formData.append('hero_image', form.value.hero_image)
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

const editProject = (item: any) => {
  form.value = {
    id: item.id,
    title: item.title,
    description: item.description || '',
    technologies: item.technologies || '',
    project_url: item.project_url || '',
    github_url: item.github_url || '',
    featured: item.featured || false,
    image: null,
    status: item.status || 'planning',
    overview: item.overview || '',
    problem: item.problem || '',
    solution: item.solution || '',
    results: item.results || '',
    features: item.features || '',
    tech_stack: item.tech_stack || '',
    gallery: item.gallery || '',
    hero_image: null,
  }
  previewImage.value = item.image || ''
  previewHeroImage.value = item.hero_image || ''
  editingProject.value = item
}

const confirmDelete = (id: number) => {
  deleteId.value = id
  showDeleteModal.value = true
}

const deleteProject = async () => {
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

// handleHeroImageUpload
const handleHeroImageUpload = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]

  if (file) {
    form.value.hero_image = file
    previewHeroImage.value = URL.createObjectURL(file)
  }
}

onMounted(() => {
  store.load()
})

</script>

<template>
  <div class="space-y-2">
    <PageHeader title="Projects" subtitle="Manage portfolio projects" />

    <!-- Form -->
     <div class="bg-white rounded-3xl border p-6 space-y-4">
      <BaseInput v-model="form.title" placeholder="Project title" />
      <BaseTextArea v-model="form.description" placeholder="Short description" rows="3" />
      <BaseInput v-model="form.technologies" placeholder="Technologies (comma separated, e.g., Django, Vue)" />
      <BaseInput v-model="form.project_url" placeholder="Lice demo URL (optional)" />
      <BaseInput v-model="form.github_url" placeholder="Github URL (optional)" />

      <div class="flex gap-4 flex-wrap items-center">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="form.featured" />
          Featured
        </label>
      </div>

      <div class="">
        <label class="block text-sm font-medium mb-1">Image</label>
        <input type="file" accept="image/*" @change="handleImageUpload" />
        <img v-if="previewImage" :src="previewImage" class="mt-2 h-32 w-auto object-cover rounded border" />
      </div>

      <!-- Case Study Fields -->
       <BaseTextArea v-model="form.overview" placeholder="Overview" rows="2" />
       <BaseTextArea v-model="form.problem" placeholder="Problem" rows="2" />
       <BaseTextArea v-model="form.solution" placeholder="Solution" rows="2" />
       <BaseTextArea v-model="form.results" placeholder="Results (comma separated, e.g., 40% faster, 50% more leads)" rows="2" />
       <BaseTextArea v-model="form.features" placeholder="Features (comma separated)" rows="2" />
       <BaseInput v-model="form.tech_stack" placeholder="Tech Stack (comma separated)" />
       <BaseInput v-model="form.gallery" placeholder="Gallery image URLS (comma separated)" />

       <div class="">
        <label class="block text-sm font-medium mb-1">Hero Image</label>
        <input type="file" accept="image/*" @change="handleHeroImageUpload" />
        <img v-if="previewHeroImage" :src="previewHeroImage" class="mt-2 h-32 w-auto object-cover rounded border">
       </div>
       
       <select v-model="form.status" class="border rounded-xl px-4 py-2">
        <option value="planning">Planning</option>
        <option value="in_progress">In Progress</option>
        <option value="launched">LAunched</option>
        <option value="maintainance">Maintainance</option>
       </select>

      <div class="flex gap-3">
        <BaseButton @click="saveProject" :disabled="loading">
          {{ form.id ? 'Update' : 'Create' }} Project
        </BaseButton>
        <BaseButton variant="secondary" @click="resetForm">
          Cancel
        </BaseButton>
      </div>
     </div>

     <!-- List -->
      <div class="bg-white rounded-3xl border overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="px-6 py-3 text-left">Title</th>
              <th class="px-6 py-3 text-left">Technologies</th>
              <th class="px-6 py-3 text-left">Featured</th>
              <th class="px-6 py-3 text-left">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in store.projects" :key="item.id" class="border-b">
              <td class="px-6 py-4 flex items-center gap-2">
                <img v-if="item.image" :src="item.image" class="h-10 w-10 object-cover rounded" />
                <span>{{ item.title }}</span>
              </td>
              <td class="px-6 py-4 max-w-xs truncate">{{ item.technologies }}</td>
              <td class="px-6 py-4">{{ item.featured ? '⭐' : '—' }}</td>
              <td class="px-6 py-4">
                <button @click="editProject(item)" class="text-blue-600 mr-3">Edit</button>
                <button @click="confirmDelete(item.id)" class="text-red-600">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- DeleteModal -->
       <DeleteModal
        :show="showDeleteModal" 
        title="Delete Project?" 
        message="This action cannot be undone." 
        @close="showDeleteModal=false" 
        @confirm="deleteProject" 
      />
  </div>
</template>