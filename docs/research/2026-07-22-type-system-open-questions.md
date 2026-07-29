# Type system research queue (2026-07-22)

Companion to `docs/architecture/staqex-type-system.md` and ADR 0018.
Status: open investigation — not implementation authorization.

## Settled

- Runtime = `State<T>` in one joint; classical only via lift or post-measure.
- Kernel ops: `State<Int>` with `+,-,*`.
- String concat as pushforward is design-plausible (finite support).

## Abstraction + stdlib layer (settled direction)

- Generics / traits / `system` — ADR 0019.
- **`map` / `project` / `interfer` / `interface System`** — ADR 0021
  (`given`/`fold`/`QSystem` naming superseded).
- See `staqex-stdlib-combinators.md`, semantics §Project / §Interfer.

## Investigate next

### 1. Symbol vs String for `when` exhaustiveness

- Hypothesis: `Symbol` = closed enum-like finite set → static exhaustiveness.
- `String` = open atom set → require `_` wildcard more often.
- Action: draft 1-page comparison with 2–3 narrative examples from QM labeling
  (basis names) vs logging/text pipelines.

### 2. Partial arithmetic (`/`, `%`)

- Options: (A) forbid in MVP; (B) error atom / absorbing failure mass;
  (C) rational carrier `State<Rat>`.
- Action: prefer (A) until a fixture forces otherwise; record choice in ADR.

### 3. `State<Float>`

- Options: fixed bins, exact rationals, Monte Carlo bags (conflicts with
  exact Discrete PMF story if mixed carelessly).
- Action: keep out of Kernel; tie to stance (a) approx roadmap.

### 4. Boolean connectives without short-circuit

- Encode `&&` / `||` as total truth-table pushforwards on `State<Bool>`, or
  desugar to `when`.
- Action: write truth-table denotation before any surface sugar.

### 5. Prior art pointers (to deepen later)

- Probabilistic lambda / Giry: typed measures over carriers.
- Quantum languages: classical/quantum type splits (Staqex inverts default).
- Finite-support string PCF / symbolic automata — for `State<String>` bounds.
