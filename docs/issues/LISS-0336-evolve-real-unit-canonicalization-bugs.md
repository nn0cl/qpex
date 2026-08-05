# LISS-0336: fix two real-unit `evolve` bugs and re-verify A03/A05/A06/A10 (urgent, blocks WP-0095 continuation)

## Metadata

- Local issue ID: LISS-0336
- Status/phase: proposed / pre-Phase-1 (2026-08-05)
- Type: Feature Path (Kernel bug fix — `compiler/staqex/runtime/sparse_pauli.py`,
  `compiler/staqex/runtime/evaluator.py`; re-verification of four already-merged
  example migrations)
- Priority: **P0 — urgent**. Blocks WP-0095 work unit 6+ (including A11's
  planned rewrite, paused for this).
- Initial planning size: `M`
- Owner / agent: Claude Code
- Program: not itself a WP-0095 work unit; a Kernel correctness fix
  discovered while investigating WP-0095 work unit 6 design intake
  (A11 sensing-theme content)
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
  (the real-ℏ migration whose glue code contains these bugs)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md) (introduced
  the affected code paths)
- Blocks: WP-0095 work unit 6+ (paused); re-verification of
  [LISS-0332](LISS-0332-a03-h2-real-unit-migration.md) (A03),
  [LISS-0333](LISS-0333-a05-qaoa-arbitrary-unit-migration.md) (A05),
  [LISS-0334](LISS-0334-a06-ssh-real-unit-migration.md) (A06),
  [LISS-0335](LISS-0335-a10-mission-observatory-real-unit-migration.md) (A10)
- Branch: `fix/liss-0336-evolve-real-unit-canonicalization-bugs`
- GitHub Issue / PR: none yet

## How this was found

While doing live design-intake verification for WP-0095 work unit 6 (a
proposed A11 rewrite, quantum-magnetometry sensing theme, using a
literature-real NV-center zero-field splitting constant D ≈ 2.87 GHz), a
minimal single-qubit probe (`Operator H = defect * X; evolve psi under H
for dur`) showed **zero measurable evolution** regardless of duration —
`expect(Z, psi)` stayed exactly at its initial value for every tested
duration from 0.1 fs to 200 ps. Instrumented tracing (temporary debug
prints, since reverted) found two independent, real bugs in the `evolve`
duration/coefficient pipeline, both introduced by LISS-0330's real-ℏ
migration and never caught because every WP-0095 Green test so far only
asserted "compiles, runs, reaches a non-vacuum measurement" — an
assertion weak enough that both bugs (which produce a wrong but still
non-vacuum result) pass silently.

## Bug 1 — `_coalesce` absolute epsilon zeroes real Joule-scale coefficients

`compiler/staqex/runtime/sparse_pauli.py:163`:

```python
return [PauliTerm(coeff=c, kinds=k) for k, c in acc.items() if abs(c) > 1e-15]
```

This absolute `1e-15` threshold was correct for the pre-ADR-0195
natural-units convention (Hamiltonian coefficients O(0.1–10)), where it
existed to drop terms that exactly (or near-exactly, from floating-point
cancellation) cancel to zero during coalescing. Under real SI Energy
units, a coefficient of 1 eV is `1.602176634e-19` J — four orders of
magnitude *below* this threshold — so **every real-unit qubit-Pauli
Hamiltonian term compiled through `compile_sparse_pauli` is silently
dropped**, leaving `evolve` as a no-op identity transform.

Confirmed live: `Operator H_mixer = w_mix * X[0] + w_mix * X[1]` and
`Operator H_cost = ...` from the already-merged `A05_qaoa_portfolio`
(`w_mix ≈ 1.6e-19` J) both compile to `terms = []` via
`compile_sparse_pauli`.

**Only the multi-qubit-Pauli-Operator path (`compile_sparse_pauli` /
`_eval` in `sparse_pauli.py`) is affected.** The Fock/`hop()`-based path
(`compile_hamiltonian` / `_eval_fock` in `hamiltonian.py`, used by
`A06_topological_edge_memory` and `A10_mission_observatory`'s SSH
Hamiltonians, and by `A03_h2_vqe`'s Jordan-Wigner-mapped-then-summed
`Operator`) does not coalesce via this function and has no equivalent
absolute-epsilon drop — confirmed by reading `_eval_fock`/`_eval_qubits`
in `hamiltonian.py`, which build dense matrices via direct `mat_add`
with no term-dropping step at all. Bug 1 is confirmed to affect
**A05 only** among the four merged examples (its `Operator H_mixer`/
`H_cost` are direct `X[i]`/`Z[i]` qubit-Pauli Operators, not
Fock/`hop()`-routed).

## Bug 2 — `evolve`'s duration is never canonicalized to seconds

`compiler/staqex/runtime/evaluator.py:1502`:

```python
t = float(self._eval_value(expr.duration, {}))
```

