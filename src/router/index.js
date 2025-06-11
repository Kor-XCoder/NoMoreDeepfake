import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import ResultView from "../views/ResultView.vue";
import InfoView from "../views/InfoView.vue";


const routes = [
  { path: "/", component: HomeView },
  { path: "/result", component: ResultView,
    props: route => ({
      fileId: route.query.fileId,
      isDeepfake: route.query.isDeepfake,
      reliability: route.query.reliability,
    }),
   },
  { path: "/info", component: InfoView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
