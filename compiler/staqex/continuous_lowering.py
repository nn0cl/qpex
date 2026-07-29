"""Numerical lowering for explicit discretization bridges (LISS-0111)."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .ast_nodes import DiscretizationBridgeDecl, DiscretizationDecl, ScientificScopeDecl, StateBind
from .discretization import DiscretizationBridge, DiscretizationContract
from .runtime.hamiltonian import compile_hamiltonian
from .runtime.matrix import Matrix

DISCRETIZATION_LOWERING_ERROR = "DISCRETIZATION_LOWERING_ERROR"

_DEFAULT_XMIN = -math.pi
_DEFAULT_XMAX = math.pi
_FD_ORDER_RE = re.compile(r"FiniteDifference\s*\(\s*order\s*=\s*(\d+)\s*\)")


@dataclass(frozen=True, slots=True)
class GridHamiltonianRef:
    """Runtime marker for a lowered discretization bridge alias."""

    alias: str


@dataclass(frozen=True, slots=True)
class GridHamiltonian:
    """Finite grid Hamiltonian produced from a Theory-to-Kernel bridge."""

    alias: str
    contract: str
    source: str
    xs: tuple[float, ...]
    matrix: tuple[tuple[complex, ...], ...]
    sealed: bool = True


def lower_discretization_bridges(
    bridges: dict[str, DiscretizationBridge],
    contracts: dict[str, DiscretizationContract],
    scopes: tuple[ScientificScopeDecl, ...],
) -> tuple[dict[str, GridHamiltonian], list[dict]]:
    lowered: dict[str, GridHamiltonian] = {}
    diagnostics: list[dict] = []
    scope_by_name = {scope.name: scope for scope in scopes}
    for alias, bridge in bridges.items():
        contract = contracts.get(bridge.contract)
        if contract is None:
            continue
        diag = _validate_mvp_contract(contract)
        if diag is not None:
            diagnostics.append(diag)
            continue
        theory_op = _theory_operator_expr(bridge.source, scope_by_name)
        if theory_op is None:
            diagnostics.append(
                _diag(
                    DISCRETIZATION_LOWERING_ERROR,
                    f"bridge `{alias}` cannot resolve theory operator `{bridge.source}`",
                )
            )
            continue
        try:
            xs = _uniform_periodic_grid(int(contract.resolution))
            matrix = compile_hamiltonian(
                theory_op,
                env={},
                scalars={},
                n_qubits=-1,
                grid_xs=xs,
            )
        except (TypeError, ValueError) as exc:
            diagnostics.append(
                _diag(
                    DISCRETIZATION_LOWERING_ERROR,
                    f"bridge `{alias}` lowering failed: {exc}",
                )
            )
            continue
        lowered[alias] = GridHamiltonian(
            alias=alias,
            contract=bridge.contract,
            source=bridge.source,
            xs=tuple(xs),
            matrix=_freeze_matrix(matrix),
        )
    return lowered, diagnostics


def _validate_mvp_contract(contract: DiscretizationContract) -> dict | None:
    if contract.domain != "Position":
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            (
                f"discretization `{contract.name}` domain `{contract.domain}` is not "
                "lowered in the LISS-0111 MVP (Position only)"
            ),
        )
    if contract.basis != "UniformGrid":
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            (
                f"discretization `{contract.name}` basis `{contract.basis}` is not "
                "lowered in the LISS-0111 MVP (UniformGrid only)"
            ),
        )
    if contract.boundary != "Periodic":
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            (
                f"discretization `{contract.name}` boundary `{contract.boundary}` is not "
                "lowered in the LISS-0111 MVP (Periodic only)"
            ),
        )
    match = _FD_ORDER_RE.search(contract.approximation)
    if match is None or int(match.group(1)) != 2:
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            (
                f"discretization `{contract.name}` approximation "
                f"`{contract.approximation}` requires FiniteDifference(order = 2)"
            ),
        )
    try:
        resolution = int(contract.resolution)
    except ValueError:
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            f"discretization `{contract.name}` resolution must be an integer literal",
        )
    if resolution < 2:
        return _diag(
            DISCRETIZATION_LOWERING_ERROR,
            f"discretization `{contract.name}` resolution must be at least 2",
        )
    return None


def _uniform_periodic_grid(resolution: int) -> list[float]:
  xmin, xmax = _DEFAULT_XMIN, _DEFAULT_XMAX
  return [xmin + (xmax - xmin) * index / resolution for index in range(resolution)]


def _theory_operator_expr(
    source: str,
    scopes: dict[str, ScientificScopeDecl],
) -> object | None:
    parts = source.split(".")
    if len(parts) != 2:
        return None
    scope = scopes.get(parts[0])
    if scope is None or scope.kind != "theory":
        return None
    for declaration in scope.body_declarations:
        if (
            isinstance(declaration, StateBind)
            and declaration.ty is not None
            and declaration.ty.name == "Operator"
            and declaration.names == [parts[1]]
        ):
            return declaration.expr
    return None


def _freeze_matrix(matrix: Matrix) -> tuple[tuple[complex, ...], ...]:
    return tuple(tuple(row) for row in matrix)


def _diag(code: str, message: str) -> dict:
    return {"code": code, "message": message}
