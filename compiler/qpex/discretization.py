"""Resolution of explicit continuous-domain discretization contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .ast_nodes import DiscretizationBridgeDecl, DiscretizationDecl, ScientificScopeDecl


@dataclass(frozen=True, slots=True)
class DiscretizationContract:
    name: str
    domain: str
    basis: str
    resolution: str
    boundary: str
    approximation: str
    error_bound: str | None
    sealed: bool = True


@dataclass(frozen=True, slots=True)
class DiscretizationBridge:
    alias: str
    contract: str
    source: str
    sealed: bool = True


_REQUIRED = ("domain", "basis", "resolution", "boundary", "approximation")


def resolve_discretization_contracts(
    declarations: tuple[DiscretizationDecl, ...],
) -> tuple[dict[str, DiscretizationContract], list[dict]]:
    contracts: dict[str, DiscretizationContract] = {}
    diagnostics: list[dict] = []
    for declaration in declarations:
        fields = dict(declaration.fields)
        missing = [field for field in _REQUIRED if field not in fields]
        if missing:
            diagnostics.append(
                {
                    "code": "DISCRETIZATION_CONTRACT_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": (
                        f"discretization `{declaration.name}` is missing: "
                        + ", ".join(missing)
                    ),
                }
            )
            continue
        if fields["domain"] not in {"Position", "Momentum", "PhaseAngle"}:
            diagnostics.append(
                {
                    "code": "DISCRETIZATION_CONTRACT_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": f"unsupported MVP discretization domain `{fields['domain']}`",
                }
            )
        if fields["basis"] not in {"UniformGrid", "FourierBasis", "PlaneWave", "DVR"}:
            diagnostics.append(
                {
                    "code": "DISCRETIZATION_CONTRACT_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": f"unsupported MVP basis `{fields['basis']}`",
                }
            )
        contracts[declaration.name] = DiscretizationContract(
            name=declaration.name,
            domain=fields["domain"],
            basis=fields["basis"],
            resolution=fields["resolution"],
            boundary=fields["boundary"],
            approximation=fields["approximation"],
            error_bound=fields.get("error_bound"),
        )
    return contracts, diagnostics


def resolve_discretization_bridges(
    bridges: tuple[DiscretizationBridgeDecl, ...],
    contracts: dict[str, DiscretizationContract],
    declarations: tuple[ScientificScopeDecl, ...],
) -> tuple[dict[str, DiscretizationBridge], list[dict]]:
    resolved: dict[str, DiscretizationBridge] = {}
    diagnostics: list[dict] = []
    scopes = {declaration.name: declaration for declaration in declarations}
    for bridge in bridges:
        source_parts = bridge.source.split(".")
        source_scope = scopes.get(source_parts[0])
        source_name = source_parts[1] if len(source_parts) == 2 else None
        has_source = bool(
            source_scope
            and source_scope.kind == "theory"
            and source_name
            and any(
                getattr(item, "names", []) == [source_name]
                for item in source_scope.body_declarations
            )
        )
        if bridge.contract not in contracts or not has_source:
            diagnostics.append(
                {
                    "code": "DISCRETIZATION_BRIDGE_ERROR",
                    "line": bridge.span.line,
                    "col": bridge.span.col,
                    "message": (
                        f"bridge `{bridge.alias}` requires a known discretization "
                        f"contract and Theory operator: {bridge.contract} / {bridge.source}"
                    ),
                }
            )
            continue
        resolved[bridge.alias] = DiscretizationBridge(
            alias=bridge.alias,
            contract=bridge.contract,
            source=bridge.source,
        )
    return resolved, diagnostics
