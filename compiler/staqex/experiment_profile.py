"""Experiment surface profile detection (ADR 0176 / LISS-0270)."""

from __future__ import annotations

import re

# Source-visible marker: // staqex-profile: experiment
_PROFILE_RE = re.compile(
    r"^\s*//\s*staqex-profile\s*:\s*experiment\s*$",
    re.MULTILINE | re.IGNORECASE,
)

DEFAULT_EXPERIMENT_PACKAGE = ("staqex", "experiment")


def has_experiment_profile(source: str) -> bool:
    """Return True when source declares the experiment profile marker."""
    return _PROFILE_RE.search(source) is not None
