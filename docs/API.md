# HealthPal API 文档

**版本：** v1  
**基础 URL：** `https://api.healthpal.com/v1`

---

## 一、认证机制

### 1.1 获取 Token

```http
POST /auth/login
Content-Type: application/json

{
    "phone": "13800138000",
    "password": "encrypted_password",
    "verify_code": "123456"
}

Response:
{
    "code": 0,
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIs...",
        "expires_in": 604800,
        "user": {
            "uuid": "xxx",
            "nickname": "xxx",
            "avatar": "xxx"
        }
    }
}
```

### 1.2 Token 使用

所有需要认证的接口需在 Header 中携带：

```http
Authorization: Bearer {token}
```

---

## 二、用户接口

### 2.1 用户注册

```http
POST /auth/register
Content-Type: application/json

{
    "phone": "13800138000",
    "password": "encrypted_password",
    "verify_code": "123456",
    "nickname": "张三"
}
```

### 2.2 获取用户信息

```http
GET /user/profile

Response:
{
    "code": 0,
    "data": {
        "uuid": "xxx",
        "phone": "138****8000",
        "email": "",
        "nickname": "张三",
        "avatar": "https://...",
        "gender": 1,
        "birthday": "1990-01-01"
    }
}
```

### 2.3 更新用户信息

```http
PUT /user/profile
Content-Type: application/json

{
    "nickname": "新昵称",
    "avatar": "https://...",
    "gender": 1,
    "birthday": "1990-01-01"
}
```

---

## 三、家庭成员接口

### 3.1 添加家庭成员

```http
POST /family/members
Content-Type: application/json

{
    "name": "李四",
    "relation": "父亲",
    "gender": 1,
    "birthday": "1965-05-15",
    "phone": "13900139000"
}
```

### 3.2 获取家庭成员列表

```http
GET /family/members

Response:
{
    "code": 0,
    "data": {
        "members": [
            {
                "uuid": "xxx",
                "name": "本人",
                "relation": "本人",
                "gender": 1,
                "birthday": "1990-01-01"
            },
            {
                "uuid": "xxx",
                "name": "李四",
                "relation": "父亲",
                "gender": 1,
                "birthday": "1965-05-15"
            }
        ]
    }
}
```

---

## 四、健康档案接口

### 4.1 上传健康文档

```http
POST /records/upload
Content-Type: multipart/form-data

file: [图片/PDF 文件]
member_id: [可选，家庭成员 ID]
record_type: "体检报告"
title: "2026 年年度体检"
record_date: "2026-03-01"

Response:
{
    "code": 0,
    "data": {
        "record_id": "xxx",
        "ocr_status": 0
    }
}
```

### 4.2 获取档案列表

```http
GET /records?member_id=xxx&record_type=体检报告&page=1&page_size=20

Response:
{
    "code": 0,
    "data": {
        "total": 10,
        "records": [
            {
                "uuid": "xxx",
                "title": "2026 年年度体检",
                "record_type": "体检报告",
                "hospital": "北京协和医院",
                "record_date": "2026-03-01",
                "ocr_status": 2,
                "file_urls": ["https://..."]
            }
        ]
    }
}
```

### 4.3 获取档案详情

```http
GET /records/{record_id}

Response:
{
    "code": 0,
    "data": {
        "uuid": "xxx",
        "title": "2026 年年度体检",
        "record_type": "体检报告",
        "hospital": "北京协和医院",
        "department": "体检中心",
        "record_date": "2026-03-01",
        "structured_data": {
            "indicators": [
                {
                    "code": "BP_HIGH",
                    "name": "收缩压",
                    "value": 120,
                    "unit": "mmHg",
                    "reference_min": 90,
                    "reference_max": 140,
                    "status": 0
                }
            ]
        },
        "file_urls": ["https://..."]
    }
}
```

### 4.4 删除档案

```http
DELETE /records/{record_id}
```

---

## 五、健康指标接口

### 5.1 获取指标趋势

```http
GET /indicators/trend?indicator_code=BP_HIGH&member_id=xxx&start_date=2025-01-01&end_date=2026-03-08

Response:
{
    "code": 0,
    "data": {
        "indicator": {
            "code": "BP_HIGH",
            "name": "收缩压",
            "unit": "mmHg"
        },
        "points": [
            {"date": "2025-06-01", "value": 118},
            {"date": "2025-12-01", "value": 122},
            {"date": "2026-03-01", "value": 120}
        ],
        "statistics": {
            "avg": 120,
            "min": 115,
            "max": 125
        }
    }
}
```

### 5.2 手动添加指标

```http
POST /indicators
Content-Type: application/json

{
    "member_id": "xxx",
    "indicator_code": "BP_HIGH",
    "value": 120,
    "unit": "mmHg",
    "measure_date": "2026-03-08"
}
```

---

## 六、用药提醒接口

### 6.1 创建用药提醒

```http
POST /medications/reminders
Content-Type: application/json

{
    "member_id": "xxx",
    "medicine_name": "阿司匹林肠溶片",
    "dosage": "100mg",
    "frequency": "每日 1 次",
    "reminder_times": ["08:00"],
    "start_date": "2026-03-08",
    "end_date": "2026-06-08"
}
```

### 6.2 获取提醒列表

```http
GET /medications/reminders?status=1

Response:
{
    "code": 0,
    "data": {
        "reminders": [
            {
                "id": 1,
                "medicine_name": "阿司匹林肠溶片",
                "dosage": "100mg",
                "frequency": "每日 1 次",
                "reminder_times": ["08:00"],
                "status": 1
            }
        ]
    }
}
```

### 6.3 确认用药

```http
POST /medications/reminders/{reminder_id}/confirm
Content-Type: application/json

{
    "take_time": "2026-03-08 08:05:00"
}
```

---

## 七、AI 分析接口

### 7.1 获取健康分析报告

```http
GET /ai/analysis/report?member_id=xxx

Response:
{
    "code": 0,
    "data": {
        "health_score": 85,
        "summary": "整体健康状况良好...",
        "risks": [
            {
                "level": "low",
                "name": "心血管疾病风险",
                "description": "基于血压和血脂指标..."
            }
        ],
        "suggestions": [
            {
                "category": "饮食",
                "content": "建议减少盐分摄入..."
            },
            {
                "category": "运动",
                "content": "每周保持 150 分钟中等强度运动..."
            }
        ]
    }
}
```

---

## 八、错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | Token 无效或过期 |
| 1003 | 权限不足 |
| 2001 | 资源不存在 |
| 2002 | 资源已存在 |
| 3001 | OCR 识别失败 |
| 3002 | AI 分析失败 |
| 5000 | 服务器内部错误 |

---

## 九、限流策略

| 接口类型 | 限流 | 说明 |
|----------|------|------|
| 认证接口 | 5 次/分钟 | 防止暴力破解 |
| 上传接口 | 10 次/分钟 | 防止滥用 |
| 普通查询 | 100 次/分钟 | 正常查询 |
| AI 分析 | 20 次/小时 | 计算密集型 |

---

**最后更新：** 2026-03-08
