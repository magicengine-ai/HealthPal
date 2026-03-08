#!/bin/bash
# HealthPal 开发环境搭建脚本
# 使用方式：bash scripts/setup_env.sh

set -e

echo "🚀 HealthPal 开发环境搭建开始..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查系统
echo -e "${YELLOW}检查系统环境...${NC}"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✓ Linux 系统 detected"
    ELIGIBLE=true
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✓ macOS 系统 detected"
    ELIGIBLE=true
else
    echo -e "${RED}不支持的系统：$OSTYPE${NC}"
    exit 1
fi

# 创建项目目录结构
echo -e "${YELLOW}创建项目目录结构...${NC}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p $PROJECT_ROOT/{src/{mobile/{ios,android},backend,embedded},docs,scripts,config,tests}
echo "✓ 目录结构创建完成"

# 检查并安装 Go
echo -e "${YELLOW}检查 Go 环境...${NC}"
if command -v go &> /dev/null; then
    GO_VERSION=$(go version)
    echo "✓ $GO_VERSION"
else
    echo -e "${YELLOW}Go 未安装，请手动安装：https://golang.org/dl/${NC}"
fi

# 检查并安装 Node.js
echo -e "${YELLOW}检查 Node.js 环境...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION"
else
    echo -e "${YELLOW}Node.js 未安装，请手动安装：https://nodejs.org/${NC}"
fi

# 检查并安装 Docker
echo -e "${YELLOW}检查 Docker 环境...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✓ $DOCKER_VERSION"
else
    echo -e "${YELLOW}Docker 未安装，请手动安装：https://docs.docker.com/get-docker/${NC}"
fi

# 检查并安装 MySQL 客户端
echo -e "${YELLOW}检查 MySQL 环境...${NC}"
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version)
    echo "✓ $MYSQL_VERSION"
else
    echo -e "${YELLOW}MySQL 客户端未安装${NC}"
fi

# 检查并安装 Git
echo -e "${YELLOW}检查 Git 环境...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✓ $GIT_VERSION"
else
    echo -e "${RED}Git 未安装，请先安装 Git${NC}"
    exit 1
fi

# 初始化 Git 仓库
echo -e "${YELLOW}初始化 Git 仓库...${NC}"
cd $PROJECT_ROOT
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git 仓库初始化完成"
else
    echo "✓ Git 仓库已存在"
fi

# 创建 .gitignore
echo -e "${YELLOW}创建 .gitignore...${NC}"
cat > $PROJECT_ROOT/.gitignore << 'EOF'
# 依赖
node_modules/
vendor/
__pycache__/
*.pyc

# 编译产物
build/
dist/
*.o
*.so
*.exe

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# 日志
logs/
*.log

# 环境配置
.env
.env.local
config/secrets.*

# 数据库
*.db
*.sqlite

# 移动端
mobile/ios/Pods/
mobile/android/.gradle/
mobile/android/build/
EOF
echo "✓ .gitignore 创建完成"

# 创建后端项目结构
echo -e "${YELLOW}创建后端项目结构...${NC}"
mkdir -p $PROJECT_ROOT/src/backend/{cmd,internal/{config,handler,service,repository,models},pkg,api}
echo "✓ 后端目录创建完成"

# 创建 Go module
if command -v go &> /dev/null; then
    cd $PROJECT_ROOT/src/backend
    go mod init healthpal-backend
    echo "✓ Go module 初始化完成"
fi

# 创建移动端项目占位
echo -e "${YELLOW}创建移动端项目占位...${NC}"
mkdir -p $PROJECT_ROOT/src/mobile/{ios,android}
echo "✓ 移动端目录创建完成"

# 创建嵌入式项目占位
echo -e "${YELLOW}创建嵌入式项目占位...${NC}"
mkdir -p $PROJECT_ROOT/src/embedded/{firmware,drivers,protocols}
echo "✓ 嵌入式目录创建完成"

