// pages/family-add/family-add.js
const app = getApp()

Page({
  data: {
    relations: ['本人', '父亲', '母亲', '配偶', '儿子', '女儿', '其他'],
    relationIndex: 0,
    name: '',
    gender: 'male',
    birthday: '',
    phone: '',
    note: ''
  },

  onLoad() {
    // 如果是从 profile 页面传来关系，预设
    const pages = getCurrentPages()
    if (pages.length > 1) {
      const prevPage = pages[pages.length - 2]
      if (prevPage.route === 'pages/profile/profile') {
        // 预设关系
      }
    }
  },

  // 关系选择
  onRelationChange(e) {
    this.setData({ relationIndex: parseInt(e.detail.value) })
  },

  // 姓名输入
  onNameInput(e) {
    this.setData({ name: e.detail.value })
  },

  // 性别选择
  onGenderChange(e) {
    this.setData({ gender: e.detail.value })
  },

  // 生日选择
  onBirthdayChange(e) {
    this.setData({ birthday: e.detail.value })
  },

  // 手机号输入
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value })
  },

  // 备注输入
  onNoteInput(e) {
    this.setData({ note: e.detail.value })
  },

  // 提交
  async submit() {
    const { name, relationIndex, relations, phone } = this.data
    
    // 验证必填项
    if (!name.trim()) {
      wx.showToast({ title: '请输入姓名', icon: 'none' })
      return
    }
    
    // 验证手机号
    if (phone && !/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({ title: '手机号格式不正确', icon: 'none' })
      return
    }
    
    wx.showLoading({ title: '创建中...', mask: true })
    
    try {
      // TODO: 调用后端 API 创建家庭成员
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/family`,
      //   method: 'POST',
      //   data: {
      //     name,
      //     relation: relations[relationIndex],
      //     gender: this.data.gender,
      //     birthday: this.data.birthday,
      //     phone,
      //     note: this.data.note
      //   },
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      
      // 模拟成功
      setTimeout(() => {
        wx.hideLoading()
        wx.showToast({ title: '创建成功', icon: 'success' })
        
        // 返回上一页
        setTimeout(() => {
          wx.navigateBack()
        }, 1500)
      }, 1000)
      
    } catch (error) {
      wx.hideLoading()
      console.error('创建失败:', error)
      wx.showToast({ title: '创建失败', icon: 'none' })
    }
  }
})
