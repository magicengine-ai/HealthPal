# HealthPal 数据库设计

## 一、MySQL - 关系型数据

### 1.1 用户表 (users)

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    gender TINYINT DEFAULT 0 COMMENT '0:未知 1:男 2:女',
    birthday DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_phone (phone),
    INDEX idx_email (email),
    INDEX idx_uuid (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.2 家庭成员表 (family_members)

```sql
CREATE TABLE family_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    member_uuid VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    relation VARCHAR(20) COMMENT '本人/父亲/母亲/配偶/子女等',
    gender TINYINT DEFAULT 0,
    birthday DATE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.3 健康档案表 (health_records)

```sql
CREATE TABLE health_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL,
    member_id BIGINT,
    record_type VARCHAR(50) NOT NULL COMMENT '体检报告/病历/处方/检查单',
    title VARCHAR(200) NOT NULL,
    hospital VARCHAR(100),
    department VARCHAR(50),
    record_date DATE NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ocr_status TINYINT DEFAULT 0 COMMENT '0:待识别 1:识别中 2:已完成 3:失败',
    ocr_result JSON COMMENT 'OCR 识别结果',
    structured_data JSON COMMENT '结构化数据',
    tags JSON COMMENT '标签数组',
    file_urls JSON COMMENT '文件 URL 列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (member_id) REFERENCES family_members(id),
    INDEX idx_user_id (user_id),
    INDEX idx_member_id (member_id),
    INDEX idx_record_date (record_date),
    INDEX idx_record_type (record_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.4 健康指标表 (health_indicators)

```sql
CREATE TABLE health_indicators (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    record_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    member_id BIGINT,
    indicator_code VARCHAR(50) NOT NULL COMMENT '指标编码 BP_HIGH/BS/GLU 等',
    indicator_name VARCHAR(100) NOT NULL COMMENT '指标名称',
    value DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    reference_min DECIMAL(10,2),
    reference_max DECIMAL(10,2),
    status TINYINT DEFAULT 0 COMMENT '0:正常 1:偏低 2:偏高 3:异常',
    measure_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES health_records(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_code (user_id, indicator_code),
    INDEX idx_measure_date (measure_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.5 用药提醒表 (medication_reminders)

```sql
CREATE TABLE medication_reminders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    member_id BIGINT,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) COMMENT '每次剂量',
    frequency VARCHAR(50) COMMENT '频次 每日 3 次',
    reminder_times JSON COMMENT '提醒时间 ["08:00","12:00","20:00"]',
    start_date DATE NOT NULL,
    end_date DATE,
    status TINYINT DEFAULT 1 COMMENT '0:停用 1:启用',
    completed_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 1.6 提醒记录表 (reminder_logs)

```sql
CREATE TABLE reminder_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reminder_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    actual_time DATETIME,
    status TINYINT DEFAULT 0 COMMENT '0:待发送 1:已发送 2:已确认 3:已忽略',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reminder_id) REFERENCES medication_reminders(id),
    INDEX idx_scheduled_time (scheduled_time),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 二、MongoDB - 文档型数据

### 2.1 用户行为日志 (user_behaviors)

```javascript
{
    _id: ObjectId,
    userId: String,
    action: String,  // view/upload/search/export
    targetType: String,  // record/indicator/report
    targetId: String,
    metadata: Object,
    timestamp: Date,
    deviceId: String,
    ip: String
}
```

### 2.2 AI 分析结果 (ai_analyses)

```javascript
{
    _id: ObjectId,
    userId: String,
    memberId: String,
    analysisType: String,  // trend/risk/suggestion
    inputData: Object,
    result: {
        summary: String,
        scores: Object,
        risks: Array,
        suggestions: Array
    },
    modelVersion: String,
    createdAt: Date,
    expiresAt: Date
}
```

### 2.3 设备数据缓存 (device_data_cache)

```javascript
{
    _id: ObjectId,
    userId: String,
    deviceId: String,
    deviceType: String,  // blood_pressure/glucose/weight
    measurements: [{
        timestamp: Date,
        data: Object,
        synced: Boolean
    }],
    lastSyncAt: Date,
    updatedAt: Date
}
```

---

## 三、Redis - 缓存

### 3.1 Key 命名规范

```
# 用户 Session
session:{uuid}

# 用户 Token 黑名单
token:blacklist:{jti}

# 验证码
sms:code:{phone}
email:code:{email}

# 热点数据缓存
user:profile:{userId}
record:detail:{recordId}

# 分布式锁
lock:upload:{userId}
lock:ocr:{recordId}

# 限流计数
ratelimit:api:{userId}:{endpoint}
```

### 3.2 过期时间策略

| Key 类型 | 过期时间 | 说明 |
|----------|----------|------|
| session | 7 天 | 用户登录态 |
| token:blacklist | Token 剩余有效期 | 防止重放 |
| sms:code | 5 分钟 | 短信验证码 |
| user:profile | 30 分钟 | 用户资料 |
| ratelimit | 1 分钟 | 限流窗口 |

---

## 四、索引优化建议

### 4.1 MySQL 索引

```sql
-- 复合索引示例
CREATE INDEX idx_user_date_type ON health_records(user_id, record_date, record_type);
CREATE INDEX idx_user_indicator_date ON health_indicators(user_id, indicator_code, measure_date);

-- 全文索引（搜索功能）
ALTER TABLE health_records ADD FULLTEXT INDEX ft_search (title, hospital);
```

### 4.2 MongoDB 索引

```javascript
// 用户行为分析
db.user_behaviors.createIndex({ userId: 1, timestamp: -1 });

// AI 分析结果
db.ai_analyses.createIndex({ userId: 1, analysisType: 1, createdAt: -1 });
db.ai_analyses.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
```

---

## 五、数据迁移策略

### 5.1 迁移工具

使用 golang-migrate 或 gorm-migrator 进行数据库版本管理

### 5.2 迁移流程

```bash
# 创建新迁移
migrate create -ext sql -dir db/migrations add_user_avatar

# 执行迁移
migrate -path db/migrations -database "mysql://user:pass@tcp(host:3306)/db" up
```

---

**最后更新：** 2026-03-08
