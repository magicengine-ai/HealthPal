// pages/settings/settings.js
Page({
  data: {
    medicineReminder: true,
    measurementReminder: false,
    alertEnabled: true,
    privacyIndex: 0,
    privacyOptions: ['仅自己', '家人可见', '完全公开'],
    syncEnabled: true,
    darkMode: false
  },

  onLoad() {
    this.loadSettings()
  },

  // 加载设置
  async loadSettings() {
    try {
      const settings = wx.getStorageSync('settings')
      if (settings) {
        this.setData(settings)
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  },

  // 保存设置
  saveSettings() {
    try {
      wx.setStorageSync('settings', {
        medicineReminder: this.data.medicineReminder,
        measurementReminder: this.data.measurementReminder,
        alertEnabled: this.data.alertEnabled,
        privacyIndex: this.data.privacyIndex,
        syncEnabled: this.data.syncEnabled,
        darkMode: this.data.darkMode
      })
    } catch (error) {
      console.error('保存设置失败:', error)
    }
  },

  // 切换用药提醒
  toggleMedicineReminder(e) {
    this.setData({ medicineReminder: e.detail.value })
    this.saveSettings()
    wx.showToast({
      title: e.detail.value ? '已开启' : '已关闭',
      icon: 'success'
    })
  },

  // 切换测量提醒
  toggleMeasurementReminder(e) {
    this.setData({ measurementReminder: e.detail.value })
    this.saveSettings()
    wx.showToast({
      title: e.detail.value ? '已开启' : '已关闭',
      icon: 'success'
    })
  },

  // 切换异常预警
  toggleAlert(e) {
    this.setData({ alertEnabled: e.detail.value })
    this.saveSettings()
    wx.showToast({
      title: e.detail.value ? '已开启' : '已关闭',
      icon: 'success'
    })
  },

  // 隐私设置变更
  onPrivacyChange(e) {
    this.setData({ privacyIndex: parseInt(e.detail.value) })
    this.saveSettings()
    wx.showToast({
      title: '已保存',
      icon: 'success'
    })
  },

  // 切换数据同步
  toggleSync(e) {
    this.setData({ syncEnabled: e.detail.value })
    this.saveSettings()
    wx.showToast({
      title: e.detail.value ? '已开启' : '已关闭',
      icon: 'success'
    })
  },

  // 切换深色模式
  toggleDarkMode(e) {
    this.setData({ darkMode: e.detail.value })
    this.saveSettings()
    wx.showToast({
      title: '重启后生效',
      icon: 'success'
    })
  },

  // 清除缓存
  clearCache() {
    wx.showModal({
      title: '清除缓存',
      content: '确定要清除缓存吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync()
          wx.showToast({
            title: '已清除',
            icon: 'success'
          })
        }
      }
    })
  },

  // 清除所有数据
  clearAllData() {
    wx.showModal({
      title: '⚠️ 危险操作',
      content: '确定要清除所有数据吗？此操作不可恢复！',
      confirmColor: '#f5222d',
      success: (res) => {
        if (res.confirm) {
          wx.showModal({
            title: '再次确认',
            content: '真的要清除所有数据吗？',
            confirmColor: '#f5222d',
            success: (res2) => {
              if (res2.confirm) {
                wx.clearStorageSync()
                wx.showToast({
                  title: '已清除所有数据',
                  icon: 'success',
                  duration: 2000
                })
                setTimeout(() => {
                  wx.reLaunch({ url: '/pages/index/index' })
                }, 2000)
              }
            }
          })
        }
      }
    })
  }
})
