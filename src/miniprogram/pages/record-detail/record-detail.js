// pages/record-detail/record-detail.js
const app = getApp()

Page({
  data: {
    recordId: '',
    record: {
      icon: '🏥',
      title: '2026 年年度体检',
      hospital: '北京协和医院',
      department: '体检中心',
      date: '2026-03-01'
    },
    indicators: [
      { name: '收缩压', value: '120', unit: 'mmHg', status: 'normal', statusText: '正常' },
      { name: '舒张压', value: '80', unit: 'mmHg', status: 'normal', statusText: '正常' },
      { name: '空腹血糖', value: '5.6', unit: 'mmol/L', status: 'normal', statusText: '正常' },
      { name: '总胆固醇', value: '5.8', unit: 'mmol/L', status: 'warning', statusText: '偏高' },
      { name: '甘油三酯', value: '1.5', unit: 'mmol/L', status: 'normal', statusText: '正常' },
      { name: '白细胞', value: '6.5', unit: '×10⁹/L', status: 'normal', statusText: '正常' },
      { name: '红细胞', value: '4.8', unit: '×10¹²/L', status: 'normal', statusText: '正常' },
      { name: '血小板', value: '250', unit: '×10⁹/L', status: 'normal', statusText: '正常' }
    ],
    aiAnalysis: '本次体检整体结果良好，大部分指标在正常范围内。需要注意的是总胆固醇略高于正常值（正常范围：<5.2 mmol/L），建议：\n\n1. 饮食控制：减少高脂肪、高胆固醇食物摄入\n2. 增加运动：每周至少 150 分钟中等强度有氧运动\n3. 3 个月后复查血脂指标\n\n其他指标均正常，请继续保持良好的生活习惯。',
    originalImages: [
      '/images/report-1.jpg',
      '/images/report-2.jpg'
    ]
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ recordId: options.id })
      this.loadRecordDetail(options.id)
    }
  },

  // 加载档案详情
  async loadRecordDetail(id) {
    try {
      // TODO: 从后端 API 加载
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/records/${id}`,
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      // this.setData(res.data)
      
      console.log('加载档案详情:', id)
    } catch (error) {
      console.error('加载详情失败:', error)
    }
  },

  // 导出报告
  exportReport() {
    wx.showActionSheet({
      itemList: ['导出为 PDF', '导出为图片', '分享给医生'],
      success: (res) => {
        const options = ['PDF', '图片', '分享']
        wx.showToast({
          title: `正在导出${options[res.tapIndex]}`,
          icon: 'loading',
          duration: 2000
        })
      }
    })
  },

  // 预览图片
  previewImage(e) {
    const index = e.currentTarget.dataset.index
    wx.previewImage({
      current: this.data.originalImages[index],
      urls: this.data.originalImages
    })
  },

  // 追问 AI
  askAI() {
    wx.navigateTo({
      url: `/pages/analysis/analysis?mode=chat&recordId=${this.data.recordId}`
    })
  },

  // 分享报告
  shareReport() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    })
    
    wx.showActionSheet({
      itemList: ['分享给好友', '分享到朋友圈', '复制链接'],
      success: (res) => {
        wx.showToast({
          title: '分享功能开发中',
          icon: 'none'
        })
      }
    })
  },

  // 在线咨询
  consultDoctor() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 分享
  onShareAppMessage() {
    return {
      title: `${this.data.record.title} - HealthPal`,
      path: `/pages/record-detail/record-detail?id=${this.data.recordId}`
    }
  }
})
