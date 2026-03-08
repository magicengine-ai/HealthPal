# HealthPal 移动端开发计划

## 一、技术选型

### 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **原生开发** (Swift + Kotlin) | 性能最佳、体验最好 | 开发成本高、维护两套代码 | ⭐⭐⭐⭐ |
| **Flutter** | 跨平台、性能好、UI 一致 | Dart 学习成本、包体积较大 | ⭐⭐⭐⭐⭐ |
| **React Native** | JS 生态、热更新 | 性能一般、依赖原生模块 | ⭐⭐⭐ |

### 推荐方案：Flutter

**理由：**
- 一套代码同时生成 iOS 和 Android
- 性能接近原生（Skia 引擎直接渲染）
- 丰富的 UI 组件库，适合健康类 App
- 图表库成熟（fl_chart）
- 热重载提升开发效率

---

## 二、Flutter 项目结构

```
mobile/
├── lib/
│   ├── main.dart              # 入口
│   ├── app.dart               # App 配置
│   ├── config/                # 配置文件
│   │   ├── routes.dart        # 路由配置
│   │   └── theme.dart         # 主题配置
│   ├── models/                # 数据模型
│   │   ├── user.dart
│   │   ├── health_record.dart
│   │   └── indicator.dart
│   ├── services/              # 服务层
│   │   ├── api_service.dart   # API 调用
│   │   ├── storage_service.dart # 本地存储
│   │   └── auth_service.dart  # 认证服务
│   ├── providers/             # 状态管理 (Provider/Riverpod)
│   │   ├── user_provider.dart
│   │   └── records_provider.dart
│   ├── screens/               # 页面
│   │   ├── home/              # 首页
│   │   ├── records/           # 档案管理
│   │   ├── analysis/          # 分析报告
│   │   ├── management/        # 健康管理
│   │   └── profile/           # 个人中心
│   ├── widgets/               # 通用组件
│   │   ├── record_card.dart
│   │   ├── indicator_chart.dart
│   │   └── reminder_item.dart
│   └── utils/                 # 工具类
│       ├── date_utils.dart
│       └── validator.dart
├── assets/                    # 资源文件
│   ├── images/
│   ├── icons/
│   └── fonts/
├── test/                      # 测试
└── pubspec.yaml               # 依赖配置
```

---

## 三、核心页面设计

### 3.1 首页 (HomeScreen)

```
┌─────────────────────────────┐
│  健康评分 85                 │ ← 顶部卡片
│  ████████░░ 良好             │
├─────────────────────────────┤
│  最近指标                    │
│  ┌─────┐ ┌─────┐ ┌─────┐   │
│  │血压 │ │血糖 │ │体重 │   │ ← 指标卡片
│  │120  │ │5.6  │ │65kg │   │
│  │正常 │ │正常 │ │正常 │   │
│  └─────┘ └─────┘ └─────┘   │
├─────────────────────────────┤
│  今日提醒                    │
│  ☑ 08:00 阿司匹林 100mg     │ ← 提醒列表
│  ☐ 12:00 午餐后测血糖       │
│  ☐ 20:00 运动 30 分钟        │
├─────────────────────────────┤
│  [📷 上传] [📝 记录症状]     │ ← 快捷操作
└─────────────────────────────┘
```

### 3.2 档案列表页 (RecordsScreen)

```
┌─────────────────────────────┐
│  健康档案           [+ 上传] │
├─────────────────────────────┤
│  [全部] [体检] [病历] [检查] │ ← 分类筛选
├─────────────────────────────┤
│  📄 2026 年年度体检           │
│     北京协和医院 · 3 月 1 日   │
│     12 项指标 · 2 项异常      │
├─────────────────────────────┤
│  📄 血常规检查               │
│     协和医院 · 2 月 15 日      │
│     8 项指标 · 全部正常      │
├─────────────────────────────┤
│  📄 心电图报告               │
│     协和医院 · 1 月 10 日      │
│     窦性心律 · 正常          │
└─────────────────────────────┘
```

### 3.3 指标趋势页 (TrendScreen)

```
┌─────────────────────────────┐
│  < 血压趋势            [导出] │
├─────────────────────────────┤
│  [收缩压] [舒张压] [脉搏]    │ ← 指标切换
├─────────────────────────────┤
│                             │
│    140 ─ ─ ─ ─ ─ ●          │
│        │           ╲        │
│    120 ─ ● ─ ─ ─ ─ ─ ●      │ ← 折线图
│        │ ╲                  │
│    100 ─ ●                  │
│                             │
│    1 月   2 月   3 月   4 月   │
├─────────────────────────────┤
│  平均：120 mmHg             │
│  最高：135 mmHg             │
│  最低：115 mmHg             │
└─────────────────────────────┘
```

### 3.4 档案详情页 (RecordDetailScreen)

```
┌─────────────────────────────┐
│  < 2026 年年度体检      [...] │
├─────────────────────────────┤
│  🏥 北京协和医院             │
│  📅 2026-03-01              │
│  📋 体检中心                 │
├─────────────────────────────┤
│  关键指标                    │
│  ┌─────────────────────┐    │
│  │ 收缩压    120 正常   │    │
│  │ 舒张压     80 正常   │    │
│  │ 空腹血糖  5.6 正常   │    │
│  │ 总胆固醇  5.8 ↑偏高  │    │
│  └─────────────────────┘    │
├─────────────────────────────┤
│  [查看原始报告 ▶]            │
└─────────────────────────────┘
```

