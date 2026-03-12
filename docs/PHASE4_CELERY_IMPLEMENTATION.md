# 第四阶段：异步任务（Celery）+ 中间件集成

**实施日期：** 2026-03-12  
**状态：** ✅ 已完成

---

## 📋 实施概览

### 完成内容

| 模块 | 状态 | 说明 |
|------|------|------|
| **Celery 配置** | ✅ | 核心配置、队列路由、定时任务 |
| **OCR 异步任务** | ✅ | 文档识别、状态轮询、批量处理 |
| **通知异步任务** | ✅ | 用药提醒、健康报告、预约提醒 |
| **分析异步任务** | ✅ | 指标分析、日报生成、异常检测 |
| **Docker 集成** | ✅ | Worker、Beat、Flower 服务 |
| **API 集成** | ✅ | 任务状态查询、OCR 任务提交 |
| **监控面板** | ✅ | Flower 实时监控 |

---

## 🏗️ 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户请求                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI (Web 应用)                        │
│  - REST API                                                 │
│  - 任务提交                                                 │
│  - 状态查询                                                 │
└────────────┬────────────────────────────────────────────────┘
             │ 提交任务
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Redis (消息代理)                          │
│  - 任务队列 (ocr_queue, notification_queue, analysis_queue) │
│  - 结果存储                                                 │
└────────────┬────────────────────────────────────────────────┘
             │ 消费任务
             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Celery Worker (4 并发)                      │
│  - OCR 任务处理                                              │
│  - 通知推送                                                 │
│  - 数据分析                                                 │
└─────────────────────────────────────────────────────────────┘
             ▲
             │ 调度
┌────────────┴────────────────────────────────────────────────┐
│                   Celery Beat (定时器)                       │
│  - 每 5 分钟：用药提醒检查                                    │
│  - 每天 08:00：健康日报生成                                  │
│  - 每天 02:00：数据备份                                      │
│  - 每周 03:00：文件清理                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 新增文件清单

### 核心配置

```
src/backend/app/core/
└── celery_config.py          # Celery 应用配置
```

### 异步任务模块

```
src/backend/app/tasks/
├── __init__.py
├── ocr_tasks.py              # OCR 相关任务
├── notification_tasks.py     # 通知推送任务
└── analysis_tasks.py         # 数据分析任务
```

### 启动脚本

```
src/backend/scripts/
├── start_celery_worker.sh    # Worker 启动脚本
├── start_celery_beat.sh      # Beat 启动脚本
└── start_flower.sh           # Flower 监控启动脚本
```

### API 路由

```
src/backend/app/api/
└── tasks.py                  # 任务管理 API
```

### 文档

```
docs/
└── CELERY_GUIDE.md           # Celery 使用指南
```

### 配置文件

```
config/
└── docker-compose.yml        # 更新：添加 Celery 服务
```

---

## 🔧 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| **Celery** | 5.3.4 | 分布式任务队列 |
| **Redis** | 7 | 消息代理 + 结果存储 |
| **Flower** | 2.0.1 | 监控面板 |
| **FastAPI** | 0.109.0 | Web 框架 |

---

## 🚀 部署指南

### Docker 部署（推荐）

```bash
# 1. 启动所有服务
cd config
docker-compose up -d

# 2. 查看服务状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
docker-compose logs -f flower
```

### 服务列表

| 服务名 | 容器名 | 端口 | 说明 |
|--------|--------|------|------|
| backend | healthpal-backend | 8000 | FastAPI 应用 |
| celery_worker | healthpal-celery-worker | - | 任务执行器 |
| celery_beat | healthpal-celery-beat | - | 定时任务调度器 |
| flower | healthpal-flower | 5555 | 监控面板 |

---

## 📊 任务队列设计

### 队列分类

| 队列名 | 优先级 | 任务类型 | 并发数 |
|--------|--------|----------|--------|
| `ocr_queue` | 高 | OCR 识别 | 2 |
| `notification_queue` | 中 | 通知推送 | 4 |
| `analysis_queue` | 低 | 数据分析 | 2 |
| `default` | 中 | 其他任务 | 4 |

### 任务路由

```python
task_routes = {
    'app.tasks.ocr_tasks.*': {'queue': 'ocr_queue'},
    'app.tasks.notification_tasks.*': {'queue': 'notification_queue'},
    'app.tasks.analysis_tasks.*': {'queue': 'analysis_queue'},
}
```

---

## ⏰ 定时任务配置

### 已配置的定时任务

| 任务名 | 频率 | 时间 | 说明 |
|--------|------|------|------|
| `daily-backup` | 每天 | 02:00 | 健康数据备份 |
| `check-medication-reminders` | 每 5 分钟 | - | 用药提醒检查 |
| `generate-daily-report` | 每天 | 08:00 | 健康日报生成 |
| `cleanup-expired-files` | 每周 | 周日 03:00 | 过期文件清理 |

### 配置位置

