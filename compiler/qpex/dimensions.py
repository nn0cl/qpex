"""Physical dimensions — Lᴹ Mᵀ style exponent vectors (compile-time only)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Dim:
    """Dimension vector (L, M, T) exponents."""

    L: int = 0
    M: int = 0
    T: int = 0

    def mul(self, other: Dim) -> Dim:
        return Dim(self.L + other.L, self.M + other.M, self.T + other.T)

    def div(self, other: Dim) -> Dim:
        return Dim(self.L - other.L, self.M - other.M, self.T - other.T)

    def pow(self, n: int) -> Dim:
        return Dim(self.L * n, self.M * n, self.T * n)

    def matches(self, other: Dim) -> bool:
        return self.L == other.L and self.M == other.M and self.T == other.T

    def is_dimensionless(self) -> bool:
        return self.L == 0 and self.M == 0 and self.T == 0

    def pretty(self) -> str:
        """Physicist-facing bracket, e.g. `[Length]` or `[Time · Length]`."""
        if self.is_dimensionless():
            return "[1]"
        named = _NAME_BY_DIM.get((self.L, self.M, self.T))
        if named is not None:
            return f"[{named}]"
        parts: list[str] = []
        for e, label in ((self.L, "Length"), (self.M, "Mass"), (self.T, "Time")):
            if e == 0:
                continue
            if e == 1:
                parts.append(label)
            elif e == -1:
                parts.append(f"{label}^{{-1}}")
            else:
                parts.append(f"{label}^{{{e}}}")
        return "[" + " · ".join(parts) + "]"

    def __str__(self) -> str:
        return self.pretty()


DIMLESS = Dim()

# Named quantity → dimension
TYPE_DIMS: dict[str, Dim] = {
    "Int": DIMLESS,
    "Float": DIMLESS,
    "Bool": DIMLESS,
    "String": DIMLESS,
    "Any": DIMLESS,
    "Length": Dim(L=1),
    "Mass": Dim(M=1),
    "Time": Dim(T=1),
    "Momentum": Dim(L=1, M=1, T=-1),
    "Force": Dim(L=1, M=1, T=-2),
    "Energy": Dim(L=2, M=1, T=-2),
    "Stiffness": Dim(M=1, T=-2),  # N/m = kg/s²
    "Frequency": Dim(T=-1),
    "Angle": DIMLESS,
    "Dimensionless": DIMLESS,
}

_NAME_BY_DIM: dict[tuple[int, int, int], str] = {
    (d.L, d.M, d.T): name
    for name, d in TYPE_DIMS.items()
    if name
    not in {"Int", "Float", "Bool", "String", "Any", "Angle", "Dimensionless"}
}

# Unit suffix on numeric literal → (payload name, dimension)
UNIT_TABLE: dict[str, tuple[str, Dim]] = {
    "m": ("Length", Dim(L=1)),
    "kg": ("Mass", Dim(M=1)),
    "s": ("Time", Dim(T=1)),
    "ms": ("Time", Dim(T=1)),  # magnitude still raw; no SI scale convert in MVP
    "kg_m_s": ("Momentum", Dim(L=1, M=1, T=-1)),
    "N": ("Force", Dim(L=1, M=1, T=-2)),
    "N_m": ("Stiffness", Dim(M=1, T=-2)),
    "J": ("Energy", Dim(L=2, M=1, T=-2)),
    "Hz": ("Frequency", Dim(T=-1)),
    "rad": ("Angle", DIMLESS),
}

# Type names that may head a Type-First declaration (besides Capitalized idents)
TYPE_HEADS: frozenset[str] = frozenset(TYPE_DIMS) | frozenset({"State", "Delta"})


def dim_of_type_name(name: str) -> Dim:
    return TYPE_DIMS.get(name, DIMLESS)


def format_dim_mismatch(left: Dim, right: Dim, op: str) -> str:
    return (
        f"dimension mismatch for `{op}`: {left.pretty()} vs {right.pretty()} "
        f"— physically incompatible"
    )
