// app.js
App({
  onLaunch() {
    // 小程序启动时执行
    console.log('HealthPal 小程序启动');
    
    // 检查登录状态
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
      this.globalData.isLoggedIn = true;
    }
    
    // 初始化 API 基础 URL
    this.globalData.apiBaseUrl = wx.getStorageSync('apiBaseUrl') || 'http://localhost:8000';
  },
  
  globalData: {
    userInfo: null,
    isLoggedIn: false,
    apiBaseUrl: 'http://localhost:8000',
    healthScore: 0,
    reminders: []
  }
})
