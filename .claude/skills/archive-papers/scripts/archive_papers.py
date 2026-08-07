#!/usr/bin/env python3
"""归档论文：扫描 Inbox、移动文件、重写图片路径、更新 05_Papers/index.md。

由 archive-papers skill 调用，只做确定性文件操作，不做 LLM 推理。

新架构（2026-08-06 起）：
- 05_Papers/articles/<slug>.md    # 平铺，不再按 category 分子目录
- 99_Attachments/papers/pdfs/<slug>.pdf
- 99_Attachments/papers/images/<slug>/*
- 05_Papers/notes/<slug>.md
- 05_Papers/index.md             # 平铺链接列表，不再按分类
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

ARXIV_RE = re.compile(r"^arxiv-([\d\.]+)(?:\.pdf)?$", re.IGNORECASE)
# 匹配 ![](images/xxx.jpg) 或 ![alt](images/xxx.jpg)
IMG_RE = re.compile(r"!\[([^\]]*)\]\((images/[^)]+)\)")


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


def rewrite_image_paths(md_text: str, slug: str) -> str:
    """将 full.md 中的 images/xxx 重写为指向 99_Attachments/papers/images/<slug>/ 的相对路径。"""
    def repl(m):
        alt = m.group(1)
        filename = Path(m.group(2)).name
        # 从 05_Papers/articles/<slug>.md 出发：../../99_Attachments/papers/images/<slug>/<filename>
        new_path = f"../../99_Attachments/papers/images/{slug}/{filename}"
        return f"![{alt}]({new_path})"
    return IMG_RE.sub(repl, md_text)


def move_paper(slug: str, source_pdf: Path | None, source_dir: Path | None):
    """执行物理迁移。"""
    target_images_dir = IMAGES_DIR / slug
    target_pdf = PDFS_DIR / f"{slug}.pdf"
    target_md = ARTICLES_DIR / f"{slug}.md"

    target_images_dir.mkdir(parents=True, exist_ok=True)
    PDFS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

    if source_pdf and source_pdf.exists():
        shutil.move(str(source_pdf), str(target_pdf))

    if source_dir and source_dir.is_dir():
        for img in (source_dir / "images").glob("*"):
            shutil.move(str(img), str(target_images_dir / img.name))
        source_md = source_dir / "full.md"
        if source_md.exists():
            md_text = source_md.read_text(encoding="utf-8")
            md_text = rewrite_image_paths(md_text, slug)
            target_md.write_text(md_text, encoding="utf-8")
        # 清理空源目录
        shutil.rmtree(source_dir, ignore_errors=True)

    return {
        "article": str(target_md),
        "images_dir": str(target_images_dir),
        "pdf": str(target_pdf),
    }


def update_index(slug: str):
    """更新 05_Papers/index.md：在平铺论文列表中按字母序添加链接。"""
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"index.md 不存在: {INDEX_FILE}")

    text = INDEX_FILE.read_text(encoding="utf-8")
    link_line = f"- [[05_Papers/notes/{slug}|{slug}]]"

    # 优先匹配 "## 论文列表" 后的平铺列表
    section_pattern = r"(## 论文列表\n\n)(.*?)(\n## |\Z)"
    match = re.search(section_pattern, text, re.DOTALL)
    if not match:
        # 兼容旧 index：匹配 "## 按方向浏览" 后的第一个分类区之前的区域，或 "## 目录"
        section_pattern = r"(## 目录\n\n)(.*?)(\n## |\Z)"
        match = re.search(section_pattern, text, re.DOTALL)

    if not match:
        raise ValueError("未在 index.md 找到 '## 论文列表' 或 '## 目录' 区")

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

    sub.add_parser("scan", help="扫描 Inbox 候选论文")

    p_move = sub.add_parser("move", help="移动文件到目标位置")
    p_move.add_argument("--slug", required=True)
    p_move.add_argument("--pdf", help="源 PDF 路径")
    p_move.add_argument("--dir", help="源转换目录路径")

    p_index = sub.add_parser("update-index", help="更新 05_Papers/index.md")
    p_index.add_argument("--slug", required=True)

    args = parser.parse_args()

    if args.cmd == "scan":
        candidates = scan_inbox()
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        return

    if args.cmd == "move":
        source_pdf = Path(args.pdf) if args.pdf else None
        source_dir = Path(args.dir) if args.dir else None
        result = move_paper(args.slug, source_pdf, source_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "update-index":
        result = update_index(args.slug)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
