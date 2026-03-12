# HealthPal Flutter 移动端开发指南

**创建日期：** 2026-03-12  
**状态：** 🚧 开发中

---

## 📋 开发进度

### Phase 1.2: 移动端基础开发

| 任务 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| **Flutter 环境配置** | ✅ | 100% | pubspec.yaml + 依赖配置 |
| **项目脚手架** | ✅ | 100% | 目录结构 + 基础文件 |
| **主题配置** | ✅ | 100% | AppTheme + 设计规范 |
| **路由配置** | ✅ | 100% | GoRouter + 页面路由 |
| **服务层** | ✅ | 100% | API + 本地存储 |
| **状态管理** | ✅ | 100% | Provider |
| **数据模型** | ✅ | 100% | User/Record/Medication |
| **启动页** | ✅ | 100% | SplashScreen |
| **登录页** | ✅ | 100% | LoginScreen |
| **首页** | ✅ | 100% | HomeScreen + 底部导航 |
| **档案页** | 🚧 | 50% | 基础框架 |
| **分析页** | 🚧 | 30% | 占位页面 |
| **用药页** | 🚧 | 30% | 占位页面 |
| **个人中心** | ✅ | 80% | 基础功能 |

---

## 🏗️ 项目结构

```
mobile/
├── lib/
│   ├── main.dart                    # 应用入口
│   ├── config/
│   │   ├── theme.dart               # 主题配置
│   │   └── routes.dart              # 路由配置
│   ├── models/
│   │   ├── user_model.dart          # 用户模型
│   │   ├── record_model.dart        # 档案模型
│   │   └── medication_model.dart    # 用药模型
│   ├── providers/
│   │   ├── user_provider.dart       # 用户状态
│   │   ├── records_provider.dart    # 档案状态
│   │   └── medication_provider.dart # 用药状态
│   ├── services/
│   │   ├── api_service.dart         # API 服务
│   │   └── storage_service.dart     # 本地存储
│   ├── screens/
│   │   ├── splash/                  # 启动页
│   │   ├── auth/                    # 认证页面
│   │   ├── home/                    # 首页
│   │   ├── records/                 # 档案页面
│   │   ├── analysis/                # 分析页面
│   │   ├── management/              # 管理页面
│   │   └── profile/                 # 个人中心
│   ├── widgets/                     # 通用组件（待创建）
│   └── utils/                       # 工具类
├── assets/
│   ├── images/                      # 图片资源
│   ├── icons/                       # 图标资源
│   ├── animations/                  # 动画资源
│   └── fonts/                       # 字体资源
├── test/                            # 测试文件
├── pubspec.yaml                     # 依赖配置
└── analysis_options.yaml            # 代码分析配置
```

---

## 🎨 设计规范

### 配色方案

```dart
// 主色调
primaryBlue: #1890FF    // 健康蓝
lifeGreen: #52C41A      // 生命绿

// 辅助色
warningOrange: #FA8C16  // 警告
errorRed: #F5222D       // 错误
successGreen: #73D13D   // 成功

// 中性色
textPrimary: #333333
textSecondary: #666666
textHint: #999999
divider: #E8E8E8
background: #F5F5F5
```

### 字体规范

| 级别 | 大小 | 粗细 | 用途 |
|------|------|------|------|
| textSizeXLarge | 24sp | Bold | 大标题 |
| textSizeLarge | 18sp | Medium | 标题 |
| textSizeMedium | 16sp | Normal | 正文 |
| textSizeNormal | 14sp | Normal | 次要文本 |
| textSizeSmall | 12sp | Normal | 辅助文本 |

### 圆角规范

- borderRadiusSmall: 4px - 小元素
- borderRadiusMedium: 8px - 按钮、输入框
- borderRadiusLarge: 12px - 卡片
- borderRadiusXLarge: 16px - 大卡片

---

## 🚀 快速开始

### 1. 安装 Flutter

```bash
# macOS
brew install --cask flutter

# 或者从官网下载
# https://flutter.dev/docs/get-started/install

# 验证安装
flutter doctor
```

### 2. 配置环境

```bash
# 进入项目目录
cd src/mobile

# 获取依赖
flutter pub get

# 运行代码生成（如需要）
flutter pub run build_runner build --delete-conflicting-outputs
```

### 3. 运行应用

```bash
# 查看可用设备
flutter devices

# 运行到模拟器
flutter run

# 运行到真机
flutter run -d <device_id>

# 发布模式
flutter run --release
```

### 4. 构建应用

```bash
# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release
```

---

## 📦 核心依赖

### 状态管理

```yaml
provider: ^6.1.1  # 官方推荐的状态管理
```

### 网络请求

```yaml
dio: ^5.4.0           # HTTP 客户端
retrofit: ^4.0.3      # REST API 封装
connectivity_plus: ^5.0.2  # 网络状态检测
```

### 本地存储

```yaml
hive: ^2.2.3              # 高性能键值存储
hive_flutter: ^1.1.0      # Flutter 集成
shared_preferences: ^2.2.2 # 简单键值存储
flutter_secure_storage: ^9.0.0  # 安全存储（Token）
```

### 路由

