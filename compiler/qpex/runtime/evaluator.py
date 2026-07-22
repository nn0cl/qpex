"""Kernel evaluator — AST → Joint transformers + terminal measure."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable, TextIO

from ..ast_nodes import (
    Attr,
    BinOp,
    Call,
    Coin,
    CompilationUnit,
    Dirac,
    Expr,
    Inspect,
    Lambda,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    Measure,
    Pipe,
    Snapshot,
    StateBind,
    Vacuum,
    Var,
    WhenExpr,
)
from ..stdlib import math_ops
from ..stdlib.io_ops import format_marginal_table, format_snapshot_csv, write_sink
from .joint import EPS, Joint, sample_from_marginal

RELATIONAL = {"==", "!=", "<", "<=", ">", ">="}


@dataclass
class MeasureResult:
    value: Any | None
    vacuum: bool
    marginal: dict[Any, float]
    rng_calls: int
    sink: str | None = None
    output: str = ""


@dataclass
class EvalResult:
    joint: Joint
    measure: MeasureResult | None = None
    rng_calls_before_measure: int = 0
    logs: list[str] = field(default_factory=list)


class KernelError(Exception):
    pass


class Evaluator:
    """Discrete PMF Kernel (stance a). Pure stmts are Joint → Joint."""

    def __init__(
        self,
        *,
        rng: random.Random | None = None,
        seed: int | None = None,
        inspect_sink: TextIO | None = None,
    ) -> None:
        if rng is not None:
            self.rng = rng
        elif seed is not None:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()
        self.rng_calls = 0
        self._rng_calls_before_measure = 0
        self.inspect_sink = inspect_sink

    def run_unit(self, unit: CompilationUnit, *, stdout: TextIO | None = None) -> EvalResult:
        joint = Joint.unit()
        if unit.main is None:
            return EvalResult(joint=Joint.empty())

        measure_result: MeasureResult | None = None
        logs: list[str] = []
        inspect_out = self.inspect_sink if self.inspect_sink is not None else stdout

        for stmt in unit.main.body.stmts:
            if isinstance(stmt, StateBind):
                joint = self._bind(joint, stmt.name, stmt.expr, logs=logs, inspect_out=inspect_out)
            elif isinstance(stmt, Snapshot):
                marg = self._expr_marginal(joint, stmt.expr)
                text = format_snapshot_csv(marg)
                write_sink(stmt.sink, text, stdout=stdout)
                logs.append(f"snapshot:{stmt.sink}:{marg}")
            elif isinstance(stmt, Measure):
                self._rng_calls_before_measure = self.rng_calls
                measure_result = self._measure(joint, stmt.expr, sink=stmt.sink, stdout=stdout)
                break
            else:
                raise KernelError(f"unsupported stmt {type(stmt)}")

        return EvalResult(
            joint=joint,
            measure=measure_result,
            rng_calls_before_measure=self._rng_calls_before_measure,
            logs=logs,
        )

    def _bind(
        self,
        joint: Joint,
        name: str,
        expr: Expr,
        *,
        logs: list[str] | None = None,
        inspect_out: TextIO | None = None,
    ) -> Joint:
        if isinstance(expr, Inspect):
            # identity bind of inner; side-effect host log
            marg = self._expr_marginal(joint, expr.expr)
            text = format_marginal_table(marg, label=expr.label)
            if inspect_out is not None:
                inspect_out.write(text)
            if logs is not None:
                logs.append(f"inspect:{expr.label or ''}:{marg}")
            return self._bind(joint, name, expr.expr, logs=logs, inspect_out=inspect_out)
        if isinstance(expr, Coin):
            return joint.bind_split(name, {0: 0.5, 1: 0.5})
        if isinstance(expr, Vacuum):
            return Joint.empty()
        if isinstance(expr, Dirac):
            if self._is_closed(expr.arg):
                return joint.bind_const(name, self._eval_value(expr.arg, {}))
            return joint.bind_pushforward(name, lambda a: self._eval_value(expr.arg, a))
        if isinstance(expr, (LitInt, LitFloat, LitBool, LitString)):
            return joint.bind_const(name, self._lit(expr))
        if isinstance(expr, Var):
            return joint.bind_pushforward(name, lambda a: a[expr.name])
        if isinstance(expr, BinOp):
            return joint.bind_pushforward(name, lambda a: self._eval_value(expr, a))
        if isinstance(expr, WhenExpr):
            return self._bind_when(joint, name, expr)
        if isinstance(expr, Call):
            return self._bind_call(joint, name, expr)
        if isinstance(expr, Pipe):
            return self._bind(joint, name, expr.rhs, logs=logs, inspect_out=inspect_out)
        raise KernelError(f"cannot bind expr {type(expr).__name__}")

    def _bind_when(self, joint: Joint, name: str, expr: WhenExpr) -> Joint:
        if joint.is_vacuum():
            return Joint.empty()
        out_worlds = []
        from .joint import World, _coalesce

        for w in joint.worlds:
            for ctrl, cp in self._ctrl_masses(expr.ctrl, w.assign).items():
                if cp <= EPS:
                    continue
                arm_body = None
                for arm in expr.arms:
                    if arm.is_else:
                        continue
                    if _pat_match(arm.pat, ctrl):
                        arm_body = arm.body
                        break
                if arm_body is None:
                    for arm in expr.arms:
                        if arm.is_else:
                            arm_body = arm.body
                            break
                if arm_body is None:
                    continue
                mass = w.mass * cp
                if isinstance(arm_body, Coin):
                    for val, p in ((0, 0.5), (1, 0.5)):
                        out_worlds.append(
                            World(assign={**w.assign, name: val}, mass=mass * p)
                        )
                else:
                    val = self._eval_value(arm_body, w.assign)
                    out_worlds.append(World(assign={**w.assign, name: val}, mass=mass))
        if not out_worlds:
            return Joint.empty()
        return Joint(worlds=_coalesce(out_worlds))

    def _ctrl_masses(self, ctrl: Expr, assign: dict[str, Any]) -> dict[Any, float]:
        if isinstance(ctrl, Coin):
            return {0: 0.5, 1: 0.5}
        if isinstance(ctrl, Var):
            return {assign[ctrl.name]: 1.0}
        if isinstance(ctrl, (LitInt, LitFloat, LitBool)):
            return {self._lit(ctrl): 1.0}
        v = self._eval_value(ctrl, assign)
        return {v: 1.0}

    def _bind_call(self, joint: Joint, name: str, expr: Call) -> Joint:
        callee = expr.callee

        # Math.sin(x) / Math.cos(x) / …
        if isinstance(callee, Attr):
            if isinstance(callee.obj, Var) and callee.obj.name == "Math":
                if not math_ops.known_math_op(callee.name):
                    raise KernelError(f"unknown Math.{callee.name}")
                if len(expr.args) != 1 or not isinstance(expr.args[0], Var):
                    raise KernelError(f"Math.{callee.name} expects one State variable")
                src = expr.args[0].name
                op = callee.name
                return joint.map_coord(src, name, lambda v: math_ops.apply_math(op, v))
            # extension: x.sin() → Math.sin(x)
            if isinstance(callee.obj, Var) and math_ops.known_math_op(callee.name):
                src = callee.obj.name
                op = callee.name
                return joint.map_coord(src, name, lambda v: math_ops.apply_math(op, v))
            # x.map(fn) / x.project(fn)
            if isinstance(callee.obj, Var) and callee.name in {"map", "project"}:
                src_expr = callee.obj
                if callee.name == "map":
                    if len(expr.args) < 1:
                        raise KernelError("map requires a lambda")
                    f = self._as_unary_fn(expr.args[0])
                    return joint.map_coord(src_expr.name, name, f)
                p = self._as_pred_fn(expr.args[0])
                projected = joint.project_coord(src_expr.name, p)
                if projected.is_vacuum():
                    return Joint.empty()
                return projected.bind_pushforward(name, lambda a: a[src_expr.name])
            raise KernelError(f"unsupported method {callee.name}")

        if isinstance(callee, Var):
            op = callee.name
        elif isinstance(callee, Coin):
            return joint.bind_split(name, {0: 0.5, 1: 0.5})
        else:
            raise KernelError(f"unsupported callee {type(callee)}")

        if op == "map":
            if len(expr.args) < 2:
                raise KernelError("map requires (src, fn)")
            src_expr, fn = expr.args[0], expr.args[1]
            if not isinstance(src_expr, Var):
                raise KernelError("map src must be a variable")
            f = self._as_unary_fn(fn)
            return joint.map_coord(src_expr.name, name, f)

        if op == "project":
            if len(expr.args) < 2:
                raise KernelError("project requires (src, pred)")
            src_expr, pred = expr.args[0], expr.args[1]
            if not isinstance(src_expr, Var):
                raise KernelError("project src must be a variable")
            p = self._as_pred_fn(pred)
            projected = joint.project_coord(src_expr.name, p)
            if projected.is_vacuum():
                return Joint.empty()
            return projected.bind_pushforward(name, lambda a: a[src_expr.name])

        if op == "interfer":
            if not expr.args:
                return Joint.empty()
            from .joint import World, _coalesce

            n = len(expr.args)
            out = []
            for w in joint.worlds:
                for arg in expr.args:
                    val = self._eval_value(arg, w.assign)
                    out.append(World(assign={**w.assign, name: val}, mass=w.mass / n))
            return Joint(worlds=_coalesce(out))

        if op == "coin":
            return joint.bind_split(name, {0: 0.5, 1: 0.5})
        if op == "vacuum":
            return Joint.empty()
        if op == "dirac":
            if not expr.args:
                raise KernelError("dirac requires an argument")
            return joint.bind_pushforward(name, lambda a: self._eval_value(expr.args[0], a))
        if math_ops.known_math_op(op):
            if len(expr.args) != 1 or not isinstance(expr.args[0], Var):
                raise KernelError(f"{op} expects one State variable")
            src = expr.args[0].name
            return joint.map_coord(src, name, lambda v: math_ops.apply_math(op, v))

        raise KernelError(f"unknown function `{op}`")

    def _as_unary_fn(self, fn: Expr) -> Callable[[Any], Any]:
        if isinstance(fn, Lambda):
            param = fn.param

            def f(v: Any) -> Any:
                return self._eval_value(fn.body, {param: v})

            return f
        raise KernelError("map/project fn must be a lambda (x -> expr)")

    def _as_pred_fn(self, fn: Expr) -> Callable[[Any], bool]:
        f = self._as_unary_fn(fn)

        def p(v: Any) -> bool:
            r = f(v)
            return bool(r)

        return p

    def _is_closed(self, expr: Expr) -> bool:
        if isinstance(expr, (LitInt, LitFloat, LitBool, LitString)):
            return True
        if isinstance(expr, Var):
            return False
        if isinstance(expr, BinOp):
            return self._is_closed(expr.lhs) and self._is_closed(expr.rhs)
        return False

    def _lit(self, expr: Expr) -> Any:
        if isinstance(expr, LitInt):
            return expr.value
        if isinstance(expr, LitFloat):
            return expr.value
        if isinstance(expr, LitBool):
            return expr.value
        if isinstance(expr, LitString):
            return expr.value
        raise KernelError("not a literal")

    def _eval_value(self, expr: Expr, assign: dict[str, Any]) -> Any:
        if isinstance(expr, LitInt):
            return expr.value
        if isinstance(expr, LitFloat):
            return expr.value
        if isinstance(expr, LitBool):
            return expr.value
        if isinstance(expr, LitString):
            return expr.value
        if isinstance(expr, Var):
            if expr.name not in assign:
                raise KernelError(f"unbound variable `{expr.name}`")
            return assign[expr.name]
        if isinstance(expr, Coin):
            # classical eval of coin is forbidden mid-value; sample (counts as rng — avoid)
            raise KernelError("coin() cannot be evaluated as a classical value; bind via state")
        if isinstance(expr, Vacuum):
            raise KernelError("vacuum() is not a classical value")
        if isinstance(expr, Dirac):
            return self._eval_value(expr.arg, assign)
        if isinstance(expr, BinOp):
            l = self._eval_value(expr.lhs, assign)
            r = self._eval_value(expr.rhs, assign)
            return _apply_op(expr.op, l, r)
        if isinstance(expr, WhenExpr):
            ctrl = self._eval_value(expr.ctrl, assign)
            for arm in expr.arms:
                if not arm.is_else and arm.pat == ctrl:
                    return self._eval_value(arm.body, assign)
            for arm in expr.arms:
                if arm.is_else:
                    return self._eval_value(arm.body, assign)
            raise KernelError("when: no matching arm")
        if isinstance(expr, Call):
            # allow pure calls on values: not yet
            raise KernelError("call cannot be classical value in Phase 2.2 value context")
        raise KernelError(f"cannot evaluate {type(expr).__name__} as value")

    def _expr_marginal(self, joint: Joint, expr: Expr) -> dict[Any, float]:
        if isinstance(expr, Var):
            return joint.marginal(expr.name)
        # general: pushforward values across worlds
        from collections import defaultdict

        acc: dict[Any, float] = defaultdict(float)
        if joint.is_vacuum():
            return {}
        for w in joint.worlds:
            try:
                v = self._eval_value(expr, w.assign)
            except KernelError:
                continue
            acc[v] += w.mass
        return {k: v for k, v in acc.items() if v > EPS}

    def _measure(
        self,
        joint: Joint,
        expr: Expr,
        *,
        sink: str | None,
        stdout: TextIO | None,
    ) -> MeasureResult:
        marginal = self._expr_marginal(joint, expr)
        if not marginal:
            out = ""
            text = ""  # vacuum: no sample
            if stdout is not None:
                stdout.write(text)
            return MeasureResult(
                value=None,
                vacuum=True,
                marginal={},
                rng_calls=self.rng_calls,
                sink=sink,
                output=text,
            )

        self.rng_calls += 1  # terminal measure draws once
        value = sample_from_marginal(marginal, self.rng)
        text = "" if value is None else _format_value(value)
        if sink is None or sink in {"stdout", "Stdout", "STDOUT"}:
            if stdout is not None and text:
                stdout.write(text + "\n")
            output = text
        else:
            # File sink: write via qpex.io helper
            from ..stdlib.io_ops import write_sink as _ws

            _ws(sink, (text + "\n") if text else "", stdout=None)
            output = text
        return MeasureResult(
            value=value,
            vacuum=False,
            marginal=marginal,
            rng_calls=self.rng_calls,
            sink=sink,
            output=output,
        )


def _apply_op(op: str, l: Any, r: Any) -> Any:
    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "*":
        return l * r
    if op == "/":
        if r == 0 or r == 0.0:
            # failure as value tag (ADR 0025) — classical context in joint atom
            return ("Err", "DivByZero")
        return l / r
    if op == "==":
        return l == r
    if op == "!=":
        return l != r
    if op == "<":
        return l < r
    if op == "<=":
        return l <= r
    if op == ">":
        return l > r
    if op == ">=":
        return l >= r
    raise KernelError(f"unknown op {op}")


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _pat_match(pat: Any, ctrl: Any) -> bool:
    if pat == ctrl:
        return True
    if isinstance(pat, (int, float)) and isinstance(ctrl, (int, float)):
        return float(pat) == float(ctrl)
    return False
