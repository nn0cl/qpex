# QPex Spec Verification Protocol（仕様検証メタテスト仕様書）

| Field | Value |
|-------|-------|
| Status | Active (AT-TDD / Kernel PoC harness) |
| Normative Language Spec | `docs/specs/qpex-language-specification.md` (**v1.0**) |
| Grammar | `docs/specs/grammar/qpex.ebnf` |
| Spec spine | Normative Spec + umbrella `docs/architecture/qpex-language-spec.md`, ADR 0021–**0105**; north-star ADR 0106 |
| Diagnostic catalog | `docs/specs/qpex-v1-diagnostic-catalog.md` |
| Acceptance envelopes | `docs/specs/qpex-v1-acceptance-envelopes.md` |
| Dimensional types | `docs/architecture/qpex-dimensional-types.md` (ADR 0037) |
| Harness | `tests/spec_verification/` |
| Report | Spec Compliance Rate（目標 **100%**） |

---

## 0. Purpose

古典的な「最終スカラー値の比較」だけでは、QPex の公理（Never Leave the State・Lit-Lift・確率保存・Early Collapse 禁止・Vacuum・Forbidden/Retired）を検証できない。

本プロトコルは、ランタイム／コンパイラ／型検査器を **5 大メタ検証アサーション** で直接テストする AT-TDD 契約を定義する。

---

## 1. Five Meta Verification Assertions

テストハーネス（および将来のランタイム診断 API）は、少なくとも次を提供する。

### 1.1 `assertNormEquals(state, expectedNorm)`

| | |
|--|--|
| **意味** | $\mathrm{norm}(\rho) = \sum_i |c_i|^2$（Discrete MVP では $\sum_i p_i$）が `expectedNorm` と一致する |
| **既定** | 通常演算後は `1.0`；Vacuum のみ `0.0` |
| **失敗時** | `NORM_MISMATCH` |
| **公理** | 確率保存（ADR 0016 Discrete / 将来 Amplitude） |

許容誤差: `|actual - expected| ≤ ε`（既定 `ε = 1e-12`）。

### 1.2 `assertSuperposition(state, expectedBases)`

| | |
|--|--|
| **意味** | 状態が指定基底集合と振幅／質量で一致する（非破壊） |
| **入力例** | `{0: 0.5, 1: 0.5}` または tagged `Result` 基底 |
| **失敗時** | `SUPERPOSITION_MISMATCH` |
| **公理** | `when` / 分岐は世界線破棄ではなく結合（ADR 0024） |

`inspect` と同様、観測を起こさない。比較はサポート集合の完全一致＋各質量の ε 比較。

### 1.3 `assertTypeIsState<T>(expr)`

| | |
|--|--|
| **意味** | `expr` の静的／ハーネス型が裸の古典型ではなく厳密に `State<T>` |
| **失敗時** | `TYPE_NOT_STATE` |
| **公理** | Lit-Lift・Never Leave the State（言語仕様 §1–§2） |

PoC ハーネスでは、値ラッパ `State[T]` の存在と、演算結果が常に `State` であることを検証する。本番型検査器実装後は同一アサーション名でコンパイル時検証に昇格する。

### 1.4 `assertCompileError(codeSnippet, expectedErrorCode)`

| | |
|--|--|
| **意味** | 禁止構文／不正プログラムがビルド時に拒絶される |
| **代表コード** | `EARLY_COLLAPSE_ERROR`, `FORBIDDEN_KEYWORD`, `RETIRED_KEYWORD`, `DIMENSION_MISMATCH_ERROR`, `TOPLEVEL_EXECUTION_ERROR`, `NESTED_WHEN_ERROR` |
| **公理** | ADR 0027（端末 `measure`）、ADR 0035（Forbidden / Retired）、ADR **0037**（Type-First / dims / structured `main`） |

本番経路: `compiler/qpex/`（Lexer → Parser → Early Collapse → Typecheck）。
`compile_gate.analyze_source` は `compiler.qpex.pipeline.analyze_source` に委譲する。

### 1.5 `assertVacuum(state)`

| | |
|--|--|
| **意味** | `state` が `State.vacuum()`（ノルム 0・空サポート）であり、例外を投げない |
| **失敗時** | `NOT_VACUUM` |
| **公理** | ADR 0034 |

`assertVacuum(s)` ⟹ `assertNormEquals(s, 0.0)` ∧ support empty ∧ type `State<_>`。