```yaml
go_router: ^12.1.1  # 声明式路由
```

### UI 组件

```yaml
fl_chart: ^0.65.0           # 图表库
flutter_svg: ^2.0.9         # SVG 支持
lottie: ^2.7.0              # 动画支持
shimmer: ^3.0.0             # 骨架屏
cached_network_image: ^3.3.0 # 图片缓存
```

### 工具

```yaml
logger: ^2.0.2+1     # 日志
equatable: ^2.0.5    # 值比较
dartz: ^0.10.1       # 函数式编程
```

---

## 🔧 开发规范

### 命名规范

```dart
// 文件命名：snake_case
user_model.dart
login_screen.dart

// 类命名：PascalCase
class UserModel {}
class LoginScreen {}

// 变量/方法命名：camelCase
String userName;
void loadData() {}

// 常量命名：camelCase + static final
static final primaryColor = Color(0xFF1890FF);

// 枚举命名：PascalCase
enum LoadingStatus { idle, loading, success, failure }
```

### 代码组织

```dart
// 1. Dart imports
import 'dart:async';

// 2. Flutter imports
import 'package:flutter/material.dart';

// 3. Package imports
import 'package:provider/provider.dart';

// 4. Project imports
import '../models/user_model.dart';
```

### Widget 构建顺序

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: ...,
    body: ...,
    floatingActionButton: ...,
    bottomNavigationBar: ...,
  );
}
```

---

## 📱 核心页面实现指南

### 1. 登录页

```dart
// 已实现：lib/screens/auth/login_screen.dart
// 功能：手机号 + 密码登录、忘记密码、第三方登录
```

### 2. 首页

```dart
// 已实现：lib/screens/home/home_screen.dart
// 功能：健康评分、指标卡片、提醒列表、快捷操作
```

### 3. 档案列表页

```dart
// 待完善：lib/screens/records/records_screen.dart
// 需要实现：
// - 档案列表展示
// - 分类筛选
// - 下拉刷新
// - 上拉加载更多
```

### 4. 档案上传页

```dart
// 待完善：lib/screens/records/upload_record_screen.dart
// 需要实现：
// - 拍照/选择图片
// - 表单填写
// - 文件上传
// - OCR 状态轮询
```

---

## 🔌 API 集成

### 认证

```dart
// 登录
POST /api/v1/auth/login
{
  "phone": "13800138000",
  "password": "password123"
}

// 注册
POST /api/v1/auth/register
{
  "phone": "13800138000",
  "password": "password123",
  "code": "123456"
}
```

### 档案

```dart
// 获取档案列表
GET /api/v1/records?page=1&page_size=20

// 获取档案详情
GET /api/v1/records/{id}

// 上传档案
POST /api/v1/records/upload
FormData: file, record_type, title, record_date

// 删除档案
DELETE /api/v1/records/{id}
```

### 任务状态

```dart
// 查询任务状态
GET /api/v1/tasks/{task_id}
```

---

## 🧪 测试

### 单元测试

```dart
// test/models/user_model_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:healthpal/models/user_model.dart';

void main() {
  test('UserModel fromJson', () {
    final json = {'id': '1', 'phone': '13800138000'};
    final user = UserModel.fromJson(json);
    expect(user.id, '1');
    expect(user.phone, '13800138000');
  });
}
```

### Widget 测试

```dart
// test/widgets/health_score_card_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:healthpal/widgets/health_score_card.dart';

void main() {
  testWidgets('HealthScoreCard displays score', (tester) async {
    await tester.pumpWidget(
      MaterialApp(home: HealthScoreCard(score: 85)),
    );
    expect(find.text('85'), findsOneWidget);
  });
}
```

---

## 🐛 常见问题

### 1. 依赖冲突

```bash
flutter clean
flutter pub get
```

### 2. 代码生成失败

```bash
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

### 3. iOS 构建失败

```bash
cd ios
pod install
cd ..
```

### 4. Android 签名问题

编辑 `android/app/build.gradle`:
```gradle
android {
    defaultConfig {
        applicationId "com.healthpal.app"
        minSdkVersion 21
        targetSdkVersion 34
    }
}
```

---

## 📅 后续计划

### Phase 1.2 剩余工作

- [ ] 完善档案列表页（筛选、加载）
- [ ] 实现档案上传功能
- [ ] 实现档案详情页
- [ ] 完善用药管理页
- [ ] 实现健康分析图表
- [ ] 添加通用 Widget 组件库
- [ ] 添加加载状态/空状态
- [ ] 完善错误处理

### Phase 1.3: 核心功能

- [ ] OCR 状态轮询
- [ ] 推送通知集成
- [ ] 图片上传优化
- [ ] 离线缓存
- [ ] 数据可视化

---

## 📚 参考资源

- [Flutter 官方文档](https://flutter.dev/docs)
- [Provider 文档](https://pub.dev/packages/provider)
- [GoRouter 文档](https://pub.dev/packages/go_router)
- [Dio 文档](https://pub.dev/packages/dio)
- [Flutter 中文社区](https://flutterchina.club/)

---

**维护者：** HealthPal 开发团队  
**最后更新：** 2026-03-12
