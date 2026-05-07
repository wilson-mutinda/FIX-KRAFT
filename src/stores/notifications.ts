import { defineStore } from "pinia";
import { ref } from "vue";

export const useNotifications = defineStore('notofications', () => {
    const notifications = ref<any[]>([])

    const show = (
        message: string,
        type = 'success'
    ) => {

        const id = Date.now()

        notifications.value.push({
            id,
            message,
            type
        })

        setTimeout(() => {
            notifications.value = 
                notifications.value.filter(n => n.id !== id)
        }, 3000);
    }

    return {
        notifications,
        show
    }
})