"""
用户 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.common import ResponseModel
from app.services.user_service import UserService
from app.services.file_service import FileService
from app.utils.validator import validate_email

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/profile", response_model=ResponseModel, summary="获取用户资料")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户资料"""
    user_service = UserService(db)
    profile = await user_service.get_user_profile(current_user)
    
    return ResponseModel(
        code=0,
        data=profile
    )


@router.put("/profile", response_model=ResponseModel, summary="更新用户资料")
async def update_user_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户资料"""
    user_service = UserService(db)
    
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # 验证邮箱
    if "email" in update_data and update_data["email"]:
        if not validate_email(update_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱格式错误"
            )
        
        # 检查邮箱是否已被使用
        exists = await user_service.check_email_exists(
            update_data["email"],
            exclude_user_id=current_user.id
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )
    
    user = await user_service.update_profile(current_user, update_data)
    
    return ResponseModel(
        code=0,
        message="更新成功"
    )


@router.post("/avatar", response_model=ResponseModel, summary="上传头像")
async def upload_avatar(
    file: UploadFile = File(..., description="头像图片"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传用户头像"""
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件格式，支持 JPG/PNG/GIF"
        )
    
    # 读取文件
    content = await file.read()
    
    # 验证大小（2MB）
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小超过 2MB"
        )
    
    file_service = FileService()
    user_service = UserService(db)
    
    # 上传文件
    file_url = await file_service.upload_file(
        content=content,
        filename=file.filename,
        content_type=file.content_type,
        record_uuid=f"avatar_{current_user.uuid}"
    )
    
    # 更新用户头像
    await user_service.update_avatar(current_user, file_url)
    
    return ResponseModel(
        code=0,
        message="上传成功",
        data={"avatar_url": file_url}
    )


@router.post("/bind-email", response_model=ResponseModel, summary="绑定邮箱")
async def bind_email(
    email: str,
    verify_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """绑定邮箱"""
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱格式错误"
        )
    
    user_service = UserService(db)
    
    # 检查邮箱是否已被使用
    exists = await user_service.check_email_exists(
        email,
        exclude_user_id=current_user.id
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被使用"
        )
    
    # TODO: 验证邮箱验证码
    
    # 绑定邮箱
    success = await user_service.bind_email(current_user, email)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="绑定失败"
        )
    
    return ResponseModel(
        code=0,
        message="绑定成功"
    )


@router.get("/statistics", response_model=ResponseModel, summary="获取用户统计")
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户统计数据"""
    user_service = UserService(db)
    
    stats = await user_service.get_user_statistics(current_user)
    
    return ResponseModel(
        code=0,
        data=stats
    )


@router.post("/delete-account", response_model=ResponseModel, summary="删除账户")
async def delete_account(
    password: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除账户（软删除）
    
    需要验证密码
    """
    from app.utils.password import verify_password
    
    # 验证密码
    if not verify_password(password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码错误"
        )
    
    user_service = UserService(db)
    
    success = await user_service.delete_account(current_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="删除失败"
        )
    
    return ResponseModel(
        code=0,
        message="账户已删除"
    )
