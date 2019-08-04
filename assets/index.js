import 'babel-polyfill'
import Vue from 'vue'
import Vuex from 'vuex'

import createStore from './store'
import App from './components/App.vue'

Vue.config.productionTip = false
Vue.use(Vuex)

new Vue({
  store: createStore(),
  render: h => h(App)
}).$mount("#app");
