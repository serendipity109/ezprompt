import { createApp } from 'vue'
import App from './App.vue'
import './assets/tailwind.css'
import { createVuetify } from "vuetify";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'

const vuetify = createVuetify({});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title // 設置網頁標題
  next()
})

createApp(App)
  .use(router)
  .use(vuetify)
  .use(ElementPlus)
  .mount('#app')
