# ADR 0038: Dirac ket literals, Hamiltonian evolve, non-destructive expect

## Status

Accepted (2026-07-23).

Companions: `staqex-language-spec.md`, ADR 0016 (amplitude lift), ADR 0037
(Type-First / structure). Verification: **SV-17**.

## Context

After Type-First + dimensional algebra (ADR 0037) and complex amplitudes
(SV-14), the remaining mind-model gap is Dirac notation and Schrödinger
evolution written as physicists write them — not `dirac(0)` / hand-rolled
phase tables.

## Dependency Adoption Evidence

Not applicable.

## Decision

### A. Ket literals

1. Lexer/Parser accept **`|…>`** as `KetLit` (object-language State prep).
2. MVP lexicon:
   - `|0>`, `|1>` → Dirac on `{0,1}`
   - `|+>` → equal superposition (amp $1/\sqrt{2}$ each)
   - `|->` → $(|0\rangle-|1\rangle)/\sqrt{2}$
   - `|01>`, `|10>`, … → Dirac on the integer with that binary encoding
3. `dirac(c)` remains valid sugar.

### B. Hamiltonian evolution

1. Surface: **`evolve psi under H for t`** (optional parens on `psi`).
2. Meaning: bind result of $U = e^{-i H t}$ applied to amplitudes of `psi`
   (Never Leave the State — pure Joint→Joint).
3. MVP named Hamiltonians (Prelude / ambient): Pauli **`X`**, **`Y`**, **`Z`**
   on a qubit coordinate; extend later to user operators / matrices.
4. Existing **`evolve (seeds) times N {…}`** / **`for dt {…}`** block
   pushforwards remain (classical / Euler mind-model).

### C. Non-destructive expect

1. Prelude **`expect(O, psi)`** → `State<Float>` Dirac of
   $\langle\psi|\hat O|\psi\rangle$ (Born-weighted), **no collapse**.
2. MVP operators: `Z`, `X` (diagonal / Pauli expectations on `{0,1}`
   support), or identity on numeric coordinates (`expect` of values).

### D. Dimensional error pretty-print

`DIMENSION_MISMATCH_ERROR` messages prefer quantity names
(`[Length]` vs `[Time]`) over raw `[L]` / `[T]` when the vector matches a
named quantity; compounds use `·` and superscripts.

## Consequences

Positive:

- Blackboard Dirac / Schrödinger surface.
- Expectation without violating terminal-`measure` law.

Negative:

- Full sparse operator IR / arbitrary $H$ matrix still later-phase.
- Ket `|ψ>` with Unicode / named kets deferred.

## Enforcement

Reject normative examples that treat `expect` as collapsing measure.
SV-17 must stay green with the full suite.
