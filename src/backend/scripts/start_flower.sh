#!/bin/bash
# Celery Flower 监控面板启动脚本

set -e

echo "📊 启动 HealthPal Celery Flower 监控..."

# 激活虚拟环境
source venv/bin/activate

# 启动 Flower
# --port: 访问端口
# --broker: Redis 地址
celery -A app.core.celery_config.celery_app flower \
    --port=5555 \
    --broker=redis://localhost:6379/0 \
    --logfile=logs/flower.log \
    --persistent=True
