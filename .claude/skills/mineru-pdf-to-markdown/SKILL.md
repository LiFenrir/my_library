---
name: mineru-pdf-to-markdown
description: Convert PDFs, images, and Office documents to Markdown using the MinerU precise parsing API. Use this skill whenever the user wants to extract Markdown from a PDF, convert a document to Markdown, parse a PDF for RAG/knowledge base, or mentions MinerU document parsing. This applies to local files, remote URLs, single files, and batch processing.
compatibility: Requires Python 3, requests library, and a MinerU API token at /home/kemove/.mineru/config.
---

# MinerU PDF to Markdown

Use the MinerU precise parsing API (`/api/v4/extract/task`) to convert documents into Markdown.

## Supported inputs

- PDF, images (png/jpg/jpeg/jp2/webp/gif/bmp), Doc, Docx, Ppt, PPTx, Xls, Xlsx
- Single file via URL
- Single local file via signed upload
- Batch URLs or local files

## Token

Read the MinerU API token from `/home/kemove/.mineru/config`.

File format:

```
token=<JWT token string>
```

Parse the file to extract the token value, then use it in the `Authorization: Bearer <token>` header.

## Model version selection

The `model_version` parameter controls parsing quality and speed.

- `vlm`（默认）: recommended for complex documents, scanned pages, mixed layouts, tables, and formulas. Slower but more accurate.
- `pipeline`: faster, good for clean, standard electronic PDFs.
- `MinerU-HTML`: required when the input is an HTML file.

When the user does not specify a model, default to `vlm` unless the file is a clean text PDF and speed matters more.

## Workflow

1. **Identify the input**
   - If the user provides a URL, use the URL endpoint.
   - If the user provides a local file path, use the file upload endpoint.
   - If the user provides multiple files, use the batch endpoints.
2. **Choose the model version** (default `vlm`).
3. **Submit the task** and get `task_id` (or `batch_id`).
4. **Poll** the result endpoint until `state` is `done` or `failed`.
5. **Download the ZIP** from `full_zip_url`.
6. **Extract the entire ZIP**, not just `full.md`. The ZIP also contains:
   - `images/`: extracted images referenced by `full.md`
   - `full.md`: primary Markdown output
   - `content_list.json` / `layout.json`: structured content and layout metadata
7. **Save** `full.md` to the location the user requested, preserving the relative `images/` directory so image links work.

## Output structure

For a single input, produce a directory like:

```
<input_stem>/
├── full.md          # Markdown text with tables preserved as Markdown tables
├── full.html        # HTML output if extra_formats includes html
├── full.tex         # LaTeX output if extra_formats includes latex
├── images/          # images referenced by full.md
├── layout.json      # layout analysis data
└── content_list.json
```

If the user asks for a specific `.md` file path, place `full.md` at that path and keep `images/` next to it so `![](images/...)` references resolve.

When no output path is given, create a directory named after the input file stem (e.g. `paper.pdf` → `paper/`) and put all outputs there.

## API endpoints

### Single URL

```
POST https://mineru.net/api/v4/extract/task
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com/file.pdf",
  "model_version": "vlm"
}
```

### Single local file

1. Request upload URLs:

```
POST https://mineru.net/api/v4/file-urls/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "files": [{"name": "file.pdf"}],
  "model_version": "vlm"
}
```

2. PUT the file bytes to the returned `file_urls[0]`.
3. Poll `https://mineru.net/api/v4/extract-results/batch/{batch_id}`.

### Batch URLs

```
POST https://mineru.net/api/v4/extract/task/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "files": [{"url": "https://example.com/a.pdf"}, {"url": "https://example.com/b.pdf"}],
  "model_version": "vlm"
}
```

### Poll single task

```
GET https://mineru.net/api/v4/extract/task/{task_id}
Authorization: Bearer <token>
```

### Poll batch

```
GET https://mineru.net/api/v4/extract-results/batch/{batch_id}
Authorization: Bearer <token>
```

## Common parameters

- `model_version`: `pipeline` | `vlm` | `MinerU-HTML`
- `is_ocr`: `true`/`false` (default `false`)
- `enable_formula`: `true`/`false` (default `true`)
- `enable_table`: `true`/`false` (default `true`)
- `language`: default `ch`, see language reference in the API docs
- `page_ranges`: e.g. `"1-5,8,10-12"`
- `extra_formats`: e.g. `["docx", "html"]` — useful when the user wants better table/formula rendering than plain Markdown provides

## Images, tables, and formulas

- **Images**: stored in `images/` inside the result ZIP. `full.md` references them with `![](images/...)`. Always extract the entire ZIP so these links remain valid.
- **Tables**: the helper script converts HTML tables into Markdown tables and replaces the corresponding plain-text blocks in `full.md`. To guarantee table structure, use `extra_formats: ["html"]` as well.
- **Formulas**: written as LaTeX in `full.md`. Enable `enable_formula: true` (default). For Word/Office-style equation rendering, export HTML or DOCX.

### Obsidian users

Obsidian renders Markdown tables, but table cells cannot contain block-level `$$...$$` formulas or complex LaTeX such as `\frac`, `\text{...}`, or multi-line expressions. For documents with complex tables/formulas, always export HTML (`extra_formats: ["html"]`) and open `full.html` in a browser or embed it as an iframe. Use `full.md` for text search, editing, and simple content; use `full.html` for faithful rendering of tables and formulas.

## Result handling

When `state == "done"`, the response contains `full_zip_url`. Download and unzip the entire archive.

If `state == "failed"`, surface `err_msg` to the user and stop.

## Errors

Common error codes:

- `A0202`: Token error
- `A0211`: Token expired
- `-60005`: File exceeds 200MB
- `-60006`: File exceeds 200 pages
- `-60018`: Daily quota exhausted

## Helper script

For deterministic execution, call `scripts/mineru_convert.py`:

```bash
python scripts/mineru_convert.py <input> [output.md or output_dir] \
  [--model vlm|pipeline|MinerU-HTML] \
  [--ocr] [--no-table] [--no-formula] \
  [--language ch] \
  [--page-ranges "1-5,8"] \
  [--extra-formats html,docx]
```

The script reads the token automatically, handles upload/polling/zip extraction, converts HTML tables into Markdown tables, preserves the `images/` directory, and writes the Markdown file.

## Output

When no output path is given, create a directory named after the input file stem (e.g. `paper.pdf` → `paper/`) and put all outputs there.

If the user requested a specific output path ending in `.md`, use that path for `full.md`. Otherwise save `full.md` inside the auto-created directory.

Always keep the `images/` directory next to `full.md` so image references resolve.
