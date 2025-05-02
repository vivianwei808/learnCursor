<template>
  <view class="container">
    <view class="user-info" v-if="hasLogin">
      <image class="avatar" :src="userInfo.avatar || '/static/images/default-avatar.png'" mode="aspectFill"></image>
      <text class="nickname">{{ userInfo.nickname || '未设置昵称' }}</text>
    </view>
    
    <view class="login-box" v-else>
      <button class="btn btn-primary" @click="handleLogin">点击登录</button>
    </view>

    <view class="menu-list">
      <view class="menu-item" v-for="(item, index) in menuList" :key="index" @click="handleMenuClick(item)">
        <text class="menu-title">{{ item.title }}</text>
        <text class="arrow">></text>
      </view>
    </view>

    <view class="logout" v-if="hasLogin">
      <button class="btn btn-default" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      menuList: [
        { title: '我的订单', path: '/pages/order/order' },
        { title: '收货地址', path: '/pages/address/address' },
        { title: '设置', path: '/pages/settings/settings' }
      ]
    }
  },
  computed: {
    ...mapState({
      userInfo: state => state.userInfo,
      hasLogin: state => state.hasLogin
    })
  },
  methods: {
    ...mapActions(['login', 'logout']),
    
    handleLogin() {
      // 模拟登录
      this.login({
        nickname: '测试用户',
        avatar: '/static/images/default-avatar.png'
      })
    },
    
    handleLogout() {
      this.logout()
      this.showToast('已退出登录')
    },
    
    handleMenuClick(item) {
      if (!this.hasLogin && item.needLogin) {
        this.showToast('请先登录')
        return
      }
      uni.navigateTo({
        url: item.path
      })
    }
  }
}
</script>

<style lang="scss">
.container {
  padding: 30rpx;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 0;
  
  .avatar {
    width: 150rpx;
    height: 150rpx;
    border-radius: 50%;
    margin-bottom: 20rpx;
  }
  
  .nickname {
    font-size: 32rpx;
    color: #333;
  }
}

.login-box {
  padding: 40rpx 0;
  text-align: center;
}

.menu-list {
  background-color: #fff;
  border-radius: 12rpx;
  margin-top: 30rpx;
  
  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
    
    .menu-title {
      font-size: 30rpx;
      color: #333;
    }
    
    .arrow {
      color: #999;
      font-size: 28rpx;
    }
  }
}

.logout {
  margin-top: 60rpx;
  text-align: center;
}
</style> 