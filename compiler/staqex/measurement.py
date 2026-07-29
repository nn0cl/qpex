"""Static contracts for terminal POVM measurement declarations."""

from __future__ import annotations

from dataclasses import dataclass

from .ast_nodes import Call, CompilationUnit, Measure, StateBind, Var


@dataclass(frozen=True, slots=True)
class POVMContract:
    name: str
    domain: str
    kind: str


def resolve_measurement_contracts(
    unit: CompilationUnit,
) -> tuple[dict[str, POVMContract], list[dict]]:
    if unit.main is None:
        return {}, []
    povms: dict[str, POVMContract] = {}
    states: dict[str, str] = {}
    diagnostics: list[dict] = []
    for statement in unit.main.body.stmts:
        if not isinstance(statement, StateBind) or statement.ty is None:
            continue
        if len(statement.names) != 1:
            continue
        name = statement.names[0]
        if statement.ty.name in {"State", "DensityState"}:
            domain = statement.ty.args[0].name if statement.ty.args else "Unknown"
            states[name] = domain
        elif statement.ty.name == "POVM":
            domain = _declared_domain(statement)
            if not _is_computational_basis(statement.expr):
                diagnostics.append(
                    _diagnostic(
                        "INVALID_POVM_EFFECT",
                        statement,
                        "the MVP POVM constructor is ComputationalBasis()",
                    )
                )
            povms[name] = POVMContract(
                name=name,
                domain=domain,
                kind="ComputationalBasis",
            )
    for statement in unit.main.body.stmts:
        if not isinstance(statement, Measure) or statement.povm is None:
            continue
        if not isinstance(statement.povm, Var) or statement.povm.name not in povms:
            diagnostics.append(
                _diagnostic(
                    "INVALID_POVM_EFFECT",
                    statement,
                    "measurement requires a declared POVM value",
                )
            )
            continue
        if isinstance(statement.expr, Var):
            source_domain = states.get(statement.expr.name)
            povm_domain = povms[statement.povm.name].domain
            if source_domain is not None and source_domain != povm_domain:
                diagnostics.append(
                    _diagnostic(
                        "POVM_DOMAIN_MISMATCH",
                        statement,
                        f"POVM domain `{povm_domain}` does not match `{source_domain}`",
                    )
                )
    return povms, diagnostics


def _is_computational_basis(expr: object) -> bool:
    return (
        isinstance(expr, Call)
        and isinstance(expr.callee, Var)
        and expr.callee.name == "ComputationalBasis"
        and not expr.args
    )


def _declared_domain(statement: StateBind) -> str:
    return statement.ty.args[0].name if statement.ty and statement.ty.args else "Unknown"


def _diagnostic(code: str, statement: StateBind | Measure, message: str) -> dict:
    span = statement.span
    return {"code": code, "line": span.line, "col": span.col, "message": message}
