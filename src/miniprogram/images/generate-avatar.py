#!/usr/bin/env python3
"""
生成默认头像图标
"""

from PIL import Image, ImageDraw

def create_default_avatar():
    """创建默认头像"""
    size = 200
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景圆形
    draw.ellipse([10, 10, 190, 190], fill='#1890FF')
    
    # 头部（圆形）
    draw.ellipse([60, 50, 140, 130], fill='white')
    
    # 身体（半圆形）
    draw.arc([40, 120, 160, 200], 0, 180, fill='white', width=60)
    
    return img

if __name__ == '__main__':
    import os
    output_dir = os.path.dirname(os.path.abspath(__file__))
    avatar = create_default_avatar()
    avatar_path = os.path.join(output_dir, 'default-avatar.png')
    avatar.save(avatar_path, 'PNG')
    print(f"✓ 已生成默认头像：{avatar_path}")
