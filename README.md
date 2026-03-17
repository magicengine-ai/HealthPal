# HealthPal - 个人健康档案 AI 助手

一款基于 AI 技术的个人健康管理工具，帮助用户整合、分析和管理个人及家庭健康数据。

> **项目状态**: 🟢 开发中  
> **最后更新**: 2026-03-17

## ✨ 核心功能

- 📄 **健康档案数字化** - 拍照上传体检报告，AI 自动 OCR 识别
- 📊 **健康指标追踪** - 血压、血糖、体重等指标趋势分析
- 🤖 **AI 健康咨询** - 7×24 小时在线健康问答
- 👨‍👩‍👧 **家庭健康管理** - 多成员档案，全家健康一手掌握
- ⏰ **智能提醒** - 用药提醒、测量提醒、复诊提醒
- 📱 **多端同步** - 微信小程序 + Flutter App + Web 端

## 📁 项目结构

```
HealthPal/
├── config/                    # Docker 配置
│   ├── docker-compose.yml     # 完整服务栈
│   └── docker-compose-simple.yml  # 简化版
├── docs/                      # 项目文档
│   ├── API.md                 # API 接口文档
│   ├── DB_DESIGN.md           # 数据库设计
│   ├── BACKEND_FRAMEWORK.md   # 后端技术架构
│   ├── CELERY_GUIDE.md        # Celery 异步任务指南
│   └── FLUTTER_DEV_GUIDE.md   # Flutter 开发指南
├── src/
│   ├── backend/               # Python FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/           # API 路由
│   │   │   ├── core/          # 核心配置
│   │   │   ├── db/            # 数据库
│   │   │   ├── models/        # 数据模型
│   │   │   ├── schemas/       # Pydantic 模型
│   │   │   ├── services/      # 业务逻辑
│   │   │   └── tasks/         # Celery 任务
│   │   ├── tests/             # 单元测试
│   │   └── requirements.txt   # Python 依赖
│   ├── miniprogram/           # 微信小程序
│   │   ├── pages/             # 页面
│   │   ├── components/        # 组件
│   │   ├── services/          # API 服务
│   │   └── utils/             # 工具函数
│   └── mobile/                # Flutter 移动端
│       ├── lib/
│       │   ├── screens/       # 页面
│       │   ├── widgets/       # 组件
│       │   ├── providers/     # 状态管理
│       │   └── api/           # API 接口
│       └── pubspec.yaml       # Flutter 依赖
└── tests/                     # 集成测试
```

## 🚀 快速开始

### 环境要求

- **Python 3.11+**
- **Node.js 18+** (小程序开发)
- **Flutter 3.x** (移动端开发)
- **Docker & Docker Compose**
- **微信开发者工具** (小程序开发)

### 方式一：Docker 一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/magicengine-ai/HealthPal.git
cd HealthPal

# 启动所有服务（包括 Celery 异步任务）
cd config
docker-compose up -d

# 查看服务状态
docker-compose ps
```

**访问服务：**
- 📡 API 文档：http://localhost:8000/docs
- 🌸 Celery 监控：http://localhost:5555
- 🗄️ MySQL: localhost:3306
- 📦 MongoDB: localhost:27017
- 🔴 Redis: localhost:6379

### 方式二：本地开发模式

#### 1. 启动基础服务

```bash
cd config
docker-compose up -d mysql mongodb redis
```

#### 2. 启动后端服务

```bash
cd src/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动 FastAPI（支持热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 启动 Celery Worker（异步任务）

```bash
# 终端 2: Celery Worker
celery -A app.core.celery_config.celery_app worker -l info -c 4

# 终端 3: Celery Beat（定时任务）
celery -A app.core.celery_config.celery_app beat -l info

# 终端 4: Flower 监控（可选）
celery -A app.core.celery_config.celery_app flower --port=5555
```

#### 4. 启动微信小程序

1. 打开 **微信开发者工具**
2. 导入项目：`HealthPal/src/miniprogram`
3. 配置 AppID（或使用测试号）
4. 编译运行

