<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { usePublicBlogStore } from '@/stores/publicBlog';

const route = useRoute();
const store = usePublicBlogStore();
const post = ref<any>(null);
const loading = ref(true);

onMounted(async () => {
  const slug = route.params.slug as string;
  post.value = await store.getPostBySlug(slug);
  loading.value = false;
});
</script>

<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen py-20">
    <div class="max-w-4xl mx-auto px-6">
      <!-- Back Link -->
       <div class="mb-8">
        <router-link to="/blog" class="text-primary hover:underline inline-flex items-center gap-1">
          ← Back to Blog
        </router-link>
       </div>

      <div v-if="loading" class="text-center py-20">Loading...</div>
      <div v-else-if="!post" class="text-center py-20">
        <p class="text-gray-500">Post not found.</p>
        <router-link to="/blog" class="text-primary mt-4 inline-block">← Back to blog</router-link>
      </div>
      <div v-else class="">
        <article class="prose dark:prose-invert lg:prose-lg max-w-none">
          <h1 class="text-4xl font-bold mb-4">{{ post.title }}</h1>
          <div class="flex items-center gap-4 text-gray-500 text-sm mb-8">
            <span>{{ new Date(post.published_at).toLocaleDateString() }}</span>
            <span>•</span>
            <span>{{ post.author }}</span>
            <span>•</span>
            <span>{{ post.read_time }} min read</span>
          </div>
          <img :src="post.image || 'https://via.placeholder.com/800x400'" class="w-full rounded-xl mb-8" />
          <div class="text-gray-700 dark:text-gray-200" v-html="post.content"></div>
        </article>

        <!-- Footer actions -->
         <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-wrap gap-4 justify-between items-center">
            <router-link to="/blog" class="text-primary hover:underline inline-flex items-center gap-1">
              ← Back to all posts
            </router-link>
            <router-link to="/contact" class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary/90 transition">
              Start a Project
            </router-link>
          </div>
         </div>
      </div>
    </div>
  </div>
</template>