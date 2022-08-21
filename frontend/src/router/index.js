import { createRouter, createWebHistory } from 'vue-router';
import notebooksList from '../components/NotebooksList.vue';
import { authGuard } from '@auth0/auth0-vue';
import BoardView from '../components/BoardView.vue';
import NewBoard from '../components/NewBoard.vue';

const routes = [
  {
    path: '/notebook/:notebookId',
    name: 'Notebook',
    component: BoardView,
    props: true,
    beforeEnter: authGuard,
  },
  {
    path: '/:notebookId/new',
    name: 'New Notebook',
    component: NewBoard,
    props: true,
    beforeEnter: authGuard,
  },
  {
    path: '/',
    name: 'Home',
    component: notebooksList,
    props: true,
    beforeEnter: authGuard,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
