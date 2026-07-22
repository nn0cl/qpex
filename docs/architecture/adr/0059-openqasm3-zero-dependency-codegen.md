# ADR 0059: OpenQASM 3.0 zero-dependency codegen (Braket path)

## Status

**Accepted** (2026-07-23).

Companions: ADR **0036** (portable `--target` / QPU fork), ADR **0032** (DAG IR),
local issue **LISS-0002**.

## Context

Hardware / cloud backends (AWS Amazon Braket, IBM Quantum, …) consume
**OpenQASM** (or similar IR), not QPex source. Pulling `amazon-braket-sdk` or
`qiskit` into the **compiler core** would:

1. bloat and slow the Kernel,
2. couple language semantics to a vendor SDK lifecycle,
3. violate ADR 0036’s “source remains backend-agnostic” rule.

## Decision

1. **Codegen is stdlib-only.** `compiler/qpex/codegen_qasm.py` and
   `compiler/qpex/backend/qasm/*` MUST NOT import vendor quantum SDKs.
2. **AST / CompilationUnit in → OpenQASM 3.0 text out.** Emission runs only
   after a successful compile (`compile_path` / `compile_source`).
3. **Public API:** `OpenQASM3Generator` and
   `QPexCompiler.compile_to_qasm3(file_path) -> str`
   (import path `compiler.qpex` or `compiler.qpex.compiler`).
4. **Mandatory QASM header / registers / measure** as OpenQASM 3:
   `OPENQASM 3.0;`, `include "stdgates.inc";`, `qubit[N] q;`, `bit[N] c;`,
   `c[i] = measure q[j];`.
5. **MVP gate set shipped:** `h`,`x`,`y`,`z`,`rz`,`cx`,`cz`,`swap`,`measure`
   (lowered from ket / `cnot` / `apply` / `capply` patterns).
6. **Braket (and peers) are host adapters**, not Kernel deps: they may wrap
   the emitted string + credentials **outside** `compiler/qpex/`.
7. **Deferred (tracked in LISS-0002):** Trotterization of
   `evolve … under H for t`; gates `s`,`t`,`rx`,`ry`.

## Consequences

Positive:

- Compiler stays lightweight and portable.
- One QASM artifact can feed multiple clouds.

Negative:

- Continuous-time Hamiltonians need an explicit Trotter pass before NISQ
  devices accept them (not yet automatic).

## Enforcement

- Reject PRs that add braket/qiskit imports under `compiler/qpex/`.
- Keep SV-10 / SV-11 and `tests/test_qasm3_codegen.py` green when touching emit.

## Verification

```bash
python3 tests/test_qasm3_codegen.py
python3 tests/spec_verification/run_all.py
```
