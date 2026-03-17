// pages/about/about.js
Page({
  // 复制邮箱
  copyEmail() {
    wx.setClipboardData({
      data: 'support@healthpal.com',
      success: () => {
        wx.showToast({ title: '已复制', icon: 'success' })
      }
    })
  },

  // 访问网站
  visitWebsite() {
    wx.navigateTo({
      url: '/pages/webview/webview?url=https://www.healthpal.com'
    })
  },

  // 查看协议
  viewAgreement(e) {
    const type = e.currentTarget.dataset.type
    const titles = {
      privacy: '隐私政策',
      terms: '用户协议'
    }
    const contents = {
      privacy: `
隐私政策

1. 信息收集
我们收集您的健康数据、使用记录等信息，用于提供个性化服务。

2. 信息使用
您的数据仅用于为您提供健康分析和建议，不会用于其他用途。

3. 信息共享
我们不会向第三方共享您的个人健康数据，除非获得您的明确授权。

4. 信息安全
我们采取严格的技术措施保护您的数据安全。

5. 您的权利
您可以随时查看、修改、删除您的数据。
      `,
      terms: `
用户协议

1. 服务内容
HealthPal 提供健康档案管理、数据分析等服务。

2. 用户义务
您应提供真实、准确的健康信息。

3. 免责声明
本应用提供的健康建议仅供参考，不能替代专业医疗诊断。

4. 知识产权
本应用的所有内容归 HealthPal Team 所有。

5. 协议修改
我们保留随时修改本协议的权利。
      `
    }

    wx.showModal({
      title: titles[type],
      content: contents[type],
      showCancel: false,
      confirmText: '我知道了',
      scrollable: true
    })
  }
})
