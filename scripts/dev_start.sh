#!/bin/bash

# HealthPal 快速启动脚本（开发环境）
# 使用：./scripts/dev_start.sh

set -e

echo "🚀 HealthPal 开发环境启动"
echo "================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装"
    exit 1
fi

# 启动后端服务
echo "📦 启动后端服务..."
cd config
docker-compose up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "📊 服务状态:"
docker-compose ps

# 检查后端是否可访问
echo ""
echo "🔍 检查后端服务..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/docs" | grep -q "200"; then
    echo "✅ 后端服务正常 (http://localhost:8000)"
else
    echo "❌ 后端服务异常，请查看日志"
    docker-compose logs backend
    exit 1
fi

# 检查 Flower 监控
echo ""
echo "🔍 检查 Flower 监控..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:5555" | grep -q "200"; then
    echo "✅ Flower 监控正常 (http://localhost:5555)"
else
    echo "⚠️  Flower 监控未响应"
fi

# 检查数据库
echo ""
echo "🔍 检查数据库..."
if docker-compose ps mysql | grep -q "Up"; then
    echo "✅ MySQL 正常"
fi

if docker-compose ps mongodb | grep -q "Up"; then
    echo "✅ MongoDB 正常"
fi

if docker-compose ps redis | grep -q "Up"; then
    echo "✅ Redis 正常"
fi

# 检查 Celery Worker
echo ""
echo "🔍 检查 Celery Worker..."
if docker-compose ps celery_worker | grep -q "Up"; then
    echo "✅ Celery Worker 正常"
fi

if docker-compose ps celery_beat | grep -q "Up"; then
    echo "✅ Celery Beat 正常"
fi

echo ""
echo "================================"
echo "🎉 所有服务启动完成！"
echo "================================"
echo ""
echo "📱 访问地址:"
echo "   - API 文档：http://localhost:8000/docs"
echo "   - Flower 监控：http://localhost:5555"
echo "   - MySQL: localhost:3306"
echo "   - MongoDB: localhost:27017"
echo "   - Redis: localhost:6379"
echo ""
echo "📝 常用命令:"
echo "   - 查看日志：docker-compose logs -f"
echo "   - 停止服务：docker-compose down"
echo "   - 重启服务：docker-compose restart"
echo "   - 运行测试：./scripts/test_api.sh"
echo ""
echo "📱 启动移动端:"
echo "   cd src/mobile"
echo "   flutter pub get"
echo "   flutter run"
echo ""
