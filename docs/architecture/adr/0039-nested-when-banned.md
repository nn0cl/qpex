# ADR 0039 — Nested `when` banned (coherence / QASM–QIR alignment)

- Status: Accepted
- Date: 2026-07-23
- Deciders: Language design (QPex axioms + low-level QPU comparison)

## Context

Single-level `when` is the Discrete mixture / pushforward form (ADR 0024): it
keeps positively weighted arms without sampling. Nested `when (s0) { … when
(s1) … }` however:

1. Reads like sequential classical `if` / mid-circuit measure on unmeasured
   State.
2. Encourages non-unitary “value remapping” that drops a clear unitary vs
   reduction distinction.
3. Is rejected by OpenQASM / QIR at the type/grammar level: branch only on
   classical bits after explicit measure.

Official samples (Ising agreement, Grover index, classical walk) previously
used nested `when` as sugar for joint functions — physically misleading.

## Decision

1. **Nested `when` is a hard compile error** `NESTED_WHEN_ERROR` (pipeline pass
   after Early Collapse).
2. Coherent multi-wire transforms use operators (`cnot`, `evolve`, `expect`,
   …) or **joint pushforwards** (`s0 == s1`, `b0 * 2 + b1`, sequenced
   single-level `when` binds).
3. Explicit reduction remains `project` / terminal `measure` (not nested
   `when`).
4. Fuller static **unitarity** proofs (`NON_UNITARY_TRANSFORM_ERROR` on all
   non-isometric remaps) are **Deferred** — nesting ban is the v0.1 gate
   aligned with QASM/QIR.

## Consequences

- Parser still accepts nested `when` syntactically; the dedicated pass rejects.
- Examples / SV fixtures must not nest `when`.
- Language Spec §3 Normative; verification protocol lists the code.
