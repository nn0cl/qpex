# Staqex

**Staqex**（スタケックス / *Quantum-Probabilistic Executable*）は、理論物理の計算式を書くように、
量子コンピュータ向けのプログラムを書けることをめざしたプログラミング言語です。

[English README](README.md) · [Quickstart](QUICKSTART.ja.md) ·
[アーキテクチャ](docs/architecture/README.md) ·
[言語仕様](docs/specs/staqex-language-specification.md)

> **旧称は QPex。** 2026-07-29 に商標上の競合を理由として Staqex に改称しました。
> 言語仕様・ADR の内容に変更はありません。改称の詳細は
> [`docs/architecture/README.md`](docs/architecture/README.md#project-rename-history)
> を参照してください。

## ライセンス

**MIT OR Apache-2.0** のデュアルライセンス。
[LICENSE](LICENSE) / [LICENSE-MIT](LICENSE-MIT) / [LICENSE-APACHE](LICENSE-APACHE)。

## 現状（正直な棚卸し）

| 層 | 実態 |
|----|------|
| 協働 / AT-TDD | `llm-project-template` を導入済み（`AGENTS.md`、ADR 0001–0012 など） |
| 規範的な言語面 | `docs/specs/staqex-language-specification.md` と ADR 0013 以降 |
| **今動く Kernel** | **Python** の `compiler/staqex/`（字句〜型検査〜 Joint 評価） |
| 長期ランタイム | まず Rust VM / シミュレータ、QPU は後段のポート |
| 仕様検証 | `python3 tests/spec_verification/run_all.py`（緑を維持） |

受け入れ済み仕様と明示された AT-TDD フェーズなしに、言語挙動を実装しないこと
（`AGENTS.md`）。

## 物理学者向け DX

プログラマ道具は「物理の単位」として見せる（Java 式の儀式は置かない）:

| 構文 | 物理的な読み |
|------|----------------|
| `enum` | 排他的な幾何・基底 |
| `struct` | 不変パラメータの束 |
| `class` + `fun init` | **物理系** / 実験セットアップ（`new` は禁止） |
| `namespace` | 理論のセクター |
| 修飾なし / `pub` / `_` | モジュール内 / 公開 API / クラス私有（`protected` なし） |

詳細: [`docs/architecture/physicist-dx-harmony.md`](docs/architecture/physicist-dx-harmony.md)、
ADR **0054–0056**、**0058**。

## 実行

```bash
python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.sqx --seed 0
python3 -m compiler.staqex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx --seed 0
```

例一覧: [`examples/README.md`](examples/README.md)。

## 検証

```bash
python3 tests/spec_verification/run_all.py
python3 tests/test_modern_oop_and_visibility.py
```

## エージェント入口

1. `AGENTS.md`  
2. `docs/architecture/agent-quickstart.md`  
3. `docs/collaboration/session-start-and-resume.md`  

テンプレート同期は `.collaboration-template-version` を基準に、
`update-ai-collaboration-files.sh` で行う。
**製品 README と言語 ADR はターゲット所有**であり、テンプレの README では
上書きしない。
