import Vue from 'vue'
import App from './App'
import store from './store'

Vue.config.productionTip = false

// 全局混入
Vue.mixin({
  methods: {
    // 全局方法示例
    showToast(title) {
      uni.showToast({
        title,
        icon: 'none'
      })
    }
  }
})

App.mpType = 'app'

const app = new Vue({
  store,
  ...App
})
app.$mount() 