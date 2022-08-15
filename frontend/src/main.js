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
import contenteditable from 'vue-contenteditable'

import dayjs from 'dayjs'
import updateLocale from 'dayjs/plugin/updateLocale'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'

import FloatingVue from 'floating-vue'

dayjs.extend(updateLocale)
dayjs.extend(relativeTime)
dayjs.extend(utc)

dayjs.updateLocale('en', {
  relativeTime: {
    future: 'in %s',
    past: '%s ago',
    s: 'a few seconds',
    m: 'a minute',
    mm: '%d mins',
    h: 'an hour',
    hh: '%d hours',
    d: 'a day',
    dd: '%d days',
    M: 'a month',
    MM: '%d months',
    y: 'a year',
    yy: '%d years',
  },
})

const app = createApp(App);
app.use(FloatingVue)

// Make sure to _use_ the router instance to make the
// whole app router-aware.
// app.use(contenteditable)

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
  
