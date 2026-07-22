# Challenge intake: OpenQASM 3.0 Codegen (Braket path)

| Field | Value |
|-------|-------|
| Received | 2026-07-23 |
| Channel | Adjudicator paste (GitHub Issue template style) |
| Local ledger | **[LISS-0002](../LISS-0002-openqasm3-codegen-backend.md)** |
| ADR | **[0059](../../architecture/adr/0059-openqasm3-zero-dependency-codegen.md)** |
| GitHub | ignored (project-local management only) |

## Objective (from inbound)

Translate type-checked QPex AST → OpenQASM 3.0 text with **zero** compiler
dependencies on amazon-braket-sdk / qiskit, enabling later host submit to
Braket / IBM / etc.

## Disposition

| Inbound ask | Disposition |
|-------------|-------------|
| `OpenQASM3Generator` + header / registers / measure | **Done** (`codegen_qasm.py`) |
| `compile_to_qasm3(path)` | **Done** (`QPexCompiler`; also `compiler.py` alias) |
| Gate map X/Y/Z/H/CX/CZ/SWAP/Rz | **Mostly done** (S/T/Rx/Ry still Open) |
| Trotterize `evolve under H` | **Open** — tracked in LISS-0002 |
| `tests/test_qasm3_codegen.py` | **Done** |
| Keep SV suite green | **Done** at intake time |
| Put file under `.github/ISSUE_TEMPLATE/` | **Rejected** — use `docs/issues/` per template |

## Agent prompt (short)

See LISS-0002 §References and ADR 0059. For remaining work, open Feature Path
only for items still unchecked in LISS-0002 Acceptance Notes.

## Original inbound body (archived)

The following is the pasted GitHub-style issue (kept for audit; not normative).

---

# Issue: Add OpenQASM 3.0 Codegen Backend for AWS Amazon Braket Integration

## Context & Objective

QPex has successfully established a type-first, physics-axiomatic language kernel with static unit checking and explicit quantum state verification. To execute QPex quantum programs on actual physical hardware (such as IBM Quantum or devices on AWS Amazon Braket like Rigetti, IonQ, IQM, and SV1 simulators), QPex requires an **OpenQASM 3.0 Codegen Backend**.

This issue requests the implementation of `OpenQASM3Generator` which directly translates type-checked QPex AST nodes into valid OpenQASM 3.0 code strings **without introducing any external runtime dependencies (zero-dependency)**.

## Requirements & Specifications

### 1. Architecture Constraints

- **Zero-Dependency Mandate**: The compiler backend (`compiler/qpex/codegen_qasm.py`) must rely **ONLY on Python Standard Library**. Do NOT import external SDKs like `amazon-braket-sdk` or `qiskit` into the compiler core.
- **AST-First Translation**: The generator must consume type-checked AST nodes emitted after successful pass through `typechecker.py`.

### 2. OpenQASM 3.0 Standard Compliance

- Header: `OPENQASM 3.0;` / `include "stdgates.inc";`
- Registers: `qubit[N] q;` / `bit[N] c;`
- Gates: X,Y,Z,H,S,T,Rx,Ry,Rz / CX,CZ,SWAP / measure
- Dynamic / Trotter: decompose `evolve … under H` into discrete gates

### 3. Expected File Changes

- `compiler/qpex/codegen_qasm.py` — `OpenQASM3Generator`
- `compiler/qpex/compiler.py` — `compile_to_qasm3`
- `tests/test_qasm3_codegen.py`

### 4. Acceptance Criteria

- Valid QASM from Bell-style examples
- Trotterization for \(e^{-iHt}\)
- No new core deps in pyproject/requirements
- Existing 155+ tests green
- New unit tests pass

### 5. Agent execution prompt

(See inbound paste in chat; execute against LISS-0002 open checkboxes only.)
