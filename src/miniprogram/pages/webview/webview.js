// pages/webview/webview.js
Page({
  data: {
    url: ''
  },

  onLoad(options) {
    // 根据类型加载不同 URL
    if (options.url) {
      this.setData({ url: options.url })
    } else if (options.type) {
      const urls = {
        privacy: 'https://www.healthpal.com/privacy',
        terms: 'https://www.healthpal.com/terms'
      }
      this.setData({ url: urls[options.type] || '' })
    }
  }
})
