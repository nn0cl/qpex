# Kernel PoC fixtures

Design fixtures for the Adjudicator-authorized **Kernel PoC track**.
These are not Feature Path Phase 1 tests by themselves; a harness that turns
them green is the unlock condition for Phase 1 Red.

| ID | File | Law under test |
|----|------|----------------|
| PoC A | `poc-a-correlated-self-sum.json` | `x + x` is pushforward $x \mapsto 2x$; mass on `{0,2}` only |
| PoC B | `poc-b-deferred-rng.json` | Zero `RngPort` calls until terminal `observe` |

Normative semantics: `docs/specs/qpex-formal-semantics-sketch.md`.

## Harness contract (when implemented)

1. Load fixture JSON.
2. Build initial joint from `initial_joint`.
3. Apply `steps` as pure joint transformers until `observe`.
4. Assert every `assertions[]` entry.
5. Fail the fixture if any RNG counter violates `rng.calls_allowed_before_observe`.

Do not implement production language surface beyond what the fixture requires.
