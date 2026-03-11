"""
简单测试脚本 - 直接导入应用测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from app.main import app
from fastapi.testclient import TestClient

print("🧪 HealthPal 认证系统测试（简化版）")
print("=" * 60)

# 使用 FastAPI TestClient（同步测试）
client = TestClient(app)

# 测试健康检查
print("\n📊 1. 健康检查...")
response = client.get("/health")
print(f"   状态码：{response.status_code}")
print(f"   响应：{response.json()}")
assert response.status_code == 200, "健康检查失败"
print("   ✅ 通过")

# 测试根路径
print("\n🏠 2. 根路径...")
response = client.get("/")
print(f"   状态码：{response.status_code}")
print(f"   响应：{response.json()}")
assert response.status_code == 200, "根路径失败"
print("   ✅ 通过")

# 测试发送验证码
print("\n📱 3. 发送验证码...")
response = client.post("/api/v1/auth/send-code", json={"phone": "13800138000"})
print(f"   状态码：{response.status_code}")
print(f"   响应：{response.json()}")
# 可能成功或因 Redis 失败
if response.status_code == 200:
    print("   ✅ 验证码发送成功")
elif response.status_code == 429:
    print("   ⚠️  发送频繁（预期行为）")
else:
    print(f"   ⚠️  Redis 未连接：{response.json()}")

# 测试用户注册（验证码用 123456）
print("\n👤 4. 用户注册...")
response = client.post("/api/v1/auth/register", json={
    "phone": "13800138000",
    "password": "test123456",
    "verify_code": "123456",
    "nickname": "测试用户"
})
print(f"   状态码：{response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data["token"]
    print(f"   ✅ 注册成功")
    print(f"   Token: {token[:30]}...")
    print(f"   用户 UUID: {data['user']['uuid']}")
elif response.status_code == 400:
    print(f"   ⚠️  {response.json()}")
    print("   （可能已注册或验证码错误）")
else:
    print(f"   ❌ 失败：{response.json()}")

# 测试用户登录
print("\n🔐 5. 用户登录...")
response = client.post("/api/v1/auth/login", json={
    "phone": "13800138000",
    "password": "test123456"
})
print(f"   状态码：{response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data["token"]
    print(f"   ✅ 登录成功")
    print(f"   Token: {token[:30]}...")
else:
    print(f"   ❌ 失败：{response.json()}")
    token = None

# 测试获取用户信息（需要 Token）
if token:
    print("\n📋 6. 获取用户信息...")
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"   状态码：{response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ 用户信息：{response.json()}")
    else:
        print(f"   ❌ 失败：{response.json()}")
    
    # 测试更新用户信息
    print("\n✏️  7. 更新用户信息...")
    response = client.put(
        "/api/v1/users/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={"nickname": "新昵称", "gender": 1}
    )
    print(f"   状态码：{response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ 更新成功：{response.json()}")
    else:
        print(f"   ❌ 失败：{response.json()}")

print("\n" + "=" * 60)
print("✅ 测试完成")
print("\n📖 API 文档：http://localhost:8000/docs")
