# LISS-0002: OpenQASM 3.0 codegen backend (zero-dependency; Braket path)

## Metadata

- Local issue ID: LISS-0002
- GitHub issue: none (local-only; GitHub template ignored by design)
- Status: **in progress** (MVP codegen shipped; Trotter / extended gates Open)
- Phase: Feature Path — Green for MVP emit; Architecture for Trotter follow-on
- Type: feature + architecture
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: local working tree (docs/language-axioms-mvp-spec lineage)

## Summary

Provide an **OpenQASM 3.0 Codegen Backend** so type-checked QPex programs can
be lowered to vendor-portable QASM text for later host submit (AWS Amazon
Braket, IBM, etc.) **without** pulling cloud SDKs into the compiler core.

Inbound request (GitHub-style paste) is archived under
`docs/issues/inbox/2026-07-23-openqasm3-braket-codegen.md`.

## Acceptance Notes

### Shipped (Kernel — 2026-07-23)

- [x] Zero-dependency: `compiler/qpex/codegen_qasm.py` + `backend/qasm/*`
      use Python stdlib only (no braket/qiskit imports).
- [x] `OpenQASM3Generator` emits `OPENQASM 3.0;`, `include "stdgates.inc";`,
      `qubit[N] q;`, `bit[N] c;`, gates, `c[i] = measure q[j];`.
- [x] Gate map (MVP): `h`,`x`,`y`,`z`,`rz`,`cx`,`cz`,`swap`,`measure`
      (from ket/`cnot`/`apply`/`capply` patterns).
- [x] Public API: `QPexCompiler.compile_to_qasm3(file_path) -> str`
      (module `codegen_qasm.py`; also re-exported from `compiler.qpex`).
- [x] Thin alias `compiler/qpex/compiler.py` for the issue’s expected path.
- [x] AT-TDD: `tests/test_qasm3_codegen.py` (Bell / portable_bell examples).
- [x] Existing SV suite remains green (156/156 at last check).
- [x] ADR **0059** records zero-dependency + Braket-as-host-adapter stance.

### Still Open (this issue remains open until checked)

- [ ] Extended single-qubit: `S`, `T`, `rx`, `ry` (beyond existing `rz`).
- [ ] Trotterization: `evolve … under H for t` → discrete `rz`/`cx` sequences.
- [ ] Explicit rejection path tests when compile fails before emit.
- [ ] Optional example alias `examples/01_bell_state.qpex` path named in
      inbound DoD (current: `examples/03_quantum_information/bell_state.qpex`
      / `portable_bell_qpu.qpex`).

## Dependencies

- Parent: none
- Depends on: ADR 0036 (backend targets), ADR 0032 (DAG IR), shipping Kernel
- Blocks: host-side Braket submit adapter (out of compiler core)
- Related: ADR 0059, LISS-0001 (axioms / MVP), SV-10 / SV-11

## Adjudicator Decision Points

- [x] Compiler core must stay zero-dependency (approved by inbound constraint;
      recorded in ADR 0059).
- [x] Braket / IBM credentials and submit live **outside** codegen (host
      adapter later) — not in `examples/` source.
- [ ] Approve Feature Path Phase 1 Red for **Trotter** sub-scope when ready
      (not requested yet).
- [ ] Whether `S`/`T`/`rx`/`ry` land in the same ADR amendment or a follow-on.

## Context

- Included: inbound OpenQASM3 + Braket integration ask; existing
  `backend/qasm` emitter; portable Bell example.
- Omitted: cloud account wiring, pulse-level IR, mid-circuit measure
  (still Forbidden by Early Collapse).
- Assumptions: OpenQASM 3 text is the interchange; vendor SDK is a **host**
  concern after emit.

## AI Planning Records

### AIP-0002-001

- Status: accepted
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-23
- Planning size: M
- Intended execution route: Feature Path (MVP emit already Green) +
  Architecture Path (ADR 0059)
- Intended scope: local issue ledger, ADR, `compiler.py` alias, honest
  DoD split (shipped vs Open)
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: documentation + thin alias only in this planning unit
- Assumptions: Trotter deferred; no GitHub Issue creation
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: none

## References

- OpenQASM 3 Live Spec (community): https://openqasm.com/
- ADR 0036: `docs/architecture/adr/0036-backend-targets-cli.md`
- ADR 0059: `docs/architecture/adr/0059-openqasm3-zero-dependency-codegen.md`
- Tests: `tests/test_qasm3_codegen.py`
- Facade: `compiler/qpex/codegen_qasm.py`

## Work Notes

- Inbound DoD cited `examples/01_bell_state.qpex` — that path does not exist;
  use `03_quantum_information/bell_state.qpex` or `portable_bell_qpu.qpex`.
- `QPexCompiler` lives in `codegen_qasm.py`; `compiler.py` is a stable import
  path alias for agents following the inbound file list.

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 -c "from compiler.qpex.compiler import QPexCompiler; print(QPexCompiler().compile_to_qasm3('examples/03_quantum_information/portable_bell_qpu.qpex'))"
python3 tests/spec_verification/run_all.py
```
