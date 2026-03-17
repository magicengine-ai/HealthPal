// pages/devices/devices.js
Page({
  data: {
    devices: [
      {
        id: 1,
        name: '小米手环',
        icon: '⌚',
        connected: false
      },
      {
        id: 2,
        name: '华为手表',
        icon: '⌚',
        connected: false
      },
      {
        id: 3,
        name: '欧姆龙血压计',
        icon: '💓',
        connected: false
      },
      {
        id: 4,
        name: '鱼跃血糖仪',
        icon: '🩸',
        connected: false
      },
      {
        id: 5,
        name: '小米体重秤',
        icon: '⚖️',
        connected: false
      }
    ]
  },

  // 绑定设备
  bindDevice(e) {
    const id = e.currentTarget.dataset.id
    const device = this.data.devices.find(d => d.id === id)
    
    if (device && device.connected) {
      // 已连接，显示管理菜单
      wx.showActionSheet({
        itemList: ['同步数据', '解除绑定', '设备设置'],
        success: (res) => {
          const actions = ['sync', 'unbind', 'settings']
          this.handleDeviceAction(actions[res.tapIndex], device)
        }
      })
    } else {
      // 未连接，开始绑定
      this.startBinding(device)
    }
  },

  // 开始绑定
  startBinding(device) {
    wx.showLoading({ title: '搜索设备...', mask: true })
    
    // 模拟蓝牙搜索
    setTimeout(() => {
      wx.hideLoading()
      
      wx.showModal({
        title: `绑定 ${device.name}`,
        content: '请确保设备已开启并靠近手机，然后按照设备说明书进行配对。',
        confirmText: '开始配对',
        success: (res) => {
          if (res.confirm) {
            // TODO: 调用蓝牙 API 进行配对
            wx.showToast({
              title: '配对成功',
              icon: 'success'
            })
            
            // 更新设备状态
            const devices = this.data.devices
            const index = devices.findIndex(d => d.id === device.id)
            if (index !== -1) {
              devices[index].connected = true
              this.setData({ devices })
            }
          }
        }
      })
    }, 1500)
  },

  // 处理设备操作
  handleDeviceAction(action, device) {
    switch (action) {
      case 'sync':
        wx.showLoading({ title: '同步中...', mask: true })
        setTimeout(() => {
          wx.hideLoading()
          wx.showToast({ title: '同步完成', icon: 'success' })
        }, 2000)
        break
        
      case 'unbind':
        wx.showModal({
          title: '解除绑定',
          content: `确定要解除与 ${device.name} 的绑定吗？`,
          confirmColor: '#f5222d',
          success: (res) => {
            if (res.confirm) {
              const devices = this.data.devices
              const index = devices.findIndex(d => d.id === device.id)
              if (index !== -1) {
                devices[index].connected = false
                this.setData({ devices })
              }
              wx.showToast({ title: '已解除绑定', icon: 'success' })
            }
          }
        })
        break
        
      case 'settings':
        wx.navigateTo({
          url: `/pages/device-settings/device-settings?id=${device.id}`
        })
        break
    }
  },

  // 添加设备
  addDevice() {
    wx.navigateTo({
      url: '/pages/device-add/device-add'
    })
  }
})
