#!/usr/bin/env python3
"""Convert Markdown to PDF with proper Chinese font support"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import re

def md_to_pdf(md_path, pdf_path):
    # Read markdown file
    md_content = Path(md_path).read_text(encoding='utf-8')
    
    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'codehilite', 'nl2br'],
        output_format='html5'
    )
    
    # Wrap in proper HTML document with local Chinese fonts
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthPal 技术框架文档</title>
    <style>
        @font-face {{
            font-family: 'Noto Sans SC';
            src: local('Noto Sans CJK SC'), local('Noto Sans SC'), local('Source Han Sans SC'), local('Source Han Sans CN');
            font-weight: normal;
        }}
        @font-face {{
            font-family: 'Noto Serif SC';
            src: local('Noto Serif CJK SC'), local('Noto Serif SC'), local('Source Han Serif SC'), local('Source Han Serif CN');
            font-weight: normal;
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans SC', 'Microsoft YaHei', 'SimHei', sans-serif;
            line-height: 1.8;
            color: #333;
            font-size: 11pt;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            font-family: 'Noto Serif SC', 'Microsoft YaHei', serif;
            font-size: 22pt;
            color: #1a1a1a;
            border-bottom: 3px solid #1890FF;
            padding-bottom: 12px;
            margin-top: 0;
            page-break-after: avoid;
        }}
        h2 {{
            font-family: 'Noto Serif SC', 'Microsoft YaHei', serif;
            font-size: 16pt;
            color: #1a1a1a;
            border-bottom: 1px solid #d9d9d9;
            padding-bottom: 8px;
            margin-top: 1.5em;
            page-break-after: avoid;
        }}
        h3 {{
            font-family: 'Noto Serif SC', 'Microsoft YaHei', serif;
            font-size: 13pt;
            color: #262626;
            margin-top: 1.2em;
            page-break-after: avoid;
        }}
        h4 {{
            font-size: 11pt;
            font-weight: 600;
            color: #262626;
            margin-top: 1em;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 10pt;
            color: #eb2f96;
        }}
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #e8e8e8;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.5;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: #333;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #d9d9d9;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #fafafa;
            font-weight: 600;
            color: #262626;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        tr:hover {{
            background-color: #f0f7ff;
        }}
        blockquote {{
            border-left: 4px solid #1890FF;
            margin: 1em 0;
            padding-left: 16px;
            color: #595959;
            background-color: #fafafa;
            padding: 8px 12px 8px 16px;
        }}
        a {{
            color: #1890FF;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 24px;
        }}
        li {{
            margin: 0.5em 0;
        }}
        strong {{
            font-weight: 600;
            color: #262626;
        }}
        em {{
            font-style: italic;
            color: #595959;
        }}
        hr {{
            border: none;
            border-top: 1px solid #d9d9d9;
            margin: 2em 0;
        }}
        .page-break {{
            page-break-before: always;
        }}
        /* Code block syntax highlighting colors */
        .hljs-comment {{ color: #8c8c8c; }}
        .hljs-keyword {{ color: #f5222d; }}
        .hljs-string {{ color: #52c41a; }}
        .hljs-number {{ color: #fa8c16; }}
        .hljs-function {{ color: #722ed1; }}
        .hljs-class {{ color: #13c2c2; }}
        
        @page {{
            size: A4;
            margin: 2.5cm 2cm 2.5cm 2cm;
            @bottom-center {{
                content: counter(page);
                font-size: 9pt;
                color: #8c8c8c;
            }}
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            a {{
                text-decoration: none;
                color: #333;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>'''
    
    # Generate PDF with font configuration
    html_obj = HTML(string=full_html)
    html_obj.write_pdf(pdf_path)
    print(f"✓ PDF 生成成功：{pdf_path}")
    
    # Get file size
    size = Path(pdf_path).stat().st_size
    print(f"  文件大小：{size / 1024:.1f} KB")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        md_to_pdf(sys.argv[1], sys.argv[2])
    else:
        # Default paths
        md_to_pdf(
            'HealthPal/docs/TECH_FRAMEWORK.md',
            'HealthPal/docs/HealthPal_技术框架.pdf'
        )