# 创建 Docker Compose 配置
echo -e "${YELLOW}创建 Docker Compose 配置...${NC}"
cat > $PROJECT_ROOT/config/docker-compose.yml << 'EOF'
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: healthpal-mysql
    environment:
      MYSQL_ROOT_PASSWORD: healthpal_root
      MYSQL_DATABASE: healthpal
      MYSQL_USER: healthpal
      MYSQL_PASSWORD: healthpal_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - healthpal-net

  mongodb:
    image: mongo:6
    container_name: healthpal-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: healthpal
      MONGO_INITDB_ROOT_PASSWORD: healthpal_pass
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    networks:
      - healthpal-net

  redis:
    image: redis:7-alpine
    container_name: healthpal-redis
    ports:
      - "6379:6379"
    networks:
      - healthpal-net

  backend:
    build:
      context: ../src/backend
      dockerfile: Dockerfile
    container_name: healthpal-backend
    ports:
      - "8080:8080"
    depends_on:
      - mysql
      - mongodb
      - redis
    environment:
      DB_HOST: mysql
      MONGO_HOST: mongodb
      REDIS_HOST: redis
    networks:
      - healthpal-net

volumes:
  mysql_data:
  mongo_data:

networks:
  healthpal-net:
    driver: bridge
EOF
echo "✓ Docker Compose 配置创建完成"

# 创建 README
echo -e "${YELLOW}创建项目 README...${NC}"
cat > $PROJECT_ROOT/README.md << 'EOF'
# HealthPal - 个人健康档案 AI 助手

一款基于 AI 技术的个人健康管理工具，帮助用户整合、分析和管理个人及家庭健康数据。

## 📁 项目结构

```
HealthPal/
├── src/
│   ├── mobile/      # 移动端 (iOS/Android)
│   ├── backend/     # 后端服务 (Go)
│   └── embedded/    # 嵌入式固件 (设备接入)
├── docs/            # 文档
├── scripts/         # 脚本工具
├── config/          # 配置文件
└── tests/           # 测试用例
```

## 🚀 快速开始

### 环境要求

- Go 1.21+
- Node.js 18+
- Docker & Docker Compose
- MySQL 8.0+
- MongoDB 6+
- Redis 7+

### 启动开发环境

```bash
# 1. 启动数据库和中间件
cd config
docker-compose up -d mysql mongodb redis

# 2. 启动后端服务
cd ../src/backend
go run cmd/main.go

# 3. 移动端开发
# iOS: 打开 src/mobile/ios/HealthPal.xcodeproj
# Android: 打开 src/mobile/android 在 Android Studio
```

## 📋 开发文档

- [任务分解](docs/TASK_BREAKDOWN.md)
- [API 文档](docs/API.md)
- [数据库设计](docs/DB_DESIGN.md)

## 📄 许可证

内部项目，未经许可不得外传
EOF
echo "✓ README 创建完成"

# 创建后端 main.go 占位
echo -e "${YELLOW}创建后端入口文件...${NC}"
cat > $PROJECT_ROOT/src/backend/cmd/main.go << 'EOF'
package main

import (
	"log"
	"net/http"
)

func main() {
	log.Println("🚀 HealthPal Backend Starting...")
	
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})
	
	log.Println("📡 Server listening on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
EOF
echo "✓ 后端入口文件创建完成"

# 首次 Git 提交
echo -e "${YELLOW}执行首次 Git 提交...${NC}"
cd $PROJECT_ROOT
git add -A
git commit -m "feat: 初始化 HealthPal 项目结构

- 创建项目目录结构
- 配置 Docker Compose 开发环境
- 初始化 Go 后端项目
- 添加任务分解文档
- 创建环境搭建脚本"
echo "✓ 首次提交完成"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ 开发环境搭建完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "下一步："
echo "1. 安装 Go 依赖：cd src/backend && go mod tidy"
echo "2. 启动数据库：cd config && docker-compose up -d"
echo "3. 运行后端：cd src/backend && go run cmd/main.go"
echo ""
echo "查看任务分解：cat docs/TASK_BREAKDOWN.md"
echo ""
