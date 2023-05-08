import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/HomePage.vue'
import Prompt from './components/PromptPage.vue'
import Test from './components/TestPage.vue'
import Gen from './components/GenPage.vue'
import './assets/tailwind.css'
import { createVuetify } from "vuetify";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/', redirect: '/home'},
    {path: '/test', component: Test},
    {path: '/home', component: Home, meta: {title: 'EZPrompt'}},
    {
      path: '/image/:img',
      component: Prompt,
      meta: {title: 'EZPrompt - prompt'}
    },
    {path: '/generate', component: Gen, meta: {title: 'EZPrompt - Generate'}}
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title // 設置網頁標題
  next()
})

app.use(router)

const vuetify = createVuetify({});
app.use(vuetify);

app.use(ElementPlus)

app.mount('#app')
