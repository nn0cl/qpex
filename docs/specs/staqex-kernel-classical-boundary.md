# Staqex Kernel classical boundary and static `forEach` (historical slice)

| Field | Value |
|---|---|
| Status | **Accepted bounded implementation slice; superseded as the final type surface** (2026-07-23) |
| Issue | [LISS-0026](../issues/LISS-0026-kernel-classical-boundary-and-static-foreach.md) |
| Decision | [ADR 0069](../architecture/adr/0069-kernel-static-hilbert-space.md) |
| Scope | QPU-targeted Kernel surface; Host API is outside the language |

This document is a reviewable contract. It is not an implementation guide and
does not authorize a parser, runtime, or provider change.

The bounded `register(N)` fixture described here is historical and is rejected
as a compatibility alias. The normative surface is
[`staqex-static-hilbert-kernel.md`](staqex-static-hilbert-kernel.md) with
`QubitRegister<N>`; the MVP migration/resource boundary is complete under
LISS-0029.

## 1. Terms

- **Kernel lane:** source that is eligible for circuit/QPU lowering.
- **Host lane:** code using the Python/Rust Host API to prepare, submit, and
  retrieve a Job.
- **Static collection:** a register, wire set, or domain whose membership is
  fixed before circuit emission/submission.
- **Element handle:** an opaque value naming one member of a static collection;
  it is not an `Int` index exposed to Kernel arithmetic.
- **Elaboration:** deterministic expansion of a static `forEach` into a finite
  sequence of Kernel operations before backend emission.

## 2. Normative rules

1. QPU Kernel code MUST NOT use ordinary runtime `Int`, `Float`, or `Bool`
   values as general-purpose loop/control state.
2. `Host<T>` MUST remain outside the Kernel value/state model. Passing host data
   into a Job is an explicit Host API operation; it is not an implicit source
   variable in the submitted Kernel.
3. A valid `forEach` MUST identify a statically known finite collection.
4. The loop variable MUST be an element handle. Kernel arithmetic MUST NOT
   inspect, increment, compare, or convert it to a classical scalar.
5. The body MUST be elaborated once per collection member in deterministic
   collection order. The body MUST NOT perform `measure` or alter collection
   membership.
6. Bounds or membership depending on a measurement, an unbounded source, or a
   runtime provider result MUST be rejected before submission.
7. A backend MUST either emit the elaborated operations or report an explicit
   unsupported-feature diagnostic. It MUST NOT silently run the iteration on
   the host while presenting it as QPU execution.

## 3. Canonical example

```staqex
pub fn apply_hadamards() -> Unit {
    QubitRegister<3> register = system()
    forEach q in register {
        apply(H, q)
    }
}
```

The semantic point is that `q` is a wire handle and the emitted circuit
contains one `H` operation for each statically known wire. Target-specific
resource profiles remain a later QPU IR concern.

## 4. Invalid examples

```staqex
(* Invalid: measurement controls circuit construction. *)
forEach q in register(measure n) { apply(H, q) }
```

```staqex
(* Invalid: the Kernel loop variable is exposed as classical arithmetic. *)
forEach q in register {
    Int i = index(q)
    apply(Rz(i), q)
}
```

```staqex
(* Invalid: unbounded host-style iteration is not Kernel syntax. *)
while (has_more_wires()) { apply(H, next_wire()) }
```

The static surface diagnostic is `STATIC_HILBERT_SURFACE_ERROR`; measurement
dependent bounds remain `FOR_EACH_DYNAMIC_BOUND_ERROR`.

## 5. Boundary sequence

```text
Host input / static shape
        -> Kernel elaboration (`forEach`)
        -> OpenQASM/QPU IR
        -> Job submission adapter
        -> JobResult / terminal measurement
```

Only the first and last nodes are Host concerns. The middle two do not expose
provider scheduling or host loop execution to the Staqex program.

## 6. Open decisions

- whether QPU parameters get a dedicated type distinct from `Host<T>`;
- target-specific expansion/resource profiles beyond the MVP 1024 logical-qubit
  safety budget;
- dynamic-circuit support and classical feed-forward;
- concrete QPU IR and provider capability negotiation.
