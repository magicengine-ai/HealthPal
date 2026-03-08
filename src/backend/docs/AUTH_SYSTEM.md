# HealthPal 认证系统文档

## 一、认证流程

### 1.1 用户注册流程

```
1. 用户输入手机号 → 点击获取验证码
2. 后端发送短信验证码（6 位数字，5 分钟有效）
3. 用户输入验证码 + 密码 → 提交注册
4. 后端验证验证码 → 创建用户 → 返回 JWT Token
5. 客户端保存 Token，后续请求携带 Token
```

### 1.2 用户登录流程

```
1. 用户输入手机号 + 密码
2. 后端验证密码 → 返回 JWT Token
3. 客户端保存 Token
```

### 1.3 密码重置流程

```
1. 用户输入手机号 → 获取验证码
2. 输入验证码 + 新密码 → 提交
3. 后端验证验证码 → 更新密码
```

---

## 二、API 接口

### 2.1 发送短信验证码

```http
POST /api/v1/auth/send-code
Content-Type: application/json

{
    "phone": "13800138000"
}

Response:
{
    "message": "验证码已发送",
    "expire_in": 300
}
```

**限制：**
- 60 秒内只能发送一次
- 验证码 5 分钟有效
- 最多尝试 3 次验证

---

### 2.2 用户注册

```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "phone": "13800138000",
    "password": "test123456",
    "verify_code": "123456",
    "nickname": "张三"
}

Response:
{
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 604800,
    "user": {
        "uuid": "xxx",
        "phone": "13800138000",
        "nickname": "张三",
        "avatar_url": null,
        "gender": 0,
        "birthday": null
    }
}
```

---

### 2.3 用户登录

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "phone": "13800138000",
    "password": "test123456"
}

Response: 同注册接口
```

---

### 2.4 获取当前用户信息

```http
GET /api/v1/auth/me
Authorization: Bearer {token}

Response:
{
    "uuid": "xxx",
    "phone": "138****8000",
    "nickname": "张三",
    "avatar_url": "https://...",
    "gender": 1,
    "birthday": "1990-01-01",
    "email": "xxx@example.com"
}
```

---

### 2.5 更新用户信息

```http
PUT /api/v1/users/profile
Authorization: Bearer {token}
Content-Type: application/json

{
    "nickname": "新昵称",
    "avatar_url": "https://...",
    "gender": 1,
    "birthday": "1990-01-01",
    "email": "xxx@example.com"
}
```

---

### 2.6 修改密码（已登录）

```http
POST /api/v1/auth/change-password
Authorization: Bearer {token}
Content-Type: application/json

{
    "old_password": "test123456",
    "new_password": "new123456"
}
```

---

### 2.7 重置密码（未登录）

```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
    "phone": "13800138000",
    "verify_code": "123456",
    "new_password": "new123456"
}
```

---

### 2.8 用户登出

```http
POST /api/v1/auth/logout
Authorization: Bearer {token}

Response:
{
    "message": "登出成功"
}
```

---

### 2.9 注销用户

```http
DELETE /api/v1/users/profile
Authorization: Bearer {token}

Response:
{
    "message": "账号已注销"
}
```

---

## 三、错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 参数错误/验证码错误 |
| 401 | 认证失败（Token 无效/过期） |
| 404 | 用户不存在 |
| 429 | 请求过于频繁 |

---

## 四、安全机制

### 4.1 密码加密

- 使用 **bcrypt** 算法
- 自动加盐
- 不可逆加密

### 4.2 JWT Token

- 有效期：7 天
- 算法：HS256
- 包含用户 UUID 和 Token 类型

### 4.3 验证码安全

- 6 位随机数字
- 5 分钟有效期
- 60 秒发送间隔
- 3 次验证失败锁定

### 4.4 Token 黑名单

- 登出时 Token 加入黑名单
- 黑名单自动过期（Token 剩余有效期）
- Redis 存储

---

## 五、测试

### 运行测试脚本

```bash
cd src/backend
python tests/test_auth.py
```

### 使用 Swagger UI 测试

1. 启动服务：`uvicorn app.main:app --reload`
2. 访问：http://localhost:8000/docs
3. 点击Authorize 输入 Token

---

## 六、依赖服务

| 服务 | 用途 | 端口 |
|------|------|------|
| MySQL | 用户数据存储 | 3306 |
| Redis | 验证码/Token 黑名单 | 6379 |
| MongoDB | 日志存储（可选） | 27017 |

---

**最后更新：** 2026-03-08
