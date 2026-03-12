#!/bin/bash
# Celery Beat 定时任务调度器启动脚本

set -e

echo "⏰ 启动 HealthPal Celery Beat..."

# 激活虚拟环境
source venv/bin/activate

# 启动 Celery Beat
# -l: 日志级别
celery -A app.core.celery_config.celery_app beat \
    -l info \
    --logfile=logs/celery_beat.log \
    --pidfile=logs/celery_beat.pid \
    --scheduler celery.beat:PersistentScheduler
