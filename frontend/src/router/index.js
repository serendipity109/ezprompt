import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/HomePage.vue";
import Prompt from "@/views/PromptPage.vue";
import Test from "@/views/TestPage.vue";
// import Gen from "@/views/GenPage.vue";
import CGen from "@/views/ControlGenPage.vue";
import Hist from "@/views/HistPage.vue";
import Acc from "@/views/AccountPage.vue";
import Show from "@/views/ShowPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/home" },
    { path: "/test", component: Test },
    {
      path: "/home",
      component: Home,
      props: (route) => ({ token: route.query.token }),
      meta: { title: "EZPrompt" },
    },
    {
      path: "/image/:id",
      component: Prompt,
      meta: { title: "EZPrompt - prompt" },
    },
    {
      path: "/generate",
      component: CGen,
      meta: { title: "EZPrompt - ControlGenerate" },
    },
    {
      path: "/history",
      component: Hist,
      meta: { title: "EZPrompt - History" },
    },
    {
      path: "/showcase",
      component: Show,
      meta: { title: "EZPrompt - Showcase" },
    },
    {
      path: "/account",
      component: Acc,
      meta: { title: "EZPrompt - Account" },
    },
  ],
});

export default router;
