# QPex Quickstart（開発者向け）

このリポジトリで人間 / エージェントが作業するための入口です。
**協働テンプレートの導入手順ではありません**
（そちらは `docs/collaboration/adoption-guide.md`）。

[English](QUICKSTART.md) · [README](README.ja.md)

## 0. 前提

- Python 3.11+ 推奨（現行 Kernel は標準ライブラリ中心）
- カレントディレクトリはリポジトリルート

## 1. 公式例を実行する

```bash
python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.qpex --seed 0
python3 -m compiler.staqex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
```

複数ファイルは `import` + パスリンク（ADR **0054**）。
ローカル脚本に `module-info.qpex` は不要（ADR **0058** 改訂）。

## 2. 適合ゲートを緑に保つ

```bash
python3 tests/spec_verification/run_all.py
```

OOP / 可視性:

```bash
python3 tests/test_modern_oop_and_visibility.py
python3 tests/test_enum_support.py
python3 tests/test_encapsulation_and_module_info.py
```

## 3. 最小プログラム

```qpex
package demo
public fun main() {
    state x = dirac(0)
    measure x
}
```

## 4. 物理向けのまとめ方（任意）

`enum` / `struct` / `class` + `fun init` / `pub` / `_`。
`fun` を使う（Retired の `fn` ではない）。`new` と `protected` は禁止。

詳細とサンプルは `QUICKSTART.md` §4、および
`docs/architecture/physicist-dx-harmony.md`。

## 5. 次に読むもの

| 目的 | 文書 |
|------|------|
| エージェント手順 | `AGENTS.md`, `docs/architecture/agent-quickstart.md` |
| 公理 | `docs/architecture/qpex-language-axioms.md` |
| 規範仕様 | `docs/specs/qpex-language-specification.md` |
| 物理 × DX | `docs/architecture/physicist-dx-harmony.md` |
| 例 | `examples/README.md` |
| テンプレ運用 | `docs/collaboration/adoption-guide.md` |
