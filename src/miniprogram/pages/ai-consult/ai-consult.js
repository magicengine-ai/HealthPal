// pages/ai-consult/ai-consult.js
const app = getApp()

Page({
  data: {
    inputText: '',
    scrollToView: '',
    messages: [
      {
        id: 1,
        content: '您好，我是 HealthPal AI 健康助手。请问有什么健康问题需要咨询？',
        isAi: true,
        time: this.formatTime(new Date())
      }
    ],
    quickQuestions: [
      '血压偏高怎么办？',
      '血糖正常范围是多少？',
      '如何改善睡眠质量？',
      '每天应该运动多久？'
    ]
  },

  // 格式化时间
  formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  // 输入
  onInput(e) {
    this.setData({ inputText: e.detail.value })
  },

  // 发送消息
  async send() {
    const { inputText, messages } = this.data
    
    if (!inputText.trim()) return
    
    // 添加用户消息
    const userMsg = {
      id: messages.length + 1,
      content: inputText,
      isAi: false,
      time: this.formatTime(new Date())
    }
    
    messages.push(userMsg)
    this.setData({
      messages,
      inputText: '',
      scrollToView: `msg-${messages.length}`
    })
    
    // 显示正在输入
    wx.showLoading({ title: 'AI 思考中...', mask: true })
    
    try {
      // TODO: 调用后端 AI 接口
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/ai/consult`,
      //   method: 'POST',
      //   data: { question: inputText }
      // })
      
      // 模拟 AI 回复
      setTimeout(() => {
        wx.hideLoading()
        
        const aiMsg = {
          id: messages.length + 1,
          content: this.getMockResponse(inputText),
          isAi: true,
          time: this.formatTime(new Date())
        }
        
        messages.push(aiMsg)
        this.setData({
          messages,
          scrollToView: `msg-${messages.length}`
        })
      }, 1500)
      
    } catch (error) {
      wx.hideLoading()
      console.error('AI 咨询失败:', error)
      wx.showToast({ title: 'AI 回复失败', icon: 'none' })
    }
  },

  // 快捷问题
  askQuick(e) {
    const question = e.currentTarget.dataset.question
    this.setData({ inputText: question })
    this.send()
  },

  // 模拟 AI 回复
  getMockResponse(question) {
    const responses = {
      '血压': '血压偏高建议您：1. 低盐饮食，每日盐摄入量控制在 6g 以内；2. 规律运动，每周至少 150 分钟中等强度有氧运动；3. 保持健康体重；4. 戒烟限酒；5. 定期监测血压。如持续偏高，请及时就医。',
      '血糖': '正常空腹血糖范围为 3.9-6.1 mmol/L，餐后 2 小时血糖应小于 7.8 mmol/L。建议您定期监测，保持健康饮食和适量运动。',
      '睡眠': '改善睡眠质量建议：1. 保持规律作息，每天固定时间睡觉和起床；2. 睡前避免使用电子设备；3. 创造安静舒适的睡眠环境；4. 避免睡前摄入咖啡因；5. 适当运动但避免睡前剧烈运动。',
      '运动': '建议成年人每周进行至少 150 分钟中等强度有氧运动（如快走、游泳），或 75 分钟高强度运动， plus 每周 2 次力量训练。'
    }
    
    for (const [key, value] of Object.entries(responses)) {
      if (question.includes(key)) {
        return value
      }
    }
    
    return '感谢您的咨询。根据您的描述，建议您：1. 保持良好的生活习惯；2. 定期监测相关健康指标；3. 如有不适请及时就医。如需更详细的建议，请咨询专业医生。'
  }
})
