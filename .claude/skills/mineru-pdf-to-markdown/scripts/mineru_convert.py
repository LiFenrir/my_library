#!/usr/bin/env python3
"""Convert PDFs/images/Office docs to Markdown using the MinerU precise API.

读取 /home/kemove/.mineru/config 中的 token，支持 URL 和本地文件两种输入，
自动轮询结果、下载 ZIP、提取 full.md，并用 full.html 中的表格结构增强 Markdown。
"""

import argparse
import io
import re
import sys
import time
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

BASE_URL = "https://mineru.net"
TOKEN_PATH = Path.home() / ".mineru" / "config"
DEFAULT_TIMEOUT = 600
POLL_INTERVAL = 3


def load_token():
    """从 ~/.mineru/config 读取 token。"""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Token 文件不存在: {TOKEN_PATH}")

    content = TOKEN_PATH.read_text(encoding="utf-8").strip()
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("token="):
            return line[len("token="):].strip()
        if "=" in line:
            key, value = line.split("=", 1)
            if key.strip().lower() == "token":
                return value.strip()
    raise ValueError(f"未在 {TOKEN_PATH} 中找到 token 字段")


def is_url(text: str) -> bool:
    parsed = urlparse(text)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def submit_url_task(session: requests.Session, url: str, model_version: str, options: dict):
    """提交 URL 解析任务，返回 task_id。"""
    payload = {"url": url, "model_version": model_version, **options}
    resp = session.post(f"{BASE_URL}/api/v4/extract/task", json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"提交任务失败: {data.get('msg')} (code={data.get('code')})")
    return data["data"]["task_id"]


def submit_local_file(session: requests.Session, file_path: Path, model_version: str, options: dict):
    """申请上传 URL，上传文件，返回 batch_id。"""
    payload = {
        "files": [{"name": file_path.name}],
        "model_version": model_version,
        **{k: v for k, v in options.items() if k != "files"},
    }
    resp = session.post(f"{BASE_URL}/api/v4/file-urls/batch", json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"申请上传 URL 失败: {data.get('msg')} (code={data.get('code')})")

    batch_id = data["data"]["batch_id"]
    upload_url = data["data"]["file_urls"][0]

    with file_path.open("rb") as f:
        put_resp = session.put(upload_url, data=f)
    put_resp.raise_for_status()

    return batch_id


def poll_single_task(session: requests.Session, task_id: str, timeout: int = DEFAULT_TIMEOUT):
    """轮询单任务结果，返回 full_zip_url。"""
    url = f"{BASE_URL}/api/v4/extract/task/{task_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = session.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"查询任务失败: {data.get('msg')} (code={data.get('code')})")

        task = data["data"]
        state = task.get("state")
        if state == "done":
            return task["full_zip_url"]
        if state == "failed":
            raise RuntimeError(f"解析失败: {task.get('err_msg', '未知错误')}")

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"轮询任务 {task_id} 超时")


def poll_batch(session: requests.Session, batch_id: str, timeout: int = DEFAULT_TIMEOUT):
    """轮询批量任务，返回第一个成功的 full_zip_url。"""
    url = f"{BASE_URL}/api/v4/extract-results/batch/{batch_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = session.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"查询批量任务失败: {data.get('msg')} (code={data.get('code')})")

        results = data["data"].get("extract_result", [])
        for result in results:
            if result.get("state") == "done":
                return result["full_zip_url"]
            if result.get("state") == "failed":
                raise RuntimeError(f"解析失败: {result.get('err_msg', '未知错误')}")

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"轮询批量任务 {batch_id} 超时")


def extract_zip(session: requests.Session, zip_url: str, output_dir: Path) -> tuple[Path, Path | None]:
    """下载 ZIP 并解压到 output_dir，返回 (full.md 路径, full.html 路径)。"""
    resp = session.get(zip_url)
    resp.raise_for_status()
    output_dir.mkdir(parents=True, exist_ok=True)

    full_md_path = None
    full_html_path = None
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            target = output_dir / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith("/"):
                continue
            target.write_bytes(zf.read(name))
            lower_name = name.lower()
            if lower_name.endswith("full.md") or lower_name == "full.md":
                full_md_path = target
            if lower_name.endswith("full.html") or lower_name == "full.html":
                full_html_path = target

    if not full_md_path or not full_md_path.exists():
        raise FileNotFoundError("ZIP 中未找到 full.md")
    return full_md_path, full_html_path


def _normalize(text: str) -> set[str]:
    """提取用于匹配的文本特征词。"""
    text = re.sub(r"[\$\\\(\)\[\]\{\}]", " ", text)
    return {w for w in re.split(r"\W+", text.lower()) if len(w) > 2}


