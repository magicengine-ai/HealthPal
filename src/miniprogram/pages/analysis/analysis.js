// pages/analysis/analysis.js
const app = getApp()

Page({
  data: {
    currentIndicator: 'blood-pressure',
    indicatorName: '血压',
    timeRange: 'month',
    stats: {
      average: '120',
      max: '135',
      min: '115'
    },
    suggestions: [
      {
        id: 1,
        icon: '🥗',
        title: '饮食建议',
        description: '保持低盐饮食，每日盐摄入量控制在 6g 以内，多吃蔬菜水果。'
      },
      {
        id: 2,
        icon: '🏃',
        title: '运动建议',
        description: '每周进行至少 150 分钟中等强度有氧运动，如快走、游泳。'
      },
      {
        id: 3,
        icon: '😴',
        title: '作息建议',
        description: '保证每天 7-8 小时睡眠，避免熬夜，保持规律作息。'
      }
    ],
    warnings: [
      '最近一次测量值偏高，建议密切关注',
      '连续 3 天超过正常范围，建议咨询医生'
    ],
    chartData: []
  },

  onLoad(options) {
    if (options.type) {
      this.setData({
        currentIndicator: options.type,
        indicatorName: this.getIndicatorName(options.type)
      })
    }
    
    this.loadData()
  },

  // 获取指标中文名称
  getIndicatorName(type) {
    const names = {
      'blood-pressure': '血压',
      'blood-sugar': '血糖',
      'weight': '体重',
      'heart-rate': '心率',
      'temperature': '体温'
    }
    return names[type] || '指标'
  },

  // 加载数据
  async loadData() {
    try {
      // TODO: 从后端 API 加载数据
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/health/trend`,
      //   data: {
      //     type: this.data.currentIndicator,
      //     range: this.data.timeRange
      //   }
      // })
      // this.setData({ chartData: res.data })
      
      // 模拟数据
      this.generateMockData()
      this.drawChart()
    } catch (error) {
      console.error('加载数据失败:', error)
    }
  },

  // 生成模拟数据
  generateMockData() {
    const mockData = {
      'blood-pressure': [
        { date: '11-01', value: 118 },
        { date: '11-15', value: 122 },
        { date: '12-01', value: 120 },
        { date: '12-15', value: 125 },
        { date: '01-01', value: 123 },
        { date: '01-15', value: 120 },
        { date: '02-01', value: 119 },
        { date: '02-15', value: 121 },
        { date: '03-01', value: 120 }
      ],
      'blood-sugar': [
        { date: '11-01', value: 5.4 },
        { date: '11-15', value: 5.6 },
        { date: '12-01', value: 5.5 },
        { date: '12-15', value: 5.8 },
        { date: '01-01', value: 5.7 },
        { date: '01-15', value: 5.6 },
        { date: '02-01', value: 5.5 },
        { date: '02-15', value: 5.6 },
        { date: '03-01', value: 5.6 }
      ],
      'weight': [
        { date: '11-01', value: 66 },
        { date: '11-15', value: 65.5 },
        { date: '12-01', value: 65.2 },
        { date: '12-15', value: 65 },
        { date: '01-01', value: 64.8 },
        { date: '01-15', value: 65 },
        { date: '02-01', value: 64.5 },
        { date: '02-15', value: 65 },
        { date: '03-01', value: 65 }
      ]
    }
    
    this.setData({
      chartData: mockData[this.data.currentIndicator] || []
    })
  },

  // 切换指标
  switchIndicator(e) {
    const type = e.currentTarget.dataset.type
    this.setData({
      currentIndicator: type,
      indicatorName: this.getIndicatorName(type)
    })
    this.loadData()
  },

  // 切换时间范围
  switchTimeRange(e) {
    const range = e.currentTarget.dataset.range
    this.setData({
      timeRange: range
    })
    this.loadData()
  },

  // 绘制图表
  drawChart() {
    const query = wx.createSelectorQuery()
    query.select('#trendChart')
      .fields({ node: true, size: true })
      .exec((res) => {
        if (!res[0]) {
          console.error('未找到 canvas 节点')
          return
        }
        
        const canvas = res[0].node
        const ctx = canvas.getContext('2d')
        const dpr = wx.getSystemInfoSync().pixelRatio
        
        // 设置 canvas 尺寸
        canvas.width = res[0].width * dpr
        canvas.height = res[0].height * dpr
        ctx.scale(dpr, dpr)
        
        const data = this.data.chartData
        const width = res[0].width
        const height = res[0].height
        const padding = { top: 20, right: 20, bottom: 40, left: 50 }
        
        // 清空画布
        ctx.clearRect(0, 0, width, height)
        
        if (data.length === 0) return
        
        // 计算数据范围
        const values = data.map(item => item.value)
        const maxValue = Math.max(...values)
        const minValue = Math.min(...values)
        const valueRange = maxValue - minValue || 1
        
        // 绘制网格线
        ctx.strokeStyle = '#E8E8E8'
        ctx.lineWidth = 1
        for (let i = 0; i <= 4; i++) {
          const y = padding.top + (height - padding.top - padding.bottom) * i / 4
          ctx.beginPath()
          ctx.moveTo(padding.left, y)
          ctx.lineTo(width - padding.right, y)
          ctx.stroke()
        }
        
        // 绘制折线
        ctx.strokeStyle = '#1890FF'
        ctx.lineWidth = 3
        ctx.lineJoin = 'round'
        ctx.beginPath()
        
        const chartWidth = width - padding.left - padding.right
        const chartHeight = height - padding.top - padding.bottom
        
        data.forEach((item, index) => {
          const x = padding.left + chartWidth * index / (data.length - 1)
          const y = padding.top + chartHeight * (1 - (item.value - minValue) / valueRange)
          
          if (index === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        })
        ctx.stroke()
        
        // 绘制数据点
        data.forEach((item, index) => {
          const x = padding.left + chartWidth * index / (data.length - 1)
          const y = padding.top + chartHeight * (1 - (item.value - minValue) / valueRange)
          
          // 绘制圆点
          ctx.fillStyle = '#1890FF'
          ctx.beginPath()
          ctx.arc(x, y, 6, 0, Math.PI * 2)
          ctx.fill()
          
          // 绘制数值标签
          ctx.fillStyle = '#666666'
          ctx.font = '12px sans-serif'
          ctx.textAlign = 'center'
          ctx.fillText(item.value.toString(), x, y - 12)
          
          // 绘制日期标签
          ctx.fillStyle = '#999999'
          ctx.font = '11px sans-serif'
          ctx.fillText(item.date, x, height - padding.bottom + 20)
        })
      })
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadData().then(() => {
      wx.stopPullDownRefresh()
    })
  }
})
