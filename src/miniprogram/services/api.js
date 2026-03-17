// services/api.js
const app = getApp()

// API 基础配置
// WSL2 环境：
// - 模拟器调试：使用 localhost
// - 真机调试：使用 Windows 主机 IP（需要配置端口转发和防火墙）
const API_BASE_URL = 'http://localhost:8000/api'  // 模拟器用
// const API_BASE_URL = 'http://192.168.8.250:8000/api'  // 真机用（Windows IP）
const TIMEOUT = 10000

/**
 * 封装请求方法
 */
function request(options) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token')
    
    wx.request({
      url: `${API_BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        ...options.header
      },
      timeout: TIMEOUT,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，跳转到登录页
          wx.removeStorageSync('token')
          wx.reLaunch({
            url: '/pages/login/login'
          })
          reject(new Error('未授权'))
        } else if (res.statusCode === 403) {
          reject(new Error('无权限访问'))
        } else {
          reject(new Error(res.data.message || '请求失败'))
        }
      },
      fail: (err) => {
        console.error('请求失败:', err)
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * 上传文件
 */
function uploadFile(options) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token')
    
    wx.uploadFile({
      url: `${API_BASE_URL}${options.url}`,
      filePath: options.filePath,
      name: options.name || 'file',
      formData: options.formData || {},
      header: {
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        const data = JSON.parse(res.data)
        if (res.statusCode === 200) {
          resolve(data)
        } else {
          reject(new Error(data.message || '上传失败'))
        }
      },
      fail: (err) => {
        console.error('上传失败:', err)
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

// 健康档案相关 API
export const recordsAPI = {
  // 获取档案列表
  getList: (params) => request({
    url: '/records',
    method: 'GET',
    data: params
  }),
  
  // 获取档案详情
  getDetail: (id) => request({
    url: `/records/${id}`,
    method: 'GET'
  }),
  
  // 上传档案
  upload: (filePath, formData) => uploadFile({
    url: '/records/upload',
    filePath,
    formData
  }),
  
  // 删除档案
  delete: (id) => request({
    url: `/records/${id}`,
    method: 'DELETE'
  }),
  
  // 获取 OCR 状态
  getOcrStatus: (id) => request({
    url: `/records/${id}/ocr-status`,
    method: 'GET'
  })
}

// 健康指标相关 API
export const indicatorsAPI = {
  // 获取指标列表
  getList: (params) => request({
    url: '/indicators',
    method: 'GET',
    data: params
  }),
  
  // 添加指标
  add: (data) => request({
    url: '/indicators',
    method: 'POST',
    data
  }),
  
  // 获取指标趋势
  getTrend: (type, range) => request({
    url: '/indicators/trend',
    method: 'GET',
    data: { type, range }
  })
}

// 提醒相关 API
export const remindersAPI = {
  // 获取提醒列表
  getList: (params) => request({
    url: '/reminders',
    method: 'GET',
    data: params
  }),
  
  // 添加提醒
  add: (data) => request({
    url: '/reminders',
    method: 'POST',
    data
  }),
  
  // 更新提醒
  update: (id, data) => request({
    url: `/reminders/${id}`,
    method: 'PUT',
    data
  }),
  
  // 删除提醒
  delete: (id) => request({
    url: `/reminders/${id}`,
    method: 'DELETE'
  })
}

// 用户相关 API
export const userAPI = {
  // 获取用户信息
  getInfo: () => request({
    url: '/user/info',
    method: 'GET'
  }),
  
  // 更新用户信息
  updateInfo: (data) => request({
    url: '/user/info',
    method: 'PUT',
    data
  }),
  
  // 获取统计数据
  getStats: () => request({
    url: '/user/stats',
    method: 'GET'
  })
}

// AI 问诊相关 API
export const aiAPI = {
  // 健康咨询
  consult: (question, context) => request({
    url: '/ai/consult',
    method: 'POST',
    data: { question, context }
  }),
  
  // 报告解读
  analyzeReport: (recordId) => request({
    url: '/ai/analyze-report',
    method: 'POST',
    data: { recordId }
  })
}

export default {
  request,
  uploadFile,
  recordsAPI,
  indicatorsAPI,
  remindersAPI,
  userAPI,
  aiAPI
}
