import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomePage.vue'
import Prompt from '@/views/PromptPage.vue'
import Test from '@/views/TestPage.vue'
import Gen from '@/views/GenPage.vue'
import Auth from '@/views/GoogleAuth.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', redirect: '/home'},
        {path: '/auth', component: Auth},
        {path: '/test', component: Test},
        {path: '/home', component: Home, meta: {title: 'EZPrompt'}},
        {
            path: '/image/:img',
            component: Prompt,
            meta: {title: 'EZPrompt - prompt'}
        },
        {path: '/generate', component: Gen, meta: {title: 'EZPrompt - Generate'}}
        ]
  });

export default router