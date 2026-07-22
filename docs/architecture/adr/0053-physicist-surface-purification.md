# ADR 0053: Physicist mental-model surface purification

## Status

Accepted (2026-07-23).

Companions: ADR 0045/0052 (unitarity), 0049/0051 (HO). Verification: SV-23/29/30 + examples.

## Context

Audit of reserved words and pedagogy found classical-programming smells
(`project` as filter, `measure` of ⟨O⟩, `Xx`/`Px`, toy Ising/gauge).

## Decision (zero compromise)

1. **Context-typed `X`/`P` on Position grids** — `H = ½(P²+X²)` uses bare
   Pauli letter `X` and momentum `P`; `op_space` selects grid vs Fock (`N`/`Q`)
   vs qubit. Legacy `Xx`/`Px` removed from the surface.
2. **`project(state, k)`** — Hilbert $|k\rangle\langle k|$ (Lüders + renorm).
   Predicate lambdas and classical `coin` filters → `PREDICATE_PROJECTOR_ERROR`.
3. **`measure`** — Born collapse on quantum States only.
   `measure(expect(…))` / classical scalars →
   `CANNOT_MEASURE_CLASSICAL_VALUE_ERROR`.
4. **`vacuum()`** — computational / Fock $|0\rangle$. Empty support → `empty()`.
5. **`grover_diffuse` / `walk_shift`** — rename from `diffuse` / `shift`
   (aliases kept in evaluator for one release).
6. **Examples** — TFIM replaces classical Ising; U(1) phase+Hilbert project
   replaces coin gauge toy.
7. **`if` diagnostics** — `NON_UNITARY_DECOHERENCE_ERROR` wording.

## Consequences

Positive: blackboard `X,P` and true projectors. Negative: classical filter
pedagogy gone; harness `State.project(pred)` remains Python-only.

## Verification

SV-23/29/30 + full example suite.
