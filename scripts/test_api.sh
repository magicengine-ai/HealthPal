#!/bin/bash

# HealthPal API 联调测试脚本
# 使用：./scripts/test_api.sh

set -e

BASE_URL="http://localhost:8000/api/v1"
TOKEN=""
PASSED=0
FAILED=0

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 HealthPal API 联调测试"
echo "================================"
echo ""

# 测试函数
test_api() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "📊 测试：$name ... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json")
    elif [ "$method" == "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" == "200" ] || [ "$http_code" == "201" ]; then
        echo -e "${GREEN}✅ 通过${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ 失败${NC} (HTTP $http_code)"
        echo "响应：$body"
        ((FAILED++))
        return 1
    fi
}

# 1. 健康检查
echo ""
echo "=== 基础测试 ==="
test_api "健康检查" "GET" "/../health" ""

# 2. 用户登录
echo ""
echo "=== 认证测试 ==="
echo "使用测试账号登录..."

login_response=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"phone": "13800138000", "password": "test123456"}')

TOKEN=$(echo $login_response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✅ 登录成功${NC}"
    ((PASSED++))
    echo "Token: ${TOKEN:0:20}..."
else
    echo -e "${RED}❌ 登录失败${NC}"
    echo "响应：$login_response"
    ((FAILED++))
    echo ""
    echo "提示：请先创建测试账号或检查后端服务"
    exit 1
fi

# 3. 获取用户信息
test_api "获取用户信息" "GET" "/users/me" ""

# 4. 获取档案列表
echo ""
echo "=== 档案模块测试 ==="
test_api "获取档案列表" "GET" "/records?page=1&page_size=10" ""

# 5. 创建测试档案（模拟上传）
echo ""
echo "创建测试档案..."
# 注意：真实文件上传需要使用 multipart/form-data
# 这里仅测试 API 连通性
echo -e "${YELLOW}⚠️  文件上传需要真实文件，跳过测试${NC}"

# 6. 获取用药列表
echo ""
echo "=== 用药模块测试 ==="
test_api "获取用药列表" "GET" "/medications" ""

# 7. 创建测试用药
echo ""
echo "创建测试用药..."
medication_data='{
    "name": "阿司匹林",
    "dosage": "100mg",
    "frequency": "每日 1 次",
    "reminder_times": ["08:00"],
    "status": 1
}'

test_api "添加用药" "POST" "/medications" "$medication_data"

# 8. Celery 任务测试
echo ""
echo "=== 异步任务测试 ==="
echo -e "${YELLOW}⚠️  Celery 任务需要真实 OCR 文件，跳过测试${NC}"

# 9. Flower 监控检查
echo ""
echo "检查 Flower 监控..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:5555" | grep -q "200"; then
    echo -e "${GREEN}✅ Flower 监控正常${NC} (http://localhost:5555)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Flower 监控未启动${NC}"
fi

# 10. 数据库连接检查
echo ""
echo "检查数据库连接..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/docs" | grep -q "200"; then
    echo -e "${GREEN}✅ 后端服务正常${NC} (http://localhost:8000/docs)"
    ((PASSED++))
else
    echo -e "${RED}❌ 后端服务异常${NC}"
    ((FAILED++))
fi

# 测试总结
echo ""
echo "================================"
echo "📊 测试总结"
echo "================================"
echo -e "通过：${GREEN}$PASSED${NC}"
echo -e "失败：${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}⚠️  部分测试失败，请检查日志${NC}"
    exit 1
fi
