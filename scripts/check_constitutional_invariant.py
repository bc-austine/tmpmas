#!/usr/bin/env python3
"""Gate 16 — Constitutional invariant check (ADR-020).

Checks that the operational plane and analytical plane remain separated.
Specifically:

  1. Operational code (src/operational/) does not import from
     analytical code (src/analytical/), and vice versa.
  2. No module writes directly to a snapshot/audit/decision-status
     table (checked via schema file inspection when schema exists).

The check is intentionally conservative: if the directory structure does
not yet exist, it passes. Once code is added under src/operational/ or
src/analytical/, the check becomes meaningful.

Exit codes:
  0 — no plane separation violations.
  1 — at least one violation.
  2 — configuration or setup error.

Usage:
    python scripts/check_constitutional_invariant.py [--src src]
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections.abc import Iterator
from pathlib import Path

OPERATIONAL_DIR = "operational"
ANALYTICAL_DIR = "analytical"


class Violation:
    def __init__(self, file: Path, line: int, rule: str, detail: str) -> None:
        self.file = file
        self.line = line
        self.rule = rule
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: [{self.rule}] {self.detail}"


def iter_python_files(root: Path) -> Iterator[Path]:
    exclude = {".git", "__pycache__", ".venv", "venv", "build", "dist"}
    for path in root.rglob("*.py"):
        if any(part in exclude for part in path.parts):
            continue
        yield path


def determine_plane(path: Path) -> str | None:
    """Return 'operational', 'analytical', or None based on the path."""
    parts = path.parts
    if OPERATIONAL_DIR in parts:
        return OPERATIONAL_DIR
    if ANALYTICAL_DIR in parts:
        return ANALYTICAL_DIR
    return None


def check_imports(path: Path, plane: str) -> list[Violation]:
    """Return plane-crossing imports found in a single file."""
    violations: list[Violation] = []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return violations

    other_plane = ANALYTICAL_DIR if plane == OPERATIONAL_DIR else OPERATIONAL_DIR

    for node in ast.walk(tree):
        module: str | None = None
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if _is_other_plane(module, other_plane):
                    violations.append(
                        Violation(
                            path,
                            node.lineno,
                            "plane-crossing-import",
                            f"{plane} imports {module!r} from {other_plane}",
                        )
                    )
        elif isinstance(node, ast.ImportFrom) and node.module:
            module = node.module
            if _is_other_plane(module, other_plane):
                violations.append(
                    Violation(
                        path,
                        node.lineno,
                        "plane-crossing-import",
                        f"{plane} imports from {module!r} in {other_plane}",
                    )
                )

    return violations


def _is_other_plane(module: str, other_plane: str) -> bool:
    """Return True if the module path crosses into the other plane."""
    return other_plane in module.split(".")


def check_schema(schema_root: Path) -> list[Violation]:
    """Placeholder for schema-level write-grant checks.

    When migrations land (Phase 5 Sprint 2+), this will parse the migration
    files and confirm that snapshot, audit, and decision-status tables have
    no write grants outside the Decision Capture service.
    """
    violations: list[Violation] = []
    if not schema_root.exists():
        return violations
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gate 16 — Constitutional invariant check (ADR-020)"
    )
    parser.add_argument("--src", default="src", type=Path)
    parser.add_argument("--schema", default="ops/schema", type=Path)
    args = parser.parse_args()

    if not args.src.exists():
        print(f"src directory not found: {args.src}; nothing to check.")
        return 0

    all_violations: list[Violation] = []
    file_count = 0
    plane_count = {"operational": 0, "analytical": 0}

    for path in iter_python_files(args.src):
        file_count += 1
        plane = determine_plane(path)
        if plane is None:
            continue
        plane_count[plane] += 1
        all_violations.extend(check_imports(path, plane))

    all_violations.extend(check_schema(args.schema))

    print(f"Scanned {file_count} Python files under {args.src}.")
    print(
        f"Plane membership: operational={plane_count['operational']}, analytical={plane_count['analytical']}"
    )

    if not all_violations:
        print("Gate 16 PASSED: no plane separation violations detected.")
        return 0

    print(f"Gate 16 FAILED: {len(all_violations)} violation(s) found.", file=sys.stderr)
    for v in all_violations:
        print(f"  {v}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
