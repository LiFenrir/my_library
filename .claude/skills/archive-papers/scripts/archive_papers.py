#!/usr/bin/env python3
"""归档论文：扫描 Inbox、移动文件、更新 05_Papers/index.md。

由 archive-papers skill 调用，只做确定性文件操作，不做 LLM 推理。
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def get_library_root() -> Path:
    """从当前工作目录向上查找 library 根目录（包含 05_Papers 的目录）。"""
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / "05_Papers").is_dir() and (p / "00_Inbox").is_dir():
            return p
    raise FileNotFoundError("未找到 library 根目录（缺少 05_Papers 或 00_Inbox）")


LIBRARY_ROOT = get_library_root()
INBOX_DIR = LIBRARY_ROOT / "00_Inbox"
PAPERS_DIR = LIBRARY_ROOT / "05_Papers"
ARTICLES_DIR = PAPERS_DIR / "articles"
NOTES_DIR = PAPERS_DIR / "notes"
ATTACHMENTS_DIR = LIBRARY_ROOT / "99_Attachments" / "papers"
PDFS_DIR = ATTACHMENTS_DIR / "pdfs"
IMAGES_DIR = ATTACHMENTS_DIR / "images"
INDEX_FILE = PAPERS_DIR / "index.md"

# 分类英文目录 -> 中文标题（与 05_Papers/index.md 中的标题一致）
CATEGORY_MAP = {
    "vla": "VLA",
    "world-model": "世界模型",
    "world-action-model": "世界动作模型",
    "embodied-ai": "具身智能",
    "rl": "强化学习",
}

ARXIV_RE = re.compile(r"^arxiv-([\d\.]+)(?:\.pdf)?$", re.IGNORECASE)


def slugify(title: str) -> str:
    """从标题生成 slug：小写、去停用词、空格/下划线转连字符。"""
    stopwords = {"a", "an", "the", "of", "for", "in", "on", "with", "and", "or", "to", "from"}
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    parts = [p for p in s.split() if p and p not in stopwords]
    slug = "-".join(parts)[:60].rstrip("-")
    return slug or "paper"


def scan_inbox():
    """扫描 Inbox，返回候选论文列表。"""
    candidates = []
    if not INBOX_DIR.is_dir():
        return candidates
    for entry in sorted(INBOX_DIR.iterdir()):
        if entry.is_file() and entry.suffix.lower() == ".pdf":
            m = ARXIV_RE.match(entry.stem)
            arxiv_id = m.group(1) if m else None
            candidates.append({
                "type": "pdf",
                "path": str(entry),
                "arxiv_id": arxiv_id,
                "suggested_slug": arxiv_id or slugify(entry.stem),
            })
        elif entry.is_dir() and (entry / "full.md").is_file():
            m = ARXIV_RE.match(entry.name)
            arxiv_id = m.group(1) if m else None
            candidates.append({
                "type": "converted",
                "path": str(entry),
                "arxiv_id": arxiv_id,
                "suggested_slug": arxiv_id or slugify(entry.name),
            })
    return candidates


def move_paper(slug: str, category: str, source_pdf: Path | None, source_dir: Path | None):
    """执行物理迁移。"""
    if category not in CATEGORY_MAP:
        raise ValueError(f"未知分类: {category}")

    target_article_dir = ARTICLES_DIR / category / slug
    target_images_dir = IMAGES_DIR / slug
    target_pdf = PDFS_DIR / f"{slug}.pdf"

    target_article_dir.mkdir(parents=True, exist_ok=True)
    target_images_dir.mkdir(parents=True, exist_ok=True)
    PDFS_DIR.mkdir(parents=True, exist_ok=True)

    if source_pdf and source_pdf.exists():
        shutil.move(str(source_pdf), str(target_pdf))

    if source_dir and source_dir.is_dir():
        for img in (source_dir / "images").glob("*"):
            shutil.move(str(img), str(target_images_dir / img.name))
        source_md = source_dir / "full.md"
        if source_md.exists():
            target_md = target_article_dir / f"{slug}.md"
            shutil.move(str(source_md), str(target_md))
        # 清理空源目录
        shutil.rmtree(source_dir, ignore_errors=True)

    return {
        "article_dir": str(target_article_dir),
        "images_dir": str(target_images_dir),
        "pdf": str(target_pdf),
    }


def update_index(slug: str, category: str):
    """更新 05_Papers/index.md：在对应分类下添加链接，更新统计数。"""
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"index.md 不存在: {INDEX_FILE}")

    text = INDEX_FILE.read_text(encoding="utf-8")
    section_title = CATEGORY_MAP[category]
    link_line = f"- [[{slug}|{slug}]]"

    # 在对应分类区插入链接（按字母序）
    pattern = rf"(### {re.escape(section_title)}\n\n)(.*?)(\n### |\n## |\n--- |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        raise ValueError(f"未在 index.md 找到分类区: {section_title}")

    existing = match.group(2)
    lines = [ln for ln in existing.splitlines() if ln.strip()]
    if link_line in lines:
        return {"updated": False, "reason": "链接已存在"}

    lines.append(link_line)
    lines.sort(key=lambda s: s.lower())
    new_section = "\n".join(lines) + "\n"
    text = text[:match.start(2)] + new_section + text[match.end(2):]

    # 更新统计数
    text = re.sub(
        r"(- 人工笔记：)(\d+)( 篇)",
        lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}",
        text,
        count=1,
    )
    text = re.sub(
        r"(- MinerU 原文：)(\d+)( 篇)",
        lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}",
        text,
        count=1,
    )

    INDEX_FILE.write_text(text, encoding="utf-8")
    return {"updated": True}


def main():
    parser = argparse.ArgumentParser(description="论文归档辅助脚本")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="扫描 Inbox 候选论文")

    p_move = sub.add_parser("move", help="移动文件到目标位置")
    p_move.add_argument("--slug", required=True)
    p_move.add_argument("--category", required=True, choices=list(CATEGORY_MAP))
    p_move.add_argument("--pdf", help="源 PDF 路径")
    p_move.add_argument("--dir", help="源转换目录路径")

    p_index = sub.add_parser("update-index", help="更新 05_Papers/index.md")
    p_index.add_argument("--slug", required=True)
    p_index.add_argument("--category", required=True, choices=list(CATEGORY_MAP))

    args = parser.parse_args()

    if args.cmd == "scan":
        candidates = scan_inbox()
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        return

    if args.cmd == "move":
        source_pdf = Path(args.pdf) if args.pdf else None
        source_dir = Path(args.dir) if args.dir else None
        result = move_paper(args.slug, args.category, source_pdf, source_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "update-index":
        result = update_index(args.slug, args.category)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
