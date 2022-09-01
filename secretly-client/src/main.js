import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
// import router from './router'

import "@/assets/main.css";
import VeeValidatePlugin from "@/includes/validation.js";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faCheck,
  faCircleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import { faSquareGithub } from "@fortawesome/free-brands-svg-icons";

library.add(faCheck, faCircleExclamation, faSquareGithub);

const app = createApp(App);

app.use(createPinia());
app.use(VeeValidatePlugin);

app.component("font-awesome-icon", FontAwesomeIcon);
// app.use(router);

app.mount("#app");
