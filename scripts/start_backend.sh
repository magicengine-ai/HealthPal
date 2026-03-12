#!/bin/bash

# HealthPal 后端服务启动脚本（无 Docker Compose 版本）
# 使用：./scripts/start_backend.sh

set -e

echo "🚀 HealthPal 后端服务启动"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 进入后端目录
cd "$(dirname "$0")/../src/backend"

echo "📦 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

echo "📦 安装依赖..."
pip install -q -r requirements.txt

echo ""
echo "📊 服务信息:"
echo "   - API 文档：http://localhost:8000/docs"
echo "   - API 地址：http://localhost:8000/api/v1"
echo ""

echo "⚠️  注意：此脚本仅启动 FastAPI 服务"
echo "   Celery Worker 和数据库需要单独启动"
echo ""

echo "🚀 启动 FastAPI 服务..."
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