The fail-closed check just above this line (LISS-0330, ADR 0195) verifies
that the duration variable's *tracked unit name* maps to the `Time`
dimension family (`self.scalar_units[name]`, e.g. `"fs"`), but then this
line discards that unit information and reads the **raw declared
magnitude** via `_eval_value` — which, per `dimensions.py`'s own
documented convention ("Bare suffixes stay raw; only `expr to target`
applies these factors"), is *not* SI-canonical unless the source used an
explicit `to s` conversion. Every WP-0095 migration so far wrote `Time
dur = X.fs` (bare suffix, matching the syntax LISS-0330/LISS-0332
verified compiles) and never `X.fs to s` — so in every case, `t` is the
raw declared-unit count treated as if it were already in seconds. E.g.
`Time dur = 1.0.fs` yields `t = 1.0` (one **second**), not `1e-15`
seconds — off by 15 orders of magnitude.

Confirmed live: instrumented trace on a probe showed `t = 10.0` for a
declared `Time dur = 10.0.fs`.

This bug is **unit-family-general** (would equally affect `ps`/`ns`/`ms`
durations) and **path-general** — `t` is computed once in
`_hamiltonian_evolve_one_step` before branching to the Fock (nq==0),
grid (nq<0), or qubit-Pauli (nq>0) physics, so it affects **all four**
already-merged examples (A03, A05, A06, A10), regardless of whether Bug
1 also applies to them.

## Fix

1. `sparse_pauli.py::_coalesce`: replace the absolute `1e-15` threshold
   with a threshold relative to the largest coefficient magnitude present
   in the coalesced term set (catches genuine floating-point
   cancellation-to-zero regardless of the physical unit scale in play,
   without zeroing real small-magnitude SI values):
   ```python
   def _coalesce(terms):
       acc = {}
       for t in terms:
           acc[t.kinds] = acc.get(t.kinds, 0j) + t.coeff
       if not acc:
           return []
       scale = max(abs(c) for c in acc.values())
       if scale == 0:
           return []
       tol = scale * 1e-12
       return [PauliTerm(coeff=c, kinds=k) for k, c in acc.items() if abs(c) > tol]
   ```
2. `evaluator.py::_hamiltonian_evolve_one_step`: canonicalize `t` from
   `duration_unit` to seconds via `dimensions.to_canonical_magnitude`
   right after the fail-closed check, before using it in any physics
   path:
   ```python
   from ..dimensions import to_canonical_magnitude
   t_raw = float(self._eval_value(expr.duration, {}))
   t, _canon_unit = to_canonical_magnitude(t_raw, duration_unit)
   ```
3. Re-run each of A03/A05/A06/A10 under the fixed Kernel. Given both
   fixes change the actual physics (durations become ~1e15x smaller;
   A05's Hamiltonian terms stop being silently zeroed), each example's
   specific numeric duration (and, if needed, coefficient magnitudes)
   will likely need re-tuning — following the same live-verification
   process used during each example's original design intake — to
   continue producing a physically sensible (non-trivial, non-chaotically-
   wrapped) result, not just "any" non-vacuum measurement.
4. Strengthen each of the four examples' own regression test (or add a
   shared one) to assert something stronger than "non-vacuum measurement"
   where practical — e.g., a hand-computed expected order of magnitude for
   the phase, or a check that the Hamiltonian's compiled term list is
   non-empty — so a future regression of either bug class fails loudly
   instead of silently passing.

## Explicitly out of scope

- Any change to `expm_ih`/`expm_ih_apply` themselves (LISS-0330's own
  hand-verified reference tests call them directly with pre-computed
  correct-seconds values and pass; the primitives are not the source of
  either bug).
- WP-0095 work unit 6 (A11 rewrite) — paused, resumes after this Issue.
- A general audit of every other `to`-conversion-adjacent code path for
  similar bugs, beyond the two confirmed here and the four examples this
  Issue re-verifies.

## Acceptance reference

```gherkin
Feature: evolve correctly canonicalizes real-unit duration and does not drop real-unit coefficients

  Scenario: a femtosecond-declared duration is used as real seconds, not raw magnitude
    Given `Time dur = 1.0.fs` and a Hamiltonian with a known real Energy coefficient
    When `evolve ... for dur` runs
    Then the resulting phase matches a hand-computed value using t = 1e-15 s, not t = 1.0 s

  Scenario: a real-unit multi-qubit Pauli Operator is not silently zeroed
    Given `Operator H = e * X[0]` with e ~ 1e-19 J (eV scale)
    When the Operator is compiled via compile_sparse_pauli
    Then the resulting term list is non-empty and its coefficient matches e

  Scenario: A03/A05/A06/A10 still compile, run, and reach a non-vacuum measurement
    Given each example under the fixed Kernel, with durations/coefficients
      re-tuned as needed
    When each is compiled and run with a fixed seed
    Then it reaches a non-vacuum terminal measurement reflecting real,
      non-trivial (not identity, not chaotically-wrapped) dynamics
```

## AI planning record (size M)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `M` — two small, localized Kernel fixes plus re-verification
  (and likely numeric re-tuning) of four already-shipped examples.
- Route: direct implementation by this session.
- Assumptions: no other `evolve`-adjacent code path duplicates either bug
  (confirmed by grep: `_coalesce`'s absolute-epsilon pattern and the
  duration-canonicalization gap each occur at exactly one call site).
- Confidence: high for the root-cause diagnosis (both confirmed via live
  instrumented tracing, not inference); medium for how much numeric
  re-tuning each of the four examples will need until re-run.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: tests demonstrating both bugs added, fail for the
      documented reasons.
- [ ] Phase 2 Green: both fixes applied; new tests pass; A03/A05/A06/A10
      re-run and (if needed) re-tuned to keep producing sensible,
      non-trivial dynamics; each example's own existing regression test
      still passes.
- [ ] Phase 3 Refactor: reviewer empathy summary; any example README/
      Issue notes updated if numeric values changed.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check`.
- [ ] LISS-0332/0333/0334/0335 each get a short addendum note pointing to
      this Issue if their example's numeric values changed.

## Non-goals

- Broader audit of all unit-conversion code paths beyond the two bugs
  found.
- WP-0095 work unit 6 (resumes separately after this Issue closes).
