"""Experiment surface profile + lane detection (ADR 0176 / 0178)."""

from __future__ import annotations

import re

# Source-visible marker: // staqex-profile: experiment
_PROFILE_RE = re.compile(
    r"^\s*//\s*staqex-profile\s*:\s*experiment\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# ADR 0178: // staqex-lane: experiment|circuit|open
_LANE_RE = re.compile(
    r"^\s*//\s*staqex-lane\s*:\s*(experiment|circuit|open)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

DEFAULT_EXPERIMENT_PACKAGE = ("staqex", "experiment")

# Explicit package declaration (multi-file / library entry).
_PACKAGE_RE = re.compile(r"^\s*package\b", re.MULTILINE)


def has_experiment_profile(source: str) -> bool:
    """Return True for explicit marker or ADR 0182 default (no package line)."""
    if _PROFILE_RE.search(source) is not None:
        return True
    # ADR 0182: single-file / no-package sources default to experiment profile.
    if _PACKAGE_RE.search(source) is None:
        return True
    return False


def detect_lane(source: str) -> str | None:
    """Return explicit lane from source marker, or None if unmarked."""
    m = _LANE_RE.search(source)
    if m is None:
        return None
    return m.group(1).lower()
