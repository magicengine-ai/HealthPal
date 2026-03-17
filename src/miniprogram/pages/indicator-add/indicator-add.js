// pages/indicator-add/indicator-add.js
const app = getApp()

Page({
  data: {
    indicatorTypes: ['血压', '血糖', '体重', '心率', '体温'],
    typeIndex: 0,
    showSystolic: false,
    showValue: true,
    unit: '',
    systolic: '',
    diastolic: '',
    value: '',
    measureTime: '',
    note: ''
  },

  onLoad(options) {
    // 如果从首页传来类型，预设
    if (options.type) {
      const typeMap = { '血压': 0, '血糖': 1, '体重': 2, '心率': 3, '体温': 4 }
      const index = typeMap[options.type]
      if (index !== undefined) {
        this.setData({ typeIndex: index })
        this.updateUnit(index)
      }
    }
    
    // 设置默认时间为当前时间
    const now = new Date()
    const time = `${now.getFullYear()}-${(now.getMonth()+1).toString().padStart(2,'0')}-${now.getDate().toString().padStart(2,'0')} ${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`
    this.setData({ measureTime: time })
  },

  // 更新单位和显示
  updateUnit(index) {
    const units = ['', '', 'kg', 'bpm', '°C']
    const showSystolic = index === 0
    const showValue = index !== 0
    this.setData({
      unit: units[index],
      showSystolic,
      showValue
    })
  },

  // 类型选择
  onTypeChange(e) {
    const index = parseInt(e.detail.value)
    this.setData({ typeIndex: index })
    this.updateUnit(index)
  },

  // 收缩压输入
  onSystolicInput(e) {
    this.setData({ systolic: e.detail.value })
  },

  // 舒张压输入
  onDiastolicInput(e) {
    this.setData({ diastolic: e.detail.value })
  },

  // 数值输入
  onValueInput(e) {
    this.setData({ value: e.detail.value })
  },

  // 时间选择
  onTimeChange(e) {
    this.setData({ measureTime: e.detail.value })
  },

  // 备注输入
  onNoteInput(e) {
    this.setData({ note: e.detail.value })
  },

  // 提交
  async submit() {
    const { typeIndex, indicatorTypes, systolic, diastolic, value, measureTime } = this.data
    
    // 验证必填项
    if (this.data.showSystolic) {
      if (!systolic || !diastolic) {
        wx.showToast({ title: '请填写血压值', icon: 'none' })
        return
      }
    } else if (!value) {
      wx.showToast({ title: '请填写测量值', icon: 'none' })
      return
    }
    
    if (!measureTime) {
      wx.showToast({ title: '请选择测量时间', icon: 'none' })
      return
    }
    
    wx.showLoading({ title: '保存中...', mask: true })
    
    try {
      // 构建数据
      const indicatorData = {
        type: indicatorTypes[typeIndex],
        measureTime,
        note: this.data.note
      }
      
      if (this.data.showSystolic) {
        indicatorData.systolic = parseInt(systolic)
        indicatorData.diastolic = parseInt(diastolic)
      } else {
        indicatorData.value = parseFloat(value)
      }
      
      // TODO: 调用后端 API 保存
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/indicators`,
      //   method: 'POST',
      //   data: indicatorData
      // })
      
      // 模拟保存成功
      setTimeout(() => {
        wx.hideLoading()
        wx.showToast({ title: '保存成功', icon: 'success' })
        
        // 返回首页或上一页
        setTimeout(() => {
          wx.navigateBack()
        }, 1500)
      }, 1000)
      
    } catch (error) {
      wx.hideLoading()
      console.error('保存失败:', error)
      wx.showToast({ title: '保存失败', icon: 'none' })
    }
  }
})
