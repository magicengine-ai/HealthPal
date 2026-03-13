# HealthPal 微信小程序

HealthPal 个人健康档案 AI 助手的微信小程序版本。

## 📁 项目结构

```
miniprogram/
├── app.js                 # 小程序入口
├── app.json              # 小程序配置
├── app.wxss              # 全局样式
├── project.config.json   # 项目配置
├── sitemap.json          # 搜索配置
├── pages/                # 页面目录
│   ├── index/           # 首页
│   ├── records/         # 档案列表
│   ├── record-detail/   # 档案详情
│   ├── analysis/        # 健康分析
│   └── profile/         # 个人中心
├── components/           # 自定义组件
│   ├── record-card/     # 档案卡片
│   ├── indicator-card/  # 指标卡片
│   └── reminder-item/   # 提醒项
├── services/             # API 服务
│   └── api.js           # API 封装
├── utils/                # 工具函数
│   └── util.js          # 通用工具
└── images/               # 图片资源
```

## 🚀 快速开始

### 1. 环境准备

- 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- 注册微信小程序账号，获取 AppID

### 2. 导入项目

1. 打开微信开发者工具
2. 选择「导入项目」
3. 选择项目目录：`HealthPal/src/miniprogram`
4. 填入你的 AppID
5. 点击「导入」

### 3. 配置开发

在 `project.config.json` 中修改：

```json
{
  "appid": "你的小程序 AppID"
}
```

### 4. 配置后端 API

在 `services/api.js` 中修改 API 基础 URL：

```javascript
const API_BASE_URL = 'http://your-server:8000/api'
```

### 5. 运行项目

- 点击微信开发者工具的「编译」按钮
- 在真机调试中扫码测试

## 📋 核心功能

### 首页 (index)
- 健康评分展示
- 最近指标概览
- 今日提醒列表
- 快捷操作入口

### 档案管理 (records)
- 档案列表展示
- 分类筛选
- 搜索功能
- 图片上传 + OCR 识别

### 档案详情 (record-detail)
- 指标详细数据
- AI 报告解读
- 原始报告查看
- 导出分享功能

### 健康分析 (analysis)
- 指标趋势图表
- 健康建议
- 异常提醒

### 个人中心 (profile)
- 用户信息管理
- 家庭成员切换
- 功能菜单
- 设置与反馈

## 🎨 UI 设计规范

### 主题色
- 主色：`#1890FF` (健康蓝)
- 辅助色：`#52C41A` (生命绿)
- 警告色：`#FA8C16`
- 错误色：`#F5222D`

### 字体大小
- 小字：`24rpx`
- 正文：`28rpx`
- 标题：`30-36rpx`

### 圆角规范
- 卡片：`12rpx`
- 按钮：`44rpx` (胶囊形)
- 小标签：`20rpx`

## 🔌 API 接口

需要后端提供的 API 接口：

### 健康档案
- `GET /api/records` - 获取档案列表
- `GET /api/records/:id` - 获取档案详情
- `POST /api/records/upload` - 上传档案
- `DELETE /api/records/:id` - 删除档案

### 健康指标
- `GET /api/indicators` - 获取指标列表
- `POST /api/indicators` - 添加指标
- `GET /api/indicators/trend` - 获取趋势数据

### 提醒
- `GET /api/reminders` - 获取提醒列表
- `POST /api/reminders` - 添加提醒
- `PUT /api/reminders/:id` - 更新提醒
- `DELETE /api/reminders/:id` - 删除提醒

### AI 问诊
- `POST /api/ai/consult` - 健康咨询
- `POST /api/ai/analyze-report` - 报告解读

## 📝 开发注意事项

### 1. 图片上传
```javascript
wx.chooseMedia({
  count: 9,
  mediaType: ['image'],
  sourceType: ['album', 'camera'],
  success: (res) => {
    // 处理选择的图片
  }
})
```

### 2. 图表绘制
使用原生 canvas 2D API 绘制趋势图，参考 `pages/analysis/analysis.js`

### 3. 本地存储
```javascript
// 存储
wx.setStorageSync('key', value)

// 读取
const value = wx.getStorageSync('key')

// 清除
wx.clearStorageSync()
```

### 4. 授权登录
```javascript
wx.login({
  success: (res) => {
    // 获取 code，发送到后端换取 token
  }
})
```

## 🔧 常用命令

### 预览
- 微信开发者工具 → 预览 → 扫码

### 上传代码
- 微信开发者工具 → 上传 → 填写版本号和描述

### 版本管理
- 登录 [微信公众平台](https://mp.weixin.qq.com)
- 版本管理 → 审核 → 发布

## 📱 真机调试

1. 点击微信开发者工具的「真机调试」
2. 选择「真机调试模式」
3. 使用微信扫码
4. 在真机上测试功能

## 🐛 常见问题

### 1. 请求失败
- 检查 API URL 是否正确
- 检查域名是否在后台配置
- 检查 HTTPS 证书

### 2. 图片无法上传
- 检查图片大小限制（通常 10MB）
- 检查网络权限
- 检查后端接收接口

### 3. Canvas 不显示
- 确保使用 `type="2d"`
- 设置正确的宽高
- 处理 DPI 缩放

## 📄 许可证

内部项目，未经许可不得外传

---

**开发团队：** HealthPal Team  
**最后更新：** 2026-03-14
