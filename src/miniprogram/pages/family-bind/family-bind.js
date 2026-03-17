// pages/family-bind/family-bind.js
Page({
  data: {
    searchText: '',
    searchResult: null
  },

  onSearchInput(e) {
    this.setData({ searchText: e.detail.value })
  },

  search() {
    if (!this.data.searchText.trim()) {
      wx.showToast({ title: '请输入搜索内容', icon: 'none' })
      return
    }
    
    // TODO: 调用后端 API 搜索用户
    // 模拟搜索结果
    this.setData({
      searchResult: {
        avatar: '/images/default-avatar.png',
        name: '张三',
        relation: '父亲'
      }
    })
  },

  confirmBind() {
    wx.showModal({
      title: '确认绑定',
      content: '确定要绑定该用户的健康档案吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '绑定成功', icon: 'success' })
          setTimeout(() => {
            wx.navigateBack()
          }, 1500)
        }
      }
    })
  }
})
