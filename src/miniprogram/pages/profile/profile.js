// pages/profile/profile.js
const app = getApp()

Page({
  data: {
    userInfo: {
      avatarUrl: '/images/default-avatar.png',
      nickName: '微信用户',
      userId: 'HP123456'
    },
    stats: {
      recordCount: 15,
      followDays: 128,
      healthScore: 85
    },
    familyMembers: [
      {
        id: 1,
        name: '张三',
        relation: '本人',
        avatar: '/images/default-avatar.png',
        isCurrent: true
      },
      {
        id: 2,
        name: '李四',
        relation: '父亲',
        avatar: '/images/default-avatar.png',
        isCurrent: false
      },
      {
        id: 3,
        name: '王五',
        relation: '母亲',
        avatar: '/images/default-avatar.png',
        isCurrent: false
      }
    ]
  },

  onLoad() {
    this.loadUserInfo()
  },

  onShow() {
    // 每次页面显示时刷新数据
    this.loadUserInfo()
  },

  // 加载用户信息
  async loadUserInfo() {
    try {
      // 获取微信用户信息
      const userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        this.setData({ userInfo })
      } else {
        // 未登录，跳转到登录页
        wx.redirectTo({
          url: '/pages/login/login'
        })
      }
      
      // TODO: 从后端加载统计数据
      // const res = await wx.request({
      //   url: `${app.globalData.apiBaseUrl}/api/user/stats`,
      //   header: {
      //     'Authorization': `Bearer ${wx.getStorageSync('token')}`
      //   }
      // })
      // this.setData({ stats: res.data.stats })
    } catch (error) {
      console.error('加载用户信息失败:', error)
    }
  },

  // 添加家庭成员
  addFamilyMember() {
    wx.showActionSheet({
      itemList: ['创建新档案', '绑定已有档案'],
      success: (res) => {
        if (res.tapIndex === 0) {
          wx.navigateTo({
            url: '/pages/family-add/family-add'
          })
        } else {
          wx.navigateTo({
            url: '/pages/family-bind/family-bind'
          })
        }
      }
    })
  },

  // 切换家庭成员
  switchFamily(e) {
    const id = e.currentTarget.dataset.id
    const members = this.data.familyMembers
    
    members.forEach(member => {
      member.isCurrent = member.id === id
    })
    
    this.setData({ familyMembers: members })
    
    // TODO: 切换到对应家庭成员的数据
    wx.showToast({
      title: '已切换',
      icon: 'success'
    })
  },

  // 菜单导航
  navigateTo(e) {
    const page = e.currentTarget.dataset.page
    const pages = {
      'reminders': '/pages/reminders/reminders',
      'devices': '/pages/devices/devices',
      'ai-consult': '/pages/ai-consult/ai-consult',
      'settings': '/pages/settings/settings',
      'about': '/pages/about/about',
      'feedback': '/pages/feedback/feedback'
    }
    
    const url = pages[page]
    if (url) {
      wx.navigateTo({ url })
    } else {
      wx.showToast({
        title: '功能开发中',
        icon: 'none'
      })
    }
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除本地存储
          wx.clearStorageSync()
          
          // 跳转到登录页
          wx.redirectTo({
            url: '/pages/login/login'
          })
        }
      }
    })
  }
})
