# Package root naming (official samples)

| Field | Value |
|---|---|
| Status | **Accepted with WP-0089 plan** (2026-08-03) — policy for official examples |
| Program | [WP-0089](documentation-compression-map.md) / [LISS-0279](documentation-compression-map.md) |
| Parents | [surface modernization north star](surface-modernization-north-star.md); ADR 0054 modules |

## Policy

| Context | Package root |
|---|---|
| **Single-file notebook / basics** | Prefer **no package** + `// staqex-profile: experiment` (default teaching face) |
| **Official multi-file samples** | Short root: **`examples.…`** (e.g. `examples.showcase.s01_disaster`) |
| **External / user libraries** | Any legal package path; reverse-DNS remains **valid** Kernel surface |

## Rationale

`com.staqex.examples…` is JVM reverse-DNS ceremony without a physics reading.
Short `examples.…` keeps multi-file modules honest while cutting enterprise feel.

**Do not** use `staqex.examples…` as the sample root: the `staqex.*` prefix is
reserved for **stdlib / Kernel prelude** paths (e.g. `import staqex.math.*`).
Colliding sample packages with that prefix breaks resolution.

## Non-goals

- Deleting the package system
- Forcing experiment profile on multi-file graphs
- Breaking third-party packages that use `com.*`

## Migration (LISS-0279)

Official tree under `examples/` and related fixtures use `examples.…` after
2026-08-03. Older `com.staqex.examples…` sources still compile if present
outside the official tree.
