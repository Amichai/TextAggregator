import {createRouter, createWebHistory} from 'vue-router'
import HelloWorld from './../components/HelloWorld.vue'
import ProjectBoard from './../components/ProjectBoard.vue'
import ProjectsList from './../components/ProjectsList.vue'

const routes = [
    { path: '/', component: HelloWorld },
    { 
      path: '/project/:projectId', 
      name: "Project",
      component: ProjectBoard,
      props: true,    
    },
    { 
      path: '/projects', 
      name: "Projects",
      component: ProjectsList,
      props: true,
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router;