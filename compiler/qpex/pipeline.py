"""Compiler pipeline: Lexer → Parser → Early Collapse → Typecheck."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .ast_nodes import CompilationUnit, DiscretizationBridgeDecl, DiscretizationDecl, ScientificScopeDecl, ScientificScopeContract
from .finite_binder import IDENTITY_ACTING_SPACE_UNDETERMINED
from .early_collapse import check_early_collapse
from .lexer import Lexer
from .modules import load_module_graph, merge_modules
from .nested_when import check_nested_when
from .parser import ParseError, Parser
from .physical_axioms import check_physical_axioms
from .symbolic_ir import build_symbolic_ir
from .scientific_scopes import resolve_scientific_scopes
from .workflow_surface import WorkflowContract, resolve_workflow_contracts
from .discretization import DiscretizationBridge, DiscretizationContract, resolve_discretization_bridges, resolve_discretization_contracts
from .mixed_state import MixedStateContract, resolve_mixed_state_contracts
from .measurement import POVMContract, resolve_measurement_contracts
from .qpu_ir import build_qpu_ir, qpu_ir_diagnostics
from .typecheck import TypeChecker
from .unitarity_check import check_unitarity

_HARD_CODES = {
    "FORBIDDEN_KEYWORD",
    "RETIRED_KEYWORD",
    "RETIRED_OPERATOR_INDEX_SYNTAX",
    "EARLY_COLLAPSE_ERROR",
    "NESTED_WHEN_ERROR",
    "INTERFER_INDEPENDENT_STATE_ERROR",
    "EXPECT_CLASSICAL_ONLY_ERROR",
    "TYPE_MISMATCH",
    "COIN_IN_EVOLVE_ERROR",
    "NON_UNITARY_TRANSFORM_ERROR",
    "PREDICATE_PROJECTOR_ERROR",
    "CANNOT_MEASURE_CLASSICAL_VALUE_ERROR",
    "PARSE_ERROR",
    "LEX_ERROR",
    "TYPE_NOT_STATE",
    "DIMENSION_MISMATCH_ERROR",
    "TOPLEVEL_EXECUTION_ERROR",
    "PRODUCT_BIND_ERROR",
    "PRODUCT_ARITY_ERROR",
    "PRODUCT_TYPE_MISMATCH",
            "MODULE_NOT_FOUND_ERROR",
            "MODULE_CYCLE_ERROR",
            "IMMUTABLE_ASSIGNMENT_ERROR",
            "ENUM_TYPE_MISMATCH",
            "ACCESS_CONTROL_VIOLATION_ERROR",
            "PRIVATE_ACCESS_VIOLATION_ERROR",
    "MODULE_PRIVATE_ACCESS_ERROR",
    "MAIN_RETURN_ERROR",
    "RETURN_NOT_TERMINAL",
    "MISSING_RETURN_STATEMENT",
    "INIT_RETURN_ERROR",
    "LEXICAL_SCOPE_ERROR",
            "PACKAGE_NOT_EXPORTED_ERROR",
    "MAIN_RETURN_TYPE_ERROR",
    "MISSING_RETURN_TYPE",
            "MAIN_RESULT_ERROR",
            "RETURN_TYPE_MISMATCH",
            "MISSING_RETURN_VALUE",
            "MEASURE_IN_FUNCTION_ERROR",
    "SNAPSHOT_IN_FUNCTION_ERROR",
    "HOST_TYPE_IN_KERNEL_ERROR",
    "FOR_EACH_DYNAMIC_BOUND_ERROR",
    "FOR_EACH_MEASURE_ERROR",
    "QPU_CLASSICAL_CONTROL_ERROR",
    "PARAMETER_CONTROL_ERROR",
    "PARAMETER_TYPE_ERROR",
    "STATIC_REGISTER_TYPE_ERROR",
    "STATIC_HILBERT_SURFACE_ERROR",
    "STATIC_HILBERT_RESOURCE_ERROR",
    "QFT_REGISTER_TYPE_ERROR",
    "QFT_RESOURCE_ERROR",
    "EVOLVE_UNTIL_BOUND_ERROR",
    "EVOLVE_UNTIL_EFFECT_ERROR",
    "EVOLVE_UNTIL_MAX_STEPS_ERROR",
    "PIPE_EFFECT_ERROR",
    "PIPE_CALLABLE_ERROR",
    "PIPE_TYPE_ERROR",
    "EFFECT_DECLARATION_ERROR",
    "EFFECT_VIOLATION_ERROR",
    "EFFECT_MEASURE_RETURN_ERROR",
    "IMPL_COHERENCE_ERROR",
    "IMPL_VISIBILITY_ERROR",
    "SYSTEM_EXPRESSION_ERROR",
    "SUZUKI_ORDER_ERROR",
    "SUZUKI_POLICY_ERROR",
    "DYNAMIC_CAPABILITY_REQUIRED_ERROR",
    "DYNAMIC_UNSUPPORTED_FEATURE_ERROR",
    "SEMANTIC_CARRIER_MISMATCH_ERROR",
    "PHASE_TYPE_VISIBILITY_ERROR",
    "SEMANTIC_CARRIER_OPERATION_ERROR",
    "BINDER_RESOURCE_ERROR",
    "MATHEMATICAL_BINDER_EFFECT_ERROR",
    "BINDER_DOMAIN_ERROR",
    "BINDER_INDEX_OUT_OF_BOUNDS",
    "BINDER_LOWERING_UNSUPPORTED",
    IDENTITY_ACTING_SPACE_UNDETERMINED,
    "OPERATOR_ALGEBRA_TYPE_ERROR",
    "OPERATOR_DOMAIN_ERROR",
    "SECOND_QUANTIZATION_TYPE_ERROR",
    "FERMION_MAPPING_REQUIRED_ERROR",
    "SECOND_QUANTIZATION_MAPPING_UNSUPPORTED",
    "PHASE_SCOPE_DEPENDENCY_ERROR",
    "PHASE_SCOPE_CYCLE_ERROR",
    "PHASE_SCOPE_DIRECTION_ERROR",
    "PHASE_SCOPE_REFERENCE_ERROR",
    "WORKFLOW_SURFACE_ERROR",
    "DISCRETIZATION_REQUIRED_ERROR",
    "DISCRETIZATION_CONTRACT_ERROR",
    "DISCRETIZATION_BRIDGE_ERROR",
    "MIXED_STATE_TYPE_ERROR",
    "MALFORMED_DENSITY_STATE",
    "INCOMPLETE_KRAUS_CHANNEL",
    "INVALID_LINDBLAD_JUMP_SET",
    "LINDBLAD_JUMP_DIMENSION_ERROR",
    "SYMBOLIC_JUMP_LOWERING_REQUIRED",
    "POVM_DOMAIN_MISMATCH",
    "INVALID_POVM_EFFECT",
    "INCOMPLETE_POVM",
    "MID_CIRCUIT_MEASUREMENT_REQUIRES_DYNAMIC_LANE",
    # Backend capability diagnostics are reported for a later emission
    # boundary; they do not invalidate an otherwise valid Kernel program.
}


@dataclass
class CompileResult:
    unit: CompilationUnit | None
    diagnostics: list[dict[str, Any]]
    checker: TypeChecker | None = None
    symbolic_ir: dict[str, Any] | None = None
    scope_contracts: Mapping[str, ScientificScopeContract] | None = None
    workflow_contracts: Mapping[str, WorkflowContract] | None = None
    discretization_contracts: Mapping[str, DiscretizationContract] | None = None
    discretization_bridges: Mapping[str, DiscretizationBridge] | None = None
    mixed_state_contracts: Mapping[str, MixedStateContract] | None = None
    povm_contracts: Mapping[str, POVMContract] | None = None
    qpu_ir: Mapping[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return not any(d.get("code") in _HARD_CODES for d in self.diagnostics)


def _analyze_unit(unit: CompilationUnit, diags: list[dict[str, Any]]) -> CompileResult:
    diags.extend(check_early_collapse(unit))
    diags.extend(check_nested_when(unit))
    diags.extend(check_physical_axioms(unit))
    diags.extend(check_unitarity(unit))

    checker = TypeChecker()
    diags.extend(checker.check_unit(unit))
    scope_contracts, scope_diags = resolve_scientific_scopes(
        declaration
        for declaration in unit.decls
        if isinstance(declaration, ScientificScopeDecl)
    )
    diags.extend(scope_diags)
    workflow_contracts, workflow_diags = resolve_workflow_contracts(
        tuple(
            declaration
            for declaration in unit.decls
            if isinstance(declaration, ScientificScopeDecl)
        )
    )
    diags.extend(workflow_diags)
    discretization_contracts, discretization_diags = resolve_discretization_contracts(
        tuple(
            declaration
            for declaration in unit.decls
            if isinstance(declaration, DiscretizationDecl)
        )
    )
    diags.extend(discretization_diags)
    discretization_bridges, bridge_diags = resolve_discretization_bridges(
        tuple(
            declaration
            for declaration in unit.decls
            if isinstance(declaration, DiscretizationBridgeDecl)
        ),
        discretization_contracts,
        tuple(
            declaration
            for declaration in unit.decls
            if isinstance(declaration, ScientificScopeDecl)
        ),
    )
    diags.extend(bridge_diags)
    mixed_state_contracts, mixed_state_diags = resolve_mixed_state_contracts(unit)
    diags.extend(mixed_state_diags)
    povm_contracts, povm_diags = resolve_measurement_contracts(unit)
    diags.extend(povm_diags)

    symbolic_ir = build_symbolic_ir(unit)
    diags.extend(qpu_ir_diagnostics(unit))
    qpu_ir = build_qpu_ir(unit, symbolic_ir)
    return CompileResult(
        unit=unit,
        diagnostics=diags,
        checker=checker,
        symbolic_ir=symbolic_ir,
        scope_contracts=MappingProxyType(scope_contracts),
        workflow_contracts=MappingProxyType(workflow_contracts),
        discretization_contracts=MappingProxyType(discretization_contracts),
        discretization_bridges=MappingProxyType(discretization_bridges),
        mixed_state_contracts=MappingProxyType(mixed_state_contracts),
        povm_contracts=MappingProxyType(povm_contracts),
        qpu_ir=qpu_ir,
    )


def compile_source(source: str) -> CompileResult:
    lexer = Lexer(source)
    tokens, lex_diags = lexer.tokenize()
    diags: list[dict[str, Any]] = list(lex_diags)

    unit: CompilationUnit | None = None
    try:
        parser = Parser(tokens)
        unit = parser.parse()
        diags.extend(parser.diagnostics)
    except ParseError as e:
        diags.append(
            {
                "code": "PARSE_ERROR",
                "line": e.line,
                "col": e.col,
                "message": e.message,
            }
        )
        return CompileResult(unit=None, diagnostics=diags)

    return _analyze_unit(unit, diags)


def compile_path(entry: str | Path) -> CompileResult:
    """Compile an entry `.qpex` file with ADR 0054 user-module import linking."""
    path = Path(entry)
    graph = load_module_graph(path)
    diags: list[dict[str, Any]] = list(graph.diagnostics)
    if any(d.get("code") in _HARD_CODES for d in diags):
        return CompileResult(unit=None, diagnostics=diags)

    unit = merge_modules(path.resolve(), graph)
    diags = list(graph.diagnostics)
    if unit is None:
        diags.append(
            {
                "code": "MODULE_NOT_FOUND_ERROR",
                "line": 1,
                "col": 1,
                "message": f"failed to merge modules for {path}",
            }
        )
        return CompileResult(unit=None, diagnostics=diags)

    if any(d.get("code") in _HARD_CODES for d in diags):
        return CompileResult(unit=unit, diagnostics=diags, checker=None)

    return _analyze_unit(unit, diags)


def analyze_source(source: str) -> list[dict[str, Any]]:
    """Drop-in for spec-verification compile_gate (same diagnostic dict shape)."""
    return compile_source(source).diagnostics
