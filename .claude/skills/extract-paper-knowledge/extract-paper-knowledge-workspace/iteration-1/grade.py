"""Grade extract-paper-knowledge skill outputs and produce run-1 grading.json."""
import json
import os
import re
import shutil
from pathlib import Path

WORKSPACE = Path("/home/kemove/INNOV/library/.claude/skills/extract-paper-knowledge/extract-paper-knowledge-workspace/iteration-1")


def find_files(directory: Path):
    if not directory.exists():
        return []
    return [p for p in directory.rglob("*") if p.is_file()]


def exists_file_under_path(run_dir: Path, prefix: str) -> tuple[bool, str]:
    prefix_path = run_dir / prefix
    files = list(prefix_path.rglob("*.md")) if prefix_path.exists() else []
    if files:
        return True, f"Found {len(files)} files under {prefix}, e.g. {files[0].relative_to(run_dir)}"
    return False, f"No .md files found under {prefix}"


def exists_file_under_any_path(run_dir: Path, *prefixes: str) -> tuple[bool, str]:
    for prefix in prefixes:
        prefix_path = run_dir / prefix
        files = list(prefix_path.rglob("*.md")) if prefix_path.exists() else []
        if files:
            return True, f"Found {len(files)} files under {prefix}, e.g. {files[0].relative_to(run_dir)}"
    return False, f"No .md files found under any of {prefixes}"


def no_file_under_path(run_dir: Path, prefix: str) -> tuple[bool, str]:
    prefix_path = run_dir / prefix
    files = list(prefix_path.rglob("*.md")) if prefix_path.exists() else []
    if files:
        return False, f"Unexpected files under {prefix}: {[f.relative_to(run_dir) for f in files]}"
    return True, f"No .md files under {prefix}"


def file_exists(run_dir: Path, filename: str) -> tuple[bool, str]:
    target = run_dir / filename
    if target.exists():
        return True, f"{filename} exists"
    return False, f"{filename} missing"


def summary_contains(run_dir: Path, *keywords) -> tuple[bool, str]:
    summary = run_dir / "summary.md"
    if not summary.exists():
        return False, "summary.md missing"
    text = summary.read_text(encoding="utf-8")
    missing = [k for k in keywords if k not in text]
    if missing:
        return False, f"summary.md missing keywords: {missing}"
    return True, f"summary.md contains all keywords: {keywords}"


def summary_or_files_contain(run_dir: Path, *keywords) -> tuple[bool, str]:
    files = find_files(run_dir)
    if not files:
        return False, "no output files"
    all_text = ""
    for f in files:
        try:
            all_text += f.read_text(encoding="utf-8") + "\n"
        except Exception:
            pass
    lower = all_text.lower()
    found = [k for k in keywords if k.lower() in lower]
    if found:
        return True, f"found keywords: {found}"
    return False, f"none of keywords found: {keywords}"


def max_files_matching(run_dir: Path, pattern: str, max_count: str) -> tuple[bool, str]:
    max_count = int(max_count)
    regex = re.compile(pattern, re.IGNORECASE)
    files = [f for f in find_files(run_dir) if regex.search(f.name)]
    if len(files) <= max_count:
        return True, f"{len(files)} files match {pattern} (<= {max_count})"
    return False, f"{len(files)} files match {pattern} (> {max_count}): {[f.name for f in files]}"


def distinct_top_level_dirs(run_dir: Path, min_count: str) -> tuple[bool, str]:
    min_count = int(min_count)
    dirs = set()
    for f in find_files(run_dir):
        rel = f.relative_to(run_dir)
        parts = rel.parts
        if parts and parts[0] != "summary.md":
            dirs.add(parts[0])
    if len(dirs) >= min_count:
        return True, f"{len(dirs)} top-level dirs: {sorted(dirs)}"
    return False, f"only {len(dirs)} top-level dirs: {sorted(dirs)}"


def file_contains(run_dir: Path, *keywords) -> tuple[bool, str]:
    files = [f for f in find_files(run_dir) if f.suffix == ".md"]
    if not files:
        return False, "no markdown files"
    for f in files:
        text = f.read_text(encoding="utf-8")
        if all(k in text for k in keywords):
            return True, f"{f.relative_to(run_dir)} contains {keywords}"
    return False, f"no file contains all keywords: {keywords}"


CHECKS = {
    "exists_file_under_path": exists_file_under_path,
    "exists_file_under_any_path": exists_file_under_any_path,
    "no_file_under_path": no_file_under_path,
    "file_exists": file_exists,
    "summary_contains": summary_contains,
    "summary_or_files_contain": summary_or_files_contain,
    "max_files_matching": max_files_matching,
    "distinct_top_level_dirs": distinct_top_level_dirs,
    "file_contains": file_contains,
}


def grade_run(run_dir: Path, assertions: list[dict]) -> dict:
    expectations = []
    passed = 0
    failed = 0
    for assertion in assertions:
        check_name = assertion["check"]
        check_fn = CHECKS.get(check_name)
        if not check_fn:
            p, evidence = False, f"unknown check: {check_name}"
        else:
            try:
                p, evidence = check_fn(run_dir, *assertion.get("args", []))
            except Exception as e:
                p, evidence = False, f"check error: {e}"
        expectations.append({"text": assertion["text"], "passed": p, "evidence": evidence})
        if p:
            passed += 1
        else:
            failed += 1
    total = len(expectations)
    pass_rate = passed / total if total > 0 else 0.0
    return {
        "summary": {"pass_rate": pass_rate, "passed": passed, "failed": failed, "total": total},
        "expectations": expectations,
    }


def grade_eval(eval_dir: Path):
    metadata_path = eval_dir / "eval_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    result = {"eval_id": metadata["eval_id"], "eval_name": metadata["eval_name"], "runs": {}}

    assertions_by_target: dict[str, list] = {}
    for assertion in metadata.get("assertions", []):
        target = assertion.get("target", "with_skill")
        assertions_by_target.setdefault(target, []).append(assertion)

    for config in ["with_skill", "without_skill"]:
        config_dir = eval_dir / config
        outputs_dir = config_dir / "outputs"
        run_dir = config_dir / "run-1"
        run_dir.mkdir(parents=True, exist_ok=True)

        # Copy/move timing.json into run_dir if it exists at config level
        timing_src = config_dir / "timing.json"
        timing_dst = run_dir / "timing.json"
        if timing_src.exists():
            shutil.copy2(timing_src, timing_dst)

        grading = grade_run(outputs_dir, assertions_by_target.get(config, []))
        result["runs"][config] = grading

        run_grading_path = run_dir / "grading.json"
        run_grading_path.write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")

    eval_grading_path = eval_dir / "grading.json"
    eval_grading_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main():
    all_results = []
    for eval_dir in sorted(WORKSPACE.iterdir()):
        if eval_dir.is_dir() and (eval_dir / "eval_metadata.json").exists():
            result = grade_eval(eval_dir)
            all_results.append(result)
            print(f"graded {eval_dir.name}")

    summary_path = WORKSPACE / "grading_summary.json"
    summary_path.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"summary -> {summary_path}")


if __name__ == "__main__":
    main()
