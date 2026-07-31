"""Physical dimensions — Lᴹ Mᵀ I Θ style exponent vectors (compile-time only)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Dim:
    """Dimension vector (L, M, T, I, Theta) exponents (ADR 0121)."""

    L: int = 0
    M: int = 0
    T: int = 0
    I: int = 0
    Theta: int = 0

    def mul(self, other: Dim) -> Dim:
        return Dim(
            self.L + other.L,
            self.M + other.M,
            self.T + other.T,
            self.I + other.I,
            self.Theta + other.Theta,
        )

    def div(self, other: Dim) -> Dim:
        return Dim(
            self.L - other.L,
            self.M - other.M,
            self.T - other.T,
            self.I - other.I,
            self.Theta - other.Theta,
        )

    def pow(self, n: int) -> Dim:
        return Dim(self.L * n, self.M * n, self.T * n, self.I * n, self.Theta * n)

    def matches(self, other: Dim) -> bool:
        return (
            self.L == other.L
            and self.M == other.M
            and self.T == other.T
            and self.I == other.I
            and self.Theta == other.Theta
        )

    def is_dimensionless(self) -> bool:
        return (
            self.L == 0
            and self.M == 0
            and self.T == 0
            and self.I == 0
            and self.Theta == 0
        )

    def pretty(self) -> str:
        """Physicist-facing bracket, e.g. `[Length]` or `[Time · Length]`."""
        if self.is_dimensionless():
            return "[1]"
        named = _NAME_BY_DIM.get((self.L, self.M, self.T, self.I, self.Theta))
        if named is not None:
            return f"[{named}]"
        parts: list[str] = []
        for e, label in (
            (self.L, "Length"),
            (self.M, "Mass"),
            (self.T, "Time"),
            (self.I, "Current"),
            (self.Theta, "Temperature"),
        ):
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
    "Current": Dim(I=1),
    "Temperature": Dim(Theta=1),
    "Momentum": Dim(L=1, M=1, T=-1),
    "Force": Dim(L=1, M=1, T=-2),
    "Energy": Dim(L=2, M=1, T=-2),
    "Stiffness": Dim(M=1, T=-2),  # N/m = kg/s²
    "Frequency": Dim(T=-1),
    "Angle": DIMLESS,
    "Dimensionless": DIMLESS,
    # Discrete quantum / walk carriers (dimensionless labels; ADR 0044)
    "Qubit": DIMLESS,
    "Coin": DIMLESS,
    "Position": DIMLESS,
}

# ADR 0114 / LISS-0121: Type-First heads that are elaboration coefficients
# (classical VO), not linear quantum Joint coordinates.
ELABORATION_COEFFICIENT_HEADS: frozenset[str] = frozenset({
    "Int",
    "Float",
    "Bool",
    "String",
    "Angle",
    "Dimensionless",
    "Length",
    "Mass",
    "Time",
    "Current",
    "Temperature",
    "Momentum",
    "Force",
    "Energy",
    "Stiffness",
    "Frequency",
})

_NAME_BY_DIM: dict[tuple[int, int, int, int, int], str] = {
    (d.L, d.M, d.T, d.I, d.Theta): name
    for name, d in TYPE_DIMS.items()
    if name
    not in {"Int", "Float", "Bool", "String", "Any", "Angle", "Dimensionless"}
}

# Unit suffix on numeric literal → (payload name, dimension)
UNIT_TABLE: dict[str, tuple[str, Dim]] = {
    "m": ("Length", Dim(L=1)),
    "nm": ("Length", Dim(L=1)),  # magnitude raw; no SI scale convert in MVP
    "kg": ("Mass", Dim(M=1)),
    "s": ("Time", Dim(T=1)),
    "ms": ("Time", Dim(T=1)),  # magnitude still raw; no SI scale convert in MVP
    "ps": ("Time", Dim(T=1)),
    "A": ("Current", Dim(I=1)),
    "K": ("Temperature", Dim(Theta=1)),
    "kg_m_s": ("Momentum", Dim(L=1, M=1, T=-1)),
    "N": ("Force", Dim(L=1, M=1, T=-2)),
    "N_m": ("Stiffness", Dim(M=1, T=-2)),
    "J": ("Energy", Dim(L=2, M=1, T=-2)),
    "eV": ("Energy", Dim(L=2, M=1, T=-2)),
    "Hz": ("Frequency", Dim(T=-1)),
    "GHz": ("Frequency", Dim(T=-1)),
    "rad": ("Angle", DIMLESS),
}

# Type names that may head a Type-First declaration (besides Capitalized idents)
TYPE_HEADS: frozenset[str] = frozenset(TYPE_DIMS) | frozenset(
    {"State", "Delta", "Operator"}
)


def product_payload(parts: list[str]) -> str:
    """Encode product carrier as `(A, B, …)` for State<(…)>. """
    if len(parts) == 1:
        return parts[0]
    return "(" + ", ".join(parts) + ")"


def split_product_payload(payload: str) -> list[str] | None:
    """Parse `(A, B)` product payload; None if not a product."""
    s = payload.strip()
    if not (s.startswith("(") and s.endswith(")")):
        return None
    inner = s[1:-1].strip()
    if not inner:
        return []
    parts: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in inner:
        if ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf).strip())
    return parts if all(parts) else None


def dim_of_type_name(name: str) -> Dim:
    return TYPE_DIMS.get(name, DIMLESS)


def format_dim_mismatch(left: Dim, right: Dim, op: str) -> str:
    return (
        f"dimension mismatch for `{op}`: {left.pretty()} vs {right.pretty()} "
        f"— physically incompatible"
    )
