# LISS-0008: Trotterize `evolve … under H for t` → OpenQASM gates

## Metadata

- Local issue ID: LISS-0008
- GitHub issue: none
- Status: **done**
- Phase: Feature Path — Green
- Type: feature + architecture
- Priority: P1
- Initial planning size: L
- Current planning size: M
- Reclassification reason: Split from [LISS-0002](LISS-0002-openqasm3-codegen-backend.md);
  shipped under ADR **0063**.
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Lower continuous-time Schrödinger evolution

\[
U = e^{-iHt}
\]

appearing as `evolve … under H for t` into a finite product of OpenQASM 3
gates (Pauli-string first-order Trotter → `rz` / `rx` / `h` / `cx`
sequences), **without** introducing vendor SDKs into the compiler core
(ADR 0059 / 0063).

## Acceptance Notes

- [x] Adjudicator Accepts Trotter design (ADR 0063: first-order, fixed-N policy,
      Pauli-only MVP).
- [x] Codegen path: successful compile of `evolve under H for t` emits discrete
      gates (or an explicit diagnostic when H is unsupported).
- [x] Fixture: 2-site TFIM (`quantum_ising.staqex`) + single-qubit `X` round-trip
      tested in `tests/test_qasm3_codegen.py`.
- [x] Unsupported H (Fock) → `QASM_TROTTER_UNSUPPORTED_H` (not silent empty).
- [x] Zero new third-party quantum SDK imports.
- [x] SV suite + `tests/test_qasm3_codegen.py` green.

## Dependencies

- Parent: [LISS-0002](LISS-0002-openqasm3-codegen-backend.md)
- Depends on: ADR 0059; shipping `rx`/`ry`/`rz`/`cx` gate emit
- Related: ADR 0038 / 0041 (evolve under H), ADR 0050 (sparse Pauli), ADR 0063

## Adjudicator Decision Points

- [x] First-order Trotter for MVP (higher-order Suzuki deferred).
- [x] Default slice count: `clamp(ceil(|t|·8), 1, 64)`.
- [x] New ADR **0063** (amends 0059 deferred note).

## Context

- Included: OpenQASM emit of qubit Pauli / sparse-Pauli Hamiltonians.
- Omitted: pulse-level IR; mid-circuit measure; cloud submit; Suzuki order-2+.
- Assumptions: Kernel evaluator already does dense/sparse evolve; codegen must
  approximate for gate backends.

## AI Planning Records

### AIP-0008-001

- Status: done
- Created at: 2026-07-23
- Planning size: M
- Intended execution route: Architecture Accept (ADR 0063) + Feature Path
- Intended scope: QASM lowering only; no change to Kernel evolve semantics
- Confidence: high (after ship)

## References

- ADR 0059, ADR 0063, LISS-0002
- Implementation: `compiler/staqex/backend/qasm/trotter.py`

## Work Notes

- 2026-07-23: split out of LISS-0002 for clear ownership.
- 2026-07-23: shipped first-order Pauli Trotter + reject codes + tests.

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```
