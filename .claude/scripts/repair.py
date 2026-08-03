#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MinerU Markdown 修复脚本
功能：修复 MinerU 转换后的 Markdown 格式问题

用法：
    python repair.py <markdown文件路径>
    python repair.py D:/paper/VLA/论文目录/论文名.md
"""

import re
import sys
import argparse
from pathlib import Path


def merge_latex_formulas(content: str) -> str:
    """合并被换行符拆散的 LaTeX 公式"""
    # 匹配行内公式：$...$ 被换行拆散的情况
    content = re.sub(
        r'\$\s*\n\s*([^$\n]+?)\s*\n\s*\$',
        r'$\1$',
        content
    )
    # 匹配行间公式：$$...$$ 被换行拆散的情况
    content = re.sub(
        r'\$\$\s*\n\s*([^$\n]+?)\s*\n\s*\$\$',
        r'$$\1$$',
        content
    )
    return content


def merge_scattered_authors(content: str) -> str:
    """合并分散的作者名和机构信息"""
    # 匹配常见的作者分散格式：名字 + 换行 + 数字/符号
    content = re.sub(
        r'([A-Z][a-z]+\s+[A-Z][a-z]+)\n\s*(\d+|[*†♮])',
        r'\1\2',
        content
    )
    # 合并多个连续短行（可能是作者列表）
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 如果当前行是短行且下一行也是短行，可能是作者名
        if len(line.strip()) < 50 and i + 1 < len(lines):
            next_line = lines[i + 1]
            if len(next_line.strip()) < 50 and not next_line.strip().startswith('#'):
                # 合并这两行
                new_lines.append(line + ' ' + next_line.strip())
                i += 2
                continue
        new_lines.append(line)
        i += 1
    return '\n'.join(new_lines)


def fix_reference_citations(content: str) -> str:
    """修复 [num,\nnum] 类的引用格式"""
    # 修复 [num,\nnum] -> [num, num]
    content = re.sub(r'\[\s*(\d+)\s*,\s*\n\s*(\d+)\s*\]', r'[\1, \2]', content)
    # 修复 [num, num,\nnum] -> [num, num, num]
    content = re.sub(r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*\n\s*(\d+)\s*\]', r'[\1, \2, \3]', content)
    # 修复 [num, num, num,\nnum] -> [num, num, num, num]
    content = re.sub(r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\n\s*(\d+)\s*\]', r'[\1, \2, \3, \4]', content)
    # 修复 [num, num, num, num,\nnum] -> [num, num, num, num, num]
    content = re.sub(r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\n\s*(\d+)\s*\]', r'[\1, \2, \3, \4, \5]', content)
    # 修复 [num, num, num, num, num,\nnum] -> [num, num, num, num, num, num]
    content = re.sub(r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\n\s*(\d+)\s*\]', r'[\1, \2, \3, \4, \5, \6]', content)
    # 修复单个 [\nnum\n] -> [num]
    content = re.sub(r'\[\s*\n\s*(\d+)\s*\n\s*\]', r'[\1]', content)
    return content


def fix_figure_table_refs(content: str) -> str:
    """修复 Figure、Table、Section 等引用格式"""
    # Figure X\n: -> **Figure X:**
    content = re.sub(r'Figure\s+(\d+)\s*\n\s*:\s*', r'**Figure \1:** ', content)
    # TABLE X\n: -> **TABLE X:**
    content = re.sub(r'TABLE\s+(\w+)\s*\n\s*:\s*', r'**TABLE \1:** ', content)
    # Sec.\nX -> Sec. X
    content = re.sub(r'Sec\.\s*\n\s*(\w+)', r'Sec. \1', content)
    # Fig.\nX -> Fig. X
    content = re.sub(r'Fig\.\s*\n\s*(\d+)', r'Fig. \1', content)
    # Eq.\nX -> Eq. X
    content = re.sub(r'Eq\.\s*\n\s*(\d+)', r'Eq. \1', content)
    return content


def fix_duplicate_titles(content: str) -> str:
    """修复重复的标题"""
    # 匹配：标题\n标题\n: -> 标题
    content = re.sub(
        r'^(.+?)\n\1\n:\n',
        r'\1\n\n',
        content,
        flags=re.MULTILINE
    )
    return content


def clean_extra_newlines(content: str) -> str:
    """清理多余的空行"""
    # 3个以上连续空行 -> 2个空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def add_yaml_frontmatter(content: str, title: str = "", authors: str = "", arxiv: str = "", year: str = "") -> str:
    """添加 YAML 前置元数据"""
    # 检查是否已有 frontmatter
    if content.startswith('---'):
        return content

    # 尝试从内容中提取标题
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

    # 尝试从内容中提取作者
    if not authors:
        author_match = re.search(r'(?:Authors?|作者)[：:]\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if author_match:
            authors = author_match.group(1).strip()

    header = f"""---
title: "{title}"
authors: "{authors}"
venue: ""
year: "{year}"
tags: []
---

"""
    return header + content


def repair_markdown(content: str, add_metadata: bool = True) -> str:
    """执行所有修复操作"""
    content = fix_duplicate_titles(content)
    content = merge_latex_formulas(content)
    content = merge_scattered_authors(content)
    content = fix_reference_citations(content)
    content = fix_figure_table_refs(content)
    content = clean_extra_newlines(content)

    if add_metadata:
        content = add_yaml_frontmatter(content)

    return content


def main():
    parser = argparse.ArgumentParser(description="修复 MinerU 转换的 Markdown 文件")
    parser.add_argument("filepath", help="Markdown 文件路径")
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="不添加 YAML 前置元数据"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径（默认覆盖原文件）"
    )

    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"错误: 文件不存在 {filepath}")
        sys.exit(1)

    # 读取文件
    content = filepath.read_text(encoding="utf-8")

    # 修复
    repaired = repair_markdown(content, add_metadata=not args.no_metadata)

    # 保存
    output_path = Path(args.output) if args.output else filepath
    output_path.write_text(repaired, encoding="utf-8")

    print(f"修复完成: {output_path}")


if __name__ == "__main__":
    main()