`app/core/celery_config.py` → `beat_schedule`

---

## 🔍 监控方案

### Flower 监控面板

**访问地址：** http://localhost:5555

**功能：**
- ✅ 实时任务监控
- ✅ Worker 状态查看
- ✅ 任务历史记录
- ✅ 统计图表
- ✅ 任务撤销/重试

### 命令行监控

```bash
# Worker 状态
celery -A app.core.celery_config.celery_app inspect ping

# 活跃任务
celery -A app.core.celery_config.celery_app inspect active

# 任务统计
celery -A app.core.celery_config.celery_app inspect stats

# 已注册任务
celery -A app.core.celery_config.celery_app inspect registered
```

---

## 📝 使用示例

### 1. 提交 OCR 任务

```python
from app.tasks.ocr_tasks import process_ocr_task

# 上传文件后触发 OCR
task = process_ocr_task.delay(
    record_id="record_123",
    file_path="/uploads/file.jpg",
    ocr_provider="baidu"
)

print(f"Task ID: {task.id}")
```

### 2. 查询任务状态

```python
from celery.result import AsyncResult
from app.core.celery_config import celery_app

result = AsyncResult("task_id", app=celery_app)

print(f"Status: {result.status}")  # PENDING, STARTED, SUCCESS, FAILURE

if result.ready():
    print(f"Result: {result.result}")
```

### 3. API 调用

```bash
# 上传档案（自动触发 OCR）
curl -X POST "http://localhost:8000/api/v1/records/upload" \
  -F "file=@report.jpg" \
  -F "record_type=体检" \
  -F "title=2026 年体检" \
  -F "record_date=2026-03-12"

# 查询任务状态
curl "http://localhost:8000/api/v1/tasks/{task_id}"
```

---

## ✅ 测试验证

### 1. 基础功能测试

```bash
# 测试 OCR 任务
python -c "
from app.tasks.ocr_tasks import process_ocr_task
result = process_ocr_task.delay('test_id', '/path/to/file.jpg')
print(f'Task ID: {result.id}')
"

# 测试通知任务
python -c "
from app.tasks.notification_tasks import send_medication_reminder
result = send_medication_reminder.delay('user_123', 'med_456', '08:00')
print(f'Result: {result.result}')
"
```

### 2. 定时任务测试

```bash
# 手动触发定时任务
celery -A app.core.celery_config.celery_app call \
  app.tasks.notification_tasks.send_medication_reminders
```

### 3. 监控面板验证

访问 http://localhost:5555，检查：
- [ ] Workers 标签页显示 4 个活跃 Worker
- [ ] Tasks 标签页显示任务历史
- [ ] Broker 标签页显示 Redis 连接正常

---

## 🔒 安全配置

### 1. Redis 认证

```python
# 生产环境启用密码
REDIS_PASSWORD=your_redis_password
```

### 2. 任务序列化

```python
# 仅接受 JSON 序列化
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
```

### 3. 任务确认

```python
# 延迟确认，防止任务丢失
task_acks_late = True
task_reject_on_worker_lost = True
```

---

## 📈 性能优化

### 1. 并发配置

```bash
# 根据 CPU 核心数调整
celery worker -c 4  # 4 个并发进程
```

### 2. 预取优化

```python
# 避免任务堆积
worker_prefetch_multiplier = 1
```

### 3. 结果过期

```python
# 1 小时后自动清理
result_expires = 3600
```

### 4. 任务限流

```python
# OCR 任务限流
task_default_rate_limit = '10/m'  # 每分钟最多 10 个
```

---

## 🐛 故障排查

### 常见问题

#### 1. Worker 不消费任务

```bash
# 检查 Worker 日志
docker logs healthpal-celery-worker

# 检查队列
celery -A app.core.celery_config.celery_app inspect stats

# 重启 Worker
docker-compose restart celery_worker
```

#### 2. 任务执行失败

```bash
# 查看错误日志
docker logs healthpal-celery-worker | grep "Task failed"

# 查看 Flower 面板
open http://localhost:5555
```

#### 3. Beat 不触发定时任务

```bash
# 检查 Beat 日志
docker logs healthpal-celery-beat

# 检查调度器数据
docker exec healthpal-celery-beat ls -la /app/logs/
```

---

## 📅 后续计划

### Phase 5 规划

- [ ] 推送服务集成（极光推送/个推）
- [ ] 短信通知集成
- [ ] 邮件通知集成
- [ ] WebSocket 实时通知
- [ ] 任务优先级动态调整

---

## 📚 参考文档

- [Celery 官方文档](https://docs.celeryq.dev/)
- [Flower 监控文档](https://github.com/mher/flower)
- [Redis 文档](https://redis.io/documentation)
- [HealthPal Celery 使用指南](./CELERY_GUIDE.md)

---

**实施者：** HealthPal 开发团队  
**审核者：** -  
**下次更新：** 根据 Phase 5 进展
