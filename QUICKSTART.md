# HealthPal 快速启动指南

## 🚀 一键启动所有服务

### 前提条件

- Docker & Docker Compose
- Git

### 启动步骤

```bash
# 1. 克隆项目
git clone https://github.com/magicengine-ai/HealthPal.git
cd HealthPal

# 2. 启动所有服务（包括 Celery）
cd config
docker-compose up -d

# 3. 查看服务状态
docker-compose ps
```

### 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| **API 文档** | http://localhost:8000/docs | FastAPI Swagger UI |
| **Flower 监控** | http://localhost:5555 | Celery 任务监控 |
| **MySQL** | localhost:3306 | 关系型数据库 |
| **MongoDB** | localhost:27017 | 文档数据库 |
| **Redis** | localhost:6379 | 消息队列 + 缓存 |

---

## 📝 测试异步任务

### 1. 上传健康档案（触发 OCR 任务）

```bash
curl -X POST "http://localhost:8000/api/v1/records/upload" \
  -F "file=@test_report.jpg" \
  -F "record_type=体检" \
  -F "title=2026 年体检" \
  -F "record_date=2026-03-12"
```

返回示例：
```json
{
  "code": 0,
  "message": "上传成功，OCR 识别任务已提交",
  "data": {
    "record_id": "uuid_xxx",
    "task_id": "celery_task_id_xxx",
    "ocr_status": "pending"
  }
}
```

### 2. 查询任务状态

```bash
curl "http://localhost:8000/api/v1/tasks/{task_id}"
```

返回示例：
```json
{
  "code": 0,
  "data": {
    "task_id": "celery_task_id_xxx",
    "status": "SUCCESS",
    "ready": true,
    "result": {
      "success": true,
      "indicators_count": 12,
      "message": "OCR 识别完成"
    }
  }
}
```

### 3. 查看 Flower 监控

访问 http://localhost:5555

- 查看 **Workers** 标签页 → 确认 4 个 Worker 在线
- 查看 **Tasks** 标签页 → 查看任务执行历史
- 查看 **Broker** 标签页 → 确认 Redis 连接正常

---

## 🔧 本地开发模式

### 1. 启动基础服务

```bash
# 只启动数据库和 Redis
docker-compose up -d mysql mongodb redis
```

### 2. 配置 Python 环境

```bash
cd src/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 启动后端服务

```bash
# 终端 1: FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动 Celery Worker

```bash
# 终端 2: Celery Worker
celery -A app.core.celery_config.celery_app worker -l info -c 4
```

### 5. 启动 Celery Beat

```bash
# 终端 3: Celery Beat
celery -A app.core.celery_config.celery_app beat -l info
```

### 6. 启动 Flower（可选）

```bash
# 终端 4: Flower 监控
celery -A app.core.celery_config.celery_app flower --port=5555
```

---

## 📊 监控命令

```bash
# 查看 Worker 状态
celery -A app.core.celery_config.celery_app inspect ping

# 查看活跃任务
celery -A app.core.celery_config.celery_app inspect active

# 查看任务统计
celery -A app.core.celery_config.celery_app inspect stats

# 查看已注册任务
celery -A app.core.celery_config.celery_app inspect registered
```

---

## 🐛 故障排查

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
docker-compose logs -f flower
```

### 重启服务

```bash
# 重启单个服务
docker-compose restart celery_worker

# 重启所有服务
docker-compose restart
```

### 清理并重新开始

```bash
# 停止并删除所有容器和数据
docker-compose down -v

# 重新启动
docker-compose up -d
```

---

## 📚 更多文档

- [Celery 使用指南](./docs/CELERY_GUIDE.md)
- [Phase 4 实施报告](./docs/PHASE4_CELERY_IMPLEMENTATION.md)
- [任务分解](./docs/TASK_BREAKDOWN.md)
- [API 文档](./docs/API.md)

---

**最后更新：** 2026-03-12  
**维护者：** HealthPal 开发团队
