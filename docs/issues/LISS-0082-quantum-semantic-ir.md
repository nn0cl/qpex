# LISS-0082: Quantum Semantic IR

## Metadata

- Local issue ID: LISS-0082
- Status: **plan intake** — Slice A Phase 1 Red gated
- Phase: Architecture / Feature Path plan intake
- Type: semantic IR / quantum domain
- Priority: P0
- Initial planning size: XL
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md) E2 — Semantic IR
- Depends on: [LISS-0075](LISS-0075-linear-quantum-usage.md) **complete**;
  [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md) **complete**
- Unlocks: [LISS-0083](../work-plans/WP-0025-staqex-v1-north-star.md) Algorithm
  Plan IR; [LISS-0077](../work-plans/WP-0025-staqex-v1-north-star.md) Dynamic QPU
  (also needs 0076 **complete**)
- Related branch: `docs/liss-0082-plan-intake` → later `feature/liss-0082-*`
- Authority: [ADR 0106](../architecture/adr/0106-staqex-v1-north-star-language-and-compiler.md)
  D9 / D11; [compiler blueprint §4.3](../architecture/staqex-v1-compiler-blueprint.md);
  [v1 language north star](../specs/staqex-v1-language-north-star.md)
- Plan companion:
  [`staqex-v1-quantum-semantic-ir-plan.md`](../specs/staqex-v1-quantum-semantic-ir-plan.md)

## Summary

Introduce a provider-neutral **Quantum Semantic IR** on the Python Shipping
Kernel. This IR captures **executable finite quantum semantics** after Physics
IR: finite acting spaces, pure/mixed transformations, unitary/channel/measurement
regions, static and dynamic control markers, parameter symbols, linear/ancilla
lifetime markers, and exact-versus-approximate markers.

Simulator planning and QPU planning must consume the **same** semantic contract.
No target/provider types appear in this IR. The first implementation is
additive: a new module adjacent to Physics IR, not a big-bang rewrite of the
evaluator or pipeline.

## Acceptance scenarios

1. **Given** a reviewed Physics IR / Kernel contract with finite acting-space
   intent, **when** it is lowered to Quantum Semantic IR, **then** the IR
   records a finite acting space with source provenance and does not expand
   gates or choose a provider.
2. **Given** pure or mixed transformation regions, **when** they are
   represented, **then** purity/mixedness and transformation identity remain
   explicit and inspectable.
3. **Given** unitary, isometry, channel, or measurement regions, **when** they
   are represented, **then** region kind boundaries remain distinct without
   collapsing into OpenQASM opcodes.
4. **Given** static control and parameter symbols, **when** they are
   represented, **then** control structure and parameters remain explicit;
   dynamic controller values cannot redefine acting-space shape in this Issue
   (full Dynamic QPU remains LISS-0077).
5. **Given** linear resource / ancilla lifetime markers required by reviewed
   tests, **when** the verifier runs, **then** missing provenance or invalid
   region contracts emit named diagnostics and do not silently repair.
6. **Given** an exact or approximate operation marker, **when** it is present,
   **then** the marker is retained for later Algorithm Plan IR; numerical
   error bounds and mapping choices remain out of scope here.
7. **Given** simulator and QPU planning consumers, **when** they read this IR,
   **then** neither embeds provider SDK types; unsupported targets fail later
   at ports, not by forking semantics.

## Non-goals

- no numerical equation solving, state-vector execution, or simulator engines;
- no gate or matrix expansion / circuit synthesis;
- no Jordan–Wigner or other encoding **execution** (decision ledger → LISS-0083);
- no Algorithm Plan IR, verified pass manager, or Logical QPU IR;
- no provider SDK, credentials, network, OpenQASM-as-semantics, or QIR-as-semantics;
- no Equation DTO extensions or auto-extraction (LISS-0116 minimal form stands;
  further work → LISS-0119+);
- no Dynamic QPU controller surface (`dynamic qpu fn` → LISS-0077);
- no `compile_source` soft wire unless a separately approved Slice E;
- no Rust mirror (LISS-0070 deferred).

## Proposed slices

| Slice | Scope | Gate |
|---|---|---|
| **A** | Immutable root DTOs (`QuantumSemanticModule` / region / provenance), verifier, importable builder stub | Phase 1 Red after this plan approval |
| **B** | Finite acting space; pure/mixed transformations; unitary vs channel regions | Separate Red approval |
| **C** | Static control; parameters; measurement regions; linear / ancilla lifetime markers | Separate Red approval |
| **D** | Exact vs approximate markers; minimal Physics IR → Quantum Semantic lowering evidence; docs/catalog | Separate Red approval |
| **E** (optional) | Soft `CompileResult` wire | Explicit Adjudicator approval |

Each slice remains additive and provider-neutral. Phase 2 may implement only
reviewed Red assertions; Phase 3 is behavior-preserving cleanup.

## Exclusive write paths (initial)

| Path | Role |
|---|---|
| `compiler/staqex/quantum_semantic_ir.py` | **new** — DTOs, verifier, builder |
| `tests/test_quantum_semantic_ir_*.py` | Red/Green for this Issue |

**Read-only by default:** `physics_ir.py`, `physics_equation.py`,
`physics_ir_lower.py`, evaluator, QPU adapters.

**Forbidden until Slice E approval:** routine `pipeline.py` edits.

## Adjudicator Decision Points

- [ ] Approve Issue body / plan intake (this document + companion plan)
- [ ] Authorize Slice A Phase 1 Red only (separate message)
- [ ] Confirm out-of-scope list (numerical / gate / JW / QPU / Equation
      extension / 0083 / soft wire)
- [ ] Confirm module name `quantum_semantic_ir.py` adjacent to Physics IR
- [ ] Approve later Slices B–E individually

## Design decisions requested (plan intake)

1. Accept blueprint §4.3 as the authoritative vocabulary boundary for this
   Issue.
2. Keep diagnostics non-compile-hard until a later Issue promotes selected
   codes (mirror Physics IR policy).
3. Defer all encoding / approximation **choices** to LISS-0083 even when
   markers exist on Quantum Semantic IR.
