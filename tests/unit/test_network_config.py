"""Validate ops/network/betting-domains.yaml and the DNS blocklist config.

These tests run in CI (stage 6 — unit-tests) and verify:
  - The YAML parses cleanly.
  - The pattern list is non-empty.
  - Every pattern is a valid regex.
  - The network_policy enforcement block is enabled.
  - The generate-config.py script extracts the expected domains.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "ops" / "network" / "betting-domains.yaml"


@pytest.fixture(scope="module")
def config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_config_file_exists() -> None:
    assert CONFIG_PATH.exists(), f"Missing {CONFIG_PATH}"


def test_config_parses_as_yaml(config: dict) -> None:
    assert isinstance(config, dict)


def test_has_prohibited_patterns(config: dict) -> None:
    patterns = config.get("write_prohibited_patterns", [])
    assert len(patterns) >= 1, "Must have at least one prohibited pattern"


def test_every_pattern_is_valid_regex(config: dict) -> None:
    patterns = config.get("write_prohibited_patterns", [])
    for entry in patterns:
        pattern = entry.get("pattern")
        assert pattern, f"Entry missing 'pattern': {entry}"
        # Should not raise
        re.compile(pattern)


def test_every_pattern_matches_expected_shape(config: dict) -> None:
    """Every pattern should be extractable by generate-config.py's regex."""
    extractor = re.compile(r"^\(\^\|\\\.\)(.+?)\\\.(.+?)\$$")
    patterns = config.get("write_prohibited_patterns", [])
    unmatched = [e["pattern"] for e in patterns if not extractor.match(e["pattern"])]
    assert not unmatched, f"Patterns not extractable as domains: {unmatched}"


def test_network_policy_enabled(config: dict) -> None:
    enforcement = config.get("enforcement", {})
    net_policy = enforcement.get("network_policy", {})
    assert net_policy.get("enabled") is True, "Network policy must be enabled"
    assert net_policy.get("mechanism") == "dns-blocklist"


def test_approved_sources_have_metadata(config: dict) -> None:
    """Every approved source should have domain + purpose fields."""
    sources = config.get("approved_sources", [])
    for source in sources:
        assert "name" in source
        assert "domains" in source
        assert isinstance(source["domains"], list)
        assert "purpose" in source


def test_known_blocked_domain_extracted(config: dict) -> None:
    """A known pattern ('bet365.com') must be present and extractable."""
    patterns = [e["pattern"] for e in config.get("write_prohibited_patterns", [])]
    assert any("bet365" in p for p in patterns), "Expected bet365.com in blocklist"
