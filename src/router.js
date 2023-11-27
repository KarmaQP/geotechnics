import { createRouter, createWebHistory } from 'vue-router';

import CreateScheme from './components/pages/CreateScheme.vue';
import CalculatedProperties from './components/pages/CalculatedProperties.vue';
import MaterialCharacteristics from './components/pages/MaterialCharacteristics.vue';
import CalculatedStages from './components/pages/CalculatedStages.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/page1' },
    { path: '/page1', component: CreateScheme },
    { path: '/page2', component: CalculatedProperties },
    { path: '/page3', component: MaterialCharacteristics },
    { path: '/page4', component: CalculatedStages },
  ],
});

export default router;
