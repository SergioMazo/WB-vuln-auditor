"""Documentation integrity tests that require no external network."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


def test_internal_markdown_links_resolve() -> None:
    failures: list[str] = []

    for document in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv"} for part in document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue
            path_text = unquote(target.split("#", maxsplit=1)[0])
            resolved = (document.parent / path_text).resolve()
            if not resolved.exists():
                failures.append(
                    f"{document.relative_to(ROOT)} -> {target}"
                )

    assert not failures, "Broken internal Markdown links:\n" + "\n".join(failures)
