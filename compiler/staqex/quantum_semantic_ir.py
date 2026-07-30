"""Quantum Semantic IR identity, root, acting-space, and Joint-value contracts.

Slice A owns immutable semantic identities, provenance, schema versioning, and
deterministic root diagnostics. Slice B adds finite acting spaces, the
pure/density whole-Joint-state carriers, and the generation-use laws.

Region behavior, control and measurement lanes, finite-space lowering, pipeline
wiring, and target adapters belong to later LISS-0082 slices or other Issues.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = 1
Diagnostic = dict[str, Any]

__all__ = [
    "ActingFactor",
    "ActingSpace",
    "ChannelRegion",
    "DensityJointStateValue",
    "IsometryRegion",
    "Diagnostic",
    "JointValueUse",
    "PureJointStateValue",
    "QuantumSemanticModule",
    "RegionValidity",
    "SCHEMA_VERSION",
    "SemanticId",
    "SemanticOrigin",
    "UnitaryRegion",
    "verify_quantum_semantic_ir",
]


@dataclass(frozen=True, slots=True)
class SemanticId:
    """Stable identity for a semantic object within a named scope."""

    kind: str
    scope: str
    ordinal: int

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("semantic identity kind must not be empty")
        if not self.scope:
            raise ValueError("semantic identity scope must not be empty")
        if self.ordinal < 0:
            raise ValueError("semantic identity ordinal must not be negative")


@dataclass(frozen=True, slots=True)
class SemanticOrigin:
    """Closed source and transformation ancestry for a semantic identity."""

    source_id: str
    line: int
    col: int
    upstream_ids: tuple[str, ...] = field(default_factory=tuple)
    transform_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "upstream_ids", tuple(self.upstream_ids))


@dataclass(frozen=True, slots=True)
class ActingFactor:
    """One ordered tensor factor of a finite acting space."""

    factor_id: SemanticId
    dimension: int
    label: str = ""


@dataclass(frozen=True, slots=True)
class ActingSpace:
    """Ordered finite carrier a Joint state value acts on."""

    space_id: SemanticId
    factors: tuple[ActingFactor, ...]
    total_dimension: int
    origin: SemanticOrigin

    def __post_init__(self) -> None:
        object.__setattr__(self, "factors", tuple(self.factors))


@dataclass(frozen=True, slots=True)
class _JointStateValue:
    """Shared shape of one immutable whole-Joint-store generation.

    Resources name coordinates inside this single value. They never assert
    separability, and no amplitude or density matrix is stored. Purity is
    carried by the concrete subclass, never by a mutable flag.
    """

    value_id: SemanticId
    space_id: SemanticId
    resources: tuple[SemanticId, ...]
    producer_id: SemanticId | None
    origin: SemanticOrigin

    def __post_init__(self) -> None:
        object.__setattr__(self, "resources", tuple(self.resources))


@dataclass(frozen=True, slots=True)
class PureJointStateValue(_JointStateValue):
    """One immutable pure whole-Joint-store generation."""

    @property
    def is_pure(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class DensityJointStateValue(_JointStateValue):
    """One immutable mixed whole-Joint-store generation."""

    @property
    def is_pure(self) -> bool:
        return False


JointStateValue = PureJointStateValue | DensityJointStateValue


@dataclass(frozen=True, slots=True)
class RegionValidity:
    """One declared, evidenced, or deferred region validity claim."""

    kind: str
    reference: str | None = None

    def __post_init__(self) -> None:
        if self.kind not in {"Declared", "Verified", "Required"}:
            raise ValueError(f"unsupported region validity kind: {self.kind}")
        if self.kind == "Declared" and self.reference is not None:
            raise ValueError("Declared validity must not carry a reference")
        if self.kind != "Declared" and not self.reference:
            raise ValueError(f"{self.kind} validity requires a reference")


@dataclass(frozen=True, slots=True)
class _TransformationRegion:
    """Shared provider-neutral signature of one transformation region."""

    region_id: SemanticId
    input_value_id: SemanticId
    output_value_id: SemanticId
    input_space_id: SemanticId
    output_space_id: SemanticId
    validity: RegionValidity
    origin: SemanticOrigin


@dataclass(frozen=True, slots=True)
class UnitaryRegion(_TransformationRegion):
    """Pure, reversible transformation over one unchanged acting space."""


@dataclass(frozen=True, slots=True)
class IsometryRegion(_TransformationRegion):
    """Pure transformation whose finite output space may be larger."""


@dataclass(frozen=True, slots=True)
class ChannelRegion(_TransformationRegion):
    """Physicality-obligation boundary producing a density carrier."""


@dataclass(frozen=True, slots=True)
class JointValueUse:
    """One consuming path of a whole-Joint-state generation.

    `factor_id` is populated only by an invalid attempt to consume a factor as
    an independent state value; the verifier reports it.
    """

    value_id: SemanticId
    consumer_id: SemanticId
    factor_id: SemanticId | None = None


@dataclass(frozen=True, slots=True)
class QuantumSemanticModule:
    """Schema-versioned immutable root for later Semantic IR slices."""

    schema_version: int
    roots: tuple[SemanticId, ...] = field(default_factory=tuple)
    region_roots: tuple[SemanticId, ...] = field(default_factory=tuple)
    origins: tuple[SemanticOrigin, ...] = field(default_factory=tuple)
    acting_spaces: tuple[ActingSpace, ...] = field(default_factory=tuple)
    values: tuple[JointStateValue, ...] = field(default_factory=tuple)
    value_uses: tuple[JointValueUse, ...] = field(default_factory=tuple)
    regions: tuple[UnitaryRegion | IsometryRegion | ChannelRegion, ...] = field(
        default_factory=tuple
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "roots", tuple(self.roots))
        object.__setattr__(self, "region_roots", tuple(self.region_roots))
        object.__setattr__(self, "origins", tuple(self.origins))
        object.__setattr__(self, "acting_spaces", tuple(self.acting_spaces))
        object.__setattr__(self, "values", tuple(self.values))
        object.__setattr__(self, "value_uses", tuple(self.value_uses))
        object.__setattr__(self, "regions", tuple(self.regions))


def _diagnostic(code: str, message: str, **details: Any) -> Diagnostic:
    result: Diagnostic = {"code": code, "message": message}
    result.update(details)
    return result


def _defined_identities(module: QuantumSemanticModule) -> tuple[SemanticId, ...]:
    """Return every identity the module *defines*, in canonical order.

    Only definition sites count. An identity that merely appears as a reference
    -- `value.space_id`, `value.resources`, `producer_id`, a `JointValueUse`
    target, or `SemanticOrigin.upstream_ids` -- is resolved elsewhere and is
    never a redefinition.
    """

    defined: list[SemanticId] = list(module.roots)
    defined.extend(module.region_roots)
    for space in module.acting_spaces:
        defined.append(space.space_id)
        defined.extend(factor.factor_id for factor in space.factors)
    defined.extend(value.value_id for value in module.values)
    defined.extend(region.region_id for region in module.regions)
    return tuple(defined)


def _origin_is_incomplete(origin: SemanticOrigin) -> bool:
    return (
        not origin.source_id
        or origin.line < 1
        or origin.col < 1
        or not origin.transform_id
    )


def _report_incomplete_origin(
    origin: SemanticOrigin,
    diagnostics: list[Diagnostic],
    message: str,
    **details: Any,
) -> None:
    """Apply the one ancestry predicate to one definition site."""

    if _origin_is_incomplete(origin):
        diagnostics.append(
            _diagnostic("QSEM_PROVENANCE_INCOMPLETE", message, **details, origin=origin)
        )


def _verify_root(
    module: QuantumSemanticModule, diagnostics: list[Diagnostic]
) -> None:
    """Report unsupported schema, duplicate identity, and missing ancestry."""

    if module.schema_version != SCHEMA_VERSION:
        diagnostics.append(
            _diagnostic(
                "QSEM_SCHEMA_VERSION_UNSUPPORTED",
                "unsupported Quantum Semantic IR schema version",
                schema_version=module.schema_version,
            )
        )

    identities = _defined_identities(module)
    seen: set[SemanticId] = set()
    for identity in identities:
        if identity in seen:
            diagnostics.append(
                _diagnostic(
                    "QSEM_IDENTITY_CONFLICT",
                    "semantic identity is defined more than once",
                    identity=identity,
                )
            )
        seen.add(identity)

    if identities and not module.origins:
        diagnostics.append(
            _diagnostic(
                "QSEM_PROVENANCE_INCOMPLETE",
                "semantic roots require at least one source origin",
            )
        )

    for origin in module.origins:
        _report_incomplete_origin(
            origin,
            diagnostics,
            "source origin is missing required ancestry fields",
        )


def _verify_acting_spaces(
    module: QuantumSemanticModule, diagnostics: list[Diagnostic]
) -> None:
    """Report invalid acting-space shape and incomplete acting-space ancestry."""

    for space in module.acting_spaces:
        _report_incomplete_origin(
            space.origin,
            diagnostics,
            "acting space origin is missing required ancestry fields",
            acting_space=space.space_id,
        )

        if not space.factors:
            diagnostics.append(
                _diagnostic(
                    "QSEM_ACTING_SPACE_INVALID",
                    "acting space has no tensor factors",
                    acting_space=space.space_id,
                )
            )
            continue

        product = 1
        has_invalid_factor = False
        for factor in space.factors:
            if factor.dimension < 1:
                diagnostics.append(
                    _diagnostic(
                        "QSEM_ACTING_SPACE_INVALID",
                        "acting space factor dimension must be positive",
                        acting_space=space.space_id,
                        factor=factor.factor_id,
                        dimension=factor.dimension,
                    )
                )
                has_invalid_factor = True
            product *= factor.dimension

        if not has_invalid_factor and space.total_dimension != product:
            diagnostics.append(
                _diagnostic(
                    "QSEM_ACTING_SPACE_INVALID",
                    "acting space total dimension does not match its factors",
                    acting_space=space.space_id,
                    total_dimension=space.total_dimension,
                    factor_product=product,
                )
            )


def _verify_joint_values(
    module: QuantumSemanticModule, diagnostics: list[Diagnostic]
) -> None:
    """Report unknown carriers, resource drift, ancestry, and missing producers."""

    spaces = {space.space_id: space for space in module.acting_spaces}
    for value in module.values:
        _report_incomplete_origin(
            value.origin,
            diagnostics,
            "joint state value origin is missing required ancestry fields",
            value=value.value_id,
        )

        space = spaces.get(value.space_id)
        if space is None:
            diagnostics.append(
                _diagnostic(
                    "QSEM_ACTING_SPACE_INVALID",
                    "joint state value references an unknown acting space",
                    value=value.value_id,
                    acting_space=value.space_id,
                )
            )
        else:
            factor_ids = tuple(factor.factor_id for factor in space.factors)
            if value.resources != factor_ids:
                diagnostics.append(
                    _diagnostic(
                        "QSEM_ACTING_SPACE_INVALID",
                        "joint state value resources do not match the ordered "
                        "acting space factors",
                        value=value.value_id,
                        acting_space=value.space_id,
                        resources=value.resources,
                        factors=factor_ids,
                    )
                )

        if value.producer_id is None:
            diagnostics.append(
                _diagnostic(
                    "QSEM_VALUE_USE_INVALID",
                    "joint state generation has no producer",
                    value=value.value_id,
                )
            )


def _verify_value_uses(
    module: QuantumSemanticModule, diagnostics: list[Diagnostic]
) -> None:
    """Report unknown, fanned-out, or factor-level consumption of a generation."""

    known_values = {value.value_id for value in module.values}
    consumed: set[SemanticId] = set()
    for use in module.value_uses:
        if use.value_id not in known_values:
            diagnostics.append(
                _diagnostic(
                    "QSEM_VALUE_USE_INVALID",
                    "value use references an unknown joint state generation",
                    value=use.value_id,
                    consumer=use.consumer_id,
                )
            )
            continue

        if use.factor_id is not None:
            diagnostics.append(
                _diagnostic(
                    "QSEM_VALUE_USE_INVALID",
                    "a factor cannot be consumed as an independent state value",
                    value=use.value_id,
                    factor=use.factor_id,
                    consumer=use.consumer_id,
                )
            )
            continue

        if use.value_id in consumed:
            diagnostics.append(
                _diagnostic(
                    "QSEM_VALUE_USE_INVALID",
                    "joint state generation has more than one consuming path",
                    value=use.value_id,
                    consumer=use.consumer_id,
                )
            )
        consumed.add(use.value_id)


def _region_signature_diagnostic(
    region: _TransformationRegion, message: str, **details: Any
) -> Diagnostic:
    return _diagnostic(
        "QSEM_REGION_SIGNATURE_INVALID",
        message,
        region=region.region_id,
        **details,
    )


def _verify_region_references(
    region: _TransformationRegion,
    values: dict[SemanticId, JointStateValue],
    spaces: dict[SemanticId, ActingSpace],
    diagnostics: list[Diagnostic],
) -> tuple[
    JointStateValue | None,
    JointStateValue | None,
    ActingSpace | None,
    ActingSpace | None,
]:
    input_value = values.get(region.input_value_id)
    output_value = values.get(region.output_value_id)
    input_space = spaces.get(region.input_space_id)
    output_space = spaces.get(region.output_space_id)

    if input_value is None or output_value is None:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "transformation region references an unknown Joint value",
                input_value=region.input_value_id,
                output_value=region.output_value_id,
            )
        )
    if input_space is None or output_space is None:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "transformation region references an unknown acting space",
                input_space=region.input_space_id,
                output_space=region.output_space_id,
            )
        )

    if input_value is not None and input_value.space_id != region.input_space_id:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "input Joint value does not inhabit the declared input space",
                input_value=region.input_value_id,
                input_space=region.input_space_id,
            )
        )
    if output_value is not None and output_value.space_id != region.output_space_id:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "output Joint value does not inhabit the declared output space",
                output_value=region.output_value_id,
                output_space=region.output_space_id,
            )
        )

    return input_value, output_value, input_space, output_space


def _verify_unitary(
    region: UnitaryRegion,
    input_value: JointStateValue | None,
    output_value: JointStateValue | None,
    input_space: ActingSpace | None,
    output_space: ActingSpace | None,
    diagnostics: list[Diagnostic],
) -> None:
    valid_signature = (
        input_value is not None
        and output_value is not None
        and isinstance(input_value, PureJointStateValue)
        and isinstance(output_value, PureJointStateValue)
        and input_space is not None
        and output_space is not None
        and region.input_space_id == region.output_space_id
        and input_space.total_dimension == output_space.total_dimension
    )
    if not valid_signature:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "UnitaryRegion must preserve a pure carrier and acting space",
            )
        )


def _verify_isometry(
    region: IsometryRegion,
    input_value: JointStateValue | None,
    output_value: JointStateValue | None,
    input_space: ActingSpace | None,
    output_space: ActingSpace | None,
    diagnostics: list[Diagnostic],
) -> None:
    valid_signature = (
        input_value is not None
        and output_value is not None
        and isinstance(input_value, PureJointStateValue)
        and isinstance(output_value, PureJointStateValue)
        and input_space is not None
        and output_space is not None
        and input_space.total_dimension <= output_space.total_dimension
    )
    if not valid_signature:
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "IsometryRegion requires pure carriers and non-decreasing finite dimension",
            )
        )

    if (
        input_space is not None
        and output_space is not None
        and input_space.total_dimension < output_space.total_dimension
        and region.validity.kind != "Required"
    ):
        diagnostics.append(
            _diagnostic(
                "QSEM_REGION_VALIDITY_INVALID",
                "IsometryRegion dimension increase requires an explicit obligation",
                region=region.region_id,
            )
        )


def _verify_channel(
    region: ChannelRegion,
    input_value: JointStateValue | None,
    output_value: JointStateValue | None,
    diagnostics: list[Diagnostic],
) -> None:
    if input_value is None or output_value is None or not isinstance(
        output_value, DensityJointStateValue
    ):
        diagnostics.append(
            _region_signature_diagnostic(
                region,
                "ChannelRegion must produce a density carrier",
            )
        )


def _verify_regions(
    module: QuantumSemanticModule, diagnostics: list[Diagnostic]
) -> None:
    values: dict[SemanticId, JointStateValue] = {
        value.value_id: value for value in module.values
    }
    spaces = {space.space_id: space for space in module.acting_spaces}
    for region in module.regions:
        _report_incomplete_origin(
            region.origin,
            diagnostics,
            "transformation region origin is missing required ancestry fields",
            region=region.region_id,
        )
        input_value, output_value, input_space, output_space = _verify_region_references(
            region, values, spaces, diagnostics
        )
        if isinstance(region, UnitaryRegion):
            _verify_unitary(
                region, input_value, output_value, input_space, output_space, diagnostics
            )
        elif isinstance(region, IsometryRegion):
            _verify_isometry(
                region, input_value, output_value, input_space, output_space, diagnostics
            )
        elif isinstance(region, ChannelRegion):
            _verify_channel(region, input_value, output_value, diagnostics)


def verify_quantum_semantic_ir(module: QuantumSemanticModule) -> list[Diagnostic]:
    """Return deterministic non-mutating diagnostics for the semantic module.

    Diagnostics are appended in a fixed pass order — root, acting spaces,
    Joint state values, value uses — so the report is reproducible. The module
    is never repaired.
    """

    diagnostics: list[Diagnostic] = []
    _verify_root(module, diagnostics)
    _verify_acting_spaces(module, diagnostics)
    _verify_joint_values(module, diagnostics)
    _verify_value_uses(module, diagnostics)
    _verify_regions(module, diagnostics)
    return diagnostics
