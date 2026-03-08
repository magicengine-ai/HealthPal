# 嵌入式设备接入模块

## 一、概述

本模块负责健康设备（血压计、血糖仪、体重秤等）的蓝牙 BLE 接入和数据同步。

## 二、支持设备

| 设备类型 | 协议 | 状态 |
|----------|------|------|
| 欧姆龙血压计 | BLE GATT | TODO |
| 鱼跃血糖仪 | BLE 私有 | TODO |
| 小米体重秤 2 | BLE GATT | TODO |
| 华为手环 | BLE GATT | TODO |

## 三、目录结构

```
embedded/
├── firmware/          # 固件代码
│   ├── main.c         # 主程序
│   ├── ble_stack.c    # BLE 协议栈
│   └── drivers/       # 设备驱动
├── protocols/         # 协议解析
│   ├── ble_gatt.c     # GATT 服务
│   ├── omron.c        # 欧姆龙协议
│   └── xiaomi.c       # 小米协议
└── docs/              # 协议文档
```

## 四、BLE GATT 服务定义

### 4.1 血压计服务

```c
// 血压计 GATT 服务 UUID
#define BLOOD_PRESSURE_SERVICE_UUID    0x1810
#define BLOOD_PRESSURE_MEASUREMENT_UUID 0x2A35

// 血压测量数据结构
typedef struct {
    uint8_t flags;
    uint16_t systolic;      // 收缩压
    uint16_t diastolic;     // 舒张压
    uint16_t pulse;         // 脉搏
    uint8_t status;         // 测量状态
    char timestamp[20];     // 时间戳
} bp_measurement_t;
```

### 4.2 体重秤服务

```c
// 体重秤 GATT 服务 UUID
#define WEIGHT_SCALE_SERVICE_UUID    0x181D
#define WEIGHT_MEASUREMENT_UUID      0x2A9D

// 体重测量数据结构
typedef struct {
    uint8_t flags;
    float weight;           // 体重 (kg)
    float body_fat;         // 体脂率 (%)
    uint8_t unit;           // 单位
    char timestamp[20];     // 时间戳
} weight_measurement_t;
```

## 五、数据同步流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BLE 设备   │───▶│  手机 App   │───▶│  云端服务   │
└─────────────┘    └─────────────┘    └─────────────┘
     │                   │                   │
     │ 1. BLE 广播发现    │                   │
     │ 2. 连接 & 配对     │                   │
     │ 3. 读取测量数据    │                   │
     │                   │ 4. 数据加密上传    │
     │                   │──────────────────▶│
     │                   │ 5. 云端存储分析    │
     │                   │◀──────────────────│
     │                   │ 6. 同步确认        │
```

## 六、开发计划

### Phase 3.1 (第 7 月)
- [ ] BLE 协议栈集成
- [ ] 血压计数据解析
- [ ] 基础数据同步

### Phase 3.2 (第 8 月)
- [ ] 血糖仪协议适配
- [ ] 体重秤协议适配
- [ ] 多设备管理

### Phase 3.3 (第 9 月)
- [ ] OTA 固件升级
- [ ] 离线数据缓存
- [ ] 设备绑定管理

## 七、参考文档

- [Bluetooth SIG - Health Device Profiles](https://www.bluetooth.com/specifications/specs/)
- [Nordic BLE Stack](https://www.nordicsemi.com/Products/Development-software/nrf-connect-sdk)
- [ESP32 BLE Arduino](https://github.com/nkolban/ESP32_BLE_Arduino)
