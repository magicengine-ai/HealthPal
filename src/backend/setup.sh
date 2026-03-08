#!/bin/bash
# HealthPal Python 后端环境搭建脚本

set -e

echo "🚀 HealthPal Python 后端环境搭建开始..."

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 检查 Python 版本
echo -e "${YELLOW}检查 Python 环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo -e "${RED}Python3 未安装，请先安装 Python 3.11+${NC}"
    exit 1
fi

# 检查 pip
echo -e "${YELLOW}检查 pip...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✓ $PIP_VERSION"
else
    echo -e "${RED}pip3 未安装${NC}"
    exit 1
fi

# 创建虚拟环境
echo -e "${YELLOW}创建虚拟环境...${NC}"
cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [ ! -d "venv" ]; then
    if python3 -m venv venv 2>/dev/null; then
        echo "✓ 虚拟环境创建完成"
        USE_VENV=true
    else
        echo -e "${YELLOW}⚠️ 虚拟环境创建失败，使用全局 Python 环境${NC}"
        echo -e "${YELLOW}提示：安装 python3-venv 包可创建虚拟环境：sudo apt install python3.12-venv${NC}"
        USE_VENV=false
    fi
else
    echo "✓ 虚拟环境已存在"
    USE_VENV=true
fi

# 激活虚拟环境
if [ "$USE_VENV" = true ]; then
    echo -e "${YELLOW}激活虚拟环境...${NC}"
    source venv/bin/activate
fi

# 安装依赖
echo -e "${YELLOW}安装 Python 依赖...${NC}"
if [ "$USE_VENV" = true ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    pip3 install --upgrade pip
    pip3 install --break-system-packages -r requirements.txt
fi
echo "✓ 依赖安装完成"

# 复制环境配置
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}创建环境配置文件...${NC}"
    cp .env.example .env
    echo "✓ 环境配置创建完成，请编辑 .env 文件配置数据库和密钥"
else
    echo "✓ 环境配置已存在"
fi

# 创建必要目录
echo -e "${YELLOW}创建必要目录...${NC}"
mkdir -p uploads
mkdir -p alembic/versions
echo "✓ 目录创建完成"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Python 后端环境搭建完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "下一步："
echo "1. 启动数据库：cd ../../config && docker-compose up -d"
echo "2. 激活虚拟环境：source venv/bin/activate"
echo "3. 运行后端：uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "4. 访问文档：http://localhost:8000/docs"
echo ""