#### 5. 启动 Flutter App

```bash
cd src/mobile

# 获取依赖
flutter pub get

# 运行（连接设备或模拟器）
flutter run
```

## 📱 功能模块

### 微信小程序（已完成）

| 页面 | 功能 | 状态 |
|------|------|------|
| 首页 | 健康概览、快捷操作、今日提醒 | ✅ |
| 档案 | 档案列表、上传报告、OCR 识别 | ✅ |
| 档案详情 | 指标详情、AI 解读、原始报告 | ✅ |
| 分析 | 指标趋势图、健康建议 | ✅ |
| 我的 | 用户信息、家庭成员管理 | ✅ |
| 设置 | 通知、隐私、通用设置 | ✅ |
| AI 问诊 | 智能健康咨询 | ✅ |
| 提醒管理 | 用药/测量提醒 | ✅ |
| 智能设备 | 设备绑定与管理 | ✅ |
| 指标录入 | 血压/血糖/体重等 | ✅ |

### 后端 API（已完成）

- ✅ 用户认证（手机号验证码登录）
- ✅ 健康档案管理（CRUD）
- ✅ OCR 识别任务（Celery 异步）
- ✅ 健康指标管理
- ✅ 提醒管理
- ✅ AI 健康咨询
- ✅ 家庭成员管理

### Flutter App（开发中）

- ✅ 基础框架搭建
- ✅ 路由配置
- ✅ 状态管理（Provider）
- 🔄 页面开发中

## 🔧 技术架构

### 后端技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| Web 框架 | FastAPI | 0.109+ |
| ORM | SQLAlchemy | 2.0+ |
| 异步任务 | Celery | 5.3+ |
| 消息队列 | Redis | 7 |
| 关系数据库 | MySQL | 8.0 |
| 文档数据库 | MongoDB | 6 |
| 认证 | JWT | - |
| 文档 | Swagger/OpenAPI | - |

### 前端技术栈

| 平台 | 技术 | 说明 |
|------|------|------|
| 微信小程序 | 原生小程序 | 完整功能 |
| iOS/Android | Flutter 3.x | 跨平台 |
| Web | Vue 3 (计划) | 管理后台 |

### 基础设施

- **Docker** - 容器化部署
- **Nginx** - 反向代理
- **Celery Flower** - 任务监控
- **GitHub Actions** - CI/CD（计划）

## 📋 开发文档

详细文档请查看 [docs/](docs/) 目录：

- 📖 [API 接口文档](docs/API.md)
- 🗄️ [数据库设计](docs/DB_DESIGN.md)
- 🏗️ [后端技术架构](docs/BACKEND_FRAMEWORK.md)
- 📱 [Flutter 开发指南](docs/FLUTTER_DEV_GUIDE.md)
- 🤖 [Celery 异步任务指南](docs/CELERY_GUIDE.md)
- 📝 [任务分解](docs/TASK_BREAKDOWN.md)

## 🧪 测试

### 后端测试

```bash
cd src/backend

# 运行单元测试
pytest

# 运行特定测试
pytest tests/test_auth.py -v

# 测试覆盖率
pytest --cov=app tests/
```

### API 测试

```bash
# 使用 curl 测试健康检查
curl http://localhost:8000/health

# 测试档案上传
curl -X POST "http://localhost:8000/api/v1/records/upload" \
  -F "file=@test_report.jpg" \
  -F "record_type=体检" \
  -F "title=2026 年体检"
```

### 小程序测试

1. 微信开发者工具 → 真机调试
2. 确保手机和电脑在同一局域网
3. 配置 API 地址为电脑 IP

## 🤝 贡献指南

本项目为内部项目，如需贡献代码：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

内部项目，未经许可不得外传

---

## 📞 联系方式

- **项目地址**: https://github.com/magicengine-ai/HealthPal
- **问题反馈**: 请在 GitHub 提交 Issue

---

**Made with ❤️ by HealthPal Team**
