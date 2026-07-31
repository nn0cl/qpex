"""Kernel evaluator — AST → Joint transformers + terminal measure."""

from __future__ import annotations

import cmath
import random
from dataclasses import dataclass, field
from typing import Any, Callable, TextIO

from ..ast_nodes import (
    AssignStmt,
    Attr,
    BinOp,
    Call,
    ClassDecl,
    Coin,
    CompilationUnit,
    Dirac,
    EnumDecl,
    EvolveExpr,
    Expr,
    ExprStmt,
    FunDecl,
    ForEachStmt,
    Inspect,
    KetLit,
    Lambda,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    ListExpr,
    Measure,
    OpBin,
    OpHop,
    OpLit,
    OpNumber,
    OpQuadrature,
    OpGridQuad,
    OpPauli,
    OpPow,
    OpVar,
    OpAttr,
    OpIndexed,
    OpBinder,
    OpIdentity,
    OpCall,
    Pipe,
    ReturnStmt,
    Snapshot,
    StateBind,
    StructDecl,
    TensorExpr,
    TupleExpr,
    Vacuum,
    Var,
    WhenExpr,
)
from ..continuous_lowering import GridHamiltonian, GridHamiltonianRef
from ..finite_binder import operator_declared_space
from ..second_quantization import SecondQuantizationMappingError, resolve_mapping_expr
from ..stdlib import math_ops
from ..stdlib.io_ops import format_marginal_table, format_snapshot_csv, write_sink
from .op_attr_elaboration import (
    OpAttrElaborationError,
    materialize_op_attrs,
    materialize_op_scalar_vars,
)
from .joint import EPS, Joint, sample_from_marginal
from .mixed_state import DensityStateValue, density_from_call, matrix_from_list
from .lindblad import evolve_lindblad
from .matrix import Matrix
from ..static_hilbert import MVP_MAX_LOGICAL_QUBITS

RELATIONAL = {"==", "!=", "<", "<=", ">", ">="}


@dataclass
class EnumValue:
    """Runtime enum tag (ADR OOP)."""

    enum_name: str
    variant: str

    def __repr__(self) -> str:
        return f"{self.enum_name}.{self.variant}"


@dataclass
class StructValue:
    """Immutable value-type instance (copy-on-pass)."""

    struct_name: str
    fields: dict[str, Any]

    def copy(self) -> "StructValue":
        return StructValue(
            struct_name=self.struct_name,
            fields={k: (v.copy() if isinstance(v, StructValue) else v) for k, v in self.fields.items()},
        )


@dataclass
class ClassInstance:
    """Runtime object for ADR 0056 class instances (reference semantics)."""

    class_name: str
    fields: dict[str, Any]
    mutable: set[str] = field(default_factory=set)


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
    mixed_state_measured: bool = False
    execution_lane: str | None = None
    measurement_kind: str | None = None


class KernelError(Exception):
    pass


