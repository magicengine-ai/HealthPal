// pages/login/login.js
const app = getApp()

Page({
  data: {
    phone: '',
    code: '',
    countdown: 0,
    agreed: false,
    canLogin: false
  },

  onLoad() {
    // 检查是否已登录
    const token = wx.getStorageSync('token')
    if (token) {
      wx.reLaunch({ url: '/pages/index/index' })
    }
  },

  // 手机号输入
  onPhoneInput(e) {
    const phone = e.detail.value
    this.setData({ phone })
    this.checkCanLogin()
  },

  // 验证码输入
  onCodeInput(e) {
    const code = e.detail.value
    this.setData({ code })
    this.checkCanLogin()
  },

  // 检查是否可以登录
  checkCanLogin() {
    const { phone, code, agreed } = this.data
    const canLogin = /^1[3-9]\d{9}$/.test(phone) && /^\d{6}$/.test(code) && agreed
    this.setData({ canLogin })
  },

  // 同意协议
  onAgreeChange(e) {
    const agreed = e.detail.value.includes('agree')
    this.setData({ agreed })
    this.checkCanLogin()
  },

  // 发送验证码
  async sendCode() {
    const { phone } = this.data
    
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' })
      return
    }
    
    // 开始倒计时
    this.setData({ countdown: 60 })
    const timer = setInterval(() => {
      let countdown = this.data.countdown - 1
      this.setData({ countdown })
      
      if (countdown <= 0) {
        clearInterval(timer)
      }
    }, 1000)
    
    // TODO: 调用后端发送验证码 API
    // await wx.request({
    //   url: `${app.globalData.apiBaseUrl}/api/auth/send-code`,
    //   method: 'POST',
    //   data: { phone }
    // })
    
    wx.showToast({ title: '验证码已发送', icon: 'success' })
    
    // 模拟自动填充验证码（开发用）
    setTimeout(() => {
      this.setData({ code: '123456' })
      this.checkCanLogin()
    }, 1000)
  },

  // 登录
  async login() {
    const { phone, code } = this.data
    
    if (!this.data.canLogin) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' })
      return
    }
    
    wx.showLoading({ title: '登录中...', mask: true })
    
    try {
      // TODO: 调用后端登录 API
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/auth/login`,
      //   method: 'POST',
      //   data: { phone, code }
      // })
      
      // 模拟登录成功
      setTimeout(() => {
        wx.hideLoading()
        
        // 保存 token 和用户信息
        wx.setStorageSync('token', 'mock_token_' + Date.now())
        wx.setStorageSync('userInfo', {
          avatarUrl: '/images/default-avatar.png',
          nickName: '微信用户',
          userId: 'HP' + Date.now().toString().substr(-6)
        })
        
        wx.showToast({ title: '登录成功', icon: 'success' })
        
        setTimeout(() => {
          wx.reLaunch({ url: '/pages/index/index' })
        }, 1500)
      }, 1000)
      
    } catch (error) {
      wx.hideLoading()
      console.error('登录失败:', error)
      wx.showToast({ title: '登录失败', icon: 'none' })
    }
  },

  // 查看协议
  viewAgreement(e) {
    const type = e.currentTarget.dataset.type
    wx.navigateTo({
      url: `/pages/webview/webview?type=${type}`
    })
  }
})
