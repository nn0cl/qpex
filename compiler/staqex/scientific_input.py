"""Typed Host-side scientific inputs for LISS-0045.

These value objects stop at the Host boundary. They do not parse files, call
providers, or become values in the Staqex Kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from types import MappingProxyType
from typing import Mapping


_UNITS_BY_DIMENSION = {
    "Angle": frozenset({"rad", "deg"}),
    "Length": frozenset({"m", "cm", "mm", "angstrom", "Å"}),
    "Time": frozenset({"s", "ms", "us", "ns"}),
    "Energy": frozenset({"J", "eV", "Ha"}),
}


class ScientificInputValidationError(ValueError):
    """Hard validation failure for a scientific Host input contract."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class InputProvenance:
    """Identity needed to reproduce a scientific input."""

    source_formula: str
    input_id: str

    def __post_init__(self) -> None:
        if not self.source_formula.strip():
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_PROVENANCE_ERROR",
                "source_formula must not be empty",
            )
        if not self.input_id.strip():
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_PROVENANCE_ERROR",
                "input_id must not be empty",
            )


@dataclass(frozen=True)
class ParameterBinding:
    """One finite scalar value bound to a declared parameter."""

    name: str
    value: Real
    unit: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_PARAMETER_ERROR",
                "parameter name must not be empty",
            )
        if isinstance(self.value, bool) or not isinstance(self.value, Real):
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_VALUE_ERROR",
                f"parameter {self.name!r} requires a real scalar value",
            )
        if not math.isfinite(float(self.value)):
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_VALUE_ERROR",
                f"parameter {self.name!r} requires a finite scalar value",
            )
        if not self.unit.strip():
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_UNIT_ERROR",
                f"parameter {self.name!r} requires unit metadata",
            )


@dataclass(frozen=True)
class ScientificInput:
    """Validated scalar bindings and their source identity."""

    declared_parameters: Mapping[str, str | None] | tuple[str, ...]
    bindings: tuple[ParameterBinding, ...]
    provenance: InputProvenance | Mapping[str, str]

    def __post_init__(self) -> None:
        declared = _declared_parameter_map(self.declared_parameters)
        bindings = tuple(self.bindings)
        _validate_bindings(declared, bindings)
        object.__setattr__(self, "declared_parameters", MappingProxyType(declared))
        object.__setattr__(self, "bindings", bindings)
        object.__setattr__(self, "provenance", _coerce_provenance(self.provenance))


@dataclass(frozen=True)
class ParameterSweep:
    """Finite immutable collection of complete or partial binding sets."""

    bindings: tuple[tuple[ParameterBinding, ...], ...]
    provenance: InputProvenance

    def __post_init__(self) -> None:
        rows = tuple(tuple(row) for row in self.bindings)
        if not rows:
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_EMPTY_SWEEP",
                "parameter sweep must contain at least one binding set",
            )
        object.__setattr__(self, "bindings", rows)
        object.__setattr__(self, "provenance", _coerce_provenance(self.provenance))


def _validate_bindings(
    declared: Mapping[str, str | None],
    bindings: tuple[ParameterBinding, ...],
) -> None:
    seen: set[str] = set()
    for binding in bindings:
        _validate_binding_name(declared, seen, binding)
        expected_dimension = declared[binding.name]
        if expected_dimension and not _unit_matches_dimension(
            binding.unit, expected_dimension
        ):
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_DIMENSION_ERROR",
                f"unit {binding.unit!r} does not match {expected_dimension}",
            )


def _validate_binding_name(
    declared: Mapping[str, str | None],
    seen: set[str],
    binding: ParameterBinding,
) -> None:
    if binding.name in seen:
        raise ScientificInputValidationError(
            "SCIENTIFIC_INPUT_DUPLICATE_PARAMETER",
            f"parameter {binding.name!r} is bound more than once",
        )
    seen.add(binding.name)
    if binding.name not in declared:
        raise ScientificInputValidationError(
            "SCIENTIFIC_INPUT_UNKNOWN_PARAMETER",
            f"parameter {binding.name!r} is not declared",
        )


def _coerce_provenance(
    provenance: InputProvenance | Mapping[str, str],
) -> InputProvenance:
    if isinstance(provenance, InputProvenance):
        return provenance
    if isinstance(provenance, Mapping):
        try:
            return InputProvenance(
                source_formula=str(provenance["source_formula"]),
                input_id=str(provenance["input_id"]),
            )
        except KeyError as error:
            raise ScientificInputValidationError(
                "SCIENTIFIC_INPUT_PROVENANCE_ERROR",
                "provenance requires source_formula and input_id",
            ) from error
    raise ScientificInputValidationError(
        "SCIENTIFIC_INPUT_PROVENANCE_ERROR",
        "provenance must be an InputProvenance value",
    )


def _declared_parameter_map(
    declared: tuple[str, ...] | Mapping[str, str],
) -> dict[str, str | None]:
    if isinstance(declared, Mapping):
        return {str(name): str(dimension) for name, dimension in declared.items()}
    return {str(name): None for name in declared}


def _unit_matches_dimension(unit: str, dimension: str) -> bool:
    allowed_units = _UNITS_BY_DIMENSION.get(dimension)
    return allowed_units is None or unit in allowed_units
