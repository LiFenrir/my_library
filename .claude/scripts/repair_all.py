#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 MinerU Markdown 文件
功能：递归扫描目录，修复所有 Markdown 文件

用法：
    python repair_all.py <目录路径>
    python repair_all.py D:/paper/VLA/论文目录/
    python repair_all.py D:/paper/ --dry-run  # 预览模式
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# 导入 repair.py 中的修复函数
sys.path.insert(0, str(Path(__file__).parent))
from repair import repair_markdown


def find_markdown_files(directory: Path) -> List[Path]:
    """递归查找目录下的所有 Markdown 文件"""
    md_files = []
    for md_file in directory.rglob("*.md"):
        # 排除已修复的文件（.repaired.md）
        if not md_file.name.endswith(".repaired.md"):
            md_files.append(md_file)
    return sorted(md_files)


def repair_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    修复单个 Markdown 文件
    返回: (是否成功, 消息)
    """
    try:
        content = filepath.read_text(encoding="utf-8")

        # 检查是否已有 YAML frontmatter
        has_frontmatter = content.startswith('---')

        repaired = repair_markdown(content, add_metadata=not has_frontmatter)

        if dry_run:
            return True, f"[预览] 将修复: {filepath}"

        # 保存为 .repaired.md 避免覆盖原文件
        output_path = filepath.with_suffix('.repaired.md')
        output_path.write_text(repaired, encoding="utf-8")

        return True, f"已修复: {filepath} -> {output_path.name}"

    except Exception as e:
        return False, f"修复失败: {filepath} - {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="批量修复 MinerU Markdown 文件")
    parser.add_argument("directory", help="要扫描的目录路径")
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="预览模式：只显示将要修复的文件，不实际执行"
    )
    parser.add_argument(
        "--overwrite", "-w",
        action="store_true",
        help="直接覆盖原文件（不生成 .repaired.md）"
    )
    parser.add_argument(
        "--pattern", "-p",
        default="*.md",
        help="文件匹配模式（默认: *.md）"
    )

    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.exists():
        print(f"错误: 目录不存在 {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"错误: {directory} 不是目录")
        sys.exit(1)

    # 查找所有 Markdown 文件
    md_files = find_markdown_files(directory)

    if not md_files:
        print(f"在 {directory} 中未找到 Markdown 文件")
        return

    print(f"=" * 60)
    print(f"扫描目录: {directory}")
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    if args.dry_run:
        print("[预览模式] 不会修改任何文件")
    print(f"=" * 60)

    # 修复每个文件
    success_count = 0
    fail_count = 0

    for filepath in md_files:
        success, message = repair_file(filepath, dry_run=args.dry_run)

        if success:
            success_count += 1
            print(f"  ✓ {message}")
        else:
            fail_count += 1
            print(f"  ✗ {message}")

    # 统计
    print(f"\n{'=' * 60}")
    print(f"处理完成!")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
