# ADR 0063: First-order Pauli Trotter for OpenQASM evolve

## Status

**Accepted** (2026-07-23).

Companions: ADR **0059** (OpenQASM codegen), ADR **0038** / **0041** (evolve under H),
ADR **0050** (sparse Pauli). Follow-up issue: [LISS-0008](../../issues/LISS-0008-trotter-evolve-qasm.md).

## Context

Kernel evaluates `evolve … under H for t` exactly (Taylor / dense). Gate backends
need a discrete product of `rx`/`ry`/`rz`/`cx`. Vendor Trotter SDKs are banned from
`compiler/qpex/` (ADR 0059).

## Decision

1. **MVP formula:** first-order Lie–Trotter
   \(e^{-iHt}\approx\bigl(\prod_k e^{-i H_k\Delta t}\bigr)^N\), \(\Delta t=t/N\).
2. **Slice policy:** `N = clamp(ceil(|t|·8), 1, 64)` unless an explicit override is
   passed to the lowering helper (tests may fix N).
3. **In-scope H:** qubit Pauli / sparse-Pauli Operators (`compile_sparse_pauli`).
   Each non-identity term uses basis change (X→`h`, Y→`rx(π/2)`), CNOT ladder,
   `rz(2θ)` with \(θ=c·\Delta t\), then undo.
4. **Out of scope / reject:** Fock (`N`, hop), grid quadrature, non-Hermitian
   complex coeffs. Emit fails with codes:
   - `QASM_TROTTER_UNSUPPORTED_H`
   - `QASM_TROTTER_BAD_TIME`
   - `QASM_TROTTER_COMPLEX_COEFF`
5. **No Kernel semantics change.** Approximation is codegen-only.
6. **Zero vendor SDKs.**

## Consequences

Positive: TFIM / single-qubit Pauli programs emit runnable QASM.  
Negative: Trotter error is uncontrolled beyond fixed-N; higher-order Suzuki later.

## Enforcement

- Implementation: `compiler/qpex/backend/qasm/trotter.py` + `lower.py`.
- Tests: `tests/test_qasm3_codegen.py` (Ising / X evolve + Fock reject).

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```
