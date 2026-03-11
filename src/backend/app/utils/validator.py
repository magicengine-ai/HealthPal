"""
数据验证工具
"""
import re
from typing import Optional
from pydantic import ValidationError


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 手机号字符串
        
    Returns:
        验证结果：True/False
    """
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱字符串
        
    Returns:
        验证结果：True/False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    验证密码强度
    
    Args:
        password: 密码字符串
        
    Returns:
        (验证结果，错误信息)
    """
    if len(password) < 6:
        return False, "密码长度至少 6 位"
    
    if len(password) > 32:
        return False, "密码长度不能超过 32 位"
    
    if not re.match(r"^[a-zA-Z0-9_@#$%^&+=!~.-]+$", password):
        return False, "密码只能包含字母、数字和特殊字符"
    
    return True, None


def validate_verify_code(code: str) -> bool:
    """
    验证验证码格式（6 位数字）
    
    Args:
        code: 验证码字符串
        
    Returns:
        验证结果：True/False
    """
    pattern = r"^\d{6}$"
    return bool(re.match(pattern, code))


def sanitize_string(value: str, max_length: int = 200) -> str:
    """
    清理字符串（去除首尾空格、限制长度）
    
    Args:
        value: 原始字符串
        max_length: 最大长度
        
    Returns:
        清理后的字符串
    """
    if not value:
        return ""
    
    value = value.strip()
    return value[:max_length]


def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """
    验证日期格式
    
    Args:
        date_str: 日期字符串
        format: 期望的日期格式
        
    Returns:
        验证结果：True/False
    """
    try:
        from datetime import datetime
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def validate_indicator_value(value: str) -> bool:
    """
    验证指标值格式（支持数字、范围、文本）
    
    Args:
        value: 指标值字符串
        
    Returns:
        验证结果：True/False
    """
    if not value or len(value) > 50:
        return False
    
    # 允许数字、小数点、正负号、范围符号
    pattern = r"^[-+]?[0-9]*\.?[0-9]+([/-][-+]?[0-9]*\.?[0-9]+)?$|^[a-zA-Z\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\s\-\+\(\)]*$"
    return bool(re.match(pattern, value))
