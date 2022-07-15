import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { guard } from './helpers/guard';
// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'bootstrap/dist/css/bootstrap.css';

import 'bootstrap/dist/js/bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App);
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router);

app.mount('#app');

app.directive('focus', {
  mounted: (element, binding) => {
    guard(binding.value === false) || element.focus();
  },
});
