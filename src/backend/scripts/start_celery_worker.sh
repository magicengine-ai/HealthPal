#!/bin/bash
# Celery Worker 启动脚本

set -e

echo "🚀 启动 HealthPal Celery Worker..."

# 激活虚拟环境
source venv/bin/activate

# 启动 Celery Worker
# -Q: 指定队列
# -l: 日志级别
# -c: 并发进程数
celery -A app.core.celery_config.celery_app worker \
    -Q ocr_queue,notification_queue,analysis_queue,default \
    -l info \
    -c 4 \
    --logfile=logs/celery_worker.log \
    --pidfile=logs/celery_worker.pid
