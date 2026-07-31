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
    "nm": ("Length", Dim(L=1)),  # bare magnitude raw; convert via `to` (ADR 0124)
    "km": ("Length", Dim(L=1)),  # ADR 0129
    "kg": ("Mass", Dim(M=1)),
    "g": ("Mass", Dim(M=1)),  # ADR 0136
    "lb": ("Mass", Dim(M=1)),  # avoirdupois pound; ADR 0145
    "oz": ("Mass", Dim(M=1)),  # avoirdupois ounce; ADR 0146
    "st": ("Mass", Dim(M=1)),  # British stone; ADR 0147
    "s": ("Time", Dim(T=1)),
    "ms": ("Time", Dim(T=1)),  # bare magnitude raw; convert via `to` (ADR 0124)
    "us": ("Time", Dim(T=1)),  # microsecond ASCII (ADR 0129)
    "ps": ("Time", Dim(T=1)),
    "A": ("Current", Dim(I=1)),
    "K": ("Temperature", Dim(Theta=1)),
    "C": ("Temperature", Dim(Theta=1)),  # Celsius magnitude; convert via affine (ADR 0134)
    "F": ("Temperature", Dim(Theta=1)),  # Fahrenheit; affine (ADR 0135)
    "R": ("Temperature", Dim(Theta=1)),  # Rankine; affine (ADR 0144)
    "kg_m_s": ("Momentum", Dim(L=1, M=1, T=-1)),
    "N": ("Force", Dim(L=1, M=1, T=-2)),
    "N_m": ("Stiffness", Dim(M=1, T=-2)),
    "J": ("Energy", Dim(L=2, M=1, T=-2)),
    "eV": ("Energy", Dim(L=2, M=1, T=-2)),
    "Hz": ("Frequency", Dim(T=-1)),
    "kHz": ("Frequency", Dim(T=-1)),  # ADR 0129
    "MHz": ("Frequency", Dim(T=-1)),  # ADR 0129
    "GHz": ("Frequency", Dim(T=-1)),
    "rad": ("Angle", DIMLESS),
}

# ADR 0124 / 0129: source unit → factor relative to a canonical unit of the same Dim.
# Bare suffixes stay raw; only `expr to target` applies these factors.
UNIT_SCALE_TO_CANONICAL: dict[str, tuple[str, float]] = {
    "ps": ("s", 1e-12),
    "us": ("s", 1e-6),
    "ms": ("s", 1e-3),
    "nm": ("m", 1e-9),
    "km": ("m", 1e3),
    "kHz": ("Hz", 1e3),
    "MHz": ("Hz", 1e6),
    "GHz": ("Hz", 1e9),
    # ADR 0132: exact SI elementary charge (2019) — 1 eV = e J.
    "eV": ("J", 1.602176634e-19),
    # ADR 0136: gram ↔ kilogram.
    "g": ("kg", 1e-3),
    # ADR 0145: international avoirdupois pound (exact).
    "lb": ("kg", 0.45359237),
    # ADR 0146: avoirdupois ounce = lb / 16 (exact).
    "oz": ("kg", 0.45359237 / 16.0),
    # ADR 0147: British stone = 14 lb (exact).
    "st": ("kg", 0.45359237 * 14.0),
    # Canonical units map to themselves (identity) for `x.s to s`.
    "s": ("s", 1.0),
    "m": ("m", 1.0),
    "Hz": ("Hz", 1.0),
    "J": ("J", 1.0),
    "kg": ("kg", 1.0),
}

# ADR 0134 / 0135 / 0144: affine family — canonical = raw * scale + offset.
_F_SCALE = 5.0 / 9.0
_F_OFFSET = 273.15 - 32.0 * _F_SCALE  # ≡ (F + 459.67) * 5/9
_R_SCALE = 5.0 / 9.0  # Rankine absolute; T_K = T_R * 5/9
UNIT_AFFINE_TO_CANONICAL: dict[str, tuple[str, float, float]] = {
    "C": ("K", 1.0, 273.15),
    "F": ("K", _F_SCALE, _F_OFFSET),
    "R": ("K", _R_SCALE, 0.0),
    "K": ("K", 1.0, 0.0),
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
