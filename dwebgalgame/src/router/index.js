import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

  const routes = [
  //场景管理
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  //角色仓库
  {
    path: '/actor-store',
    name: 'ActorStore',
    component: () => import(/* webpackChunkName: "about" */ '../views/ActorStore.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
