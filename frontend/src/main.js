import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { guard } from './helpers/guard';
import { createAuth0 } from '@auth0/auth0-vue';
import vClickOutside from 'click-outside-vue3'

// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap';

const app = createApp(App);
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router);
app.use(vClickOutside);

app.use(
  createAuth0({
    domain: "aggregator.us.auth0.com",
    client_id: "Mqq6ULo4pNo87OUctjgLxrFHQoql8tJI",
    redirect_uri: window.location.origin
  })
);

  
app.mount('#app');

app.directive('focus', {
  mounted: (element, binding) => {
    guard(binding.value === false) || element.focus();
  },
});
  
