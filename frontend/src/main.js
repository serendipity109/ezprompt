import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import Home from './components/HomePage.vue'
import Page from './components/PromptPage.vue'
import './assets/tailwind.css'

Vue.config.productionTip = false
Vue.config.devtools = true

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {path: '/', component: Home, meta: {title: 'SDXL'}},
    {
      path: '/image/:img',
      component: Page,
      meta: {title: 'SDXL - prompt'}
    },
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title // 設置網頁標題
  next()
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
