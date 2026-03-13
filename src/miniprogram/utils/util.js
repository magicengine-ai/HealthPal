// utils/util.js

/**
 * 格式化日期
 */
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化相对时间
 */
function formatRelativeTime(date) {
  const now = new Date()
  const diff = now - new Date(date)
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const months = Math.floor(days / 30)
  const years = Math.floor(months / 12)
  
  if (years > 0) return `${years}年前`
  if (months > 0) return `${months}个月前`
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

/**
 * 格式化数字（添加千分位）
 */
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化健康指标值
 */
function formatIndicatorValue(value, unit) {
  if (value === null || value === undefined) return '-'
  return `${value} ${unit}`
}

/**
 * 判断指标状态
 */
function getIndicatorStatus(value, min, max) {
  if (value < min) return { status: 'warning', text: '偏低' }
  if (value > max) return { status: 'warning', text: '偏高' }
  return { status: 'normal', text: '正常' }
}

/**
 * 计算健康评分
 */
function calculateHealthScore(indicators) {
  let score = 100
  let count = 0
  
  for (const indicator of indicators) {
    if (indicator.status === 'warning') {
      score -= 10
    } else if (indicator.status === 'error') {
      score -= 20
    }
    count++
  }
  
  return Math.max(0, Math.min(100, score))
}

/**
 * 防抖函数
 */
function debounce(fn, delay = 300) {
  let timer = null
  return function(...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 */
function throttle(fn, delay = 300) {
  let lastTime = 0
  return function(...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      fn.apply(this, args)
      lastTime = now
    }
  }
}

/**
 * 深拷贝
 */
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  
  const cloned = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloned[key] = deepClone(obj[key])
    }
  }
  return cloned
}

/**
 * 验证手机号
 */
function validatePhone(phone) {
  return /^1[3-9]\d{9}$/.test(phone)
}

/**
 * 验证身份证号
 */
function validateIdCard(idCard) {
  return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(idCard)
}

/**
 * 获取系统信息
 */
function getSystemInfo() {
  return wx.getSystemInfoSync()
}

/**
 * 检查更新
 */
function checkUpdate() {
  if (wx.canIUse('getUpdateManager')) {
    const updateManager = wx.getUpdateManager()
    
    updateManager.onCheckForUpdate((res) => {
      if (res.hasUpdate) {
        updateManager.onUpdateReady(() => {
          wx.showModal({
            title: '更新提示',
            content: '新版本已经准备好，是否重启应用？',
            success: (res) => {
              if (res.confirm) {
                updateManager.applyUpdate()
              }
            }
          })
        })
      }
    })
  }
}

module.exports = {
  formatDate,
  formatRelativeTime,
  formatNumber,
  formatIndicatorValue,
  getIndicatorStatus,
  calculateHealthScore,
  debounce,
  throttle,
  deepClone,
  validatePhone,
  validateIdCard,
  getSystemInfo,
  checkUpdate
}
