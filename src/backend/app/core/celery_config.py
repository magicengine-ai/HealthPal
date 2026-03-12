"""
Celery 异步任务配置
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings


# 创建 Celery 应用
celery_app = Celery(
    'healthpal',
    broker=settings.redis_url,  # Redis 作为消息代理
    backend=settings.redis_url,  # Redis 作为结果存储
    include=['app.tasks.ocr_tasks', 'app.tasks.notification_tasks', 'app.tasks.analysis_tasks']
)

# Celery 配置
celery_app.conf.update(
    # 时区配置
    timezone='Asia/Shanghai',
    
    # 任务序列化
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # 任务确认
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # 结果过期时间（秒）
    result_expires=3600,
    
    # 任务路由
    task_routes={
        'app.tasks.ocr_tasks.*': {'queue': 'ocr_queue'},
        'app.tasks.notification_tasks.*': {'queue': 'notification_queue'},
        'app.tasks.analysis_tasks.*': {'queue': 'analysis_queue'},
    },
    
    # 队列定义
    task_queues={
        'ocr_queue': {'exchange': 'ocr', 'routing_key': 'ocr'},
        'notification_queue': {'exchange': 'notification', 'routing_key': 'notification'},
        'analysis_queue': {'exchange': 'analysis', 'routing_key': 'analysis'},
    },
    
    # 任务限流
    worker_prefetch_multiplier=1,
    task_default_rate_limit='10/m',
    
    # 定时任务调度器
    beat_scheduler='celery.beat:PersistentScheduler',
    
    # 定时任务配置
    beat_schedule={
        # 每天凌晨 2 点执行健康数据备份
        'daily-backup': {
            'task': 'app.tasks.analysis_tasks.daily_health_backup',
            'schedule': crontab(hour=2, minute=0),
        },
        
        # 每 5 分钟检查用药提醒
        'check-medication-reminders': {
            'task': 'app.tasks.notification_tasks.send_medication_reminders',
            'schedule': crontab(minute='*/5'),
        },
        
        # 每天早上 8 点生成健康日报
        'generate-daily-report': {
            'task': 'app.tasks.analysis_tasks.generate_daily_health_report',
            'schedule': crontab(hour=8, minute=0),
        },
        
        # 每周日凌晨 3 点清理过期文件
        'cleanup-expired-files': {
            'task': 'app.tasks.ocr_tasks.cleanup_expired_files',
            'schedule': crontab(hour=3, minute=0, day_of_week=0),
        },
    },
    
    # 监控配置
    worker_send_task_events=True,
    task_send_sent_event=True,
)


# 自动发现任务
celery_app.autodiscover_tasks(['app.tasks'])


@celery_app.task(bind=True)
def debug_task(self):
    """调试任务"""
    return f"Task executed: {self.request.id}"
