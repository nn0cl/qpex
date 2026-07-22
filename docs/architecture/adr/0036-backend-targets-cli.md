# ADR 0036: Backend targets via CLI (`--target`) — portable State programs

## Status

Accepted (2026-07-23).

Canonical: `docs/architecture/qpex-backend-targets.md`.

## Context

DAG IR (ADR 0032 / Phase 3) is the fork point for CPU Joint evaluation,
GPU batch kernels, and QPU transpilation (OpenQASM 3 / QIR / pulse).

Baking `@Target(IBM…)` or `import qpex.backend.IBMQuantum` into **source**
would couple physics models to a vendor and violate “Never Leave the State”
portability: the program must describe **only** Joint→Joint evolution plus
terminal `measure`.

## Decision

1. **Source remains backend-agnostic.** No required hardware imports or
   target attributes in `.qpex` for Kernel / research programs.
2. **Execution target is a compile/run option:**  
   `qpex run --target cpu|gpu|qpu:<profile>` (and `qpex check --target …`
   for target-aware limits when those land).
3. **Codegen fork after DAG IR:**
   - `cpu` — Discrete PMF / Joint evaluator (current default)
   - `gpu` — reserved (CuStateVec / data-parallel; later)
   - `qpu:*` — Quantum Transpiler → OpenQASM 3 / QIR → vendor submit (later)
4. **Early Collapse ban (ADR 0027)** is also a **NISQ friendliness law**:
   mid-circuit measure is rejected in source before any QPU mapping.
5. Topology (SWAP insertion), qubit-count caps, and depth / T1–T2 warnings
   are **target-profile checks**, not surface syntax.

## Consequences

Positive:

- Write-once State programs; simulator ↔ QPU without edits.
- Matches Hilbert-space / unitary+measure mental model.

Negative:

- Vendor credentials and cloud submit live in host config, not in language
  examples (documented separately when wired).

## Enforcement

Reject PRs that add required `import qpex.backend.*` or `@Target` as the
**only** way to select a QPU for portable samples.
