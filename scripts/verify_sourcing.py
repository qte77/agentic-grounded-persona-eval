#!/usr/bin/env python3
"""Fails if any blockquote in a findings.md's markdown lacks a sourced URL.

Usage: verify_sourcing.py <findings.md> [...]
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

LINK_RE = re.compile(r"\[[^\]]*\]\(https?://[^)]+\)")
QUOTE_LINE_RE = re.compile(r"^>\s?(.*)$")


@dataclass(frozen=True)
class Violation:
    start_line: int
    snippet: str


def find_unsourced_quotes(markdown: str) -> list[Violation]:
    """Groups consecutive '>' lines into blockquotes; flags any group with no markdown link."""
    violations: list[Violation] = []
    group_lines: list[str] = []
    group_start = 0

    def flush() -> None:
        if not group_lines:
            return
        text = "\n".join(group_lines)
        if not LINK_RE.search(text):
            snippet = group_lines[0][:80]
            violations.append(Violation(start_line=group_start, snippet=snippet))

    for lineno, raw_line in enumerate(markdown.splitlines(), start=1):
        m = QUOTE_LINE_RE.match(raw_line)
        if m:
            if not group_lines:
                group_start = lineno
            group_lines.append(m.group(1))
        else:
            flush()
            group_lines = []
    flush()

    return violations


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: verify_sourcing.py <findings.md> [...]", file=sys.stderr)
        return 2

    exit_code = 0
    for path in argv:
        with open(path, encoding="utf-8") as f:
            markdown = f.read()
        violations = find_unsourced_quotes(markdown)
        if violations:
            exit_code = 1
            print(f"{path}: {len(violations)} unsourced quote block(s)")
            for v in violations:
                print(f"  line {v.start_line}: {v.snippet!r}")
        else:
            print(f"{path}: all quote blocks sourced")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
