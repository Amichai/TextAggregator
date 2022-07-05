import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

import "bootstrap/dist/css/bootstrap.css";

const app = createApp(App);
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router);

app.mount("#app");

import "bootstrap/dist/js/bootstrap.js";
