#!/usr/bin/env python3
"""
生成微信小程序 tabBar 图标（PNG 格式）
使用 Pillow 库生成简单的占位图标
"""

from PIL import Image, ImageDraw

# 图标配置
ICONS = {
    'home': ('首页', '#1890FF'),
    'records': ('档案', '#1890FF'),
    'analysis': ('分析', '#1890FF'),
    'profile': ('我的', '#1890FF'),
}

SIZE = 81  # 微信小程序推荐图标尺寸
ACTIVE_SIZE = 81

def create_icon(name, label, color, active=False):
    """创建单个图标"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制简单图形
    if name == 'home':
        # 房子形状
        points = [(40, 20), (70, 45), (70, 70), (55, 70), (55, 50), (25, 50), (25, 70), (10, 70), (10, 45)]
        draw.polygon(points, fill=color if active else '#999999')
    elif name == 'records':
        # 文档形状
        draw.rectangle([15, 20, 65, 70], fill=color if active else '#999999')
        draw.rectangle([20, 30, 60, 35], fill='white')
        draw.rectangle([20, 45, 60, 50], fill='white')
        draw.rectangle([20, 60, 50, 65], fill='white')
    elif name == 'analysis':
        # 图表形状
        draw.rectangle([15, 50, 30, 70], fill=color if active else '#999999')
        draw.rectangle([35, 35, 50, 70], fill=color if active else '#999999')
        draw.rectangle([55, 20, 70, 70], fill=color if active else '#999999')
    elif name == 'profile':
        # 用户形状
        draw.ellipse([25, 20, 55, 50], fill=color if active else '#999999')
        draw.ellipse([15, 50, 65, 70], fill=color if active else '#999999')
    
    return img

def main():
    import os
    
    # 创建输出目录
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("生成 tabBar 图标...")
    
    for name, (label, color) in ICONS.items():
        # 普通状态
        icon = create_icon(name, label, color, active=False)
        icon_path = os.path.join(output_dir, f"{name}.png")
        icon.save(icon_path, 'PNG')
        print(f"✓ {name}.png")
        
        # 选中状态
        icon_active = create_icon(name, label, color, active=True)
        icon_active_path = os.path.join(output_dir, f"{name}-active.png")
        icon_active.save(icon_active_path, 'PNG')
        print(f"✓ {name}-active.png")
    
    print(f"\n完成！共生成 {len(ICONS) * 2} 个图标文件")
    print(f"输出目录：{output_dir}")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("错误：需要安装 Pillow 库")
        print("运行：pip install Pillow")
        exit(1)
