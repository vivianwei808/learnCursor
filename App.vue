<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
    // 检查更新
    if (uni.canIUse('getUpdateManager')) {
      const updateManager = uni.getUpdateManager()
      updateManager.onCheckForUpdate(function(res) {
        if (res.hasUpdate) {
          updateManager.onUpdateReady(function() {
            uni.showModal({
              title: '更新提示',
              content: '新版本已经准备好，是否重启应用？',
              success: function(res) {
                if (res.confirm) {
                  updateManager.applyUpdate()
                }
              }
            })
          })
        }
      })
    }
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
/* 全局样式 */
page {
  background-color: #f8f8f8;
  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica,
    Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei',
    sans-serif;
}

/* 清除浮动 */
.clearfix:after {
  content: '';
  display: block;
  clear: both;
}

/* 通用容器 */
.container {
  padding: 20rpx;
}

/* 通用按钮样式 */
.btn {
  padding: 20rpx 40rpx;
  border-radius: 8rpx;
  text-align: center;
  font-size: 28rpx;
}

.btn-primary {
  background-color: #007aff;
  color: #ffffff;
}

.btn-default {
  background-color: #f8f8f8;
  color: #333333;
  border: 1px solid #dddddd;
}
</style> 