// pages/records/records.js
const app = getApp()

Page({
  data: {
    searchKeyword: '',
    currentCategory: 'all',
    records: [
      {
        id: 1,
        icon: '🏥',
        title: '2026 年年度体检',
        hospital: '北京协和医院',
        date: '3 月 1 日',
        summary: '12 项指标 · 2 项异常',
        tags: ['体检', '年度'],
        status: 'completed',
        statusText: '已完成'
      },
      {
        id: 2,
        icon: '🩸',
        title: '血常规检查',
        hospital: '北京协和医院',
        date: '2 月 15 日',
        summary: '8 项指标 · 全部正常',
        tags: ['检查', '血常规'],
        status: 'completed',
        statusText: '已完成'
      },
      {
        id: 3,
        icon: '💓',
        title: '心电图报告',
        hospital: '北京协和医院',
        date: '1 月 10 日',
        summary: '窦性心律 · 正常',
        tags: ['检查', '心电图'],
        status: 'completed',
        statusText: '已完成'
      },
      {
        id: 4,
        icon: '💊',
        title: '门诊病历',
        hospital: '北京协和医院',
        date: '1 月 5 日',
        summary: '诊断：上呼吸道感染',
        tags: ['病历', '门诊'],
        status: 'completed',
        statusText: '已完成'
      },
      {
        id: 5,
        icon: '📄',
        title: '肝功能检查',
        hospital: '北京协和医院',
        date: '12 月 20 日',
        summary: 'OCR 识别中...',
        tags: ['检查', '肝功能'],
        status: 'processing',
        statusText: '识别中'
      }
    ]
  },

  onLoad(options) {
    // 处理从首页传来的参数
    if (options.action === 'add_symptom') {
      this.uploadRecord()
    }
  },

  get filteredRecords() {
    const { searchKeyword, currentCategory, records } = this.data
    
    return records.filter(record => {
      // 分类筛选
      if (currentCategory !== 'all') {
        const categoryMap = {
          'checkup': '体检',
          'medical': '病历',
          'lab': '检查',
          'prescription': '处方'
        }
        const category = categoryMap[currentCategory]
        if (!record.tags.includes(category)) {
          return false
        }
      }
      
      // 搜索筛选
      if (searchKeyword) {
        const keyword = searchKeyword.toLowerCase()
        return record.title.toLowerCase().includes(keyword) ||
               record.hospital.toLowerCase().includes(keyword) ||
               record.summary.toLowerCase().includes(keyword)
      }
      
      return true
    })
  },

  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    })
  },

  // 切换分类
  switchCategory(e) {
    const category = e.currentTarget.dataset.category
    this.setData({
      currentCategory: category
    })
  },

  // 跳转到详情页
  goToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/record-detail/record-detail?id=${id}`
    })
  },

  // 上传档案
  uploadRecord() {
    wx.chooseMedia({
      count: 9,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFiles = res.tempFiles
        console.log('选择的文件:', tempFiles)
        
        // 显示上传进度
        wx.showLoading({
          title: '上传中...',
          mask: true
        })
        
        // TODO: 上传到服务器
        setTimeout(() => {
          wx.hideLoading()
          wx.showToast({
            title: '上传成功',
            icon: 'success'
          })
          
          // 刷新列表
          this.loadRecords()
        }, 1500)
      }
    })
  },

  // 加载档案列表
  async loadRecords() {
    try {
      // TODO: 从后端 API 加载
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/records`,
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      // this.setData({ records: res.data.records })
      
      console.log('加载档案列表')
    } catch (error) {
      console.error('加载档案失败:', error)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadRecords().then(() => {
      wx.stopPullDownRefresh()
    })
  }
})
