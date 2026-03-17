"""
认证 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.common import ResponseModel, TokenData
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.utils.validator import validate_phone, validate_password, validate_verify_code
from app.core.config import settings
import uuid

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ResponseModel, summary="用户注册")
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    
    - **phone**: 手机号（11 位中国大陆手机号）
    - **password**: 密码（6-32 位）
    - **verify_code**: 短信验证码
    - **nickname**: 昵称（可选）
    """
    # 验证手机号
    if not validate_phone(user_data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式错误"
        )
    
    # 验证密码
    is_valid, msg = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    
    # 验证验证码
    if not validate_verify_code(user_data.verify_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码格式错误"
        )
    
    auth_service = AuthService(db)
    
    # 验证短信验证码（开发环境跳过）
    if not settings.DEBUG:
        if not await auth_service.verify_sms_code(user_data.phone, user_data.verify_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )
    
    # 检查手机号是否已注册
    existing_user = await auth_service.get_user_by_phone(user_data.phone)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已注册"
        )
    
    # 创建用户
    user = await auth_service.create_user(
        phone=user_data.phone,
        password=user_data.password,
        nickname=user_data.nickname
    )
    
    # 生成 Token
    access_token = await auth_service.create_access_token(user.uuid)
    
    return ResponseModel(
        code=0,
        message="注册成功",
        data={
            "uuid": user.uuid,
            "token": access_token,
            "token_type": "Bearer",
            "expires_in": 604800,  # 7 天
        }
    )


@router.post("/login", response_model=ResponseModel, summary="用户登录")
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    
    返回 JWT Token 和用户信息
    """
    # 验证手机号
    if not validate_phone(login_data.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式错误"
        )
    
    auth_service = AuthService(db)
    
    # 验证用户
    user = await auth_service.authenticate_user(
        phone=login_data.phone,
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 Token
    access_token = await auth_service.create_access_token(user.uuid)
    
    user_service = UserService(db)
    profile = await user_service.get_user_profile(user)
    
    return ResponseModel(
        code=0,
        message="登录成功",
        data={
            "token": access_token,
            "token_type": "Bearer",
            "expires_in": 604800,  # 7 天
            "user": profile
        }
    )


@router.post("/logout", response_model=ResponseModel, summary="用户登出")
async def logout(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登出
    
    将 Token 加入黑名单
    """
    auth_service = AuthService(db)
    await auth_service.blacklist_token(token)
    
    return ResponseModel(
        code=0,
        message="登出成功"
    )


@router.get("/me", response_model=ResponseModel, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前登录用户信息"""
    user_service = UserService(db)
    profile = await user_service.get_user_profile(current_user)
    
    return ResponseModel(
        code=0,
        data=profile
    )


@router.post("/send-code", response_model=ResponseModel, summary="发送短信验证码")
async def send_verification_code(
    phone: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    发送短信验证码
    
    - **phone**: 手机号
    """
    # 验证手机号
    if not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式错误"
        )
    
    auth_service = AuthService(db)
    
    # 发送验证码
    success = await auth_service.send_sms_code(phone)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="发送过于频繁，请稍后再试"
        )
    
    return ResponseModel(
        code=0,
        message="验证码已发送",
        data={"expire_in": 300}
    )


@router.post("/reset-password", response_model=ResponseModel, summary="重置密码")
async def reset_password(
    phone: str,
    verify_code: str,
    new_password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码
    
    - **phone**: 手机号
    - **verify_code**: 短信验证码
    - **new_password**: 新密码
    """
    auth_service = AuthService(db)
    
    # 验证验证码
    if not await auth_service.verify_sms_code(phone, verify_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
    # 查询用户
    user = await auth_service.get_user_by_phone(phone)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新密码
    success = await auth_service.change_password(user, user.password_hash, new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码更新失败"
        )
    
    return ResponseModel(
        code=0,
        message="密码重置成功"
    )


@router.post("/change-password", response_model=ResponseModel, summary="修改密码")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码（需要登录）
    
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    auth_service = AuthService(db)
    
    success = await auth_service.change_password(
        current_user,
        old_password,
        new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    return ResponseModel(
        code=0,
        message="密码修改成功"
    )
