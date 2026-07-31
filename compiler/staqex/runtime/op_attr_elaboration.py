"""Elaborate OpAttr field projections into OpLit (ADR 0114 / LISS-0121).

Keeps Operator DSL ``struct.field * Pauli`` equivalent to a named classical
coefficient after struct construction, without treating the field as a linear
quantum resource.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..ast_nodes import (
    OpAttr,
    OpBin,
    OpBinder,
    OpCall,
    OpExpr,
    OpIndexed,
    OpLit,
    OpPow,
    OpVar,
)


class OpAttrElaborationError(ValueError):
    """Struct field could not be elaborated as a numeric Operator coefficient."""


def materialize_op_attrs(op: OpExpr, objects: Mapping[str, Any]) -> OpExpr:
    """Rewrite ``OpAttr`` nodes to ``OpLit`` using runtime struct field values."""
    if isinstance(op, OpAttr):
        return OpLit(value=float(_op_attr_float(op, objects)), span=op.span)
    if isinstance(op, OpBin):
        return OpBin(
            op=op.op,
            lhs=materialize_op_attrs(op.lhs, objects),
            rhs=materialize_op_attrs(op.rhs, objects),
            span=op.span,
        )
    if isinstance(op, OpPow):
        return OpPow(
            base=materialize_op_attrs(op.base, objects),
            exp=op.exp,
            span=op.span,
        )
    if isinstance(op, OpIndexed):
        return OpIndexed(
            base=materialize_op_attrs(op.base, objects),
            index=materialize_op_attrs(op.index, objects),
            span=op.span,
        )
    if isinstance(op, OpBinder):
        return OpBinder(
            kind=op.kind,
            variable=op.variable,
            domain=op.domain,
            body=materialize_op_attrs(op.body, objects),
            span=op.span,
            guard=(
                None
                if op.guard is None
                else materialize_op_attrs(op.guard, objects)
            ),
            origin=op.origin,
        )
    if isinstance(op, OpCall):
        return OpCall(
            name=op.name,
            args=[materialize_op_attrs(a, objects) for a in op.args],
            span=op.span,
        )
    return op


def _op_attr_float(op: OpAttr, objects: Mapping[str, Any]) -> float:
    if not isinstance(op.obj, OpVar):
        raise OpAttrElaborationError(
            "Operator field projection requires a struct binding "
            f"(got `{type(op.obj).__name__}`)"
        )
    obj = objects.get(op.obj.name)
    fields = getattr(obj, "fields", None)
    if not isinstance(fields, dict):
        raise OpAttrElaborationError(
            f"unbound struct for Operator coefficient `{op.obj.name}.{op.name}`"
        )
    if op.name not in fields:
        raise OpAttrElaborationError(
            f"unknown struct field `{op.name}` on `{op.obj.name}`"
        )
    raw = fields[op.name]
    try:
        return float(raw)
    except (TypeError, ValueError) as exc:
        raise OpAttrElaborationError(
            f"struct field `{op.obj.name}.{op.name}` is not a numeric "
            "elaboration coefficient"
        ) from exc
