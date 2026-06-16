import { API_BASE_URI } from "@/config/api";
import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const usePublicBlogStore = defineStore('publicBlog', () => {
    const posts = ref<any[]>([])
    const loading = ref(false)

    const load = async () => {
        loading.value = true
        try {
            const res = await axios.get(`${API_BASE_URI}/blog/?status=published`)
            posts.value = res.data
        } catch (err) {
            console.error(err)
        } finally {
            loading.value = false
        }
    }

    const getPostBySlug = async (slug: string) => {
        const res = await axios.get(`${API_BASE_URI}/blog/?slug=${slug}`)
        return res.data[0]
    }

    return {
        posts,
        loading,
        load,
        getPostBySlug
    }
})