def _cell_text(cell) -> str:
    """提取单元格文本，并把块级 LaTeX 降级为行内公式（Obsidian 表格兼容）。"""
    text = cell.get_text(strip=True)
    text = text.replace("|", "\\|")
    text = re.sub(r"\s+", " ", text)
    # Obsidian 表格单元格只支持行内公式，不支持 $$...$$
    text = re.sub(r"\$\$(.+?)\$\$", r"$\1$", text, flags=re.DOTALL)
    return text


def _table_to_markdown(table) -> str:
    """把 BeautifulSoup table 转成 Markdown 表格。"""
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        for cell in tr.find_all(["td", "th"]):
            text = _cell_text(cell)
            cells.append(text)
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    max_len = max(len(r) for r in rows)
    rows = [r + [""] * (max_len - len(r)) for r in rows]
    lines = []
    for i, row in enumerate(rows):
        lines.append("| " + " | ".join(row) + " |")
        if i == 0:
            lines.append("|" + "|".join(["---"] * max_len) + "|")
    return "\n".join(lines)


def enhance_markdown_tables(md_path: Path, html_path: Path | None) -> None:
    """用 full.html 中的表格结构增强 full.md。"""
    if not html_path or not html_path.exists():
        return
    if BeautifulSoup is None:
        print("警告：未安装 beautifulsoup4，跳过表格增强", file=sys.stderr)
        return

    md_text = md_path.read_text(encoding="utf-8", errors="ignore")
    # 已经包含 Markdown 表格则不做改动
    if "\n|---" in md_text or "\n| ---" in md_text:
        return

    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html_text, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return

    paragraphs = re.split(r"\n\s*\n", md_text)
    replaced = set()

    for table in tables:
        md_table = _table_to_markdown(table)
        if not md_table:
            continue

        table_words = _normalize(md_table)
        if len(table_words) < 4:
            continue

        best_idx = -1
        best_score = 0.0
        for idx, para in enumerate(paragraphs):
            if idx in replaced:
                continue
            para_words = _normalize(para)
            if not para_words:
                continue
            common = table_words & para_words
            score = len(common) / max(len(table_words), len(para_words), 1)
            if score > best_score and score >= 0.3:
                best_score = score
                best_idx = idx

        if best_idx >= 0:
            paragraphs[best_idx] = md_table
            replaced.add(best_idx)

    md_path.write_text("\n\n".join(paragraphs), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="MinerU PDF to Markdown")
    parser.add_argument("input", help="PDF URL 或本地文件路径")
    parser.add_argument("output", nargs="?", help="输出 Markdown 文件路径或目录")
    parser.add_argument("--model", default="vlm", choices=["pipeline", "vlm", "MinerU-HTML"])
    parser.add_argument("--ocr", action="store_true", help="启用 OCR")
    parser.add_argument("--no-table", action="store_true", help="禁用表格识别")
    parser.add_argument("--no-formula", action="store_true", help="禁用公式识别")
    parser.add_argument("--language", default="ch")
    parser.add_argument("--page-ranges")
    parser.add_argument("--extra-formats", help="额外导出格式，逗号分隔：docx,html,latex")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    token = load_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    options = {
        "is_ocr": args.ocr,
        "enable_table": not args.no_table,
        "enable_formula": not args.no_formula,
        "language": args.language,
    }
    if args.page_ranges:
        options["page_ranges"] = args.page_ranges
    if args.extra_formats:
        fmts = [f.strip() for f in args.extra_formats.split(",") if f.strip()]
        options["extra_formats"] = fmts

    if is_url(args.input):
        task_id = submit_url_task(session, args.input, args.model, options)
        print(f"URL 任务已提交: {task_id}", file=sys.stderr)
        zip_url = poll_single_task(session, task_id, timeout=args.timeout)
    else:
        file_path = Path(args.input).expanduser().resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        batch_id = submit_local_file(session, file_path, args.model, options)
        print(f"本地文件任务已提交: {batch_id}", file=sys.stderr)
        zip_url = poll_batch(session, batch_id, timeout=args.timeout)

    print(f"下载结果: {zip_url}", file=sys.stderr)

    if args.output:
        output_arg = Path(args.output).expanduser()
        if output_arg.suffix.lower() == ".md":
            # 用户指定了具体的 .md 文件：把它作为目标，输出目录用它所在的目录
            md_target = output_arg
            output_dir = md_target.parent
        else:
            # 用户指定的是目录
            output_dir = output_arg
            md_target = output_dir / "full.md"
    else:
        # 默认：在输入文件同名目录下输出
        input_path = Path(args.input)
        stem = input_path.stem if not is_url(args.input) else Path(input_path.name).stem or "output"
        output_dir = input_path.parent / stem
        md_target = output_dir / "full.md"

    full_md_path, full_html_path = extract_zip(session, zip_url, output_dir)

    if md_target != full_md_path:
        md_target.write_text(full_md_path.read_text(encoding="utf-8"), encoding="utf-8")
        enhance_markdown_tables(md_target, full_html_path)
    else:
        enhance_markdown_tables(full_md_path, full_html_path)

    print(md_target)


if __name__ == "__main__":
    main()
