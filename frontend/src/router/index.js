import { createRouter, createWebHistory } from 'vue-router';
import notebookBoard from '../components/NotebookBoard.vue';
import notebooksList from '../components/NotebooksList.vue';
import NewSnippet from '../components/NewSnippet.vue';
import { authGuard } from '@auth0/auth0-vue';
import BoardView from '../components/BoardView.vue'


const routes = [
  {
    path: '/notebook/:notebookId',
    name: 'notebook',
    component: BoardView,
    props: true,
    beforeEnter: authGuard
  },
  {
    path: '/:notebookId/Snippet/:snippetId',
    name: 'Snippet',
    component: NewSnippet,
    props: true,
    beforeEnter: authGuard
  },
  {
    path: '/',
    name: 'Home',
    component: notebooksList,
    props: true,
    beforeEnter: authGuard
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
