<script setup lang="ts">
import { onMounted } from 'vue';
import { usePublicBlogStore } from '@/stores/publicBlog';

const store = usePublicBlogStore();
onMounted(() => store.load());
</script>

<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen">
    <section class="py-20 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-4xl mx-auto px-6">
        <h1 class="text-4xl font-bold mb-4">Insights & Updates</h1>
        <p class="text-gray-300">Practical advice and industry news from FixKraft Digital</p>
      </div>
    </section>

    <section class="py-20">
      <div class="max-w-7xl mx-auto px-6">
        <div v-if="store.loading" class="text-center py-20">Loading posts...</div>
        <div v-else-if="store.posts.length === 0" class="text-center py-20">No posts yet.</div>
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="post in store.posts" :key="post.id" class="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow hover:shadow-lg transition">
            <img :src="post.image || 'https://via.placeholder.com/400x200'" class="h-48 w-full object-cover" />
            <div class="p-6">
              <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-2">
                <span>{{ post.category }}</span>
                <span>•</span>
                <span>{{ new Date(post.published_at).toLocaleDateString() }}</span>
                <span>•</span>
                <span>{{ post.read_time }} min read</span>
              </div>
              <h2 class="text-xl font-bold mb-2">
                <router-link :to="`/blog/${post.slug}`" class="hover:text-primary transition">{{ post.title }}</router-link>
              </h2>
              <p class="text-gray-600 dark:text-gray-300 mb-4">{{ post.excerpt }}</p>
              <router-link :to="`/blog/${post.slug}`" class="text-primary font-semibold inline-flex items-center gap-1">
                Read more →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>