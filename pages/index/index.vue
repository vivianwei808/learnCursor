<template>
  <view class="container">
    <view class="header">
      <text class="title">欢迎使用 UniApp</text>
    </view>
    
    <view class="content">
      <view class="card" v-for="(item, index) in list" :key="index">
        <text class="card-title">{{ item.title }}</text>
        <text class="card-desc">{{ item.desc }}</text>
      </view>
    </view>

    <view class="footer">
      <button class="btn btn-primary" @click="handleClick">点击事件</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      list: [
        {
          title: 'UniApp 跨平台开发',
          desc: '一套代码，多端运行'
        },
        {
          title: 'Vue.js 框架',
          desc: '易学易用，性能出色'
        },
        {
          title: 'iOS 原生体验',
          desc: '接近原生的性能和体验'
        }
      ]
    }
  },
  methods: {
    handleClick() {
      this.showToast('按钮被点击了')
    }
  }
}
</script>

<style lang="scss">
.container {
  padding: 30rpx;
}

.header {
  text-align: center;
  padding: 40rpx 0;
  
  .title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
  }
}

.content {
  .card {
    background-color: #fff;
    border-radius: 12rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.1);
    
    .card-title {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 20rpx;
      display: block;
    }
    
    .card-desc {
      font-size: 28rpx;
      color: #666;
      display: block;
    }
  }
}

.footer {
  margin-top: 40rpx;
  text-align: center;
}
</style> 