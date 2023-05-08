import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/HomePage.vue'
import Prompt from '@/components/PromptPage.vue'
import Test from '@/components/TestPage.vue'
import Gen from '@/components/GenPage.vue'


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
  });

export default router