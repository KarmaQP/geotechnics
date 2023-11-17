import { createRouter, createWebHistory } from 'vue-router';

// import TheIsofields from './components/figures/TheIsofields.vue';
import CreateScheme from './components/pages/CreateScheme.vue';
import CalculatedProperties from './components/pages/CalculatedProperties.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/page1' },
    { path: '/page1', component: CreateScheme },
    { path: '/page2', component: CalculatedProperties },
  ],
});

export default router;
