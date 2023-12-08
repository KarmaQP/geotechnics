import { createApp } from 'vue';

import App from './App.vue';
import router from './router.js';
import store from './store/index.js';

import TheIsofields from './components/figures/TheIsofields.vue';
import BaseDialog from './components/UI/BaseDialog.vue';

const app = createApp(App);

app.use(router);
app.use(store);

app.component('the-isofields', TheIsofields);
app.component('base-dialog', BaseDialog);

app.mount('#app');