---

## 四、核心功能实现

### 4.1 图片上传 + OCR

```dart
// 拍照/选择图片
final ImagePicker picker = ImagePicker();
final XFile? image = await picker.pickImage(
  source: ImageSource.camera,
);

// 上传到服务器
final formData = FormData.fromMap({
  'file': await MultipartFile.fromFile(image!.path),
  'record_type': '体检报告',
  'title': '2026 年体检',
});

final response = await apiService.post('/records/upload', formData);

// 轮询 OCR 状态
Future<void> pollOcrStatus(String recordId) async {
  for (int i = 0; i < 30; i++) {
    final result = await apiService.get('/records/$recordId');
    if (result['ocr_status'] == 2) {
      // OCR 完成，刷新 UI
      break;
    }
    await Future.delayed(Duration(seconds: 2));
  }
}
```

### 4.2 指标趋势图

```dart
import 'package:fl_chart/fl_chart.dart';

LineChart(
  LineChartData(
    titlesData: FlTitlesData(show: true),
    lineBarsData: [
      LineChartBarData(
        spots: [
          FlSpot(0, 118),  // 1 月
          FlSpot(1, 122),  // 2 月
          FlSpot(2, 120),  // 3 月
        ],
        isCurved: true,
        color: Colors.blue,
        dotData: FlDotData(show: true),
      ),
    ],
  ),
)
```

### 4.3 本地存储 (用药提醒)

```dart
import 'package:hive/hive.dart';

// 初始化
await Hive.initFlutter();
var box = await Hive.openBox('reminders');

// 保存提醒
await box.put('reminder_1', {
  'medicine_name': '阿司匹林',
  'dosage': '100mg',
  'reminder_times': ['08:00'],
  'status': 1,
});

// 读取提醒
var reminders = box.values.toList();
```

### 4.4 推送通知

```dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

final FlutterLocalNotificationsPlugin notifications = 
    FlutterLocalNotificationsPlugin();

// 初始化
await notifications.initialize(
  InitializationSettings(
    android: AndroidInitializationSettings('@mipmap/ic_launcher'),
    iOS: IOSInitializationSettings(),
  ),
);

// 创建用药提醒渠道
await notifications
    .resolvePlatformSpecificImplementation<
        AndroidFlutterLocalNotificationsPlugin>()
    ?.createNotificationChannel(AndroidNotificationChannel(
      'medications',
      '用药提醒',
      description: '用药时间提醒',
      importance: Importance.high,
    ));

// 显示通知
await notifications.show(
  0,
  '用药提醒',
  '该吃阿司匹林了 (100mg)',
  NotificationDetails(
    android: AndroidNotificationDetails(
      'medications',
      '用药提醒',
      channelDescription: '用药时间提醒',
      importance: Importance.high,
    ),
  ),
);
```

---

## 五、依赖配置 (pubspec.yaml)

```yaml
name: healthpal
description: 个人健康档案 AI 助手
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # 状态管理
  provider: ^6.0.5
  # 或 riverpod: ^2.4.0
  
  # 网络请求
  dio: ^5.3.0
  retrofit: ^4.0.1
  
  # 本地存储
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  shared_preferences: ^2.2.0
  
  # 图片处理
  image_picker: ^1.0.0
  image_cropper: ^5.0.0
  
  # 图表
  fl_chart: ^0.64.0
  
  # 推送通知
  flutter_local_notifications: ^16.1.0
  
  # 权限
  permission_handler: ^11.0.0
  
  # 工具
  intl: ^0.18.0
  path_provider: ^2.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  retrofit_generator: ^7.0.0
```

---

## 六、开发里程碑

### 第 1 月：项目搭建
- [ ] Flutter 环境配置
- [ ] 项目脚手架创建
- [ ] 基础 UI 组件库
- [ ] API 服务封装
- [ ] 登录注册页面

### 第 2 月：核心功能
- [ ] 首页开发
- [ ] 图片上传功能
- [ ] 档案列表页
- [ ] 档案详情页
- [ ] OCR 状态轮询

### 第 3 月：完善优化
- [ ] 指标趋势图
- [ ] 用药提醒功能
- [ ] 推送通知
- [ ] 性能优化
- [ ] 测试与修复

---

## 七、UI 设计规范

### 配色方案

```dart
// 主色调
static const primaryBlue = Color(0xFF1890FF);    // 健康蓝
static const lifeGreen = Color(0xFF52C41A);      // 生命绿

// 辅助色
static const warningOrange = Color(0xFFFA8C16);  // 警告
static const errorRed = Color(0xFFF5222D);       // 错误
static const successGreen = Color(0xFF73D13D);   // 成功

// 中性色
static const textPrimary = Color(0xFF333333);
static const textSecondary = Color(0xFF666666);
static const textHint = Color(0xFF999999);
static const divider = Color(0xFFE8E8E8);
static const background = Color(0xFFF5F5F5);
```

### 字体规范

```dart
// 字体大小
static const textSizeSmall = 12.0;
static const textSizeNormal = 14.0;
static const textSizeMedium = 16.0;
static const textSizeLarge = 18.0;
static const textSizeXLarge = 24.0;

// 字体粗细
static const fontWeightNormal = FontWeight.w400;
static const fontWeightMedium = FontWeight.w500;
static const fontWeightBold = FontWeight.w600;
```

---

**最后更新：** 2026-03-08
