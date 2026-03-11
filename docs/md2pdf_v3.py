#!/usr/bin/env python3
"""Convert Markdown to PDF with Mermaid SVG embedding using base64"""

import markdown
from weasyprint import HTML
from pathlib import Path
import subprocess
import tempfile
import os
import re
import base64

def render_mermaid_svg(mermaid_code: str) -> str:
    """Render mermaid code to inline SVG using mmdc"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            mmd_path = os.path.join(tmpdir, 'chart.mmd')
            svg_path = os.path.join(tmpdir, 'chart.svg')
            
            # Write mermaid code
            with open(mmd_path, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            
            # Render using mmdc with explicit config
            cmd = [
                'mmdc',
                '-i', mmd_path,
                '-o', svg_path,
                '-b', '#ffffff',
                '-w', '1400',
                '--pdfFit', 'true',
                '--puppeteerConfigFile', '/dev/null'
            ]
            
            env = os.environ.copy()
            env['PUPPETEER_SKIP_CHROMIUM_DOWNLOAD'] = 'true'
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                env=env
            )
            
            if result.returncode == 0 and os.path.exists(svg_path):
                with open(svg_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                return svg_content
            else:
                print(f"mmdc error: {result.stderr}")
                return None
                
    except subprocess.TimeoutExpired:
        print("Mermaid render timeout")
        return None
    except Exception as e:
        print(f"Mermaid render failed: {e}")
        return None

def process_mermaid_blocks(html_content: str) -> str:
    """Replace mermaid code blocks with inline SVG"""
    
    # Pattern for mermaid code blocks in HTML
    pattern = r'<pre><code class="language-mermaid">(.*?)</code></pre>'
    
    def replace_mermaid(match):
        mermaid_code = match.group(1)
        # Decode HTML entities
        mermaid_code = mermaid_code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        
        # Try to render
        svg = render_mermaid_svg(mermaid_code)
        
        if svg:
            return f'<div class="mermaid-svg">{svg}</div>'
        else:
            # Fallback to code display
            return f'''<div class="mermaid-fallback">
                <div class="mermaid-label">📊 Diagram</div>
                <pre><code class="language-mermaid">{mermaid_code[:800]}{'...' if len(mermaid_code) > 800 else ''}</code></pre>
            </div>'''
    
    return re.sub(pattern, replace_mermaid, html_content, flags=re.DOTALL)

def md_to_pdf(md_path, pdf_path):
    # Read markdown file
    md_content = Path(md_path).read_text(encoding='utf-8')
    
    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'nl2br'],
        output_format='html5'
    )
    
    # Process mermaid diagrams
    print("Processing Mermaid diagrams...")
    html_content = process_mermaid_blocks(html_content)
    print("Mermaid processing complete")
    
    # Full HTML with styles
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>HealthPal Technical Framework</title>
    <style>
        @font-face {{
            font-family: 'Noto Sans SC';
            src: local('Noto Sans CJK SC'), local('Source Han Sans SC');
        }}
        @font-face {{
            font-family: 'Noto Serif SC';
            src: local('Noto Serif CJK SC'), local('Source Han Serif SC');
        }}
        body {{
            font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.8;
            color: #333;
            font-size: 11pt;
        }}
        h1 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 22pt;
            border-bottom: 3px solid #1890FF;
            padding-bottom: 12px;
        }}
        h2 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 16pt;
            border-bottom: 1px solid #d9d9d9;
            padding-bottom: 8px;
            margin-top: 1.5em;
        }}
        h3 {{
            font-size: 13pt;
            margin-top: 1.2em;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: Consolas, Monaco, monospace;
            font-size: 10pt;
            color: #eb2f96;
        }}
        pre {{
            background: #f8f8f8;
            border: 1px solid #e8e8e8;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
            font-size: 9pt;
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
            background: #fafafa;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #fafafa;
        }}
        .mermaid-svg {{
            text-align: center;
            margin: 2em 0;
            page-break-inside: avoid;
        }}
        .mermaid-svg svg {{
            max-width: 100%;
            height: auto;
        }}
        .mermaid-fallback {{
            background: #f0f7ff;
            border: 2px solid #1890FF;
            border-radius: 8px;
            padding: 16px;
            margin: 2em 0;
        }}
        .mermaid-label {{
            font-size: 12pt;
            font-weight: 600;
            color: #1890FF;
            margin-bottom: 12px;
        }}
        @page {{
            size: A4;
            margin: 2.5cm 2cm;
            @bottom-center {{
                content: counter(page);
                font-size: 9pt;
                color: #8c8c8c;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>'''
    
    # Generate PDF
    HTML(string=full_html).write_pdf(pdf_path)
    print(f"✓ PDF generated: {pdf_path}")
    size = Path(pdf_path).stat().st_size
    print(f"  File size: {size / 1024:.1f} KB")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        md_to_pdf(sys.argv[1], sys.argv[2])
    else:
        md_to_pdf(
            'HealthPal/docs/BACKEND_FRAMEWORK_V2.md',
            'HealthPal/docs/HealthPal_Backend_Framework_v3.pdf'
        )
