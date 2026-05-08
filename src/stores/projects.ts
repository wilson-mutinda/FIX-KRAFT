import { defineStore } from "pinia";
import { ref } from "vue";

export const useProjectsStore = defineStore('projects', () => {

    const projects = ref<any[]>([])

    const load = () => {
        const saved = localStorage.getItem('projects')
        if (saved) projects.value = JSON.parse(saved)
    }

    const save = () => {
        localStorage.setItem('projects', JSON.stringify(projects.value))
    }

    const addProject = (project: any) => {
        project.id = Date.now()
        projects.value.push(project)
        save()
    }

    const deleteProject = (id: number) => {
        projects.value = projects.value.filter(p => p.id !== id)
        save()
    }

    const updateProject = (
        id: number,
        updated: any
        ) => {

        const index =
            projects.value.findIndex(
            p => p.id === id
            )

        if (index !== -1) {

            projects.value[index] = {
            ...projects.value[index],
            ...updated
            }

            save()
        }
    }

    const getById = (id: number) => {
        return projects.value.find(p => p.id === id)
    }

    return {
        projects,
        load,
        addProject,
        updateProject,
        deleteProject,
        getById
    }
})