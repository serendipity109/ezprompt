import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/HomePage.vue'
import Prompt from './components/PromptPage.vue'
import Gen from './components/GenPage.vue'
import './assets/tailwind.css'

const app = createApp(App)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/', redirect: '/home'},
    {path: '/home', component: Home, meta: {title: 'SDXL'}},
    {
      path: '/image/:img',
      component: Prompt,
      meta: {title: 'SDXL - prompt'}
    },
    {path: '/generate', component: Gen, meta: {title: 'SDXL - Generate'}}
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title // 設置網頁標題
  next()
})

app.use(router)

app.mount('#app')
