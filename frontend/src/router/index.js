import { createRouter, createWebHistory } from 'vue-router';
// import notebookBoard from '../components/ProjectBoard.vue';
// import notebooksList from '../components/ProjectsList.vue';
import notebookBoard from '../components/NotebookBoard.vue';
import notebooksList from '../components/NotebooksList.vue';
import NewSnippet from '../components/NewSnippet.vue';

const routes = [
  {
    path: '/notebook/:notebookId',
    name: 'notebook',
    component: notebookBoard,
    props: true,
  },
  {
    path: '/:notebookId/NewSnippet',
    name: 'New Snippet',
    component: NewSnippet,
    props: true,
  },
  {
    path: '/',
    name: 'Home',
    component: notebooksList,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
