# QPex Spec Verification Protocol（仕様検証メタテスト仕様書）

| Field | Value |
|-------|-------|
| Status | Active (AT-TDD / Kernel PoC harness) |
| Spec spine | `docs/architecture/qpex-language-spec.md`, ADR 0021–0035 |
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
| **代表コード** | `EARLY_COLLAPSE_ERROR`, `FORBIDDEN_KEYWORD`, `RETIRED_KEYWORD` |
| **公理** | ADR 0027（端末 `measure` のみ）、ADR 0035（Forbidden / Retired） |

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

## 2. Mandatory Categories（6 suites）

| ID | Suite | Primary assertions | ADR / Spec |
|----|-------|-------------------|------------|
| **SV-01** | Lit-Lift / スカラー全廃 | `assertTypeIsState`, `assertNormEquals` | §2 Lit-Lift |
| **SV-02** | `when` 非破壊保存 | `assertSuperposition`, `assertNormEquals` | ADR 0024 |
| **SV-03** | 失敗の重ね合わせ | `assertSuperposition`, `assertNormEquals` | ADR 0025–0026 |
| **SV-04** | Early Collapse 非許容 | `assertCompileError(..., EARLY_COLLAPSE_ERROR)` | ADR 0027 |
| **SV-05** | Vacuum + 比較 → `State<Bool>` | `assertVacuum`, `assertTypeIsState<Bool>` | ADR 0034 |
| **SV-06** | Package + Forbidden/Retired | `assertCompileError`, namespace resolve | ADR 0024/0035 |
| **SV-07** | Kernel eval (`when`/`map`/`project`/`interfer`/`measure`) | `assertSuperposition`, vacuum measure | Phase 2.2 / PoC A |
| **SV-08** | Prelude / Math / CLI / inspect / DAG IR | ecosystem checks | Phase 3 / ADR 0031–0032 |

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
| `FORBIDDEN_KEYWORD` | ADR 0035 Forbidden |
| `RETIRED_KEYWORD` | ADR 0035 Retired |
| `PACKAGE_RESOLVE_ERROR` | import / namespace failure |
| `UNEXPECTED_EXCEPTION` | SV-03 must not throw |

---

## 5. Execution

```bash
python3 tests/spec_verification/run_all.py
```

成果物:

- stdout: サマリ（pass/fail + rate）
- `tests/spec_verification/reports/latest.json`
- `tests/spec_verification/reports/latest.md`

---

## 6. Relation to Kernel PoC fixtures

既存 `tests/fixtures/poc/*.json`（相関自己和・Deferred RNG）は **Kernel PoC track** のまま存続する。本プロトコルは **言語仕様メタ検証 track** であり、アサーション集合が異なる。将来、両 track を同一ランナーに統合してよい。

---

## 7. Hold note

ADR 0034 により Kernel PoC / parser / AST / typechecker 向け Hold は解除済み。本ハーネスはその AT-TDD 入口である。IR optimizer・Float Math 本番・QPU は引き続き後段。
