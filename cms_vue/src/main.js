// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import axios from './http/http'

import mavonEditor from 'mavon-editor' //markdown
import 'mavon-editor/dist/css/index.css'

import token from './tool/token'
import Request from './tool/Requst'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(mavonEditor)
Vue.prototype.$axios = axios
Vue.prototype.$token = token
Vue.prototype.$request = Request
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
