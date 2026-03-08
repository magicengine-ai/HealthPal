-- HealthPal 数据库初始化脚本
-- 执行：mysql -u root -p < init.sql

-- 创建数据库
CREATE DATABASE IF NOT EXISTS healthpal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER IF NOT EXISTS 'healthpal'@'%' IDENTIFIED BY 'healthpal_pass';
GRANT ALL PRIVILEGES ON healthpal.* TO 'healthpal'@'%';
FLUSH PRIVILEGES;

-- 使用数据库
USE healthpal;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
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

-- 家庭成员表
CREATE TABLE IF NOT EXISTS family_members (
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

-- 健康档案表
CREATE TABLE IF NOT EXISTS health_records (
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

-- 健康指标表
CREATE TABLE IF NOT EXISTS health_indicators (
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

-- 用药提醒表
CREATE TABLE IF NOT EXISTS medication_reminders (
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

-- 提醒记录表
CREATE TABLE IF NOT EXISTS reminder_logs (
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

-- 插入测试用户（密码：123456）
-- INSERT INTO users (uuid, phone, password_hash, nickname) VALUES 
-- ('test-user-001', '13800138000', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', '测试用户');
