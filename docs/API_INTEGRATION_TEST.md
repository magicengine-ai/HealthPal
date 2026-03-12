# HealthPal 前后端 API 联调测试指南

**创建日期：** 2026-03-12  
**测试环境：** 开发环境

---

## 📋 测试前准备

### 1. 环境检查清单

#### 后端环境
```bash
# 检查 Python 版本
python3 --version  # 应该 >= 3.11

# 检查虚拟环境
cd HealthPal/src/backend
source venv/bin/activate

# 检查依赖
pip list | grep -E "fastapi|celery|redis"
```

#### 移动端环境
```bash
# 检查 Flutter 版本
flutter --version  # 应该 >= 3.0

# 检查设备
flutter devices

# 检查依赖
cd HealthPal/src/mobile
flutter pub get
```

---

## 🚀 第一步：启动后端服务

### 方式一：Docker Compose (推荐)

```bash
cd HealthPal/config

# 启动所有服务（包括 Celery）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f flower
```

启动的服务：
- **backend** - FastAPI (http://localhost:8000)
- **celery_worker** - Celery 任务执行器
- **celery_beat** - 定时任务调度器
- **flower** - 监控面板 (http://localhost:5555)
- **mysql** - 数据库 (localhost:3306)
- **mongodb** - 文档库 (localhost:27017)
- **redis** - 缓存/消息队列 (localhost:6379)

### 方式二：本地开发模式

```bash
# 终端 1: 启动数据库和 Redis
cd HealthPal/config
docker-compose up -d mysql mongodb redis

# 终端 2: 启动 FastAPI
cd HealthPal/src/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端 3: 启动 Celery Worker
celery -A app.core.celery_config.celery_app worker -l info -c 4

# 终端 4: 启动 Celery Beat
celery -A app.core.celery_config.celery_app beat -l info
```

---

## 📱 第二步：配置移动端 API 地址

### 修改 API 服务配置

编辑 `src/mobile/lib/services/api_service.dart`:

```dart
// 开发环境（模拟器）
static const String _baseUrl = 'http://10.0.2.2:8000/api/v1';  // Android 模拟器
// 或
static const String _baseUrl = 'http://localhost:8000/api/v1';  // iOS 模拟器/真机

// 测试环境
// static const String _baseUrl = 'http://your-server-ip:8000/api/v1';
```

**注意：**
- Android 模拟器访问本机：使用 `10.0.2.2`
- iOS 模拟器访问本机：使用 `localhost`
- 真机测试：使用电脑 IP 地址（如 `192.168.1.100`）

---

## 🧪 第三步：API 接口测试

### 1. 测试后端 API (使用 curl 或 Postman)

#### 健康检查
```bash
curl http://localhost:8000/health
```

#### 访问 API 文档
打开浏览器：http://localhost:8000/docs

### 2. 完整测试流程

#### Step 1: 用户注册
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "test123456",
    "code": "123456"
  }'
```

#### Step 2: 用户登录
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "test123456"
  }'
```

保存返回的 `access_token`。

#### Step 3: 获取用户信息
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Step 4: 上传健康档案
```bash
curl -X POST "http://localhost:8000/api/v1/records/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test_report.jpg" \
  -F "record_type=体检" \
  -F "title=2026 年体检" \
  -F "record_date=2026-03-12"
```

#### Step 5: 查询任务状态
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/TASK_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Step 6: 获取档案列表
```bash
curl -X GET "http://localhost:8000/api/v1/records?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Step 7: 获取档案详情
```bash
curl -X GET "http://localhost:8000/api/v1/records/RECORD_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📱 第四步：移动端测试

### 1. 启动应用

```bash
cd HealthPal/src/mobile

# Android 模拟器
flutter run

# iOS 模拟器
flutter run -d ios

# 指定设备
flutter devices
flutter run -d <device_id>
```

### 2. 测试流程清单

#### 认证流程
- [ ] 启动页正常显示
- [ ] 跳转到登录页
- [ ] 输入手机号和密码
- [ ] 点击登录，查看网络请求
- [ ] 登录成功，跳转到首页
- [ ] Token 已保存

#### 档案列表
- [ ] 档案列表加载
- [ ] 分类筛选功能
- [ ] 下拉刷新
- [ ] 上拉加载更多
- [ ] 空状态显示
- [ ] 点击卡片跳转到详情

#### 档案详情
- [ ] 基本信息显示
- [ ] 指标列表显示
- [ ] OCR 状态显示
- [ ] 文件预览
- [ ] 删除功能

#### 档案上传
- [ ] 点击拍照/选图
- [ ] 图片预览
- [ ] 表单填写
- [ ] 点击上传
- [ ] 上传进度显示
- [ ] 上传成功提示

#### 用药管理
- [ ] 用药列表加载
- [ ] 今日提醒显示
- [ ] 添加用药对话框
- [ ] 时间选择器
- [ ] 日期选择器
- [ ] 标记服用
- [ ] 删除用药

#### 健康分析
- [ ] 图表加载
- [ ] 指标切换
- [ ] 统计数据
- [ ] 健康建议

---

## 🔍 第五步：调试技巧

### 查看移动端日志

```bash
# Flutter 日志
flutter logs

# 过滤特定标签
flutter logs | grep -i "healthpal"
flutter logs | grep -i "dio"  # HTTP 请求日志
```

### 查看后端日志

```bash
# Docker 日志
docker-compose logs -f backend
docker-compose logs -f celery_worker

# 查看特定时间日志
docker-compose logs --since=10m backend
```

### 网络请求调试

在 `api_service.dart` 中添加日志：

```dart
_dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      print('📤 Request: ${options.method} ${options.path}');
      print('Headers: ${options.headers}');
      print('Data: ${options.data}');
      return handler.next(options);
    },
    onResponse: (response, handler) {
      print('📥 Response: ${response.statusCode} ${response.requestOptions.path}');
      return handler.next(response);
    },
    onError: (error, handler) {
      print('❌ Error: ${error.response?.statusCode}');
      print('Message: ${error.message}');
      return handler.next(error);
    },
  ),
);
```

---

## 🧪 第六步：自动化测试脚本

创建测试脚本 `scripts/test_api.sh`:

```bash
#!/bin/bash

# HealthPal API 测试脚本

BASE_URL="http://localhost:8000/api/v1"
TOKEN=""

echo "🚀 开始 API 测试..."

# 1. 健康检查
echo "\n📊 测试 1: 健康检查"
curl -s "$BASE_URL/../health" | jq .

# 2. 用户登录
echo "\n📊 测试 2: 用户登录"
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000", "password": "test123456"}')

TOKEN=$(echo $RESPONSE | jq -r '.data.access_token')
echo "Token: $TOKEN"

# 3. 获取用户信息
echo "\n📊 测试 3: 获取用户信息"
curl -s "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 4. 获取档案列表
echo "\n📊 测试 4: 获取档案列表"
curl -s "$BASE_URL/records?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 5. 获取用药列表
echo "\n📊 测试 5: 获取用药列表"
curl -s "$BASE_URL/medications" \
  -H "Authorization: Bearer $TOKEN" | jq .

echo "\n✅ API 测试完成！"
```

使用：
```bash
cd HealthPal
chmod +x scripts/test_api.sh
./scripts/test_api.sh
```

---

## 🐛 常见问题排查

### 1. 后端连接失败

**错误：** `Connection refused`

**解决：**
```bash
# 检查后端是否启动
docker-compose ps

# 检查端口占用
lsof -i :8000

# 重启后端
docker-compose restart backend
```

### 2. 数据库连接失败

**错误：** `Can't connect to MySQL server`

**解决：**
```bash
# 检查数据库状态
docker-compose ps mysql

# 查看数据库日志
docker-compose logs mysql

# 重启数据库
docker-compose restart mysql
```

### 3. Celery 任务不执行

**错误：** OCR 任务一直处于 pending 状态

**解决：**
```bash
# 检查 Celery Worker
docker-compose logs celery_worker

# 检查 Redis
docker-compose logs redis

# 重启 Celery
docker-compose restart celery_worker celery_beat
```

### 4. 移动端网络错误

**错误：** `HandshakeException` 或 `SocketException`

**解决：**
- Android 模拟器：使用 `10.0.2.2` 而不是 `localhost`
- 真机测试：确保手机和电脑在同一 WiFi，使用电脑 IP
- 检查防火墙设置

### 5. Token 失效

**错误：** `401 Unauthorized`

**解决：**
```bash
# 清除本地存储的 Token
# 移动端：重新登录
# 测试：重新获取 Token
```

---

## 📊 测试报告模板

创建测试报告 `docs/TEST_REPORT.md`:

```markdown
# API 联调测试报告

**测试日期：** 2026-03-12
**测试人员：** 
**测试环境：** 开发环境

## 测试结果

### 认证模块
- [ ] 用户注册
- [ ] 用户登录
- [ ] Token 刷新

### 档案模块
- [ ] 档案列表
- [ ] 档案详情
- [ ] 档案上传
- [ ] OCR 识别
- [ ] 档案删除

### 用药模块
- [ ] 用药列表
- [ ] 添加用药
- [ ] 编辑用药
- [ ] 删除用药
- [ ] 标记服用

### 分析模块
- [ ] 趋势图表
- [ ] 统计数据

## 发现问题

| 问题描述 | 严重程度 | 状态 | 备注 |
|---------|---------|------|------|
|         |         |      |      |

## 测试结论

[ ] 通过，可以进入下一阶段
[ ] 部分通过，需要修复问题
[ ] 未通过，需要大量修改
```

---

## 🎯 测试完成标准

- [ ] 所有 API 接口测试通过
- [ ] 移动端所有页面功能正常
- [ ] 前后端数据同步正确
- [ ] OCR 流程完整测试通过
- [ ] 推送通知测试通过
- [ ] 无严重 Bug
- [ ] 性能指标达标

---

## 📚 参考文档

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Flutter 网络](https://flutter.dev/docs/development/data-and-backend/networking)
- [Dio 文档](https://pub.dev/packages/dio)
- [Postman 文档](https://learning.postman.com/)

---

**维护者：** HealthPal 开发团队  
**最后更新：** 2026-03-12
