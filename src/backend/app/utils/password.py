"""
密码加密工具
"""
import bcrypt
from typing import Union


def hash_password(password: str) -> str:
    """
    对密码进行哈希加密
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码哈希
    """
    # bcrypt 最大支持 72 字节
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 原始密码
        hashed_password: 加密后的密码哈希
        
    Returns:
        验证结果：True/False
    """
    try:
        password_bytes = plain_password.encode('utf-8')[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    获取密码哈希（别名，保持兼容性）
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码哈希
    """
    return hash_password(password)
