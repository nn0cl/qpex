"""Resolution of the declarative Workflow source surface (LISS-0035)."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .ast_nodes import ScientificScopeDecl


@dataclass(frozen=True, slots=True)
class WorkflowContract:
    name: str
    experiment: str
    parameters: tuple[str, ...]
    parameter_types: tuple[str, ...]
    observables: tuple[str, ...]
    until: str | None
    update: str | None
    sealed: bool = True


def resolve_workflow_contracts(
    declarations: tuple[ScientificScopeDecl, ...],
) -> tuple[dict[str, WorkflowContract], list[dict]]:
    contracts: dict[str, WorkflowContract] = {}
    diagnostics: list[dict] = []
    experiment_names = {
        declaration.name
        for declaration in declarations
        if declaration.kind == "experiment"
    }
    for declaration in declarations:
        if declaration.kind != "workflow":
            continue
        fields = dict(declaration.workflow_fields)
        parameters = tuple(value for key, value in declaration.workflow_fields if key == "parameter")
        observables = tuple(value for key, value in declaration.workflow_fields if key == "observable")
        parameter_types = declaration.workflow_parameter_types
        experiment = fields.get("experiment")
        until = fields.get("until")
        update = fields.get("update")
        if experiment is None:
            diagnostics.append(
                {
                    "code": "WORKFLOW_SURFACE_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": f"workflow `{declaration.name}` requires an experiment",
                }
            )
            continue
        if experiment not in experiment_names:
            diagnostics.append(
                {
                    "code": "WORKFLOW_SURFACE_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": f"workflow references unknown experiment `{experiment}`",
                }
            )
        if any(not re.fullmatch(r"Param<[^<>]+>", item) for item in parameter_types):
            diagnostics.append(
                {
                    "code": "WORKFLOW_SURFACE_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": "workflow parameters must use Param<T>",
                }
            )
        if len(set(parameters)) != len(parameters) or len(set(observables)) != len(observables):
            diagnostics.append(
                {
                    "code": "WORKFLOW_SURFACE_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": "workflow parameters and observables must be unique",
                }
            )
        if until is not None:
            match = re.fullmatch(
                r"([A-Za-z_][A-Za-z0-9_]*)\s*(<=|>=|==|!=|<|>)\s*([A-Za-z_][A-Za-z0-9_]*|[0-9]+(?:\.[0-9]+)?)",
                until,
            )
            if match is None or match.group(1) not in observables:
                diagnostics.append(
                    {
                        "code": "WORKFLOW_SURFACE_ERROR",
                        "line": declaration.span.line,
                        "col": declaration.span.col,
                        "message": "until must compare a declared observable with a scalar",
                    }
                )
        if update is not None and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", update):
            diagnostics.append(
                {
                    "code": "WORKFLOW_SURFACE_ERROR",
                    "line": declaration.span.line,
                    "col": declaration.span.col,
                    "message": "update must name a Host callback",
                }
            )
        contracts[declaration.name] = WorkflowContract(
            name=declaration.name,
            experiment=experiment,
            parameters=parameters,
            parameter_types=parameter_types,
            observables=observables,
            until=until,
            update=update,
        )
    return contracts, diagnostics
