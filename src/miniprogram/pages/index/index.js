// pages/index/index.js
const app = getApp()

Page({
  data: {
    today: '',
    healthScore: 85,
    scoreLevel: '良好',
    beatPercent: 72,
    indicators: {
      bloodPressure: '120/80',
      bloodPressureStatus: 'normal',
      bloodPressureStatusText: '正常',
      bloodSugar: '5.6',
      bloodSugarStatus: 'normal',
      bloodSugarStatusText: '正常',
      weight: '65kg',
      weightStatus: 'normal',
      weightStatusText: '正常',
      heartRate: '72',
      heartRateStatus: 'normal',
      heartRateStatusText: '正常'
    },
    reminders: [
      {
        id: 1,
        time: '08:00',
        text: '阿司匹林 100mg',
        completed: true
      },
      {
        id: 2,
        time: '12:00',
        text: '午餐后测血糖',
        completed: false
      },
      {
        id: 3,
        time: '20:00',
        text: '运动 30 分钟',
        completed: false
      }
    ]
  },

  onLoad() {
    // 设置今天日期
    const today = new Date()
    const formattedDate = `${today.getMonth() + 1}月${today.getDate()}日`
    this.setData({ today: formattedDate })
    
    // 加载用户数据
    this.loadUserData()
  },

  onShow() {
    // 每次页面显示时刷新数据
    this.loadUserData()
  },

  // 加载用户健康数据
  async loadUserData() {
    try {
      // TODO: 从后端 API 加载真实数据
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/health/summary`,
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      // this.setData(res.data)
      
      console.log('加载健康数据')
    } catch (error) {
      console.error('加载数据失败:', error)
    }
  },

  // 切换提醒状态
  toggleReminder(e) {
    const id = e.currentTarget.dataset.id
    const reminders = this.data.reminders
    const index = reminders.findIndex(r => r.id === id)
    
    if (index !== -1) {
      reminders[index].completed = !reminders[index].completed
      this.setData({ reminders })
      
      // TODO: 同步到后端
      console.log(`提醒 ${id} 状态更新为: ${reminders[index].completed}`)
    }
  },

  // 跳转到指标详情
  goToIndicatorDetail(e) {
    const type = e.currentTarget.dataset.type
    wx.navigateTo({
      url: `/pages/analysis/analysis?type=${type}`
    })
  },

  // 跳转到分析页面
  goToAnalysis() {
    wx.switchTab({
      url: '/pages/analysis/analysis'
    })
  },

  // 跳转到提醒管理
  goToReminders() {
    // TODO: 跳转到提醒管理页面
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 上传报告
  uploadRecord() {
    wx.chooseMedia({
      count: 9,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFiles = res.tempFiles
        console.log('选择的文件:', tempFiles)
        
        // TODO: 上传到服务器进行 OCR 识别
        wx.showToast({
          title: '开始上传...',
          icon: 'loading',
          duration: 2000
        })
      }
    })
  },

  // 记录症状
  recordSymptom() {
    wx.navigateTo({
      url: '/pages/records/records?action=add_symptom'
    })
  },

  // 添加指标
  addIndicator() {
    wx.showActionSheet({
      itemList: ['血压', '血糖', '体重', '心率', '体温'],
      success: (res) => {
        const types = ['血压', '血糖', '体重', '心率', '体温']
        const type = types[res.tapIndex]
        // 跳转到指标录入页面
        wx.navigateTo({
          url: `/pages/indicator-add/indicator-add?type=${type}`
        })
      }
    })
  },

  // AI 问诊
  askAI() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  }
})
