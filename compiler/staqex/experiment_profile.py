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


def has_experiment_profile(source: str) -> bool:
    """Return True when source declares the experiment profile marker."""
    return _PROFILE_RE.search(source) is not None


def detect_lane(source: str) -> str | None:
    """Return explicit lane from source marker, or None if unmarked."""
    m = _LANE_RE.search(source)
    if m is None:
        return None
    return m.group(1).lower()
