# QPex 設計思想（Design Philosophy）

| Field | Value |
|-------|-------|
| Status | **Accepted archive**（設計者意図の定着） |
| Source | Gemini 対話エクスポート「確率的プログラミング言語の名前提案」 |
| 原本 | `~/Downloads/確率的プログラミング言語の名前提案.docx`（2026-07-22 頃） |
| Companions | [`qpex-positioning.md`](qpex-positioning.md)、[`qpex-language-axioms.md`](qpex-language-axioms.md)、規範仕様 [`../specs/qpex-language-specification.md`](../specs/qpex-language-specification.md) |

本文は対話ログの全文転載ではない。**設計者が繰り返し立てた公理・語感・拒否事項**を、実装・ADR と照合できる形に圧縮したものである。歴史的表面語（例: `span`）は現行語（`when`）への注記付きで残す。

---

## 0. 一節で言うと

> **理論物理の研究者が、論文の数式（Dirac・密度行列・制御ユニタリ・次元解析）を片手にコードを開き、脳内ナラティブとノイズなく 1:1 対応できる言語であること。**

これが文法・キーワード・型・静的検査の**最上位目的（Design Goal）**である。  
「古典ホストに量子島を挿す」でも「動く PMF ライブラリ」でもない。

---

## 1. 最高公理（Philosophy）

### 1.1 数式 ↔ コードの直体感

- コードを見た瞬間に、対応する Hilbert / 確率空間上の操作が確信できる。
- キーワード選定は「プログラマの慣習」より**物理の術語**を優先する（後に Kotlin DX と両立させた経緯は §4）。

### 1.2 Never Leave the State（Wedge）

- 実行中は joint / 振幅の中に留まる。古典スカラーは**端末 `measure` まで**出てこない。
- 途中の `if` / `return` / `break` / mid-`measure` は「世界線ジャンプ＝Early Collapse」として拒否する。

### 1.3 物理学者の標準ナラティブ（処理の順序）

論文・黒板での思考順そのものがプログラム構造になる:

| 段階 | 物理 | 表面（現行） | 歴史メモ |
|------|------|--------------|----------|
| 準備 | State preparation $\|\\psi\\rangle$ | `state` / `dirac` / `\|0>` / `coin` | — |
| 重ね合わせ | Controlled span / mixture | `when (c) { … }` | 初期案 `span` → ADR 0024 で `when` |
| 時間発展 | $U=e^{-iHt}$ / pushforward | `evolve` / `evolve under H for t` | — |
| 干渉 | Path interference | `interfer` / `phase` | — |
| 射影・縮約 | Projection / collapse | `project` / 端末 `measure` | `observe` は Retired |
| 非破壊読取 | $\\langle O\\rangle$ | `expect` / `inspect` | — |

---

## 2. ブロック・制御の物理モデル

### 2.1 `evolve` は純粋な状態変換

- 古典 `for`/`while`（命令アドレスのループ）ではない。
- ブロック内の各行は **Joint 上の pushforward**。途中で RNG・collapse を起こさない。
- **式指向**: `return` 文は無い。ブロック最終式が結果。複数軸は **タプル** `(a, b)` で外へ出す。
- 破壊的上書きより **immutable な遷移**（`let z1 = z + …`）を本義とする。

### 2.2 `when` は場合分けジャンプではない

- 古典 `if`（片方破棄）ではなく、制御状態による**重ね合わせ／線形結合**。
- 語感議論の着地: 初期 `span`（空間生成の名詞）から、条件付き状態準備の**動詞的語感**として `when` を採用（ADR 0024）。物理の「基底展開」に合わせる意図は不変。

### 2.3 禁止される古典制御

設計対話で明示的に「言語に無い／あってはならない」とされたもの:

- `if` / `switch` / `while` / `break` / `return`
- `null` / 例外 throw-catch
- オブジェクト言語のスレッド / `async`/`await`（並行は superposition / DAG 側）
- 自由な mid-circuit 古典分岐（QASM/QIR と同様、測定後の古典ビットなしに分岐しない）

後続の厳格化: **ネスト `when`** は暗黙デコヒーレンスに見えるため `NESTED_WHEN_ERROR`（ADR 0039）。

