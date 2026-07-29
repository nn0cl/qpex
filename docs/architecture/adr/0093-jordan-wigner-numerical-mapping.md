# ADR 0093: Jordan–Wigner numerical mapping

## Status

Accepted (Adjudicator, 2026-07-25) for the LISS-0032 numerical mapping
slice. This is the follow-up lowering slice for the accepted typed
second-quantized boundary in LISS-0032, structurally parallel to ADR 0088
(finite binder lowering) for LISS-0030.

## Context

LISS-0032 shipped the typed families (`FermionOperator`, `BosonOperator`,
`SpinOperator`, `QubitOperator`), the symbolic atoms (`create`,
`annihilate`, `spin_raise`, `spin_lower`), statistics/canonical-ordering
provenance, and the explicit `map(operator, mapping)` boundary. It
deliberately deferred numerical mapping.

Direct probe of the shipped Kernel (2026-07-25) established what that
deferral costs a physicist:

- A second-quantized program **type-checks** (`check` reports `ok`).
- `map(H, JordanWigner)` records only a name string in the Symbolic IR
  (`{"operator": "mapped", "mapping": "JordanWigner"}`); no Pauli operator
  is produced.
- Running it fails: the evaluator does not know `create` at all
  (`RUNTIME_ERROR: call cannot be classical value ...`, exit 1).
- Lowering it fails: `emit-qasm` rejects with
  `QASM_TROTTER_UNSUPPORTED_H: unknown Operator` (exit 1).

Both failures are honest (non-zero exit, explicit diagnostic) — this is not
a silent-output defect of the LISS-0049 class. The gap is that a physicist
can write a second-quantized Hamiltonian and obtain **no artifact at all**:
neither a simulation result nor a QASM circuit to keep for future hardware.
This is independent of QPU hardware availability.

The same probe confirmed the receiving machinery already exists. Pauli
operator trees of exactly the shape Jordan–Wigner produces run and lower
today:

| Probe | `run` (SV) | `emit-qasm` |
|---|---|---|
| `0.5 * I - 0.5 * Z` (diagonal, the $n_p$ shape) | ok | Trotterized `rz` |
| `-J * (Z(0) * Z(1)) - h * (X(0) + X(1))` (multi-qubit strings) | ok | `cx`/`rz`/`cx` |

So one transformation — fermionic operator to concrete Pauli `Operator` —
opens both the simulator path and the QASM path at once. No new back end is
required.

## Decision

1. **Convention is fixed and normative.** With $\prod_{k<p} Z_k$ as the
   parity (Jordan–Wigner) string:

   $$a_p = \left(\prod_{k<p} Z_k\right)\frac{X_p + iY_p}{2}, \qquad
     a_p^\dagger = \left(\prod_{k<p} Z_k\right)\frac{X_p - iY_p}{2}$$

   Consequences that a physicist may rely on:

   - $n_p = a_p^\dagger a_p = \dfrac{I - Z_p}{2}$;
   - an **occupied** orbital is $|1\rangle$ and an empty orbital is
     $|0\rangle$.

2. **Orbital index maps to qubit index directly** ($p \mapsto q_p$), with no
   reordering. Any future active-space or reordering scheme is a separate
   decision, not an implicit default.

3. **Scope covers one-body and two-body terms.** Both

   $$a_p^\dagger a_q \quad\text{and}\quad a_p^\dagger a_q^\dagger a_r a_s$$

   are in scope for this slice, including $p \neq q$ hopping terms and the
   full two-body interaction terms of electronic-structure Hamiltonians.
   Two-body terms are explicitly **not** deferred.

4. **Correct mapping outranks compile and simulation cost.** The
   Adjudicator's decision (2026-07-25) is that this project is deliberately
   ambitious and that functional correctness comes first. Therefore:

   - the two-body Pauli-string count growing as $O(N^4)$ is **not** a reason
     to narrow this slice;
   - no hard resource limit is introduced whose only justification is term
     count, compile time, or simulation cost;
   - performance work — term-count reduction, Pauli-string grouping,
     canonical-form caching, simulator throughput — is **separate future
     work, out of scope here**, and must not be smuggled in as a scope
     restriction on this slice.

   This is a statement about *justification*, not indifference: optimization
   remains a legitimate concern to be addressed on its own terms, later.

5. **The mapping result is a concrete Pauli `Operator` tree**, the same value
   the existing SV evaluator and the existing Trotter/QASM lowering path
   already consume (see the Context table). `map` stops producing a
   name-only record.

6. **Provenance is retained**: mapping name, input family/domain, output
   domain, qubit count, and source span. The symbolic second-quantized form
   remains available as provenance; it is not the executable value.

7. **Hermiticity is not re-implemented here.** `compiler/staqex/unitarity_check.py`
   already rejects a non-Hermitian Hamiltonian used in `evolve`
   (`_check_hamiltonian_hermitian`), and `backend/qasm/trotter.py` already
   rejects non-Hermitian Pauli coefficients. A Jordan–Wigner result that is
   non-Hermitian — for example a bare $a_p^\dagger a_q$ with $p \neq q$,
   which is Hermitian only in a combination such as
   $a_p^\dagger a_q + a_q^\dagger a_p$ — is caught by those existing checks.
   This slice adds no parallel mechanism.

8. **No silent fallback.** Any second-quantized construct this slice does not
   cover must produce an explicit diagnostic, never a plausible-looking but
   wrong operator or circuit, consistent with the posture accepted in
   LISS-0049 and ADR 0074/0075.

## Deferred

Bravyi–Kitaev and parity mappings; `BosonOperator` mapping (its
infinite-dimensional mode space needs a truncation decision of its own);
`SpinOperator` mapping; active-space selection, orbital freezing, and index
reordering; exchange-law normalization beyond the canonical ordering already
shipped by LISS-0032; chemistry solvers and molecular integral engines;
provider SDKs; and all term-count/performance optimization per Decision 4.

## Verification contract

- $a_0^\dagger a_0$ mapped through Jordan–Wigner is numerically equivalent to
  the hand-written `0.5 * I - 0.5 * Z(0)`, verified by identical simulation
  behavior rather than by asserting an internal representation.
- A program using a mapped one-body Hamiltonian **runs** on the SV simulator
  and **emits QASM**; both are required, neither alone is acceptance.
- A program using a mapped two-body Hamiltonian likewise runs and emits QASM.
- A $p \neq q$ hopping term produces the parity ($Z$) string between the
  operator indices.
- Mapping provenance records the mapping name and qubit count.
- An unsupported second-quantized construct produces an explicit diagnostic,
  not a silent empty or fabricated operator.
