# ADR 0069: Static Hilbert Kernel

## Status

**Accepted — revised** (2026-07-23). This revision supersedes the surface
wording of the bounded `register(N)` implementation slice from LISS-0026. It
does not authorize the follow-up migration or the Parametric/Dynamic lanes.

Companions: [LISS-0029](../../issues/LISS-0029-static-hilbert-kernel-surface.md),
[ADR 0070](0070-parametric-circuit.md), [ADR 0071](0071-dynamic-qpu-lane.md),
[static Hilbert specification](../../specs/qpex-static-hilbert-kernel.md).

## Context

For a theory-oriented user, a qubit is a degree of freedom of the physical
system, not a resource created by a runtime function call. A register size
fixes the tensor-product space before execution:

\[
\mathcal{H}_2^{\otimes N} \cong \mathbb{C}^{2^N}.
\]

The earlier `register(N)` spelling is useful as an implementation fixture but
looks like a runtime classical function call. It obscures that `N` is part of
the system's static shape and can suggest that the QPU allocates wires during
Kernel execution.

QPex must also retain its core ontology: `State<T>` is the pre-measurement
joint quantum/probabilistic state, while `T` becomes observable outside the
Kernel only after terminal `measure`.

## Decision

1. **Static system shape is type-level.** The normative surface is
   `QubitRegister<N>`, where `N` is compile-time metadata describing the
   logical tensor factors. It is not a runtime `Int` and does not participate
   in `State<T>` arithmetic.

   ```qpex
   QubitRegister<3> reg
   ```

   Exact declaration/initialization syntax is tracked by LISS-0029.
2. **`State<T>` remains the pre-measurement value model.**
   `QubitRegister<N>` describes the available degrees of freedom; a state
   evolves over those degrees of freedom and is observed only by terminal
   `measure`. This ADR does not introduce `StateVector<N>` as the public state
   representation, leaving room for density-matrix/CPTP work under ADR 0057.
3. **`forEach` is static tensor-factor elaboration.** The loop variable is an
   opaque element handle. The compiler expands a finite body over the
   register's logical factors before QPU IR/OpenQASM emission.

   ```qpex
   forEach q in reg {
       apply(H, q)
   }
   ```

   The construct is not a runtime loop, does not expose an index, and cannot
   change the Hilbert-space shape.
4. **Static resource checks are mandatory.** The compiler/transpiler must
   reject unsupported logical qubit count, ancilla count, generated operation
   count, or target-profile limits. It must never silently truncate a
   register or partially emit a circuit. Circuit depth and coherence budget
   may be a target-profile hard error or warning according to explicit profile
   policy; they are not silently ignored.
5. **Classical scalar types are lane-scoped, not globally deleted.** `Int`,
   `Float`, and `Bool` remain valid carriers such as `State<Int>` and remain
   available to Host APIs. They are not ordinary runtime control values in the
   Static Hilbert Kernel.
6. **Parametric and dynamic behavior are separate decisions.** `Param<T>` is
   defined by ADR 0070; mid-circuit measurement/feed-forward is defined by
   ADR 0071. Neither is implicitly part of `forEach`.

## Rejected alternatives

- `register(N)` as the normative physical-system declaration: rejected as a
  final surface because it resembles runtime allocation. It remains a
  historical implementation fixture until LISS-0029 replaces it.
- `StateVector<N>` as the public state type: rejected because it prematurely
  commits the language to one representation and conflicts with future mixed
  states.
- Exposing `Int i` for register elements: rejected; tensor-factor identity is
  structural, not a user-visible classical computation.
- Allowing measurement-dependent shape changes: rejected; this belongs to the
  separately specified Dynamic QPU lane.

## Consequences

Positive:

- Source matches the physicist's static tensor-product mental model.
- Logical degrees of freedom are separated from Host values and provider
  allocation details.
- Static expansion remains compatible with OpenQASM and Job submission.
- Future density matrices, symbolic parameters, and dynamic circuits have
  explicit extension points without changing the Core meaning.

Negative / deferred:

- A type-level declaration/initialization syntax and generic-bound rules are
  still required.
- Resource profile data and post-routing checks need a QPU IR/backend issue.
- Existing `register(N)` examples require deliberate migration; no implicit
  compatibility alias is promised.

## Verification direction

- LISS-0029: static type surface and migration from the bounded fixture.
- LISS-0027: symbolic parameter boundary and gate-argument checks.
- LISS-0028: dynamic-circuit semantics and capability profiles.
- Existing terminal-measure, CPU, QASM, and Job boundary tests remain green.
