# LISS-0002: OpenQASM 3.0 codegen backend (zero-dependency; Braket path)

## Metadata

- Local issue ID: LISS-0002
- GitHub issue: none (local-only)
- Status: **done** (gates + reject paths; Trotter completed in LISS-0008 / ADR 0063)
- Phase: Feature Path — Green
- Type: feature + architecture
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Provide an **OpenQASM 3.0 Codegen Backend** so type-checked Staqex programs can
be lowered to vendor-portable QASM text for later host submit (AWS Amazon
Braket, IBM, etc.) **without** pulling cloud SDKs into the compiler core.

## Acceptance Notes

### Shipped

- [x] Zero-dependency codegen (`codegen_qasm.py` + `backend/qasm/*`)
- [x] OpenQASM 3 header / registers / measure
- [x] Gate map: `h`,`x`,`y`,`z`,`s`,`t`,`rx`,`ry`,`rz`,`cx`,`cz`,`swap`,`measure`
- [x] `apply(S|T, q)` runtime + QASM; `apply(rx(θ)|ry(θ), q)` with closed θ
- [x] Public API `StaqexCompiler.compile_to_qasm3` + `compiler.py` alias
- [x] AT-TDD: `tests/test_qasm3_codegen.py` (Bell, S/T/rx/ry, reject paths)
- [x] Explicit reject: compile failure / missing file before emit
- [x] ADR **0059** updated for extended gates
- [x] SV suite green

### Still Open

- [x] Trotterization → **done in [LISS-0008](LISS-0008-trotter-evolve-qasm.md)** / ADR 0063
- [x] Optional inbound alias `examples/01_bell_state.staqex` — **wontfix**;
      use `03_quantum_information/portable_bell_qpu.staqex`

## Dependencies

- Related: ADR 0059, LISS-0001 (closed), [LISS-0008](LISS-0008-trotter-evolve-qasm.md)

## Adjudicator Decision Points

- [x] Zero-dependency compiler core
- [x] `S`/`T`/`rx`/`ry` in same ADR 0059 amendment (done)
- [x] Approve Feature Path Red for **Trotter** (LISS-0008 / ADR 0063)

## Work Notes

- 2026-07-23: extended gates + reject tests; Trotter closed via LISS-0008.

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```
