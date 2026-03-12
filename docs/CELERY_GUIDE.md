# Celery 异步任务使用指南

## 📋 目录

- [架构概述](#架构概述)
- [快速开始](#快速开始)
- [任务队列](#任务队列)
- [使用示例](#使用示例)
- [定时任务](#定时任务)
- [监控面板](#监控面板)
- [最佳实践](#最佳实践)

---

## 架构概述

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   FastAPI   │────▶│    Redis     │◀────│Celery Worker│
│   (Web App) │     │   (Broker)   │     │  (4 workers)│
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Celery Beat │
                    │ (Scheduler)  │
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Flower    │
                    │  (Monitor)   │
                    └──────────────┘
```

### 组件说明

| 组件 | 作用 | 端口 |
|------|------|------|
| **Redis** | 消息代理 + 结果存储 | 6379 |
| **Celery Worker** | 执行异步任务 | - |
| **Celery Beat** | 定时任务调度器 | - |
| **Flower** | 监控面板 | 5555 |

---

## 快速开始

### 1. 安装依赖

```bash
cd src/backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 启动服务（Docker）

```bash
cd config
docker-compose up -d
```

启动的服务：
- `healthpal-backend` - FastAPI 应用 (8000)
- `healthpal-celery-worker` - Celery Worker
- `healthpal-celery-beat` - 定时任务调度器
- `healthpal-flower` - 监控面板 (5555)

### 3. 本地开发模式

```bash
# 终端 1: 启动 Redis
docker run -d -p 6379:6379 --name healthpal-redis redis:7-alpine

# 终端 2: 启动 Celery Worker
cd src/backend
source venv/bin/activate
celery -A app.core.celery_config.celery_app worker -l info -c 4

# 终端 3: 启动 Celery Beat
celery -A app.core.celery_config.celery_app beat -l info

# 终端 4: 启动 Flower（可选）
celery -A app.core.celery_config.celery_app flower --port=5555
```

---

## 任务队列

### 队列定义

| 队列名 | 用途 | 优先级 |
|--------|------|--------|
| `ocr_queue` | OCR 识别任务 | 高 |
| `notification_queue` | 通知推送任务 | 中 |
| `analysis_queue` | 数据分析任务 | 低 |
| `default` | 默认队列 | 中 |

### 任务路由

```python
# 自动路由配置
task_routes={
    'app.tasks.ocr_tasks.*': {'queue': 'ocr_queue'},
    'app.tasks.notification_tasks.*': {'queue': 'notification_queue'},
    'app.tasks.analysis_tasks.*': {'queue': 'analysis_queue'},
}
```

---

## 使用示例

### 1. 调用 OCR 异步任务

```python
from app.tasks.ocr_tasks import process_ocr_task

# 上传文件后，异步调用 OCR
@app.post("/records/upload")
async def upload_record(file: UploadFile, record_data: RecordCreate):
    # 1. 保存文件
    file_path = save_file(file)
    
    # 2. 创建档案记录
    record = await create_record(record_data)
    
    # 3. 异步触发 OCR 任务
    task = process_ocr_task.delay(
        record_id=record.id,
        file_path=file_path,
        ocr_provider="baidu"
    )
    
    return {
        "record_id": record.id,
        "task_id": task.id,
        "status": "processing"
    }
```

### 2. 获取任务状态

```python
from celery.result import AsyncResult
from app.core.celery_config import celery_app

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    
    return {
        "task_id": task_id,
        "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE
        "result": result.result if result.ready() else None
    }
```

### 3. 发送用药提醒

```python
from app.tasks.notification_tasks import send_medication_reminder

# 立即发送
send_medication_reminder.delay(
    user_id="user_123",
    medication_id="med_456",
    reminder_time="08:00"
)
```

### 4. 批量分析用户数据

```python
from app.tasks.analysis_tasks import batch_analyze_users

# 批量分析
task = batch_analyze_users.delay(
    user_ids=["user_1", "user_2", "user_3"],
    days=30
)
```

---

## 定时任务

### 已配置的定时任务

| 任务 | 频率 | 说明 |
|------|------|------|
| `daily-backup` | 每天 02:00 | 健康数据备份 |
| `check-medication-reminders` | 每 5 分钟 | 检查并发送用药提醒 |
| `generate-daily-report` | 每天 08:00 | 生成健康日报 |
| `cleanup-expired-files` | 每周日 03:00 | 清理过期文件 |

### 添加新的定时任务

编辑 `app/core/celery_config.py`:

```python
beat_schedule={
    # 新增：每小时检查一次异常指标
    'check-abnormal-indicators': {
        'task': 'app.tasks.analysis_tasks.detect_abnormal_indicators',
        'schedule': crontab(minute=0),  # 每小时
        'options': {'kwargs': {'user_id': 'all'}}
    },
}
```

---

## 监控面板

### Flower 监控

访问：http://localhost:5555

**功能：**
- ✅ 实时查看任务执行状态
- ✅ 查看任务历史记录
- ✅ 监控 Worker 状态
- ✅ 查看任务统计图表
- ✅ 手动触发任务
- ✅ 查看任务参数和结果

### 监控指标

```bash
# 查看 Worker 状态
celery -A app.core.celery_config.celery_app inspect ping

# 查看活跃任务
celery -A app.core.celery_config.celery_app inspect active

# 查看已注册任务
celery -A app.core.celery_config.celery_app inspect registered

# 查看任务统计
celery -A app.core.celery_config.celery_app inspect stats
```

---

## 最佳实践

### 1. 任务设计

```python
# ✅ 好的做法：任务幂等性
@celery_app.task(bind=True, max_retries=3)
def process_ocr_task(self, record_id: str, file_path: str):
    try:
        # 检查是否已处理
        if is_already_processed(record_id):
            return {'success': True, 'message': 'Already processed'}
        
        # 处理逻辑...
    except Exception as e:
        # 自动重试
        raise self.retry(exc=e, countdown=60)

# ❌ 避免：非幂等操作
@celery_app.task
def charge_user(user_id: str, amount: float):
    # 可能重复扣费！
    deduct_balance(user_id, amount)
```

### 2. 错误处理

```python
@celery_app.task(bind=True, max_retries=3)
def fragile_task(self, data: dict):
    try:
        # 可能失败的操作
        result = risky_operation(data)
        return {'success': True, 'result': result}
    
    except ConnectionError as e:
        # 网络错误，自动重试
        raise self.retry(exc=e, countdown=60)
    
    except ValueError as e:
        # 参数错误，不重试
        return {'success': False, 'error': str(e)}
    
    except Exception as e:
        # 其他错误，记录日志后重试
        logger.error(f"Task failed: {e}")
        raise self.retry(exc=e, countdown=120)
```

### 3. 任务限流

```python
# 限制任务执行频率
@celery_app.task(rate_limit='10/m')
def rate_limited_task():
    pass

# 在配置中设置
task_default_rate_limit = '10/m'  # 每分钟最多 10 个任务
```

### 4. 任务超时

```python
# 设置任务超时时间
@celery_app.task(time_limit=300)  # 5 分钟超时
def long_running_task():
    pass

# 调用时指定超时
task = process_ocr_task.apply_async(
    args=[record_id, file_path],
    task_time_limit=300
)
```

### 5. 任务链

```python
from celery import chain, group

# 任务链：依次执行
workflow = chain(
    process_ocr_task.s(record_id, file_path),
    extract_indicators.s(),
    save_to_database.s()
)
result = workflow.apply_async()

# 任务组：并行执行
workflow = group(
    analyze_blood_pressure.s(user_id),
    analyze_blood_sugar.s(user_id),
    analyze_heart_rate.s(user_id)
)
result = workflow.apply_async()
```

---

## 故障排查

### Worker 不消费任务

```bash
# 检查 Worker 状态
docker logs healthpal-celery-worker

# 检查队列长度
celery -A app.core.celery_config.celery_app inspect stats

# 重启 Worker
docker-compose restart celery_worker
```

### 任务执行失败

```bash
# 查看任务日志
docker logs healthpal-celery-worker | grep "Task failed"

# 查看 Flower 面板
open http://localhost:5555
```

### Beat 不触发定时任务

```bash
# 检查 Beat 日志
docker logs healthpal-celery-beat

# 检查调度器数据
docker exec healthpal-celery-beat cat /app/logs/celerybeat-schedule
```

---

## 性能优化

### 1. 并发配置

```python
# 根据 CPU 核心数调整
celery worker -c $(nproc)  # CPU 核心数
```

### 2. 预取优化

```python
# 每个 worker 预取任务数
worker_prefetch_multiplier = 1  # 避免任务堆积
```

### 3. 结果过期

```python
# 及时清理结果
result_expires = 3600  # 1 小时后过期
```

---

**最后更新：** 2026-03-12  
**维护者：** HealthPal 开发团队
