"""Provider-neutral verified pass orchestration for LISS-0087."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


Diagnostic = dict[str, Any]
PassCallable = Callable[[Any], "PassOutput"]


@dataclass(frozen=True)
class PassProvenance:
    source_id: str
    upstream_ids: tuple[str, ...]
    transform_id: str


@dataclass(frozen=True)
class PassConfiguration:
    pass_id: str
    version: str
    parameters: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class PassInput:
    value: Any
    verified: bool
    provenance: PassProvenance
    exactness: str
    obligations: tuple[str, ...]


@dataclass(frozen=True)
class PassOutput:
    value: Any
    provenance: PassProvenance
    exactness: str
    obligations: tuple[str, ...]


@dataclass(frozen=True)
class PassDefinition:
    pass_id: str
    configuration: PassConfiguration
    execute: PassCallable
    precondition: bool
    postcondition: bool


@dataclass(frozen=True)
class PassPipeline:
    passes: tuple[PassDefinition, ...]


@dataclass(frozen=True)
class PassResult:
    status: str
    output: PassOutput | None
    diagnostics: tuple[Diagnostic, ...]
    pass_id: str | None
    configuration_id: str | None


def _diagnostic(code: str, message: str, **details: Any) -> Diagnostic:
    return {"code": code, "message": message, **details}


def _provenance_complete(provenance: PassProvenance) -> bool:
    return bool(
        provenance.source_id
        and provenance.upstream_ids
        and provenance.transform_id
    )


def _failed(
    code: str,
    message: str,
    *,
    pass_definition: PassDefinition | None = None,
) -> PassResult:
    pass_id = pass_definition.pass_id if pass_definition is not None else None
    configuration_id = (
        pass_definition.configuration.pass_id
        if pass_definition is not None
        else None
    )
    details = {"pass_id": pass_id} if pass_id is not None else {}
    return PassResult(
        status="failed",
        output=None,
        diagnostics=(_diagnostic(code, message, **details),),
        pass_id=pass_id,
        configuration_id=configuration_id,
    )


def _policy_is_allowed(pass_definition: PassDefinition) -> bool:
    return not (
        "provider." in pass_definition.pass_id
        or "runtime" in pass_definition.pass_id
    )


def verify_pass_result(result: PassResult) -> list[Diagnostic]:
    """Return deterministic diagnostics for a pass result boundary."""

    diagnostics: list[Diagnostic] = list(result.diagnostics)
    if result.status == "verified":
        if result.output is None:
            diagnostics.append(
                _diagnostic(
                    "PASS_OUTPUT_MISSING",
                    "verified result requires output",
                )
            )
        elif not _provenance_complete(result.output.provenance):
            diagnostics.append(
                _diagnostic(
                    "PASS_PROVENANCE_INCOMPLETE",
                    "verified output provenance is incomplete",
                )
            )
    diagnostics.sort(key=lambda item: item["code"])
    return diagnostics


def _verified_result(output: PassOutput, last: PassDefinition) -> PassResult:
    result = PassResult(
        status="verified",
        output=output,
        diagnostics=(),
        pass_id=last.pass_id,
        configuration_id=last.configuration.pass_id,
    )
    diagnostics = verify_pass_result(result)
    if diagnostics:
        return PassResult(
            status="failed",
            output=None,
            diagnostics=tuple(diagnostics),
            pass_id=last.pass_id,
            configuration_id=last.configuration.pass_id,
        )
    return result


def run_verified_pipeline(
    input_value: PassInput,
    pipeline: PassPipeline,
) -> PassResult:
    """Run passes in order and hard-stop on the first invalid boundary."""

    if not input_value.verified:
        return _failed(
            "PASS_INPUT_UNVERIFIED",
            "an unverified input cannot enter a pass",
        )

    current: Any = input_value
    for pass_definition in pipeline.passes:
        if not _policy_is_allowed(pass_definition):
            return _failed(
                "PASS_POLICY_INVALID",
                "provider and runtime-adaptive pass policy is forbidden",
                pass_definition=pass_definition,
            )
        if not pass_definition.precondition:
            return _failed(
                "PASS_PRECONDITION_FAILED",
                "pass precondition failed",
                pass_definition=pass_definition,
            )

        output = pass_definition.execute(current)
        if not pass_definition.postcondition:
            return _failed(
                "PASS_POSTCONDITION_FAILED",
                "pass postcondition failed",
                pass_definition=pass_definition,
            )
        if not _provenance_complete(output.provenance):
            return _failed(
                "PASS_PROVENANCE_INCOMPLETE",
                "pass output provenance is incomplete",
                pass_definition=pass_definition,
            )
        current = output

    if not pipeline.passes:
        return PassResult(
            status="verified",
            output=PassOutput(
                value=input_value.value,
                provenance=input_value.provenance,
                exactness=input_value.exactness,
                obligations=input_value.obligations,
            ),
            diagnostics=(),
            pass_id=None,
            configuration_id=None,
        )

    return _verified_result(current, pipeline.passes[-1])
