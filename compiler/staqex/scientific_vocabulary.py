"""Compact scientific spellings shared by the surface parser."""

from __future__ import annotations


# These aliases are lexical conveniences, not runtime constants. Keeping the
# canonical form in the AST gives Unicode and ASCII source one binding identity.
SCIENTIFIC_NAME_ALIASES: dict[str, str] = {
    "psi": "ψ",
    "phi": "φ",
    "rho": "ρ",
}

ALGEBRA_ALIASES: dict[str, str] = {
    "cm": "commutator",
    "ac": "anticommutator",
}


def normalize_scientific_name(name: str) -> str:
    return SCIENTIFIC_NAME_ALIASES.get(name, name)


def normalize_algebra_name(name: str) -> str:
    return ALGEBRA_ALIASES.get(name, name)


def resolve_scientific_binding(name: str, available: object) -> str:
    """Resolve an alias only when its canonical binding is present."""
    if isinstance(available, dict):
        canonical = normalize_scientific_name(name)
        if canonical in available:
            return canonical
    return name
