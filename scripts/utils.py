from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def root_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def load_json(*parts: str) -> Any:
    path = root_path(*parts)
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def configured_site_url(brand: dict[str, Any]) -> str:
    value = os.environ.get("SITE_URL") or brand.get("site_url") or ""
    value = value.strip()
    if not value:
        value = "https://example.github.io/anonymous-monetization-kit/"
    return value.rstrip("/") + "/"


def product_url(site_url: str, product: dict[str, Any]) -> str:
    return f"{site_url}products/{product['slug']}/"


def compact(text: str) -> str:
    return " ".join(text.split())

