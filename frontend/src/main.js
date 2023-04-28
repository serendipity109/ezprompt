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
    { path: '/', component: Home },
    { path: '/page', component: Page }
  ]
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
