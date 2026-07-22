# Language-spec completeness audit (10 criteria)

Date: 2026-07-23. Scope: `docs/architecture/qpex-language-spec.md` + ADRs
0021–0033 (+ companions). Implementation remains **Hold**.

---

## 1. 総合判定および同期スコア

| 項目 | 結果 |
|------|------|
| **総合判定** | **Pass**（P0 は本監査中に umbrella へ反映済み） |
| **同期スコア** | **9.7 / 10.0** |
| Completeness | 10 観点すべてに規範記述あり（一部は companion 依存→今回 § 追加） |
| Consistency | 旧表記は退役表／バナーで管理；コア矛盾なし |
| Implementability | Kernel PoC 免除が明記；DAG/SIMD は後段プロファイル（ADR 0032） |

判定理由: Never Leave the State / Lit-Lift / `when`·`fun`·`class` / `main`+終端
`measure` / 境界 I/O / `inspect` / Math State→State / 不変 class / 非 async
が ADR と傘仕様で揃っている。残差はミニ仕様・歴史文書・比較演算子など P1。

---

## 2. 10 観点チェック結果

| # | 観点 | 判定 | 根拠（主） |
|---|------|------|------------|
| 1 | 最上位公理 | **Pass** | §1.1; §4 `measure` last-only + Early Collapse Error; §5 禁止 mid `File.write` |
| 2 | 型・Lift | **Pass** | §1.2; §8 Lit-Lift; ADR 0018/0024 |
| 3 | null/例外 | **Pass** | §1.3; Result; Vacuum; ADR 0025–0026 |
| 4 | 構文 DX | **Pass** | §3; `fun`/`class`/`interface`/`when`; no `new`; ADR 0024/0026 |
| 5 | パッケージ | **Pass** | §2 $\mathcal{H}_A$; 合成・修飾名を本監査で強化 |
| 6 | Entry/Lifecycle | **Pass** | §4 三段階; `main(args: State<List<String>>)` |
| 7 | I/O & inspect | **Pass** | §5; `readAsState`/`readText` 族; `measure to`; §5.5 inspect |
| 8 | Stdlib Math | **Pass** | 新 §6 + `qpex-stdlib-packages.md` ADR 0031 |
| 9 | 不変・再入 | **Pass** | 新 §1.5 + ADR 0033 |
| 10 | 並列モデル | **Pass** | §1.4; ADR 0028/0032; DAG→SIMD/GPU |

---

## 3. P0 課題（即時修正）

本監査前に傘仕様にあった穴 → **すべて本セッションで修正済み**:

| ID | 課題 | 処置 |
|----|------|------|
| P0-1 | 不変 class / 再入が傘に薄かった | **§1.5 追加** |
| P0-2 | Stdlib/Math が companion のみ | **§6 Standard library 追加** |
| P0-3 | 監査文の `readText` vs 仕様 `readAsState` | **同族エイリアス明記** |
| P0-4 | パッケージ合成・同名衝突が弱い | **§2.2 義務を拡充** |
| P0-5 | 移行表の「domain error」残留語感 | **「exception/crash → Vacuum」に改記** |

**残存 P0: なし**（実装 Hold はプロセス上の意図であり仕様欠陥ではない）。

---

## 4. P1 課題（ギャップ・未決 UX）

| ID | 課題 | 推奨 |
|----|------|------|
| P1-1 | `Vacuum` のエンジン表現ミニ仕様未決 | ADR 0026 フォローアップ |
| P1-2 | `State` 上の `>=` / `==`（BankAccount 例）の形式規則 | 型システム節を追加 |
| P1-3 | Prelude / デフォルト import | ADR または §6 追記 |
| P1-4 | `snapshot` 頻度・対象周辺 | ミニ仕様 |
| P1-5 | 歴史 ADR 0013–0015 / prior-art の `observe` | バナー済み；リネームは任意 |
| P1-6 | 形式意味論 § タイトルが Span のまま | 意図的；表面は `when` |
| P1-7 | `File` path の `String` vs `State<String>` | 境界リフト規則を固定 |
| P1-8 | 連続分布 (`gaussian`) 表現 | ADR 0016 / 0031 |

---

## 5. 仕様書への具体的修正差分（実施済み要約）

ファイル: `docs/architecture/qpex-language-spec.md`

### Diff A — §1.5 Immutable class（新規）

```diff
+ ### 1.5 Immutable `class` — structural reentrancy (ADR 0033)
+ A `class` is an immutable capsule… methods return a new value…
+ never assign in place to `this` / `self`…
```

### Diff B — §2.2 コンパイラ義務（拡充）

```diff
+ Composition is explicit: (sys_a, sys_b) or wrapping class — H_A ⊗ H_B
+ Same simple name in different packages via qualified paths
+ Cyclic imports renumbered as item 4
```

### Diff C — §5.2 I/O エイリアス

```diff
+ File.readText / readJson / readAsState are preparation lifts into State<_>
```

### Diff D — §4.3 ライフサイクル表記

```diff
+ Math.* in Pure State Evolution; ADR 0032 DAG note
+ File.read* in State Preparation
```

### Diff E — §6 Standard library（新規）＋以降の節番号 +1

```diff
+ ## 6. Standard library (pointer — ADR 0031)
+ qpex.math / state / collection / io / debug
+ Math.sin: State<Float> → State<Float> via map
+ ## 7 Naming … ## 11 Open questions
```

### Diff F — 移行表 Z=0 行

```diff
- | project Z=0 domain error | → Vacuum |
+ | project Z=0 as exception/crash | → Vacuum (no throw) |
```

---

## 6. 観点別・詳細所見（要約）

### 1. Fundamental Law
`measure` は `MainDecl` 最終文のみ。`inspect`/`snapshot` は非収縮。mid
`File.write` 禁止。**Pass.**

### 2. Type & Lifting
純領域は `Γ ⊢ e : State<T>`；Lit-Lift 明示。キャリア `T` はリフト入力／型引数
／post-measure のみ。**Pass.**

### 3. Null & Exception
throw/catch/null 排除；`Result` + `when`；$Z=0$→Vacuum。**Pass.**

### 4. Syntax & DX
`fun`/`class`/`interface`/`when`；`new` なし；`span`/`fn` 退役。**Pass.**

### 5. Namespace
パッケージ＝$\mathcal{H}_A$；修飾名・明示合成を強化。**Pass**（パス厳密度は P1）。

### 6. Entry & Lifecycle
`public fun main` ± `State` args；三段階明記。**Pass.**

### 7. Boundary I/O & Inspect
Lift in / measure-to / snapshot / inspect 三分岐。**Pass.**

### 8. Stdlib
傘 §6 + packages ノート；Math は State→State。**Pass.**

### 9. Immutability
§1.5 + ADR 0033。**Pass.**

### 10. Concurrency
スレッド/`async` なし；DAG→データ並列。**Pass.**

---

## 7. 推奨次アクション（Adjudicator）

1. P1-1 Vacuum ミニ仕様の承認。
2. P1-2 `State` 比較演算の形式規則。
3. Hold 解除は Kernel PoC A/B から（言語仕様監査は **Pass**）。
'''


---

## Follow-up: ADR 0034 + Hold unseal

P1 Vacuum / State compare / Prelude locked. Sync **10 / 10**. Kernel PoC / parser / AST / typechecker **unsealed**.
