"""Compile-gate: production compiler pipeline + package namespace helpers."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Resolve production compiler package
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.pipeline import analyze_source as _compiler_analyze  # noqa: E402


@dataclass
class PackageEnv:
    """Minimal package/class namespace for SV-06."""

    packages: dict[str, dict[str, str]]

    def define(self, package: str, name: str, kind: str = "class") -> None:
        self.packages.setdefault(package, {})
        if name in self.packages[package]:
            raise ValueError(f"duplicate {name} in {package}")
        self.packages[package][name] = kind

    def resolve(self, package: str, name: str) -> str:
        if package not in self.packages or name not in self.packages[package]:
            raise LookupError(f"PACKAGE_RESOLVE_ERROR: {package}.{name}")
        return f"{package}.{name}"

    def tensor_compose(self, left: str, right: str) -> str:
        return f"({left}) ⊗ ({right})"


def analyze_source(source: str) -> list[dict[str, Any]]:
    """Lex → Parse → Early Collapse → Typecheck (ADR 0035 / 0027 / Lit-Lift)."""
    return _compiler_analyze(source)
