# ADR 0059: OpenQASM 3.0 zero-dependency codegen (Braket path)

## Status

**Accepted** (2026-07-23).

Companions: ADR **0036** (portable `--target` / QPU fork), ADR **0032** (DAG IR),
local issue **LISS-0002**.

## Context

Hardware / cloud backends (AWS Amazon Braket, IBM Quantum, …) consume
**OpenQASM** (or similar IR), not Staqex source. Pulling `amazon-braket-sdk` or
`qiskit` into the **compiler core** would:

1. bloat and slow the Kernel,
2. couple language semantics to a vendor SDK lifecycle,
3. violate ADR 0036’s “source remains backend-agnostic” rule.

## Decision

1. **Codegen is stdlib-only.** `compiler/staqex/codegen_qasm.py` and
   `compiler/staqex/backend/qasm/*` MUST NOT import vendor quantum SDKs.
2. **AST / CompilationUnit in → OpenQASM 3.0 text out.** Emission runs only
   after a successful compile (`compile_path` / `compile_source`).
3. **Public API:** `OpenQASM3Generator` and
   `StaqexCompiler.compile_to_qasm3(file_path) -> str`
   (import path `compiler.staqex` or `compiler.staqex.compiler`).
4. **Mandatory QASM header / registers / measure** as OpenQASM 3:
   `OPENQASM 3.0;`, `include "stdgates.inc";`, `qubit[N] q;`, `bit[N] c;`,
   `c[i] = measure q[j];`.
5. **Gate set (extended 2026-07-23):** `h`,`x`,`y`,`z`,`s`,`t`,`rx`,`ry`,`rz`,
   `cx`,`cz`,`swap`,`measure` (lowered from ket / `cnot` / `apply` /
   `capply` / `apply(S|T|rx(θ)|ry(θ), …)`).
6. **Braket (and peers) are host adapters**, not Kernel deps: they may wrap
   the emitted string + credentials **outside** `compiler/staqex/`.
7. **Trotter of `evolve … under H for t`:** shipped in ADR **0063** /
   [LISS-0008](../../issues/LISS-0008-trotter-evolve-qasm.md) (first-order Pauli).
   Optional inbound path alias `examples/01_bell_state.staqex` remains unused —
   use `03_quantum_information/portable_bell_qpu.staqex`.

## Consequences

Positive:

- Compiler stays lightweight and portable.
- One QASM artifact can feed multiple clouds.
- Pauli Hamiltonians lower to discrete gates without vendor SDKs.

Negative:

- Trotter is first-order / fixed-N; Fock / grid H still reject at emit.

## Enforcement

- Reject PRs that add braket/qiskit imports under `compiler/staqex/`.
- Keep SV-10 / SV-11 and `tests/test_qasm3_codegen.py` green when touching emit.

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```
