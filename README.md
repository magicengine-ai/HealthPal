# HealthPal - 个人健康档案 AI 助手

一款基于 AI 技术的个人健康管理工具，帮助用户整合、分析和管理个人及家庭健康数据。

## 📁 项目结构

```
HealthPal/
├── config/              # 配置文件
│   └── docker-compose.yml   # MySQL+MongoDB+Redis
├── docs/                # 文档
│   ├── TASK_BREAKDOWN.md  # 任务分解
│   ├── DB_DESIGN.md       # 数据库设计
│   ├── API.md             # 接口文档
│   └── MOBILE_DEV_PLAN.md # 移动端开发计划
├── src/
│   ├── backend/         # Python FastAPI 后端
│   │   ├── app/         # 应用代码
│   │   ├── tests/       # 测试
│   │   └── scripts/     # 脚本
│   └── mobile/          # Flutter 移动端
└── tests/               # 测试用例
```

## 🚀 快速开始

### 环境要求

- **Python 3.11+**
- **Node.js 18+** (移动端开发)
- **Flutter 3.x** (移动端开发)
- **Docker & Docker Compose**

### 1. 启动数据库和中间件

```bash
cd config
docker-compose up -d
```

### 2. 启动后端服务

```bash
cd src/backend

# 方式一：使用搭建脚本（首次）
bash setup.sh

# 方式二：手动安装
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 运行服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档：http://localhost:8000/docs

### 3. 启动移动端开发

```bash
cd src/mobile

# 创建 Flutter 项目（首次）
flutter create --org com.healthpal --project-name healthpal

# 运行
flutter run
```

## 📋 开发文档

- [任务分解](docs/TASK_BREAKDOWN.md)
- [API 文档](docs/API.md)
- [数据库设计](docs/DB_DESIGN.md)
- [移动端开发计划](docs/MOBILE_DEV_PLAN.md)

## 🔧 技术栈

| 模块 | 技术 |
|------|------|
| 后端 | Python + FastAPI |
| 移动端 | Flutter 3.x |
| MySQL | 8.0 |
| MongoDB | 6 |
| Redis | 7 |
| OCR | 百度/腾讯 OCR |

## 📄 许可证

内部项目，未经许可不得外传
