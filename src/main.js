import { createApp } from 'vue';

import TheIsofields from './components/figures/TheIsofields.vue';

import App from './App.vue';
import router from './router.js';

const app = createApp(App);

app.use(router);

app.component('the-isofields', TheIsofields);

app.mount('#app');
