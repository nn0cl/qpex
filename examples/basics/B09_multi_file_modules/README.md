# B09 — Multi-file modules

Teaches ADR 0054 `import` linking with `domain/` and `operators/` layout.

**Honesty (WP-0089):** multi-file **requires** packages. That is not the default
notebook face — single-file basics use `// staqex-profile: experiment` without
package ceremony. Package root for official samples is short `examples.…`
(not reverse-DNS `com.staqex…`); see
[package-root-naming](../../../docs/architecture/package-root-naming.md).

Legacy source: `examples/09_complex_simulations/`.

```bash
python3 -m compiler.staqex run examples/basics/B09_multi_file_modules/main_multi_file_modules.sqx --seed 0
```
