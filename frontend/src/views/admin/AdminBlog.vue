<script setup lang="ts">
import DeleteModal from '@/components/admin/DeleteModal.vue';
import PageHeader from '@/components/admin/PageHeader.vue';
import BaseButton from '@/components/ui/BaseButton.vue';
import BaseInput from '@/components/ui/BaseInput.vue';
import BaseTextArea from '@/components/ui/BaseTextArea.vue';
import { useBlogStore } from '@/stores/blog';
import { onMounted, ref } from 'vue';

const loading = ref(false);
const store = useBlogStore();
const editingPost = ref<any>(null);
const showDeleteModal = ref(false);
const deleteId = ref<number | null>(null);

interface PostForm {
  id: number | null;
  title: string;
  excerpt: string;
  content: string;
  category: string;
  status: string;
  read_time: number;
  image: File | null;
}

const form = ref<PostForm>({
  id: null,
  title: '',
  excerpt: '',
  content: '',
  category: '',
  status: 'draft',
  read_time: 3,
  image: null,
});

const previewImage = ref('');

const resetForm = () => {
  form.value = {
    id: null,
    title: '',
    excerpt: '',
    content: '',
    category: '',
    status: 'draft',
    read_time: 3,
    image: null,
  };
  previewImage.value = '';
  editingPost.value = null;
};

const savePost = async () => {
  loading.value = true;
  const formData = new FormData();
  // Append all fields except 'id' and 'image' (handle image separately)
  (Object.keys(form.value) as Array<keyof PostForm>).forEach(key => {
    if (key !== 'id' && key !== 'image' && form.value[key] !== null && form.value[key] !== undefined) {
      formData.append(key, String(form.value[key]));
    }
  });
  if (form.value.image) {
    formData.append('image', form.value.image);
  }
  if (form.value.id) {
    await store.update(form.value.id, formData);
  } else {
    await store.create(formData);
  }
  resetForm();
  await store.load();
  loading.value = false;
};

const editPost = (post: any) => {
  form.value = { ...post, image: null };
  previewImage.value = post.image;
  editingPost.value = post;
};

const confirmDelete = (id: number) => {
  deleteId.value = id;
  showDeleteModal.value = true;
};

const deletePost = async () => {
  if (deleteId.value) {
    await store.remove(deleteId.value);
    await store.load();
  }
  showDeleteModal.value = false;
};

const handleImageUpload = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    form.value.image = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

onMounted(() => {
  store.load();
});
</script>

<template>
  <div class="space-y-3">
    <PageHeader title="Blog Manager" subtitle="Create, edit and delete blog posts" />

    <!-- Form -->
    <div class="bg-white rounded-3xl border p-6 space-y-4">
      <BaseInput v-model="form.title" placeholder="Post title" />
      <BaseInput v-model="form.category" placeholder="Category (e.g., Insights, Trends)" />
      <BaseTextArea v-model="form.excerpt" placeholder="Short excerpt (used on listing)" rows="2" />
      <BaseTextArea v-model="form.content" placeholder="Full content (HTML / markdown)" rows="6" />
      <div class="flex gap-4">
        <select v-model="form.status" class="border rounded-xl px-4 py-2">
          <option value="draft">Draft</option>
          <option value="published">Published</option>
        </select>
        <input type="number" v-model="form.read_time" class="border rounded-xl px-4 py-2 w-24" placeholder="Read time (min)" />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Featured image</label>
        <input type="file" accept="image/*" @change="handleImageUpload" />
        <img v-if="previewImage" :src="previewImage" class="mt-2 h-32 w-auto object-cover rounded" />
      </div>
      <div class="flex gap-3">
        <BaseButton @click="savePost" :disabled="loading">{{ form.id ? 'Update' : 'Create' }} Post</BaseButton>
        <BaseButton variant="secondary" @click="resetForm">Cancel</BaseButton>
      </div>
    </div>

    <!-- List -->
    <div class="bg-white rounded-3xl border overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b">
          <tr>
            <th class="px-6 py-3 text-left">Title</th>
            <th class="px-6 py-3 text-left">Category</th>
            <th class="px-6 py-3 text-left">Status</th>
            <th class="px-6 py-3 text-left">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in store.posts" :key="post.id" class="border-b">
            <td class="px-6 py-4">{{ post.title }}</td>
            <td class="px-6 py-4">{{ post.category }}</td>
            <td class="px-6 py-4">{{ post.status }}</td>
            <td class="px-6 py-4">
              <button @click="editPost(post)" class="text-blue-600 mr-3">Edit</button>
              <button @click="confirmDelete(post.id)" class="text-red-600">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <DeleteModal :show="showDeleteModal" title="Delete Post?" message="This action cannot be undone." @close="showDeleteModal=false" @confirm="deletePost" />
  </div>
</template>