---

## 3. 型と次元 — 「量」が先、「変数」が後

### 3.1 Type-First

物理学者の頭: 「まず $\\Delta t$ という量があり、それを `dt` と名付ける」。  
プログラマ慣習の `val dt: Delta<Time> = …`（先に val、後から型注釈）は**語感として許せない**、というのが設計者の明確な拒否。

正しい向き:

```qpex
Delta<Time> dt = 0.05.s
Mass m = 1.0.kg
State<Length> x = …
```

### 3.2 次元代数であってクラス階層ではない

- 表面は `+ - * /` のまま（`.add()` / Java 風 Unit オブジェクトは不要）。
- 内部は $\\mathbf{d}=(L,M,T)$ の乗除推論。
- エラーは OOP cast ではなく **physically incompatible** の言葉で。

### 3.3 コンパイラは物理公理の番人

「文法的に動くから OK」は基準にしない。  
ユニタリ性・明示測定・次元保存・テンソル／干渉の誠実さに反する構文は、**静的に弾いて初めて仕様**である（設計対話終盤の監査方針と一致）。

---

## 4. DX との両立（Kotlin 風表面）

Java/Rust 的な `package` / `fn` / `class` / `pub fn main` は「物理を捨てた」のではなく:

- **系（System）** を名前空間で衝突なく書くための工学的必然
- `fn` / `class` は論文の「系の定義」に対応する語感として再解釈
- `new` / `null` / 例外は採用しない

物理語感が一次、現代プログラマの読み書き負荷低減が二次。衝突時は物理側を勝たせる。

---

## 5. ホスト境界と観測の区別

| 操作 | 意味 | 崩壊 |
|------|------|------|
| `inspect` / `snapshot` | ホスト向けデバッグ・ログ | しない |
| `expect` | $\\langle O\\rangle$（古典スカラー抽出） | しない（結果を量子座標に戻さない） |
| `project` | 明示的縮約／部分空間 | 質量を落とし得る |
| `measure` | 端末の射影測定 | する（`main` 最終） |

ファイル I/O 等の OS API は境界アダプタに閉じ、世界線中の自由副作用にしない。

---

## 6. マインドモデル直撃の表面（実装優先度として語られたもの）

設計者が「動くが式が見えない」と sorったギャップと、その後の着地:

1. `evolve` + タプル bind + 相関演算（相空間写像が一行で見える）
2. 複素振幅 + `phase` / `interfer`（量子サンプルが確率物語で止まらない）
3. ケット `\|…>` / `evolve under H` / `expect`（論文記法そのもの）
4. Type-First + 次元代数 + 構造化 `main`
5. 物理公理の静的検査（ネスト `when` 禁止など）— 継続課題あり

---

## 7. 意図的に捨てたもの（非目標の要約）

- 古典スカラーを作業メモリにする言語
- PPL の `observe`＝条件付き推論ホストモデル（命名衝突を避け `measure` に固定）
- 「量子の皮をかぶった `if`/`when` ネスト」で Bell / ウォーク / ゲージを自称すること
- 次元を無視した数値遊び、H-evolve に Length を渡すこと、独立状態の偽 `interfer`

---

## 8. 現行リポジトリとの対応

| 思想 | 文書 / 実装 |
|------|-------------|
| Never Leave the State | axioms / positioning / ADR 0013–0018 |
| `when` / `evolve` / `measure` | ADR 0024, 0027, 0038 |
| Type-First・次元 | ADR 0037, `qpex-dimensional-types.md` |
| ネスト `when` 禁止 | ADR 0039 |
| 規範再実装仕様 | `docs/specs/qpex-language-specification.md` |
| 検証 | `docs/testing/qpex-spec-verification-protocol.md` |

---

## 9. 原本について

- 原本 DOCX は Gemini 対話の長尺ログ（プロンプト約 85 往復）であり、途中の仮説・旧キーワード（`span`）・実装ログが混在する。
- **規範の単一ソースは本ファイル＋ ADR／Language Spec**。原本は設計意図の考古学的ソースとして手元に保持すれば足りる（リポジトリにバイナリ全文は置かない）。

Document history: 2026-07-23 — DOCX から設計思想を抽出・定着。
