import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    userInfo: null,
    token: '',
    hasLogin: false
  },
  mutations: {
    // 设置用户信息
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo
    },
    // 设置登录状态
    setLoginStatus(state, status) {
      state.hasLogin = status
    },
    // 设置token
    setToken(state, token) {
      state.token = token
    }
  },
  actions: {
    // 登录
    login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        // 这里可以调用登录接口
        // 模拟登录成功
        commit('setUserInfo', userInfo)
        commit('setLoginStatus', true)
        commit('setToken', 'mock-token')
        resolve()
      })
    },
    // 登出
    logout({ commit }) {
      commit('setUserInfo', null)
      commit('setLoginStatus', false)
      commit('setToken', '')
    }
  },
  getters: {
    // 获取用户信息
    getUserInfo: state => state.userInfo,
    // 获取登录状态
    getLoginStatus: state => state.hasLogin,
    // 获取token
    getToken: state => state.token
  }
})

export default store 