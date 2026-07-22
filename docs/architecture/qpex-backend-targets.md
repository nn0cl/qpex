# QPex backend targets & QPU mapping

Status: **Accepted** (2026-07-23). ADR **0036**.
Companions: ADR 0027 (terminal `measure`), ADR 0032 (DAG runtime),
`compiler/qpex/ir/`, `compiler/qpex/codegen/`.

---

## 0. Thesis

QPex source describes **pure state-space evolution**. Where that evolution
runs — CPU Joint store, GPU tensor kernels, or a physical QPU — is a
**host/CLI concern**, not an object-language import.

```text
[QPex source] ──► AST ──► DAG IR ──┬── --target cpu  → Joint evaluator
                                   ├── --target gpu  → (reserved) batch kernels
                                   └── --target qpu:* → Transpiler → OpenQASM/QIR
                                                              → pulse / cloud API
```

---

## 1. Why this matches hardware

| Language law | Hardware reading |
|--------------|------------------|
| Never Leave the State | Program stays in Hilbert / probability space |
| Terminal `measure` only | Avoids mid-circuit collapse / NISQ decoherence traps |
| `when` / joint product | Controlled ops / entanglement structure in IR |
| `package` as $\mathcal{H}_A$ | Logical subspaces; physical layout is transpiler |
| No threads / async colouring | Concurrency = superposition, not OS threads |

Programmers write Kotlin-like DX; the IR still looks like operators on a
state, which is what QPUs execute.

---

## 2. CLI surface (normative)

```bash
# Default: local Discrete PMF / Joint (Phase 2–3)
python3 -m compiler.qpex run --target cpu main.qpex

# Reserved — GPU batch path (not required for Kernel green)
python3 -m compiler.qpex run --target gpu main.qpex

# Emit OpenQASM 3 sketch from DAG (submit optional / later)
python3 -m compiler.qpex emit-qasm main.qpex
python3 -m compiler.qpex run --target qpu:ibm_eagle --emit-qasm main.qpex

# Target-aware check (qubit caps / depth warnings when profiles land)
python3 -m compiler.qpex check --target qpu:ibm_eagle main.qpex
```

**Forbidden as the primary portability model:** required
`import qpex.backend.IBMQuantum` or `@Target(...)` inside portable physics
samples. Host credentials belong in environment / config files for the
submitter, not in the State program.

---

## 3. Illustrative lowering (pedagogy)

```qpex
state q = coin()
state result = when (q) {
  0 -> dirac(0),
  else -> dirac(1),
}
measure result
```

Logical intent under amplitude IR:

| Surface | Gate sketch |
|---------|-------------|
| `coin()` | Hadamard on a fresh qubit |
| `when (q) { 0 -> \|0⟩, else -> \|1⟩ }` on a second wire | CNOT (ctrl=q) |
| `measure result` | computational-basis measure |

Emitted OpenQASM 3 (illustrative; see `codegen/openqasm.py`):

```qasm
OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[1] c;
h q[0];
cx q[0], q[1];
c[0] = measure q[1];
```

Discrete PMF `--target cpu` still evaluates the same source via Joint store
without claiming gate fidelity.

---

## 4. Target-aware checks (design)

| Check | `cpu` / `gpu` | `qpu:*` |
|-------|---------------|---------|
| Qubit / support size | Memory-bound | ≤ profile qubit count |
| Circuit depth | Free | Warn vs T1/T2 budget |
| Gate set | Any pushforward | Decompose to native gates |
| Mid-`measure` | **Hard error** (ADR 0027) | Same (already rejected) |

---

## 5. Implementation status

| Piece | Status |
|-------|--------|
| DAG IR extract | Done (`compiler/qpex/ir`) |
| `--target cpu` run | Done (Joint evaluator) |
| `--target` CLI flag + `emit-qasm` | Scaffolding (this ADR) |
| Pattern→OpenQASM for coin/when/measure | PoC emitter |
| GPU / cloud submit / topology SWAP | Later |

---

## 6. Write once

The same `.qpex` under `examples/` must remain valid for `cpu` today and
`qpu:*` tomorrow. Backend choice never rewrites the physics source.
