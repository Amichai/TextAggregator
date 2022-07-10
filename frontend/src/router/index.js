import { createRouter, createWebHistory } from 'vue-router';
import ProjectBoard from '../components/ProjectBoard.vue';
import ProjectsList from '../components/ProjectsList.vue';
import NewSnippet from '../components/NewSnippet.vue';

const routes = [
  {
    path: '/project/:projectId',
    name: 'Project',
    component: ProjectBoard,
    props: true,
  },
  {
    path: '/:projectId/NewSnippet',
    name: 'New Snippet',
    component: NewSnippet,
    props: true,
  },
  {
    path: '/',
    name: 'Home',
    component: ProjectsList,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
