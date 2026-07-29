# Kernel PoC fixtures

Design fixtures for the Adjudicator-authorized **Kernel PoC track**.
Surface lexicon: `docs/architecture/staqex-syntax-vocabulary.md` (ADR 0017).

| ID | File | Law under test |
|----|------|----------------|
| PoC A | `poc-a-correlated-self-sum.json` | `x + x` is pushforward $x \mapsto 2x$; mass on `{0,2}` only |
| PoC B | `poc-b-deferred-rng.json` | Zero `RngPort` calls until terminal `measure` |

Normative semantics: `docs/specs/staqex-formal-semantics-sketch.md`.

## Harness contract (when implemented)

1. Load fixture JSON.
2. Build initial joint from `initial_joint`.
3. Apply `steps` as pure joint transformers until `measure`.
4. Assert every `assertions[]` entry.
5. Fail the fixture if any RNG counter violates `rng.calls_allowed_before_measure`.

Do not implement production language surface beyond what the fixture requires.
