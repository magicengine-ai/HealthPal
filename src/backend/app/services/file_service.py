"""
文件存储服务
"""
import os
import uuid
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from app.core.config import settings


class FileService:
    """文件存储服务类"""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        初始化文件服务
        
        Args:
            base_dir: 基础目录（可选，默认使用配置中的 UPLOAD_DIR）
        """
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(settings.UPLOAD_DIR)
        
        # 确保基础目录存在
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_filename(self, original_filename: str, record_uuid: str) -> str:
        """
        生成安全的文件名
        
        Args:
            original_filename: 原始文件名
            record_uuid: 档案 UUID
            
        Returns:
            新文件名
        """
        # 获取文件扩展名
        ext = Path(original_filename).suffix.lower()
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        return f"{record_uuid}_{timestamp}_{unique_id}{ext}"
    
    def _get_file_path(self, filename: str, record_uuid: str) -> Path:
        """
        获取文件存储路径
        
        Args:
            filename: 文件名
            record_uuid: 档案 UUID
            
        Returns:
            文件完整路径
        """
        # 按日期创建子目录
        date_dir = datetime.now().strftime("%Y/%m/%d")
        file_dir = self.base_dir / record_uuid / date_dir
        file_dir.mkdir(parents=True, exist_ok=True)
        
        return file_dir / filename
    
    async def upload_file(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        record_uuid: str
    ) -> str:
        """
        上传文件
        
        Args:
            content: 文件内容（bytes）
            filename: 文件名
            content_type: MIME 类型
            record_uuid: 档案 UUID
            
        Returns:
            文件 URL/路径
        """
        # 生成安全文件名
        safe_filename = self._generate_filename(filename, record_uuid)
        
        # 获取文件路径
        file_path = self._get_file_path(safe_filename, record_uuid)
        
        # 写入文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 返回相对路径（生产环境可改为 CDN URL）
        relative_path = file_path.relative_to(self.base_dir)
        return f"/uploads/{relative_path}"
    
    async def upload_files(
        self,
        files: List[dict],
        record_uuid: str
    ) -> List[str]:
        """
        批量上传文件
        
        Args:
            files: 文件列表 [{"content": bytes, "filename": str, "content_type": str}, ...]
            record_uuid: 档案 UUID
            
        Returns:
            文件 URL 列表
        """
        urls = []
        
        for file_info in files:
            url = await self.upload_file(
                content=file_info["content"],
                filename=file_info["filename"],
                content_type=file_info["content_type"],
                record_uuid=record_uuid
            )
            urls.append(url)
        
        return urls
    
    async def get_file(self, file_path: str) -> Optional[bytes]:
        """
        获取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容或 None
        """
        full_path = self.base_dir / file_path.lstrip("/uploads/")
        
        if not full_path.exists():
            return None
        
        with open(full_path, "rb") as f:
            return f.read()
    
    async def delete_file(self, file_path: str) -> bool:
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            删除结果：True/False
        """
        full_path = self.base_dir / file_path.lstrip("/uploads/")
        
        if not full_path.exists():
            return False
        
        full_path.unlink()
        return True
    
    async def delete_files(self, file_paths: List[str]) -> int:
        """
        批量删除文件
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            成功删除的文件数量
        """
        count = 0
        
        for file_path in file_paths:
            if await self.delete_file(file_path):
                count += 1
        
        return count
    
    def get_file_size(self, file_path: str) -> int:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（字节）
        """
        full_path = self.base_dir / file_path.lstrip("/uploads/")
        
        if not full_path.exists():
            return 0
        
        return full_path.stat().st_size
    
    def validate_file(
        self,
        content: bytes,
        content_type: str,
        max_size: Optional[int] = None
    ) -> tuple[bool, Optional[str]]:
        """
        验证文件
        
        Args:
            content: 文件内容
            content_type: MIME 类型
            max_size: 最大文件大小（字节）
            
        Returns:
            (验证结果，错误信息)
        """
        # 验证文件大小
        file_size = len(content)
        if max_size is None:
            max_size = settings.MAX_UPLOAD_SIZE
        
        if file_size > max_size:
            return False, f"文件大小超过限制 ({max_size / 1024 / 1024:.1f}MB)"
        
        # 验证文件类型
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/gif",
            "application/pdf",
        ]
        
        if content_type not in allowed_types:
            return False, "不支持的文件格式"
        
        return True, None
