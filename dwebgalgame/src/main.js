import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import router from './router'
import store from './store'
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/icon/iconfont.css'
import './assets/css/mystyle.css'


Vue.use(ElementUI)
new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
