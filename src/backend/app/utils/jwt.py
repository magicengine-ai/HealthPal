"""
JWT Token 工具
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas.common import TokenData


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问 Token
    
    Args:
        data: Token 负载数据
        expires_delta: Token 有效期增量（可选）
        
    Returns:
        JWT Token 字符串
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    验证 Token
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        TokenData 对象，验证失败返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        uuid: str = payload.get("sub")
        if uuid is None:
            return None
        return TokenData(uuid=uuid)
    except JWTError:
        return None


def decode_token(token: str) -> Optional[dict]:
    """
    解码 Token（获取完整 payload）
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        解码后的 payload 字典，验证失败返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
