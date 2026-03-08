# HealthPal - 个人健康档案 AI 助手

一款基于 AI 技术的个人健康管理工具，帮助用户整合、分析和管理个人及家庭健康数据。

## 📁 项目结构

```
HealthPal/
├── src/
│   ├── mobile/      # 移动端 (iOS/Android)
│   └── backend/     # 后端服务 (Go)
├── docs/            # 文档
├── scripts/         # 脚本工具
├── config/          # 配置文件
└── tests/           # 测试用例
```

## 🚀 快速开始

### 环境要求

- Go 1.21+
- Node.js 18+
- Docker & Docker Compose
- MySQL 8.0+
- MongoDB 6+
- Redis 7+

### 启动开发环境

```bash
# 1. 启动数据库和中间件
cd config
docker-compose up -d mysql mongodb redis

# 2. 启动后端服务
cd ../src/backend
go run cmd/main.go

# 3. 移动端开发
# iOS: 打开 src/mobile/ios/HealthPal.xcodeproj
# Android: 打开 src/mobile/android 在 Android Studio
```

## 📋 开发文档

- [任务分解](docs/TASK_BREAKDOWN.md)
- [API 文档](docs/API.md)
- [数据库设计](docs/DB_DESIGN.md)

## 📄 许可证

内部项目，未经许可不得外传
