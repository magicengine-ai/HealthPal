# HealthPal 后端服务启动指南

**创建日期：** 2026-03-12

---

## 🚀 快速启动

### 方式一：使用启动脚本（推荐）

```bash
cd HealthPal
./scripts/start_backend.sh
```

访问：http://localhost:8000/docs

---

## 📋 完整启动流程

### 1. 安装 Docker Compose（可选，用于完整服务）

如果你有 sudo 权限：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

# 验证安装
docker compose version
```

### 2. 启动数据库和中间件（需要 Docker）

```bash
cd HealthPal/config

# 只启动数据库和 Redis（不需要 Celery）
docker compose up -d mysql mongodb redis

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 3. 启动后端服务

#### 方式 A：使用脚本

```bash
cd HealthPal
./scripts/start_backend.sh
```

#### 方式 B：手动启动

```bash
cd HealthPal/src/backend

# 创建/激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动 Celery Worker（可选）

```bash
cd HealthPal/src/backend
source venv/bin/activate

# 启动 Worker
celery -A app.core.celery_config.celery_app worker -l info -c 4

# 启动 Beat（定时任务）
celery -A app.core.celery_config.celery_app beat -l info
```

---

## 🔍 服务检查

### 检查后端服务

```bash
curl http://localhost:8000/health
```

### 访问 API 文档

浏览器打开：http://localhost:8000/docs

### 检查数据库

```bash
# MySQL
docker compose ps mysql

# MongoDB
docker compose ps mongodb

# Redis
docker compose ps redis
```

---

## 🛠️ 无 Docker 环境（仅开发测试）

如果无法使用 Docker，可以使用外部数据库服务：

### 1. 安装本地数据库

```bash
# MySQL
sudo apt-get install -y mysql-server

# MongoDB
sudo apt-get install -y mongodb

# Redis
sudo apt-get install -y redis-server
```

### 2. 配置数据库连接

编辑 `src/backend/.env`：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=healthpal
MYSQL_PASSWORD=healthpal_pass
MYSQL_DATABASE=healthpal

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=healthpal
MONGO_PASSWORD=healthpal_pass

REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. 启动后端

```bash
cd HealthPal/src/backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📱 移动端配置

启动后端后，配置移动端 API 地址：

### Android 模拟器
编辑 `src/mobile/lib/services/api_service.dart`:
```dart
static const String _baseUrl = 'http://10.0.2.2:8000/api/v1';
```

### iOS 模拟器/真机
```dart
static const String _baseUrl = 'http://localhost:8000/api/v1';
```

### 真机测试（同一 WiFi）
```dart
static const String _baseUrl = 'http://192.168.1.XXX:8000/api/v1';
// 替换为你的电脑 IP 地址
```

---

## 🧪 测试后端

```bash
# 运行测试脚本
./scripts/test_api.sh

# 或手动测试
curl http://localhost:8000/docs
```

---

## 🐛 常见问题

### 1. 端口被占用

**错误：** `Address already in use`

**解决：**
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 2. 虚拟环境问题

**错误：** `ModuleNotFoundError`

**解决：**
```bash
cd HealthPal/src/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 数据库连接失败

**错误：** `Can't connect to MySQL server`

**解决：**
```bash
# 检查数据库是否运行
docker compose ps

# 或检查本地服务
sudo systemctl status mysql
sudo systemctl status mongodb
sudo systemctl status redis
```

---

## 📊 服务端口

| 服务 | 端口 | 地址 |
|------|------|------|
| FastAPI | 8000 | http://localhost:8000 |
| MySQL | 3306 | localhost:3306 |
| MongoDB | 27017 | localhost:27017 |
| Redis | 6379 | localhost:6379 |
| Flower | 5555 | http://localhost:5555 |

---

## 📝 常用命令

```bash
# 启动所有服务（Docker Compose）
cd HealthPal/config
docker compose up -d

# 停止所有服务
docker compose down

# 查看日志
docker compose logs -f backend

# 重启服务
docker compose restart

# 进入容器
docker compose exec backend bash

# 查看数据库
docker compose exec mysql mysql -u healthpal -p healthpal
```

---

**维护者：** HealthPal 开发团队  
**最后更新：** 2026-03-12
