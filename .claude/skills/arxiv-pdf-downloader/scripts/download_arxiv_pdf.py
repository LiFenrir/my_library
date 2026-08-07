#!/usr/bin/env python3
"""下载 arXiv 论文原始 PDF 到指定目录."""

import argparse
import re
import sys
import urllib.request
from pathlib import Path


def slugify(title: str) -> str:
    """从标题生成简短 slug: 小写、去停用词、连字符连接."""
    stop = {"a", "an", "the", "for", "of", "on", "in", "to", "and", "with", "from", "by"}
    s = re.sub(r"[^\w\s-]", "", title)
    words = [w.lower() for w in s.split() if w.lower() not in stop and w.strip()]
    return "-".join(words[:5]) or "paper"


def download_pdf(arxiv_id: str, out_dir: Path, title: str | None = None) -> Path:
    """下载 PDF 并返回保存路径."""
    arxiv_id = arxiv_id.strip()
    if arxiv_id.lower().startswith("arxiv:"):
        arxiv_id = arxiv_id[6:].strip()

    slug = slugify(title) if title else "paper"
    filename = f"{slug}-{arxiv_id}.pdf"
    out_path = out_dir / filename

    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; arxiv-pdf-downloader/1.0)"
        },
    )

    with urllib.request.urlopen(req, timeout=120) as resp, open(out_path, "wb") as f:
        f.write(resp.read())

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="下载 arXiv PDF")
    parser.add_argument("arxiv_id", help="arXiv ID, 例如 2608.02580v1")
    parser.add_argument("--title", "-t", help="论文标题,用于生成文件名 slug")
    parser.add_argument("--out-dir", "-o", type=Path, default=Path("00_Inbox"), help="输出目录")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        out_path = download_pdf(args.arxiv_id, args.out_dir, args.title)
        print(out_path)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
