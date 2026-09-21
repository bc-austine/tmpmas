#!/usr/bin/env python3
"""Gate 15 — Outbound-API pattern scan (ADR-019).

Scans `src/` for any pattern that would establish outbound write capability
to an external betting platform. Detects:

  1. HTTP method calls (POST, PUT, PATCH, DELETE) to hosts matching
     patterns in `ops/network/betting-domains.yaml`.
  2. Imports of outbound-transactional libraries not on the approved list.
  3. Hardcoded domain strings matching the prohibited pattern set.

Exit codes:
  0 — no violations found.
  1 — at least one violation found; build should fail.

Usage:
    python scripts/check_outbound_api.py [--config ops/network/betting-domains.yaml] [--src src]
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections.abc import Iterator
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# HTTP methods that indicate a write operation.
WRITE_METHODS = {"post", "put", "patch", "delete"}

# Modules that provide outbound HTTP clients. If any of these is imported and
# used with a write method against a prohibited host, it's a violation.
HTTP_CLIENT_MODULES = {"requests", "httpx", "aiohttp", "urllib.request"}

# Libraries whose import alone suggests outbound transactional intent.
# Anything imported from these that isn't on the allowlist is flagged.
PROHIBITED_LIBRARY_PATTERNS = [
    r"^stripe$",
    r"^paypal",
    r"^braintree",
    r"^squareup",
]


class Violation:
    """A single detected violation."""

    def __init__(self, file: Path, line: int, rule: str, detail: str) -> None:
        self.file = file
        self.line = line
        self.rule = rule
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: [{self.rule}] {self.detail}"


def load_config(config_path: Path) -> tuple[list[str], list[str]]:
    """Return (prohibited_patterns, approved_domains) from the YAML config."""
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    prohibited = [entry["pattern"] for entry in config.get("write_prohibited_patterns", [])]
    approved = []
    for source in config.get("approved_sources", []):
        approved.extend(source.get("domains", []))

    return prohibited, approved


def iter_python_files(root: Path) -> Iterator[Path]:
    """Yield every .py file under root, excluding noise directories."""
    exclude = {".git", "__pycache__", ".venv", "venv", "build", "dist"}
    for path in root.rglob("*.py"):
        if any(part in exclude for part in path.parts):
            continue
        yield path


def scan_file(path: Path, prohibited: list[str], approved: list[str]) -> list[Violation]:
    """Return violations found in a single file."""
    violations: list[Violation] = []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return violations

    # --- Rule 1: HTTP write calls to prohibited hosts ------------------------
    for node in ast.walk(tree):
        # Look for `requests.post(...)` style calls
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in WRITE_METHODS:
                # Look for a string literal URL argument
                url_literal = _extract_url_from_call(node)
                if url_literal and _matches_any(url_literal, prohibited):
                    violations.append(
                        Violation(
                            path,
                            node.lineno,
                            "outbound-write-to-prohibited-host",
                            f"{func.attr.upper()} to prohibited host in {url_literal!r}",
                        )
                    )

    # --- Rule 2: Hardcoded prohibited domain strings -------------------------
    for lineno, line in enumerate(source.splitlines(), start=1):
        for pattern in prohibited:
            if re.search(pattern, line, re.IGNORECASE):
                # Skip the config file itself and comments that look like doc
                if "# " in line and line.strip().startswith("#"):
                    continue
                violations.append(
                    Violation(
                        path,
                        lineno,
                        "hardcoded-prohibited-domain",
                        f"line matches prohibited pattern {pattern!r}",
                    )
                )

    # --- Rule 3: Prohibited library imports ----------------------------------
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for pattern in PROHIBITED_LIBRARY_PATTERNS:
                    if re.match(pattern, alias.name):
                        violations.append(
                            Violation(
                                path,
                                node.lineno,
                                "prohibited-library-import",
                                f"imports prohibited library {alias.name!r}",
                            )
                        )
        elif isinstance(node, ast.ImportFrom) and node.module:
            for pattern in PROHIBITED_LIBRARY_PATTERNS:
                if re.match(pattern, node.module):
                    violations.append(
                        Violation(
                            path,
                            node.lineno,
                            "prohibited-library-import",
                            f"imports prohibited library {node.module!r}",
                        )
                    )

    return violations


def _extract_url_from_call(node: ast.Call) -> str | None:
    """Extract the URL literal from a call like requests.post('https://...')."""
    if node.args and isinstance(node.args[0], ast.Constant):
        value = node.args[0].value
        if isinstance(value, str):
            return value
    for keyword in node.keywords:
        if keyword.arg == "url" and isinstance(keyword.value, ast.Constant):
            value = keyword.value.value
            if isinstance(value, str):
                return value
    return None


def _matches_any(url: str, patterns: list[str]) -> bool:
    """Return True if the URL matches any of the given regex patterns."""
    for pattern in patterns:
        try:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        except re.error:
            continue
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate 15 — Outbound-API pattern scan (ADR-019)")
    parser.add_argument("--config", default="ops/network/betting-domains.yaml", type=Path)
    parser.add_argument("--src", default="src", type=Path)
    args = parser.parse_args()

    if not args.config.exists():
        print(f"ERROR: config file not found: {args.config}", file=sys.stderr)
        return 2

    if not args.src.exists():
        print(f"src directory not found: {args.src}; nothing to scan.")
        return 0

    prohibited, approved = load_config(args.config)
    print(f"Loaded {len(prohibited)} prohibited patterns, {len(approved)} approved domains.")

    all_violations: list[Violation] = []
    file_count = 0
    for path in iter_python_files(args.src):
        file_count += 1
        all_violations.extend(scan_file(path, prohibited, approved))

    print(f"Scanned {file_count} Python files under {args.src}.")

    if not all_violations:
        print("Gate 15 PASSED: no outbound transactional patterns detected.")
        return 0

    print(f"Gate 15 FAILED: {len(all_violations)} violation(s) found.", file=sys.stderr)
    for v in all_violations:
        print(f"  {v}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
