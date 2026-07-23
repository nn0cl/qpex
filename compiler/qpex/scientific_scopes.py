"""Resolution of phase-separated scientific scope contracts (LISS-0034)."""

from __future__ import annotations

from collections.abc import Iterable

from .ast_nodes import ScientificScopeContract, ScientificScopeDecl


_ALLOWED_REFERENCES = {
    "theory": {"theory"},
    "experiment": {"theory", "experiment"},
    "workflow": {"theory", "experiment", "workflow"},
    "execution": {"theory", "experiment", "workflow", "execution"},
    "report": {"execution", "report"},
}


def resolve_scientific_scopes(
    declarations: Iterable[ScientificScopeDecl],
) -> tuple[dict[str, ScientificScopeContract], list[dict]]:
    """Seal scope declarations and validate their dependency direction."""

    declarations = tuple(declarations)
    names = {declaration.name for declaration in declarations}
    contracts: dict[str, ScientificScopeContract] = {}
    diagnostics: list[dict] = []

    for declaration in declarations:
        for reference in declaration.references:
            if reference not in names:
                diagnostics.append(
                    {
                        "code": "PHASE_SCOPE_REFERENCE_ERROR",
                        "line": declaration.span.line,
                        "col": declaration.span.col,
                        "message": (
                            f"scope `{declaration.name}` references unknown "
                            f"scope `{reference}`"
                        ),
                    }
                )
                continue
            referenced = next(
                item for item in declarations if item.name == reference
            )
            allowed = _ALLOWED_REFERENCES.get(declaration.kind, set())
            if referenced.kind not in allowed:
                diagnostics.append(
                    {
                        "code": "PHASE_SCOPE_DIRECTION_ERROR",
                        "line": declaration.span.line,
                        "col": declaration.span.col,
                        "message": (
                            f"{declaration.kind} scope `{declaration.name}` "
                            f"cannot depend on {referenced.kind} scope "
                            f"`{reference}`"
                        ),
                    }
                )
        contracts[declaration.name] = ScientificScopeContract(
            kind=declaration.kind,
            name=declaration.name,
            references=tuple(declaration.references),
            symbols=tuple(declaration.symbols),
        )

    return contracts, diagnostics
