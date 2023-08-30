import { createApp } from "vue";
import App from "./App.vue";
import "./assets/tailwind.css";
import { createVuetify } from "vuetify";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import router from "./router";
import vue3GoogleLogin from 'vue3-google-login'

const vuetify = createVuetify({});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title; // 設置網頁標題
  next();
});

// create your Vue app
const app = createApp(App);

app.use(vue3GoogleLogin, {
  clientId: '734101254265-37fk1rd4de279jecj99m6l78pq8rqljh.apps.googleusercontent.com'
});

app.use(router).use(vuetify).use(ElementPlus).mount("#app");
