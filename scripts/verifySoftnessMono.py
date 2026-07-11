#!/usr/bin/env python3
"""Verify generated fonts identify exclusively as Softness Mono."""

from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIRS = (ROOT / "fonts" / "variable", ROOT / "fonts" / "ttf")
EXPECTED_FAMILY = "Softness Mono"
FORBIDDEN_FAMILY = "Ubuntu Sans Mono"


def decoded_names(font: TTFont) -> list[str]:
    values: list[str] = []
    for record in font["name"].names:
        try:
            values.append(record.toUnicode())
        except Exception:
            continue
    return values


def main() -> int:
    paths: list[Path] = []
    for directory in FONT_DIRS:
        if directory.exists():
            paths.extend(sorted(directory.glob("*.ttf")))
            paths.extend(sorted(directory.glob("*.otf")))

    if not paths:
        print("No generated font files were found.", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in paths:
        font = TTFont(path)
        names = decoded_names(font)
        if not any(EXPECTED_FAMILY in name for name in names):
            failures.append(f"{path.relative_to(ROOT)} has no Softness Mono family name")
        if any(FORBIDDEN_FAMILY in name for name in names):
            failures.append(f"{path.relative_to(ROOT)} still exposes Ubuntu Sans Mono")
        if not path.name.startswith("SoftnessMono"):
            failures.append(f"{path.relative_to(ROOT)} has a legacy output filename")

    if failures:
        print("Generated font naming verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"Verified Softness Mono naming in {len(paths)} generated fonts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