class KernelDiagnosticError(KernelError):
    """Runtime failure with a stable diagnostic code (ADR 0079)."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        line: int = 0,
        col: int = 0,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.line = line
        self.col = col


_SECOND_QUANTIZED_FAMILIES = {
    "FermionOperator",
    "BosonOperator",
    "SpinOperator",
    "QubitOperator",
}


class Evaluator:
    """Discrete PMF Kernel (stance a). Pure stmts are Joint → Joint."""

    SOURCE_LINDBLAD_DT = 0.01

    def __init__(
        self,
        *,
        rng: random.Random | None = None,
        seed: int | None = None,
        inspect_sink: TextIO | None = None,
        grid_hamiltonians: dict[str, GridHamiltonian] | None = None,
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
        self.operators: dict[str, Any] = {}
        # Typed second-quantized locals (FermionOperator/BosonOperator/...)
        # keyed by name -> raw symbolic expr (create/annihilate atoms),
        # kept separate from self.operators until a mapping resolves them
        # into an ordinary Pauli OpExpr (LISS-0032, ADR 0093).
        self.second_quantized_operators: dict[str, Any] = {}
        # Classical scalars for Operator coefficients (Float J = 1.0 → OpVar J)
        # Seed prelude constants (ADR 0062: pi, …)
        from ..stdlib.prelude import PRELUDE_CONSTANTS

        self.scalars: dict[str, float] = dict(PRELUDE_CONSTANTS)
        self.funs: dict[str, FunDecl] = {}
        self.classes: dict[str, ClassDecl] = {}
        self.enums: dict[str, EnumDecl] = {}
        self.structs: dict[str, StructDecl] = {}
        self.objects: dict[str, Any] = {}  # ClassInstance | StructValue | EnumValue
        self._this: ClassInstance | None = None
        self._in_init: bool = False  # `fn init` may assign `val` fields once
        self.mixed_states: dict[str, DensityStateValue] = {}
        self.povms: dict[str, tuple[str, str]] = {}
        self.static_register_sizes: dict[str, int] = {}
        self.mixed_state_measured = False
        self.execution_lane: str | None = None
        self.grid_hamiltonians = dict(grid_hamiltonians or {})

    def run_unit(self, unit: CompilationUnit, *, stdout: TextIO | None = None) -> EvalResult:
        joint = Joint.unit()
        if unit.main is None:
            return EvalResult(joint=Joint.empty())

        self.funs = {}
        self.classes = {}
        self.enums = {}
        self.structs = {}
        self.objects = {}
        self.mixed_states = {}
        self.povms = {}
        self.static_register_sizes = {}
        self.operator_spaces: dict[str, int] = {}
        self.mixed_state_measured = False
        self.execution_lane = None
        self._this = None
        self.operators = {
            alias: GridHamiltonianRef(alias) for alias in self.grid_hamiltonians
        }
        from ..finite_binder import lower_finite_binder_operators

        lowered_binders, _ = lower_finite_binder_operators(unit)
        for stmt in unit.main.body.stmts:
            if (
                isinstance(stmt, StateBind)
                and stmt.ty is not None
                and stmt.ty.name == "QubitRegister"
                and len(stmt.names) == 1
                and len(stmt.ty.args) == 1
            ):
                try:
                    self.static_register_sizes[stmt.names[0]] = int(stmt.ty.args[0].name)
                except ValueError:
                    pass
        from ..stdlib.prelude import PRELUDE_CONSTANTS

        self.scalars = dict(PRELUDE_CONSTANTS)
        for d in unit.decls:
            if isinstance(d, FunDecl) and d.name != "main":
                self.funs[d.qualified_name] = d
                self.funs[d.name] = d
            elif isinstance(d, ClassDecl):
                self.classes[d.qualified_name] = d
                self.classes[d.name] = d
            elif isinstance(d, EnumDecl):
                self.enums[d.qualified_name] = d
                self.enums[d.name] = d
            elif isinstance(d, StructDecl):
                self.structs[d.qualified_name] = d
                self.structs[d.name] = d

        measure_result: MeasureResult | None = None
        measurement_kind: str | None = None
        logs: list[str] = []
        inspect_out = self.inspect_sink if self.inspect_sink is not None else stdout

        for stmt in unit.main.body.stmts:
            if isinstance(stmt, ReturnStmt):
                raise KernelError("`main` cannot return; use terminal `measure`")
            if isinstance(stmt, ForEachStmt):
                joint = self._run_foreach(joint, stmt)
                continue
            if isinstance(stmt, ExprStmt):
                if isinstance(stmt.expr, Call):
                    joint = self._bind_call(joint, "__expr_stmt", stmt.expr)
                    continue
                raise KernelError("unsupported expression statement")
            if isinstance(stmt, StateBind):
                if stmt.ty is not None and stmt.ty.name == "POVM":
                    self._bind_povm(stmt)
                    continue
                if stmt.ty is not None and stmt.ty.name == "DensityState":
                    self._bind_mixed_state(stmt)
                    continue
                if stmt.ty is not None and stmt.ty.name == "QubitRegister":
                    # Static Hilbert shape is compile-time metadata; it has no
                    # runtime allocation or state coordinate in the Kernel.
                    continue
                if stmt.ty is not None and stmt.ty.name == "Operator":
                    if len(stmt.names) != 1:
                        raise KernelError("Operator bind expects a single name")
                    declared_space = operator_declared_space(stmt.ty)
                    if declared_space is not None:
                        self.operator_spaces[stmt.names[0]] = declared_space
                    self.operators[stmt.names[0]] = (
                        lowered_binders[stmt.names[0]]
                        if stmt.names[0] in lowered_binders
                        else self._resolve_operator_expr(stmt.expr)
                    )
                    continue
                if stmt.ty is not None and stmt.ty.name in _SECOND_QUANTIZED_FAMILIES:
                    if len(stmt.names) != 1:
                        raise KernelError("second-quantized bind expects a single name")
                    self._bind_second_quantized(stmt.names[0], stmt.ty.name, stmt.expr)
                    continue
                # Class / struct construction
                if stmt.ty is not None and len(stmt.names) == 1:
                    tname = stmt.ty.name
                    if tname in self.classes:
                        self.objects[stmt.names[0]] = self._construct_instance(
                            tname, stmt.expr
                        )
                        continue
                    if tname in self.structs:
                        self.objects[stmt.names[0]] = self._construct_struct(
                            tname, stmt.expr
                        )
                        continue
                    if tname in self.enums:
                        val = self._eval_value(stmt.expr, {})
                        if not isinstance(val, EnumValue) or (
                            val.enum_name not in {tname, self.enums[tname].qualified_name}
                            and val.enum_name.split(".")[-1] != tname.split(".")[-1]
                        ):
                            raise KernelError(
                                f"ENUM_TYPE_MISMATCH: expected `{tname}`, got {val!r}"
                            )
                        self.objects[stmt.names[0]] = val
                        continue
                # Capture Type-First classical scalars for H coefficients
                if (
                    stmt.ty is not None
                    and stmt.ty.name not in {"State", "Operator", "Delta"}
                    and stmt.ty.name not in self.classes
                    and stmt.ty.name not in self.structs
                    and stmt.ty.name not in self.enums
                    and len(stmt.names) == 1
                    and self._is_closed(stmt.expr)
                ):
                    try:
                        self.scalars[stmt.names[0]] = float(
                            self._eval_value(stmt.expr, {})
                        )
                    except (KernelError, TypeError, ValueError):
                        pass
                joint = self._bind_names(
                    joint, stmt.names, stmt.expr, logs=logs, inspect_out=inspect_out
                )
                # LISS-0137: method / joint-bound classical Float → scalars for
                # Operator coeffs and `evolve … for t` (empty-env _eval_value).
                if (
                    stmt.ty is not None
                    and stmt.ty.name
                    not in {
                        "State",
                        "Operator",
                        "Delta",
                        "POVM",
                        "DensityState",
                        "QubitRegister",
                    }
                    and stmt.ty.name not in self.classes
                    and stmt.ty.name not in self.structs
                    and stmt.ty.name not in self.enums
                    and len(stmt.names) == 1
                    and stmt.names[0] not in self.scalars
                ):
                    self._maybe_capture_classical_scalar(joint, stmt.names[0])
            elif isinstance(stmt, AssignStmt):
                self._exec_assign(stmt)
            elif isinstance(stmt, Snapshot):
                marg = self._expr_marginal(joint, stmt.expr)
                text = format_snapshot_csv(marg)
                write_sink(stmt.sink, text, stdout=stdout)
                logs.append(f"snapshot:{stmt.sink}:{marg}")
            elif isinstance(stmt, Measure):
                self._rng_calls_before_measure = self.rng_calls
                measurement_kind = self._resolve_measurement_kind(stmt.povm)
                if isinstance(stmt.expr, Var) and stmt.expr.name in self.mixed_states:
                    measure_result = self._measure_mixed(
                        self.mixed_states[stmt.expr.name], sink=stmt.sink, stdout=stdout
                    )
                    self.mixed_state_measured = True
                else:
                    measure_result = self._measure(joint, stmt.expr, sink=stmt.sink, stdout=stdout)
                break
            else:
                raise KernelError(f"unsupported stmt {type(stmt)}")

        return EvalResult(
            joint=joint,
            measure=measure_result,
            rng_calls_before_measure=self._rng_calls_before_measure,
            logs=logs,
            mixed_state_measured=self.mixed_state_measured,
            execution_lane=self.execution_lane,
            measurement_kind=measurement_kind,
        )

    def _resolve_measurement_kind(self, povm: Expr | None) -> str:
        if povm is None:
            return "ComputationalBasis"
        if isinstance(povm, Var) and povm.name in self.povms:
            return self.povms[povm.name][1]
        raise KernelError("INVALID_POVM_EFFECT")

    def _bind_povm(self, stmt: StateBind) -> None:
        if (
            isinstance(stmt.expr, Call)
            and _call_name(stmt.expr) == "ComputationalBasis"
        ):
            domain = stmt.ty.args[0].name if stmt.ty and stmt.ty.args else "Unknown"
            self.povms[stmt.names[0]] = (domain, "ComputationalBasis")
            return
        raise KernelError("INVALID_POVM_EFFECT")

    def _bind_mixed_state(self, stmt: StateBind) -> None:
        if len(stmt.names) != 1 or stmt.ty is None:
            raise KernelError("DensityState bind expects one name")
        domain = stmt.ty.args[0].name if stmt.ty.args else "Unknown"
        expr = stmt.expr
        if isinstance(expr, Call) and _call_name(expr) == "DensityState":
            try:
                self.mixed_states[stmt.names[0]] = density_from_call(expr, domain=domain)
            except ValueError as exc:
                raise KernelError(str(exc)) from exc
            return
        if isinstance(expr, Call) and _call_name(expr) == "lindblad":
            if len(expr.args) != 4 or not isinstance(expr.args[0], Var):
                raise KernelError("lindblad requires a DensityState source")
            source = self.mixed_states.get(expr.args[0].name)
            if source is None:
                raise KernelError("lindblad source must be a DensityState")
            # A declaration-only source contract may still carry unresolved
            # placeholders. Keep that path opaque; numerical lowering starts
            # only when all MVP inputs are explicit.
            if (
                isinstance(expr.args[1], Var)
                and expr.args[1].name not in self.operators
            ) or (
                isinstance(expr.args[2], Var)
            ) or (
                isinstance(expr.args[3], Var)
                and expr.args[3].name not in self.scalars
            ):
                self.mixed_states[stmt.names[0]] = DensityStateValue(
                    matrix=[row[:] for row in source.matrix],
                    domain=domain,
                    operation="lindblad",
                )
                self.execution_lane = "cpu/simulator"
                return
            n_qubits = _density_matrix_n_qubits(source.matrix)
            hamiltonian = self._resolve_lindblad_hamiltonian(expr.args[1], n_qubits)
            jumps = self._resolve_lindblad_jumps(expr.args[2], n_qubits)
            try:
                total_time = float(self._eval_value(expr.args[3], {}))
                evolved = evolve_lindblad(
                    source.matrix,
                    hamiltonian,
                    jumps,
                    total_time=total_time,
                    dt=self.SOURCE_LINDBLAD_DT,
                )
            except (KernelError, TypeError, ValueError, RuntimeError) as exc:
                raise KernelError(str(exc)) from exc
            self.mixed_states[stmt.names[0]] = DensityStateValue(
                matrix=evolved,
                domain=domain,
                operation="lindblad",
            )
            self.execution_lane = "cpu/simulator"
            return
        if isinstance(expr, Call) and _call_name(expr) == "apply":
            if len(expr.args) < 2 or not isinstance(expr.args[1], Var):
                raise KernelError("mixed apply requires a DensityState source")
            source = self.mixed_states.get(expr.args[1].name)
            if source is None:
                raise KernelError("mixed apply source must be a DensityState")
            self.mixed_states[stmt.names[0]] = source
            return
        raise KernelError("unsupported DensityState construction")

    def _resolve_lindblad_jumps(self, expr: Expr, n_qubits: int) -> list[Matrix]:
        if isinstance(expr, ListExpr):
            if expr.items:
                raise KernelError(
                    "non-empty Lindblad jumps must use JumpSet([RawMatrix(...)])"
                )
            return []
        if not isinstance(expr, Call) or _call_name(expr) != "JumpSet":
            raise KernelError("Lindblad jump input must be JumpSet or an empty list")
        if len(expr.args) != 1 or not isinstance(expr.args[0], ListExpr):
            raise KernelError("JumpSet requires a finite list")
        jumps: list[Matrix] = []
        for item in expr.args[0].items:
            if isinstance(item, Var):
                if item.name not in self.operators:
                    raise KernelError(
                        f"SYMBOLIC_JUMP_LOWERING_REQUIRED: jump `{item.name}` "
                        "must resolve to an Operator"
                    )
                try:
                    jumps.append(self._compile_lindblad_operator(item.name, n_qubits))
                except ValueError as exc:
                    raise KernelError(str(exc)) from exc
                continue
            if not isinstance(item, Call) or _call_name(item) != "RawMatrix":
                raise KernelError("JumpSet entries must be explicit RawMatrix values")
            if len(item.args) != 1:
                raise KernelError("RawMatrix requires a finite square numeric matrix")
            try:
                matrix = matrix_from_list(item.args[0])
            except ValueError as exc:
                raise KernelError(str(exc)) from exc
            jumps.append(matrix)
        return jumps

    def _resolve_lindblad_hamiltonian(self, expr: Expr, n_qubits: int) -> Matrix:
        from .unitaries import named_gate_matrix

        if isinstance(expr, Var) and expr.name in self.operators:
            try:
                return self._compile_lindblad_operator(expr.name, n_qubits)
            except ValueError as exc:
                raise KernelError(str(exc)) from exc
        if isinstance(expr, Var):
            matrix = named_gate_matrix(expr.name)
            if matrix is not None:
                return matrix
        raise KernelError("source Lindblad MVP requires a resolvable Hamiltonian")

    def _compile_lindblad_operator(self, name: str, n_qubits: int) -> Matrix:
        from .hamiltonian import compile_hamiltonian

        return compile_hamiltonian(
            self.operators[name],
            env=self.operators,
            scalars=self.scalars,
            n_qubits=n_qubits,
        )

    def _measure_mixed(
        self,
        state: DensityStateValue,
        *,
        sink: str | None,
        stdout: TextIO | None,
    ) -> MeasureResult:
        marginal = {
            index: max(0.0, float(state.matrix[index][index].real))
            for index in range(len(state.matrix))
        }
        marginal = {key: value for key, value in marginal.items() if value > EPS}
        if not marginal:
            return MeasureResult(
                value=None, vacuum=True, marginal={}, rng_calls=self.rng_calls, sink=sink
            )
        self.rng_calls += 1
        value = sample_from_marginal(marginal, self.rng)
        text = _format_value(value)
        if sink is None or sink in {"stdout", "Stdout", "STDOUT"}:
            if stdout is not None:
                stdout.write(text + "\n")
        else:
            write_sink(sink, text + "\n", stdout=None)
        return MeasureResult(
            value=value,
            vacuum=False,
            marginal=marginal,
            rng_calls=self.rng_calls,
            sink=sink,
            output=text,
        )

    def _run_foreach(self, joint: Joint, stmt: ForEachStmt) -> Joint:
        """Expand a static register loop into compiler-internal wire names."""
        collection = stmt.collection
        if isinstance(collection, Var):
            count = self.static_register_sizes.get(collection.name)
        elif (
            isinstance(collection, Call)
            and isinstance(collection.callee, Var)
            and collection.callee.name == "register"
            and len(collection.args) == 1
            and isinstance(collection.args[0], LitInt)
            and collection.args[0].value > 0
        ):
            count = collection.args[0].value
        else:
            count = None
        if count is None or count <= 0:
            raise KernelError("FOR_EACH_DYNAMIC_BOUND_ERROR: static register required")
        if count > MVP_MAX_LOGICAL_QUBITS:
            raise KernelError(
                "STATIC_HILBERT_RESOURCE_ERROR: static Hilbert expansion exceeds "
                f"the MVP budget ({MVP_MAX_LOGICAL_QUBITS})"
            )
        for index in range(count):
            wire = f"__foreach_{stmt.element}_{index}"
            joint = self._bind_names(
                joint,
                [wire],
                KetLit(label="0", span=stmt.span),
                logs=[],
                inspect_out=None,
            )
            for body_stmt in stmt.body.stmts:
                if not isinstance(body_stmt, ExprStmt) or not isinstance(body_stmt.expr, Call):
                    raise KernelError("forEach body supports Kernel operation calls only")
                call = body_stmt.expr
                if (
                    not isinstance(call.callee, Var)
                    or call.callee.name != "apply"
                    or len(call.args) != 2
                    or not isinstance(call.args[1], Var)
                    or call.args[1].name != stmt.element
                ):
                    raise KernelError("forEach body must apply an operator to its element")
                expanded = Call(
                    callee=call.callee,
                    args=[call.args[0], Var(name=wire, span=stmt.span)],
                    span=call.span,
                )
                joint = self._bind_call(joint, wire, expanded)
        return joint

    def _require_uncompute_zero(self, joint: Joint, name: str) -> None:
        """LISS-0114 F: simulator-equivalence check for ≈ computational |0⟩."""
        from .uncompute import require_computational_basis_zero

        try:
            require_computational_basis_zero(joint, name)
        except ValueError as exc:
            raise KernelError(str(exc)) from exc

    def _verify_static_uncompute_bind(
        self, joint: Joint, name: str, expr: Expr
    ) -> None:
        if isinstance(expr, Vacuum) or (
            isinstance(expr, KetLit) and expr.label == "0"
        ):
            self._require_uncompute_zero(joint, name)

    def _bind_names(
        self,
        joint: Joint,
        names: list[str],
        expr: Expr,
        *,
        logs: list[str] | None = None,
        inspect_out: TextIO | None = None,
    ) -> Joint:
        if isinstance(expr, EvolveExpr):
            return self._bind_evolve(joint, names, expr)
        if isinstance(expr, TensorExpr):
            return self._bind_tensor(joint, names, expr)
        if isinstance(expr, Call) and isinstance(expr.callee, Var):
            fun = self.funs.get(expr.callee.name)
            if fun is not None:
                return self._bind_user_fun(
                    joint, names, expr, fun, logs=logs, inspect_out=inspect_out
                )
        if isinstance(expr, TupleExpr):
            if len(expr.items) != len(names):
                raise KernelError(
                    f"tuple arity {len(expr.items)} != bind arity {len(names)}"
                )
            updates = {
                name: (lambda a, e=item: self._eval_value(e, a))
                for name, item in zip(names, expr.items)
            }
            return joint.bind_multi(updates)
        if len(names) != 1:
            raise KernelError(f"cannot bind {len(names)} names to {type(expr).__name__}")
        out = self._bind(joint, names[0], expr, logs=logs, inspect_out=inspect_out)
        self._verify_static_uncompute_bind(out, names[0], expr)
        return out

    def _bind_tensor(self, joint: Joint, names: list[str], expr: TensorExpr) -> Joint:
        """Independent reduced-state tensor: (a, b) = left *|* right."""
        from .joint import World, _coalesce

        if len(names) != 2:
            raise KernelError("`*|*` / tensor bind expects two names `(a, b) = …`")

        # Both sides already on the joint → relabel product wires (preserve amps)
        if isinstance(expr.left, Var) and isinstance(expr.right, Var):
            ln, rn = expr.left.name, expr.right.name
            out: list[World] = []
            for w in joint.worlds:
                if ln not in w.assign or rn not in w.assign:
                    raise KernelError(
                        f"`*|*` needs coordinates `{ln}` and `{rn}` on the joint"
                    )
                assign = {k: v for k, v in w.assign.items() if k not in {ln, rn}}
                assign[names[0]] = w.assign[ln]
                assign[names[1]] = w.assign[rn]
                cp = {
                    k: v
                    for k, v in w.coord_phase.items()
                    if k not in {ln, rn}
                }
                if ln in w.coord_phase:
                    cp[names[0]] = w.coord_phase[ln]
                if rn in w.coord_phase:
                    cp[names[1]] = w.coord_phase[rn]
                out.append(World(assign=assign, amp=w.amp, coord_phase=cp))
            return Joint(worlds=_coalesce(out))

        def _amps_indep(side: Expr) -> list[tuple[Any, complex]]:
            jl = self._bind(Joint.unit(), "_T", side)
            return [(w.assign["_T"], w.amp) for w in jl.worlds]

        left = _amps_indep(expr.left)
        right = _amps_indep(expr.right)
        if not left or not right:
            return Joint.empty()
        out = [
            World(assign={names[0]: vl, names[1]: vr}, amp=al * ar)
            for vl, al in left
            for vr, ar in right
        ]
        return Joint(worlds=_coalesce(out))

    def _eval_times(self, times: Expr | int) -> int:
        """ADR 0060: resolve evolve `times` to a non-negative int (Float truncates)."""
        if isinstance(times, int):
            n = times
        else:
            raw = self._eval_value(times, {})
            try:
                n = int(float(raw))
            except (TypeError, ValueError) as e:
                raise KernelError(
                    f"evolve times must evaluate to a number, got {raw!r}"
                ) from e
        if n < 0:
            raise KernelError(f"evolve times must be non-negative, got {n}")
        return n

    def _bind_evolve(self, joint: Joint, names: list[str], expr: EvolveExpr) -> Joint:
        if len(expr.seeds) != len(names):
            raise KernelError(
                f"evolve seeds {len(expr.seeds)} != bind names {len(names)}"
            )

        # Hamiltonian path: evolve psi under H for t  (ADR 0038 / 0041)
        if expr.hamiltonian is not None:
            return self._bind_evolve_hamiltonian(joint, names, expr)

        # Initialize working coordinates from seeds (correlated copy / eval).
        init: dict[str, Callable[[dict[str, Any]], Any]] = {}
        for name, seed in zip(names, expr.seeds):
            if isinstance(seed, Var):
                sn = seed.name
                init[name] = lambda a, sn=sn: a[sn]
            else:
                init[name] = lambda a, s=seed: self._eval_value(s, a)
        joint = joint.bind_multi(init)

        if expr.body is None:
            raise KernelError("block evolve requires a `{ … }` body")

        n_times = self._eval_times(expr.times)
        for _step in range(n_times):
            for let in expr.body.lets:
                ln = let.name
                le = let.expr
                # Gate / walk Call must use Joint transformers, not scalar eval
                if isinstance(le, Call):
                    joint = self._bind(joint, ln, le)
                else:
                    joint = joint.bind_pushforward(
                        ln, lambda a, e=le: self._eval_value(e, a)
                    )
            res = expr.body.result
            if isinstance(res, Call) and isinstance(res.callee, Var):
                fun = self.funs.get(res.callee.name)
                if fun is not None:
                    joint = self._bind_user_fun(joint, names, res, fun)
                    continue
            if isinstance(res, TupleExpr):
                if len(res.items) != len(names):
                    raise KernelError("evolve result tuple arity mismatch")
                updates = {
                    name: (lambda a, e=item: self._eval_value(e, a))
                    for name, item in zip(names, res.items)
                }
                joint = joint.bind_multi(updates)
            else:
                if len(names) != 1:
                    raise KernelError("evolve scalar result requires a single bind name")
                if isinstance(res, Call):
                    joint = self._bind(joint, names[0], res)
                else:
                    joint = joint.bind_pushforward(
                        names[0], lambda a, e=res: self._eval_value(e, a)
                    )
        return joint

        return n

    def _eval_max_steps(self, max_steps: Expr | None) -> int:
        if not isinstance(max_steps, LitInt) or max_steps.value <= 0:
            raise KernelError("evolve until requires a positive compile-time `max` bound")
        return max_steps.value

    def _eval_until_predicate(
        self, joint: Joint, names: list[str], predicate: Expr
    ) -> bool:
        """Pure Kernel predicate: no RNG, measure, or outer mutation (ADR 0079)."""
        if isinstance(predicate, LitBool):
            return predicate.value
        if isinstance(predicate, Call) and isinstance(predicate.callee, Var):
            if predicate.callee.name == "converged":
                if len(predicate.args) != 1 or not isinstance(predicate.args[0], Var):
                    raise KernelError("converged requires one state variable")
                coord = predicate.args[0].name
                if coord not in names:
                    raise KernelError(
                        f"converged predicate may reference evolve seeds only, got `{coord}`"
                    )
                return len(joint.amplitude_marginal(coord)) == 1
        raise KernelError(
            "evolve until predicates support `converged(state)` or literal booleans only"
        )

    def _bind_evolve_hamiltonian(
        self, joint: Joint, names: list[str], expr: EvolveExpr
    ) -> Joint:
        if len(names) != len(expr.seeds):
            raise KernelError("hamiltonian evolve seed/bind arity mismatch")
        if expr.hamiltonian is None or expr.duration is None:
            raise KernelError("hamiltonian evolve requires `under H for t`")

        # Resolve seed coords into `names` working wires
        init: dict[str, Callable[[dict[str, Any]], Any]] = {}
        for name, seed in zip(names, expr.seeds):
            if isinstance(seed, Var):
                sn = seed.name
                init[name] = lambda a, sn=sn: a[sn]
            else:
                init[name] = lambda a, s=seed: self._eval_value(s, a)
        joint = joint.bind_multi(init)

        if expr.until_predicate is None:
            return self._hamiltonian_evolve_one_step(joint, names, expr)

        max_n = self._eval_max_steps(expr.max_steps)
        for _ in range(max_n):
            joint = self._hamiltonian_evolve_one_step(joint, names, expr)
            if self._eval_until_predicate(joint, names, expr.until_predicate):
                return joint
        raise KernelDiagnosticError(
            "EVOLVE_UNTIL_MAX_STEPS_ERROR",
            "evolve until reached max steps without predicate success",
            line=expr.span.line,
            col=expr.span.col,
        )

    def _hamiltonian_evolve_one_step(
        self, joint: Joint, names: list[str], expr: EvolveExpr
    ) -> Joint:
        from .hamiltonian import compile_hamiltonian, hop_basis_dim, op_n_qubits
        from .joint import World, _coalesce
        from .matrix import apply_mat, expm_ih
        from .quantum_ops import apply_u2, pauli_u
        from ..ast_nodes import (
            OpBin,
            OpGridQuad,
            OpHop,
            OpLit,
            OpNumber,
            OpPauli,
            OpPow,
            OpQuadrature,
            OpVar,
        )

        t = float(self._eval_value(expr.duration, {}))
        hop = expr.hamiltonian
        assert hop is not None

        # Legacy single-name Pauli string: evolve psi under X for t
        if isinstance(hop, Var) and hop.name.upper() in {"I", "X", "Y", "Z"} and len(names) == 1:
            # LISS-0112 Slice B: Identity is a no-op on any computational level
            # (matches qubit `pauli_u(I)` = I; enables D=3 |2⟩ support).
            if hop.name.upper() in {"I", "ID", "IDENTITY"}:
                return joint
            try:
                u = pauli_u(hop.name, t)
            except ValueError as e:
                raise KernelError(str(e)) from e
            src = names[0]
            amps = joint.amplitude_marginal(src)
            a0, a1 = amps.get(0, 0j), amps.get(1, 0j)
            if any(v not in (0, 1) for v in amps):
                raise KernelError(
                    f"hamiltonian `{hop.name}` expects qubit support {{0,1}}, got {sorted(amps)}"
                )
            b0, b1 = apply_u2(a0, a1, u)
            out: list[World] = []
            if abs(b0) ** 2 > EPS:
                out.append(World(assign={names[0]: 0}, amp=b0))
            if abs(b1) ** 2 > EPS:
                out.append(World(assign={names[0]: 1}, amp=b1))
            return Joint(worlds=_coalesce(out))

        # Operator expression or bound Operator name
        if isinstance(hop, Var):
            if hop.name not in self.operators:
                # bare Pauli already handled; unknown
                raise KernelError(f"unknown Operator / Hamiltonian `{hop.name}`")
            op_ast = self.operators[hop.name]
        elif isinstance(
            hop,
            (
                OpPauli,
                OpNumber,
                OpQuadrature,
                OpGridQuad,
                OpHop,
                OpLit,
                OpBin,
                OpPow,
                OpVar,
                OpAttr,
                OpIndexed,
                OpBinder,
                OpIdentity,
                OpCall,
            ),
        ):
            op_ast = hop
        else:
            raise KernelError("hamiltonian must be Operator name or Pauli literal")

        try:
            op_ast = materialize_op_attrs(op_ast, self.objects)
        except OpAttrElaborationError as exc:
            raise KernelError(str(exc)) from exc

        declared_space = (
            self.operator_spaces.get(hop.name)
            if isinstance(hop, Var)
            else None
        )
        if isinstance(op_ast, GridHamiltonianRef):
            gh = self.grid_hamiltonians[op_ast.alias]
            return self._evolve_precomputed_grid(joint, names, gh, t)
        try:
            nq = (
                declared_space
                if declared_space is not None
                else op_n_qubits(op_ast, self.operators, self.scalars)
            )
        except ValueError as e:
            raise KernelError(str(e)) from e

        if nq == 0:
            # Fock / site-basis: single coordinate, levels 0..dim-1
            if len(names) != 1:
                raise KernelError("Fock Hamiltonian evolve requires a single bind name")
            src = names[0]
            amps = joint.amplitude_marginal(src)
            keys = sorted(amps.keys())
            if not keys or any(not isinstance(k, int) or k < 0 for k in keys):
                raise KernelError("Fock evolve expects non-negative Int levels")
            dim = max(keys) + 1
            dim = max(dim, hop_basis_dim(op_ast, self.operators, self.scalars), 2)
            try:
                hmat = compile_hamiltonian(
                    op_ast,
                    env=self.operators,
                    scalars=self.scalars,
                    n_qubits=0,
                    fock_dim=dim,
                )
                u = expm_ih(hmat, t)
            except ValueError as e:
                raise KernelError(str(e)) from e
            vec = [amps.get(i, 0j) for i in range(dim)]
            outv = apply_mat(u, vec)
            out_w = [
                World(assign={src: i}, amp=outv[i])
                for i in range(dim)
                if abs(outv[i]) ** 2 > EPS
            ]
            return Joint(worlds=_coalesce(out_w))

        if nq < 0:
            # Position grid: Float abscissae on a single wire
            if len(names) != 1:
                raise KernelError("grid Hamiltonian evolve requires a single bind name")
            src = names[0]
            amps = joint.amplitude_marginal(src)
            keys = sorted(amps.keys(), key=lambda x: float(x))
            if not keys or any(not isinstance(k, (int, float)) for k in keys):
                raise KernelError("grid evolve expects Float (or Int) abscissae")
            xs = [float(k) for k in keys]
            try:
                hmat = compile_hamiltonian(
                    op_ast,
                    env=self.operators,
                    scalars=self.scalars,
                    n_qubits=-1,
                    grid_xs=xs,
                )
                u = expm_ih(hmat, t)
            except ValueError as e:
                raise KernelError(str(e)) from e
            vec = [amps[k] for k in keys]
            outv = apply_mat(u, vec)
            out_w = [
                World(assign={src: keys[i]}, amp=outv[i])
                for i in range(len(keys))
                if abs(outv[i]) ** 2 > EPS
            ]
            return Joint(worlds=_coalesce(out_w))

        # Multi-qubit Pauli H on names[0..nq) — sparse Pauli-sum + Taylor e^{-iHt}
        if len(names) < nq:
            raise KernelError(
                f"Operator needs {nq} qubit wires, bind has {len(names)}"
            )
        wires = names[:nq]
        from .sparse_pauli import compile_sparse_pauli, expm_ih_apply

        try:
            terms = compile_sparse_pauli(
                op_ast,
                env=self.operators,
                scalars=self.scalars,
                n_qubits=nq,
            )
        except ValueError as e:
            raise KernelError(str(e)) from e

        dim = 2**nq
        # Build amplitude vector over computational basis; other coords kept per world
        # Strategy: group worlds by non-wire assigns; within each group apply U on wire bits
        from collections import defaultdict

        groups: dict[tuple, list[World]] = defaultdict(list)
        for w in joint.worlds:
            key = tuple(sorted((k, v) for k, v in w.assign.items() if k not in wires))
            groups[key].append(w)

        out_worlds: list[World] = []
        for key, ws in groups.items():
            vec = [0j] * dim
            phases = {}
            for w in ws:
                bits = []
                ok = True
                for name in wires:
                    if name not in w.assign or w.assign[name] not in (0, 1):
                        ok = False
                        break
                    bits.append(int(w.assign[name]))
                if not ok:
                    raise KernelError(
                        f"hamiltonian evolve expects qubit bits on {wires}"
                    )
                idx = 0
                for b in bits:
                    idx = (idx << 1) | b
                vec[idx] += w.amp
                phases[idx] = dict(w.coord_phase)
            outv = expm_ih_apply(terms, t, vec)
            base_assign = dict(key)
            for idx, amp in enumerate(outv):
                if abs(amp) ** 2 <= EPS:
                    continue
                assign = dict(base_assign)
                # unpack bits MSB = wires[0]
                x = idx
                bit_list = []
                for _ in range(nq):
                    bit_list.append(x & 1)
                    x >>= 1
                bit_list.reverse()
                for name, bit in zip(wires, bit_list):
                    assign[name] = bit
                out_worlds.append(
                    World(
                        assign=assign,
                        amp=amp,
                        coord_phase=phases.get(idx, {}),
                    )
                )
        return Joint(worlds=_coalesce(out_worlds))

    def _evolve_precomputed_grid(
        self,
        joint: Joint,
        names: list[str],
        grid: GridHamiltonian,
        t: float,
    ) -> Joint:
        from .joint import World, _coalesce
        from .matrix import apply_mat, expm_ih

        if len(names) != 1:
            raise KernelError("grid Hamiltonian evolve requires a single bind name")
        src = names[0]
        amps = joint.amplitude_marginal(src)
        keys = sorted(amps.keys(), key=lambda x: float(x))
        if not keys or any(not isinstance(k, (int, float)) for k in keys):
            raise KernelError("grid evolve expects Float (or Int) abscissae")
        xs = list(grid.xs)
        if len(keys) != len(xs) or any(abs(float(k) - x) > 1e-9 for k, x in zip(keys, xs)):
            raise KernelError(
                "grid state abscissae must match the lowered discretization grid"
            )
        hmat = [list(row) for row in grid.matrix]
        u = expm_ih(hmat, t)
        vec = [amps[k] for k in keys]
        outv = apply_mat(u, vec)
        out_w = [
            World(assign={src: keys[i]}, amp=outv[i])
            for i in range(len(keys))
            if abs(outv[i]) ** 2 > EPS
        ]
        return Joint(worlds=_coalesce(out_w))

    def _operator_name(self, expr: Expr) -> str:
        if isinstance(expr, Var):
            return expr.name
        raise KernelError("hamiltonian / observable must be a named operator (X,Y,Z,…)")

    def _resolve_unitary_matrix(self, u_expr: Expr, n_wires: int) -> list[list[complex]]:
        """Resolve Operator / Hadamard / Pauli / S|T / rx|ry|rz → dense unitary."""
        from .hamiltonian import compile_hamiltonian, op_n_qubits
        from .unitaries import named_gate_matrix, rotation_gate_matrix

        if isinstance(u_expr, Call) and isinstance(u_expr.callee, Var):
            op = u_expr.callee.name.lower()
            if op in {"rx", "ry", "rz"}:
                if len(u_expr.args) != 1:
                    raise KernelError(f"{op} requires (theta)")
                if n_wires != 1:
                    raise KernelError(f"{op} is 1-qubit; pass one target wire")
                theta = float(self._eval_value(u_expr.args[0], {}))
                return rotation_gate_matrix(op[1], theta)

        if not isinstance(u_expr, Var):
            raise KernelError(
                "unitary must be an Operator / gate name / rx|ry|rz(theta)"
            )
        uname = u_expr.name
        if uname in self.operators:
            op_ast = self.operators[uname]
            try:
                nq = op_n_qubits(op_ast, self.operators, self.scalars)
                if nq == 0:
                    raise KernelError("unitary apply does not support Fock N operators")
                if nq != n_wires:
                    raise KernelError(
                        f"Operator `{uname}` needs {nq} wires, got {n_wires}"
                    )
                return compile_hamiltonian(
                    op_ast,
                    env=self.operators,
                    scalars=self.scalars,
                    n_qubits=n_wires,
                )
            except ValueError as e:
                raise KernelError(str(e)) from e
        u_mat = named_gate_matrix(uname)
        if u_mat is None:
            raise KernelError(
                f"unknown unitary `{uname}` "
                "(Operator name, H/S/T, Pauli X|Y|Z|I, or rx|ry|rz(theta))"
            )
        if n_wires != 1:
            raise KernelError(f"gate `{uname}` is 1-qubit; pass one target wire")
        return u_mat

    def _bind_apply(self, joint: Joint, name: str, expr: Call) -> Joint:
        """apply(U, w0[, w1, …]) — apply unitary matrix (not e^{-iHt})."""
        from .unitaries import apply_unitary_on_wires

        if len(expr.args) < 2:
            raise KernelError("apply requires (U, wire[, wire…])")
        u_expr = expr.args[0]
        wire_args = expr.args[1:]
        if not all(isinstance(a, Var) for a in wire_args):
            raise KernelError("apply wires must be state variables")
        wires = [a.name for a in wire_args]  # type: ignore[union-attr]
        # LISS-0112 Slice B: bare Identity is a no-op (preserves D=3 levels).
        if (
            isinstance(u_expr, Var)
            and u_expr.name.upper() in {"I", "ID", "IDENTITY"}
            and len(wires) == 1
        ):
            if name in wires:
                return joint
            w0 = wires[0]
            return joint.bind_pushforward(name, lambda a, w=w0: a[w])
        u_mat = self._resolve_unitary_matrix(u_expr, len(wires))
        try:
            updated = apply_unitary_on_wires(joint, wires, u_mat)
        except ValueError as e:
            raise KernelError(str(e)) from e

        if name in wires:
            return updated
        w0 = wires[0]
        return updated.bind_pushforward(name, lambda a, w=w0: a[w])

    def _is_unitary_name(self, name: str) -> bool:
        from .unitaries import named_gate_matrix

        return name in self.operators or named_gate_matrix(name) is not None

    def _split_capply_args(
        self, args: list
    ) -> tuple[list[str], list[int], Expr, list[str]]:
        """Parse capply(c0[, !c1…], U, t0[, …]) — polarity 1=filled, 0=open (`!`)."""
        from ..ast_nodes import UnaryNot

        u_idx = None
        for i, a in enumerate(args):
            if isinstance(a, Var) and self._is_unitary_name(a.name):
                u_idx = i
                break
        if u_idx is None:
            raise KernelError(
                "capply requires a unitary name (Operator / Hadamard / Pauli) "
                "between controls and targets"
            )
        if u_idx < 1:
            raise KernelError("capply requires at least one control before U")
        if u_idx >= len(args) - 1:
            raise KernelError("capply requires at least one target after U")
        ctrl_args = args[:u_idx]
        u_expr = args[u_idx]
        tgt_args = args[u_idx + 1 :]

        ctrls: list[str] = []
        poles: list[int] = []
        for a in ctrl_args:
            if isinstance(a, Var):
                ctrls.append(a.name)
                poles.append(1)
            elif isinstance(a, UnaryNot) and isinstance(a.expr, Var):
                ctrls.append(a.expr.name)
                poles.append(0)
            else:
                raise KernelError(
                    "capply controls must be state vars or open-polarity `!var`"
                )
        if not all(isinstance(a, Var) for a in tgt_args):
            raise KernelError("capply targets must be state variables")
        tgts = [a.name for a in tgt_args]  # type: ignore[union-attr]
        if len(set(ctrls + tgts)) != len(ctrls) + len(tgts):
            raise KernelError("capply wires must be distinct")
        return ctrls, poles, u_expr, tgts

    def _bind_capply(
        self,
        joint: Joint,
        name: str,
        expr: Call,
        *,
        force_all_open: bool = False,
        op_label: str = "capply",
    ) -> Joint:
        """capply / ocapply — filled, open, or mixed polarities (ADR 0048)."""
        from .unitaries import apply_unitary_on_wires, multi_controlled_unitary

        if len(expr.args) < 3:
            raise KernelError(f"{op_label} requires (ctrl[, …], U, tgt[, …])")
        ctrls, poles, u_expr, tgts = self._split_capply_args(list(expr.args))
        if force_all_open:
            poles = [0] * len(ctrls)
        u_mat = self._resolve_unitary_matrix(u_expr, len(tgts))
        mask = 0
        for p in poles:
            mask = (mask << 1) | p
        cu = multi_controlled_unitary(
            u_mat, n_controls=len(ctrls), active_mask=mask
        )
        wires = [*ctrls, *tgts]
        try:
            updated = apply_unitary_on_wires(joint, wires, cu)
        except ValueError as e:
            raise KernelError(str(e)) from e
        if name in wires:
            return updated
        t0 = tgts[0]
        return updated.bind_pushforward(name, lambda a, w=t0: a[w])

    def _bind_ket(self, joint: Joint, name: str, expr: KetLit) -> Joint:
        from .joint import World, _coalesce
        from .quantum_ops import ket_support

        try:
            pairs = ket_support(expr.label)
        except ValueError as e:
            raise KernelError(str(e)) from e
        if joint.is_vacuum():
            return Joint.empty()
        out: list[World] = []
        for w in joint.worlds:
            for val, amp in pairs:
                na = w.amp * amp
                if abs(na) ** 2 > EPS:
                    out.append(
                        World(
                            assign={**w.assign, name: val},
                            amp=na,
                            coord_phase=dict(w.coord_phase),
                        )
                    )
        return Joint(worlds=_coalesce(out))

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
        if isinstance(expr, KetLit):
            return self._bind_ket(joint, name, expr)
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
        if isinstance(expr, Attr):
            return joint.bind_pushforward(name, lambda a: self._eval_value(expr, a))
        if isinstance(expr, WhenExpr):
            return self._bind_when(joint, name, expr)
        if isinstance(expr, Call):
            return self._bind_call(joint, name, expr)
        if isinstance(expr, Pipe):
            if isinstance(expr.rhs, Call):
                return self._bind_call(joint, name, self._piped_call(expr))
            raise KernelError(
                "PIPE_CALLABLE_ERROR: pipeline right-hand side must be a function call"
            )
        if isinstance(expr, EvolveExpr):
            return self._bind_evolve(joint, [name], expr)
        if isinstance(expr, TensorExpr):
            raise KernelError("tensor product requires tuple bind `(a, b) = left *|* right`")
        raise KernelError(f"cannot bind expr {type(expr).__name__}")

    @staticmethod
    def _piped_call(expr: Pipe) -> Call:
        rhs = expr.rhs
        if not isinstance(rhs, Call):
            raise KernelError(
                "PIPE_CALLABLE_ERROR: pipeline right-hand side must be a function call"
            )
        return Call(callee=rhs.callee, args=[expr.lhs, *rhs.args], span=rhs.span)

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
                amp = w.amp * cmath.sqrt(cp)
                if isinstance(arm_body, Coin):
                    for val, p in ((0, 0.5), (1, 0.5)):
                        out_worlds.append(
                            World(
                                assign={**w.assign, name: val},
                                amp=amp * cmath.sqrt(p),
                                coord_phase=dict(w.coord_phase),
                            )
                        )
                elif isinstance(arm_body, KetLit):
                    # LISS-0138: prepare branching with ket arms (Never Leave
                    # the State — mixture of computational / ± supports).
                    from .quantum_ops import ket_support

                    try:
                        pairs = ket_support(arm_body.label)
                    except ValueError as e:
                        raise KernelError(str(e)) from e
                    for val, kamp in pairs:
                        na = amp * kamp
                        if abs(na) ** 2 > EPS:
                            out_worlds.append(
                                World(
                                    assign={**w.assign, name: val},
                                    amp=na,
                                    coord_phase=dict(w.coord_phase),
                                )
                            )
                else:
                    val = self._eval_value(arm_body, w.assign)
                    out_worlds.append(
                        World(
                            assign={**w.assign, name: val},
                            amp=amp,
                            coord_phase=dict(w.coord_phase),
                        )
                    )
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

    def _expr_qualname(self, expr: Expr) -> str | None:
        """`Topology.ChainLattice` path from Var/Attr chain."""
        if isinstance(expr, Var):
            return expr.name
        if isinstance(expr, Attr):
            base = self._expr_qualname(expr.obj)
            if base is None:
                return None
            return f"{base}.{expr.name}"
        return None

    def _construct_instance(self, class_name: str, expr: Expr) -> ClassInstance:
        cls = self.classes.get(class_name)
        if cls is None:
            raise KernelError(f"unknown class `{class_name}`")
        if not isinstance(expr, Call):
            raise KernelError(
                f"class `{class_name}` instance requires `{cls.qualified_name}(…)`"
            )
        q = self._expr_qualname(expr.callee)
        if q is not None and q not in self.classes:
            raise KernelError(f"unknown constructor `{q}()`")

        init = next((m for m in cls.methods if m.name == "init"), None)
        if expr.args and init is None:
            raise KernelError(
                f"`{cls.qualified_name}(…)` has no `fn init`; "
                f"use defaults or declare `fn init(...)`"
            )
        if init is not None and len(expr.args) != len(init.params):
            raise KernelError(
                f"`{cls.qualified_name}(…)` / `init` expects {len(init.params)} args, "
                f"got {len(expr.args)}"
            )

        fields: dict[str, Any] = {}
        mutable: set[str] = set()
        for fbind in cls.fields:
            if len(fbind.names) != 1:
                raise KernelError("class field must be a single name")
            fields[fbind.names[0]] = self._eval_value(fbind.expr, {})
        for mem in cls.members:
            if mem.default is not None:
                fields[mem.name] = self._eval_value(mem.default, {})
            if mem.mutable:
                mutable.add(mem.name)

        inst = ClassInstance(
            class_name=cls.qualified_name, fields=fields, mutable=mutable
        )
        if init is not None:
            self._run_init(inst, init, list(expr.args))
        else:
            # No init: every member must already have a default
            for mem in cls.members:
                if mem.name not in inst.fields:
                    raise KernelError(
                        f"class `{cls.qualified_name}` member `{mem.name}` needs a "
                        f"default or `fn init`"
                    )
        for mem in cls.members:
            if mem.name not in inst.fields:
                raise KernelError(
                    f"class `{cls.qualified_name}` field `{mem.name}` was not "
                        f"initialized by `fn init`"
                )
        return inst

    def _run_init(
        self, receiver: ClassInstance, init: FunDecl, args: list[Expr]
    ) -> None:
        """Execute `fn init(...)` — may assign `val` fields; no return bind required."""
        prev_this = self._this
        prev_init = self._in_init
        self._this = receiver
        self._in_init = True
        local: dict[str, Any] = dict(receiver.fields)
        try:
            for param, arg in zip(init.params, args):
                if isinstance(arg, Var) and arg.name in self.objects:
                    obj = self.objects[arg.name]
                    local[param.name] = (
                        obj.copy() if isinstance(obj, StructValue) else obj
                    )
                else:
                    v = self._eval_value(arg, {})
                    local[param.name] = (
                        v.copy() if isinstance(v, StructValue) else v
                    )
            for stmt in init.body.stmts:
                if isinstance(stmt, (Measure, Snapshot)):
                    raise KernelError("`measure`/`snapshot` forbidden inside `init`")
                if isinstance(stmt, ReturnStmt):
                    raise KernelError("`init` cannot return a value")
                if isinstance(stmt, AssignStmt):
                    self._exec_assign(stmt, local)
                    local.update(receiver.fields)
                    continue
                if isinstance(stmt, StateBind):
                    if len(stmt.names) != 1:
                        raise KernelError("`init` binds must be single-name")
                    val = self._eval_value(stmt.expr, local)
                    local[stmt.names[0]] = val
                else:
                    raise KernelError(
                        f"unsupported stmt in `init`: {type(stmt).__name__}"
                    )
        finally:
            self._this = prev_this
            self._in_init = prev_init

    def _construct_struct(self, struct_name: str, expr: Expr) -> StructValue:
        st = self.structs.get(struct_name)
        if st is None:
            raise KernelError(f"unknown struct `{struct_name}`")
        if not isinstance(expr, Call):
            raise KernelError(
                f"struct `{struct_name}` requires `{st.qualified_name}(…)`"
            )
        q = self._expr_qualname(expr.callee)
        if q is not None and q not in self.structs:
            raise KernelError(f"unknown struct constructor `{q}()`")
        # Positional args matching field order; or all-defaults
        fields: dict[str, Any] = {}
        if not expr.args:
            for mem in st.fields:
                if mem.default is None:
                    raise KernelError(
                        f"struct `{st.qualified_name}` field `{mem.name}` "
                        f"requires a constructor argument"
                    )
                fields[mem.name] = self._eval_value(mem.default, {})
        else:
            if len(expr.args) != len(st.fields):
                raise KernelError(
                    f"`{st.qualified_name}(…)` expects {len(st.fields)} args, "
                    f"got {len(expr.args)}"
                )
            for mem, arg in zip(st.fields, expr.args):
                fields[mem.name] = self._eval_value(arg, {})
        return StructValue(struct_name=st.qualified_name, fields=fields)

    def _resolve_operator_expr(self, expr: Any) -> Any:
        """Resolve an explicit Operator value/factory without leaking locals."""
        if isinstance(expr, OpVar) and expr.name in self.grid_hamiltonians:
            return GridHamiltonianRef(expr.name)
        if isinstance(expr, Var) and expr.name in self.grid_hamiltonians:
            return GridHamiltonianRef(expr.name)
        if isinstance(expr, OpVar) and expr.name in self.operators:
            return self.operators[expr.name]
        if isinstance(expr, Var) and expr.name in self.operators:
            return self.operators[expr.name]
        if isinstance(expr, Call) and isinstance(expr.callee, Var):
            fun = self.funs.get(expr.callee.name)
            if fun is not None:
                return self._resolve_operator_factory_call(expr, fun)
        # LISS-0139: Operator H = recv.method(…)
        if isinstance(expr, Call) and isinstance(expr.callee, Attr):
            return self._resolve_operator_method_call(expr)
        return expr

    def _resolve_operator_factory_call(self, expr: Call, fun: FunDecl) -> Any:
        """Evaluate a `fn … -> Operator` Call into a materialized OpExpr."""
        local_scalars: dict[str, float] = {}
        local_ops: dict[str, Any] = {}
        if len(expr.args) != len(fun.params):
            raise KernelError(
                f"`{fun.name}` expects {len(fun.params)} args, "
                f"got {len(expr.args)}"
            )
        for param, arg in zip(fun.params, expr.args):
            if param.ty is not None and param.ty.name == "Operator":
                continue
            try:
                local_scalars[param.name] = float(self._eval_value(arg, {}))
            except (KernelError, TypeError, ValueError):
                if isinstance(arg, Var) and arg.name in self.scalars:
                    local_scalars[param.name] = float(self.scalars[arg.name])
        for stmt in fun.body.stmts:
            if not isinstance(stmt, StateBind) or stmt.ty is None:
                continue
            if stmt.ty.name == "Operator" and len(stmt.names) == 1:
                raw = self._resolve_operator_expr(stmt.expr)
                local_ops[stmt.names[0]] = materialize_op_scalar_vars(
                    raw,
                    local_scalars,
                    local_operators=local_ops,
                )
                continue
            if (
                stmt.ty.name
                not in {
                    "State",
                    "Operator",
                    "Delta",
                    "POVM",
                    "DensityState",
                    "QubitRegister",
                }
                and stmt.ty.name not in self.classes
                and stmt.ty.name not in self.structs
                and stmt.ty.name not in self.enums
                and len(stmt.names) == 1
                and self._is_closed(stmt.expr)
            ):
                try:
                    local_scalars[stmt.names[0]] = float(
                        self._eval_value(stmt.expr, {})
                    )
                except (KernelError, TypeError, ValueError):
                    pass
        result = next(
            (stmt.expr for stmt in fun.body.stmts if isinstance(stmt, ReturnStmt)),
            fun.body.result,
        )
        if isinstance(result, (Var, OpVar)) and result.name in local_ops:
            return local_ops[result.name]
        if result is not None and not isinstance(result, (Var, OpVar)):
            return materialize_op_scalar_vars(
                result,
                local_scalars,
                local_operators=local_ops,
            )
        return expr

    def _resolve_operator_method_call(self, expr: Call) -> Any:
        """Evaluate `recv.method(…)` returning Operator (LISS-0139)."""
        callee = expr.callee
        if not isinstance(callee, Attr):
            return expr
        recv_expr = callee.obj
        method_name = callee.name
        if not isinstance(recv_expr, Var) or recv_expr.name not in self.objects:
            raise KernelError(
                f"Operator method call requires a bound receiver "
                f"(got `{type(recv_expr).__name__}`)"
            )
        inst = self.objects[recv_expr.name]
        if not isinstance(inst, ClassInstance):
            raise KernelError(
                f"Operator method `{method_name}` requires a class instance"
            )
        cls = self.classes.get(inst.class_name) or self.classes.get(
            inst.class_name.split(".")[-1]
        )
        if cls is None:
            raise KernelError(f"unknown class `{inst.class_name}`")
        method = next((m for m in cls.methods if m.name == method_name), None)
        if method is None:
            raise KernelError(
                f"class `{inst.class_name}` has no method `{method_name}`"
            )
        if method.return_type is None or method.return_type.name != "Operator":
            raise KernelError(
                f"method `{method_name}` must return Operator for "
                f"`Operator … = recv.{method_name}(…)`"
            )
        # Evaluate method body with `this` = receiver; reuse factory scalar fold.
        prev_this = self._this
        self._this = inst
        try:
            local_scalars: dict[str, float] = {}
            local_ops: dict[str, Any] = {}
            # Seed scalars from instance fields (this.J → Float J pattern).
            for fname, fval in inst.fields.items():
                try:
                    local_scalars[fname] = float(fval)
                except (TypeError, ValueError):
                    pass
            if len(expr.args) != len(method.params):
                raise KernelError(
                    f"`{method_name}` expects {len(method.params)} args, "
                    f"got {len(expr.args)}"
                )
            for param, arg in zip(method.params, expr.args):
                if param.ty is not None and param.ty.name == "Operator":
                    continue
                try:
                    local_scalars[param.name] = float(self._eval_value(arg, {}))
                except (KernelError, TypeError, ValueError):
                    if isinstance(arg, Var) and arg.name in self.scalars:
                        local_scalars[param.name] = float(self.scalars[arg.name])
            for stmt in method.body.stmts:
                if isinstance(stmt, ReturnStmt):
                    continue
                if isinstance(stmt, AssignStmt):
                    self._exec_assign(stmt)
                    local_scalars.update(
                        {
                            k: float(v)
                            for k, v in inst.fields.items()
                            if _is_numeric(v)
                        }
                    )
                    continue
                if not isinstance(stmt, StateBind) or stmt.ty is None:
                    continue
                if stmt.ty.name == "Operator" and len(stmt.names) == 1:
                    raw = stmt.expr
                    # Resolve this.field / local Float into OpLit via scalars.
                    local_ops[stmt.names[0]] = materialize_op_scalar_vars(
                        raw,
                        {**local_scalars, **{
                            k: float(v)
                            for k, v in inst.fields.items()
                            if _is_numeric(v)
                        }},
                        local_operators=local_ops,
                    )
                    continue
                if stmt.ty.name == "Float" and len(stmt.names) == 1:
                    try:
                        local_scalars[stmt.names[0]] = float(
                            self._eval_value(stmt.expr, {})
                        )
                    except (KernelError, TypeError, ValueError):
                        pass
            result = next(
                (
                    stmt.expr
                    for stmt in method.body.stmts
                    if isinstance(stmt, ReturnStmt)
                ),
                method.body.result,
            )
            field_scalars = {
                k: float(v) for k, v in inst.fields.items() if _is_numeric(v)
            }
            merged = {**field_scalars, **local_scalars}
            if isinstance(result, (Var, OpVar)) and result.name in local_ops:
                return materialize_op_scalar_vars(
                    local_ops[result.name], merged, local_operators=local_ops
                )
            if result is not None and not isinstance(result, (Var, OpVar)):
                return materialize_op_scalar_vars(
                    result, merged, local_operators=local_ops
                )
            raise KernelError(
                f"method `{method_name}` did not return an Operator"
            )
        finally:
            self._this = prev_this

    def _bind_second_quantized(self, name: str, family: str, expr: Any) -> None:
        """Bind a typed second-quantized local (LISS-0032, ADR 0093).

        `FermionOperator`/`BosonOperator`/`SpinOperator` locals are kept
        symbolic (no classical value, no numeric mapping yet). A
        `QubitOperator` bind whose expr is `map(op, JordanWigner)` resolves
        the referenced `FermionOperator` through the Jordan-Wigner mapping
        into an ordinary Pauli OpExpr, stored in `self.operators` exactly
        like a hand-written `Operator` bind so `evolve`/`apply` need no
        special-casing downstream.
        """
        if family == "QubitOperator":
            try:
                mapped_expr = resolve_mapping_expr(expr, self.second_quantized_operators)
            except SecondQuantizationMappingError as exc:
                raise KernelError(f"{exc.code}: {exc.message}") from exc
            if mapped_expr is not None:
                self.operators[name] = mapped_expr
                return
        self.second_quantized_operators[name] = expr

    def _exec_assign(self, stmt: AssignStmt, local: dict[str, Any] | None = None) -> None:
        target = stmt.target
        if not isinstance(target, Attr):
            raise KernelError("assignment target must be `obj.field` or `this.field`")
        env = local if local is not None else {}
        val = self._eval_value(stmt.value, env)
        # this.field =
        if isinstance(target.obj, Var) and target.obj.name == "this":
            if self._this is None:
                raise KernelError("`this` is only valid inside a class method")
            if target.name not in self._this.mutable and not self._in_init:
                raise KernelError(
                    f"IMMUTABLE_ASSIGNMENT_ERROR: field `{target.name}` is not "
                    f"`var` (cannot assign through `this`)"
                )
            self._this.fields[target.name] = val
            return
        # obj.field =
        if isinstance(target.obj, Var) and target.obj.name in self.objects:
            obj = self.objects[target.obj.name]
            if isinstance(obj, StructValue):
                raise KernelError(
                    f"IMMUTABLE_ASSIGNMENT_ERROR: struct `{obj.struct_name}` "
                    f"fields are immutable"
                )
            if isinstance(obj, ClassInstance):
                if target.name not in obj.mutable:
                    raise KernelError(
                        f"IMMUTABLE_ASSIGNMENT_ERROR: field `{target.name}` is not "
                        f"`var`"
                    )
                obj.fields[target.name] = val
                return
        raise KernelError("assignment target is not a mutable object field")

    def _bind_method(
        self,
        joint: Joint,
        name: str,
        receiver: ClassInstance,
        method: FunDecl,
        args: list[Expr],
        *,
        logs: list[str] | None = None,
        inspect_out: TextIO | None = None,
    ) -> Joint:
        """Run a measure-free method and bind its result.

        New signatures return the explicit terminal `return` expression.
        """
        if method.name == "init":
            raise KernelError("`init` is a constructor; call `ClassName(…)` instead")
        if len(args) != len(method.params):
            raise KernelError(
                f"`{method.name}` expects {len(method.params)} args, got {len(args)}"
            )
        prev_this = self._this
        self._this = receiver
        # Local classical env for params + this fields
        local: dict[str, Any] = dict(receiver.fields)
        for param, arg in zip(method.params, args):
            if isinstance(arg, Var) and arg.name in self.objects:
                obj = self.objects[arg.name]
                # struct: copy-on-pass; class: reference
                if isinstance(obj, StructValue):
                    local[param.name] = obj.copy()
                else:
                    local[param.name] = obj
            else:
                v = self._eval_value(arg, {})
                if isinstance(v, StructValue):
                    local[param.name] = v.copy()
                else:
                    local[param.name] = v

        last_val: Any = None
        result_joint: Joint | None = None
        try:
            for stmt in method.body.stmts:
                if isinstance(stmt, Measure):
                    raise KernelError(
                        f"`measure` forbidden inside method `{method.name}`"
                    )
                if isinstance(stmt, Snapshot):
                    raise KernelError(
                        f"`snapshot` forbidden inside method `{method.name}`"
                    )
                if isinstance(stmt, ReturnStmt):
                    continue
                if isinstance(stmt, AssignStmt):
                    self._exec_assign(stmt, local)
                    # Reflect this.fields into local for subsequent reads of bare names
                    local.update(receiver.fields)
                    continue
                if isinstance(stmt, StateBind):
                    if stmt.ty is not None and stmt.ty.name == "Operator":
                        if len(stmt.names) != 1:
                            raise KernelError("Operator bind expects a single name")
                        self.operators[stmt.names[0]] = stmt.expr
                        continue
                    # Evaluate RHS with this/local; bind into local (classical methods)
                    if len(stmt.names) != 1:
                        raise KernelError(
                            f"method `{method.name}` binds must be single-name"
                        )
                    # Prefer classical eval of method bodies (physics helpers)
                    try:
                        val = self._eval_value(stmt.expr, local)
                        local[stmt.names[0]] = val
                        last_val = val
                        if (
                            stmt.ty is not None
                            and stmt.ty.name not in {"State", "Operator", "Delta"}
                        ):
                            try:
                                self.scalars[stmt.names[0]] = float(val)
                            except (TypeError, ValueError):
                                pass
                    except KernelError:
                        # Quantum bind path (rare in methods)
                        joint = self._bind_names(
                            joint,
                            stmt.names,
                            stmt.expr,
                            logs=logs,
                            inspect_out=inspect_out,
                        )
                        last_val = None
                else:
                    raise KernelError(
                        f"unsupported stmt in method `{method.name}`: "
                        f"{type(stmt).__name__}"
                    )
            if method.body.result is not None:
                try:
                    # Methods such as `advance()` return a classical field
                    # projection after updating the receiver.  Resolve that
                    # expression in the method-local environment first;
                    # quantum expressions still use the Joint binder.
                    value = self._eval_value(method.body.result, local)
                    result_joint = joint.bind_const(name, value)
                except KernelError:
                    result_joint = self._bind(
                        joint,
                        name,
                        method.body.result,
                        logs=logs,
                        inspect_out=inspect_out,
                    )
        finally:
            self._this = prev_this

        if result_joint is not None:
            return result_joint

        if method.body.result is None:
            raise KernelError(
                f"method `{method.name}` has no explicit return"
            )
        if last_val is None:
            return self._bind(
                joint,
                name,
                method.body.result,
                logs=logs,
                inspect_out=inspect_out,
            )
        return joint.bind_const(name, last_val)

    def _bind_user_fun(
        self,
        joint: Joint,
        names: list[str],
        expr: Call,
        fun: FunDecl,
        *,
        logs: list[str] | None = None,
        inspect_out: TextIO | None = None,
    ) -> Joint:
        """Execute a measure-free library `fn` and bind results to `names`."""
        if len(expr.args) != len(fun.params):
            raise KernelError(
                f"`{fun.name}` expects {len(fun.params)} args, got {len(expr.args)}"
            )
        saved_operators = dict(self.operators)
        # Bind arguments onto parameter coordinates
        for param, arg in zip(fun.params, expr.args):
            if param.ty is not None and param.ty.name == "Operator":
                self.operators[param.name] = self._resolve_operator_expr(arg)
                continue
            if isinstance(arg, Var) and arg.name == param.name:
                continue
            if isinstance(arg, Var):
                src = arg.name
                joint = joint.bind_pushforward(
                    param.name, lambda a, s=src: a[s]
                )
            else:
                joint = joint.bind_pushforward(
                    param.name, lambda a, e=arg: self._eval_value(e, a)
                )

        for stmt in fun.body.stmts:
            if isinstance(stmt, Measure):
                raise KernelError(
                f"`measure` is forbidden inside library fn `{fun.name}` "
                    "(measure-free module boundary)"
                )
            if isinstance(stmt, Snapshot):
                raise KernelError(
                    f"`snapshot` is forbidden inside library fn `{fun.name}`"
                )
            if isinstance(stmt, ReturnStmt):
                continue
            if isinstance(stmt, StateBind):
                if stmt.ty is not None and stmt.ty.name == "Operator":
                    if len(stmt.names) != 1:
                        raise KernelError("Operator bind expects a single name")
                    self.operators[stmt.names[0]] = stmt.expr
                    continue
                joint = self._bind_names(
                    joint,
                    stmt.names,
                    stmt.expr,
                    logs=logs,
                    inspect_out=inspect_out,
                )
            else:
                raise KernelError(
                    f"unsupported stmt in fn `{fun.name}`: {type(stmt).__name__}"
                )

        if fun.body.result is not None:
            if len(names) == 0:
                # A result with no destination is still evaluated for its
                # state-preserving transform, but has no visible coordinate.
                self.operators = saved_operators
                return joint
            result_joint = self._bind_names(
                joint,
                names,
                fun.body.result,
                logs=logs,
                inspect_out=inspect_out,
            )
            if "Uncompute" in fun.effects:
                for n in names:
                    self._require_uncompute_zero(result_joint, n)
            self.operators = saved_operators
            return result_joint

        # Legacy state-transformer path: project parameter coordinates into
        # the caller's bind names when no explicit result expression exists.
        if len(names) == 0:
            self.operators = saved_operators
            return joint
        if len(names) == len(fun.params):
            updates = {
                n: (lambda a, p=p.name: a[p])
                for n, p in zip(names, fun.params)
            }
            result_joint = joint.bind_multi(updates)
            self.operators = saved_operators
            return result_joint
        if len(names) == 1 and len(fun.params) == 1:
            p = fun.params[0].name
            result_joint = joint.bind_pushforward(names[0], lambda a, pn=p: a[pn])
            self.operators = saved_operators
            return result_joint
        raise KernelError(
            f"`{fun.name}` result arity {len(fun.params)} != bind arity {len(names)}"
        )

    def _bind_call(self, joint: Joint, name: str, expr: Call) -> Joint:
        callee = expr.callee

        # ADR 0056: instance.method(args)
        if isinstance(callee, Attr):
            recv_expr = callee.obj
            method_name = callee.name
            q = self._expr_qualname(callee)
            if q is not None and q in self.funs:
                return self._bind_user_fun(joint, [name], expr, self.funs[q])
            if q is not None and q in self.classes:
                raise KernelError(
                    f"construct `{q}()` via Type-First "
                    f"`{q} obj = {q}()`, not as a State expression"
                )
            if isinstance(recv_expr, Var) and recv_expr.name in self.objects:
                inst = self.objects[recv_expr.name]
                if isinstance(inst, ClassInstance):
                    cls = self.classes.get(inst.class_name) or self.classes.get(
                        inst.class_name.split(".")[-1]
                    )
                    if cls is None:
                        raise KernelError(f"unknown class `{inst.class_name}`")
                    method = next(
                        (m for m in cls.methods if m.name == method_name), None
                    )
                    if method is None:
                        raise KernelError(
                            f"class `{inst.class_name}` has no method `{method_name}`"
                        )
                    return self._bind_method(
                        joint, name, inst, method, list(expr.args)
                    )
                if isinstance(inst, StructValue):
                    raise KernelError(
                        f"struct `{inst.struct_name}` has no methods "
                        f"(use class for methods)"
                    )
            # Fall through to Math.* / map / etc.

        # User-module fn (ADR 0054)
        if isinstance(callee, Var) and callee.name in self.funs:
            return self._bind_user_fun(joint, [name], expr, self.funs[callee.name])

        # Math.sin(x) / Math.cos(x) / …
        if isinstance(callee, Attr):
            if isinstance(callee.obj, Var) and callee.obj.name == "Complex":
                if callee.name == "cis":
                    if len(expr.args) != 1:
                        raise KernelError("Complex.cis requires (theta)")
                    theta = float(self._eval_value(expr.args[0], {}))
                    from .joint import World

                    return Joint(
                        worlds=[World(assign={name: 0}, amp=cmath.exp(1j * theta))]
                    )
                raise KernelError(f"unknown Complex.{callee.name}")
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
            # x.map(fn) — project is not a method (Hilbert project(state, k) only)
            if isinstance(callee.obj, Var) and callee.name == "map":
                src_expr = callee.obj
                if len(expr.args) < 1:
                    raise KernelError("map requires a lambda")
                f = self._as_unary_fn(expr.args[0])
                return joint.map_coord(src_expr.name, name, f)
            if isinstance(callee.obj, Var) and callee.name == "project":
                raise KernelError(
                    "use project(state, k) for Hilbert |k⟩⟨k|; "
                    "method form state.project(pred) is removed"
                )
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
            # Hilbert projector P̂ = |k⟩⟨k| on a wire (Lüders), then renorm.
            # Predicate filters are forbidden (classical programming smell).
            if len(expr.args) < 2:
                raise KernelError(
                    "project requires (state, basisLabel) — Hilbert |k⟩⟨k|, "
                    "not a predicate lambda"
                )
            src_expr, target = expr.args[0], expr.args[1]
            if not isinstance(src_expr, Var):
                raise KernelError("project src must be a state variable")
            if isinstance(target, Lambda):
                raise KernelError(
                    "PREDICATE_PROJECTOR_ERROR: `project` is the Hilbert "
                    "projector |k⟩⟨k|, not a classical filter. "
                    "Write project(psi, 0) or project(psi, |0>)."
                )
            if isinstance(target, KetLit):
                bits = target.label
                if bits in {"0", "1"}:
                    label: Any = int(bits)
                elif set(bits) <= {"0", "1"} and bits != "":
                    label = int(bits, 2)
                else:
                    raise KernelError(
                        f"project onto |{bits}⟩: MVP supports "
                        "computational |0⟩/|1⟩ (and bitstrings) only"
                    )
            else:
                label = self._eval_value(target, {})
            projected = joint.project_coord(src_expr.name, lambda v, lab=label: v == lab)
            if projected.is_vacuum():
                return Joint.empty()
            # Renormalize after Lüders projection
            from .joint import World, _coalesce

            total = sum(abs(w.amp) ** 2 for w in projected.worlds)
            if total <= EPS:
                return Joint.empty()
            scale = 1.0 / cmath.sqrt(total)
            out = [
                World(
                    assign=dict(w.assign),
                    amp=w.amp * scale,
                    coord_phase=dict(w.coord_phase),
                )
                for w in projected.worlds
            ]
            return Joint(worlds=_coalesce(out)).bind_pushforward(
                name, lambda a: a[src_expr.name]
            )

        if op == "interfer":
            if not expr.args:
                return Joint.empty()
            from .joint import World, _coalesce

            # Sum complex amplitudes per result value (path interference).
            from collections import defaultdict

            amps: dict[Any, complex] = defaultdict(complex)
            for arg in expr.args:
                if isinstance(arg, Var):
                    for val, c in joint.amplitude_marginal(arg.name).items():
                        amps[val] += c
                elif isinstance(arg, (LitInt, LitFloat, LitBool)):
                    amps[self._lit(arg)] += complex(1.0, 0.0)
                else:
                    for w in joint.worlds:
                        val = self._eval_value(arg, w.assign)
                        amps[val] += w.amp
            # Drop cancelled bins; renormalize Born measure (SV-07 mixture).
            alive = {v: c for v, c in amps.items() if abs(c) ** 2 > EPS}
            if not alive:
                return Joint.empty()
            total = sum(abs(c) ** 2 for c in alive.values())
            scale = 1.0 / cmath.sqrt(total)
            out = [
                World(assign={name: val}, amp=c * scale) for val, c in alive.items()
            ]
            return Joint(worlds=_coalesce(out))

        if op == "phase":
            # phase(src, theta) or phase(src, theta, only_value)
            # ADR 0060: θ / only resolve against scalars ∪ objects ∪ assign
            if len(expr.args) < 2 or not isinstance(expr.args[0], Var):
                raise KernelError("phase requires (src, theta[, only])")
            src = expr.args[0].name
            theta = float(self._eval_value(expr.args[1], {}))
            only = None
            if len(expr.args) >= 3:
                only = self._eval_value(expr.args[2], {})
            return joint.phase_copy(src, name, theta, only=only)

        if op in {"grover_diffuse", "diffuse"}:
            # grover_diffuse(src) — Grover inversion about mean
            if len(expr.args) != 1 or not isinstance(expr.args[0], Var):
                raise KernelError("grover_diffuse requires (src)")
            return joint.diffuse_copy(expr.args[0].name, name)

        if op == "cis":
            # cis(theta): unit |0⟩ with amplitude e^{iθ}
            if len(expr.args) != 1:
                raise KernelError("cis requires (theta)")
            theta = float(self._eval_value(expr.args[0], {}))
            from .joint import World

            return Joint(worlds=[World(assign={name: 0}, amp=cmath.exp(1j * theta))])

        if op == "cnot":
            # cnot(ctrl, tgt) — unitary |c,t⟩↦|c,t⊕c⟩; bind result as new tgt wire
            if len(expr.args) != 2:
                raise KernelError("cnot requires (ctrl, tgt)")
            if not isinstance(expr.args[0], Var) or not isinstance(expr.args[1], Var):
                raise KernelError("cnot args must be state variables")
            from .quantum_ops import cnot_bit

            ctrl_n = expr.args[0].name
            tgt_n = expr.args[1].name
            return joint.bind_pushforward(
                name, lambda a: cnot_bit(a[ctrl_n], a[tgt_n])
            )

        if op == "apply":
            # apply(U, w0[, w1, …]) — unitary on wires (H⊗I…); U = Operator | Hadamard | Pauli
            return self._bind_apply(joint, name, expr)

        if op == "capply":
            # capply(ctrl[, …], U, tgt[, …]) — Cⁿ(U) on |1…1⟩
            return self._bind_capply(joint, name, expr)

        if op == "ocapply":
            # ocapply(ctrl[, …], U, tgt[, …]) — all open (|0⟩) controls
            return self._bind_capply(
                joint, name, expr, force_all_open=True, op_label="ocapply"
            )

        if op == "toffoli":
            # toffoli(c0, c1, tgt) — sugar for capply(c0, c1, X, tgt)
            if len(expr.args) != 3:
                raise KernelError("toffoli requires (ctrl0, ctrl1, tgt)")
            if not all(isinstance(a, Var) for a in expr.args):
                raise KernelError("toffoli args must be state variables")
            sp = expr.span
            synthetic = Call(
                callee=Var(name="capply", span=sp),
                args=[
                    expr.args[0],
                    expr.args[1],
                    Var(name="X", span=sp),
                    expr.args[2],
                ],
                span=sp,
            )
            return self._bind_capply(joint, name, synthetic)

        if op == "hadamard":
            # hadamard(w) — sugar for apply(Hadamard, w)
            if len(expr.args) != 1 or not isinstance(expr.args[0], Var):
                raise KernelError("hadamard requires (wire)")
            from .unitaries import apply_unitary_on_wires, hadamard

            wire = expr.args[0].name
            try:
                updated = apply_unitary_on_wires(joint, [wire], hadamard())
            except ValueError as e:
                raise KernelError(str(e)) from e
            if name == wire:
                return updated
            return updated.bind_pushforward(name, lambda a, w=wire: a[w])

        if op in {"walk_shift", "shift"}:
            # walk_shift(coin, pos) — DTQW conditional translation
            if len(expr.args) != 2:
                raise KernelError("walk_shift requires (coin, pos)")
            if not isinstance(expr.args[0], Var) or not isinstance(expr.args[1], Var):
                raise KernelError("walk_shift args must be state variables")
            from .unitaries import shift_position

            coin_n = expr.args[0].name
            pos_n = expr.args[1].name
            return joint.bind_pushforward(
                name, lambda a: shift_position(a[coin_n], a[pos_n])
            )

        if op == "tensor":
            raise KernelError("use `(a, b) = left *|* right`")

        if op == "trace_out":
            # trace_out(coord) — partial trace / discard subsystem coordinate
            if len(expr.args) != 1 or not isinstance(expr.args[0], Var):
                raise KernelError("trace_out requires (coordVar)")
            coord = expr.args[0].name
            trimmed = joint.trace_out(coord)
            # Placeholder classical bind; remaining coordinates stay measurable
            return trimmed.bind_const(name, 0)

        if op == "expect":
            # expect(O, psi) — single-qubit ⟨P⟩
            # expect(ZZ, a, b) — two-qubit ⟨Z⊗Z⟩ (Bell correlation; no collapse)
            from .quantum_ops import expect_pauli, expect_zz

            if len(expr.args) == 2 and isinstance(expr.args[1], Var):
                op_name = self._operator_name(expr.args[0])
                if op_name.upper() == "ZZ":
                    raise KernelError("expect(ZZ, …) requires two qubit variables")
                src = expr.args[1].name
                amps = joint.amplitude_marginal(src)
                a0 = amps.get(0, 0j)
                a1 = amps.get(1, 0j)
                try:
                    val = expect_pauli(op_name, a0, a1)
                except ValueError as e:
                    raise KernelError(str(e)) from e
                # Non-destructive: bind scalar onto existing joint worlds
                return joint.bind_const(name, float(val))
            if (
                len(expr.args) == 3
                and isinstance(expr.args[1], Var)
                and isinstance(expr.args[2], Var)
            ):
                op_name = self._operator_name(expr.args[0])
                if op_name.upper() != "ZZ":
                    raise KernelError(
                        f"two-qubit expect supports ZZ only, got `{op_name}`"
                    )
                try:
                    val = expect_zz(
                        joint.worlds, expr.args[1].name, expr.args[2].name
                    )
                except ValueError as e:
                    raise KernelError(str(e)) from e
                return joint.bind_const(name, float(val))
            raise KernelError(
                "expect requires (operator, stateVar) or (ZZ, qubitA, qubitB)"
            )

        if op == "occupation":
            # occupation(psi, k) — Born weight |⟨k|ψ⟩|² on Int site / Fock label
            if len(expr.args) != 2 or not isinstance(expr.args[0], Var):
                raise KernelError("occupation requires (stateVar, siteIndex)")
            src = expr.args[0].name
            k = self._eval_value(expr.args[1], {})
            if not isinstance(k, int):
                try:
                    k = int(k)
                except (TypeError, ValueError) as e:
                    raise KernelError("occupation site index must be Int") from e
            amps = joint.amplitude_marginal(src)
            val = float(abs(amps.get(k, 0j)) ** 2)
            return joint.bind_const(name, val)

        if op == "coin":
            return joint.bind_split(name, {0: 0.5, 1: 0.5})
        if op == "vacuum":
            # vacuum() = |0⟩ (Fock / computational ground), NOT empty support
            return joint.bind_pushforward(name, lambda a: 0)
        if op == "empty":
            # empty support (destructive interference / null joint)
            return Joint.empty()
        if op == "dirac":
            if not expr.args:
                raise KernelError("dirac requires an argument (point mass δ_c)")
            return joint.bind_pushforward(name, lambda a: self._eval_value(expr.args[0], a))
        if op == "wavepacket":
            # wavepacket(xmin, xmax, n, x0, sigma) — Gaussian on a uniform grid
            if len(expr.args) != 5:
                raise KernelError(
                    "wavepacket requires (xmin, xmax, n, x0, sigma)"
                )
            xmin = float(self._eval_value(expr.args[0], {}))
            xmax = float(self._eval_value(expr.args[1], {}))
            n_raw = self._eval_value(expr.args[2], {})
            if type(n_raw) is not int:
                raise KernelError("wavepacket n must be Int")
            n = n_raw
            x0 = float(self._eval_value(expr.args[3], {}))
            sigma = float(self._eval_value(expr.args[4], {}))
            if n < 2:
                raise KernelError("wavepacket needs n >= 2")
            if sigma <= 0:
                raise KernelError("wavepacket sigma must be positive")
            if xmax <= xmin:
                raise KernelError("wavepacket requires xmax > xmin")
            dx = (xmax - xmin) / float(n)
            xs = [xmin + i * dx for i in range(n)]
            # ψ ∝ exp(-(x-x0)²/(4σ²)) so |ψ|² has std σ
            import math as _math

            raw = [
                _math.exp(-((x - x0) ** 2) / (4.0 * sigma * sigma)) for x in xs
            ]
            norm2 = sum(a * a for a in raw)
            if norm2 <= EPS:
                raise KernelError("wavepacket amplitudes vanished")
            dist = {xs[i]: (raw[i] * raw[i]) / norm2 for i in range(n)}
            return joint.bind_split(name, dist)
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

    def _maybe_capture_classical_scalar(self, joint: Joint, name: str) -> None:
        """Promote a deterministic classical Joint coordinate into scalars.

        Used when Type-First `Float x = …` was bound via a method Call (not
        `_is_closed`), so `evolve … for x` and Operator OpVars can resolve it
        (LISS-0137).
        """
        if name in self.scalars:
            return
        try:
            marg = joint.marginal(name)
        except Exception:
            return
        if len(marg) != 1:
            return
        raw = next(iter(marg))
        try:
            self.scalars[name] = float(raw)
        except (TypeError, ValueError):
            pass

    def _is_closed(self, expr: Expr) -> bool:
        if isinstance(expr, (LitInt, LitFloat, LitBool, LitString)):
            return True
        if isinstance(expr, Var):
            # Prelude / already-bound classical scalars (ADR 0062)
            return expr.name in self.scalars
        if isinstance(expr, Attr):
            if (
                isinstance(expr.obj, Var)
                and expr.obj.name == "Math"
                and expr.name in {"pi", "sqrt2", "inv_sqrt2"}
            ):
                return True
            # Struct / class field projections are classical once the object exists
            # (LISS-0137: Float J = c.J → Operator coeffs).
            if isinstance(expr.obj, Var) and expr.obj.name in self.objects:
                return True
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
            if expr.name in assign:
                return assign[expr.name]
            # ADR 0060: classical Type-First scalars (Float cfg = …)
            if expr.name in self.scalars:
                return self.scalars[expr.name]
            raise KernelError(f"unbound variable `{expr.name}`")
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
        if isinstance(expr, Attr):
            # Unit suffix is compile-time only: 1.0.kg → 1.0 at runtime
            from ..dimensions import UNIT_TABLE

            if isinstance(expr.obj, (LitInt, LitFloat)) and expr.name in UNIT_TABLE:
                return float(expr.obj.value)
            # ADR 0062: Math.<const> ≡ prelude classical constants
            if (
                isinstance(expr.obj, Var)
                and expr.obj.name == "Math"
                and expr.name in {"pi", "sqrt2", "inv_sqrt2"}
            ):
                from ..stdlib.prelude import PRELUDE_CONSTANTS

                return PRELUDE_CONSTANTS[expr.name]
            # Enum.Variant (incl. Namespace.Enum.Variant)
            eq = self._expr_qualname(expr.obj)
            if eq is not None and eq in self.enums:
                ed = self.enums[eq]
                if expr.name not in ed.variants:
                    raise KernelError(
                        f"enum `{ed.qualified_name}` has no variant `{expr.name}`"
                    )
                return EnumValue(enum_name=ed.qualified_name, variant=expr.name)
            # ADR 0056: this.field
            if isinstance(expr.obj, Var) and expr.obj.name == "this":
                if self._this is None:
                    raise KernelError("`this` is only valid inside a class method")
                if expr.name not in self._this.fields:
                    raise KernelError(
                        f"class `{self._this.class_name}` has no field `{expr.name}`"
                    )
                return self._this.fields[expr.name]
            # instance.field (classical object field read)
            if isinstance(expr.obj, Var) and expr.obj.name in self.objects:
                inst = self.objects[expr.obj.name]
                if isinstance(inst, (ClassInstance, StructValue)):
                    fields = inst.fields
                    cname = (
                        inst.class_name
                        if isinstance(inst, ClassInstance)
                        else inst.struct_name
                    )
                    if expr.name not in fields:
                        raise KernelError(f"`{cname}` has no field `{expr.name}`")
                    return fields[expr.name]
                if isinstance(inst, EnumValue):
                    raise KernelError("enum values have no fields")
            obj = self._eval_value(expr.obj, assign)
            if isinstance(obj, (ClassInstance, StructValue)):
                fields = obj.fields
                cname = (
                    obj.class_name if isinstance(obj, ClassInstance) else obj.struct_name
                )
                if expr.name not in fields:
                    raise KernelError(f"`{cname}` has no field `{expr.name}`")
                return fields[expr.name]
            if isinstance(obj, EnumValue):
                raise KernelError("enum values have no fields")
            raise KernelError(f"cannot evaluate attribute `.{expr.name}` on {obj!r}")
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
            q = self._expr_qualname(expr.callee)
            if q is not None and q in self.structs:
                return self._construct_struct(q, expr)
            if q is not None and q in self.classes:
                return self._construct_instance(q, expr)
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
            acc[v] += abs(w.amp) ** 2
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
            # File sink: write via staqex.io helper
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


def _is_numeric(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


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


def _call_name(expr: Call) -> str | None:
    return expr.callee.name if isinstance(expr.callee, Var) else None


def _density_matrix_n_qubits(matrix: Matrix) -> int:
    """Qubit count implied by a density matrix's own dimension (LISS-0011):
    the DensityState type parameter, e.g. `Qubit`, is a domain label only
    and never encodes a qubit count -- the constructed matrix is the only
    source of truth."""
    return max(len(matrix), 2).bit_length() - 1


def _pat_match(pat: Any, ctrl: Any) -> bool:
    if pat == ctrl:
        return True
    if isinstance(pat, (int, float)) and isinstance(ctrl, (int, float)):
        return float(pat) == float(ctrl)
    return False
