"""Jordan-Wigner numerical mapping for typed second-quantized operators.

LISS-0032 / ADR 0093. Expands a `FermionOperator` symbolic expression (built
from `create(p)` / `annihilate(p)` atoms combined with `+`, `-`, `*`) into an
`OpExpr` Pauli-sum AST -- the same representation a hand-written `Operator`
expression (`X(0) * Z(1)`, ...) already produces -- so the existing SV
evaluator and QASM/Trotter lowering consume it unchanged.

Convention (normative, ADR 0093):

    a_p     = (prod_{k<p} Z_k) * (X_p + i Y_p) / 2
    a_p^dag = (prod_{k<p} Z_k) * (X_p - i Y_p) / 2

Scope: one-body and two-body fermionic terms (Bravyi-Kitaev, Boson, and Spin
mappings remain deferred). Correctness over performance: terms are expanded
by direct distribution (O(2^k) growth for a k-atom product) with no
term-count optimization, per the Adjudicator's explicit 2026-07-25 decision.
"""

from __future__ import annotations

from .ast_nodes import BinOp, Call, LitInt, OpBin, OpLit, OpPauli, Span, Var

# Single-site Pauli multiplication: (phase, kind) = A * B (same table as
# runtime/sparse_pauli.py's _PAULI_MUL; duplicated to keep this module
# dependency-free of the runtime package).
_PAULI_MUL: dict[tuple[str, str], tuple[complex, str]] = {
    ("I", "I"): (1, "I"),
    ("I", "X"): (1, "X"),
    ("I", "Y"): (1, "Y"),
    ("I", "Z"): (1, "Z"),
    ("X", "I"): (1, "X"),
    ("Y", "I"): (1, "Y"),
    ("Z", "I"): (1, "Z"),
    ("X", "X"): (1, "I"),
    ("Y", "Y"): (1, "I"),
    ("Z", "Z"): (1, "I"),
    ("X", "Y"): (1j, "Z"),
    ("Y", "X"): (-1j, "Z"),
    ("Y", "Z"): (1j, "X"),
    ("Z", "Y"): (-1j, "X"),
    ("Z", "X"): (1j, "Y"),
    ("X", "Z"): (-1j, "Y"),
}

_REAL_TOL = 1e-9
_ZERO_TOL = 1e-12

# A term is (complex coefficient, {qubit_index: pauli_letter}); the dict
# omits identity ("I") entries.
_Term = tuple[complex, dict]


class SecondQuantizationMappingError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _mul_term(a: _Term, b: _Term) -> _Term:
    coeff = a[0] * b[0]
    ops = dict(a[1])
    for q, letter in b[1].items():
        if q in ops:
            phase, result = _PAULI_MUL[(ops[q], letter)]
            coeff *= phase
            if result == "I":
                del ops[q]
            else:
                ops[q] = result
        else:
            ops[q] = letter
    return (coeff, ops)


def _mul_sums(s1: list[_Term], s2: list[_Term]) -> list[_Term]:
    return [_mul_term(a, b) for a in s1 for b in s2]


def _scale_sum(s: list[_Term], factor: complex) -> list[_Term]:
    return [(coeff * factor, ops) for coeff, ops in s]


def _parity_prefix(index: int) -> _Term:
    return (1 + 0j, {k: "Z" for k in range(index)})


def _create(index: int) -> list[_Term]:
    prefix = _parity_prefix(index)
    return [
        _mul_term(prefix, (0.5 + 0j, {index: "X"})),
        _mul_term(prefix, (-0.5j, {index: "Y"})),
    ]


def _annihilate(index: int) -> list[_Term]:
    prefix = _parity_prefix(index)
    return [
        _mul_term(prefix, (0.5 + 0j, {index: "X"})),
        _mul_term(prefix, (0.5j, {index: "Y"})),
    ]


def _orbital_index(expr) -> int:
    if len(expr.args) == 1 and isinstance(expr.args[0], LitInt):
        return expr.args[0].value
    raise SecondQuantizationMappingError(
        "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
        "Jordan-Wigner mapping requires a static integer orbital index",
    )


def _expand(expr) -> list[_Term]:
    """Expand a FermionOperator symbolic expr into a raw (uncoalesced) Pauli
    sum with complex coefficients."""
    if isinstance(expr, Call) and isinstance(expr.callee, Var):
        name = expr.callee.name
        if name == "create":
            return _create(_orbital_index(expr))
        if name == "annihilate":
            return _annihilate(_orbital_index(expr))
        raise SecondQuantizationMappingError(
            "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
            f"`{name}` is not covered by the Jordan-Wigner mapping slice",
        )
    if isinstance(expr, BinOp):
        lhs = _expand(expr.lhs)
        rhs = _expand(expr.rhs)
        if expr.op == "*":
            return _mul_sums(lhs, rhs)
        if expr.op == "+":
            return lhs + rhs
        if expr.op == "-":
            return lhs + _scale_sum(rhs, -1)
        raise SecondQuantizationMappingError(
            "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
            f"operator `{expr.op}` is not covered by the Jordan-Wigner mapping slice",
        )
    raise SecondQuantizationMappingError(
        "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
        f"`{type(expr).__name__}` is not covered by the Jordan-Wigner mapping slice",
    )


def _term_to_op_expr(ops: dict, span: Span):
    if not ops:
        return OpPauli(kind="I", site=None, span=span)
    node = None
    for site in sorted(ops):
        atom = OpPauli(kind=ops[site], site=site, span=span)
        node = atom if node is None else OpBin(op="*", lhs=node, rhs=atom, span=span)
    return node


def jordan_wigner_map(expr, *, span: Span) -> tuple[object, int]:
    """Expand a FermionOperator expr into an (OpExpr, qubit_count) pair.

    The OpExpr is built from real OpLit coefficients and OpPauli/OpBin
    nodes -- the same shape the parser produces for a hand-written Operator
    expression -- so it is consumable by the existing SV evaluator and the
    existing QASM/Trotter lowering path without any further change there.
    """
    raw_terms = _expand(expr)

    grouped: dict[tuple, complex] = {}
    for coeff, ops in raw_terms:
        key = tuple(sorted(ops.items()))
        grouped[key] = grouped.get(key, 0j) + coeff

    max_index = -1
    for key in grouped:
        for site, _letter in key:
            max_index = max(max_index, site)
    qubit_count = max(max_index + 1, 1)

    result = None
    for key, coeff in grouped.items():
        if abs(coeff) < _ZERO_TOL:
            continue
        if abs(coeff.imag) > _REAL_TOL:
            raise SecondQuantizationMappingError(
                "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
                "Jordan-Wigner mapping result is not expressible as a real "
                f"Pauli sum (non-Hermitian residual {coeff!r} on term {dict(key)!r}); "
                "the source fermionic expression must be Hermitian",
            )
        term_node = _term_to_op_expr(dict(key), span)
        real_coeff = coeff.real
        scaled = (
            term_node
            if real_coeff == 1.0
            else OpBin(op="*", lhs=OpLit(value=real_coeff, span=span), rhs=term_node, span=span)
        )
        result = scaled if result is None else OpBin(op="+", lhs=result, rhs=scaled, span=span)

    if result is None:
        result = OpLit(value=0.0, span=span)
    return result, qubit_count
