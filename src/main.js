import { createApp } from 'vue';

import App from './App.vue';
import router from './router.js';
import store from './store/index.js';
import TheIsofields from './components/figures/TheIsofields.vue';

const app = createApp(App);

app.use(router);
app.use(store);

app.component('the-isofields', TheIsofields);

app.mount('#app');
