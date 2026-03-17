// pages/feedback/feedback.js
const app = getApp()

Page({
  data: {
    feedbackTypes: ['功能异常', '使用建议', '内容问题', '其他'],
    typeIndex: 0,
    contact: '',
    content: '',
    imageUrl: ''
  },

  // 类型选择
  onTypeChange(e) {
    this.setData({ typeIndex: parseInt(e.detail.value) })
  },

  // 联系方式输入
  onContactInput(e) {
    this.setData({ contact: e.detail.value })
  },

  // 内容输入
  onContentInput(e) {
    this.setData({ content: e.detail.value })
  },

  // 选择图片
  chooseImage() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        this.setData({
          imageUrl: res.tempFiles[0].tempFilePath
        })
      }
    })
  },

  // 预览图片
  previewImage() {
    if (this.data.imageUrl) {
      wx.previewImage({
        urls: [this.data.imageUrl]
      })
    }
  },

  // 删除图片
  deleteImage() {
    this.setData({ imageUrl: '' })
  },

  // 提交反馈
  async submit() {
    const { typeIndex, feedbackTypes, content, contact } = this.data
    
    // 验证必填项
    if (!content.trim()) {
      wx.showToast({ title: '请填写反馈内容', icon: 'none' })
      return
    }
    
    wx.showLoading({ title: '提交中...', mask: true })
    
    try {
      // TODO: 调用后端 API 提交反馈
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/feedback`,
      //   method: 'POST',
      //   data: {
      //     type: feedbackTypes[typeIndex],
      //     content,
      //     contact,
      //     image: this.data.imageUrl
      //   }
      // })
      
      // 模拟成功
      setTimeout(() => {
        wx.hideLoading()
        wx.showToast({ title: '提交成功', icon: 'success' })
        
        // 返回首页
        setTimeout(() => {
          wx.switchTab({ url: '/pages/index/index' })
        }, 1500)
      }, 1000)
      
    } catch (error) {
      wx.hideLoading()
      console.error('提交失败:', error)
      wx.showToast({ title: '提交失败', icon: 'none' })
    }
  }
})
