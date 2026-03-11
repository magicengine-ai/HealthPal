"""
认证系统测试脚本

测试认证系统的完整流程：
1. 发送验证码
2. 用户注册
3. 用户登录
4. 获取用户信息
5. 更新用户信息
6. 修改密码
7. 用户登出
"""
import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

# 测试手机号和密码
TEST_PHONE = "13800138000"
TEST_PASSWORD = "test123456"
TEST_NICKNAME = "测试用户"


async def test_auth_flow():
    """测试认证完整流程"""
    # 禁用代理
    import os
    os.environ['NO_PROXY'] = '*'
    os.environ['no_proxy'] = '*'
    
    transport = httpx.AsyncHTTPTransport(local_address="127.0.0.1")
    async with httpx.AsyncClient(transport=transport, proxies=None) as client:
        token = None
        current_password = TEST_PASSWORD
        
        # 1. 发送验证码
        print("\n📱 1. 发送验证码...")
        response = await client.post(
            f"{BASE_URL}/auth/send-code",
            json={"phone": TEST_PHONE}
        )
        print(f"   状态码：{response.status_code}")
        print(f"   响应：{response.json()}")
        
        # 从日志中获取验证码（实际项目中不会这样）
        # 这里假设验证码是 123456
        VERIFY_CODE = "123456"
        
        # 2. 用户注册
        print("\n👤 2. 用户注册...")
        response = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "phone": TEST_PHONE,
                "password": current_password,
                "verify_code": VERIFY_CODE,
                "nickname": TEST_NICKNAME
            }
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data["token"]
            print(f"   ✅ 注册成功，Token: {token[:20]}...")
            print(f"   用户 UUID: {data['user']['uuid']}")
        else:
            print(f"   ❌ 注册失败：{response.json()}")
            # 如果已注册，尝试登录
            print("\n🔐 尝试登录...")
            response = await client.post(
                f"{BASE_URL}/auth/login",
                json={
                    "phone": TEST_PHONE,
                    "password": current_password
                }
            )
            print(f"   状态码：{response.status_code}")
            if response.status_code == 200:
                data = response.json()
                token = data["token"]
                print(f"   ✅ 登录成功，Token: {token[:20]}...")
            else:
                print(f"   ❌ 登录失败：{response.json()}")
                return
        
        # 3. 获取用户信息
        print("\n📋 3. 获取用户信息...")
        response = await client.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 用户信息：{response.json()}")
        else:
            print(f"   ❌ 获取失败：{response.json()}")
        
        # 4. 更新用户信息
        print("\n✏️  4. 更新用户信息...")
        response = await client.put(
            f"{BASE_URL}/users/profile",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nickname": "新昵称",
                "gender": 1
            }
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 更新成功：{response.json()}")
        else:
            print(f"   ❌ 更新失败：{response.json()}")
        
        # 5. 修改密码
        print("\n🔑 5. 修改密码...")
        response = await client.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": current_password,
                "new_password": "new123456"
            }
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 密码修改成功")
            # 更新密码用于后续测试
            current_password = "new123456"
        else:
            print(f"   ❌ 密码修改失败：{response.json()}")
        
        # 6. 用户登出
        print("\n👋 6. 用户登出...")
        response = await client.post(
            f"{BASE_URL}/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 登出成功")
        else:
            print(f"   ❌ 登出失败：{response.json()}")
        
        # 7. 验证 Token 已失效
        print("\n🚫 7. 验证 Token 已失效...")
        response = await client.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   状态码：{response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Token 已失效，验证通过")
        else:
            print(f"   ❌ Token 仍然有效")


if __name__ == "__main__":
    print("🧪 HealthPal 认证系统测试")
    print("=" * 50)
    asyncio.run(test_auth_flow())
    print("\n" + "=" * 50)
    print("✅ 测试完成")