---

## 2. Mandatory Categories（SV suites）

Harness modules ship **SV-01–SV-11** and **SV-13–SV-31**. **SV-12 is absent**
(no `sv12_*.py`; number reserved / not shipped).

| ID | Suite | Primary assertions | ADR / Spec |
|----|-------|-------------------|------------|
| **SV-01** | Lit-Lift / スカラー全廃 | `assertTypeIsState`, `assertNormEquals` | §2 Lit-Lift |
| **SV-02** | `when` 非破壊保存 | `assertSuperposition`, `assertNormEquals` | ADR 0024 |
| **SV-03** | 失敗の重ね合わせ | `assertSuperposition`, `assertNormEquals` | ADR 0025–0026 |
| **SV-04** | Early Collapse 非許容 | `assertCompileError(..., EARLY_COLLAPSE_ERROR)` | ADR 0027 |
| **SV-05** | Vacuum + 比較 → `State<Bool>` | `assertVacuum`, `assertTypeIsState<Bool>` | ADR 0034 |
| **SV-06** | Package + Forbidden/Retired + nested `when` | `assertCompileError`, namespace resolve | ADR 0024/0035/**0039** |
| **SV-07** | Kernel eval (`when`/`map`/`project`/`interfer`/`measure`) | `assertSuperposition`, vacuum measure | Phase 2.2 / PoC A |
| **SV-08** | Prelude / Math / CLI / inspect / DAG IR | ecosystem checks | Phase 3 / ADR 0031–0032 |
| **SV-09** | Official `examples/` physics samples | check + run | examples/ |
| **SV-10** | Backend `--target` + OpenQASM emit | portable QPU path | ADR 0036 |
| **SV-11** | QASM3Emitter + SWAP routing (Phase 4.1) | `qpu:openqasm3` | `backend/qasm/` |
| **SV-13** | `evolve times` + tuple bind + correlated Euler | physical syntax P1 | mind-model |
| **SV-14** | Complex amplitudes + `phase`/`cis`/`interfer` cancel | Priority 2 | ADR 0016 lift |
| **SV-15** | Type-First decls + dimensional analysis | `DIMENSION_MISMATCH_ERROR` | **ADR 0037** |
| **SV-16** | Structured `package` + `pub fn main` | `TOPLEVEL_EXECUTION_ERROR` | **ADR 0037** / 0027 / 0066 |
| **SV-17** | Ket / `evolve under H` / `expect` / pretty dims | quantum mind-model | **ADR 0038** |
| **SV-18** | Physical axiom typechecks (P0/P1 audit) | dim / interfer / expect / coin-in-evolve | audit 2026-07-23 |
| **SV-19** | Arbitrary Operator H, $e^{-iHt}$, tensor `*|*`, partial trace | evolve / trace | ADR 0041 area |
| **SV-20** | `apply(U,…)`, hadamard, shift — DTQW | apply surface | ADR 0042 |
| **SV-21** | `capply(ctrl, U, tgt)` controlled unitaries | capply | ADR 0043 |
| **SV-22** | Typed product `State<(A,B)>`, `*|*`, `trace_out` | typed tensor | ADR 0044 |
| **SV-23** | Static unitarity — `NON_UNITARY_TRANSFORM_ERROR` | compile reject | ADR 0045/0053 |
| **SV-24** | Multi-controlled `capply` / toffoli | multi-control | ADR 0046 |
| **SV-25** | Open-controlled `ocapply` | open control | ADR 0047 |
| **SV-26** | Mixed open/filled control `!c` | mixed polarity | ADR 0048 |
| **SV-27** | Fock Q/P quadratures — $H=\frac12(P^2+Q^2)$ | fock HO | ADR 0049 |
| **SV-28** | Sparse Pauli-sum IR multi-qubit evolve | sparse H | ADR 0050 |
| **SV-29** | Position-grid HO — X/P + wavepacket | grid HO | ADR 0051 |
| **SV-30** | Extended static unitarity | apply/map/evolve gates | ADR 0052 |
| **SV-31** | User-module import linker | `compile_path` / import | ADR 0054 |

### 2.1 SV-01 — Lit-Lift

- リテラル `10`, `0.01` は `dirac(...)` / `State<Int|Float>` に昇格する。
- `10 + 20` は `State` 同士の演算であり、ハーネス結果に裸 `int`/`float` を露出しない。
- ノルムは 1.0。

### 2.2 SV-02 — `when` preservation

- `when (coin()) { 0 -> A, else -> B }` は両世界線を保持し、各質量 0.5（または指定質量）の結合状態になる。
- `assertSuperposition` で両アームの基底が残ることを確認する。

### 2.3 SV-03 — Failure as superposition

- ゼロ除算等は例外を投げず、`Result.Success` / `Result.Error` の重ね合わせで完走する。
- 終端まで `assertNormEquals(1.0)`。

### 2.4 SV-04 — Early Collapse

- `main` 途中の `measure` 後に別処理があるソースは `EARLY_COLLAPSE_ERROR` でビルド失敗。

### 2.5 SV-05 — Vacuum & comparison

1. 全棄却 `project` → `assertVacuum`；後続 `map` / `measure` は空結果で安全終了。
2. `state A >= state B` → `State<Boolean>`（`assertTypeIsState<Bool>`）；ノルム 1.0。

### 2.6 SV-06 — Packages & vocabulary

- 異なる `package` の同名 `class` は衝突せず import 可能（部分空間の直積合成の契約）。
- Forbidden（`if`, `null`, `throw`, …）は hard error；Retired（`observe`, `span`, `fn`, `trait`）は Retired 診断。
- Nested `when (s0) { when (s1) … }` → `NESTED_WHEN_ERROR`（ADR **0039**）。

---

## 3. Harness architecture（PoC）

```
tests/spec_verification/
  harness/
    state.py          # Discrete PMF State[T]
    assertions.py     # 5 meta assertions
    compile_gate.py   # Early Collapse / Forbidden / Retired stub
    report.py         # Spec Compliance Rate
  suites/
    sv01_lifting.py
    sv02_when.py
    sv03_failure_superposition.py
    sv04_early_collapse.py
    sv05_vacuum_compare.py
    sv06_package_vocab.py
  fixtures/           # .qpex snippets for compile_gate
  run_all.py          # entrypoint → JSON + Markdown report
```

### 3.1 Discrete MVP model

- `State` = finite support map `value → mass` with `sum(mass) = norm`.
- `dirac(v)` / Lit-Lift: `{v: 1.0}`.
- `vacuum()`: `{}`, norm `0`.
- Ops: `map`, `project`, `when`, arithmetic pushforward, comparison → `State[bool]`.

### 3.2 Compliance Rate

\[
\text{Spec Compliance Rate} = \frac{\#\text{passed}}{\#\text{total}} \times 100\%
\]

ゲート: **100%** でパス。1 件でも失敗すれば CI は非ゼロ終了。

### 3.3 Migration to production compiler

| Assertion | Runtime PoC | Compiler / Kernel (Phase 2.1–2.2) |
|-----------|-------------|------------------------|
| Norm / Superposition / Vacuum | Discrete PMF harness | `compiler/qpex/runtime` Joint + Evaluator |
| `assertTypeIsState` | Python `State` wrapper | `compiler/qpex/typecheck.py` |
| `assertCompileError` | — | Lexer + Parser + Early Collapse |

アサーション **名前とエラーコードは固定**。実装だけ差し替える。

---

## 4. Error codes（canonical）

| Code | Used by |
|------|---------|
| `NORM_MISMATCH` | `assertNormEquals` |
| `SUPERPOSITION_MISMATCH` | `assertSuperposition` |
| `TYPE_NOT_STATE` | `assertTypeIsState` |
| `NOT_VACUUM` | `assertVacuum` |
| `EARLY_COLLAPSE_ERROR` | mid-`measure` |
| `NESTED_WHEN_ERROR` | nested `when` (ADR 0039) |
| `INTERFER_INDEPENDENT_STATE_ERROR` | `interfer` without shared lineage |
| `EXPECT_CLASSICAL_ONLY_ERROR` | mix `expect` scalar into State arith |
| `COIN_IN_EVOLVE_ERROR` | `coin()` inside `evolve` |
| `TOPLEVEL_EXECUTION_ERROR` | executable stmt outside `main` (SV-16 / ADR 0037) |
| `DIMENSION_MISMATCH_ERROR` | dimensional algebra failure (SV-15 / ADR 0037) |
| `FORBIDDEN_KEYWORD` | ADR 0035 Forbidden |
| `RETIRED_KEYWORD` | ADR 0035 Retired |
| `PACKAGE_RESOLVE_ERROR` | import / namespace failure |
| `UNEXPECTED_EXCEPTION` | SV-03 must not throw |

### 4.1 SV-15 — Type-First + dimensions (ADR 0037)

- `Delta<Time> dt = 0.05.s` parses inside `main` and evaluates magnitude `0.05`.
- Dimension-consistent Euler (`x + (dt/m)*p`, …) typechecks.
- `x + dt` (Length + Time) → `DIMENSION_MISMATCH_ERROR`.
- Official `phase_space.qpex` uses Type-First + units.

### 4.2 SV-16 — Structured units (ADR 0037)

- `package` + `pub fn main() -> Unit { … }` runs.
- Bare top-level Type-First / `state` / `measure` → `TOPLEVEL_EXECUTION_ERROR`.
- `import qpex.math.*` parses; `unit.package` / `unit.main` populated.
- Test helper: `harness.as_main(body)` for wrapping suite snippets.

### 4.3 SV-17 — Quantum mechanics surface (ADR 0038)

- Ket literals `|0>`, `|+>`, `|01>`, …
- `evolve psi under X|Y|Z for t` applies $U=e^{-iHt}$ on qubit amplitudes.
- `expect(Z, psi)` returns Dirac `Float` of $\langle Z\rangle$ (no collapse).
- `cnot(ctrl, tgt)` + `expect(ZZ, a, b)` prepare / read $\Phi^+$ correlation
  (not nested `when`).
- Dimension errors prefer `[Length]` / `[Time]` over `[L]` / `[T]`.

### 4.4 SV-31 — User-module import linker (ADR 0054)

- `compile_path` / `run_path` resolve `import` under the entry package directory.
- Type-First `class` fields and library `Operator` / `pub fn` merge into entry.
- `examples/09_complex_simulations/main_quantum_walk.qpex` linked run (50-step DTQW).
- Missing import → `MODULE_NOT_FOUND_ERROR`.

---

## 5. Execution

```bash
# Local default: run suites, print summary, do not write reports/latest.*
python3 tests/spec_verification/run_all.py

# CI / explicit artifact write:
python3 tests/spec_verification/run_all.py --write-report
```

成果物:

- stdout: サマリ（pass/fail + rate）
- with `--write-report`: `tests/spec_verification/reports/latest.json` and
  `latest.md` (avoids ordinary local timestamp-only git drift; LISS-0071 Slice A)

---

## 6. Relation to Kernel PoC fixtures

既存 `tests/fixtures/poc/*.json`（相関自己和・Deferred RNG）は **Kernel PoC track** のまま存続する。本プロトコルは **言語仕様メタ検証 track** であり、アサーション集合が異なる。将来、両 track を同一ランナーに統合してよい。

---

## 7. Language Spec Conformance

規範仕様 [`docs/specs/qpex-language-specification.md`](../specs/qpex-language-specification.md)
の各節は、次の SV スイートで回帰検証する。ドキュメントのみの変更でも
`python3 tests/spec_verification/run_all.py` が **100%** であること。

| Spec § | Topic | Primary suites |
|--------|-------|----------------|
| §1 Introduction | axioms / terminology | SV-01, SV-04 |
| §2 Lexical | tokens / Forbidden / ket | SV-06, SV-17 |
| §3 Syntax | precedence / `main` / evolve | SV-13, SV-16, SV-17 |
| §4 Types / dims | Type-First / $(L,M,T)$ | SV-15 |
| §5 Semantics | Joint / when / phase / expect | SV-02–SV-05, SV-07, SV-14, SV-17 |
| §6 Modules | package / top-level | SV-06, SV-16 |
| §7 Stdlib / runtime | Prelude / Math / `--target` | SV-08–SV-11 |
| Appendix A–C | EBNF / codes / ADR map | (manual + suite codes) |

**Future (non-mandatory for v0.1):** a grammar-snapshot case under
`tests/spec_verification` may pin `qpex.ebnf` against lexer/parser drift.

Error codes in §4 of this protocol MUST stay aligned with Language Spec
Appendix B.

---

## 8. Hold note

ADR 0034 により Kernel PoC / parser / AST / typechecker 向け Hold は解除済み。本ハーネスはその AT-TDD 入口である。IR optimizer・Float Math 本番・QPU は引き続き後段。
