#!/usr/bin/env python3
"""
SEO 自动配置工具
为新增文档自动生成 front matter SEO 元数据
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

def extract_title(content):
    """从文档内容中提取标题"""
    # 匹配 H1 标题
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return None

def extract_first_paragraph(content):
    """提取第一段非空文本作为描述基础"""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # 跳过 front matter、标题、空行、表格等
        if not line or line.startswith('---') or line.startswith('#') or \
           line.startswith('|') or line.startswith('- ') or line.startswith('**'):
            continue
        # 清理 markdown 标记
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # 移除链接
        clean = re.sub(r'\*\*|__', '', clean)  # 移除粗体
        clean = re.sub(r'\*|_', '', clean)  # 移除斜体
        if len(clean) > 20:  # 至少20个字符
            return clean[:160]  # 限制长度
    return None

def generate_description(title, first_para, doc_type):
    """生成描述"""
    if first_para and len(first_para) > 50:
        return first_para[:160]
    
    templates = {
        'free-models': f"{title} - 免费AI模型使用指南，包含详细参数、使用限制和快速上手指南。",
        'hermes': f"{title} - Hermes Agent 配置教程，帮助你快速设置和优化 AI 助手。",
        'reports': f"{title} - 技术深度分析，提供实用的 AI 工具和方法论见解。",
        'default': f"{title} - Evolve 技术文档，免费AI模型指南与工具配置教程。"
    }
    return templates.get(doc_type, templates['default'])

def generate_keywords(title, doc_type):
    """生成关键词"""
    base_keywords = {
        'free-models': ['免费AI模型', 'OpenRouter', 'LLM', '大语言模型', 'AI编程'],
        'hermes': ['Hermes Agent', 'AI助手', '工具配置', '自动化', 'MCP'],
        'reports': ['AI技术', '技术报告', '最佳实践', '架构设计'],
        'default': ['AI工具', '技术教程', '免费模型']
    }
    
    # 从标题提取额外关键词
    extra = []
    if 'Elephant' in title:
        extra.append('Elephant Alpha')
    if 'NVIDIA' in title or 'Nemotron' in title:
        extra.append('NVIDIA Nemotron')
    if 'Gemma' in title:
        extra.append('Google Gemma')
    if 'Qwen' in title:
        extra.append('Qwen')
    if 'Llama' in title:
        extra.append('Llama')
    if 'GPT' in title:
        extra.append('GPT')
    
    keywords = base_keywords.get(doc_type, base_keywords['default'])
    if extra:
        keywords = extra + keywords
    
    return ', '.join(keywords[:8])  # 最多8个关键词

def detect_doc_type(file_path):
    """检测文档类型"""
    path_str = str(file_path)
    if 'free-models' in path_str:
        return 'free-models'
    elif 'hermes' in path_str:
        return 'hermes'
    elif 'reports' in path_str:
        return 'reports'
    return 'default'

def has_front_matter(content):
    """检查是否已有 front matter"""
    return content.startswith('---')

def generate_front_matter(title, description, keywords):
    """生成 front matter"""
    today = datetime.now().strftime('%Y-%m-%d')
    return f"""---
description: {description}
keywords: {keywords}
date: {today}
---

"""

def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已有 front matter，跳过
    if has_front_matter(content):
        print(f"  ⏭️  跳过（已有 front matter）: {file_path}")
        return False
    
    # 提取信息
    title = extract_title(content)
    if not title:
        print(f"  ⚠️  无法提取标题: {file_path}")
        return False
    
    first_para = extract_first_paragraph(content)
    doc_type = detect_doc_type(file_path)
    
    description = generate_description(title, first_para, doc_type)
    keywords = generate_keywords(title, doc_type)
    
    front_matter = generate_front_matter(title, description, keywords)
    
    # 写入文件
    new_content = front_matter + content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ 已添加 SEO: {file_path.name}")
    return True

def main():
    """主函数"""
    docs_dir = Path('docs')
    check_only = '--check-only' in sys.argv
    
    if not docs_dir.exists():
        print("错误：docs 目录不存在")
        sys.exit(1)
    
    processed = 0
    skipped = 0
    missing = []
    
    print("🔍 扫描文档...")
    
    # 遍历所有 markdown 文件
    for md_file in docs_dir.rglob('*.md'):
        # 跳过 index.md（通常已有配置）
        if md_file.name == 'index.md' and md_file.parent.name != 'docs':
            continue
        
        # 跳过 site-info 目录
        if 'site-info' in str(md_file):
            continue
        
        if check_only:
            # 仅检查模式
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if not has_front_matter(content):
                missing.append(str(md_file))
        else:
            if process_file(md_file):
                processed += 1
            else:
                skipped += 1
    
    if check_only:
        if missing:
            print(f"\n⚠️  发现 {len(missing)} 个文档缺少 SEO front matter:")
            for f in missing:
                print(f"  - {f}")
            sys.exit(1)
        else:
            print("\n✅ 所有文档都已配置 SEO front matter")
            sys.exit(0)
    else:
        print(f"\n📊 完成：处理了 {processed} 个文件，跳过了 {skipped} 个文件")
        
        if processed > 0:
            print("\n💡 提示：请检查生成的 front matter，根据需要手动调整")

if __name__ == '__main__':
    main()
