#!/usr/bin/env python3
"""Normalize derivative font naming before building Softness Mono.

This script changes naming metadata only. It must never modify glyph outlines,
kerning, features, metrics, or original copyright and licence attribution.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"

TEXT_SUFFIXES = {".designspace", ".yaml", ".yml", ".plist", ".py", ".md", ".txt"}

REPLACEMENTS = (
    ("Ubuntu Sans Mono", "Softness Mono"),
    ("UbuntuSansMono", "SoftnessMono"),
)

# These files intentionally preserve the upstream project name for attribution.
ATTRIBUTION_FILES = {
    ROOT / "LICENSE.txt",
    ROOT / "DERIVATIVE-NOTICE.md",
    ROOT / "FONTLOG.txt",
}


def eligible(path: Path) -> bool:
    if path in ATTRIBUTION_FILES:
        return False
    if any(part in {".git", "fonts", "out", "venv"} for part in path.parts):
        return False
    if path.name == "contents.plist":
        return False
    return path.suffix in TEXT_SUFFIXES or path.name == "fontinfo.plist"


def transformed(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def process(check: bool) -> int:
    changed: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or not eligible(path):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated = transformed(original)
        if updated == original:
            continue

        changed.append(path.relative_to(ROOT))
        if not check:
            path.write_text(updated, encoding="utf-8")

    if check and changed:
        print("Softness Mono naming preparation is required in:")
        for path in changed:
            print(f"  - {path}")
        return 1

    if changed:
        print(f"Normalized Softness Mono naming in {len(changed)} files.")
    else:
        print("Softness Mono naming is already normalized.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report files that need normalization without modifying them.",
    )
    args = parser.parse_args()
    return process(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
