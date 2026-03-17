// pages/reminders/reminders.js
const app = getApp()

Page({
  data: {
    reminders: [
      {
        id: 1,
        time: '08:00',
        text: '阿司匹林 100mg',
        enabled: true
      },
      {
        id: 2,
        time: '12:00',
        text: '午餐后测血糖',
        enabled: false
      },
      {
        id: 3,
        time: '20:00',
        text: '运动 30 分钟',
        enabled: true
      }
    ]
  },

  onLoad() {
    this.loadReminders()
  },

  // 加载提醒列表
  async loadReminders() {
    try {
      // TODO: 从后端 API 加载
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/reminders`,
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      // this.setData({ reminders: res.data })
    } catch (error) {
      console.error('加载提醒失败:', error)
    }
  },

  // 添加提醒
  addReminder() {
    wx.showActionSheet({
      itemList: ['用药提醒', '测量提醒', '运动提醒', '自定义提醒'],
      success: (res) => {
        const types = ['medicine', 'measurement', 'exercise', 'custom']
        const type = types[res.tapIndex]
        
        // 跳转到添加页面（需要创建）
        wx.navigateTo({
          url: `/pages/reminder-add/reminder-add?type=${type}`
        })
      }
    })
  },

  // 编辑提醒
  editReminder(e) {
    const id = e.currentTarget.dataset.id
    const reminder = this.data.reminders.find(r => r.id === id)
    
    if (reminder) {
      wx.navigateTo({
        url: `/pages/reminder-edit/reminder-edit?id=${id}`
      })
    }
  },

  // 切换提醒状态
  toggleReminder(e) {
    const id = e.currentTarget.dataset.id
    const reminders = this.data.reminders
    const index = reminders.findIndex(r => r.id === id)
    
    if (index !== -1) {
      reminders[index].enabled = !reminders[index].enabled
      this.setData({ reminders })
      
      wx.showToast({
        title: reminders[index].enabled ? '已开启' : '已关闭',
        icon: 'success'
      })
      
      // TODO: 同步到后端
    }
  }
})
