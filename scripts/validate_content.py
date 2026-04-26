from __future__ import annotations

from pathlib import Path

from utils import load_json, root_path


def scan_files() -> list[Path]:
    paths: list[Path] = []
    for folder, patterns in [
        ("site", ["*.html", "*.xml", "*.txt"]),
        ("dist", ["*.csv", "*.json", "*.md"]),
    ]:
        base = root_path(folder)
        if not base.exists():
            continue
        for pattern in patterns:
            paths.extend(base.rglob(pattern))
    return paths


def validate() -> list[str]:
    rules = load_json("config", "rules.json")
    required = rules["required_disclosure"]
    banned = rules.get("banned_phrases", [])
    errors: list[str] = []

    for path in scan_files():
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        for phrase in banned:
            if phrase in text:
                errors.append(f"{path}: banned phrase found: {phrase}")

    for path in root_path("dist", "note_drafts").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if required not in text:
            errors.append(f"{path}: missing disclosure")
        if "<!-- note-paid-line -->" not in text:
            errors.append(f"{path}: missing note paid-line marker")

    for path in root_path("site", "products").glob("*/index.html"):
        text = path.read_text(encoding="utf-8")
        if required not in text:
            errors.append(f"{path}: missing disclosure")

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("validation ok")

